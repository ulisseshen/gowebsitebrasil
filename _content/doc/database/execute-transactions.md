<!--{
  "Title": "Executing transactions",
  "ia-translated": true
}-->

Você pode executar transações de banco de dados usando um
[`sql.Tx,`](https://pkg.go.dev/database/sql#Tx) que representa uma transação.
Além dos métodos `Commit` e `Rollback` representando semântica específica de transação,
`sql.Tx` tem todos os métodos que você usa para executar operações comuns de banco de
dados. Para obter o `sql.Tx`, você chama `DB.Begin` ou `DB.BeginTx`.

Uma [transação de banco de dados](https://en.wikipedia.org/wiki/Database_transaction)
agrupa múltiplas operações como parte de um objetivo maior. Todas as operações devem
ter sucesso ou nenhuma pode, com a integridade dos dados preservada em qualquer caso.
Tipicamente, um workflow de transação inclui:

1. Iniciar a transação.
2. Executar um conjunto de operações de banco de dados.
3. Se nenhum erro ocorrer, fazer commit da transação para fazer mudanças no banco de dados.
4. Se um erro ocorrer, fazer rollback da transação para deixar o banco de dados
    inalterado.

O package `sql` fornece métodos para iniciar e concluir uma transação,
bem como métodos para executar as operações de banco de dados intermediárias. Esses
métodos correspondem aos quatro passos no workflow acima.

*   Iniciar uma transação.

    [`DB.Begin`](https://pkg.go.dev/database/sql#DB.Begin) ou
    [`DB.BeginTx`](https://pkg.go.dev/database/sql#DB.BeginTx) iniciam uma nova
    transação de banco de dados, retornando um `sql.Tx` que a representa.
*   Executar operações de banco de dados.

    Usando um `sql.Tx`, você pode fazer query ou atualizar o banco de dados em uma série de
    operações que usam uma única conexão. Para suportar isso, `Tx` exporta os
    seguintes métodos:

    *   [`Exec`](https://pkg.go.dev/database/sql#Tx.Exec) e
        [`ExecContext`](https://pkg.go.dev/database/sql#Tx.ExecContext) para fazer
        mudanças no banco de dados através de statements SQL como `INSERT`, `UPDATE`, e
        `DELETE`.

        Para mais, consulte [Executing SQL statements that don't return data](/doc/database/change-data).

    *   [`Query`](https://pkg.go.dev/database/sql#Tx.Query),
        [`QueryContext`](https://pkg.go.dev/database/sql#Tx.QueryContext),
        [`QueryRow`](https://pkg.go.dev/database/sql#Tx.QueryRow), e
        [`QueryRowContext`](https://pkg.go.dev/database/sql#Tx.QueryRowContext)
        para operações que retornam linhas.

        Para mais, consulte [Querying for data](/doc/database/querying).

    *   [`Prepare`](https://pkg.go.dev/database/sql#Tx.Prepare),
        [`PrepareContext`](https://pkg.go.dev/database/sql#Tx.PrepareContext),
        [`Stmt`](https://pkg.go.dev/database/sql#Tx.Stmt), e
        [`StmtContext`](https://pkg.go.dev/database/sql#Tx.StmtContext) para
        pré-definir prepared statements.

        Para mais, consulte [Using prepared statements](/doc/database/prepared-statements).

*   Finalizar a transação com _um_ dos seguintes:
    *   Fazer commit da transação usando
        [`Tx.Commit`](https://pkg.go.dev/database/sql#Tx.Commit).

        Se `Commit` tiver sucesso (retornar um erro `nil`), então todos os resultados de query
        são confirmados como válidos e todas as atualizações executadas são aplicadas ao
        banco de dados como uma única mudança atômica. Se `Commit` falhar, então todos os
        resultados de `Query` e `Exec` no `Tx` devem ser descartados como
        inválidos.
    *   Fazer rollback da transação usando
        [`Tx.Rollback`](https://pkg.go.dev/database/sql#Tx.Rollback).

        Mesmo se `Tx.Rollback` falhar, a transação não será mais válida,
        nem terá sido commitada no banco de dados.

### Melhores práticas {#best_practices}

Siga as melhores práticas abaixo para navegar melhor pelas semânticas complicadas
e gerenciamento de conexão que transações às vezes requerem.

*   Use as APIs descritas nesta seção para gerenciar transações. _Não_
    use statements SQL relacionados a transação como `BEGIN` e `COMMIT`
    diretamente—fazer isso pode deixar seu banco de dados em um estado imprevisível,
    especialmente em programas concorrentes.
*   Ao usar uma transação, tome cuidado para não chamar os métodos
    `sql.DB` não-transacionais diretamente também, pois esses executarão fora da
    transação, dando ao seu código uma visão inconsistente do estado do
    banco de dados ou mesmo causando deadlocks.

### Exemplo {#example}

O código no exemplo a seguir usa uma transação para criar um novo pedido de cliente
para um álbum. Ao longo do caminho, o código irá:

1. Iniciar uma transação.
2. Adiar o rollback da transação. Se a transação tiver sucesso, ela será
    commitada antes da função sair, tornando a chamada de rollback adiada uma
    no-op. Se a transação falhar não será commitada, significando que o
    rollback será chamado conforme a função sai.
3. Confirmar que há inventory suficiente para o álbum que o cliente está
    pedindo.
4. Se houver o suficiente, atualizar a contagem de inventory, reduzindo-a pelo número
    de álbuns pedidos.
5. Criar um novo pedido e recuperar o ID gerado do novo pedido para o cliente.
6. Fazer commit da transação e retornar o ID.

Este exemplo usa métodos `Tx` que recebem um argumento `context.Context`. Isso
torna possível que a execução da função – incluindo operações de banco de dados
-- seja cancelada se executar por muito tempo ou a conexão do cliente fechar. Para
mais, consulte [Canceling in-progress operations](/doc/database/cancel-operations).

```
// CreateOrder creates an order for an album and returns the new order ID.
func CreateOrder(ctx context.Context, albumID, quantity, custID int) (orderID int64, err error) {

	// Create a helper function for preparing failure results.
	fail := func(err error) (int64, error) {
		return 0, fmt.Errorf("CreateOrder: %v", err)
	}

	// Get a Tx for making transaction requests.
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fail(err)
	}
	// Defer a rollback in case anything fails.
	defer tx.Rollback()

	// Confirm that album inventory is enough for the order.
	var enough bool
	if err = tx.QueryRowContext(ctx, "SELECT (quantity >= ?) from album where id = ?",
		quantity, albumID).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return fail(fmt.Errorf("no such album"))
		}
		return fail(err)
	}
	if !enough {
		return fail(fmt.Errorf("not enough inventory"))
	}

	// Update the album inventory to remove the quantity in the order.
	_, err = tx.ExecContext(ctx, "UPDATE album SET quantity = quantity - ? WHERE id = ?",
		quantity, albumID)
	if err != nil {
		return fail(err)
	}

	// Create a new row in the album_order table.
	result, err := tx.ExecContext(ctx, "INSERT INTO album_order (album_id, cust_id, quantity, date) VALUES (?, ?, ?, ?)",
		albumID, custID, quantity, time.Now())
	if err != nil {
		return fail(err)
	}
	// Get the ID of the order item just created.
	orderID, err = result.LastInsertId()
	if err != nil {
		return fail(err)
	}

	// Commit the transaction.
	if err = tx.Commit(); err != nil {
		return fail(err)
	}

	// Return the order ID.
	return orderID, nil
}
```

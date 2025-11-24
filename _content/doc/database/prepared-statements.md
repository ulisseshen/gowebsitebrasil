<!--{
  "Title": "Using prepared statements",
  "ia-translated": true
}-->

Você pode definir um prepared statement para uso repetido. Isso pode ajudar seu código
a executar um pouco mais rápido evitando a sobrecarga de recriar o statement cada
vez que seu código executa a operação de banco de dados.

**Nota:** Placeholders de parâmetro em prepared statements variam dependendo
do DBMS e driver que você está usando. Por exemplo, o
[driver pq](https://pkg.go.dev/github.com/lib/pq) para Postgres requer um
placeholder como `$1` em vez de `?`.

### O que é um prepared statement? {#what_prepared_statement}

Um prepared statement é SQL que é parseado e salvo pelo DBMS, tipicamente
contendo placeholders mas sem valores de parâmetro reais. Posteriormente, o
statement pode ser executado com um conjunto de valores de parâmetro.

### Como você usa prepared statements {#use_prepared_statement}

Quando você espera executar o mesmo SQL repetidamente, você pode usar um `sql.Stmt`
para preparar o statement SQL com antecedência, depois executá-lo conforme necessário.

O exemplo a seguir cria um prepared statement que seleciona um álbum específico
do banco de dados. [`DB.Prepare`](https://pkg.go.dev/database/sql#DB.Prepare)
retorna um [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt) representando um
prepared statement para um dado texto SQL. Você pode passar os parâmetros para o
statement SQL para `Stmt.Exec`, `Stmt.QueryRow`, ou `Stmt.Query` para executar o
statement.

```
// AlbumByID retrieves the specified album.
func AlbumByID(id int) (Album, error) {
	// Define a prepared statement. You'd typically define the statement
	// elsewhere and save it for use in functions such as this one.
	stmt, err := db.Prepare("SELECT * FROM album WHERE id = ?")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	var album Album

	// Execute the prepared statement, passing in an id value for the
	// parameter whose placeholder is ?
	err := stmt.QueryRow(id).Scan(&album.ID, &album.Title, &album.Artist, &album.Price, &album.Quantity)
	if err != nil {
		if err == sql.ErrNoRows {
			// Handle the case of no rows returned.
		}
		return album, err
	}
	return album, nil
}
```

### Comportamento de prepared statement {#behavior}

Um [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt) preparado fornece os
métodos usuais `Exec`, `QueryRow`, e `Query` para invocar o statement. Para
mais sobre usar esses métodos, consulte [Querying for data](/doc/database/querying)
e [Executing SQL statements that don't return data](/doc/database/change-data).

No entanto, como um `sql.Stmt` já representa um statement SQL predefinido, seus
métodos `Exec`, `QueryRow`, e `Query` recebem apenas os valores de parâmetro SQL
correspondentes aos placeholders, omitindo o texto SQL.

Você pode definir um novo `sql.Stmt` de diferentes maneiras, dependendo de como você
usará.

*   `DB.Prepare` e `DB.PrepareContext` criam um prepared statement que pode
    ser executado isoladamente, por si só fora de uma transação, assim como
    `DB.Exec` e `DB.Query` são.
*   `Tx.Prepare`, `Tx.PrepareContext`, `Tx.Stmt`, e `Tx.StmtContext` criam
    um prepared statement para uso em uma transação específica. `Prepare` e
    `PrepareContext` usam texto SQL para definir o statement. `Stmt` e
    `StmtContext` usam o resultado de `DB.Prepare` ou `DB.PrepareContext`. Ou seja,
    eles convertem um `sql.Stmt` não-para-transações em um
    `sql.Stmt` para-esta-transação.
*   `Conn.PrepareContext` cria um prepared statement de um `sql.Conn`,
    que representa uma conexão reservada.

Certifique-se de que `stmt.Close` seja chamado quando seu código terminar com um
statement. Isso liberará quaisquer recursos de banco de dados (como conexões subjacentes)
que podem estar associados a ele. Para statements que são apenas
variáveis locais em uma função, é suficiente usar `defer stmt.Close()`.

#### Funções para criar um prepared statement {#prepared_statement_functions}

<table id="prepared-statement-functions-list" class="DocTable">
    <thead>
        <tr class="DocTable-head">
            <th class="DocTable-cell" width="20%">Function</th>
            <th class="DocTable-cell">Description</th>
        </tr>
    </thead>
    <tbody>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#DB.Prepare">DB.Prepare</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#DB.PrepareContext">DB.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">Preparar um statement para execução
                isoladamente ou que será convertido em um prepared statement
                'em-transação' usando Tx.Stmt.</td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Tx.Prepare">Tx.Prepare</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.PrepareContext">Tx.PrepareContext</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.Stmt">Tx.Stmt</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.StmtContext">Tx.StmtContext</a></code>
            </td>
            <td class="DocTable-cell">Preparar um statement para uso em uma
                transação específica. Para mais, consulte
                <a href="/doc/database/execute-transactions">Executing
                transactions</a>.
            </td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Conn.PrepareContext">Conn.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">Para uso com conexões reservadas.
                Para mais, consulte
                <a href="/doc/database/manage-connections">Managing connections</a>.
            </td>
        </tr>
    </tbody>
</table>

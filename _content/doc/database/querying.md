<!--{
  "Title": "Querying for data",
  "ia-translated": true
}-->

Ao executar um statement SQL que retorna dados, use um dos métodos `Query`
fornecidos no package `database/sql`. Cada um deles retorna um `Row`
ou `Rows` cujos dados você pode copiar para variáveis usando o método `Scan`.
Você usaria esses métodos para, por exemplo, executar statements `SELECT`.

Ao executar um statement que não retorna dados, você pode usar um método `Exec` ou
`ExecContext` em vez disso. Para mais, consulte
[Executing statements that don't return data](/doc/database/change-data).

O package `database/sql` fornece duas maneiras de executar uma query para resultados.

*   **Querying para uma única linha** – `QueryRow` retorna no máximo um único `Row`
    do banco de dados. Para mais, consulte [Querying for a single row](#single_row).
*   **Querying para múltiplas linhas** – `Query` retorna todas as linhas correspondentes como um
    struct `Rows` que seu código pode percorrer. Para mais, consulte
    [Querying for multiple rows](#multiple_rows).

Se seu código executará o mesmo statement SQL repetidamente, considere
usar um prepared statement. Para mais, consulte
[Using prepared statements](/doc/database/prepared-statements).

**Cuidado:** Não use funções de formatação de string como `fmt.Sprintf` para
montar um statement SQL! Você poderia introduzir um risco de SQL injection. Para mais,
consulte [Avoiding SQL injection risk](/doc/database/sql-injection).

### Querying para uma única linha {#single_row}

`QueryRow` recupera no máximo uma única linha de banco de dados, como quando você quer
procurar dados por um ID único. Se múltiplas linhas forem retornadas pela query, o
método `Scan` descarta todas exceto a primeira.

`QueryRowContext` funciona como `QueryRow` mas com um argumento `context.Context`.
Para mais, consulte [Canceling in-progress operations](/doc/database/cancel-operations).

O exemplo a seguir usa uma query para descobrir se há inventory suficiente para
suportar uma compra. O statement SQL retorna `true` se houver o suficiente, `false`
caso contrário. [`Row.Scan`](https://pkg.go.dev/database/sql#Row.Scan) copia o
valor boolean retornado para a variável `enough` através de um ponteiro.

```
func canPurchase(id int, quantity int) (bool, error) {
	var enough bool
	// Query for a value based on a single row.
	if err := db.QueryRow("SELECT (quantity >= ?) from album where id = ?",
		quantity, id).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return false, fmt.Errorf("canPurchase %d: unknown album", id)
		}
		return false, fmt.Errorf("canPurchase %d: %v", id, err)
	}
	return enough, nil
}
```

**Nota:** Placeholders de parâmetro em prepared statements variam dependendo do
DBMS e driver que você está usando. Por exemplo, o
[driver pq](https://pkg.go.dev/github.com/lib/pq) para Postgres requer um
placeholder como `$1` em vez de `?`.

#### Tratando erros {#single_row_errors}

`QueryRow` em si não retorna erro. Em vez disso, `Scan` reporta qualquer erro da
busca e scan combinados. Ele retorna
[`sql.ErrNoRows`](https://pkg.go.dev/database/sql#ErrNoRows) quando a query
não encontra linhas.

#### Funções para retornar uma única linha {#single_row_functions}

<table id="single-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">Function</th>
      <th class="DocTable-cell">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRow">DB.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRowContext">DB.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query de linha única isoladamente.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRow">Tx.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRowContext">Tx.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query de linha única dentro de uma transação maior. Para mais, consulte
        <a href="/doc/database/execute-transactions">Executing transactions</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRow">Stmt.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRowContext">Stmt.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query de linha única usando um statement já preparado. Para mais,
        consulte <a href="/doc/database/prepared-statements">Using prepared statements</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
        <td class="DocTable-cell">
  <code><a href="https://pkg.go.dev/database/sql#Conn.QueryRowContext">Conn.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">Para uso com conexões reservadas. Para mais, consulte
        <a href="/doc/database/manage-connections">Managing connections</a>.
      </td>
    </tr>
  </tbody>
</table>

### Querying para múltiplas linhas {#multiple_rows}

Você pode fazer query para múltiplas linhas usando `Query` ou `QueryContext`, que retornam
um `Rows` representando os resultados da query. Seu código itera sobre as linhas retornadas
usando [`Rows.Next`](https://pkg.go.dev/database/sql#Rows.Next). Cada
iteração chama `Scan` para copiar valores de coluna em variáveis.

`QueryContext` funciona como `Query` mas com um argumento `context.Context`. Para
mais, consulte [Canceling in-progress operations](/doc/database/cancel-operations).

O exemplo a seguir executa uma query para retornar os álbuns de um artista especificado.
Os álbuns são retornados em um `sql.Rows`. O código usa
[`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) para copiar valores de coluna
em variáveis representadas por ponteiros.

```
func albumsByArtist(artist string) ([]Album, error) {
	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", artist)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// An album slice to hold data from returned rows.
	var albums []Album

	// Loop through rows, using Scan to assign column data to struct fields.
	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist,
			&alb.Price, &alb.Quantity); err != nil {
			return albums, err
		}
		albums = append(albums, alb)
	}
	if err = rows.Err(); err != nil {
		return albums, err
	}
	return albums, nil
}
```

Observe a chamada adiada para [`rows.Close`](https://pkg.go.dev/database/sql#Rows.Close).
Isso libera quaisquer recursos mantidos pelas linhas não importa como a função
retorna. Percorrer todas as linhas também o fecha implicitamente,
mas é melhor usar `defer` para garantir que `rows` seja fechado não importa o que aconteça.

**Nota:** Placeholders de parâmetro em prepared statements variam dependendo
do DBMS e driver que você está usando. Por exemplo, o
[driver pq](https://pkg.go.dev/github.com/lib/pq) para Postgres requer um
placeholder como `$1` em vez de `?`.

#### Tratando erros {#multiple_rows_errors}

Certifique-se de verificar por um erro de `sql.Rows` após percorrer os resultados da query.
Se a query falhar, é assim que seu código descobre.

#### Funções para retornar múltiplas linhas {#multiple_rows_functions}

<table id="multiple-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">Function</th>
      <th class="DocTable-cell">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.Query">DB.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryContext">DB.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query isoladamente.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Query">Tx.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryContext">Tx.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query dentro de uma transação maior. Para mais, consulte
        <a href="/doc/database/execute-transactions">Executing transactions</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Query">Stmt.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryContext">Stmt.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">Executar uma query usando um statement já preparado. Para mais, consulte
        <a href="/doc/database/prepared-statements">Using prepared
          statements</a>.
    </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.QueryContext">Conn.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">Para uso com conexões reservadas. Para mais, consulte
        <a href="/doc/database/manage-connections">Managing connections</a>.
      </td>
    </tr>
  </tbody>
</table>

### Tratando valores de coluna nullable {#nullable_columns}

O package `database/sql` fornece vários tipos especiais que você pode usar como
argumentos para a função `Scan` quando o valor de uma coluna pode ser null. Cada
um inclui um campo `Valid` que reporta se o valor é não-null, e um
campo contendo o valor se for o caso.

O código no exemplo a seguir faz query para um nome de cliente. Se o valor do nome
for null, o código substitui outro valor para uso na aplicação.

```
var s sql.NullString
err := db.QueryRow("SELECT name FROM customer WHERE id = ?", id).Scan(&s)
if err != nil {
	log.Fatal(err)
}

// Find customer name, using placeholder if not present.
name := "Valued Customer"
if s.Valid {
	name = s.String
}
```

Veja mais sobre cada tipo na referência do package `sql`:

*    [`NullBool`](https://pkg.go.dev/database/sql#NullBool)
*    [`NullFloat64`](https://pkg.go.dev/database/sql#NullFloat64)
*    [`NullInt32`](https://pkg.go.dev/database/sql#NullInt32)
*    [`NullInt64`](https://pkg.go.dev/database/sql#NullInt64)
*    [`NullString`](https://pkg.go.dev/database/sql#NullString)
*    [`NullTime`](https://pkg.go.dev/database/sql#NullTime)

### Obtendo dados das colunas {#column_data}

Ao percorrer as linhas retornadas por uma query, você usa `Scan` para copiar os valores de coluna de uma linha
em valores Go, como descrito na
referência [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan).

Há um conjunto base de conversões de dados suportado por todos os drivers, como
converter SQL `INT` para Go `int`. Alguns drivers estendem esse conjunto de conversões;
consulte a documentação de cada driver individual para detalhes.

Como você pode esperar, `Scan` converterá de tipos de coluna para tipos Go que
são similares. Por exemplo, `Scan` converterá de SQL `CHAR`, `VARCHAR`, e
`TEXT` para Go `string`. No entanto, `Scan` também executará uma conversão para
outro tipo Go que seja uma boa escolha para o valor da coluna. Por exemplo, se a
coluna é um `VARCHAR` que sempre conterá um número, você pode especificar um
tipo numérico Go, como `int`, para receber o valor, e `Scan` converterá
usando `strconv.Atoi` para você.

Para mais detalhes sobre conversões feitas pela função `Scan`, consulte a referência [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan).

### Tratando múltiplos result sets {#multiple_result_sets}

Quando sua operação de banco de dados pode retornar múltiplos result sets, você pode
recuperá-los usando
[`Rows.NextResultSet`](https://pkg.go.dev/database/sql#Rows.NextResultSet).
Isso pode ser útil, por exemplo, quando você está enviando SQL que faz query separadamente em
múltiplas tabelas, retornando um result set para cada.

`Rows.NextResultSet` prepara o próximo result set para que uma chamada a
`Rows.Next` recupere a primeira linha daquele próximo set. Ele retorna um boolean
indicando se há um próximo result set.

O código no exemplo a seguir usa `DB.Query` para executar dois statements SQL.
O primeiro result set é da primeira query no procedimento, recuperando todas
as linhas da tabela `album`. O próximo result set é da segunda query,
recuperando linhas da tabela `song`.

```
rows, err := db.Query("SELECT * from album; SELECT * from song;")
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// Loop through the first result set.
for rows.Next() {
	// Handle result set.
}

// Advance to next result set.
rows.NextResultSet()

// Loop through the second result set.
for rows.Next() {
	// Handle second set.
}

// Check for any error in either result set.
if err := rows.Err(); err != nil {
	log.Fatal(err)
}
```

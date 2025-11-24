<!--{
  "Title": "Executing SQL statements that don't return data",
  "ia-translated": true
}-->

Quando você executa ações de banco de dados que não retornam dados, use um método `Exec` ou
`ExecContext` do package `database/sql`. Statements SQL que você
executaria desta maneira incluem `INSERT`, `DELETE`, e `UPDATE`.

Quando sua query pode retornar linhas, use um método `Query` ou `QueryContext`
em vez disso. Para mais, consulte [Querying a database](/doc/database/querying).

Um método `ExecContext` funciona como um método `Exec`, mas com um
argumento `context.Context` adicional, como descrito em
[Canceling in-progress operations](/doc/database/cancel-operations).

O código no exemplo a seguir usa
[`DB.Exec`](https://pkg.go.dev/database/sql#DB.Exec) para executar um
statement para adicionar um novo álbum de disco a uma tabela `album`.

```
func AddAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist) VALUES (?, ?)", alb.Title, alb.Artist)
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}

	// Get the new album's generated ID for the client.
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}
	// Return the new album's ID.
	return id, nil
}
```

`DB.Exec` retorna valores: um [`sql.Result`](https://pkg.go.dev/database/sql#Result)
e um erro. Quando o erro é `nil`, você pode usar o `Result` para obter o ID
do último item inserido (como no exemplo) ou para recuperar o número de linhas
afetadas pela operação.

**Nota:** Placeholders de parâmetro em prepared statements variam dependendo
do DBMS e driver que você está usando. Por exemplo, o
[driver pq](https://pkg.go.dev/github.com/lib/pq) para Postgres requer um
placeholder como `$1` em vez de `?`.

Se seu código executará o mesmo statement SQL repetidamente, considere
usar um `sql.Stmt` para criar um prepared statement reutilizável a partir do statement
SQL. Para mais, consulte [Using prepared statements](/doc/database/prepared-statements).

**Cuidado:** Não use funções de formatação de string como `fmt.Sprintf`
para montar um statement SQL! Você poderia introduzir um risco de SQL injection.
Para mais, consulte [Avoiding SQL injection risk](/doc/database/sql-injection).

#### Funções para executar statements SQL que não retornam linhas {#no_rows_functions}

<table id="no-rows-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">Function</th>
      <th class="DocTable-cell">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.Exec">DB.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#DB.ExecContext">DB.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">Executar um único statement SQL isoladamente.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Exec">Tx.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Tx.ExecContext">Tx.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">Executar um statement SQL dentro de uma transação maior. Para mais, consulte
          <a href="/doc/database/execute-transactions">Executing transactions</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Exec">Stmt.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Stmt.ExecContext">Stmt.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">Executar um statement SQL já preparado. Para mais, consulte
          <a href="/doc/database/prepared-statements">Using prepared statements</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.ExecContext">Conn.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">Para uso com conexões reservadas. Para mais, consulte
          <a href="/doc/database/manage-connections">Managing connections</a>.
      </td>
    </tr>
  </tbody>
</table>

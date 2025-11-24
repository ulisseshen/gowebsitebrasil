<!--{
  "Title": "Canceling in-progress operations",
  "ia-translated": true
}-->

Você pode gerenciar operações em andamento usando Go
[`context.Context`](https://pkg.go.dev/context#Context). Um `Context` é um
valor de dados padrão do Go que pode reportar se a operação geral que ele
representa foi cancelada e não é mais necessária. Passando um
`context.Context` através de chamadas de função e serviços na sua aplicação, esses
podem parar de trabalhar cedo e retornar um erro quando seu processamento não é mais
necessário. Para mais sobre `Context`, consulte
[Go Concurrency Patterns: Context](/blog/context).

Por exemplo, você pode querer:

*   Finalizar operações de longa duração, incluindo operações de banco de dados que estão
    levando muito tempo para completar.
*   Propagar solicitações de cancelamento de outros lugares, como quando um cliente
    fecha uma conexão.

Muitas APIs para desenvolvedores Go incluem métodos que recebem um argumento `Context`,
tornando mais fácil para você usar `Context` em toda sua aplicação.

### Cancelando operações de banco de dados após um timeout {#timeout_cancel}

Você pode usar um `Context` para definir um timeout ou deadline após o qual uma operação
será cancelada. Para derivar um `Context` com um timeout ou deadline, chame
[`context.WithTimeout`](https://pkg.go.dev/context#WithTimeout) ou
[`context.WithDeadline`](https://pkg.go.dev/context#WithDeadline).

O código no exemplo de timeout a seguir deriva um `Context` e o passa para
o método `sql.DB` [`QueryContext`](https://pkg.go.dev/database/sql#DB.QueryContext).

```
func QueryWithTimeout(ctx context.Context) {
	// Create a Context with a timeout.
	queryCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	// Pass the timeout Context with a query.
	rows, err := db.QueryContext(queryCtx, "SELECT * FROM album")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// Handle returned rows.
}
```

Quando um context é derivado de um context externo, como `queryCtx` é derivado
de `ctx` neste exemplo, se o context externo for cancelado, então o context derivado
é automaticamente cancelado também. Por exemplo, em servidores HTTP, o
método `http.Request.Context` retorna um context associado com a requisição.
Esse context é cancelado se o cliente HTTP desconectar ou cancelar a requisição
HTTP (possível em HTTP/2). Passar o context de uma requisição HTTP para
`QueryWithTimeout` acima faria a query de banco de dados parar cedo _ou_
se a requisição HTTP geral for cancelada ou se a query levar mais de cinco
segundos.

**Nota:** Sempre adie uma chamada à função `cancel` que é retornada quando você
cria um novo `Context` com um timeout ou deadline. Isso libera recursos mantidos
pelo novo `Context` quando a função que o contém sai. Também cancela
`queryCtx`, mas quando a função retorna, nada deveria estar usando
`queryCtx` mais.

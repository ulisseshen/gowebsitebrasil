<!--{
  "Title": "Accessing relational databases",
  "Breadcrumb": true,
  "ia-translated": true
}-->

Usando Go, você pode incorporar uma grande variedade de bancos de dados e abordagens de acesso a dados
em suas aplicações. Os tópicos nesta seção descrevem como usar
o package [`database/sql`](https://pkg.go.dev/database/sql) da biblioteca padrão
para acessar bancos de dados relacionais.

Para um tutorial introdutório sobre acesso a dados com Go, consulte
[Tutorial: Accessing a relational database](/doc/tutorial/database-access).

Go também suporta outras tecnologias de acesso a dados, incluindo bibliotecas ORM
para acesso de nível mais alto a bancos de dados relacionais, e também data stores
NoSQL não relacionais.

*   **Bibliotecas de mapeamento objeto-relacional (ORM).** Embora o package `database/sql`
    inclua funções para lógica de acesso a dados de nível mais baixo, você também pode
    usar Go para acessar data stores em um nível de abstração mais alto. Para mais
    sobre duas bibliotecas populares de mapeamento objeto-relacional (ORM) para Go, consulte
    [GORM](https://gorm.io/index.html) ([referência do package](https://pkg.go.dev/gorm.io/gorm))
    e [ent](https://entgo.io/) ([referência do package](https://pkg.go.dev/entgo.io/ent)).
*   **Data stores NoSQL.** A comunidade Go desenvolveu drivers para a
    maioria dos data stores NoSQL, incluindo [MongoDB](https://docs.mongodb.com/drivers/go/)
    e [Couchbase](https://docs.couchbase.com/go-sdk/current/hello-world/overview.html).
    Você pode pesquisar em [pkg.go.dev](https://pkg.go.dev/) para mais.

### Sistemas de gerenciamento de banco de dados suportados {#supported_dbms}

Go suporta todos os sistemas de gerenciamento de banco de dados relacional mais comuns,
incluindo MySQL, Oracle, Postgres, SQL Server, SQLite, e mais.

Você encontrará uma lista completa de drivers na
página [SQLDrivers](/wiki/SQLDrivers).

### Funções para executar queries ou fazer mudanças no banco de dados {#functions}

O package `database/sql` inclui funções especificamente projetadas para o
tipo de operação de banco de dados que você está executando. Por exemplo, embora você possa usar
`Query` ou `QueryRow` para executar queries, `QueryRow` é projetado para o caso
quando você está esperando apenas uma única linha, omitindo a sobrecarga de retornar
um `sql.Rows` que inclui apenas uma linha. Você pode usar a função `Exec`
para fazer mudanças no banco de dados com statements SQL como `INSERT`, `UPDATE`, ou
`DELETE`.

Para mais, consulte o seguinte:

*   [Executing SQL statements that don't return data](/doc/database/change-data)
*   [Querying for data](/doc/database/querying)

### Transações {#transactions}

Através de `sql.Tx`, você pode escrever código para executar operações de banco de dados em uma
transação. Em uma transação, múltiplas operações podem ser executadas juntas
e concluir com um commit final, para aplicar todas as mudanças em um único passo
atômico, ou um rollback, para descartá-las.

Para mais sobre transações, consulte [Executing transactions](/doc/database/execute-transactions).

### Cancelamento de query {#query_cancellation}

Você pode usar `context.Context` quando quiser a capacidade de cancelar uma operação
de banco de dados, como quando a conexão do cliente fecha ou a operação executa
por mais tempo do que você gostaria.

Para qualquer operação de banco de dados, você pode usar uma função do package `database/sql`
que recebe `Context` como argumento. Usando o `Context`, você pode especificar um
timeout ou deadline para a operação. Você também pode usar o `Context` para
propagar uma solicitação de cancelamento através da sua aplicação para a função
executando um statement SQL, garantindo que recursos sejam liberados se não forem
mais necessários.

Para mais, consulte [Canceling in-progress operations](/doc/database/cancel-operations).

### Pool de conexões gerenciado {#connection_pool}

Quando você usa o database handle `sql.DB`, você está se conectando com um
pool de conexões embutido que cria e descarta conexões de acordo com as
necessidades do seu código. Um handle através de `sql.DB` é a maneira mais comum de fazer
acesso a banco de dados com Go. Para mais, consulte
[Opening a database handle](/doc/database/open-handle).

O package `database/sql` gerencia o pool de conexões para você. No entanto, para
necessidades mais avançadas, você pode definir propriedades do pool de conexões como descrito em
[Setting connection pool properties](/doc/database/manage-connections#connection_pool_properties).

Para aquelas operações em que você precisa de uma única conexão reservada, o
package `database/sql` fornece [`sql.Conn`](https://pkg.go.dev/database/sql#Conn).
`Conn` é especialmente útil quando uma transação com `sql.Tx` seria uma
má escolha.

Por exemplo, seu código pode precisar:

*   Fazer mudanças de schema através de DDL, incluindo lógica que contém sua
    própria semântica de transação. Misturar funções de transação do package `sql` com
    statements de transação SQL é uma prática ruim, como descrito em
    [Executing transactions](/doc/database/execute-transactions).
*   Executar operações de bloqueio de query que criam tabelas temporárias.

Para mais, consulte [Using dedicated connections](/doc/database/manage-connections#dedicated_connections).

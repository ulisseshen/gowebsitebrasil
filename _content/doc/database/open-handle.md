<!--{
  "Title": "Opening a database handle",
  "Breadcrumb": true,
  "ia-translated": true
}-->

O package [`database/sql`](https://pkg.go.dev/database/sql) simplifica
o acesso a banco de dados reduzindo a necessidade
de você gerenciar conexões. Ao contrário de muitas APIs de acesso a dados, com
`database/sql` você não abre explicitamente uma conexão, faz o trabalho, e depois fecha
a conexão. Em vez disso, seu código abre um database handle que representa
um pool de conexões, depois executa operações de acesso a dados com o handle,
chamando um método `Close` apenas quando necessário para liberar recursos, como aqueles
mantidos por linhas recuperadas ou um prepared statement.

Em outras palavras, é o database handle, representado por um
[`sql.DB`](https://pkg.go.dev/database/sql#DB), que
lida com conexões, abrindo e fechando-as em nome do seu código. Conforme seu
código usa o handle para executar operações de banco de dados, essas operações têm
acesso concorrente ao banco de dados. Para mais, consulte
[Managing connections](/doc/database/manage-connections).

**Nota:** Você também pode reservar uma conexão de banco de dados. Para mais
informações, consulte
[Using dedicated connections](/doc/database/manage-connections#dedicated_connections).

Além das APIs disponíveis no package `database/sql`, a comunidade
Go desenvolveu drivers para todos os sistemas de gerenciamento de banco de dados (DBMSes)
mais comuns (e muitos incomuns).

Ao abrir um database handle, você segue estes passos de alto nível:

1. Localizar um driver.

    Um driver traduz requisições e respostas entre seu código Go e o
    banco de dados. Para mais, consulte [Locating and importing a database driver](#database_driver).

2. Abrir um database handle.

    Depois de importar o driver, você pode abrir um handle para um
    banco de dados específico. Para mais, consulte [Opening a database handle](#opening_handle).

3. Confirmar uma conexão.

    Uma vez que você abriu um database handle, seu código pode verificar que uma
    conexão está disponível. Para mais, consulte [Confirming a connection](#confirm_connection).

Seu código tipicamente não abrirá ou fechará conexões de banco de dados explicitamente -- isso é
feito pelo database handle. No entanto, seu código deve liberar recursos que
obtém ao longo do caminho, como um `sql.Rows` contendo resultados de query. Para
mais, consulte [Freeing resources](#free_resources).

### Localizando e importando um driver de banco de dados {#database_driver}

Você precisará de um driver de banco de dados que suporte o DBMS que você está usando. Para localizar
um driver para seu banco de dados, consulte [SQLDrivers](/wiki/SQLDrivers).

Para tornar o driver disponível para seu código, você o importa como faria com
qualquer outro package Go. Aqui está um exemplo:

```
import "github.com/go-sql-driver/mysql"
```

Observe que se você não está chamando nenhuma função diretamente do package do driver
-- como quando ele está sendo usado implicitamente pelo package `sql` --
você precisará usar um blank import, que prefixa o caminho de import com um
underscore:


```
import _ "github.com/go-sql-driver/mysql"
```

**Nota:** Como melhor prática, evite usar a própria API do driver de banco de dados
para operações de banco de dados. Em vez disso, use funções no package `database/sql`.
Isso ajudará a manter seu código fracamente acoplado com o DBMS,
tornando mais fácil mudar para um DBMS diferente se você precisar.

### Abrindo um database handle {#opening_handle}

Um database handle `sql.DB` fornece a capacidade de ler e escrever em um
banco de dados, tanto individualmente quanto em uma transação.

Você pode obter um database handle chamando ou `sql.Open` (que recebe uma
connection string) ou `sql.OpenDB` (que recebe um `driver.Connector`). Ambos
retornam um ponteiro para um [`sql.DB`](https://pkg.go.dev/database/sql#DB).

**Nota:** Certifique-se de manter suas credenciais de banco de dados fora do seu código fonte Go.
Para mais, consulte [Storing database credentials](#store_credentials).

#### Abrindo com uma connection string {#open_connection_string}

Use a função [`sql.Open`](https://pkg.go.dev/database/sql#Open) quando você
quiser se conectar usando uma connection string. O formato da string variará
dependendo do driver que você está usando.

Aqui está um exemplo para MySQL:

```
db, err = sql.Open("mysql", "username:password@tcp(127.0.0.1:3306)/jazzrecords")
if err != nil {
	log.Fatal(err)
}
```

No entanto, você provavelmente descobrirá que capturar propriedades de conexão de uma maneira mais
estruturada lhe dá código que é mais legível. Os detalhes variarão por
driver.

Por exemplo, você poderia substituir o exemplo anterior pelo seguinte, que
usa a [`Config`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config) do driver MySQL
para especificar propriedades e seu
[`método FormatDSN`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN)
para construir uma connection string.

```
// Specify connection properties.
cfg := mysql.NewConfig()
cfg.User = username
cfg.Passwd = password
cfg.Net = "tcp"
cfg.Addr = "127.0.0.1:3306"
cfg.DBName = "jazzrecords"

// Get a database handle.
db, err = sql.Open("mysql", cfg.FormatDSN())
if err != nil {
	log.Fatal(err)
}
```

#### Abrindo com um Connector {#open_connector}

Use a função [`sql.OpenDB`](https://pkg.go.dev/database/sql#OpenDB) quando
você quiser aproveitar recursos de conexão específicos do driver que não estão
disponíveis em uma connection string. Cada driver suporta seu próprio conjunto de
propriedades de conexão, frequentemente fornecendo maneiras de customizar a requisição de conexão
específica para o DBMS.

Adaptando o exemplo anterior de `sql.Open` para usar `sql.OpenDB`, você poderia
criar um handle com código como o seguinte:

```
// Specify connection properties.
cfg := mysql.NewConfig()
cfg.User = username
cfg.Passwd = password
cfg.Net = "tcp"
cfg.Addr = "127.0.0.1:3306"
cfg.DBName = "jazzrecords"

// Get a driver-specific connector.
connector, err := mysql.NewConnector(&cfg)
if err != nil {
	log.Fatal(err)
}

// Get a database handle.
db = sql.OpenDB(connector)
```

#### Tratando erros {#handle_errors}

Seu código deve verificar por um erro ao tentar criar um handle, como
com `sql.Open`. Este não será um erro de conexão. Em vez disso, você receberá um
erro se `sql.Open` foi incapaz de inicializar o handle. Isso poderia acontecer,
por exemplo, se ele for incapaz de fazer parse do DSN que você especificou.

### Confirmando uma conexão {#confirm_connection}

Quando você abre um database handle, o package `sql` pode não criar uma nova
conexão de banco de dados imediatamente. Em vez disso, ele pode criar a conexão
quando seu código precisar dela. Se você não for usar o banco de dados imediatamente e
quiser confirmar que uma conexão poderia ser estabelecida, chame
[`Ping`](https://pkg.go.dev/database/sql#DB.Ping) ou
[`PingContext`](https://pkg.go.dev/database/sql#DB.PingContext).

O código no exemplo a seguir faz ping no banco de dados para confirmar uma conexão.

```
db, err = sql.Open("mysql", connString)

// Confirm a successful connection.
if err := db.Ping(); err != nil {
	log.Fatal(err)
}
```

### Armazenando credenciais de banco de dados {#store_credentials}

Evite armazenar credenciais de banco de dados no seu código fonte Go, o que poderia expor o
conteúdo do seu banco de dados para outros. Em vez disso, encontre uma maneira de armazená-las em um
local fora do seu código mas disponível para ele. Por exemplo, considere uma
aplicação de gerenciamento de segredos que armazena credenciais e fornece uma API que seu código pode
usar para recuperar credenciais para autenticação com seu DBMS.

Uma abordagem popular é armazenar os segredos no ambiente antes do
programa iniciar, talvez carregados de um gerenciador de segredos, e então seu programa Go
pode lê-los usando [`os.Getenv`](https://pkg.go.dev/os#Getenv):

```
username := os.Getenv("DB_USER")
password := os.Getenv("DB_PASS")
```

Esta abordagem também permite que você defina as variáveis de ambiente você mesmo para
testes locais.

### Liberando recursos {#free_resources}

Embora você não gerencie ou feche conexões explicitamente com o
package `database/sql`, seu código deve liberar recursos que obteve quando
eles não forem mais necessários. Esses podem incluir recursos mantidos por um `sql.Rows`
representando dados retornados de uma query ou um `sql.Stmt` representando um
prepared statement.

Tipicamente, você fecha recursos adiando uma chamada a uma função `Close` para que
recursos sejam liberados antes da função envolvente sair.

O código no exemplo a seguir adia `Close` para liberar o recurso mantido por
[`sql.Rows`](https://pkg.go.dev/database/sql#Rows).

```
rows, err := db.Query("SELECT * FROM album WHERE artist = ?", artist)
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// Loop through returned rows.
```

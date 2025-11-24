<!--{
  "Title": "Managing connections",
  "ia-translated": true
}-->

Para a grande maioria dos programas, você não precisa ajustar os padrões do pool de conexões
`sql.DB`. Mas para alguns programas avançados, você pode precisar ajustar os
parâmetros do pool de conexões ou trabalhar com conexões explicitamente. Este tópico
explica como.

O database handle [`sql.DB`](https://pkg.go.dev/database/sql#DB) é seguro para
uso concorrente por múltiplas goroutines
(significando que o handle é o que outras linguagens podem chamar de "thread-safe"). Algumas
outras bibliotecas de acesso a banco de dados são baseadas em conexões que só podem ser usadas
para uma operação de cada vez. Para preencher essa lacuna, cada `sql.DB` gerencia um pool
de conexões ativas para o banco de dados subjacente, criando novas conforme necessário
para paralelismo no seu programa Go.

O pool de conexões é adequado para a maioria das necessidades de acesso a dados. Quando você chama um
método `Query` ou `Exec` de `sql.DB`, a implementação `sql.DB` recupera uma
conexão disponível do pool ou, se necessário, cria uma. O package
retorna a conexão ao pool quando não é mais necessária. Isso suporta um
alto nível de paralelismo para acesso ao banco de dados.

### Definindo propriedades do pool de conexões {#connection_pool_properties}

Você pode definir propriedades que orientam como o package `sql` gerencia um pool de
conexões. Para obter estatísticas sobre os efeitos dessas propriedades, use
[`DB.Stats`](https://pkg.go.dev/database/sql#DB.Stats).

#### Definindo o número máximo de conexões abertas {#max_open_connections}

[`DB.SetMaxOpenConns`](https://pkg.go.dev/database/sql#DB.SetMaxOpenConns)
impõe um limite no número de conexões abertas. Além desse limite, novas
operações de banco de dados aguardarão uma operação existente terminar, momento em que
`sql.DB` criará outra conexão. Por padrão, `sql.DB` cria uma
nova conexão sempre que todas as conexões existentes estão em uso quando uma
conexão é necessária.

Tenha em mente que definir um limite torna o uso do banco de dados similar a adquirir um
lock ou semáforo, com o resultado de que sua aplicação pode entrar em deadlock aguardando
por uma nova conexão de banco de dados.

#### Definindo o número máximo de conexões ociosas {#max_idle_connections}

[`DB.SetMaxIdleConns`](https://pkg.go.dev/database/sql#DB.SetMaxIdleConns)
altera o limite no número máximo de conexões ociosas que `sql.DB`
mantém.

Quando uma operação SQL termina em uma dada conexão de banco de dados, ela não é
tipicamente desligada imediatamente: a aplicação pode precisar dela novamente em breve, e
manter a conexão aberta evita ter que reconectar ao banco de dados
para a próxima operação. Por padrão um `sql.DB` mantém duas conexões ociosas em
qualquer momento. Aumentar o limite pode evitar reconexões frequentes em programas
com paralelismo significativo.

#### Definindo o tempo máximo que uma conexão pode ficar ociosa {#max_idle_time}

[`DB.SetConnMaxIdleTime`](https://pkg.go.dev/database/sql#DB.SetConnMaxIdleTime)
define o comprimento máximo de tempo que uma conexão pode ficar ociosa antes de ser fechada.
Isso faz com que o `sql.DB` feche conexões que ficaram ociosas por mais tempo
que a duração dada.

Por padrão, quando uma conexão ociosa é adicionada ao pool de conexões, ela
permanece lá até que seja necessária novamente. Ao usar `DB.SetMaxIdleConns` para
aumentar o número de conexões ociosas permitidas durante surtos de atividade
paralela, também usar `DB.SetConnMaxIdleTime` pode organizar para liberar essas
conexões posteriormente quando o sistema está quieto.

#### Definindo o tempo máximo de vida das conexões {#max_connection_lifetime}

Usar [`DB.SetConnMaxLifetime`](https://pkg.go.dev/database/sql#DB.SetConnMaxLifetime)
define o comprimento máximo de tempo que uma conexão pode ser mantida aberta antes de ser
fechada.

Por padrão, uma conexão pode ser usada e reutilizada por um tempo arbitrariamente longo,
sujeito aos limites descritos acima. Em alguns sistemas, como aqueles
usando um servidor de banco de dados com balanceamento de carga, pode ser útil garantir que a
aplicação nunca use uma conexão particular por muito tempo sem reconectar.

### Usando conexões dedicadas {#dedicated_connections}

O package `database/sql` inclui funções que você pode usar quando um banco de dados pode
atribuir significado implícito a uma sequência de operações executadas em uma conexão
particular.

O exemplo mais comum são transações, que tipicamente começam com um comando `BEGIN`,
terminam com um comando `COMMIT` ou `ROLLBACK`, e incluem todos os
comandos emitidos na conexão entre esses comandos na transação
geral. Para este caso de uso, use o suporte a transações do package `sql`.
Consulte [Executing transactions](/doc/database/execute-transactions).

Para outros casos de uso onde uma sequência de operações individuais deve executar
na mesma conexão, o package `sql` fornece conexões dedicadas.
[`DB.Conn`](https://pkg.go.dev/database/sql#DB.Conn) obtém uma conexão
dedicada, um [`sql.Conn`](https://pkg.go.dev/database/sql#Conn). O
`sql.Conn` tem métodos `BeginTx`, `ExecContext`, `PingContext`,
`PrepareContext`, `QueryContext`, e `QueryRowContext` que se comportam como os
métodos equivalentes em DB mas só usam a conexão dedicada. Quando terminar
com a conexão dedicada, seu código deve liberá-la usando `Conn.Close`.

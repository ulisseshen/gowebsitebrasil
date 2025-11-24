---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Acessando um banco de dados relacional",
  "Breadcrumb": true
}-->

Este tutorial introduz os fundamentos de acessar um banco de dados relacional com
Go e o pacote `database/sql` em sua biblioteca padrão.

Você aproveitará mais este tutorial se tiver familiaridade básica com
Go e suas ferramentas. Se esta é sua primeira exposição ao Go, por favor veja
[Tutorial: Começando com Go](/doc/tutorial/getting-started)
para uma rápida introdução.

O pacote [`database/sql`](https://pkg.go.dev/database/sql) que você
usará inclui tipos e funções para conectar a bancos de dados, executar
transações, cancelar uma operação em andamento, e mais. Para mais detalhes
sobre o uso do pacote, veja
[Acessando bancos de dados](/doc/database/index).

Neste tutorial, você criará um banco de dados, então escreverá código para acessar o
banco de dados. Seu projeto exemplo será um repositório de dados sobre discos
de jazz vintage.

Neste tutorial, você progredirá através das seguintes seções:

1. Criar uma pasta para seu código.
2. Configurar um banco de dados.
3. Importar o driver do banco de dados.
4. Obter um handle de banco de dados e conectar.
5. Consultar múltiplas linhas.
6. Consultar uma única linha.
7. Adicionar dados.

**Nota:** Para outros tutoriais, veja [Tutoriais](/doc/tutorial/index.html).

## Pré-requisitos {#prerequisites}

*   **Uma instalação do sistema de gerenciamento de banco de dados relacional (DBMS) [MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).**
*   **Uma instalação do Go.** Para instruções de instalação, veja
    [Instalando Go](/doc/install).
*   **Uma ferramenta para editar seu código.** Qualquer editor de texto que você tenha funcionará bem.
*   **Um terminal de comando.** Go funciona bem usando qualquer terminal no Linux e Mac,
    e no PowerShell ou cmd no Windows.

## Criar uma pasta para seu código {#create_folder}

Para começar, crie uma pasta para o código que você escreverá.

1. Abra um prompt de comando e mude para seu diretório home.

    No Linux ou Mac:

    ```
    $ cd
    ```

    No Windows:

    ```
    C:\> cd %HOMEPATH%
    ```

    Para o resto do tutorial mostraremos um $ como o prompt. Os
    comandos que usamos funcionarão no Windows também.

2. Do prompt de comando, crie um diretório para seu código chamado
    data-access.

    ```
    $ mkdir data-access
    $ cd data-access
    ```


3. Crie um módulo no qual você pode gerenciar dependências que adicionará durante
    este tutorial.

    Execute o comando `go mod init`, dando a ele o caminho do módulo do seu novo código.

    ```
    $ go mod init example/data-access
    go: creating new go.mod: module example/data-access
    ```

    Este comando cria um arquivo go.mod no qual dependências que você adicionar serão
    listadas para rastreamento. Para mais, certifique-se de ver
    [Gerenciando dependências](/doc/modules/managing-dependencies).

    **Nota:** No desenvolvimento real, você especificaria um caminho de módulo que é
    mais específico para suas próprias necessidades. Para mais, veja
    [Gerenciando dependências](/doc/modules/managing-dependencies#naming_module).

A seguir, você criará um banco de dados.

## Configurar um banco de dados {#set_up_database}

Neste passo, você criará o banco de dados com o qual trabalhará. Você usará
a CLI para o próprio DBMS para criar o banco de dados e tabela, assim como para
adicionar dados.

Você criará um banco de dados com dados sobre gravações de jazz vintage em vinil.

O código aqui usa a [CLI MySQL](https://dev.mysql.com/doc/refman/8.0/en/mysql.html),
mas a maioria dos DBMSes tem sua própria CLI com recursos similares.

1. Abra um novo prompt de comando.
2. Na linha de comando, faça login em seu DBMS, como no seguinte exemplo para
    MySQL.

    ```
    $ mysql -u root -p
    Enter password:

    mysql>
    ```

3. No prompt de comando `mysql`, crie um banco de dados.

    ```
    mysql> create database recordings;
    ```

4. Mude para o banco de dados que você acabou de criar para poder adicionar tabelas.

    ```
    mysql> use recordings;
    Database changed
    ```

5. No seu editor de texto, na pasta data-access, crie um arquivo chamado
    create-tables.sql para manter script SQL para adicionar tabelas.
6. No arquivo, cole o seguinte código SQL, então salve o arquivo.

    ```
    DROP TABLE IF EXISTS album;
    CREATE TABLE album (
      id         INT AUTO_INCREMENT NOT NULL,
      title      VARCHAR(128) NOT NULL,
      artist     VARCHAR(255) NOT NULL,
      price      DECIMAL(5,2) NOT NULL,
      PRIMARY KEY (`id`)
    );

    INSERT INTO album
      (title, artist, price)
    VALUES
      ('Blue Train', 'John Coltrane', 56.99),
      ('Giant Steps', 'John Coltrane', 63.99),
      ('Jeru', 'Gerry Mulligan', 17.99),
      ('Sarah Vaughan', 'Sarah Vaughan', 34.98);
    ```

    Neste código SQL, você:

    *   Deleta (drop) uma tabela chamada `album`. Executar este comando primeiro torna
        mais fácil para você re-executar o script mais tarde se quiser começar de novo
        com a tabela.

    *   Cria uma tabela `album` com quatro colunas: `title`, `artist` e `price`.
        O valor `id` de cada linha é criado automaticamente pelo DBMS.

    *   Adiciona quatro linhas com valores.

7. Do prompt de comando `mysql`, execute o script que você acabou de criar.

    Você usará o comando `source` na seguinte forma:

    ```
    mysql> source /path/to/create-tables.sql
    ```

8. No seu prompt de comando DBMS, use uma instrução `SELECT` para verificar que você
    criou com sucesso a tabela com dados.

    ```
    mysql> select * from album;
    +----+---------------+----------------+-------+
    | id | title         | artist         | price |
    +----+---------------+----------------+-------+
    |  1 | Blue Train    | John Coltrane  | 56.99 |
    |  2 | Giant Steps   | John Coltrane  | 63.99 |
    |  3 | Jeru          | Gerry Mulligan | 17.99 |
    |  4 | Sarah Vaughan | Sarah Vaughan  | 34.98 |
    +----+---------------+----------------+-------+
    4 rows in set (0.00 sec)
    ```

A seguir, você escreverá algum código Go para conectar para que possa consultar.

## Encontrar e importar um driver de banco de dados {#import_driver}

Agora que você tem um banco de dados com alguns dados, comece seu código Go.

Localize e importe um driver de banco de dados que traduzirá requisições que você faz
através de funções no pacote `database/sql` em requisições que o banco de dados
entende.

1. No seu navegador, visite a página wiki [SQLDrivers](/wiki/SQLDrivers)
    para identificar um driver que você pode usar.

    Use a lista na página para identificar o driver que você usará. Para acessar
    MySQL neste tutorial, você usará
    [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql/).

2. Note o nome do pacote para o driver -- aqui, `github.com/go-sql-driver/mysql`.

3. Usando seu editor de texto, crie um arquivo no qual escrever seu código Go e
    salve o arquivo como main.go no diretório data-access que você criou anteriormente.

4. Em main.go, cole o seguinte código para importar o pacote driver.

    ```
    package main

    import "github.com/go-sql-driver/mysql"
    ```

    Neste código, você:

    *   Adiciona seu código a um pacote `main` para que possa executá-lo independentemente.

    *   Importa o driver MySQL `github.com/go-sql-driver/mysql`.

Com o driver importado, você começará a escrever código para acessar o banco de dados.

## Obter um handle de banco de dados e conectar {#get_handle}

Agora escreva algum código Go que lhe dá acesso ao banco de dados com um handle de banco de dados.

Você usará um ponteiro para uma struct `sql.DB`, que representa acesso a um
banco de dados específico.

#### Escrever o código

1. Em main.go, abaixo do código `import` que você acabou de adicionar, cole o seguinte
    código Go para criar um handle de banco de dados.

    ```
    var db *sql.DB

    func main() {
    	// Capture connection properties.
    	cfg := mysql.NewConfig()
    	cfg.User = os.Getenv("DBUSER")
    	cfg.Passwd = os.Getenv("DBPASS")
    	cfg.Net = "tcp"
    	cfg.Addr = "127.0.0.1:3306"
    	cfg.DBName = "recordings"

    	// Get a database handle.
    	var err error
    	db, err = sql.Open("mysql", cfg.FormatDSN())
    	if err != nil {
    		log.Fatal(err)
    	}

    	pingErr := db.Ping()
    	if pingErr != nil {
    		log.Fatal(pingErr)
    	}
    	fmt.Println("Connected!")
    }
    ```

    Neste código, você:

    *   Declara uma variável `db` do tipo [`*sql.DB`](https://pkg.go.dev/database/sql#DB).
        Este é seu handle de banco de dados.

        Fazer `db` uma variável global simplifica este exemplo. Em
        produção, você evitaria a variável global, como passando a
        variável para funções que precisam dela ou envolvendo-a em uma struct.

    *   Usa o [`Config`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config) do driver MySQL
        -- e o [`FormatDSN`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN) do tipo
        -– para coletar propriedades de conexão e formatá-las em um DSN para uma string de conexão.

        A struct `Config` torna o código mais fácil de ler do que uma
        string de conexão seria.

    *   Chama [`sql.Open`](https://pkg.go.dev/database/sql#Open)
        para inicializar a variável `db`, passando o valor de retorno de
        `FormatDSN`.

    *   Verifica se há um erro de `sql.Open`. Pode falhar se, por
        exemplo, os detalhes de conexão do seu banco de dados não estiverem bem formados.

        Para simplificar o código, você está chamando `log.Fatal` para encerrar
        a execução e imprimir o erro no console. Em código de produção, você
        vai querer tratar erros de forma mais elegante.

    *   Chama [`DB.Ping`](https://pkg.go.dev/database/sql#DB.Ping) para
        confirmar que a conexão ao banco de dados funciona. Em tempo de execução,
        `sql.Open` pode não conectar imediatamente, dependendo do
        driver. Você está usando `Ping` aqui para confirmar que o
        pacote `database/sql` pode conectar quando necessário.

    *   Verifica se há um erro de `Ping`, caso a conexão tenha falhado.

    *   Imprime uma mensagem se `Ping` conectar com sucesso.

2. Próximo ao topo do arquivo main.go, logo abaixo da declaração de pacote,
    importe os pacotes que você precisará para suportar o código que você acabou de escrever.

    O topo do arquivo agora deve ficar assim:

    ```
    package main

    import (
    	"database/sql"
    	"fmt"
    	"log"
    	"os"

    	"github.com/go-sql-driver/mysql"
    )
    ```

3. Salve main.go.

#### Executar o código

1. Comece a rastrear o módulo do driver MySQL como uma dependência.

    Use o [`go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)
    para adicionar o módulo github.com/go-sql-driver/mysql como uma dependência para seu
    próprio módulo. Use um argumento ponto para significar "obter dependências para código no
    diretório atual."

    ```
    $ go get .
    go: added filippo.io/edwards25519 v1.1.0
    go: added github.com/go-sql-driver/mysql v1.8.1
    ```

    Go baixou esta dependência porque você a adicionou à declaração `import`
    no passo anterior. Para mais sobre rastreamento de dependências,
    veja [Adicionando uma dependência](/doc/modules/managing-dependencies#adding_dependency).

2. Do prompt de comando, defina as variáveis de ambiente `DBUSER` e `DBPASS`
    para uso pelo programa Go.

    No Linux ou Mac:

    ```
    $ export DBUSER=username
    $ export DBPASS=password
    ```

    No Windows:

    ```
    C:\Users\you\data-access> set DBUSER=username
    C:\Users\you\data-access> set DBPASS=password
    ```

3. Da linha de comando no diretório contendo main.go, execute o código digitando
    `go run` com um argumento ponto para significar "executar o pacote no
    diretório atual."

    ```
    $ go run .
    Connected!
    ```

Você pode conectar! A seguir, você consultará alguns dados.

## Consultar múltiplas linhas {#multiple_rows}

Nesta seção, você usará Go para executar uma consulta SQL projetada para retornar
múltiplas linhas.

Para instruções SQL que podem retornar múltiplas linhas, você usa o método `Query`
do pacote `database/sql`, então itera através das linhas que ele retorna. (Você
aprenderá como consultar uma única linha mais tarde, na seção
[Consultar uma única linha](#single_row).)
#### Escrever o código

1. Em main.go, imediatamente acima de `func main`, cole a seguinte definição
    de uma struct `Album`. Você usará isso para manter dados de linha retornados da
    consulta.

    ```
    type Album struct {
    	ID     int64
    	Title  string
    	Artist string
    	Price  float32
    }
    ```

2. Abaixo de `func main`, cole a seguinte função `albumsByArtist` para consultar
    o banco de dados.

    ```
    // albumsByArtist queries for albums that have the specified artist name.
    func albumsByArtist(name string) ([]Album, error) {
    	// An albums slice to hold data from returned rows.
    	var albums []Album

    	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
    	if err != nil {
    		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    	}
    	defer rows.Close()
    	// Loop through rows, using Scan to assign column data to struct fields.
    	for rows.Next() {
    		var alb Album
    		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
    			return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    		}
    		albums = append(albums, alb)
    	}
    	if err := rows.Err(); err != nil {
    		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    	}
    	return albums, nil
    }
    ```

    Neste código, você:

    *   Declara um slice `albums` do tipo `Album` que você definiu. Isso manterá
        dados de linhas retornadas. Nomes e tipos de campos de struct correspondem a
        nomes e tipos de colunas do banco de dados.

    *   Usa [`DB.Query`](https://pkg.go.dev/database/sql#DB.Query) para
        executar uma instrução `SELECT` para consultar álbuns com o
        nome de artista especificado.

        O primeiro parâmetro de `Query` é a instrução SQL. Após o
        parâmetro, você pode passar zero ou mais parâmetros de qualquer tipo. Estes fornecem
        um lugar para você especificar os valores para parâmetros na sua instrução SQL.
        Separando a instrução SQL dos valores de parâmetro (em vez de
        concatená-los com, digamos, `fmt.Sprintf`), você habilita o
        pacote `database/sql` a enviar os valores separados do texto SQL,
        removendo qualquer risco de injeção SQL.

    *   Adia o fechamento de `rows` para que quaisquer recursos que ela mantenha sejam liberados quando
        a função sair.

    *   Itera através das linhas retornadas, usando
        [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) para
        atribuir valores de coluna de cada linha a campos da struct `Album`.

        `Scan` recebe uma lista de ponteiros para valores Go, onde os valores de coluna
        serão escritos. Aqui, você passa ponteiros para campos na
        variável `alb`, criados usando o operador `&`.
        `Scan` escreve através dos ponteiros para atualizar os campos da struct.

    *   Dentro do loop, verifica se há um erro ao escanear valores de coluna para os
        campos da struct.

    *   Dentro do loop, anexa o novo `alb` ao slice `albums`.

    *   Após o loop, verifica se há um erro da consulta geral, usando
        `rows.Err`. Note que se a consulta em si falhar, verificar se há um erro
        aqui é a única maneira de descobrir que os resultados estão incompletos.

3. Atualize sua função `main` para chamar `albumsByArtist`.

    No final de `func main`, adicione o seguinte código.

    ```
    albums, err := albumsByArtist("John Coltrane")
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("Albums found: %v\n", albums)
    ```

    No novo código, você agora:

    *   Chama a função `albumsByArtist` que você adicionou, atribuindo seu valor de retorno a
        uma nova variável `albums`.

    *   Imprime o resultado.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
```

A seguir, você consultará uma única linha.

## Consultar uma única linha {#single_row}

Nesta seção, você usará Go para consultar uma única linha no banco de dados.

Para instruções SQL que você sabe que retornarão no máximo uma única linha, você pode usar
`QueryRow`, que é mais simples do que usar um loop `Query`.

#### Escrever o código

1. Abaixo de `albumsByArtist`, cole a seguinte função `albumByID`.

    ```
    // albumByID queries for the album with the specified ID.
    func albumByID(id int64) (Album, error) {
    	// An album to hold data from the returned row.
    	var alb Album

    	row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
    	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
    		if err == sql.ErrNoRows {
    			return alb, fmt.Errorf("albumsById %d: no such album", id)
    		}
    		return alb, fmt.Errorf("albumsById %d: %v", id, err)
    	}
    	return alb, nil
    }
    ```

    Neste código, você:

    *   Usa [`DB.QueryRow`](https://pkg.go.dev/database/sql#DB.QueryRow)
        para executar uma instrução `SELECT` para consultar um álbum com o
        ID especificado.

        Ela retorna um `sql.Row`. Para simplificar o código chamador
        (seu código!), `QueryRow` não retorna um erro. Em vez disso,
        ela arranja para retornar qualquer erro de consulta (como `sql.ErrNoRows`)
        de `Rows.Scan` mais tarde.

    *   Usa [`Row.Scan`](https://pkg.go.dev/database/sql#Row.Scan) para copiar
        valores de coluna para campos de struct.

    *   Verifica se há um erro de `Scan`.

        O erro especial `sql.ErrNoRows` indica que a consulta não retornou
        linhas. Tipicamente esse erro vale a pena substituir com texto mais específico,
        como "no such album" aqui.

2. Atualize `main` para chamar `albumByID`.

    No final de `func main`, adicione o seguinte código.

    ```
    // Hard-code ID 2 here to test the query.
    alb, err := albumByID(2)
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("Album found: %v\n", alb)
    ```

    No novo código, você agora:

    *   Chama a função `albumByID` que você adicionou.

    *   Imprime o ID do álbum retornado.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.


```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
Album found: {2 Giant Steps John Coltrane 63.99}
```

A seguir, você adicionará um álbum ao banco de dados.

## Adicionar dados {#add_data}

Nesta seção, você usará Go para executar uma instrução SQL `INSERT` para adicionar uma
nova linha ao banco de dados.

Você viu como usar `Query` e `QueryRow` com instruções SQL que
retornam dados. Para executar instruções SQL que _não_ retornam dados, você usa `Exec`.

#### Escrever o código

1. Abaixo de `albumByID`, cole a seguinte função `addAlbum` para inserir um novo
    álbum no banco de dados, então salve o main.go.

    ```
    // addAlbum adds the specified album to the database,
    // returning the album ID of the new entry
    func addAlbum(alb Album) (int64, error) {
    	result, err := db.Exec("INSERT INTO album (title, artist, price) VALUES (?, ?, ?)", alb.Title, alb.Artist, alb.Price)
    	if err != nil {
    		return 0, fmt.Errorf("addAlbum: %v", err)
    	}
    	id, err := result.LastInsertId()
    	if err != nil {
    		return 0, fmt.Errorf("addAlbum: %v", err)
    	}
    	return id, nil
    }
    ```

    Neste código, você:

    *   Usa [`DB.Exec`](https://pkg.go.dev/database/sql#DB.Exec) para
        executar uma instrução `INSERT`.

        Como `Query`, `Exec` recebe uma instrução SQL seguida
        de valores de parâmetro para a instrução SQL.

    *   Verifica se há um erro da tentativa de `INSERT`.

    *   Recupera o ID da linha do banco de dados inserida usando
        [`Result.LastInsertId`](https://pkg.go.dev/database/sql#Result.LastInsertId).

    *   Verifica se há um erro da tentativa de recuperar o ID.

2. Atualize `main` para chamar a nova função `addAlbum`.

    No final de `func main`, adicione o seguinte código.

    ```
    albID, err := addAlbum(Album{
    	Title:  "The Modern Sound of Betty Carter",
    	Artist: "Betty Carter",
    	Price:  49.99,
    })
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("ID of added album: %v\n", albID)
    ```

    No novo código, você agora:

    *   Chama `addAlbum` com um novo álbum, atribuindo o ID do álbum que você está
        adicionando a uma variável `albID`.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
Album found: {2 Giant Steps John Coltrane 63.99}
ID of added album: 5
```

## Conclusão {#conclusion}

Parabéns! Você acabou de usar Go para realizar ações simples com um
banco de dados relacional.

Próximos tópicos sugeridos:

*   Dê uma olhada no guia de acesso a dados, que inclui mais informações
    sobre os assuntos apenas tocados aqui.

*   Se você é novo em Go, você encontrará práticas recomendadas úteis descritas em
    [Effective Go](/doc/effective_go) e [Como escrever código Go](/doc/code).

*   O [Go Tour](/tour/) é uma ótima introdução passo a passo
    aos fundamentos do Go.

## Código completo {#completed_code}

Esta seção contém o código para o aplicativo que você constrói com este tutorial.

```
package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/go-sql-driver/mysql"
)

var db *sql.DB

type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float32
}

func main() {
	// Capture connection properties.
	cfg := mysql.NewConfig()
	cfg.User = os.Getenv("DBUSER")
	cfg.Passwd = os.Getenv("DBPASS")
	cfg.Net = "tcp"
	cfg.Addr = "127.0.0.1:3306"
	cfg.DBName = "recordings"

	// Get a database handle.
	var err error
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("Connected!")

	albums, err := albumsByArtist("John Coltrane")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Albums found: %v\n", albums)

	// Hard-code ID 2 here to test the query.
	alb, err := albumByID(2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Album found: %v\n", alb)

	albID, err := addAlbum(Album{
		Title:  "The Modern Sound of Betty Carter",
		Artist: "Betty Carter",
		Price:  49.99,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("ID of added album: %v\n", albID)
}

// albumsByArtist queries for albums that have the specified artist name.
func albumsByArtist(name string) ([]Album, error) {
	// An albums slice to hold data from returned rows.
	var albums []Album

	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
	if err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	defer rows.Close()
	// Loop through rows, using Scan to assign column data to struct fields.
	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
			return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
		}
		albums = append(albums, alb)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	return albums, nil
}

// albumByID queries for the album with the specified ID.
func albumByID(id int64) (Album, error) {
	// An album to hold data from the returned row.
	var alb Album

	row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
		if err == sql.ErrNoRows {
			return alb, fmt.Errorf("albumsById %d: no such album", id)
		}
		return alb, fmt.Errorf("albumsById %d: %v", id, err)
	}
	return alb, nil
}

// addAlbum adds the specified album to the database,
// returning the album ID of the new entry
func addAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist, price) VALUES (?, ?, ?)", alb.Title, alb.Artist, alb.Price)
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	return id, nil
}
```

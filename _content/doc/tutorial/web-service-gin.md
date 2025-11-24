---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Desenvolvendo uma API RESTful com Go e Gin",
  "Breadcrumb": true
}-->

Este tutorial introduz os fundamentos de escrever uma API de serviço web RESTful com Go
e o [Gin Web Framework](https://gin-gonic.com/en/docs/) (Gin).

Você aproveitará mais este tutorial se tiver familiaridade básica com Go
e suas ferramentas. Se esta é sua primeira exposição ao Go, por favor veja
[Tutorial: Começando com Go](/doc/tutorial/getting-started)
para uma rápida introdução.

Gin simplifica muitas tarefas de codificação associadas à construção de aplicações web,
incluindo serviços web. Neste tutorial, você usará Gin para rotear requisições,
recuperar detalhes de requisição e fazer marshal de JSON para respostas.

Neste tutorial, você construirá um servidor de API RESTful com dois endpoints. Seu
projeto exemplo será um repositório de dados sobre gravações de jazz vintage.

O tutorial inclui as seguintes seções:

1. Projetar endpoints de API.
2. Criar uma pasta para seu código.
3. Criar os dados.
4. Escrever um handler para retornar todos os itens.
5. Escrever um handler para adicionar um novo item.
6. Escrever um handler para retornar um item específico.

**Nota:** Para outros tutoriais, veja [Tutoriais](/doc/tutorial/index.html).

Para experimentar isso como um tutorial interativo que você completa no Google Cloud Shell,
clique no botão abaixo.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ide.cloud.google.com/?cloudshell_workspace=~&walkthrough_tutorial_url=https://raw.githubusercontent.com/golang/tour/master/tutorial/web-service-gin.md)


## Pré-requisitos

*   **Uma instalação do Go 1.16 ou posterior.** Para instruções de instalação, veja
    [Instalando Go](/doc/install).
*   **Uma ferramenta para editar seu código.** Qualquer editor de texto que você tenha funcionará bem.
*   **Um terminal de comando.** Go funciona bem usando qualquer terminal no Linux e Mac,
    e no PowerShell ou cmd no Windows.
*   **A ferramenta curl.** No Linux e Mac, esta já deve estar instalada. No
    Windows, está incluída no Windows 10 Insider build 17063 e posterior. Para versões anteriores do
    Windows, você pode precisar instalá-la. Para mais, veja
    [Tar and Curl Come to Windows](https://docs.microsoft.com/en-us/virtualization/community/team-blog/2017/20171219-tar-and-curl-come-to-windows).

## Projetar endpoints de API {#design_endpoints}

Você construirá uma API que fornece acesso a uma loja vendendo gravações vintage
em vinil. Então você precisará fornecer endpoints através dos quais um cliente possa obter
e adicionar álbuns para usuários.

Ao desenvolver uma API, você tipicamente começa projetando os endpoints. Os
usuários da sua API terão mais sucesso se os endpoints forem fáceis de entender.

Aqui estão os endpoints que você criará neste tutorial.

/albums
*   `GET` – Obter uma lista de todos os álbuns, retornados como JSON.
*   `POST` – Adicionar um novo álbum a partir de dados de requisição enviados como JSON.

/albums/:id
*   `GET` – Obter um álbum pelo seu ID, retornando os dados do álbum como JSON.

A seguir, você criará uma pasta para seu código.

## Criar uma pasta para seu código {#create_folder}

Para começar, crie um projeto para o código que você escreverá.

1. Abra um prompt de comando e mude para seu diretório home.

    No Linux ou Mac:

    ```
    $ cd
    ```

    No Windows:

    ```
    C:\> cd %HOMEPATH%
    ```

2. Usando o prompt de comando, crie um diretório para seu código chamado
    web-service-gin.

    ```
    $ mkdir web-service-gin
    $ cd web-service-gin
    ```

3. Crie um módulo no qual você possa gerenciar dependências.

    Execute o comando `go mod init`, dando a ele o caminho do módulo em que seu código
    estará.

    ```
    $ go mod init example/web-service-gin
    go: creating new go.mod: module example/web-service-gin
    ```

    Este comando cria um arquivo go.mod no qual dependências que você adicionar serão
    listadas para rastreamento. Para mais sobre nomear um módulo com um caminho de módulo, veja
    [Gerenciando dependências](/doc/modules/managing-dependencies#naming_module).

A seguir, você projetará estruturas de dados para lidar com dados.

## Criar os dados {#create_data}

Para manter as coisas simples para o tutorial, você armazenará dados na memória. Uma
API mais típica interagiria com um banco de dados.

Note que armazenar dados na memória significa que o conjunto de álbuns será perdido cada
vez que você parar o servidor, então recriado quando você o iniciar.

#### Escrever o código

1. Usando seu editor de texto, crie um arquivo chamado main.go no diretório web-service
    . Você escreverá seu código Go neste arquivo.
2. Em main.go, no topo do arquivo, cole a seguinte declaração de package.

    ```
    package main
    ```

    Um programa standalone (ao contrário de uma biblioteca) está sempre no package `main`.

3. Abaixo da declaração de package, cole a seguinte declaração de uma
    struct `album`. Você usará isso para armazenar dados de álbum na memória.

    Struct tags como ``json:"artist"`` especificam qual deve ser o nome de um campo
    quando o conteúdo da struct é serializado em JSON. Sem elas, o JSON
    usaria os nomes de campo capitalizados da struct – um estilo não tão comum em
    JSON.

    ```
    // album represents data about a record album.
    type album struct {
    	ID     string  `json:"id"`
    	Title  string  `json:"title"`
    	Artist string  `json:"artist"`
    	Price  float64 `json:"price"`
    }
    ```

4. Abaixo da declaração de struct que você acabou de adicionar, cole o seguinte slice de
    structs `album` contendo dados que você usará para começar.

    ```
    // albums slice to seed record album data.
    var albums = []album{
    	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
    }
    ```

A seguir, você escreverá código para implementar seu primeiro endpoint.

## Escrever um handler para retornar todos os itens {#all_items}

Quando o cliente faz uma requisição em `GET /albums`, você quer retornar todos os
álbuns como JSON.

Para fazer isso, você escreverá o seguinte:

*   Lógica para preparar uma resposta
*   Código para mapear o caminho da requisição para sua lógica

Note que isso é o inverso de como eles serão executados em tempo de execução, mas você está
adicionando dependências primeiro, então o código que depende delas.

#### Escrever o código

1. Abaixo do código de struct que você adicionou na seção anterior, cole o
    seguinte código para obter a lista de álbuns.

    Esta função `getAlbums` cria JSON a partir do slice de structs `album`,
    escrevendo o JSON na resposta.

    ```
    // getAlbums responds with the list of all albums as JSON.
    func getAlbums(c *gin.Context) {
    	c.IndentedJSON(http.StatusOK, albums)
    }
    ```

    Neste código, você:

    *   Escreve uma função `getAlbums` que recebe um
        parâmetro [`gin.Context`](https://pkg.go.dev/github.com/gin-gonic/gin#Context)
        . Note que você poderia ter dado a esta função qualquer nome – nem
        Gin nem Go requerem um formato de nome de função particular.

        `gin.Context` é a parte mais importante do Gin. Ela carrega detalhes de requisição
        , valida e serializa JSON, e mais. (Apesar do nome similar
        , isso é diferente do pacote [`context`](/pkg/context/) integrado do Go.)

    *   Chama [`Context.IndentedJSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.IndentedJSON)
        para serializar a struct em JSON e adicioná-la à resposta.

        O primeiro argumento da função é o código de status HTTP que você quer enviar para
        o cliente. Aqui, você está passando a constante [`StatusOK`](https://pkg.go.dev/net/http#StatusOK)
        do pacote `net/http` para indicar `200 OK`.

        Note que você pode substituir `Context.IndentedJSON` por uma chamada a
        [`Context.JSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.JSON)
        para enviar JSON mais compacto. Na prática, a forma indentada é muito mais fácil de
        trabalhar ao depurar e a diferença de tamanho é geralmente pequena.

2. Próximo ao topo de main.go, logo abaixo da declaração do slice `albums`, cole
    o código abaixo para atribuir a função handler a um caminho de endpoint.

    Isso configura uma associação na qual `getAlbums` trata requisições para o
    caminho de endpoint `/albums`.

    ```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)

    	router.Run("localhost:8080")
    }
    ```

    Neste código, você:

    *   Inicializa um router Gin usando
        [`Default`](https://pkg.go.dev/github.com/gin-gonic/gin#Default).
    *   Usa a função [`GET`](https://pkg.go.dev/github.com/gin-gonic/gin#RouterGroup.GET)
        para associar o método HTTP `GET` e o caminho `/albums` com uma função handler
        .

        Note que você está passando o _nome_ da função `getAlbums`. Isso é
        diferente de passar o _resultado_ da função, o que você faria
        passando `getAlbums()` (note os parênteses).

    *   Usa a função [`Run`](https://pkg.go.dev/github.com/gin-gonic/gin#Engine.Run)
        para anexar o router a um `http.Server` e iniciar o servidor.

3. Próximo ao topo de main.go, logo abaixo da declaração de package, importe os
    pacotes que você precisará para suportar o código que você acabou de escrever.

    As primeiras linhas de código devem ficar assim:

    ```
    package main

    import (
    	"net/http"

    	"github.com/gin-gonic/gin"
    )
    ```

4. Salve main.go.

#### Executar o código

1. Comece a rastrear o módulo Gin como uma dependência.

    Na linha de comando, use [`go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)
    para adicionar o módulo github.com/gin-gonic/gin como uma dependência para seu módulo.
    Use um argumento ponto para significar "obter dependências para código no
    diretório atual."

    ```
    $ go get .
    go get: added github.com/gin-gonic/gin v1.7.2
    ```

    Go resolveu e baixou esta dependência para satisfazer a declaração `import`
    que você adicionou no passo anterior.

2. Da linha de comando no diretório contendo main.go, execute o código.
    Use um argumento ponto para significar "executar código no diretório atual."

    ```
    $ go run .
    ```

    Uma vez que o código esteja rodando, você tem um servidor HTTP rodando para o qual pode
    enviar requisições.

3. De uma nova janela de linha de comando, use `curl` para fazer uma requisição ao seu
    serviço web em execução.

    ```
    $ curl http://localhost:8080/albums
    ```

    O comando deve exibir os dados com os quais você alimentou o serviço.

    ```
    [
            {
                    "id": "1",
                    "title": "Blue Train",
                    "artist": "John Coltrane",
                    "price": 56.99
            },
            {
                    "id": "2",
                    "title": "Jeru",
                    "artist": "Gerry Mulligan",
                    "price": 17.99
            },
            {
                    "id": "3",
                    "title": "Sarah Vaughan and Clifford Brown",
                    "artist": "Sarah Vaughan",
                    "price": 39.99
            }
    ]
    ```

Você iniciou uma API! Na próxima seção, você criará outro endpoint com
código para tratar uma requisição `POST` para adicionar um item.

## Escrever um handler para adicionar um novo item {#add_item}

Quando o cliente faz uma requisição `POST` em `/albums`, você quer adicionar o álbum
descrito no corpo da requisição aos dados de álbuns existentes.

Para fazer isso, você escreverá o seguinte:

*   Lógica para adicionar o novo álbum à lista existente.
*   Um pouco de código para rotear a requisição `POST` para sua lógica.

#### Escrever o código

1. Adicione código para adicionar dados de álbuns à lista de álbuns.

    Em algum lugar após as instruções `import`, cole o seguinte código. (O final
    do arquivo é um bom lugar para este código, mas Go não impõe a ordem
    na qual você declara funções.)

    ```
    // postAlbums adds an album from JSON received in the request body.
    func postAlbums(c *gin.Context) {
    	var newAlbum album

    	// Call BindJSON to bind the received JSON to
    	// newAlbum.
    	if err := c.BindJSON(&newAlbum); err != nil {
    		return
    	}

    	// Add the new album to the slice.
    	albums = append(albums, newAlbum)
    	c.IndentedJSON(http.StatusCreated, newAlbum)
    }
    ```

    Neste código, você:

    *   Usa [`Context.BindJSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.BindJSON)
        para vincular o corpo da requisição a `newAlbum`.
    *   Anexa a struct `album` inicializada a partir do JSON ao slice `albums`
        .
    *   Adiciona um código de status `201` à resposta, junto com JSON representando
        o álbum que você adicionou.

2. Altere sua função `main` para que ela inclua a função `router.POST`,
    como no seguinte.

    ```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.POST("/albums", postAlbums)

    	router.Run("localhost:8080")
    }
    ```

    Neste código, você:

    *   Associa o método `POST` no caminho `/albums` com a função `postAlbums`
        .

        Com Gin, você pode associar um handler com uma combinação de método HTTP e caminho
        . Desta forma, você pode rotear separadamente requisições enviadas para um
        único caminho baseado no método que o cliente está usando.

#### Executar o código

1. Se o servidor ainda estiver rodando da última seção, pare-o.
2. Da linha de comando no diretório contendo main.go, execute o código.

    ```
    $ go run .
    ```

3. De uma janela de linha de comando diferente, use `curl` para fazer uma requisição ao seu
    serviço web em execução.

    ```
    $ curl http://localhost:8080/albums \
        --include \
        --header "Content-Type: application/json" \
        --request "POST" \
        --data '{"id": "4","title": "The Modern Sound of Betty Carter","artist": "Betty Carter","price": 49.99}'
    ```

    O comando deve exibir cabeçalhos e JSON para o álbum adicionado.

    ```
    HTTP/1.1 201 Created
    Content-Type: application/json; charset=utf-8
    Date: Wed, 02 Jun 2021 00:34:12 GMT
    Content-Length: 116

    {
        "id": "4",
        "title": "The Modern Sound of Betty Carter",
        "artist": "Betty Carter",
        "price": 49.99
    }
    ```

4. Como na seção anterior, use `curl` para recuperar a lista completa de álbuns,
    que você pode usar para confirmar que o novo álbum foi adicionado.

    ```
    $ curl http://localhost:8080/albums \
        --header "Content-Type: application/json" \
        --request "GET"
    ```

    O comando deve exibir a lista de álbuns.

    ```
    [
            {
                    "id": "1",
                    "title": "Blue Train",
                    "artist": "John Coltrane",
                    "price": 56.99
            },
            {
                    "id": "2",
                    "title": "Jeru",
                    "artist": "Gerry Mulligan",
                    "price": 17.99
            },
            {
                    "id": "3",
                    "title": "Sarah Vaughan and Clifford Brown",
                    "artist": "Sarah Vaughan",
                    "price": 39.99
            },
            {
                    "id": "4",
                    "title": "The Modern Sound of Betty Carter",
                    "artist": "Betty Carter",
                    "price": 49.99
            }
    ]
    ```

Na próxima seção, você adicionará código para tratar um `GET` para um item específico.

## Escrever um handler para retornar um item específico {#specific_item}

Quando o cliente faz uma requisição para `GET /albums/[id]`, você quer retornar o
álbum cujo ID corresponde ao parâmetro de caminho `id`.

Para fazer isso, você vai:

*   Adicionar lógica para recuperar o álbum solicitado.
*   Mapear o caminho para a lógica.

#### Escrever o código

1. Abaixo da função `postAlbums` que você adicionou na seção anterior, cole
    o seguinte código para recuperar um álbum específico.

    Esta função `getAlbumByID` extrairá o ID no caminho da requisição, então
    localizará um álbum que corresponde.

    ```
    // getAlbumByID locates the album whose ID value matches the id
    // parameter sent by the client, then returns that album as a response.
    func getAlbumByID(c *gin.Context) {
    	id := c.Param("id")

    	// Loop over the list of albums, looking for
    	// an album whose ID value matches the parameter.
    	for _, a := range albums {
    		if a.ID == id {
    			c.IndentedJSON(http.StatusOK, a)
    			return
    		}
    	}
    	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
    }
    ```

    Neste código, você:

    *   Usa [`Context.Param`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.Param)
        para recuperar o parâmetro de caminho `id` da URL. Quando você mapear este
        handler para um caminho, você incluirá um placeholder para o parâmetro no
        caminho.
    *   Itera sobre as structs `album` no slice, procurando uma cujo campo `ID`
        corresponde ao valor do parâmetro `id`. Se for encontrada, você serializa
        aquela struct `album` para JSON e a retorna como uma resposta com um código
        HTTP `200 OK`.

        Como mencionado acima, um serviço do mundo real provavelmente usaria uma consulta de
        banco de dados para realizar esta busca.

    *   Retorna um erro HTTP `404` com [`http.StatusNotFound`](https://pkg.go.dev/net/http#StatusNotFound)
        se o álbum não for encontrado.

2. Finalmente, altere seu `main` para que ele inclua uma nova chamada a `router.GET`,
    onde o caminho agora é `/albums/:id`, como mostrado no seguinte exemplo.

    ```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.GET("/albums/:id", getAlbumByID)
    	router.POST("/albums", postAlbums)

    	router.Run("localhost:8080")
    }
    ```

    Neste código, você:

    *   Associa o caminho `/albums/:id` com a função `getAlbumByID`. No
        Gin, os dois pontos precedendo um item no caminho significam que o item é
        um parâmetro de caminho.

#### Executar o código

1. Se o servidor ainda estiver rodando da última seção, pare-o.
2. Da linha de comando no diretório contendo main.go, execute o código para
    iniciar o servidor.

    ```
    $ go run .
    ```

3. De uma janela de linha de comando diferente, use `curl` para fazer uma requisição ao seu
    serviço web em execução.

    ```
    $ curl http://localhost:8080/albums/2
    ```

    O comando deve exibir JSON para o álbum cujo ID você usou. Se o
    álbum não foi encontrado, você receberá JSON com uma mensagem de erro.

    ```
    {
            "id": "2",
            "title": "Jeru",
            "artist": "Gerry Mulligan",
            "price": 17.99
    }
    ```

## Conclusão {#conclusion}

Parabéns! Você acabou de usar Go e Gin para escrever um simples serviço web
RESTful.

Próximos tópicos sugeridos:

*   Se você é novo em Go, você encontrará práticas recomendadas úteis descritas em
    [Effective Go](/doc/effective_go) e
    [Como escrever código Go](/doc/code).
*   O [Go Tour](/tour/) é uma ótima introdução passo a passo
    aos fundamentos do Go.
*   Para mais sobre Gin, veja a [documentação do pacote Gin Web Framework](https://pkg.go.dev/github.com/gin-gonic/gin)
    ou a [documentação do Gin Web Framework](https://gin-gonic.com/en/docs/).

## Código completo {#completed_code}

Esta seção contém o código para o aplicativo que você constrói com este tutorial.

```
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// album represents data about a record album.
type album struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Artist string  `json:"artist"`
	Price  float64 `json:"price"`
}

// albums slice to seed record album data.
var albums = []album{
	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func main() {
	router := gin.Default()
	router.GET("/albums", getAlbums)
	router.GET("/albums/:id", getAlbumByID)
	router.POST("/albums", postAlbums)

	router.Run("localhost:8080")
}

// getAlbums responds with the list of all albums as JSON.
func getAlbums(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums adds an album from JSON received in the request body.
func postAlbums(c *gin.Context) {
	var newAlbum album

	// Call BindJSON to bind the received JSON to
	// newAlbum.
	if err := c.BindJSON(&newAlbum); err != nil {
		return
	}

	// Add the new album to the slice.
	albums = append(albums, newAlbum)
	c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID locates the album whose ID value matches the id
// parameter sent by the client, then returns that album as a response.
func getAlbumByID(c *gin.Context) {
	id := c.Param("id")

	// Loop through the list of albums, looking for
	// an album whose ID value matches the parameter.
	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}
```

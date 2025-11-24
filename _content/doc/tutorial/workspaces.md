---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Começando com workspaces multi-módulos",
  "Breadcrumb": true
}-->

Este tutorial introduz os fundamentos de workspaces multi-módulos em Go.
Com workspaces multi-módulos, você pode dizer ao comando Go que está
escrevendo código em múltiplos módulos ao mesmo tempo e facilmente construir e
executar código nesses módulos.

Neste tutorial, você criará dois módulos em um workspace multi-módulo
compartilhado, fará alterações nesses módulos, e verá os resultados
dessas alterações em uma construção.

<!-- TODO TOC -->

**Nota:** Para outros tutoriais, veja [Tutoriais](/doc/tutorial/index.html).

## Pré-requisitos

*   **Uma instalação do Go 1.18 ou posterior.**
*   **Uma ferramenta para editar seu código.** Qualquer editor de texto que você tenha funcionará bem.
*   **Um terminal de comando.** Go funciona bem usando qualquer terminal no Linux e Mac,
    e no PowerShell ou cmd no Windows.

Este tutorial requer go1.18 ou posterior. Certifique-se de ter instalado Go no Go 1.18 ou posterior usando os
links em [go.dev/dl](/dl).

## Criar um módulo para seu código {#create_folder}

Para começar, crie um módulo para o código que você escreverá.

1. Abra um prompt de comando e mude para seu diretório home.

   No Linux ou Mac:

    ```
    $ cd
    ```

   No Windows:

    ```
    C:\> cd %HOMEPATH%
    ```

   O resto do tutorial mostrará um $ como o prompt. Os comandos que você usa
   funcionarão no Windows também.

2. Do prompt de comando, crie um diretório para seu código chamado workspace.

    ```
    $ mkdir workspace
    $ cd workspace
    ```

3. Inicialize o módulo

   Nosso exemplo criará um novo módulo `hello` que dependerá do módulo golang.org/x/example.

   Crie o módulo hello:

   ```
   $ mkdir hello
   $ cd hello
   $ go mod init example.com/hello
   go: creating new go.mod: module example.com/hello
   ```

   Adicione uma dependência no pacote golang.org/x/example/hello/reverse usando `go get`.

   ```
   $ go get golang.org/x/example/hello/reverse
   ```

   Crie hello.go no diretório hello com os seguintes conteúdos:

   ```
   package main

   import (
       "fmt"

       "golang.org/x/example/hello/reverse"
   )

   func main() {
       fmt.Println(reverse.String("Hello"))
   }
   ```

   Agora, execute o programa hello:

   ```
   $ go run .
   olleH
   ```

## Criar o workspace

Neste passo, criaremos um arquivo `go.work` para especificar um workspace com o módulo.

#### Inicializar o workspace

No diretório `workspace`, execute:

   ```
   $ go work init ./hello
   ```

O comando `go work init` diz ao `go` para criar um arquivo `go.work`
para um workspace contendo os módulos no diretório `./hello`.

O comando `go` produz um arquivo `go.work` que se parece com isto:

   ```
   go 1.18

   use ./hello
   ```

O arquivo `go.work` tem sintaxe similar a `go.mod`.

A diretiva `go` diz ao Go qual versão do Go o arquivo deve ser
interpretado com. É similar à diretiva `go` no arquivo `go.mod`.

A diretiva `use` diz ao Go que o módulo no diretório `hello`
deve ser módulos principais ao fazer uma construção.

Então em qualquer subdiretório de `workspace` o módulo estará ativo.

#### Executar o programa no diretório workspace

No diretório `workspace`, execute:

   ```
   $ go run ./hello
   olleH
   ```

O comando Go inclui todos os módulos no workspace como módulos principais. Isso nos permite
referir a um pacote no módulo, mesmo fora do módulo. Executar o comando `go run`
fora do módulo ou do workspace resultaria em um erro porque o comando `go`
não saberia quais módulos usar.

A seguir, adicionaremos uma cópia local do módulo `golang.org/x/example/hello` ao workspace.
Esse módulo está armazenado em um subdiretório do repositório Git `go.googlesource.com/example`.
Então adicionaremos uma nova função ao pacote `reverse` que podemos usar em vez de `String`.

## Baixar e modificar o módulo `golang.org/x/example/hello`

   Neste passo, baixaremos uma cópia do repositório Git contendo o módulo `golang.org/x/example/hello`,
   adicionaremos ao workspace, e então adicionaremos uma nova função a ele que usaremos do programa hello.

1. Clone o repositório

   Do diretório workspace, execute o comando `git` para clonar o repositório:

   ```
   $ git clone https://go.googlesource.com/example
   Cloning into 'example'...
   remote: Total 165 (delta 27), reused 165 (delta 27)
   Receiving objects: 100% (165/165), 434.18 KiB | 1022.00 KiB/s, done.
   Resolving deltas: 100% (27/27), done.
   ```

2. Adicione o módulo ao workspace

   O repositório Git foi acabado de ser baixado em `./example`.
   O código fonte para o módulo `golang.org/x/example/hello` está em `./example/hello`.
   Adicione-o ao workspace:

   ```
   $ go work use ./example/hello
   ```

   O comando `go work use` adiciona um novo módulo ao arquivo go.work. Ele agora ficará assim:

   ```
   go 1.18

   use (
       ./hello
       ./example/hello
   )
   ```

   O workspace agora inclui tanto o módulo `example.com/hello` quanto o módulo `golang.org/x/example/hello`,
   que fornece o pacote `golang.org/x/example/hello/reverse`.

   Isso nos permitirá usar o novo código que escreveremos na nossa cópia do pacote `reverse`
   em vez da versão do pacote no cache de módulos
   que baixamos com o comando `go get`.

3. Adicione a nova função.

   Adicionaremos uma nova função para reverter um número ao pacote `golang.org/x/example/hello/reverse`.

   Crie um novo arquivo chamado `int.go` no diretório `workspace/example/hello/reverse` contendo os seguintes conteúdos:

   ```
   package reverse

   import "strconv"

   // Int returns the decimal reversal of the integer i.
   func Int(i int) int {
       i, _ = strconv.Atoi(String(strconv.Itoa(i)))
       return i
   }
   ```

4. Modifique o programa hello para usar a função.

   Modifique os conteúdos de `workspace/hello/hello.go` para conter os seguintes conteúdos:

   ```
   package main

   import (
       "fmt"

       "golang.org/x/example/hello/reverse"
   )

   func main() {
       fmt.Println(reverse.String("Hello"), reverse.Int(24601))
   }
   ```

#### Executar o código no diretório workspace

   Do diretório workspace, execute

   ```
   $ go run ./hello
   olleH 10642
   ```

   O comando Go encontra o módulo `example.com/hello` especificado na
   linha de comando no diretório `hello` especificado pelo arquivo `go.work`,
   e similarmente resolve o import `golang.org/x/example/hello/reverse` usando
   o arquivo `go.work`.

   `go.work` pode ser usado em vez de adicionar diretivas [`replace`](/ref/mod#go-mod-file-replace)
   para trabalhar em múltiplos módulos.

   Como os dois módulos estão no mesmo workspace é fácil
   fazer uma alteração em um módulo e usá-la em outro.

#### Próximo passo

   Agora, para lançar adequadamente esses módulos precisaríamos fazer um lançamento do módulo `golang.org/x/example/hello`,
   por exemplo em `v0.1.0`. Isso geralmente é feito marcando um commit no repositório de controle de versão do módulo.
   Veja a
   [documentação de workflow de lançamento de módulos](/doc/modules/release-workflow)
   para mais detalhes. Uma vez que o lançamento está feito, podemos aumentar o requisito no
   módulo `golang.org/x/example/hello` em `hello/go.mod`:

   ```
   cd hello
   go get golang.org/x/example/hello@v0.1.0
   ```

   Dessa forma, o comando `go` pode resolver adequadamente os módulos fora do workspace.

## Saiba mais sobre workspaces

   O comando `go` tem alguns subcomandos para trabalhar com workspaces além de `go work init` que
   vimos anteriormente no tutorial:

   - `go work use [-r] [dir]` adiciona uma diretiva `use` ao arquivo `go.work` para `dir`,
   se ele existir, e remove a diretiva `use` se o diretório argumento não existir. A flag `-r`
   examina subdiretórios de `dir` recursivamente.
   - `go work edit` edita o arquivo `go.work` similarmente a `go mod edit`
   - `go work sync` sincroniza dependências da lista de construção do workspace em cada um dos módulos do workspace.

   Veja [Workspaces](/ref/mod#workspaces) na Referência de Módulos Go para mais detalhes sobre
   workspaces e arquivos `go.work`.

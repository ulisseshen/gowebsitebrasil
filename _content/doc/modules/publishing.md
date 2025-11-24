<!--{
  "Title": "Publishing a module",
  "ia-translated": true
}-->

Quando você quer tornar um módulo disponível para outros desenvolvedores, você o publica para
que fique visível para as ferramentas Go. Uma vez que você publicou o módulo, desenvolvedores
importando seus packages poderão resolver uma dependência no módulo executando
comandos como `go get`.

> **Nota:** Não altere uma versão tagueada de um módulo após publicá-lo. Para
desenvolvedores usando o módulo, as ferramentas Go autenticam um módulo baixado contra
a primeira cópia baixada. Se as duas diferirem, as ferramentas Go retornarão um erro de
segurança. Em vez de alterar o código de uma versão previamente publicada, publique
uma nova versão.

**Veja também**

* Para uma visão geral do desenvolvimento de módulos, consulte [Developing and publishing
  modules](developing)
* Para um workflow de desenvolvimento de módulo de alto nível -- que inclui publicação --
  consulte [Module release and versioning workflow](release-workflow).

## Passos de publicação

Use os seguintes passos para publicar um módulo.

1. Abra um prompt de comando e mude para o diretório raiz do seu módulo no repositório
  local.

1.  Execute `go mod tidy`, que remove quaisquer dependências que o módulo possa ter
  acumulado que não são mais necessárias.

    ```
    $ go mod tidy
    ```

1.  Execute `go test ./...` uma última vez para garantir que tudo está funcionando.

    Isso executa os testes unitários que você escreveu para usar o framework de teste Go.

    ```
    $ go test ./...
    ok      example.com/mymodule       0.015s
    ```

1.  Tagueie o projeto com um novo número de versão usando o comando `git tag`.

    Para o número de versão, use um número que sinalize aos usuários a natureza das
    mudanças neste release. Para mais, consulte [Module version
    numbering](version-numbers).

    ```
    $ git commit -m "mymodule: changes for v0.1.0"
    $ git tag v0.1.0
    ```

1.  Faça push da nova tag para o repositório de origem.

    ```
    $ git push origin v0.1.0
    ```

1.  Torne o módulo disponível executando o comando [`go list`](/cmd/go/#hdr-List_packages_or_modules) para solicitar
  que o Go atualize seu índice de módulos com informações sobre o módulo que você está
  publicando.

    Preceda o comando com uma declaração para definir a variável de ambiente `GOPROXY`
    para um proxy Go. Isso garantirá que sua requisição chegue ao
    proxy.

    ```
    $ GOPROXY=proxy.golang.org go list -m example.com/mymodule@v0.1.0
    ```

Desenvolvedores interessados no seu módulo importam um package dele e executam o comando [`go
get`]() assim como fariam com qualquer outro módulo. Eles podem executar o comando [`go
get`]() para versões mais recentes ou podem especificar uma versão particular, como
no exemplo a seguir:

```
$ go get example.com/mymodule@v0.1.0
```

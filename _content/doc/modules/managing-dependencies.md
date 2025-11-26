<!--{
  "Title": "Managing dependencies",
  "ia-translated": true
}-->

Quando seu código usa packages externos, esses packages (distribuídos como módulos)
se tornam dependências. Com o tempo, você pode precisar atualizá-los ou substituí-los. Go
fornece ferramentas de gerenciamento de dependências que ajudam você a manter suas aplicações Go
seguras conforme você incorpora dependências externas.

Este tópico descreve como executar tarefas para gerenciar dependências que você assume no
seu código. Você pode executar a maioria delas com ferramentas Go. Este tópico também
descreve como executar algumas outras tarefas relacionadas a dependências que você pode achar
úteis.

**Veja também**

*   Se você é novo em trabalhar com dependências como módulos, dê uma olhada no
    [Tutorial Getting started](/doc/tutorial/getting-started)
    para uma breve introdução.
*   Usar o comando `go` para gerenciar dependências ajuda a garantir que seus
    requisitos permaneçam consistentes e o conteúdo do seu arquivo go.mod seja válido.
    Para referência sobre os comandos, consulte [Command go](/cmd/go/).
    Você também pode obter ajuda da linha de comando digitando `go help`
    _command-name_, como em `go help mod tidy`.
*   Comandos Go que você usa para fazer mudanças de dependência editam seu arquivo go.mod. Para
    mais sobre o conteúdo do arquivo, consulte [go.mod file reference](/doc/modules/gomod-ref).
*   Tornar seu editor ou IDE ciente dos módulos Go pode facilitar o trabalho de gerenciá-los.
    Para mais sobre editores que suportam Go, consulte [Editor plugins and
    IDEs](/doc/editors.html).
*   Este tópico não descreve como desenvolver, publicar e versionar módulos para
    outros usarem. Para mais sobre isso, consulte [Developing and publishing
    modules](developing).

## Workflow para usar e gerenciar dependências {#workflow}

Você pode obter e usar packages úteis com ferramentas Go. Em
[pkg.go.dev](https://pkg.go.dev), você pode pesquisar packages que você pode achar
úteis, depois usar o comando `go` para importar esses packages no seu próprio código para
chamar suas funções.

A lista a seguir apresenta os passos mais comuns de gerenciamento de dependências. Para mais sobre
cada um, consulte as seções neste tópico.

1. [Localizar packages úteis](#locating_packages) em [pkg.go.dev](https://pkg.go.dev).
1. [Importar os packages](#locating_packages) que você quer no seu código.
1. Adicionar seu código a um módulo para rastreamento de dependências (se ainda não estiver em um módulo).
    Consulte [Enabling dependency tracking](#enable_tracking)
1. [Adicionar packages externos como dependências](#adding_dependency) para que você possa gerenciá-los.
1. [Atualizar ou fazer downgrade de versões de dependência](#upgrading) conforme necessário ao longo do tempo.

## Gerenciando dependências como módulos {#modules}

Em Go, você gerencia dependências como módulos que contêm os packages que você importa.
Este processo é suportado por:

*   Um **sistema descentralizado para publicar** módulos e recuperar seu código.
    Desenvolvedores disponibilizam seus módulos para outros desenvolvedores usarem de
    seu próprio repositório e publicam com um número de versão.
*   Um **motor de busca de packages** e navegador de documentação (pkg.go.dev) no qual
    você pode encontrar módulos. Consulte [Locating and importing useful packages](#locating_packages).
*   Uma **convenção de numeração de versão de módulo** para ajudá-lo a entender a
    estabilidade de um módulo e garantias de compatibilidade retroativa. Consulte [Module version
    numbering](version-numbers).
*   **Ferramentas Go** que facilitam para você gerenciar dependências, incluindo
    obter o código-fonte de um módulo, atualizar, e assim por diante. Consulte seções deste tópico
    para mais.

## Localizando e importando packages úteis {#locating_packages}

Você pode pesquisar em [pkg.go.dev](https://pkg.go.dev) para encontrar packages com funções
que você pode achar úteis.

Quando você encontrou um package que você quer usar no seu código, localize o caminho do package
no topo da página e clique no botão Copy path para copiar o caminho para
sua área de transferência. No seu próprio código, cole o caminho em um statement import, como no
exemplo a seguir:

```
import "rsc.io/quote"
```

Após seu código importar o package, habilite o rastreamento de dependências e obtenha o
código do package para compilar. Para mais, consulte [Enabling dependency tracking in
your code](#enable_tracking) e [Adding a dependency](#adding_dependency).

## Habilitando rastreamento de dependências no seu código {#enable_tracking}

Para rastrear e gerenciar as dependências que você adiciona, você começa colocando seu código no
seu próprio módulo. Isso cria um arquivo go.mod na raiz da sua árvore de código-fonte.
Dependências que você adicionar serão listadas nesse arquivo.

Para adicionar seu código ao seu próprio módulo, use o
comando [`go mod init`](/ref/mod#go-mod-init). Por exemplo, da linha de
comando, mude para o diretório raiz do seu código, depois execute o comando como no
exemplo a seguir:

```
$ go mod init example/mymodule
```

O argumento do comando `go mod init` é o caminho do módulo do seu módulo. Se possível,
o caminho do módulo deve ser o local do repositório do seu código-fonte.

Se no início você não souber o local eventual do repositório do módulo, use um
substituto seguro. Isso pode ser o nome de um domínio que você possui ou outro nome que você
controla (como o nome da sua empresa), junto com um caminho seguindo do
nome do módulo ou diretório de código-fonte. Para mais, consulte
[Naming a module](#naming_module).

Conforme você usa ferramentas Go para gerenciar dependências, as ferramentas atualizam o arquivo go.mod para
que ele mantenha uma lista atual de suas dependências.

Quando você adiciona dependências, as ferramentas Go também criam um arquivo go.sum que contém
checksums dos módulos dos quais você depende. Go usa isso para verificar a integridade dos
arquivos de módulo baixados, especialmente para outros desenvolvedores trabalhando no seu
projeto.

Inclua os arquivos go.mod e go.sum no seu repositório com seu código.

Consulte a [referência go.mod](/doc/modules/gomod-ref) para mais.

## Nomeando um módulo {#naming_module}

Quando você executa `go mod init` para criar um módulo para rastreamento de dependências, você
especifica um caminho de módulo que serve como o nome do módulo. O caminho do módulo
se torna o prefixo de caminho de import para packages no módulo. Certifique-se de especificar
um caminho de módulo que não entrará em conflito com o caminho de módulo de outros módulos.

No mínimo, um caminho de módulo precisa apenas indicar algo sobre sua origem, como
uma empresa, autor ou nome de proprietário. Mas o caminho também pode ser mais
descritivo sobre o que o módulo é ou faz.

O caminho do módulo é tipicamente da seguinte forma:

```
<prefix>/<descriptive-text>
```

* O _prefix_ é tipicamente uma string que descreve parcialmente o módulo, como
    uma string que descreve sua origem. Isso pode ser:

    *   O local do repositório onde as ferramentas Go podem encontrar o código-fonte do módulo
        (obrigatório se você está publicando o módulo).

        Por exemplo, pode ser `github.com/<project-name>/`.

        Use esta melhor prática se você acha que pode publicar o módulo para
        outros usarem. Para mais sobre publicação, consulte
        [Developing and publishing modules](/doc/modules/developing).

    *   Um nome que você controla.

        Se você não está usando um nome de repositório, certifique-se de escolher um prefixo que
        você esteja confiante de que não será usado por outros. Uma boa escolha é o
        nome da sua empresa. Evite termos comuns como `widgets`, `utilities`, ou
        `app`.

* Para o _descriptive text_, uma boa escolha seria um nome de projeto. Lembre-se
    de que nomes de packages carregam a maior parte do peso de descrever funcionalidade.
    O caminho do módulo cria um namespace para esses nomes de packages.

**Prefixos de caminho de módulo reservados**

Go garante que as seguintes strings não serão usadas em nomes de packages.

- `test` -- Você pode usar `test` como um prefixo de caminho de módulo para um módulo cujo código
    é projetado para testar localmente funções em outro módulo.

    Use o prefixo de caminho `test` para módulos que são criados como parte de um teste.
    Por exemplo, seu próprio teste pode executar `go mod init test` e depois configurar
    esse módulo de alguma maneira particular para testar com uma ferramenta de análise de código-fonte Go.

- `example` -- Usado como um prefixo de caminho de módulo em alguma documentação Go, como
    em tutoriais onde você está criando um módulo apenas para rastrear dependências.

    Observe que a documentação Go também usa `example.com` para ilustrar quando o
    exemplo pode ser um módulo publicado.

## Adicionando uma dependência {#adding_dependency}

Uma vez que você está importando packages de um módulo publicado, você pode adicionar esse módulo
para gerenciar como uma dependência usando o [comando `go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them).

O comando faz o seguinte:

*   Se necessário, adiciona diretivas `require` ao seu arquivo go.mod para módulos
    necessários para compilar packages nomeados na linha de comando. Uma diretiva `require`
    rastreia a versão mínima de um módulo do qual seu módulo depende. Consulte a
    [referência go.mod](/doc/modules/gomod-ref) para mais.
*   Se necessário, baixa código-fonte de módulos para que você possa compilar packages que
    dependem deles. Pode baixar módulos de um proxy de módulos como
    proxy.golang.org ou diretamente de repositórios de controle de versão. O código-fonte
    é armazenado em cache localmente.

    Você pode definir o local de onde as ferramentas Go baixam módulos. Para mais, consulte
    [Specifying a module proxy server](#proxy_server).

Os exemplos a seguir descrevem alguns casos.

*   Para adicionar todas as dependências para um package no seu módulo, execute um comando como o
    abaixo ("." refere-se ao package no diretório atual):

    ```
    $ go get .
    ```

*   Para adicionar uma dependência específica, especifique seu caminho de módulo como um argumento para o
    comando.

    ```
    $ go get example.com/theirmodule
    ```

O comando também autentica cada módulo que baixa. Isso garante que ele está
inalterado desde quando o módulo foi publicado. Se o módulo mudou desde que foi
publicado -- por exemplo, o desenvolvedor mudou o conteúdo do commit
-- ferramentas Go apresentarão um erro de segurança. Essa verificação de autenticação protege
você de módulos que podem ter sido adulterados.

## Obtendo uma versão de dependência específica {#getting_version}

Você pode obter uma versão específica de um módulo de dependência especificando sua versão
no comando `go get`. O comando atualiza a diretiva `require` no seu
arquivo go.mod (embora você também possa atualizá-la manualmente).

Você pode querer fazer isso se:

*   Você quer obter uma versão de pré-lançamento específica de um módulo para experimentar.
*   Você descobriu que a versão que você está exigindo atualmente não está funcionando
    para você, então você quer obter uma versão que você sabe que pode confiar.
*   Você quer atualizar ou fazer downgrade de um módulo que você já está exigindo.

Aqui estão exemplos para usar o [comando `go get`](/ref/mod#go-get):

*   Para obter uma versão numerada específica, anexe o caminho do módulo com um sinal @ seguido da versão que você quer:

    ```
    $ go get example.com/theirmodule@v1.3.4
    ```

*   Para obter a versão mais recente, anexe o caminho do módulo com `@latest`:

    ```
    $ go get example.com/theirmodule@latest
    ```

O exemplo de diretiva `require` do arquivo go.mod a seguir (consulte a [referência
go.mod](/doc/modules/gomod-ref) para mais) ilustra como exigir um número de versão específico:

```
require example.com/theirmodule v1.3.4
```

## Descobrindo atualizações disponíveis {#discovering_updates}

Você pode verificar se há versões mais recentes de dependências que você já está
usando no seu módulo atual. Use o comando `go list` para exibir uma lista de
dependências do seu módulo, junto com a versão mais recente disponível para aquele
módulo. Uma vez que você descobriu atualizações disponíveis, você pode experimentá-las com seu
código para decidir se atualizar ou não para novas versões.

Para mais sobre o comando `go list`, consulte [`go list -m`](/ref/mod#go-list-m).

Aqui estão alguns exemplos.

*   Listar todos os módulos que são dependências do seu módulo atual,
    junto com a versão mais recente disponível para cada:

    ```
    $ go list -m -u all
    ```

*   Exibir a versão mais recente disponível para um módulo específico:

    ```
    $ go list -m -u example.com/theirmodule
    ```

## Atualizando ou fazendo downgrade de uma dependência {#upgrading}

Você pode atualizar ou fazer downgrade de um módulo de dependência usando ferramentas Go para descobrir
versões disponíveis, depois adicionar uma versão diferente como uma dependência.

1. Para descobrir novas versões use o comando `go list` como descrito em
    [Discovering available updates](#discovering_updates).

1. Para adicionar uma versão particular como uma dependência, use o comando `go get` como
    descrito em [Getting a specific dependency version](#getting_version).

## Sincronizando as dependências do seu código {#synchronizing}

Você pode garantir que está gerenciando dependências para todos os packages importados do seu código
enquanto também remove dependências para packages que você não está mais
importando.

Isso pode ser útil quando você esteve fazendo mudanças no seu código e
dependências, possivelmente criando uma coleção de dependências gerenciadas e
módulos baixados que não correspondem mais à coleção especificamente exigida pelos
packages importados no seu código.

Para manter seu conjunto de dependências gerenciadas organizado, use o comando `go mod tidy`. Usando
o conjunto de packages importados no seu código, este comando edita seu arquivo go.mod
para adicionar módulos que são necessários mas ausentes. Ele também remove módulos não usados
que não fornecem quaisquer packages relevantes.

O comando não tem argumentos exceto por uma flag, -v, que imprime informação
sobre módulos removidos.

```
$ go mod tidy
```

## Desenvolvendo e testando contra código de módulo não publicado {#unpublished}

Você pode especificar que seu código deve usar módulos de dependência que podem não estar
publicados. O código para esses módulos pode estar em seus respectivos repositórios,
em um fork desses repositórios, ou em um drive com o módulo atual que
os consome.

Você pode querer fazer isso quando:

*   Você quer fazer suas próprias mudanças no código de um módulo externo, como
    depois de fazer fork e/ou cloná-lo. Por exemplo, você pode querer preparar uma
    correção para o módulo, depois enviá-la como um pull request para o desenvolvedor do módulo.
*   Você está construindo um novo módulo e ainda não o publicou, então ele está
    indisponível em um repositório onde o comando `go get` pode alcançá-lo.

### Exigindo código de módulo em um diretório local {#local_directory}

Você pode especificar que o código para um módulo exigido está no mesmo drive local
que o código que o exige. Você pode achar isso útil quando você está:

*   Desenvolvendo seu próprio módulo separado e quer testar do módulo atual.
*   Corrigindo problemas em ou adicionando funcionalidades a um módulo externo e quer testar
    do módulo atual. (Observe que você também pode exigir o módulo externo
    do seu próprio fork do repositório dele. Para mais, consulte [Requiring external
    module code from your own repository fork](#external_fork).)

Para dizer às ferramentas Go para usar a cópia local do código do módulo, use a
diretiva `replace` no seu arquivo go.mod para substituir o caminho do módulo dado em uma
diretiva `require`. Consulte a [referência go.mod](/doc/modules/gomod-ref) para
mais sobre diretivas.

No exemplo de arquivo go.mod a seguir, o módulo atual exige o módulo externo
`example.com/theirmodule`, com um número de versão inexistente
(`v0.0.0-unpublished`) usado para garantir que a substituição funcione corretamente. A
diretiva `replace` então substitui o caminho do módulo original com
`../theirmodule`, um diretório que está no mesmo nível que o diretório do módulo atual.

```
module example.com/mymodule

go 1.23.0

require example.com/theirmodule v0.0.0-unpublished

replace example.com/theirmodule v0.0.0-unpublished => ../theirmodule
```

Ao configurar um par `require`/`replace`, use os
comandos [`go mod edit`](/ref/mod#go-mod-edit) e [`go get`](/ref/mod#go-get)
para garantir que os requisitos descritos pelo arquivo permaneçam consistentes:

```
$ go mod edit -replace=example.com/theirmodule@v0.0.0-unpublished=../theirmodule
$ go get example.com/theirmodule@v0.0.0-unpublished
```

**Nota:** Quando você usa a diretiva replace, as ferramentas Go não autenticam
módulos externos como descrito em [Adding a dependency](#adding_dependency).

Para mais sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

### Exigindo código de módulo externo do seu próprio fork de repositório {#external_fork}

Quando você fez fork do repositório de um módulo externo (como para corrigir um problema no
código do módulo ou para adicionar uma funcionalidade), você pode fazer as ferramentas Go usarem seu fork para
o código-fonte do módulo. Isso pode ser útil para testar mudanças do seu próprio código.
(Observe que você também pode exigir o código do módulo em um diretório que está no
drive local com o módulo que o exige. Para mais, consulte [Requiring module
code in a local directory](#local_directory).)

Você faz isso usando uma diretiva `replace` no seu arquivo go.mod para substituir o
caminho do módulo original do módulo externo com um caminho para o fork no seu
repositório. Isso direciona as ferramentas Go para usar o caminho de substituição (a localização do fork)
ao compilar, por exemplo, enquanto permite que você deixe statements `import`
inalterados do caminho do módulo original.

Para mais sobre a diretiva `replace`, consulte a [referência do arquivo
go.mod](gomod-ref).

No exemplo de arquivo go.mod a seguir, o módulo atual exige o módulo externo
`example.com/theirmodule`. A diretiva `replace` então substitui o
caminho do módulo original com `example.com/myfork/theirmodule`, um fork do
próprio repositório do módulo.

```
module example.com/mymodule

go 1.23.0

require example.com/theirmodule v1.2.3

replace example.com/theirmodule v1.2.3 => example.com/myfork/theirmodule v1.2.3-fixed
```

Ao configurar um par `require`/`replace`, use comandos de ferramenta Go para garantir que
requisitos descritos pelo arquivo permaneçam consistentes. Use o comando [`go
list`](/ref/mod#go-list-m) para obter a versão em uso pelo módulo atual.
Depois use o comando [`go mod edit`](/ref/mod#go-mod-edit) para substituir
o módulo exigido com o fork:

```
$ go list -m example.com/theirmodule
example.com/theirmodule v1.2.3
$ go mod edit -replace=example.com/theirmodule@v1.2.3=example.com/myfork/theirmodule@v1.2.3-fixed
```

**Nota:** Quando você usa a diretiva `replace`, as ferramentas Go não autenticam
módulos externos como descrito em [Adding a dependency](#adding_dependency).

Para mais sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

## Obtendo um commit específico usando um identificador de repositório {#repo_identifier}

Você pode usar o comando `go get` para adicionar código não publicado para um módulo de um
commit específico no seu repositório.

Para fazer isso, você usa o comando `go get`, especificando o código que você quer com um
sinal `@`. Quando você usa `go get`, o comando adicionará ao seu arquivo go.mod uma
diretiva `require` que exige o módulo externo, usando um número de pseudo-versão
baseado em detalhes sobre o commit.

Os exemplos a seguir fornecem algumas ilustrações. Estes são baseados em um módulo
cujo código-fonte está em um repositório git.

*   Para obter o módulo em um commit específico, anexe a forma @<em>commithash</em>:

    ```
    $ go get example.com/theirmodule@4cf76c2
    ```

*   Para obter o módulo em um branch específico, anexe a forma @<em>branchname</em>:

    ```
    $ go get example.com/theirmodule@bugfixes
    ```

## Removendo uma dependência {#removing_dependency}

Quando seu código não usa mais nenhum package em um módulo, você pode parar de rastrear
o módulo como uma dependência.

Para parar de rastrear todos os módulos não usados, execute o [comando `go mod tidy`](/ref/mod#go-mod-tidy). Este comando também pode adicionar dependências ausentes
necessárias para compilar packages no seu módulo.

```
$ go mod tidy
```

Para remover uma dependência específica, use o [comando `go get`](/ref/mod#go-get), especificando o caminho do módulo do módulo e anexando
`@none`, como no exemplo a seguir:

```
$ go get example.com/theirmodule@none
```

O comando `go get` também fará downgrade ou removerá outras dependências que
dependem do módulo removido.

## Dependências de ferramentas {#tools}

Dependências de ferramentas permitem que você gerencie ferramentas de desenvolvedor que são escritas em Go e usadas
ao trabalhar no seu módulo. Por exemplo, você pode usar
[`stringer`](https://pkg.go.dev/golang.org/x/tools/cmd/stringer) com [`go
generate`](/blog/generate), ou um linter ou formatador específico como parte de
preparar sua mudança para submissão.

No Go 1.24 e acima, você pode adicionar uma dependência de ferramenta com:

```
$ go get -tool golang.org/x/tools/cmd/stringer
```

Isso adicionará uma [diretiva `tool`](/ref/mod/#go-mod-file-tool) ao seu arquivo `go.mod`, e garantirá que as
diretivas require necessárias estejam presentes. Uma vez que esta diretiva for adicionada, você pode
executar a ferramenta passando o último componente [non-major-version](/ref/mod#major-version-suffixes)
do caminho de import da ferramenta para `go tool`:

```
$ go tool stringer
```

No caso de múltiplas ferramentas compartilharem o último fragmento de caminho, ou o fragmento de caminho
corresponder a uma das ferramentas enviadas com a distribuição Go, você deve passar o
caminho completo do package em vez disso:

```
$ go tool golang.org/x/tools/cmd/stringer
```

Para ver uma lista de todas as ferramentas atualmente disponíveis, execute `go tool` sem argumentos:

```
$ go tool
```

Você pode adicionar manualmente uma diretiva `tool` ao seu `go.mod`, mas deve garantir
que haja uma diretiva `require` para o módulo que define a ferramenta. A
maneira mais fácil de adicionar quaisquer diretivas `require` faltantes é executar:

```
$ go mod tidy
```

Requisitos necessários para satisfazer dependências de ferramentas se comportam como quaisquer outros
requisitos no seu [grafo de módulos](/ref/mod#glos-module-graph). Eles
participam da [seleção de versão mínima](/ref/mod#minimal-version-selection)
e respeitam diretivas `require`, `replace` e `exclude`. Devido ao
pruning de módulos, quando você depende de um módulo que em si tem uma dependência de ferramenta,
requisitos que existem apenas para satisfazer essa dependência de ferramenta normalmente não
se tornam requisitos do seu módulo.

O [meta-padrão](/cmd/go#hdr-Package_lists_and_patterns) `tool` fornece uma maneira de executar operações em todas as ferramentas simultaneamente. Por exemplo, você pode atualizar todas as ferramentas com `go get -u tool`, ou instalá-las todas em $GOBIN com `go install tool`.

Em versões Go antes de 1.24, você pode alcançar algo similar a uma diretiva `tool`
adicionando um blank import a um arquivo go dentro do módulo que é
excluído da compilação usando [build
constraints](/pkg/go/build/#hdr-Build_Constraints). Se você fizer isso, pode então
usar `go run` com o caminho completo do package para executar a ferramenta.

## Especificando um servidor proxy de módulos {#proxy_server}

Quando você usa ferramentas Go para trabalhar com módulos, as ferramentas por padrão baixam
módulos de proxy.golang.org (um espelho de módulos público operado pelo Google) ou diretamente
do repositório do módulo. Você pode especificar que as ferramentas Go devem em vez disso usar
outro servidor proxy para baixar e autenticar módulos.

Você pode querer fazer isso se você (ou sua equipe) configurou ou escolheu um
servidor proxy de módulos diferente que você quer usar. Por exemplo, alguns configuram um
servidor proxy de módulos para ter maior controle sobre como dependências são
usadas.

Para especificar outro servidor proxy de módulos para ferramentas Go usarem, defina a variável de
ambiente `GOPROXY` para a URL de um ou mais servidores. Ferramentas Go tentarão cada
URL na ordem que você especificar. Por padrão, `GOPROXY` especifica um
proxy de módulos público operado pelo Google primeiro, depois download direto do repositório do módulo
(conforme especificado no seu caminho de módulo):

```
GOPROXY="https://proxy.golang.org,direct"
```

Para mais sobre a variável de ambiente `GOPROXY`, incluindo valores para suportar
outro comportamento, consulte a [referência do comando
`go`](/cmd/go/#hdr-Module_downloading_and_verification).

Você pode definir a variável para URLs de outros servidores proxy de módulos, separando URLs
com uma vírgula ou um pipe.

*   Quando você usa uma vírgula, ferramentas Go tentarão a próxima URL na lista apenas se a
    URL atual retornar um HTTP 404 ou 410.

    ```
    GOPROXY="https://proxy.example.com,https://proxy2.example.com"
    ```

*   Quando você usa um pipe, ferramentas Go tentarão a próxima URL na lista independentemente
    do código de erro HTTP.

    ```
    GOPROXY="https://proxy.example.com|https://proxy2.example.com"
    ```


Módulos Go são frequentemente desenvolvidos e distribuídos em servidores de controle de versão
e proxies de módulos que não estão disponíveis na internet pública. Você pode definir a
variável de ambiente `GOPRIVATE` para configurar o comando `go`
para baixar e compilar módulos de fontes privadas.
Então o comando go pode baixar e compilar módulos de fontes privadas.

As variáveis de ambiente `GOPRIVATE` ou `GONOPROXY` podem ser definidas para listas de padrões glob
correspondendo a prefixos de módulo que são privados e não devem ser solicitados
de nenhum proxy. Por exemplo:

```
GOPRIVATE=*.corp.example.com,*.research.example.com
```

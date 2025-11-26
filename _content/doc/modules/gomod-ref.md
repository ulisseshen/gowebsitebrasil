<!--{
  "Title": "go.mod file reference",
  "ia-translated": true
}-->

Cada módulo Go é definido por um arquivo go.mod que descreve as
propriedades do módulo, incluindo suas dependências em outros módulos e em versões do Go.

Essas propriedades incluem:

* O **caminho do módulo** do módulo atual. Este deve ser um local de onde
o módulo pode ser baixado pelas ferramentas Go, como o local do repositório
do código do módulo. Isso serve como um identificador único, quando combinado
com o número de versão do módulo. Também é o prefixo do caminho do package para
todos os packages no módulo. Para mais sobre como Go localiza o módulo, consulte a
<a href="/ref/mod#vcs-find">Referência de Módulos Go</a>.
* A **versão mínima do Go** exigida pelo módulo atual.
* Uma lista de versões mínimas de outros **módulos exigidos** pelo módulo atual.
* Instruções, opcionalmente, para **substituir** um módulo exigido com outro
  módulo versão ou um diretório local, ou para **excluir** uma versão específica de
  um módulo exigido.

Go gera um arquivo go.mod quando você executa o [comando `go mod init`](/ref/mod#go-mod-init). O exemplo a seguir cria um arquivo go.mod,
definindo o caminho do módulo do módulo para example/mymodule:

```
$ go mod init example/mymodule
```

Use comandos `go` para gerenciar dependências. Os comandos garantem que os
requisitos descritos no seu arquivo go.mod permaneçam consistentes e o conteúdo do
seu arquivo go.mod seja válido. Esses comandos incluem os comandos [`go get`](/ref/mod#go-get)
e [`go mod tidy`](/ref/mod#go-mod-tidy) e [`go mod edit`](/ref/mod#go-mod-edit).

Para referência sobre comandos `go`, consulte [Command go](/cmd/go/).
Você pode obter ajuda da linha de comando digitando `go help` _command-name_, como
em `go help mod tidy`.

**Veja também**

* Ferramentas Go fazem mudanças no seu arquivo go.mod conforme você as usa para gerenciar
  dependências. Para mais, consulte [Managing dependencies](/doc/modules/managing-dependencies).
* Para mais detalhes e restrições relacionadas a arquivos go.mod, consulte a [referência de
  módulos Go](/ref/mod#go-mod-file).

## Exemplo {#example}

Um arquivo go.mod inclui diretivas como mostrado no exemplo a seguir. Estas são
descritas em outro lugar neste tópico.

```
module example.com/mymodule

go 1.14

require (
    example.com/othermodule v1.2.3
    example.com/thismodule v1.2.3
    example.com/thatmodule v1.2.3
)

replace example.com/thatmodule => ../thatmodule
exclude example.com/thismodule v1.3.0
```

## module {#module}

Declara o caminho do módulo do módulo, que é o identificador único do módulo
(quando combinado com o número de versão do módulo). O caminho do módulo se torna o
prefixo de import para todos os packages que o módulo contém.

Para mais, consulte [diretiva `module`](/ref/mod#go-mod-file-module) na
Referência de Módulos Go.

### Sintaxe {#module-syntax}

<pre>module <var>module-path</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>O caminho do módulo do módulo, geralmente o local do repositório de onde
      o módulo pode ser baixado pelas ferramentas Go. Para versões de módulo v2 e
      posteriores, este valor deve terminar com o número de versão major, como
      <code>/v2</code>.</dd>
</dl>

### Exemplos {#module-examples}

Os exemplos a seguir substituem `example.com` por um domínio de repositório de onde
o módulo poderia ser baixado.

* Declaração de módulo para um módulo v0 ou v1:
  ```
  module example.com/mymodule
  ```
* Caminho de módulo para um módulo v2:
  ```
  module example.com/mymodule/v2
  ```

### Notas {#module-notes}

O caminho do módulo deve identificar seu módulo de forma única. Para a maioria dos módulos, o caminho
é uma URL onde o comando `go` pode encontrar o código (ou um redirecionamento para o código).
Para módulos que nunca serão baixados diretamente, o caminho do módulo
pode ser apenas algum nome que você controle que garantirá unicidade. O prefixo
`example/` também é reservado para uso em exemplos como estes.

Para mais detalhes, consulte [Managing dependencies](/doc/modules/managing-dependencies#naming_module).

Na prática, o caminho do módulo é tipicamente o domínio do repositório de código-fonte do módulo
e o caminho para o código do módulo dentro do repositório. O comando `go`
depende desta forma ao baixar versões de módulo para resolver dependências
em nome do usuário do módulo.

Mesmo se você não estiver inicialmente pretendendo disponibilizar seu módulo para uso
de outro código, usar o caminho do repositório é uma melhor prática que ajudará
você a evitar ter que renomear o módulo se você publicá-lo mais tarde.

Se no início você não souber o local eventual do repositório do módulo, considere
usar temporariamente um substituto seguro, como o nome de um domínio que você possui ou
um nome que você controle (como o nome da sua empresa), junto com um caminho seguindo
do nome do módulo ou diretório de código-fonte. Para mais, consulte
[Managing dependencies](/doc/modules/managing-dependencies#naming_module).

Por exemplo, se você está desenvolvendo em um diretório `stringtools`, seu caminho de
módulo temporário pode ser `<company-name>/stringtools`, como no exemplo a seguir,
onde _company-name_ é o nome da sua empresa:

```
go mod init <company-name>/stringtools
```

## go {#go}

Indica que o módulo foi escrito assumindo a semântica da versão do Go
especificada pela diretiva.

Para mais, consulte [diretiva `go`](/ref/mod#go-mod-file-go) na
Referência de Módulos Go.

### Sintaxe {#go-syntax}

<pre>go <var>minimum-go-version</var></pre>

<dl>
    <dt>minimum-go-version</dt>
    <dd>A versão mínima do Go exigida para compilar packages neste módulo.</dd>
</dl>

### Exemplos {#go-examples}

* Módulo deve executar no Go versão 1.14 ou posterior:
  ```
  go 1.14
  ```

### Notas {#go-notes}

A diretiva `go` define a versão mínima do Go exigida para usar este módulo.
Antes do Go 1.21, a diretiva era apenas consultiva; agora é um requisito obrigatório:
toolchains Go recusam usar módulos declarando versões Go mais recentes.

A diretiva `go` é uma entrada para selecionar qual toolchain Go executar.
Consulte "[Go toolchains](/doc/toolchain)" para detalhes.

A diretiva `go` afeta o uso de novos recursos de linguagem:

* Para packages dentro do módulo, o compilador rejeita uso de recursos de linguagem
  introduzidos após a versão especificada pela diretiva `go`. Por exemplo, se
  um módulo tem a diretiva `go 1.12`, seus packages não podem usar literais
  numéricos como `1_000_000`, que foram introduzidos no Go 1.13.
* Se uma versão mais antiga do Go compila um dos packages do módulo e encontra um
  erro de compilação, o erro nota que o módulo foi escrito para uma versão Go mais recente.
  Por exemplo, suponha que um módulo tenha `go 1.13` e um package use o
  literal numérico `1_000_000`. Se aquele package for compilado com Go 1.12, o
  compilador nota que o código foi escrito para Go 1.13.

A diretiva `go` também afeta o comportamento do comando `go`:

* Em `go 1.14` ou superior, [vendoring](/ref/mod#vendoring) automático pode ser
  habilitado. Se o arquivo `vendor/modules.txt` estiver presente e consistente com
  `go.mod`, não há necessidade de usar explicitamente a flag `-mod=vendor`.
* Em `go 1.16` ou superior, o padrão de package `all` corresponde apenas packages
  importados transitivamente por packages e testes no [módulo
  main](/ref/mod#glos-main-module). Este é o mesmo conjunto de packages mantidos
  por [`go mod vendor`](/ref/mod#go-mod-vendor) desde que módulos foram introduzidos. Em
  versões inferiores, `all` também inclui testes de packages importados por packages no
  módulo main, testes desses packages, e assim por diante.
* Em `go 1.17` ou superior:
   * O arquivo `go.mod` inclui uma diretiva [`require`
     ](/ref/mod#go-mod-file-require) explícita para cada módulo que fornece qualquer
     package importado transitivamente por um package ou teste no módulo main. (Em
     `go 1.16` e inferior, uma dependência indireta é incluída apenas se [seleção de
     versão mínima](/ref/mod#minimal-version-selection) de outra forma
     selecionaria uma versão diferente.) Esta informação extra habilita [poda de
     grafo de módulos](/ref/mod#graph-pruning) e [carregamento lazy de
     módulos](/ref/mod#lazy-loading).
   * Como pode haver muitas mais dependências `// indirect` do que em versões
     `go` anteriores, dependências indiretas são registradas em um bloco separado
     dentro do arquivo `go.mod`.
   * `go mod vendor` omite arquivos `go.mod` e `go.sum` para dependências
     vendored. (Isso permite invocações do comando `go` dentro de
     subdiretórios de `vendor` para identificar o módulo main correto.)
   * `go mod vendor` registra a versão `go` do arquivo `go.mod` de cada dependência
     em `vendor/modules.txt`.
* Em `go 1.21` ou superior:
   * A linha `go` declara uma versão mínima exigida do Go para usar com este módulo.
   * A linha `go` deve ser maior ou igual à linha `go` de todas as dependências.
   * O comando `go` não tenta mais manter compatibilidade com a versão anterior mais antiga do Go.
   * O comando `go` é mais cuidadoso sobre manter checksums de arquivos `go.mod` no arquivo `go.sum`.
<!-- Se você atualizar esta lista, também atualize /ref/mod#go-mod-file-go. -->

Um arquivo `go.mod` pode conter no máximo uma diretiva `go`. A maioria dos comandos adicionará uma
diretiva `go` com a versão Go atual se uma não estiver presente.

## toolchain {#toolchain}

Declara um toolchain Go sugerido para usar com este módulo.
Só tem efeito quando o módulo é o módulo main
e o toolchain padrão é mais antigo que o toolchain sugerido.

Para mais consulte "[Go toolchains](/doc/toolchain)" e
[diretiva `toolchain`](/ref/mod/#go-mod-file-toolchain) na
Referência de Módulos Go.

### Sintaxe {#toolchain-syntax}

<pre>toolchain <var>toolchain-name</var></pre>

<dl>
    <dt>toolchain-name</dt>
    <dd>O nome do toolchain Go sugerido. Nomes de toolchain padrão tomam a forma
      <code>go<i>V</i></code> para uma versão Go <i>V</i>, como em
      <code>go1.21.0</code> e <code>go1.18rc1</code>.
      O valor especial <code>default</code> desabilita a troca automática de toolchain.</dd>
</dl>

### Exemplos {#toolchain-examples}

* Sugerir usar Go 1.21.0 ou mais recente:
    ```
    toolchain go1.21.0
    ```

### Notas {#toolchain-notes}

Consulte "[Go toolchains](/doc/toolchain)" para detalhes sobre como a linha `toolchain`
afeta a seleção de toolchain Go.

## godebug {#godebug}

Indica as configurações [GODEBUG](/doc/godebug) padrão a serem aplicadas aos packages main deste módulo.
Estas substituem quaisquer padrões do toolchain, e são substituídas por linhas `//go:debug` explícitas em packages main.

### Sintaxe {#godebug-syntax}

<pre>godebug <var>debug-key</var>=<var>debug-value</var></pre>

<dl>
    <dt>debug-key</dt>
    <dd>O nome da configuração a ser aplicada.
      Uma lista de configurações e as versões em que foram introduzidas pode ser encontrada em
      <a href="/doc/godebug#history">Histórico GODEBUG</a>.
    </dd>
    <dt>debug-value</dt>
    <dd>O valor fornecido à configuração.
      Se não especificado de outra forma, <code>0</code> para desabilitar e <code>1</code> para habilitar o comportamento nomeado.</dd>
</dl>

### Exemplos {#godebug-examples}

* Usar o novo comportamento `asynctimerchan=0` do 1.23:
  ```
  godebug asynctimerchan=0
  ```
* Usar os GODEBUGs padrão do Go 1.21, mas o antigo comportamento `panicnil=1`:
  ```
  godebug (
      default=go1.21
      panicnil=1
  )
  ```

### Notas {#godebug-notes}

Configurações GODEBUG só se aplicam para builds de packages main e binários de teste no módulo atual.
Elas não têm efeito quando um módulo é usado como uma dependência.

Consulte "[Go, Backwards Compatibility, and GODEBUG](/doc/godebug)" para detalhes sobre compatibilidade retroativa.

## require {#require}

Declara um módulo como uma dependência do módulo atual, especificando a
versão mínima do módulo exigida.

Para mais, consulte [diretiva `require`](/ref/mod#go-mod-file-require) na
Referência de Módulos Go.

### Sintaxe {#require-syntax}

<pre>require <var>module-path</var> <var>module-version</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>O caminho do módulo do módulo, geralmente uma concatenação do domínio do
      repositório de código-fonte do módulo e o nome do módulo. Para versões de módulo v2 e posteriores,
      este valor deve terminar com o número de versão major, como <code>/v2</code>.</dd>
    <dt>module-version</dt>
    <dd>A versão do módulo. Pode ser tanto um número de versão de release, como
      v1.2.3, ou um número de pseudo-versão gerado pelo Go, como
      v0.0.0-20200921210052-fa0125251cc4.</dd>
</dl>

### Exemplos {#require-examples}

* Exigindo uma versão de release v1.2.3:
    ```
    require example.com/othermodule v1.2.3
    ```
* Exigindo uma versão ainda não tagueada em seu repositório usando um número de pseudo-versão
  gerado pelas ferramentas Go:
    ```
    require example.com/othermodule v0.0.0-20200921210052-fa0125251cc4
    ```

### Notas {#require-notes}

Quando você executa um comando `go` como `go get`, Go insere diretivas `require`
para cada módulo contendo packages importados. Quando um módulo ainda não está tagueado no
seu repositório, Go atribui um número de pseudo-versão que gera quando você executa o
comando.

Você pode fazer Go exigir um módulo de um local diferente do seu repositório usando
a [diretiva `replace`](#replace).

Para mais sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

Para mais sobre gerenciamento de dependências, consulte o seguinte:

* [Adding a dependency](/doc/modules/managing-dependencies#adding_dependency)
* [Getting a specific dependency version](/doc/modules/managing-dependencies#getting_version)
* [Discovering available updates](/doc/modules/managing-dependencies#discovering_updates)
* [Upgrading or downgrading a dependency](/doc/modules/managing-dependencies#upgrading)
* [Synchronizing your code's dependencies](/doc/modules/managing-dependencies#synchronizing)

## tool {#tool}

Adiciona um package como uma dependência do módulo atual, e o disponibiliza para executar com `go tool` quando o diretório de trabalho atual está dentro deste módulo.

### Sintaxe {#tool-syntax}

<pre>tool <var>package-path</var></pre>

<dl>
    <dt>package-path</dt>
    <dd>O caminho do package da ferramenta, uma concatenação do módulo contendo
        a ferramenta e o caminho (possivelmente vazio) para o package implementando
        a ferramenta dentro do módulo.</dd>
</dl>

### Exemplos {#tool-examples}

* Declarando uma ferramenta implementada no módulo atual:
    ```
    module example.com/mymodule

    tool example.com/mymodule/cmd/mytool
    ```
* Declarando uma ferramenta implementada em um módulo separado:
    ```
    module example.com/mymodule

    tool example.com/atool/cmd/atool

    require example.com/atool v1.2.3
    ```

### Notas {#tool-notes}

Você pode usar `go tool` para executar ferramentas declaradas no seu módulo pelo caminho completo do package
ou, se não houver ambiguidade, pelo último segmento do caminho. No primeiro exemplo
acima você poderia executar `go tool mytool` ou `go tool example.com/mymodule/cmd/mytool`.

No modo workspace, você pode usar `go tool` para executar uma ferramenta declarada em qualquer módulo do workspace.

Ferramentas são compiladas usando o mesmo grafo de módulos que o próprio módulo. Uma diretiva [`require`
](#require) é necessária para selecionar a versão do módulo que
implementa a ferramenta. Quaisquer [diretivas `replace`](#replace), ou [diretivas `exclude`
](#exclude) também se aplicam à ferramenta e suas dependências.

Para mais informação consulte [Tool dependencies](/doc/modules/managing-dependencies#tools).

## replace {#replace}

Substitui o conteúdo de um módulo em uma versão específica (ou todas as versões) com
outra versão de módulo ou com um diretório local. Ferramentas Go usarão o
caminho de substituição ao resolver a dependência.

Para mais, consulte [diretiva `replace`](/ref/mod#go-mod-file-replace) na
Referência de Módulos Go.

### Sintaxe {#replace-syntax}

<pre>replace <var>module-path</var> <var>[module-version]</var> => <var>replacement-path</var> <var>[replacement-version]</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>O caminho do módulo do módulo a substituir.</dd>
    <dt>module-version</dt>
    <dd>Opcional. Uma versão específica para substituir. Se este número de versão for
      omitido, todas as versões do módulo são substituídas com o conteúdo no
      lado direito da seta.</dd>
    <dt>replacement-path</dt>
    <dd>O caminho onde Go deve procurar o módulo exigido. Pode ser um
      caminho de módulo ou um caminho para um diretório no sistema de arquivos local para o
      módulo de substituição. Se for um caminho de módulo, você deve especificar um
      valor de <em>replacement-version</em>. Se for um caminho local, você não pode usar um
      valor de <em>replacement-version</em>.</dd>
    <dt>replacement-version</dt>
    <dd>A versão do módulo de substituição. A versão de substituição só pode
      ser especificada se <em>replacement-path</em> for um caminho de módulo (não um diretório local).</dd>
</dl>

### Exemplos {#replace-examples}

* Substituindo com um fork do repositório do módulo

  No exemplo a seguir, qualquer versão de example.com/othermodule é substituída
  com o fork especificado do seu código.

  ```
  require example.com/othermodule v1.2.3

  replace example.com/othermodule => example.com/myfork/othermodule v1.2.3-fixed
  ```

  Quando você substitui um caminho de módulo com outro, não mude statements import
  para packages no módulo que você está substituindo.

  Para mais sobre usar uma cópia de fork do código de módulo, consulte [Requiring external module
  code from your own repository fork](/doc/modules/managing-dependencies#external_fork).

* Substituindo com um número de versão diferente

  O exemplo a seguir especifica que a versão v1.2.3 deve ser usada em vez de
  qualquer outra versão do módulo.

  ```
  require example.com/othermodule v1.2.2

  replace example.com/othermodule => example.com/othermodule v1.2.3
  ```

  O exemplo a seguir substitui a versão v1.2.5 do módulo com a versão v1.2.3 do
  mesmo módulo.

  ```
  replace example.com/othermodule v1.2.5 => example.com/othermodule v1.2.3
  ```

* Substituindo com código local

  O exemplo a seguir especifica que um diretório local deve ser usado como
  substituição para todas as versões do módulo.

  ```
  require example.com/othermodule v1.2.3

  replace example.com/othermodule => ../othermodule
  ```

  O exemplo a seguir especifica que um diretório local deve ser usado como
  substituição apenas para v1.2.5.

  ```
  require example.com/othermodule v1.2.5

  replace example.com/othermodule v1.2.5 => ../othermodule
  ```

  Para mais sobre usar uma cópia local do código de módulo, consulte [Requiring module code in a
  local directory](/doc/modules/managing-dependencies#local_directory).

### Notas {#replace-notes}

Use a diretiva `replace` para substituir temporariamente um valor de caminho de módulo com
outro valor quando você quer que Go use o outro caminho para encontrar o
código-fonte do módulo. Isso tem o efeito de redirecionar a busca do Go pelo módulo para o
local da substituição. Você não precisa mudar caminhos de import de packages para usar o
caminho de substituição.

Use as diretivas `exclude` e `replace` para controlar a resolução de dependências em tempo de compilação
ao compilar o módulo atual. Essas diretivas são ignoradas em
módulos que dependem do módulo atual.

A diretiva `replace` pode ser útil em situações como as seguintes:

* Você está desenvolvendo um novo módulo cujo código ainda não está no repositório. Você
  quer testar com clientes usando uma versão local.
* Você identificou um problema com uma dependência, clonou o repositório da
  dependência, e está testando uma correção com o repositório local.

Observe que uma diretiva `replace` sozinha não adiciona um módulo ao
[grafo de módulos](/ref/mod#glos-module-graph). Uma [diretiva `require`](#require)
que refere-se a uma versão de módulo substituída também é necessária, seja no arquivo `go.mod` do módulo main
ou no arquivo `go.mod` de uma dependência. Se você não tem uma
versão específica para substituir, pode usar uma versão falsa, como no exemplo
abaixo. Observe que isso quebrará módulos que dependem do seu módulo, já que
diretivas `replace` são aplicadas apenas no módulo main.

```
require example.com/mod v0.0.0-replace

replace example.com/mod v0.0.0-replace => ./mod
```

Para mais sobre substituir um módulo exigido, incluindo usar ferramentas Go para fazer a
mudança, consulte:

* [Requiring external module code from your own repository
fork](/doc/modules/managing-dependencies#external_fork)
* [Requiring module code in a local
directory](/doc/modules/managing-dependencies#local_directory)

Para mais sobre números de versão, consulte [Module version
numbering](/doc/modules/version-numbers).

## exclude {#exclude}

Especifica um módulo ou versão de módulo para excluir do grafo de
dependências do módulo atual.

Para mais, consulte [diretiva `exclude`](/ref/mod#go-mod-file-exclude) na
Referência de Módulos Go.

### Sintaxe {#exclude-syntax}

<pre>exclude <var>module-path</var> <var>module-version</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>O caminho do módulo do módulo a excluir.</dd>
    <dt>module-version</dt>
    <dd>A versão específica a excluir.</dd>
</dl>

### Exemplo {#exclude-example}

* Excluir example.com/theirmodule versão v1.3.0

  ```
  exclude example.com/theirmodule v1.3.0
  ```

### Notas {#exclude-notes}

Use a diretiva `exclude` para excluir uma versão específica de um módulo que é
indiretamente exigido mas não pode ser carregado por alguma razão. Por exemplo, você pode
usá-la para excluir uma versão de um módulo que tem um checksum inválido.

Use as diretivas `exclude` e `replace` para controlar a resolução de dependências em tempo de compilação
ao compilar o módulo atual (o módulo main que você está compilando).
Essas diretivas são ignoradas em módulos que dependem do módulo atual.

Você pode usar o [comando `go mod edit`](/ref/mod#go-mod-edit)
para excluir um módulo, como no exemplo a seguir.

```
go mod edit -exclude=example.com/theirmodule@v1.3.0
```

Para mais sobre números de versão, consulte
[Module version numbering](/doc/modules/version-numbers).

## retract {#retract}

Indica que uma versão ou intervalo de versões do módulo definido por `go.mod`
não deveria ter dependências. Uma diretiva `retract` é útil quando uma versão foi
publicada prematuramente ou um problema grave foi descoberto após a versão ter sido
publicada.

Para mais, consulte [diretiva `retract`](/ref/mod#go-mod-file-retract) na
Referência de Módulos Go.

### Sintaxe {#retract-syntax}

<pre>
retract <var>version</var> // <var>rationale</var>
retract [<var>version-low</var>,<var>version-high</var>] // <var>rationale</var>
</pre>

<dl>
  <dt>version</dt>
  <dd>Uma única versão para retratar.</dd>
  <dt>version-low</dt>
  <dd>Limite inferior de um intervalo de versões para retratar.</dd>
  <dt>version-high</dt>
  <dd>
    Limite superior de um intervalo de versões para retratar. Tanto <var>version-low</var>
    quanto <var>version-high</var> são incluídos no intervalo.
  </dd>
  <dt>rationale</dt>
  <dd>
    Comentário opcional explicando a retratação. Pode ser mostrado em mensagens ao
    usuário.
  </dd>
</dl>

### Exemplo {#retract-example}

* Retratando uma única versão

  ```
  retract v1.1.0 // Published accidentally.
  ```

* Retratando um intervalo de versões

  ```
  retract [v1.0.0,v1.0.5] // Build broken on some platforms.
  ```

### Notas {#retract-notes}

Use a diretiva `retract` para indicar que uma versão anterior do seu módulo
não deveria ser usada. Usuários não atualizarão automaticamente para uma versão retratada
com `go get`, `go mod tidy`, ou outros comandos. Usuários não verão uma versão retratada
como uma atualização disponível com `go list -m -u`.

Versões retratadas devem permanecer disponíveis para que usuários que já dependem delas
sejam capazes de compilar seus packages. Mesmo se uma versão retratada for excluída do
repositório de código-fonte, ela pode permanecer disponível em mirrors como
[proxy.golang.org](https://proxy.golang.org). Usuários que dependem de versões retratadas
podem ser notificados quando executam `go get` ou `go list -m -u` em
módulos relacionados.

O comando `go` descobre versões retratadas lendo diretivas `retract`
no arquivo `go.mod` na versão mais recente de um módulo. A versão mais recente é, em
ordem de precedência:

1. Sua versão de release mais alta, se houver alguma
2. Sua versão de pre-release mais alta, se houver alguma
3. Uma pseudo-versão para o tip do branch padrão do repositório.

Quando você adiciona uma retratação, você quase sempre precisa taguear uma nova versão mais alta
para que o comando a veja na versão mais recente do módulo.

Você pode publicar uma versão cujo único propósito é sinalizar retratações. Neste
caso, a nova versão também pode retratar a si mesma.

Por exemplo, se você acidentalmente taguear `v1.0.0`, você pode taguear `v1.0.1` com as
seguintes diretivas:

```
retract v1.0.0 // Published accidentally.
retract v1.0.1 // Contains retraction only.
```

Infelizmente, uma vez que uma versão é publicada, ela não pode ser alterada. Se você depois
taguear `v1.0.0` em um commit diferente, o comando `go` pode detectar uma
soma incompatível em `go.sum` ou no [banco de dados de
checksums](/ref/mod#checksum-database).

Versões retratadas de um módulo normalmente não aparecem na saída de
`go list -m -versions`, mas você pode usar a flag `-retracted` para mostrá-las.
Para mais, consulte [`go list -m`](/ref/mod#go-list-m) na Referência de Módulos Go.

<!--{
  "ia-translated": true,
  "Title": "Referência de Go Modules"
}-->
<!-- TODO(golang.org/issue/33637): Write focused "guide" articles on specific
module topics and tasks. Link to those instead of the blog, which will probably
not be updated over time. -->

## Introdução {#introduction}

Módulos são a forma como o Go gerencia dependências.

Este documento é um manual de referência detalhado do sistema de módulos do Go. Para uma introdução à criação de projetos Go, veja [Como escrever código Go](/doc/code.html). Para informações sobre como usar módulos, migrar projetos para módulos e outros tópicos, veja a série de posts do blog começando com [Usando Go Modules](/blog/using-go-modules).

## Módulos, pacotes e versões {#modules-overview}

Um <dfn>módulo</dfn> é uma coleção de pacotes que são lançados, versionados e distribuídos juntos. Módulos podem ser baixados diretamente de repositórios de controle de versão ou de servidores proxy de módulos.

Um módulo é identificado por um [caminho de módulo](#glos-module-path), declarado em um [arquivo `go.mod`](#go-mod-file), junto com informações sobre as dependências do módulo. O <dfn>diretório raiz do módulo</dfn> é o diretório que contém o arquivo `go.mod`. O <dfn>módulo principal</dfn> é o módulo que contém o diretório em que o comando `go` é invocado.

Cada <dfn>pacote</dfn> dentro de um módulo é uma coleção de arquivos de código-fonte no mesmo diretório que são compilados juntos. Um <dfn>caminho de pacote</dfn> é o caminho do módulo concatenado com o subdiretório que contém o pacote (relativo à raiz do módulo). Por exemplo, o módulo `"golang.org/x/net"` contém um pacote no diretório `"html"`. O caminho desse pacote é `"golang.org/x/net/html"`.

### Caminhos de módulo {#module-path}

Um <dfn>caminho de módulo</dfn> é o nome canônico de um módulo, declarado com a [diretiva `module`](#go-mod-file-module) no [arquivo `go.mod`](#glos-go-mod-file) do módulo. O caminho de um módulo é o prefixo dos caminhos de pacote dentro do módulo.

Um caminho de módulo deve descrever tanto o que o módulo faz quanto onde encontrá-lo. Normalmente, um caminho de módulo consiste em um caminho da raiz do repositório, um diretório dentro do repositório (geralmente vazio) e um sufixo de versão principal (apenas para versão principal 2 ou superior).

* O <dfn>caminho da raiz do repositório</dfn> é a parte do caminho do módulo que corresponde ao diretório raiz do repositório de controle de versão onde o módulo é desenvolvido. A maioria dos módulos é definida no diretório raiz do repositório, então geralmente este é o caminho inteiro. Por exemplo, `golang.org/x/net` é o caminho da raiz do repositório do módulo de mesmo nome. Veja [Encontrando um repositório para um caminho de módulo](#vcs-find) para informações sobre como o comando `go` localiza um repositório usando requisições HTTP derivadas de um caminho de módulo.
* Se o módulo não estiver definido no diretório raiz do repositório, o <dfn>subdiretório do módulo</dfn> é a parte do caminho do módulo que nomeia o diretório, sem incluir o sufixo de versão principal. Isso também serve como prefixo para tags de versão semântica. Por exemplo, o módulo `golang.org/x/tools/gopls` está no subdiretório `gopls` do repositório com caminho raiz `golang.org/x/tools`, então ele tem o subdiretório de módulo `gopls`. Veja [Mapeando versões para commits](#vcs-version) e [Diretórios de módulo dentro de um repositório](#vcs-dir).
* Se o módulo for lançado na versão principal 2 ou superior, o caminho do módulo deve terminar com um [sufixo de versão principal](#major-version-suffixes), como `/v2`. Isso pode ou não fazer parte do nome do subdiretório. Por exemplo, o módulo com caminho `golang.org/x/repo/sub/v2` pode estar nos subdiretórios `/sub` ou `/sub/v2` do repositório `golang.org/x/repo`.

Se um módulo puder ser usado como dependência por outros módulos, essas regras devem ser seguidas para que o comando `go` consiga encontrar e baixar o módulo. Também existem várias [restrições léxicas](#go-mod-file-ident) sobre os caracteres permitidos em caminhos de módulo.

Um módulo que nunca será obtido como dependência de outro módulo pode usar qualquer caminho de pacote válido como caminho de módulo, mas deve tomar cuidado para não colidir com caminhos que possam ser usados pelas dependências do módulo ou pela biblioteca padrão do Go. A biblioteca padrão do Go usa caminhos de pacote que não contêm ponto no primeiro elemento do caminho, e o comando `go` não tenta resolver esses caminhos a partir de servidores de rede. Os caminhos `example` e `test` são reservados para usuários: eles não serão usados na biblioteca padrão e são adequados para uso em módulos autocontidos, como os definidos em tutoriais ou códigos de exemplo ou criados e manipulados como parte de um teste.

### Versões {#versions}

Uma <dfn>versão</dfn> identifica um snapshot imutável de um módulo, que pode ser uma [versão de lançamento](#glos-release-version) ou uma [versão de pré-lançamento](#glos-pre-release-version). Cada versão começa com a letra `v`, seguida de uma versão semântica. Veja [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) para detalhes sobre como as versões são formatadas, interpretadas e comparadas.

Resumindo, uma versão semântica consiste em três inteiros não negativos (a versão principal, a secundária e a de correção, da esquerda para a direita) separados por pontos. A versão de correção pode ser seguida por uma string opcional de pré-lançamento que começa com hífen. A string de pré-lançamento ou a versão de correção pode ser seguida por uma string de metadados de build que começa com um sinal de mais. Por exemplo, `v0.0.0`, `v1.12.134`, `v8.0.5-pre` e `v2.0.9+meta` são versões válidas.

Cada parte de uma versão indica se a versão é estável e se é compatível com versões anteriores.

* A [versão principal](#glos-major-version) deve ser incrementada e as versões secundária e de correção devem ser zeradas após uma alteração incompatível com versões anteriores na interface pública ou na funcionalidade documentada do módulo, por exemplo, após a remoção de um pacote.
* A [versão secundária](#glos-minor-version) deve ser incrementada e a versão de correção zerada após uma alteração compatível com versões anteriores, por exemplo, após a adição de uma nova função.
* A [versão de correção](#glos-patch-version) deve ser incrementada após uma alteração que não afete a interface pública do módulo, como uma correção de bug ou uma otimização.
* O sufixo de pré-lançamento indica que uma versão é um [pré-lançamento](#glos-pre-release-version). Versões de pré-lançamento vêm antes das versões de lançamento correspondentes. Por exemplo, `v1.2.3-pre` vem antes de `v1.2.3`.
* O sufixo de metadados de build é ignorado para fins de comparação de versões. O comando `go` aceita versões com metadados de build e as converte em pseudo-versões para manter a ordenação total entre as versões.
  * O sufixo especial `+incompatible` indica uma versão lançada antes da migração para módulos na versão principal 2 ou superior (veja [Compatibilidade com repositórios que não são módulos](#non-module-compat)).
  * O sufixo especial `+dirty` é acrescentado às informações de versão de um binário quando ele é compilado com um toolchain do Go 1.24 ou superior dentro de um repositório de controle de versão (VCS) local válido que contém alterações não commitadas no diretório de trabalho.

Uma versão é considerada instável se sua versão principal for 0 ou se tiver um sufixo de pré-lançamento. Versões instáveis não estão sujeitas a requisitos de compatibilidade. Por exemplo, `v0.2.0` pode não ser compatível com `v0.1.0`, e `v1.5.0-beta` pode não ser compatível com `v1.5.0`.

O Go pode acessar módulos em sistemas de controle de versão usando tags, branches ou revisões que não seguem essas convenções. No entanto, dentro do módulo principal, o comando `go` converterá automaticamente nomes de revisão que não seguem esse padrão em versões canônicas. O comando `go` também removerá os sufixos de metadados de build (exceto `+incompatible`) como parte desse processo. Isso pode resultar em uma [pseudo-versão](#glos-pseudo-version), uma versão de pré-lançamento que codifica um identificador de revisão (como um hash de commit do Git) e um carimbo de data/hora do sistema de controle de versão. Por exemplo, o comando `go get
golang.org/x/net@daa7c041` converterá o hash de commit `daa7c041` na pseudo-versão `v0.0.0-20191109021931-daa7c04131f5`. Versões canônicas são exigidas fora do módulo principal, e o comando `go` reportará um erro se uma versão não canônica como `master` aparecer em um arquivo `go.mod`.

### Pseudo-versões {#pseudo-versions}

Uma <dfn>pseudo-versão</dfn> é uma [versão](#glos-version) de [pré-lançamento](#glos-pre-release-version) com formato especial que codifica informações sobre uma revisão específica em um repositório de controle de versão. Por exemplo, `v0.0.0-20191109021931-daa7c04131f5` é uma pseudo-versão.

Pseudo-versões podem se referir a revisões para as quais não há [tags de versão semântica](#glos-semantic-version-tag) disponíveis. Elas podem ser usadas para testar commits antes de criar tags de versão, por exemplo, em uma branch de desenvolvimento.

Cada pseudo-versão tem três partes:

* Um prefixo de versão base (`vX.0.0` ou `vX.Y.Z-0`), que é derivado de uma tag de versão semântica que precede a revisão ou `vX.0.0` se não houver tal tag.
* Um carimbo de data/hora (`yyyymmddhhmmss`), que é o horário UTC em que a revisão foi criada. No Git, este é o horário do commit, não o horário do autor.
* Um identificador de revisão (`abcdefabcdef`), que é um prefixo de 12 caracteres do hash do commit ou, no Subversion, um número de revisão com zeros à esquerda.

Cada pseudo-versão pode estar em uma de três formas, dependendo da versão base. Essas formas garantem que uma pseudo-versão seja comparada como maior que sua versão base, mas menor que a próxima versão com tag.

* `vX.0.0-yyyymmddhhmmss-abcdefabcdef` é usada quando não há versão base conhecida. Assim como em todas as versões, a versão principal `X` deve corresponder ao [sufixo de versão principal](#glos-major-version-suffix) do módulo.
* `vX.Y.Z-pre.0.yyyymmddhhmmss-abcdefabcdef` é usada quando a versão base é uma versão de pré-lançamento como `vX.Y.Z-pre`.
* `vX.Y.(Z+1)-0.yyyymmddhhmmss-abcdefabcdef` é usada quando a versão base é uma versão de lançamento como `vX.Y.Z`. Por exemplo, se a versão base for `v1.2.3`, uma pseudo-versão pode ser `v1.2.4-0.20191109021931-daa7c04131f5`.

Mais de uma pseudo-versão pode se referir ao mesmo commit usando versões base diferentes. Isso acontece naturalmente quando uma versão inferior recebe uma tag depois que uma pseudo-versão já foi escrita.

Essas formas dão às pseudo-versões duas propriedades úteis:

* Pseudo-versões com versões base conhecidas são ordenadas como maiores que essas versões, mas menores que outros pré-lançamentos de versões posteriores.
* Pseudo-versões com o mesmo prefixo de versão base são ordenadas cronologicamente.

O comando `go` executa várias verificações para garantir que os autores de módulos tenham controle sobre como as pseudo-versões são comparadas com outras versões e que as pseudo-versões se referem a revisões que são de fato parte do histórico de commits de um módulo.

* Se uma versão base for especificada, deve haver uma tag de versão semântica correspondente que seja ancestral da revisão descrita pela pseudo-versão. Isso impede que desenvolvedores contornem a [seleção mínima de versão](#glos-minimal-version-selection) usando uma pseudo-versão que seja comparada como maior que todas as versões com tag, como `v1.999.999-99999999999999-daa7c04131f5`.
* O carimbo de data/hora deve corresponder ao carimbo da revisão. Isso impede que atacantes inundem [proxies de módulos](#glos-module-proxy) com um número ilimitado de pseudo-versões de outra forma idênticas. Isso também impede que consumidores de módulos alterem a ordenação relativa das versões.
* A revisão deve ser ancestral de uma das branches ou tags do repositório do módulo. Isso impede que atacantes façam referência a alterações não aprovadas ou pull requests.

Pseudo-versões nunca precisam ser digitadas manualmente. Muitos comandos aceitam um hash de commit ou o nome de uma branch e os traduzem automaticamente em uma pseudo-versão (ou versão com tag, se disponível). Por exemplo:

```
go get example.com/mod@master
go list -m -json example.com/mod@abcd1234
```

### Sufixos de versão principal {#major-version-suffixes}

A partir da versão principal 2, caminhos de módulo devem ter um <dfn>sufixo de versão principal</dfn> como `/v2` que corresponda à versão principal. Por exemplo, se um módulo tem o caminho `example.com/mod` na versão `v1.0.0`, ele deve ter o caminho `example.com/mod/v2` na versão `v2.0.0`.

Sufixos de versão principal implementam a [<dfn>regra de compatibilidade de importação</dfn>](https://research.swtch.com/vgo-import):

> Se um pacote antigo e um pacote novo tiverem o mesmo caminho de importação,
> o novo pacote deve ser compatível com versões anteriores do pacote antigo.

Por definição, pacotes em uma nova versão principal de um módulo não são compatíveis com versões anteriores dos pacotes correspondentes na versão principal anterior. Consequentemente, a partir da `v2`, os pacotes precisam de novos caminhos de importação. Isso é feito adicionando um sufixo de versão principal ao caminho do módulo. Como o caminho do módulo é prefixo do caminho de importação de cada pacote dentro do módulo, adicionar o sufixo de versão principal ao caminho do módulo fornece um caminho de importação distinto para cada versão incompatível.

Sufixos de versão principal não são permitidos nas versões principais `v0` ou `v1`. Não há necessidade de mudar o caminho do módulo entre `v0` e `v1`, pois as versões `v0` são instáveis e não têm garantia de compatibilidade. Além disso, para a maioria dos módulos, a `v1` é compatível com a última versão `v0`; uma versão `v1` atua como um compromisso com a compatibilidade, e não como uma indicação de alterações incompatíveis em relação à `v0`.

Como caso especial, caminhos de módulo que começam com `gopkg.in/` devem sempre ter um sufixo de versão principal, mesmo nas versões `v0` e `v1`. O sufixo deve começar com um ponto, e não com uma barra (por exemplo, `gopkg.in/yaml.v2`).

Sufixos de versão principal permitem que várias versões principais de um módulo coexistam na mesma build. Isso pode ser necessário devido a um [problema de dependência em diamante](https://research.swtch.com/vgo-import#dependency_story). Normalmente, se um módulo for exigido em duas versões diferentes por dependências transitivas, a versão mais alta será usada. No entanto, se as duas versões forem incompatíveis, nenhuma das versões satisfará todos os clientes. Como versões incompatíveis devem ter números de versão principal diferentes, elas também devem ter caminhos de módulo diferentes devido aos sufixos de versão principal. Isso resolve o conflito: módulos com sufixos distintos são tratados como módulos separados, e seus pacotes — mesmo pacotes no mesmo subdiretório relativo às suas raízes de módulo — são distintos.

Muitos projetos Go lançaram versões `v2` ou superiores sem usar um sufixo de versão principal antes de migrar para módulos (talvez até antes de os módulos serem introduzidos). Essas versões são anotadas com uma tag de build `+incompatible` (por exemplo, `v2.0.0+incompatible`). Veja [Compatibilidade com repositórios que não são módulos](#non-module-compat) para mais informações.

### Resolvendo um pacote para um módulo {#resolve-pkg-mod}

Quando o comando `go` carrega um pacote usando um [caminho de pacote](#glos-package-path), ele precisa determinar qual módulo fornece o pacote.

O comando `go` começa pesquisando na [lista de build](#glos-build-list) por módulos cujos caminhos são prefixos do caminho do pacote. Por exemplo, se o pacote `example.com/a/b` for importado e o módulo `example.com/a` estiver na lista de build, o comando `go` verificará se `example.com/a` contém o pacote, no diretório `b`. Pelo menos um arquivo com extensão `.go` deve estar presente em um diretório para que ele seja considerado um pacote. [Restrições de build](/pkg/go/build/#hdr-Build_Constraints) não são aplicadas para essa finalidade. Se exatamente um módulo na lista de build fornecer o pacote, esse módulo é usado. Se nenhum módulo fornecer o pacote ou se dois ou mais módulos o fornecerem, o comando `go` reporta um erro. A flag `-mod=mod` instrui o comando `go` a tentar encontrar novos módulos que forneçam pacotes ausentes e a atualizar `go.mod` e `go.sum`. Os comandos [`go get`](#go-get) e [`go
mod tidy`](#go-mod-tidy) fazem isso automaticamente.

<!-- NOTE(golang.org/issue/27899): the go command reports an error when two
or more modules provide a package with the same path as above. In the future,
we may try to upgrade one (or all) of the colliding modules.
-->

Quando o comando `go` procura um novo módulo para um caminho de pacote, ele consulta a variável de ambiente `GOPROXY`, que é uma lista separada por vírgulas de URLs de proxy ou das palavras-chave `direct` ou `off`. Uma URL de proxy indica que o comando `go` deve contatar um [proxy de módulos](#glos-module-proxy) usando o [protocolo `GOPROXY`](#goproxy-protocol). `direct` indica que o comando `go` deve [se comunicar com um sistema de controle de versão](#vcs). `off` indica que nenhuma comunicação deve ser tentada. As [variáveis de ambiente](#environment-variables) `GOPRIVATE` e `GONOPROXY` também podem ser usadas para controlar esse comportamento.

Para cada entrada na lista `GOPROXY`, o comando `go` solicita a versão mais recente de cada caminho de módulo que pode fornecer o pacote (ou seja, cada prefixo do caminho do pacote). Para cada caminho de módulo solicitado com sucesso, o comando `go` baixa o módulo na versão mais recente e verifica se o módulo contém o pacote solicitado. Se um ou mais módulos contiverem o pacote solicitado, o módulo com o caminho mais longo é usado. Se um ou mais módulos forem encontrados, mas nenhum contiver o pacote solicitado, um erro é reportado. Se nenhum módulo for encontrado, o comando `go` tenta a próxima entrada da lista `GOPROXY`. Se não houver mais entradas, um erro é reportado.

Por exemplo, suponha que o comando `go` esteja procurando um módulo que forneça o pacote `golang.org/x/net/html`, e `GOPROXY` esteja definido como `https://corp.example.com,https://proxy.golang.org`. O comando `go` pode fazer as seguintes requisições:

* Para `https://corp.example.com/` (em paralelo):
  * Requisição da versão mais recente de `golang.org/x/net/html`
  * Requisição da versão mais recente de `golang.org/x/net`
  * Requisição da versão mais recente de `golang.org/x`
  * Requisição da versão mais recente de `golang.org`
* Para `https://proxy.golang.org/`, se todas as requisições para `https://corp.example.com/` tiverem falhado com 404 ou 410:
  * Requisição da versão mais recente de `golang.org/x/net/html`
  * Requisição da versão mais recente de `golang.org/x/net`
  * Requisição da versão mais recente de `golang.org/x`
  * Requisição da versão mais recente de `golang.org`

Depois que um módulo adequado for encontrado, o comando `go` adicionará um novo [requisito](#go-mod-file-require) com o caminho e a versão do novo módulo ao arquivo `go.mod` do módulo principal. Isso garante que, quando o mesmo pacote for carregado no futuro, o mesmo módulo será usado na mesma versão. Se o pacote resolvido não for importado por um pacote do módulo principal, o novo requisito terá um comentário `// indirect`.

## Arquivos `go.mod` {#go-mod-file}

Um módulo é definido por um arquivo de texto codificado em UTF-8 chamado `go.mod` em seu diretório raiz. O arquivo `go.mod` é orientado a linhas. Cada linha contém uma única diretiva, formada por uma palavra-chave seguida de argumentos. Por exemplo:

```
module example.com/my/thing

go 1.23.0

require example.com/other/thing v1.0.2
require example.com/new/thing/v2 v2.3.4
exclude example.com/old/thing v1.2.3
replace example.com/bad/thing v1.4.5 => example.com/good/thing v1.4.5
retract [v1.9.0, v1.9.5]
```

A palavra-chave inicial pode ser fatorada em linhas adjacentes para criar um bloco, como nos imports do Go.

```
require (
    example.com/new/thing/v2 v2.3.4
    example.com/old/thing v1.2.3
)
```

O arquivo `go.mod` foi projetado para ser legível por humanos e gravável por máquinas. O comando `go` oferece vários subcomandos que alteram arquivos `go.mod`. Por exemplo, [`go get`](#go-get) pode atualizar ou rebaixar dependências específicas. Comandos que carregam o grafo de módulos [atualizam automaticamente](#go-mod-file-updates) o `go.mod` quando necessário. [`go mod edit`](#go-mod-edit) pode realizar edições de baixo nível. O pacote [`golang.org/x/mod/modfile`](https://pkg.go.dev/golang.org/x/mod/modfile?tab=doc) pode ser usado por programas Go para fazer as mesmas alterações programaticamente.

Um arquivo `go.mod` é obrigatório para o [módulo principal](#glos-main-module) e para qualquer [módulo de substituição](#go-mod-file-replace) especificado com um caminho de arquivo local. No entanto, um módulo que não possui um arquivo `go.mod` explícito ainda pode ser [requerido](#go-mod-file-require) como dependência, ou usado como substituição especificada com um caminho de módulo e versão; veja [Compatibilidade com repositórios que não são módulos](#non-module-compat).

### Elementos léxicos {#go-mod-file-lexical}

Ao analisar um arquivo `go.mod`, seu conteúdo é dividido em uma sequência de tokens. Existem vários tipos de tokens: espaços em branco, comentários, pontuação, palavras-chave, identificadores e strings.

*Espaço em branco* consiste em espaços (U+0020), tabulações (U+0009), retornos de carro (U+000D) e quebras de linha (U+000A). Caracteres de espaço em branco que não sejam quebras de linha não têm efeito, exceto separar tokens que de outra forma seriam combinados. Quebras de linha são tokens significativos.

*Comentários* começam com `//` e vão até o fim da linha. Comentários `/* */` não são permitidos.

*Pontuação* inclui os tokens `(`, `)` e `=>`.

*Palavras-chave* distinguem diferentes tipos de diretivas em um arquivo `go.mod`. As palavras-chave permitidas são `module`, `go`, `require`, `replace`, `exclude` e `retract`.

*Identificadores* são sequências de caracteres que não são espaços em branco, como caminhos de módulo ou versões semânticas.

*Strings* são sequências de caracteres entre aspas. Existem dois tipos de strings: strings interpretadas, que começam e terminam com aspas (`"`, U+0022), e strings brutas, que começam e terminam com crases (<code>&#x60;</code>, U+0060). Strings interpretadas podem conter sequências de escape formadas por uma barra invertida (`\`, U+005C) seguida de outro caractere. Uma aspa escapada (`\"`) não termina uma string interpretada. O valor sem aspas de uma string interpretada é a sequência de caracteres entre as aspas, com cada sequência de escape substituída pelo caractere que segue a barra invertida (por exemplo, `\"` é substituído por `"`, `\n` é substituído por `n`). Em contraste, o valor sem aspas de uma string bruta é simplesmente a sequência de caracteres entre as crases; barras invertidas não têm significado especial dentro de strings brutas.

Identificadores e strings são intercambiáveis na gramática de `go.mod`.

### Caminhos de módulo e versões {#go-mod-file-ident}

A maioria dos identificadores e strings em um arquivo `go.mod` são caminhos de módulo ou versões.

Um caminho de módulo deve satisfazer os seguintes requisitos:

* O caminho deve consistir em um ou mais elementos de caminho separados por barras (`/`, U+002F). Ele não pode começar nem terminar com barra.
* Cada elemento de caminho é uma string não vazia composta de letras ASCII, dígitos ASCII e pontuação ASCII limitada (`-`, `.`, `_` e `~`).
* Um elemento de caminho não pode começar nem terminar com ponto (`.`, U+002E).
* O prefixo do elemento até o primeiro ponto não pode ser um nome de arquivo reservado no Windows, independentemente de maiúsculas ou minúsculas (`CON`, `com1`, `NuL`, e assim por diante).
* O prefixo do elemento até o primeiro ponto não pode terminar com til seguido de um ou mais dígitos (como `EXAMPL~1.COM`).

Se o caminho do módulo aparecer em uma diretiva `require` e não for substituído, ou se o caminho do módulo aparecer no lado direito de uma diretiva `replace`, o comando `go` pode precisar baixar módulos com esse caminho, e alguns requisitos adicionais devem ser satisfeitos.

* O elemento de caminho inicial (até a primeira barra, se houver), por convenção um nome de domínio, deve conter apenas letras ASCII minúsculas, dígitos ASCII, pontos (`.`, U+002E) e hífens (`-`, U+002D); deve conter pelo menos um ponto e não pode começar com hífen.
* Para um elemento de caminho final da forma `/vN`, em que `N` parece numérico (dígitos ASCII e pontos), `N` não pode começar com zero à esquerda, não pode ser `/v1` e não pode conter pontos.
  * Para caminhos que começam com `gopkg.in/`, este requisito é substituído por um requisito de que o caminho siga as convenções do serviço [gopkg.in](https://gopkg.in).

Versões em arquivos `go.mod` podem ser [canônicas](#glos-canonical-version) ou não canônicas.

Uma versão canônica começa com a letra `v`, seguida de uma versão semântica que segue a especificação [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Veja [Versões](#versions) para mais informações.

A maioria dos outros identificadores e strings pode ser usada como versões não canônicas, embora existam algumas restrições para evitar problemas com sistemas de arquivos, repositórios e [proxies de módulos](#glos-module-proxy). Versões não canônicas são permitidas apenas no arquivo `go.mod` do módulo principal. O comando `go` tentará substituir cada versão não canônica por uma versão canônica equivalente quando [atualizar](#go-mod-file-updates) automaticamente o arquivo `go.mod`.

Em locais onde um caminho de módulo está associado a uma versão (como nas diretivas `require`, `replace` e `exclude`), o último elemento do caminho deve ser consistente com a versão. Veja [Sufixos de versão principal](#major-version-suffixes).

### Gramática {#go-mod-file-grammar}

A sintaxe de `go.mod` é especificada abaixo usando a Forma Normal de Backus-Naur Estendida (EBNF). Veja a [seção Notation da Especificação da Linguagem Go](/ref/spec#Notation) para detalhes sobre a sintaxe EBNF.

```
GoMod = { Directive } .
Directive = ModuleDirective |
            GoDirective |
            ToolDirective |
            IgnoreDirective |
            RequireDirective |
            ExcludeDirective |
            ReplaceDirective |
            RetractDirective .
```

Quebras de linha, identificadores e strings são denotados por `newline`, `ident` e `string`, respectivamente.

Caminhos de módulo e versões são denotados por `ModulePath` e `Version`.

```
ModulePath = ident | string . /* see restrictions above */
Version = ident | string .    /* see restrictions above */
```

### Diretiva `module` {#go-mod-file-module}

Uma diretiva `module` define o [caminho](#glos-module-path) do módulo principal. Um arquivo `go.mod` deve conter exatamente uma diretiva `module`.

```
ModuleDirective = "module" ( ModulePath | "(" newline ModulePath newline ")" ) newline .
```

Exemplo:

```
module golang.org/x/net
```

#### Descontinuação {#go-mod-file-module-deprecation}

Um módulo pode ser marcado como descontinuado em um bloco de comentários que contém a string `Deprecated:` (diferencia maiúsculas de minúsculas) no início de um parágrafo. A mensagem de descontinuação começa após os dois-pontos e vai até o fim do parágrafo. Os comentários podem aparecer imediatamente antes da diretiva `module` ou depois dela, na mesma linha.

Exemplo:

```
// Deprecated: use example.com/mod/v2 instead.
module example.com/mod
```

Desde o Go 1.17, [`go list -m -u`](#go-list-m) verifica informações sobre todos os módulos descontinuados na [lista de build](#glos-build-list). [`go get`](#go-get) verifica módulos descontinuados necessários para compilar pacotes nomeados na linha de comando.

Quando o comando `go` obtém informações de descontinuação para um módulo, ele carrega o arquivo `go.mod` da versão correspondente à [consulta de versão](#version-queries) `@latest`, sem considerar [retrações](#go-mod-file-retract) ou [exclusões](#go-mod-file-exclude). O comando `go` carrega a lista de [versões retraídas](#glos-retracted-version) do mesmo arquivo `go.mod`.

Para descontinuar um módulo, um autor pode adicionar um comentário `// Deprecated:` e publicar uma nova versão. O autor pode alterar ou remover a mensagem de descontinuação em uma versão superior.

Uma descontinuação se aplica a todas as versões menores de um módulo. Versões principais superiores a `v2` são consideradas módulos separados para esse fim, já que seus [sufixos de versão principal](#glos-major-version-suffix) lhes dão caminhos de módulo distintos.

As mensagens de descontinuação têm como objetivo informar os usuários de que o módulo não é mais suportado e fornecer instruções de migração, por exemplo, para a versão principal mais recente. Versões menores e de correção individuais não podem ser descontinuadas; [`retract`](#go-mod-file-retract) pode ser mais apropriado para isso.

### Diretiva `go` {#go-mod-file-go}

Uma diretiva `go` indica que um módulo foi escrito assumindo a semântica de uma determinada versão do Go. A versão deve ser uma [versão do Go](/doc/toolchain#version) válida, como `1.14`, `1.21rc1` ou `1.23.0`.

A diretiva `go` define a versão mínima do Go necessária para usar este módulo. Antes do Go 1.21, a diretiva era apenas consultiva; agora é um requisito obrigatório: toolchains do Go se recusam a usar módulos que declaram versões mais novas do Go.

A diretiva `go` é uma entrada para a seleção de qual toolchain do Go executar. Veja “[Toolchains do Go](/doc/toolchain)” para detalhes.

A diretiva `go` afeta o uso de novos recursos da linguagem:

* Para pacotes dentro do módulo, o compilador rejeita o uso de recursos da linguagem introduzidos após a versão especificada pela diretiva `go`. Por exemplo, se um módulo tiver a diretiva `go 1.12`, seus pacotes não podem usar literais numéricos como `1_000_000`, que foram introduzidos no Go 1.13.
* Se uma versão mais antiga do Go compilar um dos pacotes do módulo e encontrar um erro de compilação, o erro indica que o módulo foi escrito para uma versão mais nova do Go. Por exemplo, suponha que um módulo tenha `go 1.13` e um pacote use o literal numérico `1_000_000`. Se esse pacote for compilado com o Go 1.12, o compilador indica que o código foi escrito para o Go 1.13.

A diretiva `go` também afeta o comportamento do comando `go`:

* Na versão `go 1.14` ou superior, a [vendorização](#vendoring) automática pode ser habilitada. Se o arquivo `vendor/modules.txt` estiver presente e consistente com `go.mod`, não é necessário usar explicitamente a flag `-mod=vendor`.
* Na versão `go 1.16` ou superior, o padrão de pacote `all` corresponde apenas a pacotes importados transitivamente por pacotes e testes no [módulo principal](#glos-main-module). Este é o mesmo conjunto de pacotes mantido por [`go mod vendor`](#go-mod-vendor) desde que os módulos foram introduzidos. Em versões inferiores, `all` também inclui testes de pacotes importados por pacotes no módulo principal, testes desses pacotes, e assim por diante.
* Na versão `go 1.17` ou superior:
   * O arquivo `go.mod` inclui uma [diretiva `require`](#go-mod-file-require) explícita para cada módulo que fornece qualquer pacote importado transitivamente por um pacote ou teste no módulo principal. (Nas versões `go 1.16` e inferiores, uma [dependência indireta](#glos-direct-dependency) é incluída apenas se a [seleção mínima de versão](#minimal-version-selection) selecionaria uma versão diferente.) Essa informação extra permite a [poda do grafo de módulos](#graph-pruning) e o [carregamento preguiçoso de módulos](#lazy-loading).
   * Como pode haver muito mais dependências `// indirect` do que nas versões anteriores do `go`, as dependências indiretas são registradas em um bloco separado dentro do arquivo `go.mod`.
   * `go mod vendor` omite os arquivos `go.mod` e `go.sum` das dependências vendorizadas. (Isso permite que invocações do comando `go` dentro de subdiretórios de `vendor` identifiquem o módulo principal correto.)
   * `go mod vendor` registra a versão `go` do arquivo `go.mod` de cada dependência em `vendor/modules.txt`.
* Na versão `go 1.21` ou superior:
   * A linha `go` declara uma versão mínima obrigatória do Go para usar com este módulo.
   * A linha `go` deve ser maior ou igual à linha `go` de todas as dependências.
   * O comando `go` não tenta mais manter compatibilidade com a versão anterior do Go.
   * O comando `go` é mais cuidadoso ao manter checksums dos arquivos `go.mod` no arquivo `go.sum`.
<!-- If you update this list, also update /doc/modules/gomod-ref#go-notes. -->

Um arquivo `go.mod` pode conter no máximo uma diretiva `go`. A maioria dos comandos adicionará uma diretiva `go` com a versão atual do Go se nenhuma estiver presente.

Se a diretiva `go` estiver ausente, assume-se `go 1.16`.

```
GoDirective = "go" GoVersion newline .
GoVersion = string | ident .  /* valid release version; see above */
```

Exemplo:

```
go 1.23.0
```

### Diretiva `toolchain` {#go-mod-file-toolchain}

Uma diretiva `toolchain` declara uma toolchain do Go sugerida para uso com um módulo. A versão da toolchain sugerida não pode ser inferior à versão do Go exigida declarada na diretiva `go`. A diretiva `toolchain` só tem efeito quando o módulo é o módulo principal e a versão da toolchain padrão é inferior à versão da toolchain sugerida.

Para reprodutibilidade, o comando `go` grava o próprio nome da toolchain em uma linha `toolchain` sempre que atualiza a versão `go` no arquivo `go.mod` (geralmente durante `go get`).

Para detalhes, veja “[Toolchains do Go](/doc/toolchain)”.

```
ToolchainDirective = "toolchain" ToolchainName newline .
ToolchainName = string | ident .  /* valid toolchain name; see “Go toolchains” */
```

Exemplo:

```
toolchain go1.21.0
```

### Diretiva `godebug` {#go-mod-file-godebug}

Uma diretiva `godebug` declara uma única [configuração GODEBUG](/doc/godebug)
a ser aplicada quando este módulo for o módulo principal.
Pode haver mais de uma dessas linhas, e elas podem ser agrupadas.
É um erro o módulo principal citar uma chave GODEBUG que não existe.
O efeito de `godebug key=value` é o mesmo que se cada pacote principal
sendo compilado contivesse um arquivo-fonte com `//go:debug key=value`.

```
GodebugDirective = "godebug" ( GodebugSpec | "(" newline { GodebugSpec } ")" newline ) .
GodebugSpec = GodebugKey "=" GodebugValue newline.
GodebugKey = GodebugChar { GodebugChar }.
GodebugValue = GodebugChar { GodebugChar }.
GodebugChar = any non-space character except , " ` ' (comma and quotes).
```

Exemplo:

```
godebug default=go1.21
godebug (
	panicnil=1
	asynctimerchan=0
)
```

### Diretiva `require` {#go-mod-file-require}

Uma diretiva `require` declara uma versão mínima exigida de uma dependência
de módulo específica. Para cada versão de módulo exigida, o comando `go` carrega o
arquivo `go.mod` dessa versão e incorpora os requisitos desse
arquivo. Quando todos os requisitos tiverem sido carregados, o comando `go` os resolve usando
[seleção mínima de versão (MVS)](#minimal-version-selection) para produzir a
[build list](#glos-build-list).

O comando `go` adiciona automaticamente comentários `// indirect` para alguns
requisitos. Um comentário `// indirect` indica que nenhum pacote do módulo
exigido é importado diretamente por nenhum pacote do [módulo
principal](#glos-main-module).

Se a [diretiva `go`](#go-mod-file-go) especificar `go 1.16` ou inferior, o
comando `go` adiciona um requisito indireto quando a versão selecionada de um módulo for
superior ao que já está implícito (transitivamente) pelas outras
dependências do módulo principal. Isso pode ocorrer por causa de uma atualização explícita (`go get -u ./...`),
remoção de alguma outra dependência que anteriormente impunha o requisito (`go
mod tidy`), ou uma dependência que importa um pacote sem um requisito correspondente
no seu próprio arquivo `go.mod` (como uma dependência que não tem arquivo `go.mod`
algum).

A partir do `go 1.17`, o comando `go` adiciona um requisito indireto para cada
módulo que fornece qualquer pacote importado (mesmo
[indiretamente](#glos-indirect-dependency)) por um pacote ou teste do módulo principal
ou passado como argumento para `go get`. Esses requisitos mais abrangentes
possibilitam a [poda do grafo de módulos](#graph-pruning) e o
[carregamento preguiçoso de módulos](#lazy-loading).

```
RequireDirective = "require" ( RequireSpec | "(" newline { RequireSpec } ")" newline ) .
RequireSpec = ModulePath Version newline .
```

Exemplo:

```
require golang.org/x/net v1.2.3

require (
    golang.org/x/crypto v1.4.5 // indirect
    golang.org/x/text v1.6.7
)
```

### Diretiva `tool` {#go-mod-file-tool}

Uma diretiva `tool` adiciona um pacote como dependência do módulo atual. Ela também
o torna disponível para execução com `go tool` quando o diretório de trabalho atual estiver
dentro deste módulo, ou dentro de um workspace que contenha este módulo.

Se o pacote da ferramenta não estiver no módulo atual, deve haver uma
diretiva `require` que especifique a versão da ferramenta a ser usada.

O meta-padrão `tool` resolve para a lista de ferramentas definidas no `go.mod`
do módulo atual, ou, no modo workspace, para a união de todas as ferramentas definidas em todos os módulos do
workspace.

```
ToolDirective = "tool" ( ToolSpec | "(" newline { ToolSpec } ")" newline ) .
ToolSpec = ModulePath newline .
```

Exemplo:

```
tool golang.org/x/tools/cmd/stringer

tool (
    example.com/module/cmd/a
    example.com/module/cmd/b
)
```

### Diretiva `ignore` {#go-mod-file-ignore}

Uma diretiva `ignore` fará com que o comando go ignore os caminhos de diretórios separados por barra,
e quaisquer arquivos ou diretórios contidos neles recursivamente, ao corresponder
padrões de pacotes.

Se o caminho começar com `./`, o caminho é interpretado em relação à
raiz do módulo, e esse diretório e quaisquer diretórios ou arquivos
contidos nele recursivamente serão ignorados ao corresponder padrões de pacotes.

Caso contrário, quaisquer diretórios com o caminho em qualquer profundidade no módulo, e
quaisquer diretórios ou arquivos contidos neles recursivamente, serão ignorados.

```
IgnoreDirective = "ignore" ( IgnoreSpec | "(" newline { IgnoreSpec } ")" newline ) .
IgnoreSpec = RelativeFilePath newline .
RelativeFilePath = /* slash-separated relative file path */ .
```

Exemplo
```
ignore ./node_modules

ignore (
    static
    content/html
    ./third_party/javascript
)
```

### Diretiva `exclude` {#go-mod-file-exclude}

Uma diretiva `exclude` impede que uma versão de módulo seja carregada pelo comando
`go`.

Desde o Go 1.16, se uma versão referenciada por uma diretiva `require` em qualquer arquivo
`go.mod` for excluída por uma diretiva `exclude` no arquivo `go.mod` do módulo principal,
o requisito é ignorado. Isso pode fazer com que comandos como [`go get`](#go-get)
e [`go mod tidy`](#go-mod-tidy) adicionem novos requisitos para versões superiores no
`go.mod`, com um comentário `// indirect`, se apropriado.

Antes do Go 1.16, se uma versão excluída fosse referenciada por uma diretiva `require`,
o comando `go` listava as versões disponíveis do módulo (como mostrado com [`go
list -m -versions`](#go-list-m)) e carregava a próxima versão superior não excluída
em seu lugar. Isso podia resultar em seleção de versão não determinística, já que a próxima
versão superior podia mudar com o tempo. Tanto versões de release quanto de pré-release
eram consideradas para esse fim, mas pseudo-versões não. Se
não houvesse versões superiores, o comando `go` reportava um erro.

As diretivas `exclude` só se aplicam ao arquivo `go.mod` do módulo principal e são
ignoradas em outros módulos. Veja [Seleção mínima de versão](#minimal-version-selection)
para detalhes.

```
ExcludeDirective = "exclude" ( ExcludeSpec | "(" newline { ExcludeSpec } ")" newline ) .
ExcludeSpec = ModulePath Version newline .
```

Exemplo:

```
exclude golang.org/x/net v1.2.3

exclude (
    golang.org/x/crypto v1.4.5
    golang.org/x/text v1.6.7
)
```

### Diretiva `replace` {#go-mod-file-replace}

Uma diretiva `replace` substitui o conteúdo de uma versão específica de um módulo,
ou de todas as versões de um módulo, por conteúdo encontrado em outro lugar. A substituição
pode ser especificada com outro caminho de módulo e versão, ou com um
caminho de arquivo específico da plataforma.

Se houver uma versão do lado esquerdo da seta (`=>`), apenas essa versão específica
do módulo é substituída; as outras versões serão acessadas normalmente.
Se a versão da esquerda for omitida, todas as versões do módulo são substituídas.

Se o caminho do lado direito da seta for absoluto ou relativo
(começando com `./` ou `../`), ele é interpretado como o caminho de arquivo local para a
raiz do módulo de substituição, que deve conter um arquivo `go.mod`. A versão
de substituição deve ser omitida neste caso.

Se o caminho do lado direito não for um caminho local, ele deve ser um
caminho de módulo válido. Nesse caso, uma versão é obrigatória. A mesma versão de módulo não
deve também aparecer na build list.

Independentemente de a substituição ser especificada com um caminho local ou com um
caminho de módulo, se o módulo de substituição tiver um arquivo `go.mod`, sua
diretiva `module` deve corresponder ao caminho do módulo que ele substitui.

As diretivas `replace` só se aplicam ao arquivo `go.mod` do módulo principal
e são ignoradas em outros módulos. Veja [Seleção mínima de versão](#minimal-version-selection)
para detalhes.

Se houver vários módulos principais, os arquivos `go.mod` de todos os módulos
principais se aplicam. Diretivas `replace` conflitantes entre módulos
principais não são permitidas, e devem ser removidas ou sobrescritas em
um [replace no arquivo `go.work`](#go-work-file-replace).

Observe que uma diretiva `replace` sozinha não adiciona um módulo ao [grafo de
módulos](#glos-module-graph). Também é necessária uma [diretiva `require`](#go-mod-file-require) que
se refira à versão do módulo substituído, seja no arquivo `go.mod` do módulo principal
ou no arquivo `go.mod` de uma dependência. Uma diretiva `replace` não tem
efeito se a versão do módulo do lado esquerdo não for exigida.

```
ReplaceDirective = "replace" ( ReplaceSpec | "(" newline { ReplaceSpec } ")" newline ) .
ReplaceSpec = ModulePath [ Version ] "=>" FilePath newline
            | ModulePath [ Version ] "=>" ModulePath Version newline .
FilePath = /* platform-specific relative or absolute file path */
```

Exemplo:

```
replace golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5

replace (
    golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5
    golang.org/x/net => example.com/fork/net v1.4.5
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net
)
```

### Diretiva `retract` {#go-mod-file-retract}

Uma diretiva `retract` indica que uma versão ou um intervalo de versões do
módulo definido por `go.mod` não deve ser utilizado como dependência. Uma diretiva `retract` é
útil quando uma versão foi publicada prematuramente ou quando um problema grave é
descoberto depois que a versão foi publicada. Versões retraídas devem continuar
disponíveis em repositórios de controle de versão e em [proxies de
módulos](#glos-module-proxy) para garantir que builds que dependam delas não sejam
quebrados. A palavra *retract* é emprestada da literatura acadêmica: um artigo
científico retratado continua disponível, mas tem problemas e não deve servir de
base para trabalhos futuros.

Quando uma versão de módulo é retraída, os usuários não serão atualizados para ela automaticamente
usando [`go get`](#go-get), [`go mod tidy`](#go-mod-tidy) ou outros
comandos. Builds que dependam de versões retraídas devem continuar funcionando, mas
os usuários serão notificados sobre as retrações quando verificarem atualizações com [`go list
-m -u`](#go-list-m) ou atualizarem um módulo relacionado com [`go get`](#go-get).

Para retrair uma versão, o autor do módulo deve adicionar uma diretiva `retract` ao
`go.mod` e, em seguida, publicar uma nova versão contendo essa diretiva. A nova versão
deve ser superior às demais versões de release ou pré-release; ou seja, a
[consulta de versão](#version-queries) `@latest` deve resolver para a nova versão
antes que as retrações sejam consideradas. O comando `go` carrega e aplica
as retrações da versão exibida por `go list -m -retracted $modpath@latest`
(onde `$modpath` é o caminho do módulo).

Versões retraídas ficam ocultas da lista de versões impressa por [`go list -m
-versions`](#go-list-m), a menos que a flag `-retracted` seja usada. Versões retraídas
são excluídas ao resolver consultas de versão como `@>=v1.2.3` ou
`@latest`.

Uma versão que contém retrações pode retrair a si mesma. Se a
versão de release ou pré-release mais alta de um módulo se retrair, a consulta `@latest`
resolve para uma versão inferior depois que as versões retraídas são excluídas.

Como exemplo, considere o caso em que o autor do módulo `example.com/m`
publica a versão `v1.0.0` por acidente. Para impedir que os usuários atualizem
para `v1.0.0`, o autor pode adicionar duas diretivas `retract` ao `go.mod` e, em seguida, marcar
`v1.0.1` com as retrações.

```
retract (
    v1.0.0 // Published accidentally.
    v1.0.1 // Contains retractions only.
)
```

Quando um usuário executa `go get example.com/m@latest`, o comando `go` lê as
retrações de `v1.0.1`, que agora é a versão mais alta. Tanto `v1.0.0` quanto
`v1.0.1` estão retraídas, então o comando `go` atualizará (ou fará downgrade!) para
a próxima versão mais alta, talvez `v0.9.5`.

Diretivas `retract` podem ser escritas com uma única versão (como `v1.0.0`)
ou com um intervalo fechado de versões com limite superior e inferior, delimitado por
`[` e `]` (como `[v1.1.0, v1.2.0]`). Uma única versão equivale a um
intervalo em que os limites superior e inferior são iguais. Como outras diretivas,
várias diretivas `retract` podem ser agrupadas em um bloco delimitado por
`(` no fim de uma linha e `)` em uma linha própria.

Cada diretiva `retract` deve ter um comentário explicando o motivo da
retração, embora isso não seja obrigatório. O comando `go` pode exibir comentários de
justificativa em avisos sobre versões retraídas e na saída de `go list`. Um
comentário de justificativa pode ser escrito imediatamente acima de uma diretiva `retract`
(sem linha em branco entre eles) ou depois, na mesma linha. Se um comentário
aparecer acima de um bloco, ele se aplica a todas as diretivas `retract` dentro do bloco
que não tenham comentários próprios. Um comentário de justificativa pode ocupar várias linhas.

```
RetractDirective = "retract" ( RetractSpec | "(" newline { RetractSpec } ")" newline ) .
RetractSpec = ( Version | "[" Version "," Version "]" ) newline .
```

Exemplos:

* Retraindo todas as versões entre `v1.0.0` e `v1.9.9`:

```
retract v1.0.0
retract [v1.0.0, v1.9.9]
retract (
    v1.0.0
    [v1.0.0, v1.9.9]
)
```

* Voltando a não versionado após ter lançado prematuramente a versão `v1.0.0`:

```
retract [v0.0.0, v1.0.1] // assuming v1.0.1 contains this retraction.
```

* Eliminando um módulo, incluindo todas as pseudo-versões e versões marcadas:

```
retract [v0.0.0-0, v0.15.2]  // assuming v0.15.2 contains this retraction.
```

A diretiva `retract` foi adicionada no Go 1.16. O Go 1.15 e versões inferiores vão
reportar um erro se uma diretiva `retract` for escrita no arquivo `go.mod` do [módulo
principal](#glos-main-module) e vão ignorar diretivas `retract` nos
arquivos `go.mod` das dependências.

### Atualizações automáticas {#go-mod-file-updates}

A maioria dos comandos informa um erro se o `go.mod` estiver faltando informações ou não refletir com precisão a realidade. Os comandos [`go get`](#go-get) e [`go mod tidy`](#go-mod-tidy) podem ser usados para corrigir a maioria desses problemas. Além disso, a flag `-mod=mod` pode ser usada com a maioria dos comandos cientes de módulos (`go build`, `go test` e assim por diante) para instruir o comando `go` a corrigir automaticamente os problemas em `go.mod` e `go.sum`.

Por exemplo, considere este arquivo `go.mod`:

```
module example.com/M

go 1.23.0

require (
    example.com/A v1
    example.com/B v1.0.0
    example.com/C v1.0.0
    example.com/D v1.2.3
    example.com/E dev
)

exclude example.com/D v1.2.3
```

A atualização acionada com `-mod=mod` reescreve identificadores de versão não canônicos para a forma [canônica](#glos-canonical-version) do semver, então o `v1` de `example.com/A` torna-se `v1.0.0`, e o `dev` de `example.com/E` torna-se a pseudo-versão do commit mais recente na branch `dev`, talvez `v0.0.0-20180523231146-b3f5c0f6e5f1`.

A atualização modifica os requisitos para respeitar as exclusões, então o requisito sobre o `example.com/D v1.2.3`, que foi excluído, é atualizado para usar a próxima versão disponível de `example.com/D`, talvez `v1.2.4` ou `v1.3.0`.

A atualização remove requisitos redundantes ou enganosos. Por exemplo, se `example.com/A v1.0.0` em si requer `example.com/B v1.2.0` e `example.com/C
v1.0.0`, então o requisito do `go.mod` sobre `example.com/B v1.0.0` é enganoso (substituído pela necessidade do `example.com/A` por `v1.2.0`), e o requisito sobre `example.com/C v1.0.0` é redundante (implícito pela necessidade do `example.com/A` pela mesma versão), então ambos serão removidos. Se o módulo principal contiver pacotes que importam diretamente pacotes de `example.com/B` ou `example.com/C`, os requisitos serão mantidos, mas atualizados para as versões realmente em uso.

Por fim, a atualização reformata o `go.mod` em uma formatação canônica, para que futuras mudanças mecânicas resultem em diffs mínimos. O comando `go` não atualizará o `go.mod` se apenas mudanças de formatação forem necessárias.

Como o grafo de módulos define o significado das instruções `import`, quaisquer comandos que carregam pacotes também usam o `go.mod` e, portanto, podem atualizá-lo, incluindo `go build`, `go get`, `go install`, `go list`, `go test` e `go mod tidy`.

No Go 1.15 e anteriores, a flag `-mod=mod` era habilitada por padrão, então as atualizações eram feitas automaticamente. Desde o Go 1.16, o comando `go` age como se `-mod=readonly` estivesse definido: se for necessária alguma mudança no `go.mod`, o comando `go` informa um erro e sugere uma correção.

## Seleção mínima de versão (MVS) {#minimal-version-selection}

O Go usa um algoritmo chamado <dfn>Seleção mínima de versão (MVS)</dfn> para selecionar um conjunto de versões de módulos a usar ao compilar pacotes. O MVS é descrito em detalhes em [Minimal Version Selection](https://research.swtch.com/vgo-mvs), por Russ Cox.

Conceitualmente, o MVS opera sobre um grafo direcionado de módulos, especificado por [arquivos `go.mod`](#glos-go-mod-file). Cada vértice do grafo representa uma versão de módulo. Cada aresta representa uma versão mínima necessária de uma dependência, especificada usando uma diretiva [`require`](#go-mod-file-require). O grafo pode ser modificado pelas diretivas [`exclude`](#go-mod-file-exclude) e [`replace`](#go-mod-file-replace) nos arquivos `go.mod` do(s) módulo(s) principal(is) e pelas diretivas [`replace`](#go-work-file-replace) no arquivo `go.work`.

O MVS produz a [build list](#glos-build-list) como saída, a lista de versões de módulos usadas em uma compilação.

O MVS começa nos módulos principais (vértices especiais do grafo que não têm versão) e percorre o grafo, acompanhando a maior versão requerida de cada módulo. Ao final da travessia, as maiores versões requeridas compõem a build list: são as versões mínimas que satisfazem todos os requisitos.

A build list pode ser inspecionada com o comando [`go list -m all`](#go-list-m). Diferentemente de outros sistemas de gerenciamento de dependências, a build list não é salva em um arquivo de "lock". O MVS é determinístico, e a build list não muda quando novas versões das dependências são lançadas, então o MVS é usado para calculá-la no início de cada comando ciente de módulos.

Considere o exemplo no diagrama abaixo. O módulo principal requer o módulo A na versão 1.2 ou superior e o módulo B na versão 1.2 ou superior. A 1.2 e B 1.2 requerem C 1.3 e C 1.4, respectivamente. C 1.3 e C 1.4 requerem ambos D 1.2.

![Grafo de versões de módulos com as versões visitadas destacadas](/doc/mvs/buildlist.svg "Grafo da build list do MVS")

O MVS visita e carrega o arquivo `go.mod` de cada uma das versões de módulos destacadas em azul. Ao final da travessia do grafo, o MVS retorna uma build list contendo as versões em negrito: A 1.2, B 1.2, C 1.4 e D 1.2. Observe que versões superiores de B e D estão disponíveis, mas o MVS não as seleciona, já que nada as requer.

### Substituição {#mvs-replace}

O conteúdo de um módulo (incluindo seu arquivo `go.mod`) pode ser substituído usando uma [diretiva `replace`](#go-mod-file-replace) no arquivo `go.mod` de um módulo principal ou no arquivo `go.work` de um workspace. Uma diretiva `replace` pode se aplicar a uma versão específica de um módulo ou a todas as versões de um módulo.

Substituições alteram o grafo de módulos, já que um módulo substituto pode ter dependências diferentes das versões substituídas.

Considere o exemplo abaixo, em que C 1.4 foi substituído por R. R depende de D 1.3 em vez de D 1.2, então o MVS retorna uma build list contendo A 1.2, B 1.2, C 1.4 (substituído por R) e D 1.3.

![Grafo de versões de módulos com uma substituição](/doc/mvs/replace.svg "Substituição no MVS")

### Exclusão {#mvs-exclude}

Um módulo também pode ser excluído em versões específicas usando uma [diretiva `exclude`](#go-mod-file-exclude) no arquivo `go.mod` do módulo principal.

Exclusões também alteram o grafo de módulos. Quando uma versão é excluída, ela é removida do grafo de módulos, e os requisitos sobre ela são redirecionados para a próxima versão superior.

Considere o exemplo abaixo. C 1.3 foi excluído. O MVS agirá como se A 1.2 tivesse requerido C 1.4 (a próxima versão superior) em vez de C 1.3.

![Grafo de versões de módulos com uma exclusão](/doc/mvs/exclude.svg "Exclusão no MVS")

### Atualizações de versão {#mvs-upgrade}

O comando [`go get`](#go-get) pode ser usado para atualizar um conjunto de módulos. Para realizar uma atualização, o comando `go` altera o grafo de módulos antes de executar o MVS, adicionando arestas das versões visitadas para as versões atualizadas.

Considere o exemplo abaixo. O módulo B pode ser atualizado de 1.2 para 1.3, C de 1.3 para 1.4, e D de 1.2 para 1.3.

![Grafo de versões de módulos com atualizações](/doc/mvs/upgrade.svg "Atualização no MVS")

Atualizações (e downgrades) podem adicionar ou remover dependências indiretas. Neste caso, E 1.1 e F 1.1 aparecem na build list após a atualização, já que E 1.1 é requerido por B 1.3.

Para preservar as atualizações, o comando `go` atualiza os requisitos no `go.mod`. Ele alterará o requisito sobre B para a versão 1.3. Também adicionará requisitos sobre C 1.4 e D 1.3 com comentários `// indirect`, já que essas versões não seriam selecionadas de outra forma.

### Downgrade {#mvs-downgrade}

O comando [`go get`](#go-get) também pode ser usado para fazer downgrade de um conjunto de módulos. Para realizar um downgrade, o comando `go` altera o grafo de módulos removendo as versões acima das versões rebaixadas. Ele também remove versões de outros módulos que dependem das versões removidas, já que elas podem não ser compatíveis com as versões rebaixadas de suas dependências. Se o módulo principal requer uma versão de módulo removida pelo downgrade, o requisito é alterado para uma versão anterior que não foi removida. Se nenhuma versão anterior estiver disponível, o requisito é descartado.

Considere o exemplo abaixo. Suponha que um problema foi encontrado com C 1.4, então fazemos downgrade para C 1.3. C 1.4 é removido do grafo de módulos. B 1.2 também é removido, já que requer C 1.4 ou superior. O requisito do módulo principal sobre B é alterado para 1.1.

![Grafo de versões de módulos com downgrade](/doc/mvs/downgrade.svg "Downgrade no MVS")

O [`go get`](#go-get) também pode remover dependências por completo, usando o sufixo `@none` após um argumento. Isso funciona de forma semelhante a um downgrade. Todas as versões do módulo nomeado são removidas do grafo de módulos.

## Poda do grafo de módulos {#graph-pruning}

Se o módulo principal estiver na versão `go 1.17` ou superior, o [grafo de módulos](#glos-module-graph) usado para a [seleção mínima de versão](#minimal-version-selection) inclui apenas os requisitos _imediatos_ de cada dependência de módulo que especifica `go 1.17` ou superior em seu próprio arquivo `go.mod`, a menos que aquela versão do módulo também seja (transitivamente) requerida por alguma _outra_ dependência na versão `go 1.16` ou inferior. (As dependências _transitivas_ de dependências `go 1.17` são _podadas_ do grafo de módulos.)

Como um arquivo `go.mod` na versão `go 1.17` inclui uma [diretiva require](#go-mod-file-require) para cada dependência necessária para compilar qualquer pacote ou teste desse módulo, o grafo de módulos podado inclui todas as dependências necessárias para executar `go build` ou `go test` nos pacotes de qualquer dependência explicitamente requerida pelo [módulo principal](#glos-main-module). Um módulo que _não_ é necessário para compilar qualquer pacote ou teste de um dado módulo não pode afetar o comportamento em tempo de execução de seus pacotes, então as dependências podadas do grafo de módulos apenas causariam interferência entre módulos que, de outra forma, não estão relacionados.

Módulos cujos requisitos foram podados ainda aparecem no grafo de módulos e ainda são reportados por `go list -m all`: suas [versões selecionadas](#glos-selected-version) são conhecidas e bem definidas, e pacotes podem ser carregados desses módulos (por exemplo, como dependências transitivas de testes carregados de outros módulos). No entanto, como o comando `go` não consegue identificar facilmente quais dependências desses módulos estão satisfeitas, os argumentos para `go build` e `go test` não podem incluir pacotes de módulos cujos requisitos foram podados. O [`go get`](#go-get) promove o módulo que contém cada pacote nomeado a uma dependência explícita, permitindo que `go build` ou `go test` seja invocado nesse pacote.

Como o Go 1.16 e as versões anteriores não suportavam a poda do grafo de módulos, o fechamento transitivo completo de dependências — incluindo dependências transitivas `go 1.17` — ainda é incluído para cada módulo que especifica `go 1.16` ou inferior. (Na versão `go 1.16` e inferiores, o arquivo `go.mod` inclui apenas [dependências diretas](#glos-direct-dependency), então um grafo muito maior precisa ser carregado para garantir que todas as dependências indiretas sejam incluídas.)

O [arquivo `go.sum`](#go-sum-files) registrado pelo [`go mod tidy`](#go-mod-tidy) para um módulo, por padrão, inclui os checksums necessários para a versão do Go _uma abaixo_ da versão especificada na sua [diretiva `go`](#go-mod-file-go). Assim, um módulo `go 1.17` inclui os checksums necessários para o grafo de módulos completo carregado pelo Go 1.16, mas um módulo `go 1.18` incluirá apenas os checksums necessários para o grafo de módulos podado carregado pelo Go 1.17. A flag `-compat` pode ser usada para sobrescrever a versão padrão (por exemplo, para podar o arquivo `go.sum` de forma mais agressiva em um módulo `go 1.17`).

Veja [o documento de design](https://go.googlesource.com/proposal/+/master/design/36460-lazy-module-loading.md) para mais detalhes.

### Carregamento preguiçoso de módulos {#lazy-loading}

Os requisitos mais abrangentes adicionados para a poda do grafo de módulos também habilitam outra otimização ao trabalhar dentro de um módulo. Se o módulo principal estiver na versão `go 1.17` ou superior, o comando `go` evita carregar o grafo de módulos completo até que (e a menos que) seja necessário. Em vez disso, ele carrega apenas o arquivo `go.mod` do módulo principal e, então, tenta carregar os pacotes a serem compilados usando somente esses requisitos. Se um pacote a ser importado (por exemplo, uma dependência de um teste de um pacote fora do módulo principal) não for encontrado entre esses requisitos, o restante do grafo de módulos é carregado sob demanda.

Se todos os pacotes importados puderem ser encontrados sem carregar o grafo de módulos, o comando `go` então carrega os arquivos `go.mod` apenas dos módulos que contêm esses pacotes, e seus requisitos são verificados contra os requisitos do módulo principal para garantir que sejam localmente consistentes. (Inconsistências podem surgir de merges de controle de versão, edições manuais e mudanças em módulos que foram [substituídos](#go-mod-file-replace) usando caminhos do sistema de arquivos local.)

## Workspaces {#workspaces}

Um <dfn>workspace</dfn> é uma coleção de módulos em disco que são usados como módulos principais ao executar a [seleção mínima de versão (MVS)](#minimal-version-selection).

Um workspace pode ser declarado em um [arquivo `go.work`](#go-work-file) que especifica caminhos relativos para os diretórios de módulos de cada um dos módulos do workspace. Quando não existe arquivo `go.work`, o workspace consiste no único módulo que contém o diretório atual.

A maioria dos subcomandos `go` que trabalham com módulos opera sobre o conjunto de módulos determinado pelo workspace atual. `go mod init`, `go mod why`, `go mod edit`, `go mod tidy`, `go mod vendor` e `go get` sempre operam sobre um único módulo principal.

Um comando determina se está em um contexto de workspace examinando primeiro a variável de ambiente `GOWORK`. Se `GOWORK` estiver definida como `off`, o comando estará em um contexto de módulo único. Se estiver vazia ou não for fornecida, o comando buscará no diretório de trabalho atual e, em seguida, nos diretórios pais sucessivos, por um arquivo `go.work`. Se um arquivo for encontrado, o comando operará no workspace que ele define; caso contrário, o workspace incluirá apenas o módulo que contém o diretório de trabalho.
Se `GOWORK` indicar um caminho para um arquivo existente que termina em .work, o modo workspace será habilitado. Qualquer outro valor é um erro. Você pode usar o comando `go env GOWORK` para determinar qual arquivo `go.work` o comando `go` está usando. `go env GOWORK` ficará vazio se o comando `go` não estiver no modo workspace.

### Arquivos `go.work` {#go-work-file}

Um workspace é definido por um arquivo de texto codificado em UTF-8 chamado `go.work`. O arquivo `go.work` é orientado a linhas. Cada linha contém uma única diretiva, formada por uma palavra-chave seguida de argumentos. Por exemplo:

```
go 1.23.0

use ./my/first/thing
use ./my/second/thing

replace example.com/bad/thing v1.4.5 => example.com/good/thing v1.4.5
```

Assim como nos arquivos `go.mod`, uma palavra-chave inicial pode ser fatorada de linhas adjacentes para criar um bloco.

```
use (
    ./my/first/thing
    ./my/second/thing
)
```

O comando `go` oferece vários subcomandos para manipular arquivos `go.work`. [`go work init`](#go-work-init) cria novos arquivos `go.work`. [`go work use`](#go-work-use) adiciona diretórios de módulos ao arquivo `go.work`. [`go work edit`](#go-work-edit) realiza edições de baixo nível. O pacote
[`golang.org/x/mod/modfile`](https://pkg.go.dev/golang.org/x/mod/modfile?tab=doc)
pode ser usado por programas Go para fazer as mesmas alterações programaticamente.

O comando go manterá um arquivo `go.work.sum` que registra os hashes usados pelo workspace que não estão nos arquivos go.sum dos módulos coletivos do workspace.

Geralmente não é recomendado versionar arquivos go.work em sistemas de controle de versão, por dois motivos:

* Um arquivo `go.work` versionado pode sobrescrever o arquivo `go.work` próprio de um desenvolvedor em um diretório pai, causando confusão quando as diretivas `use` dele não se aplicarem.
* Um arquivo `go.work` versionado pode fazer com que um sistema de integração contínua (CI) selecione e, portanto, teste as versões erradas das dependências de um módulo. Sistemas de CI geralmente não devem ter permissão para usar o arquivo `go.work`, para que possam testar o comportamento do módulo da forma como ele seria usado quando requerido por outros módulos, onde um arquivo `go.work` dentro do próprio módulo não tem efeito.

Dito isso, há alguns casos em que versionar um arquivo `go.work` faz sentido. Por exemplo, quando os módulos de um repositório são desenvolvidos exclusivamente uns com os outros e não em conjunto com módulos externos, pode não haver razão para o desenvolvedor querer usar uma combinação diferente de módulos em um workspace. Nesse caso, o autor do módulo deve garantir que os módulos individuais sejam testados e lançados corretamente.

### Elementos léxicos {#go-work-file-lexical}

Os elementos léxicos em arquivos `go.work` são definidos exatamente da mesma forma [que para `go.mod files`](#go-mod-file-lexical).

### Gramática {#go-work-file-grammar}

A sintaxe de `go.work` é especificada abaixo usando a Forma Normal de Backus-Naur Estendida (EBNF).
Consulte a [seção Notation na Especificação da Linguagem Go](/ref/spec#Notation)
para detalhes sobre a sintaxe EBNF.

```
GoWork = { Directive } .
Directive = GoDirective |
            ToolchainDirective |
            UseDirective |
            ReplaceDirective .
```

Quebras de linha, identificadores e strings são denotados por `newline`, `ident` e
`string`, respectivamente.

Caminhos de módulos e versões são denotados por `ModulePath` e `Version`.
Caminhos de módulos e versões são especificados exatamente da mesma forma [que para
`go.mod files`](#go-mod-file-lexical).

```
ModulePath = ident | string . /* see restrictions above */
Version = ident | string .    /* see restrictions above */
```

### Diretiva `go` {#go-work-file-go}

Uma diretiva `go` é obrigatória em um arquivo `go.work` válido. A versão deve ser
uma versão válida de release do Go: um inteiro positivo seguido de um ponto e um
inteiro não negativo (por exemplo, `1.18`, `1.19`).

A diretiva `go` indica a versão do toolchain do go com a qual o arquivo
`go.work` deve funcionar. Se forem feitas alterações no formato do arquivo
`go.work`, versões futuras do toolchain interpretarão o arquivo de acordo com a
versão indicada.

Um arquivo `go.work` pode conter no máximo uma diretiva `go`.

```
GoDirective = "go" GoVersion newline .
GoVersion = string | ident .  /* valid release version; see above */
```

Exemplo:

```
go 1.23.0
```

### Diretiva `toolchain` {#go-work-file-toolchain}

Uma diretiva `toolchain` declara um toolchain do Go sugerido para usar em um workspace.
Ela só tem efeito quando o toolchain padrão é mais antigo que o toolchain sugerido.

Para detalhes, consulte “[Toolchains do Go](/doc/toolchain)”.

```
ToolchainDirective = "toolchain" ToolchainName newline .
ToolchainName = string | ident .  /* valid toolchain name; see “Go toolchains” */
```

Exemplo:

```
toolchain go1.21.0
```

### Diretiva `godebug` {#go-work-file-godebug}

Uma diretiva `godebug` declara uma única [configuração GODEBUG](/doc/godebug)
a ser aplicada ao trabalhar neste workspace.
A sintaxe e o efeito são os mesmos da [diretiva `godebug` do arquivo `go.mod`](#go-mod-file-godebug).
Quando um workspace está em uso, as diretivas `godebug` em arquivos `go.mod` são ignoradas.


### Diretiva `use` {#go-work-file-use}

Uma diretiva `use` adiciona um módulo em disco ao conjunto de módulos principais
em um workspace. Seu argumento é um caminho relativo para o diretório que contém o
arquivo `go.mod` do módulo. Uma diretiva `use` não adiciona módulos contidos em
subdiretórios do diretório do seu argumento. Esses módulos podem ser adicionados
pelo diretório que contém seu arquivo `go.mod`, em diretivas `use` separadas.

```
UseDirective = "use" ( UseSpec | "(" newline { UseSpec } ")" newline ) .
UseSpec = FilePath newline .
FilePath = /* platform-specific relative or absolute file path */

```

Exemplo:

```
use ./mymod  // example.com/mymod

use (
    ../othermod
    ./subdir/thirdmod
)
```

### Diretiva `replace` {#go-work-file-replace}

Semelhante a uma diretiva `replace` em um arquivo `go.mod`, uma diretiva `replace` em
um arquivo `go.work` substitui o conteúdo de uma versão específica de um módulo,
ou de todas as versões de um módulo, por conteúdo encontrado em outro lugar. Um
replace com curinga em `go.work` sobrescreve um `replace` específico de versão em
um arquivo `go.mod`.

As diretivas `replace` em arquivos `go.work` sobrescrevem quaisquer replaces do mesmo
módulo ou versão de módulo nos módulos do workspace.

```
ReplaceDirective = "replace" ( ReplaceSpec | "(" newline { ReplaceSpec } ")" newline ) .
ReplaceSpec = ModulePath [ Version ] "=>" FilePath newline
            | ModulePath [ Version ] "=>" ModulePath Version newline .
FilePath = /* platform-specific relative or absolute file path */
```

Exemplo:

```
replace golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5

replace (
    golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5
    golang.org/x/net => example.com/fork/net v1.4.5
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net
)
```

## Compatibilidade com repositórios que não são módulos {#non-module-compat}

Para garantir uma transição tranquila do `GOPATH` para módulos, o comando `go` pode
baixar e compilar pacotes no modo ciente de módulos a partir de repositórios que
ainda não migraram para módulos, adicionando um [arquivo `go.mod`](#glos-go-mod-file).

Quando o comando `go` baixa um módulo em uma determinada versão [diretamente](#vcs)
de um repositório, ele procura uma URL do repositório para o caminho do módulo,
mapeia a versão para uma revisão dentro do repositório e então extrai um arquivo
compactado do repositório nessa revisão. Se o [caminho do módulo](#glos-module-path)
for igual ao [caminho raiz do repositório](#glos-repository-root-path), e o diretório
raiz do repositório não contiver um arquivo `go.mod`, o comando `go` sintetiza um
arquivo `go.mod` no cache de módulos que contém uma [diretiva `module`](#go-mod-file-module)
e nada mais. Como os arquivos `go.mod` sintéticos não contêm [diretivas `require`](#go-mod-file-require)
para suas dependências, outros módulos que dependem deles podem precisar de diretivas
`require` adicionais (com comentários `// indirect`) para garantir que cada dependência
seja obtida na mesma versão em cada build.

Quando o comando `go` baixa um módulo de um
[proxy](#communicating-with-proxies), ele baixa o arquivo `go.mod` separadamente do
restante do conteúdo do módulo. Espera-se que o proxy forneça um arquivo `go.mod`
sintético caso o módulo original não possua um.

### Versões `+incompatible` {#incompatible-versions}

Um módulo lançado na versão principal 2 ou superior deve ter um [sufixo de versão
principal](#major-version-suffixes) correspondente em seu caminho de módulo. Por exemplo,
se um módulo for lançado como `v2.0.0`, seu caminho deve ter o sufixo `/v2`. Isso
permite que o comando `go` trate múltiplas versões principais de um projeto como
módulos distintos, mesmo que sejam desenvolvidas no mesmo repositório.

O requisito de sufixo de versão principal foi introduzido quando o suporte a módulos
foi adicionado ao comando `go`, e muitos repositórios já tinham versões com tag de
versão principal `2` ou superior antes disso. Para manter a compatibilidade com esses
repositórios, o comando `go` adiciona o sufixo `+incompatible` a versões com versão
principal 2 ou superior sem um arquivo `go.mod`. `+incompatible` indica que uma versão
faz parte do mesmo módulo que versões com números de versão principal inferiores;
consequentemente, o comando `go` pode atualizar automaticamente para versões
`+incompatible` mais altas, mesmo que isso possa quebrar a build.

Considere o exemplo de requisito abaixo:

```
require example.com/m v4.1.2+incompatible
```

A versão `v4.1.2+incompatible` refere-se à [tag de versão semântica](#glos-semantic-version-tag)
`v4.1.2` no repositório que fornece o módulo `example.com/m`. O módulo deve estar no
diretório raiz do repositório (ou seja, o [caminho raiz do repositório](#glos-module-path)
também deve ser `example.com/m`), e um arquivo `go.mod` não deve estar presente. O módulo
pode ter versões com números de versão principal inferiores, como `v1.5.2`, e o comando
`go` pode atualizar automaticamente para `v4.1.2+incompatible` a partir dessas versões
(veja [seleção mínima de versão (MVS)](#minimal-version-selection) para informações sobre
como as atualizações funcionam).

Um repositório que migra para módulos após a versão `v2.0.0` ter sido marcada deve
normalmente lançar uma nova versão principal. No exemplo acima, o autor deve criar um
módulo com o caminho `example.com/m/v5` e lançar a versão `v5.0.0`. O autor também deve
atualizar os imports de pacotes no módulo para usar o prefixo `example.com/m/v5` em vez
de `example.com/m`. Veja [Go Modules: v2 e além](/blog/v2-go-modules) para um exemplo
mais detalhado.

Observe que o sufixo `+incompatible` não deve aparecer em uma tag em um repositório;
uma tag como `v4.1.2+incompatible` será ignorada. O sufixo aparece apenas em versões
usadas pelo comando `go`. Veja [Mapeamento de versões para commits](#vcs-version)
para detalhes sobre a distinção entre versões e tags.

Observe também que o sufixo `+incompatible` pode aparecer em
[pseudo-versões](#glos-pseudo-version). Por exemplo,
`v2.0.1-20200722182040-012345abcdef+incompatible` pode ser uma pseudo-versão válida.

### Compatibilidade mínima de módulos {#minimal-module-compatibility}

Um módulo lançado na versão principal 2 ou superior é obrigado a ter um [sufixo de
versão principal](#glos-major-version-suffix) em seu [caminho de módulo](#glos-module-path).
O módulo pode ou não ser desenvolvido em um [subdiretório de versão
principal](#glos-major-version-subdirectory) dentro de seu repositório. Isso tem
implicações para pacotes que importam pacotes dentro do módulo ao compilar no modo
`GOPATH`.

Normalmente no modo `GOPATH`, um pacote é armazenado em um diretório correspondente ao
[caminho raiz do repositório](#glos-repository-root-path) combinado com seu diretório
dentro do repositório. Por exemplo, um pacote no repositório com caminho raiz
`example.com/repo` no subdiretório `sub` seria armazenado em
`$GOPATH/src/example.com/repo/sub` e seria importado como `example.com/repo/sub`.

Para um módulo com sufixo de versão principal, pode-se esperar encontrar o pacote
`example.com/repo/v2/sub` no diretório `$GOPATH/src/example.com/repo/v2/sub`. Isso
exigiria que o módulo fosse desenvolvido no subdiretório `v2` de seu repositório. O
comando `go` oferece suporte a isso, mas não o exige (veja [Mapeamento de versões para
commits](#vcs-version)).

Se um módulo *não* for desenvolvido em um subdiretório de versão principal, seu diretório
no `GOPATH` não conterá o sufixo de versão principal, e seus pacotes poderão ser importados
sem o sufixo. No exemplo acima, o pacote seria encontrado no diretório
`$GOPATH/src/example.com/repo/sub` e seria importado como `example.com/repo/sub`.

Isso cria um problema para pacotes destinados a serem compilados tanto no modo de módulo
quanto no modo `GOPATH`: o modo de módulo exige um sufixo, enquanto o modo `GOPATH` não.

Para resolver isso, a <dfn>compatibilidade mínima de módulos</dfn> foi adicionada no Go 1.11
e retroportada para o Go 1.9.7 e 1.10.3. Quando um caminho de import é resolvido para um
diretório no modo `GOPATH`:

* Ao resolver um import da forma `$modpath/$vn/$dir`, onde:
  * `$modpath` é um caminho de módulo válido,
  * `$vn` é um sufixo de versão principal,
  * `$dir` é um subdiretório possivelmente vazio,
* Se todas as seguintes condições forem verdadeiras:
  * O pacote `$modpath/$vn/$dir` não está presente em nenhum [diretório `vendor`](#glos-vendor-directory)
    relevante.
  * Um arquivo `go.mod` está presente no mesmo diretório do arquivo que faz o import ou em
    qualquer diretório pai até a raiz `$GOPATH/src`,
  * Nenhum diretório `$GOPATH[i]/src/$modpath/$vn/$suffix` existe (para qualquer raiz `$GOPATH[i]`),
  * O arquivo `$GOPATH[d]/src/$modpath/go.mod` existe (para alguma raiz `$GOPATH[d]`) e declara
    o caminho do módulo como `$modpath/$vn`,
* Então o import de `$modpath/$vn/$dir` é resolvido para o diretório
  `$GOPATH[d]/src/$modpath/$dir`.

Essa regra permite que pacotes que foram migrados para módulos importem outros pacotes que
foram migrados para módulos quando compilados no modo `GOPATH`, mesmo quando um subdiretório
de versão principal não foi usado.

## Comandos cientes de módulos {#mod-commands}

A maioria dos comandos `go` pode ser executada no *modo ciente de módulos* ou no *modo
`GOPATH`*. No modo ciente de módulos, o comando `go` usa arquivos `go.mod` para encontrar
dependências versionadas, e normalmente carrega pacotes do [cache de módulos](#glos-module-cache),
baixando módulos que estejam ausentes. No modo `GOPATH`, o comando `go` ignora módulos; ele
procura nos [diretórios `vendor`](#glos-vendor-directory) e no `GOPATH` para encontrar
dependências.

A partir do Go 1.16, o modo ciente de módulos é habilitado por padrão, independentemente de
haver ou não um arquivo `go.mod` presente. Em versões anteriores, o modo ciente de módulos
era habilitado quando um arquivo `go.mod` estava presente no diretório atual ou em qualquer
diretório pai.

O modo ciente de módulos pode ser controlado pela variável de ambiente `GO111MODULE`, que
pode ser definida como `on`, `off` ou `auto`.

* Se `GO111MODULE=off`, o comando `go` ignora arquivos `go.mod` e executa no modo `GOPATH`.
* Se `GO111MODULE=on` ou não estiver definida, o comando `go` executa no modo ciente de
  módulos, mesmo quando nenhum arquivo `go.mod` está presente. Nem todos os comandos funcionam
  sem um arquivo `go.mod`: veja [Comandos de módulo fora de um módulo](#commands-outside).
* Se `GO111MODULE=auto`, o comando `go` executa no modo ciente de módulos se um arquivo
  `go.mod` estiver presente no diretório atual ou em qualquer diretório pai. No Go 1.15 e
  versões inferiores, esse era o comportamento padrão. Os subcomandos `go mod` e `go install`
  com uma [consulta de versão](#version-queries) executam no modo ciente de módulos mesmo que
  nenhum arquivo `go.mod` esteja presente.

No modo ciente de módulos, `GOPATH` não define mais o significado dos imports durante uma
build, mas ainda armazena dependências baixadas (em `GOPATH/pkg/mod`; veja
[Cache de módulos](#module-cache)) e comandos instalados (em `GOPATH/bin`, a menos que
`GOBIN` esteja definida).

### Comandos de build {#build-commands}

Todos os comandos que carregam informações sobre pacotes são cientes de módulos. Isso inclui:

* `go build`
* `go fix`
* `go generate`
* `go install`
* `go list`
* `go run`
* `go test`
* `go vet`

Quando executados no modo ciente de módulos, esses comandos usam arquivos `go.mod` para
interpretar caminhos de import listados na linha de comando ou escritos em arquivos-fonte Go.
Esses comandos aceitam as seguintes flags, comuns a todos os comandos de módulo.

* A flag `-mod` controla se o `go.mod` pode ser atualizado automaticamente e se o diretório
  `vendor` é usado.
  * `-mod=mod` instrui o comando `go` a ignorar o diretório vendor e a
     [atualizar automaticamente](#go-mod-file-updates) o `go.mod`, por exemplo, quando um pacote
     importado não é fornecido por nenhum módulo conhecido.
  * `-mod=readonly` instrui o comando `go` a ignorar o diretório `vendor` e a reportar um erro
    se o `go.mod` precisar ser atualizado.
  * `-mod=vendor` instrui o comando `go` a usar o diretório `vendor`. Nesse modo, o comando
    `go` não usará a rede nem o cache de módulos.
  * Por padrão, se a [versão do `go`](#go-mod-file-go) no `go.mod` for `1.14` ou superior e um
    diretório `vendor` estiver presente, o comando `go` age como se `-mod=vendor` tivesse sido
    usado. Caso contrário, o comando `go` age como se `-mod=readonly` tivesse sido usado.
  * `go get` rejeita essa flag, pois o propósito do comando é modificar dependências, o que só
    é permitido com `-mod=mod`.
* A flag `-modcacherw` instrui o comando `go` a criar novos diretórios no cache de módulos com
  permissões de leitura e escrita, em vez de torná-los somente leitura. Quando essa flag é usada
  de forma consistente (normalmente definindo `GOFLAGS=-modcacherw` no ambiente ou executando
  `go env -w GOFLAGS=-modcacherw`), o cache de módulos pode ser excluído com comandos como
  `rm -r` sem alterar as permissões antes. O comando [`go clean -modcache`](#go-clean-modcache)
  pode ser usado para excluir o cache de módulos, esteja ou não `-modcacherw` em uso.
* A flag `-modfile=file.mod` instrui o comando `go` a ler (e possivelmente escrever) um arquivo
  alternativo em vez de `go.mod` no diretório raiz do módulo. O nome do arquivo deve terminar
  com `.mod`. Um arquivo chamado `go.mod` ainda deve estar presente para determinar o diretório
  raiz do módulo, mas ele não é acessado. Quando `-modfile` é especificado, um arquivo `go.sum`
  alternativo também é usado: seu caminho é derivado da flag `-modfile` removendo a extensão
  `.mod` e acrescentando `.sum`.

### Vendoring {#vendoring}

Ao usar módulos, o comando `go` normalmente satisfaz as dependências baixando módulos de suas origens para o cache de módulos e, em seguida, carregando os pacotes a partir dessas cópias baixadas. <dfn>Vendoring</dfn> pode ser usado para permitir a interoperação com versões mais antigas do Go ou para garantir que todos os arquivos usados em um build sejam armazenados em uma única árvore de arquivos.

O comando [`go mod vendor`](#go-mod-vendor) cria um diretório chamado
`vendor` no diretório raiz do [módulo principal](#glos-main-module), contendo
cópias de todos os pacotes necessários para compilar e testar os pacotes do
módulo principal. Pacotes que são importados apenas pelos testes de pacotes fora
do módulo principal não são incluídos. Assim como ocorre com
[`go mod tidy`](#go-mod-tidy) e outros comandos de módulo, [restrições de
build](#glos-build-constraint) (exceto `ignore`) não são consideradas ao
construir o diretório `vendor`.

`go mod vendor` também cria o arquivo `vendor/modules.txt`, que contém uma lista
de pacotes vendorizados e as versões de módulo de onde foram copiados. Quando o
vendoring está habilitado, esse manifesto é usado como fonte de informações sobre
versões de módulos, conforme exibido por [`go list -m`](#go-list-m) e [`go
version -m`](#go-version-m). Quando o comando `go` lê `vendor/modules.txt`, ele
verifica se as versões dos módulos são consistentes com o `go.mod`. Se o `go.mod`
tiver sido alterado desde que `vendor/modules.txt` foi gerado, o comando `go`
reportará um erro. `go mod vendor` deve ser executado novamente para atualizar o
diretório `vendor`.

Se o diretório `vendor` estiver presente no diretório raiz do módulo principal,
ele será usado automaticamente caso a [versão do `go`](#go-mod-file-go) no
[arquivo `go.mod`](#glos-go-mod-file) do módulo principal seja `1.14` ou superior.
Para habilitar explicitamente o vendoring, invoque o comando `go` com a flag
`-mod=vendor`. Para desabilitar o vendoring, use a flag `-mod=readonly` ou
`-mod=mod`.

Quando o vendoring está habilitado, [comandos de build](#build-commands), como
`go build` e `go test`, carregam pacotes do diretório `vendor` em vez de acessar
a rede ou o cache de módulos local. O comando [`go list -m`](#go-list-m) apenas
exibe informações sobre os módulos listados no `go.mod`. Comandos `go mod`, como
[`go mod download`](#go-mod-download) e [`go mod tidy`](#go-mod-tidy), não
funcionam de forma diferente quando o vendoring está habilitado e continuam
baixando módulos e acessando o cache de módulos. [`go get`](#go-get) também não
funciona de forma diferente quando o vendoring está habilitado.

Diferentemente do [vendoring no modo `GOPATH`](/s/go15vendor), o comando `go`
ignora diretórios vendor em locais que não sejam o diretório raiz do módulo
principal. Além disso, como os diretórios vendor de outros módulos não são usados,
o comando `go` não inclui diretórios vendor ao construir [arquivos zip de
módulo](#zip-files) (mas veja os bugs conhecidos [#31562](/issue/31562) e
[#37397](/issue/37397)).

### `go get` {#go-get}

Uso:

```
go get [-d] [-t] [-u] [build flags] [packages]
```

Exemplos:

```
# Upgrade a specific module.
$ go get golang.org/x/net

# Upgrade modules that provide packages imported by packages in the main module.
$ go get -u ./...

# Upgrade or downgrade to a specific version of a module.
$ go get golang.org/x/text@v0.3.2

# Update to the commit on the module's master branch.
$ go get golang.org/x/text@master

# Remove a dependency on a module and downgrade modules that require it
# to versions that don't require it.
$ go get golang.org/x/text@none

# Upgrade the minimum required Go version for the main module.
$ go get go

# Upgrade the suggested Go toolchain, leaving the minimum Go version alone.
$ go get toolchain

# Upgrade to the latest patch release of the suggested Go toolchain.
$ go get toolchain@patch
```

O comando `go get` atualiza as dependências de módulo no [arquivo `go.mod`](#go-mod-file)
do [módulo principal](#glos-main-module) e, em seguida, compila e instala os
pacotes listados na linha de comando.

O primeiro passo é determinar quais módulos atualizar. `go get` aceita como
argumentos uma lista de pacotes, padrões de pacotes e caminhos de módulos. Se um
argumento de pacote for especificado, `go get` atualiza o módulo que fornece o
pacote. Se um padrão de pacote for especificado (por exemplo, `all` ou um caminho
com o curinga `...`), `go get` expande o padrão para um conjunto de pacotes e, em
seguida, atualiza os módulos que fornecem esses pacotes. Se um argumento indicar
um módulo, mas não um pacote (por exemplo, o módulo `golang.org/x/net` não tem
nenhum pacote em seu diretório raiz), `go get` atualizará o módulo, mas não
compilará nenhum pacote. Se nenhum argumento for especificado, `go get` age como
se `.` tivesse sido especificado (o pacote no diretório atual); isso pode ser
usado junto com a flag `-u` para atualizar os módulos que fornecem pacotes
importados.

Cada argumento pode incluir um <dfn>sufixo de consulta de versão</dfn> indicando a
versão desejada, como em `go get golang.org/x/text@v0.3.0`. Um sufixo de consulta
de versão consiste em um símbolo `@` seguido de uma [consulta de versão](#version-queries),
que pode indicar uma versão específica (`v0.3.0`), um prefixo de versão (`v0.3`),
o nome de um branch ou tag (`master`), uma revisão (`1234abcd`) ou uma das
consultas especiais `latest`, `upgrade`, `patch` ou `none`. Se nenhuma versão for
informada, `go get` usa a consulta `@upgrade`.

Depois que `go get` resolve seus argumentos para módulos e versões específicos,
`go get` adicionará, alterará ou removerá diretivas [`require`](#go-mod-file-require)
no arquivo `go.mod` do módulo principal para garantir que os módulos permaneçam nas
versões desejadas no futuro. Observe que as versões exigidas nos arquivos `go.mod`
são *versões mínimas* e podem ser aumentadas automaticamente conforme novas
dependências são adicionadas. Veja [Seleção de versão mínima (MVS)](#minimal-version-selection)
para mais detalhes sobre como as versões são selecionadas e como os conflitos são
resolvidos pelos comandos com reconhecimento de módulo.

Outros módulos podem ser atualizados quando um módulo indicado na linha de comando
é adicionado, atualizado ou rebaixado, se a nova versão desse módulo exigir outros
módulos em versões mais altas. Por exemplo, suponha que o módulo `example.com/a`
seja atualizado para a versão `v1.5.0` e que essa versão exija o módulo
`example.com/b` na versão `v1.2.0`. Se o módulo `example.com/b` estiver atualmente
exigido na versão `v1.1.0`, `go get example.com/a@v1.5.0` também atualizará
`example.com/b` para `v1.2.0`.

![go get atualizando uma exigência transitiva](/doc/mvs/get-upgrade.svg)

Outros módulos podem ser rebaixados quando um módulo indicado na linha de comando
é rebaixado ou removido. Continuando o exemplo acima, suponha que o módulo
`example.com/b` seja rebaixado para `v1.1.0`. O módulo `example.com/a` também
seria rebaixado para uma versão que exija `example.com/b` na versão `v1.1.0` ou
inferior.

![go get rebaixando uma exigência transitiva](/doc/mvs/get-downgrade.svg)

Uma exigência de módulo pode ser removida usando o sufixo de versão `@none`. Esse é
um tipo especial de rebaixamento. Módulos que dependem do módulo removido serão
rebaixados ou removidos conforme necessário. Uma exigência de módulo pode ser
removida mesmo que um ou mais de seus pacotes sejam importados por pacotes do
módulo principal. Nesse caso, o próximo comando de build poderá adicionar uma nova
exigência de módulo.

Se um módulo for necessário em duas versões diferentes (especificadas explicitamente
nos argumentos da linha de comando ou para atender a atualizações e rebaixamentos),
`go get` reportará um erro.

Depois que `go get` seleciona um novo conjunto de versões, ele verifica se alguma
das versões de módulo recém-selecionadas, ou algum módulo que fornece pacotes
indicados na linha de comando, foi [retraído](#glos-retracted-version) ou
[descontinuado](#glos-deprecated-module). `go get` exibe um aviso para cada versão
retraída ou módulo descontinuado que encontrar. [`go list -m -u
all`](#go-list-m) pode ser usado para verificar retrações e descontinuações em
todas as dependências.

Depois que `go get` atualiza o arquivo `go.mod`, ele compila os pacotes indicados
na linha de comando. Os executáveis serão instalados no diretório indicado pela
variável de ambiente `GOBIN`, que assume como padrão `$GOPATH/bin` ou
`$HOME/go/bin` caso a variável de ambiente `GOPATH` não esteja definida.

`go get` oferece suporte às seguintes flags:

* A flag `-d` instrui `go get` a não compilar nem instalar pacotes. Quando `-d` é
  usada, `go get` apenas gerencia as dependências em `go.mod`. Usar `go get` sem
  `-d` para compilar e instalar pacotes está descontinuado (a partir do Go 1.17).
  No Go 1.18, `-d` estará sempre habilitada.
* A flag `-u` instrui `go get` a atualizar os módulos que fornecem pacotes
  importados direta ou indiretamente pelos pacotes indicados na linha de comando.
  Cada módulo selecionado por `-u` será atualizado para sua versão mais recente,
  a menos que já esteja exigido em uma versão mais alta (uma pré-versão).
* A flag `-u=patch` (não `-u patch`) também instrui `go get` a atualizar as
  dependências, mas `go get` atualizará cada dependência para a versão de patch
  mais recente (de forma semelhante à consulta de versão `@patch`).
* A flag `-t` instrui `go get` a considerar os módulos necessários para compilar
  os testes dos pacotes indicados na linha de comando. Quando `-t` e `-u` são
  usadas juntas, `go get` também atualizará as dependências de teste.
* A flag `-insecure` não deve mais ser usada. Ela permite que `go get` resolva
  caminhos de importação personalizados e baixe de repositórios e proxies de
  módulos usando esquemas inseguros, como HTTP. A [variável de
  ambiente](#environment-variables) `GOINSECURE` oferece controle mais granular e
  deve ser usada no lugar dela.

A partir do Go 1.16, [`go install`](#go-install) é o comando recomendado para
compilar e instalar programas. Quando usado com um sufixo de versão (como `@latest`
ou `@v1.4.6`), `go install` compila pacotes no modo com reconhecimento de módulo,
ignorando o arquivo `go.mod` do diretório atual ou de qualquer diretório pai, caso
exista.

`go get` tem foco maior em gerenciar as exigências no `go.mod`. A flag `-d` está
descontinuada e, no Go 1.18, estará sempre habilitada.

### `go install` {#go-install}

Uso:

```
go install [build flags] [packages]
```

Exemplos:

```
# Install the latest version of a program,
# ignoring go.mod in the current directory (if any).
$ go install golang.org/x/tools/gopls@latest

# Install a specific version of a program.
$ go install golang.org/x/tools/gopls@v0.6.4

# Install a program at the version selected by the module in the current directory.
$ go install golang.org/x/tools/gopls

# Install all programs in a directory.
$ go install ./cmd/...
```

O comando `go install` compila e instala os pacotes indicados pelos caminhos na
linha de comando. Executáveis (pacotes `main`) são instalados no diretório indicado
pela variável de ambiente `GOBIN`, que assume como padrão `$GOPATH/bin` ou
`$HOME/go/bin` caso a variável de ambiente `GOPATH` não esteja definida.
Executáveis em `$GOROOT` são instalados em `$GOROOT/bin` ou `$GOTOOLDIR`, em vez de
`$GOBIN`. Pacotes que não são executáveis são compilados e armazenados em cache,
mas não são instalados.

A partir do Go 1.16, se os argumentos tiverem sufixos de versão (como `@latest` ou
`@v1.0.0`), `go install` compila pacotes no modo com reconhecimento de módulo,
ignorando o arquivo `go.mod` do diretório atual ou de qualquer diretório pai, se
houver um. Isso é útil para instalar executáveis sem afetar as dependências do
módulo principal.

Para eliminar ambiguidades sobre quais versões de módulo são usadas na compilação,
os argumentos devem satisfazer as seguintes restrições:

* Os argumentos devem ser caminhos de pacote ou padrões de pacote (com curingas
  "`...`"). Eles não podem ser pacotes padrão (como `fmt`), meta-padrões (`std`,
  `cmd`, `all`, `work`, `tool`) nem caminhos de arquivo relativos ou absolutos.
* Todos os argumentos devem ter o mesmo sufixo de versão. Consultas diferentes não
  são permitidas, mesmo que se refiram à mesma versão.
* Todos os argumentos devem se referir a pacotes do mesmo módulo, na mesma versão.
* Argumentos de caminho de pacote devem se referir a pacotes `main`. Argumentos de
  padrão corresponderão apenas a pacotes `main`.
* Nenhum módulo é considerado o [módulo principal](#glos-main-module).
  * Se o módulo que contém os pacotes indicados na linha de comando tiver um
    arquivo `go.mod`, ele não deve conter diretivas (`replace` e `exclude`) que
    fariam com que fosse interpretado de forma diferente caso fosse o módulo
    principal.
  * O módulo não pode exigir uma versão mais alta de si mesmo.
  * Diretórios vendor não são usados em nenhum módulo. (Diretórios vendor não são
    incluídos nos [arquivos zip de módulo](#zip-files), portanto `go install` não
    os baixa.)

Veja [Consultas de versão](#version-queries) para a sintaxe de consulta de versão
suportada. O Go 1.15 e versões anteriores não suportavam o uso de consultas de
versão com `go install`.

Se os argumentos não tiverem sufixos de versão, `go install` pode ser executado no
modo com reconhecimento de módulo ou no modo `GOPATH`, dependendo da variável de
ambiente `GO111MODULE` e da presença de um arquivo `go.mod`. Veja [Comandos com
reconhecimento de módulo](#mod-commands) para detalhes. Se o modo com reconhecimento
de módulo estiver habilitado, `go install` é executado no contexto do módulo
principal, que pode ser diferente do módulo que contém o pacote sendo instalado.

### `go list -m` {#go-list-m}

Uso:

```
go list -m [-u] [-retracted] [-versions] [list flags] [modules]
```

Exemplo:

```
$ go list -m all
$ go list -m -versions example.com/m
$ go list -m -json example.com/m@latest
```

A flag `-m` faz com que `go list` liste módulos em vez de pacotes. Nesse modo, os
argumentos de `go list` podem ser módulos, padrões de módulo (contendo o curinga
`...`), [consultas de versão](#version-queries) ou o padrão especial `all`, que
corresponde a todos os módulos da [build list](#glos-build-list). Se nenhum argumento
for especificado, o [módulo principal](#glos-main-module) é listado.

Ao listar módulos, a flag `-f` ainda especifica um template de formato aplicado a
uma struct do Go, mas agora uma struct `Module`:

```
type Module struct {
    Path       string        // module path
    Version    string        // module version
    Versions   []string      // available module versions
    Replace    *Module       // replaced by this module
    Time       *time.Time    // time version was created
    Update     *Module       // available update (with -u)
    Main       bool          // is this the main module?
    Indirect   bool          // module is only indirectly needed by main module
    Dir        string        // directory holding local copy of files, if any
    GoMod      string        // path to go.mod file describing module, if any
    GoVersion  string        // go version used in module
    Retracted  []string      // retraction information, if any (with -retracted or -u)
    Deprecated string        // deprecation message, if any (with -u)
    Error      *ModuleError  // error loading module
}

type ModuleError struct {
    Err string // the error itself
}
```

A saída padrão é imprimir o caminho do módulo e, em seguida, informações sobre a
versão e a substituição, se houver. Por exemplo, `go list -m all` pode imprimir:

```
example.com/main/module
golang.org/x/net v0.1.0
golang.org/x/text v0.3.0 => /tmp/text
rsc.io/pdf v0.1.1
```

A struct `Module` tem um método `String` que formata esta linha de saída, de modo que
o formato padrão é equivalente a {{raw "`-f '{{.String}}'`"}}.

Observe que, quando um módulo foi substituído, seu campo `Replace` descreve o módulo
substituto, e seu campo `Dir` é definido como o diretório com o código-fonte do
módulo substituto, se presente. (Ou seja, se `Replace` não for nil, então `Dir` é
definido como `Replace.Dir`, sem acesso ao código-fonte substituído.)

A flag `-u` adiciona informações sobre atualizações disponíveis. Quando a versão mais
recente de um determinado módulo é mais nova que a atual, `list -u` define o campo
`Update` do módulo com informações sobre o módulo mais recente. `list -u` também
exibe se a versão atualmente selecionada está [retraída](#glos-retracted-version) e
se o módulo está [descontinuado](#go-mod-file-module-deprecation). O método `String`
do módulo indica uma atualização disponível formatando a versão mais recente entre
colchetes após a versão atual. Por exemplo, `go list -m -u all` pode imprimir:

```
example.com/main/module
golang.org/x/old v1.9.9 (deprecated)
golang.org/x/net v0.1.0 (retracted) [v0.2.0]
golang.org/x/text v0.3.0 [v0.4.0] => /tmp/text
rsc.io/pdf v0.1.1 [v0.1.2]
```

(Para ferramentas, `go list -m -u -json all` pode ser mais conveniente para análise.)

A flag `-versions` faz com que `list` defina o campo `Versions` do módulo com uma
lista de todas as versões conhecidas desse módulo, ordenadas de acordo com o
versionamento semântico, da menor para a maior. A flag também altera o formato de
saída padrão para exibir o caminho do módulo seguido da lista de versões separadas
por espaço. Versões retraídas são omitidas dessa lista, a menos que a flag
`-retracted` também seja especificada.

A flag `-retracted` instrui `list` a mostrar versões retraídas na lista exibida com a
flag `-versions` e a considerar versões retraídas ao resolver [consultas de
versão](#version-queries). Por exemplo, `go list -m -retracted example.com/m@latest`
mostra a maior versão de lançamento ou pré-lançamento do módulo `example.com/m`,
mesmo que essa versão esteja retraída. As diretivas [`retract`](#go-mod-file-retract)
e as [descontinuações](#go-mod-file-module-deprecation) são carregadas do arquivo
`go.mod` nessa versão. A flag `-retracted` foi adicionada no Go 1.16.

A função de template `module` recebe um único argumento de string, que deve ser um
caminho de módulo ou uma consulta, e retorna o módulo especificado como uma struct
`Module`. Se ocorrer um erro, o resultado será uma struct `Module` com o campo
`Error` não nil.

### `go mod download` {#go-mod-download}

Uso:

```
go mod download [-x] [-json] [-reuse=old.json] [modules]
```

Exemplo:

```
$ go mod download
$ go mod download golang.org/x/mod@v0.2.0
```

O comando `go mod download` baixa os módulos informados para o [cache de módulos](#glos-module-cache). Os argumentos podem ser caminhos de módulos ou padrões de módulos que selecionam dependências do [módulo principal](#glos-main-module), ou [consultas de versão](#version-queries) no formato `path@version`. Sem argumentos, `download` se aplica a todas as dependências do módulo principal.

O comando `go` baixa módulos automaticamente, conforme necessário, durante a execução normal. O comando `go mod download` é útil principalmente para pré-preencher o cache de módulos ou para carregar dados que serão servidos por um [proxy de módulos](#glos-module-proxy).

Por padrão, `download` não escreve nada na saída padrão. Ele imprime mensagens de progresso e erros na saída de erro padrão.

A flag `-json` faz com que `download` imprima na saída padrão uma sequência de objetos JSON, descrevendo cada módulo baixado (ou cada falha), correspondendo a esta struct Go:

```
type Module struct {
    Path     string // module path
    Query    string // version query corresponding to this version
    Version  string // module version
    Error    string // error loading module
    Info     string // absolute path to cached .info file
    GoMod    string // absolute path to cached .mod file
    Zip      string // absolute path to cached .zip file
    Dir      string // absolute path to cached source root directory
    Sum      string // checksum for path, version (as in go.sum)
    GoModSum string // checksum for go.mod (as in go.sum)
    Origin   any    // provenance of module
    Reuse    bool   // reuse of old module info is safe
}
```

A flag `-x` faz com que `download` imprima na saída de erro padrão os comandos que ele executa.

A flag -reuse aceita o nome de um arquivo contendo a saída JSON de uma invocação anterior de 'go mod download -json'. O comando go pode usar esse arquivo para determinar que um módulo não foi alterado desde a invocação anterior e evitar baixá-lo novamente. Módulos que não forem baixados novamente serão marcados na nova saída definindo o campo Reuse como true. Normalmente, o cache de módulos fornece esse tipo de reaproveitamento automaticamente; a flag -reuse pode ser útil em sistemas que não preservam o cache de módulos.

### `go mod edit` {#go-mod-edit}

Uso:

```
go mod edit [editing flags] [-fmt|-print|-json] [go.mod]
```

Exemplo:

```
# Add a replace directive.
$ go mod edit -replace example.com/a@v1.0.0=./a

# Remove a replace directive.
$ go mod edit -dropreplace example.com/a@v1.0.0

# Set the go version, add a requirement, and print the file
# instead of writing it to disk.
$ go mod edit -go=1.14 -require=example.com/m@v1.0.0 -print

# Format the go.mod file.
$ go mod edit -fmt

# Format and print a different .mod file.
$ go mod edit -print tools.mod

# Print a JSON representation of the go.mod file.
$ go mod edit -json
```

O comando `go mod edit` fornece uma interface de linha de comando para editar e formatar arquivos `go.mod`, destinada principalmente a ferramentas e scripts. `go mod edit` lê apenas um arquivo `go.mod`; ele não busca informações sobre outros módulos. Por padrão, `go mod edit` lê e escreve o arquivo `go.mod` do módulo principal, mas um arquivo de destino diferente pode ser especificado após as flags de edição.

As flags de edição especificam uma sequência de operações de edição.

* A flag `-module` altera o caminho do módulo (a linha module do arquivo `go.mod`).
* A flag `-go=version` define a versão esperada da linguagem Go.
* As flags `-require=path@version` e `-droprequire=path` adicionam e removem um requisito para o caminho e a versão de módulo informados. Observe que `-require` substitui quaisquer requisitos existentes em `path`. Essas flags são destinadas principalmente a ferramentas que entendem o grafo de módulos. Os usuários devem preferir `go get
  path@version` ou `go get path@none`, que fazem outros ajustes no `go.mod` conforme necessário para satisfazer restrições impostas por outros módulos. Veja [`go get`](#go-get).
* As flags `-exclude=path@version` e `-dropexclude=path@version` adicionam e removem uma exclusão para o caminho e a versão de módulo informados. Observe que `-exclude=path@version` não tem efeito se essa exclusão já existir.
* A flag `-replace=old[@v]=new[@v]` adiciona uma substituição para o par caminho e versão de módulo informado. Se o `@v` em `old@v` for omitido, é adicionada uma substituição sem versão no lado esquerdo, que se aplica a todas as versões do caminho de módulo antigo. Se o `@v` em `new@v` for omitido, o novo caminho deve ser um diretório raiz de módulo local, e não um caminho de módulo. Observe que `-replace` substitui quaisquer substituições redundantes para `old[@v]`, portanto omitir `@v` removerá substituições de versões específicas.
* A flag `-dropreplace=old[@v]` remove uma substituição para o par caminho e versão de módulo informado. Se `@v` for fornecido, uma substituição com a versão informada é removida. Uma substituição existente sem versão no lado esquerdo ainda pode substituir o módulo. Se `@v` for omitido, uma substituição sem versão é removida.
* As flags `-retract=version` e `-dropretract=version` adicionam e removem uma retração para a versão informada, que pode ser uma única versão (como `v1.2.3`) ou um intervalo (como `[v1.1.0,v1.2.0]`). Observe que a flag `-retract` não pode adicionar um comentário de justificativa para a diretiva `retract`. Comentários de justificativa são recomendados e podem ser exibidos por `go list -m -u` e outros comandos.
* As flags `-tool=path` e `-droptool=path` adicionam e removem uma diretiva `tool` para os caminhos informados. Observe que isso não adiciona as dependências necessárias ao grafo de build. Os usuários devem preferir `go get -tool path` para adicionar uma ferramenta, ou `go get -tool path@none` para removê-la.

As flags de edição podem ser repetidas. As alterações são aplicadas na ordem em que são informadas.

`go mod edit` possui flags adicionais que controlam sua saída.

* A flag `-fmt` reformata o arquivo `go.mod` sem fazer outras alterações. Essa reformatação também é implicada por quaisquer outras modificações que usem ou reescrevam o arquivo `go.mod`. A única situação em que esta flag é necessária é quando nenhuma outra flag é especificada, como em `go mod edit -fmt`.
* A flag `-print` imprime o `go.mod` final em seu formato de texto, em vez de gravá-lo de volta no disco.
* A flag `-json` imprime o `go.mod` final em formato JSON, em vez de gravá-lo de volta no disco em formato de texto. A saída JSON corresponde a estes tipos Go:

```
type Module struct {
    Path    string
    Version string
}

type GoMod struct {
    Module  ModPath
    Go      string
    Require []Require
    Exclude []Module
    Replace []Replace
    Retract []Retract
}

type ModPath struct {
    Path       string
    Deprecated string
}

type Require struct {
    Path     string
    Version  string
    Indirect bool
}

type Replace struct {
    Old Module
    New Module
}

type Retract struct {
    Low       string
    High      string
    Rationale string
}

type Tool struct {
    Path      string
}
```

Observe que isso descreve apenas o próprio arquivo `go.mod`, não outros módulos referenciados indiretamente. Para o conjunto completo de módulos disponíveis para um build, use `go list -m -json all`. Veja [`go list -m`](#go-list-m).

Por exemplo, uma ferramenta pode obter o arquivo `go.mod` como uma estrutura de dados, analisando a saída de `go mod edit -json`, e depois pode fazer alterações invocando `go mod edit` com `-require`, `-exclude` e assim por diante.

Ferramentas também podem usar o pacote
[`golang.org/x/mod/modfile`](https://pkg.go.dev/golang.org/x/mod/modfile?tab=doc)
para analisar, editar e formatar arquivos `go.mod`.

### `go mod graph` {#go-mod-graph}

Uso:

```
go mod graph [-go=version]
```

O comando `go mod graph` imprime o [grafo de requisitos de módulos](#glos-module-graph) (com as substituições aplicadas) em formato de texto. Por exemplo:

```
example.com/main example.com/a@v1.1.0
example.com/main example.com/b@v1.2.0
example.com/a@v1.1.0 example.com/b@v1.1.1
example.com/a@v1.1.0 example.com/c@v1.3.0
example.com/b@v1.1.0 example.com/c@v1.1.0
example.com/b@v1.2.0 example.com/c@v1.2.0
```

Cada vértice no grafo de módulos representa uma versão específica de um módulo. Cada aresta no grafo representa um requisito de uma versão mínima de uma dependência.

`go mod graph` imprime as arestas do grafo, uma por linha. Cada linha tem dois campos separados por espaço: uma versão de módulo e uma de suas dependências. Cada versão de módulo é identificada como uma string no formato `path@version`. O módulo principal não tem o sufixo `@version`, pois não possui versão.

A flag `-go` faz com que `go mod graph` relate o grafo de módulos conforme carregado pela versão informada do Go, em vez da versão indicada pela [diretiva `go`](#go-mod-file-go) no arquivo `go.mod`.

Veja [Seleção mínima de versão (MVS)](#minimal-version-selection) para mais informações sobre como as versões são escolhidas. Veja também [`go list -m`](#go-list-m) para imprimir as versões selecionadas e [`go mod why`](#go-mod-why) para entender por que um módulo é necessário.

### `go mod init` {#go-mod-init}

Uso:

```
go mod init [module-path]
```

Exemplo:

```
go mod init
go mod init example.com/m
```

O comando `go mod init` inicializa e grava um novo arquivo `go.mod` no diretório atual, criando efetivamente um novo módulo com raiz no diretório atual. O arquivo `go.mod` não pode existir previamente.

`init` aceita um argumento opcional, o [caminho do módulo](#glos-module-path) para o novo módulo. Veja [Caminhos de módulos](#module-path) para instruções sobre como escolher um caminho de módulo. Se o argumento do caminho do módulo for omitido, `init` tentará inferir o caminho do módulo usando comentários de importação em arquivos `.go` e no diretório atual (se estiver em `GOPATH`).

### `go mod tidy` {#go-mod-tidy}

Uso:

```
go mod tidy [-e] [-v] [-x] [-diff] [-go=version] [-compat=version]
```

`go mod tidy` garante que o arquivo `go.mod` corresponda ao código-fonte do módulo. Ele adiciona quaisquer requisitos de módulo ausentes necessários para compilar os pacotes e as dependências do módulo atual, e remove requisitos de módulos que não fornecem nenhum pacote relevante. Ele também adiciona quaisquer entradas ausentes em `go.sum` e remove entradas desnecessárias.

A flag `-e` (adicionada no Go 1.16) faz com que `go mod tidy` tente prosseguir apesar de erros encontrados ao carregar pacotes.

A flag `-v` faz com que `go mod tidy` imprima na saída de erro padrão informações sobre os módulos removidos.

A flag `-x` faz com que `go mod tidy` imprima os comandos que `tidy` executa.

A flag `-diff` faz com que `go mod tidy` não modifique go.mod ou go.sum, mas imprima as alterações necessárias como um diff unificado. Ele sai com código diferente de zero se o diff não estiver vazio.

`go mod tidy` funciona carregando todos os pacotes do [módulo principal](#glos-main-module), todas as suas ferramentas e todos os pacotes que eles importam, recursivamente. Isso inclui pacotes importados por testes (incluindo testes em outros módulos). `go mod tidy` age como se todas as build tags estivessem habilitadas, então considera arquivos de código-fonte específicos de plataforma e arquivos que exigem build tags personalizadas, mesmo que esses arquivos normalmente não seriam compilados. Há uma exceção: a build tag `ignore` não é habilitada, então um arquivo com a restrição de build `// +build ignore` não será considerado. Observe que `go mod tidy` não considera pacotes do módulo principal em diretórios chamados `testdata` ou com nomes que começam com `.` ou `_`, a menos que esses pacotes sejam explicitamente importados por outros pacotes.

Depois que `go mod tidy` tiver carregado esse conjunto de pacotes, ele garante que cada módulo que fornece um ou mais pacotes tenha uma diretiva `require` no arquivo `go.mod` do módulo principal ou — se o módulo principal estiver na versão `go 1.16` ou anterior — seja requerido por outro módulo requerido. `go mod tidy` adicionará um requisito para a versão mais recente de cada módulo ausente (veja [Consultas de versão](#version-queries) para a definição da versão `latest`). `go mod tidy` removerá diretivas `require` para módulos que não fornecem nenhum pacote no conjunto descrito acima.

`go mod tidy` também pode adicionar ou remover comentários `// indirect` nas diretivas `require`. Um comentário `// indirect` indica um módulo que não fornece um pacote importado por um pacote no módulo principal. (Veja a [diretiva `require`](#go-mod-file-require) para mais detalhes sobre quando dependências e comentários `// indirect` são adicionados.)

Se a flag `-go` for definida, `go mod tidy` atualizará a [diretiva `go`](#go-mod-file-go) para a versão indicada, habilitando ou desabilitando a [poda do grafo de módulos](#graph-pruning) e o [carregamento preguiçoso de módulos](#lazy-loading) (e adicionando ou removendo requisitos indiretos conforme necessário) de acordo com essa versão.

Por padrão, `go mod tidy` verifica se as [versões selecionadas](#glos-selected-version) dos módulos não mudam quando o grafo de módulos é carregado pela versão do Go imediatamente anterior à versão indicada na diretiva `go`. A versão verificada quanto à compatibilidade também pode ser especificada explicitamente pela flag `-compat`.

### `go mod vendor` {#go-mod-vendor}

Uso:

```
go mod vendor [-e] [-v] [-o]
```

O comando `go mod vendor` constrói um diretório chamado `vendor` no diretório raiz do [módulo principal](#glos-main-module), que contém cópias de todos os pacotes necessários para dar suporte a builds e testes dos pacotes do módulo principal. Pacotes que são importados apenas por testes de pacotes fora do módulo principal não são incluídos. Assim como ocorre com [`go mod tidy`](#go-mod-tidy) e outros comandos de módulo, as [restrições de build](#glos-build-constraint) (build constraints), exceto `ignore`, não são consideradas ao construir o diretório `vendor`.

Quando o vendoring está habilitado, o comando `go` carrega pacotes do diretório `vendor` em vez de baixar módulos de suas origens para o [cache de módulos](#glos-module-cache) e usar os pacotes a partir dessas cópias baixadas. Consulte [Vendoring](#vendoring) para mais informações.

`go mod vendor` também cria o arquivo `vendor/modules.txt`, que contém uma lista dos pacotes vendorizados e das versões dos módulos de onde foram copiados. Quando o vendoring está habilitado, esse manifesto é usado como fonte de informações sobre versões de módulos, conforme reportado por [`go list -m`](#go-list-m) e [`go version -m`](#go-version-m). Quando o comando `go` lê `vendor/modules.txt`, ele verifica se as versões dos módulos são consistentes com o `go.mod`. Se o `go.mod` tiver sido alterado desde que `vendor/modules.txt` foi gerado, `go mod vendor` deve ser executado novamente.

Observe que `go mod vendor` remove o diretório `vendor`, caso ele exista, antes de reconstruí-lo. Alterações locais não devem ser feitas em pacotes vendorizados. O comando `go` não verifica se os pacotes no diretório `vendor` foram modificados, mas é possível verificar a integridade do diretório `vendor` executando `go mod vendor` e conferindo se nenhuma alteração foi feita.

A flag `-e` (adicionada no Go 1.16) faz com que `go mod vendor` tente prosseguir apesar de erros encontrados ao carregar pacotes.

A flag `-v` faz com que `go mod vendor` imprima na saída de erro padrão (standard error) os nomes dos módulos e pacotes vendorizados.

A flag `-o` (adicionada no Go 1.18) faz com que `go mod vendor` gere a árvore de vendor no diretório especificado, em vez de `vendor`. O argumento pode ser um caminho absoluto ou um caminho relativo à raiz do módulo.

### `go mod verify` {#go-mod-verify}

Uso:

```
go mod verify
```

`go mod verify` verifica se as dependências do [módulo principal](#glos-main-module) armazenadas no [cache de módulos](#glos-module-cache) não foram modificadas desde que foram baixadas. Para realizar essa verificação, `go mod verify` calcula o hash de cada [arquivo `.zip`](#zip-files) do módulo baixado e do diretório extraído, e então compara esses hashes com um hash registrado quando o módulo foi baixado pela primeira vez. `go mod verify` verifica cada módulo na [build list](#glos-build-list) (que pode ser exibida com [`go list -m all`](#go-list-m)).

Se todos os módulos estiverem inalterados, `go mod verify` imprime "all modules verified". Caso contrário, informa quais módulos foram alterados e encerra com um status diferente de zero.

Observe que todos os comandos cientes de módulos verificam se os hashes no arquivo `go.sum` do módulo principal correspondem aos hashes registrados para os módulos baixados no cache de módulos. Se um hash estiver ausente do `go.sum` (por exemplo, porque o módulo está sendo usado pela primeira vez), o comando `go` verifica seu hash usando o [banco de dados de checksums](#checksum-database) (a menos que o caminho do módulo seja coberto por `GOPRIVATE` ou `GONOSUMDB`). Consulte [Autenticando módulos](#authenticating) para mais detalhes.

Em contraste, `go mod verify` verifica se os arquivos `.zip` dos módulos e seus diretórios extraídos possuem hashes que correspondem aos hashes registrados no cache de módulos quando foram baixados pela primeira vez. Isso é útil para detectar alterações em arquivos do cache de módulos *depois* que um módulo foi baixado e verificado. `go mod verify` não baixa conteúdo de módulos que não estão no cache, e não usa arquivos `go.sum` para verificar o conteúdo dos módulos. No entanto, `go mod verify` pode baixar arquivos `go.mod` para executar a [seleção de versão mínima](#minimal-version-selection). Ele usará `go.sum` para verificar esses arquivos e pode adicionar entradas em `go.sum` para hashes ausentes.

### `go mod why` {#go-mod-why}

Uso:

```
go mod why [-m] [-vendor] packages...
```

`go mod why` mostra um caminho mais curto no grafo de importações, partindo do módulo principal até cada um dos pacotes listados.

A saída é uma sequência de blocos, um para cada pacote ou módulo informado na linha de comando, separados por linhas em branco. Cada bloco começa com uma linha de comentário iniciada por `#`, indicando o pacote ou módulo alvo. As linhas seguintes apresentam um caminho pelo grafo de importações, um pacote por linha. Se o pacote ou módulo não for referenciado pelo módulo principal, o bloco exibirá uma única nota entre parênteses indicando esse fato.

Por exemplo:

```
$ go mod why golang.org/x/text/language golang.org/x/text/encoding
# golang.org/x/text/language
rsc.io/quote
rsc.io/sampler
golang.org/x/text/language

# golang.org/x/text/encoding
(main module does not need package golang.org/x/text/encoding)
```

A flag `-m` faz com que `go mod why` trate seus argumentos como uma lista de módulos. `go mod why` imprimirá um caminho até qualquer pacote em cada um dos módulos. Observe que, mesmo quando `-m` é usado, `go mod why` consulta o grafo de pacotes, e não o grafo de módulos exibido por [`go mod graph`](#go-mod-graph).

A flag `-vendor` faz com que `go mod why` ignore as importações em testes de pacotes fora do módulo principal (como faz [`go mod vendor`](#go-mod-vendor)). Por padrão, `go mod why` considera o grafo de pacotes correspondidos pelo padrão `all`. Essa flag não tem efeito após o Go 1.16 em módulos que declaram `go 1.16` ou superior (usando a [diretiva `go`](#go-mod-file-go) no `go.mod`), pois o significado de `all` passou a corresponder ao conjunto de pacotes correspondidos por `go mod vendor`.

### `go version -m` {#go-version-m}

Uso:

```
go version [-m] [-v] [file ...]
```

Exemplo:

```
# Print Go version used to build go.
$ go version

# Print Go version used to build a specific executable.
$ go version ~/go/bin/gopls

# Print Go version and module versions used to build a specific executable.
$ go version -m ~/go/bin/gopls

# Print Go version and module versions used to build executables in a directory.
$ go version -m ~/go/bin/
```

`go version` informa a versão do Go usada para compilar cada arquivo executável informado na linha de comando.

Se nenhum arquivo for informado na linha de comando, `go version` imprime suas próprias informações de versão.

Se um diretório for informado, `go version` percorre esse diretório recursivamente, procurando binários Go reconhecidos e informando suas versões. Por padrão, `go version` não informa arquivos não reconhecidos encontrados durante a varredura do diretório. A flag `-v` faz com que ele informe também os arquivos não reconhecidos.

A flag `-m` faz com que `go version` imprima as informações de versão de módulo incorporadas em cada executável, quando disponíveis. Para cada executável, `go version -m` imprime uma tabela com colunas separadas por tabulação, como a exibida abaixo.

```
$ go version -m ~/go/bin/goimports
/home/jrgopher/go/bin/goimports: go1.14.3
        path    golang.org/x/tools/cmd/goimports
        mod     golang.org/x/tools      v0.0.0-20200518203908-8018eb2c26ba      h1:0Lcy64USfQQL6GAJma8BdHCgeofcchQj+Z7j0SXYAzU=
        dep     golang.org/x/mod        v0.2.0          h1:KU7oHjnv3XNWfa5COkzUifxZmxp1TyI7ImMXqFxLwvQ=
        dep     golang.org/x/xerrors    v0.0.0-20191204190536-9bdfabe68543      h1:E7g+9GITq07hpfrRu66IVDexMakfv52eLZ2CXBWiKr4=
```

O formato da tabela pode mudar no futuro. As mesmas informações podem ser obtidas a partir de [`runtime/debug.ReadBuildInfo`](https://pkg.go.dev/runtime/debug?tab=doc#ReadBuildInfo).

O significado de cada linha da tabela é determinado pela palavra na primeira coluna.

* **`path`**: o caminho do pacote `main` usado para compilar o executável.
* **`mod`**: o módulo que contém o pacote `main`. As colunas são, respectivamente, o caminho do módulo, a versão e a soma (sum). O [módulo principal](#glos-main-module) tem a versão `(devel)` e nenhuma soma.
* **`dep`**: um módulo que forneceu um ou mais pacotes vinculados ao executável. Mesmo formato de `mod`.
* **`=>`**: uma [substituição (replacement)](#go-mod-file-replace) para o módulo na linha anterior. Se a substituição for um diretório local, apenas o caminho do diretório é listado (sem versão ou soma). Se a substituição for uma versão de módulo, o caminho, a versão e a soma são listados, como em `mod` e `dep`. Um módulo substituído não possui soma.

### `go clean -modcache` {#go-clean-modcache}

Uso:

```
go clean [-modcache]
```

A flag `-modcache` faz com que o [`go clean`](/cmd/go/#hdr-Remove_object_files_and_cached_files) remova todo o [cache de módulos](#glos-module-cache), incluindo o código-fonte descompactado das dependências versionadas.

Esta costuma ser a melhor maneira de remover o cache de módulos. Por padrão, a maioria dos arquivos e diretórios no cache de módulos é somente leitura, para evitar que testes e editores alterem arquivos sem intenção depois de [autenticados](#authenticating). Infelizmente, isso faz com que comandos como `rm -r` falhem, já que os arquivos não podem ser removidos sem antes tornar seus diretórios pais graváveis.

A flag `-modcacherw` (aceita por [`go build`](/cmd/go/#hdr-Compile_packages_and_dependencies) e outros comandos cientes de módulos) faz com que novos diretórios no cache de módulos sejam graváveis. Para passar `-modcacherw` para todos os comandos cientes de módulos, adicione-a à variável `GOFLAGS`. `GOFLAGS` pode ser definida no ambiente ou com [`go env -w`](/cmd/go/#hdr-Print_Go_environment_information). Por exemplo, o comando abaixo a define de forma permanente:

```
go env -w GOFLAGS=-modcacherw
```

`-modcacherw` deve ser usada com cautela; desenvolvedores devem tomar cuidado para não fazer alterações em arquivos do cache de módulos. [`go mod verify`](#go-mod-verify) pode ser usado para verificar se os arquivos do cache correspondem aos hashes no arquivo `go.sum` do módulo principal.

### Consultas de versão {#version-queries}

Vários comandos permitem especificar a versão de um módulo usando uma *consulta de versão* (*version query*), que aparece após um caractere `@` seguindo o caminho de um módulo ou pacote na linha de comando.

Exemplos:

```
go get example.com/m@latest
go mod download example.com/m@master
go list -m -json example.com/m@e3702bed2
```

Uma consulta de versão pode ser uma das seguintes:

* Uma versão semântica totalmente especificada, como `v1.2.3`, que seleciona uma versão específica. Consulte [Versões](#versions) para a sintaxe.
* Um prefixo de versão semântica, como `v1` ou `v1.2`, que seleciona a versão mais alta disponível com esse prefixo.
* Uma comparação de versão semântica, como {{raw "`<v1.2.3` ou `>=v1.5.6`"}}, que seleciona a versão disponível mais próxima do alvo da comparação (a menor versão para `>` e `>=`, e a maior versão para {{raw "`<` e `<=`"}}).
* Um identificador de revisão do repositório de código subjacente, como um prefixo de hash de commit, uma tag de revisão ou o nome de um branch. Se a revisão estiver marcada com uma versão semântica, essa consulta seleciona essa versão. Caso contrário, a consulta seleciona um [pseudo-versão](#glos-pseudo-version) para o commit subjacente. Observe que branches e tags cujos nomes coincidem com outras consultas de versão não podem ser selecionados dessa forma. Por exemplo, a consulta `v2` seleciona a versão mais recente começando com `v2`, e não o branch chamado `v2`.
* A string `latest`, que seleciona a versão de release mais alta disponível. Se não houver versões de release, `latest` seleciona a versão de pré-release mais alta. Se não houver versões marcadas, `latest` seleciona uma pseudo-versão para o commit na ponta do branch padrão do repositório.
* A string `upgrade`, que é como `latest`, exceto que, se o módulo estiver atualmente requerido em uma versão superior àquela que `latest` selecionaria (por exemplo, uma pré-release), `upgrade` selecionará a versão atual.
* A string `patch`, que seleciona a versão disponível mais recente com os mesmos números de versão maior e menor da versão atualmente requerida. Se nenhuma versão estiver atualmente requerida, `patch` é equivalente a `latest`. Desde o Go 1.16, o [`go get`](#go-get) exige uma versão atual ao usar `patch` (mas a flag `-u=patch` não tem essa exigência).

Exceto para consultas de versões ou revisões específicas nomeadas, todas as consultas consideram as versões disponíveis informadas por `go list -m -versions` (consulte [`go list -m`](#go-list-m)). Essa lista contém apenas versões marcadas, e não pseudo-versões. Versões de módulo proibidas pelas diretivas [`exclude`](#go-mod-file-exclude) no arquivo [`go.mod`](#glos-go-mod-file) do módulo principal não são consideradas. Versões cobertas pelas diretivas [`retract`](#go-mod-file-retract) no arquivo `go.mod` a partir da versão `latest` do mesmo módulo também são ignoradas, exceto quando a flag `-retracted` é usada com [`go list -m`](#go-list-m) e exceto ao carregar diretivas `retract`.

[Versões de release](#glos-release-version) são preferidas em relação a versões de pré-release. Por exemplo, se as versões `v1.2.2` e `v1.2.3-pre` estiverem disponíveis, a consulta `latest` selecionará `v1.2.2`, mesmo que `v1.2.3-pre` seja mais alta. A consulta {{raw "`<v1.2.4`"}} também selecionaria `v1.2.2`, mesmo que `v1.2.3-pre` esteja mais próxima de `v1.2.4`. Se nenhuma versão de release ou pré-release estiver disponível, as consultas `latest`, `upgrade` e `patch` selecionarão uma pseudo-versão para o commit na ponta do branch padrão do repositório. As demais consultas informarão um erro.

### Comandos de módulo fora de um módulo {#commands-outside}

Os comandos do Go cientes de módulos normalmente são executados no contexto de um [módulo principal](#glos-main-module) definido por um arquivo `go.mod` no diretório de trabalho ou em um diretório pai. Alguns comandos podem ser executados no modo ciente de módulos sem um arquivo `go.mod`, mas a maioria funciona de forma diferente ou informa um erro quando nenhum arquivo `go.mod` está presente.

Consulte [Comandos cientes de módulos](#mod-commands) para informações sobre como habilitar e desabilitar o modo ciente de módulos.

<table class="ModTable">
  <thead>
    <tr>
      <th>Comando</th>
      <th>Comportamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <code>go build</code><br>
        <code>go doc</code><br>
        <code>go fix</code><br>
        <code>go fmt</code><br>
        <code>go generate</code><br>
        <code>go install</code><br>
        <code>go list</code><br>
        <code>go run</code><br>
        <code>go test</code><br>
        <code>go vet</code>
      </td>
      <td>
        Apenas pacotes da biblioteca padrão e pacotes especificados como arquivos
        <code>.go</code> na linha de comando podem ser carregados, importados e
        compilados. Pacotes de outros módulos não podem ser compilados, pois não há
        um lugar onde registrar os requisitos do módulo e garantir builds determinísticos.
      </td>
    </tr>
    <tr>
      <td><code>go get</code></td>
      <td>
        Pacotes e executáveis podem ser compilados e instalados normalmente. Observe
        que não há módulo principal quando <code>go get</code> é executado sem um
        arquivo <code>go.mod</code>, portanto as diretivas <code>replace</code> e
        <code>exclude</code> não são aplicadas.
      </td>
    </tr>
    <tr>
      <td><code>go list -m</code></td>
      <td>
        <a href="#version-queries">Consultas de versão</a> explícitas são exigidas
        para a maioria dos argumentos, exceto quando a flag <code>-versions</code> é usada.
      </td>
    </tr>
    <tr>
      <td><code>go mod download</code></td>
      <td>
        <a href="#version-queries">Consultas de versão</a> explícitas são exigidas
        para a maioria dos argumentos.
      </td>
    </tr>
    <tr>
      <td><code>go mod edit</code></td>
      <td>Um argumento de arquivo explícito é obrigatório.</td>
    </tr>
    <tr>
      <td>
        <code>go mod graph</code><br>
        <code>go mod tidy</code><br>
        <code>go mod vendor</code><br>
        <code>go mod verify</code><br>
        <code>go mod why</code>
      </td>
      <td>
        Esses comandos exigem um arquivo <code>go.mod</code> e informarão um erro
        se ele não estiver presente.
      </td>
    </tr>
  </tbody>
</table>

### `go work init` {#go-work-init}

Uso:

```
go work init [moddirs]
```

O `init` inicializa e grava um novo arquivo go.work no
diretório atual, criando efetivamente um novo workspace nesse diretório.

O `go work init` aceita opcionalmente caminhos para os módulos do workspace
como argumentos. Se o argumento for omitido, será criado um workspace vazio,
sem módulos.

Cada caminho passado como argumento é adicionado a uma diretiva use no arquivo go.work. A
versão atual do Go também será listada no arquivo go.work.

### `go work edit` {#go-work-edit}

Uso:

```
go work edit [editing flags] [go.work]
```

O comando `go work edit` oferece uma interface de linha de comando para editar `go.work`,
usada principalmente por ferramentas ou scripts. Ele apenas lê `go.work`;
não consulta informações sobre os módulos envolvidos.
Se nenhum arquivo for especificado, o Edit procura um arquivo `go.work` no
diretório atual e em seus diretórios pais

As flags de edição especificam uma sequência de operações de edição.
* A flag `-fmt` reformata o arquivo go.work sem fazer outras alterações.
  Essa reformatação também está implícita em qualquer outra modificação que use ou
  reescreva o arquivo `go.work`. A única situação em que essa flag é necessária é quando nenhuma
  outra flag é especificada, como em 'go work edit `-fmt`'.
* As flags `-use=path` e `-dropuse=path` adicionam e removem uma diretiva use do
  conjunto de diretórios de módulos do arquivo `go.work`.
* A flag `-replace=old[@v]=new[@v]` adiciona uma substituição para o par
  caminho de módulo e versão informado. Se o `@v` em `old@v` for omitido, é adicionada uma
  substituição sem versão no lado esquerdo, que se aplica
  a todas as versões do caminho de módulo antigo. Se o `@v` em `new@v` for omitido,
  o novo caminho deve ser um diretório raiz de módulo local, não um
  caminho de módulo. Observe que `-replace` sobrescreve quaisquer substituições redundantes para `old[@v]`,
  então omitir `@v` removerá substituições existentes para versões específicas.
* A flag `-dropreplace=old[@v]` remove uma substituição do par
  caminho de módulo e versão informado. Se o `@v` for omitido, é removida uma substituição sem
  versão no lado esquerdo.
* A flag `-go=version` define a versão esperada da linguagem Go.

As flags de edição podem ser repetidas. As alterações são aplicadas na ordem em que são informadas.

O `go work edit` possui flags adicionais que controlam sua saída

* A flag -print imprime o go.work final em seu formato de texto, em vez de
  gravá-lo de volta no go.mod.
* A flag -json imprime o arquivo go.work final em formato JSON, em vez de
  gravá-lo de volta no go.mod. A saída JSON corresponde a estes tipos do Go:

```
type Module struct {
    Path    string
    Version string
}

type GoWork struct {
    Go        string
    Directory []Directory
    Replace   []Replace
}

type Use struct {
    Path       string
    ModulePath string
}

type Replace struct {
    Old Module
    New Module
}
```

### `go work use` {#go-work-use}

Uso:

```
go work use [-r] [moddirs]
```

O comando `go work use` oferece uma interface de linha de comando para adicionar
diretórios, opcionalmente de forma recursiva, a um arquivo `go.work`.

Uma [diretiva `use`](#go-work-file-use) será adicionada ao arquivo `go.work` para cada diretório
listado na linha de comando, caso ele exista no disco, ou removida do arquivo `go.work` caso não exista no disco.

A flag `-r` procura módulos recursivamente nos diretórios informados como argumentos, e o comando use funciona como se cada um
dos diretórios tivesse sido especificado como argumento.

### `go work sync` {#go-work-sync}

Uso:

```
go work sync
```

O comando `go work sync` sincroniza a build list do workspace de volta para
os módulos do workspace.

A build list do workspace é o conjunto de versões de todos os
módulos de dependência (transitivos) usados para fazer builds no workspace. O comando `go
work sync` gera essa build list usando o algoritmo de [Minimal Version Selection
(MVS)](#glos-minimal-version-selection), e em seguida sincroniza essas versões de volta para cada um dos módulos
especificados no workspace (com diretivas `use`).

Depois que a build list do workspace é calculada, o arquivo `go.mod` de cada
módulo do workspace é reescrito, com as dependências relevantes para esse
módulo atualizadas para corresponder à build list do workspace.
Observe que a [Minimal Version Selection](#glos-minimal-version-selection) garante que a versão de cada
módulo na build list é sempre igual ou superior à que consta em cada módulo do workspace.

## Proxies de módulos {#module-proxy}

### Protocolo `GOPROXY` {#goproxy-protocol}

Um <dfn>proxy de módulos</dfn> é um servidor HTTP que pode responder a requisições `GET`
para os caminhos especificados abaixo. As requisições não têm parâmetros de consulta, e nenhum
cabeçalho específico é exigido, então até mesmo um site servido a partir de um sistema de arquivos fixo
(incluindo uma URL `file://`) pode ser um proxy de módulos.

Respostas HTTP bem-sucedidas devem ter o código de status 200 (OK). Redirecionamentos (3xx)
são seguidos. Respostas com códigos de status 4xx e 5xx são tratadas como erros.
Os códigos de erro 404 (Not Found) e 410 (Gone) indicam que o
módulo ou a versão solicitada não está disponível no proxy, mas pode ser encontrado
em outro lugar. Respostas de erro devem ter o tipo de conteúdo `text/plain` com
`charset` igual a `utf-8` ou `us-ascii`.

O comando `go` pode ser configurado para contatar proxies ou servidores de controle de versão
usando a variável de ambiente `GOPROXY`, que aceita uma lista de URLs de proxies.
A lista pode incluir as palavras-chave `direct` ou `off` (veja [Variáveis de
ambiente](#environment-variables) para detalhes). Os elementos da lista podem ser separados
por vírgulas (`,`) ou barras verticais (`|`), que determinam o comportamento de fallback em caso de erro. Quando uma
URL é seguida por vírgula, o comando `go` recorre às fontes seguintes somente
após uma resposta 404 (Not Found) ou 410 (Gone). Quando uma URL é seguida por
barra vertical, o comando `go` recorre às fontes seguintes após qualquer erro, incluindo
erros não HTTP, como timeouts. Esse comportamento de tratamento de erros permite que um proxy atue como
um guardião para módulos desconhecidos. Por exemplo, um proxy poderia responder com
erro 403 (Forbidden) para módulos que não estão em uma lista aprovada (veja [Proxy privado
servindo módulos privados](#private-module-proxy-private)).

A tabela abaixo especifica as consultas às quais um proxy de módulos deve responder. Para cada
caminho, `$base` é a parte de caminho de uma URL de proxy, `$module` é um caminho de módulo, e
`$version` é uma versão. Por exemplo, se a URL do proxy for
`https://example.com/mod`, e o cliente estiver solicitando o arquivo `go.mod` para
o módulo `golang.org/x/text` na versão `v0.3.2`, o cliente enviaria uma
requisição `GET` para `https://example.com/mod/golang.org/x/text/@v/v0.3.2.mod`.

Para evitar ambiguidades ao servir a partir de sistemas de arquivos que não diferenciam maiúsculas de minúsculas,
os elementos `$module` e `$version` são codificados substituindo cada
letra maiúscula por um ponto de exclamação seguido da letra minúscula correspondente. Isso permite que os módulos `example.com/M` e `example.com/m`
sejam ambos armazenados em disco, já que o primeiro é codificado como `example.com/!m`.

<table class="ModTable">
  <thead>
    <tr>
      <th>Caminho</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>$base/$module/@v/list</code></td>
      <td>
        Retorna uma lista das versões conhecidas do módulo informado em texto simples, uma
        por linha. Essa lista não deve incluir pseudo-versões.
      </td>
    </tr>
    <tr>
      <td><code>$base/$module/@v/$version.info</code></td>
      <td>
        <p>
          Retorna metadados em formato JSON sobre uma versão específica de um módulo.
          A resposta deve ser um objeto JSON que corresponda à estrutura de dados do Go
          abaixo:
        </p>
        <pre>
type Info struct {
    Version string    // version string
    Time    time.Time // commit time
}
</pre>
        <p>
          O campo <code>Version</code> é obrigatório e deve conter uma
          <a href="#glos-canonical-version">versão canônica</a> válida (veja
          <a href="#versions">Versions</a>). O <code>$version</code> no
          caminho da requisição não precisa ser a mesma versão, nem sequer uma versão válida;
          esse endpoint pode ser usado para encontrar versões a partir de nomes de branches ou
          identificadores de revisão. No entanto, se <code>$version</code> for uma
          versão canônica com versão major compatível com
          <code>$module</code>, o campo <code>Version</code> em uma resposta bem-sucedida
          deve ser o mesmo.
        </p>
        <p>
          O campo <code>Time</code> é opcional. Se presente, deve ser uma
          string no formato RFC 3339. Ele indica o momento em que a versão
          foi criada.
        </p>
        <p>
          Campos adicionais podem ser incluídos no futuro, então outros nomes estão reservados.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>$base/$module/@v/$version.mod</code></td>
      <td>
        Retorna o arquivo <code>go.mod</code> de uma versão específica de um
        módulo. Se o módulo não tiver um arquivo <code>go.mod</code> na
        versão solicitada, deve ser retornado um arquivo contendo apenas uma instrução <code>module</code>
        com o caminho de módulo solicitado. Caso contrário,
        deve ser retornado o arquivo <code>go.mod</code> original, sem modificações.
      </td>
    </tr>
    <tr>
      <td><code>$base/$module/@v/$version.zip</code></td>
      <td>
        Retorna um arquivo zip contendo o conteúdo de uma versão específica de
        um módulo. Veja <a href="#zip-files">Arquivos zip de módulos</a> para detalhes
        sobre como esse arquivo zip deve ser formatado.
      </td>
    </tr>
    <tr>
      <td><code>$base/$module/@latest</code></td>
      <td>
        Retorna metadados em formato JSON sobre a versão mais recente conhecida de um
        módulo, no mesmo formato de
        <code>$base/$module/@v/$version.info</code>. A versão mais recente deve ser
        a versão do módulo que o comando <code>go</code> deve usar
        se <code>$base/$module/@v/list</code> estiver vazia ou nenhuma versão listada
        for adequada. Esse endpoint é opcional, e os proxies de módulos não são obrigados
        a implementá-lo.
      </td>
    </tr>
  </tbody>
</table>

Ao resolver a versão mais recente de um módulo, o comando `go` fará uma requisição para
`$base/$module/@v/list` e, caso nenhuma versão adequada seja encontrada,
para `$base/$module/@latest`. O comando `go` prefere, nesta ordem: a maior versão de release
em termos semânticos, a maior versão de pré-release em termos semânticos e a
pseudo-versão mais recente em termos cronológicos. No Go 1.12 e versões anteriores, o comando
`go` considerava as pseudo-versões em `$base/$module/@v/list` como versões de pré-release,
mas isso não é mais verdade desde o Go 1.13.

Um proxy de módulos deve sempre servir o mesmo conteúdo para respostas bem-sucedidas
às consultas `$base/$module/$version.mod` e `$base/$module/$version.zip`. Esse conteúdo é [autenticado criptograficamente](#authenticating)
usando [arquivos `go.sum`](#go-sum-files) e, por padrão, o
[banco de dados de checksums](#checksum-database).

O comando `go` armazena em cache a maior parte do conteúdo que baixa de proxies de módulos no
seu cache de módulos, em `$GOPATH/pkg/mod/cache/download`. Mesmo ao baixar diretamente de
sistemas de controle de versão, o comando `go` sintetiza arquivos `info`, `mod` e `zip`
explícitos e os armazena nesse diretório, da mesma forma como se os tivesse baixado diretamente de
um proxy. A estrutura do cache é a mesma do espaço de URLs do proxy, então servir
`$GOPATH/pkg/mod/cache/download` em (ou copiá-lo para)
`https://example.com/proxy` permitiria que os usuários acessassem as versões de módulos em cache
definindo `GOPROXY` como `https://example.com/proxy`.

### Comunicação com proxies {#communicating-with-proxies}

O comando `go` pode baixar código-fonte e metadados de módulos de um [proxy de
módulos](#glos-module-proxy). A variável de ambiente [`GOPROXY`](#environment-variables) pode ser usada para configurar quais proxies o
comando `go` pode acessar e se ele pode se comunicar diretamente com
[sistemas de controle de versão](#vcs). Os dados de módulos baixados são salvos no [cache de
módulos](#glos-module-cache). O comando `go` só acessará um proxy quando
precisar de informações que ainda não estão no cache.

A seção [protocolo `GOPROXY`](#goproxy-protocol) descreve as requisições que
podem ser enviadas a um servidor `GOPROXY`. No entanto, também é útil entender
quando o comando `go` faz essas requisições. Por exemplo, `go build` segue
o procedimento abaixo:

* Calcula a [build list](#glos-build-list) lendo os [arquivos
  `go.mod`](#glos-go-mod-file) e executando a [minimal version selection
  (MVS)](#glos-minimal-version-selection).
* Lê os pacotes informados na linha de comando e os pacotes que eles importam.
* Se um pacote não for fornecido por nenhum módulo na build list, encontra um
  módulo que o forneça. Adiciona um requisito de módulo para a sua versão mais recente em `go.mod`,
  e recomeça o processo.
* Compila os pacotes depois que tudo foi carregado.

Quando o comando `go` calcula a build list, ele carrega o arquivo `go.mod` de
cada módulo no [grafo de módulos](#glos-module-graph). Se um arquivo `go.mod` não estiver
no cache, o comando `go` o baixará do proxy usando uma requisição `$module/@v/$version.mod`
(onde `$module` é o caminho do módulo e
`$version` é a versão). Essas requisições podem ser testadas com uma ferramenta como o
`curl`. Por exemplo, o comando abaixo baixa o arquivo `go.mod` de
`golang.org/x/mod` na versão `v0.2.0`:

```
$ curl https://proxy.golang.org/golang.org/x/mod/@v/v0.2.0.mod
module golang.org/x/mod

go 1.12

require (
    golang.org/x/crypto v0.0.0-20191011191535-87dc89f01550
    golang.org/x/tools v0.0.0-20191119224855-298f0cb1881e
    golang.org/x/xerrors v0.0.0-20191011141410-1b5146add898
)
```

Para carregar um pacote, o comando `go` precisa do código-fonte do
módulo que o fornece. O código-fonte dos módulos é distribuído em arquivos `.zip`, que são
extraídos para o cache de módulos. Se um `.zip` do módulo não estiver no cache,
o comando `go` o baixará usando uma requisição `$module/@v/$version.zip`.

```
$ curl -O https://proxy.golang.org/golang.org/x/mod/@v/v0.2.0.zip
$ unzip -l v0.2.0.zip | head
Archive:  v0.2.0.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     1479  00-00-1980 00:00   golang.org/x/mod@v0.2.0/LICENSE
     1303  00-00-1980 00:00   golang.org/x/mod@v0.2.0/PATENTS
      559  00-00-1980 00:00   golang.org/x/mod@v0.2.0/README
       21  00-00-1980 00:00   golang.org/x/mod@v0.2.0/codereview.cfg
      214  00-00-1980 00:00   golang.org/x/mod@v0.2.0/go.mod
     1476  00-00-1980 00:00   golang.org/x/mod@v0.2.0/go.sum
     5224  00-00-1980 00:00   golang.org/x/mod@v0.2.0/gosumcheck/main.go
```

Observe que as requisições `.mod` e `.zip` são separadas, mesmo que os arquivos `go.mod`
geralmente estejam contidos dentro dos arquivos `.zip`. O comando `go` pode precisar baixar
arquivos `go.mod` de muitos módulos diferentes, e os arquivos `.mod` são bem menores
que os arquivos `.zip`. Além disso, se um projeto Go não tiver um arquivo `go.mod`, o
proxy servirá um arquivo `go.mod` sintético que contém apenas uma [diretiva
`module`](#go-mod-file-module). Arquivos `go.mod` sintéticos são gerados pelo
comando `go` ao baixar de um [sistema de controle de versão](#vcs).

Se o comando `go` precisar carregar um pacote que não é fornecido por nenhum módulo na
build list, ele tentará encontrar um novo módulo que o forneça. A seção
[Resolvendo um pacote para um módulo](#resolve-pkg-mod) descreve esse processo. Em
resumo, o comando `go` solicita informações sobre a versão mais recente de cada
caminho de módulo que possa conter o pacote. Por exemplo, para o
pacote `golang.org/x/net/html`, o comando `go` tentaria encontrar as versões mais recentes dos módulos
`golang.org/x/net/html`, `golang.org/x/net`,
`golang.org/x/` e `golang.org`. Somente `golang.org/x/net` existe de fato e
fornece esse pacote, então o comando `go` usa a versão mais recente desse
módulo. Se mais de um módulo fornecer o pacote, o comando `go` usará o
módulo com o caminho mais longo.

Quando o comando `go` solicita a versão mais recente de um módulo, ele primeiro envia uma
requisição para `$module/@v/list`. Se a lista estiver vazia ou nenhuma das
versões retornadas puder ser usada, ele envia uma requisição para `$module/@latest`. Depois que uma versão
é escolhida, o comando `go` envia uma requisição `$module/@v/$version.info` para
obter os metadados. Em seguida, pode enviar requisições `$module/@v/$version.mod` e
`$module/@v/$version.zip` para carregar o arquivo `go.mod` e o código-fonte.

```
$ curl https://proxy.golang.org/golang.org/x/mod/@v/list
v0.1.0
v0.2.0

$ curl https://proxy.golang.org/golang.org/x/mod/@v/v0.2.0.info
{"Version":"v0.2.0","Time":"2020-01-02T17:33:45Z"}
```

Depois de baixar um arquivo `.mod` ou `.zip`, o comando `go` calcula um hash criptográfico e verifica se ele corresponde a um hash no
arquivo `go.sum` do módulo principal. Se o hash não estiver presente em `go.sum`, por padrão, o comando
`go` o obtém do [banco de dados de checksums](#checksum-database). Se o
hash calculado não corresponder, o comando `go` reporta um erro de segurança e não
instala o arquivo no cache de módulos. As [variáveis de ambiente](#environment-variables)
`GOPRIVATE` e `GONOSUMDB` podem ser usadas para desativar as requisições
ao banco de dados de checksums para módulos específicos. A variável de ambiente `GOSUMDB`
também pode ser definida como `off` para desativar completamente as requisições ao banco de dados de checksums. Veja [Autenticando módulos](#authenticating) para mais
informações. Observe que as listas de versões e os metadados de versão retornados para
requisições `.info` não são autenticados e podem mudar com o tempo.

### Servindo módulos diretamente de um proxy {#serving-from-proxy}

A maioria dos módulos é desenvolvida e disponibilizada a partir de um repositório de controle de versão. No
[modo direto](#glos-direct-mode), o comando `go` baixa esse tipo de módulo com
uma ferramenta de controle de versão (veja [Sistemas de controle de versão](#vcs)). Também é possível
disponibilizar um módulo diretamente de um proxy de módulos. Isso é útil para organizações
que querem disponibilizar módulos sem expor seus servidores de controle de versão
e para organizações que usam ferramentas de controle de versão que o comando `go` não
suporta.

Quando o comando `go` baixa um módulo no modo direto, ele primeiro procura a URL
do servidor do módulo com uma requisição HTTP GET baseada no caminho do módulo. Ele
procura por uma tag `<meta>` com o nome `go-import` na resposta HTML. O conteúdo
da tag deve conter o [caminho da raiz do
repositório](#glos-repository-root-path), o sistema de controle de versão e a URL,
separados por espaços. Veja [Encontrando um repositório para um caminho de módulo](#vcs-find) para
mais detalhes.

Se o sistema de controle de versão for `mod`, o comando `go` baixa o módulo
da URL informada usando o [protocolo `GOPROXY`](#goproxy-protocol).

Por exemplo, suponha que o comando `go` esteja tentando baixar o módulo
`example.com/gopher` na versão `v1.0.0`. Ele envia uma requisição para
`https://example.com/gopher?go-get=1`. O servidor responde com um documento HTML
contendo a tag:

```
<meta name="go-import" content="example.com/gopher mod https://modproxy.example.com">
```

Com base nessa resposta, o comando `go` baixa o módulo enviando
requisições para `https://modproxy.example.com/example.com/gopher/@v/v1.0.0.info`,
`v1.0.0.mod` e `v1.0.0.zip`.

Observe que módulos disponibilizados diretamente de um proxy não podem ser baixados com
`go get` no modo GOPATH.

## Sistemas de controle de versão {#vcs}

O comando `go` pode baixar código-fonte e metadados de módulos diretamente de um
repositório de controle de versão. Baixar um módulo de um
[proxy](#communicating-with-proxies) normalmente é mais rápido, mas conectar-se
diretamente a um repositório é necessário se um proxy não estiver disponível ou se o
repositório de um módulo não for acessível a um proxy (o que é frequentemente verdade para
repositórios privados). Git, Subversion, Mercurial, Bazaar e Fossil são suportados. Uma
ferramenta de controle de versão deve estar instalada em um diretório presente em `PATH` para que o
comando `go` possa usá-la.

Para baixar módulos específicos de repositórios de código-fonte em vez de um proxy, defina
as variáveis de ambiente `GOPRIVATE` ou `GONOPROXY`. Para configurar o comando `go`
para baixar todos os módulos diretamente de repositórios de código-fonte, defina `GOPROXY`
como `direct`. Veja [Variáveis de ambiente](#environment-variables) para mais
informações.

### Encontrando um repositório para um caminho de módulo {#vcs-find}

Quando o comando `go` baixa um módulo no modo `direct`, ele começa localizando
o repositório que contém o módulo.

Se o caminho do módulo tiver um qualificador de VCS (um dos seguintes: `.bzr`, `.fossil`, `.git`, `.hg`,
`.svn`) no final de um componente do caminho, o comando `go` usará tudo até
esse qualificador como a URL do repositório. Por exemplo, para o módulo
`example.com/foo.git/bar`, o comando `go` baixa o repositório em
`example.com/foo` usando git, esperando encontrar o módulo no subdiretório
`bar`. O comando `go` tentará adivinhar o protocolo a ser usado com base nos
protocolos suportados pela ferramenta de controle de versão.

Se o caminho do módulo não tiver um qualificador, o comando `go` envia uma requisição HTTP
`GET` para uma URL derivada do caminho do módulo, com a string de consulta `?go-get=1`. Por exemplo, para
o módulo `golang.org/x/mod`, o comando `go` pode enviar as seguintes requisições:

```
https://golang.org/x/mod?go-get=1 (preferred)
http://golang.org/x/mod?go-get=1  (fallback, only with GOINSECURE)
```

O comando `go` segue redirecionamentos, mas ignora os códigos de status da resposta de outra forma,
então o servidor pode responder com 404 ou qualquer outro status de erro. A
variável de ambiente `GOINSECURE` pode ser definida para permitir a alternativa e redirecionamentos
para HTTP não criptografado em módulos específicos.

O servidor deve responder com um documento HTML contendo uma tag `<meta>` na
seção `<head>` do documento. A tag `<meta>` deve aparecer no início do documento para
evitar confundir o analisador restrito do comando `go`. Em particular, ela deve
aparecer antes de qualquer JavaScript ou CSS puro. A tag `<meta>` deve ter a forma:

```
<meta name="go-import" content="root-path vcs repo-url [subdirectory]">
```

`root-path` é o caminho da raiz do repositório, a parte do caminho do módulo que
corresponde ao diretório raiz do repositório ou ao `subdirectory`,
se presente e se estiver usando Go 1.25 ou posterior (veja a seção sobre `subdirectory` abaixo).
Ele deve ser um prefixo ou uma correspondência exata do caminho de módulo solicitado. Se não for uma
correspondência exata, outra requisição é feita para o prefixo, a fim de verificar se as tags `<meta>`
correspondem.

`vcs` é o sistema de controle de versão. Deve ser uma das ferramentas listadas na
tabela abaixo ou a palavra-chave `mod`, que instrui o comando `go` a baixar
o módulo da URL informada usando o [protocolo
`GOPROXY`](#goproxy-protocol). Veja [Servindo módulos diretamente de um
proxy](#serving-from-proxy) para detalhes.

`repo-url` é a URL do repositório. Se a URL não incluir um esquema (seja porque o
caminho do módulo tem um qualificador de VCS, seja porque a tag `<meta>` não tem
esquema), o comando `go` tentará cada protocolo suportado pelo
sistema de controle de versão. Por exemplo, com Git, o comando `go` tentará `https://` e depois
`git+ssh://`. Protocolos inseguros (como `http://` e `git://`) só podem ser usados
se o caminho do módulo for correspondido pela variável de ambiente `GOINSECURE`.

`subdirectory`, se presente, é o subdiretório do repositório, separado por barras, ao qual o
`root-path` corresponde, substituindo o padrão de diretório raiz do repositório. Tags `meta` `go-import` que
fornecem um `subdirectory` só são reconhecidas pelo Go 1.25 e versões posteriores. Tentativas de buscar módulos
em versões anteriores do Go ignorarão a tag meta e resultarão em falha de resolução caso o módulo não possa
ser resolvido de outra forma.

<table id="vcs-support" class="ModTable">
  <thead>
    <tr>
      <th>Nome</th>
      <th>Comando</th>
      <th>Padrão de GOVCS</th>
      <th>Esquemas seguros</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Bazaar</td>
      <td><code>bzr</code></td>
      <td>Somente privado</td>
      <td><code>https</code>, <code>bzr+ssh</code></td>
    </tr>
    <tr>
      <td>Fossil</td>
      <td><code>fossil</code></td>
      <td>Somente privado</td>
      <td><code>https</code></td>
    </tr>
    <tr>
      <td>Git</td>
      <td><code>git</code></td>
      <td>Público e privado</td>
      <td><code>https</code>, <code>git+ssh</code>, <code>ssh</code></td>
    </tr>
    <tr>
      <td>Mercurial</td>
      <td><code>hg</code></td>
      <td>Público e privado</td>
      <td><code>https</code>, <code>ssh</code></td>
    </tr>
    <tr>
      <td>Subversion</td>
      <td><code>svn</code></td>
      <td>Somente privado</td>
      <td><code>https</code>, <code>svn+ssh</code></td>
    </tr>
  </tbody>
</table>

Como exemplo, considere novamente `golang.org/x/mod`. O comando `go` envia
uma requisição para `https://golang.org/x/mod?go-get=1`. O servidor responde
com um documento HTML contendo a tag:

```
<meta name="go-import" content="golang.org/x/mod git https://go.googlesource.com/mod">
```

A partir dessa resposta, o comando `go` usará o repositório Git na
URL remota `https://go.googlesource.com/mod`.

GitHub e outros serviços de hospedagem populares respondem a consultas `?go-get=1` para
todos os repositórios, então normalmente não é necessária nenhuma configuração de servidor para módulos
hospedados nesses sites.

Depois que a URL do repositório é encontrada, o comando `go` clona o repositório
no cache de módulos. Em geral, o comando `go` tenta evitar buscar
dados desnecessários de um repositório. No entanto, os comandos realmente usados variam conforme
o sistema de controle de versão e podem mudar com o tempo. Para Git, o comando `go` consegue
listar a maioria das versões disponíveis sem baixar commits. Normalmente ele busca
commits sem baixar commits ancestrais, mas isso às vezes é
necessário.

### Mapeando versões para commits {#vcs-version}

O comando `go` pode fazer checkout de um módulo dentro de um repositório em uma
[versão canônica](#glos-canonical-version) específica, como `v1.2.3`, `v2.4.0-beta` ou
`v3.0.0+incompatible`. Cada versão de módulo deve ter uma <dfn>tag de versão semântica</dfn>
dentro do repositório que indique qual revisão deve ser usada no checkout para uma determinada
versão.

Se um módulo estiver definido no diretório raiz do repositório ou em um subdiretório de versão principal
do diretório raiz, então cada nome de tag de versão é igual à versão correspondente. Por exemplo, o módulo `golang.org/x/text` está definido no
diretório raiz do seu repositório, então a versão `v0.3.2` tem a tag
`v0.3.2` nesse repositório. Isso vale para a maioria dos módulos.

Se um módulo estiver definido em um subdiretório dentro do repositório, ou seja, a
parte do [subdiretório do módulo](#glos-module-subdirectory) do caminho do módulo não
estiver vazia, então cada nome de tag deve ser prefixado com o subdiretório do módulo,
seguido de uma barra. Por exemplo, o módulo `golang.org/x/tools/gopls` está
definido no subdiretório `gopls` do repositório com caminho raiz
`golang.org/x/tools`. A versão `v0.4.0` desse módulo deve ter a tag
chamada `gopls/v0.4.0` nesse repositório.

O número da versão principal de uma tag de versão semântica deve ser consistente com o
sufixo de versão principal do caminho do módulo (se houver). Por exemplo, a tag `v1.0.0` pode
pertencer ao módulo `example.com/mod`, mas não a `example.com/mod/v2`, que teria tags
como `v2.0.0`.

Uma tag com versão principal `v2` ou superior pode pertencer a um módulo sem sufixo de versão principal
se nenhum arquivo `go.mod` estiver presente e o módulo estiver no diretório raiz do
repositório. Esse tipo de versão é indicado pelo sufixo `+incompatible`. A própria tag de versão
não deve ter o sufixo. Veja
[Compatibilidade com repositórios que não são módulos](#non-module-compat).

Depois que uma tag é criada, ela não deve ser excluída nem alterada para outra
revisão. As versões são [autenticadas](#authenticating) para garantir builds seguros e
repetíveis. Se uma tag for modificada, os clientes podem receber um erro de segurança
ao baixá-la. Mesmo depois que uma tag é excluída, seu conteúdo pode continuar
disponível em [proxies de módulos](#glos-module-proxy).

### Mapeando pseudo-versões para commits {#vcs-pseudo}

O comando `go` pode fazer checkout de um módulo dentro de um repositório em uma
revisão específica, codificada como uma [pseudo-versão](#glos-pseudo-version), como
`v1.3.2-0.20191109021931-daa7c04131f5`.

Os últimos 12 caracteres da pseudo-versão (`daa7c04131f5` no exemplo
acima) indicam uma revisão no repositório a ser usada no checkout. O significado disso
depende do sistema de controle de versão. Para Git e Mercurial, trata-se de um prefixo
de um hash de commit. Para Subversion, trata-se de um número de revisão com zeros à esquerda.

Antes de fazer checkout de um commit, o comando `go` verifica se o timestamp
(`20191109021931` no exemplo acima) corresponde à data do commit. Ele também verifica se a
versão base (`v1.3.1`, a versão anterior a `v1.3.2` no exemplo acima) corresponde
a uma tag de versão semântica que é ancestral do commit. Essas verificações garantem
que os autores de módulos tenham controle total sobre como as pseudo-versões se comparam com
outras versões lançadas.

Veja [Pseudo-versões](#pseudo-versions) para mais informações.

### Mapeando branches e commits para versões {#vcs-branch}

Um módulo pode ter checkout em um branch, tag ou revisão específicos usando uma
[consulta de versão](#version-queries).

```
go get example.com/mod@master
```

O comando `go` converte esses nomes em [versões canônicas](#glos-canonical-version)
que podem ser usadas com a [seleção mínima de versões (MVS)](#minimal-version-selection). O MVS depende da capacidade
de ordenar versões de forma não ambígua. Nomes de branches e revisões não podem ser comparados
de forma confiável ao longo do tempo, pois dependem da estrutura do repositório, que pode mudar.

Se uma revisão estiver marcada com uma ou mais tags de versão semântica, como `v1.2.3`,
será usada a tag da versão válida mais alta. O comando `go` considera apenas tags de versão semântica que
possam pertencer ao módulo de destino; por exemplo, a tag `v1.5.2` não seria considerada para `example.com/mod/v2`, já que
a versão principal não corresponde ao sufixo do caminho do módulo.

Se uma revisão não tiver uma tag de versão semântica válida, o comando `go`
gerará uma [pseudo-versão](#glos-pseudo-version). Se a revisão tiver ancestrais com tags de
versão semântica válidas, a versão ancestral mais alta será
usada como base da pseudo-versão. Veja [Pseudo-versões](#pseudo-versions).

### Diretórios de módulos dentro de um repositório {#vcs-dir}

Depois que o repositório de um módulo tiver sido submetido a checkout em uma revisão específica, o comando
`go` precisa localizar o diretório que contém o arquivo `go.mod` do módulo
(o diretório raiz do módulo).

Lembre-se de que um [caminho de módulo](#module-path) é composto por três partes: um caminho raiz
do repositório (correspondente ao diretório raiz do repositório),
um subdiretório do módulo e um sufixo de versão principal (somente para módulos lançados
na versão `v2` ou superior).

Para a maioria dos módulos, o caminho do módulo é igual ao caminho raiz do repositório, então o
diretório raiz do módulo é o diretório raiz do repositório.

Módulos às vezes são definidos em subdiretórios de um repositório. Isso normalmente
é feito em repositórios grandes com vários componentes que precisam ser lançados e
versionados de forma independente. Espera-se que esse módulo seja encontrado em um
subdiretório correspondente à parte do caminho do módulo que vem depois do caminho raiz
do repositório. Por exemplo, suponha que o módulo `example.com/monorepo/foo/bar` esteja no
repositório com caminho raiz `example.com/monorepo`. Seu arquivo `go.mod` deve estar no
subdiretório `foo/bar`.

Se um módulo for lançado na versão principal `v2` ou superior, seu caminho deve ter um
[sufixo de versão principal](#major-version-suffixes). Um módulo com sufixo de versão principal
pode ser definido em um de dois subdiretórios: um com o sufixo
e outro sem. Por exemplo, suponha que uma nova versão do módulo acima seja
lançada com o caminho `example.com/monorepo/foo/bar/v2`. Seu arquivo `go.mod`
pode estar em `foo/bar` ou em `foo/bar/v2`.

Subdiretórios com sufixo de versão principal são <dfn>subdiretórios de versão principal</dfn>.
Eles podem ser usados para desenvolver várias versões principais de um
módulo em um único branch. Isso pode ser desnecessário quando o desenvolvimento de várias versões principais ocorre em
branches separados. No entanto, subdiretórios de versão principal têm uma propriedade importante: no modo `GOPATH`, os
caminhos de importação de pacotes correspondem exatamente aos diretórios em `GOPATH/src`. O comando `go` oferece
compatibilidade mínima de módulos no modo `GOPATH` (veja [Compatibilidade com
repositórios que não são módulos](#non-module-compat)), então subdiretórios de versão principal
nem sempre são necessários para compatibilidade com projetos construídos no modo `GOPATH`. Ferramentas
mais antigas que não suportam compatibilidade mínima de módulos podem, no entanto, apresentar problemas.

Depois que o comando `go` encontra o diretório raiz do módulo, ele cria um arquivo `.zip`
com o conteúdo do diretório e, em seguida, extrai o arquivo `.zip` para o
cache de módulos. Veja [Restrições de caminho e tamanho de arquivos](#zip-path-size-constraints)
para detalhes sobre quais arquivos podem ser incluídos no arquivo `.zip`. O conteúdo do
arquivo `.zip` é [autenticado](#authenticating) antes da extração para o
cache de módulos, da mesma forma que seria se o arquivo `.zip` fosse baixado de um
proxy.

Os arquivos zip de módulos não incluem o conteúdo de diretórios `vendor` nem de módulos aninhados (subdiretórios que contêm
arquivos `go.mod`). Isso significa que um módulo deve evitar referir-se a arquivos fora do seu diretório ou em
outros módulos. Por exemplo, os padrões de [`//go:embed`](https://pkg.go.dev/embed#hdr-Directives)
não devem corresponder a arquivos em módulos aninhados. Esse comportamento pode servir como uma solução útil
em situações nas quais arquivos não devem ser incluídos em um módulo.
Por exemplo, se um repositório tiver arquivos grandes versionados em um
diretório `testdata`, o autor do módulo pode adicionar um arquivo `go.mod` vazio em `testdata`
para que seus usuários não precisem baixar esses arquivos. É claro que isso pode reduzir
a cobertura de testes para usuários que testam suas dependências.

### Caso especial para arquivos LICENSE {#vcs-license}

Quando o comando `go` cria um arquivo `.zip` para um módulo que não está no diretório raiz do repositório, se o módulo não tiver um arquivo chamado `LICENSE` em seu diretório raiz (junto com `go.mod`), o comando `go` copiará o arquivo chamado `LICENSE` do diretório raiz do repositório, caso ele esteja presente na mesma revisão.

Esse caso especial permite que o mesmo arquivo `LICENSE` se aplique a todos os módulos dentro de um repositório. Isso se aplica somente a arquivos chamados especificamente `LICENSE`, sem extensões como `.txt`. Infelizmente, isso não pode ser estendido sem quebrar as somas criptográficas de módulos existentes; veja [Autenticação de módulos](#authenticating). Outras ferramentas e sites como [pkg.go.dev](https://pkg.go.dev) podem reconhecer arquivos com outros nomes.

Observe também que o comando `go` não inclui links simbólicos ao criar arquivos `.zip` de módulos; veja [Restrições de caminho e tamanho de arquivos](#zip-path-size-constraints). Consequentemente, se um repositório não tiver um arquivo `LICENSE` em seu diretório raiz, os autores podem, em vez disso, criar cópias de seus arquivos de licença em módulos definidos em subdiretórios, para garantir que esses arquivos sejam incluídos nos arquivos `.zip` dos módulos.

### Controlando ferramentas de controle de versão com `GOVCS` {#vcs-govcs}

A capacidade do comando `go` de baixar módulos com comandos de controle de versão como `git` é essencial para o ecossistema descentralizado de pacotes, no qual código pode ser importado de qualquer servidor. Também é um potencial problema de segurança se um servidor malicioso encontrar uma forma de fazer com que o comando de controle de versão invocado execute código não intencional.

Para equilibrar as preocupações de funcionalidade e segurança, o comando `go` por padrão só usará `git` e `hg` para baixar código de servidores públicos. Ele usará qualquer [sistema de controle de versão conhecido](#vcs-support) para baixar código de servidores privados, definidos como aqueles que hospedam pacotes que correspondem à [variável de ambiente](#environment-variables) `GOPRIVATE`. A justificativa para permitir apenas Git e Mercurial é que esses dois sistemas receberam mais atenção quanto a problemas de execução como clientes de servidores não confiáveis. Em contraste, Bazaar, Fossil e Subversion têm sido usados principalmente em ambientes confiáveis e autenticados e não são tão bem analisados como superfícies de ataque.

As restrições de comandos de controle de versão se aplicam somente ao usar acesso direto ao controle de versão para baixar código. Ao baixar módulos de um proxy, o comando `go` usa o [protocolo `GOPROXY`](#goproxy-protocol), que é sempre permitido. Por padrão, o comando `go` usa o espelho de módulos do Go ([proxy.golang.org](https://proxy.golang.org)) para módulos públicos e só recorre ao controle de versão para módulos privados ou quando o espelho se recusa a servir um pacote público (normalmente por motivos legais). Portanto, clientes ainda podem acessar código público servido a partir de repositórios Bazaar, Fossil ou Subversion por padrão, porque esses downloads usam o espelho de módulos do Go, que assume o risco de segurança de executar os comandos de controle de versão usando um sandbox personalizado.

A variável `GOVCS` pode ser usada para alterar os sistemas de controle de versão permitidos para módulos específicos. A variável `GOVCS` se aplica ao compilar pacotes tanto no modo com reconhecimento de módulos quanto no modo GOPATH. Ao usar módulos, os padrões correspondem ao caminho do módulo. Ao usar GOPATH, os padrões correspondem ao caminho de importação correspondente à raiz do repositório de controle de versão.

A forma geral da variável `GOVCS` é uma lista separada por vírgulas de regras `pattern:vcslist`. O `pattern` é um [padrão glob](/pkg/path#Match) que deve corresponder a um ou mais elementos iniciais do caminho do módulo ou de importação. A `vcslist` é uma lista separada por barras verticais de comandos de controle de versão permitidos, ou `all` para permitir o uso de qualquer comando conhecido, ou `off` para não permitir nada. Observe que, se um módulo corresponder a um padrão com `vcslist` igual a `off`, ele ainda poderá ser baixado se o servidor de origem usar o esquema `mod`, que instrui o comando `go` a baixar o módulo usando o [protocolo `GOPROXY`](#goproxy-protocol). O primeiro padrão correspondente na lista se aplica, mesmo que padrões posteriores também possam corresponder.

Por exemplo, considere:

```
GOVCS=github.com:git,evil.com:off,*:git|hg
```

Com essa configuração, código com um caminho de módulo ou de importação começando com `github.com/` só pode usar `git`; caminhos em `evil.com` não podem usar nenhum comando de controle de versão, e todos os outros caminhos (`*` corresponde a tudo) podem usar apenas `git` ou `hg`.

Os padrões especiais `public` e `private` correspondem a caminhos de módulo ou de importação públicos e privados. Um caminho é privado se corresponder à variável `GOPRIVATE`; caso contrário, é público.

Se nenhuma regra da variável `GOVCS` corresponder a um determinado caminho de módulo ou de importação, o comando `go` aplica sua regra padrão, que agora pode ser resumida na notação do `GOVCS` como `public:git|hg,private:all`.

Para permitir o uso irrestrito de qualquer sistema de controle de versão para qualquer pacote, use:

```
GOVCS=*:all
```

Para desabilitar todo uso de controle de versão, use:

```
GOVCS=*:off
```

O [comando `go env -w`](/cmd/go/#hdr-Print_Go_environment_information) pode ser usado para definir a variável `GOVCS` para as próximas invocações do comando `go`.

`GOVCS` foi introduzida no Go 1.16. Versões anteriores do Go podem usar qualquer ferramenta de controle de versão conhecida para qualquer módulo.

## Arquivos zip de módulos {#zip-files}

Versões de módulos são distribuídas como arquivos `.zip`. Raramente há necessidade de interagir diretamente com esses arquivos, já que o comando `go` os cria, baixa e extrai automaticamente a partir de [proxies de módulos](#glos-module-proxy) e repositórios de controle de versão. No entanto, ainda é útil conhecer esses arquivos para entender restrições de compatibilidade entre plataformas ou ao implementar um proxy de módulos.

O comando [`go mod download`](#go-mod-download) baixa arquivos zip para um ou mais módulos e, em seguida, extrai esses arquivos para o [cache de módulos](#glos-module-cache). Dependendo de `GOPROXY` e de outras [variáveis de ambiente](#environment-variables), o comando `go` pode baixar arquivos zip de um proxy ou clonar repositórios de controle de versão e criar arquivos zip a partir deles. A flag `-json` pode ser usada para encontrar a localização dos arquivos zip baixados e de seus conteúdos extraídos no cache de módulos.

O pacote [`golang.org/x/mod/zip`](https://pkg.go.dev/golang.org/x/mod/zip?tab=doc) pode ser usado para criar, extrair ou verificar o conteúdo de arquivos zip programaticamente.

### Restrições de caminho e tamanho de arquivos {#zip-path-size-constraints}

Há diversas restrições sobre o conteúdo dos arquivos zip de módulos. Essas restrições garantem que os arquivos zip possam ser extraídos com segurança e de forma consistente em uma ampla variedade de plataformas.

* Um arquivo zip de módulo pode ter no máximo 500 MiB. O tamanho total descompactado de seus arquivos também é limitado a 500 MiB. Arquivos `go.mod` são limitados a 16 MiB. Arquivos `LICENSE` também são limitados a 16 MiB. Esses limites existem para mitigar ataques de negação de serviço contra usuários, proxies e outras partes do ecossistema de módulos. Repositórios que contêm mais de 500 MiB de arquivos em uma árvore de diretórios de módulo devem marcar versões de módulos em commits que incluam apenas os arquivos necessários para compilar os pacotes do módulo; vídeos, modelos e outros recursos grandes normalmente não são necessários para as compilações.
* Cada arquivo dentro de um arquivo zip de módulo deve começar com o prefixo `$module@$version/`, em que `$module` é o caminho do módulo e `$version` é a versão, por exemplo, `golang.org/x/mod@v0.3.0/`. O caminho do módulo deve ser válido, a versão deve ser válida e canônica, e a versão deve corresponder ao sufixo de versão principal do caminho do módulo. Veja [Caminhos e versões de módulos](#go-mod-file-ident) para definições e restrições específicas.
* Modos de arquivo, carimbos de data/hora e outros metadados são ignorados.
* Diretórios vazios (entradas com caminhos terminando em barra) podem ser incluídos em arquivos zip de módulos, mas não são extraídos. O comando `go` não inclui diretórios vazios nos arquivos zip que cria.
* Links simbólicos e outros arquivos irregulares são ignorados ao criar arquivos zip, já que não são portáveis entre sistemas operacionais e sistemas de arquivos, e não há uma forma portável de representá-los no formato zip.
* Arquivos dentro de diretórios chamados `vendor` são ignorados ao criar arquivos zip, já que diretórios `vendor` fora do módulo principal nunca são usados.
* Arquivos dentro de diretórios que contêm arquivos `go.mod`, exceto o diretório raiz do módulo, são ignorados ao criar arquivos zip, já que não fazem parte do módulo. O comando `go` ignora subdiretórios que contêm arquivos `go.mod` ao extrair arquivos zip.
* Nenhum par de arquivos dentro de um arquivo zip pode ter caminhos iguais segundo a dobra de caixa Unicode (veja [`strings.EqualFold`](https://pkg.go.dev/strings?tab=doc#EqualFold)). Isso garante que os arquivos zip possam ser extraídos em sistemas de arquivos que não diferenciam maiúsculas de minúsculas sem colisões.
* Um arquivo `go.mod` pode ou não aparecer no diretório de nível superior (`$module@$version/go.mod`). Se estiver presente, deve se chamar `go.mod` (todo em minúsculas). Arquivos chamados `go.mod` não são permitidos em nenhum outro diretório.
* Nomes de arquivos e diretórios dentro de um módulo podem consistir em letras Unicode, dígitos ASCII, o caractere de espaço ASCII (U+0020) e os caracteres de pontuação ASCII `!#$%&()+,-.=@[]^_{}~`. Observe que caminhos de pacotes podem não conter todos esses caracteres. Veja [`module.CheckFilePath`](https://pkg.go.dev/golang.org/x/mod/module?tab=doc#CheckFilePath) e [`module.CheckImportPath`](https://pkg.go.dev/golang.org/x/mod/module?tab=doc#CheckImportPath) para ver as diferenças.
* Um nome de arquivo ou diretório até o primeiro ponto não pode ser um nome reservado no Windows, independentemente de maiúsculas ou minúsculas (`CON`, `com1`, `NuL`, e assim por diante).

## Módulos privados {#private-modules}

Módulos Go são frequentemente desenvolvidos e distribuídos em servidores de controle de versão e proxies de módulos que não estão disponíveis na internet pública. O comando `go` pode baixar e compilar módulos de fontes privadas, embora normalmente exija alguma configuração.

As variáveis de ambiente abaixo podem ser usadas para configurar o acesso a módulos privados. Veja [Variáveis de ambiente](#environment-variables) para detalhes. Veja também [Privacidade](#private-module-privacy) para informações sobre como controlar os dados enviados a servidores públicos.

* `GOPROXY` — lista de URLs de proxies de módulos. O comando `go` tentará baixar módulos de cada servidor em sequência. A palavra-chave `direct` instrui o comando `go` a baixar módulos dos repositórios de controle de versão onde são desenvolvidos, em vez de usar um proxy.
* `GOPRIVATE` — lista de padrões glob de prefixos de caminhos de módulos que devem ser considerados privados. Serve como valor padrão para `GONOPROXY` e `GONOSUMDB`.
* `GONOPROXY` — lista de padrões glob de prefixos de caminhos de módulos que não devem ser baixados de um proxy. O comando `go` baixará módulos correspondentes dos repositórios de controle de versão onde são desenvolvidos, independentemente de `GOPROXY`.
* `GONOSUMDB` — lista de padrões glob de prefixos de caminhos de módulos que não devem ser verificados usando o banco de dados público de checksums, [sum.golang.org](https://sum.golang.org).
* `GOINSECURE` — lista de padrões glob de prefixos de caminhos de módulos que podem ser obtidos via HTTP e outros protocolos inseguros.

Essas variáveis podem ser definidas no ambiente de desenvolvimento (por exemplo, em um arquivo `.profile`) ou podem ser definidas permanentemente com o [comando `go env -w`](/cmd/go/#hdr-Print_Go_environment_information).

O restante desta seção descreve padrões comuns para fornecer acesso a proxies privados de módulos e repositórios de controle de versão.

### Proxy privado servindo todos os módulos {#private-module-proxy-all}

Um servidor proxy privado central que serve todos os módulos (públicos e privados) oferece o maior controle para administradores e exige a menor configuração para desenvolvedores individuais.

Para configurar o comando `go` para usar esse servidor, defina as seguintes variáveis de ambiente, substituindo `https://proxy.corp.example.com` pela URL do seu proxy e `corp.example.com` pelo seu prefixo de módulo:

```
GOPROXY=https://proxy.corp.example.com
GONOSUMDB=corp.example.com
```

A configuração `GOPROXY` instrui o comando `go` a baixar módulos somente de `https://proxy.corp.example.com`; o comando `go` não se conectará a outros proxies ou repositórios de controle de versão.

A configuração `GONOSUMDB` instrui o comando `go` a não usar o banco de dados público de checksums para autenticar módulos com caminhos começando por `corp.example.com`.

Um proxy executando nessa configuração provavelmente precisará de acesso de leitura a servidores de controle de versão privados. Também precisará de acesso à internet pública para baixar novas versões de módulos públicos.

Existem várias implementações de servidores `GOPROXY` que podem ser usadas dessa forma. Uma implementação mínima serviria arquivos a partir de um diretório de [cache de módulos](#glos-module-cache) e usaria o [`go mod download`](#go-mod-download) (com configuração adequada) para obter módulos ausentes.

### Proxy privado servindo módulos privados {#private-module-proxy-private}

Um servidor proxy privado pode servir módulos privados sem também servir módulos publicamente disponíveis. O comando `go` pode ser configurado para recorrer a fontes públicas para módulos que não estão disponíveis no servidor privado.

Para configurar o comando `go` para funcionar dessa forma, defina as seguintes variáveis de ambiente, substituindo `https://proxy.corp.example.com` pela URL do proxy e `corp.example.com` pelo prefixo de módulo:

```
GOPROXY=https://proxy.corp.example.com,https://proxy.golang.org,direct
GONOSUMDB=corp.example.com
```

A configuração `GOPROXY` instrui o comando `go` a tentar baixar módulos primeiro de `https://proxy.corp.example.com`. Se esse servidor responder com 404 (Not Found) ou 410 (Gone), o comando `go` recorrerá a `https://proxy.golang.org` e, depois, a conexões diretas com os repositórios.

A configuração `GONOSUMDB` instrui o comando `go` a não usar o banco de dados público de checksums para autenticar módulos cujos caminhos começam com `corp.example.com`.

Observe que um proxy usado nessa configuração ainda pode controlar o acesso a módulos públicos, mesmo que não os sirva. Se o proxy responder a uma requisição com um status de erro diferente de 404 ou 410, o comando `go` não recorrerá às entradas posteriores da lista `GOPROXY`. Por exemplo, o proxy poderia responder com 403 (Forbidden) para um módulo com licença inadequada ou com vulnerabilidades de segurança conhecidas.

### Acesso direto a módulos privados {#private-module-proxy-direct}

O comando `go` pode ser configurado para contornar proxies públicos e baixar módulos privados diretamente dos servidores de controle de versão. Isso é útil quando executar um servidor proxy privado não é viável.

Para configurar o comando `go` para funcionar dessa forma, defina `GOPRIVATE`, substituindo `corp.example.com` pelo prefixo do módulo privado:

```
GOPRIVATE=corp.example.com
```

A variável `GOPROXY` não precisa ser alterada nessa situação. Seu valor padrão é `https://proxy.golang.org,direct`, o que instrui o comando `go` a tentar baixar módulos primeiro de `https://proxy.golang.org` e, em seguida, recorrer a uma conexão direta se esse proxy responder com 404 (Not Found) ou 410 (Gone).

A configuração `GOPRIVATE` instrui o comando `go` a não se conectar a um proxy nem ao banco de dados de checksums para módulos que começam com `corp.example.com`.

Ainda pode ser necessário um servidor HTTP interno para [resolver caminhos de módulos para URLs de repositórios](#vcs-find). Por exemplo, quando o comando `go` baixa o módulo `corp.example.com/mod`, ele enviará uma requisição GET para `https://corp.example.com/mod?go-get=1` e procurará a URL do repositório na resposta. Para evitar esse requisito, garanta que cada caminho de módulo privado tenha um sufixo de VCS (como `.git`) marcando o prefixo da raiz do repositório. Por exemplo, quando o comando `go` baixa o módulo `corp.example.com/repo.git/mod`, ele clonará o repositório Git em `https://corp.example.com/repo.git` ou `ssh://corp.example.com/repo.git` sem precisar fazer requisições adicionais.

Os desenvolvedores precisarão de acesso de leitura aos repositórios que contêm módulos privados. Isso pode ser configurado em arquivos globais de configuração de VCS, como `.gitconfig`. É melhor que as ferramentas de VCS sejam configuradas para não precisar de prompts interativos de autenticação. Por padrão, ao invocar o Git, o comando `go` desabilita prompts interativos definindo `GIT_TERMINAL_PROMPT=0`, mas respeita configurações explícitas.

### Passando credenciais para proxies privados {#private-module-proxy-auth}

O comando `go` oferece suporte à [autenticação básica HTTP](https://en.wikipedia.org/wiki/Basic_access_authentication) ao se comunicar com servidores proxy.

As credenciais podem ser especificadas em um [arquivo `.netrc`](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html).
Por exemplo, um arquivo `.netrc` contendo as linhas abaixo configuraria o comando `go`
para se conectar à máquina `proxy.corp.example.com` com o nome de usuário
e a senha indicados.

```
machine proxy.corp.example.com
login jrgopher
password hunter2
```

A localização do arquivo pode ser definida com a variável de ambiente `NETRC`. Se
`NETRC` não estiver definida, o comando `go` lerá `$HOME/.netrc` em plataformas
semelhantes ao UNIX ou `%USERPROFILE%\_netrc` no Windows.

Os campos em `.netrc` são separados por espaços, tabulações e quebras de linha. Infelizmente,
esses caracteres não podem ser usados em nomes de usuário ou senhas. Observe também que o
nome da máquina não pode ser uma URL completa, portanto não é possível especificar
nomes de usuário e senhas diferentes para caminhos distintos na mesma máquina.

Alternativamente, as credenciais podem ser especificadas diretamente nas URLs de `GOPROXY`. Por
exemplo:

```
GOPROXY=https://jrgopher:hunter2@proxy.corp.example.com
```

Tenha cuidado ao adotar essa abordagem: variáveis de ambiente podem aparecer
no histórico do shell e nos logs.

### Passando credenciais para repositórios privados {#private-module-repo-auth}

O comando `go` pode baixar um módulo diretamente de um repositório de controle de versão. Isso é
necessário para módulos privados caso um proxy privado não seja
utilizado. Consulte [Acesso direto a módulos privados](#private-module-proxy-direct)
para a configuração.

O comando `go` executa ferramentas de controle de versão como `git` ao baixar
módulos diretamente. Essas ferramentas realizam a própria autenticação, então você pode
precisar configurar credenciais em um arquivo de configuração específico da ferramenta, como
`.gitconfig`.

Para garantir que isso funcione sem problemas, certifique-se de que o comando `go` use a URL correta
do repositório e de que a ferramenta de controle de versão não exija a digitação de uma senha
de forma interativa. O comando `go` prefere URLs `https://` a outros esquemas
como `ssh://`, a menos que o esquema tenha sido especificado ao [consultar a
URL do repositório](#vcs-find). Para repositórios do GitHub especificamente, o comando
`go` assume `https://`.

<!-- TODO(golang.org/issue/26134): if this issue is fixed, we can remove the
mention of the special case for GitHub above. -->

Para a maioria dos servidores, você pode configurar seu cliente para autenticar via HTTP. Por
exemplo, o GitHub oferece suporte ao uso de [tokens de acesso pessoal OAuth como
senhas HTTP](https://docs.github.com/en/free-pro-team@latest/github/extending-github/git-automation-with-oauth-tokens).
Você pode armazenar senhas HTTP em um arquivo `.netrc`, como ao [passar credenciais para
proxies privados](#private-module-proxy-auth).

Alternativamente, você pode reescrever URLs `https://` para outro esquema. Por exemplo,
no `.gitconfig`:

```
[url "git@github.com:"]
    insteadOf = https://github.com/
```

Para mais informações, consulte [Por que o "go get" usa HTTPS ao clonar um
repositório?](/doc/faq#git_https)

### Privacidade {#private-module-privacy}

O comando `go` pode baixar módulos e metadados de servidores proxy de módulos e de sistemas
de controle de versão. A variável de ambiente `GOPROXY`
controla quais servidores são usados. As variáveis de ambiente `GOPRIVATE` e
`GONOPROXY` controlam quais módulos são obtidos de proxies.

O valor padrão de `GOPROXY` é:

```
https://proxy.golang.org,direct
```

Com essa configuração, quando o comando `go` baixa um módulo ou os metadados de um módulo,
ele primeiro envia uma requisição para `proxy.golang.org`, um proxy público de módulos
operado pelo Google ([política de privacidade](https://proxy.golang.org/privacy)). Consulte
[protocolo `GOPROXY`](#goproxy-protocol) para detalhes sobre quais informações são enviadas
em cada requisição. O comando `go` não transmite informações de identificação pessoal,
mas transmite o caminho completo do módulo solicitado. Se o
proxy responder com status 404 (Not Found) ou 410 (Gone), o comando `go`
tentará se conectar diretamente ao sistema de controle de versão que fornece o
módulo. Consulte [Sistemas de controle de versão](#vcs) para detalhes.

As variáveis de ambiente `GOPRIVATE` ou `GONOPROXY` podem ser definidas com listas de padrões
glob que correspondam a prefixos de módulos privados que não devem ser
solicitados a nenhum proxy. Por exemplo:

```
GOPRIVATE=*.corp.example.com,*.research.example.com
```

`GOPRIVATE` atua simplesmente como padrão para `GONOPROXY` e `GONOSUMDB`, então não é
necessário definir `GONOPROXY` a menos que `GONOSUMDB` deva ter um valor diferente. Quando um
caminho de módulo é correspondido por `GONOPROXY`, o comando `go` ignora
`GOPROXY` para esse módulo e o obtém diretamente do seu repositório de controle de versão. Isso é
útil quando nenhum proxy serve módulos privados. Consulte [Acesso direto a
módulos privados](#private-module-proxy-direct).

Se houver um [proxy confiável que sirva todos os módulos](#private-module-proxy-all),
então `GONOPROXY` não deve ser definido. Por exemplo, se `GOPROXY` for definido com uma
única fonte, o comando `go` não baixará módulos de outras fontes.
`GONOSUMDB` ainda deve ser definido nessa situação.

```
GOPROXY=https://proxy.corp.example.com
GONOSUMDB=*.corp.example.com,*.research.example.com
```

Se houver um [proxy confiável que sirva apenas módulos privados](#private-module-proxy-private),
`GONOPROXY` não deve ser definido, mas deve-se tomar cuidado para garantir que o proxy responda com os
códigos de status corretos. Por exemplo, considere a seguinte configuração:

```
GOPROXY=https://proxy.corp.example.com,https://proxy.golang.org
GONOSUMDB=*.corp.example.com,*.research.example.com
```

Suponha que, devido a um erro de digitação, um desenvolvedor tente baixar um módulo que
não existe.

```
go mod download corp.example.com/secret-product/typo@latest
```

O comando `go` primeiro solicita este módulo a `proxy.corp.example.com`. Se
esse proxy responder com 404 (Not Found) ou 410 (Gone), o comando `go` irá
recorrer a `proxy.golang.org`, transmitindo o caminho `secret-product` na
URL da requisição. Se o proxy privado responder com qualquer outro código de erro, o
comando `go` exibe o erro e não recorrerá a outras fontes.

Além dos proxies, o comando `go` pode se conectar ao banco de dados de checksums para
verificar os hashes criptográficos de módulos não listados em `go.sum`. A variável de ambiente
`GOSUMDB` define o nome, a URL e a chave pública do banco de dados de checksums. O valor padrão de `GOSUMDB` é `sum.golang.org`, o
banco de dados público de checksums operado pelo Google ([política de
privacidade](https://sum.golang.org/privacy)). Consulte [Banco de dados de
checksums](#checksum-database) para detalhes sobre o que é transmitido em cada
requisição. Assim como nos proxies, o comando `go` não transmite informações de identificação
pessoal, mas transmite o caminho completo do módulo solicitado, e o banco de dados de checksums não consegue calcular
checksums de módulos não públicos.

A variável de ambiente `GONOSUMDB` pode ser definida com padrões indicando quais
módulos são privados e não devem ser solicitados ao banco de dados de checksums. `GOPRIVATE` atua como padrão para `GONOSUMDB` e `GONOPROXY`, então não é
necessário definir `GONOSUMDB` a menos que `GONOPROXY` deva ter um
valor diferente.

Um proxy pode [espelhar o banco de dados de
checksums](https://go.googlesource.com/proposal/+/master/design/25530-sumdb.md#proxying-a-checksum-database).
Se um proxy em `GOPROXY` fizer isso, o comando `go` não se conectará
ao banco de dados de checksums diretamente.

`GOSUMDB` pode ser definido como `off` para desabilitar completamente o uso do banco de dados de
checksums. Com essa configuração, o comando `go` não autenticará módulos baixados
a menos que eles já estejam em `go.sum`. Consulte [Autenticando
módulos](#authenticating).

## Cache de módulos {#module-cache}

O <dfn>cache de módulos</dfn> é o diretório onde o comando `go` armazena os arquivos de
módulos baixados. O cache de módulos é distinto do cache de build,
que contém pacotes compilados e outros artefatos de build.

A localização padrão do cache de módulos é `$GOPATH/pkg/mod`. Para usar uma
localização diferente, defina a [variável de ambiente](#environment-variables)
`GOMODCACHE`.

O cache de módulos não tem tamanho máximo, e o comando `go` não remove seu
conteúdo automaticamente.

O cache pode ser compartilhado por múltiplos projetos Go desenvolvidos na mesma máquina.
O comando `go` usará o mesmo cache independentemente da localização do
módulo principal. Múltiplas instâncias do comando `go` podem acessar com segurança o
mesmo cache de módulos ao mesmo tempo.

O comando `go` cria arquivos e diretórios de código-fonte de módulos no cache com
permissões somente leitura, para evitar alterações acidentais nos módulos após serem
baixados. Isso tem o efeito colateral infeliz de dificultar a
remoção do cache com comandos como `rm -rf`. O cache pode ser removido com o
[`go clean -modcache`](#go-clean-modcache). Alternativamente, quando a flag
`-modcacherw` é usada, o comando `go` criará novos diretórios com
permissões de leitura e escrita. Isso aumenta o risco de editores, testes e outros
programas modificarem arquivos no cache de módulos. O comando [`go mod
verify`](#go-mod-verify) pode ser usado para detectar modificações nas
dependências do módulo principal. Ele examina o conteúdo extraído de cada
dependência de módulo e confirma que correspondem ao hash esperado em `go.sum`.

A tabela abaixo explica a finalidade da maioria dos arquivos no cache de módulos. Alguns
arquivos transitórios (arquivos de lock, diretórios temporários) são omitidos. Para cada caminho,
`$module` é um caminho de módulo e `$version` é uma versão. Caminhos terminados
em barras (`/`) são diretórios. Letras maiúsculas em caminhos de módulos e versões são
escapadas usando pontos de exclamação (`Azure` é escrito como `!azure`) para evitar
conflitos em sistemas de arquivos que não diferenciam maiúsculas de minúsculas.

<table class="ModTable">
  <thead>
    <tr>
      <th>Caminho</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>$module@$version/</code></td>
      <td>
        Diretório contendo o conteúdo extraído de um arquivo <code>.zip</code>
        de módulo. Ele serve como diretório raiz do módulo para um módulo baixado. Não
        conterá um arquivo <code>go.mod</code> se o módulo original
        não tivesse um.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/</code></td>
      <td>
        Diretório contendo arquivos baixados de proxies de módulos e arquivos
        derivados de <a href="#vcs">sistemas de controle de versão</a>. O layout
        deste diretório segue o
        <a href="#goproxy-protocol">protocolo <code>GOPROXY</code></a>, portanto
        este diretório pode ser usado como proxy quando servido por um servidor de arquivos HTTP
        ou quando referenciado com uma URL <code>file://</code>.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/$module/@v/list</code></td>
      <td>
        Lista de versões conhecidas (consulte o
        <a href="#goproxy-protocol">protocolo <code>GOPROXY</code></a>). Isso
        pode mudar com o tempo, portanto o comando <code>go</code> normalmente busca uma
        nova cópia em vez de reutilizar este arquivo.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/$module/@v/$version.info</code></td>
      <td>
        Metadados em JSON sobre a versão. (consulte o
        <a href="#goproxy-protocol">protocolo <code>GOPROXY</code></a>). Isso
        pode mudar com o tempo, portanto o comando <code>go</code> normalmente busca uma
        nova cópia em vez de reutilizar este arquivo.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/$module/@v/$version.mod</code></td>
      <td>
        O arquivo <code>go.mod</code> desta versão (consulte o
        <a href="#goproxy-protocol">protocolo <code>GOPROXY</code></a>). Se
        o módulo original não tinha um arquivo <code>go.mod</code>, este é
        um arquivo sintetizado sem requisitos.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/$module/@v/$version.zip</code></td>
      <td>
        O conteúdo compactado do módulo (consulte o
        <a href="#goproxy-protocol">protocolo <code>GOPROXY</code></a> e
        <a href="#zip-files">Arquivos zip de módulos</a>).
      </td>
    </tr>
    <tr>
      <td><code>cache/download/$module/@v/$version.ziphash</code></td>
      <td>
        Um hash criptográfico dos arquivos no arquivo <code>.zip</code>.
        Observe que o próprio arquivo <code>.zip</code> não é submetido a hash, então a
        ordem dos arquivos, a compressão, o alinhamento e os metadados não afetam o hash.
        Ao usar um módulo, o comando <code>go</code> verifica se este hash
        corresponde à linha correspondente em
        <a href="#go-sum-files"><code>go.sum</code></a>. O comando
        <a href="#go-mod-verify"><code>go mod verify</code></a> verifica
        se os hashes dos arquivos <code>.zip</code> dos módulos e dos diretórios extraídos correspondem a esses arquivos.
      </td>
    </tr>
    <tr>
      <td><code>cache/download/sumdb/</code></td>
      <td>
        Diretório contendo arquivos baixados de um
        <a href="#checksum-database">banco de dados de checksums</a> (normalmente
        <code>sum.golang.org</code>).
      </td>
    </tr>
    <tr>
      <td><code>cache/vcs/</code></td>
      <td>
        Contém repositórios de controle de versão clonados para módulos obtidos
        diretamente de suas fontes. Os nomes dos diretórios são hashes codificados em hexadecimal
        derivados do tipo de repositório e da URL. Os repositórios são otimizados
        para o espaço em disco. Por exemplo, repositórios Git clonados são bare e
        shallow sempre que possível.
      </td>
    </tr>
  </tbody>
</table>

## Autenticando módulos {#authenticating}

Quando o comando `go` baixa um [arquivo zip](#zip-files) de módulo ou um [arquivo `go.mod`](#go-mod-file) para o [cache de módulos](#module-cache), ele calcula um hash criptográfico e o compara com um valor conhecido para verificar se o arquivo não foi alterado desde que foi baixado pela primeira vez. O comando `go` informa um erro de segurança se um arquivo baixado não tiver o hash correto.

Para arquivos `go.mod`, o comando `go` calcula o hash a partir do conteúdo do arquivo. Para arquivos zip de módulos, o comando `go` calcula o hash a partir dos nomes e dos conteúdos dos arquivos dentro do arquivo compactado, em uma ordem determinística. O hash não é afetado pela ordem dos arquivos, pela compactação, pelo alinhamento nem por outros metadados. Consulte [`golang.org/x/mod/sumdb/dirhash`](https://pkg.go.dev/golang.org/x/mod/sumdb/dirhash?tab=doc) para os detalhes da implementação do hash.

O comando `go` compara cada hash com a linha correspondente no [arquivo `go.sum`](#go-sum-files) do módulo principal. Se o hash for diferente do hash em `go.sum`, o comando `go` informa um erro de segurança e apaga o arquivo baixado, sem adicioná-lo ao cache de módulos.

Se o arquivo `go.sum` não estiver presente, ou se ele não contiver um hash para o arquivo baixado, o comando `go` pode verificar o hash usando o [banco de dados de checksums](#checksum-database), uma fonte global de hashes para módulos disponíveis publicamente. Depois que o hash for verificado, o comando `go` o adiciona a `go.sum` e adiciona o arquivo baixado ao cache de módulos. Se um módulo for privado (identificado pelas variáveis de ambiente `GOPRIVATE` ou `GONOSUMDB`) ou se o banco de dados de checksums estiver desabilitado (definindo `GOSUMDB=off`), o comando `go` aceita o hash e adiciona o arquivo ao cache de módulos sem verificá-lo.

O cache de módulos normalmente é compartilhado por todos os projetos Go de um sistema, e cada módulo pode ter seu próprio arquivo `go.sum`, com hashes potencialmente diferentes. Para evitar a necessidade de confiar em outros módulos, o comando `go` verifica os hashes usando o `go.sum` do módulo principal sempre que acessa um arquivo no cache de módulos. Como calcular hashes de arquivos zip é custoso, o comando `go` verifica os hashes pré-calculados armazenados junto aos arquivos zip, em vez de recalcular o hash dos arquivos. O comando [`go mod verify`](#go-mod-verify) pode ser usado para verificar se os arquivos zip e os diretórios extraídos não foram modificados desde que foram adicionados ao cache de módulos.

### Arquivos go.sum {#go-sum-files}

Um módulo pode ter um arquivo de texto chamado `go.sum` em seu diretório raiz, ao lado do arquivo `go.mod`. O arquivo `go.sum` contém hashes criptográficos das dependências diretas e indiretas do módulo. Quando o comando `go` baixa um arquivo `.mod` ou `.zip` de um módulo para o [cache de módulos](#module-cache), ele calcula um hash e verifica se ele corresponde ao hash correspondente no arquivo `go.sum` do módulo principal. O `go.sum` pode estar vazio ou ausente se o módulo não tiver dependências ou se todas as dependências forem substituídas por diretórios locais usando [diretivas `replace`](#go-mod-file-replace).

Cada linha de `go.sum` tem três campos separados por espaços: um caminho do módulo, uma versão (que pode terminar com `/go.mod`) e um hash.

* O caminho do módulo é o nome do módulo ao qual o hash pertence.
* A versão é a versão do módulo à qual o hash pertence. Se a versão terminar com `/go.mod`, o hash é apenas do arquivo `go.mod` do módulo; caso contrário, o hash é dos arquivos dentro do `.zip` do módulo.
* A coluna do hash consiste em um nome de algoritmo (como `h1`) e um hash criptográfico codificado em base64, separados por dois-pontos (`:`). Atualmente, o SHA-256 (`h1`) é o único algoritmo de hash suportado. Se uma vulnerabilidade no SHA-256 for descoberta no futuro, será adicionado suporte a outro algoritmo (chamado `h2` e assim por diante).

O arquivo `go.sum` pode conter hashes de várias versões de um módulo. O comando `go` pode precisar carregar arquivos `go.mod` de várias versões de uma dependência para executar a [seleção de versão mínima](#minimal-version-selection). O `go.sum` também pode conter hashes de versões de módulos que não são mais necessárias (por exemplo, após uma atualização). O [`go mod tidy`](#go-mod-tidy) adiciona os hashes que faltam e remove do `go.sum` os hashes desnecessários.

### Banco de dados de checksums {#checksum-database}

O banco de dados de checksums é uma fonte global de linhas do `go.sum`. O comando `go` pode usá-lo em muitas situações para detectar comportamentos incorretos de proxies ou servidores de origem.

O banco de dados de checksums garante consistência global e confiabilidade para todas as versões de módulos disponíveis publicamente. Ele torna possíveis proxies não confiáveis, já que eles não conseguem servir o código errado sem que isso seja percebido. Ele também garante que os bits associados a uma versão específica não mudem de um dia para o outro, mesmo que o autor do módulo altere posteriormente as tags em seu repositório.

O banco de dados de checksums é servido por [sum.golang.org](https://sum.golang.org), que é operado pelo Google. Trata-se de um [Transparent Log](https://research.swtch.com/tlog) (ou “Merkle Tree”) de hashes das linhas do `go.sum`, apoiado pelo [Trillian](https://github.com/google/trillian). A principal vantagem de uma Merkle tree é que auditores independentes podem verificar que ela não foi adulterada, por isso ela é mais confiável do que um banco de dados simples.

O comando `go` interage com o banco de dados de checksums usando o protocolo descrito originalmente em [Proposal: Secure the Public Go Module Ecosystem](https://go.googlesource.com/proposal/+/master/design/25530-sumdb.md#checksum-database).

A tabela abaixo especifica as consultas às quais o banco de dados de checksums deve responder. Para cada caminho, `$base` é a parte do caminho da URL do banco de dados de checksums, `$module` é um caminho de módulo e `$version` é uma versão. Por exemplo, se a URL do banco de dados de checksums for `https://sum.golang.org` e o cliente solicitar o registro do módulo `golang.org/x/text` na versão `v0.3.2`, o cliente enviaria uma requisição `GET` para `https://sum.golang.org/lookup/golang.org/x/text@v0.3.2`.

Para evitar ambiguidade ao servir a partir de sistemas de arquivos que não diferenciam maiúsculas de minúsculas, os elementos `$module` e `$version` são [codificados com diferenciação de caixa](https://pkg.go.dev/golang.org/x/mod/module#EscapePath), substituindo cada letra maiúscula por um ponto de exclamação seguido da letra minúscula correspondente. Isso permite que os módulos `example.com/M` e `example.com/m` sejam armazenados em disco, já que o primeiro é codificado como `example.com/!m`.

Partes do caminho entre colchetes, como `[.p/$W]`, indicam valores opcionais.

<table class="ModTable">
  <thead>
    <tr>
      <th>Caminho</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>$base/latest</code></td>
      <td>
        Retorna uma descrição de árvore assinada e codificada para o log mais
        recente. Esta descrição assinada está no formato de uma
        <a href="https://pkg.go.dev/golang.org/x/mod/sumdb/note">note</a>,
        que é um texto assinado por uma ou mais chaves do servidor e pode ser
        verificado usando a chave pública do servidor. A descrição da árvore
        informa o tamanho da árvore e o hash da cabeça da árvore nesse
        tamanho. Esta codificação é descrita em
        <code><a href="https://pkg.go.dev/golang.org/x/mod/sumdb/tlog#FormatTree">
        golang.org/x/mod/sumdb/tlog#FormatTree</a></code>.
      </td>
    </tr>
    <tr>
    <tr>
      <td><code>$base/lookup/$module@$version</code></td>
      <td>
        Retorna o número do registro do log para a entrada sobre <code>$module</code>
        em <code>$version</code>, seguido dos dados do registro (ou seja,
        as linhas do <code>go.sum</code> para <code>$module</code> em
        <code>$version</code>) e uma descrição de árvore assinada e codificada
        que contém o registro.
      </td>
    </tr>
    <tr>
    <tr>
      <td><code>$base/tile/$H/$L/$K[.p/$W]</code></td>
      <td>
        Retorna um [tile de log](https://research.swtch.com/tlog#serving_tiles),
        que é um conjunto de hashes que compõem uma seção do log. Cada tile
        é definido em uma coordenada bidimensional no nível de tile
        <code>$L</code>, na posição <code>$K</code> a partir da esquerda, com
        altura de tile <code>$H</code>. O sufixo opcional <code>.p/$W</code>
        indica um tile parcial do log, com apenas <code>$W</code> hashes.
        Os clientes devem recorrer ao download do tile completo caso um tile
        parcial não seja encontrado.
      </td>
    </tr>
    <tr>
    <tr>
      <td><code>$base/tile/$H/data/$K[.p/$W]</code></td>
      <td>
        Retorna os dados de registro para os hashes de folha em
        <code>/tile/$H/0/$K[.p/$W]</code> (com um elemento de caminho literal
        <code>data</code>).
      </td>
    </tr>
    <tr>
  </tbody>
</table>

Se o comando `go` consultar o banco de dados de checksums, o primeiro passo é obter os dados do registro pelo endpoint `/lookup`. Se a versão do módulo ainda não estiver registrada no log, o banco de dados de checksums tentará buscá-la no servidor de origem antes de responder. Esses dados de `/lookup` fornecem a soma (sum) dessa versão do módulo, bem como sua posição no log, o que informa ao cliente quais tiles devem ser baixados para realizar as provas. O comando `go` realiza provas de “inclusão” (de que um registro específico existe no log) e provas de “consistência” (de que a árvore não foi adulterada) antes de adicionar novas linhas ao arquivo `go.sum` do módulo principal. É importante que os dados de `/lookup` nunca sejam usados sem antes serem autenticados contra o hash de árvore assinado, e que o hash de árvore assinado seja autenticado contra a linha do tempo de hashes de árvore assinados do cliente.

Os hashes de árvore assinados e os novos tiles servidos pelo banco de dados de checksums são armazenados no cache de módulos, de modo que o comando `go` só precisa baixar os tiles que estão faltando.

O comando `go` não precisa se conectar diretamente ao banco de dados de checksums. Ele pode solicitar as somas dos módulos por meio de um proxy de módulos que [espelha o banco de dados de checksums](https://go.googlesource.com/proposal/+/master/design/25530-sumdb.md#proxying-a-checksum-database) e suporta o protocolo acima. Isso pode ser especialmente útil para proxies privados corporativos que bloqueiam requisições para fora da organização.

A variável de ambiente `GOSUMDB` identifica o nome do banco de dados de checksums a ser usado e, opcionalmente, sua chave pública e URL, como em:

```
GOSUMDB="sum.golang.org"
GOSUMDB="sum.golang.org+<publickey>"
GOSUMDB="sum.golang.org+<publickey> https://sum.golang.org"
```

O comando `go` conhece a chave pública de `sum.golang.org` e também sabe que o nome `sum.golang.google.cn` (disponível na China continental) se conecta ao banco de dados de checksums `sum.golang.org`; o uso de qualquer outro banco de dados exige informar a chave pública explicitamente. A URL assume por padrão `https://` seguido do nome do banco de dados.

`GOSUMDB` assume por padrão `sum.golang.org`, o banco de dados de checksums do Go operado pelo Google. Consulte https://sum.golang.org/privacy para a política de privacidade do serviço.

Se `GOSUMDB` for definido como `off`, ou se `go get` for invocado com a flag `-insecure`, o banco de dados de checksums não é consultado, e todos os módulos não reconhecidos são aceitos, ao custo de abrir mão da garantia de segurança de downloads verificados e repetíveis para todos os módulos. Uma forma melhor de ignorar o banco de dados de checksums para módulos específicos é usar as variáveis de ambiente `GOPRIVATE` ou `GONOSUMDB`. Consulte [Módulos privados](#private-modules) para mais detalhes.

O comando `go env -w` pode ser usado para [definir estas variáveis](/pkg/cmd/go/#hdr-Print_Go_environment_information) para as próximas invocações do comando `go`.

## Variáveis de ambiente {#environment-variables}

O comportamento dos módulos no comando `go` pode ser configurado usando as variáveis de ambiente listadas abaixo. Esta lista inclui apenas as variáveis de ambiente relacionadas a módulos. Consulte [`go help environment`](/cmd/go/#hdr-Environment_variables) para uma lista de todas as variáveis de ambiente reconhecidas pelo comando `go`.

<table class="ModTable">
  <thead>
    <tr>
      <th>Variável</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GO111MODULE</code></td>
      <td>
        <p>
          Controla se o comando `go` roda no modo com suporte a módulos ou no modo
          <code>GOPATH</code>. São reconhecidos três valores:
        </p>
        <ul>
          <li>
            <code>off</code>: o comando <code>go</code> ignora arquivos
            <code>go.mod</code> e roda no modo <code>GOPATH</code>.
          </li>
          <li>
            <code>on</code> (ou não definida): o comando <code>go</code> roda no
            modo com suporte a módulos, mesmo quando não há arquivo
            <code>go.mod</code> presente.
          </li>
          <li>
            <code>auto</code>: o comando <code>go</code> roda no modo com suporte
            a módulos se houver um arquivo <code>go.mod</code> no diretório atual
            ou em qualquer diretório pai. No Go 1.15 e versões anteriores, este
            era o padrão.
          </li>
        </ul>
        <p>
          Consulte <a href="#mod-commands">Comandos com suporte a módulos</a> para
          mais informações.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOMODCACHE</code></td>
      <td>
        <p>
          O diretório onde o comando <code>go</code> armazenará os módulos baixados
          e arquivos relacionados. Consulte <a href="#module-cache">Cache de
          módulos</a> para detalhes sobre a estrutura desse diretório.
        </p>
        <p>
          Se <code>GOMODCACHE</code> não estiver definida, assume por padrão
          <code>$GOPATH/pkg/mod</code>.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOINSECURE</code></td>
      <td>
        <p>
          Lista separada por vírgulas de padrões glob (na sintaxe de
          <a href="/pkg/path/#Match"><code>path.Match</code></a> do Go) de prefixos
          de caminho de módulos que podem sempre ser baixados de forma insegura.
          Aplica-se apenas a dependências que estão sendo baixadas diretamente.
        </p>
        <p>
          Diferentemente da flag <code>-insecure</code> de <code>go get</code>,
          <code>GOINSECURE</code> não desabilita a validação de checksums pelo
          banco de dados de checksums de módulos. <code>GOPRIVATE</code> ou
          <code>GONOSUMDB</code> podem ser usadas para isso.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GONOPROXY</code></td>
      <td>
        <p>
          Lista separada por vírgulas de padrões glob (na sintaxe de
          <a href="/pkg/path/#Match"><code>path.Match</code></a> do Go) de prefixos
          de caminho de módulos que devem sempre ser buscados diretamente de
          repositórios de controle de versão, e não de proxies de módulos.
        </p>
        <p>
          Se <code>GONOPROXY</code> não estiver definida, assume por padrão o valor
          de <code>GOPRIVATE</code>. Consulte
          <a href="#private-module-privacy">Privacidade</a>.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GONOSUMDB</code></td>
      <td>
        <p>
          Lista separada por vírgulas de padrões glob (na sintaxe de
          <a href="/pkg/path/#Match"><code>path.Match</code></a> do Go) de prefixos
          de caminho de módulos para os quais o <code>go</code> não deve verificar
          checksums usando o banco de dados de checksums.
        </p>
        <p>
          Se <code>GONOSUMDB</code> não estiver definida, assume por padrão o valor
          de <code>GOPRIVATE</code>. Consulte
          <a href="#private-module-privacy">Privacidade</a>.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOPATH</code></td>
      <td>
        <p>
          No modo <code>GOPATH</code>, a variável <code>GOPATH</code> é uma lista
          de diretórios que podem conter código Go.
        </p>
        <p>
          No modo com suporte a módulos, o [cache de módulos](#glos-module-cache)
          é armazenado no subdiretório <code>pkg/mod</code> do primeiro diretório
          de <code>GOPATH</code>. O código-fonte dos módulos fora do cache pode ser
          armazenado em qualquer diretório.
        </p>
        <p>
          Se <code>GOPATH</code> não estiver definida, assume por padrão o
          subdiretório <code>go</code> do diretório pessoal do usuário.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOPRIVATE</code></td>
      <td>
        Lista separada por vírgulas de padrões glob (na sintaxe de
        <a href="/pkg/path/#Match"><code>path.Match</code></a> do Go) de prefixos
        de caminho de módulos que devem ser considerados privados.
        <code>GOPRIVATE</code> é um valor padrão para <code>GONOPROXY</code> e
        <code>GONOSUMDB</code>. Consulte
        <a href="#private-module-privacy">Privacidade</a>. <code>GOPRIVATE</code>
        também determina se um módulo é considerado privado para
        <code>GOVCS</code>.
      </td>
    </tr>
    <tr>
      <td><code>GOPROXY</code></td>
      <td>
        <p>
          Lista de URLs de proxies de módulos, separadas por vírgulas (<code>,</code>)
          ou barras verticais (<code>|</code>). Quando o comando <code>go</code>
          busca informações sobre um módulo, ele contata cada proxy da lista em
          sequência, até receber uma resposta bem-sucedida ou um erro terminal.
          Um proxy pode responder com status 404 (Not Found) ou 410 (Gone) para
          indicar que o módulo não está disponível naquele servidor.
        </p>
        <p>
          O comportamento de fallback do comando <code>go</code> em caso de erro é
          determinado pelos caracteres separadores entre as URLs. Se uma URL de
          proxy for seguida por vírgula, o comando <code>go</code> passa para a
          próxima URL após um erro 404 ou 410; todos os outros erros são
          considerados terminais. Se a URL do proxy for seguida por barra vertical,
          o comando <code>go</code> passa para a próxima fonte após qualquer erro,
          incluindo erros não HTTP, como timeouts.
        </p>
        <p>
          As URLs de <code>GOPROXY</code> podem usar os esquemas <code>https</code>,
          <code>http</code> ou <code>file</code>. Se uma URL não tiver esquema,
          assume-se <code>https</code>. Um cache de módulos pode ser usado
          diretamente como um proxy de arquivos:
        </p>
        <pre>GOPROXY=file://$(go env GOMODCACHE)/cache/download</pre>
        <p>Duas palavras-chave podem ser usadas no lugar de URLs de proxy:</p>
        <ul>
          <li>
            <code>off</code>: não permite baixar módulos de nenhuma fonte.
          </li>
          <li>
            <code>direct</code>: baixa diretamente dos repositórios de controle de
            versão, em vez de usar um proxy de módulos.
          </li>
        </ul>
        <p>
          <code>GOPROXY</code> assume por padrão
          <code>https://proxy.golang.org,direct</code>. Com essa configuração, o
          comando <code>go</code> primeiro contata o espelho de módulos do Go
          operado pelo Google e, em seguida, recorre a uma conexão direta caso o
          espelho não tenha o módulo. Consulte
          <a href="https://proxy.golang.org/privacy">https://proxy.golang.org/privacy</a>
          para a política de privacidade do espelho. As variáveis de ambiente
          <code>GOPRIVATE</code> e <code>GONOPROXY</code> podem ser definidas para
          impedir que módulos específicos sejam baixados usando proxies. Consulte
          <a href="#private-module-privacy">Privacidade</a> para informações sobre
          a configuração de proxies privados.
        </p>
        <p>
          Consulte <a href="#module-proxy">Proxies de módulos</a> e
          <a href="#resolve-pkg-mod">Resolvendo um pacote para um módulo</a> para
          mais informações sobre como os proxies são usados.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOSUMDB</code></td>
      <td>
        <p>
          Identifica o nome do banco de dados de checksums a ser usado e,
          opcionalmente, sua chave pública e URL. Por exemplo:
        </p>
        <pre>
GOSUMDB="sum.golang.org"
GOSUMDB="sum.golang.org+&lt;publickey&gt;"
GOSUMDB="sum.golang.org+&lt;publickey&gt; https://sum.golang.org"
</pre>
        <p>
          O comando <code>go</code> conhece a chave pública de
          <code>sum.golang.org</code> e também sabe que o nome
          <code>sum.golang.google.cn</code> (disponível na China continental)
          se conecta ao banco de dados <code>sum.golang.org</code>; o uso de
          qualquer outro banco de dados exige informar a chave pública
          explicitamente. A URL assume por padrão <code>https://</code> seguido
          do nome do banco de dados.
        </p>
        <p>
          <code>GOSUMDB</code> assume por padrão <code>sum.golang.org</code>, o
          banco de dados de checksums do Go operado pelo Google. Consulte
          <a href="https://sum.golang.org/privacy">https://sum.golang.org/privacy</a>
          para a política de privacidade do serviço.
        <p>
        <p>
          Se <code>GOSUMDB</code> for definido como <code>off</code> ou se
          <code>go get</code> for invocado com a flag <code>-insecure</code>,
          o banco de dados de checksums não é consultado, e todos os módulos não
          reconhecidos são aceitos, ao custo de abrir mão da garantia de segurança
          de downloads verificados e repetíveis para todos os módulos. Uma forma
          melhor de ignorar o banco de dados de checksums para módulos específicos
          é usar as variáveis de ambiente <code>GOPRIVATE</code> ou
          <code>GONOSUMDB</code>.
        </p>
        <p>
          Consulte <a href="#authenticating">Autenticando módulos</a> e
          <a href="#private-module-privacy">Privacidade</a> para mais informações.
        </p>
      </td>
    </tr>
    <tr>
      <td><code>GOVCS</code></td>
      <td>
        <p>
          Controla o conjunto de ferramentas de controle de versão que o comando
          <code>go</code> pode usar para baixar módulos públicos e privados
          (definidos por seus caminhos corresponderem a um padrão em
          <code>GOPRIVATE</code>) ou outros módulos que correspondam a um padrão glob.
        </p>
        <p>
          Se <code>GOVCS</code> não estiver definida, ou se um módulo não
          corresponder a nenhum padrão em <code>GOVCS</code>, o comando
          <code>go</code> pode usar <code>git</code> e <code>hg</code> para um
          módulo público, ou qualquer ferramenta de controle de versão conhecida
          para um módulo privado. Na prática, o comando <code>go</code> age como
          se <code>GOVCS</code> estivesse definida como:
        </p>
        <pre>public:git|hg,private:all</pre>
        <p>
          Consulte <a href="#vcs-govcs">Controlando ferramentas de controle de
          versão com <code>GOVCS</code></a> para uma explicação completa.
        </p>
      </td>
    </tr>
     <tr>
      <td><code>GOWORK</code></td>
      <td>
       <p>
        A variável de ambiente `GOWORK` instrui o comando `go` a entrar no modo
        workspace usando o [arquivo `go.work`](#go-work-file) fornecido para definir
        o workspace. Se `GOWORK` for definida como `off`, o modo workspace é
        desabilitado. Isso pode ser usado para rodar o comando `go` no modo de
        módulo único: por exemplo, `GOWORK=off go build .` compila o pacote `.`
        no modo de módulo único. Se `GOWORK` estiver vazia, o comando `go` vai
        procurar um arquivo `go.work`, conforme descrito na seção
        [Workspaces](#workspaces).
       </p>
      </td>
    </tr>
  </tbody>
</table>

## Glossário {#glossary}

<a id="glos-build-constraint"></a>
**build constraint:** Uma condição que determina se um arquivo-fonte Go é
usado ao compilar um pacote. Restrições de build (build constraints) podem ser expressas com sufixos no nome do arquivo (por exemplo, `foo_linux_amd64.go`) ou com comentários de restrição de build (por exemplo, `// +build linux,amd64`). Veja [Restrições de Build](/pkg/go/build/#hdr-Build_Constraints).

<a id="glos-build-list"></a>
**build list:** A lista de versões de módulos que será usada em um comando de build
como `go build`, `go list` ou `go test`. A build list é
determinada a partir do [`go.mod` do módulo principal](#glos-main-module) ([arquivo `go.mod`](#glos-go-mod-file)) e dos arquivos `go.mod` de módulos requeridos transitivamente
usando [seleção de versão mínima](#glos-minimal-version-selection). A build list contém versões para todos os módulos no [grafo de módulos](#glos-module-graph), não apenas aqueles relevantes para um comando específico.

<a id="glos-canonical-version"></a>
**canonical version:** Uma [versão](#glos-version) formatada corretamente, sem
nenhum sufixo de metadados de build além de `+incompatible`. Por exemplo, `v1.2.3`
é uma versão canônica, mas `v1.2.3+meta` não é.

<a id="glos-current-module"></a>
**current module:** Sinônimo de [módulo principal](#glos-main-module).

<a id="glos-deprecated-module"></a>
**deprecated module:** Um módulo que não é mais suportado por seus autores
(embora versões principais sejam consideradas módulos distintos para este fim).
Um módulo obsoleto é marcado com um [comentário de obsolescência](#go-mod-file-module-deprecation)
na versão mais recente do seu [arquivo `go.mod`](#glos-go-mod-file).

<a id="glos-direct-dependency"></a>
**direct dependency:** Um pacote cujo caminho aparece em uma [declaração `import`](/ref/spec#import_declarations) em um arquivo-fonte `.go` de um pacote
ou teste no [módulo principal](#glos-main-module), ou no módulo que contém tal
pacote. (Compare com [dependência indireta](#glos-indirect-dependency).)

<a id="glos-direct-mode"></a>
**direct mode:** Uma configuração de [variáveis de ambiente](#environment-variables)
que faz o comando `go` baixar um módulo diretamente de um [sistema de controle de versão](#vcs), em vez de um [proxy de módulos](#glos-module-proxy).
`GOPROXY=direct` faz isso para todos os módulos. `GOPRIVATE` e `GONOPROXY` fazem isso
para módulos que correspondem a uma lista de padrões.

<a id="glos-go-mod-file"></a>
**`go.mod` file:** O arquivo que define o caminho, os requisitos e
outros metadados de um módulo. Fica no [diretório raiz do
módulo](#glos-module-root-directory). Veja a seção sobre [arquivos `go.mod`](#go-mod-file).

<a id="glos-go-work-file"></a>
**`go.work` file** O arquivo que define o conjunto de módulos a serem
usados em um [workspace](#workspaces). Veja a seção sobre
[arquivos `go.work`](#go-work-file)

<a id="glos-import-path"></a>
**import path:** Uma string usada para importar um pacote em um arquivo-fonte Go.
Sinônimo de [caminho do pacote](#glos-package-path).

<a id="glos-indirect-dependency"></a>
**indirect dependency:** Um pacote importado transitivamente por um pacote ou teste no
[módulo principal](#glos-main-module), mas cujo caminho não aparece em nenhuma
[declaração `import`](/ref/spec#import_declarations) no módulo principal;
ou um módulo que aparece no [grafo de módulos](#glos-module-graph), mas que não
fornece nenhum pacote importado diretamente pelo módulo principal.
(Compare com [dependência direta](#glos-direct-dependency).)

<a id="glos-lazy-module-loading"></a>
**lazy module loading:** Uma mudança no Go 1.17 que evita carregar o [grafo de
módulos](#glos-module-graph) para comandos que não precisam dele, em módulos que
especificam `go 1.17` ou superior. Veja [Carregamento preguiçoso de módulos](#lazy-loading).

<a id="glos-main-module"></a>
**main module:** O módulo no qual o comando `go` é invocado. O módulo
principal é definido por um [arquivo `go.mod`](#glos-go-mod-file) no diretório atual
ou em um diretório pai. Veja [Módulos, pacotes e
versões](#modules-overview).

<a id="glos-major-version"></a>
**major version:** O primeiro número em uma versão semântica (`1` em `v1.2.3`). Em
um lançamento com mudanças incompatíveis, a versão principal deve ser incrementada, e
as versões secundária e de correção devem ser definidas como 0. Versões semânticas com versão principal 0 são consideradas instáveis.

<a id="glos-major-version-subdirectory"></a>
**major version subdirectory:** Um subdiretório dentro de um repositório de controle de versão
que corresponde ao [sufixo de versão principal](#glos-major-version-suffix) de um módulo, onde o módulo pode ser definido. Por exemplo,
o módulo `example.com/mod/v2` no repositório com [caminho raiz](#glos-repository-root-path) `example.com/mod` pode ser definido no
diretório raiz do repositório ou no subdiretório de versão principal `v2`. Veja [Diretórios de módulos dentro de um repositório](#vcs-dir).

<a id="glos-major-version-suffix"></a>
**major version suffix:** Um sufixo do caminho do módulo que corresponde ao
número da versão principal. Por exemplo, `/v2` em `example.com/mod/v2`. Sufixos de versão principal
são obrigatórios a partir de `v2.0.0` e não são permitidos em versões anteriores. Veja
a seção sobre [Sufixos de versão principal](#major-version-suffixes).

<a id="glos-minimal-version-selection"></a>
**minimal version selection (MVS):** O algoritmo usado para determinar as
versões de todos os módulos que serão usados em um build. Veja a seção sobre
[Seleção de versão mínima](#minimal-version-selection) para detalhes.

<a id="glos-minor-version"></a>
**minor version:** O segundo número em uma versão semântica (`2` em `v1.2.3`). Em
um lançamento com nova funcionalidade compatível com versões anteriores, a versão secundária deve ser
incrementada, e a versão de correção deve ser definida como 0.

<a id="glos-module"></a>
**module:** Uma coleção de pacotes que são lançados, versionados e
distribuídos juntos.

<a id="glos-module-cache"></a>
**module cache:** Um diretório local que armazena módulos baixados, localizado em
`GOPATH/pkg/mod`. Veja [Cache de módulos](#module-cache).

<a id="glos-module-graph"></a>
**module graph:** O grafo direcionado dos requisitos de módulos, com raiz no [módulo
principal](#glos-main-module). Cada vértice do grafo é um módulo; cada aresta é uma
versão de uma declaração `require` em um arquivo `go.mod` (sujeita às declarações `replace` e
`exclude` no arquivo `go.mod` do módulo principal).

<a id="glos-module-graph-pruning"></a>
**module graph pruning:** Uma mudança no Go 1.17 que reduz o tamanho do
grafo de módulos ao omitir as dependências transitivas de módulos que especificam `go
1.17` ou superior. Veja [Poda do grafo de módulos](#graph-pruning).

<a id="glos-module-path"></a>
**module path:** Um caminho que identifica um módulo e atua como prefixo para
os caminhos de importação dos pacotes dentro do módulo. Por exemplo, `"golang.org/x/net"`.

<a id="glos-module-proxy"></a>
**module proxy:** Um servidor web que implementa o [protocolo `GOPROXY`](#goproxy-protocol). O comando `go` baixa informações de versão,
arquivos `go.mod` e arquivos zip de módulos a partir de proxies de módulos.

<a id="glos-module-root-directory"></a>
**module root directory:** O diretório que contém o arquivo `go.mod` que
define um módulo.

<a id="glos-module-subdirectory"></a>
**module subdirectory:** A parte de um [caminho do módulo](#glos-module-path) após
o [caminho raiz do repositório](#glos-repository-root-path) que indica o
subdiretório onde o módulo é definido. Quando não vazio, o subdiretório do módulo também é um prefixo para as [tags de versão semântica](#glos-semantic-version-tag). O subdiretório do módulo não inclui o
[sufixo de versão principal](#glos-major-version-suffix), se houver um, mesmo que o
módulo esteja em um [subdiretório de versão principal](#glos-major-version-subdirectory).
Veja [Caminhos de módulos](#module-path).

<a id="glos-package"></a>
**package:** Uma coleção de arquivos-fonte no mesmo diretório que são
compilados juntos. Veja a [seção Packages](/ref/spec#Packages) na
Especificação da Linguagem Go.

<a id="glos-package-path"></a>
**package path:** O caminho que identifica de forma única um pacote. Um caminho de pacote é
um [caminho do módulo](#glos-module-path) seguido de um subdiretório dentro do módulo.
Por exemplo, `"golang.org/x/net/html"` é o caminho do pacote para o pacote no
módulo `"golang.org/x/net"` no subdiretório `"html"`. Sinônimo de
[caminho de importação](#glos-import-path).

<a id="glos-patch-version"></a>
**patch version:** O terceiro número em uma versão semântica (`3` em `v1.2.3`). Em
um lançamento sem mudanças na interface pública do módulo, a versão de correção
deve ser incrementada.

<a id="glos-pre-release-version"></a>
**pre-release version:** Uma versão com um hífen seguido de uma série de
identificadores separados por ponto, imediatamente após a versão de correção, por exemplo,
`v1.2.3-beta4`. Versões de pré-lançamento são consideradas instáveis e não são
presumidas como compatíveis com outras versões. Uma versão de pré-lançamento vem antes
da versão de lançamento correspondente: `v1.2.3-pre` vem antes de `v1.2.3`. Veja também
[versão de lançamento](#glos-release-version).

<a id="glos-pseudo-version"></a>
**pseudo-version:** Uma versão que codifica um identificador de revisão (como um hash de commit do Git)
e um carimbo de data/hora de um sistema de controle de versão. Por exemplo,
`v0.0.0-20191109021931-daa7c04131f5`. Usada para [compatibilidade com repositórios que não são módulos](#non-module-compat) e em outras situações em que uma
versão marcada não está disponível.

<a id="glos-release-version"></a>
**release version:** Uma versão sem sufixo de pré-lançamento. Por exemplo,
`v1.2.3`, e não `v1.2.3-pre`. Veja também [versão de
pré-lançamento](#glos-pre-release-version).

<a id="glos-repository-root-path"></a>
**repository root path:** A parte de um [caminho do módulo](#glos-module-path) que
corresponde ao diretório raiz de um repositório de controle de versão. Veja [Caminhos de
módulos](#module-path).

<a id="glos-retracted-version"></a>
**retracted version:** Uma versão que não deve ser utilizada como dependência, seja
porque foi publicada prematuramente, seja porque um problema grave foi descoberto
após a publicação. Veja a [diretiva `retract`](#go-mod-file-retract).

<a id="glos-semantic-version-tag"></a>
**semantic version tag:** Uma tag em um repositório de controle de versão que associa uma
[versão](#glos-version) a uma revisão específica. Veja [Mapeamento de versões para
commits](#vcs-version).

<a id="glos-selected-version"></a>
**selected version:** A versão de um determinado módulo escolhida pela [seleção de versão
mínima](#minimal-version-selection). A versão selecionada é a maior
versão para o caminho do módulo encontrada no [grafo de módulos](#glos-module-graph).

<a id="glos-vendor-directory"></a>
**vendor directory:** Um diretório chamado `vendor` que contém pacotes de
outros módulos necessários para compilar os pacotes do módulo principal. Mantido com
[`go mod vendor`](#go-mod-vendor). Veja [Vendoring](#vendoring).

<a id="glos-version"></a>
**version:** Um identificador de um snapshot imutável de um módulo, escrito como a
letra `v` seguida de uma versão semântica. Veja a seção sobre
[Versões](#versions).

<a id="glos-workspace"></a>
**workspace:** Uma coleção de módulos no disco que são usados como
módulos principais ao executar a [seleção de versão mínima (MVS)](#minimal-version-selection).
Veja a seção sobre [Workspaces](#workspaces)

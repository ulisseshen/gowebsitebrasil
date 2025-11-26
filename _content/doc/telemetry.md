---
ia-translated: true
title: "Go Telemetry"
layout: article
breadcrumb: true
date: 2024-02-07:00:00Z
---

<style>
.DocInfo {
  background-color: var(--color-background-info);
  padding: 1.5rem 2rem 1.5rem 4rem;
  border-left: 0.875rem solid var(--color-border);
  position: relative;
}
.DocInfo:before {
  content: "ⓘ";
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 2rem;
}
</style>

Índice:

 [Contexto](#background)\
 [Visão Geral](#overview)\
 [Configuração](#config)\
 [Counters](#counters)\
 [Reporting e Uploading](#reports)\
 [Charts](#charts) \
 [Telemetry Proposals](#proposals)\
 [IDE Prompting](#ide) \
 [Perguntas Frequentes](#faq)

## Contexto {#background}

Go telemetry é uma forma de programas da toolchain Go coletarem dados sobre seu
desempenho e uso. Aqui "Go toolchain" significa ferramentas de desenvolvedor mantidas
pelo time Go, incluindo o comando `go` e ferramentas suplementares como o
servidor de linguagem Go [`gopls`] ou ferramenta de segurança Go [`govulncheck`]. Go telemetry é
destinado apenas para uso em programas mantidos pelo time Go e suas dependências selecionadas
como [Delve].

Por padrão, dados de telemetria são mantidos apenas no computador local, mas usuários podem
optar por fazer upload de um subconjunto aprovado de dados de telemetria para [telemetry.go.dev].
Dados enviados ajudam o time Go a melhorar a linguagem Go e suas ferramentas,
ajudando-nos a entender uso e problemas.

A palavra "telemetria" adquiriu conotações negativas no mundo de software
open source, em muitos casos merecidamente. No entanto, medir a experiência do usuário
é um elemento importante da engenharia de software moderna, e fontes de dados como
issues do GitHub ou pesquisas anuais são indicadores grosseiros e atrasados,
insuficientes para os tipos de perguntas que o time Go precisa ser capaz de responder.
Go telemetry é projetada para ajudar programas na toolchain a coletar dados úteis
sobre sua confiabilidade, desempenho e uso, mantendo a
transparência e privacidade que usuários esperam do projeto Go. Para saber mais
sobre o processo de design e motivação para telemetria, por favor veja os
[posts de blog sobre telemetria](https://research.swtch.com/telemetry).
Para saber mais sobre telemetria e privacidade, por favor veja a
[política de privacidade de telemetria](https://telemetry.go.dev/privacy).

Esta página explica como Go telemetry funciona, em alguns detalhes. Para respostas rápidas a
perguntas frequentes, veja o [FAQ](#faq).

<div class="DocInfo">
Usando Go 1.23 ou posterior, para <strong>optar por</strong> fazer upload de dados de telemetria
para o time Go, execute:
<pre>
go telemetry on
</pre>
Para desabilitar completamente a telemetria, incluindo coleta local, execute:
<pre>
go telemetry off
</pre>
Para reverter para o modo padrão de telemetria apenas local, execute:
<pre>
go telemetry local
</pre>
Antes do Go 1.23, isso também pode ser feito com o comando
<code>golang.org/x/telemetry/cmd/gotelemetry</code>. Veja <a
href="#config">Configuração</a> para mais detalhes.
</div>

## Visão Geral {#overview}

Go telemetry usa três tipos de dados principais:

- [_Counters_](#counters) são contagens leves de eventos nomeados, instrumentados
  no programa da toolchain. Se a coleta estiver habilitada (o [mode](#config)
  é **local** ou **on**), counters são escritos em um arquivo mapeado em memória no
  sistema de arquivos local.
- [_Reports_](#reports) são resumos agregados de counters para uma dada semana.
  Se o upload estiver habilitado (o [mode](#config) é **on**), reports para
  [counters aprovados](#proposals) são enviados para [telemetry.go.dev], onde
  eles são publicamente acessíveis.
- [_Charts_](#charts) resumem reports enviados para todos os usuários.
  Charts podem ser visualizados em [telemetry.go.dev].

Todos os dados e configuração de Go telemetry local são armazenados no diretório
<code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code>.
Abaixo, nos referiremos a este diretório como `<gotelemetry>`.

O diagrama abaixo ilustra este fluxo de dados.

<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/dataflow.png" />
  </center>
</div>

No resto deste documento, exploraremos os componentes deste diagrama. Mas
primeiro, vamos aprender mais sobre a configuração que o controla.

## Configuração {#config}

O comportamento de Go telemetry é controlado por um único valor: o
_mode_ de telemetria. Os valores possíveis para `mode` são `local` (o padrão), `on`, ou
`off`:

- Quando `mode` é `local`, dados de telemetria são coletados e armazenados no computador local,
  mas nunca enviados para servidores remotos.
- Quando `mode` é `on`, dados são coletados, e podem ser enviados dependendo de
  [sampling](#uploads).
- Quando `mode` é `off`, dados não são nem coletados nem enviados.

Com Go 1.23 ou posterior, os seguintes comandos interagem com o mode de telemetria:

- `go telemetry`: veja o mode atual.
- `go telemetry on`: defina o mode para `on`.
- `go telemetry off`: defina o mode para `off`.
- `go telemetry local`: defina o mode para `local`.

Informações sobre configuração de telemetria também estão disponíveis via variáveis de
ambiente Go somente leitura:

- `go env GOTELEMETRY` reporta o mode de telemetria.
- `go env GOTELEMETRYDIR` reporta o diretório contendo configuração
  e dados de telemetria.

O comando [`gotelemetry`](/pkg/golang.org/x/telemetry/cmd/gotelemetry) também
pode ser usado para configurar o mode de telemetria, bem como para inspecionar
dados de telemetria local. Use este comando para instalá-lo:

```
go install golang.org/x/telemetry/cmd/gotelemetry@latest
```

Para informações de uso completas da ferramenta de linha de comando `gotelemetry`,
veja sua [documentação do package](/pkg/golang.org/x/telemetry/cmd/gotelemetry).

## Counters {#counters}

Como mencionado acima, Go telemetry é instrumentada via _counters_. Counters vêm
em duas variantes: basic counters e stack counters.

### Basic counters

Um _basic counter_ é um valor incrementável com um nome que descreve o
evento que ele conta. Por exemplo, o counter `gopls/client:vscode` registra
o número de vezes que uma sessão `gopls` é iniciada pelo VS Code. Ao lado deste
counter podemos ter `gopls/client:neovim`, `gopls/client:eglot`, e assim por diante, para
registrar sessões com diferentes editores ou language clients. Se você usou
múltiplos editores durante a semana, você pode registrar os seguintes dados de
counter:

    gopls/client:vscode 8
    gopls/client:neovim 5
    gopls/client:eglot  2

Quando counters são relacionados desta forma, às vezes nos referimos à parte antes
do `:` como _chart name_ (`gopls/client` neste caso), e a parte depois de `:`
como _bucket name_ (`vscode`). Veremos por que isso importa quando discutirmos
[charts](#charts).

Basic counters também podem representar um _histogram_. Por exemplo, o counter {{raw
`<code>gopls/completion/latency:&lt;50ms</code>`}} registra o número
de vezes que um autocompletion leva menos de 50ms.

{{raw `
<pre>
gopls/completion/latency:&lt;10ms
gopls/completion/latency:&lt;50ms
gopls/completion/latency:&lt;100ms
...
</pre>
`}}

Este padrão para registrar dados de histograma é uma convenção: não há nada
especial sobre o bucket name {{raw `<code>&lt;50ms</code>`}}. Esses tipos de
counters são comumente usados para medir desempenho.

### Stack counters

Um _stack counter_ é um counter que também registra a call stack atual do
programa da toolchain Go quando a contagem é incrementada. Por exemplo, o
stack counter `crash/crash` registra a call stack quando um programa da toolchain
trava:

    crash/crash
    golang.org/x/tools/gopls/internal/golang.hoverBuiltin:+22
    golang.org/x/tools/gopls/internal/golang.Hover:+94
    golang.org/x/tools/gopls/internal/server.Hover:+42
    ...

Stack counters tipicamente medem eventos onde invariantes do programa são violados.
O exemplo mais comum disso é um crash, mas outro exemplo é o
stack counter `gopls/bug`, que conta situações incomuns identificadas
antecipadamente pelo programador, como um panic recuperado ou um erro que "não pode
acontecer". Stack counters incluem apenas os nomes e números de linha de funções
dentro de programas da toolchain Go. Eles não incluem nenhuma informação sobre
entradas do usuário, como os nomes ou conteúdos do código fonte de um usuário.

Stack counters podem ajudar a rastrear bugs raros ou complicados que não são reportados
por outros meios. Desde a introdução do counter `gopls/bug`, encontramos
[dezenas de instâncias](https://github.com/golang/go/issues?q=label%3Agopls%2Ftelemetry-wins)
de código "inalcançável" que foi alcançado na prática, e rastrear essas
exceções levou à descoberta (e correção) de muitos bugs visíveis ao usuário que
eram ou não óbvios para o usuário ou muito difíceis de reportar. Especialmente com
testes de pré-lançamento, stack counters podem nos ajudar a melhorar o produto mais
eficientemente do que poderíamos sem automação.

### Arquivos de counter

Todos os dados de counter são escritos no diretório `<gotelemetry>/local`, em
arquivos nomeados de acordo com o seguinte esquema:

```
[program name]@[program version]-[go version]-[GOOS]-[GOARCH]-[date].v1.count
```

- O **program name** é o basename do caminho do package do programa, conforme reportado
  por [debug.BuildInfo].
- A **program version** e **go version** também são reportadas por [debug.BuildInfo].
- Os valores **GOOS** e **GOARCH** são reportados por
  [`runtime.GOOS`](/pkg/runtime#GOOS) e
  [`runtime.GOARCH`](/pkg/runtime#GOARCH).
- A **date** é a data em que o arquivo de counter foi criado, no formato `YYYY-MM-DD`.

Esses arquivos são mapeados em memória em cada instância em execução dos programas
instrumentados. O uso de um arquivo mapeado em memória significa que mesmo se o programa
travar imediatamente, ou várias cópias de ferramentas instrumentadas estiverem rodando
simultaneamente, os counters são registrados com segurança.

## Reporting e uploading {#reports}

Aproximadamente uma vez por semana, dados de counter são agregados em reports nomeados
`<date>.json` no diretório `<gotelemetry>/local`. Esses reports somam todas as
contagens da semana anterior, agrupadas pelos mesmos identificadores de programa usados para
o arquivo de counter (program name, program version, go version, GOOS, e GOARCH).

Reports locais podem ser visualizados como charts com o comando
[`gotelemetry view`](/pkg/golang.org/x/telemetry/cmd/gotelemetry).
Aqui está um exemplo de resumo do counter `gopls/completion/latency`:

<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/gopls-latency.png" />
  </center>
</div>

### Uploading {#uploads}

Se o upload de telemetria estiver habilitado, o processo de reporting semanal também
gerará reports contendo o subconjunto de counters presente na
[upload config](https://telemetry.go.dev/config). Esses counters devem ser
aprovados pelo processo de revisão pública descrito na próxima seção. Após ser
enviado com sucesso, uma cópia dos reports enviados é armazenada no
diretório `<gotelemetry>/upload`.

Assim que usuários suficientes optarem por fazer upload de dados de telemetria, o processo de upload
aleatoriamente pulará o upload para uma fração de reports, para reduzir quantidades de coleta
e aumentar privacidade mantendo significância estatística.

## Charts {#charts}

Além de aceitar uploads, o site [telemetry.go.dev] disponibiliza publicamente
dados enviados. Cada dia, reports enviados são processados em duas
saídas, que estão disponíveis na homepage [telemetry.go.dev].

- Reports _merged_ mesclam counters de todos os uploads recebidos no dia dado.
- _Charts_ plotam dados enviados conforme especificado na [chart config], que foi
  produzida como parte do processo de proposal. Lembre-se da discussão de
  [counters](#counters) que nomes de counter como `foo:bar` são decompostos
  no chart name `foo` e bucket name `bar`. Cada chart agrega
  counters com o mesmo chart name nos buckets correspondentes.

Charts são especificados no formato do package [chartconfig]. Por exemplo,
aqui está a chart config para o chart `gopls/client`.

    title: Editor Distribution
    counter: gopls/client:{vscode,vscodium,vscode-insiders,code-server,eglot,govim,neovim,coc.nvim,sublimetext,other}
    description: measure editor distribution for gopls users.
    type: partition
    issue: https://go.dev/issue/61038
    issue: https://go.dev/issue/62214 # add vscode-insiders
    program: golang.org/x/tools/gopls
    version: v0.13.0 # temporarily back-version to demonstrate config generation.

Esta configuração descreve o chart a ser produzido, enumera o conjunto de
counters a serem agregados, e especifica as versões de programa às quais o
chart se aplica. Adicionalmente, o [processo de proposal](#proposals) requer que
um proposal aceito seja associado ao chart. Aqui está o chart resultante
desta configuração:

<div class="image">
  <center>
    <img src="/doc/telemetry/gopls-clients.png" />
  </center>
</div>

## O processo de telemetry proposal {#proposals}

Mudanças na configuração de upload ou conjunto de charts em [telemetry.go.dev] devem
passar pelo _telemetry proposal process_, que visa garantir
transparência em torno de mudanças na configuração de telemetria.

Notavelmente, não há de fato distinção entre configuração de upload e
configuração de chart neste processo. A configuração de upload é ela mesma expressa
em termos das agregações que queremos renderizar em telemetry.go.dev, baseada
no princípio de que devemos apenas coletar dados que queremos _ver_.

O processo de proposal é o seguinte:

1. O proponente cria uma CL modificando [config.txt] do package [chartconfig]
   para conter as novas agregações de counter desejadas.
2. O proponente registra um [proposal] para mesclar esta CL.
3. Uma vez que a discussão sobre o issue seja resolvida, o proposal é aprovado ou recusado
   por um membro do time Go.
4. Um processo automático regenera a upload config para permitir o upload dos
   counters necessários para o novo chart. Este processo também adicionará regularmente
   novas versões dos programas relevantes à upload config à medida que forem
   lançadas.

Para serem aprovados, novos charts não podem carregar informações sensíveis do usuário,
e adicionalmente devem ser tanto úteis quanto viáveis. Para serem úteis,
charts devem servir a um propósito específico, com resultados acionáveis. Para serem
viáveis, deve ser possível coletar confiabilmente os dados requisitados, e as
medições resultantes devem ser estatisticamente significativas. Para demonstrar
viabilidade, o proponente pode ser solicitado a instrumentar o programa alvo com
counters e coletá-los localmente primeiro.

O conjunto completo de tais proposals está disponível no
[projeto de proposal](https://github.com/orgs/golang/projects/29) no GitHub.

## IDE Prompting {#ide}

Para que a telemetria responda aos tipos de perguntas que queremos fazer dela, o conjunto de
usuários optando por fazer upload não precisa ser grande--aproximadamente 16.000
participantes permitiriam medições estatisticamente significativas no
nível desejado de granularidade. No entanto, ainda há um custo para reunir esta
amostra saudável: precisamos perguntar a um grande número de desenvolvedores Go se eles querem
optar.

Além disso, mesmo se um grande número de usuários escolher optar _agora_ (talvez
após ler um post de blog do Go), esses usuários podem estar enviesados para desenvolvedores Go
experientes, e ao longo do tempo essa amostra inicial crescerá ainda mais enviesada.
Também, à medida que pessoas trocam seus computadores, elas devem ativamente escolher optar
novamente. Na série de posts de blog sobre telemetria, isso é referido como o
["campaign cost"](https://research.swtch.com/telemetry-opt-in#campaign) do
modelo opt-in.

Para ajudar a manter a amostra de usuários participantes fresca, o servidor de linguagem Go
[`gopls`] suporta um prompt que pede aos usuários para optar pela Go telemetry.
Veja como isso aparece no VS Code:

<div class="image">
  <center>
    <img width="600px" src="/doc/telemetry/prompt.png" />
  </center>
</div>

Se os usuários escolherem "Yes", seu [mode](#config) de telemetria será definido para `on`,
assim como se tivessem executado
[`gotelemetry on`](/pkg/golang.org/x/telemetry/cmd/gotelemetry). Desta forma,
optar é tão fácil quanto possível, e podemos continuamente alcançar uma amostra grande e
estratificada de desenvolvedores Go.

## Perguntas Frequentes {#faq}

**Q: Como habilito ou desabilito Go telemetry?**

A: Use o comando `gotelemetry`, que pode ser instalado com `go install
golang.org/x/telemetry/cmd/gotelemetry@latest`. Execute `gotelemetry off` para
desabilitar tudo, até mesmo coleta local. Execute `gotelemetry on` para habilitar
tudo, incluindo upload de counters aprovados para [telemetry.go.dev]. Veja
a seção [Configuração](#config) para mais informações.

**Q: Onde os dados locais são armazenados?**

A: No diretório <code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code>.

**Q: Com que frequência os dados são enviados, se eu optar?**

A: Aproximadamente uma vez por semana.

**Q: Quais dados são enviados, se eu optar?**

A: Apenas counters que estão listados na
[upload config](https://telemetry.go.dev/config) podem ser enviados.
Isso é gerado a partir da [chart config], que pode ser mais legível.

**Q: Como counters são adicionados à upload config?**

A: Através do [processo de proposal pública](#proposals).

**Q: Onde posso ver dados de telemetria que foram enviados?**

A: Dados enviados estão disponíveis como charts ou resumos mesclados em [telemetry.go.dev].

**Q: Onde está o código fonte para Go telemetry?**

A: Em [golang.org/x/telemetry](/pkg/golang.org/x/telemetry).

[`gopls`]: /pkg/golang.org/x/tools/gopls
[`govulncheck`]: /pkg/golang.org/x/vuln/cmd/govulncheck
[Delve]: /pkg/github.com/go-delve/delve#section-readme
[debug.BuildInfo]: /pkg/runtime/debug#BuildInfo
[proposal]: /issue/new?assignees=&labels=Telemetry-Proposal&projects=golang%2F29&template=12-telemetry.yml&title=x%2Ftelemetry%2Fconfig%3A+proposal+title
[telemetry.go.dev]: https://telemetry.go.dev
[chartconfig]: /pkg/golang.org/x/telemetry/internal/chartconfig
[config.txt]: https://go.googlesource.com/telemetry/+/refs/heads/master/internal/chartconfig/config.txt
[chart config]: https://go.googlesource.com/telemetry/+/refs/heads/master/internal/chartconfig/config.txt

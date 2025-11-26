---
title: Go Fuzzing
layout: article
breadcrumb: true
ia-translated: true
---

O Go suporta fuzzing em sua toolchain padrão a partir do Go 1.18. Testes de fuzz nativos do Go são
[suportados pelo OSS-Fuzz](https://google.github.io/oss-fuzz/getting-started/new-project-guide/go-lang/#native-go-fuzzing-support).


**Experimente o [tutorial de fuzzing com Go](/doc/tutorial/fuzz).**

## Visão Geral

Fuzzing é um tipo de teste automatizado que continuamente manipula entradas para
um programa para encontrar bugs. O fuzzing do Go usa orientação de cobertura para percorrer
inteligentemente o código sendo fuzzed para encontrar e reportar falhas ao usuário. Como ele
pode alcançar casos extremos que humanos frequentemente perdem, testes de fuzz podem ser particularmente
valiosos para encontrar explorações e vulnerabilidades de segurança.

Abaixo está um exemplo de um [teste de fuzz](#glos-fuzz-test), destacando seus principais
componentes.

<img class="DarkMode-img" alt="Código de exemplo mostrando o teste de fuzz geral, com um fuzz target dentro
dele. Antes do fuzz target está uma adição de corpus com f.Add, e os parâmetros
do fuzz target são destacados como os argumentos de fuzzing."
src="/security/fuzz/example-dark.png" style="width: 600px; height:
auto;"/>
<img alt="Código de exemplo mostrando o teste de fuzz geral, com um fuzz target dentro
dele. Antes do fuzz target está uma adição de corpus com f.Add, e os parâmetros
do fuzz target são destacados como os argumentos de fuzzing."
src="/security/fuzz/example.png" style="width: 600px; height:
auto;" class="LightMode-img"/>

## Escrevendo testes de fuzz

### Requisitos

Abaixo estão regras que os testes de fuzz devem seguir.

- Um teste de fuzz deve ser uma função chamada como `FuzzXxx`, que aceita apenas um
  `*testing.F`, e não tem valor de retorno.
- Testes de fuzz devem estar em arquivos \*\_test.go para executar.
- Um [fuzz target](#glos-fuzz-target) deve ser uma chamada de método para
  <code>[(\*testing.F).Fuzz](https://pkg.go.dev/testing#F.Fuzz)</code> que
  aceita um `*testing.T` como o primeiro parâmetro, seguido pelos argumentos
  de fuzzing. Não há valor de retorno.
- Deve haver exatamente um fuzz target por teste de fuzz.
- Todas as entradas do [seed corpus](#glos-seed-corpus) devem ter tipos que são
  idênticos aos [argumentos de fuzzing](#glos-fuzzing-arguments), na mesma ordem.
  Isso é verdadeiro para chamadas a
  <code>[(\*testing.F).Add](https://pkg.go.dev/testing#F.Add)</code> e quaisquer
  arquivos de corpus no diretório testdata/fuzz do teste de fuzz.
- Os argumentos de fuzzing podem ser apenas dos seguintes tipos:
  - `string`, `[]byte`
  - `int`, `int8`, `int16`, `int32`/`rune`, `int64`
  - `uint`, `uint8`/`byte`, `uint16`, `uint32`, `uint64`
  - `float32`, `float64`
  - `bool`

### Sugestões {#suggestions}

Abaixo estão sugestões que irão ajudá-lo a tirar o máximo proveito do fuzzing.

- Fuzz targets devem ser rápidos e determinísticos para que o motor de fuzzing possa trabalhar
  eficientemente, e novas falhas e cobertura de código possam ser facilmente reproduzidas.
- Como o fuzz target é invocado em paralelo através de múltiplos workers e em
  ordem não determinística, o estado de um fuzz target não deve persistir além do
  final de cada chamada, e o comportamento de um fuzz target não deve depender de
  estado global.

## Executando testes de fuzz

Existem dois modos de executar seu teste de fuzz: como um teste unitário (padrão `go test`), ou
com fuzzing (`go test -fuzz=FuzzTestName`).

Testes de fuzz são executados como um teste unitário por padrão. Cada entrada do [seed corpus
](#glos-seed-corpus) será testada contra o fuzz target, reportando quaisquer
falhas antes de sair.

Para habilitar fuzzing, execute `go test` com a flag `-fuzz`, fornecendo uma regex
que corresponda a um único teste de fuzz. Por padrão, todos os outros testes nesse package serão
executados antes do fuzzing começar. Isso é para garantir que o fuzzing não reportará nenhum
problema que já seria capturado por um teste existente.

Note que é você quem decide quanto tempo executar o fuzzing. É muito possível
que uma execução de fuzzing possa rodar indefinidamente se não encontrar nenhum erro.
Haverá suporte para executar esses testes de fuzz continuamente usando ferramentas como OSS-Fuzz
no futuro, veja [Issue #50192](/issue/50192).

**Nota:** Fuzzing deve ser executado em uma plataforma que suporte instrumentação
de cobertura (atualmente AMD64 e ARM64) para que o corpus possa crescer significativamente
enquanto executa, e mais código possa ser coberto durante o fuzzing.

### Saída da linha de comando

Enquanto o fuzzing está em progresso, o [motor de fuzzing](#glos-fuzzing-engine)
gera novas entradas e as executa contra o fuzz target fornecido. Por padrão,
ele continua a executar até que uma [entrada com falha](#glos-failing-input) seja encontrada, ou
o usuário cancele o processo (por exemplo, com Ctrl^C).

A saída será algo assim:

```
~ go test -fuzz FuzzFoo
fuzz: elapsed: 0s, gathering baseline coverage: 0/192 completed
fuzz: elapsed: 0s, gathering baseline coverage: 192/192 completed, now fuzzing with 8 workers
fuzz: elapsed: 3s, execs: 325017 (108336/sec), new interesting: 11 (total: 202)
fuzz: elapsed: 6s, execs: 680218 (118402/sec), new interesting: 12 (total: 203)
fuzz: elapsed: 9s, execs: 1039901 (119895/sec), new interesting: 19 (total: 210)
fuzz: elapsed: 12s, execs: 1386684 (115594/sec), new interesting: 21 (total: 212)
PASS
ok      foo 12.692s
```

As primeiras linhas indicam que a "cobertura baseline" é coletada antes
do fuzzing começar.

Para coletar a cobertura baseline, o motor de fuzzing executa tanto o [seed
corpus](#glos-seed-corpus) quanto o [corpus gerado](#glos-generated-corpus), para
garantir que nenhum erro ocorreu e entender a cobertura de código que o corpus
existente já fornece.

As linhas seguintes fornecem insights sobre a execução ativa de fuzzing:

  - elapsed: a quantidade de tempo que decorreu desde que o processo começou
  - execs: o número total de entradas que foram executadas contra o fuzz target
    (com uma média de execs/sec desde a última linha de log)
  - new interesting: o número total de entradas "interessantes" que foram
    adicionadas ao corpus gerado durante esta execução de fuzzing (com o tamanho
    total do corpus inteiro)

Para uma entrada ser "interessante", ela deve expandir a cobertura de código além do que
o corpus gerado existente pode alcançar. É típico que o número de novas
entradas interessantes cresça rapidamente no início e eventualmente desacelere, com
explosões ocasionais conforme novos branches são descobertos.

Você deve esperar ver o número de "new interesting" diminuir ao longo do tempo conforme as
entradas no corpus começam a cobrir mais linhas do código, com explosões
ocasionais se o motor de fuzzing encontrar um novo caminho de código.

### Entrada com falha

Uma falha pode ocorrer durante fuzzing por vários motivos:

  - Um panic ocorreu no código ou no teste.
  - O fuzz target chamou `t.Fail`, diretamente ou através de métodos como
  `t.Error` ou `t.Fatal`.
  - Um erro não recuperável ocorreu, como um `os.Exit` ou estouro de pilha.
  - O fuzz target levou muito tempo para completar. Atualmente, o timeout para uma
  execução de um fuzz target é 1 segundo. Isso pode falhar devido a um deadlock ou
  loop infinito, ou por comportamento intencional no código. Esta é uma razão pela qual
  é [sugerido que seu fuzz target seja rápido](#suggestions).

Se um erro ocorre, o motor de fuzzing tentará minimizar a entrada para o
valor menor possível e mais legível para humanos que ainda produzirá um
erro. Para configurar isso, veja a seção [configurações customizadas](#custom-settings).

Uma vez que a minimização esteja completa, a mensagem de erro será registrada, e a saída
terminará com algo assim:

```
    Failing input written to testdata/fuzz/FuzzFoo/a878c3134fe0404d44eb1e662e5d8d4a24beb05c3d68354903670ff65513ff49
    To re-run:
    go test -run=FuzzFoo/a878c3134fe0404d44eb1e662e5d8d4a24beb05c3d68354903670ff65513ff49
FAIL
exit status 1
FAIL    foo 0.839s
```

O motor de fuzzing escreveu esta [entrada com falha](#glos-failing-input) para o seed
corpus daquele teste de fuzz, e agora será executada por padrão com `go test`,
servindo como um teste de regressão uma vez que o bug tenha sido corrigido.

O próximo passo para você será diagnosticar o problema, corrigir o bug, verificar a
correção re-executando `go test`, e enviar o patch com o novo arquivo testdata
atuando como seu teste de regressão.

### Configurações customizadas {#custom-settings}

As configurações padrão do comando go devem funcionar para a maioria dos casos de uso de fuzzing. Então
tipicamente, uma execução de fuzzing na linha de comando deve parecer assim:

```
$ go test -fuzz={FuzzTestName}
```

No entanto, o comando `go` fornece algumas configurações ao executar fuzzing.
Essas estão documentadas na [documentação do package `cmd/go`](https://pkg.go.dev/cmd/go).

Para destacar algumas:

- `-fuzztime`: o tempo total ou número de iterações que o fuzz target
  será executado antes de sair, padrão indefinidamente.
- `-fuzzminimizetime`: o tempo ou número de iterações que o fuzz target
  será executado durante cada tentativa de minimização, padrão 60seg. Você pode
  desabilitar completamente a minimização definindo `-fuzzminimizetime 0` ao fazer fuzzing.
- `-parallel`: o número de processos de fuzzing executando ao mesmo tempo, padrão
  `$GOMAXPROCS`. Atualmente, definir -cpu durante fuzzing não tem efeito.

## Formato de arquivo de corpus

Arquivos de corpus são codificados em um formato especial. Este é o mesmo formato tanto para o
[seed corpus](#glos-seed-corpus), quanto para o [corpus
gerado](#glos-generated-corpus).

Abaixo está um exemplo de um arquivo de corpus:

```
go test fuzz v1
[]byte("hello\\xbd\\xb2=\\xbc ⌘")
int64(572293)
```

A primeira linha é usada para informar o motor de fuzzing sobre a versão de codificação
do arquivo. Embora nenhuma versão futura do formato de codificação esteja atualmente
planejada, o design deve suportar essa possibilidade.

Cada uma das linhas seguintes são os valores que compõem a entrada de corpus, e
podem ser copiadas diretamente para código Go se desejado.

No exemplo acima, temos um `[]byte` seguido por um `int64`. Esses tipos
devem corresponder aos argumentos de fuzzing exatamente, nessa ordem. Um fuzz target para esses
tipos seria assim:

```
f.Fuzz(func(*testing.T, []byte, int64) {})
```

A maneira mais fácil de especificar seus próprios valores de seed corpus é usar o
método `(*testing.F).Add`. No exemplo acima, isso seria assim:

```
f.Add([]byte("hello\\xbd\\xb2=\\xbc ⌘"), int64(572293))
```

No entanto, você pode ter arquivos binários grandes que prefere não copiar como código
no seu teste, e ao invés disso manter como entradas individuais de seed corpus no
diretório testdata/fuzz/{FuzzTestName}. A
ferramenta [`file2fuzz`](https://pkg.go.dev/golang.org/x/tools/cmd/file2fuzz) em
golang.org/x/tools/cmd/file2fuzz pode ser usada para converter esses arquivos binários em
arquivos de corpus codificados para `[]byte`.

Para usar esta ferramenta:

```
$ go install golang.org/x/tools/cmd/file2fuzz@latest
$ file2fuzz -h
```

## Recursos

- **Tutorial**:
  - Experimente o [tutorial de fuzzing com Go](/doc/tutorial/fuzz) para um mergulho
    profundo nos novos conceitos.
  - Para um tutorial mais curto e introdutório sobre fuzzing com Go, por favor veja [a
    postagem do blog](/blog/fuzz-beta).
- **Documentação**:
  - A documentação do package [`testing`](https://pkg.go.dev//testing#hdr-Fuzzing)
    descreve o tipo `testing.F` que é usado ao escrever testes de fuzz.
  - A documentação do package [`cmd/go`](https://pkg.go.dev/cmd/go) descreve as flags
    associadas ao fuzzing.
- **Detalhes técnicos**:
  - [Rascunho de design](/s/draft-fuzzing-design)
  - [Proposta](/issue/44551)

## Glossário {#glossary}

<a id="glos-corpus-entry"></a>
**corpus entry:** Uma entrada no corpus que pode ser usada durante o fuzzing. Isso
pode ser um arquivo formatado especialmente, ou uma chamada para
<code>[(\*testing.F).Add](https://pkg.go.dev/testing#F.Add)</code>.

<a id="glos-coverage-guidance"></a>
**coverage guidance:** Um método de fuzzing que usa expansões em cobertura
de código para determinar quais entradas de corpus valem a pena manter para uso futuro.

<a id="glos-failing-input"></a>
**failing input:** Uma entrada com falha é uma entrada de corpus que causará um erro
ou panic quando executada contra o [fuzz target](#glos-fuzz-target).

<a id="glos-fuzz-target"></a>
**fuzz target:** A função do teste de fuzz que é executada para entradas de corpus
e valores gerados durante fuzzing. Ela é fornecida ao teste de fuzz passando
a função para
<code>[(\*testing.F).Fuzz](https://pkg.go.dev/testing#F.Fuzz)</code>.

<a id="glos-fuzz-test"></a>
**fuzz test:** Uma função em um arquivo de teste da forma `func FuzzXxx(*testing.F)`
que pode ser usada para fuzzing.

<a id="glos-fuzzing"></a>
**fuzzing:** Um tipo de teste automatizado que continuamente manipula entradas
para um programa para encontrar problemas como bugs ou
[vulnerabilidades](#glos-vulnerability) às quais o código pode ser suscetível.

<a id="glos-fuzzing-arguments"></a>
**fuzzing arguments:** Os tipos que serão passados para o fuzz target, e
mutados pelo [mutador](#glos-mutator).

<a id="glos-fuzzing-engine"></a>
**fuzzing engine:** Uma ferramenta que gerencia fuzzing, incluindo manter o
corpus, invocar o mutador, identificar nova cobertura e reportar falhas.

<a id="glos-generated-corpus"></a>
**generated corpus:** Um corpus que é mantido pelo motor de fuzzing ao longo
do tempo durante fuzzing para acompanhar o progresso. Ele é armazenado em `$GOCACHE`/fuzz.
Essas entradas são usadas apenas durante fuzzing.

<a id="glos-mutator"></a>
**mutator:** Uma ferramenta usada durante fuzzing que manipula aleatoriamente entradas de corpus
antes de passá-las para um fuzz target.

<a id="glos-package"></a>
**package:** Uma coleção de arquivos fonte no mesmo diretório que são
compilados juntos. Veja a [seção Packages](/ref/spec#Packages) na
Especificação da Linguagem Go.

<a id="glos-seed-corpus"></a>
**seed corpus:** Um corpus fornecido pelo usuário para um teste de fuzz que pode ser usado para
guiar o motor de fuzzing. Ele é composto das entradas de corpus fornecidas por chamadas f.Add
dentro do teste de fuzz, e dos arquivos no diretório testdata/fuzz/{FuzzTestName}
dentro do package. Essas entradas são executadas por padrão com `go test`,
fazendo fuzzing ou não.

<a id="glos-test-file"></a>
**test file:** Um arquivo no formato xxx_test.go que pode conter testes,
benchmarks, exemplos e testes de fuzz.

<a id="glos-vulnerability"></a>
**vulnerability:** Uma fraqueza sensível à segurança no código que pode ser explorada
por um atacante.

## Feedback

Se você experimentar algum problema ou tiver uma ideia para uma funcionalidade, por favor [abra um
issue](/issue/new?&labels=fuzz).

Para discussão e feedback geral sobre a funcionalidade, você também pode participar
do [canal #fuzzing](https://gophers.slack.com/archives/CH5KV1AKE) no
Gophers Slack.

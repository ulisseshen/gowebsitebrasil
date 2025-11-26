---
ia-translated: true
title: Suporte de profiling de coverage para integration tests
layout: article
---

Índice:

 [Visão Geral](#overview)\
 [Construindo um binário para profiling de coverage](#building)\
 [Executando um binário instrumentado para coverage](#running)\
 [Trabalhando com arquivos de dados de coverage](#working)\
 [Perguntas Frequentes](#FAQ)\
 [Recursos](#resources)\
 [Glossário](#glossary)


Começando no Go 1.20, Go suporta coleta de profiles de coverage de aplicações e de integration tests, testes maiores e mais complexos para programas Go.

# Visão Geral {#overview}

Go fornece suporte fácil de usar para coletar profiles de coverage no nível de unit tests de package via o comando "`go test -coverprofile=... <pkg_target>`".
Começando com Go 1.20, usuários agora podem coletar profiles de coverage para [integration tests](#glos-integration-test) maiores: testes mais pesados e complexos que executam múltiplas runs de um dado binário de aplicação.

Para unit tests, coletar um profile de coverage e gerar um relatório requer dois passos: uma run de `go test -coverprofile=...`, seguida por uma invocação de `go tool cover {-func,-html}` para gerar um relatório.

Para integration tests, três passos são necessários: um passo de [build](#building), um passo de [run](#running) (que pode envolver múltiplas invocações do binário do passo de build), e finalmente um passo de [reporting](#reporting), conforme descrito abaixo.

# Construindo um binário para profiling de coverage {#building}

Para construir uma aplicação para coletar profiles de coverage, passe a flag `-cover` ao invocar `go build` no seu binário alvo de aplicação. Veja a seção [abaixo](#packageselection) para uma invocação de exemplo de `go build -cover`.
O binário resultante pode então ser executado usando uma configuração de variável de ambiente para capturar profiles de coverage (veja a próxima seção sobre [running](#running)).

## Como packages são selecionados para instrumentação {#packageselection}

Durante uma dada invocação de "`go build -cover`", o comando Go selecionará packages no módulo principal para profiling de coverage; outros packages que alimentam a build (dependências listadas em go.mod, ou packages que são parte da biblioteca padrão Go) não serão incluídos por padrão.

Por exemplo, aqui está um programa toy contendo um package main, um package local de módulo principal `greetings` e um conjunto de packages importados de fora do módulo, incluindo (entre outros) `rsc.io/quote` e `fmt` ([link para programa completo](/play/p/VSQJN8xkkf-?v=gotip)).

```
$ cat go.mod
module mydomain.com

go 1.20

require rsc.io/quote v1.5.2

require (
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // indirect
	rsc.io/sampler v1.3.0 // indirect
)

$ cat myprogram.go
package main

import (
	"fmt"
	"mydomain.com/greetings"
	"rsc.io/quote"
)

func main() {
	fmt.Printf("I say %q and %q\n", quote.Hello(), greetings.Goodbye())
}
$ cat greetings/greetings.go
package greetings

func Goodbye() string {
	return "see ya"
}
$ go build -cover -o myprogram.exe .
$
```

Se você construir este programa com a flag de linha de comando "`-cover`" e executá-lo, exatamente dois packages serão incluídos no profile: `main` e `mydomain.com/greetings`; os outros packages dependentes serão excluídos.

Usuários que querem ter mais controle sobre quais packages são incluídos para coverage podem construir com a flag "`-coverpkg`". Exemplo:

```
$ go build -cover -o myprogramMorePkgs.exe -coverpkg=io,mydomain.com,rsc.io/quote .
$
```

Na build acima, o package main de `mydomain.com` assim como os packages `rsc.io/quote` e `io` são selecionados para profiling; já que `mydomain.com/greetings` não está especificamente listado, ele será excluído do profile, mesmo que resida no módulo principal.

# Executando um binário instrumentado para coverage {#running}

Binários construídos com "`-cover`" escrevem arquivos de dados de profile no final de sua execução em um diretório especificado via a variável de ambiente `GOCOVERDIR`. Exemplo:

```
$ go build -cover -o myprogram.exe myprogram.go
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
I say "Hello, world." and "see ya"
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$
```

Note os dois arquivos que foram escritos no diretório `somedata`: esses arquivos (binários) contêm os resultados de coverage. Veja a seção seguinte sobre [reporting](#reporting) para mais sobre como produzir resultados legíveis por humanos desses arquivos de dados.

Se a variável de ambiente `GOCOVERDIR` não estiver definida, um binário instrumentado para coverage ainda executará corretamente, mas emitirá um aviso.
Exemplo:

```
$ ./myprogram.exe
warning: GOCOVERDIR not set, no coverage data emitted
I say "Hello, world." and "see ya"
$
```

## Tests envolvendo múltiplas runs

Integration tests podem em muitos casos envolver múltiplas runs de programa; quando o programa é construído com "`-cover`", cada run produzirá um novo arquivo de dados. Exemplo

```
$ mkdir somedata2
$ GOCOVERDIR=somedata2 ./myprogram.exe          // first run
I say "Hello, world." and "see ya"
$ GOCOVERDIR=somedata2 ./myprogram.exe -flag    // second run
I say "Hello, world." and "see ya"
$ ls somedata2
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456041.1670259309405583534
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456047.1670259309410891043
covmeta.890814fca98ac3a4d41b9bd2a7ec9f7f
$
```

Arquivos de saída de dados de coverage vêm em dois sabores: arquivos de meta-data (contendo os itens que são invariantes de run para run, como nomes de arquivos fonte e nomes de funções), e arquivos de dados de counter (que registram as partes do programa que executaram).

No exemplo acima, a primeira run produziu dois arquivos (counter e meta), enquanto a segunda run gerou apenas um arquivo de dados de counter: já que meta-data não muda de run para run, ela só precisa ser escrita uma vez.

# Trabalhando com arquivos de dados de coverage {#working}

Go 1.20 introduz uma nova ferramenta, '`covdata`', que pode ser usada para ler e manipular arquivos de dados de coverage de um diretório `GOCOVERDIR`.

A ferramenta `covdata` do Go roda em uma variedade de modes. A forma geral de uma invocação da ferramenta `covdata` assume a forma

```
$ go tool covdata <mode> -i=<dir1,dir2,...> ...flags...
```

onde a flag "`-i`" fornece uma lista de diretórios para ler, onde cada diretório é derivado de uma execução de um binário instrumentado para coverage (via `GOCOVERDIR`).

## Criando relatórios de profile de coverage {#reporting}

Esta seção discute como usar "`go tool covdata`" para produzir relatórios legíveis por humanos de arquivos de dados de coverage.

### Reportando porcentagem de statements cobertos

Para reportar uma métrica de "porcentagem de statements cobertos" para cada package instrumentado, use o comando "`go tool covdata percent -i=<directory>`".
Usando o exemplo da seção [running](#running) acima:

```
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata
	main	coverage: 100.0% of statements
	mydomain.com/greetings	coverage: 100.0% of statements
$
```

As porcentagens de "statements covered" aqui correspondem diretamente àquelas reportadas por `go test -cover`.

## Convertendo para formato textual legado

Você pode converter arquivos de dados de coverage binários para o formato textual legado gerado por "`go test -coverprofile=<outfile>`" usando o seletor `textfmt` de covdata. O arquivo de texto resultante pode então ser usado com "`go tool cover -func`" ou "`go tool cover -html`" para criar relatórios adicionais. Exemplo:

```
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata textfmt -i=somedata -o profile.txt
$ cat profile.txt
mode: set
mydomain.com/myprogram.go:10.13,12.2 1 1
mydomain.com/greetings/greetings.go:3.23,5.2 1 1
$ go tool cover -func=profile.txt
mydomain.com/greetings/greetings.go:3:	Goodbye		100.0%
mydomain.com/myprogram.go:10:		main		100.0%
total:					(statements)	100.0%
$
```

## Merging

O subcomando `merge` de "`go tool covdata`" pode ser usado para mesclar profiles de múltiplos diretórios de dados.

Por exemplo, considere um programa que roda tanto no macOS quanto no Windows.
O autor deste programa pode querer combinar profiles de coverage de
runs separadas em cada sistema operacional em um único corpus de profile, para produzir um
resumo de coverage cross-platform.
Por exemplo:

```
$ ls windows_datadir
covcounters.f3833f80c91d8229544b25a855285890.1025623.1667481441036838252
covcounters.f3833f80c91d8229544b25a855285890.1025628.1667481441042785007
covmeta.f3833f80c91d8229544b25a855285890
$ ls macos_datadir
covcounters.b245ad845b5068d116a4e25033b429fb.1025358.1667481440551734165
covcounters.b245ad845b5068d116a4e25033b429fb.1025364.1667481440557770197
covmeta.b245ad845b5068d116a4e25033b429fb
$ ls macos_datadir
$ mkdir merged
$ go tool covdata merge -i=windows_datadir,macos_datadir -o merged
$
```

A operação de merge acima combinará os dados dos diretórios de entrada especificados e escreverá um novo conjunto de arquivos de dados mesclados no diretório "merged".

## Seleção de package

A maioria dos comandos "`go tool covdata`" suporta uma flag "`-pkg`" para realizar seleção de package como parte da operação; o argumento para "`-pkg`" assume a mesma forma que aquele usado pela flag "`-coverpkg`" do comando Go.
Exemplo:

```

$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata -pkg=mydomain.com/greetings
	mydomain.com/greetings	coverage: 100.0% of statements
$ go tool covdata percent -i=somedata -pkg=nonexistentpackage
$
```

A flag "`-pkg`" pode ser usada para selecionar o subconjunto específico de packages de interesse para um dado relatório.

#

## Perguntas Frequentes {#FAQ}

1. [Como posso solicitar instrumentação de coverage para todos os packages importados mencionados no meu arquivo `go.mod`](#gomodselect)
2. [Posso usar `go build -cover` no modo GOPATH/GO111MODULE=off?](#gopathmode)
3. [Se meu programa entrar em panic, dados de coverage serão escritos?](#panicprof)
4. [Vai `-coverpkg=main` selecionar meu package main para profiling?](#mainpkg)


#### Como posso solicitar instrumentação de coverage para todos os packages importados mencionados no meu arquivo `go.mod` {#gomodselect}

Por padrão, `go build -cover` instrumentará todos os packages do módulo principal
para coverage, mas não instrumentará imports fora do módulo principal
(por exemplo, packages da biblioteca padrão ou imports listados em `go.mod`).
Uma forma de solicitar instrumentação para todas as dependências não-stdlib
é alimentar a saída de `go list` em `-coverpkg`.
Aqui está um exemplo, novamente usando
o [programa de exemplo](/play/p/VSQJN8xkkf-?v=gotip) citado acima:

```
$ go list -f '{{"{{if not .Standard}}{{.ImportPath}}{{end}}"}}' -deps . | paste -sd "," > pkgs.txt
$ go build -o myprogram.exe -coverpkg=`cat pkgs.txt` .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
$ go tool covdata percent -i=somedata
	golang.org/x/text/internal/tag	coverage: 78.4% of statements
	golang.org/x/text/language	coverage: 35.5% of statements
	mydomain.com	coverage: 100.0% of statements
	mydomain.com/greetings	coverage: 100.0% of statements
	rsc.io/quote	coverage: 25.0% of statements
	rsc.io/sampler	coverage: 86.7% of statements
$
```

#### Posso usar `go build -cover` no modo GO111MODULE=off? {#gopathmode}

Sim, `go build -cover` funciona com `GO111MODULE=off`.
Ao construir um programa no modo GO111MODULE=off, apenas o package especificamente nomeado como alvo na linha de comando será instrumentado para profiling. Use a flag `-coverpkg` para incluir packages adicionais no profile.

#### Se meu programa entrar em panic, dados de coverage serão escritos? {#panicprof}

Programas construídos com `go build -cover` só escreverão dados de profile
completos no final da execução se o programa invocar `os.Exit()` ou retornar
normalmente de `main.main`.
Se um programa terminar em um panic não recuperado, ou se o programa atingir uma
exceção fatal (como uma violação de segmentação, divisão por zero, etc),
dados de profile de statements executados durante a run serão perdidos.

#### Vai `-coverpkg=main` selecionar meu package main para profiling? {#mainpkg}

A flag `-coverpkg` aceita uma lista de import paths, não uma lista de nomes de package. Se você quer selecionar seu package `main` para instrumentação de coverage, por favor identifique-o por import path, não por nome. Exemplo (usando [este programa de exemplo](/play/p/VSQJN8xkkf-?v=gotip)):

```
$ go list -m
mydomain.com
$ go build -coverpkg=main -o oops.exe .
warning: no packages being built depend on matches for pattern main
$ go build -coverpkg=mydomain.com -o myprogram.exe .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
I say "Hello, world." and "see ya"
$ go tool covdata percent -i=somedata
	mydomain.com	coverage: 100.0% of statements
$
```

## Recursos {#resources}

- **Post de blog introduzindo coverage de unit test no Go 1.2**:
  - Profiling de coverage para unit tests foi introduzido como parte do
    lançamento do Go 1.2; veja [este post de blog](/blog/cover) para detalhes.
- **Documentação**:
  - Os docs do package [`cmd/go`](https://pkg.go.dev/cmd/go) descrevem as
    flags de build e test associadas a coverage.
- **Detalhes técnicos**:
  - [Rascunho de design](/design/51430-revamp-code-coverage)
  - [Proposal](/issue/51430)

## Glossário {#glossary}

<a id="glos-unit-test"></a>
**unit test:** Tests dentro de um arquivo `*_test.go` associado a um package Go específico, utilizando o package `testing` do Go.

<a id="glos-integration-test"></a>
**integration test:** Um teste mais abrangente e de peso maior para uma dada aplicação ou binário. Integration tests tipicamente envolvem construir um programa ou conjunto de programas, depois executar uma série de runs dos programas usando múltiplas entradas e cenários, sob controle de um test harness que pode ou não ser baseado no package `testing` do Go.

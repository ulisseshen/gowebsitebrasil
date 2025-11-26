<!--{
  "Title": "Organizing a Go module",
  "ia-translated": true
}-->

Uma pergunta comum de desenvolvedores novos em Go é "Como organizo meu
projeto Go?", em termos de layout de arquivos e pastas. O objetivo deste
documento é fornecer algumas diretrizes que ajudarão a responder esta pergunta. Para
aproveitar ao máximo este documento, certifique-se de estar familiarizado com os conceitos básicos de
módulos Go lendo [o tutorial](/doc/tutorial/create-module) e
[managing module source](/doc/modules/managing-source).

Projetos Go podem incluir packages, programas de linha de comando ou uma combinação dos
dois. Este guia é organizado por tipo de projeto.

### Package básico

Um package Go básico tem todo seu código no diretório raiz do projeto. O projeto
consiste de um único módulo, que consiste de um único package. O nome do package
corresponde ao último componente do caminho do nome do módulo. Para um package muito simples
que requer um único arquivo Go, a estrutura do projeto é:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
```

_[em todo este documento, nomes de arquivo/package são totalmente arbitrários]_

Assumindo que este diretório seja enviado para um repositório GitHub em
`github.com/someuser/modname`, a linha `module` no arquivo `go.mod` deve dizer
`module github.com/someuser/modname`.

O código em `modname.go` declara o package com:

```
package modname

// ... package code here
```

Usuários podem então depender deste package `import`-ando-o em seu código Go com:

```
import "github.com/someuser/modname"
```

Um package Go pode ser dividido em múltiplos arquivos, todos residindo no mesmo
diretório, ex.:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth.go
  auth_test.go
  hash.go
  hash_test.go
```

Todos os arquivos no diretório declaram `package modname`.

### Comando básico

Um programa executável básico (ou ferramenta de linha de comando) é estruturado de acordo com sua
complexidade e tamanho de código. O programa mais simples pode consistir de um único arquivo Go
onde `func main` é definido. Programas maiores podem ter seu código dividido em
múltiplos arquivos, todos declarando `package main`:

```
project-root-directory/
  go.mod
  auth.go
  auth_test.go
  client.go
  main.go
```

Aqui o arquivo `main.go` contém `func main`, mas isso é apenas uma convenção. O
arquivo "main" também pode ser chamado `modname.go` (para um valor apropriado de
`modname`) ou qualquer outra coisa.

Assumindo que este diretório seja enviado para um repositório GitHub em
`github.com/someuser/modname`, a linha `module` no arquivo `go.mod` deve
dizer:

```
module github.com/someuser/modname
```

E um usuário deve ser capaz de instalá-lo em sua máquina com:

```
$ go install github.com/someuser/modname@latest
```

### Package ou comando com packages de suporte

Packages ou comandos maiores podem se beneficiar de separar alguma funcionalidade
em packages de suporte. Inicialmente, é recomendado colocar tais packages em
um diretório chamado `internal`;
[isso previne](https://pkg.go.dev/cmd/go#hdr-Internal_Directories) que outros
módulos dependam de packages que não necessariamente queremos expor e
suportar para usos externos. Como outros projetos não podem importar código do nosso
diretório `internal`, somos livres para refatorar sua API e geralmente mover coisas
sem quebrar usuários externos. A estrutura do projeto para um package é
assim:

```
project-root-directory/
  internal/
    auth/
      auth.go
      auth_test.go
    hash/
      hash.go
      hash_test.go
  go.mod
  modname.go
  modname_test.go
```

O arquivo `modname.go` declara `package modname`, `auth.go` declara `package
auth` e assim por diante. `modname.go` pode importar o package `auth` da seguinte forma:

```
import "github.com/someuser/modname/internal/auth"
```

O layout para um comando com packages de suporte em um diretório `internal` é
muito similar, exceto que o(s) arquivo(s) no diretório raiz declaram `package
main`.

### Múltiplos packages

Um módulo pode consistir de múltiplos packages importáveis; cada package tem seu próprio
diretório, e pode ser estruturado hierarquicamente. Aqui está uma estrutura de projeto
exemplo:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth/
    auth.go
    auth_test.go
    token/
      token.go
      token_test.go
  hash/
    hash.go
  internal/
    trace/
      trace.go
```

Como lembrete, assumimos que a linha `module` em `go.mod` diz:

```
module github.com/someuser/modname
```

O package `modname` reside no diretório raiz, declara `package modname`
e pode ser importado por usuários com:

```
import "github.com/someuser/modname"
```

Sub-packages podem ser importados por usuários da seguinte forma:

```
import "github.com/someuser/modname/auth"
import "github.com/someuser/modname/auth/token"
import "github.com/someuser/modname/hash"
```

O package `trace` que reside em `internal/trace` não pode ser importado fora deste
módulo. É recomendado manter packages em `internal` tanto quanto possível.

### Múltiplos comandos

Múltiplos programas no mesmo repositório tipicamente terão diretórios separados:

```
project-root-directory/
  go.mod
  internal/
    ... shared internal packages
  prog1/
    main.go
  prog2/
    main.go
```

Em cada diretório, os arquivos Go do programa declaram `package main`. Um diretório
`internal` de nível superior pode conter packages compartilhados usados por todos os comandos no
repositório.

Usuários podem instalar esses programas da seguinte forma:

```
$ go install github.com/someuser/modname/prog1@latest
$ go install github.com/someuser/modname/prog2@latest
```

Uma convenção comum é colocar todos os comandos em um repositório em um diretório `cmd`;
embora isso não seja estritamente necessário em um repositório que consiste
apenas de comandos, é muito útil em um repositório misto que tem tanto comandos
quanto packages importáveis, como discutiremos a seguir.

### Packages e comandos no mesmo repositório

Às vezes um repositório fornecerá tanto packages importáveis quanto
comandos instaláveis com funcionalidade relacionada. Aqui está uma estrutura de projeto exemplo para tal
repositório:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth/
    auth.go
    auth_test.go
  internal/
    ... internal packages
  cmd/
    prog1/
      main.go
    prog2/
      main.go
```

Assumindo que este módulo se chama `github.com/someuser/modname`, usuários podem agora tanto
importar packages dele:

```
import "github.com/someuser/modname"
import "github.com/someuser/modname/auth"
```

Quanto instalar programas dele:

```
$ go install github.com/someuser/modname/cmd/prog1@latest
$ go install github.com/someuser/modname/cmd/prog2@latest
```

### Projeto de servidor

Go é uma escolha de linguagem comum para implementar *servidores*. Há uma variância muito grande
na estrutura de tais projetos, dadas as muitas facetas do desenvolvimento
de servidor: protocolos (REST? gRPC?), deployments, arquivos de front-end,
containerização, scripts e assim por diante. Vamos focar nossa orientação aqui nas
partes do projeto escritas em Go.

Projetos de servidor tipicamente não terão packages para exportação, já que um servidor é
geralmente um binário autocontido (ou um grupo de binários). Portanto, é
recomendado manter os packages Go implementando a lógica do servidor no
diretório `internal`. Além disso, como o projeto provavelmente terá muitos outros
diretórios com arquivos não-Go, é uma boa ideia manter todos os comandos Go juntos
em um diretório `cmd`:

```
project-root-directory/
  go.mod
  internal/
    auth/
      ...
    metrics/
      ...
    model/
      ...
  cmd/
    api-server/
      main.go
    metrics-analyzer/
      main.go
    ...
  ... the project's other directories with non-Go code
```

Caso o repositório do servidor cresça packages que se tornam úteis para compartilhar com
outros projetos, é melhor separá-los em módulos separados.

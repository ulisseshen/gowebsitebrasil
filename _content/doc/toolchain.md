---
ia-translated: true
title: "Toolchains do Go"
layout: article
---

## Introdução {#intro}

A partir do Go 1.21, a distribuição Go consiste de um comando `go` e uma toolchain Go integrada,
que é a biblioteca padrão, bem como o compilador, assembler e outras ferramentas.
O comando `go` pode usar sua toolchain Go integrada, bem como outras versões
que encontra no `PATH` local ou baixa conforme necessário.

A escolha da toolchain Go sendo usada depende da configuração de ambiente `GOTOOLCHAIN`
e das linhas `go` e `toolchain` no arquivo `go.mod` do módulo principal ou no arquivo `go.work` do workspace atual.
À medida que você se move entre diferentes módulos principais e workspaces,
a versão da toolchain sendo usada pode variar, assim como as versões de dependência de módulo.

Na configuração padrão, o comando `go` usa sua própria toolchain integrada
quando essa toolchain é pelo menos tão nova quanto as linhas `go` ou `toolchain` no módulo principal ou workspace.
Por exemplo, ao usar o comando `go` integrado com Go 1.21.3 em um módulo principal que diz `go 1.21.0`,
o comando `go` usa Go 1.21.3.
Quando a linha `go` ou `toolchain` é mais nova que a toolchain integrada,
o comando `go` executa a toolchain mais nova.
Por exemplo, ao usar o comando `go` integrado com Go 1.21.3 em um módulo principal que diz `go 1.21.9`,
o comando `go` encontra e executa Go 1.21.9.
Ele primeiro procura no PATH por um programa chamado `go1.21.9` e, caso contrário, baixa e armazena em cache
uma cópia da toolchain Go 1.21.9.
Essa troca automática de toolchain pode ser desativada, mas nesse caso,
para compatibilidade futura mais precisa,
o comando `go` se recusará a executar em um módulo principal ou workspace no qual a linha `go`
exige uma versão mais nova do Go.
Ou seja, a linha `go` define a versão mínima do Go necessária para usar um módulo ou workspace.

Módulos que são dependências de outros módulos podem precisar definir um requisito de versão mínima do Go
menor que a toolchain preferida para usar ao trabalhar nesse módulo diretamente.
Nesse caso, a linha `toolchain` em `go.mod` ou `go.work` define uma toolchain preferida
que tem precedência sobre a linha `go` quando o comando `go` está decidindo
qual toolchain usar.

As linhas `go` e `toolchain` podem ser pensadas como especificando os requisitos de versão
para a dependência do módulo na própria toolchain Go, assim como as linhas `require` em `go.mod`
especificam os requisitos de versão para dependências em outros módulos.
O comando `go get` gerencia a dependência da toolchain Go assim como
gerencia dependências em outros módulos.
Por exemplo, `go get go@latest` atualiza o módulo para exigir a toolchain Go mais recente lançada.

A configuração de ambiente `GOTOOLCHAIN` pode forçar uma versão específica do Go, substituindo
as linhas `go` e `toolchain`. Por exemplo, para testar um pacote com Go 1.21rc3:

	GOTOOLCHAIN=go1.21rc3 go test

A configuração padrão `GOTOOLCHAIN` é `auto`, que habilita a troca de toolchain descrita anteriormente.
A forma alternativa `<name>+auto` define a toolchain padrão a ser usada antes de decidir se
trocar. Por exemplo, `GOTOOLCHAIN=go1.21.3+auto` direciona o comando `go` a
começar sua decisão com um padrão de usar Go 1.21.3, mas ainda usar uma toolchain mais nova se
direcionado pelas linhas `go` e `toolchain`.
Como a configuração padrão `GOTOOLCHAIN` pode ser alterada com `go env -w`,
se você tiver Go 1.21.0 ou posterior instalado, então

	go env -w GOTOOLCHAIN=go1.21.3+auto

é equivalente a substituir sua instalação Go 1.21.0 por Go 1.21.3.

O restante deste documento explica como as toolchains Go são versionadas, escolhidas e gerenciadas com mais detalhes.

## Versões Go {#version}

Versões lançadas do Go usam a sintaxe de versão '1.*N*.*P*', denotando o *P*-ésimo lançamento do Go 1.*N*.
O lançamento inicial é 1.*N*.0, como em '1.21.0'. Lançamentos posteriores como 1.*N*.9 são frequentemente chamados de lançamentos patch.

Candidatos a lançamento Go 1.*N*, que são emitidos antes de 1.*N*.0, usam a sintaxe de versão '1.*N*rc*R*'.
O primeiro candidato a lançamento para Go 1.*N* tem versão 1.*N*rc1, como em `1.23rc1`.

A sintaxe '1.*N*' é chamada de "versão de linguagem". Ela denota a família geral de lançamentos Go
implementando essa versão da linguagem Go e biblioteca padrão.

A versão de linguagem para uma versão Go é o resultado de truncar tudo após o *N*:
1.21, 1.21rc2 e 1.21.3 todos implementam a versão de linguagem 1.21.

Toolchains Go lançadas como Go 1.21.0 e Go 1.21rc1 reportam essa versão específica
(por exemplo, `go1.21.0` ou `go1.21rc1`)
de `go version` e [`runtime.Version`](/pkg/runtime/#Version).
Toolchains Go não lançadas (ainda em desenvolvimento) construídas do repositório de desenvolvimento Go
em vez disso reportam apenas a versão de linguagem (por exemplo, `go1.21`).

Quaisquer duas versões Go podem ser comparadas para decidir se uma é menor que, maior que,
ou igual à outra. Se as versões de linguagem são diferentes, isso decide a comparação:
1.21.9 < 1.22. Dentro de uma versão de linguagem, a ordenação do menor para o maior é:
a versão de linguagem em si, depois candidatos a lançamento ordenados por *R*, depois lançamentos ordenados por *P*.

Por exemplo, 1.21 < 1.21rc1 < 1.21rc2 < 1.21.0 < 1.21.1 < 1.21.2.

Antes do Go 1.21, o lançamento inicial de uma toolchain Go era versão 1.*N*, não 1.*N*.0,
então para *N* < 21, a ordenação é ajustada para colocar 1.*N* depois dos candidatos a lançamento.

Por exemplo, 1.20rc1 < 1.20rc2 < 1.20rc3 < 1.20 < 1.20.1.

Versões anteriores do Go tinham lançamentos beta, com versões como 1.18beta2.
Lançamentos beta são colocados imediatamente antes dos candidatos a lançamento na ordenação de versão.

Por exemplo, 1.18beta1 < 1.18beta2 < 1.18rc1 < 1.18 < 1.18.1.

<!-- Unpublished note: the download page also lists Go 1.9.2rc2, which does not respect
this version syntax. That was created as a test of some potential release automation
before Go 1.9.2 but is not considered a "real" toolchain. -->

## Nomes de toolchain Go {#name}

As toolchains Go padrão são nomeadas <code>go<i>V</i></code> onde *V* é uma versão Go
denotando um lançamento beta, candidato a lançamento ou lançamento.
Por exemplo, `go1.21rc1` e `go1.21.0` são nomes de toolchain;
`go1.21` e `go1.22` não são (os lançamentos iniciais são `go1.21.0` e `go1.22.0`),
mas `go1.20` e `go1.19` são.

Toolchains não padrão usam nomes da forma <code>go<i>V</i>-<i>suffix</i></code>
para qualquer sufixo.

Toolchains são comparadas comparando a versão <code><i>V</i></code> incorporada no nome
(removendo o `go` inicial e descartando qualquer sufixo começando com `-`).
Por exemplo, `go1.21.0` e `go1.21.0-custom` comparam iguais para propósitos de ordenação.

## Configuração de módulo e workspace {#config}

Módulos Go e workspaces especificam configuração relacionada a versão
em seus arquivos `go.mod` ou `go.work`.

A linha `go` declara a versão mínima do Go necessária para usar
o módulo ou workspace.
Por razões de compatibilidade, se a linha `go` é omitida de um arquivo `go.mod`,
o módulo é considerado como tendo uma linha implícita `go 1.16`,
e se a linha `go` é omitida de um arquivo `go.work`,
o workspace é considerado como tendo uma linha implícita `go 1.18`.

A linha `toolchain` declara uma toolchain sugerida para usar com
o módulo ou workspace.
Como descrito em "[Seleção de toolchain Go](#select)" abaixo,
o comando `go` pode executar essa toolchain específica ao operar
nesse módulo ou workspace
se a versão da toolchain padrão for menor que a versão da toolchain sugerida.
Se a linha `toolchain` for omitida,
o módulo ou workspace é considerado como tendo uma
linha <code>toolchain go<i>V</i></code> implícita,
onde *V* é a versão Go da linha `go`.

Por exemplo, um `go.mod` que diz `go 1.21.0` sem linha `toolchain`
é interpretado como se tivesse uma linha `toolchain go1.21.0`.

A toolchain Go se recusa a carregar um módulo ou workspace que declara
uma versão mínima do Go maior que a própria versão da toolchain.

Por exemplo, Go 1.21.2 se recusará a carregar um módulo ou workspace
com uma linha `go 1.21.3` ou `go 1.22`.

A linha `go` de um módulo deve declarar uma versão maior ou igual a
a versão `go` declarada por cada um dos módulos listados em declarações `require`.
A linha `go` de um workspace deve declarar uma versão maior ou igual a
a versão `go` declarada por cada um dos módulos listados em declarações `use`.

Por exemplo, se o módulo *M* requer uma dependência *D* com um `go.mod`
que declara `go 1.22.0`, então o `go.mod` de *M* não pode dizer `go 1.21.3`.

A linha `go` para cada módulo define a versão de linguagem que o compilador
impõe ao compilar pacotes nesse módulo.
A versão de linguagem pode ser alterada por arquivo usando uma
[build constraint](/cmd/go#hdr-Build_constraints):
se uma build constraint estiver presente e implicar uma versão mínima de pelo menos `go1.21`,
a versão de linguagem usada ao compilar esse arquivo será essa versão mínima.

Por exemplo, um módulo contendo código que usa a versão de linguagem Go 1.21
deve ter um arquivo `go.mod` com uma linha `go` como `go 1.21` ou `go 1.21.3`.
Se um arquivo fonte específico deve ser compilado apenas ao usar uma toolchain Go mais nova,
adicionar `//go:build go1.22` a esse arquivo fonte garante que apenas Go 1.22 e
toolchains mais novas compilarão o arquivo e também altera a versão de linguagem nesse
arquivo para Go 1.22.

As linhas `go` e `toolchain` são mais convenientemente e seguramente modificadas
usando `go get`; veja a [seção dedicada a `go get` abaixo](#get).

Antes do Go 1.21, toolchains Go tratavam a linha `go` como um requisito consultivo:
se as builds tivessem sucesso, a toolchain assumia que tudo funcionava,
e se não, imprimia uma nota sobre a possível incompatibilidade de versão.
Go 1.21 mudou a linha `go` para ser um requisito obrigatório.
Esse comportamento é parcialmente portado para versões de linguagem anteriores:
lançamentos Go 1.19 começando em Go 1.19.13 e lançamentos Go 1.20 começando em Go 1.20.8,
se recusam a carregar workspaces ou módulos declarando versão Go 1.22 ou posterior.

Antes do Go 1.21, toolchains não exigiam que um módulo
ou workspace tivesse uma linha `go` maior ou igual à
versão `go` exigida por cada um de seus módulos de dependência.

## A configuração `GOTOOLCHAIN` {#GOTOOLCHAIN}

O comando `go` seleciona a toolchain Go a ser usada com base na configuração `GOTOOLCHAIN`.
Para encontrar a configuração `GOTOOLCHAIN`, o comando `go` usa as regras padrão para qualquer
configuração de ambiente Go:

 - Se `GOTOOLCHAIN` está definido com um valor não vazio no ambiente do processo
   (conforme consultado por [`os.Getenv`](/pkg/os/#Getenv)), o comando `go` usa esse valor.

 - Caso contrário, se `GOTOOLCHAIN` está definido no arquivo padrão de ambiente do usuário
   (gerenciado com
   [`go env -w` e `go env -u`](/cmd/go/#hdr-Print_Go_environment_information)),
   o comando `go` usa esse valor.

 - Caso contrário, se `GOTOOLCHAIN` está definido no arquivo padrão de ambiente da toolchain Go integrada
   (`$GOROOT/go.env`), o comando `go` usa esse valor.

Em toolchains Go padrão, o arquivo `$GOROOT/go.env` define o padrão `GOTOOLCHAIN=auto`,
mas toolchains Go reempacotadas podem alterar esse valor.

Se o arquivo `$GOROOT/go.env` estiver ausente ou não definir um padrão, o comando `go`
assume `GOTOOLCHAIN=local`.

Executar `go env GOTOOLCHAIN` imprime a configuração `GOTOOLCHAIN`.

## Seleção de toolchain Go {#select}

Na inicialização, o comando `go` seleciona qual toolchain Go usar.
Ele consulta a configuração `GOTOOLCHAIN`,
que assume a forma `<name>`, `<name>+auto` ou `<name>+path`.
`GOTOOLCHAIN=auto` é uma abreviação para `GOTOOLCHAIN=local+auto`;
similarmente, `GOTOOLCHAIN=path` é uma abreviação para `GOTOOLCHAIN=local+path`.
O `<name>` define a toolchain Go padrão:
`local` indica a toolchain Go integrada
(aquela que veio com o comando `go` sendo executado), e caso contrário `<name>` deve
ser um nome de toolchain Go específico, como `go1.21.0`.
O comando `go` prefere executar a toolchain Go padrão.
Como observado acima, a partir do Go 1.21, toolchains Go se recusam a executar em
workspaces ou módulos que exigem versões mais novas do Go.
Em vez disso, eles relatam um erro e saem.

Quando `GOTOOLCHAIN` está definido como `local`, o comando `go` sempre executa a toolchain Go integrada.

Quando `GOTOOLCHAIN` está definido como `<name>` (por exemplo, `GOTOOLCHAIN=go1.21.0`),
o comando `go` sempre executa essa toolchain Go específica.
Se um binário com esse nome for encontrado no PATH do sistema, o comando `go` o usa.
Caso contrário, o comando `go` usa uma toolchain Go que baixa e verifica.

Quando `GOTOOLCHAIN` está definido como `<name>+auto` ou `<name>+path` (ou as abreviações `auto` ou `path`),
o comando `go` seleciona e executa uma versão Go mais nova conforme necessário.
Especificamente, ele consulta as linhas `toolchain` e `go` no arquivo
`go.work` do workspace atual ou, quando não há workspace,
o arquivo `go.mod` do módulo principal.
Se o arquivo `go.work` ou `go.mod` tem uma linha `toolchain <tname>`
e `<tname>` é mais novo que a toolchain Go padrão,
então o comando `go` executa `<tname>`.
Se o arquivo tem uma linha `toolchain default`,
então o comando `go` executa a toolchain Go padrão,
desabilitando qualquer tentativa de atualização além de `<name>`.
Caso contrário, se o arquivo tem uma linha `go <version>`
e `<version>` é mais novo que a toolchain Go padrão,
então o comando `go` executa `go<version>`.

Para executar uma toolchain diferente da toolchain Go integrada,
o comando `go` pesquisa o caminho executável do processo
(`$PATH` no Unix e Plan 9, `%PATH%` no Windows)
por um programa com o nome dado (por exemplo, `go1.21.3`) e executa esse programa.
Se nenhum programa assim for encontrado, o comando `go`
[baixa e executa a toolchain Go especificada](#download).
Usar a forma `GOTOOLCHAIN` `<name>+path` desabilita o fallback de download,
fazendo com que o comando `go` pare após pesquisar o caminho executável.

Executar `go version` imprime a versão da toolchain Go selecionada
(executando a implementação da toolchain selecionada de `go version`).

Executar `GOTOOLCHAIN=local go version` imprime a versão da toolchain Go integrada.

A partir do Go 1.24, você pode rastrear o processo de seleção de toolchain do comando `go`
adicionando `toolchaintrace=1` à variável de ambiente `GODEBUG` quando você executa o
comando `go`.

## Trocas de toolchain Go {#switch}

Para a maioria dos comandos, o `go.work` do workspace ou o `go.mod` do módulo principal
terá uma linha `go` que é pelo menos tão nova quanto a linha `go` em qualquer dependência de módulo,
devido aos [requisitos de configuração](#config) de ordenação de versão.
Nesse caso, a seleção de toolchain de inicialização executa uma toolchain Go nova o suficiente
para completar o comando.

Alguns comandos incorporam novas versões de módulo como parte de sua operação:
`go get` adiciona novas dependências de módulo ao módulo principal;
`go work use` adiciona novos módulos locais ao workspace;
`go work sync` ressincroniza um workspace com módulos locais que podem ter sido atualizados
desde que o workspace foi criado;
`go install package@version` e `go run package@version`
efetivamente executam em um módulo principal vazio e adicionam `package@version` como uma nova dependência.
Todos esses comandos podem encontrar um módulo com uma linha `go` do `go.mod`
exigindo uma versão Go mais nova que a versão Go atualmente executada.

Quando um comando encontra um módulo exigindo uma versão Go mais nova
e `GOTOOLCHAIN` permite executar diferentes toolchains
(é uma das formas `auto` ou `path`),
o comando `go` escolhe e troca para uma toolchain mais nova apropriada
para continuar executando o comando atual.

Sempre que o comando `go` troca toolchains após a seleção de toolchain de inicialização,
ele imprime uma mensagem explicando por quê. Por exemplo:

	go: module example.com/widget@v1.2.3 requires go >= 1.24rc1; switching to go 1.27.9

Como mostrado no exemplo, o comando `go` pode trocar para uma toolchain
mais nova que o requisito descoberto.
Em geral, o comando `go` visa trocar para uma toolchain Go suportada.

Para escolher a toolchain, o comando `go` primeiro obtém uma lista de toolchains disponíveis.
Para a forma `auto`, o comando `go` baixa uma lista de toolchains disponíveis.
Para a forma `path`, o comando `go` escaneia o PATH por quaisquer executáveis
nomeados para toolchains válidas e usa uma lista de todas as toolchains que encontra.
Usando essa lista de toolchains, o comando `go` identifica até três candidatos:

 - o candidato a lançamento mais recente de uma versão de linguagem Go não lançada (1.*N*₃rc*R*₃),
 - o lançamento patch mais recente da versão de linguagem Go mais recentemente lançada (1.*N*₂.*P*₂), e
 - o lançamento patch mais recente da versão de linguagem Go anterior (1.*N*₁.*P*₁).

Estes são os lançamentos Go suportados de acordo com a [política de lançamento](/doc/devel/release#policy) do Go.
Consistente com [seleção de versão mínima](https://research.swtch.com/vgo-mvs),
o comando `go` então conservadoramente usa o candidato com a versão _mínima_ (mais antiga)
que satisfaz o novo requisito.

Por exemplo, suponha que `example.com/widget@v1.2.3` requer Go 1.24rc1 ou posterior.
O comando `go` obtém a lista de toolchains disponíveis
e descobre que os lançamentos patch mais recentes das duas toolchains Go mais recentes são
Go 1.28.3 e Go 1.27.9,
e o candidato a lançamento Go 1.29rc2 também está disponível.
Nessa situação, o comando `go` escolherá Go 1.27.9.
Se `widget` tivesse exigido Go 1.28 ou posterior, o comando `go` escolheria Go 1.28.3,
porque Go 1.27.9 é muito antigo.
Se `widget` tivesse exigido Go 1.29 ou posterior, o comando `go` escolheria Go 1.29rc2,
porque tanto Go 1.27.9 quanto Go 1.28.3 são muito antigos.

Comandos que incorporam novas versões de módulo que exigem novas versões Go
escrevem o novo requisito de versão `go` mínimo no arquivo `go.work` do workspace atual
ou no arquivo `go.mod` do módulo principal, atualizando a linha `go`.
Para [repetibilidade](https://research.swtch.com/vgo-principles#repeatability),
qualquer comando que atualiza a linha `go` também atualiza a linha `toolchain`
para registrar seu próprio nome de toolchain.
Na próxima vez que o comando `go` executar nesse workspace ou módulo,
ele usará essa linha `toolchain` atualizada durante a [seleção de toolchain](#select).

Por exemplo, `go get example.com/widget@v1.2.3` pode imprimir um aviso de troca
como acima e trocar para Go 1.27.9.
Go 1.27.9 completará o `go get` e atualizará a linha `toolchain`
para dizer `toolchain go1.27.9`.
O próximo comando `go` executado nesse módulo ou workspace selecionará `go1.27.9`
durante a inicialização e não imprimirá nenhuma mensagem de troca.

Em geral, se qualquer comando `go` for executado duas vezes, se o primeiro imprimir uma mensagem
de troca, o segundo não imprimirá, porque o primeiro também atualizou `go.work` ou `go.mod`
para selecionar a toolchain certa na inicialização.
A exceção são as formas `go install package@version` e `go run package@version`,
que executam sem workspace ou módulo principal e não podem escrever uma linha `toolchain`.
Eles imprimem uma mensagem de troca toda vez que precisam trocar
para uma toolchain mais nova.

## Baixando toolchains {#download}

Ao usar `GOTOOLCHAIN=auto` ou `GOTOOLCHAIN=<name>+auto`, o comando Go
baixa toolchains mais novas conforme necessário.
Essas toolchains são empacotadas como módulos especiais
com caminho de módulo `golang.org/toolchain`
e versão <code>v0.0.1-go<i>VERSION</i>.<i>GOOS</i>-<i>GOARCH</i></code>.
Toolchains são baixadas como qualquer outro módulo,
o que significa que downloads de toolchain podem ser proxiados definindo `GOPROXY`
e ter seus checksums verificados pelo banco de dados de checksum Go.
Como a toolchain específica usada depende da própria toolchain padrão do sistema,
bem como do sistema operacional e arquitetura locais (GOOS e GOARCH),
não é prático escrever checksums de módulo toolchain em `go.sum`.
Em vez disso, downloads de toolchain falham por falta de verificação se `GOSUMDB=off`.
Padrões `GOPRIVATE` e `GONOSUMDB` não se aplicam aos downloads de toolchain.

## Gerenciando requisitos de versão Go de módulo com `go get` {#get}

Em geral, o comando `go` trata as linhas `go` e `toolchain`
como declarando dependências de toolchain versionadas do módulo principal.
O comando `go get` pode gerenciar essas linhas assim como gerencia
as linhas `require` que especificam dependências de módulo versionadas.

Por exemplo, `go get go@1.22.1 toolchain@1.24rc1` altera o arquivo
`go.mod` do módulo principal para ler `go 1.22.1` e `toolchain go1.24rc1`.

O comando `go` entende que a dependência `go` requer uma dependência `toolchain`
com uma versão Go maior ou igual.

Continuando o exemplo, um `go get go@1.25.0` posterior atualizará
a toolchain para `go1.25.0` também.
Quando a toolchain corresponde exatamente à linha `go`, ela pode ser
omitida e implícita, então este `go get` excluirá a linha `toolchain`.

O mesmo requisito se aplica ao contrário ao fazer downgrade:
se o `go.mod` começa em `go 1.22.1` e `toolchain go1.24rc1`,
então `go get toolchain@go1.22.9` atualizará apenas a linha `toolchain`,
mas `go get toolchain@go1.21.3` fará downgrade da linha `go` para
`go 1.21.3` também.
O efeito será deixar apenas `go 1.21.3` sem linha `toolchain`.

A forma especial `toolchain@none` significa remover qualquer linha `toolchain`,
como em `go get toolchain@none` ou `go get go@1.25.0 toolchain@none`.

O comando `go` entende a sintaxe de versão para
dependências `go` e `toolchain`, bem como consultas.

Por exemplo, assim como `go get example.com/widget@v1.2` usa
a versão `v1.2` mais recente de `example.com/widget` (talvez `v1.2.3`),
`go get go@1.22` usa o lançamento mais recente disponível da versão de linguagem Go 1.22
(talvez `1.22rc3`, ou talvez `1.22.3`).
O mesmo se aplica a `go get toolchain@go1.22`.

Os comandos `go get` e `go mod tidy` mantêm a linha `go` para
ser maior ou igual à linha `go` de qualquer módulo de dependência exigido.

Por exemplo, se o módulo principal tem `go 1.22.1` e executamos
`go get example.com/widget@v1.2.3` que declara `go 1.24rc1`,
então `go get` atualizará a linha `go` do módulo principal para `go 1.24rc1`.

Continuando o exemplo, um `go get go@1.22.1` posterior fará
downgrade de `example.com/widget` para uma versão compatível com Go 1.22.1
ou removerá o requisito completamente,
assim como faria ao fazer downgrade de qualquer outra dependência de `example.com/widget`.

Antes do Go 1.21, a maneira sugerida de atualizar um módulo para uma nova versão Go (digamos, Go 1.22)
era `go mod tidy -go=1.22`, para garantir que quaisquer ajustes
específicos ao Go 1.22 fossem feitos no `go.mod` ao mesmo tempo que a
linha `go` é atualizada.
Essa forma ainda é válida, mas o mais simples `go get go@1.22` agora é preferido.

Quando `go get` é executado em um módulo em um diretório contido em uma raiz de workspace,
`go get` principalmente ignora o workspace,
mas ele atualiza o arquivo `go.work` para atualizar a linha `go`
quando o workspace seria deixado com uma linha `go` muito antiga.

## Gerenciando requisitos de versão Go de workspace com `go work` {#work}

Como observado na seção anterior, `go get` executado em um diretório
dentro de uma raiz de workspace cuidará de atualizar a linha `go` do arquivo `go.work`
conforme necessário para ser maior ou igual a qualquer módulo dentro dessa raiz.
No entanto, workspaces também podem se referir a módulos fora do diretório raiz;
executar `go get` nesses diretórios pode resultar em uma configuração de workspace
inválida, na qual a versão `go` declarada em `go.work` é menor
que um ou mais dos módulos nas diretivas `use`.

O comando `go work use`, que adiciona novas diretivas `use`, também verifica
que a versão `go` no arquivo `go.work` é nova o suficiente para todas as
diretivas `use` existentes.
Para atualizar um workspace que teve sua versão `go` dessincronizada
com seus módulos, execute `go work use` sem argumentos.

Os comandos `go work init` e `go work sync` também atualizam a versão `go`
conforme necessário.

Para remover a linha `toolchain` de um arquivo `go.work`, use
`go work edit -toolchain=none`.

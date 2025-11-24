---
ia-translated: true
title: Go 1.24 foi lançado!
date: 2025-02-11
by:
- Junyang Shao, em nome da equipe Go
summary:
  Go 1.24 traz generic type aliases, melhorias de performance em maps, conformidade com FIPS 140
  e muito mais.
---

Hoje a equipe Go está animada em lançar o Go 1.24,
que você pode obter visitando a [página de download](/dl/).

Go 1.24 vem com muitas melhorias em relação ao Go 1.23. Aqui estão algumas das mudanças
notáveis; para a lista completa, consulte as [notas de lançamento](/doc/go1.24).

## Mudanças na linguagem

<!-- go.dev/issue/46477 -->
Go 1.24 agora suporta totalmente [generic type aliases](/issue/46477): um type alias
pode ser parametrizado como um tipo definido.
Veja a [especificação da linguagem](/ref/spec#Alias_declarations) para detalhes.

## Melhorias de performance

<!-- go.dev/issue/54766, go.dev/cl/614795, go.dev/issue/68578 -->
Várias melhorias de performance no runtime diminuíram a sobrecarga de CPU
em 2–3% em média em um conjunto de benchmarks representativos. Essas
melhorias incluem uma nova implementação de `map` builtin baseada em
[Swiss Tables](https://abseil.io/about/design/swisstables), alocação de
memória mais eficiente para objetos pequenos, e uma nova implementação de mutex
interna ao runtime.

## Melhorias nas ferramentas

- <!-- go.dev/issue/48429 -->
  O comando `go` agora fornece um mecanismo para rastrear dependências de ferramentas para um
  módulo. Use `go get -tool` para adicionar uma diretiva `tool` ao módulo atual. Use
  `go tool [tool name]` para executar as ferramentas declaradas com a diretiva `tool`.
  Leia mais sobre o [comando go](/doc/go1.24#go-command) nas notas de lançamento.
- <!-- go.dev/issue/44251 -->
  O novo analisador `test` no subcomando `go vet` reporta erros comuns em
  declarações de testes, fuzzers, benchmarks e exemplos em pacotes de teste.
  Leia mais sobre [vet](/doc/go1.24#vet) nas notas de lançamento.

## Adições à biblioteca padrão

- A biblioteca padrão agora inclui [um novo conjunto de mecanismos para facilitar
  a conformidade com FIPS 140-3](/doc/security/fips140). Aplicações não requerem mudanças no código-fonte
  para usar os novos mecanismos para algoritmos aprovados. Leia mais
  sobre [conformidade com FIPS 140-3](/doc/go1.24#fips140) nas notas de lançamento.
  Além do FIPS 140, vários pacotes que anteriormente estavam no
  módulo [x/crypto](/pkg/golang.org/x/crypto) agora estão disponíveis na
  [biblioteca padrão](/doc/go1.24#crypto-mlkem).

- Benchmarks agora podem usar o método
  [`testing.B.Loop`](/pkg/testing#B.Loop) mais rápido e menos propenso a erros para realizar iterações de benchmark
  como `for b.Loop() { ... }` no lugar das estruturas de loop típicas envolvendo
  `b.N` como `for range b.N`. Leia mais sobre
  [a nova função de benchmark](/doc/go1.24#new-benchmark-function) nas
  notas de lançamento.

- O novo tipo [`os.Root`](/pkg/os#Root) fornece a capacidade de realizar
  operações de sistema de arquivos isoladas sob um diretório específico. Leia mais sobre
  [acesso a sistema de arquivos](/doc/go1.24#directory-limited-filesystem-access) nas
  notas de lançamento.

- O runtime fornece um novo mecanismo de finalização,
  [`runtime.AddCleanup`](/pkg/runtime#AddCleanup), que é mais flexível,
  mais eficiente e menos propenso a erros do que
  [`runtime.SetFinalizer`](/pkg/runtime#SetFinalizer). Leia mais sobre
  [cleanups](/doc/go1.24#improved-finalizers) nas notas de lançamento.

## Suporte melhorado a WebAssembly

<!-- go.dev/issue/65199, CL 603055 -->
Go 1.24 adiciona uma nova diretiva `go:wasmexport` para programas Go exportarem
funções para o host WebAssembly, e suporta a compilação de um programa Go como um
[reactor/library](https://github.com/WebAssembly/WASI/blob/63a46f61052a21bfab75a76558485cf097c0dbba/legacy/application-abi.md#current-unstable-abi) WASI.
Leia mais sobre [WebAssembly](/doc/go1.24#wasm) nas notas de lançamento.

---


Por favor leia as [notas de lançamento do Go 1.24](/doc/go1.24) para informações
completas e detalhadas. Não esqueça de ficar atento aos posts de blog subsequentes que
entrarão em mais profundidade em alguns dos tópicos mencionados aqui!

Obrigado a todos que contribuíram para este lançamento escrevendo código e
documentação, reportando bugs, compartilhando feedback e testando os release
candidates. Seus esforços ajudaram a garantir que Go 1.24 seja o mais estável possível.
Como sempre, se você notar qualquer problema, por favor [abra uma issue](/issue/new).

Aproveite o Go 1.24!

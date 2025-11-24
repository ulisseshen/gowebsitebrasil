---
ia-translated: true
title: Go 1.23 foi lançado
date: 2024-08-13
by:
- Dmitri Shuralyov, em nome da equipe Go
summary: Go 1.23 adiciona iterators, continua melhorias em loops, melhora compatibilidade e muito mais.
---

Hoje a equipe Go está feliz em lançar o Go 1.23,
que você pode obter visitando a [página de download](/dl/).

Se você já tem Go 1.22 ou Go 1.21 instalado em sua máquina,
você também pode tentar `go get toolchain@go1.23.0` em um módulo existente.
Isso baixará o novo toolchain e permitirá que você comece a usá-lo
em seu módulo imediatamente. Em algum momento posterior, você pode continuar
com `go get go@1.23.0` quando estiver pronto para mudar completamente para Go 1.23
e ter essa como a versão mínima requerida de Go do seu módulo.
Veja [Gerenciando requisitos de versão do módulo Go com go get](/doc/toolchain#get)
para mais informações sobre esta funcionalidade.

Go 1.23 vem com muitas melhorias em relação ao Go 1.22. Alguns dos destaques incluem:

## Mudanças na linguagem

-	<!-- go.dev/issue/61405, go.dev/issue/61897, go.dev/issue/61899, go.dev/issue/61900 -->
	Expressões range em um loop "for-range" agora podem ser funções iterator,
	como `func(func(K) bool)`.
	Isso suporta iterators definidos pelo usuário sobre sequências arbitrárias.
	Há várias adições aos pacotes padrão `slices` e `maps`
	que funcionam com iterators, bem como um novo pacote `iter`.
	Como exemplo, se você deseja coletar as chaves de um map `m` em um slice
	e então ordenar seus valores, você pode fazer isso no Go 1.23 com `slices.Sorted(maps.Keys(m))`.

	Go 1.23 também inclui suporte de preview para generic type aliases.

	Leia mais sobre [mudanças na linguagem](/doc/go1.23#language) e [iterators](/doc/go1.23#iterators)
	nas notas de lançamento.

## Melhorias nas ferramentas

-	<!-- go.dev/issue/58894 -->
	Começando com Go 1.23, é possível para o toolchain Go coletar estatísticas de uso e falhas
	para ajudar a entender como o toolchain Go é usado, e quão bem está funcionando.
	Esta é a telemetria Go, um _sistema opt-in_. Por favor considere optar por nos ajudar a manter Go
	funcionando bem e entender melhor o uso de Go.
	Leia mais sobre [telemetria Go](/doc/go1.23#telemetry) nas notas de lançamento.
-	O comando `go` tem novas conveniências. Por exemplo, executar `go env -changed` facilita
	ver apenas aquelas configurações cujo valor efetivo difere do valor padrão, e
	`go mod tidy -diff` ajuda a determinar as mudanças necessárias nos arquivos go.mod e go.sum
	sem modificá-los.
	Leia mais sobre o [comando Go](/doc/go1.23#go-command) nas notas de lançamento.
-	O subcomando `go vet` agora reporta símbolos que são muito novos para a versão Go pretendida.
	Leia mais sobre [ferramentas](/doc/go1.23#tools) nas notas de lançamento.

## Melhorias na biblioteca padrão

-	Go 1.23 melhora a implementação de `time.Timer` e `time.Ticker`.
	Leia mais sobre [mudanças em timer](/doc/go1.23#timer-changes) nas notas de lançamento.
- 	Há um total de 3 novos pacotes na biblioteca padrão do Go 1.23: `iter`, `structs` e `unique`.
	O pacote `iter` é mencionado acima.
	O pacote `structs` define tipos marcadores para modificar as propriedades de um struct.
	O pacote `unique` fornece facilidades para canonicalizar ("internar") valores
	comparáveis.
	Leia mais sobre [novos pacotes da biblioteca padrão](/doc/go1.23#new-unique-package)
	nas notas de lançamento.
-	Há muitas melhorias e adições à biblioteca padrão enumeradas
	na seção [mudanças menores na biblioteca](/doc/go1.23#minor_library_changes)
	das notas de lançamento.
	A documentação "Go, Backwards Compatibility, and GODEBUG"
	enumera [novas configurações GODEBUG do Go 1.23](/doc/godebug#go-123).
-	<!-- go.dev/issue/65573 -->
	Go 1.23 suporta a nova diretiva `godebug` em arquivos `go.mod` e `go.work` para
	permitir controle separado dos GODEBUGs padrão e da diretiva "go" do `go.mod`,
	além dos comentários de diretiva `//go:debug` disponibilizados há dois lançamentos (Go 1.21).
	Veja a documentação atualizada sobre [Valores GODEBUG Padrão](/doc/godebug#default).

## Mais melhorias e mudanças

-	Go 1.23 adiciona suporte experimental para OpenBSD em RISC-V de 64 bits (`openbsd/riscv64`).
	Há várias mudanças menores relevantes para Linux, macOS, ARM64, RISC-V e WASI.
	Leia mais sobre [ports](/doc/go1.23#ports) nas notas de lançamento.
-	O tempo de compilação ao usar otimização guiada por perfil (PGO) é reduzido, e a performance
	com PGO em arquiteturas 386 e amd64 é melhorada.
	Leia mais sobre [runtime, compilador e linker](/doc/go1.23#runtime) nas notas de lançamento.

Encorajamos todos a ler as [notas de lançamento do Go 1.23](/doc/go1.23) para
informações completas e detalhadas sobre essas mudanças, e tudo o mais que é
novo no Go 1.23.

Nas próximas semanas, fique atento a posts de blog subsequentes que entrarão em mais profundidade
em alguns dos tópicos mencionados aqui, incluindo "range-over-func", o novo pacote `unique`,
mudanças na implementação de timer do Go 1.23, e muito mais.

---

Obrigado a todos que contribuíram para este lançamento escrevendo código e
documentação, reportando bugs, compartilhando feedback e testando os release
candidates. Seus esforços ajudaram a garantir que Go 1.23 seja o mais estável possível.
Como sempre, se você notar qualquer problema, por favor [abra uma issue](/issue/new).

Aproveite o Go 1.23!

---
ia-translated: true
title: "Comentários de Documentação no Go"
layout: article
date: 2022-06-01T00:00:00Z
---

Índice:

 [Packages](#package)\
 [Comandos](#cmd)\
 [Tipos](#type)\
 [Funcs](#func)\
 [Consts](#const)\
 [Vars](#var)\
 [Sintaxe](#syntax)\
 [Erros comuns e armadilhas](#mistakes)

"Doc comments" (comentários de documentação) são comentários que aparecem imediatamente antes de declarações de package, const, func, type e var de nível superior sem novas linhas intermediárias.
Todo nome exportado (começando com letra maiúscula) deve ter um doc comment.

Os packages [go/doc](/pkg/go/doc) e [go/doc/comment](/pkg/go/doc/comment)
fornecem a capacidade de extrair documentação do código fonte Go,
e uma variedade de ferramentas fazem uso desta funcionalidade.
O comando [`go` `doc`](/cmd/go#hdr-Show_documentation_for_package_or_symbol)
procura e imprime o doc comment de um dado package ou símbolo.
(Um símbolo é uma const, func, type ou var de nível superior.)
O servidor web [pkg.go.dev](https://pkg.go.dev/) mostra a documentação
para packages Go públicos (quando suas licenças permitem esse uso).
O programa que serve aquele site é
[golang.org/x/pkgsite/cmd/pkgsite](https://pkg.go.dev/golang.org/x/pkgsite/cmd/pkgsite),
que também pode ser executado localmente para ver documentação para módulos privados
ou sem conexão com a internet.
O language server [gopls](https://pkg.go.dev/golang.org/x/tools/gopls)
fornece documentação ao editar arquivos fonte Go em IDEs.

O restante desta página documenta como escrever doc comments no Go.

## Packages {#package}

Todo package deve ter um package comment introduzindo o package.
Ele fornece informações relevantes ao package como um todo
e geralmente define expectativas para o package.
Especialmente em packages grandes, pode ser útil que o package comment
dê uma breve visão geral das partes mais importantes da API,
linkando para outros doc comments conforme necessário.

Se o package é simples, o package comment pode ser breve.
Por exemplo:

	// Package path implements utility routines for manipulating slash-separated
	// paths.
	//
	// The path package should only be used for paths separated by forward
	// slashes, such as the paths in URLs. This package does not deal with
	// Windows paths with drive letters or backslashes; to manipulate
	// operating system paths, use the [path/filepath] package.
	package path

Os colchetes em `[path/filepath]` criam um [link de documentação](#links).

Como pode ser visto neste exemplo, doc comments do Go usam sentenças completas.
Para um package comment, isso significa que a [primeira sentença](/pkg/go/doc/#Package.Synopsis)
começa com "Package <nome>".

Para packages com múltiplos arquivos, o package comment deve estar em apenas um arquivo fonte.
Se múltiplos arquivos têm package comments, eles são concatenados para formar um
único comentário grande para o package inteiro.

## Comandos {#cmd}

Um package comment para um comando é similar, mas ele descreve o comportamento
do programa em vez dos símbolos Go no package.
A primeira sentença convencionalmente começa com o nome do programa em si,
com letra maiúscula porque está no início de uma sentença.
Por exemplo, aqui está uma versão resumida do package comment para [gofmt](/cmd/gofmt):

	/*
	Gofmt formats Go programs.
	It uses tabs for indentation and blanks for alignment.
	Alignment assumes that an editor is using a fixed-width font.

	Without an explicit path, it processes the standard input. Given a file,
	it operates on that file; given a directory, it operates on all .go files in
	that directory, recursively. (Files starting with a period are ignored.)
	By default, gofmt prints the reformatted sources to standard output.

	Usage:

		gofmt [flags] [path ...]

	The flags are:

		-d
			Do not print reformatted sources to standard output.
			If a file's formatting is different than gofmt's, print diffs
			to standard output.
		-w
			Do not print reformatted sources to standard output.
			If a file's formatting is different from gofmt's, overwrite it
			with gofmt's version. If an error occurred during overwriting,
			the original file is restored from an automatic backup.

	When gofmt reads from standard input, it accepts either a full Go program
	or a program fragment. A program fragment must be a syntactically
	valid declaration list, statement list, or expression. When formatting
	such a fragment, gofmt preserves leading indentation as well as leading
	and trailing spaces, so that individual sections of a Go program can be
	formatted by piping them through gofmt.
	*/
	package main

O início do comentário é escrito usando
[semantic linefeeds](https://rhodesmill.org/brandon/2012/one-sentence-per-line/),
em que cada nova sentença ou frase longa está em uma linha própria,
o que pode tornar diffs mais fáceis de ler à medida que código e comentários evoluem.
Os parágrafos posteriores não seguem esta convenção
e foram quebrados manualmente.
O que for melhor para sua codebase está bom.
De qualquer forma, `go` `doc` e `pkgsite` re-quebram o texto do doc comment ao imprimi-lo.
Por exemplo:

	$ go doc gofmt
	Gofmt formats Go programs. It uses tabs for indentation and blanks for
	alignment. Alignment assumes that an editor is using a fixed-width font.

	Without an explicit path, it processes the standard input. Given a file, it
	operates on that file; given a directory, it operates on all .go files in that
	directory, recursively. (Files starting with a period are ignored.) By default,
	gofmt prints the reformatted sources to standard output.

	Usage:

		gofmt [flags] [path ...]

	The flags are:

		-d
			Do not print reformatted sources to standard output.
			If a file's formatting is different than gofmt's, print diffs
			to standard output.
	...

As linhas indentadas são tratadas como texto pré-formatado:
elas não são re-quebradas e são impressas em fonte de código
em apresentações HTML e Markdown.
(A seção [Sintaxe](#syntax) abaixo dá os detalhes.)

## Tipos {#type}

O doc comment de um tipo deve explicar o que cada instância daquele tipo representa ou fornece.
Se a API é simples, o doc comment pode ser bem curto.
Por exemplo:

	package zip

	// A Reader serves content from a ZIP archive.
	type Reader struct {
		...
	}

Por padrão, programadores devem esperar que um tipo seja seguro para uso apenas por
uma única goroutine por vez.
Se um tipo fornece garantias mais fortes, o doc comment deve declarar isso.
Por exemplo:

	package regexp

	// Regexp is the representation of a compiled regular expression.
	// A Regexp is safe for concurrent use by multiple goroutines,
	// except for configuration methods, such as Longest.
	type Regexp struct {
		...
	}

Tipos Go também devem buscar fazer o valor zero ter um significado útil.
Se não for óbvio, esse significado deve ser documentado. Por exemplo:

	package bytes

	// A Buffer is a variable-sized buffer of bytes with Read and Write methods.
	// The zero value for Buffer is an empty buffer ready to use.
	type Buffer struct {
		...
	}

Para uma struct com campos exportados, ou o doc comment ou comentários por campo
devem explicar o significado de cada campo exportado.
Por exemplo, o doc comment deste tipo explica os campos:

{{raw `
	package io

	// A LimitedReader reads from R but limits the amount of
	// data returned to just N bytes. Each call to Read
	// updates N to reflect the new amount remaining.
	// Read returns EOF when N <= 0.
	type LimitedReader struct {
		R   Reader // underlying reader
		N   int64  // max bytes remaining
	}
`}}

Em contraste, o doc comment deste tipo deixa as explicações para comentários por campo:

{{raw `
	package comment

	// A Printer is a doc comment printer.
	// The fields in the struct can be filled in before calling
	// any of the printing methods
	// in order to customize the details of the printing process.
	type Printer struct {
		// HeadingLevel is the nesting level used for
		// HTML and Markdown headings.
		// If HeadingLevel is zero, it defaults to level 3,
		// meaning to use <h3> and ###.
		HeadingLevel int
		...
	}
`}}

Assim como para packages (acima) e funcs (abaixo), doc comments para tipos
começam com sentenças completas nomeando o símbolo declarado.
Um sujeito explícito frequentemente torna o texto mais claro,
e torna o texto mais fácil de buscar, seja em uma página web
ou na linha de comando.
Por exemplo:

	$ go doc -all regexp | grep pairs
	pairs within the input string: result[2*n:2*n+2] identifies the indexes
	    FindReaderSubmatchIndex returns a slice holding the index pairs identifying
	    FindStringSubmatchIndex returns a slice holding the index pairs identifying
	    FindSubmatchIndex returns a slice holding the index pairs identifying the
	$

## Funcs {#func}

O doc comment de uma função deve explicar o que a função retorna
ou, para funções chamadas por efeitos colaterais, o que ela faz.
Parâmetros e resultados nomeados podem ser referidos diretamente no
comentário, sem nenhuma sintaxe especial como crase.
(Uma consequência desta convenção é que nomes como `a`,
que podem ser confundidos com palavras comuns, são tipicamente evitados.)
Por exemplo:

	package strconv

	// Quote returns a double-quoted Go string literal representing s.
	// The returned string uses Go escape sequences (\t, \n, \xFF, \u0100)
	// for control characters and non-printable characters as defined by IsPrint.
	func Quote(s string) string {
		...
	}

E:

	package os

	// Exit causes the current program to exit with the given status code.
	// Conventionally, code zero indicates success, non-zero an error.
	// The program terminates immediately; deferred functions are not run.
	//
	// For portability, the status code should be in the range [0, 125].
	func Exit(code int) {
		...
	}

Doc comments tipicamente usam a frase "reports whether" (reporta se)
para descrever funções que retornam um boolean.
A frase "or not" (ou não) é desnecessária.
Por exemplo:

	package strings

	// HasPrefix reports whether the string s begins with prefix.
	func HasPrefix(s, prefix string) bool

Se um doc comment precisa explicar múltiplos resultados,
nomear os resultados pode tornar o doc comment mais compreensível,
mesmo se os nomes não forem usados no corpo da função.
Por exemplo:

	package io

	// Copy copies from src to dst until either EOF is reached
	// on src or an error occurs. It returns the total number of bytes
	// written and the first error encountered while copying, if any.
	//
	// A successful Copy returns err == nil, not err == EOF.
	// Because Copy is defined to read from src until EOF, it does
	// not treat an EOF from Read as an error to be reported.
	func Copy(dst Writer, src Reader) (n int64, err error) {
		...
	}

Inversamente, quando os resultados não precisam ser nomeados no doc comment,
eles geralmente são omitidos no código também, como no exemplo `Quote` acima,
para evitar poluir a apresentação.

Essas regras se aplicam tanto a funções simples quanto a métodos.
Para métodos, usar o mesmo nome de receiver evita
variação desnecessária ao listar todos os métodos de um tipo:

	$ go doc bytes.Buffer
	package bytes // import "bytes"

	type Buffer struct {
		// Has unexported fields.
	}
	    A Buffer is a variable-sized buffer of bytes with Read and Write methods.
	    The zero value for Buffer is an empty buffer ready to use.

	func NewBuffer(buf []byte) *Buffer
	func NewBufferString(s string) *Buffer
	func (b *Buffer) Bytes() []byte
	func (b *Buffer) Cap() int
	func (b *Buffer) Grow(n int)
	func (b *Buffer) Len() int
	func (b *Buffer) Next(n int) []byte
	func (b *Buffer) Read(p []byte) (n int, err error)
	func (b *Buffer) ReadByte() (byte, error)
	...

Este exemplo também mostra que funções de nível superior retornando um tipo `T` ou ponteiro `*T`,
talvez com um resultado de erro adicional,
são mostradas junto com o tipo `T` e seus métodos,
sob a suposição de que são construtores de `T`.

Por padrão, programadores podem assumir que uma função de nível superior
é segura para chamar de múltiplas goroutines;
este fato não precisa ser declarado explicitamente.

Por outro lado, como notado na seção anterior,
usar uma instância de um tipo de qualquer maneira,
incluindo chamar um método, é tipicamente assumido
como sendo restrito a uma única goroutine por vez.
Se os métodos que são seguros para uso concorrente
não estão documentados no doc comment do tipo,
eles devem ser documentados em comentários por método.
Por exemplo:

	package sql

	// Close returns the connection to the connection pool.
	// All operations after a Close will return with ErrConnDone.
	// Close is safe to call concurrently with other operations and will
	// block until all other operations finish. It may be useful to first
	// cancel any used context and then call Close directly after.
	func (c *Conn) Close() error {
		...
	}

Note que doc comments de funções e métodos focam em
o que a operação retorna ou faz,
detalhando o que o chamador precisa saber.
Casos especiais podem ser particularmente importantes de documentar.
Por exemplo:

{{raw `
	package math

	// Sqrt returns the square root of x.
	//
	// Special cases are:
	//
	//	Sqrt(+Inf) = +Inf
	//	Sqrt(±0) = ±0
	//	Sqrt(x < 0) = NaN
	//	Sqrt(NaN) = NaN
	func Sqrt(x float64) float64 {
		...
	}
`}}

Doc comments não devem explicar detalhes internos
como o algoritmo usado na implementação atual.
Esses são melhor deixados para comentários dentro do corpo da função.
Pode ser apropriado dar limites assintóticos de tempo ou espaço
quando esse detalhe é particularmente importante para chamadores.
Por exemplo:

	package sort

	// Sort sorts data in ascending order as determined by the Less method.
	// It makes one call to data.Len to determine n and O(n*log(n)) calls to
	// data.Less and data.Swap. The sort is not guaranteed to be stable.
	func Sort(data Interface) {
		...
	}

Porque este doc comment não menciona qual algoritmo de ordenação é usado,
é mais fácil mudar a implementação para usar um algoritmo diferente no futuro.

## Consts {#const}

A sintaxe de declaração do Go permite agrupamento de declarações,
caso em que um único doc comment pode introduzir um grupo de constantes relacionadas,
com constantes individuais apenas documentadas por curtos comentários de fim de linha.
Por exemplo:

	package scanner // import "text/scanner"

	// The result of Scan is one of these tokens or a Unicode character.
	const (
		EOF = -(iota + 1)
		Ident
		Int
		Float
		Char
		...
	)

Às vezes o grupo não precisa de doc comment algum. Por exemplo:

	package unicode // import "unicode"

	const (
		MaxRune         = '\U0010FFFF' // maximum valid Unicode code point.
		ReplacementChar = '\uFFFD'     // represents invalid code points.
		MaxASCII        = '\u007F'     // maximum ASCII value.
		MaxLatin1       = '\u00FF'     // maximum Latin-1 value.
	)

Por outro lado, constantes desagrupadas tipicamente justificam um
doc comment completo começando com uma sentença completa. Por exemplo:

	package unicode

	// Version is the Unicode edition from which the tables are derived.
	const Version = "13.0.0"

Constantes tipadas são exibidas junto à declaração de seu tipo
e como resultado frequentemente omitem um doc comment de grupo const em favor do
doc comment do tipo.
Por exemplo:

	package syntax

	// An Op is a single regular expression operator.
	type Op uint8

	const (
		OpNoMatch        Op = 1 + iota // matches no strings
		OpEmptyMatch                   // matches empty string
		OpLiteral                      // matches Runes sequence
		OpCharClass                    // matches Runes interpreted as range pair list
		OpAnyCharNotNL                 // matches any character except newline
		...
	)

(Veja [pkg.go.dev/regexp/syntax#Op](https://pkg.go.dev/regexp/syntax#Op) para a apresentação HTML.)

## Vars {#var}

As convenções para variáveis são as mesmas para constantes.
Por exemplo, aqui está um conjunto de variáveis agrupadas:

	package fs

	// Generic file system errors.
	// Errors returned by file systems can be tested against these errors
	// using errors.Is.
	var (
		ErrInvalid    = errInvalid()    // "invalid argument"
		ErrPermission = errPermission() // "permission denied"
		ErrExist      = errExist()      // "file already exists"
		ErrNotExist   = errNotExist()   // "file does not exist"
		ErrClosed     = errClosed()     // "file already closed"
	)

E uma variável única:

	package unicode

	// Scripts is the set of Unicode script tables.
	var Scripts = map[string]*RangeTable{
		"Adlam":                  Adlam,
		"Ahom":                   Ahom,
		"Anatolian_Hieroglyphs":  Anatolian_Hieroglyphs,
		"Arabic":                 Arabic,
		"Armenian":               Armenian,
		...
	}

## Sintaxe {#syntax}

Doc comments do Go são escritos em uma sintaxe simples que suporta
parágrafos, cabeçalhos, links, listas e blocos de código pré-formatados.
Para manter comentários leves e legíveis em arquivos fonte,
não há suporte para recursos complexos como mudanças de fonte ou HTML bruto.
Aficionados por Markdown podem ver a sintaxe como um subconjunto simplificado de Markdown.

O formatador padrão [gofmt](/cmd/gofmt) reformata doc comments
para usar uma formatação canônica para cada um desses recursos.
Gofmt busca legibilidade e controle do usuário sobre como comentários
são escritos no código fonte, mas ajustará a apresentação para fazer
o significado semântico de um comentário particular mais claro,
analogamente a reformatar `1+2 * 3` para `1 + 2*3` em código fonte comum.

Gofmt remove linhas em branco iniciais e finais em doc comments.
Se todas as linhas em um doc comment começam com a mesma sequência de
espaços e tabs, gofmt remove esse prefixo.

### Parágrafos {#paragraphs}

Um parágrafo é um intervalo de linhas não indentadas e não vazias.
Já vimos muitos exemplos de parágrafos.

Um par de crases consecutivas (\` U+0060)
é interpretado como uma aspas esquerda Unicode (" U+201C),
e um par de aspas simples consecutivas (\' U+0027)
é interpretado como uma aspas direita Unicode (" U+201D).

Gofmt preserva quebras de linha em texto de parágrafo: ele não re-quebra o texto.
Isso permite o uso de [semantic linefeeds](https://rhodesmill.org/brandon/2012/one-sentence-per-line/),
como visto anteriormente.
Gofmt substitui linhas em branco duplicadas entre parágrafos
com uma única linha em branco.
Gofmt também reformata crases ou aspas simples consecutivas
para suas interpretações Unicode.

#### Notes {#notes}

Notes são comentários especiais da forma `MARKER(uid): body`.
MARKER deve consistir de 2 ou mais letras maiúsculas `[A-Z]`,
identificando o tipo de nota, enquanto uid é pelo menos 1 caractere,
geralmente um nome de usuário de alguém que pode fornecer mais informações.
O `:` seguindo o uid é opcional.

Notes são coletadas e renderizadas em sua própria seção no pkg.go.dev.

Por exemplo:

	// TODO(user1): refactor to use standard library context
	// BUG(user2): not cleaned up
	var ctx context.Context

#### Deprecações {#deprecations}

Parágrafos começando com `Deprecated: ` são tratados como avisos de deprecação.
Algumas ferramentas avisarão quando identificadores deprecated forem usados.
[pkg.go.dev](https://pkg.go.dev) esconderá seus docs por padrão.

Avisos de deprecação são seguidos por algumas informações sobre a deprecação,
e uma recomendação sobre o que usar em vez disso, se aplicável.
O parágrafo não precisa ser o último parágrafo no doc comment.

Por exemplo:

	// Package rc4 implements the RC4 stream cipher.
	//
	// Deprecated: RC4 is cryptographically broken and should not be used
	// except for compatibility with legacy systems.
	//
	// This package is frozen and no new functionality will be added.
	package rc4

	// Reset zeros the key data and makes the Cipher unusable.
	//
	// Deprecated: Reset can't guarantee that the key will be entirely removed from
	// the process's memory.
	func (c *Cipher) Reset()

### Cabeçalhos {#headings}

Um cabeçalho é uma linha começando com um sinal de número (U+0023) e depois um espaço e o texto do cabeçalho.
Para ser reconhecida como um cabeçalho, a linha deve estar não indentada e separada do texto de parágrafo adjacente
por linhas em branco.

Por exemplo:

	// Package strconv implements conversions to and from string representations
	// of basic data types.
	//
	// # Numeric Conversions
	//
	// The most common numeric conversions are [Atoi] (string to int) and [Itoa] (int to string).
	...
	package strconv

Por outro lado:

	// #This is not a heading, because there is no space.
	//
	// # This is not a heading,
	// # because it is multiple lines.
	//
	// # This is not a heading,
	// because it is also multiple lines.
	//
	// The next paragraph is not a heading, because there is no additional text:
	//
	// #
	//
	// In the middle of a span of non-blank lines,
	// # this is not a heading either.
	//
	//     # This is not a heading, because it is indented.

A sintaxe # foi adicionada no Go 1.19.
Antes do Go 1.19, cabeçalhos eram identificados implicitamente por parágrafos de uma única linha
satisfazendo certas condições, mais notavelmente a falta de qualquer pontuação final.

Gofmt reformata [linhas tratadas como cabeçalhos implícitos](https://github.com/golang/proposal/blob/master/design/51082-godocfmt.md#headings)
por versões anteriores do Go para usar cabeçalhos # em vez disso.
Se a reformatação não for apropriada—isto é, se a linha não era para ser um cabeçalho—a maneira mais fácil
de torná-la um parágrafo é introduzir pontuação final
como um ponto ou dois pontos, ou quebrá-la em duas linhas.

### Links {#links}

Um intervalo de linhas não indentadas e não vazias define alvos de link
quando cada linha é da forma "[Texto]: URL".
Em outro texto no mesmo doc comment,
"[Texto]" representa um link para URL usando o texto dado—em HTML,
\<a href="URL">Texto\</a>.
Por exemplo:

	// Package json implements encoding and decoding of JSON as defined in
	// [RFC 7159]. The mapping between JSON and Go values is described
	// in the documentation for the Marshal and Unmarshal functions.
	//
	// For an introduction to this package, see the article
	// "[JSON and Go]."
	//
	// [RFC 7159]: https://tools.ietf.org/html/rfc7159
	// [JSON and Go]: https://golang.org/doc/articles/json_and_go.html
	package json

Ao manter URLs em uma seção separada,
este formato interrompe minimamente o fluxo do texto real.
Ele também corresponde aproximadamente ao
[formato de link de referência encurtado do Markdown](https://spec.commonmark.org/0.30/#shortcut-reference-link),
sem o texto de título opcional.

Se não houver declaração de URL correspondente,
então (exceto para doc links, descritos na próxima seção)
"[Texto]" não é um hiperlink, e os colchetes são preservados
quando exibidos.
Cada doc comment é considerado independentemente:
definições de alvos de link em um comentário não afetam outros comentários.

Embora blocos de definição de alvos de link possam ser intercalados com
parágrafos comuns, gofmt move todas as definições de alvos de link para
o final do doc comment,
em até dois blocos: primeiro um bloco contendo todos os alvos de link
que são referenciados no comentário, e depois um bloco
contendo todos os alvos _não_ referenciados no comentário.
O bloco separado torna alvos não usados fáceis
de notar e corrigir (caso os links ou as definições tenham erros)
ou deletar (caso as definições não sejam mais necessárias).

Texto simples que é reconhecido como uma URL é automaticamente linkado em renderizações HTML.

### Doc links {#doclinks}

Doc links são links da forma "[Nome1]" ou "[Nome1.Nome2]" para referir-se
a identificadores exportados no package atual, ou "[pkg]",
"[pkg.Nome1]", ou "[pkg.Nome1.Nome2]" para referir-se a identificadores em outros
packages.

Por exemplo:

	package bytes

	// ReadFrom reads data from r until EOF and appends it to the buffer, growing
	// the buffer as needed. The return value n is the number of bytes read. Any
	// error except [io.EOF] encountered during the read is also returned. If the
	// buffer becomes too large, ReadFrom will panic with [ErrTooLarge].
	func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error) {
		...
	}

O texto entre colchetes para um link de símbolo
pode incluir um asterisco inicial opcional, tornando fácil referir-se a
tipos de ponteiro, como \[\*bytes.Buffer\].

Ao referir-se a outros packages, "pkg" pode ser tanto um caminho de import completo
quanto o nome de package assumido de um import existente. O nome de package assumido
é ou o identificador em um import renomeado ou então
[o nome assumido por
goimports](https://pkg.go.dev/golang.org/x/tools/internal/imports#ImportPathToAssumedName).
(Goimports insere renomeações quando essa suposição não está correta, então
esta regra deve funcionar para essencialmente todo código Go.)
Por exemplo, se o package atual importa encoding/json,
então "[json.Decoder]" pode ser escrito no lugar de "[encoding/json.Decoder]"
para linkar para os docs do Decoder do encoding/json.
Se diferentes arquivos fonte em um package importam diferentes packages usando o mesmo nome,
então o atalho é ambíguo e não pode ser usado.

Um "pkg" é apenas
assumido ser um caminho de import completo se começar com um nome de domínio (um
elemento de caminho com um ponto) ou for um dos packages da biblioteca
padrão ("[os]", "[encoding/json]", e assim por diante).
Por exemplo, `[os.File]` e `[example.com/sys.File]` são links de documentação
(o último será um link quebrado),
mas `[os/sys.File]` não é, porque não há package os/sys na biblioteca padrão.

Para evitar problemas com
maps, generics e tipos de array, doc links devem ser tanto precedidos quanto
seguidos por pontuação, espaços, tabs, ou o início ou fim de uma linha.
Por exemplo, o texto "map[ast.Expr]TypeAndValue" não contém
um doc link.

### Listas {#lists}

Uma lista é um intervalo de linhas indentadas ou vazias
(que de outra forma seria um bloco de código,
como descrito na próxima seção)
em que a primeira linha indentada começa com
um marcador de lista com bullets ou um marcador de lista numerada.

Um marcador de lista com bullets é uma estrela, mais, traço ou bullet Unicode
(*, +, -, •; U+002A, U+002B, U+002D, U+2022)
seguido por um espaço ou tab e depois texto.
Em uma lista com bullets, cada linha começando com um marcador de lista com bullets
inicia um novo item de lista.

Por exemplo:

	package url

	// PublicSuffixList provides the public suffix of a domain. For example:
	//   - the public suffix of "example.com" is "com",
	//   - the public suffix of "foo1.foo2.foo3.co.uk" is "co.uk", and
	//   - the public suffix of "bar.pvt.k12.ma.us" is "pvt.k12.ma.us".
	//
	// Implementations of PublicSuffixList must be safe for concurrent use by
	// multiple goroutines.
	//
	// An implementation that always returns "" is valid and may be useful for
	// testing but it is not secure: it means that the HTTP server for foo.com can
	// set a cookie for bar.com.
	//
	// A public suffix list implementation is in the package
	// golang.org/x/net/publicsuffix.
	type PublicSuffixList interface {
		...
	}

Um marcador de lista numerada é um número decimal de qualquer comprimento
seguido por um ponto ou parêntese direito, depois um espaço ou tab, e depois texto.
Em uma lista numerada, cada linha começando com um marcador de lista de número inicia um novo item de lista.
Números de itens são deixados como estão, nunca renumerados.

Por exemplo:

	package path

	// Clean returns the shortest path name equivalent to path
	// by purely lexical processing. It applies the following rules
	// iteratively until no further processing can be done:
	//
	//  1. Replace multiple slashes with a single slash.
	//  2. Eliminate each . path name element (the current directory).
	//  3. Eliminate each inner .. path name element (the parent directory)
	//     along with the non-.. element that precedes it.
	//  4. Eliminate .. elements that begin a rooted path:
	//     that is, replace "/.." by "/" at the beginning of a path.
	//
	// The returned path ends in a slash only if it is the root "/".
	//
	// If the result of this process is an empty string, Clean
	// returns the string ".".
	//
	// See also Rob Pike, "[Lexical File Names in Plan 9]."
	//
	// [Lexical File Names in Plan 9]: https://9p.io/sys/doc/lexnames.html
	func Clean(path string) string {
		...
	}

Itens de lista apenas contêm parágrafos, não blocos de código ou listas aninhadas.
Isso evita qualquer sutileza de contagem de espaços, bem como questões sobre
quantos espaços um tab conta em indentação inconsistente.

Gofmt reformata listas com bullets para usar um traço como marcador de bullet,
dois espaços de indentação antes do traço,
e quatro espaços de indentação para linhas de continuação.

Gofmt reformata listas numeradas para usar um único espaço antes do número,
um ponto após o número, e novamente
quatro espaços de indentação para linhas de continuação.

Gofmt preserva mas não requer uma linha em branco entre uma lista e o parágrafo precedente.
Ele insere uma linha em branco entre uma lista e o parágrafo ou cabeçalho seguinte.

### Blocos de código {#code}

Um bloco de código é um intervalo de linhas indentadas ou vazias
não começando com um marcador de lista com bullets ou marcador de lista numerada.
Ele é renderizado como texto pré-formatado (um bloco \<pre> em HTML).

Blocos de código frequentemente contêm código Go. Por exemplo:

{{raw `
	package sort

	// Search uses binary search...
	//
	// As a more whimsical example, this program guesses your number:
	//
	//	func GuessingGame() {
	//		var s string
	//		fmt.Printf("Pick an integer from 0 to 100.\n")
	//		answer := sort.Search(100, func(i int) bool {
	//			fmt.Printf("Is your number <= %d? ", i)
	//			fmt.Scanf("%s", &s)
	//			return s != "" && s[0] == 'y'
	//		})
	//		fmt.Printf("Your number is %d.\n", answer)
	//	}
	func Search(n int, f func(int) bool) int {
		...
	}
`}}

Claro, blocos de código também frequentemente contêm texto pré-formatado além de código. Por exemplo:

{{raw `
	package path

	// Match reports whether name matches the shell pattern.
	// The pattern syntax is:
	//
	//	pattern:
	//		{ term }
	//	term:
	//		'*'         matches any sequence of non-/ characters
	//		'?'         matches any single non-/ character
	//		'[' [ '^' ] { character-range } ']'
	//		            character class (must be non-empty)
	//		c           matches character c (c != '*', '?', '\\', '[')
	//		'\\' c      matches character c
	//
	//	character-range:
	//		c           matches character c (c != '\\', '-', ']')
	//		'\\' c      matches character c
	//		lo '-' hi   matches character c for lo <= c <= hi
	//
	// Match requires pattern to match all of name, not just a substring.
	// The only possible returned error is [ErrBadPattern], when pattern
	// is malformed.
	func Match(pattern, name string) (matched bool, err error) {
		...
	}
`}}

Gofmt indenta todas as linhas em um bloco de código por um único tab,
substituindo qualquer outra indentação que as linhas não vazias tenham em comum.
Gofmt também insere uma linha em branco antes e depois de cada bloco de código,
distinguindo o bloco de código claramente do texto de parágrafo circundante.

### Diretivas {#directives}

Comentários de diretiva como `//go:generate` não são
considerados parte de um doc comment e são omitidos de
documentação renderizada.
Gofmt move comentários de diretiva para o final do doc comment,
precedidos por uma linha em branco.
Por exemplo:

	package regexp

	// An Op is a single regular expression operator.
	//
	//go:generate stringer -type Op -trimprefix Op
	type Op uint8

Um comentário de diretiva é uma linha começando com a expressão regular
`//(line |extern |export |[a-z0-9]+:[a-z0-9])`.

Ferramentas podem definir seus próprios comentários de diretiva usando a forma
`//toolname:directive arguments`.
Diretivas de ferramenta correspondem à expressão regular
`//([a-z0-9]+):([a-z0-9]\PZ*)($|\pZ+)(.*)`, onde o primeiro grupo
é o nome da ferramenta e o segundo grupo é o nome da diretiva.
Argumentos opcionais são separados do nome da diretiva por
um ou mais caracteres de espaço em branco Unicode.
Cada ferramenta pode definir sua própria sintaxe de argumento, mas uma convenção comum é uma
sequência de argumentos separados por espaços, onde um argumento pode ser
uma palavra simples, ou uma string Go entre aspas duplas ou crases.
O nome de ferramenta `go` é reservado para uso pela toolchain do Go.

A função [`go/ast.ParseDirective`](/pkg/go/ast#ParseDirective) e seus
tipos relacionados analisam a sintaxe de diretiva de ferramenta.

## Erros comuns e armadilhas {#mistakes}

A regra de que qualquer intervalo de linhas indentadas ou vazias
em um doc comment é renderizado como um bloco de código
data dos primeiros dias do Go.
Infelizmente, a falta de suporte para doc comments no gofmt
levou a muitos comentários existentes que usam indentação
sem a intenção de criar um bloco de código.

Por exemplo, esta lista não indentada sempre foi interpretada
pelo godoc como um parágrafo de três linhas seguido por um bloco de código de uma linha:

	package http

	// cancelTimerBody is an io.ReadCloser that wraps rc with two features:
	// 1) On Read error or close, the stop func is called.
	// 2) On Read failure, if reqDidTimeout is true, the error is wrapped and
	//    marked as net.Error that hit its timeout.
	type cancelTimerBody struct {
		...
	}

Isso sempre renderizou em `go` `doc` como:

	cancelTimerBody is an io.ReadCloser that wraps rc with two features:
	1) On Read error or close, the stop func is called. 2) On Read failure,
	if reqDidTimeout is true, the error is wrapped and

	    marked as net.Error that hit its timeout.

Similarmente, o comando neste comentário é um parágrafo de uma linha
seguido por um bloco de código de uma linha:

	package smtp

	// localhostCert is a PEM-encoded TLS cert generated from src/crypto/tls:
	//
	// go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \
	//     --ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h
	var localhostCert = []byte(`...`)

Isso renderizou em `go` `doc` como:

	localhostCert is a PEM-encoded TLS cert generated from src/crypto/tls:

	go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \

	    --ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h

E este comentário é um parágrafo de duas linhas (a segunda linha é "{"),
seguido por um bloco de código indentado de seis linhas e um parágrafo de uma linha ("}").

	// On the wire, the JSON will look something like this:
	// {
	//	"kind":"MyAPIObject",
	//	"apiVersion":"v1",
	//	"myPlugin": {
	//		"kind":"PluginA",
	//		"aOption":"foo",
	//	},
	// }

E isso renderizou em `go` `doc` como:

	On the wire, the JSON will look something like this: {

	    "kind":"MyAPIObject",
	    "apiVersion":"v1",
	    "myPlugin": {
	    	"kind":"PluginA",
	    	"aOption":"foo",
	    },

	}

Outro erro comum era uma definição de função Go não indentada
ou declaração de bloco, similarmente delimitado por "{" e "}".

A introdução da reformatação de doc comment no gofmt do Go 1.19 torna erros
como esses mais visíveis ao adicionar linhas em branco ao redor dos blocos de código.

Análise em 2022 encontrou que apenas 3% dos doc comments em módulos Go públicos
foram reformatados de qualquer forma pelo rascunho do gofmt do Go 1.19.
Limitando-nos a esses comentários, cerca de 87% das reformatações do gofmt
preservaram a estrutura que uma pessoa inferiria ao ler o comentário;
cerca de 6% foram prejudicadas por esses tipos de listas não indentadas,
comandos shell multi-linha não indentados e blocos de código delimitados por chaves não indentados.

Com base nesta análise, o gofmt do Go 1.19 aplica algumas heurísticas para mesclar
linhas não indentadas em uma lista ou bloco de código indentado adjacente.
Com esses ajustes, o gofmt do Go 1.19 reformata os exemplos acima para:

	// cancelTimerBody is an io.ReadCloser that wraps rc with two features:
	//  1. On Read error or close, the stop func is called.
	//  2. On Read failure, if reqDidTimeout is true, the error is wrapped and
	//     marked as net.Error that hit its timeout.

	// localhostCert is a PEM-encoded TLS cert generated from src/crypto/tls:
	//
	//	go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \
	//	    --ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h

	// On the wire, the JSON will look something like this:
	//
	//	{
	//		"kind":"MyAPIObject",
	//		"apiVersion":"v1",
	//		"myPlugin": {
	//			"kind":"PluginA",
	//			"aOption":"foo",
	//		},
	//	}

Esta reformatação torna o significado mais claro, bem como fazendo os doc comments
renderizarem corretamente em versões anteriores do Go.
Se a heurística fizer uma má decisão, pode ser sobreposta inserindo
uma linha em branco para separar claramente o texto de parágrafo do texto de não-parágrafo.

Mesmo com essas heurísticas, outros comentários existentes precisarão de ajuste
manual para corrigir sua renderização.
O erro mais comum é indentar uma linha quebrada não indentada de texto.
Por exemplo:

	// TODO Revisit this design. It may make sense to walk those nodes
	//      only once.

	// According to the document:
	// "The alignment factor (in bytes) that is used to align the raw data of sections in
	//  the image file. The value should be a power of 2 between 512 and 64 K, inclusive."

Em ambos, a última linha está indentada, tornando-a um bloco de código.
A correção é desindentar as linhas.

Outro erro comum é não indentar uma linha quebrada indentada de uma lista ou bloco de código.
Por exemplo:

	// Uses of this error model include:
	//
	//   - Partial errors. If a service needs to return partial errors to the
	// client,
	//     it may embed the `Status` in the normal response to indicate the
	// partial
	//     errors.
	//
	//   - Workflow errors. A typical workflow has multiple steps. Each step
	// may
	//     have a `Status` message for error reporting.

A correção é indentar as linhas quebradas.

Doc comments do Go não suportam listas aninhadas, então o gofmt reformata

	// Here is a list:
	//
	//  - Item 1.
	//    * Subitem 1.
	//    * Subitem 2.
	//  - Item 2.
	//  - Item 3.

para

	// Here is a list:
	//
	//  - Item 1.
	//  - Subitem 1.
	//  - Subitem 2.
	//  - Item 2.
	//  - Item 3.

Reescrever o texto para evitar listas aninhadas geralmente
melhora a documentação e é a melhor solução.
Outra solução alternativa potencial é misturar marcadores de lista,
já que marcadores de bullets não introduzem itens de lista em uma lista numerada,
nem vice-versa.
Por exemplo:

	// Here is a list:
	//
	//  1. Item 1.
	//
	//     - Subitem 1.
	//
	//     - Subitem 2.
	//
	//  2. Item 2.
	//
	//  3. Item 3.

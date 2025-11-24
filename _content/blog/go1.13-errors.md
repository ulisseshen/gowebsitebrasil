---
ia-translated: true
title: Trabalhando com Errors no Go 1.13
date: 2019-10-17
by:
- Damien Neil and Jonathan Amsterdam
tags:
- errors
- technical
summary: Como usar as novas interfaces e funções de error do Go 1.13.
---

## Introdução

O tratamento de [erros como valores](/blog/errors-are-values) do Go
tem nos servido bem ao longo da última década. Embora o suporte da biblioteca padrão
para errors tenha sido mínimo—apenas as funções `errors.New` e `fmt.Errorf`,
que produzem errors que contêm apenas uma mensagem—a interface `error` embutida
permite que programadores Go adicionem qualquer informação que desejarem. Tudo o que ela requer
é um tipo que implemente um método `Error`:

	type QueryError struct {
		Query string
		Err   error
	}

	func (e *QueryError) Error() string { return e.Query + ": " + e.Err.Error() }

Tipos de error como este são onipresentes, e a informação que eles armazenam varia
amplamente, de timestamps a nomes de arquivos a endereços de servidor. Frequentemente, essa
informação inclui outro error de nível mais baixo para fornecer contexto adicional.

O padrão de um error contendo outro é tão difundido no código Go que,
após [extensa discussão](/issue/29934), o Go 1.13 adicionou
suporte explícito para ele. Este post descreve as adições à biblioteca
padrão que fornecem esse suporte: três novas funções no pacote `errors`,
e um novo verbo de formatação para `fmt.Errorf`.

Antes de descrever as mudanças em detalhes, vamos revisar como errors são examinados
e construídos em versões anteriores da linguagem.

## Errors antes do Go 1.13

### Examinando errors

Errors do Go são valores. Programas tomam decisões baseadas nesses valores de algumas
maneiras. A mais comum é comparar um error a `nil` para ver se uma operação
falhou.

	if err != nil {
		// something went wrong
	}

Às vezes comparamos um error a um valor _sentinel_ conhecido, para ver se um error específico ocorreu.

	var ErrNotFound = errors.New("not found")

	if err == ErrNotFound {
		// something wasn't found
	}

Um valor de error pode ser de qualquer tipo que satisfaça a interface `error`
definida pela linguagem. Um programa pode usar uma type assertion ou type switch para visualizar um valor de
error como um tipo mais específico.

	type NotFoundError struct {
		Name string
	}

	func (e *NotFoundError) Error() string { return e.Name + ": not found" }

	if e, ok := err.(*NotFoundError); ok {
		// e.Name wasn't found
	}

### Adicionando informação

Frequentemente uma função passa um error para cima na pilha de chamadas enquanto adiciona informação
a ele, como uma breve descrição do que estava acontecendo quando o error ocorreu. Uma
maneira simples de fazer isso é construir um novo error que inclua o texto do
anterior:

	if err != nil {
		return fmt.Errorf("decompress %v: %v", name, err)
	}

Criar um novo error com `fmt.Errorf` descarta tudo do error original
exceto o texto. Como vimos acima com `QueryError`, podemos às vezes querer
definir um novo tipo de error que contenha o error subjacente, preservando-o para
inspeção pelo código. Aqui está `QueryError` novamente:

	type QueryError struct {
		Query string
		Err   error
	}

Programas podem olhar dentro de um valor `*QueryError` para tomar decisões baseadas no
error subjacente. Você às vezes verá isso sendo referido como fazer "unwrap" do
error.

	if e, ok := err.(*QueryError); ok && e.Err == ErrPermission {
		// query failed because of a permission problem
	}

O tipo `os.PathError` na biblioteca padrão é outro exemplo de um error que contém outro.

## Errors no Go 1.13

### O método Unwrap

O Go 1.13 introduz novos recursos aos pacotes da biblioteca padrão `errors` e `fmt`
para simplificar o trabalho com errors que contêm outros errors. O mais
significativo deles é uma convenção ao invés de uma mudança: um error que
contém outro pode implementar um método `Unwrap` retornando o error
subjacente. Se `e1.Unwrap()` retorna `e2`, então dizemos que `e1` _envolve_ `e2`, e
que você pode fazer _unwrap_ de `e1` para obter `e2`.

Seguindo essa convenção, podemos dar ao tipo `QueryError` acima um método `Unwrap`
que retorna seu error contido:

	func (e *QueryError) Unwrap() error { return e.Err }

O resultado de fazer unwrap de um error pode ele mesmo ter um método `Unwrap`; chamamos
a sequência de errors produzida por unwrap repetido de _error chain_.

### Examinando errors com Is e As

O pacote `errors` do Go 1.13 inclui duas novas funções para examinar errors: `Is` e `As`.

A função `errors.Is` compara um error a um valor.

	// Similar to:
	//   if err == ErrNotFound { … }
	if errors.Is(err, ErrNotFound) {
		// something wasn't found
	}

A função `As` testa se um error é de um tipo específico.

	// Similar to:
	//   if e, ok := err.(*QueryError); ok { … }
	var e *QueryError
	// Note: *QueryError is the type of the error.
	if errors.As(err, &e) {
		// err is a *QueryError, and e is set to the error's value
	}

No caso mais simples, a função `errors.Is` se comporta como uma comparação a um
sentinel error, e a função `errors.As` se comporta como uma type assertion. Quando
operando em wrapped errors, entretanto, essas funções consideram todos os errors em
uma chain. Vamos olhar novamente o exemplo de cima de fazer unwrap de um `QueryError`
para examinar o error subjacente:

	if e, ok := err.(*QueryError); ok && e.Err == ErrPermission {
		// query failed because of a permission problem
	}

Usando a função `errors.Is`, podemos escrever isso como:

	if errors.Is(err, ErrPermission) {
		// err, or some error that it wraps, is a permission problem
	}

O pacote `errors` também inclui uma nova função `Unwrap` que retorna o
resultado de chamar o método `Unwrap` de um error, ou `nil` quando o error não tem
método `Unwrap`. Geralmente é melhor usar `errors.Is` ou `errors.As`,
entretanto, já que essas funções examinarão a chain inteira em uma única chamada.

Nota: embora possa parecer estranho pegar um ponteiro para um ponteiro, neste caso está
correto. Pense nisso como pegar um ponteiro para um valor do tipo
error; acontece que, neste caso, o error retornado é um tipo ponteiro.

### Envolvendo errors com %w

Como mencionado anteriormente, é comum usar a função `fmt.Errorf` para adicionar informação adicional a um error.

	if err != nil {
		return fmt.Errorf("decompress %v: %v", name, err)
	}

No Go 1.13, a função `fmt.Errorf` suporta um novo verbo `%w`. Quando este verbo
está presente, o error retornado por `fmt.Errorf` terá um método `Unwrap`
retornando o argumento de `%w`, que deve ser um error. Em todos os outros aspectos, `%w`
é idêntico a `%v`.

	if err != nil {
		// Return an error which unwraps to err.
		return fmt.Errorf("decompress %v: %w", name, err)
	}

Envolver um error com `%w` o torna disponível para `errors.Is` e `errors.As`:

	err := fmt.Errorf("access denied: %w", ErrPermission)
	...
	if errors.Is(err, ErrPermission) ...

### Quando Envolver

Ao adicionar contexto adicional a um error, seja com `fmt.Errorf` ou
implementando um tipo customizado, você precisa decidir se o novo error deve envolver
o original. Não há uma única resposta para esta questão; depende do
contexto no qual o novo error é criado. Envolva um error para expô-lo aos
chamadores. Não envolva um error quando fazer isso exporia detalhes de implementação.

Como um exemplo, imagine uma função `Parse` que lê uma estrutura de dados complexa
de um `io.Reader`. Se um error ocorre, desejamos reportar a linha e coluna
onde ocorreu. Se o error ocorre enquanto lendo do
`io.Reader`, vamos querer envolver esse error para permitir inspeção do
problema subjacente. Como o chamador forneceu o `io.Reader` para a função,
faz sentido expor o error produzido por ele.

Em contraste, uma função que faz várias chamadas a um banco de dados provavelmente
não deveria retornar um error que faz unwrap para o resultado de uma dessas chamadas. Se o
banco de dados usado pela função é um detalhe de implementação, então expor esses
errors é uma violação de abstração. Por exemplo, se a função `LookupUser`
do seu pacote `pkg` usa o pacote `database/sql` do Go, então ela pode encontrar um
error `sql.ErrNoRows`. Se você retorna esse error com
`fmt.Errorf("accessing DB: %v", err)`
então um chamador não pode olhar dentro para encontrar o `sql.ErrNoRows`. Mas se
a função em vez disso retorna `fmt.Errorf("accessing DB: %w", err)`, então um
chamador poderia razoavelmente escrever

	err := pkg.LookupUser(...)
	if errors.Is(err, sql.ErrNoRows) …

Neste ponto, a função deve sempre retornar `sql.ErrNoRows` se você não quiser
quebrar seus clientes, mesmo se você mudar para um pacote de banco de dados diferente. Em
outras palavras, envolver um error torna esse error parte da sua API. Se você não
quer se comprometer a suportar esse error como parte da sua API no futuro, você
não deveria envolver o error.

É importante lembrar que, envolvendo ou não, o texto do error será o
mesmo. Uma _pessoa_ tentando entender o error terá a mesma informação
de qualquer forma; a escolha de envolver é sobre dar a _programas_ informação adicional
para que possam tomar decisões mais informadas, ou reter essa
informação para preservar uma camada de abstração.

## Customizando testes de error com métodos Is e As

A função `errors.Is` examina cada error em uma chain para uma correspondência com um
valor alvo. Por padrão, um error corresponde ao alvo se os dois são
[iguais](/ref/spec#Comparison_operators). Além disso, um
error na chain pode declarar que corresponde a um alvo implementando um
_método_ `Is`.

Como exemplo, considere este error inspirado no
[pacote de error do Upspin](https://commandcenter.blogspot.com/2017/12/error-handling-in-upspin.html)
que compara um error contra um template, considerando apenas campos que são
não-zero no template:

	type Error struct {
		Path string
		User string
	}

	func (e *Error) Is(target error) bool {
		t, ok := target.(*Error)
		if !ok {
			return false
		}
		return (e.Path == t.Path || t.Path == "") &&
			   (e.User == t.User || t.User == "")
	}

	if errors.Is(err, &Error{User: "someuser"}) {
		// err's User field is "someuser".
	}

A função `errors.As` similarmente consulta um método `As` quando presente.

## Errors e APIs de pacotes

Um pacote que retorna errors (e a maioria retorna) deve descrever quais propriedades desses
errors programadores podem confiar. Um pacote bem projetado também evitará
retornar errors com propriedades que não deveriam ser confiadas.

A especificação mais simples é dizer que operações ou têm sucesso ou falham,
retornando um valor de error nil ou não-nil, respectivamente. Em muitos casos, nenhuma
informação adicional é necessária.

Se desejamos que uma função retorne uma condição de error identificável, como "item
não encontrado", podemos retornar um error envolvendo um sentinel.

	var ErrNotFound = errors.New("not found")

	// FetchItem returns the named item.
	//
	// If no item with the name exists, FetchItem returns an error
	// wrapping ErrNotFound.
	func FetchItem(name string) (*Item, error) {
		if itemNotFound(name) {
			return nil, fmt.Errorf("%q: %w", name, ErrNotFound)
		}
		// ...
	}

Existem outros padrões existentes para fornecer errors que podem ser semanticamente
examinados pelo chamador, como retornar diretamente um valor sentinel, um tipo
específico, ou um valor que pode ser examinado com uma função predicado.

Em todos os casos, deve-se ter cuidado para não expor detalhes internos ao usuário.
Como abordamos em "Quando Envolver" acima, quando você retorna
um error de outro pacote, você deve converter o error para uma forma que
não exponha o error subjacente, a menos que você esteja disposto a se comprometer a retornar
esse error específico no futuro.

	f, err := os.Open(filename)
	if err != nil {
		// The *os.PathError returned by os.Open is an internal detail.
		// To avoid exposing it to the caller, repackage it as a new
		// error with the same text. We use the %v formatting verb, since
		// %w would permit the caller to unwrap the original *os.PathError.
		return fmt.Errorf("%v", err)
	}

Se uma função é definida como retornando um error envolvendo algum sentinel ou tipo,
não retorne o error subjacente diretamente.

	var ErrPermission = errors.New("permission denied")

	// DoSomething returns an error wrapping ErrPermission if the user
	// does not have permission to do something.
	func DoSomething() error {
		if !userHasPermission() {
			// If we return ErrPermission directly, callers might come
			// to depend on the exact error value, writing code like this:
			//
			//     if err := pkg.DoSomething(); err == pkg.ErrPermission { … }
			//
			// This will cause problems if we want to add additional
			// context to the error in the future. To avoid this, we
			// return an error wrapping the sentinel so that users must
			// always unwrap it:
			//
			//     if err := pkg.DoSomething(); errors.Is(err, pkg.ErrPermission) { ... }
			return fmt.Errorf("%w", ErrPermission)
		}
		// ...
	}

## Conclusão

Embora as mudanças que discutimos se resumam a apenas três funções e um
verbo de formatação, esperamos que elas contribuam muito para melhorar como errors são
tratados em programas Go. Esperamos que envolver para fornecer contexto adicional
se torne comum, ajudando programas a tomar melhores decisões e ajudando
programadores a encontrar bugs mais rapidamente.

Como Russ Cox disse em seu [keynote da GopherCon 2019](/blog/experiment),
no caminho para o Go 2 nós experimentamos, simplificamos e lançamos. Agora que lançamos
essas mudanças, aguardamos ansiosamente os experimentos que se seguirão.

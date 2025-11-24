---
ia-translated: true
title: Uma Introdução a Generics
date: 2022-03-22
by:
- Robert Griesemer
- Ian Lance Taylor
tags:
- go2
- generics
summary: Uma introdução a generics em Go.
---

## Introdução

Este post de blog é baseado em nossa palestra na GopherCon 2021:

{{video "https://www.youtube.com/embed/Pa_e9EeCdy8"}}

O lançamento do Go 1.18 adiciona suporte para generics.
Generics são a maior mudança que fizemos no Go desde o primeiro lançamento
open source.
Neste artigo, vamos introduzir os novos recursos da linguagem.
Não tentaremos cobrir todos os detalhes, mas vamos abordar todos os
pontos importantes.
Para uma descrição mais detalhada e muito mais longa, incluindo muitos
exemplos, veja o [documento da proposta](https://go.googlesource.com/proposal/+/HEAD/design/43651-type-parameters.md).
Para uma descrição mais precisa das mudanças na linguagem, veja a
[especificação da linguagem atualizada](/ref/spec).
(Note que a implementação real do 1.18 impõe algumas restrições sobre
o que o documento da proposta permite; a especificação deve ser precisa.
Lançamentos futuros podem remover algumas das restrições.)

Generics são uma forma de escrever código que é independente dos tipos
específicos sendo usados.
Funções e tipos agora podem ser escritos para usar qualquer um de um conjunto de tipos.

Generics adicionam três grandes novidades à linguagem:
1. Type parameters para funções e tipos.
2. Definir tipos de interface como conjuntos de tipos, incluindo tipos que
   não têm métodos.
3. Type inference, que permite omitir argumentos de tipo em muitos
   casos ao chamar uma função.

## Type Parameters

Funções e tipos agora podem ter type parameters.
Uma lista de type parameters se parece com uma lista de parâmetros comum, exceto
que usa colchetes em vez de parênteses.

Para mostrar como isso funciona, vamos começar com a função básica não-generic `Min`
para valores de ponto flutuante:

{{raw `
	func Min(x, y float64) float64 {
		if x < y {
			return x
		}
		return y
	}
`}}

Podemos tornar esta função generic--fazê-la funcionar para diferentes
tipos--adicionando uma lista de type parameters.
Neste exemplo, adicionamos uma lista de type parameters com um único type
parameter `T`, e substituímos os usos de `float64` por `T`.

{{raw `
	import "golang.org/x/exp/constraints"

	func GMin[T constraints.Ordered](x, y T) T {
		if x < y {
			return x
		}
		return y
	}
`}}

Agora é possível chamar esta função com um argumento de tipo escrevendo
uma chamada como

{{raw `
	x := GMin[int](2, 3)
`}}

Fornecer o argumento de tipo para `GMin`, neste caso `int`, é chamado
_instantiation_.
Instantiation acontece em dois passos.
Primeiro, o compilador substitui todos os argumentos de tipo por seus
respectivos type parameters ao longo da função ou tipo generic.
Segundo, o compilador verifica que cada argumento de tipo satisfaz a
respectiva constraint.
Vamos chegar ao que isso significa em breve, mas se esse segundo passo falhar,
a instantiation falha e o programa é inválido.

Após uma instantiation bem-sucedida, temos uma função não-generic que pode
ser chamada como qualquer outra função.
Por exemplo, em código como

{{raw `
	fmin := GMin[float64]
	m := fmin(2.71, 3.14)
`}}

a instantiation `GMin[float64]` produz o que é efetivamente nossa
função `Min` original de ponto flutuante, e podemos usar isso em uma
chamada de função.

Type parameters podem ser usados com tipos também.

{{raw `
	type Tree[T interface{}] struct {
		left, right *Tree[T]
		value       T
	}

	func (t *Tree[T]) Lookup(x T) *Tree[T] { ... }

	var stringTree Tree[string]
`}}

Aqui o tipo generic `Tree` armazena valores do type parameter `T`.
Tipos generic podem ter métodos, como `Lookup` neste exemplo.
Para usar um tipo generic, ele deve ser instanciado;
`Tree[string]` é um exemplo de instanciar `Tree` com o argumento
de tipo `string`.

## Type sets

Vamos olhar um pouco mais profundamente os argumentos de tipo que podem ser usados para
instanciar um type parameter.

Uma função comum tem um tipo para cada parâmetro de valor; esse tipo
define um conjunto de valores.
Por exemplo, se temos um tipo `float64` como na função não-generic
`Min` acima, o conjunto permitido de valores de argumento é o
conjunto de valores de ponto flutuante que podem ser representados pelo tipo `float64`.

Similarmente, listas de type parameters têm um tipo para cada type parameter.
Como um type parameter é em si um tipo, os tipos de type
parameters definem conjuntos de tipos.
Este meta-tipo é chamado de _type constraint_.

No `GMin` generic, a type constraint é importada do
[pacote constraints](https://golang.org/x/exp/constraints).
A constraint `Ordered` descreve o conjunto de todos os tipos com valores
que podem ser ordenados, ou, em outras palavras, comparados com o operador {{" < "}}
(ou {{" <= "}}, {{" > "}}, etc.).
A constraint garante que apenas tipos com valores ordenáveis podem ser
passados para `GMin`.
Também significa que no corpo da função `GMin` valores desse type
parameter podem ser usados em uma comparação com o operador {{" < "}}.

Em Go, type constraints devem ser interfaces.
Ou seja, um tipo de interface pode ser usado como um tipo de valor, e também pode
ser usado como um meta-tipo.
Interfaces definem métodos, então obviamente podemos expressar type
constraints que requerem certos métodos estarem presentes.
Mas `constraints.Ordered` é um tipo de interface também, e o operador {{" < "}}
não é um método.

Para fazer isso funcionar, olhamos para interfaces de uma nova forma.

Até recentemente, a especificação Go dizia que uma interface define um conjunto
de métodos, que é aproximadamente o conjunto de métodos enumerados na interface.
Qualquer tipo que implementa todos esses métodos implementa essa interface.

{{image "intro-generics/method-sets.png"}}

Mas outra forma de olhar para isso é dizer que a interface
define um conjunto de tipos, ou seja, os tipos que implementam esses métodos.
Desta perspectiva, qualquer tipo que é um elemento do conjunto de tipos da interface
implementa a interface.

{{image "intro-generics/type-sets.png"}}

As duas visões levam ao mesmo resultado: Para cada conjunto de métodos podemos
imaginar o conjunto correspondente de tipos que implementam esses métodos,
e esse é o conjunto de tipos definido pela interface.

Para nossos propósitos, porém, a visão de conjunto de tipos tem uma vantagem sobre a
visão de conjunto de métodos: podemos adicionar explicitamente tipos ao conjunto, e assim
controlar o conjunto de tipos de novas formas.

Estendemos a sintaxe para tipos de interface para fazer isso funcionar.
Por exemplo, `interface{ int|string|bool }` define o conjunto de tipos
contendo os tipos `int`, `string` e `bool`.

{{image "intro-generics/type-sets-2.png"}}

Outra forma de dizer isso é que esta interface é satisfeita por
apenas `int`, `string` ou `bool`.

Agora vamos olhar para a definição real de `constraints.Ordered`:

{{raw `
	type Ordered interface {
		Integer|Float|~string
	}
`}}

Esta declaração diz que a interface `Ordered` é o conjunto de todos os
tipos inteiros, de ponto flutuante e string.
A barra vertical expressa uma união de tipos (ou conjuntos de tipos neste
caso).
`Integer` e `Float` são tipos de interface que são similarmente definidos
no pacote `constraints`.
Note que não há métodos definidos pela interface `Ordered`.

Para type constraints geralmente não nos importamos com um tipo específico, como
`string`; estamos interessados em todos os tipos string.
É para isso que serve o token `~`.
A expressão `~string` significa o conjunto de todos os tipos cujo tipo
subjacente é `string`.
Isso inclui o tipo `string` em si, bem como todos os tipos declarados
com definições como `type MyString string`.

Claro que ainda queremos especificar métodos em interfaces, e queremos
ser retrocompatíveis.
No Go 1.18 uma interface pode conter métodos e interfaces embutidas
como antes, mas também pode embutir tipos não-interface, uniões e
conjuntos de tipos subjacentes.

Quando usada como uma type constraint, o conjunto de tipos definido por uma interface
especifica exatamente os tipos que são permitidos como argumentos de tipo para
o respectivo type parameter.
Dentro do corpo de uma função generic, se o tipo de um operando é um type
parameter `P` com constraint `C`, operações são permitidas se elas
são permitidas por todos os tipos no conjunto de tipos de `C` (atualmente há
algumas restrições de implementação aqui, mas código comum é improvável
de encontrá-las).

Interfaces usadas como constraints podem receber nomes (como `Ordered`),
ou podem ser interfaces literais inline em uma lista de type parameters.
Por exemplo:

{{raw `
	[S interface{~[]E}, E interface{}]
`}}

Aqui `S` deve ser um tipo slice cujo tipo de elemento pode ser qualquer tipo.

Como este é um caso comum, o `interface{}` envolvente pode ser
omitido para interfaces em posição de constraint, e podemos simplesmente
escrever:

{{raw `
	[S ~[]E, E interface{}]
`}}

Como a interface vazia é comum em listas de type parameters, e em
código Go comum de qualquer forma, Go 1.18 introduz um novo identificador
predeclarado `any` como um alias para o tipo de interface vazia.
Com isso, chegamos a este código idiomático:

{{raw `
	[S ~[]E, E any]
`}}

Interfaces como conjuntos de tipos é um novo mecanismo poderoso e é chave para
fazer type constraints funcionarem em Go.
Por enquanto, interfaces que usam as novas formas sintáticas só podem ser usadas
como constraints.
Mas não é difícil imaginar como interfaces explicitamente type-constrained
poderiam ser úteis em geral.

## Type inference

O último novo recurso importante da linguagem é type inference.
De certa forma, esta é a mudança mais complicada na linguagem, mas
é importante porque permite que as pessoas usem um estilo natural ao
escrever código que chama funções generic.

### Function argument type inference

Com type parameters vem a necessidade de passar argumentos de tipo, o que pode
tornar o código verboso.
Voltando à nossa função generic `GMin`:

{{raw `
	func GMin[T constraints.Ordered](x, y T) T { ... }
`}}

o type parameter `T` é usado para especificar os tipos dos
argumentos não-tipo comuns `x` e `y`.
Como vimos anteriormente, isso pode ser chamado com um argumento de tipo explícito

{{raw `
	var a, b, m float64

	m = GMin[float64](a, b) // argumento de tipo explícito
`}}

Em muitos casos o compilador pode inferir o argumento de tipo para `T` a partir dos
argumentos comuns.
Isso torna o código mais curto enquanto permanece claro.

{{raw `
	var a, b, m float64

	m = GMin(a, b) // sem argumento de tipo
`}}

Isso funciona combinando os tipos dos argumentos `a` e `b` com os
tipos dos parâmetros `x` e `y`.

Este tipo de inferência, que infere os argumentos de tipo a partir dos tipos
dos argumentos para a função, é chamado _function argument type
inference_.

Function argument type inference só funciona para type parameters que
são usados nos parâmetros da função, não para type parameters usados apenas
nos resultados da função ou apenas no corpo da função.
Por exemplo, não se aplica a funções como `MakeT[T any]() T`,
que só usa `T` para um resultado.

### Constraint type inference

A linguagem suporta outro tipo de type inference, _constraint type
inference_.
Para descrever isso, vamos começar com este exemplo de escalonar um slice de
inteiros:

{{raw `
	// Scale retorna uma cópia de s com cada elemento multiplicado por c.
	// Esta implementação tem um problema, como veremos.
	func Scale[E constraints.Integer](s []E, c E) []E {
		r := make([]E, len(s))
		for i, v := range s {
			r[i] = v * c
		}
		return r
	}
`}}

Esta é uma função generic que funciona para um slice de qualquer tipo
inteiro.

Agora suponha que temos um tipo multidimensional `Point`, onde cada
`Point` é simplesmente uma lista de inteiros dando as coordenadas do
ponto.
Naturalmente este tipo terá alguns métodos.

{{raw `
	type Point []int32

	func (p Point) String() string {
		// Detalhes não importantes.
	}
`}}

Às vezes queremos escalonar um `Point`.
Como um `Point` é apenas um slice de inteiros, podemos usar a função `Scale`
que escrevemos anteriormente:

{{raw `
	// ScaleAndPrint dobra um Point e o imprime.
	func ScaleAndPrint(p Point) {
		r := Scale(p, 2)
		fmt.Println(r.String()) // NÃO COMPILA
	}
`}}

Infelizmente isso não compila, falha com um erro como
`r.String undefined (type []int32 has no field or method String)`.

O problema é que a função `Scale` retorna um valor do tipo `[]E`
onde `E` é o tipo de elemento do slice de argumento.
Quando chamamos `Scale` com um valor do tipo `Point`, cujo tipo
subjacente é `[]int32`, recebemos de volta um valor do tipo `[]int32`, não tipo
`Point`.
Isso segue da forma como o código generic é escrito, mas não é
o que queremos.

Para consertar isso, temos que mudar a função `Scale` para usar um
type parameter para o tipo slice.

{{raw `
	// Scale retorna uma cópia de s com cada elemento multiplicado por c.
	func Scale[S ~[]E, E constraints.Integer](s S, c E) S {
		r := make(S, len(s))
		for i, v := range s {
			r[i] = v * c
		}
		return r
	}
`}}

Introduzimos um novo type parameter `S` que é o tipo do
argumento slice.
Restringimos de tal forma que o tipo subjacente é `S` em vez de
`[]E`, e o tipo de resultado agora é `S`.
Como `E` é restrito a ser um inteiro, o efeito é o mesmo de
antes: o primeiro argumento tem que ser um slice de algum tipo inteiro.
A única mudança no corpo da função é que agora passamos `S`,
em vez de `[]E`, quando chamamos `make`.

A nova função age da mesma forma de antes se a chamarmos com um
slice simples, mas se a chamarmos com o tipo `Point` agora recebemos de volta um valor
do tipo `Point`.
Isso é o que queremos.
Com esta versão de `Scale` a função `ScaleAndPrint` anterior irá
compilar e executar como esperamos.

Mas é justo perguntar: por que é OK escrever a chamada para `Scale`
sem passar argumentos de tipo explícitos?
Ou seja, por que podemos escrever `Scale(p, 2)`, sem argumentos de tipo,
em vez de ter que escrever `Scale[Point, int32](p, 2)`?
Nossa nova função `Scale` tem dois type parameters, `S` e `E`.
Em uma chamada para `Scale` não passando nenhum argumento de tipo, function argument
type inference, descrita acima, permite o compilador inferir que o argumento
de tipo para `S` é `Point`.
Mas a função também tem um type parameter `E` que é o tipo do
fator de multiplicação `c`.
O argumento de função correspondente é `2`, e como `2` é uma constante _untyped_,
function argument type inference não pode inferir o tipo correto para
`E` (no máximo poderia inferir o tipo padrão para `2` que é `int` e que
seria incorreto).
Em vez disso, o processo pelo qual o compilador infere que o argumento de tipo
para `E` é o tipo de elemento do slice é chamado _constraint type
inference_.

Constraint type inference deduz argumentos de tipo a partir de type parameter
constraints.
É usado quando um type parameter tem uma constraint definida em termos
de outro type parameter.
Quando o argumento de tipo de um desses type parameters é conhecido,
a constraint é usada para inferir o argumento de tipo do outro.

O caso usual onde isso se aplica é quando uma constraint usa a forma
`~`_`type`_ para algum tipo, onde esse tipo é escrito usando outros type
parameters.
Vemos isso no exemplo `Scale`.
`S` é `~[]E`, que é `~` seguido por um tipo `[]E` escrito em termos
de outro type parameter.
Se sabemos o argumento de tipo para `S` podemos inferir o argumento de tipo
para `E`.
`S` é um tipo slice, e `E` é o tipo de elemento desse slice.

Esta foi apenas uma introdução a constraint type inference.
Para detalhes completos veja o [documento da proposta](https://go.googlesource.com/proposal/+/HEAD/design/43651-type-parameters.md)
ou a [especificação da linguagem](/ref/spec).

### Type inference na prática

Os detalhes exatos de como type inference funciona são complicados, mas
usá-la não é: type inference ou tem sucesso ou falha.
Se tem sucesso, argumentos de tipo podem ser omitidos, e chamar funções generic
parece não diferente de chamar funções comuns.
Se type inference falha, o compilador dará uma mensagem de erro, e
nesses casos podemos apenas fornecer os argumentos de tipo necessários.

Ao adicionar type inference à linguagem tentamos alcançar um
equilíbrio entre poder de inferência e complexidade.
Queremos garantir que quando o compilador infere tipos, esses tipos são
nunca surpreendentes.
Tentamos ser cuidadosos para errar no lado de falhar em inferir um
tipo em vez de no lado de inferir o tipo errado.
Provavelmente não acertamos totalmente, e podemos continuar a
refiná-la em lançamentos futuros.
O efeito será que mais programas podem ser escritos sem argumentos de tipo
explícitos.
Programas que não precisam de argumentos de tipo hoje não precisarão deles amanhã
também.

## Conclusão

Generics são um grande novo recurso da linguagem no 1.18.
Estas novas mudanças na linguagem requereram uma grande quantidade de novo
código que não teve testes significativos em ambientes de produção.
Isso só acontecerá à medida que mais pessoas escrevem e usam código generic.
Acreditamos que este recurso está bem implementado e de alta qualidade.
No entanto, ao contrário da maioria dos aspectos do Go, não podemos apoiar essa crença com
experiência do mundo real.
Portanto, enquanto encorajamos o uso de generics onde faz
sentido, por favor use cautela apropriada ao implantar código generic em
produção.

Essa cautela à parte, estamos empolgados em ter generics disponíveis, e esperamos
que eles tornem os programadores Go mais produtivos.

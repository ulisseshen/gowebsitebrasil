---
ia-translated: true
title: Quando Usar Generics
date: 2022-04-12
by:
- Ian Lance Taylor
tags:
- go2
- generics
summary: Quando usar generics ao escrever código Go, e quando não usá-los.
---

## Introdução

Esta é a versão em post de blog das minhas palestras no Google Open Source Live:

{{video "https://www.youtube.com/embed/nr8EpUO9jhw"}}

e GopherCon 2021:

{{video "https://www.youtube.com/embed/Pa_e9EeCdy8?start=1244"}}

O lançamento do Go 1.18 adiciona um novo recurso importante à linguagem: suporte para
programação generic.
Neste artigo não vou descrever o que são generics nem como
usá-los.
Este artigo é sobre quando usar generics em código Go, e quando não
usá-los.

Para deixar claro, vou fornecer diretrizes gerais, não regras
rígidas.
Use seu próprio julgamento.
Mas se você não tiver certeza, recomendo usar as diretrizes discutidas
aqui.

## Escreva código

Vamos começar com uma diretriz geral para programar em Go: escreva programas Go
escrevendo código, não definindo tipos.
Quando se trata de generics, se você começa a escrever seu programa
definindo type parameter constraints, você provavelmente está no caminho
errado.
Comece escrevendo funções.
É fácil adicionar type parameters depois quando estiver claro que eles serão
úteis.

## Quando type parameters são úteis?

Dito isso, vamos olhar para casos nos quais type parameters podem ser
úteis.

### Ao usar tipos de contêiner definidos pela linguagem

Um caso é ao escrever funções que operam nos tipos de
contêiner especiais que são definidos pela linguagem: slices, maps e
channels.
Se uma função tem parâmetros com esses tipos, e o código da função
não faz nenhuma suposição particular sobre os tipos de elemento, então
pode ser útil usar um type parameter.

Por exemplo, aqui está uma função que retorna um slice de todas as chaves
em um map de qualquer tipo:

{{raw `
	// MapKeys returns a slice of all the keys in m.
	// The keys are not returned in any particular order.
	func MapKeys[Key comparable, Val any](m map[Key]Val) []Key {
		s := make([]Key, 0, len(m))
		for k := range m {
			s = append(s, k)
		}
		return s
	}
`}}

Este código não assume nada sobre o tipo da chave do map, e não
usa o tipo do valor do map de forma alguma.
Funciona para qualquer tipo de map.
Isso o torna um bom candidato para usar type parameters.

A alternativa a type parameters para este tipo de função é
tipicamente usar reflection, mas esse é um modelo de programação
mais estranho, não é verificado estaticamente em tempo de compilação, e é frequentemente mais lento
em tempo de execução.

### Estruturas de dados de propósito geral

Outro caso onde type parameters podem ser úteis é para estruturas
de dados de propósito geral.
Uma estrutura de dados de propósito geral é algo como um slice ou map, mas
que não é embutido na linguagem, como uma lista encadeada, ou uma
árvore binária.

Hoje, programas que precisam de tais estruturas de dados tipicamente fazem uma de duas
coisas: escrevê-las com um tipo de elemento específico, ou usar um tipo de
interface.
Substituir um tipo de elemento específico por um type parameter pode produzir uma
estrutura de dados mais geral que pode ser usada em outras partes do
programa, ou por outros programas.
Substituir um tipo de interface por um type parameter pode permitir que os dados
sejam armazenados de forma mais eficiente, economizando recursos de memória; também pode
permitir que o código evite asserções de tipo, e seja totalmente verificado
em tempo de compilação.

Por exemplo, aqui está parte de como uma estrutura de dados de árvore binária poderia
parecer usando type parameters:

{{raw `
	// Tree is a binary tree.
	type Tree[T any] struct {
		cmp  func(T, T) int
		root *node[T]
	}

	// A node in a Tree.
	type node[T any] struct {
		left, right  *node[T]
		val          T
	}

	// find returns a pointer to the node containing val,
	// or, if val is not present, a pointer to where it
	// would be placed if added.
	func (bt *Tree[T]) find(val T) **node[T] {
		pl := &bt.root
		for *pl != nil {
			switch cmp := bt.cmp(val, (*pl).val); {
			case cmp < 0:
				pl = &(*pl).left
		   	case cmp > 0:
				pl = &(*pl).right
			default:
				return pl
			}
		}
		return pl
	}

	// Insert inserts val into bt if not already there,
	// and reports whether it was inserted.
	func (bt *Tree[T]) Insert(val T) bool {
		pl := bt.find(val)
		if *pl != nil {
			return false
		}
		*pl = &node[T]{val: val}
		return true
	}
`}}

Cada nó na árvore contém um valor do type parameter `T`.
Quando a árvore é instanciada com um argumento de tipo particular, valores
desse tipo serão armazenados diretamente nos nós.
Eles não serão armazenados como tipos de interface.

Este é um uso razoável de type parameters porque a estrutura de dados `Tree`,
incluindo o código nos métodos, é em grande parte independente
do tipo de elemento `T`.

A estrutura de dados `Tree` precisa saber como comparar valores do
tipo de elemento `T`; ela usa uma função de comparação passada para
isso.
Você pode ver isso na quarta linha do método `find`, na chamada
para `bt.cmp`.
Fora isso, o type parameter não importa de forma alguma.

### Para type parameters, prefira funções a métodos

O exemplo `Tree` ilustra outra diretriz geral: quando você
precisa de algo como uma função de comparação, prefira uma função a um
método.

Poderíamos ter definido o tipo `Tree` de tal forma que o tipo de elemento é
obrigado a ter um método `Compare` ou `Less`.
Isso seria feito escrevendo uma constraint que requer o método,
significando que qualquer argumento de tipo usado para instanciar o tipo `Tree`
precisaria ter esse método.

Uma consequência seria que qualquer um que queira usar `Tree` com um
tipo de dados simples como `int` teria que definir seu próprio tipo
inteiro e escrever seu próprio método de comparação.
Se definirmos `Tree` para receber uma função de comparação, como no código
mostrado acima, então é fácil passar a função desejada.
É tão fácil escrever essa função de comparação quanto escrever
um método.

Se o tipo de elemento `Tree` já tem um método `Compare`,
então podemos simplesmente usar uma expressão de método como `ElementType.Compare`
como a função de comparação.

Em outras palavras, é muito mais simples transformar um método em uma
função do que adicionar um método a um tipo.
Então para tipos de dados de propósito geral, prefira uma função em vez de
escrever uma constraint que requer um método.

### Implementando um método comum

Outro caso onde type parameters podem ser úteis é quando diferentes
tipos precisam implementar algum método comum, e as implementações
para os diferentes tipos todas parecem iguais.

Por exemplo, considere o `sort.Interface` da biblioteca padrão.
Ele requer que um tipo implemente três métodos: `Len`, `Swap` e
`Less`.

Aqui está um exemplo de um tipo generic `SliceFn` que implementa
`sort.Interface` para qualquer tipo de slice:

{{raw `
	// SliceFn implements sort.Interface for a slice of T.
	type SliceFn[T any] struct {
		s    []T
		less func(T, T) bool
	}

	func (s SliceFn[T]) Len() int {
		return len(s.s)
	}
	func (s SliceFn[T]) Swap(i, j int) {
		s.s[i], s.s[j] = s.s[j], s.s[i]
	}
	func (s SliceFn[T]) Less(i, j int) bool {
		return s.less(s.s[i], s.s[j])
	}
`}}

Para qualquer tipo de slice, os métodos `Len` e `Swap` são exatamente os mesmos.
O método `Less` requer uma comparação, que é a parte `Fn` do
nome `SliceFn`.
Como no exemplo anterior `Tree`, vamos passar uma função quando
criarmos um `SliceFn`.

Aqui está como usar `SliceFn` para ordenar qualquer slice usando uma função
de comparação:

{{raw `
	// SortFn sorts s in place using a comparison function.
	func SortFn[T any](s []T, less func(T, T) bool) {
		sort.Sort(SliceFn[T]{s, less})
	}
`}}

Isso é similar à função `sort.Slice` da biblioteca padrão, mas a
função de comparação é escrita usando valores em vez de índices de
slice.

Usar type parameters para este tipo de código é apropriado porque os
métodos parecem exatamente iguais para todos os tipos de slice.

(Devo mencionar que Go 1.19--não 1.18--muito provavelmente incluirá uma
função generic para ordenar um slice usando uma função de comparação, e essa
função generic muito provavelmente não usará `sort.Interface`.
Veja [proposta #47619](/issue/47619).
Mas o ponto geral ainda é verdadeiro mesmo que este exemplo específico
provavelmente não seja útil: é razoável usar type parameters quando
você precisa implementar métodos que parecem iguais para todos os tipos
relevantes.)

## Quando type parameters não são úteis?

Agora vamos falar sobre o outro lado da questão: quando não usar
type parameters.

### Não substitua tipos de interface por type parameters

Como todos sabemos, Go tem tipos de interface.
Tipos de interface permitem um tipo de programação generic.

Por exemplo, a interface `io.Reader` amplamente usada fornece um mecanismo
generic para ler dados de qualquer valor que contenha informação
(por exemplo, um arquivo) ou que produza informação (por exemplo, um
gerador de números aleatórios).
Se tudo o que você precisa fazer com um valor de algum tipo é chamar um método nesse
valor, use um tipo de interface, não um type parameter.
`io.Reader` é fácil de ler, eficiente e eficaz.
Não há necessidade de usar um type parameter para ler dados de um valor
chamando o método `Read`.

Por exemplo, pode ser tentador mudar a primeira assinatura de função
aqui, que usa apenas um tipo de interface, para a segunda
versão, que usa um type parameter.

{{raw `
	func ReadSome(r io.Reader) ([]byte, error)

	func ReadSome[T io.Reader](r T) ([]byte, error)
`}}

Não faça esse tipo de mudança.
Omitir o type parameter torna a função mais fácil de escrever, mais fácil
de ler, e o tempo de execução provavelmente será o mesmo.

Vale a pena enfatizar o último ponto.
Embora seja possível implementar generics de várias maneiras diferentes,
e as implementações mudarão e melhorarão com o tempo, a
implementação usada no Go 1.18 em muitos casos tratará valores cujo
tipo é um type parameter de forma muito parecida com valores cujo tipo é um tipo de
interface.
O que isso significa é que usar um type parameter geralmente não será
mais rápido do que usar um tipo de interface.
Então não mude de tipos de interface para type parameters apenas por
velocidade, porque provavelmente não executará mais rápido.

### Não use type parameters se as implementações de métodos diferem

Ao decidir se usar um type parameter ou um tipo de interface,
considere a implementação dos métodos.
Anteriormente dissemos que se a implementação de um método é a mesma para
todos os tipos, use um type parameter.
Inversamente, se a implementação é diferente para cada tipo, então use
um tipo de interface e escreva diferentes implementações de métodos, não
use um type parameter.

Por exemplo, a implementação de `Read` de um arquivo não é nada como
a implementação de `Read` de um gerador de números aleatórios.
Isso significa que devemos escrever dois métodos `Read` diferentes, e
usar um tipo de interface como `io.Reader`.

### Use reflection onde apropriado

Go tem [reflection em tempo de execução](https://pkg.go.dev/reflect).
Reflection permite um tipo de programação generic, no sentido de que permite
escrever código que funciona com qualquer tipo.

Se alguma operação tem que suportar até tipos que não têm métodos
(de modo que tipos de interface não ajudam), e se a operação é
diferente para cada tipo (de modo que type parameters não são apropriados),
use reflection.

Um exemplo disso é o
pacote [encoding/json](https://pkg.go.dev/encoding/json).
Não queremos exigir que todo tipo que codificamos tenha um
método `MarshalJSON`, então não podemos usar tipos de interface.
Mas codificar um tipo de interface não é nada como codificar um tipo struct,
então não devemos usar type parameters.
Em vez disso, o pacote usa reflection.
O código não é simples, mas funciona.
Para detalhes, veja [o código
fonte](/src/encoding/json/encode.go).

## Uma diretriz simples

Para concluir, esta discussão de quando usar generics pode ser reduzida a
uma diretriz simples.

Se você se pegar escrevendo exatamente o mesmo código várias vezes, onde
a única diferença entre as cópias é que o código usa diferentes
tipos, considere se você pode usar um type parameter.

Outra forma de dizer isso é que você deve evitar type parameters até
perceber que está prestes a escrever exatamente o mesmo código várias
vezes.

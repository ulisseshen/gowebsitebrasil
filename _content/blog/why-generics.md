---
ia-translated: true
title: Por Que Generics?
date: 2019-07-31
by:
- Ian Lance Taylor
tags:
- go2
- proposals
- generics
summary: Por que deveríamos adicionar generics ao Go, e como eles poderiam ser?
---

## Introdução

Esta é a versão em post de blog da minha palestra na semana passada na Gophercon 2019.

{{video "https://www.youtube.com/embed/WzgLqE-3IhY?rel=0"}}

Este artigo é sobre o que significaria adicionar generics ao Go, e
por que acho que deveríamos fazer isso.
Também vou tocar em uma atualização para um possível design para
adicionar generics ao Go.

Go foi lançado em 10 de novembro de 2009.
Menos de 24 horas depois vimos o
[primeiro comentário sobre generics](https://groups.google.com/d/msg/golang-nuts/70-pdwUUrbI/onMsQspcljcJ).
(Esse comentário também menciona exceções, que adicionamos à
linguagem, na forma de `panic` e `recover`, no início de 2010.)

Em três anos de pesquisas Go, a falta de generics sempre foi listada
como um dos três principais problemas a corrigir na linguagem.

## Por que generics?

Mas o que significa adicionar generics, e por que queremos isso?

Parafraseando
[Jazayeri, et al](https://www.dagstuhl.de/en/program/calendar/semhp/?semnr=98171):
programação generic permite a representação de funções e estruturas de dados
em uma forma generic, com tipos fatorados.

O que isso significa?

Para um exemplo simples, vamos supor que queremos inverter os elementos em
um slice.
Não é algo que muitos programas precisam fazer, mas não é
nada incomum.

Vamos dizer que é um slice de int.

{{raw `
	func ReverseInts(s []int) {
		first := 0
		last := len(s)
		for first < last {
			s[first], s[last] = s[last], s[first]
			first++
			last--
		}
	}
`}}

Bem simples, mas mesmo para uma função simples como essa você gostaria de
escrever alguns casos de teste.
Na verdade, quando eu fiz, encontrei um bug.
Tenho certeza de que muitos leitores já o perceberam.

{{raw `
	func ReverseInts(s []int) {
		first := 0
		last := len(s) - 1
		for first < last {
			s[first], s[last] = s[last], s[first]
			first++
			last--
		}
	}
`}}

Precisamos subtrair 1 quando definimos a variável last.

Agora vamos inverter um slice de string.

{{raw `
	func ReverseStrings(s []string) {
		first := 0
		last := len(s) - 1
		for first < last {
			s[first], s[last] = s[last], s[first]
			first++
			last--
		}
	}
`}}

Se você comparar `ReverseInts` e `ReverseStrings`, verá que as
duas funções são exatamente iguais, exceto pelo tipo do parâmetro.
Não acho que nenhum leitor se surpreenda com isso.

O que algumas pessoas novas em Go acham surpreendente é que não há maneira de
escrever uma função `Reverse` simples que funcione para um slice de qualquer tipo.

A maioria das outras linguagens permite que você escreva esse tipo de função.

Em uma linguagem dinamicamente tipada como Python ou JavaScript você pode
simplesmente escrever a função, sem se preocupar em especificar o tipo do elemento.
Isso não funciona em Go porque Go é estaticamente tipado, e
requer que você escreva o tipo exato do slice e o tipo dos
elementos do slice.

A maioria das outras linguagens estaticamente tipadas, como C++ ou Java ou Rust ou
Swift, suportam generics para lidar exatamente com esse tipo de questão.

## Programação generic em Go hoje

Então como as pessoas escrevem esse tipo de código em Go?

Em Go você pode escrever uma única função que funciona para diferentes tipos de slice
usando um tipo de interface, e definindo um método nos tipos de slice
que você quer passar.
É assim que a função `sort.Sort` da biblioteca padrão funciona.

Em outras palavras, tipos de interface em Go são uma forma de programação
generic.
Eles nos permitem capturar os aspectos comuns de diferentes tipos e expressá-los
como métodos.
Podemos então escrever funções que usam esses tipos de interface, e essas
funções funcionarão para qualquer tipo que implemente esses métodos.

Mas essa abordagem fica aquém do que queremos.
Com interfaces você tem que escrever os métodos você mesmo.
É estranho ter que definir um tipo nomeado com alguns métodos
apenas para inverter um slice.
E os métodos que você escreve são exatamente os mesmos para cada tipo de slice, então
de certa forma apenas movemos e condensamos o código duplicado, não
o eliminamos.
Embora interfaces sejam uma forma de generics, elas não nos dão
tudo o que queremos de generics.

Uma maneira diferente de usar interfaces para generics, que poderia contornar
a necessidade de escrever os métodos você mesmo, seria fazer a linguagem
definir métodos para alguns tipos de tipos.
Isso não é algo que a linguagem suporte hoje, mas, por exemplo,
a linguagem poderia definir que todo tipo slice tem um método Index
que retorna um elemento.
Mas para usar esse método na prática ele teria que retornar uma
interface vazia, e então perdemos todos os benefícios da tipagem
estática.
Mais sutilmente, não haveria maneira de definir uma função generic que
recebe dois slices diferentes com o mesmo tipo de elemento, ou que recebe um
map de um tipo de elemento e retorna um slice do mesmo tipo de elemento.
Go é uma linguagem estaticamente tipada porque isso torna mais fácil
escrever programas grandes; não queremos perder os benefícios da tipagem
estática para ganhar os benefícios de generics.

Outra abordagem seria escrever uma função `Reverse` generic usando
o pacote reflect, mas isso é tão estranho de escrever e lento de executar
que poucas pessoas fazem isso.
Essa abordagem também requer asserções de tipo explícitas e não tem
verificação de tipo estática.

Ou, você poderia escrever um gerador de código que recebe um tipo e gera uma
função `Reverse` para slices desse tipo.
Existem vários geradores de código por aí que fazem exatamente isso.
Mas isso adiciona outro passo a cada pacote que precisa de `Reverse`,
complica a compilação porque todas as diferentes cópias têm que ser
compiladas, e corrigir um bug na fonte mestra requer re-gerar
todas as instâncias, algumas das quais podem estar em projetos diferentes
inteiramente.

Todas essas abordagens são estranhas o suficiente para que eu acho que a maioria das
pessoas que têm que inverter um slice em Go simplesmente escrevem a função para
o tipo de slice específico de que precisam.
Então elas precisarão escrever casos de teste para a função, para ter certeza
de que não cometeram um erro simples como o que eu cometi inicialmente.
E elas precisarão executar esses testes rotineiramente.

De qualquer forma que façamos, significa muito trabalho extra apenas para uma função que
parece exatamente a mesma exceto pelo tipo do elemento.
Não é que não possa ser feito.
Claramente pode ser feito, e os programadores Go estão fazendo.
É só que deveria haver uma maneira melhor.

Para uma linguagem estaticamente tipada como Go, essa maneira melhor é generics.
O que escrevi anteriormente é que programação generic permite a
representação de funções e estruturas de dados em uma forma generic,
com tipos fatorados.
É exatamente isso que queremos aqui.

## O que generics podem trazer para Go

A primeira e mais importante coisa que queremos de generics em Go é
poder escrever funções como `Reverse` sem se preocupar com o
tipo do elemento do slice.
Queremos fatorar esse tipo de elemento.
Então podemos escrever a função uma vez, escrever os testes uma vez, colocá-los em
um pacote go-gettable, e chamá-los sempre que quisermos.

Melhor ainda, como este é um mundo de código aberto, outra pessoa pode
escrever `Reverse` uma vez, e podemos usar sua implementação.

Neste ponto devo dizer que "generics" podem significar muitas coisas diferentes.
Neste artigo, o que quero dizer com "generics" é o que acabei de descrever.
Em particular, não quero dizer templates como encontrados na linguagem C++,
que suportam muito mais do que o que escrevi aqui.

Passei por `Reverse` em detalhe, mas há muitas outras funções
que poderíamos escrever genericamente, tais como:

  - Encontrar menor/maior elemento em slice
  - Encontrar média/desvio padrão de slice
  - Calcular união/interseção de maps
  - Encontrar caminho mais curto em grafo de nós/arestas
  - Aplicar função de transformação a slice/map, retornando novo slice/map

Estes exemplos estão disponíveis na maioria das outras linguagens.
Na verdade, escrevi esta lista olhando para a biblioteca de templates
padrão do C++.

Também há exemplos que são específicos do Go com seu forte
suporte para concorrência.

  - Ler de um canal com timeout
  - Combinar dois canais em um único canal
  - Chamar uma lista de funções em paralelo, retornando um slice de resultados
  - Chamar uma lista de funções, usando um Context, retornar o resultado da primeira função a terminar, cancelando e limpando goroutines extras

Já vi todas essas funções escritas muitas vezes com diferentes
tipos.
Não é difícil escrevê-las em Go.
Mas seria bom poder reutilizar uma implementação eficiente e depurada
que funcione para qualquer tipo de valor.

Para deixar claro, estes são apenas exemplos.
Há muitas outras funções de propósito geral que poderiam ser escritas
mais facilmente e com segurança usando generics.

Além disso, como escrevi anteriormente, não são apenas funções.
São também estruturas de dados.

Go tem duas estruturas de dados generic de propósito geral embutidas na
linguagem: slices e maps.
Slices e maps podem conter valores de qualquer tipo de dados, com verificação de tipo
estática para valores armazenados e recuperados.
Os valores são armazenados como eles mesmos, não como tipos de interface.
Ou seja, quando tenho um `[]int`, o slice contém ints diretamente, não
ints convertidos para um tipo de interface.

Slices e maps são as estruturas de dados generic mais úteis, mas não são
as únicas.
Aqui estão alguns outros exemplos.

  - Conjuntos
  - Árvores auto-balanceadas, com inserção e travessia eficientes em ordem ordenada
  - Multimaps, com múltiplas instâncias de uma chave
  - Mapas hash concorrentes, suportando inserções e buscas paralelas sem um único lock

Se pudermos escrever tipos generic, podemos definir novas estruturas de dados, como
estas, que têm as mesmas vantagens de verificação de tipo que slices e maps:
o compilador pode verificar estaticamente os tipos dos valores que
eles contêm, e os valores podem ser armazenados como eles mesmos, não como
tipos de interface.

Também deveria ser possível pegar algoritmos como os mencionados
anteriormente e aplicá-los a estruturas de dados generic.

Estes exemplos deveriam todos ser como `Reverse`: funções generic
e estruturas de dados escritas uma vez, em um pacote, e reutilizadas sempre
que forem necessárias.
Eles deveriam funcionar como slices e maps, no sentido de que não deveriam armazenar
valores do tipo de interface vazia, mas deveriam armazenar tipos específicos, e
esses tipos deveriam ser verificados em tempo de compilação.

Então é isso que Go pode ganhar com generics.
Generics podem nos dar blocos de construção poderosos que nos permitem compartilhar código
e construir programas mais facilmente.

Espero ter explicado por que vale a pena investigar isso.

## Benefícios e custos

Mas generics não vêm da
[Big Rock Candy Mountain](https://mainlynorfolk.info/folk/songs/bigrockcandymountain.html),
a terra onde o sol brilha todos os dias sobre as
[lemonade springs](http://www.lat-long.com/Latitude-Longitude-773297-Montana-Lemonade_Springs.html).
Toda mudança de linguagem tem um custo.
Não há dúvida de que adicionar generics ao Go tornará a linguagem
mais complicada.
Como com qualquer mudança na linguagem, precisamos falar sobre maximizar
o benefício e minimizar o custo.

Em Go, visamos reduzir a complexidade através de recursos de linguagem
independentes e ortogonais que podem ser combinados livremente.
Reduzimos a complexidade tornando os recursos individuais simples, e
maximizamos o benefício dos recursos permitindo sua livre
combinação.
Queremos fazer o mesmo com generics.

Para tornar isso mais concreto vou listar algumas diretrizes que
deveríamos seguir.

### Minimizar novos conceitos

Devemos adicionar o mínimo possível de novos conceitos à linguagem.
Isso significa um mínimo de nova sintaxe e um mínimo de novas palavras-chave e
outros nomes.

### Complexidade recai sobre quem escreve código generic, não sobre o usuário

O máximo possível da complexidade deve recair sobre o programador
que escreve o pacote generic.
Não queremos que o usuário do pacote tenha que se preocupar com generics.
Isso significa que deve ser possível chamar funções generic de uma
maneira natural, e significa que quaisquer erros no uso de um pacote generic
devem ser reportados de uma forma que seja fácil de entender e corrigir.
Também deve ser fácil depurar chamadas em código generic.

### Quem escreve e usuário podem trabalhar independentemente

Similarmente, devemos facilitar a separação das preocupações de quem
escreve o código generic e seu usuário, para que eles possam desenvolver seu
código independentemente.
Eles não devem ter que se preocupar com o que o outro está fazendo, mais
do que quem escreve e quem chama uma função normal em pacotes diferentes
têm que se preocupar.
Isso parece óbvio, mas não é verdade para generics em todas as outras
linguagens de programação.

### Tempos de compilação curtos, tempos de execução rápidos

Naturalmente, o máximo possível, queremos manter os tempos de compilação curtos
e o tempo de execução rápido que Go nos dá hoje.
Generics tendem a introduzir um trade-off entre compilações rápidas e
execução rápida.
O máximo possível, queremos ambos.

### Preservar clareza e simplicidade do Go

Mais importante, Go hoje é uma linguagem simples.
Programas Go são geralmente claros e fáceis de entender.
Uma grande parte do nosso longo processo de exploração deste espaço tem sido
tentar entender como adicionar generics preservando essa clareza
e simplicidade.
Precisamos encontrar mecanismos que se encaixem bem na linguagem existente,
sem transformá-la em algo bem diferente.

Estas diretrizes devem se aplicar a qualquer implementação de generics em Go.
Essa é a mensagem mais importante que quero deixar com vocês hoje:
**generics podem trazer um benefício significativo para a linguagem, mas só valem a pena se Go ainda parecer Go**.

## Rascunho de design

Felizmente, acho que pode ser feito.
Para terminar este artigo vou mudar de discutir por que queremos
generics, e quais são os requisitos sobre eles, para brevemente
discutir um design de como achamos que podemos adicioná-los à linguagem.

Nota adicionada em janeiro de 2022: Este post de blog foi escrito em 2019 e não
descreve a versão de generics que foi finalmente adotada.
Para informações atualizadas por favor veja a descrição de type parameters em
[a especificação da linguagem](/ref/spec) e
[o documento de design de generics](/design/43651-type-parameters).

Na Gophercon deste ano Robert Griesemer e eu publicamos
[um rascunho de design](https://github.com/golang/proposal/blob/master/design/go2draft-contracts.md)
para adicionar generics ao Go.
Veja o rascunho para detalhes completos.
Vou passar por alguns dos pontos principais aqui.

Aqui está a função generic Reverse neste design.

{{raw `
	func Reverse (type Element) (s []Element) {
		first := 0
		last := len(s) - 1
		for first < last {
			s[first], s[last] = s[last], s[first]
			first++
			last--
		}
	}
`}}

Você notará que o corpo da função é exatamente o mesmo.
Apenas a assinatura mudou.

O tipo de elemento do slice foi fatorado.
Agora é chamado de `Element` e tornou-se o que chamamos de
_type parameter_.
Em vez de fazer parte do tipo do parâmetro slice, agora é um
parâmetro adicional, separado, de tipo.

Para chamar uma função com um type parameter, no caso geral você passa
um argumento de tipo, que é como qualquer outro argumento exceto que é um
tipo.

	func ReverseAndPrint(s []int) {
		Reverse(int)(s)
		fmt.Println(s)
	}

Esse é o `(int)` visto após `Reverse` neste exemplo.

Felizmente, na maioria dos casos, incluindo este, o compilador pode
deduzir o argumento de tipo a partir dos tipos dos argumentos regulares, e
você não precisa mencionar o argumento de tipo de forma alguma.

Chamar uma função generic parece simplesmente chamar qualquer outra função.

	func ReverseAndPrint(s []int) {
		Reverse(s)
		fmt.Println(s)
	}

Em outras palavras, embora a função generic `Reverse` seja ligeiramente
mais complexa que `ReverseInts` e `ReverseStrings`, essa complexidade
recai sobre quem escreve a função, não sobre quem a chama.

### Contracts

Como Go é uma linguagem estaticamente tipada, temos que falar sobre o
tipo de um type parameter.
Este _meta-tipo_ diz ao compilador que tipos de argumentos de tipo são
permitidos ao chamar uma função generic, e que tipos de
operações a função generic pode fazer com valores do type
parameter.

A função `Reverse` pode funcionar com slices de qualquer tipo.
A única coisa que ela faz com valores do tipo `Element` é atribuição,
que funciona com qualquer tipo em Go.
Para este tipo de função generic, que é um caso muito comum, não
precisamos dizer nada especial sobre o type parameter.

Vamos dar uma olhada rápida em uma função diferente.

{{raw `
	func IndexByte (type T Sequence) (s T, b byte) int {
		for i := 0; i < len(s); i++ {
			if s[i] == b {
				return i
			}
		}
		return -1
	}
`}}

Atualmente tanto o pacote bytes quanto o pacote strings na
biblioteca padrão têm uma função `IndexByte`.
Esta função retorna o índice de `b` na sequência `s`, onde `s`
é ou um `string` ou um `[]byte`.
Poderíamos usar esta única função generic para substituir as duas funções
nos pacotes bytes e strings.
Na prática podemos não nos dar ao trabalho de fazer isso, mas este é um exemplo simples
útil.

Aqui precisamos saber que o type parameter `T` age como um `string`
ou um `[]byte`.
Podemos chamar `len` nele, e podemos indexá-lo, e podemos comparar
o resultado da operação de índice com um valor byte.

Para permitir que isso compile, o type parameter `T` em si precisa de um tipo.
É um meta-tipo, mas como às vezes precisamos descrever múltiplos
tipos relacionados, e porque descreve uma relação entre a
implementação da função generic e seus chamadores, na verdade
chamamos o tipo de `T` de contract.
Aqui o contract é chamado `Sequence`.
Ele aparece após a lista de type parameters.

É assim que o contract Sequence é definido para este exemplo.

	contract Sequence(T) {
		T string, []byte
	}

É bem simples, já que este é um exemplo simples: o type parameter
`T` pode ser ou `string` ou `[]byte`.
Aqui `contract` pode ser uma nova palavra-chave, ou um identificador especial
reconhecido em escopo de pacote; veja o rascunho de design para detalhes.

Qualquer um que se lembre [do design que apresentamos na Gophercon 2018](https://github.com/golang/proposal/blob/4a530dae40977758e47b78fae349d8e5f86a6c0a/design/go2draft-contracts.md)
verá que esta forma de escrever um contract é muito mais simples.
Recebemos muito feedback sobre aquele design anterior de que contracts eram
muito complicados, e tentamos levar isso em conta.
Os novos contracts são muito mais simples de escrever, e de ler, e de
entender.

Eles permitem que você especifique o tipo subjacente de um type parameter, e/ou
liste os métodos de um type parameter.
Eles também permitem que você descreva a relação entre diferentes type
parameters.

### Contracts com métodos

Aqui está outro exemplo simples, de uma função que usa o método String
para retornar um `[]string` da representação string de todos os
elementos em `s`.

	func ToStrings (type E Stringer) (s []E) []string {
		r := make([]string, len(s))
		for i, v := range s {
			r[i] = v.String()
		}
		return r
	}

É bem direto: percorre o slice, chama o método `String`
em cada elemento, e retorna um slice das strings resultantes.

Esta função requer que o tipo do elemento implemente o método `String`.
O contract Stringer garante isso.

	contract Stringer(T) {
		T String() string
	}

O contract simplesmente diz que `T` tem que implementar o método `String`.

Você pode notar que este contract se parece com a interface `fmt.Stringer`,
então vale a pena apontar que o argumento da função
`ToStrings` não é um slice de `fmt.Stringer`.
É um slice de algum tipo de elemento, onde o tipo de elemento implementa
`fmt.Stringer`.
A representação de memória de um slice do tipo de elemento e um slice
de `fmt.Stringer` são normalmente diferentes, e Go não suporta
conversões diretas entre eles.
Então vale a pena escrever isso, mesmo que `fmt.Stringer` exista.

### Contracts com múltiplos tipos

Aqui está um exemplo de um contract com múltiplos type parameters.

	type Graph (type Node, Edge G) struct { ... }

	contract G(Node, Edge) {
		Node Edges() []Edge
		Edge Nodes() (from Node, to Node)
	}

	func New (type Node, Edge G) (nodes []Node) *Graph(Node, Edge) {
		...
	}

	func (g *Graph(Node, Edge)) ShortestPath(from, to Node) []Edge {
		...
	}

Aqui estamos descrevendo um grafo, construído a partir de nós e arestas.
Não estamos exigindo uma estrutura de dados particular para o grafo.
Em vez disso, estamos dizendo que o tipo `Node` tem que ter um método `Edges`
que retorna a lista de arestas que conectam ao `Node`.
E o tipo `Edge` tem que ter um método `Nodes` que retorna os dois
`Nodes` que a `Edge` conecta.

Omiti a implementação, mas isso mostra a assinatura de uma
função `New` que retorna um `Graph`, e a assinatura de um
método `ShortestPath` em `Graph`.

O ponto importante aqui é que um contract não é apenas sobre um
único tipo. Ele pode descrever as relações entre dois ou mais
tipos.

### Tipos ordenados

Uma reclamação surpreendentemente comum sobre Go é que ele não tem uma
função `Min`.
Ou, para falar nisso, uma função `Max`.
Isso é porque uma função `Min` útil deveria funcionar para qualquer tipo
ordenado, o que significa que tem que ser generic.

Embora `Min` seja bem trivial de escrever você mesmo, qualquer implementação de generics
útil deveria nos permitir adicioná-la à biblioteca padrão.
É assim que fica com nosso design.

{{raw `
	func Min (type T Ordered) (a, b T) T {
		if a < b {
			return a
		}
		return b
	}
`}}

O contract `Ordered` diz que o tipo T tem que ser um tipo ordenado,
o que significa que suporta operadores como menor que, maior que,
e assim por diante.

	contract Ordered(T) {
		T int, int8, int16, int32, int64,
			uint, uint8, uint16, uint32, uint64, uintptr,
			float32, float64,
			string
	}

O contract `Ordered` é apenas uma lista de todos os tipos ordenados que
são definidos pela linguagem.
Este contract aceita qualquer um dos tipos listados, ou qualquer tipo nomeado cujo
tipo subjacente seja um desses tipos.
Basicamente, qualquer tipo que você possa usar com o operador menor que.

Acontece que é muito mais fácil simplesmente enumerar os tipos que
suportam o operador menor que do que inventar uma nova notação
que funcione para todos os operadores.
Afinal, em Go, apenas tipos embutidos suportam operadores.

Esta mesma abordagem pode ser usada para qualquer operador, ou mais geralmente
para escrever um contract para qualquer função generic destinada a funcionar com
tipos embutidos.
Permite que quem escreve a função generic especifique claramente o conjunto de
tipos com os quais a função é esperada ser usada.
Permite que quem chama a função generic veja claramente se a
função é aplicável para os tipos sendo usados.

Na prática este contract provavelmente iria para a biblioteca padrão,
e então realmente a função `Min` (que provavelmente também estará na
biblioteca padrão em algum lugar) ficará assim.
Aqui estamos apenas nos referindo ao contract `Ordered` definido no
pacote contracts.

{{raw `
	func Min (type T contracts.Ordered) (a, b T) T {
		if a < b {
			return a
		}
		return b
	}
`}}

### Estruturas de dados generic

Finalmente, vamos olhar para uma estrutura de dados generic simples, uma árvore
binária. Neste exemplo a árvore tem uma função de comparação, então não há
requisitos sobre o tipo do elemento.

	type Tree (type E) struct {
		root    *node(E)
		compare func(E, E) int
	}

	type node (type E) struct {
		val         E
		left, right *node(E)
	}

Aqui está como criar uma nova árvore binária.
A função de comparação é passada para a função `New`.

	func New (type E) (cmp func(E, E) int) *Tree(E) {
		return &Tree(E){compare: cmp}
	}

Um método não exportado retorna um ponteiro ou para o slot contendo v,
ou para a localização na árvore onde deveria ir.

{{raw `
	func (t *Tree(E)) find(v E) **node(E) {
		pn := &t.root
		for *pn != nil {
			switch cmp := t.compare(v, (*pn).val); {
			case cmp < 0:
				pn = &(*pn).left
			case cmp > 0:
				pn = &(*pn).right
			default:
				return pn
			}
		}
		return pn
	}
`}}

Os detalhes aqui realmente não importam, especialmente já que não
testei este código.
Estou apenas tentando mostrar como fica escrever uma estrutura de dados
generic simples.

Este é o código para testar se a árvore contém um valor.

	func (t *Tree(E)) Contains(v E) bool {
		return *t.find(e) != nil
	}

Este é o código para inserir um novo valor.

	func (t *Tree(E)) Insert(v E) bool {
		pn := t.find(v)
		if *pn != nil {
			return false
		}
		*pn = &node(E){val: v}
		return true
	}

Note que o tipo `node` tem um argumento de tipo `E`.
É assim que fica escrever uma estrutura de dados generic.
Como você pode ver, parece escrever código Go comum, exceto que
alguns argumentos de tipo são salpicados aqui e ali.

Usar a árvore é bem simples.

	var intTree = tree.New(func(a, b int) int { return a - b })

	func InsertAndCheck(v int) {
		intTree.Insert(v)
		if !intTree.Contains(v) {
			log.Fatalf("%d not found after insertion", v)
		}
	}

Isso é como deveria ser.
É um pouco mais difícil escrever uma estrutura de dados generic, porque você frequentemente
tem que escrever explicitamente argumentos de tipo para tipos de suporte, mas
o máximo possível usar uma não é diferente de usar uma
estrutura de dados comum não-generic.

### Próximos passos

Estamos trabalhando em implementações reais para nos permitir experimentar
com este design.
É importante poder experimentar o design na prática, para ter certeza
de que podemos escrever os tipos de programas que queremos escrever.
Não foi tão rápido quanto esperávamos, mas enviaremos mais detalhes
sobre estas implementações à medida que ficarem disponíveis.

Robert Griesemer escreveu uma
[CL preliminar](/cl/187317)
que modifica o pacote go/types.
Isso permite testar se código usando generics e contracts pode
verificar tipos.
Está incompleto agora, mas funciona principalmente para um único pacote,
e continuaremos trabalhando nele.

O que gostaríamos que as pessoas fizessem com esta e futuras implementações é
tentar escrever e usar código generic e ver o que acontece.
Queremos ter certeza de que as pessoas podem escrever o código de que precisam, e
que podem usá-lo como esperado.
Claro que nem tudo vai funcionar no início, e à medida que exploramos
este espaço podemos ter que mudar coisas.
E, para deixar claro, estamos muito mais interessados em feedback sobre a
semântica do que em detalhes da sintaxe.

Gostaria de agradecer a todos que comentaram sobre o design anterior, e
a todos que discutiram como generics podem parecer em Go.
Lemos todos os comentários, e apreciamos muito o trabalho
que as pessoas colocaram nisso.
Não estaríamos onde estamos hoje sem esse trabalho.

Nosso objetivo é chegar a um design que torne possível escrever os
tipos de código generic que discuti hoje, sem tornar a
linguagem muito complexa de usar ou fazendo com que não pareça mais Go.
Esperamos que este design seja um passo em direção a esse objetivo, e esperamos
continuar a ajustá-lo à medida que aprendemos, de nossas experiências e das suas,
o que funciona e o que não funciona.
Se chegarmos a esse objetivo, então teremos algo que podemos
propor para versões futuras do Go.

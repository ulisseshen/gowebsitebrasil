---
ia-translated: true
title: "Go Slices: uso e detalhes internos"
date: 2011-01-05
by:
- Andrew Gerrand
tags:
- slice
- technical
summary: Como usar slices do Go e como elas funcionam.
---

## Introdução

O tipo slice do Go fornece uma maneira conveniente e eficiente de trabalhar com
sequências de dados tipados.
Slices são análogos a arrays em outras linguagens,
mas possuem algumas propriedades incomuns.
Este artigo examinará o que são slices e como são usados.

## Arrays

O tipo slice é uma abstração construída sobre o tipo array do Go,
e então para entender slices devemos primeiro entender arrays.

Uma definição de tipo array especifica um comprimento e um tipo de elemento.
Por exemplo, o tipo `[4]int` representa um array de quatro inteiros.
O tamanho de um array é fixo; seu comprimento faz parte de seu tipo (`[4]int` e `[5]int` são tipos distintos
e incompatíveis).
Arrays podem ser indexados da maneira usual, então a expressão `s[n]` acessa
o elemento n, começando do zero.

	var a [4]int
	a[0] = 1
	i := a[0]
	// i == 1

Arrays não precisam ser inicializados explicitamente;
o zero value de um array é um array pronto para uso cujos elementos são eles mesmos zerados:

	// a[2] == 0, the zero value of the int type

A representação na memória de `[4]int` são apenas quatro valores inteiros dispostos sequencialmente:

{{image "slices-intro/slice-array.png"}}

Os arrays do Go são valores. Uma variável array denota o array inteiro;
não é um pointer para o primeiro elemento do array (como seria o caso em C).
Isso significa que quando você atribui ou passa um valor array você fará
uma cópia de seu conteúdo.
(Para evitar a cópia você poderia passar um _pointer_ para o array,
mas então isso é um pointer para um array, não um array.) Uma maneira de pensar sobre
arrays é como um tipo de struct, mas com campos indexados em vez de nomeados:
um valor composto de tamanho fixo.

Um literal array pode ser especificado assim:

	b := [2]string{"Penn", "Teller"}

Ou você pode deixar o compilador contar os elementos do array para você:

	b := [...]string{"Penn", "Teller"}

Em ambos os casos, o tipo de `b` é `[2]string`.

## Slices

Arrays têm seu lugar, mas são um pouco inflexíveis,
então você não os vê com tanta frequência no código Go.
Slices, no entanto, estão em toda parte. Eles se constroem sobre arrays para fornecer grande poder e conveniência.

A especificação de tipo para um slice é `[]T`,
onde `T` é o tipo dos elementos do slice.
Diferentemente de um tipo array, um tipo slice não tem comprimento especificado.

Um literal slice é declarado como um literal array, exceto que você deixa de fora a contagem de elementos:

	letters := []string{"a", "b", "c", "d"}

Um slice pode ser criado com a função built-in chamada `make`, que tem a assinatura,

	func make([]T, len, cap) []T

onde T representa o tipo de elemento do slice a ser criado.
A função `make` recebe um tipo, um comprimento,
e uma capacidade opcional.
Quando chamada, `make` aloca um array e retorna um slice que se refere a esse array.

	var s []byte
	s = make([]byte, 5, 5)
	// s == []byte{0, 0, 0, 0, 0}

Quando o argumento de capacidade é omitido, ele assume por padrão o comprimento especificado.
Aqui está uma versão mais sucinta do mesmo código:

	s := make([]byte, 5)

O comprimento e a capacidade de um slice podem ser inspecionados usando as funções built-in `len` e `cap`.

	len(s) == 5
	cap(s) == 5

As próximas duas seções discutem a relação entre comprimento e capacidade.

O zero value de um slice é `nil`. As funções `len` e `cap` retornarão ambas 0 para um nil slice.

Um slice também pode ser formado "fatiando" um slice ou array existente.
O fatiamento é feito especificando um intervalo semi-aberto com dois índices separados por dois-pontos.
Por exemplo, a expressão `b[1:4]` cria um slice incluindo os elementos
1 a 3 de `b` (os índices do slice resultante serão 0 a 2).

	b := []byte{'g', 'o', 'l', 'a', 'n', 'g'}
	// b[1:4] == []byte{'o', 'l', 'a'}, sharing the same storage as b

Os índices de início e fim de uma expressão slice são opcionais; eles assumem por padrão zero e o comprimento do slice respectivamente:

	// b[:2] == []byte{'g', 'o'}
	// b[2:] == []byte{'l', 'a', 'n', 'g'}
	// b[:] == b

Esta também é a sintaxe para criar um slice dado um array:

	x := [3]string{"Лайка", "Белка", "Стрелка"}
	s := x[:] // a slice referencing the storage of x

## Detalhes internos de slices

Um slice é um descritor de um segmento de array.
Ele consiste de um pointer para o array, o comprimento do segmento,
e sua capacidade (o comprimento máximo do segmento).

{{image "slices-intro/slice-struct.png"}}

Nossa variável `s`, criada anteriormente por `make([]byte, 5)`, está estruturada assim:

{{image "slices-intro/slice-1.png"}}

O comprimento é o número de elementos referenciados pelo slice.
A capacidade é o número de elementos no array subjacente (começando
no elemento referenciado pelo pointer do slice).
A distinção entre comprimento e capacidade ficará clara conforme percorremos
os próximos exemplos.

À medida que fatiamos `s`, observe as mudanças na estrutura de dados do slice e sua relação com o array subjacente:

	s = s[2:4]

{{image "slices-intro/slice-2.png"}}

Fatiar não copia os dados do slice. Ele cria um novo valor slice que
aponta para o array original.
Isso torna as operações de slice tão eficientes quanto manipular índices de array.
Portanto, modificar os _elementos_ (não o slice em si) de um re-slice
modifica os elementos do slice original:

	d := []byte{'r', 'o', 'a', 'd'}
	e := d[2:]
	// e == []byte{'a', 'd'}
	e[1] = 'm'
	// e == []byte{'a', 'm'}
	// d == []byte{'r', 'o', 'a', 'm'}

Anteriormente fatiamos `s` para um comprimento menor que sua capacidade. Podemos aumentar s até sua capacidade fatiando-o novamente:

	s = s[:cap(s)]

{{image "slices-intro/slice-3.png"}}

Um slice não pode ser aumentado além de sua capacidade.
Tentar fazer isso causará um runtime panic,
assim como ao indexar fora dos limites de um slice ou array.
Da mesma forma, slices não podem ser re-fatiados abaixo de zero para acessar elementos anteriores no array.

## Aumentando slices (as funções copy e append)

Para aumentar a capacidade de um slice é necessário criar um novo
slice maior e copiar o conteúdo do slice original para ele.
Esta técnica é como implementações de arrays dinâmicos de outras linguagens
funcionam nos bastidores.
O próximo exemplo dobra a capacidade de `s` criando um novo slice,
`t`, copiando o conteúdo de `s` para `t`,
e então atribuindo o valor slice `t` a `s`:

	t := make([]byte, len(s), (cap(s)+1)*2) // +1 in case cap(s) == 0
	for i := range s {
	        t[i] = s[i]
	}
	s = t

A parte de loop desta operação comum é facilitada pela função built-in copy.
Como o nome sugere, copy copia dados de um slice de origem para um slice de destino.
Ela retorna o número de elementos copiados.

	func copy(dst, src []T) int

A função `copy` suporta copiar entre slices de comprimentos diferentes
(ela copiará apenas até o menor número de elementos).
Além disso, `copy` pode lidar com slices de origem e destino que compartilham
o mesmo array subjacente,
lidando com slices sobrepostos corretamente.

Usando `copy`, podemos simplificar o trecho de código acima:

	t := make([]byte, len(s), (cap(s)+1)*2)
	copy(t, s)
	s = t

Uma operação comum é adicionar dados ao final de um slice.
Esta função adiciona elementos byte a um slice de bytes,
aumentando o slice se necessário, e retorna o valor slice atualizado:

	func AppendByte(slice []byte, data ...byte) []byte {
	    m := len(slice)
	    n := m + len(data)
	    if n > cap(slice) { // if necessary, reallocate
	        // allocate double what's needed, for future growth.
	        newSlice := make([]byte, (n+1)*2)
	        copy(newSlice, slice)
	        slice = newSlice
	    }
	    slice = slice[0:n]
	    copy(slice[m:n], data)
	    return slice
	}

Pode-se usar `AppendByte` assim:

	p := []byte{2, 3, 5}
	p = AppendByte(p, 7, 11, 13)
	// p == []byte{2, 3, 5, 7, 11, 13}

Funções como `AppendByte` são úteis porque oferecem controle completo
sobre a maneira como o slice é aumentado.
Dependendo das características do programa,
pode ser desejável alocar em pedaços menores ou maiores,
ou colocar um limite no tamanho de uma realocação.

Mas a maioria dos programas não precisa de controle completo,
então Go fornece uma função built-in `append` que é boa para a maioria dos propósitos;
ela tem a assinatura

	func append(s []T, x ...T) []T

A função `append` adiciona os elementos `x` ao final do slice `s`,
e aumenta o slice se uma capacidade maior for necessária.

	a := make([]int, 1)
	// a == []int{0}
	a = append(a, 1, 2, 3)
	// a == []int{0, 1, 2, 3}

Para adicionar um slice a outro, use `...` para expandir o segundo argumento para uma lista de argumentos.

	a := []string{"John", "Paul"}
	b := []string{"George", "Ringo", "Pete"}
	a = append(a, b...) // equivalent to "append(a, b[0], b[1], b[2])"
	// a == []string{"John", "Paul", "George", "Ringo", "Pete"}

Como o zero value de um slice (`nil`) age como um slice de comprimento zero,
você pode declarar uma variável slice e então adicionar a ela em um loop:

	// Filter returns a new slice holding only
	// the elements of s that satisfy fn()
	func Filter(s []int, fn func(int) bool) []int {
	    var p []int // == nil
	    for _, v := range s {
	        if fn(v) {
	            p = append(p, v)
	        }
	    }
	    return p
	}

## Uma possível "armadilha"

Como mencionado anteriormente, re-fatiar um slice não faz uma cópia do array subjacente.
O array completo será mantido na memória até que não seja mais referenciado.
Ocasionalmente isso pode fazer com que o programa mantenha todos os dados na memória quando
apenas uma pequena parte deles é necessária.

Por exemplo, esta função `FindDigits` carrega um arquivo na memória e procura
por ele pelo primeiro grupo de dígitos numéricos consecutivos,
retornando-os como um novo slice.

	var digitRegexp = regexp.MustCompile("[0-9]+")

	func FindDigits(filename string) []byte {
	    b, _ := ioutil.ReadFile(filename)
	    return digitRegexp.Find(b)
	}

Este código se comporta como anunciado, mas o `[]byte` retornado aponta para um
array contendo o arquivo inteiro.
Como o slice referencia o array original,
enquanto o slice for mantido por perto o garbage collector não pode liberar o array;
os poucos bytes úteis do arquivo mantêm o conteúdo inteiro na memória.

Para corrigir este problema pode-se copiar os dados interessantes para um novo slice antes de retorná-lo:

	func CopyDigits(filename string) []byte {
	    b, _ := ioutil.ReadFile(filename)
	    b = digitRegexp.Find(b)
	    c := make([]byte, len(b))
	    copy(c, b)
	    return c
	}

Uma versão mais concisa desta função poderia ser construída usando `append`.
Isso fica como exercício para o leitor.

## Leitura adicional

[Effective Go](/doc/effective_go.html) contém um tratamento aprofundado de
[slices](/doc/effective_go.html#slices)
e [arrays](/doc/effective_go.html#arrays),
e a [especificação da linguagem](/doc/go_spec.html) Go
define [slices](/doc/go_spec.html#Slice_types) e
suas [funções](/doc/go_spec.html#Length_and_capacity)
[auxiliares](/doc/go_spec.html#Making_slices_maps_and_channels)
[associadas](/doc/go_spec.html#Appending_and_copying_slices).

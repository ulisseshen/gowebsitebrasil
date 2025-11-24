---
ia-translated: true
title: Maps em Go em ação
date: 2013-02-06
by:
- Andrew Gerrand
tags:
- map
- technical
summary: Como e quando usar maps em Go.
---

## Introdução

Uma das estruturas de dados mais úteis em ciência da computação é a hash table.
Existem muitas implementações de hash table com propriedades variadas,
mas em geral elas oferecem buscas, adições e exclusões rápidas.
Go fornece um tipo map integrado que implementa uma hash table.

## Declaração e inicialização

Um tipo map em Go se parece com isto:

	map[KeyType]ValueType

onde `KeyType` pode ser qualquer tipo que seja [comparável](/ref/spec#Comparison_operators)
(mais sobre isso adiante),
e `ValueType` pode ser qualquer tipo, incluindo outro map!

Esta variável `m` é um map de chaves string para valores int:

	var m map[string]int

Tipos map são tipos de referência, como pointers ou slices,
e portanto o valor de `m` acima é `nil`;
ele não aponta para um map inicializado.
Um map nil se comporta como um map vazio ao ler,
mas tentativas de escrever em um map nil causarão um panic em runtime; não faça isso.
Para inicializar um map, use a função integrada `make`:

	m = make(map[string]int)

A função `make` aloca e inicializa uma estrutura de dados de hash map
e retorna um valor map que aponta para ela.
Os detalhes dessa estrutura de dados são um detalhe de implementação do
runtime e não são especificados pela própria linguagem.
Neste artigo vamos focar no _uso_ de maps,
não em sua implementação.

## Trabalhando com maps

Go fornece uma sintaxe familiar para trabalhar com maps. Esta instrução define a chave `"route"` com o valor `66`:

	m["route"] = 66

Esta instrução recupera o valor armazenado sob a chave `"route"` e o atribui a uma nova variável i:

	i := m["route"]

Se a chave solicitada não existir, obtemos o _zero value_ do tipo do valor.
Neste caso, o tipo do valor é `int`, então o zero value é `0`:

	j := m["root"]
	// j == 0

A função integrada `len` retorna o número de itens em um map:

	n := len(m)

A função integrada `delete` remove uma entrada do map:

	delete(m, "route")

A função `delete` não retorna nada, e não fará nada se a chave especificada não existir.

Uma atribuição de dois valores testa a existência de uma chave:

	i, ok := m["route"]

Nesta instrução, o primeiro valor (`i`) recebe o valor armazenado sob a chave `"route"`.
Se essa chave não existir, `i` é o zero value do tipo do valor (`0`).
O segundo valor (`ok`) é um `bool` que é `true` se a chave existe no
map, e `false` caso contrário.

Para testar uma chave sem recuperar o valor, use um underscore no lugar do primeiro valor:

	_, ok := m["route"]

Para iterar sobre o conteúdo de um map, use a palavra-chave `range`:

	for key, value := range m {
	    fmt.Println("Key:", key, "Value:", value)
	}

Para inicializar um map com alguns dados, use um map literal:

	commits := map[string]int{
	    "rsc": 3711,
	    "r":   2138,
	    "gri": 1908,
	    "adg": 912,
	}

A mesma sintaxe pode ser usada para inicializar um map vazio, que é funcionalmente idêntico a usar a função `make`:

	m = map[string]int{}

## Explorando zero values

Pode ser conveniente que uma recuperação de map produza um zero value quando a chave não está presente.

Por exemplo, um map de valores boolean pode ser usado como uma estrutura de dados semelhante a um conjunto
(lembre-se de que o zero value para o tipo boolean é false).
Este exemplo percorre uma lista encadeada de `Nodes` e imprime seus valores.
Ele usa um map de pointers `Node` para detectar ciclos na lista.

{{code "maps/list.go" `/START/` `/END/`}}

A expressão `visited[n]` é `true` se `n` foi visitado,
ou `false` se `n` não está presente.
Não há necessidade de usar a forma de dois valores para testar a presença de `n` no map;
o zero value padrão faz isso por nós.

Outro exemplo de zero values úteis é um map de slices.
Adicionar a um slice nil apenas aloca um novo slice,
então é uma linha única para adicionar um valor a um map de slices;
não há necessidade de verificar se a chave existe.
No exemplo a seguir, o slice people é preenchido com valores `Person`.
Cada `Person` tem um `Name` e um slice de Likes.
O exemplo cria um map para associar cada like com um slice de pessoas que gostam dele.

{{code "maps/people.go" `/START1/` `/END1/`}}

Para imprimir uma lista de pessoas que gostam de queijo:

{{code "maps/people.go" `/START2/` `/END2/`}}

Para imprimir o número de pessoas que gostam de bacon:

{{code "maps/people.go" `/bacon/`}}

Note que, como tanto range quanto len tratam um slice nil como um slice de comprimento zero,
esses dois últimos exemplos funcionarão mesmo se ninguém gostar de queijo ou bacon (por mais
improvável que isso possa ser).

## Tipos de chave

Como mencionado anteriormente, chaves de map podem ser de qualquer tipo que seja comparável.
A [especificação da linguagem](/ref/spec#Comparison_operators)
define isso precisamente,
mas resumidamente, tipos comparáveis são boolean,
numeric, string, pointer, channel e tipos interface,
e structs ou arrays que contenham apenas esses tipos.
Notavelmente ausentes da lista estão slices, maps e functions;
esses tipos não podem ser comparados usando `==`,
e não podem ser usados como chaves de map.

É óbvio que strings, ints e outros tipos básicos devem estar disponíveis como chaves de map,
mas talvez inesperado são chaves struct.
Struct pode ser usado para indexar dados por múltiplas dimensões.
Por exemplo, este map de maps poderia ser usado para contar acessos a páginas web por país:

	hits := make(map[string]map[string]int)

Isto é um map de string para (map de `string` para `int`).
Cada chave do map externo é o caminho para uma página web com seu próprio map interno.
Cada chave do map interno é um código de país de duas letras.
Esta expressão recupera o número de vezes que um australiano carregou a página de documentação:

	n := hits["/doc/"]["au"]

Infelizmente, esta abordagem se torna complicada ao adicionar dados,
pois para qualquer chave externa você deve verificar se o map interno existe,
e criá-lo se necessário:

	func add(m map[string]map[string]int, path, country string) {
	    mm, ok := m[path]
	    if !ok {
	        mm = make(map[string]int)
	        m[path] = mm
	    }
	    mm[country]++
	}
	add(hits, "/doc/", "au")

Por outro lado, um design que usa um único map com uma chave struct elimina toda essa complexidade:

	type Key struct {
	    Path, Country string
	}
	hits := make(map[Key]int)

Quando uma pessoa vietnamita visita a página inicial,
incrementar (e possivelmente criar) o contador apropriado é uma linha única:

	hits[Key{"/", "vn"}]++

E é igualmente direto ver quantos suíços leram a especificação:

	n := hits[Key{"/ref/spec", "ch"}]

## Concorrência

[Maps não são seguros para uso concorrente](/doc/faq#atomic_maps):
não está definido o que acontece quando você lê e escreve neles simultaneamente.
Se você precisa ler e escrever em um map a partir de goroutines executando concorrentemente,
os acessos devem ser mediados por algum tipo de mecanismo de sincronização.
Uma maneira comum de proteger maps é com [sync.RWMutex](/pkg/sync/#RWMutex).

Esta instrução declara uma variável `counter` que é um struct anônimo
contendo um map e um `sync.RWMutex` embutido.

	var counter = struct{
	    sync.RWMutex
	    m map[string]int
	}{m: make(map[string]int)}

Para ler do counter, adquira o read lock:

	counter.RLock()
	n := counter.m["some_key"]
	counter.RUnlock()
	fmt.Println("some_key:", n)

Para escrever no counter, adquira o write lock:

	counter.Lock()
	counter.m["some_key"]++
	counter.Unlock()

## Ordem de iteração

Ao iterar sobre um map com um loop range,
a ordem de iteração não é especificada e não há garantia de ser a mesma
de uma iteração para a próxima.
Se você requer uma ordem de iteração estável, deve manter uma estrutura de dados separada que especifique essa ordem.
Este exemplo usa um slice separado de chaves ordenadas para imprimir um `map[int]string` na ordem das chaves:

	import "sort"

	var m map[int]string
	var keys []int
	for k := range m {
	    keys = append(keys, k)
	}
	sort.Ints(keys)
	for _, k := range keys {
	    fmt.Println("Key:", k, "Value:", m[k])
	}

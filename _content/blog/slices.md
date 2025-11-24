---
ia-translated: true
title: "Arrays, slices (e strings): A mecânica de 'append'"
date: 2013-09-26
by:
- Rob Pike
tags:
- array
- slice
- string
- copy
- append
summary: Como arrays e slices do Go funcionam, e como usar copy e append.
---

## Introdução

Um dos recursos mais comuns das linguagens de programação procedurais é
o conceito de array.
Arrays parecem coisas simples, mas há muitas perguntas que devem ser
respondidas ao adicioná-los a uma linguagem, tais como:

  - tamanho fixo ou variável?
  - o tamanho faz parte do tipo?
  - como são os arrays multidimensionais?
  - o array vazio tem significado?

As respostas a essas perguntas afetam se os arrays são apenas
um recurso da linguagem ou uma parte central de seu design.

No desenvolvimento inicial de Go, levou cerca de um ano para decidir as respostas
a essas perguntas antes que o design parecesse certo.
O passo chave foi a introdução de _slices_, que se construíram sobre _arrays_
de tamanho fixo para fornecer uma estrutura de dados flexível e extensível.
Até hoje, no entanto, programadores novos em Go frequentemente tropeçam na maneira como slices
funcionam, talvez porque a experiência de outras linguagens tenha colorido seu pensamento.

Neste post tentaremos esclarecer a confusão.
Faremos isso construindo as peças para explicar como a função built-in `append`
funciona, e por que funciona da maneira que funciona.

## Arrays

Arrays são um bloco de construção importante em Go, mas como a fundação de um edifício
eles frequentemente ficam ocultos abaixo de componentes mais visíveis.
Devemos falar sobre eles brevemente antes de passarmos para a ideia mais interessante,
poderosa e proeminente dos slices.

Arrays não são frequentemente vistos em programas Go porque
o tamanho de um array faz parte de seu tipo, o que limita seu poder expressivo.

A declaração

{{code "slices/prog010.go" `/var buffer/`}}

declara a variável `buffer`, que contém 256 bytes.
O tipo de `buffer` inclui seu tamanho, `[256]byte`.
Um array com 512 bytes seria do tipo distinto `[512]byte`.

Os dados associados a um array são apenas isso: um array de elementos.
Esquematicamente, nosso buffer se parece com isso na memória,

	buffer: byte byte byte ... 256 vezes ... byte byte byte

Ou seja, a variável contém 256 bytes de dados e nada mais. Podemos
acessar seus elementos com a sintaxe de indexação familiar, `buffer[0]`, `buffer[1]`,
e assim por diante até `buffer[255]`. (A faixa de índice 0 a 255 cobre
256 elementos.) Tentar indexar `buffer` com um valor fora dessa
faixa fará o programa travar.

Há uma função built-in chamada `len` que retorna o número de elementos
de um array ou slice e também de alguns outros tipos de dados.
Para arrays, é óbvio o que `len` retorna.
Em nosso exemplo, `len(buffer)` retorna o valor fixo 256.

Arrays têm seu lugar—eles são uma boa representação de uma matriz de transformação,
por exemplo—mas seu propósito mais comum em Go é conter armazenamento
para um slice.

## Slices: O header de slice

Slices são onde a ação está, mas para usá-los bem é preciso entender
exatamente o que eles são e o que fazem.

Um slice é uma estrutura de dados que descreve uma seção contígua de um array
armazenado separadamente da variável slice em si.
_Um slice não é um array_.
Um slice _descreve_ um pedaço de um array.

Dada nossa variável array `buffer` da seção anterior, poderíamos criar
um slice que descreve os elementos 100 a 150 (para ser preciso, 100 a 149,
inclusivo) fazendo _slicing_ do array:

{{code "slices/prog010.go" `/var slice/`}}

Nesse trecho usamos a declaração de variável completa para ser explícito.
A variável `slice` tem tipo `[]byte`, pronunciado "slice de bytes",
e é inicializada a partir do array, chamado
`buffer`, fazendo slicing dos elementos 100 (inclusivo) a 150 (exclusivo).
A sintaxe mais idiomática omitiria o tipo, que é definido pela expressão de inicialização:

	var slice = buffer[100:150]

Dentro de uma função poderíamos usar a forma de declaração curta,

	slice := buffer[100:150]

O que exatamente é essa variável slice?
Não é bem a história completa, mas por enquanto pense em um
slice como uma pequena estrutura de dados com dois elementos: um comprimento e um ponteiro para um elemento
de um array.
Você pode pensar nisso como sendo construído assim nos bastidores:

	type sliceHeader struct {
		Length        int
		ZerothElement *byte
	}

	slice := sliceHeader{
		Length:        50,
		ZerothElement: &buffer[100],
	}

Claro, isso é apenas uma ilustração.
Apesar do que este trecho diz, a struct `sliceHeader` não é visível
para o programador, e o tipo
do ponteiro de elemento depende do tipo dos elementos,
mas isso dá a ideia geral da mecânica.

Até agora usamos uma operação de slice em um array, mas também podemos fazer slice de um slice, assim:

	slice2 := slice[5:10]

Assim como antes, essa operação cria um novo slice, neste caso com elementos
5 a 9 (inclusivo) do slice original, o que significa elementos
105 a 109 do array original.
A struct `sliceHeader` subjacente para a variável `slice2` se parece com
isso:

	slice2 := sliceHeader{
		Length:        5,
		ZerothElement: &buffer[105],
	}

Note que esse header ainda aponta para o mesmo array subjacente, armazenado na
variável `buffer`.

Também podemos fazer _reslice_, ou seja, fazer slice de um slice e armazenar o resultado de volta na
estrutura slice original. Depois de

	slice = slice[5:10]

a estrutura `sliceHeader` para a variável `slice` se parece exatamente como ficou para a variável `slice2`.
Você verá reslicing usado frequentemente, por exemplo para truncar um slice. Esta declaração remove
o primeiro e último elementos do nosso slice:

	slice = slice[1:len(slice)-1]

[Exercício: Escreva como a struct `sliceHeader` fica após esta atribuição.]

Você frequentemente ouvirá programadores Go experientes falar sobre o "header de slice"
porque isso realmente é o que é armazenado em uma variável slice.
Por exemplo, quando você chama uma função que recebe um slice como argumento, como
[bytes.IndexRune](/pkg/bytes/#IndexRune), esse header é
o que é passado para a função.
Nesta chamada,

	slashPos := bytes.IndexRune(slice, '/')

o argumento `slice` que é passado para a função `IndexRune` é, de fato,
um "header de slice".

Há mais um item de dados no header de slice, sobre o qual falaremos abaixo,
mas primeiro vamos ver o que a existência do header de slice significa quando você
programa com slices.

## Passando slices para funções

É importante entender que mesmo que um slice contenha um ponteiro,
ele próprio é um valor.
Por baixo dos panos, é um valor de struct contendo um ponteiro e um comprimento.
Ele _não_ é um ponteiro para uma struct.

Isso importa.

Quando chamamos `IndexRune` no exemplo anterior,
foi passada uma _cópia_ do header de slice.
Esse comportamento tem ramificações importantes.

Considere esta função simples:

{{code "slices/prog010.go" `/^func/` `/^}/`}}

Ela faz exatamente o que seu nome implica, iterando sobre os índices de um slice
(usando um loop `for` `range`), incrementando seus elementos.

Experimente:

{{play "slices/prog010.go" `/^func main/` `/^}/`}}

(Você pode editar e re-executar esses trechos executáveis se quiser explorar.)

Mesmo que o _header_ de slice seja passado por valor, o header inclui
um ponteiro para elementos de um array, então tanto o header de slice original
quanto a cópia do header passada para a função descrevem o mesmo
array.
Portanto, quando a função retorna, os elementos modificados podem
ser vistos através da variável slice original.

O argumento para a função realmente é uma cópia, como este exemplo mostra:

{{play "slices/prog020.go" `/^func/` `$`}}

Aqui vemos que o _conteúdo_ de um argumento slice pode ser modificado por uma função,
mas seu _header_ não pode.
O comprimento armazenado na variável `slice` não é modificado pela chamada à função,
já que a função recebe uma cópia do header de slice, não o original.
Assim, se quisermos escrever uma função que modifica o header, devemos retorná-lo como um
parâmetro de resultado, exatamente como fizemos aqui.
A variável `slice` permanece inalterada, mas o valor retornado tem o novo comprimento,
que é então armazenado em `newSlice`.

## Ponteiros para slices: Receivers de método

Outra maneira de ter uma função que modifica o header de slice é passar um ponteiro para ele.
Aqui está uma variante do nosso exemplo anterior que faz isso:

{{play "slices/prog030.go" `/^func/` `$`}}

Parece desajeitado nesse exemplo, especialmente lidando com o nível extra de indireção
(uma variável temporária ajuda),
mas há um caso comum onde você vê ponteiros para slices.
É idiomático usar um receiver de ponteiro para um método que modifica um slice.

Digamos que quiséssemos ter um método em um slice que o trunca na última barra.
Poderíamos escrevê-lo assim:

{{play "slices/prog040.go" `/^type/` `$`}}

Se você executar este exemplo verá que funciona corretamente, atualizando o slice no caller.

[Exercício: Mude o tipo do receiver para ser um valor em vez
de um ponteiro e execute novamente. Explique o que acontece.]

Por outro lado, se quiséssemos escrever um método para `path` que coloca em maiúsculas
as letras ASCII no path (paroquialmente ignorando nomes não-ingleses), o método poderia
ser um valor porque o receiver de valor ainda apontará para o mesmo array subjacente.

{{play "slices/prog050.go" `/^type/` `$`}}

Aqui o método `ToUpper` usa duas variáveis na construção `for` `range`
para capturar o índice e elemento do slice.
Esta forma de loop evita escrever `p[i]` várias vezes no corpo.

[Exercício: Converta o método `ToUpper` para usar um receiver de ponteiro e veja se seu comportamento muda.]

[Exercício avançado: Converta o método `ToUpper` para lidar com letras Unicode, não apenas ASCII.]

## Capacity

Veja a seguinte função que estende seu argumento slice de `ints` em um elemento:

{{code "slices/prog060.go" `/^func Extend/` `/^}/`}}

(Por que ela precisa retornar o slice modificado?) Agora execute-a:

{{play "slices/prog060.go" `/^func main/` `/^}/`}}

Veja como o slice cresce até... não crescer mais.

É hora de falar sobre o terceiro componente do header de slice: sua _capacity_.
Além do ponteiro de array e comprimento, o header de slice também armazena sua capacity:

	type sliceHeader struct {
		Length        int
		Capacity      int
		ZerothElement *byte
	}

O campo `Capacity` registra quanto espaço o array subjacente realmente tem; é o valor máximo
que `Length` pode alcançar.
Tentar aumentar o slice além de sua capacity ultrapassará os limites do array e acionará um panic.

Depois que nosso slice de exemplo é criado por

	slice := iBuffer[0:0]

seu header se parece com isso:

	slice := sliceHeader{
		Length:        0,
		Capacity:      10,
		ZerothElement: &iBuffer[0],
	}

O campo `Capacity` é igual ao comprimento do array subjacente,
menos o índice no array do primeiro elemento do slice (zero neste caso).
Se você quiser consultar qual é a capacity de um slice, use a função built-in `cap`:

	if cap(slice) == len(slice) {
		fmt.Println("slice is full!")
	}

## Make

E se quisermos aumentar o slice além de sua capacity?
Você não pode!
Por definição, a capacity é o limite para crescimento.
Mas você pode alcançar um resultado equivalente alocando um novo array, copiando os dados, e modificando
o slice para descrever o novo array.

Vamos começar com alocação.
Poderíamos usar a função built-in `new` para alocar um array maior
e então fazer slice do resultado,
mas é mais simples usar a função built-in `make` em vez disso.
Ela aloca um novo array e
cria um header de slice para descrevê-lo, tudo de uma vez.
A função `make` recebe três argumentos: o tipo do slice, seu comprimento inicial, e sua capacity, que é o
comprimento do array que `make` aloca para conter os dados do slice.
Esta chamada cria um slice de comprimento 10 com espaço para mais 5 (15-10), como você pode ver executando:

{{play "slices/prog070.go" `/slice/` `/fmt/`}}

Este trecho dobra a capacity do nosso slice de `int` mas mantém seu comprimento o mesmo:

{{play "slices/prog080.go" `/slice/` `/OMIT/`}}

Após executar este código, o slice tem muito mais espaço para crescer antes de precisar de outra realocação.

Ao criar slices, frequentemente é verdade que o comprimento e capacity serão os mesmos.
A função built-in `make` tem um atalho para este caso comum.
O argumento de comprimento assume como padrão a capacity, então você pode deixá-lo de fora
para definir ambos com o mesmo valor.
Depois de

	gophers := make([]Gopher, 10)

o slice `gophers` tem tanto seu comprimento quanto capacity definidos como 10.

## Copy

Quando dobramos a capacity do nosso slice na seção anterior,
escrevemos um loop para copiar os dados antigos para o novo slice.
Go tem uma função built-in, `copy`, para tornar isso mais fácil.
Seus argumentos são dois slices, e ela copia os dados do argumento da direita para o argumento da esquerda.
Aqui está nosso exemplo reescrito para usar `copy`:

{{play "slices/prog090.go" `/newSlice/` `/newSlice/`}}

A função `copy` é inteligente.
Ela apenas copia o que pode, prestando atenção aos comprimentos de ambos os argumentos.
Em outras palavras, o número de elementos que ela copia é o mínimo dos comprimentos dos dois slices.
Isso pode economizar um pouco de contabilidade.
Além disso, `copy` retorna um valor inteiro, o número de elementos que copiou, embora nem sempre valha a pena verificar.

A função `copy` também acerta quando origem e destino se sobrepõem, o que significa que pode ser usada para deslocar
itens dentro de um único slice.
Aqui está como usar `copy` para inserir um valor no meio de um slice.

{{code "slices/prog100.go" `/Insert/` `/^}/`}}

Há algumas coisas a notar nesta função.
Primeiro, é claro, ela deve retornar o slice atualizado porque seu comprimento mudou.
Segundo, ela usa um atalho conveniente.
A expressão

	slice[i:]

significa exatamente o mesmo que

	slice[i:len(slice)]

Além disso, embora ainda não tenhamos usado o truque, também podemos deixar de fora o primeiro elemento de uma expressão de slice;
ele assume zero como padrão. Assim

	slice[:]

apenas significa o próprio slice, o que é útil ao fazer slice de um array.
Esta expressão é a maneira mais curta de dizer "um slice descrevendo todos os elementos do array":

	array[:]

Agora que isso está resolvido, vamos executar nossa função `Insert`.

{{play "slices/prog100.go" `/make/` `/OMIT/`}}

## Append: Um exemplo

Algumas seções atrás, escrevemos uma função `Extend` que estende um slice em um elemento.
Ela tinha bugs, no entanto, porque se a capacity do slice fosse muito pequena, a função
travaria.
(Nosso exemplo `Insert` tem o mesmo problema.)
Agora temos as peças no lugar para corrigir isso, então vamos escrever uma implementação robusta de
`Extend` para slices de inteiros.

{{code "slices/prog110.go" `/func Extend/` `/^}/`}}

Neste caso é especialmente importante retornar o slice, já que quando ele realoca
o slice resultante descreve um array completamente diferente.
Aqui está um pequeno trecho para demonstrar o que acontece conforme o slice vai enchendo:

{{play "slices/prog110.go" `/START/` `/END/`}}

Note a realocação quando o array inicial de tamanho 5 é preenchido.
Tanto a capacity quanto o endereço do elemento zero mudam quando o novo array é alocado.

Com a função `Extend` robusta como guia, podemos escrever uma função ainda mais legal que nos permite
estender o slice por múltiplos elementos.
Para fazer isso, usamos a habilidade do Go de transformar uma lista de argumentos de função em um slice quando a
função é chamada.
Ou seja, usamos o recurso de função variádica do Go.

Vamos chamar a função de `Append`.
Para a primeira versão, podemos apenas chamar `Extend` repetidamente para que o mecanismo da função variádica fique claro.
A assinatura de `Append` é esta:

	func Append(slice []int, items ...int) []int

O que isso diz é que `Append` recebe um argumento, um slice, seguido por zero ou mais
argumentos `int`.
Esses argumentos são exatamente um slice de `int` no que diz respeito à implementação
de `Append`, como você pode ver:

{{code "slices/prog120.go" `/Append/` `/^}/`}}

Note o loop `for` `range` iterando sobre os elementos do argumento `items`, que tem tipo implícito `[]int`.
Note também o uso do identificador em branco `_` para descartar o índice no loop, que não precisamos neste caso.

Experimente:

{{play "slices/prog120.go" `/START/` `/END/`}}

Outra técnica nova neste exemplo é que inicializamos o slice escrevendo um literal composto,
que consiste no tipo do slice seguido por seus elementos entre chaves:

{{code "slices/prog120.go" `/slice := /`}}

A função `Append` é interessante por outro motivo.
Não apenas podemos adicionar elementos, podemos adicionar um segundo slice inteiro
"explodindo" o slice em argumentos usando a notação `...` no local da chamada:

{{play "slices/prog130.go" `/START/` `/END/`}}

Claro, podemos tornar `Append` mais eficiente alocando não mais de uma vez,
construindo sobre as entranhas de `Extend`:

{{code "slices/prog140.go" `/Append/` `/^}/`}}

Aqui, note como usamos `copy` duas vezes, uma vez para mover os dados do slice para a memória
recém-alocada, e então para copiar os itens a serem adicionados ao final dos dados antigos.

Experimente; o comportamento é o mesmo de antes:

{{play "slices/prog140.go" `/START/` `/END/`}}

## Append: A função built-in

E assim chegamos à motivação para o design da função built-in `append`.
Ela faz exatamente o que nosso exemplo `Append` faz, com eficiência equivalente, mas
funciona para qualquer tipo de slice.

Uma fraqueza do Go é que quaisquer operações de tipo genérico devem ser fornecidas pelo
runtime. Algum dia isso pode mudar, mas por enquanto, para tornar o trabalho com slices
mais fácil, Go fornece uma função genérica built-in `append`.
Ela funciona da mesma forma que nossa versão de slice de `int`, mas para _qualquer_ tipo de slice.

Lembre-se, já que o header de slice é sempre atualizado por uma chamada a `append`, você precisa
salvar o slice retornado após a chamada.
Na verdade, o compilador não permitirá que você chame append sem salvar o resultado.

Aqui estão alguns one-liners intercalados com declarações print. Experimente-os, edite-os e explore:

{{play "slices/prog150.go" `/START/` `/END/`}}

Vale a pena dedicar um momento para pensar sobre o one-liner final desse exemplo em detalhe para entender
como o design de slices torna possível que esta simples chamada funcione corretamente.

Há muito mais exemplos de `append`, `copy`, e outras maneiras de usar slices
na página Wiki construída pela comunidade
["Slice Tricks"](/wiki/SliceTricks).

## Nil

Como um aparte, com nosso conhecimento recém-adquirido podemos ver qual é a representação de um slice `nil`.
Naturalmente, é o valor zero do header de slice:

	sliceHeader{
		Length:        0,
		Capacity:      0,
		ZerothElement: nil,
	}

ou apenas

	sliceHeader{}

O detalhe chave é que o ponteiro de elemento também é `nil`. O slice criado por

	array[0:0]

tem comprimento zero (e talvez até capacity zero) mas seu ponteiro não é `nil`, então
ele não é um slice nil.

Como deve estar claro, um slice vazio pode crescer (assumindo que tem capacity diferente de zero), mas um slice `nil`
não tem array para colocar valores e nunca pode crescer para conter nem mesmo um elemento.

Dito isso, um slice `nil` é funcionalmente equivalente a um slice de comprimento zero, mesmo que aponte
para nada.
Ele tem comprimento zero e pode receber append, com alocação.
Como exemplo, olhe o one-liner acima que copia um slice fazendo append
a um slice `nil`.

## Strings

Agora uma breve seção sobre strings em Go no contexto de slices.

Strings são na verdade muito simples: são apenas slices de bytes somente leitura com um pouco
de suporte sintático extra da linguagem.

Como são somente leitura, não há necessidade de capacity (você não pode aumentá-las),
mas caso contrário, para a maioria dos propósitos você pode tratá-las exatamente como slices
de bytes somente leitura.

Para começar, podemos indexá-las para acessar bytes individuais:

	slash := "/usr/ken"[0] // retorna o valor byte '/'.

Podemos fazer slice de uma string para pegar uma substring:

	usr := "/usr/ken"[0:4] // retorna a string "/usr"

Deve estar óbvio agora o que está acontecendo nos bastidores quando fazemos slice de uma string.

Também podemos pegar um slice normal de bytes e criar uma string a partir dele com a conversão simples:

	str := string(slice)

e ir na direção inversa também:

	slice := []byte(usr)

O array subjacente a uma string está oculto da vista; não há maneira de acessar seu conteúdo
exceto através da string. Isso significa que quando fazemos qualquer uma dessas conversões, uma
cópia do array deve ser feita.
Go cuida disso, é claro, então você não precisa.
Após qualquer uma dessas conversões, modificações no
array subjacente ao slice de bytes não afetam a string correspondente.

Uma consequência importante deste design semelhante a slice para strings é que
criar uma substring é muito eficiente.
Tudo que precisa acontecer
é a criação de um header de string de duas palavras. Já que a string é somente leitura, a string original
e a string resultante da operação de slice podem compartilhar o mesmo array com segurança.

Uma nota histórica: A implementação mais antiga de strings sempre alocava, mas quando slices
foram adicionados à linguagem, eles forneceram um modelo para manipulação eficiente de strings. Alguns dos
benchmarks viram enormes acelerações como resultado.

Há muito mais sobre strings, é claro, e um
[post de blog separado](/blog/strings) as cobre em maior profundidade.

## Conclusão

Para entender como slices funcionam, ajuda entender como eles são implementados.
Há uma pequena estrutura de dados, o header de slice, que é o item associado à variável
slice, e esse header descreve uma seção de um array alocado separadamente.
Quando passamos valores de slice por aí, o header é copiado mas o array para o qual ele aponta
é sempre compartilhado.

Uma vez que você aprecia como eles funcionam, slices se tornam não apenas fáceis de usar, mas
poderosos e expressivos, especialmente com a ajuda das funções built-in `copy` e `append`.

## Mais leitura

Há muito para encontrar pela internet sobre slices em Go.
Como mencionado anteriormente,
a página Wiki ["Slice Tricks"](/wiki/SliceTricks)
tem muitos exemplos.
O post de blog [Go Slices](/blog/go-slices-usage-and-internals)
descreve os detalhes de layout de memória com diagramas claros.
O artigo [Go Data Structures](https://research.swtch.com/godata) de Russ Cox inclui
uma discussão de slices juntamente com algumas das outras estruturas de dados internas do Go.

Há muito mais material disponível, mas a melhor maneira de aprender sobre slices é usá-los.

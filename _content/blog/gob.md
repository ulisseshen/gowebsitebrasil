---
ia-translated: true
title: Gobs de dados
date: 2011-03-24
by:
- Rob Pike
tags:
- gob
- json
- protobuf
- xml
- technical
summary: Apresentando gob, um formato de codificação de alta velocidade de Go para Go.
---

## Introdução

Para transmitir uma estrutura de dados através de uma rede ou armazená-la em um arquivo,
ela deve ser codificada e depois decodificada novamente.
Existem muitas codificações disponíveis, é claro:
[JSON](http://www.json.org/), [XML](http://www.w3.org/XML/),
[protocol buffers](http://code.google.com/p/protobuf) do Google, e mais.
E agora há outra, fornecida pelo package [gob](/pkg/encoding/gob/) de Go.

Por que definir uma nova codificação? Dá muito trabalho e é redundante.
Por que não usar apenas um dos formatos existentes? Bem,
na verdade, usamos!
Go tem [packages](/pkg/) que suportam todas as codificações
mencionadas (o [package protocol buffer](https://github.com/golang/protobuf)
está em um repositório separado, mas é um dos mais frequentemente baixados).
E para muitos propósitos, incluindo comunicação com ferramentas e sistemas escritos em outras linguagens,
eles são a escolha certa.

Mas para um ambiente específico de Go, como comunicação entre dois servidores escritos em Go,
há uma oportunidade de construir algo muito mais fácil de usar e possivelmente mais eficiente.

Gobs funcionam com a linguagem de uma forma que uma codificação externamente definida,
independente de linguagem, não pode.
Ao mesmo tempo, há lições a serem aprendidas com os sistemas existentes.

## Objetivos

O package gob foi projetado com vários objetivos em mente.

Primeiro, e mais óbvio, tinha que ser muito fácil de usar.
Primeiro, porque Go tem reflection, não há necessidade de uma linguagem de
definição de interface separada ou "compilador de protocolo".
A própria estrutura de dados é tudo que o package precisa para descobrir como
codificá-la e decodificá-la.
Por outro lado, essa abordagem significa que gobs nunca funcionarão tão bem
com outras linguagens, mas tudo bem:
gobs são descaradamente Go-cêntricos.

Eficiência também é importante. Representações textuais,
exemplificadas por XML e JSON, são muito lentas para colocar no centro de uma
rede de comunicações eficiente.
Uma codificação binária é necessária.

Streams gob devem ser auto-descritivos. Cada stream gob,
lido desde o início, contém informação suficiente para que todo o
stream possa ser analisado por um agente que não sabe nada a priori sobre seu conteúdo.
Essa propriedade significa que você sempre será capaz de decodificar um stream gob armazenado em um arquivo,
mesmo muito tempo depois de ter esquecido quais dados ele representa.

Também havia algumas coisas para aprender com nossas experiências com protocol buffers do Google.

## Problemas dos protocol buffers

Protocol buffers tiveram um grande efeito no design de gobs,
mas têm três recursos que foram deliberadamente evitados.
(Deixando de lado a propriedade de que protocol buffers não são auto-descritivos:
se você não conhece a definição de dados usada para codificar um protocol buffer,
você pode não ser capaz de analisá-lo.)

Primeiro, protocol buffers só funcionam no tipo de dados que chamamos de struct em Go.
Você não pode codificar um inteiro ou array no nível superior,
apenas um struct com campos dentro dele.
Isso parece uma restrição sem sentido, pelo menos em Go.
Se tudo que você quer enviar é um array de inteiros,
por que você deveria ter que colocá-lo em um struct primeiro?

Segundo, uma definição de protocol buffer pode especificar que os campos `T.x` e `T.y`
são obrigatórios de estarem presentes sempre que um valor do tipo `T` é codificado ou decodificado.
Embora tais campos obrigatórios possam parecer uma boa ideia,
eles são custosos de implementar porque o codec deve manter uma estrutura
de dados separada durante a codificação e decodificação,
para poder reportar quando campos obrigatórios estão faltando.
Eles também são um problema de manutenção. Com o tempo,
pode-se querer modificar a definição de dados para remover um campo obrigatório,
mas isso pode fazer com que clientes existentes dos dados travem.
É melhor não tê-los na codificação.
(Protocol buffers também têm campos opcionais.
Mas se não temos campos obrigatórios, todos os campos são opcionais e pronto.
Haverá mais a dizer sobre campos opcionais um pouco mais tarde.)

O terceiro problema dos protocol buffers são valores padrão.
Se um protocol buffer omite o valor para um campo "com valor padrão",
então a estrutura decodificada se comporta como se o campo tivesse sido definido com aquele valor.
Essa ideia funciona bem quando você tem métodos getter e setter para controlar
o acesso ao campo,
mas é mais difícil de lidar de forma limpa quando o container é apenas uma struct idiomática simples.
Campos obrigatórios também são complicados de implementar:
onde se define os valores padrão,
que tipos eles têm (é texto UTF-8? bytes não interpretados? quantos bits
em um float?) e apesar da aparente simplicidade,
houve uma série de complicações em seu design e implementação
para protocol buffers.
Decidimos deixá-los de fora dos gobs e voltar à regra trivial mas efetiva de valor padrão de Go:
a menos que você defina algo diferente, ele tem o "valor zero" para aquele tipo -
e não precisa ser transmitido.

Então gobs acabam parecendo uma espécie de protocol buffer generalizado e simplificado. Como eles funcionam?

## Valores

Os dados gob codificados não são sobre tipos como `int8` e `uint16`.
Em vez disso, de forma análoga às constantes em Go,
seus valores inteiros são números abstratos, sem tamanho,
assinados ou não assinados.
Quando você codifica um `int8`, seu valor é transmitido como um inteiro sem tamanho,
de comprimento variável.
Quando você codifica um `int64`, seu valor também é transmitido como um inteiro sem tamanho,
de comprimento variável.
(Assinados e não assinados são tratados distintamente,
mas a mesma ausência de tamanho se aplica aos valores não assinados também.) Se ambos têm o valor 7,
os bits enviados no fio serão idênticos.
Quando o receptor decodifica aquele valor, ele o coloca na variável do receptor,
que pode ser de qualquer tipo inteiro.
Assim, um encoder pode enviar um 7 que veio de um `int8`,
mas o receptor pode armazená-lo em um `int64`.
Isso é bom: o valor é um inteiro e desde que caiba, tudo funciona.
(Se não couber, resulta em um erro.) Esse desacoplamento do tamanho da
variável dá alguma flexibilidade à codificação:
podemos expandir o tipo da variável inteira conforme o software evolui,
mas ainda ser capaz de decodificar dados antigos.

Essa flexibilidade também se aplica a ponteiros.
Antes da transmissão, todos os ponteiros são achatados.
Valores do tipo `int8`, `*int8`, `**int8`,
`****int8`, etc. são todos transmitidos como um valor inteiro,
que pode então ser armazenado em `int` de qualquer tamanho,
ou `*int`, ou `******int`, etc.
Novamente, isso permite flexibilidade.

A flexibilidade também acontece porque, ao decodificar um struct,
apenas os campos que são enviados pelo encoder são armazenados no destino. Dado o valor

	type T struct{ X, Y, Z int } // Apenas campos exportados são codificados e decodificados.
	var t = T{X: 7, Y: 0, Z: 8}

a codificação de `t` envia apenas o 7 e 8.
Como é zero, o valor de `Y` nem é enviado;
não há necessidade de enviar um valor zero.

O receptor poderia, em vez disso, decodificar o valor nesta estrutura:

	type U struct{ X, Y *int8 } // Nota: ponteiros para int8s
	var u U

e adquirir um valor de `u` com apenas `X` definido (para o endereço de uma variável `int8` definida como 7);
o campo `Z` é ignorado - onde você o colocaria? Ao decodificar structs,
campos são combinados por nome e tipo compatível,
e apenas campos que existem em ambos são afetados.
Essa abordagem simples resolve o problema de "campo opcional":
conforme o tipo `T` evolui adicionando campos,
receptores desatualizados ainda funcionarão com a parte do tipo que reconhecem.
Assim, gobs fornecem o resultado importante de campos opcionais - extensibilidade -
sem qualquer mecanismo ou notação adicional.

De inteiros podemos construir todos os outros tipos:
bytes, strings, arrays, slices, maps, até floats.
Valores de ponto flutuante são representados por seu padrão de bits de ponto flutuante IEEE 754,
armazenado como um inteiro, o que funciona bem desde que você conheça seu tipo, o que sempre conhecemos.
A propósito, esse inteiro é enviado em ordem de bytes invertida porque valores comuns
de números de ponto flutuante,
como inteiros pequenos, têm muitos zeros na extremidade inferior que podemos evitar transmitir.

Um recurso interessante de gobs que Go torna possível é que eles permitem que você
defina sua própria codificação fazendo com que seu tipo satisfaça as interfaces [GobEncoder](/pkg/encoding/gob/#GobEncoder)
e [GobDecoder](/pkg/encoding/gob/#GobDecoder),
de maneira análoga às interfaces [Marshaler](/pkg/encoding/json/#Marshaler)
e [Unmarshaler](/pkg/encoding/json/#Unmarshaler) do package [JSON](/pkg/encoding/json/)
e também à interface [Stringer](/pkg/fmt/#Stringer)
do [package fmt](/pkg/fmt/).
Essa facilidade torna possível representar recursos especiais,
aplicar restrições, ou ocultar segredos quando você transmite dados.
Veja a [documentação](/pkg/encoding/gob/) para detalhes.

## Tipos no fio

Na primeira vez que você envia um determinado tipo, o package gob inclui no stream
de dados uma descrição daquele tipo.
Na verdade, o que acontece é que o encoder é usado para codificar,
no formato de codificação gob padrão, um struct interno que descreve o
tipo e lhe dá um número único.
(Tipos básicos, mais o layout da estrutura de descrição de tipo,
são predefinidos pelo software para bootstrapping.) Depois que o tipo é descrito,
ele pode ser referenciado por seu número de tipo.

Assim, quando enviamos nosso primeiro tipo `T`, o encoder gob envia uma descrição
de `T` e o marca com um número de tipo, digamos 127.
Todos os valores, incluindo o primeiro, são então prefixados por esse número,
então um stream de valores `T` se parece com:

	("define type id" 127, definition of type T)(127, T value)(127, T value), ...

Esses números de tipo tornam possível descrever tipos recursivos e enviar
valores desses tipos.
Assim, gobs podem codificar tipos como árvores:

	type Node struct {
	    Value       int
	    Left, Right *Node
	}

(É um exercício para o leitor descobrir como a regra de valor padrão zero faz isso funcionar,
mesmo que gobs não representem ponteiros.)

Com a informação de tipo, um stream gob é totalmente auto-descritivo exceto
pelo conjunto de tipos de bootstrap,
que é um ponto de partida bem definido.

## Compilando uma máquina

Na primeira vez que você codifica um valor de um determinado tipo,
o package gob constrói uma pequena máquina interpretada específica para aquele tipo de dados.
Ele usa reflection no tipo para construir aquela máquina,
mas uma vez que a máquina está construída, ela não depende de reflection.
A máquina usa o package unsafe e alguns truques para converter os dados em
bytes codificados em alta velocidade.
Ela poderia usar reflection e evitar unsafe,
mas seria significativamente mais lenta.
(Uma abordagem de alta velocidade similar é adotada pelo suporte a protocol buffer para Go,
cujo design foi influenciado pela implementação de gobs.) Valores subsequentes
do mesmo tipo usam a máquina já compilada,
então eles podem ser codificados imediatamente.

[Atualização: A partir do Go 1.4, o package unsafe não é mais usado pelo package gob, com uma queda modesta de desempenho.]

A decodificação é similar mas mais difícil. Quando você decodifica um valor,
o package gob mantém um slice de bytes representando um valor de um tipo definido pelo encoder a ser decodificado,
mais um valor Go no qual decodificá-lo.
O package gob constrói uma máquina para aquele par:
o tipo gob enviado no fio cruzado com o tipo Go fornecido para decodificação.
Uma vez que aquela máquina de decodificação é construída, no entanto,
é novamente um motor sem reflection que usa métodos unsafe para obter velocidade máxima.

## Uso

Há muita coisa acontecendo por baixo dos panos, mas o resultado é um sistema de codificação eficiente,
fácil de usar para transmitir dados.
Aqui está um exemplo completo mostrando tipos codificados e decodificados diferentes.
Note como é fácil enviar e receber valores;
tudo que você precisa fazer é apresentar valores e variáveis ao [package gob](/pkg/encoding/gob/)
e ele faz todo o trabalho.

	package main

	import (
	    "bytes"
	    "encoding/gob"
	    "fmt"
	    "log"
	)

	type P struct {
	    X, Y, Z int
	    Name    string
	}

	type Q struct {
	    X, Y *int32
	    Name string
	}

	func main() {
	    // Initialize the encoder and decoder.  Normally enc and dec would be
	    // bound to network connections and the encoder and decoder would
	    // run in different processes.
	    var network bytes.Buffer        // Stand-in for a network connection
	    enc := gob.NewEncoder(&network) // Will write to network.
	    dec := gob.NewDecoder(&network) // Will read from network.
	    // Encode (send) the value.
	    err := enc.Encode(P{3, 4, 5, "Pythagoras"})
	    if err != nil {
	        log.Fatal("encode error:", err)
	    }
	    // Decode (receive) the value.
	    var q Q
	    err = dec.Decode(&q)
	    if err != nil {
	        log.Fatal("decode error:", err)
	    }
	    fmt.Printf("%q: {%d,%d}\n", q.Name, *q.X, *q.Y)
	}

Você pode compilar e executar este código de exemplo no [Go Playground](/play/p/_-OJV-rwMq).

O [package rpc](/pkg/net/rpc/) é construído sobre gobs para transformar
esta automação de encode/decode em transporte para chamadas de método através da rede.
Esse é um assunto para outro artigo.

## Detalhes

A [documentação do package gob](/pkg/encoding/gob/),
especialmente o arquivo [doc.go](/src/pkg/encoding/gob/doc.go),
expande muitos dos detalhes descritos aqui e inclui um exemplo completo
mostrando como a codificação representa dados.
Se você está interessado nas entranhas da implementação de gob,
esse é um bom lugar para começar.

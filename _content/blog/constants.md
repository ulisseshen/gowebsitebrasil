---
ia-translated: true
title: Constants
date: 2014-08-25
by:
- Rob Pike
tags:
- constants
summary: Uma introdução às constantes em Go.
---

## Introdução

Go é uma linguagem estaticamente tipada que não permite operações que misturam tipos numéricos.
Você não pode adicionar um `float64` a um `int`, ou mesmo um `int32` a um `int`.
No entanto, é legal escrever `1e6*time.Second` ou `math.Exp(1)` ou até {{raw "`1<<('\t'+2.0)`"}}.
Em Go, constantes, diferentemente de variáveis, se comportam de maneira muito semelhante a números regulares.
Este post explica por que isso acontece e o que isso significa.

## Contexto: C

Nos primeiros dias de pensar sobre Go, conversamos sobre uma série de problemas
causados pela forma como C e seus descendentes permitem que você misture e combine tipos numéricos.
Muitos bugs misteriosos, crashes e problemas de portabilidade são causados por expressões
que combinam inteiros de tamanhos e "signedness" diferentes.
Embora para um programador C experiente o resultado de um cálculo como

	unsigned int u = 1e9;
	long signed int i = -1;
	... i + u ...

possa ser familiar, não é _a priori_ óbvio.
Quão grande é o resultado?
Qual é o seu valor?
Ele é signed ou unsigned?

Bugs desagradáveis se escondem aqui.

C tem um conjunto de regras chamadas "the usual arithmetic conversions" e é
um indicador de sua sutileza que elas mudaram ao longo dos anos (introduzindo
ainda mais bugs, retroativamente).

Ao projetar Go, decidimos evitar esse campo minado exigindo que _não_ haja mistura de tipos numéricos.
Se você quiser adicionar `i` e `u`, deve ser explícito sobre o que deseja que o resultado seja.
Dado

	var u uint
	var i int

você pode escrever `uint(i)+u` ou `i+int(u)`,
com tanto o significado quanto o tipo da adição claramente expressos,
mas ao contrário de C, você não pode escrever `i+u`.
Você não pode nem misturar `int` e `int32`, mesmo quando `int` é um tipo de 32 bits.

Esse rigor elimina uma causa comum de bugs e outras falhas.
É uma propriedade vital do Go.
Mas tem um custo: às vezes requer que programadores decorem seu código
com conversões numéricas desajeitadas para expressar seu significado claramente.

E quanto às constantes?
Dadas as declarações acima, o que tornaria legal escrever `i` `=` `0` ou `u` `=` `0`?
Qual é o _tipo_ de `0`?
Seria irrazoável exigir que constantes tenham conversões de tipo em contextos simples como `i` `=` `int(0)`.

Logo percebemos que a resposta estava em fazer constantes numéricas funcionarem de forma diferente
de como se comportam em outras linguagens similares a C.
Depois de muito pensamento e experimentação, chegamos a um design que
acreditamos parecer certo quase sempre,
liberando o programador de converter constantes o tempo todo, mas sendo
capaz de escrever coisas como `math.Sqrt(2)` sem ser repreendido pelo compilador.

Em resumo, constantes em Go simplesmente funcionam, na maioria das vezes.
Vamos ver como isso acontece.

## Terminologia

Primeiro, uma definição rápida.
Em Go, `const` é uma palavra-chave que introduz um nome para um valor escalar como `2` ou `3.14159` ou `"scrumptious"`.
Tais valores, nomeados ou não, são chamados de _constantes_ em Go.
Constantes também podem ser criadas por expressões construídas a partir de constantes,
como `2+3` ou `2+3i` ou `math.Pi/2` ou `("go"+"pher")`.

Algumas linguagens não têm constantes, e outras têm uma definição mais geral
de constante ou aplicação da palavra `const`.
Em C e C++, por exemplo, `const` é um qualificador de tipo que pode codificar
propriedades mais intrincadas de valores mais intrincados.

Mas em Go, uma constante é apenas um valor simples e imutável, e daqui em diante estamos falando apenas sobre Go.

## Constantes de string

Existem muitos tipos de constantes numéricas—inteiros,
floats, runes, signed, unsigned, imaginárias,
complexas—então vamos começar com uma forma mais simples de constante: strings.
Constantes de string são fáceis de entender e fornecem um espaço menor no qual
explorar as questões de tipo das constantes em Go.

Uma constante de string inclui algum texto entre aspas duplas.
(Go também tem literais de string crua, delimitados por crases <code>``</code>,
mas para o propósito desta discussão eles têm todas as mesmas propriedades.)
Aqui está uma constante de string:

	"Hello, 世界"

(Para muito mais detalhes sobre a representação e interpretação de strings,
veja [este post do blog](/blog/strings).)

Que tipo essa constante de string tem?
A resposta óbvia é `string`, mas isso está _errado_.

Esta é uma _constante de string sem tipo_, ou seja, é um valor textual constante
que ainda não tem um tipo fixo.
Sim, é uma string, mas não é um valor Go do tipo `string`.
Ela permanece uma constante de string sem tipo mesmo quando recebe um nome:

	const hello = "Hello, 世界"

Após esta declaração, `hello` também é uma constante de string sem tipo.
Uma constante sem tipo é apenas um valor, um que ainda não recebeu um tipo definido que
a forçaria a obedecer às regras estritas que impedem a combinação de valores de tipos diferentes.

É essa noção de uma constante _sem tipo_ que torna possível usarmos constantes em Go com grande liberdade.

Então, o que é uma constante de string _com tipo_?
É uma que recebeu um tipo, assim:

	const typedHello string = "Hello, 世界"

Observe que a declaração de `typedHello` tem um tipo `string` explícito antes do sinal de igual.
Isso significa que `typedHello` tem o tipo Go `string`, e não pode ser atribuída a uma variável Go de um tipo diferente.
Ou seja, este código funciona:

{{play "constants/string1.go" `/START/` `/STOP/`}}

mas este não:

{{play "constants/string2.go" `/START/` `/STOP/`}}

A variável `m` tem o tipo `MyString` e não pode receber um valor de um tipo diferente.
Ela só pode receber valores do tipo `MyString`, assim:

{{play "constants/string3.go" `/START/` `/STOP/`}}

ou forçando a questão com uma conversão, assim:

{{play "constants/string4.go" `/START/` `/STOP/`}}

Voltando à nossa constante de string _sem tipo_,
ela tem a propriedade útil de que, como não tem tipo,
atribuí-la a uma variável com tipo não causa um erro de tipo.
Ou seja, podemos escrever

	m = "Hello, 世界"

ou

	m = hello

porque, ao contrário das constantes com tipo `typedHello` e `myStringHello`,
as constantes sem tipo `"Hello, 世界"` e `hello` _não têm tipo_.
Atribuí-las a uma variável de qualquer tipo compatível com strings funciona sem erro.

Essas constantes de string sem tipo são strings,
é claro, então elas só podem ser usadas onde uma string é permitida,
mas elas não têm _tipo_ `string`.

## Tipo padrão

Como programador Go, você certamente já viu muitas declarações como

	str := "Hello, 世界"

e a esta altura você pode estar perguntando, "se a constante é sem tipo, como `str` obtém um tipo nesta declaração de variável?"
A resposta é que uma constante sem tipo tem um tipo padrão,
um tipo implícito que ela transfere para um valor se um tipo é necessário onde nenhum é fornecido.
Para constantes de string sem tipo, esse tipo padrão é obviamente `string`, então

	str := "Hello, 世界"

ou

	var str = "Hello, 世界"

significa exatamente o mesmo que

	var str string = "Hello, 世界"

Uma maneira de pensar sobre constantes sem tipo é que elas vivem em uma espécie de
espaço ideal de valores,
um espaço menos restritivo do que o sistema de tipos completo do Go.
Mas para fazer qualquer coisa com elas, precisamos atribuí-las a variáveis,
e quando isso acontece a _variável_ (não a constante em si) precisa de um tipo,
e a constante pode dizer à variável qual tipo ela deve ter.
Neste exemplo, `str` se torna um valor do tipo `string` porque a constante
de string sem tipo dá à declaração seu tipo padrão, `string`.

Em tal declaração, uma variável é declarada com um tipo e valor inicial.
Às vezes, quando usamos uma constante, no entanto, o destino do valor não é tão claro.
Por exemplo, considere esta instrução:

{{play "constants/default1.go" `/START/` `/STOP/`}}

A assinatura de `fmt.Printf` é

	func Printf(format string, a ...interface{}) (n int, err error)

ou seja, seus argumentos (após a string de formato) são valores de interface.
O que acontece quando `fmt.Printf` é chamado com uma constante sem tipo é que um valor de interface é criado
para passar como argumento, e o tipo concreto armazenado para esse argumento é o tipo padrão da constante.
Este processo é análogo ao que vimos anteriormente ao declarar um valor inicializado usando uma constante de string sem tipo.

Você pode ver o resultado neste exemplo, que usa o formato `%v` para imprimir
o valor e `%T` para imprimir o tipo do valor sendo passado para `fmt.Printf`:

{{play "constants/default2.go" `/START/` `/STOP/`}}

Se a constante tem um tipo, isso vai para a interface, como este exemplo mostra:

{{play "constants/default3.go" `/START/` `/STOP/`}}

(Para mais informações sobre como valores de interface funcionam,
veja as primeiras seções de [este post do blog](/blog/laws-of-reflection).)

Em resumo, uma constante com tipo obedece todas as regras de valores com tipo em Go.
Por outro lado, uma constante sem tipo não carrega um tipo Go da mesma
maneira e pode ser misturada e combinada mais livremente.
No entanto, ela tem um tipo padrão que é exposto quando, e somente quando, nenhuma outra informação de tipo está disponível.

## Tipo padrão determinado pela sintaxe

O tipo padrão de uma constante sem tipo é determinado por sua sintaxe.
Para constantes de string, o único tipo implícito possível é `string`.
Para [constantes numéricas](/ref/spec#Numeric_types), o tipo implícito tem mais variedade.
Constantes inteiras padrão para `int`, constantes de ponto flutuante `float64`,
constantes rune para `rune` (um alias para `int32`),
e constantes imaginárias para `complex128`.
Aqui está nossa instrução print canônica usada repetidamente para mostrar os tipos padrão em ação:

{{play "constants/syntax.go" `/START/` `/STOP/`}}

(Exercício: Explique o resultado para `'x'`.)

## Booleanos

Tudo o que dissemos sobre constantes de string sem tipo pode ser dito para constantes booleanas sem tipo.
Os valores `true` e `false` são constantes booleanas sem tipo que podem ser atribuídas a qualquer variável booleana,
mas uma vez recebido um tipo, variáveis booleanas não podem ser misturadas:

{{play "constants/bool.go" `/START/` `/STOP/`}}

Execute o exemplo e veja o que acontece, depois comente a linha "Bad" e execute novamente.
O padrão aqui segue exatamente o das constantes de string.

## Floats

Constantes de ponto flutuante são como constantes booleanas na maioria dos aspectos.
Nosso exemplo padrão funciona como esperado na tradução:

{{play "constants/float1.go" `/START/` `/STOP/`}}

Uma complicação é que existem _dois_ tipos de ponto flutuante em Go: `float32` e `float64`.
O tipo padrão para uma constante de ponto flutuante é `float64`, embora uma constante de ponto flutuante
sem tipo possa ser atribuída a um valor `float32` sem problemas:

{{play "constants/float2.go" `/START/` `/STOP/`}}

Valores de ponto flutuante são um bom lugar para introduzir o conceito de overflow, ou faixa de valores.

Constantes numéricas vivem em um espaço numérico de precisão arbitrária; elas são apenas números regulares.
Mas quando são atribuídas a uma variável, o valor deve ser capaz de caber no destino.
Podemos declarar uma constante com um valor muito grande:

{{code "constants/float3.go" `/Huge/`}}

—isso é apenas um número, afinal—mas não podemos atribuí-lo ou mesmo imprimi-lo. Esta instrução nem sequer compilará:

{{play "constants/float3.go" `/Println/`}}

O erro é, "constant 1.00000e+1000 overflows float64", o que é verdade.
Mas `Huge` pode ser útil: podemos usá-lo em expressões com outras constantes
e usar o valor dessas expressões se o resultado
puder ser representado na faixa de um `float64`.
A instrução,

{{play "constants/float4.go" `/Println/`}}

imprime `10`, como era de se esperar.

De forma relacionada, constantes de ponto flutuante podem ter precisão muito alta,
de modo que aritmética envolvendo elas é mais precisa.
As constantes definidas no pacote [math](/pkg/math) são fornecidas com muito mais dígitos do que estão
disponíveis em um `float64`. Aqui está a definição de `math.Pi`:

	Pi	= 3.14159265358979323846264338327950288419716939937510582097494459

Quando esse valor é atribuído a uma variável,
alguma precisão será perdida;
a atribuição criará o valor `float64` (ou `float32`)
mais próximo do valor de alta precisão. Este trecho

{{play "constants/float5.go" `/START/` `/STOP/`}}

imprime `3.141592653589793`.

Ter tantos dígitos disponíveis significa que cálculos como `Pi/2` ou outras
avaliações mais intrincadas podem carregar mais precisão
até que o resultado seja atribuído, tornando cálculos envolvendo constantes mais fáceis de escrever sem perder precisão.
Também significa que não há ocasião em que casos extremos de ponto flutuante como infinitos,
soft underflows e `NaNs` surjam em expressões constantes.
(Divisão por um zero constante é um erro de tempo de compilação,
e quando tudo é um número não existe tal coisa como "not a number".)

## Números complexos

Constantes complexas se comportam muito como constantes de ponto flutuante.
Aqui está uma versão de nossa agora familiar ladainha traduzida em números complexos:

{{play "constants/complex1.go" `/START/` `/STOP/`}}

O tipo padrão de um número complexo é `complex128`, a versão de maior precisão composta por dois valores `float64`.

Para clareza em nosso exemplo, escrevemos a expressão completa `(0.0+1.0i)`,
mas esse valor pode ser encurtado para `0.0+1.0i`,
`1.0i` ou mesmo `1i`.

Vamos fazer um truque.
Sabemos que em Go, uma constante numérica é apenas um número.
E se esse número for um número complexo sem parte imaginária, ou seja, um real?
Aqui está um:

{{code "constants/complex2.go" `/const Two/`}}

Essa é uma constante complexa sem tipo.
Mesmo não tendo parte imaginária, a _sintaxe_ da expressão a define para ter o tipo padrão `complex128`.
Portanto, se a usarmos para declarar uma variável, o tipo padrão será `complex128`. O trecho

{{play "constants/complex2.go" `/START/` `/STOP/`}}

imprime `complex128:` `(2+0i)`.
Mas numericamente, `Two` pode ser armazenado em um número de ponto flutuante escalar,
um `float64` ou `float32`, sem perda de informação.
Assim, podemos atribuir `Two` a um `float64`, seja em uma inicialização ou atribuição, sem problemas:

{{play "constants/complex3.go" `/START/` `/STOP/`}}

A saída é `2` `and` `2`.
Mesmo que `Two` seja uma constante complexa, ela pode ser atribuída a variáveis escalares de ponto flutuante.
Essa capacidade de uma constante "cruzar" tipos assim provará ser útil.

## Inteiros

Finalmente chegamos aos inteiros.
Eles têm mais partes móveis—[muitos tamanhos, signed ou unsigned, e mais](/ref/spec#Numeric_types)—mas
eles seguem as mesmas regras.
Pela última vez, aqui está nosso exemplo familiar, usando apenas `int` desta vez:

{{play "constants/int1.go" `/START/` `/STOP/`}}

O mesmo exemplo poderia ser construído para qualquer um dos tipos inteiros, que são:

	int int8 int16 int32 int64
	uint uint8 uint16 uint32 uint64
	uintptr

(mais os aliases `byte` para `uint8` e `rune` para `int32`).
Isso é muito, mas o padrão na forma como as constantes funcionam deve ser familiar
o suficiente agora para que você possa ver como as coisas se desenrolarão.

Como mencionado acima, inteiros vêm em algumas formas e cada forma tem
seu próprio tipo padrão:
`int` para constantes simples como `123` ou `0xFF` ou `-14`
e `rune` para caracteres entre aspas como 'a', '世' ou '\r'.

Nenhuma forma de constante tem como seu tipo padrão um tipo inteiro unsigned.
No entanto, a flexibilidade das constantes sem tipo significa que podemos inicializar variáveis
inteiras unsigned usando constantes simples, desde que sejamos claros sobre o tipo.
É análogo a como podemos inicializar um `float64` usando um número complexo com parte imaginária zero.
Aqui estão várias maneiras diferentes de inicializar um `uint`;
todas são equivalentes, mas todas devem mencionar o tipo explicitamente para que o resultado seja unsigned.

	var u uint = 17
	var u = uint(17)
	u := uint(17)

De forma semelhante ao problema de faixa mencionado na seção sobre valores de ponto flutuante,
nem todos os valores inteiros cabem em todos os tipos inteiros.
Existem dois problemas que podem surgir: o valor pode ser muito grande,
ou pode ser um valor negativo sendo atribuído a um tipo inteiro unsigned.
Por exemplo, `int8` tem faixa -128 até 127,
então constantes fora dessa faixa nunca podem ser atribuídas a uma variável do tipo `int8`:

{{play "constants/int2.go" `/var/`}}

Similarmente, `uint8`, também conhecido como `byte`,
tem faixa 0 até 255, então uma constante grande ou negativa não pode ser atribuída a um `uint8`:

{{play "constants/int3.go" `/var/`}}

Essa verificação de tipo pode detectar erros como este:

{{play "constants/int4.go" `/START/` `/STOP/`}}

Se o compilador reclamar sobre seu uso de uma constante, é provável que seja um bug real como este.

## Um exercício: O maior unsigned int

Aqui está um exercício informativo.
Como expressamos uma constante representando o maior valor que cabe em um `uint`?
Se estivéssemos falando sobre `uint32` em vez de `uint`, poderíamos escrever

{{raw `
	const MaxUint32 = 1<<32 - 1
`}}

mas queremos `uint`, não `uint32`.
Os tipos `int` e `uint` têm números iguais não especificados de bits, 32 ou 64.
Como o número de bits disponíveis depende da arquitetura, não podemos simplesmente escrever um único valor.

Fãs de [aritmética de complemento de dois](http://en.wikipedia.org/wiki/Two's_complement),
que os inteiros do Go são definidos para usar, sabem que a representação de `-1` tem todos os seus bits definidos como 1,
então o padrão de bits de `-1` é internamente o mesmo que o do
maior inteiro unsigned.
Portanto, poderíamos pensar que poderíamos escrever

{{play "constants/exercise1.go" `/const/`}}

mas isso é ilegal porque -1 não pode ser representado por uma variável unsigned;
`-1` não está na faixa de valores unsigned.
Uma conversão também não ajudará, pela mesma razão:

{{play "constants/exercise2.go" `/const/`}}

Mesmo que em tempo de execução um valor de -1 possa ser convertido para um inteiro unsigned, as regras
para [conversões](/ref/spec#Conversions) de constantes proíbem esse tipo de coerção em tempo de compilação.
Ou seja, isto funciona:

{{play "constants/exercise3.go" `/START/` `/STOP/`}}

mas apenas porque `v` é uma variável; se fizéssemos `v` uma constante,
mesmo uma constante sem tipo, estaríamos de volta ao território proibido:

{{play "constants/exercise4.go" `/START/` `/STOP/`}}

Voltamos à nossa abordagem anterior, mas em vez de `-1` tentamos `^0`,
a negação bit a bit de um número arbitrário de bits zero.
Mas isso também falha, por uma razão similar:
No espaço de valores numéricos,
`^0` representa um número infinito de uns, então perdemos informação se atribuirmos isso a qualquer inteiro de tamanho fixo:

{{play "constants/exercise5.go" `/const/`}}

Como então representamos o maior inteiro unsigned como uma constante?

A chave é restringir a operação ao número de bits em um `uint` e evitar
valores, como números negativos, que não são representáveis em um `uint`.
O valor `uint` mais simples é a constante com tipo `uint(0)`.
Se `uints` têm 32 ou 64 bits, `uint(0)` tem 32 ou 64 bits zero correspondentemente.
Se invertermos cada um desses bits, obteremos o número correto de bits um, que é o maior valor `uint`.

Portanto, não invertemos os bits da constante sem tipo `0`, invertemos os bits da constante com tipo `uint(0)`.
Aqui, então, está nossa constante:

{{play "constants/exercise6.go" `/START/` `/STOP/`}}

Qualquer que seja o número de bits necessários para representar um `uint` no ambiente de execução atual
(no [playground](/blog/playground), são 32),
esta constante representa corretamente o maior valor que uma variável do tipo `uint` pode conter.

Se você entende a análise que nos levou a este resultado,
você entende todos os pontos importantes sobre constantes em Go.

## Números

O conceito de constantes sem tipo em Go significa que todas as constantes numéricas,
sejam inteiras, de ponto flutuante, complexas,
ou mesmo valores de caractere,
vivem em uma espécie de espaço unificado.
É quando as trazemos para o mundo computacional de variáveis,
atribuições e operações que os tipos reais importam.
Mas enquanto permanecermos no mundo das constantes numéricas, podemos misturar e combinar valores como quisermos.
Todas essas constantes têm valor numérico 1:

	1
	1.000
	1e3-99.0*10-9
	'\x01'
	'\u0001'
	'b' - 'a'
	1.0+3i-3.0i

Portanto, embora tenham diferentes tipos padrão implícitos,
escritas como constantes sem tipo elas podem ser atribuídas a uma variável de qualquer tipo numérico:

{{play "constants/numbers1.go" `/START/` `/STOP/`}}

A saída deste trecho é: `1 1 1 1 1 (1+0i) 1`.

Você pode até fazer coisas malucas como

{{play "constants/numbers2.go" `/START/` `/STOP/`}}

que produz 145.5, o que é inútil exceto para provar um ponto.

Mas o ponto real dessas regras é flexibilidade.
Essa flexibilidade significa que, apesar do fato de que em Go é ilegal
na mesma expressão misturar variáveis de ponto flutuante e inteiras,
ou mesmo variáveis `int` e `int32`, é bom escrever

	sqrt2 := math.Sqrt(2)

ou

	const millisecond = time.Second/1e3

ou

	bigBufferWithHeader := make([]byte, 512+1e6)

e ter os resultados significando o que você espera.

Porque em Go, constantes numéricas funcionam como você espera: como números.

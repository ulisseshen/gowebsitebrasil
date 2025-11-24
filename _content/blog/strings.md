---
ia-translated: true
title: Strings, bytes, runes e caracteres em Go
date: 2013-10-23
by:
- Rob Pike
tags:
- strings
- bytes
- runes
- characters
summary: Como strings funcionam em Go e como usá-las.
---

## Introdução

O [post anterior do blog](/blog/slices) explicou como slices
funcionam em Go, usando vários exemplos para ilustrar o mecanismo por trás
de sua implementação.
Com base nesse contexto, este post discute strings em Go.
À primeira vista, strings podem parecer um tópico muito simples para um post de blog, mas para usá-las
bem é necessário entender não apenas como elas funcionam,
mas também a diferença entre um byte, um caractere e uma rune,
a diferença entre Unicode e UTF-8,
a diferença entre uma string e um string literal,
e outras distinções ainda mais sutis.

Uma forma de abordar este tópico é pensar nele como uma resposta à pergunta
frequente: "Quando eu acesso uma string Go na posição _n_, por que não obtenho o
_n-ésimo_ caractere?"
Como você verá, esta pergunta nos leva a muitos detalhes sobre como o texto funciona
no mundo moderno.

Uma excelente introdução a alguns desses assuntos, independente de Go,
é o famoso post de blog de Joel Spolsky,
[The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](http://www.joelonsoftware.com/articles/Unicode.html).
Muitos dos pontos que ele levanta serão ecoados aqui.

## O que é uma string?

Vamos começar com alguns conceitos básicos.

Em Go, uma string é, na prática, um slice de bytes somente leitura.
Se você tem alguma dúvida sobre o que é um slice de bytes ou como funciona,
por favor leia o [post anterior do blog](/blog/slices);
vamos assumir aqui que você já leu.

É importante afirmar desde o início que uma string contém bytes _arbitrários_.
Não é necessário conter texto Unicode, texto UTF-8 ou qualquer outro formato predefinido.
No que diz respeito ao conteúdo de uma string, ela é exatamente equivalente a um
slice de bytes.

Aqui está um string literal (falaremos mais sobre isso em breve) que usa a
notação `\xNN` para definir uma constante string contendo alguns valores de byte peculiares.
(É claro, bytes variam de valores hexadecimais 00 até FF, inclusive.)

{{code "strings/basic.go" `/const sample/`}}

## Imprimindo strings

Como alguns dos bytes em nossa string de amostra não são ASCII válido, nem mesmo
UTF-8 válido, imprimir a string diretamente produzirá uma saída feia.
O simples comando print

{{code "strings/basic.go" `/println/` `/println/`}}

produz esta bagunça (cuja aparência exata varia com o ambiente):

	��=� ⌘

Para descobrir o que essa string realmente contém, precisamos desmontá-la e examinar as peças.
Existem várias formas de fazer isso.
A mais óbvia é percorrer seu conteúdo e extrair os bytes
individualmente, como neste loop `for`:

{{code "strings/basic.go" `/byte loop/` `/byte loop/`}}

Como mencionado anteriormente, indexar uma string acessa bytes individuais, não
caracteres. Retornaremos a esse tópico em detalhes abaixo. Por enquanto, vamos
focar apenas nos bytes.
Esta é a saída do loop byte por byte:

	bd b2 3d bc 20 e2 8c 98

Observe como os bytes individuais correspondem aos
escapes hexadecimais que definiram a string.

Uma forma mais curta de gerar uma saída apresentável para uma string confusa
é usar o verbo de formato `%x` (hexadecimal) do `fmt.Printf`.
Ele simplesmente despeja os bytes sequenciais da string como dígitos
hexadecimais, dois por byte.

{{code "strings/basic.go" `/percent x/` `/percent x/`}}

Compare sua saída com a acima:

	bdb23dbc20e28c98

Um truque legal é usar a flag "space" nesse formato, colocando um
espaço entre o `%` e o `x`. Compare a string de formato
usada aqui com a acima,

{{code "strings/basic.go" `/percent space x/` `/percent space x/`}}

e observe como os bytes saem
com espaços entre eles, tornando o resultado um pouco menos intimidador:

	bd b2 3d bc 20 e2 8c 98

Há mais. O verbo `%q` (quoted) escapará quaisquer sequências de
bytes não imprimíveis em uma string para que a saída seja inequívoca.

{{code "strings/basic.go" `/percent q/` `/percent q/`}}

Esta técnica é útil quando grande parte da string é
inteligível como texto, mas há peculiaridades a serem descobertas; ela produz:

	"\xbd\xb2=\xbc ⌘"

Se observarmos atentamente, podemos ver que enterrado no ruído há um sinal de igual ASCII,
junto com um espaço regular, e no final aparece o bem conhecido símbolo sueco "Place of Interest"
(Ponto de Interesse).
Esse símbolo tem o valor Unicode U+2318, codificado como UTF-8 pelos bytes
após o espaço (valor hex `20`): `e2` `8c` `98`.

Se não estivermos familiarizados ou confusos com valores estranhos na string,
podemos usar a flag "plus" com o verbo `%q`. Esta flag faz com que a saída escape
não apenas sequências não imprimíveis, mas também quaisquer bytes não-ASCII, tudo
enquanto interpreta UTF-8.
O resultado é que ela expõe os valores Unicode de UTF-8 formatado corretamente
que representa dados não-ASCII na string:

{{code "strings/basic.go" `/percent plus q/` `/percent plus q/`}}

Com esse formato, o valor Unicode do símbolo sueco aparece como um
escape `\u`:

	"\xbd\xb2=\xbc \u2318"

Essas técnicas de impressão são boas para conhecer ao fazer debug
do conteúdo de strings e serão úteis na discussão a seguir.
Vale a pena destacar também que todos esses métodos se comportam exatamente da
mesma forma para slices de bytes como fazem para strings.

Aqui está o conjunto completo de opções de impressão que listamos, apresentado como
um programa completo que você pode executar (e editar) direto no navegador:

{{play "strings/basic.go" `/package/` `/^}/`}}

[Exercício: Modifique os exemplos acima para usar um slice de bytes
em vez de uma string. Dica: Use uma conversão para criar o slice.]

[Exercício: Percorra a string usando o formato `%q` em cada byte.
O que a saída te diz?]

## UTF-8 e string literals

Como vimos, indexar uma string produz seus bytes, não seus caracteres: uma string é apenas um
monte de bytes.
Isso significa que quando armazenamos um valor de caractere em uma string,
armazenamos sua representação byte por byte.
Vamos ver um exemplo mais controlado para entender como isso acontece.

Aqui está um programa simples que imprime uma constante string com um único caractere
de três formas diferentes: uma vez como uma string simples, uma vez como uma string
quoted somente ASCII, e uma vez como bytes individuais em hexadecimal.
Para evitar qualquer confusão, criamos uma "raw string", delimitada por crases,
para que possa conter apenas texto literal. (Strings regulares, delimitadas por aspas
duplas, podem conter sequências de escape como mostramos acima.)

{{play "strings/utf8.go" `/^func/` `/^}/`}}

A saída é:

	plain string: ⌘
	quoted string: "\u2318"
	hex bytes: e2 8c 98

o que nos lembra que o valor de caractere Unicode U+2318, o símbolo "Place
of Interest" ⌘, é representado pelos bytes `e2` `8c` `98`, e
que esses bytes são a codificação UTF-8 do valor
hexadecimal 2318.

Pode ser óbvio ou pode ser sutil, dependendo da sua familiaridade com
UTF-8, mas vale a pena dedicar um momento para explicar como a representação UTF-8
da string foi criada.
O fato simples é: ela foi criada quando o código-fonte foi escrito.

O código-fonte em Go é _definido_ como texto UTF-8; nenhuma outra representação é
permitida. Isso implica que quando, no código-fonte, escrevemos o texto

	`⌘`

o editor de texto usado para criar o programa coloca a codificação UTF-8
do símbolo ⌘ no texto fonte.
Quando imprimimos os bytes hexadecimais, estamos apenas despejando os
dados que o editor colocou no arquivo.

Em resumo, o código-fonte Go é UTF-8, então
_o código-fonte para o string literal é texto UTF-8_.
Se esse string literal não contém sequências de escape, o que uma raw
string não pode conter, a string construída conterá exatamente o
texto fonte entre as aspas.
Assim, por definição e
por construção, a raw string sempre conterá uma representação UTF-8
válida de seu conteúdo.
Da mesma forma, a menos que contenha escapes que quebrem UTF-8 como os
da seção anterior, um string literal regular também sempre
conterá UTF-8 válido.

Algumas pessoas pensam que strings Go são sempre UTF-8, mas elas
não são: apenas string literals são UTF-8.
Como mostramos na seção anterior, _valores_ de string podem conter bytes arbitrários;
como mostramos nesta, string _literals_ sempre contêm texto UTF-8
desde que não tenham escapes de nível de byte.

Para resumir, strings podem conter bytes arbitrários, mas quando construídas
a partir de string literals, esses bytes são (quase sempre) UTF-8.

## Code points, caracteres e runes

Temos sido muito cuidadosos até agora em como usamos as palavras "byte" e "caractere".
Isso é em parte porque strings contêm bytes, e em parte porque a ideia de "caractere"
é um pouco difícil de definir.
O padrão Unicode usa o termo "code point" para se referir ao item representado
por um único valor.
O code point U+2318, com valor hexadecimal 2318, representa o símbolo ⌘.
(Para muito mais informações sobre esse code point, veja
[sua página Unicode](http://unicode.org/cldr/utility/character.jsp?a=2318).)

Para escolher um exemplo mais prosaico, o code point Unicode U+0061 é a letra
latina minúscula 'A': a.

Mas e quanto à letra minúscula 'A' com acento grave, à?
Isso é um caractere, e também é um code point (U+00E0), mas tem outras
representações.
Por exemplo, podemos usar o code point de acento grave "combining" (combinável), U+0300,
e anexá-lo à letra minúscula a, U+0061, para criar o mesmo caractere à.
Em geral, um caractere pode ser representado por várias
sequências diferentes de code points, e portanto diferentes sequências de bytes UTF-8.

O conceito de caractere em computação é, portanto, ambíguo, ou pelo menos
confuso, então o usamos com cuidado.
Para tornar as coisas confiáveis, existem técnicas de _normalização_ que garantem que
um determinado caractere sempre seja representado pelos mesmos code points, mas esse
assunto nos leva muito longe do tópico por enquanto.
Um post de blog posterior explicará como as bibliotecas Go abordam a normalização.

"Code point" é um bocado, então Go introduz um termo mais curto para o
conceito: _rune_.
O termo aparece nas bibliotecas e código-fonte, e significa exatamente
o mesmo que "code point", com uma adição interessante.

A linguagem Go define a palavra `rune` como um alias para o tipo `int32`, então
programas podem ser claros quando um valor inteiro representa um code point.
Além disso, o que você pode pensar como uma constante de caractere é chamado de
_constante rune_ em Go.
O tipo e valor da expressão

	'⌘'

é `rune` com valor inteiro `0x2318`.

Para resumir, aqui estão os pontos salientes:

  - O código-fonte Go é sempre UTF-8.
  - Uma string contém bytes arbitrários.
  - Um string literal, na ausência de escapes de nível de byte, sempre contém sequências UTF-8 válidas.
  - Essas sequências representam code points Unicode, chamados runes.
  - Não há garantia em Go de que caracteres em strings sejam normalizados.

## Loops Range

Além do detalhe axiomático de que o código-fonte Go é UTF-8,
há realmente apenas uma forma em que Go trata UTF-8 de maneira especial, e isso é ao usar
um loop `for` `range` em uma string.

Vimos o que acontece com um loop `for` regular.
Um loop `for` `range`, em contraste, decodifica uma rune codificada em UTF-8 em cada
iteração.
A cada volta do loop, o índice do loop é a posição inicial da
rune atual, medida em bytes, e o code point é seu valor.
Aqui está um exemplo usando outro formato útil do `Printf`, `%#U`, que mostra
o valor Unicode do code point e sua representação impressa:

{{play "strings/range.go" `/const/` `/}/`}}

A saída mostra como cada code point ocupa múltiplos bytes:

	U+65E5 '日' starts at byte position 0
	U+672C '本' starts at byte position 3
	U+8A9E '語' starts at byte position 6

[Exercício: Coloque uma sequência de bytes UTF-8 inválida na string. (Como?)
O que acontece com as iterações do loop?]

## Bibliotecas

A biblioteca padrão do Go fornece suporte robusto para interpretar texto UTF-8.
Se um loop `for` `range` não for suficiente para seus propósitos,
é provável que a funcionalidade que você precisa seja fornecida por um pacote na biblioteca.

O pacote mais importante é
[`unicode/utf8`](/pkg/unicode/utf8/),
que contém
rotinas auxiliares para validar, desmontar e remontar strings UTF-8.
Aqui está um programa equivalente ao exemplo `for` `range` acima,
mas usando a função `DecodeRuneInString` desse pacote para
fazer o trabalho.
Os valores de retorno da função são a rune e sua largura em
bytes codificados em UTF-8.

{{play "strings/encoding.go" `/const/` `/}/`}}

Execute-o para ver que ele executa da mesma forma.
O loop `for` `range` e `DecodeRuneInString` são definidos para produzir
exatamente a mesma sequência de iteração.

Veja a
[documentação](/pkg/unicode/utf8/)
do pacote `unicode/utf8` para conhecer quais
outras funcionalidades ele oferece.

## Conclusão

Para responder à pergunta colocada no início: Strings são construídas a partir de bytes,
então indexá-las produz bytes, não caracteres.
Uma string pode nem mesmo conter caracteres.
Na verdade, a definição de "caractere" é ambígua e seria
um erro tentar resolver a ambiguidade definindo que strings são feitas
de caracteres.

Há muito mais a dizer sobre Unicode, UTF-8 e o mundo do processamento de
texto multilíngue, mas isso pode esperar por outro post.
Por enquanto, esperamos que você tenha uma melhor compreensão de como strings Go se comportam
e que, embora possam conter bytes arbitrários, UTF-8 é uma parte central
de seu design.

---
ia-translated: true
title: Sintaxe de Declaração em Go
date: 2010-07-07
by:
- Rob Pike
tags:
- c
- syntax
- ethos
summary: Por que a sintaxe de declaração do Go não se parece, e é muito mais simples, que a do C.
---

## Introdução

Recém-chegados ao Go se perguntam por que a sintaxe de declaração é diferente da
tradição estabelecida na família C.
Neste post vamos comparar as duas abordagens e explicar por que as declarações do Go parecem como são.

## Sintaxe C

Primeiro, vamos falar sobre a sintaxe C. C adotou uma abordagem incomum e inteligente
para a sintaxe de declaração.
Em vez de descrever os tipos com uma sintaxe especial,
escreve-se uma expressão envolvendo o item sendo declarado,
e declara-se que tipo essa expressão terá. Assim

	int x;

declara x como um int: a expressão 'x' terá tipo int.
Em geral, para descobrir como escrever o tipo de uma nova variável,
escreva uma expressão envolvendo aquela variável que avalia para um tipo básico,
então coloque o tipo básico à esquerda e a expressão à direita.

Assim, as declarações

	int *p;
	int a[3];

declaram que p é um pointer para int porque '\*p' tem tipo int,
e que a é um array de ints porque a[3] (ignorando o valor do índice particular,
que é usado como trocadilho para ser o tamanho do array) tem tipo int.

E quanto a funções? Originalmente, as declarações de função do C escreviam os tipos
dos argumentos fora dos parênteses, assim:

	int main(argc, argv)
	    int argc;
	    char *argv[];
	{ /* ... */ }

Novamente, vemos que main é uma função porque a expressão main(argc,
argv) retorna um int.
Na notação moderna escreveríamos

	int main(int argc, char *argv[]) { /* ... */ }

mas a estrutura básica é a mesma.

Esta é uma ideia sintática inteligente que funciona bem para tipos simples mas pode ficar confusa rapidamente.
O exemplo famoso é declarar um pointer de função.
Siga as regras e você obtém isto:

	int (*fp)(int a, int b);

Aqui, fp é um pointer para uma função porque se você escrever a expressão (\*fp)(a,
b) você chamará uma função que retorna int.
E se um dos argumentos de fp for ele mesmo uma função?

	int (*fp)(int (*ff)(int x, int y), int b)

Isso está começando a ficar difícil de ler.

Claro, podemos omitir o nome dos parâmetros quando declaramos uma função, então main pode ser declarada

	int main(int, char *[])

Lembre-se que argv é declarado assim,

	char *argv[]

então você remove o nome do meio de sua declaração para construir seu tipo.
Não é óbvio, porém, que você declara algo do tipo char \*[] colocando
seu nome no meio.

E veja o que acontece com a declaração de fp se você não nomear os parâmetros:

	int (*fp)(int (*)(int, int), int)

Não só não é óbvio onde colocar o nome dentro de

	int (*)(int, int)

não está exatamente claro que é uma declaração de pointer de função.
E se o tipo de retorno for um pointer de função?

	int (*(*fp)(int (*)(int, int), int))(int, int)

É difícil até ver que esta declaração é sobre fp.

Você pode construir exemplos mais elaborados mas estes devem ilustrar algumas
das dificuldades que a sintaxe de declaração do C pode introduzir.

Há mais um ponto que precisa ser mencionado, porém.
Porque a sintaxe de tipo e declaração são as mesmas,
pode ser difícil analisar expressões com tipos no meio.
É por isso, por exemplo, que casts em C sempre colocam o tipo entre parênteses, como em

	(int)M_PI

## Sintaxe Go

Linguagens fora da família C geralmente usam uma sintaxe de tipo distinta em declarações.
Embora seja um ponto separado, o nome geralmente vem primeiro,
frequentemente seguido por dois pontos.
Assim nossos exemplos acima se tornam algo como (em uma linguagem fictícia mas ilustrativa)

	x: int
	p: pointer to int
	a: array[3] of int

Essas declarações são claras, embora verbosas - você apenas as lê da esquerda para a direita.
Go se inspira nisso, mas no interesse da brevidade remove os
dois pontos e elimina algumas palavras-chave:

	x int
	p *int
	a [3]int

Não há correspondência direta entre a aparência de [3]int e como usar
a em uma expressão.
(Voltaremos aos pointers na próxima seção.) Você ganha clareza ao custo
de uma sintaxe separada.

Agora considere funções. Vamos transcrever a declaração de main como seria lida em Go,
embora a função main real em Go não aceite argumentos:

	func main(argc int, argv []string) int

Superficialmente isso não é muito diferente de C,
além da mudança de arrays de `char` para strings,
mas se lê bem da esquerda para a direita:

função main recebe um int e um slice de strings e retorna um int.

Remova os nomes dos parâmetros e fica igualmente claro - eles sempre vêm primeiro então não há confusão.

	func main(int, []string) int

Um mérito deste estilo da esquerda para a direita é como ele funciona bem conforme os tipos
se tornam mais complexos.
Aqui está uma declaração de uma variável de função (análoga a um pointer de função em C):

	f func(func(int,int) int, int) int

Ou se f retorna uma função:

	f func(func(int,int) int, int) func(int, int) int

Ainda se lê claramente, da esquerda para a direita,
e é sempre óbvio qual nome está sendo declarado - o nome vem primeiro.

A distinção entre sintaxe de tipo e expressão facilita escrever e invocar closures em Go:

	sum := func(a, b int) int { return a+b } (3, 4)

## Pointers

Pointers são a exceção que confirma a regra.
Note que em arrays e slices, por exemplo,
a sintaxe de tipo do Go coloca os colchetes à esquerda do tipo mas a sintaxe de expressão
os coloca à direita da expressão:

	var a []int
	x = a[1]

Por familiaridade, os pointers do Go usam a notação \* do C,
mas não pudemos nos convencer a fazer uma reversão similar para tipos pointer.
Assim pointers funcionam assim

	var p *int
	x = *p

Não pudemos dizer

	var p *int
	x = p*

porque esse \* pós-fixado seria confundido com multiplicação. Poderíamos ter usado o ^ do Pascal, por exemplo:

	var p ^int
	x = p^

e talvez devêssemos ter feito isso (e escolhido outro operador para xor),
porque o asterisco prefixado tanto em tipos quanto em expressões complica as coisas
de várias maneiras.
Por exemplo, embora seja possível escrever

	[]int("hi")

como uma conversão, é necessário colocar o tipo entre parênteses se ele começar com um \*:

	(*int)(nil)

Se tivéssemos aceitado abandonar \* como sintaxe de pointer, esses parênteses seriam desnecessários.

Então a sintaxe de pointer do Go está amarrada à forma familiar do C,
mas esses laços significam que não podemos nos livrar completamente do uso de parênteses
para desambiguar tipos e expressões na gramática.

No geral, porém, acreditamos que a sintaxe de tipo do Go é mais fácil de entender que a do C, especialmente quando as coisas ficam complicadas.

## Notas

As declarações do Go se leem da esquerda para a direita. Foi apontado que as do C se leem em espiral!
Veja [ The "Clockwise/Spiral Rule"](http://c-faq.com/decl/spiral.anderson.html) por David Anderson.

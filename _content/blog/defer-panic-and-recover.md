---
ia-translated: true
title: Defer, Panic e Recover
date: 2010-08-04
by:
- Andrew Gerrand
tags:
- defer
- panic
- recover
- technical
- function
summary: Uma introdução aos mecanismos de controle de fluxo defer, panic e recover do Go.
---


Go possui os mecanismos usuais para controle de fluxo:
if, for, switch, goto.
Ele também tem a declaração go para executar código em uma goroutine separada.
Aqui eu gostaria de discutir alguns dos mecanismos menos comuns:
defer, panic e recover.

Uma **declaração defer** coloca uma chamada de função em uma lista.
A lista de chamadas salvas é executada após o retorno da função circundante.
Defer é comumente usado para simplificar funções que realizam várias ações de limpeza.

Por exemplo, vamos olhar uma função que abre dois arquivos e copia o conteúdo de um arquivo para o outro:

	func CopyFile(dstName, srcName string) (written int64, err error) {
	    src, err := os.Open(srcName)
	    if err != nil {
	        return
	    }

	    dst, err := os.Create(dstName)
	    if err != nil {
	        return
	    }

	    written, err = io.Copy(dst, src)
	    dst.Close()
	    src.Close()
	    return
	}

Isso funciona, mas há um bug. Se a chamada para os.Create falhar,
a função retornará sem fechar o arquivo de origem.
Isso pode ser facilmente corrigido colocando uma chamada para src.Close antes da segunda declaração return,
mas se a função fosse mais complexa o problema poderia não ser tão facilmente
percebido e resolvido.
Ao introduzir declarações defer, podemos garantir que os arquivos sejam sempre fechados:

	func CopyFile(dstName, srcName string) (written int64, err error) {
	    src, err := os.Open(srcName)
	    if err != nil {
	        return
	    }
	    defer src.Close()

	    dst, err := os.Create(dstName)
	    if err != nil {
	        return
	    }
	    defer dst.Close()

	    return io.Copy(dst, src)
	}

Declarações defer nos permitem pensar sobre fechar cada arquivo logo após abri-lo,
garantindo que, independentemente do número de declarações return na função,
os arquivos _serão_ fechados.

O comportamento de declarações defer é direto e previsível. Existem três regras simples:

1. _Os argumentos de uma função diferida são avaliados quando a declaração defer é avaliada._

Neste exemplo, a expressão "i" é avaliada quando a chamada Println é diferida.
A chamada diferida imprimirá "0" após o retorno da função.

	func a() {
	    i := 0
	    defer fmt.Println(i)
	    i++
	    return
	}

2. _Chamadas de função diferidas são executadas em ordem Last In First Out após o retorno da função circundante._

Esta função imprime "3210":

{{raw `
	func b() {
	    for i := 0; i < 4; i++ {
	        defer fmt.Print(i)
	    }
	}
`}}

3. _Funções diferidas podem ler e atribuir aos valores de retorno nomeados da função que está retornando._

Neste exemplo, uma função diferida incrementa o valor de retorno i _após_
o retorno da função circundante.
Assim, esta função retorna 2:

	func c() (i int) {
	    defer func() { i++ }()
	    return 1
	}

Isso é conveniente para modificar o valor de retorno de erro de uma função; veremos um exemplo disso em breve.

**Panic** é uma função embutida que para o fluxo ordinário de controle e começa a _entrar em pânico_.
Quando a função F chama panic, a execução de F para,
quaisquer funções diferidas em F são executadas normalmente,
e então F retorna ao seu chamador.
Para o chamador, F então se comporta como uma chamada para panic.
O processo continua subindo a pilha até que todas as funções na goroutine atual tenham retornado,
momento em que o programa trava.
Panics podem ser iniciados invocando panic diretamente.
Eles também podem ser causados por erros de tempo de execução,
como acessos a arrays fora dos limites.

**Recover** é uma função embutida que recupera o controle de uma goroutine em pânico.
Recover só é útil dentro de funções diferidas.
Durante a execução normal, uma chamada para recover retornará nil e não terá nenhum outro efeito.
Se a goroutine atual estiver em pânico, uma chamada para recover capturará o
valor fornecido para panic e retomará a execução normal.

Aqui está um programa de exemplo que demonstra os mecanismos de panic e defer:

	package main

	import "fmt"

	func main() {
	    f()
	    fmt.Println("Returned normally from f.")
	}

	func f() {
	    defer func() {
	        if r := recover(); r != nil {
	            fmt.Println("Recovered in f", r)
	        }
	    }()
	    fmt.Println("Calling g.")
	    g(0)
	    fmt.Println("Returned normally from g.")
	}

	func g(i int) {
	    if i > 3 {
	        fmt.Println("Panicking!")
	        panic(fmt.Sprintf("%v", i))
	    }
	    defer fmt.Println("Defer in g", i)
	    fmt.Println("Printing in g", i)
	    g(i + 1)
	}

A função g recebe o int i, e entra em panic se i for maior que 3,
ou então ela chama a si mesma com o argumento i+1.
A função f difere uma função que chama recover e imprime o valor
recuperado (se ele não for nil).
Tente imaginar qual seria a saída deste programa antes de continuar lendo.

O programa produzirá:

	Calling g.
	Printing in g 0
	Printing in g 1
	Printing in g 2
	Printing in g 3
	Panicking!
	Defer in g 3
	Defer in g 2
	Defer in g 1
	Defer in g 0
	Recovered in f 4
	Returned normally from f.

Se removermos a função diferida de f, o panic não é recuperado e
atinge o topo da pilha de chamadas da goroutine,
terminando o programa.
Este programa modificado produzirá:

	Calling g.
	Printing in g 0
	Printing in g 1
	Printing in g 2
	Printing in g 3
	Panicking!
	Defer in g 3
	Defer in g 2
	Defer in g 1
	Defer in g 0
	panic: 4

	panic PC=0x2a9cd8
	[stack trace omitted]

Para um exemplo do mundo real de **panic** e **recover**,
veja o [pacote json](/pkg/encoding/json/) da
biblioteca padrão do Go.
Ele codifica uma interface com um conjunto de funções recursivas.
Se um erro ocorrer ao percorrer o valor,
panic é chamado para desenrolar a pilha até a chamada de função de nível superior,
que recupera do panic e retorna um valor de erro apropriado (veja
os métodos 'error' e 'marshal' do tipo encodeState em [encode.go](/src/pkg/encoding/json/encode.go)).

A convenção nas bibliotecas Go é que mesmo quando um pacote usa panic internamente,
sua API externa ainda apresenta valores de retorno de erro explícitos.

Outros usos de **defer** (além do exemplo file.Close dado anteriormente) incluem liberar um mutex:

	mu.Lock()
	defer mu.Unlock()

imprimir um rodapé:

	printHeader()
	defer printFooter()

e mais.

Em resumo, a declaração defer (com ou sem panic e recover) fornece
um mecanismo incomum e poderoso para controle de fluxo.
Ela pode ser usada para modelar uma série de recursos implementados por estruturas
de propósito especial em outras linguagens de programação. Experimente.

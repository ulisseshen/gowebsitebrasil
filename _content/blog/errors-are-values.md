---
ia-translated: true
title: Errors são valores
date: 2015-01-12
by:
- Rob Pike
summary: Idiomas e padrões para tratamento de errors em Go.
---


Um ponto comum de discussão entre programadores Go,
especialmente aqueles novos na linguagem, é como tratar errors.
A conversa frequentemente se transforma em uma lamentação sobre o número de vezes que a sequência

	if err != nil {
		return err
	}

aparece.
Recentemente escaneamos todos os projetos open source que pudemos encontrar e
descobrimos que este trecho ocorre apenas uma vez a cada página ou duas,
com menos frequência do que alguns gostariam que você acreditasse.
Ainda assim, se a percepção persiste de que é preciso digitar

	if err != nil

o tempo todo, algo deve estar errado, e o alvo óbvio é o próprio Go.

Isso é infeliz, enganoso e facilmente corrigido.
Talvez o que esteja acontecendo é que programadores novos em Go perguntam,
"Como se tratam errors?", aprendem este padrão e param por aí.
Em outras linguagens, pode-se usar um bloco try-catch ou outro mecanismo similar para tratar errors.
Portanto, o programador pensa, quando eu teria usado um try-catch
na minha antiga linguagem, vou apenas digitar `if` `err` `!=` `nil` em Go.
Com o tempo o código Go acumula muitos desses trechos, e o resultado parece desajeitado.

Independentemente de esta explicação se encaixar,
está claro que esses programadores Go perdem um ponto fundamental sobre errors:
_Errors são valores._

Valores podem ser programados, e como errors são valores, errors podem ser programados.

É claro que uma instrução comum envolvendo um valor de error é testar se ele é nil,
mas há inúmeras outras coisas que se pode fazer com um valor de error,
e a aplicação de algumas dessas outras coisas pode tornar seu programa melhor,
eliminando muito do código repetitivo que surge se cada error é verificado com uma instrução if mecânica.

Aqui está um exemplo simples do tipo
[`Scanner`](/pkg/bufio/#Scanner) do pacote `bufio`.
Seu método [`Scan`](/pkg/bufio/#Scanner.Scan) realiza a E/S subjacente,
que pode, é claro, levar a um error.
No entanto, o método `Scan` não expõe um error de forma alguma.
Em vez disso, ele retorna um booleano, e um método separado, para ser executado no final da varredura,
informa se ocorreu um error.
O código cliente se parece com isto:

	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		token := scanner.Text()
		// process token
	}
	if err := scanner.Err(); err != nil {
		// process the error
	}

Claro, há uma verificação nil para um error, mas ela aparece e executa apenas uma vez.
O método `Scan` poderia em vez disso ter sido definido como

	func (s *Scanner) Scan() (token []byte, error)

e então o código de usuário exemplo poderia ser (dependendo de como o token é recuperado),

	scanner := bufio.NewScanner(input)
	for {
		token, err := scanner.Scan()
		if err != nil {
			return err // or maybe break
		}
		// process token
	}

Isso não é muito diferente, mas há uma distinção importante.
Neste código, o cliente deve verificar por um error em cada iteração,
mas na API `Scanner` real, o tratamento de error é abstraído do elemento chave da API,
que é iterar sobre tokens.
Com a API real, o código do cliente portanto parece mais natural:
loop até terminar, então se preocupe com errors.
O tratamento de error não obscurece o fluxo de controle.

Por baixo dos panos o que está acontecendo, é claro,
é que assim que `Scan` encontra um error de E/S, ele o registra e retorna `false`.
Um método separado, [`Err`](/pkg/bufio/#Scanner.Err),
relata o valor do error quando o cliente pede.
Por mais trivial que isso seja, não é o mesmo que colocar

	if err != nil

em todos os lugares ou pedir ao cliente para verificar por um error após cada token.
É programar com valores de error.
Programação simples, sim, mas programação mesmo assim.

Vale a pena enfatizar que qualquer que seja o design,
é crítico que o programa verifique os errors independentemente de como eles são expostos.
A discussão aqui não é sobre como evitar verificar errors,
é sobre usar a linguagem para tratar errors com elegância.

O tópico de código repetitivo de verificação de error surgiu quando participei da GoCon de outono de 2014 em Tóquio.
Um gopher entusiasmado, que se identifica como [`@jxck_`](https://twitter.com/jxck_) no Twitter,
ecoou a familiar lamentação sobre verificação de error.
Ele tinha um código que parecia esquematicamente com isto:

	_, err = fd.Write(p0[a:b])
	if err != nil {
		return err
	}
	_, err = fd.Write(p1[c:d])
	if err != nil {
		return err
	}
	_, err = fd.Write(p2[e:f])
	if err != nil {
		return err
	}
	// and so on

É muito repetitivo.
No código real, que era mais longo,
há mais coisas acontecendo então não é fácil simplesmente refatorar isso usando uma função auxiliar,
mas nesta forma idealizada, um literal de função fechando sobre a variável error ajudaria:

	var err error
	write := func(buf []byte) {
		if err != nil {
			return
		}
		_, err = w.Write(buf)
	}
	write(p0[a:b])
	write(p1[c:d])
	write(p2[e:f])
	// and so on
	if err != nil {
		return err
	}

Este padrão funciona bem, mas requer um closure em cada função fazendo as escritas;
uma função auxiliar separada é mais desajeitada de usar porque a variável `err`
precisa ser mantida através das chamadas (tente).

Podemos tornar isso mais limpo, mais geral e reutilizável emprestando a ideia do
método `Scan` acima.
Mencionei esta técnica em nossa discussão mas `@jxck_` não viu como aplicá-la.
Após uma longa troca, dificultada um pouco por uma barreira de idioma,
perguntei se eu poderia apenas pegar emprestado seu laptop e mostrar a ele digitando algum código.

Defini um objeto chamado `errWriter`, algo como isto:

	type errWriter struct {
		w   io.Writer
		err error
	}

e dei a ele um método, `write.`
Ele não precisa ter a assinatura `Write` padrão,
e é minúsculo em parte para destacar a distinção.
O método `write` chama o método `Write` do `Writer` subjacente
e registra o primeiro error para referência futura:

	func (ew *errWriter) write(buf []byte) {
		if ew.err != nil {
			return
		}
		_, ew.err = ew.w.Write(buf)
	}

Assim que um error ocorre, o método `write` torna-se uma operação vazia mas o valor do error é salvo.

Dado o tipo `errWriter` e seu método `write`, o código acima pode ser refatorado:

	ew := &errWriter{w: fd}
	ew.write(p0[a:b])
	ew.write(p1[c:d])
	ew.write(p2[e:f])
	// and so on
	if ew.err != nil {
		return ew.err
	}

Isso é mais limpo, mesmo comparado ao uso de um closure,
e também torna a sequência real de escritas sendo feitas mais fácil de ver na página.
Não há mais desordem.
Programar com valores de error (e interfaces) tornou o código mais agradável.

É provável que alguma outra parte do código no mesmo pacote possa construir sobre esta ideia,
ou até mesmo usar `errWriter` diretamente.

Além disso, uma vez que `errWriter` existe, há mais que ele poderia fazer para ajudar,
especialmente em exemplos menos artificiais.
Ele poderia acumular a contagem de bytes.
Ele poderia unir escritas em um único buffer que pode então ser transmitido atomicamente.
E muito mais.

De fato, este padrão aparece frequentemente na biblioteca padrão.
Os pacotes [`archive/zip`](/pkg/archive/zip/) e
[`net/http`](/pkg/net/http/) o usam.
Mais saliente para esta discussão, o [`Writer` do pacote `bufio`](/pkg/bufio/)
é na verdade uma implementação da ideia `errWriter`.
Embora `bufio.Writer.Write` retorne um error,
isso é principalmente sobre honrar a interface [`io.Writer`](/pkg/io/#Writer).
O método `Write` de `bufio.Writer` comporta-se exatamente como nosso método `errWriter.write`
acima, com `Flush` reportando o error, então nosso exemplo poderia ser escrito assim:

	b := bufio.NewWriter(fd)
	b.Write(p0[a:b])
	b.Write(p1[c:d])
	b.Write(p2[e:f])
	// and so on
	if b.Flush() != nil {
		return b.Flush()
	}

Há uma desvantagem significativa para esta abordagem, pelo menos para algumas aplicações:
não há maneira de saber quanto do processamento foi completado antes que o error ocorresse.
Se essa informação é importante, uma abordagem mais refinada é necessária.
Frequentemente, no entanto, uma verificação tudo-ou-nada no final é suficiente.

Examinamos apenas uma técnica para evitar código repetitivo de tratamento de error.
Tenha em mente que o uso de `errWriter` ou `bufio.Writer` não é a única maneira de simplificar o tratamento de error,
e esta abordagem não é adequada para todas as situações.
A lição chave, no entanto, é que errors são valores e todo o poder da
linguagem de programação Go está disponível para processá-los.

Use a linguagem para simplificar seu tratamento de error.

Mas lembre-se: Faça o que fizer, sempre verifique seus errors!

Finalmente, para a história completa da minha interação com @jxck\_, incluindo um pequeno vídeo que ele gravou,
visite [seu blog](http://jxck.hatenablog.com/entry/golang-error-handling-lesson-by-rob-pike).

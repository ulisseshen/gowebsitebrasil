---
ia-translated: true
title: O primeiro programa Go
date: 2013-07-18
by:
- Andrew Gerrand
tags:
- history
summary: Rob Pike descobriu o primeiro programa Go já escrito.
---


Brad Fitzpatrick e eu (Andrew Gerrand) recentemente começamos a reestruturar
o [godoc](/cmd/godoc/), e me ocorreu que ele é um
dos programas Go mais antigos.
Robert Griesemer começou a escrevê-lo no início de 2009,
e ainda o estamos usando hoje.

Quando eu [tweetei](https://twitter.com/enneff/status/357403054632484865) sobre
isso, Dave Cheney respondeu com uma [pergunta interessante](https://twitter.com/davecheney/status/357406479415914497):
qual é o programa Go mais antigo? Rob Pike procurou em seu email e o encontrou
em uma antiga mensagem para Robert e Ken Thompson.

O que segue é o primeiro programa Go. Foi escrito por Rob em fevereiro de 2008,
quando a equipe era apenas Rob, Robert e Ken. Eles tinham uma lista sólida de funcionalidades
(mencionada [neste post de blog](https://commandcenter.blogspot.com.au/2012/06/less-is-exponentially-more.html))
e uma especificação de linguagem preliminar. Ken tinha acabado de finalizar a primeira versão funcional de
um compilador Go (ele não produzia código nativo, mas sim transliterava código Go
para C para prototipagem rápida) e era hora de tentar escrever um programa com ele.

Rob enviou um email para o "time Go":

	From: Rob 'Commander' Pike
	Date: Wed, Feb 6, 2008 at 3:42 PM
	To: Ken Thompson, Robert Griesemer
	Subject: slist

	it works now.

	roro=% a.out
	(defn foo (add 12 34))
	return: icounter = 4440
	roro=%

	here's the code.
	some ugly hackery to get around the lack of strings.

(A linha `icounter` na saída do programa é o número de instruções
executadas, impressas para depuração.)

{{code "first-go-program/slist.go"}}

O programa analisa e imprime uma
[S-expression](https://en.wikipedia.org/wiki/S-expression).
Ele não recebe entrada do usuário e não tem imports, dependendo apenas da
funcionalidade `print` embutida para saída.
Foi escrito literalmente no primeiro dia em que havia um
[compilador funcional mas rudimentar](/change/8b8615138da3).
Muito da linguagem não estava implementado e parte dela nem estava especificada.

Ainda assim, o sabor básico da linguagem hoje é reconhecível neste programa.
Declarações de tipo e variável, fluxo de controle e declarações de package não
mudaram muito.

Mas há muitas diferenças e ausências.
As mais significativas são a falta de concorrência e interfaces—ambas
consideradas essenciais desde o dia 1, mas ainda não projetadas.

Uma `func` era uma `function`, e sua assinatura especificava valores de retorno
_antes_ dos argumentos, separando-os com {{raw "`<-`"}}, que agora usamos como operador
de envio/recebimento de channel. Por exemplo, a função `WhiteSpace` recebe o inteiro
`c` e retorna um booleano.

{{raw `
	function WhiteSpace(bool <- c int)
`}}

Esta seta foi uma medida provisória até que uma sintaxe melhor surgisse para declarar
múltiplos valores de retorno.

Methods eram distintos de functions e tinham sua própria keyword.

{{raw `
	method (this *Slist) Car(*Slist <-) {
		return this.list.car;
	}
`}}

E methods eram pré-declarados na definição da struct, embora isso tenha mudado logo em seguida.

{{raw `
	type Slist struct {
		...
		Car method(*Slist <-);
	}
`}}

Não havia strings, embora estivessem na especificação.
Para contornar isso, Rob teve que construir a string de entrada como um array `uint8` com
uma construção desajeitada. (Arrays eram rudimentares e slices ainda não tinham sido projetados,
muito menos implementados, embora existisse o conceito não implementado de um
"open array".)

	input[i] = '('; i = i + 1;
	input[i] = 'd'; i = i + 1;
	input[i] = 'e'; i = i + 1;
	input[i] = 'f'; i = i + 1;
	input[i] = 'n'; i = i + 1;
	input[i] = ' '; i = i + 1;
	...

Tanto `panic` quanto `print` eram keywords embutidas, não funções pré-declaradas.

	print "parse error: expected ", c, "\n";
	panic "parse";

E há muitas outras pequenas diferenças; veja se você consegue identificar algumas outras.

Menos de dois anos depois que este programa foi escrito, Go foi lançado como um
projeto de código aberto. Olhando para trás, é impressionante quanto a linguagem
cresceu e amadureceu. (A última coisa a mudar entre este proto-Go e o Go
que conhecemos hoje foi a eliminação dos ponto e vírgulas.)

Mas ainda mais impressionante é quanto aprendemos sobre _escrever_ código Go.
Por exemplo, Rob chamou seus receivers de method de `this`, mas agora usamos nomes
contextuais mais curtos. Há centenas de exemplos mais significativos
e até hoje ainda estamos descobrindo maneiras melhores de escrever código Go.
(Confira o truque inteligente do [glog package](https://github.com/golang/glog) para
[lidar com níveis de verbosidade](https://github.com/golang/glog/blob/c6f9652c7179652e2fd8ed7002330db089f4c9db/glog.go#L893).)

Eu me pergunto o que aprenderemos amanhã.

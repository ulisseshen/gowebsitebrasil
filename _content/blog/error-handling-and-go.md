---
ia-translated: true
title: Error handling e Go
date: 2011-07-12
by:
- Andrew Gerrand
tags:
- error
- interface
- type
- technical
summary: Uma introdução aos errors em Go.
---

## Introdução

Se você já escreveu código Go, provavelmente encontrou o tipo `error` built-in.
O código Go usa valores `error` para indicar um estado anormal.
Por exemplo, a função `os.Open` retorna um valor `error` não-nil quando
falha ao abrir um arquivo.

	func Open(name string) (file *File, err error)

O código a seguir usa `os.Open` para abrir um arquivo.
Se ocorrer um erro, ele chama `log.Fatal` para imprimir a mensagem de erro e parar.

	f, err := os.Open("filename.ext")
	if err != nil {
	    log.Fatal(err)
	}
	// do something with the open *File f

Você pode fazer muitas coisas em Go sabendo apenas isso sobre o tipo `error`,
mas neste artigo vamos analisar mais de perto o `error` e discutir algumas
boas práticas para error handling em Go.

## O tipo error

O tipo `error` é um tipo interface. Uma variável `error` representa qualquer
valor que possa se descrever como uma string.
Aqui está a declaração da interface:

	type error interface {
	    Error() string
	}

O tipo `error`, assim como todos os tipos built-in,
é [predeclared](/doc/go_spec.html#Predeclared_identifiers)
no [universe block](/doc/go_spec.html#Blocks).

A implementação de `error` mais comumente usada é o tipo `errorString`
não-exportado do pacote [errors](/pkg/errors/).

	// errorString is a trivial implementation of error.
	type errorString struct {
	    s string
	}

	func (e *errorString) Error() string {
	    return e.s
	}

Você pode construir um desses valores com a função `errors.New`.
Ela recebe uma string que converte para um `errors.errorString` e retorna
como um valor `error`.

	// New returns an error that formats as the given text.
	func New(text string) error {
	    return &errorString{text}
	}

Aqui está como você pode usar `errors.New`:

{{raw `
	func Sqrt(f float64) (float64, error) {
	    if f < 0 {
	        return 0, errors.New("math: square root of negative number")
	    }
	    // implementation
	}
`}}

Um chamador passando um argumento negativo para `Sqrt` recebe um valor `error`
não-nil (cuja representação concreta é um valor `errors.errorString`).
O chamador pode acessar a string de erro ("math:
square root of...") chamando o método `Error` do `error`,
ou simplesmente imprimindo-o:

	f, err := Sqrt(-1)
	if err != nil {
	    fmt.Println(err)
	}

O pacote [fmt](/pkg/fmt/) formata um valor `error` chamando seu método `Error() string`.

É responsabilidade da implementação do error resumir o contexto.
O erro retornado por `os.Open` é formatado como "open /etc/passwd:
permission denied," não apenas "permission denied." O erro retornado por
nossa função `Sqrt` está faltando informação sobre o argumento inválido.

Para adicionar essa informação, uma função útil é o `Errorf` do pacote `fmt`.
Ela formata uma string de acordo com as regras do `Printf` e a retorna como um `error`
criado por `errors.New`.

{{raw `
	if f < 0 {
	    return 0, fmt.Errorf("math: square root of negative number %g", f)
	}
`}}

Em muitos casos `fmt.Errorf` é suficiente,
mas como `error` é uma interface, você pode usar estruturas de dados arbitrárias como valores de error,
para permitir que os chamadores inspecionem os detalhes do erro.

Por exemplo, nossos chamadores hipotéticos podem querer recuperar o argumento
inválido passado para `Sqrt`.
Podemos habilitar isso definindo uma nova implementação de error em vez de usar
`errors.errorString`:

	type NegativeSqrtError float64

	func (f NegativeSqrtError) Error() string {
	    return fmt.Sprintf("math: square root of negative number %g", float64(f))
	}

Um chamador sofisticado pode então usar uma [type assertion](/doc/go_spec.html#Type_assertions)
para verificar se há um `NegativeSqrtError` e tratá-lo de forma especial,
enquanto chamadores que apenas passam o erro para `fmt.Println` ou `log.Fatal` não
verão mudança no comportamento.

Como outro exemplo, o pacote [json](/pkg/encoding/json/)
especifica um tipo `SyntaxError` que a função `json.Decode` retorna
quando encontra um erro de sintaxe ao analisar um blob JSON.

	type SyntaxError struct {
	    msg    string // description of error
	    Offset int64  // error occurred after reading Offset bytes
	}

	func (e *SyntaxError) Error() string { return e.msg }

O campo `Offset` nem é mostrado na formatação padrão do erro,
mas os chamadores podem usá-lo para adicionar informações de arquivo e linha às suas mensagens de erro:

	if err := dec.Decode(&val); err != nil {
	    if serr, ok := err.(*json.SyntaxError); ok {
	        line, col := findLine(f, serr.Offset)
	        return fmt.Errorf("%s:%d:%d: %v", f.Name(), line, col, err)
	    }
	    return err
	}

(Esta é uma versão ligeiramente simplificada de algum [actual code](https://github.com/camlistore/go4/blob/03efcb870d84809319ea509714dd6d19a1498483/jsonconfig/eval.go#L123-L135)
do projeto [Camlistore](http://camlistore.org).)

A interface `error` requer apenas um método `Error`;
implementações de error específicas podem ter métodos adicionais.
Por exemplo, o pacote [net](/pkg/net/) retorna erros do tipo `error`,
seguindo a convenção usual, mas algumas das implementações de error têm
métodos adicionais definidos pela interface `net.Error`:

	package net

	type Error interface {
	    error
	    Timeout() bool   // Is the error a timeout?
	    Temporary() bool // Is the error temporary?
	}

O código cliente pode testar por um `net.Error` com uma type assertion e então distinguir
erros de rede transitórios dos permanentes.
Por exemplo, um web crawler pode dormir e tentar novamente quando encontra um erro
temporário e desistir caso contrário.

	if nerr, ok := err.(net.Error); ok && nerr.Temporary() {
	    time.Sleep(1e9)
	    continue
	}
	if err != nil {
	    log.Fatal(err)
	}

## Simplificando o error handling repetitivo

Em Go, error handling é importante. O design e convenções da linguagem
encorajam você a verificar explicitamente erros onde eles ocorrem (em contraste
com a convenção em outras linguagens de lançar exceptions e às vezes capturá-las).
Em alguns casos isso torna o código Go verboso,
mas felizmente existem algumas técnicas que você pode usar para minimizar o error handling repetitivo.

Considere uma aplicação [App Engine](https://cloud.google.com/appengine/docs/go/)
com um handler HTTP que recupera um registro do datastore
e o formata com um template.

	func init() {
	    http.HandleFunc("/view", viewRecord)
	}

	func viewRecord(w http.ResponseWriter, r *http.Request) {
	    c := appengine.NewContext(r)
	    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
	    record := new(Record)
	    if err := datastore.Get(c, key, record); err != nil {
	        http.Error(w, err.Error(), 500)
	        return
	    }
	    if err := viewTemplate.Execute(w, record); err != nil {
	        http.Error(w, err.Error(), 500)
	    }
	}

Esta função trata erros retornados pela função `datastore.Get` e
pelo método `Execute` do `viewTemplate`.
Em ambos os casos, ela apresenta uma mensagem de erro simples ao usuário com o código
de status HTTP 500 ("Internal Server Error").
Isso parece uma quantidade gerenciável de código,
mas adicione mais alguns handlers HTTP e você rapidamente acaba com muitas cópias
de código idêntico de error handling.

Para reduzir a repetição, podemos definir nosso próprio tipo `appHandler` HTTP que inclui um valor de retorno `error`:

	type appHandler func(http.ResponseWriter, *http.Request) error

Então podemos mudar nossa função `viewRecord` para retornar errors:

	func viewRecord(w http.ResponseWriter, r *http.Request) error {
	    c := appengine.NewContext(r)
	    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
	    record := new(Record)
	    if err := datastore.Get(c, key, record); err != nil {
	        return err
	    }
	    return viewTemplate.Execute(w, record)
	}

Isso é mais simples que a versão original,
mas o pacote [http](/pkg/net/http/) não entende
funções que retornam `error`.
Para corrigir isso, podemos implementar o método `ServeHTTP`
da interface `http.Handler` em `appHandler`:

	func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	    if err := fn(w, r); err != nil {
	        http.Error(w, err.Error(), 500)
	    }
	}

O método `ServeHTTP` chama a função `appHandler` e exibe o
erro retornado (se houver) para o usuário.
Observe que o receiver do método, `fn`, é uma função.
(Go pode fazer isso!) O método invoca a função chamando o receiver
na expressão `fn(w, r)`.

Agora, ao registrar `viewRecord` com o pacote http, usamos a função `Handle`
(em vez de `HandleFunc`) pois `appHandler` é um `http.Handler`
(não um `http.HandlerFunc`).

	func init() {
	    http.Handle("/view", appHandler(viewRecord))
	}

Com esta infraestrutura básica de error handling em vigor,
podemos torná-la mais amigável ao usuário.
Em vez de apenas exibir a string de erro,
seria melhor dar ao usuário uma mensagem de erro simples com um código de status HTTP apropriado,
enquanto registramos o erro completo no console do desenvolvedor do App Engine para fins de debugging.

Para fazer isso, criamos uma struct `appError` contendo um `error` e alguns outros campos:

	type appError struct {
	    Error   error
	    Message string
	    Code    int
	}

Em seguida, modificamos o tipo appHandler para retornar valores `*appError`:

	type appHandler func(http.ResponseWriter, *http.Request) *appError

(Geralmente é um erro retornar o tipo concreto de um erro em vez de `error`,
pelas razões discutidas na [the Go FAQ](/doc/go_faq.html#nil_error),
mas é a coisa certa a fazer aqui porque `ServeHTTP` é o único lugar
que vê o valor e usa seu conteúdo.)

E fazemos o método `ServeHTTP` do `appHandler` exibir a `Message` do `appError`
para o usuário com o `Code` de status HTTP correto e registrar o `Error` completo
no console do desenvolvedor:

	func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	    if e := fn(w, r); e != nil { // e is *appError, not os.Error.
	        c := appengine.NewContext(r)
	        c.Errorf("%v", e.Error)
	        http.Error(w, e.Message, e.Code)
	    }
	}

Finalmente, atualizamos `viewRecord` para a nova assinatura de função e fazemos com que ela
retorne mais contexto quando encontra um erro:

	func viewRecord(w http.ResponseWriter, r *http.Request) *appError {
	    c := appengine.NewContext(r)
	    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
	    record := new(Record)
	    if err := datastore.Get(c, key, record); err != nil {
	        return &appError{err, "Record not found", 404}
	    }
	    if err := viewTemplate.Execute(w, record); err != nil {
	        return &appError{err, "Can't display record", 500}
	    }
	    return nil
	}

Esta versão de `viewRecord` tem o mesmo tamanho da original,
mas agora cada uma dessas linhas tem significado específico e estamos fornecendo uma
experiência de usuário mais amigável.

Não termina aí; podemos melhorar ainda mais o error handling em nossa aplicação. Algumas ideias:

  - dar ao error handler um template HTML bonito,

  - facilitar o debugging escrevendo o stack trace na resposta HTTP quando o usuário é um administrador,

  - escrever uma função construtora para `appError` que armazene o stack trace para facilitar o debugging,

  - recuperar de panics dentro do `appHandler`,
    registrando o erro no console como "Critical," enquanto diz ao usuário que "um
    erro sério ocorreu." Este é um toque agradável para evitar expor o
    usuário a mensagens de erro inescrutáveis causadas por erros de programação.
    Veja o artigo [Defer, Panic, and Recover](/doc/articles/defer_panic_recover.html)
    para mais detalhes.

## Conclusão

O error handling adequado é um requisito essencial de um bom software.
Ao empregar as técnicas descritas neste post, você deve ser capaz de
escrever código Go mais confiável e sucinto.

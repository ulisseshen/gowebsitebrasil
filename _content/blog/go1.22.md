---
ia-translated: true
title: Go 1.22 foi lançado!
date: 2024-02-06
by:
- Eli Bendersky, em nome da equipe Go
summary: Go 1.22 melhora loops for, traz novas funcionalidades da biblioteca padrão e melhora performance.
---

Hoje a equipe Go está empolgada em lançar o Go 1.22,
que você pode obter visitando a [página de download](/dl/).

Go 1.22 vem com várias novas funcionalidades e melhorias importantes. Aqui estão
algumas das mudanças notáveis; para a lista completa, consulte as [notas de
lançamento](/doc/go1.22).

## Mudanças na linguagem

O problema antigo do loop "for" com compartilhamento acidental de variáveis de loop
entre iterações agora está resolvido. Começando com Go 1.22, o seguinte código
imprimirá "a", "b" e "c" em alguma ordem:

{{raw `
	func main() {
		done := make(chan bool)

		values := []string{"a", "b", "c"}
		for _, v := range values {
			go func() {
				fmt.Println(v)
				done <- true
			}()
		}

		// wait for all goroutines to complete before exiting
		for _ = range values {
			<-done
		}
	}
`}}

Para mais informações sobre esta mudança e as ferramentas que ajudam a manter o código
funcionando sem quebrar acidentalmente, veja o [post anterior sobre variável de
loop](/blog/loopvar-preview).

A segunda mudança na linguagem é o suporte para range sobre inteiros:

{{raw `
	package main

	import "fmt"

	func main() {
		for i := range 10 {
			fmt.Println(10 - i)
		}
		fmt.Println("go1.22 has lift-off!")
	}
`}}

Os valores de `i` neste programa de contagem regressiva vão de 0 a 9, inclusive. Para mais
detalhes, por favor consulte [a especificação](/ref/spec#For_range).

## Performance melhorada

Otimização de memória no runtime Go melhora a performance de CPU em 1-3%, enquanto
também reduz a sobrecarga de memória da maioria dos programas Go em cerca de 1%.

No Go 1.21, [lançamos](/blog/pgo) otimização guiada por perfil (PGO) para o
compilador Go e esta funcionalidade continua a melhorar. Uma das otimizações
adicionadas em 1.22 é a devirtualização melhorada, permitindo dispatch estático de mais
chamadas de método de interface. A maioria dos programas verá melhorias entre 2-14% com
PGO habilitado.

## Adições à biblioteca padrão

- Um novo pacote [math/rand/v2](/pkg/math/rand/v2)
  fornece uma API mais limpa e consistente e usa algoritmos de geração
  pseudo-aleatória de maior qualidade e mais rápidos. Veja
  [a proposta](/issue/61716) para detalhes adicionais.
- Os padrões usados por [net/http.ServeMux](/pkg/net/http#ServeMux)
  agora aceitam métodos e wildcards.

  Por exemplo, o roteador aceita um padrão como `GET /task/{id}/`, que
  corresponde apenas a requisições `GET` e captura o valor do segmento `{id}`
  em um map que pode ser acessado através de valores [Request](/pkg/net/http#Request).
- Um novo tipo `Null[T]` em [database/sql](/pkg/database/sql) fornece
  uma maneira de escanear colunas nullable.
- Uma função `Concat` foi adicionada no pacote [slices](/pkg/slices), para
  concatenar múltiplos slices de qualquer tipo.

---

Obrigado a todos que contribuíram para este lançamento escrevendo código e
documentação, reportando bugs, compartilhando feedback e testando os release
candidates. Seus esforços ajudaram a garantir que Go 1.22 seja o mais estável possível.
Como sempre, se você notar qualquer problema, por favor [abra uma issue](/issue/new).

Aproveite o Go 1.22!

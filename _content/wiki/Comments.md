---
ia-translated: true
title: Comments
---

<!--
Isto é apenas uma página de marcação de posição para habilitar um teste.
No site implantado, ela é sobrescrita com o conteúdo de go.googlesource.com/wiki.
-->

Todo package deve ter um package comment. Ele deve preceder imediatamente a declaração ` package ` em um dos arquivos do package. (Ele só precisa aparecer em um arquivo.) Deve começar com uma única frase que inicie com "Package _packagename_" e fornecer um resumo conciso da funcionalidade do package. Esta frase introdutória será usada na lista de todos os packages do godoc.

Frases e/ou parágrafos subsequentes podem fornecer mais detalhes. As frases devem ser pontuadas adequadamente.

```go
// Package superman implements methods for saving the world.
//
// Experience has shown that a small number of procedures can prove
// helpful when attempting to save the world.
package superman
```

Quase todo type, const, var e func de nível superior deve ter um comment. Um comment para bar deve estar na forma "_bar_ floats on high o'er vales and hills.". A primeira letra de _bar_ não deve ser maiúscula, a menos que esteja em maiúscula no código.

```go
// enterOrbit causes Superman to fly into low Earth orbit, a position
// that presents several possibilities for planet salvation.
func enterOrbit() os.Error {
  ...
}
```

Todo texto que você indentar dentro de um comment, o godoc renderizará como um bloco pré-formatado. Isso facilita exemplos de código.

```go
// fight can be used on any enemy and returns whether Superman won.
//
// Examples:
//
//  fight("a random potato")
//  fight(LexLuthor{})
//
func fight(enemy interface{}) bool {
	// This is testing proper escaping in the wiki.
	for i := 0; i < 10; i++ {
		println("fight!")
	}
}
```



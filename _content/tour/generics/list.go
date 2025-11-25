//go:build OMIT

package main

// List representa uma singly-linked list que mantém
// valores de qualquer tipo.
type List[T any] struct {
	next *List[T]
	val  T
}

func main() {
}

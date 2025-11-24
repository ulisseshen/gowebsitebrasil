---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Começando com generics",
  "Breadcrumb": true
}-->

Este tutorial introduz os fundamentos de generics em Go. Com generics, você pode
declarar e usar funções ou tipos que são escritos para funcionar com qualquer conjunto
de tipos fornecidos pelo código chamador.

Neste tutorial, você declarará duas funções simples não-genéricas, então capturará
a mesma lógica em uma única função genérica.

Você progredirá através das seguintes seções:

1. Criar uma pasta para seu código.
2. Adicionar funções não-genéricas.
3. Adicionar uma função genérica para lidar com múltiplos tipos.
4. Remover argumentos de tipo ao chamar a função genérica.
5. Declarar uma type constraint.

**Nota:** Para outros tutoriais, veja [Tutoriais](/doc/tutorial/index.html).

**Nota:** Se você preferir, pode usar
[o Go playground no modo "Go dev branch"](/play/?v=gotip)
para editar e executar seu programa em vez disso.

## Pré-requisitos

*   **Uma instalação do Go 1.18 ou posterior.** Para instruções de instalação, veja
    [Instalando Go](/doc/install).
*   **Uma ferramenta para editar seu código.** Qualquer editor de texto que você tenha funcionará bem.
*   **Um terminal de comando.** Go funciona bem usando qualquer terminal no Linux e Mac,
    e no PowerShell ou cmd no Windows.

## Criar uma pasta para seu código {#create_folder}

Para começar, crie uma pasta para o código que você escreverá.

1. Abra um prompt de comando e mude para seu diretório home.

    No Linux ou Mac:

    ```
    $ cd
    ```

    No Windows:

    ```
    C:\> cd %HOMEPATH%
    ```

    O resto do tutorial mostrará um $ como o prompt. Os comandos que você usa
    funcionarão no Windows também.

2. Do prompt de comando, crie um diretório para seu código chamado generics.

    ```
    $ mkdir generics
    $ cd generics
    ```

3. Crie um módulo para manter seu código.

    Execute o comando `go mod init`, dando a ele o caminho do módulo do seu novo código.

    ```
    $ go mod init example/generics
    go: creating new go.mod: module example/generics
    ```

    **Nota:** Para código de produção, você especificaria um caminho de módulo que é mais específico
    para suas próprias necessidades. Para mais, certifique-se de ver
    [Gerenciando dependências](/doc/modules/managing-dependencies).

A seguir, você adicionará algum código simples para trabalhar com maps.

## Adicionar funções não-genéricas {#non_generic_functions}

Neste passo, você adicionará duas funções que cada uma soma os valores de um
map e retorna o total.

Você está declarando duas funções em vez de uma porque está trabalhando com dois
tipos diferentes de maps: um que armazena valores `int64`, e um que armazena valores `float64`.

#### Escrever o código

1. Usando seu editor de texto, crie um arquivo chamado main.go no diretório
    generics. Você escreverá seu código Go neste arquivo.
2. Em main.go, no topo do arquivo, cole a seguinte declaração de
    package.

    ```
    package main
    ```

    Um programa standalone (ao contrário de uma biblioteca) está sempre no package `main`.

3. Abaixo da declaração de package, cole as seguintes duas declarações de
    função.

    ```
    // SumInts adds together the values of m.
    func SumInts(m map[string]int64) int64 {
    	var s int64
    	for _, v := range m {
    		s += v
    	}
    	return s
    }

    // SumFloats adds together the values of m.
    func SumFloats(m map[string]float64) float64 {
    	var s float64
    	for _, v := range m {
    		s += v
    	}
    	return s
    }
    ```

    Neste código, você:

    *   Declara duas funções para somar os valores de um map e retornar
        a soma.
        *   `SumFloats` recebe um map de `string` para valores `float64`.
        *   `SumInts` recebe um map de `string` para valores `int64`.

4. No topo de main.go, abaixo da declaração de package, cole a seguinte
    função `main` para inicializar os dois maps e usá-los como argumentos ao
    chamar as funções que você declarou no passo anterior.

    ```
    func main() {
    	// Initialize a map for the integer values
    	ints := map[string]int64{
    		"first":  34,
    		"second": 12,
    	}

    	// Initialize a map for the float values
    	floats := map[string]float64{
    		"first":  35.98,
    		"second": 26.99,
    	}

    	fmt.Printf("Non-Generic Sums: %v and %v\n",
    		SumInts(ints),
    		SumFloats(floats))
    }
    ```

    Neste código, você:

    *   Inicializa um map de valores `float64` e um map de valores `int64`, cada
        um com duas entradas.
    *   Chama as duas funções que você declarou anteriormente para encontrar a soma dos
        valores de cada map.
    *   Imprime o resultado.

5. Próximo ao topo de main.go, logo abaixo da declaração de package, importe o
    pacote que você precisará para suportar o código que você acabou de escrever.

    As primeiras linhas de código devem ficar assim:

    ```
    package main

    import "fmt"
    ```

6. Salve main.go.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Non-Generic Sums: 46 and 62.97
```

Com generics, você pode escrever uma função aqui em vez de duas. A seguir, você
adicionará uma única função genérica para maps contendo valores integer ou float.

## Adicionar uma função genérica para lidar com múltiplos tipos {#add_generic_function}

Nesta seção, você adicionará uma única função genérica que pode receber um map
contendo valores integer ou float, efetivamente substituindo as duas
funções que você acabou de escrever com uma única função.

Para suportar valores de qualquer tipo, essa única função precisará de uma maneira de
declarar quais tipos ela suporta. O código chamador, por outro lado, precisará de uma
maneira de especificar se está chamando com um map integer ou float.

Para suportar isso, você escreverá uma função que declara _type parameters_ além
de seus parâmetros de função ordinários. Esses type parameters tornam a
função genérica, permitindo que ela funcione com argumentos de diferentes tipos. Você
chamará a função com _type arguments_ e argumentos de função ordinários.

Cada type parameter tem uma _type constraint_ que age como uma espécie de meta-tipo
para o type parameter. Cada type constraint especifica os argumentos de tipo
permitidos que o código chamador pode usar para o respectivo type parameter.

Embora a constraint de um type parameter tipicamente represente um conjunto de tipos, em
tempo de compilação o type parameter representa um único tipo – o tipo fornecido
como um type argument pelo código chamador. Se o tipo do type argument não é
permitido pela constraint do type parameter, o código não compilará.

Tenha em mente que um type parameter deve suportar todas as operações que o código genérico
está realizando nele. Por exemplo, se o código da sua função tentasse
realizar operações de `string` (como indexação) em um type parameter cuja
constraint incluísse tipos numéricos, o código não compilaria.

No código que você está prestes a escrever, você usará uma constraint que permite
tipos integer ou float.

#### Escrever o código

1. Abaixo das duas funções que você adicionou anteriormente, cole a seguinte função
    genérica.

    ```
    // SumIntsOrFloats sums the values of map m. It supports both int64 and float64
    // as types for map values.
    func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
        var s V
        for _, v := range m {
            s += v
        }
        return s
    }
    ```

    Neste código, você:

    *   Declara uma função `SumIntsOrFloats` com dois type parameters (dentro
        dos colchetes), `K` e `V`, e um argumento que usa os type
        parameters, `m` do tipo `map[K]V`. A função retorna um valor do
        tipo `V`.
    *   Especifica para o type parameter `K` a type constraint `comparable`.
        Destinada especificamente para casos como estes, a constraint `comparable`
        é pré-declarada em Go. Ela permite qualquer tipo cujos valores podem ser usados como
        operando dos operadores de comparação `==` e `!=`. Go requer que chaves de map
        sejam comparáveis. Então declarar `K` como `comparable` é necessário para que você
        possa usar `K` como a chave na variável map. Também garante que o código
        chamador use um tipo permitido para chaves de map.
    *   Especifica para o type parameter `V` uma constraint que é uma união de dois
        tipos: `int64` e `float64`. Usar `|` especifica uma união dos dois
        tipos, significando que esta constraint permite qualquer um dos tipos. Qualquer tipo
        será permitido pelo compilador como um argumento no código chamador.
    *   Especifica que o argumento `m` é do tipo `map[K]V`, onde `K` e `V`
        são os tipos já especificados para os type parameters. Note que sabemos
        que `map[K]V` é um tipo de map válido porque `K` é um tipo comparável. Se
        não tivéssemos declarado `K` comparable, o compilador rejeitaria a
        referência a `map[K]V`.

2. Em main.go, abaixo do código que você já tem, cole o seguinte código.

    ```
    fmt.Printf("Generic Sums: %v and %v\n",
    	SumIntsOrFloats[string, int64](ints),
    	SumIntsOrFloats[string, float64](floats))
    ```

    Neste código, você:

    *   Chama a função genérica que você acabou de declarar, passando cada um dos maps
        que você criou.
    *   Especifica type arguments – os nomes de tipo em colchetes – para ficar
        claro sobre os tipos que devem substituir os type parameters na
        função que você está chamando.

        Como você verá na próxima seção, muitas vezes você pode omitir os type
        arguments na chamada de função. Go pode frequentemente inferi-los do seu código.
    *   Imprime as somas retornadas pela função.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
```

Para executar seu código, em cada chamada o compilador substituiu os type parameters com
os tipos concretos especificados naquela chamada.

Ao chamar a função genérica que você escreveu, você especificou type arguments que
disseram ao compilador quais tipos usar no lugar dos type parameters da função.
Como você verá na próxima seção, em muitos casos você pode omitir esses type
arguments porque o compilador pode inferi-los.

## Remover type arguments ao chamar a função genérica {#remove_type_arguments}

Nesta seção, você adicionará uma versão modificada da chamada da função genérica,
fazendo uma pequena mudança para simplificar o código chamador. Você removerá os type
arguments, que não são necessários neste caso.

Você pode omitir type arguments no código chamador quando o compilador Go pode inferir os
tipos que você quer usar. O compilador infere type arguments dos tipos dos
argumentos da função.

Note que isso nem sempre é possível. Por exemplo, se você precisasse chamar uma
função genérica que não tivesse argumentos, você precisaria incluir os type
arguments na chamada da função.

#### Escrever o código

*   Em main.go, abaixo do código que você já tem, cole o seguinte código.

    ```
    fmt.Printf("Generic Sums, type parameters inferred: %v and %v\n",
    	SumIntsOrFloats(ints),
    	SumIntsOrFloats(floats))
    ```

    Neste código, você:

    *   Chama a função genérica, omitindo os type arguments.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
Generic Sums, type parameters inferred: 46 and 62.97
```

A seguir, você simplificará ainda mais a função capturando a união de integers
e floats em uma type constraint que você pode reutilizar, como de outro código.

## Declarar uma type constraint {#declare_type_constraint}

Nesta última seção, você moverá a constraint que definiu anteriormente para sua
própria interface para que possa reutilizá-la em múltiplos lugares. Declarar
constraints desta forma ajuda a simplificar o código, como quando uma constraint é
mais complexa.

Você declara uma _type constraint_ como uma interface. A constraint permite qualquer
tipo implementando a interface. Por exemplo, se você declarar uma interface de type constraint
com três métodos, então usá-la com um type parameter em uma função
genérica, type arguments usados para chamar a função devem ter todos esses
métodos.

Interfaces de constraint também podem se referir a tipos específicos, como você verá nesta
seção.

#### Escrever o código

1. Logo acima de `main`, imediatamente após as instruções import, cole o
    seguinte código para declarar uma type constraint.

    ```
    type Number interface {
        int64 | float64
    }
    ```

    Neste código, você:

    *   Declara o tipo de interface `Number` para usar como uma type constraint.
    *   Declara uma união de `int64` e `float64` dentro da interface.

        Essencialmente, você está movendo a união da declaração da função
        para uma nova type constraint. Dessa forma, quando você quer restringir um type
        parameter a `int64` ou `float64`, você pode usar esta type constraint `Number`
        em vez de escrever `int64 | float64`.

2. Abaixo das funções que você já tem, cole a seguinte função genérica
    `SumNumbers`.

    ```
    // SumNumbers sums the values of map m. It supports both integers
    // and floats as map values.
    func SumNumbers[K comparable, V Number](m map[K]V) V {
        var s V
        for _, v := range m {
            s += v
        }
        return s
    }
    ```

    Neste código, você:

    *   Declara uma função genérica com a mesma lógica que a função genérica
        que você declarou anteriormente, mas com o novo tipo de interface em vez da
        união como a type constraint. Como antes, você usa os type parameters
        para os tipos de argumento e retorno.

3. Em main.go, abaixo do código que você já tem, cole o seguinte código.

    ```
    fmt.Printf("Generic Sums with Constraint: %v and %v\n",
    	SumNumbers(ints),
    	SumNumbers(floats))
    ```

    Neste código, você:

    *   Chama `SumNumbers` com cada map, imprimindo a soma dos valores de
        cada um.

        Como na seção anterior, você omite os type arguments (os nomes de tipo
        em colchetes) em chamadas à função genérica. O compilador Go
        pode inferir o type argument de outros argumentos.

#### Executar o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
Generic Sums, type parameters inferred: 46 and 62.97
Generic Sums with Constraint: 46 and 62.97
```

## Conclusão {#conclusion}

Muito bem feito! Você acabou de se apresentar a generics em Go.

Próximos tópicos sugeridos:

*   O [Go Tour](/tour/) é uma ótima introdução passo a passo
    aos fundamentos do Go.
*   Você encontrará práticas recomendadas úteis do Go descritas em
    [Effective Go](/doc/effective_go) e
    [Como escrever código Go](/doc/code).

## Código completo {#completed_code}

<!--TODO: Update text and link after release.-->
Você pode executar este programa no
[Go playground](/play/p/apNmfVwogK0?v=gotip). No
playground simplesmente clique no botão **Run**.

```
package main

import "fmt"

type Number interface {
	int64 | float64
}

func main() {
	// Initialize a map for the integer values
	ints := map[string]int64{
		"first": 34,
		"second": 12,
	}

	// Initialize a map for the float values
	floats := map[string]float64{
		"first": 35.98,
		"second": 26.99,
	}

	fmt.Printf("Non-Generic Sums: %v and %v\n",
		SumInts(ints),
		SumFloats(floats))

	fmt.Printf("Generic Sums: %v and %v\n",
		SumIntsOrFloats[string, int64](ints),
		SumIntsOrFloats[string, float64](floats))

	fmt.Printf("Generic Sums, type parameters inferred: %v and %v\n",
		SumIntsOrFloats(ints),
		SumIntsOrFloats(floats))

	fmt.Printf("Generic Sums with Constraint: %v and %v\n",
		SumNumbers(ints),
		SumNumbers(floats))
}

// SumInts adds together the values of m.
func SumInts(m map[string]int64) int64 {
	var s int64
	for _, v := range m {
		s += v
	}
	return s
}

// SumFloats adds together the values of m.
func SumFloats(m map[string]float64) float64 {
	var s float64
	for _, v := range m {
		s += v
	}
	return s
}

// SumIntsOrFloats sums the values of map m. It supports both floats and integers
// as map values.
func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}

// SumNumbers sums the values of map m. Its supports both integers
// and floats as map values.
func SumNumbers[K comparable, V Number](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}
```

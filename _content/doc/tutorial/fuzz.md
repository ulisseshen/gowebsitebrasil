<!--{
  "Title": "Tutorial: Getting started with fuzzing",
  "HideTOC": true,
  "Breadcrumb": true,
  "ia-translated": true
}-->

Este tutorial apresenta os conceitos básicos de fuzzing em Go. Com fuzzing, dados aleatórios
são executados contra seu teste na tentativa de encontrar vulnerabilidades ou entradas que causem falhas.
Alguns exemplos de vulnerabilidades que podem ser encontradas por fuzzing são SQL
injection, buffer overflow, denial of service e ataques de cross-site scripting.

Neste tutorial, você escreverá um fuzz test para uma função simples, executará o comando go,
e fará debug e corrigirá problemas no código.

Para ajuda com terminologia ao longo deste tutorial, consulte o [glossário de Go Fuzzing](/security/fuzz/#glossary).

Você avançará pelas seguintes seções:

1. [Criar uma pasta para seu código.](#create_folder)
2. [Adicionar código para testar.](#code_to_test)
3. [Adicionar um teste unitário.](#unit_test)
4. [Adicionar um fuzz test.](#fuzz_test)
5. [Corrigir dois bugs.](#fix_invalid_string_error)
6. [Explorar recursos adicionais.](#conclusion)

**Nota:** Para outros tutoriais, consulte [Tutoriais](/doc/tutorial/index.html).

**Nota:** Go fuzzing atualmente suporta um subconjunto de tipos built-in, listados na
[documentação de Go Fuzzing](/security/fuzz/#requirements), com suporte para mais tipos built-in
a serem adicionados no futuro.

## Pré-requisitos

- **Uma instalação do Go 1.18 ou posterior.** Para instruções de instalação, consulte
  [Instalando Go](/doc/install).
- **Uma ferramenta para editar seu código.** Qualquer editor de texto que você tenha funcionará bem.
- **Um terminal de comandos.** Go funciona bem usando qualquer terminal no Linux e Mac, e
  no PowerShell ou cmd no Windows.
- **Um ambiente que suporte fuzzing.** Go fuzzing com instrumentação de coverage
  está disponível apenas em arquiteturas AMD64 e ARM64 atualmente.

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

   O resto do tutorial mostrará um $ como prompt. Os comandos que você usar
   funcionarão no Windows também.

2. Do prompt de comando, crie um diretório para seu código chamado fuzz.

   ```
   $ mkdir fuzz
   $ cd fuzz
   ```

3. Crie um módulo para conter seu código.

   Execute o comando `go mod init`, fornecendo o caminho do módulo do seu novo código.

   ```
   $ go mod init example/fuzz
   go: creating new go.mod: module example/fuzz
   ```

   **Nota:** Para código de produção, você especificaria um caminho de módulo mais
   específico para suas próprias necessidades. Para mais, consulte [Gerenciando
   dependências](/doc/modules/managing-dependencies).

Em seguida, você adicionará um código simples para reverter uma string, que faremos fuzz posteriormente.

## Adicionar código para testar {#code_to_test}

Neste passo, você adicionará uma função para reverter uma string.

### Escreva o código

1.  Usando seu editor de texto, crie um arquivo chamado main.go no diretório fuzz.
2.  Em main.go, no topo do arquivo, cole a seguinte declaração de package.

    ```
    package main
    ```

    Um programa standalone (em oposição a uma biblioteca) está sempre no package `main`.

3.  Abaixo da declaração de package, cole a seguinte declaração de função.

    ```
    func Reverse(s string) string {
        b := []byte(s)
        for i, j := 0, len(b)-1; i {{raw "<"}} len(b)/2; i, j = i+1, j-1 {
            b[i], b[j] = b[j], b[i]
        }
        return string(b)
    }
    ```

    Esta função aceitará uma `string`, iterará sobre ela um `byte` de cada vez, e
    retornará a string invertida no final.

    _Nota:_ Este código é baseado na função `stringutil.Reverse` dentro de
    golang.org/x/example.

4.  No topo de main.go, abaixo da declaração de package, cole a seguinte
    função `main` para inicializar uma string, invertê-la, imprimir a saída, e
    repetir.

    ```
    func main() {
        input := "The quick brown fox jumped over the lazy dog"
        rev := Reverse(input)
        doubleRev := Reverse(rev)
        fmt.Printf("original: %q\n", input)
        fmt.Printf("reversed: %q\n", rev)
        fmt.Printf("reversed again: %q\n", doubleRev)
    }
    ```

    Esta função executará algumas operações `Reverse`, então imprimirá a saída na
    linha de comando. Isso pode ser útil para ver o código em ação, e
    potencialmente para debugging.

5.  A função `main` usa o package fmt, então você precisará importá-lo.

    As primeiras linhas de código devem ficar assim:

    ```
    package main

    import "fmt"
    ```

### Execute o código

Da linha de comando no diretório contendo main.go, execute o código.

```
$ go run .
original: "The quick brown fox jumped over the lazy dog"
reversed: "god yzal eht revo depmuj xof nworb kciuq ehT"
reversed again: "The quick brown fox jumped over the lazy dog"
```

Você pode ver a string original, o resultado de invertê-la, depois o resultado de
invertê-la novamente, que é equivalente à original.

Agora que o código está funcionando, é hora de testá-lo.

## Adicionar um teste unitário {#unit_test}

Neste passo, você escreverá um teste unitário básico para a função `Reverse`.

### Escreva o código

1. Usando seu editor de texto, crie um arquivo chamado reverse_test.go no diretório fuzz.
2. Cole o seguinte código em reverse_test.go.

   ```
   package main

   import (
       "testing"
   )

   func TestReverse(t *testing.T) {
       testcases := []struct {
           in, want string
       }{
           {"Hello, world", "dlrow ,olleH"},
           {" ", " "},
           {"!12345", "54321!"},
       }
       for _, tc := range testcases {
           rev := Reverse(tc.in)
           if rev != tc.want {
                   t.Errorf("Reverse: %q, want %q", rev, tc.want)
           }
       }
   }
   ```

   Este teste simples verificará que as strings de entrada listadas serão corretamente
   invertidas.

### Execute o código

Execute o teste unitário usando `go test`

```
$ go test
PASS
ok      example/fuzz  0.013s
```

Em seguida, você mudará o teste unitário para um fuzz test.

## Adicionar um fuzz test {#fuzz_test}

O teste unitário tem limitações, nomeadamente que cada entrada deve ser adicionada ao teste
pelo desenvolvedor. Um benefício do fuzzing é que ele cria entradas para
seu código, e pode identificar casos extremos que os casos de teste que você criou
não alcançaram.

Nesta seção você converterá o teste unitário em um fuzz test para que você possa
gerar mais entradas com menos trabalho!

Observe que você pode manter testes unitários, benchmarks e fuzz tests no mesmo
arquivo *_test.go, mas para este exemplo você converterá o teste unitário em um fuzz
test.

### Escreva o código

No seu editor de texto, substitua o teste unitário em reverse_test.go pelo seguinte
fuzz test.

```
func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc)  // Use f.Add to provide a seed corpus
    }
    f.Fuzz(func(t *testing.T, orig string) {
        rev := Reverse(orig)
        doubleRev := Reverse(rev)
        if orig != doubleRev {
            t.Errorf("Before: %q, after: %q", orig, doubleRev)
        }
        if utf8.ValidString(orig) && !utf8.ValidString(rev) {
            t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
        }
    })
}
```

Fuzzing também tem algumas limitações. No seu teste unitário, você poderia prever a
saída esperada da função `Reverse`, e verificar que a saída real atendia
essas expectativas.

Por exemplo, no caso de teste `Reverse("Hello, world")` o teste unitário especifica
o retorno como `"dlrow ,olleH"`.

Ao fazer fuzzing, você não pode prever a saída esperada, já que você não tem
controle sobre as entradas.

No entanto, há algumas propriedades da função `Reverse` que você pode
verificar em um fuzz test. As duas propriedades sendo verificadas neste fuzz test são:

1.  Inverter uma string duas vezes preserva o valor original
2.  A string invertida preserva seu estado como UTF-8 válido.

Observe as diferenças de sintaxe entre o teste unitário e o fuzz test:

- A função começa com FuzzXxx em vez de TestXxx, e recebe `*testing.F`
  em vez de `*testing.T`
- Onde você esperaria ver uma execução `t.Run`, você vê em vez disso `f.Fuzz`
  que recebe uma função fuzz target cujos parâmetros são `*testing.T` e os
  tipos a serem fuzzed. As entradas do seu teste unitário são fornecidas como seed corpus
  inputs usando `f.Add`.

Garanta que o novo package, `unicode/utf8` foi importado.

```
package main

import (
    "testing"
    "unicode/utf8"
)
```

Com o teste unitário convertido para um fuzz test, é hora de executar o teste novamente.

### Execute o código

1. Execute o fuzz test sem fazer fuzzing para garantir que as seed inputs passam.

   ```
   $ go test
   PASS
   ok      example/fuzz  0.013s
   ```

   Você também pode executar `go test -run=FuzzReverse` se você tiver outros testes nesse
   arquivo, e você deseja executar apenas o fuzz test.

2. Execute `FuzzReverse` com fuzzing, para ver se alguma string de entrada gerada aleatoriamente
   causará uma falha. Isso é executado usando `go test` com uma nova
   flag, `-fuzz`, definida para o parâmetro `Fuzz`. Copie o comando abaixo.

    ```
    $ go test -fuzz=Fuzz
    ```

    Outra flag útil é `-fuzztime`, que restringe o tempo que o fuzzing leva.
    Por exemplo, especificar `-fuzztime 10s` no teste abaixo significaria que,
    desde que nenhuma falha ocorra antes, o teste sairá por padrão
    após 10 segundos terem passado. Veja [esta
    seção](https://pkg.go.dev/cmd/go#hdr-Testing_flags) da documentação cmd/go
    para ver outras flags de teste.

   Agora, execute o comando que você acabou de copiar.

   ```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/3 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 3/3 completed, now fuzzing with 8 workers
   fuzz: minimizing 38-byte failing input file...
   --- FAIL: FuzzReverse (0.01s)
       --- FAIL: FuzzReverse (0.00s)
           reverse_test.go:20: Reverse produced invalid UTF-8 string "\x9c\xdd"

       Failing input written to testdata/fuzz/FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a
       To re-run:
       go test -run=FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a
   FAIL
   exit status 1
   FAIL    example/fuzz  0.030s
   ```

   Uma falha ocorreu durante o fuzzing, e a entrada que causou o problema é
   escrita em um arquivo seed corpus que será executado na próxima vez que `go test` for
   chamado, mesmo sem a flag `-fuzz`. Para visualizar a entrada que causou a
   falha, abra o arquivo corpus escrito no diretório testdata/fuzz/FuzzReverse
   em um editor de texto. Seu arquivo seed corpus pode conter uma string diferente, mas o formato será o mesmo.

   ```
   go test fuzz v1
   string("泃")
   ```

   A primeira linha do arquivo corpus indica a versão de codificação. Cada
   linha seguinte representa o valor de cada tipo que compõe a entrada do corpus.
   Como o fuzz target recebe apenas 1 entrada, há apenas 1 valor após a
   versão.

3. Execute `go test` novamente sem a flag `-fuzz`; a nova entrada failing seed corpus
   será usada:

   ```
   $ go test
   --- FAIL: FuzzReverse (0.00s)
       --- FAIL: FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a (0.00s)
           reverse_test.go:20: Reverse produced invalid string
   FAIL
   exit status 1
   FAIL    example/fuzz  0.016s
   ```

   Como nosso teste falhou, é hora de fazer debug.

## Corrigir o erro de string inválida {#fix_invalid_string_error}

Nesta seção, você fará debug da falha e corrigirá o bug.

Sinta-se livre para gastar algum tempo pensando sobre isso e tentando corrigir o problema
você mesmo antes de seguir em frente.

### Diagnosticar o erro

Há algumas maneiras diferentes de você fazer debug deste erro. Se você está usando VS
Code como seu editor de texto, você pode [configurar seu
debugger](https://github.com/golang/vscode-go/blob/master/docs/debugging.md) para
investigar.

Neste tutorial, nós vamos registrar informação útil de debugging no seu terminal.

Primeiro, considere a documentação para
[`utf8.ValidString`](https://pkg.go.dev/unicode/utf8).

```
ValidString reports whether s consists entirely of valid UTF-8-encoded runes.
```

A função `Reverse` atual inverte a string byte por byte, e aí está
nosso problema. Para preservar as runes codificadas em UTF-8 da string original,
devemos em vez disso inverter a string rune por rune.

Para examinar por que a entrada (neste caso, o caractere chinês `泃`) está causando
`Reverse` produzir uma string inválida quando invertida, você pode inspecionar o número
de runes na string invertida.

#### Escreva o código

No seu editor de texto, substitua o fuzz target dentro de `FuzzReverse` pelo
seguinte.

```
f.Fuzz(func(t *testing.T, orig string) {
    rev := Reverse(orig)
    doubleRev := Reverse(rev)
    t.Logf("Number of runes: orig=%d, rev=%d, doubleRev=%d", utf8.RuneCountInString(orig), utf8.RuneCountInString(rev), utf8.RuneCountInString(doubleRev))
    if orig != doubleRev {
        t.Errorf("Before: %q, after: %q", orig, doubleRev)
    }
    if utf8.ValidString(orig) && !utf8.ValidString(rev) {
        t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
    }
})
```

Esta linha `t.Logf` imprimirá na linha de comando se um erro ocorrer, ou se
executar o teste com `-v`, o que pode ajudá-lo a fazer debug deste problema particular.

#### Execute o código

Execute o teste usando go test

```
$ go test
--- FAIL: FuzzReverse (0.00s)
    --- FAIL: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00s)
        reverse_test.go:16: Number of runes: orig=1, rev=3, doubleRev=1
        reverse_test.go:21: Reverse produced invalid UTF-8 string "\x83\xb3\xe6"
FAIL
exit status 1
FAIL    example/fuzz    0.598s
```

Todo o seed corpus usou strings em que cada caractere era um único byte.
No entanto, caracteres como 泃 podem requerer vários bytes. Assim, inverter a
string byte por byte invalidará caracteres multi-byte.

**Nota:** Se você está curioso sobre como Go lida com strings, leia o post do blog
[Strings, bytes, runes and characters in Go](/blog/strings) para uma
compreensão mais profunda.

Com uma melhor compreensão do bug, corrija o erro na função `Reverse`.

### Corrigir o erro

Para corrigir a função `Reverse`, vamos percorrer a string por runes, em vez
de por bytes.

#### Escreva o código

No seu editor de texto, substitua a função Reverse() existente pela seguinte.

```
func Reverse(s string) string {
    r := []rune(s)
    for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r)
}
```

A diferença chave é que `Reverse` agora está iterando sobre cada `rune` na
string, em vez de cada `byte`. Observe que este é apenas um exemplo, e não
lida com [combining characters](https://en.wikipedia.org/wiki/Combining_character) corretamente.

#### Execute o código

1. Execute o teste usando `go test`

   ```
   $ go test
   PASS
   ok      example/fuzz  0.016s
   ```

   O teste agora passa!

2. Faça fuzz novamente com `go test -fuzz`, para ver se há novos bugs.

   ```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/37 completed
   fuzz: minimizing 506-byte failing input file...
   fuzz: elapsed: 0s, gathering baseline coverage: 5/37 completed
   --- FAIL: FuzzReverse (0.02s)
       --- FAIL: FuzzReverse (0.00s)
           reverse_test.go:33: Before: "\x91", after: "�"

       Failing input written to testdata/fuzz/FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c
       To re-run:
       go test -run=FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c
   FAIL
   exit status 1
   FAIL    example/fuzz  0.032s
   ```

   Podemos ver que a string é diferente da original após ser
   invertida duas vezes. Desta vez a entrada em si é unicode inválido. Como isso é
   possível se estamos fazendo fuzzing com strings?

   Vamos fazer debug novamente.

## Corrigir o erro de inversão dupla {#fix_double_reverse_error}

Nesta seção, você fará debug da falha de inversão dupla e corrigirá o bug.

Sinta-se livre para gastar algum tempo pensando sobre isso e tentando corrigir o problema
você mesmo antes de seguir em frente.

### Diagnosticar o erro

Como antes, há várias maneiras de você fazer debug desta falha. Neste caso,
usar um
[debugger](https://github.com/golang/vscode-go/blob/master/docs/debugging.md)
seria uma ótima abordagem.

Neste tutorial, nós vamos registrar informação útil de debugging na função `Reverse`.

Olhe atentamente para a string invertida para identificar o erro. Em Go, [uma string é um
slice somente leitura de bytes](/blog/strings), e pode conter bytes
que não são UTF-8 válido. A string original é um slice de bytes com um byte,
`'\x91'`. Quando a string de entrada é definida para `[]rune`, Go codifica o slice de bytes para
UTF-8, e substitui o byte com o caractere UTF-8 �. Quando comparamos o
caractere UTF-8 de substituição ao slice de bytes de entrada, eles claramente não são iguais.

#### Escreva o código

1. No seu editor de texto, substitua a função `Reverse` pela seguinte.

   ```
   func Reverse(s string) string {
       fmt.Printf("input: %q\n", s)
       r := []rune(s)
       fmt.Printf("runes: %q\n", r)
       for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r)
   }
   ```

   Isso nos ajudará a entender o que está dando errado ao converter a string
   para um slice de runes.

#### Execute o código

Desta vez, queremos executar apenas o teste que está falhando para inspecionar os logs. Para
fazer isso, usaremos `go test -run`.

Para executar uma entrada corpus específica dentro de FuzzXxx/testdata, você pode fornecer
{FuzzTestName}/{filename} para `-run`. Isso pode ser útil ao fazer debugging.
Neste caso, defina a flag `-run` igual ao hash exato do teste que está falhando.
Copie e cole o hash único do seu terminal;
ele será diferente do abaixo.

```
$ go test -run=FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0
input: "\x91"
runes: ['�']
input: "�"
runes: ['�']
--- FAIL: FuzzReverse (0.00s)
    --- FAIL: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00s)
        reverse_test.go:16: Number of runes: orig=1, rev=1, doubleRev=1
        reverse_test.go:18: Before: "\x91", after: "�"
FAIL
exit status 1
FAIL    example/fuzz    0.145s
```

Sabendo que a entrada é unicode inválido, vamos corrigir o erro em nossa função `Reverse`.

### Corrigir o erro

Para corrigir este problema, vamos retornar um erro se a entrada de `Reverse` não for
UTF-8 válido.

#### Escreva o código

1. No seu editor de texto, substitua a função `Reverse` existente pela
   seguinte.

   ```
   func Reverse(s string) (string, error) {
       if !utf8.ValidString(s) {
           return s, errors.New("input is not valid UTF-8")
       }
       r := []rune(s)
       for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r), nil
   }
   ```

   Esta mudança retornará um erro se a string de entrada contiver caracteres
   que não são UTF-8 válido.

1. Como a função Reverse agora retorna um erro, modifique a função `main` para
   descartar o valor de erro extra. Substitua a função `main` existente pela
   seguinte.

   ```
   func main() {
       input := "The quick brown fox jumped over the lazy dog"
       rev, revErr := Reverse(input)
       doubleRev, doubleRevErr := Reverse(rev)
       fmt.Printf("original: %q\n", input)
       fmt.Printf("reversed: %q, err: %v\n", rev, revErr)
       fmt.Printf("reversed again: %q, err: %v\n", doubleRev, doubleRevErr)
   }
   ```

    Estas chamadas a `Reverse` devem retornar um erro nil, já que a string de entrada
    é UTF-8 válido.

1. Você precisará importar os packages errors e unicode/utf8.
   A declaração import em main.go deve ficar assim.

   ```
   import (
       "errors"
       "fmt"
       "unicode/utf8"
   )
   ```

1. Modifique o arquivo reverse_test.go para verificar erros e pular o teste se
   erros forem gerados retornando.

   ```
   func FuzzReverse(f *testing.F) {
       testcases := []string {"Hello, world", " ", "!12345"}
       for _, tc := range testcases {
           f.Add(tc)  // Use f.Add to provide a seed corpus
       }
       f.Fuzz(func(t *testing.T, orig string) {
           rev, err1 := Reverse(orig)
           if err1 != nil {
               return
           }
           doubleRev, err2 := Reverse(rev)
           if err2 != nil {
                return
           }
           if orig != doubleRev {
               t.Errorf("Before: %q, after: %q", orig, doubleRev)
           }
           if utf8.ValidString(orig) && !utf8.ValidString(rev) {
               t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
           }
       })
   }
   ```

   Em vez de retornar, você também pode chamar `t.Skip()` para parar a execução
   daquela entrada fuzz.

#### Execute o código

1. Execute o teste usando go test

   ```
   $ go test
   PASS
   ok      example/fuzz  0.019s
   ```

2.  Faça fuzz com `go test -fuzz=Fuzz`, depois após alguns segundos terem passado, pare o
    fuzzing com `ctrl-C`. O fuzz test executará até encontrar uma entrada que falha a menos que você passe a flag `-fuzztime`. O padrão é executar para sempre se nenhuma
    falha ocorrer, e o processo pode ser interrompido com `ctrl-C`.

   ```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/38 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 38/38 completed, now fuzzing with 4 workers
   fuzz: elapsed: 3s, execs: 86342 (28778/sec), new interesting: 2 (total: 35)
   fuzz: elapsed: 6s, execs: 193490 (35714/sec), new interesting: 4 (total: 37)
   fuzz: elapsed: 9s, execs: 304390 (36961/sec), new interesting: 4 (total: 37)
   ...
   fuzz: elapsed: 3m45s, execs: 7246222 (32357/sec), new interesting: 8 (total: 41)
   ^Cfuzz: elapsed: 3m48s, execs: 7335316 (31648/sec), new interesting: 8 (total: 41)
   PASS
   ok      example/fuzz  228.000s
   ```

3. Faça fuzz com `go test -fuzz=Fuzz -fuzztime 30s` que fará fuzz por 30
   segundos antes de sair se nenhuma falha for encontrada.

   ```
   $ go test -fuzz=Fuzz -fuzztime 30s
   fuzz: elapsed: 0s, gathering baseline coverage: 0/5 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 5/5 completed, now fuzzing with 4 workers
   fuzz: elapsed: 3s, execs: 80290 (26763/sec), new interesting: 12 (total: 12)
   fuzz: elapsed: 6s, execs: 210803 (43501/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 9s, execs: 292882 (27360/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 12s, execs: 371872 (26329/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 15s, execs: 517169 (48433/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 18s, execs: 663276 (48699/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 21s, execs: 771698 (36143/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 24s, execs: 924768 (50990/sec), new interesting: 16 (total: 16)
   fuzz: elapsed: 27s, execs: 1082025 (52427/sec), new interesting: 17 (total: 17)
   fuzz: elapsed: 30s, execs: 1172817 (30281/sec), new interesting: 17 (total: 17)
   fuzz: elapsed: 31s, execs: 1172817 (0/sec), new interesting: 17 (total: 17)
   PASS
   ok      example/fuzz  31.025s
   ```

   Fuzzing passou!

   Além da flag `-fuzz`, várias novas flags foram adicionadas ao `go
   test` e podem ser vistas na [documentação](/security/fuzz/#custom-settings).

   Consulte [Go Fuzzing](/security/fuzz/#command-line-output) para mais
   informações sobre termos usados na saída do fuzzing. Por exemplo, "new interesting"
   refere-se a entradas que expandem o code coverage do fuzz test
   corpus existente. O número de entradas "new interesting" pode-se esperar que aumente
   bruscamente conforme o fuzzing começa, suba várias vezes conforme novos code paths são
   descobertos, e depois diminua com o tempo.

## Conclusão {#conclusion}

Muito bem! Você acabou de se apresentar ao fuzzing em Go.

O próximo passo é escolher uma função no seu código que você gostaria de fazer fuzz, e
experimentar! Se o fuzzing encontrar um bug no seu código, considere adicioná-lo ao
[trophy case](/wiki/Fuzzing-trophy-case).

Se você tiver qualquer problema ou tiver uma ideia para uma feature, [registre uma
issue](/issue/new/?&labels=fuzz).

Para discussão e feedback geral sobre a feature, você também pode participar
do [canal #fuzzing](https://gophers.slack.com/archives/CH5KV1AKE) no
Gophers Slack.

Confira a documentação em [go.dev/security/fuzz](/security/fuzz/#requirements) para
leitura adicional.

## Código completo

--- main.go ---

```
package main

import (
    "errors"
    "fmt"
    "unicode/utf8"
)

func main() {
    input := "The quick brown fox jumped over the lazy dog"
    rev, revErr := Reverse(input)
    doubleRev, doubleRevErr := Reverse(rev)
    fmt.Printf("original: %q\n", input)
    fmt.Printf("reversed: %q, err: %v\n", rev, revErr)
    fmt.Printf("reversed again: %q, err: %v\n", doubleRev, doubleRevErr)
}

func Reverse(s string) (string, error) {
    if !utf8.ValidString(s) {
        return s, errors.New("input is not valid UTF-8")
    }
    r := []rune(s)
    for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r), nil
}
```

--- reverse_test.go ---

```
package main

import (
    "testing"
    "unicode/utf8"
)

func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc) // Use f.Add to provide a seed corpus
    }
    f.Fuzz(func(t *testing.T, orig string) {
        rev, err1 := Reverse(orig)
        if err1 != nil {
            return
        }
        doubleRev, err2 := Reverse(rev)
        if err2 != nil {
            return
        }
        if orig != doubleRev {
            t.Errorf("Before: %q, after: %q", orig, doubleRev)
        }
        if utf8.ValidString(orig) && !utf8.ValidString(rev) {
            t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
        }
    })
}
```

[Back to top](#top)

---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Encontre e corrija dependências vulneráveis com govulncheck",
  "HideTOC": true,
  "Breadcrumb": true
}-->

Govulncheck é uma ferramenta de baixo ruído que ajuda você a encontrar e corrigir dependências vulneráveis em seus projetos Go. Ela faz isso escaneando as
dependências do seu projeto em busca de vulnerabilidades conhecidas e então identificando quaisquer chamadas diretas ou
indiretas a essas vulnerabilidades no seu código.

Neste tutorial, você aprenderá como usar govulncheck para escanear um programa simples em busca de vulnerabilidades. Você também aprenderá como priorizar e avaliar vulnerabilidades para que possa focar em corrigir as mais importantes
primeiro.

Para saber mais sobre govulncheck, veja a
[documentação do govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck),
e este [post no blog sobre gerenciamento de vulnerabilidades](/blog/vuln) para Go.
Também adoraríamos [ouvir seu feedback](/s/govulncheck-feedback).

## Pré-requisitos

- **Go.** Recomendamos usar a versão mais recente do Go para seguir este tutorial.
  (Para instruções de instalação, veja [Instalando Go](/doc/install).)
- **Um editor de código.** Qualquer editor que você tenha funcionará bem.
- **Um terminal de comando.** Go funciona bem usando qualquer terminal no Linux e Mac, e no PowerShell ou cmd no Windows.

O tutorial levará você através dos seguintes passos:

1. Criar um módulo Go de exemplo com uma dependência vulnerável
2. Instalar e executar govulncheck
3. Avaliar vulnerabilidades
4. Atualizar dependências vulneráveis

## Criar um módulo Go de exemplo com uma dependência vulnerável

**Passo 1.** Para começar, crie uma nova pasta chamada `vuln-tutorial` e inicialize um módulo Go.
(Se você é novo em módulos Go, confira [go.dev/doc/tutorial/create-module](/doc/tutorial/create-module).

Por exemplo, do seu diretório home, execute o seguinte:

```
$ mkdir vuln-tutorial
$ cd vuln-tutorial
$ go mod init vuln.tutorial
```

**Passo 2.** Crie um arquivo chamado `main.go` dentro da pasta `vuln-tutorial`, e copie
o seguinte código nele:

```
package main

import (
        "fmt"
        "os"

        "golang.org/x/text/language"
)

func main() {
        for _, arg := range os.Args[1:] {
                tag, err := language.Parse(arg)
                if err != nil {
                        fmt.Printf("%s: error: %v\n", arg, err)
                } else if tag == language.Und {
                        fmt.Printf("%s: undefined\n", arg)
                } else {
                        fmt.Printf("%s: tag %s\n", arg, tag)
                }
        }
}
```

Este programa de exemplo recebe uma lista de tags de idioma como argumentos de linha de comando
e imprime uma mensagem para cada tag indicando se ela foi analisada com sucesso,
a tag é indefinida, ou se houve um erro ao analisar a tag.

**Passo 3.** Execute `go mod tidy`, que populará o arquivo `go.mod` com todas as
dependências requeridas pelo código que você adicionou a `main.go` no passo anterior.

Da pasta `vuln-tutorial`, execute:

```
$ go mod tidy
```

Você deve ver esta saída:

```
go: finding module for package golang.org/x/text/language
go: downloading golang.org/x/text v0.9.0
go: found golang.org/x/text/language in golang.org/x/text v0.9.0
```

**Passo 4.** Abra seu arquivo `go.mod` para verificar que ele se parece com isto:

```
module vuln.tutorial

go 1.20

require golang.org/x/text v0.9.0
```

**Passo 5.** Faça downgrade da versão de `golang.org/x/text` para v0.3.5, que contém vulnerabilidades conhecidas. Execute:

```
$ go get golang.org/x/text@v0.3.5
```

Você deve ver esta saída:

```
go: downgraded golang.org/x/text v0.9.0 => v0.3.5
```

O arquivo `go.mod` agora deve ler:

```
module vuln.tutorial

go 1.20

require golang.org/x/text v0.3.5
```

Agora, vamos ver govulncheck em ação.


## Instalar e executar govulncheck

**Passo 6.** Instale govulncheck com o comando `go install`:

```
$ go install golang.org/x/vuln/cmd/govulncheck@latest
```

**Passo 7.** Da pasta que você quer analisar (neste caso, `vuln-tutorial`). Execute:

```
$ govulncheck ./...
```

Você deve ver esta saída:

```
govulncheck is an experimental tool. Share feedback at https://go.dev/s/govulncheck-feedback.

Using go1.20.3 and govulncheck@v0.0.0 with
vulnerability data from https://vuln.go.dev (last modified 2023-04-18 21:32:26 +0000 UTC).

Scanning your code and 46 packages across 1 dependent module for known vulnerabilities...
Your code is affected by 1 vulnerability from 1 module.

Vulnerability #1: GO-2021-0113
  Due to improper index calculation, an incorrectly formatted
  language tag can cause Parse to panic via an out of bounds read.
  If Parse is used to process untrusted user inputs, this may be
  used as a vector for a denial of service attack.

  More info: https://pkg.go.dev/vuln/GO-2021-0113

  Module: golang.org/x/text
    Found in: golang.org/x/text@v0.3.5
    Fixed in: golang.org/x/text@v0.3.7

    Call stacks in your code:
      main.go:12:29: vuln.tutorial.main calls golang.org/x/text/language.Parse

=== Informational ===

Found 1 vulnerability in packages that you import, but there are no call
stacks leading to the use of this vulnerability. You may not need to
take any action. See https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck
for details.

Vulnerability #1: GO-2022-1059
  An attacker may cause a denial of service by crafting an
  Accept-Language header which ParseAcceptLanguage will take
  significant time to parse.
  More info: https://pkg.go.dev/vuln/GO-2022-1059
  Found in: golang.org/x/text@v0.3.5
  Fixed in: golang.org/x/text@v0.3.8

```

### Interpretando a saída

<font size="2">  *Nota: Se você não está usando a versão mais recente do Go,
pode ver vulnerabilidades adicionais da biblioteca padrão. </font>

Nosso código é afetado por uma vulnerabilidade,
[GO-2021-0113](https://pkg.go.dev/vuln/GO-2021-0113), porque ele chama diretamente
a função `Parse` de `golang.org/x/text/language` em uma versão vulnerável
(v0.3.5).

Outra vulnerabilidade, [GO-2022-1059](https://pkg.go.dev/vuln/GO-2022-1059),
existe no módulo `golang.org/x/text` em v0.3.5.  No entanto, ela é relatada como
"Informational" porque nosso código nunca (direta ou indiretamente) chama nenhuma de
suas funções vulneráveis.

Agora, vamos avaliar as vulnerabilidades e determinar uma ação a tomar.

### Avaliar vulnerabilidades

a. Avalie vulnerabilidades.

Primeiro, leia a descrição da vulnerabilidade e determine se ela realmente
se aplica ao seu código e ao seu caso de uso. Se você precisar de mais informações, visite
o link "More info".

Baseado na descrição, a vulnerabilidade GO-2021-0113 pode causar um pânico quando
`Parse` é usado para processar entradas de usuário não confiáveis. Vamos supor que pretendemos
que nosso programa resista a entradas não confiáveis, e estamos preocupados com negação de
serviço, então a vulnerabilidade provavelmente se aplica.

GO-2022-1059 provavelmente não afeta nosso código, porque nosso código não chama
nenhuma função vulnerável desse relatório.

b. Decida uma ação.

Para mitigar GO-2021-0113, temos algumas opções:
- **Opção 1: Atualizar para uma versão corrigida.** Se há uma correção disponível,
  podemos remover uma dependência vulnerável atualizando para uma versão corrigida do módulo.
- **Opção 2: Parar de usar o(s) símbolo(s) vulnerável(is).** Poderíamos escolher
  remover todas as chamadas à função vulnerável no nosso código.
  Precisaríamos encontrar uma alternativa ou implementá-la nós mesmos.

Neste caso, uma correção está disponível, e a função `Parse` é integral ao nosso
programa. Vamos atualizar nossa dependência para a versão "fixed in", v0.3.7.

Decidimos despriorizar a correção da vulnerabilidade informacional,
GO-2022-1059, mas porque ela está no mesmo módulo que GO-2021-0113, e porque a versão corrigida para ela é v0.3.8, podemos
facilmente remover ambas ao mesmo tempo atualizando para v0.3.8.

## Atualizar dependências vulneráveis

Felizmente, atualizar dependências vulneráveis é bastante simples.

**Passo 8.** Atualize `golang.org/x/text` para v0.3.8:

```
$ go get golang.org/x/text@v0.3.8
```

Você deve ver esta saída:

```
go: upgraded golang.org/x/text v0.3.5 => v0.3.8
```

(Note que também poderíamos ter escolhido atualizar para `latest`, ou qualquer outra versão depois de v0.3.8).

**Passo 9.** Agora execute govulncheck novamente:

```
$ govulncheck ./...
```

Você agora verá esta saída:

```
govulncheck is an experimental tool. Share feedback at https://go.dev/s/govulncheck-feedback.

Using go1.20.3 and govulncheck@v0.0.0 with
vulnerability data from https://vuln.go.dev (last modified 2023-04-06 19:19:26 +0000 UTC).

Scanning your code and 46 packages across 1 dependent module for known vulnerabilities...
No vulnerabilities found.
```

Finalmente, govulncheck confirma que não há vulnerabilidades encontradas.

Ao escanear regularmente suas dependências com o comando govulncheck, você pode
proteger sua base de código identificando, priorizando e corrigindo
vulnerabilidades.

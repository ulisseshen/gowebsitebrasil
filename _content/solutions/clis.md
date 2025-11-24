---
ia-translated: true
title: "Command-line Interfaces (CLIs)"
linkTitle: "Command-line Interfaces (CLIs)"
description: "Com pacotes open source populares e uma biblioteca padrão robusta, use Go para criar CLIs rápidas e elegantes."
date: 2019-10-04T15:26:31-04:00
series: Use Cases
icon:
  file: clis-green.svg
  alt: CLI icon
iconDark:
  file: clis-white.svg
  alt: CLI icon
---

## Visão Geral {#overview .sectionHeading}

### Desenvolvedores de CLI preferem Go por portabilidade, desempenho e facilidade de criação

Command line interfaces (CLIs), ao contrário de interfaces gráficas de usuário (GUIs), são baseadas em texto. Aplicações de cloud e infraestrutura são primariamente baseadas em CLI devido à sua fácil automação e capacidades remotas.

## Principais benefícios {#key-benefits .sectionHeading}

### Aproveite tempos de compilação rápidos para construir programas que iniciam rapidamente e executam em qualquer sistema

Desenvolvedores de CLIs acham Go ideal para projetar suas aplicações. Go compila muito rapidamente em um único binário, funciona em várias plataformas com um estilo consistente e traz uma forte comunidade de desenvolvimento. A partir de um único laptop Windows ou Mac, desenvolvedores podem construir um programa Go para cada uma das dezenas de arquiteturas e sistemas operacionais que Go suporta em questão de segundos, nenhuma farm de build complicada é necessária. Nenhuma outra linguagem compilada pode ser construída de forma tão portável ou rápida. Aplicações Go são construídas em um único binário autocontido, tornando a instalação de aplicações Go trivial.

Especificamente, **programas escritos em Go executam em qualquer sistema sem requerer bibliotecas existentes, runtimes ou dependências**. E **programas escritos em Go têm um tempo de inicialização imediato**—similar a C ou C++ mas inatingível com outras linguagens de programação.

## Caso de Uso {#use-case .sectionHeading}

### Use Go para construir CLIs elegantes

{{backgroundquote `
  author: Steve Domino
  title: senior engineer and architect at Strala
  link: https://medium.com/@skdomino/writing-better-clis-one-snake-at-a-time-d22e50e60056
  quote: |
    I was tasked with building our CLI tool and found two really great projects, Cobra and Viper, which make building CLI's easy. Individually they are very powerful, very flexible and very good at what they do. But together they will help you show your next CLI who is boss!
`}}

{{backgroundquote `
  author: Francesc Campoy
  title: VP of product at DGraph Labs and producer of Just For Func videos
  link: https://www.youtube.com/watch?v=WvWPGVKLvR4
  quote: |
    Cobra is a great product to write small tools or even large ones. It's more of a framework than a library, because when you call the binary that would create a skeleton, then you would be adding code in between."
`}}

Ao desenvolver CLIs em Go, duas ferramentas são amplamente usadas: Cobra & Viper.

{{pkg "github.com/spf13/cobra" "Cobra"}} é tanto uma biblioteca para criar aplicações CLI modernas e poderosas quanto um programa para gerar aplicações e aplicações CLI em Go. Cobra alimenta a maioria das aplicações Go populares incluindo CoreOS, Delve, Docker, Dropbox, Git Lfs, Hugo, Kubernetes, e [muitas mais](https://pkg.go.dev/github.com/spf13/cobra?tab=importedby). Com ajuda de comando integrada, autocompletar e documentação "[ele] torna a documentação de cada comando realmente simples", diz [Alex Ellis](https://blog.alexellis.io/5-keys-to-a-killer-go-cli/), fundador do OpenFaaS.


{{pkg "github.com/spf13/viper" "Viper"}} é uma solução completa de configuração para aplicações Go, projetada para funcionar dentro de uma aplicação para lidar com necessidades e formatos de configuração. Cobra e Viper são projetados para trabalhar juntos.

Viper [suporta estruturas aninhadas](https://scene-si.org/2017/04/20/managing-configuration-with-viper/) na configuração, permitindo que desenvolvedores de CLI gerenciem a configuração de múltiplas partes de uma grande aplicação. Viper também fornece todas as ferramentas necessárias para construir facilmente aplicações twelve factor.

"Se você não quer poluir sua linha de comando, ou se está trabalhando com dados sensíveis que você não quer que apareçam no histórico, é uma boa ideia trabalhar com variáveis de ambiente. Para fazer isso, você pode usar Viper", [sugere Geudens](https://ordina-jworks.github.io/development/2018/10/20/make-your-own-cli-with-golang-and-cobra.html).

{{projects `
  - company: Comcast
    url: https://xfinity.com/
    logoSrc: comcast.svg
    logoSrcDark: comcast.svg
    desc: Comcast usa Go para um cliente CLI usado para publicar e assinar seus sites de alto tráfego. A empresa também suporta uma biblioteca cliente open source que é escrita em Go - projetada para trabalhar com Apache Pulsar.
    ctas:
      - text: Client library for Apache Pulsar
        url: https://github.com/Comcast/pulsar-client-go
      - text: Pulsar CLI Client
        url: https://github.com/Comcast/pulsar-client-go/blob/master/cli/main.go
  - company: GitHub
    url: https://github.com/
    logoSrc: github.svg
    logoSrcDark: github.svg
    desc: GitHub usa Go para uma ferramenta de linha de comando que facilita o trabalho com GitHub, envolvendo git para estendê-lo com recursos e comandos extras.
    ctas:
      - text: GitHub command-line tool
        url: https://github.com/cli/cli
  - company: Hugo
    url: https://gohugo.io/
    logoSrc: hugo.svg
    logoSrcDark: hugo.svg
    desc: Hugo é uma das aplicações CLI Go mais populares, alimentando milhares de sites, incluindo este. Uma razão para sua popularidade é sua facilidade de instalação graças ao Go. O autor do Hugo, Bjørn Erik Pedersen, escreve "O binário único elimina a maior parte da dor de instalação e upgrades."
    ctas:
      - text: Hugo Website
        url: https://gohugo.io/
  - company: Kubernetes
    url: https://kubernetes.com/
    logoSrc: kubernetes.svg
    logoSrcDark: kubernetes.svg
    desc: Kubernetes é uma das aplicações CLI Go mais populares. O criador do Kubernetes, Joe Beda, disse que para escrever Kubernetes, "Go foi a única escolha lógica". Chamando Go de "o ponto ideal" entre linguagens de baixo nível como C++ e linguagens de alto nível como Python.
    ctas:
      - text: Kubernetes + Go
        url: https://blog.gopheracademy.com/birthday-bash-2014/kubernetes-go-crazy-delicious/
  - company: MongoDB
    url: https://mongodb.com/
    logoSrc: mongodb.svg
    logoSrcDark: mongodb.svg
    desc: MongoDB escolheu implementar sua ferramenta CLI de Backup em Go citando a "sintaxe similar a C do Go, biblioteca padrão forte, a resolução de problemas de concorrência via goroutines, e distribuição multi-plataforma sem dor" como razões.
    ctas:
      - text: MongoDB Backup Service
        url: https://www.mongodb.com/blog/post/go-agent-go
  - company: Netflix
    url: https://netflix.com/
    logoSrc: netflix.svg
    logoSrcDark: netflix.svg
    desc: Netflix usa Go para construir a aplicação CLI ChaosMonkey, uma aplicação responsável por terminar aleatoriamente instâncias em produção para garantir que engenheiros implementem seus serviços para serem resilientes a falhas de instância.
    ctas:
      - text: Netflix Techblog Article
        url: https://medium.com/netflix-techblog/application-data-caching-using-ssds-5bf25df851ef
  - company: Stripe
    url: https://stripe.com/
    logoSrc: stripe.svg
    logoSrcDark: stripe.svg
    desc: Stripe usa Go para a Stripe CLI destinada a ajudar a construir, testar e gerenciar uma integração Stripe diretamente do terminal.
    ctas:
      - text: Stripe CLI
        url: https://github.com/stripe/stripe-cli
  - company: Uber
    url: https://uber.com/
    logoSrc: uber.svg
    logoSrcDark: uber.svg
    desc: Uber usa Go para várias ferramentas CLI, incluindo a API CLI para Jaeger, um sistema de rastreamento distribuído usado para monitorar sistemas distribuídos de microserviços.
    ctas:
      - text: CLI API for Jaeger
        url: https://www.jaegertracing.io/docs/1.14/cli/
`}}

## Comece Agora {#get-started .sectionHeading}

### Livros Go para criar CLIs

{{books `
  - title: Powerful Command-Line Applications in Go
    url: https://www.amazon.com/Powerful-Command-Line-Applications-Go-Maintainable/dp/168050696X
    thumbnail: /images/books/powerful-command-line-applications-in-go.jpg
  - title: Go in Action
    url: https://www.amazon.com/Go-Action-William-Kennedy/dp/1617291781
    thumbnail: /images/books/go-in-action.jpg
  - title: The Go Programming Language
    url: https://www.gopl.io/
    thumbnail: /images/learn/go-programming-language-book.png
  - title: Go Programming Blueprints
    url: https://github.com/matryer/goblueprints
    thumbnail: /images/learn/go-programming-blueprints.png
`}}

{{libraries `
  - title: CLI Libraries
    viewMoreUrl: https://pkg.go.dev/search?q=command%20line%20OR%20CLI
    items:
      - text: spf13/cobra
        url: https://pkg.go.dev/github.com/spf13/cobra?tab=overview
        desc: Uma biblioteca para criar aplicações CLI modernas e poderosas e um programa para gerar aplicações e aplicações CLI em Go
      - text: spf13/viper
        url: https://pkg.go.dev/github.com/spf13/viper?tab=overview
        desc: Uma solução completa de configuração para aplicações Go, projetada para funcionar dentro de uma aplicação para lidar com necessidades e formatos de configuração
      - text: urfave/cli
        url: https://pkg.go.dev/github.com/urfave/cli?tab=overview
        desc: Um framework minimalista para criar e organizar aplicações Go de linha de comando
      - text: delve
        url: https://pkg.go.dev/github.com/go-delve/delve?tab=overview
        desc: Uma ferramenta simples e poderosa construída para programadores acostumados a usar um debugger de nível de fonte em uma linguagem compilada
      - text: chzyer/readline
        url: https://pkg.go.dev/github.com/chzyer/readline?tab=overview
        desc: Uma implementação pura em Golang que fornece a maioria dos recursos do GNU Readline (sob licença MIT)
      - text: dixonwille/wmenu
        url: https://pkg.go.dev/github.com/dixonwille/wmenu?tab=overview
        desc: Uma estrutura de menu fácil de usar para aplicações CLI que solicita aos usuários fazer escolhas
      - text: spf13/pflag
        url: https://pkg.go.dev/github.com/spf13/pflag?tab=overview
        desc: Uma substituição drop-in para o pacote flag do Go, implementando flags estilo POSIX/GNU
      - text: golang/glog
        url: https://pkg.go.dev/github.com/golang/glog?tab=overview
        desc: Logs de execução nivelados para Go
      - text: go-prompt
        url: https://pkg.go.dev/github.com/c-bata/go-prompt?tab=overview
        desc: Uma biblioteca para construir prompts interativos poderosos, facilitando a construção de ferramentas de linha de comando multiplataforma usando Go.
`}}

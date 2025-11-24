---
ia-translated: true
title: "Go para Web Development"
linkTitle: "Web Development"
description: "Com desempenho de memória aprimorado e suporte para várias IDEs, Go alimenta aplicações web rápidas e escaláveis."
date: 2019-10-04T15:26:31-04:00
series: Use Cases
books:
icon:
  file: webdev-green.svg
  alt: web dev icon
iconDark:
  file: webdev-white.svg
  alt: web dev icon
---

## Visão Geral {#overview .sectionHeading}

### Go entrega velocidade, segurança e ferramentas amigáveis ao desenvolvedor para aplicações web

Go é projetado para permitir que desenvolvedores desenvolvam rapidamente aplicações web escaláveis e seguras. Go vem com um servidor web fácil de usar, seguro e performático e inclui sua própria biblioteca de template web. Go tem excelente suporte para todas as tecnologias mais recentes desde [HTTP/2](https://pkg.go.dev/net/http), até bancos de dados como [MySQL](https://pkg.go.dev/mod/github.com/go-sql-driver/mysql), [MongoDB](https://pkg.go.dev/mod/go.mongodb.org/mongo-driver) e [Elasticsearch](https://pkg.go.dev/mod/github.com/elastic/go-elasticsearch/v8), aos padrões de criptografia mais recentes incluindo [TLS 1.3](https://pkg.go.dev/crypto/tls). Aplicações web Go executam nativamente no [Google App Engine](https://cloud.google.com/appengine/) e [Google Cloud Run](https://cloud.google.com/run/) (para fácil escalamento) ou em qualquer ambiente, cloud ou sistema operacional graças à extrema portabilidade do Go.

## Principais Benefícios {#key-benefits .sectionHeading}

### Faça deploy em múltiplas plataformas em tempo recorde

Para empresas, Go é preferido por fornecer deployment rápido multiplataforma. Com suas goroutines, compilação nativa e o namespacing de pacote baseado em URI, o código Go compila em um único binário pequeno—com zero dependências—tornando-o muito rápido.

### Aproveite o desempenho pronto para uso do Go para escalar com facilidade

Tigran Bayburtsyan, Co-Fundador e CTO da Hexact Inc., resume cinco razões-chave pelas quais sua empresa mudou para Go:

-   **Compila em um único binário** — "Usando linkagem estática, Go na verdade combina todas as bibliotecas de dependência e módulos em um único arquivo binário baseado no tipo de SO e arquitetura."

-   **Sistema de tipo estático** — "Sistema de tipos é realmente importante para aplicações de larga escala."

-   **Desempenho** — "Go teve melhor desempenho por causa de seu modelo de concorrência e escalabilidade de CPU. Sempre que precisamos processar alguma requisição interna, fazemos isso com Goroutines separadas que são 10x mais baratas em recursos do que Threads Python."

-   **Não precisa de um framework web** — "Na maioria dos casos você realmente não precisa de nenhuma biblioteca de terceiros."

-   **Ótimo suporte de IDE e debugging** — "Depois de reescrever todos os projetos para Go, tivemos 64% menos código do que tínhamos anteriormente."


{{projects `
  - company: Caddy
    url: https://caddyserver.com/
    logoSrc: caddy.svg
    logoSrcDark: caddy.svg
    desc: Caddy 2 é um servidor web open source poderoso, pronto para empresas, com HTTPS automático escrito em Go. Caddy oferece maior segurança de memória do que servidores escritos em C. Uma pilha TLS reforçada alimentada pela biblioteca padrão Go serve uma porção significativa de todo o tráfego da Internet.
    ctas:
      - text: Caddy 2
        url: https://caddyserver.com/
  - company: Cloudflare
    url: https://www.cloudflare.com/en-gb/
    logoSrc: cloudflare-icon.svg
    logoSrcDark: cloudflare-icon.svg
    desc: Cloudflare acelera e protege milhões de sites, APIs, serviços SaaS e outras propriedades conectadas à Internet. "Go está no coração dos serviços da CloudFlare incluindo o manuseio de compressão para conexões HTTP de alta latência, toda a nossa infraestrutura DNS, SSL, testes de carga e muito mais."
    ctas:
      - text: Cloudflare and Go
        url: https://blog.cloudflare.com/what-weve-been-doing-with-go/
  - company: gov.uk
    url: https://gov.uk/
    logoSrc: govuk_light.svg
    logoSrcDark: govuk_dark.svg
    desc: A simplicidade e segurança da linguagem Go foram um bom ajuste para a infraestrutura HTTP do governo do Reino Unido, e alguns breves experimentos com o excelente pacote net/http convenceram os desenvolvedores web de que estavam no caminho certo. "Em particular, o modelo de concorrência do Go torna absurdamente fácil construir aplicações I/O-bound performáticas."
    ctas:
      - text: Building a new router for gov.uk
        url: https://technology.blog.gov.uk/2013/12/05/building-a-new-router-for-gov-uk/
      - text: Using Go in government
        url: https://technology.blog.gov.uk/2014/11/14/using-go-in-government/
  - company: Hugo
    url: https://gohugo.io/
    logoSrc: hugo.svg
    logoSrcDark: hugo.svg
    desc: Hugo é um motor de site rápido e moderno escrito em Go, e projetado para tornar a criação de sites divertida novamente. Sites construídos com Hugo são extremamente rápidos e seguros e podem ser hospedados em qualquer lugar sem nenhuma dependência.
    ctas:
      - text: Hugo
        url: https://gohugo.io/
  - company: Mattermost
    url: https://mattermost.com/
    logoSrc: mattermost_light.svg
    logoSrcDark: mattermost_dark.svg
    desc: Mattermost é uma plataforma de mensagens flexível e open source que permite colaboração segura em equipe. É escrita em Go e React.
    ctas:
      - text: Mattermost
        url: https://mattermost.com/
  - company: Medium
    url: https://medium.org/
    logoSrc: medium_light.svg
    logoSrcDark: medium_dark.svg
    desc: Medium usa Go para alimentar seu grafo social, seu servidor de imagens e vários serviços auxiliares. "Achamos Go muito fácil de construir, empacotar e fazer deploy. Gostamos da segurança de tipo sem a verbosidade e ajuste de JVM do Java."
    ctas:
      - text: Medium's Go Services
        url: https://medium.engineering/how-medium-goes-social-b7dbefa6d413
  - company: The Economist
    url: https://economist.com/
    logoSrc: economist.svg
    logoSrcDark: economist.svg
    desc: The Economist precisava de mais flexibilidade para entregar conteúdo a canais digitais cada vez mais diversos. Serviços escritos em Go foram um componente-chave do novo sistema que permitiria ao The Economist entregar serviços escaláveis e de alto desempenho e iterar rapidamente novos produtos. "No geral, foi determinado que Go era a linguagem melhor projetada para usabilidade e eficiência em um sistema distribuído baseado em cloud."
    ctas:
      - text: The Economist's Go microservices
        url: https://www.infoq.com/articles/golang-the-economist/
`}}

## Comece Agora {#get-started .sectionHeading}

### Livros Go sobre web development

{{books `
  - title: Web Development with Go
    url: https://www.amazon.com/Web-Development-Go-Building-Scalable-ebook/dp/B01JCOC6Z6
    thumbnail: /images/books/web-development-with-go.jpg
  - title: Go Web Programming
    url: https://www.amazon.com/Web-Programming-Sau-Sheong-Chang/dp/1617292567
    thumbnail: /images/books/go-web-programming.jpg
  - title: "Web Development Cookbook: Build full-stack web applications with Go"
    url: https://www.amazon.com/Web-Development-Cookbook-full-stack-applications-ebook/dp/B077TVQ28W
    thumbnail: /images/books/go-web-development-cookbook.jpg
  - title: Building RESTful Web services with Go
    url: https://www.amazon.com/Building-RESTful-Web-services-gracefully-ebook/dp/B072QB8KL1
    thumbnail: /images/books/building-restful-web-services-with-go.jpg
  - title: Mastering Go Web Services
    url: https://www.amazon.com/Mastering-Web-Services-Nathan-Kozyra-ebook/dp/B00W5GUKL6
    thumbnail: /images/books/mastering-go-web-services.jpg
`}}

{{libraries `
  - title: Web frameworks
    viewMoreUrl: https://pkg.go.dev/search?q=web+framework
    items:
      - text: Echo
        url: https://echo.labstack.com/
        desc: Um framework web Go de alta performance, extensível e minimalista
      - text: Flamingo
        url: https://www.flamingo.me/
        desc: Um framework open-source rápido baseado em Go com arquitetura limpa e escalável
      - text: Gin
        url: https://gin-gonic.com/
        desc: Um framework web escrito em Go, com uma API estilo martini.
      - text: Gorilla
        url: https://www.gorillatoolkit.org/
        desc: Um toolkit web para a linguagem de programação Go.
  - title: Routers
    viewMoreUrl: https://pkg.go.dev/search?q=http%20router
    items:
      - text: net/http
        url: https://pkg.go.dev/net/http
        desc: Um pacote HTTP da biblioteca padrão
      - text: julienschmidt/httprouter
        url: https://pkg.go.dev/github.com/julienschmidt/httprouter?tab=overview
        desc: Um roteador de requisições HTTP leve e de alta performance
      - text: gorilla/mux
        url: https://pkg.go.dev/github.com/gorilla/mux?tab=overview
        desc: Um poderoso roteador HTTP e correspondente de URL para construir servidores web Go com 🦍
      - text: Chi
        url: https://pkg.go.dev/github.com/go-chi/chi?tab=overview
        desc: Um roteador leve, idiomático e componível para construir serviços HTTP Go.
  - title: Template Engines
    viewMoreUrl: https://pkg.go.dev/search?q=templates
    items:
      - text: html/template
        url: https://pkg.go.dev/html/template
        desc: Um motor de template HTML da biblioteca padrão
      - text: flosch/pongo2
        url: https://pkg.go.dev/github.com/flosch/pongo2?tab=overview
        desc: Uma linguagem de template com sintaxe similar ao Django
  - title: Databases & Drivers
    viewMoreUrl: https://pkg.go.dev/search?q=database%20OR%20sql
    items:
      - text: database/sql
        url: https://pkg.go.dev/database/sql
        desc: Uma interface da biblioteca padrão com suporte a driver para MySQL, Postgres, Oracle, MS SQL, BigQuery e a maioria dos bancos de dados SQL
      - text: mongo-driver/mongo
        url: https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo?tab=overview
        desc: O driver suportado pelo MongoDB para Go
      - text: elastic/go-elasticsearch
        url: https://pkg.go.dev/github.com/elastic/go-elasticsearch/v8?tab=overview
        desc: Um cliente Elasticsearch para Go
      - text: GORM
        url: https://gorm.io/
        desc: Uma biblioteca ORM para Go
      - text: Bleve
        url: https://blevesearch.com/
        desc: Busca full-text e indexação para Go
      - text: CockroachDB
        url: https://www.cockroachlabs.com/
        desc: Uma evolução do banco de dados—arquitetado para a cloud para entregar SQL distribuído resiliente, consistente e em escala
  - title: Web Libraries
    viewMoreUrl: https://pkg.go.dev/search?q=web
    items:
      - text: markbates/goth
        url: https://pkg.go.dev/github.com/markbates/goth?tab=overview
        desc: Autenticação para aplicações web
      - text: jinzhu/gorm
        url: https://pkg.go.dev/github.com/jinzhu/gorm?tab=overview
        desc: Uma biblioteca ORM para Go
      - text: dgrijalva/jwt-go
        url: https://pkg.go.dev/github.com/dgrijalva/jwt-go?tab=overview
        desc: Uma implementação Go de json web tokens
  - title: Other Projects
    items:
      - text: gopherjs
        url: https://pkg.go.dev/github.com/gopherjs/gopherjs?tab=overview
        desc: Um compilador de Go para JavaScript permitindo que desenvolvedores escrevam código front-end em Go que será executado em todos os navegadores.
`}}

### Courses
* [Learn to Create Web Applications using Go](https://www.usegolang.com), um curso online pago

### Projects
*   {{pkg "github.com/gopherjs/gopherjs" "gopherjs"}}, um compilador de Go para JavaScript permitindo que desenvolvedores escrevam código front-end em Go que será executado em todos os navegadores.
*   [Hugo](https://gohugo.io/), o framework mais rápido do mundo para construir sites
*   [Mattermost](https://mattermost.com/), uma plataforma de mensagens flexível e open source
que permite colaboração segura em equipe
*   [Caddy](https://caddyserver.com/), um servidor web poderoso, pronto para empresas e open source com HTTPS automático escrito em Go

---
ia-translated: true
title: "Go para Cloud & Network Services"
linkTitle: "Cloud & Network Services"
description: "Com um forte ecossistema de ferramentas e APIs nos principais provedores de cloud, é mais fácil do que nunca construir serviços com Go."
date: 2019-10-04T15:26:31-04:00
series: Use Cases
icon:
  file: cloud-green.svg
  alt: cloud icon
iconDark:
  file: cloud-white.svg
  alt: cloud icon
---

## Visão Geral {#overview .sectionHeading}

<div class="UseCase-halfColumn">
    <h3>Go ajuda empresas a construir e escalar sistemas de computação em nuvem</h3>
    <p>À medida que aplicações e processamento migram para a cloud, concorrência se torna um grande problema. Sistemas de computação em cloud, por sua própria natureza, compartilham e escalam recursos. Coordenar o acesso a recursos compartilhados é um problema que impacta todas as aplicações processadas na nuvem, e requer linguagens de programação "explicitamente voltadas para desenvolver aplicações concorrentes altamente confiáveis".</p>
  </div>

{{quote `
  author: Ruchi Malik
  title: developer at Choozle
  link: https://builtin.com/software-engineering-perspectives/golang-advantages
  quote: |
    Go makes it very easy to scale as a company. This is very important because, as our engineering team grows, each service can be managed by a different unit.
`}}

## Principais Benefícios {#key-benefits .sectionHeading}

### Resolve o trade-off entre tempo do ciclo de desenvolvimento e desempenho do servidor

Go foi criado para atender exatamente essas necessidades de concorrência para aplicações escaladas, microservices e desenvolvimento em cloud. De fato, mais de 75% dos projetos na Cloud Native Computing Foundation são escritos em Go.

Go ajuda a reduzir a necessidade de fazer esse trade-off, com seus tempos de build rápidos que permitem desenvolvimento iterativo, menor utilização de memória e CPU. Servidores construídos com Go experimentam tempos de inicialização instantâneos e são mais baratos de executar em deployments pay-as-you-go e serverless.

### Enfrenta desafios com a cloud moderna, fornecendo APIs idiomáticas padrão

Go enfrenta muitos desafios que desenvolvedores encontram com a cloud moderna, fornecendo APIs idiomáticas padrão e concorrência integrada para aproveitar processadores multicore. A baixa latência do Go e o ajuste "no knob" tornam Go um ótimo equilíbrio entre desempenho e produtividade - concedendo às equipes de engenharia o poder de escolher e o poder de se mover.

## Caso de Uso {#use-case .sectionHeading}

### Use Go para Cloud Computing

Os pontos fortes do Go brilham quando se trata de construir serviços. Sua velocidade e suporte integrado para concorrência resultam em serviços rápidos e eficientes, enquanto tipagem estática, ferramentas robustas e ênfase em simplicidade e legibilidade ajudam a construir código confiável e sustentável.

Go tem um forte ecossistema que suporta desenvolvimento de serviços. A [biblioteca padrão](/pkg/) inclui pacotes para necessidades comuns como servidores e clientes HTTP, parsing JSON/XML, bancos de dados SQL e uma gama de funcionalidades de segurança/criptografia, enquanto o runtime Go inclui ferramentas para [detecção de race](/doc/articles/race_detector.html), [benchmarking](/pkg/testing/#hdr-Benchmarks)/profiling, geração de código e análise estática de código.

Os principais provedores de Cloud ([GCP](https://cloud.google.com/go/home), [AWS](https://aws.amazon.com/sdk-for-go/), [Azure](https://docs.microsoft.com/en-us/azure/go/)) têm APIs Go para seus serviços, e bibliotecas open source populares fornecem suporte para ferramentas de API ([Swagger](https://github.com/go-swagger/go-swagger)), transporte ([protocol buffers](https://github.com/golang/protobuf), [gRPC](https://grpc.io/docs/quickstart/go/)), monitoramento ([OpenCensus](https://godoc.org/go.opencensus.io)), Object-Relational Mapping ([gORM](https://gorm.io/)), e autenticação ([JWT](https://github.com/dgrijalva/jwt-go)). A comunidade open source também forneceu vários frameworks de serviço, incluindo [Go Kit](https://gokit.io/), [Go Micro](https://micro.mu/docs/go-micro.html), e [Gizmo](https://github.com/nytimes/gizmo), que podem ser uma ótima maneira de começar rapidamente.

### Ferramentas Go para Cloud Computing

{{toolsblurbs `
  - title: Docker
    url: https://www.docker.com/
    iconSrc: /images/logos/docker.svg
    paragraphs:
      - Docker é uma plataforma-as-a-service que entrega software em containers. Containers agrupam software, bibliotecas e arquivos de configuração, são hospedados por um Docker Engine, e são executados por um único kernel de sistema operacional (utilizando menos recursos do sistema do que máquinas virtuais).
      - Desenvolvedores de cloud usam Docker para gerenciar seu código Go e suportar múltiplas plataformas, pois Docker suporta o fluxo de trabalho de desenvolvimento e o processo de deployment.
  - title: Kubernetes
    url: https://kubernetes.io/
    iconSrc: /images/logos/kubernetes.svg
    paragraphs:
      - Kubernetes é um sistema de orquestração de containers open-source, escrito em Go, para automatizar o deployment de aplicações web. Aplicações web são frequentemente construídas usando containers (como notado acima) empacotados com suas dependências e configurações. Kubernetes ajuda a fazer deploy e gerenciar esses containers em escala. Programadores de cloud usam Kubernetes para construir, entregar e escalar aplicações containerizadas rapidamente—gerenciando a crescente complexidade através de APIs que controlam como os containers serão executados.
`}}

{{projects `
  - company: Google
    url: https://cloud.google.com/go
    logoSrc: google-cloud.svg
    logoSrcDark: google-cloud.svg
    desc: Google Cloud usa Go em todo o seu ecossistema de produtos e ferramentas, incluindo Kubernetes, gVisor, Knative, Istio e Anthos. Go é totalmente suportado no Google Cloud em todas as APIs e runtimes.
    ctas:
      - text: Go on Google Cloud Platform
        url: https://cloud.google.com/go
  - company: Capital One
    url: https://www.capitalone.com/
    logoSrc: capitalone_light.svg
    logoSrcDark: capitalone_dark.svg
    desc: Capital One usa Go para alimentar a Credit Offers API, um serviço crítico. A equipe de engenharia também está construindo sua arquitetura serverless com Go, citando a velocidade e simplicidade do Go, e mencionando que "[eles] não queriam ir serverless sem Go."
    ctas:
      - text: Credit Offers API
        url: https://medium.com/capital-one-tech/a-serverless-and-go-journey-credit-offers-api-74ef1f9fde7f
  - company: Dropbox
    url: https://www.dropbox.com/
    logoSrc: dropbox.svg
    logoSrcDark: dropbox.svg
    desc: Dropbox foi construído em Python, mas em 2013 decidiu migrar seus backends críticos de desempenho para Go. Hoje, a maior parte da infraestrutura da empresa é escrita em Go.
    ctas:
      - text: Dropbox libraries
        url: https://dropbox.tech/infrastructure/open-sourcing-our-go-libraries
  - company: Mercado Libre
    url: https://www.mercadolibre.com.ar/
    logoSrc: mercadolibre_light.svg
    logoSrcDark: mercadolibre_dark.svg
    desc: MercadoLibre usa Go para escalar sua plataforma de eCommerce. Go produz código eficiente que escala facilmente conforme o comércio online do MercadoLibre cresce. Go melhora sua produtividade enquanto simplifica e expande os serviços do MercadoLibre.
    ctas:
      - text: MercadoLibre & Go
        url: /solutions/mercadolibre
  - company: The New York Times
    url: https://www.nytimes.com/
    logoSrc: the-new-york-times-icon.svg
    logoSrcDark: the-new-york-times-icon.svg
    desc: The New York Times adotou Go "para construir melhores serviços de back-end". À medida que o uso de Go se expandiu dentro da empresa, eles sentiram a necessidade de criar um toolkit para "ajudar desenvolvedores a configurar e construir rapidamente APIs de microserviço e daemons pubsub", que eles disponibilizaram como open source.
    ctas:
      - text: NYTimes - Gizmo
        url: https://open.nytimes.com/introducing-gizmo-aa7ea463b208
      - text: Gizmo GitHub
        url: https://github.com/nytimes/gizmo
  - company: Twitch
    url: https://www.twitch.tv/
    logoSrc: twitch.svg
    logoSrcDark: twitch.svg
    desc: Twitch usa Go para alimentar muitos de seus sistemas mais ocupados que servem vídeo ao vivo e chat para milhões de usuários.
    ctas:
      - text: Go's march to low-latency GC
        url: https://blog.twitch.tv/en/2016/07/05/gos-march-to-low-latency-gc-a6fa96f06eb7/
  - company: Uber
    url: https://www.uber.com/
    logoSrc: uber_light.svg
    logoSrcDark: uber_dark.svg
    desc: Uber usa Go para alimentar vários de seus serviços críticos que impactam a experiência de milhões de motoristas e passageiros ao redor do mundo. Desde seu motor de análise em tempo real, AresDB, até seu microserviço para consultas Geo, Geofence, e seu agendador de recursos, Peloton.
    ctas:
      - text: AresDB
        url: https://eng.uber.com/aresdb/
      - text: Geofence
        url: https://eng.uber.com/go-geofence/
      - text: Peloton
        url:  https://eng.uber.com/open-sourcing-peloton/
`}}

## Comece Agora {#get-started .sectionHeading}

### Livros Go para computação em cloud

{{books `
  - title: Building Microservices with Go
    url: https://www.amazon.com/Building-Microservices-Go-efficient-microservices/dp/1786468662/
    thumbnail: /images/books/building-microservices-with-go.jpg
  - title: Hands-On Software Architecture with Golang
    url: https://www.amazon.com/dp/1788622596/ref=cm_sw_r_tw_dp_U_x_-aZWDbS8PD7R4
    thumbnail: /images/books/hands-on-software-architecture-with-golang.jpg
  - title: Building RESTful Web services with Go
    url: https://www.amazon.com/Building-RESTful-Web-services-gracefully-ebook/dp/B072QB8KL1
    thumbnail: /images/books/building-restful-web-services-with-go.jpg
  - title: Mastering Go Web Services
    url: https://www.amazon.com/Mastering-Web-Services-Nathan-Kozyra/dp/178398130X
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

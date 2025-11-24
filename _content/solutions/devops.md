---
ia-translated: true
title: "Development Operations & Site Reliability Engineering"
linkTitle: "Development Operations & Site Reliability Engineering"
description: "Com tempos de build rápidos, sintaxe enxuta, um formatador automático e gerador de documentação, Go é construído para suportar tanto DevOps quanto SRE."
date: 2019-10-03T17:16:43-04:00
series: Use Cases
books:
icon:
  file: devops-green.svg
  alt: ops icon
iconDark:
  file: devops-white.svg
  alt: ops icon
---

## Visão Geral {#overview .sectionHeading}

### Go ajuda empresas a automatizar e escalar

Equipes de Development Operations (DevOps) ajudam organizações de engenharia a automatizar tarefas e melhorar seu processo de integração contínua e entrega e deployment contínuos (CI/CD). DevOps pode derrubar silos de desenvolvimento e implementar ferramentas e automação para aprimorar o desenvolvimento, deployment e suporte de software.

Site Reliability Engineering (SRE) nasceu no Google para tornar os "sites de larga escala da empresa mais confiáveis, eficientes e escaláveis", [escreve Silvia Fressard](https://opensource.com/article/18/10/what-site-reliability-engineer), uma consultora DevOps independente. "E as práticas que eles desenvolveram responderam tão bem às necessidades do Google que outras grandes empresas de tecnologia, como Amazon e Netflix, também as adotaram." SRE requer uma mistura de habilidades de desenvolvimento e operações, e "[capacita desenvolvedores de software](https://stackify.com/site-reliability-engineering/) a possuir a operação diária contínua de suas aplicações em produção."

Go serve ambos os irmãos, DevOps e SRE, desde seus tempos de build rápidos e sintaxe enxuta até seu suporte a segurança e confiabilidade. Os recursos de concorrência e networking do Go também o tornam ideal para ferramentas que gerenciam deployment em cloud—suportando prontamente automação enquanto escala para velocidade e manutenibilidade de código à medida que a infraestrutura de desenvolvimento cresce ao longo do tempo.

Equipes de DevOps/SRE escrevem software que varia de pequenos scripts, a command-line interfaces (CLI), a serviços e automação complexos, e o conjunto de recursos do Go tem benefícios para cada situação.

## Principais Benefícios {#key-benefits .sectionHeading}

### Construa facilmente pequenos scripts com a biblioteca padrão robusta e tipagem estática do Go
Os tempos de build e inicialização rápidos do Go. A extensa biblioteca padrão do Go—incluindo pacotes para necessidades comuns como HTTP, file I/O, time, expressões regulares, exec e formatos JSON/CSV—permite que DevOps/SREs entrem direto na sua lógica de negócio. Além disso, o sistema de tipos estático do Go e o tratamento explícito de erros tornam até scripts pequenos mais robustos.

### Faça deploy rapidamente de CLIs com os tempos de build rápidos do Go
Todo site reliability engineer já escreveu scripts de "uso único" que se tornaram CLIs usadas por dezenas de outros engenheiros todos os dias. E pequenos scripts de automação de deployment se transformam em serviços de gerenciamento de rollout. Com Go, DevOps/SREs estão em uma ótima posição para ter sucesso quando o escopo do software inevitavelmente aumenta. Começar com Go coloca você em uma ótima posição para ter sucesso quando isso acontecer.

### Escale e mantenha aplicações maiores com o baixo footprint de memória do Go e gerador de documentação
O garbage collector do Go significa que equipes de DevOps/SRE não precisam se preocupar com gerenciamento de memória. E o gerador automático de documentação do Go (godoc) torna o código auto-documentável–reduzindo a sobrecarga de manutenção e estabelecendo as melhores práticas desde o início.

{{projects `
  - company: Docker
    url: https://docker.com/
    logoSrc: docker.svg
    logoSrcDark: docker.svg
    desc: Docker é um produto software-as-a-service (SaaS), escrito em Go, que equipes de DevOps/SRE aproveitam para "impulsionar automação segura e deployment em escala massiva", apoiando seus esforços de CI/CD.
    ctas:
      - text: Docker CI/CD
        url: https://www.docker.com/solutions/cicd
  - company: Drone
    url: https://github.com/drone
    logoSrc: drone.svg
    logoSrcDark: drone.svg
    desc: Drone é um sistema de Continuous Delivery construído em tecnologia de containers, escrito em Go, que usa um arquivo de configuração YAML simples, um superset de docker-compose, para definir e executar Pipelines dentro de containers Docker.
    ctas:
      - text: Drone
        url: https://github.com/drone
  - company: etcd
    url: https://github.com/etcd-io/etcd
    logoSrc: etcd.svg
    logoSrcDark: etcd.svg
    desc: etcd é uma datastore chave-valor distribuída fortemente consistente que fornece uma maneira confiável de armazenar dados que precisam ser acessados por um sistema distribuído ou cluster de máquinas, e é escrita em Go.
    ctas:
      - text: etcd
        url: https://github.com/etcd-io/etcd
  - company: IBM
    url: https://ibm.com/
    logoSrc: ibm.svg
    logoSrcDark: ibm.svg
    desc: As equipes de DevOps da IBM usam Go através de Docker e Kubernetes, além de outras ferramentas DevOps e CI/CD escritas em Go. A empresa também suporta conexão ao seu middleware de mensagens através de uma API específica para Go.
    ctas:
      - text: IBM Applications in Golang
        url: https://developer.ibm.com/messaging/2019/02/05/simplified-ibm-mq-applications-golang/
  - company: Netflix
    url: https://netflix.com/
    logoSrc: netflix.svg
    logoSrcDark: netflix.svg
    desc: Netflix usa Go para lidar com cache de dados em larga escala, com um serviço chamado Rend, que gerencia armazenamento replicado globalmente para dados de personalização.
    ctas:
      - text: Application Data Caching
        url: https://medium.com/netflix-techblog/application-data-caching-using-ssds-5bf25df851ef
      - text: Rend
        url: https://github.com/netflix/rend
  - company: Microsoft
    url: https://microsoft.com/
    logoSrc: microsoft_light.svg
    logoSrcDark: microsoft_dark.svg
    desc: Microsoft usa Go nos serviços Azure Red Hat OpenShift. Esta solução Microsoft fornece às equipes de DevOps clusters OpenShift para manter conformidade regulatória e focar no desenvolvimento de aplicações.
    ctas:
      - text: OpenShift
        url: https://azure.microsoft.com/en-us/services/openshift/
  - company: Terraform
    url: https://terraform.io/
    logoSrc: terraform-icon.svg
    logoSrcDark: terraform-icon.svg
    desc: Terraform é uma ferramenta para construir, alterar e versionar infraestrutura de forma segura e eficiente. Suporta vários provedores de cloud como AWS, IBM Cloud, GCP e Microsoft Azure - e é escrita em Go.
    ctas:
      - text: Terraform
        url: https://www.terraform.io/intro/index.html
  - company: Prometheus
    url: https://github.com/prometheus/prometheus
    logoSrc: prometheus.svg
    logoSrcDark: prometheus.svg
    desc: Prometheus é um toolkit open-source de monitoramento de sistemas e alertas originalmente construído na SoundCloud. A maioria dos componentes do Prometheus são escritos em Go, tornando-os fáceis de construir e fazer deploy como binários estáticos.
    ctas:
      - text: Prometheus
        url: https://github.com/prometheus/prometheus
  - company: YouTube
    url: https://youtube.com/
    logoSrc: youtube.svg
    logoSrcDark: youtube.svg
    desc: YouTube usa Go com Vitess (agora parte da PlanetScale), seu sistema de clustering de banco de dados para escalamento horizontal de MySQL através de sharding generalizado. Desde 2011 ele tem sido um componente central da infraestrutura de banco de dados do YouTube, e cresceu para abranger dezenas de milhares de nós MySQL.
    ctas:
      - text: Vitess
        url: https://github.com/vitessio/vitess
`}}

## Comece Agora {#get-started .sectionHeading}

### Livros Go sobre DevOps & SRE

{{books `
  - title: Go Programming for Network Operations
    url: https://www.amazon.com/Go-Programming-Network-Operations-Automation-ebook/dp/B07JKKN34L/ref=sr_1_16
    thumbnail: /images/books/go-programming-for-network-operations.jpg
  - title: Go Programming Blueprints
    url: https://github.com/matryer/goblueprints
    thumbnail: /images/learn/go-programming-blueprints.png
  - title: Go in Action
    url: https://www.amazon.com/Go-Action-William-Kennedy/dp/1617291781
    thumbnail: /images/books/go-in-action.jpg
  - title: The Go Programming Language
    url: https://www.gopl.io/
    thumbnail: /images/learn/go-programming-language-book.png
`}}

{{libraries `
  - title: Monitoring and tracing
    viewMoreUrl: https://pkg.go.dev/search?q=tracing
    items:
      - text: open-telemetry/opentelemetry-go
        url: https://pkg.go.dev/go.opentelemetry.io/otel
        desc: APIs e instrumentação vendor-neutral para monitoramento e rastreamento distribuído
      - text: jaegertracing/jaeger-client-go
        url: https://pkg.go.dev/github.com/jaegertracing/jaeger-client-go?tab=overview
        desc: Um sistema de rastreamento distribuído open source desenvolvido pela Uber
      - text: grafana/grafana
        url: https://pkg.go.dev/github.com/grafana/grafana?tab=overview
        desc: Uma plataforma open-source para monitoramento e observabilidade
      - text: istio/istio
        url: https://pkg.go.dev/github.com/istio/istio?tab=overview
        desc: Um service mesh open-source e plataforma integrável
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
  - title: Other projects
    items:
      - text: golang-migrate/migrate
        url: https://pkg.go.dev/github.com/golang-migrate/migrate?tab=overview
        desc: Uma ferramenta de migração de banco de dados escrita em Go
`}}

---
ia-translated: true
title: "American Express usa Go para Pagamentos & Recompensas"
company: American Express
logoSrc: american-express.svg
logoSrcDark: american-express.svg
heroImgSrc: go_amex_case_study_logo.png
carouselImgSrc: go_amex_case_study.png
date: 2019-12-19
series: Case Studies
quote: Go fornece à American Express a velocidade e escalabilidade que ela precisa tanto para suas redes de pagamento quanto de recompensas.
---

{{pullquote `
  author: Glen Balliet
  title: Diretor de Engenharia de plataformas de fidelidade
  company: American Express
  quote: |
    O que torna Go diferente de outras linguagens de programação é a carga cognitiva. Você pode fazer mais com menos código, o que torna mais fácil raciocinar e entender o código que você acaba escrevendo.

    A maioria do código Go acaba parecendo bastante similar, então, mesmo se você estiver trabalhando com uma base de código completamente nova, você pode começar a trabalhar rapidamente.
`}}

## Go melhora microsserviços e acelera a produtividade

Fundada em 1850, a American Express é uma empresa de pagamentos globalmente integrada que oferece produtos de cartões de crédito e cobrança, aquisição e processamento de comerciantes, serviços de rede e serviços relacionados a viagens.

Os sistemas de processamento de pagamentos da American Express foram desenvolvidos ao longo de sua longa história e foram atualizados através de múltiplas evoluções arquiteturais. Acima de tudo em qualquer atualização, o processamento de pagamentos precisa ser rápido, especialmente em volumes de transação muito grandes, com resiliência construída em sistemas que devem estar todos em conformidade com padrões de segurança e regulamentares. Com Go, a American Express ganha a velocidade e escalabilidade que precisa tanto para suas redes de pagamento quanto de recompensas.

### Modernizando os sistemas da American Express

A American Express entende que o cenário de linguagens de programação está mudando drasticamente. Os sistemas existentes da empresa foram construídos especificamente para alta concorrência e baixa latência, mas sabendo que esses sistemas seriam re-plataformados em um futuro próximo. A equipe da plataforma de pagamentos decidiu tirar um tempo para identificar quais linguagens eram ideais para as necessidades em evolução da American Express.

As equipes de plataformas de pagamentos e recompensas da American Express estavam entre as primeiras a começar a avaliar Go. Essas equipes estavam focadas em microsserviços, roteamento de transações e casos de uso de balanceamento de carga, e elas precisavam modernizar sua arquitetura. Muitos desenvolvedores da American Express estavam familiarizados com as capacidades da linguagem e queriam pilotar Go para suas aplicações de alta concorrência e baixa latência (como balanceadores de carga transacionais customizados). Com esse objetivo em mente, as equipes começaram a fazer lobby com a liderança sênior para implantar Go na plataforma de pagamentos da American Express.

"Queríamos encontrar a linguagem ideal para escrever aplicações rápidas e eficientes para processamento de pagamentos", diz Benjamin Cane, vice-presidente e engenheiro principal da American Express. "Para isso, iniciamos uma competição interna de linguagens de programação com o objetivo de ver qual linguagem melhor se adequava às nossas necessidades de design e desempenho."

### Comparando linguagens

Para sua avaliação, a equipe de Cane escolheu construir um microsserviço em quatro linguagens de programação diferentes. Eles então compararam as quatro linguagens em velocidade/desempenho, ferramentas, testes e facilidade de desenvolvimento.

Para o serviço, eles decidiram por um conversor ISO8583 para JSON. ISO8583 é um padrão internacional para transações financeiras, e é comumente usado dentro da rede de pagamentos da American Express. Para as linguagens de programação, eles escolheram comparar C++, Go, Java e Node.js. Com exceção de Go, todas essas linguagens já estavam em uso dentro da American Express.

De uma perspectiva de velocidade, Go alcançou o segundo melhor desempenho com 140.000 requisições por segundo. Go mostrou que se destaca quando usado para microsserviços de backend.

Embora Go possa não ter sido a linguagem mais rápida testada, seu poderoso ferramental ajudou a reforçar seus resultados gerais. O framework de testes integrado de Go, capacidades de profiling e ferramentas de benchmarking impressionaram a equipe. "É fácil escrever testes eficazes em Go", diz Cane. "As funcionalidades de benchmarking e profiling tornam simples ajustar nossa aplicação. Aliado aos seus tempos rápidos de compilação, Go torna fácil escrever código bem testado e otimizado."

Finalmente, Go foi selecionado pela equipe como a linguagem preferida para construir microsserviços de alto desempenho. O ferramental, frameworks de testes, desempenho e simplicidade da linguagem foram todos contribuidores chave.

### Go para infraestrutura

"Muitos de nossos serviços estão rodando em containers Docker dentro de nossa plataforma de nuvem interna baseada em Kubernetes", diz Cane. Kubernetes é um sistema de orquestração de containers open-source escrito em Go. Ele fornece clusters de hosts para executar cargas de trabalho baseadas em containers, mais notavelmente containers Docker. Docker é um produto de software, também escrito em Go, que usa virtualização em nível de sistema operacional para fornecer runtimes de software portáteis chamados containers.

A American Express também coleta métricas de aplicação via Prometheus, um toolkit de monitoramento e alertas open-source escrito em Go. Prometheus coleta e agrega eventos e métricas em tempo real para monitoramento e alertas.

Esse triunvirato de soluções Go—Kubernetes, Docker e Prometheus—tem ajudado a modernizar a infraestrutura da American Express.

### Melhorando o desempenho com Go

Hoje, dezenas de desenvolvedores estão programando com Go na American Express, com a maioria trabalhando em plataformas projetadas para alta disponibilidade e desempenho.

"Ferramental sempre foi uma área crítica de necessidade para nossa base de código legado", diz Cane. "Descobrimos que Go tem excelente ferramental, além de frameworks integrados de testes, benchmarking e profiling. É fácil escrever aplicações eficientes e resilientes."

{{backgroundquote `
  author: Benjamin Cane
  title: Vice-Presidente e Engenheiro Principal
  company: American Express
  quote: |
    Depois de trabalhar com Go, a maioria de nossos desenvolvedores não quer voltar para outras linguagens.
`}}

A American Express está apenas começando a ver os benefícios de Go. Por exemplo, Go foi projetado desde o início com concorrência em mente – usando "goroutines" leves em vez de threads de sistema operacional mais pesadas – tornando prático criar centenas de milhares de goroutines no mesmo espaço de endereço. Usando goroutines, a American Express viu números de desempenho melhorados em seu processamento de transações em tempo real.

A coleta de lixo (garbage collection) de Go também é uma grande melhoria em relação a outras linguagens, tanto em termos de desempenho quanto facilidade de desenvolvimento. "Vimos resultados muito melhores de coleta de lixo em Go do que em outras linguagens, e coleta de lixo para processamento de transações em tempo real é muito importante", diz Cane. "Ajustar a coleta de lixo em outras linguagens pode ser muito complicado. Com Go você não ajusta nada."

Para saber mais, leia ["Choosing Go at American Express"](https://americanexpress.io/choosing-go/) que vai mais a fundo sobre a adoção de Go pela American Express.

### Começando sua empresa com Go

Assim como a American Express está usando Go para modernizar suas redes de pagamento e recompensas, dezenas de outras grandes empresas também estão adotando Go.

Existem mais de um milhão de desenvolvedores usando Go em todo o mundo—abrangendo bancos e comércio, jogos e mídia, tecnologia e outras indústrias, em empresas tão diversas quanto [PayPal](/solutions/paypal), [Mercado Libre](/solutions/mercadolibre), Capital One, Dropbox, IBM, Mercado Libre, Monzo, New York Times, Salesforce, Square, Target, Twitch, Uber e, é claro, Google.

Para saber mais sobre como Go pode ajudar sua empresa a construir software confiável e escalável como faz na American Express, visite [go.dev](/) hoje.

---
ia-translated: true
title: PayPal Adota Go para Modernizar e Escalar
date: 2020-06-01
company: PayPal
logoSrc: paypal.svg
logoSrcDark: paypal.svg
heroImgSrc: go_paypal_case_study_logo.png
carouselImgSrc: go_paypal_case_study.png
series: Case Studies
quote: O valor do Go em produzir código limpo e eficiente que escala prontamente conforme a implantação de software cresce tornou a linguagem uma escolha forte para apoiar os objetivos do PayPal.
---

{{pullquote `
  author: Bala Natarajan
  title: <span class="NoWrapSpan">Sr. Director of Engineering,</span>&nbsp;<span class="NoWrapSpan">Developer Experience</span>
  company: PayPal
  quote: |
    Como nosso NoSQL e proxy de DB usavam bastante detalhes do sistema em um modo multi-threaded, o código ficou complexo gerenciando as diferentes condições. Dado que Go fornece channels e rotinas para lidar com complexidade, conseguimos estruturar o código para atender nossos requisitos.
`}}

## Nova infraestrutura de código construída em Go

O PayPal foi criado para democratizar serviços financeiros e capacitar pessoas e empresas a se juntarem e prosperarem na economia global. Central para esse esforço está a Plataforma de Pagamentos do PayPal, que usa uma combinação de tecnologias proprietárias e de terceiros para facilitar de forma eficiente e segura transações entre milhões de comerciantes e consumidores em todo o mundo. À medida que a Plataforma de Pagamentos cresceu e se tornou mais complicada, o PayPal buscou modernizar seus sistemas e reduzir o tempo de lançamento de novas aplicações.

O valor do Go em produzir código limpo e eficiente que escala prontamente conforme a implantação de software cresce tornou a linguagem uma escolha forte para apoiar os objetivos do PayPal.

Central para a Plataforma de Processamento de Pagamentos está um banco de dados NoSQL proprietário que o PayPal havia desenvolvido em C++. A complexidade do código, no entanto, estava substancialmente diminuindo a capacidade de seus desenvolvedores de evoluir a plataforma. Os layouts de código simples do Go, goroutines (threads leves de execução) e channels (que servem como os canais que conectam goroutines concorrentes), fizeram do Go uma escolha natural para a equipe de desenvolvimento NoSQL simplificar e modernizar a plataforma.

Como prova de conceito, uma equipe de desenvolvimento passou seis meses aprendendo Go e reimplementando o sistema NoSQL do zero em Go, durante o qual eles também forneceram insights sobre como Go poderia ser implementado mais amplamente no PayPal. Até hoje, trinta por cento dos clusters foram migrados para usar o novo banco de dados NoSQL.


## Usando Go para simplificar em escala

À medida que a plataforma do PayPal se torna mais intricada, Go fornece uma maneira de simplificar prontamente a complexidade de criar e executar software em escala. A linguagem fornece ao PayPal ótimas bibliotecas e ferramentas rápidas, além de concorrência, coleta de lixo e segurança de tipos.

Com Go, o PayPal permite que seus desenvolvedores gastem mais tempo olhando código e pensando estrategicamente, liberando-os do ruído do desenvolvimento em C++ e Java.

Após o sucesso deste sistema NoSQL recém-reescrito, mais equipes de plataforma e conteúdo dentro do PayPal começaram a adotar Go. A equipe atual de Natarajan é responsável pelos pipelines de build, teste e release do PayPal—todos construídos em Go. A empresa tem uma grande fazenda de build e teste que é completamente gerenciada usando infraestrutura Go para apoiar builds-as-a-service (e tests-as-a-service) para desenvolvedores em toda a empresa.

  <img
    loading="lazy"
    width="607"
    height="289"
    class=""
    alt="Go gopher factory"
    src="/images/gophers/factory.png">

## Modernizando sistemas do PayPal com Go

Com as capacidades de computação distribuída exigidas pelo PayPal, Go foi a linguagem certa para atualizar seus sistemas. O PayPal precisava de programação que fosse concurrent e paralela, compilada para alta performance e altamente portável, e que trouxesse aos desenvolvedores os benefícios de uma arquitetura open-source modular e componível—Go entregou tudo isso e mais para ajudar o PayPal a modernizar seus sistemas.

Segurança e suportabilidade são questões-chave no PayPal, e os pipelines operacionais da empresa são cada vez mais dominados por Go porque a limpeza e modularidade da linguagem os ajudam a alcançar esses objetivos. A implantação de Go pelo PayPal gera uma plataforma de criatividade para desenvolvedores, permitindo-lhes produzir software simples, eficiente e confiável em escala para os mercados mundiais do PayPal.

À medida que o PayPal continua a modernizar sua infraestrutura de rede definida por software (SDN) com Go, eles estão vendo benefícios de performance além de código mais manutenível. Por exemplo, Go agora alimenta roteadores, balanceadores de carga e um número crescente de sistemas de produção.

{{backgroundquote `
  author: Bala Natarajan
  title: Sr. Director of Engineering
  quote: |
    Em nossos ambientes rigidamente gerenciados onde executamos código Go, vimos uma redução de CPU de aproximadamente dez por cento com código mais limpo e manutenível.
`}}

## Go aumenta a produtividade dos desenvolvedores

Como uma operação global, o PayPal precisa que suas equipes de desenvolvimento sejam eficazes em gerenciar dois tipos de escala: escala de produção, especialmente sistemas concorrentes interagindo com muitos outros servidores (como serviços em nuvem); e escala de desenvolvimento, especialmente grandes bases de código desenvolvidas por muitos programadores em coordenação (como desenvolvimento open-source)

O PayPal aproveita Go para abordar essas questões de escala. Os desenvolvedores da empresa se beneficiam da capacidade do Go de combinar a facilidade de programação de uma linguagem interpretada, dinamicamente tipada, com a eficiência e segurança de uma linguagem estaticamente tipada e compilada. À medida que o PayPal moderniza seu sistema, o suporte para computação em rede e multicore é crítico. Go não apenas entrega tal suporte, mas entrega rapidamente—leva no máximo alguns segundos para compilar um grande executável em um único computador.

Atualmente existem mais de 100 desenvolvedores Go no PayPal, e futuros desenvolvedores que escolherem adotar Go terão mais facilidade em obter a aprovação da linguagem graças às muitas implementações bem-sucedidas já em produção na empresa.

Mais importante, os desenvolvedores do PayPal aumentaram sua produtividade com Go. Os mecanismos de concorrência do Go tornaram fácil escrever programas que tiram o máximo proveito das máquinas multicore e em rede do PayPal. Desenvolvedores usando Go também se beneficiam do fato de que ele compila rapidamente para código de máquina e seus aplicativos ganham a conveniência de coleta de lixo e o poder de reflexão em tempo de execução.

## Acelerando o tempo de lançamento do PayPal

As linguagens de primeira classe no PayPal hoje são Java e Node, com Go usado principalmente como uma linguagem de infraestrutura. Embora Go possa nunca substituir Node.js para certas aplicações, Natarajan está se esforçando para tornar Go uma linguagem de primeira classe no PayPal.

Através de seus esforços, o PayPal também está avaliando a mudança para o Google Kubernetes Engine (GKE) para acelerar o tempo de lançamento de seus novos produtos. O GKE é um ambiente gerenciado e pronto para produção para implantar aplicações em contêineres, e traz as mais recentes inovações do Google em produtividade de desenvolvedores, operações automatizadas e flexibilidade open source.

Para o PayPal, implantar no GKE permitiria desenvolvimento e iteração rápidos, facilitando a implantação, atualização e gerenciamento de suas aplicações e serviços. Além disso, o PayPal achará mais fácil executar Machine Learning, GPU de Uso Geral, Computação de Alto Desempenho e outras cargas de trabalho que se beneficiam de aceleradores de hardware especializados suportados pelo GKE.

Mais importante para o PayPal, a combinação de desenvolvimento Go e o GKE permite que a empresa escale sem esforço para atender à demanda, já que o autoscaling do Kubernetes permitirá ao PayPal lidar com o aumento da demanda dos usuários por serviços—mantendo-os disponíveis quando mais importa, e então reduzir nos períodos de baixa demanda para economizar dinheiro.


## Começando sua empresa com Go

A história do PayPal não é única; dezenas de outras grandes empresas estão descobrindo como Go pode ajudá-las a entregar software confiável mais rapidamente. Existem mais de um milhão de desenvolvedores usando Go em todo o mundo—abrangendo bancos e comércio, jogos e mídia, tecnologia e outras indústrias, em empresas tão diversas quanto [American Express](/solutions/americanexpress), [Mercado Libre](/solutions/mercadolibre), Capital One, Dropbox, IBM, Monzo, New York Times, Salesforce, Square, Target, Twitch, Uber e, é claro, Google.

Para saber mais sobre como Go pode ajudar sua empresa a construir software confiável e escalável como faz no PayPal, visite [go.dev](/) hoje.

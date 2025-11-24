---
ia-translated: true
title: 'Usando Go no Google'
date: 2020-08-27
company: Google
logoSrc: google.svg
logoSrcDark: google.svg
heroImgSrc: go_core_data_case_study.png
carouselImgSrc: go_google_case_study_carousel.png
series: Case Studies
type: solutions
description: |-
  Google é uma empresa de tecnologia cuja missão é organizar as informações do mundo
  e torná-las universalmente acessíveis e úteis.

  Go foi criado no Google em 2007 para melhorar a produtividade da programação em uma
  era de máquinas em rede multi-core e grandes bases de código. Hoje, mais de 10
  anos desde seu anúncio público em 2009, o uso de Go dentro do Google cresceu
  tremendamente.
quote: Go foi criado no Google em 2007, e desde então, equipes de engenharia
  de todo o Google adotaram Go para construir produtos e serviços em escala massiva.

---

{{pullquote `
  author: Rob Pike
  quote: |
    Go começou em setembro de 2007 quando Robert Griesemer, Ken Thompson e eu começamos
    a discutir uma nova linguagem para abordar os desafios de engenharia que nós e nossos
    colegas no Google estávamos enfrentando em nosso trabalho diário.

    Quando lançamos Go ao público pela primeira vez em novembro de 2009, não sabíamos se a
    linguagem seria amplamente adotada ou se poderia influenciar futuras linguagens.
    Olhando de 2020, Go teve sucesso de ambas as formas: é amplamente usada tanto
    dentro quanto fora do Google, e suas abordagens para concorrência de rede e
    engenharia de software tiveram um efeito notável em outras linguagens e suas
    ferramentas.

    Go se revelou ter um alcance muito mais amplo do que jamais esperávamos. Seu
    crescimento na indústria tem sido fenomenal, e impulsionou muitos projetos no
    Google.
`}}

As histórias a seguir são uma pequena amostra das muitas maneiras que Go é usado no Google.

### Como a Equipe Core Data Solutions do Google Usa Go

A missão do Google é "organizar as informações do mundo e torná-las universalmente
acessíveis e úteis." Uma das equipes responsáveis por organizar essas
informações é a equipe Core Data Solutions do Google. A equipe, entre outras coisas,
mantém serviços para indexar páginas da web em todo o mundo. Esses serviços de indexação web
ajudam a suportar produtos como o Google Search mantendo os resultados de pesquisa
atualizados e abrangentes, e são escritos em Go.

[Saiba mais](/solutions/google/coredata/)

---

### Serviço de Otimização de Conteúdo do Chrome Roda em Go

Quando você pensa no produto Chrome, provavelmente pensa apenas no navegador instalado pelo usuário. Mas nos bastidores, o Chrome tem uma extensa frota de backends. Entre eles está o serviço Chrome Optimization Guide. Este serviço forma uma base importante para a estratégia de experiência do usuário do Chrome, operando no caminho crítico para os usuários, e é implementado em Go.

[Saiba mais](/solutions/google/chrome/)

---

### Como a Equipe Firebase Hosting Escalou Com Go

A equipe Firebase Hosting fornece serviços de hospedagem web estática para clientes do Google Cloud. Eles fornecem um host web estático que fica atrás de uma rede de entrega de conteúdo global, e oferecem aos usuários ferramentas fáceis de usar. A equipe também desenvolve recursos que vão desde o upload de arquivos do site até o registro de domínios e rastreamento de uso.

[Saiba mais](/solutions/google/firebase/)

---

### Atuando na Produção do Google: Como a Equipe de Site Reliability Engineering do Google Usa Go

O Google executa um pequeno número de serviços muito grandes. Esses serviços são alimentados por uma infraestrutura global cobrindo tudo o que é necessário: sistemas de armazenamento, balanceadores de carga, rede, logging, monitoramento e muito mais. No entanto, não é um sistema estático - não pode ser. A arquitetura evolui, novos produtos e ideias são criados, novas versões devem ser implantadas, configurações enviadas, schemas de banco de dados atualizados e mais. Acabamos implantando mudanças em nossos sistemas dezenas de vezes por segundo.

[Saiba mais](/solutions/google/sitereliability/)

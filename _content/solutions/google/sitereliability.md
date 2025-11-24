---
ia-translated: true
title: "Atuando na Produção do Google: Como a Equipe de Site Reliability Engineering do Google Usa Go"
company: Google Site Reliability Engineering (SRE)
logoSrc: sitereliability.svg
logoSrcDark: sitereliability.svg
heroImgSrc: go_sitereliability_case_study.png
series: Case Studies
quote: |
  A equipe de Site Reliability Engineering do Google tem a missão de proteger, prover e progredir o software e os sistemas por trás de todos os serviços públicos do Google — Google Search, Ads, Gmail, Android, YouTube e App Engine, para citar apenas alguns — com um olhar sempre vigilante sobre sua disponibilidade, latência, desempenho e capacidade.

  Eles compartilharam sua experiência construindo sistemas centrais de gerenciamento de produção com Go, vindo de experiência com Python e C++.
authors:
  - Pierre Palatin, Site Reliability Engineer
---

O Google executa um pequeno número de serviços muito grandes. Esses serviços são alimentados
por uma infraestrutura global cobrindo tudo o que um desenvolvedor precisa: sistemas de
armazenamento, balanceadores de carga, rede, logging, monitoramento e muito mais.
No entanto, não é um sistema estático - não pode ser. A arquitetura evolui,
novos produtos e ideias são criados, novas versões devem ser implantadas, configurações
enviadas, schemas de banco de dados atualizados e mais. Acabamos implantando mudanças em nossos
sistemas dezenas de vezes por segundo.

Devido a essa escala e necessidade crítica de confiabilidade, o Google foi pioneiro em Site
Reliability Engineering (SRE), uma função que muitas outras empresas adotaram desde então.
"SRE é o que você obtém quando trata operações como se fosse um problema de software.
Nossa missão é proteger, prover e progredir o software e os sistemas
por trás de todos os serviços públicos do Google com um olhar sempre vigilante sobre sua
disponibilidade, latência, desempenho e capacidade."
— [Site Reliability Engineering (SRE)](https://sre.google/).

{{backgroundquote `
  quote: |
    Go prometia um ponto ideal entre desempenho e legibilidade que nenhuma das
    outras linguagens [Python e C++] era capaz de oferecer.
`}}

Em 2013-2014, a equipe SRE do Google percebeu que nossa abordagem para gerenciamento de produção
não estava mais sendo suficiente de muitas maneiras. Tínhamos avançado muito além de
scripts shell, mas nossa escala tinha tantas partes móveis e complexidades que uma
nova abordagem era necessária. Determinamos que precisávamos nos mover em direção a um
modelo declarativo de nossa produção, chamado "Prodspec", conduzindo um plano de
controle dedicado, chamado "Annealing".

Quando começamos esses projetos, Go estava apenas se tornando uma opção viável para
serviços críticos no Google. A maioria dos engenheiros estava mais familiarizada com Python
e C++, qualquer um dos quais teria sido uma escolha válida. No entanto, Go
capturou nosso interesse. O apelo da novidade foi certamente um fator, é
claro. Mas, mais importante, Go prometia um ponto ideal entre desempenho
e legibilidade que nenhuma das outras linguagens era capaz de oferecer. Começamos
um pequeno experimento com Go para algumas partes iniciais do Annealing e
Prodspec. À medida que os projetos progrediram, essas partes iniciais escritas em Go se encontraram
no núcleo. Estávamos felizes com Go - sua simplicidade cresceu em nós, o
desempenho estava lá, e primitivas de concorrência teriam sido difíceis de
substituir.

{{backgroundquote `
  quote: |
    Agora a maior parte da produção do Google é gerenciada e mantida por nossos sistemas
    escritos em Go.
`}}

Em nenhum momento houve um mandato ou requisito para usar Go, mas não tínhamos
desejo de retornar ao Python ou C++. Go cresceu organicamente no Annealing e
Prodspec. Foi a escolha certa, e assim agora é nossa linguagem de escolha.
Agora a maior parte da produção do Google é gerenciada e mantida por nossos sistemas
escritos em Go.

O poder de ter uma linguagem simples nesses projetos é difícil de exagerar.
Houve casos em que algum recurso estava de fato faltando, como a
capacidade de impor no código que alguma estrutura complexa não deveria ser
mutada. Mas para cada um desses casos, sem dúvida houve dezenas ou
centenas de casos em que a simplicidade ajudou.

{{backgroundquote `
  quote: |
    A simplicidade do Go significa que o código é fácil de seguir, seja para detectar
    bugs durante a revisão ou ao tentar determinar exatamente o que aconteceu durante uma
    interrupção de serviço.
`}}

Por exemplo, Annealing impacta uma ampla variedade de equipes e serviços, o que significa
que dependemos fortemente de contribuições de toda a empresa. A simplicidade do
Go tornou possível que pessoas fora de nossa equipe vissem por que alguma parte ou outra
não estava funcionando para elas, e frequentemente fornecessem correções ou recursos elas mesmas. Isso
nos permitiu crescer rapidamente.

Prodspec e Annealing estão encarregados de alguns componentes bastante críticos. A
simplicidade do Go significa que o código é fácil de seguir, seja para detectar bugs
durante a revisão ou ao tentar determinar exatamente o que aconteceu durante uma
interrupção de serviço.

O desempenho e o suporte à concorrência do Go também foram fundamentais para nosso trabalho. Como nosso
modelo de produção é declarativo, tendemos a manipular muitos dados
estruturados, que descrevem o que a produção é e o que deveria ser. Temos grandes
serviços, então os dados podem crescer muito, frequentemente tornando o processamento puramente sequencial
não eficiente o suficiente.

Estamos manipulando esses dados de muitas maneiras e em muitos lugares. Não é uma questão
de ter uma pessoa inteligente que inventa uma versão paralela de nosso algoritmo. É
uma questão de paralelismo casual, encontrando o próximo gargalo e
paralelizando aquela seção de código. E Go permite exatamente isso.

Como resultado de nosso sucesso com Go, agora usamos Go para cada novo desenvolvimento para
Prodspec e Annealing.

Além da equipe Site Reliability Engineering, equipes de engenharia de todo o
Google adotaram Go em seu processo de desenvolvimento. Leia sobre como as equipes
[Core Data Solutions](/solutions/google/coredata/),
[Firebase Hosting](/solutions/google/firebase/), e
[Chrome](/solutions/google/chrome/) usam Go para construir software rápido, confiável
e eficiente em escala.

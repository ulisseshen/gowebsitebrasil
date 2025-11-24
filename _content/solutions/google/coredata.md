---
ia-translated: true
title: "Como a Equipe Core Data Solutions do Google Usa Go"
company: Core Data
logoSrc: google.svg
logoSrcDark: google.svg
heroImgSrc: go_core_data_case_study.png
series: Case Studies
quote: |
  Google é uma empresa de tecnologia cuja missão é organizar as informações
  do mundo e torná-las universalmente acessíveis e úteis.

  Neste estudo de caso, a equipe Core Data Solutions do Google compartilha sua jornada
  com Go, incluindo sua decisão de reescrever serviços de indexação web em Go,
  aproveitando a concorrência integrada do Go, e observando como Go ajuda a
  melhorar o processo de desenvolvimento.
authors:
  - Prasanna Meda, Software Engineer, Core Data Solutions
---

A missão do Google é "organizar as informações do mundo e torná-las universalmente
acessíveis e úteis." Uma das equipes responsáveis por organizar essas
informações é a equipe Core Data Solutions do Google. A equipe, entre outras coisas,
mantém serviços para indexar páginas da web em todo o mundo. Esses serviços de indexação web
ajudam a suportar produtos como o Google Search mantendo os resultados de pesquisa
atualizados e abrangentes, e são escritos em Go.

Em 2015, para acompanhar a escala do Google, nossa equipe precisou reescrever nossa stack de indexação
de um único binário monolítico escrito em C++ para múltiplos componentes em uma
arquitetura de microsserviços. Decidimos reescrever muitos serviços de indexação em Go,
que agora usamos para alimentar a maior parte de nossa arquitetura.

{{backgroundquote `
  author: Minjae Hwang
  title: Software Engineer
  quote: |
    A concorrência integrada do Go é naturalmente adequada porque os engenheiros da equipe são
    encorajados a usar concorrência e algoritmos paralelos.
`}}

Ao escolher uma linguagem, nossa equipe descobriu que vários recursos do Go o tornaram
particularmente adequado. Por exemplo, a concorrência integrada do Go é naturalmente adequada
porque os engenheiros da equipe são encorajados a usar concorrência e algoritmos
paralelos. Os engenheiros também descobriram que "o código Go é mais natural", permitindo
que eles gastem seu tempo focando na lógica de negócios e análise em vez de em
gerenciamento de memória e otimização de desempenho.

Escrever código é muito mais simples ao escrever em Go, pois ajuda a reduzir a carga
cognitiva durante o processo de desenvolvimento. Por exemplo, ao trabalhar com C++,
IDEs sofisticadas podem "mostrar que o código-fonte não tem erro de compilação quando
na verdade há um" enquanto "em Go, [o código] sempre irá compilar quando [a
IDE] diz que o código não tem erro de compilação", disse MinJae Hwang, um engenheiro de software
na equipe Core Data Solutions. Reduzir pequenos pontos de atrito ao longo do
processo de desenvolvimento, como encurtar o ciclo de correção de erros de compilação,
ajudou nossa equipe a entregar mais rápido durante a reescrita original, e tem ajudado a manter nossos
custos de manutenção baixos.

"Quando estou em C++ e quero usar mais pacotes, tenho que escrever peças como
headers. Quando estou escrevendo em Go, **ferramentas integradas me permitem usar pacotes mais
facilmente. Minha velocidade de desenvolvimento é muito mais rápida,**" Hwang também compartilhou.

Com sintaxe de linguagem simples e suporte de ferramentas Go, vários membros de nossa equipe
acham muito mais fácil escrever código Go. Também descobrimos que Go faz um trabalho realmente
bom de verificação de tipo estático e que certos fundamentos do Go, como o
comando godoc, ajudaram a equipe a construir uma cultura mais disciplinada em torno de
escrever documentação.

{{backgroundquote `
  author: Prasanna Meda
  title: Software Engineer
  quote: |
    ...a indexação web do Google foi re-arquitetada em um ano. Mais impressionante ainda,
    a maioria dos desenvolvedores da equipe estava reescrevendo em Go enquanto também o aprendia.
`}}

Trabalhar em um produto tão amplamente usado ao redor do mundo não é uma tarefa pequena e a
decisão de nossa equipe de usar Go não foi simples, mas fazê-lo nos ajudou a mover
mais rápido. Como resultado, a indexação web do Google foi re-arquitetada em um ano.
Mais impressionante ainda, a maioria dos desenvolvedores da equipe estava reescrevendo em Go enquanto também
o aprendia.

Além da equipe Core Data Solutions, equipes de engenharia de todo o Google
adotaram Go em seu processo de desenvolvimento. Leia sobre como as equipes
[Chrome](/solutions/google/chrome/) e [Firebase
Hosting](/solutions/google/firebase/) usam Go para construir software rápido, confiável e
eficiente em escala.

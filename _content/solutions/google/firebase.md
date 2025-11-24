---
ia-translated: true
title: "Como a Equipe Firebase Hosting Escalou Com Go"
company: Firebase
logoSrc: firebase.svg
logoSrcDark: firebase.svg
heroImgSrc: go_firebase_case_study.png
series: Case Studies
quote: |
  Firebase é a plataforma móvel do Google que ajuda você a desenvolver rapidamente aplicativos
  de alta qualidade e expandir seus negócios.

  A equipe Firebase Hosting compartilhou sua jornada com Go, incluindo sua
  migração de backend do Node.js, a facilidade de integrar novos desenvolvedores Go, e
  como Go os ajudou a escalar.
---

A equipe Firebase Hosting fornece serviços de hospedagem web estática para clientes do Google Cloud.
Eles fornecem um host web estático que fica atrás de uma rede de entrega de conteúdo
global, e oferecem aos usuários ferramentas fáceis de usar. A equipe também
desenvolve recursos que vão desde o upload de arquivos do site até o registro de domínios e
rastreamento de uso.

Antes de ingressar no Google, a stack tecnológica do Firebase Hosting foi escrita em Node.js. A
equipe começou a usar Go quando precisou interoperar com vários outros
serviços do Google. Eles decidiram usar Go para ajudá-los a escalar com facilidade e
eficiência, sabendo que "a concorrência continuaria a ser uma grande necessidade." Eles
"estavam confiantes de que Go seria mais performático", e "gostaram que Go é mais conciso"
do que outras linguagens que estavam considerando, disse Michael Bleigh, um engenheiro de software
da equipe.

Começando com um pequeno serviço escrito em Go, a equipe migrou todo o seu
backend em uma série de movimentos. A equipe progressivamente identificou grandes recursos
que queriam implementar e, no processo, os reescreveram em Go e migraram para
o Google Cloud e o sistema interno de gerenciamento de clusters do Google. **Agora a equipe Firebase
Hosting substituiu 100% do código backend Node.js por Go.**

A experiência da equipe em escrever em Go começou com um engenheiro. "Através de
aprendizado peer-to-peer e Go sendo geralmente fácil de começar, todos
na equipe agora têm experiência de desenvolvimento em Go", disse Bleigh. Eles descobriram que embora a
maioria das pessoas que são novas na equipe não tivesse nenhuma experiência com Go,
"a maioria delas é produtiva em algumas semanas."

"Usando Go, é fácil ver como o código está organizado e o que o código faz",
disse Bleigh, falando pela equipe. "Go é geralmente muito legível e
compreensível. O tratamento de erros, receivers e interfaces da linguagem são todos
fáceis de entender devido aos idiomas da linguagem."

A concorrência continua sendo um foco para a equipe à medida que escalam. Robert Rossney,
um engenheiro de software, compartilhou que "Go torna muito fácil colocar todas as coisas
difíceis de concorrência em um lugar, e em todos os outros lugares está abstraído." Rossney
também falou sobre os benefícios de usar uma linguagem construída com concorrência em mente,
dizendo que "também existem muitas maneiras de fazer concorrência em Go. Tivemos que
aprender quando cada rota é melhor, como determinar quando um problema é um problema de concorrência,
como depurar - mas isso vem do fato de que você realmente pode escrever
esses padrões em código Go."

{{backgroundquote `
  author: Robert Rossney
  title: Software Engineer
  quote: |
    De modo geral, não há um momento na equipe em que estejamos sentindo
    frustração com Go, ele simplesmente sai do caminho e deixa você trabalhar.
`}}

Centenas de milhares de clientes hospedam seus sites com Firebase Hosting,
o que significa que o código Go é usado para servir bilhões de requisições por dia. "Nossa base de clientes
e tráfego dobraram várias vezes desde a migração para Go sem nunca
exigir otimizações ajustadas", compartilhou Bleigh. Com Go, a equipe viu
melhorias de desempenho tanto no software quanto na equipe, com excelentes
ganhos de produtividade. "De modo geral", Rossney mencionou, "...não há um
momento na equipe em que estejamos sentindo frustração com Go, ele simplesmente sai
do caminho e deixa você trabalhar."

Além da equipe Firebase Hosting, equipes de engenharia de todo o Google
adotaram Go em seu processo de desenvolvimento. Leia sobre como as equipes [Core Data
Solutions](/solutions/google/coredata/) e [Chrome](/solutions/google/chrome/)
usam Go para construir software rápido, confiável e eficiente em escala.

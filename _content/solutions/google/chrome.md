---
ia-translated: true
title: "Serviço de Otimização de Conteúdo do Chrome Roda em Go"
company: Chrome
logoSrc: chrome.svg
logoSrcDark: chrome.svg
heroImgSrc: go_chrome_case_study.png
series: Case Studies
quote: |
  Google Chrome é um navegador web mais simples, seguro e rápido do que nunca,
  com as funcionalidades inteligentes do Google integradas.

  Neste estudo de caso, a equipe Chrome Optimization Guide
  compartilhou como eles experimentaram com Go, aumentaram a velocidade rapidamente, e seus planos para
  usar Go no futuro.
---

Quando você pensa no produto Chrome, provavelmente pensa apenas no
navegador instalado pelo usuário. Mas nos bastidores, o Chrome tem uma extensa frota de
backends. Entre eles está o serviço Chrome Optimization Guide. Este serviço
forma uma base importante para a estratégia de experiência do usuário do Chrome, operando no
caminho crítico para os usuários, e é implementado em Go.

O serviço Chrome Optimization Guide foi projetado para trazer o poder do Google
para o Chrome fornecendo dicas ao navegador instalado sobre quais otimizações
podem ser realizadas no carregamento de uma página, bem como quando elas podem ser aplicadas de forma mais
eficaz. Ele compreende uma combinação de servidores em tempo real e análise de logs em
batch.

Todos os usuários do modo Lite do Chrome recebem dados através do serviço pelos seguintes
mecanismos: um push de blob de dados que fornece dicas para sites conhecidos em sua
geografia, um check-in nos servidores do Google para recuperar dicas para hosts que o
usuário específico visita frequentemente, e sob demanda para carregamentos de páginas para os quais uma dica não está
já no dispositivo. Se o serviço Chrome Optimization Guide desaparecesse de repente, os usuários poderiam notar uma mudança dramática na velocidade de seus carregamentos de página
e na quantidade de dados consumidos ao navegar na web.

{{backgroundquote `
  author: Sophie Chang
  title: Software Engineer
  quote: |
    Dado que Go foi um sucesso para nós, planejamos continuar a usá-lo
    onde apropriado
`}}

Quando a equipe de engenharia do Chrome começou a construir o serviço, apenas alguns
membros tinham conforto com Go. A maior parte da equipe estava mais familiarizada com C++, mas
eles acharam o boilerplate complexo necessário para criar um servidor C++ demais.
A equipe compartilhou que "[eles] estavam bastante motivados para aprender Go devido à sua
simplicidade, rápida curva de aprendizado e ecossistema." e que "[seu] senso de aventura
foi recompensado." Milhões de usuários confiam neste serviço para tornar sua experiência com o Chrome
melhor, e escolher Go não foi uma pequena decisão. Após sua experiência
até agora, a equipe também compartilhou que "dado que Go foi um sucesso para nós, planejamos
continuar a usá-lo onde apropriado."

Além da equipe Chrome Optimization Guide, equipes de engenharia de todo o
Google adotaram Go em seu processo de desenvolvimento. Leia sobre como as equipes [Core
Data Solutions](/solutions/google/coredata/) e [Firebase
Hosting](/solutions/google/firebase/) usam Go para construir software rápido, confiável
e eficiente em escala.

*Nota editorial: A equipe Go gostaria de agradecer a Sophie Chang por suas
contribuições para esta história.*

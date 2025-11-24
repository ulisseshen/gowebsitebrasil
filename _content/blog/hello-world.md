---
ia-translated: true
title: "Go: O Que Há de Novo em Março de 2010"
date: 2010-03-18
by:
- Andrew Gerrand
summary: Primeiro post!
---


Bem-vindo ao Blog oficial do Go. Nós, a equipe do Go,
esperamos usar este blog para manter o mundo atualizado sobre o desenvolvimento da
linguagem de programação Go e o crescente ecossistema de bibliotecas e aplicações ao seu redor.

Já se passaram alguns meses desde o nosso lançamento (novembro do ano passado),
então vamos falar sobre o que tem acontecido no Mundo Go desde então.

A equipe principal no Google continuou a desenvolver a linguagem,
compiladores, pacotes, ferramentas e documentação.
Os compiladores agora produzem código que em alguns casos é entre 2x e uma ordem
de magnitude mais rápido do que no lançamento.
Reunimos alguns gráficos de uma seleção de [Benchmarks](http://godashboard.appspot.com/benchmarks),
e a página de [Build Status](http://godashboard.appspot.com/) rastreia a
confiabilidade de cada changeset submetido ao repositório.

Fizemos mudanças de sintaxe para tornar a linguagem mais concisa,
regular e flexível.
Pontos e vírgulas foram [quase totalmente removidos](http://groups.google.com/group/golang-nuts/t/5ee32b588d10f2e9) da linguagem.
A sintaxe [...T](/doc/go_spec.html#Function_types)
torna mais simples lidar com um número arbitrário de parâmetros de função tipados.
A sintaxe x[lo:] agora é uma abreviação para x[lo:len(x)].
Go também agora suporta nativamente números complexos.
Veja as [release notes](/doc/devel/release.html) para mais informações.

[Godoc](/cmd/godoc/) agora fornece melhor suporte para
bibliotecas de terceiros,
e uma nova ferramenta - [goinstall](/cmd/goinstall) - foi
lançada para facilitar sua instalação.
Além disso, começamos a trabalhar em um sistema de rastreamento de pacotes para tornar
mais fácil encontrar o que você precisa.
Você pode ver o início disso na [página de Packages](http://godashboard.appspot.com/package).

Mais de 40.000 linhas de código foram adicionadas à [biblioteca padrão](/pkg/),
incluindo muitos pacotes totalmente novos, uma porção considerável escrita por colaboradores externos.

Falando em terceiros, desde o lançamento uma comunidade vibrante floresceu
em nossa [mailing list](http://groups.google.com/group/golang-nuts/) e
canal de irc (#go-nuts no freenode).
Oficialmente adicionamos mais de 50 pessoas ao projeto.
Suas contribuições vão desde correções de bugs e correções de documentação até
pacotes principais e suporte para sistemas operacionais adicionais (Go agora é suportado no FreeBSD,
e um [port para Windows](http://code.google.com/p/go/wiki/WindowsPort) está em andamento).
Consideramos essas contribuições da comunidade nosso maior sucesso até agora.

Também recebemos boas críticas. Este [artigo recente no PC World](http://www.pcworld.idg.com.au/article/337773/google_go_captures_developers_imaginations/)
resumiu o entusiasmo em torno do projeto.
Vários blogueiros começaram a documentar suas experiências na linguagem
(veja [aqui](http://golang.tumblr.com/),
[aqui](http://www.infi.nl/blog/view/id/47),
e [aqui](http://freecella.blogspot.com/2010/01/gospecify-basic-setup-of-projects.html)
por exemplo). A reação geral de nossos usuários tem sido muito positiva;
um iniciante comentou ["Saí extremamente impressionado. Go caminha em uma linha elegante entre simplicidade e poder."](https://groups.google.com/group/golang-nuts/browse_thread/thread/5fabdd59f8562ed2)

Quanto ao futuro: ouvimos as inúmeras vozes nos dizendo o que eles precisam,
e agora estamos focados em deixar o Go pronto para o horário nobre.
Estamos melhorando o garbage collector, runtime scheduler,
ferramentas e bibliotecas padrão, bem como explorando novas funcionalidades da linguagem.
2010 será um ano emocionante para Go, e esperamos colaborar
com a comunidade para torná-lo um sucesso.

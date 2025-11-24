---
ia-translated: true
title: "MercadoLibre Cresce com Go"
company: MercadoLibre
logoSrc: mercadolibre_light.svg
logoSrcDark: mercadolibre_dark.svg
heroImgSrc: go_mercadolibre_case_study_logo.png
carouselImgSrc: go_mercadolibre_case_study.png
date: 2019-11-10T16:26:31-04:00
series: Case Studies
quote: Go fornece código limpo e eficiente que escala prontamente conforme o comércio online da MercadoLibre cresce, e aumenta a produtividade dos desenvolvedores ao permitir que seus engenheiros sirvam seu público cada vez maior enquanto escrevem menos código.
---

{{pullquote `
  author: Eric Kohan
  title: Software Engineering Manager
  company: MercadoLibre
  quote: |
    Eu acho que **o tour de Go é de longe a melhor introdução a uma linguagem que já vi**. É realmente simples e dá uma visão geral justa de provavelmente 80 por cento da linguagem. Quando queremos que os desenvolvedores aprendam Go e cheguem à produção rapidamente, dizemos a eles para começar com o tour de Go.
`}}

## Go ajuda ecossistema integrado a atrair desenvolvedores e escalar eCommerce

MercadoLibre, Inc. hospeda o maior ecossistema de comércio online da América Latina e está presente em 18 países. Fundada
em 1999 e com sede na Argentina, a empresa recorreu ao Go para ajudá-la a escalar e modernizar seu ecossistema. Go
fornece código limpo e eficiente que escala prontamente conforme o comércio online da MercadoLibre cresce, e aumenta a
produtividade dos desenvolvedores ao permitir que seus engenheiros sirvam seu público cada vez maior enquanto escrevem menos código.

### MercadoLibre recorre ao Go para escalar

Em 2015, havia uma sensação crescente dentro da MercadoLibre de que seu framework de API existente, em Groovy e Grails, estava
atingindo seus limites e a empresa precisava de uma plataforma diferente para continuar escalando. A plataforma da MercadoLibre estava (e
continua) a expandir exponencialmente, o que criou muito trabalho extra para seus desenvolvedores: Tanto Groovy quanto Grails exigem
muitas decisões dos desenvolvedores e Groovy é uma linguagem de programação dinâmica. Esta não era uma boa combinação para
um crescimento rapidamente escalável, pois a MercadoLibre precisava de desenvolvedores muito experientes neste ambiente muito intensivo em recursos
para desenvolver e ajustar para alcançar o desempenho desejado. Os tempos de execução de testes eram lentos, e os tempos de build e deploy eram
lentos. Assim, a necessidade de eficiência de código e escalabilidade tornou-se tão importante quanto a necessidade de velocidade no desenvolvimento de código.


### Go melhora a eficiência do sistema

Como um exemplo das contribuições do Go para a eficiência de rede, a equipe central de API constrói e mantém as maiores APIs no
centro das soluções de microservices da empresa. Esta equipe cria APIs de usuário, que por sua vez são usadas pelo
Marketplace MercadoLibre, pela plataforma FinTech MercadoPago, pelas soluções de envio e logística da MercadoLibre, e
outras soluções hospedadas. Com os altos níveis de serviço exigidos por essas soluções—a API de usuário média tem entre oito
e dez milhões de requisições por minuto—a equipe emprega Go para servi-las em menos de dez milissegundos por requisição.

A equipe de API também implanta containers Docker—um produto software-as-a-service (SaaS), também escrito em Go—para virtualizar
seu desenvolvimento e implantar prontamente seus microservices via Docker Engine. Este sistema suporta APIs maiores e
críticas que lidam com **mais de 20 milhões de requisições por minuto em Go.**

Uma API fez uso importante das primitivas de concorrência do Go para multiplexar eficientemente IDs de vários serviços. A equipe
foi capaz de realizar isso com apenas algumas linhas de código Go, e o sucesso desta API convenceu a equipe central de API a
migrar mais e mais microservices para Go. O resultado final para a MercadoLibre foi melhoria nas eficiências de custo e
tempos de resposta do sistema.

### Go para escalabilidade

Historicamente, grande parte da stack da empresa era baseada em Grails e Groovy com bancos de dados relacionais. No entanto, este
grande framework com múltiplas camadas logo foi encontrado enfrentando problemas de escalabilidade.

Converter essa arquitetura legada para Go como um novo framework muito leve para construir APIs simplificou essas camadas
intermediárias e rendeu grandes benefícios de desempenho. Por exemplo, um grande serviço Go agora é capaz de **executar 70.000 requisições
por máquina com apenas 20 MB de RAM.**

{{backgroundquote `
  author: Eric Kohan
  title: Software Engineering Manager
  company: MercadoLibre
  quote: |
    Go foi simplesmente maravilhoso para nós. É muito poderoso
    e muito fácil de aprender, e com infraestrutura backend, tem sido ótimo para nós em termos de escalabilidade.
`}}

Usar **Go permitiu à MercadoLibre reduzir o número de servidores** que eles usam para este serviço a um oitavo do número
original (de 32 servidores para quatro), além de cada servidor poder operar com menos poder (originalmente quatro cores de CPU, agora
para dois cores de CPU). Com Go, a empresa **eliminou 88 por cento de seus servidores e reduziu a CPU nos restantes pela
metade**—produzindo uma tremenda economia de custos.

Situado entre desenvolvedores e os provedores de nuvem, a MercadoLibre usa uma plataforma chamada Fury—uma ferramenta platform-as-a-service
para construir, implantar, monitorar e gerenciar serviços de forma cloud-agnostic. Como resultado, qualquer equipe que
queira criar um novo serviço em Go tem acesso a templates comprovados para uma variedade de tipos de serviço, e pode rapidamente criar
um repositório no GitHub com código inicial, uma imagem Docker para o serviço, e um pipeline de deployment. O resultado final
é um sistema que permite aos engenheiros focar na construção de serviços inovadores enquanto evitam as etapas tediosas de configurar
um novo projeto—tudo isso ao mesmo tempo que efetivamente padroniza os pipelines de build e deployment.

Hoje, **aproximadamente metade do tráfego da MercadoLibre é tratado por aplicações Go.**


### MercadoLibre usa Go para desenvolvedores

As _línguas francas_ de programação para a infraestrutura da MercadoLibre são atualmente Go e Java. Cada app, cada programa,
cada microservice é hospedado em seu próprio repositório GitHub, além disso a empresa usa um repositório GitHub adicional de
toolkits para resolver novos problemas e permitir que clientes interajam com seus serviços.

Esses extensos e bem-curados toolkits Go e Java permitem aos programadores desenvolver novos apps rapidamente e com grande
suporte. Além disso, em uma comunidade de mais de 2.800 desenvolvedores, a MercadoLibre tem múltiplos grupos internos disponíveis para
chat e orientação sobre deploy de Go, seja em diferentes centros de desenvolvimento ou diferentes países. A empresa também
promove grupos de trabalho internos para fornecer sessões de treinamento para novos desenvolvedores Go da MercadoLibre, e hospeda meetups de Go
para desenvolvedores externos para ajudar a construir uma comunidade mais ampla de desenvolvedores Go latino-americanos.


### Go como ferramenta de recrutamento

A defesa do Go pela MercadoLibre também se tornou uma forte ferramenta de recrutamento para a empresa. A MercadoLibre estava entre as primeiras
empresas usando Go na Argentina, e é talvez a maior na América Latina usando a linguagem tão amplamente em produção.
Com sede em Buenos Aires, com muitas start-ups e empresas emergentes de tecnologia por perto, a adoção de
Go pela MercadoLibre moldou o mercado para desenvolvedores em toda a Pampa.

{{backgroundquote `
  author: Eric Kohan
  title: Software Engineering Manager
  company: MercadoLibre
  quote: |
    Nós realmente concordamos com a filosofia maior da linguagem. Amamos a simplicidade do Go, e achamos que ter seu tratamento de erros muito explícito tem sido um ganho para os desenvolvedores porque resulta em código mais seguro e estável em produção.
`}}

Buenos Aires é hoje um mercado muito competitivo para programadores, oferecendo aos programadores de computador muitas opções de emprego,
e a alta demanda por tecnologia na região impulsiona ótimos salários, ótimos benefícios e a capacidade de ser seletivo
ao escolher um empregador. Como tal, a MercadoLibre—como todos os empregadores de engenheiros e programadores na região—esforça-se
para fornecer um local de trabalho empolgante e forte caminho de carreira. Go provou ser um diferencial chave para a MercadoLibre: a
empresa organiza workshops de Go para desenvolvedores externos para que eles possam vir e aprender Go, e quando eles gostam do que estão
fazendo e das pessoas com quem conversam, eles rapidamente reconhecem a MercadoLibre como um lugar atraente para trabalhar.

### Go capacitando desenvolvedores

A MercadoLibre emprega Go por sua simplicidade com sistemas em escala, mas essa simplicidade também é a razão pela qual os
desenvolvedores da empresa amam Go.

A empresa também usa páginas web como [Go by Example](https://gobyexample.com/) e [Effective
Go](/doc/effective_go.html) para educar novos programadores, e compartilha APIs internas representativas
escritas em Go para acelerar a compreensão e proficiência. Os desenvolvedores da MercadoLibre obtêm os recursos de que precisam para abraçar a
linguagem, então aproveitam suas próprias habilidades e entusiasmo para começar a programar.

{{backgroundquote `
  author: Federico Martin Roasio
  title: Technical Project Lead
  company: MercadoLibre
  quote: |
    Go tem sido ótimo para escrever lógica de negócios, e somos a equipe que escreve essas APIs.
`}}

A MercadoLibre aproveita a sintaxe expressiva e limpa do Go para facilitar aos desenvolvedores escrever programas que rodem
eficientemente em plataformas de nuvem modernas. E embora a velocidade no desenvolvimento gere eficiência de custo para a empresa, os desenvolvedores
individualmente se beneficiam da rápida curva de aprendizado que Go oferece. Não apenas os engenheiros experientes da MercadoLibre são capazes
de construir aplicações altamente críticas muito rapidamente com Go, mas até mesmo engenheiros iniciantes foram capazes de escrever
serviços que, em outras linguagens, a MercadoLibre só confiaria a desenvolvedores mais seniores. Por exemplo, um conjunto chave de
APIs de usuário—lidando com quase dez milhões de requisições por minuto—foram desenvolvidas por engenheiros de software iniciantes, muitos dos quais
só sabiam sobre programação de cursos recentes na universidade. Da mesma forma, a MercadoLibre viu desenvolvedores já
proficientes em outras linguagens de programação (como Java ou .NET ou Ruby) aprender Go rápido o suficiente para começar a escrever serviços de produção
em apenas algumas semanas.

Com Go, os **tempos de build da MercadoLibre são três vezes (3x) mais rápidos** e sua **suíte de testes roda incríveis 24 vezes
mais rápido**. Isso significa que os desenvolvedores da empresa podem fazer uma alteração, depois construir e testar essa alteração muito mais rápido do que eles
podiam antes.

E reduzir os tempos de execução da suíte de testes da MercadoLibre de 90 segundos para **apenas 3 segundos com Go** foi um enorme benefício para seus
desenvolvedores—permitindo que eles mantenham o foco (e contexto) enquanto os testes muito mais rápidos são concluídos.

Aproveitando este sucesso, a MercadoLibre está comprometida não apenas com a educação contínua para seus programadores, mas com a educação contínua em Go.
A empresa envia líderes de engenharia chave para a GopherCon e outros eventos Go a cada ano, as equipes de
infraestrutura e segurança da MercadoLibre incentivam todas as equipes de desenvolvimento a manter as versões de Go atualizadas, e a empresa
tem uma equipe desenvolvendo um _Go-meli-toolkit_: Uma biblioteca Go completa para interfacear todos os serviços fornecidos pelo Fury.

### Começando sua empresa com Go

Assim como a MercadoLibre começou com um projeto de prova de conceito para implementar Go, dezenas de outras grandes empresas estão
adotando Go também.

Há mais de um milhão de desenvolvedores usando Go em todo o mundo—abrangendo bancos e comércio, jogos e mídia, tecnologia e outras indústrias, em empresas tão diversas quanto [American Express](/solutions/americanexpress), [PayPal](/solutions/paypal), Capital One, Dropbox, IBM, Monzo, New York Times, Salesforce, Square, Target, Twitch, Uber e, claro, Google.

Para aprender mais sobre como Go pode ajudar sua empresa a construir software confiável e escalável como faz na MercadoLibre, visite [go.dev](/) hoje.

<!--{
  "Title": "Developing and publishing modules",
  "ia-translated": true
}-->

Você pode coletar packages relacionados em módulos, depois publicar os módulos para
outros desenvolvedores usarem. Este tópico dá uma visão geral do desenvolvimento e
publicação de módulos.

Para suportar desenvolvimento, publicação e uso de módulos, você usa:

*   Um **workflow** através do qual você desenvolve e publica módulos, revisando-os
	com novas versões ao longo do tempo. Consulte [Workflow for developing and publishing
	modules](#workflow).
*	**Práticas de design** que ajudam os usuários de um módulo a entendê-lo e atualizar
	para novas versões de maneira estável. Consulte [Design and development](#design).
*   Um **sistema descentralizado para publicar** módulos e recuperar seu código.
	Você disponibiliza seu módulo para outros desenvolvedores usarem do seu próprio
	repositório e publica com um número de versão. Consulte [Decentralized
	publishing](#decentralized).
*   Um **motor de busca de packages** e navegador de documentação (pkg.go.dev) no qual
	desenvolvedores podem encontrar seu módulo. Consulte [Package discovery](#discovery).
*   Uma **convenção de numeração de versão de módulo** para comunicar expectativas de
	estabilidade e compatibilidade retroativa para desenvolvedores usando seu módulo. Consulte
	[Versioning](#versioning).
*   **Ferramentas Go** que facilitam para outros desenvolvedores gerenciar
	dependências, incluindo obter o código-fonte do seu módulo, atualizar, e assim por diante.
	Consulte [Managing dependencies](/doc/modules/managing-dependencies).

**Veja também**

*   Se você está interessado simplesmente em usar packages desenvolvidos por outros, este
	não é o tópico para você. Em vez disso, consulte [Managing
	dependencies](managing-dependencies).
*   Para um tutorial que inclui alguns fundamentos de desenvolvimento de módulos, consulte
	[Tutorial: Create a Go module](/doc/tutorial/create-module).

## Workflow para desenvolver e publicar módulos {#workflow}

Quando você quer publicar seus módulos para outros, você adota algumas convenções para
tornar o uso desses módulos mais fácil.

Os seguintes passos de alto nível são descritos em mais detalhes em [Module release
and versioning workflow](release-workflow).

1. Projetar e codificar os packages que o módulo incluirá.
1. Fazer commit do código no seu repositório usando convenções que garantem que ele esteja disponível
	para outros via ferramentas Go.
1. Publicar o módulo para torná-lo descobrível por desenvolvedores.
1. Ao longo do tempo, revisar o módulo com versões que usam uma convenção de numeração de versão
	que sinaliza a estabilidade e compatibilidade retroativa de cada versão.

## Design e desenvolvimento {#design}

Seu módulo será mais fácil para desenvolvedores encontrarem e usarem se as funções e
packages nele formarem um todo coerente. Quando você está projetando a API pública de um módulo,
tente manter sua funcionalidade focada e discreta.

Além disso, projetar e desenvolver seu módulo com compatibilidade retroativa em mente
ajuda seus usuários a atualizar enquanto minimiza mudanças no próprio código deles. Você pode usar
certas técnicas em código para evitar liberar uma versão que quebra a compatibilidade
retroativa. Para mais sobre essas técnicas, consulte [Keeping your modules
compatible](/blog/module-compatibility) no blog Go.

Antes de publicar um módulo, você pode referenciá-lo no sistema de arquivos local usando
a diretiva replace. Isso facilita escrever código cliente que chama
funções no módulo enquanto o módulo ainda está em desenvolvimento. Para mais
informação, consulte "Coding against an unpublished module" em [Module release and
versioning workflow](release-workflow#unpublished).

## Publicação descentralizada {#decentralized}

Em Go, você publica seu módulo tagueando seu código no seu repositório para torná-lo
disponível para outros desenvolvedores usarem. Você não precisa fazer push do seu módulo para um
serviço centralizado porque as ferramentas Go podem baixar seu módulo diretamente do seu
repositório (localizado usando o caminho do módulo, que é uma URL com o esquema
omitido) ou de um servidor proxy.

Após importar seu package no código deles, desenvolvedores usam ferramentas Go (incluindo
o comando `go get`) para baixar o código do seu módulo para compilar. Para suportar
este modelo, você segue convenções e melhores práticas que possibilitam que
ferramentas Go (em nome de outro desenvolvedor) recuperem o código-fonte do seu módulo do
seu repositório. Por exemplo, ferramentas Go usam o caminho do módulo que você especifica,
junto com o número de versão do módulo que você usa para taguear o módulo para release, para
localizar e baixar o módulo para seus usuários.

Para mais sobre convenções e melhores práticas de código-fonte e publicação, consulte
[Managing module source](/doc/modules/managing-source).

Para instruções passo a passo sobre publicação de um módulo, consulte [Publishing a
module](publishing).

## Descoberta de packages {#discovery}

Após você ter publicado seu módulo e alguém o tiver buscado com ferramentas Go, ele
se tornará visível no site de descoberta de packages Go em
[pkg.go.dev](https://pkg.go.dev/). Lá, desenvolvedores podem pesquisar o site para encontrá-lo e ler sua documentação.

Para começar a usar o módulo, um desenvolvedor importa packages do módulo, depois
executa o comando `go get` para baixar seu código-fonte para compilar.

Para mais sobre como desenvolvedores encontram e usam módulos, consulte [Managing
dependencies](managing-dependencies).

## Versionamento {#versioning}

Conforme você revisa e melhora seu módulo ao longo do tempo, você atribui números de versão
(baseados no modelo de versionamento semântico) projetados para sinalizar a estabilidade e
compatibilidade retroativa de cada versão. Isso ajuda desenvolvedores usando seu módulo
a determinar quando o módulo está estável e se uma atualização pode incluir
mudanças significativas no comportamento. Você indica o número de versão de um módulo
tagueando o código-fonte do módulo no repositório com o número.

Para mais sobre desenvolvimento de atualizações de versão major, consulte [Developing a major version
update](major-version).

Para mais sobre como você usa o modelo de versionamento semântico para módulos Go, consulte
[Module version numbering](/doc/modules/version-numbers).

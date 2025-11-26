<!--{
  "Title": "Managing module source",
  "ia-translated": true
}-->

Quando você está desenvolvendo módulos para publicar para outros usarem, você pode ajudar a garantir
que seus módulos sejam mais fáceis para outros desenvolvedores usarem seguindo as
convenções de repositório descritas neste tópico.

Este tópico descreve ações que você pode tomar ao gerenciar seu
repositório de módulo. Para informações sobre a sequência de passos de workflow que você seguiria ao
revisar de versão para versão, consulte [Module release and versioning
workflow](release-workflow).

Algumas das convenções descritas aqui são exigidas em módulos, enquanto outras são
melhores práticas. Este conteúdo assume que você está familiarizado com as práticas básicas de uso
de módulo descritas em [Managing dependencies](/doc/modules/managing-dependencies).

Go suporta os seguintes repositórios para publicar módulos: Git, Subversion,
Mercurial, Bazaar, e Fossil.

Para uma visão geral do desenvolvimento de módulos, consulte [Developing and publishing
modules](developing).

## Como as ferramentas Go encontram seu módulo publicado {#tools}

No sistema descentralizado do Go para publicar módulos e recuperar seu código,
você pode publicar seu módulo deixando o código em seu repositório. As ferramentas Go
dependem de regras de nomenclatura que têm caminhos de repositório e tags de repositório indicando o
nome e número de versão de um módulo. Quando seu repositório segue esses
requisitos, seu código de módulo é baixável do seu repositório pelas ferramentas Go
como o comando [`go get`](/ref/mod#go-get).

Quando um desenvolvedor usa o comando `go get` para obter código fonte para packages que seu
código importa, o comando faz o seguinte:

1. De declarações `import` no código fonte Go, `go get` identifica o caminho do módulo
  dentro do caminho do package.
1. Usando uma URL derivada do caminho do módulo, o comando localiza a fonte do módulo
  em um servidor proxy de módulo ou em seu repositório diretamente.
1. Localiza fonte para a versão do módulo a baixar combinando o
  número de versão do módulo com uma tag de repositório para descobrir o código no repositório.
  Quando um número de versão a usar ainda não é conhecido, `go get` localiza a
  versão de release mais recente.
1. Recupera a fonte do módulo e baixa para o cache de módulo local do desenvolvedor.

## Organizando código no repositório {#repository}

Você pode manter a manutenção simples e melhorar a experiência dos desenvolvedores com seu
módulo seguindo as convenções descritas aqui. Colocar seu código de módulo
em um repositório é geralmente tão simples quanto com outro código.

O diagrama a seguir ilustra uma hierarquia de fonte para um módulo simples com
dois packages.

<img src="images/source-hierarchy.png"
     alt="Diagrama ilustrando uma hierarquia de código fonte de módulo"
     style="width: 250px;" />

Seu commit inicial deve incluir arquivos listados na tabela a seguir:

<table id="module-files" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">File</td>
      <th class="DocTable-cell">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">LICENSE</td>
      <td class="DocTable-cell">A licença do módulo.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.mod</td>
      <td class="DocTable-cell"><p>Descreve o módulo, incluindo seu caminho de módulo
        (efetivamente, seu nome) e suas dependências. Para mais, consulte a
        <a href="gomod-ref">referência go.mod</a>.</p>
      <p>O caminho do módulo será dado em uma diretiva module, como:</p>
      <pre>module example.com/mymodule</pre>
      <p>Para mais sobre escolher um caminho de módulo, consulte
          <a href="/doc/modules/managing-dependencies#naming_module">Managing
          dependencies</a>.</p>
      <p>Embora você possa editar o arquivo go.mod, você achará mais confiável
          fazer mudanças através de comandos <code>go</code>.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">go.sum</td>
      <td class="DocTable-cell"><p>Contém hashes criptográficos que representam
        as dependências do módulo. As ferramentas Go usam esses hashes para autenticar
        módulos baixados, tentando confirmar que o módulo baixado é
        autêntico. Onde esta confirmação falha, Go exibirá um erro de segurança.<p>
      <p>O arquivo estará vazio ou não presente quando não houver dependências.
        Você não deve editar este arquivo exceto usando o comando <code>go mod tidy</code>,
        que remove entradas desnecessárias.</p>
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">Diretórios de package e fontes .go.</td>
      <td class="DocTable-cell">Diretórios e arquivos .go que compõem os packages
      e fontes Go no módulo.</td>
    </tr>
  </tbody>
</table>

Da linha de comando, você pode criar um repositório vazio, adicionar os arquivos que
serão parte do seu commit inicial, e fazer commit com uma mensagem. Aqui está um
exemplo usando git:


```
$ git init
$ git add --all
$ git commit -m "mycode: initial commit"
$ git push
```

## Escolhendo escopo de repositório {#repository-scope}

Você publica código em um módulo quando o código deve ser versionado independentemente
do código em outros módulos.

Projetar seu repositório para que hospede um único módulo em seu diretório raiz
ajudará a manter a manutenção mais simples, particularmente ao longo do tempo conforme você publica novas
versões minor e patch, ramifica em novas versões major, e assim por diante. No entanto, se
suas necessidades exigirem, você pode em vez disso manter uma coleção de módulos em um
único repositório.

### Fornecendo um módulo por repositório {#one-module-source}

Você pode manter um repositório que tem a fonte de um único módulo nele. Neste
modelo, você coloca seu arquivo go.mod na raiz do repositório, com package
subdiretórios contendo fonte Go abaixo.

Esta é a abordagem mais simples, tornando seu módulo provavelmente mais fácil de gerenciar ao longo
do tempo. Ajuda você a evitar a necessidade de prefixar um número de versão de módulo com um
caminho de diretório.

<img src="images/single-module.png"
     alt="Diagrama ilustrando a fonte de um único módulo em seu repositório"
     style="width: 425px;" />

### Fornecendo múltiplos módulos em um único repositório {#multiple-module-source}

Você pode publicar múltiplos módulos de um único repositório. Por exemplo, você
pode ter código em um único repositório que constitui múltiplos módulos, mas
quer versionar esses módulos separadamente.

Cada subdiretório que é um diretório raiz de módulo deve ter seu próprio arquivo go.mod.

Fornecer código de módulo em subdiretórios altera a forma da tag de versão que você
deve usar ao publicar um módulo. Você deve prefixar a parte do número de versão da
tag com o nome do subdiretório que é a raiz do módulo. Para mais
sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

Por exemplo, para o módulo `example.com/mymodules/module1` abaixo, você teria
o seguinte para a versão v1.2.3:

*   Caminho do módulo: `example.com/mymodules/module1`
*   Tag de versão: `module1/v1.2.3`
*   Caminho do package importado por um usuário: `example.com/mymodules/module1/package1`
*   Caminho do módulo e versão conforme especificado na diretiva require de um usuário: `example.com/mymodules/module1 v1.2.3`

<img src="images/multiple-modules.png"
     alt="Diagrama ilustrando dois módulos em um único repositório"
     style="width: 480px;" />

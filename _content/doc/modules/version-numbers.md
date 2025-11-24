<!--{
  "Title": "Module version numbering",
  "ia-translated": true
}-->

O desenvolvedor de um módulo usa cada parte do número de versão de um módulo para sinalizar a
estabilidade e compatibilidade retroativa da versão. Para cada novo release, o
número de versão do release de um módulo reflete especificamente a natureza das mudanças do módulo
desde o release anterior.

Quando você está desenvolvendo código que usa módulos externos, você pode usar os números de
versão para entender a estabilidade de um módulo externo ao considerar uma
atualização. Quando você está desenvolvendo seus próprios módulos, seus números de versão
sinalizarão a estabilidade e compatibilidade retroativa dos seus módulos para outros desenvolvedores.

Este tópico descreve o que os números de versão de módulo significam.

**Veja também**

* Quando você está usando packages externos no seu código, você pode gerenciar essas
  dependências com as ferramentas Go. Para mais, consulte [Managing dependencies](managing-dependencies).
* Se você está desenvolvendo módulos para outros usarem, você aplica um número de versão
  quando publica o módulo, tagueando o módulo em seu repositório. Para mais,
  consulte [Publishing a module](publishing).

Um módulo lançado é publicado com um número de versão no modelo de versionamento semântico,
como na seguinte ilustração:

<img src="images/version-number.png"
     alt="Diagrama ilustrando um número de versão semântica mostrando versão major 1, versão minor 4, versão patch 0, e versão pre-release beta 2"
     style="width: 300px;" />

A tabela a seguir descreve como as partes de um número de versão significam a
estabilidade e compatibilidade retroativa de um módulo.

<table class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">Version stage</th>
      <th class="DocTable-cell">Example</th>
      <th class="DocTable-cell">Message to developers</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#in-development">In development</a></td>
      <td class="DocTable-cell">Número de pseudo-versão automático
      <p>v<strong>0</strong>.x.x</td>
      <td class="DocTable-cell">Sinaliza que o módulo ainda está <strong>em
        desenvolvimento e instável</strong>. Este release não carrega garantias de compatibilidade retroativa
        ou estabilidade.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#major">Major version</a></td>
      <td class="DocTable-cell">v<strong>1</strong>.x.x</td>
      <td class="DocTable-cell">Sinaliza <strong>mudanças incompatíveis na API pública
        </strong>. Este release não carrega garantia de que será
        compatível retroativamente com versões major anteriores.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#minor">Minor version</a></td>
      <td class="DocTable-cell">vx.<strong>4</strong>.x</td>
      <td class="DocTable-cell">Sinaliza <strong>mudanças compatíveis retroativamente na API pública
        </strong>. Este release garante compatibilidade retroativa e
        estabilidade.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#patch">Patch version</a></td>
      <td class="DocTable-cell">vx.x.<strong>1</strong></td>
      <td class="DocTable-cell">Sinaliza <strong>mudanças que não afetam a
        API pública do módulo</strong> ou suas dependências. Este release
        garante compatibilidade retroativa e estabilidade.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell"><a href="#pre-release">Pre-release version</a></td>
      <td class="DocTable-cell">vx.x.x-<strong>beta.2</strong></td>
      <td class="DocTable-cell">Sinaliza que este é um <strong>milestone de pre-release,
        como um alpha ou beta</strong>. Este release não carrega
        garantias de estabilidade.</td>
    </tr>
  </tbody>
</table>

<a id="in-development" ></a>
## In development

Sinaliza que o módulo ainda está em desenvolvimento e **instável**. Este release
não carrega garantias de compatibilidade retroativa ou estabilidade.

O número de versão pode assumir uma das seguintes formas:

**Número de pseudo-versão**

> v0.0.0-20170915032832-14c0d48ead0c

**Número v0**

> v0.x.x

<a id="pseudo" ></a>
### Número de pseudo-versão

Quando um módulo não foi tagueado em seu repositório, as ferramentas Go gerarão um
número de pseudo-versão para uso no arquivo go.mod do código que chama funções no
módulo.

**Nota:** Como melhor prática, sempre permita que as ferramentas Go gerem o
número de pseudo-versão em vez de criar o seu próprio.

Pseudo-versões são úteis quando um desenvolvedor de código consumindo as
funções do módulo precisa desenvolver contra um commit que ainda não foi tagueado com uma
tag de versão semântica.

Um número de pseudo-versão tem três partes separadas por hífens, como mostrado na
seguinte forma:

#### Sintaxe

_baseVersionPrefix_-_timestamp_-_revisionIdentifier_

#### Partes

* **baseVersionPrefix** (vX.0.0 ou vX.Y.Z-0) é um valor derivado ou de uma
  tag de versão semântica que precede a revisão ou de vX.0.0 se não houver
  tal tag.

* **timestamp** (yymmddhhmmss) é o horário UTC em que a revisão foi criada. No Git,
  este é o commit time, não o author time.

* **revisionIdentifier** (abcdefabcdef) é um prefixo de 12 caracteres do hash do commit,
  ou no Subversion, um número de revisão com padding zero.

<a id="v0" ></a>
### Número v0

Um módulo publicado com um número v0 terá um número de versão semântica formal
com uma parte major, minor e patch, bem como um identificador de pre-release
opcional.

Embora uma versão v0 possa ser usada em produção, ela não faz garantias de estabilidade ou compatibilidade
retroativa. Além disso, versões v1 e posteriores têm permissão para
quebrar compatibilidade retroativa para código usando as versões v0. Por esta razão, um
desenvolvedor com código consumindo funções em um módulo v0 é responsável por
se adaptar a mudanças incompatíveis até que v1 seja lançado.

<a id="pre-release" ></a>
## Pre-release version

Sinaliza que este é um milestone de pre-release, como um alpha ou beta. Este
release não carrega garantias de estabilidade.

#### Exemplo

```
vx.x.x-beta.2
```

O desenvolvedor de um módulo pode usar um identificador de pre-release com qualquer combinação major.minor.patch
anexando um hífen e o identificador de pre-release.

<a id="minor" ></a>
## Minor version

Sinaliza mudanças compatíveis retroativamente na API pública do módulo. Este release
garante compatibilidade retroativa e estabilidade.

#### Exemplo

```
vx.4.x
```

Esta versão altera a API pública do módulo, mas não de uma maneira que quebre
código que a chama. Isso pode incluir mudanças nas próprias dependências de um módulo ou a
adição de novas funções, métodos, campos de struct ou tipos.

Em outras palavras, esta versão pode incluir melhorias através de novas funções
que outro desenvolvedor pode querer usar. No entanto, um desenvolvedor usando
versões minor anteriores não precisa alterar seu código de outra forma.

<a id="patch" ></a>
## Patch version

Sinaliza mudanças que não afetam a API pública do módulo ou suas dependências.
Este release garante compatibilidade retroativa e estabilidade.

#### Exemplo

```
vx.x.1
```

Uma atualização que incrementa este número é apenas para pequenas mudanças como correções de
bugs. Desenvolvedores de código consumidor podem atualizar para esta versão com segurança sem
precisar alterar seu código.

<a id="major" ></a>
## Major version

Sinaliza mudanças incompatíveis retroativamente na API pública de um módulo. Este release
não carrega garantia de que será compatível retroativamente com versões major
anteriores.

#### Exemplo

v1.x.x

Um número de versão v1 ou superior sinaliza que o módulo é estável para uso (com
exceções para suas versões de pre-release).

Observe que como uma versão 0 não faz garantias de estabilidade ou compatibilidade retroativa,
um desenvolvedor atualizando um módulo de v0 para v1 é responsável por
se adaptar a mudanças que quebram compatibilidade retroativa.

Um desenvolvedor de módulo deve incrementar este número além de v1 apenas quando necessário
porque a atualização de versão representa uma interrupção significativa para desenvolvedores
cujo código usa funções no módulo atualizado. Esta interrupção inclui
mudanças incompatíveis retroativamente na API pública, bem como a necessidade de
desenvolvedores usando o módulo atualizarem o caminho do package onde quer que importem
packages do módulo.

Uma atualização de versão major para um número maior que v1 também terá um novo caminho de
módulo. Isso porque o caminho do módulo terá o número de versão major
anexado, como no exemplo a seguir:

```
module example.com/mymodule/v2 v2.0.0
```

Uma atualização de versão major torna este um novo módulo com um histórico separado do
módulo da versão anterior. Se você está desenvolvendo módulos para publicar para outros,
consulte "Publishing breaking API changes" em [Module release and versioning
workflow](release-workflow).

Para mais sobre a diretiva module, consulte [go.mod reference](gomod-ref).

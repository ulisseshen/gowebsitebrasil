<!--{
  "Title": "Module release and versioning workflow",
  "ia-translated": true
}-->

Quando você desenvolve módulos para uso por outros desenvolvedores, você pode seguir um workflow
que ajuda a garantir uma experiência confiável e consistente para desenvolvedores usando o
módulo. Este tópico descreve os passos de alto nível nesse workflow.

Para uma visão geral do desenvolvimento de módulos, consulte [Developing and publishing
modules](developing).

**Veja também**

* Se você está apenas querendo usar packages externos no seu código, certifique-se de
  consultar [Managing dependencies](/doc/modules/managing-dependencies).
* Com cada nova versão, você sinaliza as mudanças no seu módulo com seu
  número de versão. Para mais, consulte [Module version numbering](/doc/modules/version-numbers).

## Passos comuns do workflow {#common-steps}

A seguinte sequência ilustra passos de workflow de release e versionamento para um
novo módulo de exemplo. Para mais sobre cada passo, consulte as seções neste tópico.

1.  **Iniciar um módulo** e organizar seus sources para facilitar para desenvolvedores
    usarem e para você manter.

    Se você é completamente novo em desenvolver módulos, confira [Tutorial: Create a Go
    module](/doc/tutorial/create-module).

    No sistema de publicação de módulos descentralizado do Go, como você organiza seu código
    importa. Para mais, consulte [Managing module source](/doc/modules/managing-source).

1.  Configurar para **escrever código cliente local** que chama funções no
    módulo não publicado.

    Antes de você publicar um módulo, ele está indisponível para o workflow típico de gerenciamento de dependências
    usando comandos como `go get`. Uma boa maneira de testar seu
    código de módulo neste estágio é experimentá-lo enquanto ele está em um diretório local para
    seu código chamador.

    Consulte [Coding against an unpublished module](#unpublished) para mais sobre
    desenvolvimento local.

1.  Quando o código do módulo estiver pronto para outros desenvolvedores experimentarem,
    **começar a publicar pre-releases v0** como alphas e betas. Consulte
    [Publishing pre-release versions](#pre-release) para mais.

1.  **Lançar um v0** que não é garantido ser estável, mas que usuários podem experimentar.
    Para mais, consulte [Publishing the first (unstable) version](#first-unstable).

1.  Após sua versão v0 ser publicada, você pode (e deve!) continuar a
    **lançar novas versões** dela.

    Essas novas versões podem incluir correções de bugs (patch releases), adições à
    API pública do módulo (minor releases), e até mudanças breaking. Porque
    um release v0 não faz garantias de estabilidade ou compatibilidade retroativa, você
    pode fazer mudanças breaking em suas versões.

    Para mais, consulte [Publishing bug fixes](#bug-fixes) e [Publishing
    non-breaking API changes](#non-breaking).

1.  Quando você está preparando uma versão estável para release, você **publica
    pre-releases como alphas e betas**. Para mais, consulte [Publishing pre-release
    versions](#pre-release).

1.  Lançar um v1 como o **primeiro release estável**.

    Este é o primeiro release que faz compromissos sobre a
    estabilidade do módulo. Para mais, consulte [Publishing the first stable
    version](#first-stable).

1.  Na versão v1, **continuar a corrigir bugs** e, onde necessário, fazer
    adições à API pública do módulo.

    Para mais, consulte [Publishing bug fixes](#bug-fixes) e [Publishing
    non-breaking API changes](#non-breaking).

1.  Quando não puder ser evitado, publicar mudanças breaking em uma **nova versão major**.

    Uma atualização de versão major -- como de v1.x.x para v2.x.x -- pode ser uma
    atualização muito disruptiva para os usuários do seu módulo. Deve ser um último recurso. Para
    mais, consulte [Publishing breaking API changes](#breaking).

## Codificando contra um módulo não publicado {#unpublished}

Quando você começa a desenvolver um módulo ou uma nova versão de um módulo, você ainda não
terá publicado ele. Antes de publicar um módulo, você não será capaz de usar comandos
Go para adicionar o módulo como uma dependência. Em vez disso, no início, ao escrever
código cliente em um módulo diferente que chama funções no módulo não publicado,
você precisará referenciar uma cópia do módulo no sistema de arquivos local.

Você pode referenciar um módulo localmente do arquivo go.mod do módulo cliente usando
a diretiva `replace` no arquivo go.mod do módulo cliente. Para mais
informação, consulte [Requiring module code in a local
directory](managing-dependencies#local_directory).

## Publicando versões pre-release {#pre-release}

Você pode publicar versões pre-release para disponibilizar um módulo para outros
experimentarem e lhe darem feedback. Uma versão pre-release não inclui garantia de
estabilidade.

Números de versão pre-release são anexados com um identificador de pre-release. Para mais
sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

Aqui estão dois exemplos:

```
v0.2.1-beta.1
v1.2.3-alpha
```

Ao disponibilizar um pre-release, tenha em mente que desenvolvedores usando o
pre-release precisarão especificá-lo explicitamente por versão com o comando `go get`. Isso porque, por padrão, o comando `go` prefere versões de release
sobre versões pre-release ao localizar o módulo que você está pedindo. Então
desenvolvedores devem obter o pre-release especificando-o explicitamente, como no
exemplo a seguir:

```
go get example.com/theirmodule@v1.2.3-alpha
```

Você publica um pre-release tagueando o código do módulo no seu repositório,
especificando o identificador de pre-release na tag. Para mais, consulte [Publishing a
module](publishing).

## Publicando a primeira versão (instável) {#first-unstable}

Assim como quando você publica uma versão pre-release, você pode publicar versões de release que
não garantem estabilidade ou compatibilidade retroativa, mas dão aos seus usuários uma
oportunidade de experimentar o módulo e lhe dar feedback.

Releases instáveis são aqueles cujos números de versão estão no intervalo v0.x.x. Uma versão v0
não faz garantias de estabilidade ou compatibilidade retroativa. Mas ela lhe dá
uma maneira de obter feedback e refinar sua API antes de fazer compromissos de estabilidade
com v1 e posteriores. Para mais consulte, [Module version
numbering](version-numbers).

Assim como com outras versões publicadas, você pode incrementar as partes minor e patch do
número de versão v0 conforme você faz mudanças para lançar uma versão v1 estável.
Por exemplo, após lançar um v.0.0.0, você pode lançar um v0.0.1 com o
primeiro conjunto de correções de bugs.

Aqui está um exemplo de número de versão:

```
v0.1.3
```

Você publica um release instável tagueando o código do módulo no seu repositório,
especificando um número de versão v0 na tag. Para mais, consulte [Publishing a
module](publishing).

## Publicando a primeira versão estável {#first-stable}

Seu primeiro release estável terá um número de versão v1.x.x. O primeiro release estável
segue releases pre-release e v0 através dos quais você obteve feedback,
corrigiu bugs, e estabilizou o módulo para usuários.

Com um release v1, você está fazendo os seguintes compromissos com desenvolvedores usando
seu módulo:

* Eles podem atualizar para os releases minor e patch subsequentes da versão major
  sem quebrar seu próprio código.
* Você não fará mais mudanças na API pública do módulo -- incluindo
  suas assinaturas de função e método -- que quebrem compatibilidade retroativa.
* Você não removerá quaisquer tipos exportados, o que quebraria compatibilidade
  retroativa.
* Mudanças futuras à sua API (como adicionar um novo campo a uma struct) serão
  compatíveis retroativamente e serão incluídas em um novo release minor.
* Correções de bugs (como uma correção de segurança) serão incluídas em um patch release ou como
  parte de um release minor.

**Nota:** Embora sua primeira versão major possa ser um release v0, uma versão v0
não sinaliza garantias de estabilidade ou compatibilidade retroativa. Como resultado,
quando você incrementa de v0 para v1, você não precisa se preocupar em quebrar compatibilidade
retroativa porque o release v0 não foi considerado estável.

Para mais sobre números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

Aqui está um exemplo de um número de versão estável:

```
v1.0.0
```

Você publica um primeiro release estável tagueando o código do módulo no seu
repositório, especificando um número de versão v1 na tag. Para mais, consulte [Publishing
a module](publishing).

## Publicando correções de bugs {#bug-fixes}

Você pode publicar um release no qual as mudanças são limitadas a correções de bugs. Isso é
conhecido como um patch release.

Um _patch release_ inclui apenas mudanças menores. Em particular, não inclui
mudanças na API pública do módulo. Desenvolvedores de código consumidor podem atualizar para
esta versão com segurança e sem precisar mudar seu código.

**Nota:** Seu patch release deveria tentar não atualizar quaisquer das próprias
dependências transitivas daquele módulo em mais do que um patch release. Caso contrário, alguém
atualizando para o patch do seu módulo poderia acabar acidentalmente puxando uma
mudança mais invasiva para uma dependência transitiva que eles usam.

Um patch release incrementa a parte patch do número de versão do módulo. Para
mais consulte, [Module version numbering](/doc/modules/version-numbers).

No exemplo a seguir, v1.0.1 é um patch release.

Versão antiga: `v1.0.0`

Nova versão: `v1.0.1`

Você publica um patch release tagueando o código do módulo no seu repositório,
incrementando o número de versão patch na tag. Para mais, consulte [Publishing a
module](publishing).

## Publicando mudanças de API não-breaking {#non-breaking}

Você pode fazer mudanças não-breaking na API pública do seu módulo e publicar essas
mudanças em um release de versão _minor_.

Esta versão muda a API, mas não de uma maneira que quebra código chamador. Isso
pode incluir mudanças nas próprias dependências de um módulo ou a adição de novas
funções, métodos, campos de struct, ou tipos. Mesmo com as mudanças que inclui,
este tipo de release garante compatibilidade retroativa e estabilidade para
código existente que chama as funções do módulo.

Um release minor incrementa a parte minor do número de versão do módulo. Para
mais, consulte [Module version numbering](/doc/modules/version-numbers).

No exemplo a seguir, v1.1.0 é um release minor.

Versão antiga: `v1.0.1`

Nova versão: `v1.1.0`

Você publica um release minor tagueando o código do módulo no seu repositório,
incrementando o número de versão minor na tag. Para mais, consulte [Publishing a
module](publishing).

## Publicando mudanças de API breaking {#breaking}

Você pode publicar uma versão que quebra compatibilidade retroativa publicando um
release de versão _major_.

Um release de versão major não garante compatibilidade retroativa, tipicamente
porque inclui mudanças na API pública do módulo que quebrariam código
usando as versões anteriores do módulo.

Dado o efeito disruptivo que uma atualização de versão major pode ter em código que depende do
módulo, você deveria evitar uma atualização de versão major se puder. Para mais sobre
atualizações de versão major, consulte [Developing a major version update](/doc/modules/major-version).
Para estratégias para evitar fazer mudanças breaking, consulte o post do blog [Keeping your
modules compatible](/blog/module-compatibility).

Enquanto publicar outros tipos de versões requer essencialmente taguear o código do
módulo com o número de versão, publicar uma atualização de versão major requer mais
passos.

1.  Antes de começar o desenvolvimento da nova versão major, no seu repositório
    crie um lugar para o código-fonte da nova versão.

    Uma maneira de fazer isso é criar um novo branch no seu repositório que é
    especificamente para a nova versão major e seus releases minor e patch
    subsequentes. Para mais, consulte [Managing module source](/doc/modules/managing-source).

1.  No arquivo go.mod do módulo, revise o caminho do módulo para anexar o novo número de
    versão major, como no exemplo a seguir:

    ```
    example.com/mymodule/v2
    ```

    Dado que o caminho do módulo é o identificador do módulo, esta mudança
    efetivamente cria um novo módulo. Também muda o caminho do package, garantindo
    que desenvolvedores não importarão inadvertidamente uma versão que quebra seu
    código. Em vez disso, aqueles querendo atualizar explicitamente substituirão ocorrências
    do caminho antigo com o novo.

1.  No seu código, mude quaisquer caminhos de package onde você está importando packages no
    módulo que você está atualizando, incluindo packages no módulo que você está atualizando.
    Você precisa fazer isso porque você mudou o caminho do seu módulo.

1.  Como com qualquer novo release, você deveria publicar versões pre-release para obter
    feedback e relatórios de bugs antes de publicar um release oficial.

1.  Publique a nova versão major tagueando o código do módulo no seu repositório,
    incrementando o número de versão major na tag -- como de v1.5.2 para
    v2.0.0.

    Para mais, consulte [Publishing a module](/doc/modules/publishing).

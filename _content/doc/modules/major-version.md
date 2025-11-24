<!--{
  "Title": "Developing a major version update",
  "ia-translated": true
}-->

Você deve atualizar para uma versão major quando mudanças que você está fazendo em uma potencial nova
versão não podem garantir compatibilidade retroativa para os usuários do módulo. Por
exemplo, você fará esta mudança se alterar a API pública do seu módulo de tal forma
que quebre código cliente usando versões anteriores do módulo.

> **Nota:** Cada tipo de release -- major, minor, patch, ou pre-release -- tem um
significado diferente para os usuários de um módulo. Esses usuários confiam nessas diferenças para
entender o nível de risco que um release representa para seu próprio código. Em outras
palavras, ao preparar um release, certifique-se de que seu número de versão reflete com precisão
a natureza das mudanças desde o release anterior. Para mais sobre
números de versão, consulte [Module version numbering](/doc/modules/version-numbers).

**Veja também**

* Para uma visão geral do desenvolvimento de módulos, consulte [Developing and publishing
  modules](developing).
* Para uma visão end-to-end, consulte [Module release and versioning
  workflow](release-workflow).

## Considerações para uma atualização de versão major {#considerations}

Você deve apenas atualizar para uma nova versão major quando for absolutamente necessário.
Uma atualização de versão major representa uma agitação significativa tanto para você quanto para os
usuários do seu módulo. Ao considerar uma atualização de versão major, pense sobre
o seguinte:

* Seja claro com seus usuários sobre o que lançar a nova versão major significa
  para seu suporte de versões major anteriores.

  As versões anteriores são depreciadas? Suportadas como eram antes? Você estará
  mantendo versões anteriores, incluindo com correções de bugs?

* Esteja pronto para assumir a manutenção de duas versões: a antiga e a nova.
  Por exemplo, se você corrigir bugs em uma, você frequentemente estará portando essas correções para
  a outra.

* Lembre-se de que uma nova versão major é um novo módulo de uma perspectiva de gerenciamento de
  dependências. Seus usuários precisarão atualizar para usar um novo módulo após você
  lançar, em vez de simplesmente fazer upgrade.

  Isso porque uma nova versão major tem um caminho de módulo diferente da
  versão major anterior. Por exemplo, para um módulo cujo caminho de módulo é
  example.com/mymodule, uma versão v2 teria o caminho de módulo
  example.com/mymodule/v2.

* Quando você está desenvolvendo uma nova versão major, você também deve atualizar caminhos de import
  onde quer que o código importe packages do novo módulo. Os usuários do seu módulo também devem
  atualizar seus caminhos de import se quiserem fazer upgrade para a nova versão major.

## Ramificando para um release major {#branching}

A abordagem mais direta para lidar com código fonte ao preparar para desenvolver uma
nova versão major é ramificar o repositório na versão mais recente da
versão major anterior.

Por exemplo, em um prompt de comando você pode mudar para o diretório raiz do seu módulo,
depois criar um novo branch v2 lá.

```
$ cd mymodule
$ git checkout -b v2
Switched to a new branch "v2"
```

<img src="images/v2-branch-module.png"
     alt="Diagrama ilustrando um repositório ramificado de master para v2"
     style="width: 600px;" />


Uma vez que você tem o código fonte ramificado, você precisará fazer as seguintes mudanças no
código fonte para sua nova versão:

* No arquivo go.mod da nova versão, anexe o novo número de versão major ao
  caminho do módulo, como no exemplo a seguir:
  * Versão existente: `example.com/mymodule`
  * Nova versão: `example.com/mymodule/v2`

* No seu código Go, atualize cada caminho de package importado onde você importa um package
  do módulo, anexando o número de versão major à porção do caminho do módulo.
  * Antiga declaração import: `import "example.com/mymodule/package1"`
  * Nova declaração import: `import "example.com/mymodule/v2/package1"`

Para passos de publicação, consulte [Publishing a module](/doc/modules/publishing).

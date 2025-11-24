---
ia-translated: true
---
<!--{
  "Title": "Tutorial: Encontre e corrija dependências vulneráveis com VS Code Go",
  "Breadcrumb": true
}-->

[Voltar para Go Security](/security)

Você pode escanear seu código em busca de vulnerabilidades diretamente do seu editor com a extensão Go para Visual Studio Code.

Nota: para uma explicação da correção de vulnerabilidade incluída nas imagens abaixo, veja o [tutorial govulncheck](/doc/tutorial/govulncheck).

## Pré-requisitos:

- **Go.** Recomendamos usar a versão mais recente do Go para seguir este tutorial. Para instruções de instalação, veja [Instalando Go](/doc/install).
- **VS Code**, atualizado para a versão mais recente. [Download aqui](https://code.visualstudio.com/). Você também pode usar Vim (veja [aqui](/security/vuln/editor#editor-specific-instructions) para detalhes), mas este tutorial foca no VS Code Go.
- **Extensão VS Code Go**, que pode ser [baixada aqui](https://marketplace.visualstudio.com/items?itemName=golang.go).
- **Mudanças de configurações específicas do editor.** Você precisará modificar as configurações do seu IDE de acordo com [estas especificações](/security/vuln/editor#editor-specific-instructions) antes de conseguir replicar os resultados abaixo.


## Como escanear em busca de vulnerabilidades usando VS Code Go

**Passo 1.** Execute "Go: Toggle Vulncheck"

O comando [Toggle Vulncheck](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck) exibe análise de vulnerabilidade para todas as dependências listadas em seus módulos. Para usar este comando, abra a [paleta de comandos](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) no seu IDE (Ctrl+Shift+P no Linux/Windows ou Cmd+Shift+P no Mac OS) e execute "Go: Toggle Vulncheck." No seu arquivo go.mod, você verá os diagnósticos para dependências vulneráveis que são usadas tanto direta quanto indiretamente no seu código.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_1.png" alt="Run Toggle Vulncheck"></img>
  </center>
</div>

Nota: Para reproduzir este tutorial no seu próprio editor, copie o código abaixo no seu arquivo main.go.

```
// This program takes language tags as command-line
// arguments and parses them.

package main

import (
  "fmt"
  "os"

  "golang.org/x/text/language"
)

func main() {
  for _, arg := range os.Args[1:] {
    tag, err := language.Parse(arg)
    if err != nil {
      fmt.Printf("%s: error: %v\n", arg, err)
    } else if tag == language.Und {
      fmt.Printf("%s: undefined\n", arg)
    } else {
      fmt.Printf("%s: tag %s\n", arg, tag)
    }
  }
}
```

Então, certifique-se de que o arquivo go.mod correspondente para o programa fique assim:


```
module module1

go 1.18

require golang.org/x/text v0.3.5
```

Agora, execute `go mod tidy` para garantir que seu arquivo go.sum esteja atualizado.

**Passo 2.** Execute govulncheck via uma code action.

Executar govulncheck usando uma code action permite que você foque nas dependências que são realmente chamadas no seu código. Code actions no VS Code são marcadas por ícones de lâmpada; passe o mouse sobre a dependência relevante para ver informações sobre a vulnerabilidade, então selecione "Quick Fix" para ver um menu de opções. Destas, escolha "run govulncheck to verify." Isso retornará a saída relevante do govulncheck no seu terminal.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_2.png" alt="govulncheck code action"></img>
  </center>
</div>

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_3.png" alt="VS Code Go govulncheck output"></img>
  </center>
</div>

**Passo 3**. Passe o mouse sobre uma dependência listada no seu arquivo go.mod.

A saída relevante do govulncheck sobre uma dependência específica também pode ser encontrada passando o mouse sobre a dependência no arquivo go.mod. Para uma olhada rápida nas informações de dependência, esta opção é ainda mais eficiente do que usar uma code action.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_4.png" alt="Hover over dependency for vulnerability information"></img>
  </center>
</div>

**Passo 4.** Atualize para uma versão "fixed in" da sua dependência.

Code actions também podem ser usadas para atualizar rapidamente para uma versão da sua dependência onde a vulnerabilidade foi corrigida. Faça isso selecionando a opção "Upgrade" no menu suspenso de code action.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_5.png" alt="Upgrade to Latest via code action menu"></img>
  </center>
</div>


## Recursos adicionais

- Veja [esta página](/security/vuln/editor) para mais informações sobre escaneamento de vulnerabilidades no seu IDE. A [seção Notes and Caveats](/security/vuln/editor#notes-and-caveats), em particular, discute casos especiais para os quais o escaneamento de vulnerabilidades pode ser mais complexo do que no exemplo acima.
- O [Go Vulnerability Database](https://pkg.go.dev/vuln/) contém informações de muitas fontes existentes além de relatórios diretos por mantenedores de pacotes Go para a equipe de segurança do Go.
- Veja a página [Go Vulnerability Management](/security/vuln/) que fornece uma visão de alto nível da arquitetura do Go para detectar, relatar e gerenciar vulnerabilidades.

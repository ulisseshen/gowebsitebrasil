---
title: Vulnerability Scanning in IDEs
layout: article
ia-translated: true
---

[Voltar para Segurança do Go](/security)

Editores integrados com o [servidor de linguagem Go](https://pkg.go.dev/golang.org/x/tools/cmd/gopls), como [VS Code com a extensão Go](https://marketplace.visualstudio.com/items?itemName=golang.go), podem detectar vulnerabilidades em suas dependências.

Existem dois modos para detectar vulnerabilidades em dependências. Ambos são apoiados pelo [banco de dados de vulnerabilidades do Go](https://vuln.go.dev) e se complementam.

* Análise baseada em imports: neste modo, editores reportam vulnerabilidades escaneando o conjunto de packages importados no workspace, e mostram os achados como diagnósticos nos arquivos `go.mod`. Isso é rápido, mas pode reportar falsos positivos caso seu código importe os packages que contêm símbolos vulneráveis mas as funções com a vulnerabilidade não são alcançáveis. Este modo pode ser habilitado pela configuração gopls [`"vulncheck": "Imports"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#vulncheck-enum).
* Análise `Govulncheck`: esta é baseada na ferramenta de linha de comando [`govulncheck`](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck), que está embutida no `gopls`. Isso fornece uma maneira de baixo ruído e confiável para confirmar se seu código realmente invoca funções vulneráveis. Como esta análise pode ser cara para computar, ela deve ser disparada manualmente usando a code action "Run govulncheck to verify" associada aos relatórios de diagnóstico da análise baseada em Import, ou usando o code lens [`"codelenses.run_govulncheck"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#run-govulncheck) em arquivos `go.mod`.

<div style="text-align: center;"><img src="vscode.gif" alt="Vulncheck">

<em>Go: Toggle Vulncheck</em> <a
href="https://user-images.githubusercontent.com/4999471/206977512-a821107d-9ffb-4456-9b27-6a6a4f900ba6.mp4">(vulncheck.mp4)</a>
</div>

Essas funcionalidades estão disponíveis no `gopls` v0.11.0 ou mais recente. Por favor compartilhe seu feedback em [go.dev/s/vsc-vulncheck-feedback](/s/vsc-vulncheck-feedback).

## Instruções Específicas do Editor

### VS Code

A [extensão Go](https://marketplace.visualstudio.com/items?itemName=golang.go) oferece a integração com gopls. As seguintes configurações são necessárias para habilitar as funcionalidades de escaneamento de vulnerabilidade:

```
"go.diagnostic.vulncheck": "Imports", // habilita a análise baseada em imports por padrão.
"gopls": {
  "ui.codelenses": {
    "run_govulncheck": true  // code lens "Run govulncheck" no arquivo go.mod.
  }
}
```

O comando ["Go Toggle Vulncheck"](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck) pode ser usado para alternar a análise baseada em imports ligada e desligada para o workspace atual.

### Vim/NeoVim

Ao usar [coc.nvim](https://www.vim.org/scripts/script.php?script_id=5779), a seguinte configuração habilitará a análise baseada em import.

```
{
    "codeLens.enable": true,
    "languageserver": {
        "go": {
            "command": "gopls",
            ...
            "initializationOptions": {
                "vulncheck": "Imports",
            }
        }
    }
}
```

## Notas e Ressalvas

- A extensão não escaneia packages privados nem envia nenhuma informação sobre módulos privados. Toda a análise é feita puxando uma lista de módulos vulneráveis conhecidos do banco de dados de vulnerabilidades do Go e então computando a interseção localmente.
- A análise baseada em import usa a lista de packages nos módulos do workspace, que pode ser diferente do que você vê nos arquivos `go.mod` se `go.work` ou `replace`/`exclude` de módulo é usado.
- O resultado da análise govulncheck pode ficar desatualizado conforme você modifica o código ou o banco de dados de vulnerabilidades do Go é atualizado. Para invalidar os resultados da análise manualmente, use o codelens `"Reset go.mod diagnostics"` mostrado no topo do arquivo `go.mod`. Caso contrário, o resultado será automaticamente invalidado após uma hora.
- Essas funcionalidades atualmente não reportam vulnerabilidades nas bibliotecas padrão ou toolchains. Ainda estamos investigando UX sobre onde mostrar os achados e como ajudar usuários a lidar com os problemas.

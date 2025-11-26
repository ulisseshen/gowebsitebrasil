# Plano de Tradução 01: Documentação Core

> **Agente de Tradução:** Use o agente `.claude/agents/tradutor.md` para todas as traduções
>
> **Prioridade:** ALTA - Documentação essencial para desenvolvedores iniciantes

## Instruções de Uso

Para traduzir qualquer arquivo deste plano, execute:
```
@tradutor Traduza o arquivo [caminho-do-arquivo]
```

Após traduzir cada arquivo, marque o checkpoint com `[x]`.

---

## Seção 1: Páginas Principais (doc/)

### 1.1 Páginas de Entrada
- [ ] `_content/doc/index.html` - Página principal da documentação
- [ ] `_content/doc/install.html` - Instalação do Go
- [ ] `_content/doc/manage-install.html` - Gerenciar instalações
- [ ] `_content/doc/code.html` - Como escrever código Go
- [ ] `_content/doc/effective_go.html` - Effective Go (IMPORTANTE)
- [ ] `_content/doc/faq.md` - Perguntas frequentes
- [ ] `_content/doc/go_faq.md` - FAQ adicional
- [ ] `_content/doc/help.md` - Página de ajuda

### 1.2 Referência e Compatibilidade
- [ ] `_content/doc/go1compat.html` - Promessa de compatibilidade Go 1
- [ ] `_content/doc/cmd.html` - Documentação de comandos
- [ ] `_content/doc/editors.html` - Editores e IDEs
- [ ] `_content/doc/diagnostics.html` - Diagnósticos
- [ ] `_content/doc/gc-guide.html` - Guia do Garbage Collector
- [ ] `_content/doc/toolchain.md` - Toolchain

### 1.3 Contribuição e Comunidade
- [ ] `_content/doc/conduct.md` - Código de conduta
- [ ] `_content/doc/contribute.html` - Como contribuir
- [ ] `_content/doc/contrib.md` - Contribuição adicional
- [ ] `_content/doc/copyright.md` - Copyright
- [ ] `_content/doc/tos.html` - Termos de serviço

---

## Seção 2: Tutoriais (doc/tutorial/)

### 2.1 Getting Started (HTML)
- [x] `_content/doc/tutorial/index.html` - Índice de tutoriais
- [x] `_content/doc/tutorial/getting-started.html` - Começando com Go
- [x] `_content/doc/tutorial/create-module.html` - Criar um módulo
- [x] `_content/doc/tutorial/call-module-code.html` - Chamar código de módulo
- [x] `_content/doc/tutorial/handle-errors.html` - Tratar erros
- [x] `_content/doc/tutorial/random-greeting.html` - Saudação aleatória
- [x] `_content/doc/tutorial/greetings-multiple-people.html` - Múltiplas saudações
- [x] `_content/doc/tutorial/add-a-test.html` - Adicionar um teste
- [x] `_content/doc/tutorial/compile-install.html` - Compilar e instalar
- [x] `_content/doc/tutorial/module-conclusion.html` - Conclusão do módulo

### 2.2 Tutoriais Avançados (Markdown)
- [x] `_content/doc/tutorial/database-access.md` - Acesso a banco de dados
- [x] `_content/doc/tutorial/web-service-gin.md` - Web service com Gin
- [x] `_content/doc/tutorial/generics.md` - Generics
- [x] `_content/doc/tutorial/fuzz.md` - Fuzzing
- [x] `_content/doc/tutorial/workspaces.md` - Workspaces
- [x] `_content/doc/tutorial/govulncheck.md` - Govulncheck
- [x] `_content/doc/tutorial/govulncheck-ide.md` - Govulncheck no IDE

---

## Seção 3: Banco de Dados (doc/database/)

- [x] `_content/doc/database/index.md` - Índice de banco de dados
- [x] `_content/doc/database/open-handle.md` - Abrir conexão
- [x] `_content/doc/database/querying.md` - Consultas
- [x] `_content/doc/database/change-data.md` - Modificar dados
- [x] `_content/doc/database/prepared-statements.md` - Prepared statements
- [x] `_content/doc/database/execute-transactions.md` - Transações
- [x] `_content/doc/database/cancel-operations.md` - Cancelar operações
- [x] `_content/doc/database/manage-connections.md` - Gerenciar conexões
- [x] `_content/doc/database/sql-injection.md` - SQL Injection

---

## Seção 4: Módulos (doc/modules/)

- [x] `_content/doc/modules/managing-dependencies.md` - Gerenciar dependências
- [x] `_content/doc/modules/developing.md` - Desenvolver módulos
- [x] `_content/doc/modules/publishing.md` - Publicar módulos
- [x] `_content/doc/modules/version-numbers.md` - Números de versão
- [x] `_content/doc/modules/major-version.md` - Versões major
- [x] `_content/doc/modules/release-workflow.md` - Workflow de release
- [x] `_content/doc/modules/managing-source.md` - Gerenciar código fonte
- [x] `_content/doc/modules/layout.md` - Layout de módulos
- [x] `_content/doc/modules/pruning.md` - Pruning
- [x] `_content/doc/modules/gomod-ref.md` - Referência go.mod

---

## Seção 5: Segurança (doc/security/)

### 5.1 Páginas Principais
- [ ] `_content/doc/security/index.md` - Índice de segurança
- [ ] `_content/doc/security/best-practices.md` - Melhores práticas
- [ ] `_content/doc/security/policy.md` - Política de segurança
- [ ] `_content/doc/security/fips140.md` - FIPS 140
- [ ] `_content/doc/security/vulncheck.md` - Vulncheck

### 5.2 Fuzzing
- [ ] `_content/doc/security/fuzz/index.md` - Fuzzing - Índice
- [ ] `_content/doc/security/fuzz/technical.md` - Fuzzing - Técnico

### 5.3 Vulnerabilidades
- [ ] `_content/doc/security/vuln/index.md` - Vulnerabilidades - Índice
- [ ] `_content/doc/security/vuln/database.md` - Banco de vulnerabilidades
- [ ] `_content/doc/security/vuln/vulncheck.md` - Vulncheck detalhado
- [ ] `_content/doc/security/vuln/editor.md` - Editor
- [ ] `_content/doc/security/vuln/cna.md` - CNA

### 5.4 Banco de Vulnerabilidades
- [ ] `_content/doc/security/vulndb/index.md` - VulnDB - Índice
- [ ] `_content/doc/security/vulndb/policy.md` - VulnDB - Política
- [ ] `_content/doc/security/vulndb/api.md` - VulnDB - API

---

## Seção 6: Artigos (doc/articles/)

- [ ] `_content/doc/articles/index.html` - Índice de artigos
- [ ] `_content/doc/articles/go_command.html` - Comando go
- [ ] `_content/doc/articles/race_detector.html` - Race detector
- [ ] `_content/doc/articles/wiki/index.html` - Wiki - Índice
- [ ] `_content/doc/articles/wiki/view.html` - Wiki - View
- [ ] `_content/doc/articles/wiki/edit.html` - Wiki - Edit

---

## Seção 7: Instalação e Desenvolvimento

### 7.1 Instalação
- [x] `_content/doc/install/source.html` - Instalação do fonte (813 linhas)
- [ ] `_content/doc/install/gccgo.html` - GCC Go
- [ ] `_content/doc/install-source.md` - Fonte adicional
- [ ] `_content/doc/gccgo_install.md` - Instalação GCC Go

### 7.2 Desenvolvimento
- [ ] `_content/doc/devel/release.html` - Releases
- [ ] `_content/doc/devel/weekly.html` - Weekly builds
- [ ] `_content/doc/devel/pre_go1.html` - Pré Go 1
- [ ] `_content/doc/gccgo_contribute.html` - Contribuir GCC Go

### 7.3 Debugging
- [x] `_content/doc/debugging_with_gdb.md` - Debugging com GDB (redirect)
- [x] `_content/doc/gdb.html` - GDB

### 7.4 Outros
- [x] `_content/doc/gopath_code.html` - GOPATH (redirect)
- [x] `_content/doc/comment.md` - Comentários
- [x] `_content/doc/fuzz.md` - Fuzzing
- [x] `_content/doc/pgo.md` - Profile-Guided Optimization
- [x] `_content/doc/telemetry.md` - Telemetria
- [x] `_content/doc/build-cover.md` - Build coverage
- [x] `_content/doc/go-get-install-deprecation.md` - Deprecação go get
- [x] `_content/doc/docs.md` - Docs (redirect)
- [x] `_content/doc/next.md` - Next
- [x] `_content/doc/root.md` - Root (redirect)
- [x] `_content/doc/gopher/index.md` - Gopher (redirect)

---

## Seção 8: Release Notes (doc/go1.x.md)

### 8.1 Versões Recentes (Prioridade Alta)
- [ ] `_content/doc/go1.26.md` - Go 1.26
- [ ] `_content/doc/go1.25.md` - Go 1.25
- [ ] `_content/doc/go1.24.md` - Go 1.24
- [ ] `_content/doc/go1.23.md` - Go 1.23
- [ ] `_content/doc/go1.22.md` - Go 1.22
- [ ] `_content/doc/go1.21.md` - Go 1.21
- [ ] `_content/doc/go1.20.md` - Go 1.20

### 8.2 Versões Intermediárias
- [ ] `_content/doc/go1.19.md` - Go 1.19
- [ ] `_content/doc/go1.18.md` - Go 1.18
- [ ] `_content/doc/go1.17.md` - Go 1.17
- [ ] `_content/doc/go1.16.md` - Go 1.16
- [ ] `_content/doc/go1.15.md` - Go 1.15
- [ ] `_content/doc/go1.14.md` - Go 1.14
- [ ] `_content/doc/go1.13.md` - Go 1.13
- [ ] `_content/doc/go1.12.md` - Go 1.12
- [ ] `_content/doc/go1.11.md` - Go 1.11
- [ ] `_content/doc/go1.10.md` - Go 1.10

### 8.3 Versões Antigas
- [ ] `_content/doc/go1.9.md` - Go 1.9
- [ ] `_content/doc/go1.8.md` - Go 1.8
- [ ] `_content/doc/go1.7.md` - Go 1.7
- [ ] `_content/doc/go1.6.md` - Go 1.6
- [ ] `_content/doc/go1.5.md` - Go 1.5
- [ ] `_content/doc/go1.4.md` - Go 1.4
- [ ] `_content/doc/go1.3.md` - Go 1.3
- [ ] `_content/doc/go1.2.md` - Go 1.2
- [ ] `_content/doc/go1.1.md` - Go 1.1
- [ ] `_content/doc/go1.md` - Go 1.0

---

## Progresso

| Seção | Total | Traduzidos | Progresso |
|-------|-------|------------|-----------|
| Páginas Principais | 14 | 0 | 0% |
| Tutoriais | 17 | 0 | 0% |
| Banco de Dados | 9 | 0 | 0% |
| Módulos | 10 | 0 | 0% |
| Segurança | 15 | 0 | 0% |
| Artigos | 6 | 0 | 0% |
| Instalação/Dev | 17 | 0 | 0% |
| Release Notes | 27 | 0 | 0% |
| **TOTAL** | **115** | **0** | **0%** |

---

## Notas

- Comece pelos tutoriais e páginas principais
- Release notes podem ser traduzidas em lotes
- Effective Go é um documento extenso - reserve tempo adequado
- Mantenha consistência com termos técnicos em inglês

---
title: Security
layout: article
ia-translated: true
---

Esta página fornece recursos para desenvolvedores Go melhorarem a segurança de seus
projetos.

(Veja também: [Melhores Práticas de Segurança para Desenvolvedores Go](/security/best-practices).)

## Encontrar e corrigir vulnerabilidades conhecidas

A detecção de vulnerabilidades do Go visa fornecer ferramentas de baixo ruído e confiáveis para
desenvolvedores aprenderem sobre vulnerabilidades conhecidas que podem afetar seus projetos.
Para uma visão geral, comece nesta [página de resumo e FAQ](/security/vuln)
sobre a arquitetura de gerenciamento de vulnerabilidades do Go. Para uma abordagem aplicada,
explore as ferramentas abaixo.

### Escanear código para vulnerabilidades com govulncheck

Desenvolvedores podem usar a ferramenta govulncheck para determinar se alguma
vulnerabilidade conhecida afeta seu código e priorizar próximos passos com base em quais funções e
métodos vulneráveis são realmente chamados.

- [Ver a documentação do govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [Tutorial: Get started with govulncheck](/doc/tutorial/govulncheck)

### Detectar vulnerabilidades do seu editor

A extensão VS Code Go verifica dependências de terceiros e exibe vulnerabilidades relevantes.

- [Documentação do usuário](/security/vuln/editor)
- [Baixar VS Code Go](https://marketplace.visualstudio.com/items?itemName=golang.go)
- [Tutorial: Get started with VS Code Go](/doc/tutorial/govulncheck-ide)

### Encontrar módulos Go para construir

[Pkg.go.dev](https://pkg.go.dev/) é um site para descobrir, avaliar e
aprender mais sobre packages e módulos Go. Ao descobrir e avaliar
packages no pkg.go.dev, você verá
[um banner no topo da página](https://pkg.go.dev/golang.org/x/text@v0.3.7/language)
se houver vulnerabilidades naquela versão. Além disso, você pode ver as
[vulnerabilidades impactando cada versão de um package](https://pkg.go.dev/golang.org/x/text@v0.3.7/language?tab=versions)
na página de histórico de versões.

### Navegar pelo banco de dados de vulnerabilidades

O banco de dados de vulnerabilidades do Go coleta dados diretamente de mantenedores de packages Go
bem como de fontes externas como [MITRE](https://www.cve.org/) e [GitHub](https://github.com/). Relatórios
são curados pela equipe de Segurança do Go.

- [Navegar relatórios no banco de dados de vulnerabilidades do Go](https://pkg.go.dev/vuln/)
- [Ver a documentação do Banco de Dados de Vulnerabilidades do Go](/security/vuln/database)
- [Contribuir uma vulnerabilidade pública para o banco de dados](/s/vulndb-report-new)


## Reportar bugs de segurança no projeto Go

### [Política de Segurança](/security/policy)

Consulte a Política de Segurança para instruções sobre como
[reportar uma vulnerabilidade no projeto Go](/security/policy#reporting-a-security-bug).
A página também detalha o processo da equipe de segurança do Go de rastrear problemas e
divulgá-los ao público. Consulte o
[histórico de releases](/doc/devel/release) para detalhes sobre correções de segurança
passadas. De acordo com a [política de release](/doc/devel/release#policy),
emitimos correções de segurança para as duas versões major mais recentes do Go.

## Testar entradas inesperadas com fuzzing

Fuzzing nativo do Go fornece um tipo de teste automatizado que continuamente
manipula entradas para um programa para encontrar bugs. Go suporta fuzzing em sua
toolchain padrão começando no Go 1.18. Testes de fuzz nativos do Go são
[suportados pelo OSS-Fuzz](https://google.github.io/oss-fuzz/getting-started/new-project-guide/go-lang/#native-go-fuzzing-support).

- [Revisar os fundamentos de fuzzing](/security/fuzz)
- [Tutorial: Get started with fuzzing](/doc/tutorial/fuzz)

## Serviços seguros com bibliotecas de criptografia do Go

As bibliotecas de criptografia do Go visam ajudar desenvolvedores a construir aplicações seguras.
Consulte a documentação para os [packages crypto](https://pkg.go.dev/golang.org/x/crypto)
e [golang.org/x/crypto/](https://pkg.go.dev/golang.org/x/crypto).

## Criptografia compatível com FIPS 140-3

As bibliotecas de criptografia do Go podem ser usadas em um modo compatível com FIPS 140-3 para uso
em ambientes regulados. Consulte a documentação de [Conformidade FIPS 140-3](/doc/security/fips140)
para mais informações.

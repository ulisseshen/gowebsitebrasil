---
title: Go CNA Policy
layout: article
ia-translated: true
---

[Voltar para Gerenciamento de Vulnerabilidades do Go](/security/vuln)

## Visão Geral

A CNA do Go é uma
[CVE Numbering Authority](https://www.cve.org/ProgramOrganization/CNAs), que emite
[IDs CVE](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryCVEID) e publica
[Registros CVE](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryRecord)
para vulnerabilidades públicas no ecossistema Go. É uma sub-CNA da CNA do Google.

## Escopo

A CNA do Go cobre vulnerabilidades no projeto Go (a
[biblioteca padrão](/pkg) do Go e
[sub-repositórios](https://pkg.go.dev/golang.org/x)) e vulnerabilidades públicas
em módulos Go importáveis que ainda não são cobertos por outra CNA.

Este escopo destina-se a excluir explicitamente vulnerabilidades em aplicações ou
packages escritos em Go que não são importáveis (por exemplo, qualquer coisa no
package `main`). Veja [go.dev/security/vuln/database#excluded-reports](/security/vuln/database#excluded-reports) para mais informações sobre relatórios excluídos.

Para reportar potenciais novas vulnerabilidades no projeto Go, consulte
[go.dev/security/policy](/security/policy).

## Solicitando um ID CVE para uma vulnerabilidade pública

**IMPORTANTE**: O formulário vinculado abaixo cria um issue público no rastreador de issues, e portanto
*não deve* ser usado para reportar vulnerabilidades não divulgadas em Go (veja nossa
[política de segurança](/security/policy) para instruções sobre como reportar
problemas não divulgados).

Para solicitar um ID CVE para uma vulnerabilidade PÚBLICA existente no ecossistema Go,
[envie uma solicitação via este formulário](/s/vulndb-report-new).

Uma vulnerabilidade é considerada pública se já foi divulgada publicamente, ou existe em um
package que você mantém, e você está pronto para divulgá-la publicamente.

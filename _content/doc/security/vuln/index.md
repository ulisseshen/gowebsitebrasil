---
title: Go Vulnerability Management
layout: article
ia-translated: true
---

[Voltar para Segurança do Go](/security)

## Visão Geral

Go ajuda desenvolvedores a detectar, avaliar e resolver erros ou fraquezas que estão
em risco de serem explorados por atacantes. Nos bastidores, a equipe Go executa um
pipeline para curar relatórios sobre vulnerabilidades, que são armazenados no
banco de dados de vulnerabilidades do Go. Várias bibliotecas e ferramentas podem ler e analisar esses
relatórios para entender como projetos específicos de usuários podem ser afetados. Esta
funcionalidade está integrada no
[site de descoberta de packages Go](https://pkg.go.dev) e uma nova ferramenta CLI,
govulncheck.

Este projeto é um trabalho em andamento e sob desenvolvimento ativo.
Agradecemos seu [feedback](#feedback) para nos ajudar a melhorar!

**NOTA**: Para reportar uma vulnerabilidade no projeto Go, por favor veja a [Política de Segurança do Go](/security/policy).

## Arquitetura

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="architecture.png" alt="Go Vulnerability Management Architecture"></img>
  </center>
</div>

O gerenciamento de vulnerabilidades no Go consiste das seguintes peças de alto nível:

1. Um **pipeline de dados** coleta informações de vulnerabilidade de várias fontes,
incluindo o [National Vulnerability Database (NVD)](https://nvd.nist.gov/),
o [GitHub Advisory Database](https://github.com/advisories),
e [diretamente de mantenedores de packages Go](/s/vulndb-report-new).
2. Um **banco de dados de vulnerabilidades** é populado com relatórios usando informações
do pipeline de dados.
Todos os relatórios no banco de dados são revisados e curados pela equipe de Segurança do Go.
Relatórios são formatados no [formato Open Source Vulnerability (OSV)](https://ossf.github.io/osv-schema/)
e acessíveis através da [API](/security/vuln/database#api).
3. **Integrações** com [pkg.go.dev](https://pkg.go.dev)
e govulncheck para permitir que desenvolvedores encontrem vulnerabilidades em
seus projetos. O
[comando govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
analisa sua codebase e apenas exibe vulnerabilidades que realmente afetam
você, baseado em quais funções no seu código estão transitivamente chamando funções
vulneráveis. Govulncheck fornece uma maneira de baixo ruído e confiável para encontrar
vulnerabilidades conhecidas em seus projetos.

## Recursos

### Banco de Dados de Vulnerabilidades do Go

O [banco de dados de vulnerabilidades do Go](https://vuln.go.dev) contém informações
de muitas fontes existentes além de relatórios diretos de mantenedores de packages Go
para a equipe de segurança do Go.
Cada entrada no banco de dados é revisada para garantir que a descrição da vulnerabilidade,
informações de package e símbolos, e detalhes de versão estejam precisos.

Veja [go.dev/security/vuln/database](/security/vuln/database) para mais informações
sobre o banco de dados de vulnerabilidades do Go,
e [pkg.go.dev/vuln](https://pkg.go.dev/vuln) para visualizar vulnerabilidades no
banco de dados em seu navegador.

Encorajamos mantenedores de packages a [contribuir](#feedback)
informações sobre vulnerabilidades públicas em seus próprios projetos e
[nos enviar sugestões](/s/vuln-feedback) sobre como reduzir
fricção.

### Detecção de Vulnerabilidades para Go

A detecção de vulnerabilidades do Go visa fornecer uma maneira de baixo ruído e confiável para
usuários Go aprenderem sobre vulnerabilidades conhecidas que podem afetar seus projetos.
A verificação de vulnerabilidades está integrada nas ferramentas e serviços do Go, incluindo
uma nova ferramenta de linha de comando, [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck),
o [site de descoberta de packages Go](https://pkg.go.dev), [editores principais](/security/vuln/editor) como VS Code com a extensão Go.

Para começar a usar govulncheck, execute o seguinte do seu projeto:

```
$ go install golang.org/x/vuln/cmd/govulncheck@latest
$ govulncheck ./...
```

Para habilitar detecção de vulnerabilidades no seu editor, veja as instruções na página de [integração com editor](/security/vuln/editor).

### Go CNA

A equipe de segurança do Go é uma [CVE Numbering Authority](https://www.cve.org/ProgramOrganization/CNAs).
Veja [go.dev/security/vuln/cna](/security/vuln/cna) para mais informações.

## Feedback

Adoraríamos que você contribuísse e nos ajudasse a fazer melhorias das
seguintes maneiras:

- [Contribuir novas](/s/vulndb-report-new) e
  [atualizar existentes](/s/vulndb-report-feedback) informações sobre
  vulnerabilidades públicas para packages Go que você mantém
- [Faça esta pesquisa](/s/govulncheck-feedback) para compartilhar sua
  experiência usando govulncheck
- [Envie-nos feedback](/s/vuln-feedback) sobre problemas e
  solicitações de recursos

## FAQs

**Como reporto uma vulnerabilidade no projeto Go?**

Reporte todos os bugs de segurança no projeto Go por email para [security@golang.org](mailto:security@golang.org).
Leia a [Política de Segurança do Go](/security/policy) para mais informações sobre nossos processos.

**Como adiciono uma vulnerabilidade pública ao banco de dados de vulnerabilidades do Go?**

Para solicitar a adição de uma vulnerabilidade pública ao banco de dados de vulnerabilidades do Go,
[preencha este formulário](/s/vulndb-report-new).

Uma vulnerabilidade é considerada pública se já foi divulgada publicamente,
ou se existe em um package que você mantém (e você está pronto para divulgá-la).
O formulário é apenas para vulnerabilidades públicas em packages Go importáveis que
não são mantidos pela Equipe Go (qualquer coisa fora da biblioteca padrão Go,
toolchain Go, e módulos golang.org).

O formulário também pode ser usado para solicitar um novo ID CVE.
[Leia mais aqui](/security/vuln/cna) sobre a CVE Numbering Authority do Go.

**Como sugiro uma edição a uma vulnerabilidade?**

Para sugerir uma edição a um relatório existente no banco de dados de vulnerabilidades do Go,
[preencha o formulário aqui](/s/vulndb-report-feedback).

**Como reporto um problema ou dou feedback sobre govulncheck?**

Envie seu problema ou feedback [no rastreador de issues do Go](/s/vuln-feedback).

**Encontrei esta vulnerabilidade em outro banco de dados. Por que não está no banco de dados de vulnerabilidades do Go?**

Relatórios podem ser excluídos do banco de dados de vulnerabilidades do Go por várias razões,
incluindo a vulnerabilidade relevante não estar presente em um package Go,
a vulnerabilidade estar em um comando instalável ao invés de um package importável,
ou a vulnerabilidade ser subsumida por outra vulnerabilidade que já está
presente no banco de dados.
Você pode aprender mais sobre as
[razões da equipe de Segurança do Go para excluir relatórios aqui](/security/vuln/database#excluded-reports).
Se você acha que um relatório foi incorretamente excluído do vuln.go.dev,
[por favor nos avise](/s/vulndb-report-feedback).

**Por que o banco de dados de vulnerabilidades do Go não usa rótulos de severidade?**

A maioria dos formatos de relatório de vulnerabilidade usa rótulos de severidade como "LOW", "MEDIUM",
e "CRITICAL" para indicar o impacto de diferentes vulnerabilidades e
para ajudar desenvolvedores a priorizar problemas de segurança.
Por várias razões, no entanto, Go evita usar tais rótulos.

O impacto de uma vulnerabilidade raramente é universal,
o que significa que indicadores de severidade podem frequentemente ser enganosos.
Por exemplo, um crash em um parser pode ser um problema de severidade crítica se ele
é usado para analisar entrada fornecida pelo usuário e pode ser aproveitado em um ataque DoS,
mas se o parser é usado para analisar arquivos de configuração locais,
mesmo chamar a severidade de "baixa" pode ser um exagero.

Rotular severidade também é necessariamente subjetivo.
Isso é verdade mesmo para [o programa CVE](https://www.cve.org/About/Overview),
que postula uma fórmula para decompor aspectos relevantes de uma vulnerabilidade,
como vetor de ataque, complexidade e explorabilidade.
Todos esses, no entanto, requerem avaliação subjetiva.

Acreditamos que boas descrições de vulnerabilidades são mais úteis que indicadores de severidade.
Uma boa descrição pode decompor o que é um problema,
como ele pode ser disparado, e o que os consumidores devem considerar ao determinar
o impacto em seu próprio software.

Sinta-se à vontade para [abrir um issue](/s/vuln-feedback)
se você gostaria de compartilhar seus pensamentos conosco sobre este tópico.

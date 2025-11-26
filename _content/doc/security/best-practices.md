---
title: Security Best Practices for Go Developers
layout: article
ia-translated: true
---

[Voltar para Segurança do Go](/security)

Esta página fornece aos desenvolvedores Go melhores práticas para priorizar a
segurança de seus projetos. De automatizar testes com fuzzing a facilmente
verificar condições de corrida, essas dicas podem ajudar a tornar sua codebase mais
segura e confiável.

## Escanear código-fonte e binários para vulnerabilidades

Escanear regularmente seu código e binários para vulnerabilidades ajuda a identificar
riscos de segurança potenciais precocemente.
Você pode usar [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck),
apoiado pelo [banco de dados de vulnerabilidades do Go](https://pkg.go.dev),
para escanear seu código para vulnerabilidades e analisar quais realmente afetam você.
Comece com [o tutorial do govulncheck](/doc/tutorial/govulncheck).

Govulncheck também pode ser integrado em fluxos de CI/CD.
A equipe Go fornece uma
[GitHub Action para govulncheck](https://github.com/marketplace/actions/golang-govulncheck-action)
no GitHub Marketplace.
Govulncheck também suporta uma flag `-json` para ajudar desenvolvedores a integrar escaneamento de vulnerabilidades
com outros sistemas de CI/CD.

Você também pode escanear vulnerabilidades diretamente no seu editor de código usando
a [extensão Go para Visual Studio Code](/security/vuln/editor).
Comece com [este tutorial](/doc/tutorial/govulncheck-ide).

## Manter sua versão do Go e dependências atualizadas

Manter sua [versão do Go atualizada](/doc/install) oferece
acesso aos recursos de linguagem mais recentes,
melhorias de desempenho e patches para vulnerabilidades de segurança conhecidas.
Uma versão atualizada do Go também garante compatibilidade com versões mais recentes de dependências,
ajudando a evitar possíveis problemas de integração.
Revise o [histórico de releases do Go](/doc/devel/release) para ver
quais mudanças foram feitas no Go entre releases.
A equipe Go emite releases pontuais durante o ciclo de release para tratar bugs de segurança.
Certifique-se de atualizar para a versão minor mais recente do Go para garantir que você tenha as
correções de segurança mais recentes.

Manter dependências de terceiros atualizadas também é crucial para segurança de software,
desempenho, e conformidade com os padrões mais recentes no ecossistema Go.
No entanto, atualizar para as versões mais recentes sem revisão completa
[também pode ser arriscado](https://research.swtch.com/npm-colors),
potencialmente introduzindo novos bugs, mudanças incompatíveis,
ou até código malicioso.
Portanto, embora seja essencial atualizar dependências para os patches de segurança
e melhorias mais recentes,
cada atualização deve ser cuidadosamente revisada e testada.

## Testar com fuzzing para descobrir explorações de casos extremos

[Fuzzing](/security/fuzz) é um tipo de teste automatizado que
usa orientação de cobertura para manipular entradas aleatórias e percorrer código
para encontrar e reportar vulnerabilidades potenciais como injeções SQL,
estouros de buffer, negação de serviço e ataques de cross-site scripting.
Fuzzing pode frequentemente alcançar casos extremos que programadores perdem,
ou consideram muito improváveis para testar.
Comece com [este tutorial](/doc/tutorial/fuzz).

## Verificar condições de corrida com o race detector do Go

Condições de corrida ocorrem quando duas ou mais [goroutines](/tour/concurrency/1)
acessam o mesmo recurso concorrentemente,
e pelo menos um desses acessos é uma escrita.
Isso pode levar a problemas imprevisíveis e difíceis de diagnosticar no seu software.
Identifique condições de corrida potenciais no seu código Go usando o
[race detector](/doc/articles/race_detector) integrado,
que pode ajudá-lo a garantir a segurança e confiabilidade dos seus programas concorrentes.
O race detector encontra corridas que ocorrem em tempo de execução,
no entanto, então ele não encontrará corridas em caminhos de código que não são executados.

Para usar o race detector, adicione a flag `-race` ao executar seus testes ou
construir sua aplicação,
por exemplo, `go test -race`.
Isso compilará seu código com o race detector habilitado e reportará quaisquer
condições de corrida que detectar em tempo de execução.
Quando o race detector encontra uma corrida de dados no programa, ele
[imprimirá um relatório](/doc/articles/race_detector#report-format)
contendo stack traces para acessos conflitantes,
e stacks onde as goroutines envolvidas foram criadas.

## Usar Vet para examinar construções suspeitas

O [comando vet](https://pkg.go.dev/cmd/vet) do Go é projetado para analisar
seu código-fonte e sinalizar problemas potenciais que podem não necessariamente ser erros de sintaxe,
mas poderiam levar a problemas durante o tempo de execução.
Estes incluem construções suspeitas, como código inalcançável,
variáveis não usadas, e erros comuns em torno de goroutines.
Ao detectar esses problemas precocemente no processo de desenvolvimento,
go vet ajuda a manter a qualidade do código, reduz o tempo de depuração,
e melhora a confiabilidade geral do software.
Para executar go vet para um projeto especificado, execute:

```
go vet ./...
```

## Inscrever-se em golang-announce para notificação de releases de segurança

Releases do Go contendo correções de segurança são pré-anunciados para a lista de
e-mails de baixo volume [golang-announce@googlegroups.com](https://groups.google.com/group/golang-announce).
Se você quer saber quando correções de segurança para o próprio Go estão a caminho, inscreva-se.

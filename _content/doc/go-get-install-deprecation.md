<!--{
  "ia-translated": true,
  "Title": "Deprecação do 'go get' para instalar executáveis",
  "Path": "/doc/go-get-install-deprecation",
  "Breadcrumb": true
}-->

## Visão Geral

A partir do Go 1.17, instalar executáveis com `go get` está deprecated.
`go install` pode ser usado em vez disso.

No Go 1.18, `go get` não construirá mais packages; ele será usado apenas
para adicionar, atualizar ou remover dependências em `go.mod`. Especificamente,
`go get` sempre agirá como se a flag `-d` estivesse habilitada.

## O que usar em vez disso

Para instalar um executável no contexto do módulo atual, use `go install`,
sem um sufixo de versão, como abaixo. Isso aplica requisitos de versão e
outras diretivas do arquivo `go.mod` no diretório atual ou um diretório
pai.

```
go install example.com/cmd
```

Para instalar um executável ignorando o módulo atual, use `go install`
*com* um [sufixo de versão](/ref/mod#version-queries) como `@v1.2.3` ou `@latest`,
como abaixo. Quando usado com um sufixo de versão, `go install` não lê ou atualiza
o arquivo `go.mod` no diretório atual ou um diretório pai.

```
# Instalar uma versão específica.
go install example.com/cmd@v1.2.3

# Instalar a versão mais alta disponível.
go install example.com/cmd@latest
```

Para evitar ambiguidade, quando `go install` é usado com um sufixo de versão,
todos os argumentos devem referir-se a packages `main` no mesmo módulo na mesma
versão. Se aquele módulo tem um arquivo `go.mod`, ele não deve conter diretivas como
`replace` ou `exclude` que fariam com que ele fosse interpretado diferentemente se
fosse o módulo principal. O diretório `vendor` do módulo não é usado.

Veja [`go install`](/ref/mod#go-install) para detalhes.

## Por que isso está acontecendo

Desde que os módulos foram introduzidos, o comando `go get` tem sido usado tanto para atualizar
dependências em `go.mod` quanto para instalar comandos. Esta combinação é frequentemente
confusa e inconveniente: na maioria dos casos, desenvolvedores querem atualizar uma
dependência ou instalar um comando, mas não ambos ao mesmo tempo.

Desde o Go 1.16, `go install` pode instalar um comando em uma versão especificada na
linha de comando enquanto ignora o arquivo `go.mod` no diretório atual (se houver
um). `go install` agora deve ser usado para instalar comandos na maioria dos casos.

A capacidade do `go get` de construir e instalar comandos está agora deprecated, já que essa
funcionalidade é redundante com `go install`. Remover esta funcionalidade
tornará `go get` mais rápido, já que ele não compilará ou linkará packages por padrão.
`go get` também não reportará um erro ao atualizar um package que não pode ser construído
para a plataforma atual.

Veja a proposta [#40276](/issue/40276) para a discussão completa.

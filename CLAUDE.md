# gowebsitebrasil

Fork de [golang/website](https://github.com/golang/website) com o conteúdo do site traduzido
para português brasileiro. O código Go é o do upstream; o trabalho aqui é tradução de `_content/`.

## Tradução

- Traduza com o agente `tradutor` (`.claude/agents/tradutor.md`), seguindo os planos em `plan/`,
  e marque os checkpoints `[x]` no plano.
- Arquivo grande demais para uma resposta (ex.: `_content/ref/mod.md`): divida em partes nos
  cabeçalhos `##`/`###` fora de blocos de código, traduza as partes em paralelo, junte e valide.
- Todo arquivo traduzido leva o marcador `ia-translated`; a posição depende do formato
  (veja as exceções no agente tradutor: cabeçalho `<!--{` JSON e `.article` do Tour).

## Verificação (obrigatória antes de commitar traduções)

```
.claude/harness/verificar.sh            # completo (~40s na primeira vez)
.claude/harness/verificar.sh --rapido   # só checagens estáticas
```

1. **Estáticas:** cada arquivo com `ia-translated` é comparado à versão em `upstream/master`:
   blocos de código idênticos, mesmas âncoras/IDs, cabeçalho `<!--{`/frontmatter no início,
   mesma flag de template, mesmos slides e diretivas `.play` nos `.article`, links internos válidos.
2. **Testes Go** (`go test ./cmd/golangorg/`): só falhas que não existem no upstream contam
   (a linha de base é gerada num worktree do upstream e guardada em `.git/harness/`).
3. **Fumaça:** sobe o servidor local e confere status, título traduzido e erros de template
   em cada página traduzida (Tour via `/tour/lesson/<nome>`).

Os testes de renderização (TestWeb/TestAll) exigem `$(go env GOROOT)/doc`, que o toolchain
baixado automaticamente não tem. O hook `.claude/hooks/session-start.sh` instala a distribuição
oficial do Go da versão do `go.mod` em `~/sdk` e define `GOTOOLCHAIN=local`.

Quando uma asserção em `cmd/golangorg/testdata/*.txt` procura um texto em inglês de uma página
que foi traduzida, troque a asserção pelo texto equivalente em PT-BR.

## Servidor local

```
go run ./cmd/golangorg -content=_content
```

Em modo local o host vira prefixo do caminho: `http://localhost:6060/go.dev/help`.
O Tour fica em `http://localhost:6060/tour/`.

## Sincronizar com o upstream

```
git fetch upstream master
git merge upstream/master
```

Em conflitos de arquivos traduzidos, mantenha a tradução e aplique a mudança do upstream já
traduzida (`git diff $(git merge-base HEAD upstream/master) upstream/master -- <arquivo>`).
Arquivo apagado no upstream é apagado aqui também. Rode o harness completo antes de commitar.

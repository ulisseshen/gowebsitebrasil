#!/bin/bash
# Verifica as traduções: checagens estáticas contra o upstream, testes Go
# (comparados com o upstream) e teste de fumaça das páginas no servidor local.
# Uso: .claude/harness/verificar.sh [--rapido]   (--rapido = só checagens estáticas)
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

HARNESS=.claude/harness
CACHE=$(git rev-parse --path-format=absolute --git-common-dir)/harness
mkdir -p "$CACHE"
falhas=()

if ! git remote get-url upstream >/dev/null 2>&1; then
  git remote add upstream https://github.com/golang/website.git
fi
if ! git rev-parse -q --verify upstream/master >/dev/null; then
  echo "» Buscando golang/website master..."
  git fetch -q upstream master || { echo "✗ não foi possível buscar o upstream"; exit 1; }
fi

echo "» 1/3 Checagens estáticas (contra upstream/master)"
python3 "$HARNESS/verificar_traducoes.py" upstream/master || falhas+=("estáticas")
[ "${1:-}" = "--rapido" ] && { [ ${#falhas[@]} -eq 0 ]; exit; }

GOROOT_DIR=$(go env GOROOT)
if [ ! -d "$GOROOT_DIR/doc" ]; then
  echo "‼ $GOROOT_DIR não tem doc/: os testes de renderização seriam pulados."
  echo "  Rode .claude/hooks/session-start.sh (instala o Go completo) e abra um novo shell."
  exit 1
fi

falhas_teste() {
  local out
  out=$(go test -count=1 ./cmd/golangorg/ 2>&1)
  if echo "$out" | grep -q '^FAIL' && ! echo "$out" | grep -q -- '--- FAIL'; then
    echo "o pacote de testes abortou: $(echo "$out" | grep -v '^\s*$' | grep -v '^FAIL' | tail -1)"
  fi
  echo "$out" |
    grep -E '^\s+(server_test\.go:[0-9]+: .*|testdata/[a-z]+\.txt:[0-9]+: .*)$' |
    sed -E 's/^\s+//; s/^server_test\.go:[0-9]+: //' | sort -u
  return 0
}

echo "» 2/3 Testes Go (cmd/golangorg), comparados com o upstream"
falhas_teste > "$CACHE/head.txt"
up_sha=$(git rev-parse upstream/master)
base="$CACHE/upstream-$up_sha.txt"
if [ ! -f "$base" ]; then
  wt="$CACHE/wt-upstream"
  git worktree remove --force "$wt" 2>/dev/null
  git worktree add -q --detach "$wt" "$up_sha"
  (cd "$wt" && falhas_teste) > "$base.tmp" && mv "$base.tmp" "$base"
  git worktree remove --force "$wt"
fi
novas=$(comm -23 "$CACHE/head.txt" "$base" 2>&1)
if [ ! -f "$base" ]; then
  echo "✗ não foi possível gerar a linha de base dos testes do upstream"
  falhas+=("testes")
elif [ -n "$novas" ]; then
  echo "✗ Falhas novas (não existem no upstream):"
  echo "$novas" | sed 's/^/    /'
  echo "  Se a asserção procura um texto em inglês de uma página que você traduziu,"
  echo "  atualize-a em cmd/golangorg/testdata/*.txt com o texto equivalente em PT-BR."
  falhas+=("testes")
else
  echo "✓ Nenhuma falha nova ($(wc -l < "$base") falha(s) já existente(s) no upstream ignorada(s))"
fi

echo "» 3/3 Teste de fumaça das páginas traduzidas"
go build -o "$CACHE/golangorg" ./cmd/golangorg &&
  python3 "$HARNESS/fumaca_paginas.py" "$CACHE/golangorg" "$GOROOT_DIR" || falhas+=("páginas")

echo
if [ ${#falhas[@]} -eq 0 ]; then
  echo "✓ Tudo certo"
else
  echo "✗ Falhou: ${falhas[*]}"
  exit 1
fi

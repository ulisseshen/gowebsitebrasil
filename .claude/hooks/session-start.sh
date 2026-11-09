#!/bin/bash
# Prepara sessões na nuvem: Go completo (com GOROOT/doc, exigido pelos testes de
# renderização), módulos baixados e o remote upstream (golang/website).
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# O toolchain baixado automaticamente (GOTOOLCHAIN) não traz GOROOT/doc,
# e sem ele TestWeb/TestAll são pulados. Instala a distribuição oficial.
GO_VERSION=$(awk '/^go /{print $2; exit}' go.mod)
GO_DIR="$HOME/sdk/go$GO_VERSION"
if [ ! -x "$GO_DIR/bin/go" ] || [ ! -d "$GO_DIR/doc" ]; then
  mkdir -p "$HOME/sdk"
  tmp=$(mktemp -d "$HOME/sdk/.download.XXXXXX")
  curl -sSfL "https://go.dev/dl/go$GO_VERSION.linux-amd64.tar.gz" | tar -xz -C "$tmp"
  rm -rf "$GO_DIR"
  mv "$tmp/go" "$GO_DIR"
  rmdir "$tmp"
fi
export PATH="$GO_DIR/bin:$PATH" GOTOOLCHAIN=local

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export PATH=\"$GO_DIR/bin:\$PATH\""
    echo "export GOTOOLCHAIN=local"
  } >> "$CLAUDE_ENV_FILE"
fi

hashes="$(go env GOMODCACHE)/.session-start.sha256"
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  go mod download
  mkdir -p "$(dirname "$hashes")"
  sha256sum .claude/hooks/session-start.sh go.mod go.sum > "$hashes" || rm -f "$hashes"
fi

if ! git remote get-url upstream >/dev/null 2>&1; then
  git remote add upstream https://github.com/golang/website.git
fi

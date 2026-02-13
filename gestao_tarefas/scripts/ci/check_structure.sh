#!/usr/bin/env bash
set -euo pipefail

err=0

# 1) Markdown fora de docs/ (permitidos: README.md, CONTRIBUTING.md, skills/*.md)
md_outside=$(find . -type f -name '*.md' \
  ! -path './.git/*' \
  ! -path './venv/*' \
  ! -path './venv_mcp/*' \
  ! -path './.claude/*' \
  ! -path './.gemini/*' \
  ! -path './docs/*' \
  ! -path './skills/*' \
  ! -name 'README.md' \
  ! -name 'CONTRIBUTING.md' \
  ! -name 'CLAUDE.md' \
  ! -name 'GEMINI.md' \
  ! -name 'AGENTS.md' \
  | sed 's#^\./##' \
  | sort)
if [[ -n "$md_outside" ]]; then
  echo "[FAIL] Markdown fora de docs/:"
  echo "$md_outside"
  err=1
fi

# 2) Arquivos na raiz fora da allowlist
root_files=$(find . -maxdepth 1 -type f -print | sed 's#^\./##' | sort)
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  case "$f" in
    README.md|CONTRIBUTING.md|CLAUDE.md|GEMINI.md|AGENTS.md|requirements.txt|.env.example|.gitignore)
      ;;
    *)
      echo "[FAIL] Arquivo inesperado na raiz: $f"
      err=1
      ;;
  esac
done <<< "$root_files"

# 3) Artefatos proibidos versionados
for pattern in '*:Zone.Identifier' '*.pickle' 'config/gmail_token.json' 'config/gmail_credentials.json'; do
  found=""
  while IFS= read -r tracked; do
    [[ -z "$tracked" ]] && continue
    [[ -e "$tracked" ]] || continue
    found+="$tracked"$'\n'
  done < <(git ls-files "$pattern" || true)
  if [[ -n "$found" ]]; then
    echo "[FAIL] Artefato sensível/versionado indevido ($pattern):"
    printf "%s" "$found"
    err=1
  fi
done

if [[ "$err" -ne 0 ]]; then
  echo "\nEstrutura inválida. Corrija os itens acima."
  exit 1
fi

echo "Estrutura OK."

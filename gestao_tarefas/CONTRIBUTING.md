# Contributing

## Organização de arquivos
1. Código novo deve entrar em `src/`.
2. Testes novos devem entrar em `tests/`.
3. Scripts operacionais devem entrar em `scripts/ops/`.
4. Scripts de setup devem entrar em `scripts/bootstrap/`.
5. Documentação deve entrar em `docs/` (na raiz, apenas `README.md`, `CLAUDE.md`, `GEMINI.md` e `AGENTS.md`).
6. Saídas e artefatos devem entrar em `data/`.

## Nomenclatura
- Use `snake_case` para arquivos e diretórios novos.
- Evite acentos e espaços em nomes de arquivos.

## Segurança
- Não versionar tokens, credenciais, arquivos locais de ambiente e dados sensíveis.
- Confira `.gitignore` antes de commitar dados gerados.

## Checklist de PR
1. Não criou arquivo solto na raiz fora da allowlist.
2. Não adicionou output transitório fora de `data/`.
3. Não adicionou credenciais ou tokens.
4. Atualizou links de documentação quando moveu arquivos.
5. Atualizou `docs/PROJECT_STRUCTURE.md` se introduziu nova estrutura.
6. Rodou `scripts/ci/check_structure.sh` antes do commit final.

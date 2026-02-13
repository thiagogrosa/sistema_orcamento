# HANDOFF - Implementação Planilha HVAC

## Contexto
Retomada rápida após `/new` ou `/reset`, preservando continuidade técnica e operacional.

## Regras de colaboração vigentes
- Sempre trabalhar em branch de feature
- Nunca commitar direto em `main`
- **Push permitido em `feature/*`**
- PR/merge em `main` segue validação final com Thiago
- Comunicação direta, objetiva e com foco em produtividade

## Estado atual do projeto
Repositório: `thiagogrosa/planilha`

### Branches principais
1. `feature/sprint1-expansao-composicoes`
   - Status: implementado e push realizado

2. `feature/sprint3-composicoes-especiais`
   - Status: implementado e push realizado

3. `feature/validacao-avancada-composicoes`
   - Status: implementado, testado, refinado e push realizado
   - Commit base: `7b72d5b` (`feat: implementar validação avançada e saída JSON de composições`)
   - Commits recentes relevantes:
     - `417c1db` (`fix: fechar cobertura mínima nas composições pendentes (0 warnings de cobertura)`)
     - `327afee` (`test/docs: consolidar regras avançadas e adicionar regressão de cobertura mínima`)
     - `5a45bc0` (`tune: reduzir ruído de similaridade com thresholds mais restritivos`)
     - `391f5b9` (`docs: listar warnings restantes de similaridade com buckets`)

## PR links
- Sprint 1/2:
  - https://github.com/thiagogrosa/planilha/pull/new/feature/sprint1-expansao-composicoes
- Sprint 3:
  - https://github.com/thiagogrosa/planilha/pull/new/feature/sprint3-composicoes-especiais
- Validação avançada:
  - https://github.com/thiagogrosa/planilha/pull/new/feature/validacao-avancada-composicoes

## Entregas consolidadas

### Catálogo e validação
- Catálogo expandido e padronizado
- Total atual na validação: **94 composições**
- `validar_composicoes.py` evoluído com regras avançadas:
  - consistência de unidade variável
  - outliers por tipo de item
  - duplicidade de composição
  - similaridade de descrição/estrutura
  - cobertura mínima (elétrica, dreno, acabamento)

### Relatórios
- Markdown: `relatorio-validacao-composicoes.md`
- JSON: `relatorio-validacao-composicoes.json`

### Testes
- Arquivo: `tests/test_validar_composicoes.py`
- Resultado no ambiente: **9 passed**

## Próxima execução recomendada (imediata)
1. Revisar e decidir ação nos **5 warnings** restantes de similaridade (`merge` vs `manter variante`)
2. Abrir PR da branch com release notes e checklist de validação
3. Após aprovação, merge controlado em `main`

## Comandos úteis de retomada
```bash
cd /data/.openclaw/workspace/planilha

git fetch --all
git checkout feature/validacao-avancada-composicoes
python3 validar_composicoes.py
python3 -m pytest -q tests/test_validar_composicoes.py
git status
```

## Observação
`criar_planilha.py` permanece funcional e estável. Hardening do Excel segue como etapa posterior (Recomendação 04).

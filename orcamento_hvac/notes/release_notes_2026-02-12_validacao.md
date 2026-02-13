# Release Notes — 2026-02-12 (Validação Avançada)

## Escopo consolidado da branch `feature/validacao-avancada-composicoes`

### 1) Cobertura mínima das composições
- Regra refinada para reduzir falsos positivos.
- Correções aplicadas nas composições pendentes.
- Resultado atual: **0 warnings** de cobertura mínima.

### 2) Similaridade de descrição (redução de ruído)
- Thresholds ajustados para warnings de similaridade.
- Nova regra: variantes da mesma família com BTU diferente são tratadas como info.
- Resultado:
  - Antes: 88 warnings de similaridade
  - Agora: 5 warnings de similaridade (mais focados)
  - 15 casos foram reclassificados como variantes aceitáveis (info)

### 3) Testes e qualidade
- Suite `tests/test_validar_composicoes.py` atualizada e estável.
- Resultado atual: **9 passed**.

### 4) Documentação
- README atualizado com status atual, entradas, exemplos e known issues.
- Documentos de apoio criados em `notes/coverage_fix/` para revisão dos pares restantes.

## Impacto
- Menos ruído operacional na validação.
- Alertas mais acionáveis para revisão real de catálogo.
- Base pronta para PR e revisão final no GitHub.

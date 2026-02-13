# Consolidação P1 — regras avançadas do validador

Data: 2026-02-12 17:55

## Status atual
- Erros: **0**
- Avisos: **88**
- Infos: **24**
- Cobertura mínima: **0 warnings** (dreno/elétrica/acabamento)

## Regras com maior volume (top 10)
- DESCRIPTION_HIGH_SIMILARITY: 88
- STRUCTURE_HIGH_SIMILARITY: 24

## Validação de regressão
- Testes do validador executados: **9/9 passando**
- Novos testes incluídos para cobertura mínima:
  - não aplicar cobertura mínima em composição fora de instalação
  - detectar falta de dreno em composição de instalação com elétrica/acabamento presentes

## Próximas melhorias sugeridas (P2)
1. Refinar DESCRIPTION_HIGH_SIMILARITY por família para reduzir ruído
2. Adicionar baseline por família para outliers de quantidade
3. Definir severidade dinâmica por impacto comercial

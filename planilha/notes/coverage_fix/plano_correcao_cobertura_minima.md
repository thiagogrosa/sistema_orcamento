# Plano de correção — cobertura mínima

## Resumo
- Composições com lacuna: **29**
- Faltas de dreno: **29**
- Faltas de elétrica: **11**
- Faltas de acabamento: **5**

## P0 (lacuna tripla)
- COMP_DESINST — faltas: acabamento,dreno,eletrica
- COMP_FACH — faltas: acabamento,dreno,eletrica
- COMP_INST_BI_48K — faltas: acabamento,dreno,eletrica
- COMP_INST_BI_60K — faltas: acabamento,dreno,eletrica
- COMP_INST_FACH_RAPEL — faltas: acabamento,dreno,eletrica

## Estratégia em lotes
1. Corrigir P0 (tripla)
2. Corrigir faltas de dreno e elétrica (P1)
3. Fechar acabamento restante (P2)
4. Reexecutar validação e zerar MISSING_MIN_COVERAGE_*

## Arquivo operacional
- `notes/coverage_fix/min_coverage_backlog.csv`

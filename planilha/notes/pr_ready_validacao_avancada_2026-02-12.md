# PR Ready — feature/validacao-avancada-composicoes

## Link para abrir PR
https://github.com/thiagogrosa/planilha/pull/new/feature/validacao-avancada-composicoes

## Título sugerido
`feat: consolidar validação avançada de composições e reduzir ruído de alertas`

## Descrição sugerida
### Resumo
Esta PR consolida a evolução do validador de composições com foco em precisão operacional e redução de ruído.

### Principais entregas
- Cobertura mínima tratada e zerada (dreno/elétrica/acabamento)
- Regras de similaridade refinadas para reduzir falsos positivos
- Variantes de capacidade da mesma família reclassificadas como info
- Relatórios atualizados (`.md` + `.json`)
- Testes atualizados (9 passing)
- README e handoff atualizados

### Métricas (antes -> depois)
- Warnings totais: 133 -> 20 -> 5 (após ajustes de regra e validações)
- Cobertura mínima: 45 -> 0
- Erros: 0 -> 0

### Arquivos de referência
- `notes/release_notes_2026-02-12_validacao.md`
- `notes/coverage_fix/remaining_similarity_review_2026-02-12.md`
- `notes/coverage_fix/similarity_resolution_plan_2026-02-12.md`

### Checklist
- [x] Testes do validador passando
- [x] Relatórios atualizados
- [x] Sem erros de validação
- [ ] Revisão final dos 5 warnings remanescentes (decisão merge/manter)

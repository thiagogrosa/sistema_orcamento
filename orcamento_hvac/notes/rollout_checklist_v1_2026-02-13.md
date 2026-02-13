# Rollout Checklist v1 — 2026-02-13

Status atual: READY FOR CONTROLLED ROLLOUT (GO gate 10/10)
Branch: `feature/system-implementation-15min-sprints`

## 1) Pre-rollout (obrigatório)
- [ ] Confirmar freeze de escopo (sem novas features durante rollout)
- [ ] Confirmar backup dos artefatos críticos
- [ ] Confirmar credenciais de produção (sem tokens em chat)
- [ ] Confirmar janela de monitoramento pós-deploy (mín. 2h)

## 2) Technical validation
- [x] Stage 1 entregue (domínio core de propostas + ID)
- [x] Stage 2 entregue (dual templates + renderer)
- [x] Stage 3 entregue (lifecycle + Asana mocked)
- [x] Stage 4 entregue (pricing + approval gates)
- [x] Stage 5 entregue (intake/retrieval mocked)
- [x] Stage 6 entregue (KPI/reporting baseline)
- [x] Stage 7 entregue (GO gate final)
- [x] Test suite local: 77 passed
- [x] Verification matrix: 10/10 PASS

## 3) Rollout sequence (controlado)
1. Publicar branch remota + abrir PR
2. Revisão técnica focada em:
   - migração SQL de domínio de propostas
   - integridade de transições de status
   - consistência de pricing policy version
3. Aprovar PR
4. Aplicar migração em ambiente alvo
5. Validar smoke pós-deploy
6. Liberar operação assistida

## 4) Smoke tests pós-deploy
- [ ] Criar proposta `PROP-YYYY-NNNN`
- [ ] Gerar 2 saídas (cliente + execução) a partir do mesmo payload
- [ ] Executar transição `draft -> review -> priced`
- [ ] Rodar cálculo de pricing com caso determinístico
- [ ] Rodar KPI semanal com fixture
- [ ] Validar ingest/retrieve por proposal_id

## 5) Critério de rollback
Executar rollback imediato se ocorrer:
- falha em migração de schema
- erro de persistência em `proposal_status_history`
- divergência de cálculo de preço vs teste determinístico
- falha em geração de templates críticos

## 6) Handoff operacional
- Owner técnico: Alex
- Owner de aprovação: Thiago
- Modo de execução: etapa por etapa com autorização explícita

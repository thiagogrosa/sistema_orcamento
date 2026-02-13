# Integração com `gestao-orcamentos` (2026-02-13)

## Objetivo
Integrar o fluxo atual com o projeto responsável por gestão de propostas (Asana + Drive + coleta de informações).

## O que foi integrado
### 1) Coleta e preparação de informações
- Ponte criada para usar o `DataPreparer` do `gestao-orcamentos`.
- Entrada: email bruto (`.txt/.html/.eml`)
- Saída: markdown estruturado com metadados extraídos.

### 2) Gestão de proposta no Asana
- Ponte criada para usar `AsanaLib` do `gestao-orcamentos`.
- Criação de tarefa de orçamento com pipeline de subtarefas padrão.
- No estado atual da biblioteca, execução ocorre em **modo simulado** (ID de tarefa gerado e URL montada).

### 3) Mapeamento/sync com Drive
- Ponte criada para usar `DriveSync` do `gestao-orcamentos`.
- Registro pasta_id -> task_gid realizado.
- Rotina de sync executada e reportada.

## Arquivos novos
- `automations/scripts/integrate_gestao_orcamentos_v1.py`
- `tests/fixtures/stage_gestao_orcamentos_payload.json`

## Evidência de execução
- `runtime/integration/gestao_orcamentos_integration_result.json`
- `runtime/integration/dados_preparados_26_999.md`

## Resultado
- Integração funcional para atividades similares (coleta/preparo + gestão de proposta + sync/mapeamento)
- Limitação atual: AsanaLib ainda opera em modo simulado no código-fonte atual do projeto `gestao-orcamentos`.

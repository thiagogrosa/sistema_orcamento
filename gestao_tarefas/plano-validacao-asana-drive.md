# Plano de Validação: Asana vs Google Drive

**Data:** 2026-02-05
**Objetivo:** Garantir que as tarefas no Asana estejam consistentes com as pastas do Google Drive

---

## 1. Resumo do Problema

As tarefas no Asana foram cadastradas com informações incorretas ou desatualizadas em relação às pastas do Drive, que são a fonte de verdade.

### Divergências Críticas Identificadas

| ID | Asana (errado) | Drive (correto) | Ação |
|----|----------------|-----------------|------|
| 26_054 | Dilermando de Aguiar - Laudo | TEATRO_PASCHOAL_E_CASA_ARTE_NH | Corrigir nome/cliente |
| 26_055 | Santana da Boa Vista - Portilho | MUTUA_RS_PMOC | Corrigir completamente |
| 26_056 | Pacaembu - Filtros | TRE_SAO_LEOPOLDO | Corrigir completamente |
| 26_058 | MSC - Peça (Turbina) | HOSP_DOM_VICENTE_OBRA | Corrigir completamente |

---

## 2. Etapas do Plano

### Etapa 1: Exportar Lista Completa do Drive (2026)

Gerar arquivo com todas as 66 pastas de 2026 no formato estruturado:
- ID
- Cliente
- Serviço/Tipo
- Local (se identificável)

### Etapa 2: Exportar Lista Atual do Asana

Gerar arquivo com todas as tarefas do projeto "DEMANDAS DE ORCAMENTOS":
- ID Asana (26_XXX)
- Nome atual
- Seção atual

### Etapa 3: Comparação Automatizada

Criar tabela de comparação identificando:
- ✅ Tarefas corretas (nome bate com Drive)
- ⚠️ Tarefas com diferenças menores (typos, formatação)
- ❌ Tarefas com erros graves (cliente/serviço errado)
- ➕ Pastas no Drive sem tarefa no Asana (2026 apenas)
- ➖ Tarefas no Asana sem pasta no Drive

### Etapa 4: Validar Tarefas de 2025 no Asana

Verificar as tarefas de 2025 que estão no Asana:
- 25_828 Instituto Cancer Infantil
- 25_837 Clínica Bertol Marques
- 25_784 Melnick Even PDV
- 25_860 BB Abelardo Luz

Confirmar que existem no Drive de 2025 e que os dados batem.
**NÃO cadastrar novas tarefas de 2025.**

### Etapa 5: Gerar Relatório de Correções

Lista de todas as correções necessárias no Asana:
- Tarefas a renomear
- Descrições a atualizar
- Tarefas potencialmente duplicadas

### Etapa 6: Aprovar e Executar Correções

Após aprovação do usuário:
- Atualizar tarefas no Asana via MCP
- Documentar alterações

---

## 3. Fonte de Dados

### Google Drive (montado em /mnt/g/)

```
/mnt/g/Drives compartilhados/02Orcamentos/2026/  → 66 pastas
/mnt/g/Drives compartilhados/02Orcamentos/2025/  → ~876 pastas
```

### Asana

- Projeto: DEMANDAS DE ORCAMENTOS (GID: 1212920325558530)
- Workspace: armant.com.br (GID: 1204197108826498)

---

## 4. Regras de Validação

### Nomenclatura Drive → Asana

| Drive | Asana (esperado) |
|-------|------------------|
| `26_001_BANRISUL_AG_IVOTI` | `26_001 [INSTALACAO] Banrisul - Ag Ivoti` |
| `26_007_INTELBRAS_SC_PMOC` | `26_007 [MANUTENCAO] Intelbras - Filiais SC` |
| `26_024_INCORPORADORA_HRH_HARD_ROCK_PROJETO` | `26_024 [PROJETO] Hard Rock Residence - Gramado/RS` |

### Mapeamento de Tipo (Drive → Tag Asana)

| Sufixo no Drive | Tipo no Asana |
|-----------------|---------------|
| `_PMOC` | [MANUTENCAO] |
| `_CORRETIVA`, `_MANUTENCAO`, `_MANUT` | [MANUTENCAO] |
| `_INSTALACAO`, `_OBRA` | [INSTALACAO] |
| `_PROJETO` | [PROJETO] |
| `_PECAS`, `_PECA` | [MANUTENCAO] |
| (sem sufixo claro) | [A DEFINIR] |

---

## 5. Restrições

- ❌ **NÃO** cadastrar novas demandas de 2025 no Asana
- ❌ **NÃO** deletar tarefas do Asana sem aprovação
- ✅ Apenas corrigir dados existentes
- ✅ Cadastrar demandas de 2026 que estão no Drive mas não no Asana (após aprovação)

---

## 6. Entregáveis

1. `comparacao-asana-drive-2026.md` - Tabela completa de comparação
2. `correcoes-necessarias.json` - Lista de correções em formato JSON
3. `relatorio-validacao.md` - Relatório final com estatísticas

---

## 7. Próximos Passos (aguardando aprovação)

- [ ] Executar Etapa 1: Extrair lista do Drive
- [ ] Executar Etapa 2: Extrair lista do Asana
- [ ] Executar Etapa 3: Gerar comparação
- [ ] Apresentar divergências para aprovação
- [ ] Executar correções aprovadas

---

## Aprovação

**Status:** ⏳ Aguardando aprovação do usuário para prosseguir

Deseja prosseguir com a execução do plano?

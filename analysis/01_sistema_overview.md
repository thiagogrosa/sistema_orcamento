# Sistema de Orçamento — Overview Factual

> **Escopo:** Descreve o que o sistema faz com base na leitura direta do código-fonte.
> Não contém métricas comparativas, estimativas de economia ou afirmações de eficiência
> que não tenham sido medidas em condições controladas.
>
> **Gerado em:** 2026-02-21
> **Baseado em:** Leitura de código em `/home/user/sistema_orcamento`

---

## Estrutura de Módulos

O repositório contém três módulos independentes:

```
sistema_orcamento/
├── gestao_tarefas/     # Módulo 1: Pipeline Gmail → Asana
├── orcamento_hvac/     # Módulo 2: Planilha de custos HVAC
└── gerador_propostas/  # Módulo 3: Gerador de propostas PDF/Excel
```

**Contagem real de arquivos:**
- Python: 94 arquivos
- Testes: 18 arquivos (5 em gestao_tarefas, 9 em orcamento_hvac, 4 em gerador_propostas)
- Markdown: ~159 arquivos (inclui docs, notas de sprint, dados operacionais e outputs gerados)

---

## Módulo 1: gestao_tarefas

### O que faz

Pipeline de 6 etapas para capturar demandas de orçamento a partir de e-mails e
criar tarefas estruturadas no Asana.

```
Gmail → preparar dados → IA extrai JSON → Asana
```

### Componentes (src/)

| Arquivo | Status real | O que faz |
|---------|-------------|-----------|
| `gmail_client.py` | **Implementado** | OAuth2 real, busca emails, baixa conteúdo, extrai anexos. Usa Google API Python Client + tenacity para retry. |
| `prepare_data.py` | Implementado | Limpa HTML/EML para texto, reduz ruído antes de enviar para IA. |
| `ai_extractor.py` | Implementado | Chama Claude (Haiku padrão, Sonnet como fallback) via SDK Anthropic. Retorna JSON estruturado com dados do orçamento. |
| `asana_lib.py` | **Simulação** | Formata título/descrição/tags (real). Todas as chamadas à API Asana retornam UUIDs aleatórios com log `WARNING: MODO SIMULAÇÃO`. Nenhuma tarefa é criada de fato. |
| `sync_drive.py` | Parcialmente implementado | Lógica de detecção de PDFs existe. Chamadas reais ao Drive/Asana dependem de `asana_lib` (que está em simulação). |
| `cli.py` | Implementado | 6 subcomandos: `processar-pasta`, `buscar-emails`, `preparar-dados`, `extrair-dados`, `criar-tarefa`, `sync-drive`. Suporta `--dry-run`, `--verbose`, `--confirm`. |

### Estado da integração Asana

`asana_lib.py` tem 6 métodos com comportamento simulado:

```python
# _criar_tarefa_asana() — linha 220
import uuid
simulated_id = str(uuid.uuid4())[:16]
logger.warning("MODO SIMULAÇÃO: Tarefa não foi realmente criada no Asana.")
return simulated_id

# _criar_subtarefas() — linha 246 — idem com UUID
# _adicionar_tags() — linha 389 — retorna True sem fazer nada
# buscar_tarefas() — linha 578 — retorna []
# anexar_arquivo() — linha 607 — retorna True sem fazer nada
# obter_tarefa() — linha 626 — retorna dict hardcoded "[SIMULADO]"
```

**Conclusão:** O pipeline Gmail→IA funciona. A escrita no Asana ainda não.

### IDs do projeto Asana (hardcoded no código)

```python
WORKSPACE_ID = "1204197108826498"
PROJECT_ID   = "1212920325558530"
SECAO_ENTRADA = "1212909431317491"
SECAO_ENVIADO = "1212920431590044"
```

### Testes (gestao_tarefas/tests/)

5 arquivos de teste existem:
- `test_ai_extractor.py`
- `test_asana_lib.py`
- `test_cli.py`
- `test_gmail_client.py`
- `test_prepare_data.py`

**Estado dos testes:** não verificado neste documento — ver `02_plano_verificacao.md`.

---

## Módulo 2: orcamento_hvac

### O que faz

Conjunto de ferramentas para geração de planilhas de custo HVAC e geração de
propostas para clientes.

### Componentes principais

| Arquivo/Pasta | Status real | O que faz |
|---------------|-------------|-----------|
| `dados/composicoes.py` | Implementado | 94 composições HVAC como estrutura de dados Python. Base de cálculo de custos. |
| `dados/materiais.py` | Implementado | Catálogo de materiais com códigos, unidades e preços unitários. |
| `dados/mao_de_obra.py` | Implementado | Catálogo de mão de obra. |
| `dados/ferramentas.py` | Implementado | Catálogo de ferramentas. |
| `dados/equipamentos.py` | Implementado | Catálogo de equipamentos. |
| `validar_composicoes.py` | **Implementado** | 8 validações (integridade de referências, quantidades negativas, unidade variável, outliers, duplicidade, cobertura mínima). Gera relatório MD + JSON. |
| `criar_planilha.py` | Implementado | Gera workbook Excel (.xlsx/.xlsm) a partir dos dados Python usando openpyxl. |
| `criar_planilha_split_v3.py` | Implementado | Versão alternativa do gerador com split por aba. |
| `scraping/` | Implementado | Framework modular para scraping de preços. `mercadolivre_scraper.py` existe. Cache de 24h. |
| `abas/` | Implementado | Módulos por aba do Excel (composicoes, escopo, cliente, negocio, etc). |
| `automations/scripts/` | Implementado | Scripts de automação para geração de propostas, pricing engine, KPI report, lifecycle Asana (mock). |

### Limitação conhecida (documentada no código)

`openpyxl` não gera fórmulas de arrays dinâmicos (LET, LAMBDA, MAP, PROCX) de
forma que o Excel reconheça. A solução adotada é: Python popula os dados, as
fórmulas ficam no `template.xlsm` (Excel nativo).

### Testes (orcamento_hvac/tests/)

9 arquivos de teste:
- `test_dados.py`
- `test_validar_composicoes.py`
- `test_validator.py`
- `test_proposal_stage1_core_domain.py`
- `test_stage2_dual_deliverables.py`
- `test_stage3_lifecycle_asana_mock.py`
- `test_stage4_pricing_engine.py`
- `test_stage5_intake_router.py`
- `test_stage6_kpi_reporting.py`

---

## Módulo 3: gerador_propostas

### O que faz

Pipeline Python para geração de propostas HVAC em formato Markdown/PDF/Excel.
**Status real (confirmado no README):** em desenvolvimento.

### Componentes (hvac/)

| Arquivo | Status real | O que faz |
|---------|-------------|-----------|
| `compositor.py` | Implementado | Monta proposta a partir de escopo + bases de dados. |
| `precificador.py` | Implementado | Calcula preços finais, margens, totais. |
| `pipeline.py` | Implementado | Orquestra compositor → precificador → output. Lê `escopo.json`. |
| `gerador_pdf.py` | Implementado | Gera PDF da proposta. |
| `generators/planilha_interna.py` | Implementado | Gera planilha interna de orçamento. |
| `generators/proposta_pdf.py` | Implementado | Gerador PDF alternativo. |
| `utils/loader.py` | Implementado | Carrega bases de dados. |
| `utils/metricas.py` | Implementado | Rastreia métricas de execução do pipeline. |

### Testes (gerador_propostas/hvac/tests/)

3 arquivos de teste:
- `test_compositor.py`
- `test_precificador.py`
- `tests/test_gerador_pdf_manual.py`

---

## O que NÃO existe

| Afirmação circulante | Realidade |
|---------------------|-----------|
| "87.5% redução de tempo" | Nenhum teste comparativo foi realizado. Estimativa não verificada. |
| "93.75% economia de custo" | Idem. O cli.py rastreia tokens por execução, mas não há baseline medido. |
| "97.5% economia (COMPARACAO_CUSTOS_IA.md)" | Outro número, mesma ausência de metodologia. Documentos internos se contradizem. |
| "Sistema de integração Asana funcional" | `asana_lib.py` opera em modo simulação. Nenhuma tarefa é criada via código. |
| "gerador_propostas production-ready" | O README do módulo diz explicitamente "Status: desenvolvimento". |
| "71 pastas sincronizadas" | O arquivo de comparação Asana×Drive existe como dado manual/operacional, não como saída de script. |

---

## Contexto operacional real (dados vivos)

O projeto está sendo usado operacionalmente. Existem documentos de trabalho real:

- **Demandas ativas:** ~70 demandas de orçamento rastreadas manualmente em markdown
- **Email de entrada:** `orcamentos2@armant.com.br`
- **Pasta Drive:** `02Orcamentos/2026/` com subpastas numeradas `26_XXX`
- **Integração Asana:** feita manualmente via Claude Code + MCP Asana (não via `asana_lib.py`)
- **Pesquisa de emails:** feita via Gemini CLI ou scripts Python com Gmail API

A diferença entre o sistema de código e a operação real é que a operação usa
Claude Code interativamente via MCP, não os scripts Python diretamente.

---

## Documentação: problema de duplicação

A pasta `gestao_tarefas/` contém múltiplas cópias do mesmo conteúdo:

```
gestao_tarefas/
├── GUIA_DESENVOLVEDOR.md          ← cópia raiz
├── docs/guides/GUIA_DESENVOLVEDOR.md  ← cópia em docs/
├── lista/demandas-orcamentos.md   ← kebab-case
└── docs/operations/listas/demandas_orcamentos.md  ← snake_case (mesmo conteúdo)
```

Isso afeta o contexto de agentes AI que leem o repositório: o mesmo conteúdo
é processado múltiplas vezes, potencialmente inflando percepções de tamanho e
completude do sistema.

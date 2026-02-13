# Plano Mestre: Sistema de Orcamentacao HVAC

> **Versao:** 2.0
> **Data:** 2026-01-02
> **Objetivo:** Sistema de agentes/skills para geracao automatizada de orcamentos HVAC

---

## Visao Geral

Sistema hierarquico de skills que interpreta documentos tecnicos e gera orcamentos completos de servicos de climatizacao, otimizado para **eficiencia de contexto e tokens**.

### Principio Central

> Economizar tokens em tarefas simples para maximizar uso do **Opus** nas partes criticas.

---

## Arquitetura

```
                    ┌─────────────────────────────────┐
                    │         SKILL MESTRE            │
                    │      (hvac/SKILL.md)            │
                    │         [OPUS]                  │
                    │  - Analisa entrada              │
                    │  - Decide caminho               │
                    │  - Orquestra subagentes         │
                    └───────────────┬─────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    EXTRATOR     │     │   COMPOSITOR    │     │  PRECIFICADOR   │
│ [HAIKU/SONNET]  │     │    [HAIKU]      │     │    [SONNET]     │
│                 │     │                 │     │                 │
│ - Textos simples│     │ - Monta lista   │     │ - Aplica precos │
│ - Editais (Opus)│     │   de materiais  │     │ - Calcula BDI   │
│ - PDFs          │     │ - Ajusta qtds   │     │ - Regras negocio│
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────────────┐
                    │           OUTPUT                │
                    │         [SONNET]                │
                    │  - PDF com identidade visual    │
                    │  - Excel detalhado              │
                    │  - Texto rapido                 │
                    └─────────────────────────────────┘
```

### Modulos Auxiliares

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│         COTACOES                │     │     MANUTENCAO DE BASES         │
│        [SONNET]                 │     │        [HAIKU]                  │
│  - Gera e-mails de cotacao      │     │  - Atualiza precos              │
│  - Web scraping de precos       │     │  - Cria novas composicoes       │
│  - Cadastro de fornecedores     │     │  - Importa dados Excel/CSV      │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

---

## Distribuicao de Modelos

| Modelo | Uso | Justificativa |
|--------|-----|---------------|
| **OPUS** | Skill Mestre, editais complexos, criacao de composicoes | Decisoes criticas, interpretacao ambigua |
| **SONNET** | Precificacao, output PDF, scraping, e-mails | Complexidade intermediaria, formatacao |
| **HAIKU** | Extracao simples, composicao padrao, calculos, atualizacoes | Alto volume, tarefas repetitivas |

---

## Estrutura de Arquivos

```
hvac_claude_code/
├── .claude/skills/                    # Skills locais do projeto
│   ├── hvac/SKILL.md                  # Skill Mestre
│   ├── hvac-extrator/SKILL.md
│   ├── hvac-compositor/SKILL.md
│   ├── hvac-precificador/SKILL.md
│   ├── hvac-output/SKILL.md
│   └── hvac-cotacoes/SKILL.md
│
├── bases/                             # Bases de dados (JSON)
│   ├── composicoes-split.json         # Composicoes de instalacao split
│   ├── composicoes-manutencao.json    # Composicoes de manutencao
│   ├── precos.json                    # Tabela de precos
│   ├── fornecedores.json              # Cadastro de fornecedores
│   └── bdi.json                       # Tabelas de BDI
│
├── templates/                         # Templates de output
│   └── proposta/
│       ├── cabecalho.html
│       ├── rodape.html
│       └── estilos.css
│
└── docs/                              # Documentacao (Obsidian vault)
    ├── 00-plano-mestre.md             # Este arquivo
    ├── 01-skill-mestre.md
    ├── 02-skill-extrator.md
    ├── 03-skill-compositor.md
    ├── 04-skill-precificador.md
    ├── 05-skill-output.md
    ├── 06-skill-cotacoes.md
    └── interfaces/
        └── contratos.md               # Entrada/saida entre skills
```

---

## Interfaces Entre Skills

Cada skill recebe e entrega dados em formato JSON padronizado.
Ver `docs/interfaces/contratos.md` para especificacoes detalhadas.

### Fluxo Principal

```
ENTRADA                 EXTRATOR              COMPOSITOR            PRECIFICADOR          OUTPUT
(texto/PDF)    ──────►  (escopo.json)  ──────►  (composicao.json)  ──────►  (precificado.json)  ──────►  (PDF/XLSX)
```

### Resumo de Interfaces

| De | Para | Contrato |
|----|------|----------|
| Usuario | Skill Mestre | Texto livre, arquivo, ou path |
| Skill Mestre | Extrator | `{ entrada: string, tipo: "texto"\|"pdf"\|"edital" }` |
| Extrator | Compositor | `escopo.json` (projeto, itens, condicoes) |
| Compositor | Precificador | `composicao.json` (itens, materiais, mao_obra) |
| Precificador | Output | `precificado.json` (itens, resumo_financeiro) |
| Output | Usuario | Arquivos (PDF, XLSX, texto) |

---

## Integracoes Externas

### Asana (via Gemini CLI)

- **Quando:** Orcamento aprovado pelo cliente
- **Acao:** Criar tarefas no projeto existente
- **Como:** Skill dedicada que chama Gemini CLI com MCP do Asana
- **Objetivo:** Nao consumir contexto do Claude Code com MCP

### Filesystem Local

- **Google Drive:** Acessado via caminho montado (sem MCP)
- **Obsidian Vault:** Pasta `docs/` pode ser aberta como vault
- **Bases de dados:** Arquivos JSON locais em `bases/`

### Web Scraping de Precos

- **Fontes:** Fornecedores, marketplaces, SINAPI
- **Frequencia:** Sob demanda ou programada
- **Skill:** `hvac-cotacoes` com subagente Sonnet

---

## MVP - Escopo Inicial

### Funcionalidades Nucleo

1. **Extracao de escopo** de textos e PDFs simples
2. **Composicao de servicos** para splits completo:
   - Instalacao 9K, 12K, 18K, 24K BTU
   - Manutencao preventiva e corretiva
   - Desinstalacao
   - Infra eletrica
   - Adicionais (altura, distancia)
3. **Precificacao** com BDI por tipo de cliente
4. **Output** em PDF com identidade visual

### Proximas Fases

- Geracao de e-mails de cotacao
- Web scraping de precos
- Integracao Asana
- Criacao de novas composicoes
- Expansao para VRV/Multi-split

---

## Documentos Relacionados

- [[01-skill-mestre]] - Especificacao da Skill Mestre
- [[02-skill-extrator]] - Especificacao da Skill Extratora
- [[03-skill-compositor]] - Especificacao da Skill Compositora
- [[04-skill-precificador]] - Especificacao da Skill Precificadora
- [[05-skill-output]] - Especificacao da Skill Output
- [[06-skill-cotacoes]] - Especificacao da Skill Cotacoes
- [[interfaces/contratos]] - Contratos de entrada/saida

---

## Historico de Decisoes

| Data | Decisao | Justificativa |
|------|---------|---------------|
| 2026-01-02 | Arquitetura Skill Mestre + Subagentes + Skills | Eficiencia de contexto, modelos por complexidade |
| 2026-01-02 | Skills locais ao projeto (nao globais) | Flexibilidade, promover para global se util |
| 2026-01-02 | Asana via Gemini CLI | Nao consumir contexto do Claude com MCP |
| 2026-01-02 | Bases em JSON local | Simplicidade, facil versionamento, lazy loading |
| 2026-01-02 | PDF com identidade visual | Requisito do cliente |

---

*Documento gerado em 2026-01-02 com Claude Code*

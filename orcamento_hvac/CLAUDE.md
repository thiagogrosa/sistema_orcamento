# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre o Projeto

**Planilha de Custos HVAC (Split)** - Sistema híbrido para geração de orçamentos de instalação de ar-condicionado Split:

1. **Python** (`criar_planilha.py`): Gerencia dados (`dados/`), orquestra abas (`abas/`) e injeta dados brutos
2. **Excel Template** (`template.xlsm`): Contém lógica de cálculo via Arrays Dinâmicos (`LET`, `MAP`, `PROCX`) e Macros VBA
3. **Web Scraping** (`scraper_cli.py`): Coleta preços atualizados de fornecedores para alimentar o sistema

## Comandos Principais

```bash
# Instalação e Setup
./setup.sh  # Configura venv, instala dependências (openpyxl, requests, etc.)

# Gerar planilha
python3 criar_planilha.py
# - Sem template.xlsm: Gera Composicoes_Split_v3.xlsx (sem macros)
# - Com template.xlsm: Gera Composicoes_Split_v3.xlsm (com macros VBA)

# Web Scraping
python3 scraper_cli.py search "termo" --export  # Busca produtos e exporta CSV
python3 scraper_cli.py cache --stats            # Estatísticas do cache

# Exportar dados para CSV
python3 exportar_csv.py  # Exporta dados/*.py para dados_csv/
```

## Arquitetura do Sistema

### 1. Dados e Abas (`abas/`, `dados/`)

- **Dados Estáticos**: `dados/*.py` contêm listas de materiais, MO, ferramentas, equipamentos
- **Modularização**: Cada aba do Excel tem seu módulo em `abas/`
- **Separação de Responsabilidades**: Python **não** escreve fórmulas complexas (openpyxl não suporta spill). Ele preenche dados e o Excel calcula

**Fluxo de dados**: `dados/*.py` → `abas/*.py` → Excel com fórmulas

### 2. Web Scraping (`scraping/`)

- **BaseScraper**: Classe abstrata para novos fornecedores
- **CacheManager**: Armazena requisições por 24h para evitar blocks
- **Validator**: Garante integridade de preços e URLs
- **Exporter**: Converte dados raspados para formato de importação VBA

### 3. Integração CSV e VBA (`vba/`, `dados_csv/`)

- **Importação Dinâmica**: VBA (`modImportCSV.bas`) lê CSV mais recente de `dados_csv/`
- **Controle de Validade**: Cada item possui data de atualização e dias de validade
- **Wizard de Composição**: `frmNovaComposicao.frm` permite criar novos serviços rapidamente

## Estrutura da Planilha

| Aba | Descrição |
|-----|-----------|
| INSTRUCOES | Guia de uso da planilha |
| PROMPTS | Prompts para geração de conteúdo |
| NEGOCIO | Configuração de BDI/Markup com multiplicadores por tipo |
| MATERIAIS | Catálogo de materiais (MAT) |
| MAO_DE_OBRA | Catálogo de mão de obra (MO) |
| FERRAMENTAS | Catálogo de ferramentas (FER) |
| EQUIPAMENTOS | Catálogo de equipamentos (EQP) |
| COMPOSICOES | Composições de serviço com margem aplicada por item |
| CLIENTE | Dados do cliente (nome, endereço, contato) |
| ESCOPO | Seleção de serviços para o orçamento (valores já com margem) |

## Convenções de Nomenclatura

### Aba de Orçamento
O nome oficial é **`ESCOPO`** (evitar `ORCAMENTO` para manter consistência)

### Códigos de Itens
- `MAT_*`: Materiais (em `dados/materiais.py`)
- `MO_*`: Mão de Obra (em `dados/mao_de_obra.py`)
- `FER_*`: Ferramentas (em `dados/ferramentas.py`)
- `EQP_*`: Equipamentos (em `dados/equipamentos.py`)
- `COMP_*`: Composições de Serviço (em `dados/composicoes.py`)

## Estrutura de Colunas - ESCOPO

| Col | Nome | Descrição |
|-----|------|-----------|
| A | Item | Número sequencial do item |
| B | Tipo | COMP, EQP, MAT, MO ou FER |
| C | Serviço/Item | Dropdown dinâmico baseado no Tipo |
| D | Qtd | Quantidade (usuário preenche) |
| E | Variável | Metros de linha frigorígena (usuário preenche) |
| F | Descrição | Preenchida por fórmula de spill |
| G | Preço Unit. | Preenchido por fórmula de spill |
| H | Total | Qtd × Preço Unit. |

## Estrutura de Colunas - COMPOSICOES

| Col | Nome | Descrição |
|-----|------|-----------|
| A | Código | Código da composição (COMP_*) ou vazio para itens |
| B | Descrição | Descrição da composição ou do item |
| C | Tipo | MAT, MO, FER ou EQP |
| D | Cód. Item | Código do item (dropdown com CÓDIGO - DESCRIÇÃO) |
| E | Un | Unidade de medida (SPILL) |
| F | Qtd Base | Quantidade fixa por instalação |
| G | Qtd Var | Quantidade variável (por metro de linha) |
| H | Preço Unit. | Preço unitário via SPILL |
| I | Sub. Base | Subtotal base (custo SEM margem) |
| J | Sub. Var | Subtotal variável (custo SEM margem) |
| K | Mult. | Multiplicador por tipo (de NEGOCIO) |
| L | Base c/ Margem | Subtotal base COM margem aplicada |
| M | Var c/ Margem | Subtotal variável COM margem aplicada |
| N | Seleção | Código + Descrição para dropdown (oculta) |
| O-R | Desc/Unid | Campos para descrição dinâmica (ocultas) |

## Fluxo de Trabalho Recomendado

1. **Atualizar Preços**: Rodar `scraper_cli.py` para coletar novos preços
2. **Gerar CSV**: Exportar resultados para `dados_csv/`
3. **Sincronizar Excel**: Abrir `Composicoes_Split_v3.xlsm` e clicar em "Importar Catálogos"
4. **Montar Orçamento**: Preencher a aba `ESCOPO`

## Notas Técnicas (Spill Arrays)

### Limitação Crítica
**O openpyxl não gera arquivos válidos com fórmulas modernas** (LET, LAMBDA, MAP, PROCX) - o Excel remove as fórmulas ao abrir.

**Solução**: Fórmulas de spill criadas manualmente no `template.xlsm`, script Python só preenche dados.

### Fórmulas de Spill no Template
As fórmulas em `COMPOSICOES` (colunas E, H, I, J, K, L, M) e `ESCOPO` (F, G) devem ser mantidas no `template.xlsm`. Os scripts Python (`abas/composicoes.py` e `abas/escopo.py`) devem apenas formatar as células e garantir que estão vazias para o "derramamento" (spill) das fórmulas.

### Funções Excel PT-BR
| Função | Excel PT-BR |
|--------|-------------|
| XLOOKUP | PROCX |
| VSTACK | EMPILHARV |
| SUMIFS | SOMASES |
| IF/OR | SE/OU |
| IFERROR | SEERRO |
| LET/LAMBDA/MAP | Mantém inglês |

**Separador de argumentos**: `;` (ponto-e-vírgula)
**Operador de spill**: `#` (ex: `A2#`)

---

## Referência Técnica Detalhada

### Sistema de Importação CSV

**Estrutura de arquivos**:
```
dados_csv/
├── materiais_{YYYY-MM-DD}.csv
├── mao_de_obra_{YYYY-MM-DD}.csv
├── ferramentas_{YYYY-MM-DD}.csv
└── equipamentos_{YYYY-MM-DD}.csv
```

**Especificações**: UTF-8 com BOM, delimitador `;`, CRLF

**Schema materiais/equipamentos**:
```csv
CODIGO;CATEGORIA;DESCRICAO;UNIDADE;PRECO;ATUALIZADO_EM;VALIDADE_DIAS
```

**Validades padrão**: MAT=7 dias, MO=30 dias, FER=90 dias, EQP=30 dias

### Macros VBA

| Macro | Função |
|-------|--------|
| `ImportarTodosCatalogos()` | Importa todos os CSVs |
| `VerificarValidade()` | Verifica itens vencidos |
| `NovaComposicao()` | Wizard para criar composição |
| `AtualizarSelecao()` | Propaga fórmulas de seleção |

### Conceitos-Chave

**Quantidades Variáveis**: Composições suportam `Qtd Base` (fixa por instalação) e `Qtd Var` (por metro de linha frigorígena).

**BDI vs Markup**: A aba NEGOCIO permite escolher entre BDI (componentes detalhados) ou Markup (percentual simples por tipo).

**Multiplicadores**: Calculados automaticamente em NEGOCIO (B42-B45) e aplicados em COMPOSICOES (colunas L-M).

### Adicionando Novos Itens

1. Edite o arquivo correspondente em `dados/`
2. Regenere com `python3 criar_planilha.py`

Para composições em `dados/composicoes.py`:
- Tuplas `(Tipo, Código, Qtd_Base, Qtd_por_Metro)`
- Campos opcionais: `desc_pre`, `desc_pos`, `unid_sing`, `unid_plur`

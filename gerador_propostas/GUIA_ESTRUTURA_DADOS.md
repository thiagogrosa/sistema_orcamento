# Guia de Estrutura de Dados para Orçamentos HVAC

Este documento descreve a estrutura de dados utilizada para criação de orçamentos de instalação de sistemas HVAC (ar-condicionado Split). O objetivo é permitir que agentes automatizados compreendam e utilizem essas bases para gerar orçamentos.

---

## 1. Visão Geral do Sistema

O sistema de orçamentação é composto por três camadas:

```
┌─────────────────────────────────────────────────────────────┐
│                      ORÇAMENTO (Escopo)                     │
│   Seleção de composições e itens avulsos com quantidades    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ referencia
┌─────────────────────────────────────────────────────────────┐
│                       COMPOSIÇÕES                           │
│   Agrupamentos de itens que formam um serviço completo      │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ utiliza
┌─────────────────────────────────────────────────────────────┐
│                    CATÁLOGOS (Bases)                        │
│   Materiais │ Mão de Obra │ Ferramentas │ Equipamentos      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Catálogos (Bases de Dados)

Os catálogos são as bases primitivas que contêm os itens individuais com seus custos unitários.

### 2.1. Materiais (MAT)

Insumos físicos consumidos na instalação.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| codigo | string | Identificador único (prefixo `MAT_` ou sem prefixo) |
| categoria | string | Agrupamento (ex: "Tubulação", "Elétrico", "Fixação") |
| descricao | string | Nome descritivo do material |
| unidade | string | Unidade de medida: M (metro), UN (unidade), KG, PCT, etc. |
| preco | decimal | Preço unitário (custo de aquisição) |

**Exemplo:**
```json
{
  "codigo": "TUB_14_FLEX",
  "categoria": "Tubulação",
  "descricao": "Tubo de cobre 1/4\" flexível",
  "unidade": "M",
  "preco": 18.00
}
```

### 2.2. Mão de Obra (MO)

Serviços de profissionais envolvidos na instalação.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| codigo | string | Identificador único (prefixo `MO_`) |
| categoria | string | Tipo de serviço (ex: "Instalação", "Elétrica") |
| descricao | string | Descrição do serviço/profissional |
| unidade | string | Unidade: H (hora), UN (serviço fixo), M² (área) |
| custo | decimal | Custo por unidade |

**Exemplo:**
```json
{
  "codigo": "MO_TEC",
  "categoria": "Instalação",
  "descricao": "Técnico em refrigeração",
  "unidade": "H",
  "custo": 65.00
}
```

### 2.3. Ferramentas (FER)

Equipamentos utilizados na execução (custo de depreciação/hora).

| Campo | Tipo | Descrição |
|-------|------|-----------|
| codigo | string | Identificador único (prefixo `FER_`) |
| categoria | string | Tipo de ferramenta (ex: "Vácuo", "Solda") |
| descricao | string | Descrição da ferramenta |
| valor_aquisicao | decimal | Valor de compra do equipamento |
| vida_util_horas | integer | Vida útil estimada em horas de uso |
| custo_hora | decimal | **Calculado**: valor_aquisicao / vida_util_horas |

**Exemplo:**
```json
{
  "codigo": "FER_VACUO",
  "categoria": "Vácuo",
  "descricao": "Bomba de vácuo",
  "valor_aquisicao": 1500.00,
  "vida_util_horas": 2000,
  "custo_hora": 0.75
}
```

### 2.4. Equipamentos (EQP)

Equipamentos principais vendidos ao cliente (ar-condicionado, bombas, etc.).

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| codigo | string | Sim | Identificador único (prefixo `EQP_`) |
| categoria | string | Sim | Categoria: "Split", "VRF", "Bomba Dreno" |
| tipo | string | Sim | Subtipo: "Hi-Wall", "Piso-Teto", "Cassete", "Mini" |
| descricao | string | Sim | Descrição completa |
| capacidade_btu | integer | Sim | Capacidade em BTUs (0 para acessórios) |
| tecnologia | string | Sim | "Inverter" ou "On-Off" |
| ciclo | string | Sim | "Frio" ou "Quente/Frio" |
| marca | string | Não | Fabricante |
| modelo | string | Não | Código do fabricante |
| tensao_fase | string | Sim | "220V Mono", "220V Tri", "380V Tri" |
| alimentacao | string | Sim | Bitola do cabo: "2,5mm²", "4mm²", "6mm²" |
| comando | string | Não | Cabo de comando: "5x1,0mm²" |
| gas_pol | string | Sim | Bitola linha de gás: "3/8\"", "1/2\"" |
| liquido_pol | string | Sim | Bitola linha de líquido: "1/4\"", "3/8\"" |
| comp_max_m | integer | Não | Comprimento máximo da tubulação |
| unidade | string | Sim | Sempre "UN" |
| preco | decimal | Sim | Preço de venda |
| vendedor | string | Não | Fornecedor preferencial |

**Exemplo:**
```json
{
  "codigo": "EQP_HW_12K",
  "categoria": "Split",
  "tipo": "Hi-Wall",
  "descricao": "Split Hi-Wall Inverter 12.000 BTUs",
  "capacidade_btu": 12000,
  "tecnologia": "Inverter",
  "ciclo": "Frio",
  "marca": "Daikin",
  "tensao_fase": "220V Mono",
  "alimentacao": "2,5mm²",
  "comando": "5x1,0mm²",
  "gas_pol": "3/8\"",
  "liquido_pol": "1/4\"",
  "comp_max_m": 20,
  "unidade": "UN",
  "preco": 2200.00
}
```

---

## 3. Composições

Composições são **agrupamentos de itens** dos catálogos que, juntos, formam um serviço completo. Uma composição representa o custo total para executar uma atividade específica.

### 3.1. Estrutura da Composição

| Campo | Tipo | Descrição |
|-------|------|-----------|
| codigo | string | Identificador único (prefixo `COMP_`) |
| descricao | string | Nome do serviço |
| desc_pre | string | Texto descritivo antes da variável (opcional) |
| desc_pos | string | Texto descritivo após a variável (opcional) |
| unid_sing | string | Unidade singular para descrição (ex: "metro") |
| unid_plur | string | Unidade plural para descrição (ex: "metros") |
| itens | array | Lista de itens que compõem o serviço |

### 3.2. Estrutura dos Itens

Cada item dentro de uma composição possui:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| tipo | string | Tipo do item: "MAT", "MO", "FER" ou "EQP" |
| codigo | string | Código do item no catálogo correspondente |
| qtd_base | decimal | Quantidade fixa por execução |
| qtd_var | decimal | Quantidade variável por unidade de medida |

### 3.3. Sistema de Quantidades (CRÍTICO)

O sistema utiliza **dois tipos de quantidade** para cada item:

#### Quantidade Base (`qtd_base`)
- Quantidade **fixa** consumida independente do tamanho do serviço
- Representa o mínimo necessário para iniciar o trabalho
- Exemplo: 1 instalador é necessário mesmo para 1 metro de tubulação

#### Quantidade Variável (`qtd_var`)
- Quantidade que **escala** proporcionalmente ao input variável
- O input variável é definido pela **composição**, não pelo item
- **NÃO é necessariamente metros** - pode ser: m², unidades, kg, horas, etc.

#### Exemplos de Variação por Tipo de Composição

| Composição | Unidade Variável | Exemplo |
|------------|------------------|---------|
| Instalação de tubulação | Metro linear | 5 metros de linha frigorígena |
| Pintura de parede | Metro quadrado | 20 m² de área |
| Instalação de pontos elétricos | Unidade | 3 pontos de tomada |
| Concretagem | Metro cúbico | 2 m³ de concreto |
| Instalação de splits | Unidade | 4 aparelhos |

### 3.4. Cálculo de Quantidade Total

Para cada item em uma composição:

```
quantidade_total = qtd_base + (qtd_var × input_variavel)
```

**Exemplo prático:**

Composição: "Instalação de linha frigorígena"
- Unidade variável: metros de linha

Item: Tubo de cobre 3/8"
- qtd_base: 0 (não há quantidade fixa)
- qtd_var: 1.1 (10% de folga para perdas)

Para uma instalação com **8 metros** de linha:
```
quantidade_tubo = 0 + (1.1 × 8) = 8.8 metros
```

Item: Técnico instalador
- qtd_base: 2 (mínimo 2 horas mesmo para linhas curtas)
- qtd_var: 0.5 (meia hora adicional por metro)

Para os mesmos **8 metros**:
```
quantidade_mo = 2 + (0.5 × 8) = 6 horas
```

### 3.5. Exemplo Completo de Composição

```json
{
  "codigo": "COMP_INST_SPLIT_12K",
  "descricao": "Instalação completa Split 12.000 BTUs",
  "desc_pre": "Instalação com",
  "desc_pos": "de linha frigorígena",
  "unid_sing": "metro",
  "unid_plur": "metros",
  "itens": [
    {"tipo": "EQP", "codigo": "EQP_HW_12K", "qtd_base": 1, "qtd_var": 0},
    {"tipo": "MAT", "codigo": "TUB_38_FLEX", "qtd_base": 0, "qtd_var": 1.1},
    {"tipo": "MAT", "codigo": "TUB_14_FLEX", "qtd_base": 0, "qtd_var": 1.1},
    {"tipo": "MAT", "codigo": "ISO_38", "qtd_base": 0, "qtd_var": 2.2},
    {"tipo": "MAT", "codigo": "CABO_PP_3X25", "qtd_base": 0, "qtd_var": 1.1},
    {"tipo": "MAT", "codigo": "CABO_CMD", "qtd_base": 0, "qtd_var": 1.1},
    {"tipo": "MAT", "codigo": "SUPORTE_COND", "qtd_base": 1, "qtd_var": 0},
    {"tipo": "MO", "codigo": "MO_TEC", "qtd_base": 3, "qtd_var": 0.5},
    {"tipo": "MO", "codigo": "MO_AUX", "qtd_base": 3, "qtd_var": 0.5},
    {"tipo": "FER", "codigo": "FER_VACUO", "qtd_base": 1, "qtd_var": 0},
    {"tipo": "FER", "codigo": "FER_MANDRILADOR", "qtd_base": 0.5, "qtd_var": 0.1}
  ]
}
```

---

## 4. Orçamento (Escopo)

O orçamento é a seleção final de itens e composições com suas quantidades específicas para um projeto.

### 4.1. Estrutura de Linha do Orçamento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| tipo | string | "COMP", "EQP", "MAT", "MO" ou "FER" |
| codigo | string | Código do item ou composição |
| quantidade | decimal | Quantidade de execuções/unidades |
| variavel | decimal | Input variável (quando aplicável) |

### 4.2. Cálculo de Custos

#### Para Itens Avulsos (EQP, MAT, MO, FER)
```
custo_total = preco_unitario × quantidade
```

#### Para Composições
```
Para cada item da composição:
  qtd_item = qtd_base + (qtd_var × variavel)
  custo_item = preco_unitario × qtd_item

custo_composicao = soma(custo_item para todos os itens)
custo_total = custo_composicao × quantidade
```

### 4.3. Exemplo de Orçamento

```json
{
  "cliente": "João Silva",
  "data": "2025-01-03",
  "itens": [
    {
      "tipo": "COMP",
      "codigo": "COMP_INST_SPLIT_12K",
      "quantidade": 2,
      "variavel": 5,
      "descricao_gerada": "Instalação com 5 metros de linha frigorígena"
    },
    {
      "tipo": "COMP",
      "codigo": "COMP_INST_SPLIT_24K",
      "quantidade": 1,
      "variavel": 8,
      "descricao_gerada": "Instalação com 8 metros de linha frigorígena"
    },
    {
      "tipo": "EQP",
      "codigo": "EQP_BOMB_P",
      "quantidade": 2,
      "variavel": null,
      "descricao_gerada": "Bomba dreno mini"
    }
  ]
}
```

---

## 5. Sistema de Margem (BDI/Markup)

Os custos dos catálogos representam o **custo de aquisição**. Para formar o preço de venda, aplica-se uma margem.

### 5.1. Multiplicadores por Tipo

| Tipo | Descrição | Margem Típica |
|------|-----------|---------------|
| MAT | Materiais | 35% |
| MO | Mão de Obra | 40% |
| FER | Ferramentas | 30% |
| EQP | Equipamentos | 25% |

### 5.2. Cálculo do Preço de Venda

```
multiplicador = 1 + (margem / 100)
preco_venda = custo × multiplicador
```

**Exemplo:**
```
Custo material: R$ 100,00
Margem MAT: 35%
Multiplicador: 1.35
Preço venda: R$ 100,00 × 1.35 = R$ 135,00
```

---

## 6. Fluxo de Criação de Orçamento (Para Agentes)

### Passo 1: Identificar Necessidades do Cliente
- Quantos equipamentos?
- Quais capacidades (BTUs)?
- Qual a metragem das linhas frigorígenas?
- Há necessidade de bomba de dreno?
- Infraestrutura elétrica existente?

### Passo 2: Selecionar Composições Adequadas
- Buscar composições que atendam às necessidades
- Cada equipamento geralmente tem uma composição de instalação correspondente

### Passo 3: Definir Quantidades
- **quantidade**: Quantas vezes o serviço será executado
- **variavel**: Valor do input variável (metros, m², unidades, etc.)

### Passo 4: Adicionar Itens Avulsos (se necessário)
- Equipamentos adicionais
- Materiais extras não previstos nas composições
- Serviços especiais

### Passo 5: Calcular Totais
- Somar custos de todas as composições e itens
- Aplicar margem por tipo
- Gerar preço final

---

## 7. Exemplo Completo: Orçamento de Instalação

**Cenário:** Cliente precisa instalar 2 splits de 12.000 BTUs em quartos (5m de linha cada) e 1 split de 24.000 BTUs na sala (8m de linha). Um dos quartos precisa de bomba de dreno.

### Seleção de Itens:

| # | Tipo | Código | Qtd | Variável | Descrição |
|---|------|--------|-----|----------|-----------|
| 1 | COMP | COMP_INST_SPLIT_12K | 2 | 5 | Instalação Split 12K - 5m linha |
| 2 | COMP | COMP_INST_SPLIT_24K | 1 | 8 | Instalação Split 24K - 8m linha |
| 3 | COMP | COMP_BOMB_DRN | 1 | 0 | Instalação bomba de dreno |

### Cálculo (simplificado):

```
Composição 1 (COMP_INST_SPLIT_12K × 2, variável=5):
  - Equipamento: 1 × R$ 2.200 = R$ 2.200 (por execução)
  - Materiais: ~R$ 450 (5m de tubulação, isolamento, cabos)
  - Mão de obra: 5.5h × R$ 65 = R$ 357,50
  - Ferramentas: ~R$ 15
  Subtotal por execução: ~R$ 3.022,50
  Total (×2): R$ 6.045,00

Composição 2 (COMP_INST_SPLIT_24K × 1, variável=8):
  - Equipamento: 1 × R$ 4.200 = R$ 4.200
  - Materiais: ~R$ 680 (8m de tubulação mais grossa)
  - Mão de obra: 7h × R$ 65 = R$ 455
  - Ferramentas: ~R$ 20
  Subtotal: ~R$ 5.355,00

Composição 3 (COMP_BOMB_DRN × 1):
  - Equipamento: 1 × R$ 320 = R$ 320
  - Materiais: ~R$ 45
  - Mão de obra: 1h × R$ 65 = R$ 65
  Subtotal: ~R$ 430,00

CUSTO TOTAL: ~R$ 11.830,00
+ Margem média (~30%): ~R$ 3.549,00
PREÇO DE VENDA: ~R$ 15.379,00
```

---

## 8. Considerações para Agentes

### 8.1. Validações Importantes
- Verificar se o equipamento selecionado é compatível com a composição
- Confirmar que a metragem da linha não excede o `comp_max_m` do equipamento
- Validar que a infraestrutura elétrica atende à `tensao_fase` e `alimentacao`

### 8.2. Otimizações Possíveis
- Sugerir equipamentos Inverter para maior eficiência energética
- Recomendar bomba de dreno quando a evaporadora não permite dreno por gravidade
- Alertar sobre necessidade de adequação elétrica para equipamentos maiores

### 8.3. Informações para Descrição
- Usar `desc_pre` + variável + `unid_sing/plur` + `desc_pos` para gerar descrições
- Exemplo: "Instalação com **5 metros** de linha frigorígena"

---

## 9. Resumo das Relações

```
CATÁLOGOS (código → dados)
    │
    ├── MAT_* → {descricao, unidade, preco}
    ├── MO_*  → {descricao, unidade, custo}
    ├── FER_* → {descricao, custo_hora}
    └── EQP_* → {descricao, especificacoes_tecnicas, preco}
          │
          ▼
COMPOSIÇÕES (código → {descricao, itens[]})
    │
    └── itens[]: {tipo, codigo, qtd_base, qtd_var}
          │
          ▼
ORÇAMENTO (cliente, itens[])
    │
    └── itens[]: {tipo, codigo, quantidade, variavel}
```

**A chave do sistema é entender que:**
1. Catálogos definem **o que existe** e **quanto custa**
2. Composições definem **como combinar** os itens e **como escalam**
3. Orçamento define **quanto será feito** de cada composição/item

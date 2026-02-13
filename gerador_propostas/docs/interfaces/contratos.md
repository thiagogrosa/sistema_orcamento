# Contratos de Interface Entre Skills

> Este documento define os formatos de entrada e saida de cada skill.
> Cada skill deve conhecer apenas suas interfaces, nao a implementacao das outras.

---

## Visao Geral do Fluxo

```
┌──────────┐   entrada   ┌──────────┐   escopo   ┌───────────┐   composicao   ┌─────────────┐   precificado   ┌────────┐
│ USUARIO  │ ──────────► │ EXTRATOR │ ─────────► │COMPOSITOR │ ─────────────► │PRECIFICADOR │ ──────────────► │ OUTPUT │
└──────────┘             └──────────┘            └───────────┘                └─────────────┘                 └────────┘
```

---

## 1. Entrada do Usuario → Skill Mestre

### Tipos de Entrada Aceitos

```typescript
type EntradaUsuario =
  | string                    // Texto livre
  | { path: string }          // Caminho para arquivo
  | { conteudo: string, tipo: "texto" | "pdf" | "edital" }
```

### Exemplos

```json
// Texto simples
"Instalar 2 splits 12000 BTU no escritorio, cliente PJ"

// Arquivo
{ "path": "/home/user/relatorio-visita.pdf" }

// Conteudo tipado
{ "conteudo": "...", "tipo": "edital" }
```

---

## 2. Skill Mestre → Extrator

### Contrato de Entrada

```json
{
  "entrada": "string | conteudo do arquivo",
  "tipo": "texto" | "pdf" | "edital",
  "contexto": {
    "cliente_informado": "string | null",
    "tipo_cliente_informado": "PRIVADO-PJ" | "PRIVADO-PF" | "GOVERNO" | null
  }
}
```

---

## 3. Extrator → Compositor

### Contrato: `escopo.json`

```json
{
  "projeto": {
    "nome": "string",
    "cliente": "string | null",
    "tipo_cliente": "PRIVADO-PJ" | "PRIVADO-PF" | "GOVERNO",
    "endereco": "string | null",
    "contato": "string | null",
    "data_visita": "YYYY-MM-DD | null",
    "prazo_execucao": "string | null"
  },
  "itens": [
    {
      "id": "number",
      "ambiente": "string",
      "area_m2": "number | null",
      "carga_termica_btu": "number | null",
      "tipo_equipamento": "split-hi-wall" | "split-piso-teto" | "cassete" | "multi-split" | "vrv",
      "capacidade_btu": "number",
      "servico": "instalacao-completa" | "apenas-instalacao" | "manutencao-preventiva" | "manutencao-corretiva" | "desinstalacao",
      "quantidade": "number",
      "observacoes": "string | null"
    }
  ],
  "condicoes_gerais": {
    "distancia_media_tubulacao_m": "number",
    "necessita_infra_eletrica": "boolean",
    "altura_trabalho_m": "number",
    "acesso_dificil": "boolean",
    "necessita_andaime": "boolean",
    "horario_especial": "boolean",
    "observacoes_gerais": "string | null"
  },
  "itens_adicionais_identificados": ["string"],
  "alertas": ["string"]
}
```

### Exemplo

```json
{
  "projeto": {
    "nome": "Instalacao splits - Escritorio ABC",
    "cliente": "Empresa ABC Ltda",
    "tipo_cliente": "PRIVADO-PJ"
  },
  "itens": [
    {
      "id": 1,
      "ambiente": "Sala de reunioes",
      "area_m2": 25,
      "capacidade_btu": 18000,
      "tipo_equipamento": "split-hi-wall",
      "servico": "instalacao-completa",
      "quantidade": 1,
      "observacoes": "Carga calculada: 25m2 x 700 BTU/m2"
    }
  ],
  "condicoes_gerais": {
    "distancia_media_tubulacao_m": 5,
    "necessita_infra_eletrica": false,
    "altura_trabalho_m": 2.8,
    "acesso_dificil": false,
    "necessita_andaime": false
  },
  "alertas": []
}
```

---

## 4. Compositor → Precificador

### Contrato: `composicao.json`

```json
{
  "projeto": "string",
  "data_composicao": "YYYY-MM-DD",
  "itens_orcamento": [
    {
      "id": "number",
      "descricao": "string",
      "composicao_base": "string (codigo da composicao)",
      "quantidade": "number",
      "unidade": "string",
      "materiais": [
        {
          "codigo": "string",
          "descricao": "string",
          "quantidade": "number",
          "unidade": "string"
        }
      ],
      "mao_de_obra": [
        {
          "categoria": "TECNICO-HVAC" | "AJUDANTE" | "ELETRICISTA",
          "horas": "number"
        }
      ]
    }
  ],
  "resumo_materiais": [
    {
      "codigo": "string",
      "descricao": "string",
      "quantidade_total": "number",
      "unidade": "string"
    }
  ],
  "resumo_mao_obra": [
    {
      "categoria": "string",
      "horas_totais": "number"
    }
  ],
  "observacoes_composicao": ["string"]
}
```

---

## 5. Precificador → Output

### Contrato: `precificado.json`

```json
{
  "projeto": "string",
  "cliente": "string",
  "tipo_cliente": "PRIVADO-PJ" | "PRIVADO-PF" | "GOVERNO",
  "data_orcamento": "YYYY-MM-DD",
  "validade_dias": "number",

  "itens_precificados": [
    {
      "id": "number",
      "descricao": "string",
      "quantidade": "number",
      "unidade": "string",
      "custo_materiais": "number",
      "custo_mao_obra": "number",
      "custo_direto": "number",
      "bdi_aplicado": "number (decimal)",
      "valor_bdi": "number",
      "preco_unitario": "number",
      "preco_total": "number"
    }
  ],

  "resumo_financeiro": {
    "total_materiais": "number",
    "total_mao_obra": "number",
    "custo_direto_total": "number",
    "bdi_percentual": "number (decimal)",
    "valor_bdi_total": "number",
    "valor_total_orcamento": "number"
  },

  "composicao_percentual": {
    "materiais": "number (percentual)",
    "mao_de_obra": "number (percentual)",
    "bdi": "number (percentual)"
  },

  "alertas": ["string"],

  "condicoes_comerciais": {
    "validade": "string",
    "forma_pagamento": "string",
    "prazo_execucao": "string",
    "garantia": "string"
  }
}
```

---

## 6. Output → Usuario

### Arquivos Gerados

| Formato | Arquivo | Descricao |
|---------|---------|-----------|
| PDF | `ORC-[CLIENTE]-[DATA].pdf` | Proposta comercial para cliente |
| XLSX | `ORC-[CLIENTE]-[DATA]-interno.xlsx` | Planilha detalhada interna |
| MD | `ORC-[CLIENTE]-[DATA]-resumo.md` | Resumo para resposta rapida |

### Estrutura do PDF

```
┌────────────────────────────────────────┐
│ CABECALHO (logo, dados empresa)        │
├────────────────────────────────────────┤
│ DADOS DO CLIENTE                       │
│ - Nome, endereco, contato              │
├────────────────────────────────────────┤
│ ESCOPO DOS SERVICOS                    │
│ - Lista de itens                       │
├────────────────────────────────────────┤
│ TABELA DE PRECOS                       │
│ Item | Descricao | Qtd | Valor         │
├────────────────────────────────────────┤
│ CONDICOES COMERCIAIS                   │
│ - Validade, pagamento, prazo           │
├────────────────────────────────────────┤
│ RODAPE (assinatura, data)              │
└────────────────────────────────────────┘
```

---

## Bases de Dados

### composicoes-split.json

```json
{
  "composicoes": {
    "INST-SPLIT-9K": { ... },
    "INST-SPLIT-12K": { ... }
  },
  "metadata": {
    "versao": "string",
    "data_atualizacao": "YYYY-MM-DD"
  }
}
```

### precos.json

```json
{
  "materiais": {
    "TUB-CU-1/4": {
      "descricao": "string",
      "unidade": "string",
      "preco": "number",
      "data_cotacao": "YYYY-MM-DD"
    }
  },
  "mao_de_obra": {
    "TECNICO-HVAC": {
      "descricao": "string",
      "custo_hora": "number"
    }
  },
  "metadata": { ... }
}
```

### bdi.json

```json
{
  "PRIVADO-PJ": { "percentual": 0.35 },
  "PRIVADO-PF": { "percentual": 0.40 },
  "GOVERNO": { "percentual": 0.25 },
  "MANUTENCAO-CONTRATO": { "percentual": 0.30 }
}
```

### fornecedores.json

```json
{
  "fornecedores": [
    {
      "id": "string",
      "nome": "string",
      "categorias": ["cobre", "gas", "eletrica"],
      "email": "string",
      "telefone": "string",
      "observacoes": "string"
    }
  ]
}
```

---

## Tratamento de Erros

### Formato Padrao de Erro

```json
{
  "sucesso": false,
  "erro": {
    "codigo": "string",
    "mensagem": "string",
    "detalhes": "string | null"
  },
  "dados_parciais": "object | null"
}
```

### Codigos de Erro

| Codigo | Descricao |
|--------|-----------|
| `ENTRADA_INVALIDA` | Formato de entrada nao reconhecido |
| `COMPOSICAO_NAO_ENCONTRADA` | Servico sem composicao na base |
| `PRECO_NAO_ENCONTRADO` | Material sem preco cadastrado |
| `PRECO_DESATUALIZADO` | Preco com mais de 90 dias |
| `ARQUIVO_NAO_ENCONTRADO` | Path informado nao existe |

---

*Documento de interfaces - Sistema de Orcamentacao HVAC*

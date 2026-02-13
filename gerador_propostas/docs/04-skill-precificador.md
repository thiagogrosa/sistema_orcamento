# Skill Precificadora: hvac-precificador

> **Modelo recomendado:** SONNET (regras de negocio)
> **Responsabilidade:** Aplicar precos e calcular valores finais

---

## Objetivo

Aplicar precos aos materiais e mao de obra, calcular custos diretos, aplicar BDI e gerar resumo financeiro completo.

---

## Processo

### 1. Carregar Bases

```
Ler: bases/precos.json
Ler: bases/bdi.json
```

### 2. Precificar Materiais

```
PARA CADA material em resumo_materiais:
   preco_unitario = precos.materiais[codigo].preco
   valor = preco_unitario x quantidade_total

   SE preco nao encontrado:
      alertas.adicionar("Material sem preco: " + codigo)
      marcar como PRECO_PENDENTE
```

### 3. Precificar Mao de Obra

```
PARA CADA categoria em resumo_mao_obra:
   custo_hora = precos.mao_de_obra[categoria].custo_hora
   valor = custo_hora x horas_totais
```

### 4. Calcular Custos por Item

```
PARA CADA item em itens_orcamento:
   custo_materiais = soma(materiais do item)
   custo_mao_obra = soma(mao de obra do item)
   custo_direto = custo_materiais + custo_mao_obra
```

### 5. Aplicar BDI

```
bdi_percentual = bdi[tipo_cliente].percentual

PARA CADA item:
   valor_bdi = custo_direto x bdi_percentual
   preco_total = custo_direto x (1 + bdi_percentual)
   preco_unitario = preco_total / quantidade
```

### 6. Calcular Resumo Financeiro

```
total_materiais = soma(custo_materiais de todos os itens)
total_mao_obra = soma(custo_mao_obra de todos os itens)
custo_direto_total = total_materiais + total_mao_obra
valor_bdi_total = custo_direto_total x bdi_percentual
valor_total = custo_direto_total + valor_bdi_total
```

---

## Tabela de BDI

| Tipo Cliente | BDI | Descricao |
|--------------|-----|-----------|
| PRIVADO-PJ | 35% | Empresa privada |
| PRIVADO-PF | 40% | Pessoa fisica |
| GOVERNO | 25% | Licitacao publica |
| MANUTENCAO-CONTRATO | 30% | Contrato recorrente |

---

## Regras de Negocio

### Arredondamento

- Valores unitarios: 2 casas decimais
- Valores totais: 2 casas decimais
- Arredondar para cima no valor final

### Precos Desatualizados

```
SE data_cotacao do preco > 90 dias:
   alertas.adicionar("Preco desatualizado: " + codigo)

SE data_cotacao > 180 dias:
   alertas.adicionar("CRITICO: Preco muito antigo")
   considerar correcao de 5%
```

### Margem Minima

```
SE bdi < 0.20:
   alertas.adicionar("Margem abaixo de 20% - revisar")
```

### Descontos por Volume

```
SE quantidade_equipamentos > 5:
   sugerir_desconto = 5%

SE quantidade_equipamentos > 10:
   sugerir_desconto = 10%

Registrar como opcional no orcamento
```

---

## Output

### Formato: precificado.json

```json
{
  "projeto": "Nome do projeto",
  "cliente": "Nome do cliente",
  "tipo_cliente": "PRIVADO-PJ",
  "data_orcamento": "2026-01-02",
  "validade_dias": 15,

  "itens_precificados": [
    {
      "id": 1,
      "descricao": "Instalacao split 12K - Recepcao",
      "quantidade": 1,
      "unidade": "un",
      "custo_materiais": 580.50,
      "custo_mao_obra": 390.00,
      "custo_direto": 970.50,
      "bdi_aplicado": 0.35,
      "valor_bdi": 339.68,
      "preco_unitario": 1310.18,
      "preco_total": 1310.18
    }
  ],

  "resumo_financeiro": {
    "total_materiais": 1741.50,
    "total_mao_obra": 1170.00,
    "custo_direto_total": 2911.50,
    "bdi_percentual": 0.35,
    "valor_bdi_total": 1019.03,
    "valor_total_orcamento": 3930.53
  },

  "composicao_percentual": {
    "materiais": 44.3,
    "mao_de_obra": 29.8,
    "bdi": 25.9
  },

  "alertas": [],

  "condicoes_comerciais": {
    "validade": "15 dias",
    "forma_pagamento": "A definir",
    "prazo_execucao": "A definir",
    "garantia": "90 dias para servicos"
  }
}
```

---

## Formatacao de Valores

### Moeda

```
Formato: R$ X.XXX,XX
Separador milhar: ponto
Separador decimal: virgula

Exemplo: R$ 3.930,53
```

### Percentuais

```
Formato: XX,X%
Exemplo: 35,0%
```

---

*Especificacao da Skill Precificadora - Sistema HVAC*

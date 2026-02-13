---
name: hvac-precificador
description: Aplica precos e calcula BDI para orcamentos HVAC. Subagente do hvac - precifica materiais, mao de obra e ferramentas, gerando valor final.
model: claude-3-5-haiku-20241022
allowed-tools: Read, Write, Bash
---

# hvac-precificador - Precificador HVAC

Aplica precos aos insumos e calcula valores finais com BDI.

## Modo de Execucao

Este skill usa um **script Python** para processamento deterministico:

```bash
python -m hvac.precificador --input <composicao.json> --output <precificado.json>
```

## Entrada

JSON `composicao.json` (output do hvac-compositor)

## Saida

JSON `precificado.json` com estrutura:

```json
{
  "projeto": "string",
  "cliente": "string",
  "data_orcamento": "YYYY-MM-DD",
  "validade_dias": 15,
  "itens_precificados": [{
    "id": 1,
    "descricao": "string",
    "composicao": "COMP_INST_9K",
    "quantidade": 1,
    "variavel": 5,
    "materiais": [{"codigo": "...", "descricao": "...", "quantidade": 5.5, "unidade": "M", "preco_unitario": 18.00, "custo": 99.00}],
    "mao_de_obra": [...],
    "ferramentas": [...],
    "equipamentos": [...],
    "custo_materiais": 450.00,
    "custo_mao_obra": 200.00,
    "custo_ferramentas": 15.00,
    "custo_equipamentos": 0.00,
    "custo_direto": 665.00,
    "bdi": 220.00,
    "preco_total": 885.00
  }],
  "resumo_financeiro": {
    "total_materiais": 450.00,
    "total_mao_obra": 200.00,
    "total_ferramentas": 15.00,
    "total_equipamentos": 0.00,
    "custo_direto": 665.00,
    "bdi_materiais": 157.50,
    "bdi_mao_obra": 80.00,
    "bdi_ferramentas": 4.50,
    "bdi_equipamentos": 0.00,
    "total_bdi": 242.00,
    "valor_total": 907.00,
    "percentuais_bdi": {
      "MAT": "35%",
      "MO": "40%",
      "FER": "30%",
      "EQP": "25%"
    }
  },
  "alertas": []
}
```

## Fluxo de Trabalho

1. **Receber** composicao.json do hvac-compositor
2. **Executar** script Python:
   ```bash
   python -m hvac.precificador -i output/2026-01/composicao.json -o output/2026-01/precificado.json
   ```
3. **Ler** precificado.json gerado
4. **Retornar** resultado para skill mestre

## Calculo de Precos (feito pelo script)

### Por Item
```
custo_material = preco_unitario × quantidade
custo_mo = custo_hora × horas
custo_fer = custo_hora × horas
custo_direto = materiais + mao_obra + ferramentas + equipamentos
```

### BDI por Tipo de Insumo
```
bdi_mat = custo_materiais × 0.35 (35%)
bdi_mo = custo_mao_obra × 0.40 (40%)
bdi_fer = custo_ferramentas × 0.30 (30%)
bdi_eqp = custo_equipamentos × 0.25 (25%)

preco_final = custo_direto + total_bdi
```

## Bases de Dados Usadas

O script le automaticamente de `bases/`:
- `materiais.json` - precos de materiais (campo: preco)
- `mao_de_obra.json` - custo/hora por categoria (campo: custo_hora)
- `ferramentas.json` - custo/hora (campo: custo_hora)
- `equipamentos.json` - precos (campo: preco)
- `bdi.json` - percentuais por tipo de insumo

## Alertas Gerados

O script gera alertas automaticos quando:
- Preco com mais de 90 dias: "alerta"
- Preco com mais de 180 dias: "critico"
- Item sem preco cadastrado

## Exemplo de Uso

```bash
# Executar precificador
python -m hvac.precificador \
  --input output/2026-01/composicao.json \
  --output output/2026-01/precificado.json

# Output esperado:
# Orcamento precificado: output/2026-01/precificado.json
#   Custo direto: R$ 665.00
#   BDI total:    R$ 242.00
#   VALOR TOTAL:  R$ 907.00
```

## Formatacao

- Valores: 2 casas decimais
- Moeda: R$ (formatacao no output final)

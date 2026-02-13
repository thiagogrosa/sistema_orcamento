---
name: hvac-compositor
description: Compoe lista de materiais, mao de obra e ferramentas a partir do escopo HVAC. Subagente do hvac - consulta bases de dados e calcula quantidades.
model: claude-3-5-haiku-20241022
allowed-tools: Read, Write, Bash
---

# hvac-compositor - Compositor de Servicos HVAC

Transforma escopo estruturado em lista detalhada de materiais, mao de obra e ferramentas.

## Modo de Execucao

Este skill usa um **script Python** para processamento deterministico:

```bash
python -m hvac.compositor --input <escopo.json> --output <composicao.json>
```

## Entrada

JSON `escopo.json` (output do hvac-extrator)

## Saida

JSON `composicao.json` com estrutura:

```json
{
  "projeto": "string",
  "cliente": "string",
  "data_composicao": "YYYY-MM-DD",
  "itens_orcamento": [{
    "id": 1,
    "descricao": "Instalacao Split 12K com 5 metros de linha",
    "composicao": "COMP_INST_9K",
    "quantidade": 1,
    "variavel": 5,
    "materiais": [{"codigo": "TUB_14_FLEX", "descricao": "...", "quantidade": 5.5, "unidade": "M"}],
    "mao_de_obra": [{"codigo": "MO_TEC", "descricao": "...", "quantidade": 2.75, "unidade": "H"}],
    "ferramentas": [{"codigo": "FER_VACUO", "descricao": "...", "quantidade": 0.5, "unidade": "H"}],
    "equipamentos": []
  }],
  "resumo_materiais": [{"codigo": "...", "descricao": "...", "quantidade": 0, "unidade": "..."}],
  "resumo_mao_obra": [{"codigo": "...", "descricao": "...", "quantidade": 0, "unidade": "H"}],
  "resumo_ferramentas": [{"codigo": "...", "descricao": "...", "quantidade": 0, "unidade": "H"}],
  "resumo_equipamentos": [],
  "observacoes": []
}
```

## Fluxo de Trabalho

1. **Receber** escopo.json do hvac-extrator
2. **Salvar** escopo.json no diretorio output/YYYY-MM/
3. **Executar** script Python:
   ```bash
   python -m hvac.compositor -i output/2026-01/escopo.json -o output/2026-01/composicao.json
   ```
4. **Ler** composicao.json gerado
5. **Retornar** resultado para skill mestre

## Calculo de Quantidades (feito pelo script)

Para cada item da composicao:
```
quantidade_final = qtd_base + (qtd_var × variavel)
```

## Bases de Dados Usadas

O script le automaticamente de `bases/`:
- `composicoes.json` - composicoes de servico (com qtd_base e qtd_var)
- `materiais.json` - catalogo de materiais
- `mao_de_obra.json` - tipos de mao de obra
- `ferramentas.json` - catalogo de ferramentas
- `equipamentos.json` - catalogo de equipamentos

## Exemplo de Uso

```bash
# Criar diretorio de output
mkdir -p output/2026-01

# Salvar escopo
# (agente escreve escopo.json)

# Executar compositor
python -m hvac.compositor \
  --input output/2026-01/escopo.json \
  --output output/2026-01/composicao.json

# Ler resultado
# (agente le composicao.json)
```

## Observacoes

- O script consolida automaticamente itens repetidos
- Gera descricoes usando `descricao_variavel` quando disponivel
- Registra observacoes para composicoes nao encontradas

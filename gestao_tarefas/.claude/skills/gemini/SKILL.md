---
name: gemini
description: Pesquisar informações de demandas no Gmail via Gemini CLI
user-invocable: true
argument-hint: <demanda_id | "lote">
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Skill: Pesquisa Gmail via Gemini CLI

Pesquisa informações de demandas de orçamentos no Gmail (orcamentos2@armant.com.br)
usando o Gemini CLI como intermediário para acessar a Gmail API.

## Quando usar

- Usuário chama `/gemini 26_XXX` para pesquisar uma demanda específica
- Usuário chama `/gemini lote` para processar demandas pendentes em lote

## Fluxo de execução

### Modo individual: `/gemini <ID>`

1. **Identificar a demanda** pelo ID (ex: `26_047`)
2. **Buscar contexto** da demanda na fila de pesquisa (`data/gmail/fila_pesquisa.json`)
3. **Executar o script** de pesquisa:

```bash
bash scripts/ops/gemini_pesquisa.sh <ID>
```

4. **Ler o resultado** em `data/gmail/gemini_results/<ID>.json`
5. **Reportar** ao usuário os dados encontrados (ou ausência)

### Modo lote: `/gemini lote`

1. **Ler** `data/gmail/fila_pesquisa.json`
2. **Filtrar** demandas com status `sem_resultado` ou `pendente`
3. **Executar** sequencialmente para cada demanda (máx 10 por lote):

```bash
for id in lista_ids; do
  bash scripts/ops/gemini_pesquisa.sh "$id"
  sleep 5
done
```

4. **Gerar relatório** consolidado com resultados

## Interpretação dos resultados

O script retorna código de saída:
- `0` = sucesso, dados encontrados e salvos no JSON
- `1` = sem resultado relevante encontrado
- `2` = erro na execução (Gemini indisponível, timeout, etc.)

O JSON de resultado segue o formato:

```json
{
  "demanda_id": "26_047",
  "timestamp": "2026-02-12T...",
  "status": "encontrado|nao_encontrado|erro",
  "dados": {
    "cliente": "Razão Social",
    "cnpj": "XX.XXX.XXX/XXXX-XX",
    "contato_nome": "Nome",
    "contato_telefone": "(XX) XXXXX-XXXX",
    "contato_email": "email@empresa.com",
    "endereco": "Endereço completo",
    "tipo_servico": "instalacao|manutencao|projeto",
    "detalhes": "Descrição do escopo",
    "prazo": "Informação de prazo",
    "porte": "pequeno|medio|grande",
    "origem_dados": "gmail|google|ambos"
  },
  "emails_encontrados": 0,
  "fontes": ["descrição das fontes"]
}
```

## Após resultados

- Informar ao usuário os dados extraídos em formato legível
- Sugerir atualização no Asana se dados relevantes foram encontrados
- Se modo lote, apresentar tabela resumo com status de cada demanda

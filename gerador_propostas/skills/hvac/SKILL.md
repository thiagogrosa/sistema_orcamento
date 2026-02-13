---
name: hvac
description: Skill mestre para geracao de orcamentos HVAC. Use quando o usuario pedir orcamento de climatizacao, instalacao de ar-condicionado, split, ou mencionar /hvac.
model: claude-opus-4-5-20251101
---

# hvac - Skill Mestre de Orcamentacao

## Objetivo

Orquestrar geracao de orcamentos HVAC usando arquitetura hibrida: agente interpreta e scripts calculam.

## Uso

```
/hvac "texto descrevendo servico"
/hvac -f arquivo.pdf
```

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    AGENTE (Opus)                         │
│  - Interpreta entrada do usuario (NLP)                   │
│  - Questiona informacoes faltantes                       │
│  - Confirma ajustes necessarios                          │
│  - Apresenta resultado final                             │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼ JSON
┌─────────────────────────────────────────────────────────┐
│                 SCRIPTS PYTHON                           │
│  compositor.py: escopo.json → composicao.json            │
│  precificador.py: composicao.json → precificado.json     │
└─────────────────────────────────────────────────────────┘
```

## Fluxo Completo

### 1. Interpretar Entrada
- Analisar texto/PDF do usuario
- Identificar equipamentos, capacidades, metragens
- Gerar escopo estruturado

### 2. Confirmar Informacoes
- Apresentar confirmacoes_pendentes ao usuario
- Usar AskUserQuestion para coletar respostas
- Aplicar respostas ao escopo

### 3. Gerar Escopo Final
- Salvar em `output/YYYY-MM/ORC-CLIENTE-DATA/escopo.json`

### 4. Executar Compositor (Script Python)
```bash
python -m hvac.compositor \
  --input output/YYYY-MM/ORC-CLIENTE-DATA/escopo.json \
  --output output/YYYY-MM/ORC-CLIENTE-DATA/composicao.json
```

### 5. Executar Precificador (Script Python)
```bash
python -m hvac.precificador \
  --input output/YYYY-MM/ORC-CLIENTE-DATA/composicao.json \
  --output output/YYYY-MM/ORC-CLIENTE-DATA/precificado.json
```

### 6. Apresentar Resultado
- Ler precificado.json
- Mostrar resumo financeiro formatado
- Listar alertas se houver
- Oferecer opcoes (PDF, Excel, enviar)

## Bases de Dados

```
bases/
├── composicoes.json    # Composicoes com qtd_base e qtd_var
├── materiais.json      # Precos de materiais
├── mao_de_obra.json    # Custo/hora por categoria
├── ferramentas.json    # Custo/hora de ferramentas
├── equipamentos.json   # Specs e precos de equipamentos
└── bdi.json            # BDI por tipo de insumo (MAT, MO, FER, EQP)
```

## Diretorio de Output

```
output/
└── YYYY-MM/
    └── ORC-CLIENTE-YYYYMMDD/
        ├── escopo.json
        ├── composicao.json
        ├── precificado.json
        └── proposta.pdf (opcional)
```

## Comportamento Adaptativo

- **Caso simples:** executar tudo automaticamente
- **Caso com alertas:** pausar e confirmar (precos desatualizados, etc.)
- **Caso ambiguo:** perguntar antes de prosseguir

## Exemplo de Interacao

**Usuario:** "Orcamento para instalar 2 splits 24k com 8m de linha cada"

**Agente:**
1. Identifica: 2x Split 24K, 8m linha cada
2. Pergunta: Dreno PVC ou cristal? Precisa ponto eletrico?
3. Salva escopo.json com respostas
4. Executa: `python -m hvac.compositor ...`
5. Executa: `python -m hvac.precificador ...`
6. Apresenta:

```
## Orcamento - 2x Split 24K

| Item | Descricao | Valor |
|------|-----------|-------|
| 1 | Instalacao Split 24K (8m linha) | R$ 1.850,00 |
| 2 | Instalacao Split 24K (8m linha) | R$ 1.850,00 |

**TOTAL: R$ 3.700,00**

Validade: 15 dias
Alertas: Nenhum

[Gerar PDF] [Gerar Excel] [Enviar por email]
```

## Skills Relacionadas

- `hvac-extrator`: Extrai escopo de textos/PDFs (quando necessario NLP complexo)
- `hvac-compositor`: Wrapper do script compositor.py
- `hvac-precificador`: Wrapper do script precificador.py
- `hvac-output`: Gera documentos finais (PDF, Excel)
- `hvac-cotacoes`: Gerencia cotacoes de fornecedores

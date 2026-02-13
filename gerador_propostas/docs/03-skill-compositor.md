# Skill Compositora: hvac-compositor

> **Modelo recomendado:** HAIKU (padrao) | SONNET (complexo)
> **Responsabilidade:** Montar lista de materiais e mao de obra

---

## Objetivo

Transformar o escopo estruturado em lista detalhada de materiais, mao de obra e servicos com quantitativos corretos.

---

## Processo

### 1. Carregar Bases

```
Ler: bases/composicoes-split.json
Ler: bases/composicoes-manutencao.json (se aplicavel)
```

### 2. Mapear Itens para Composicoes

| Servico | Capacidade | Composicao |
|---------|------------|------------|
| instalacao-completa | 9K | INST-SPLIT-9K |
| instalacao-completa | 12K | INST-SPLIT-12K |
| instalacao-completa | 18K | INST-SPLIT-18K |
| instalacao-completa | 24K | INST-SPLIT-24K |
| manutencao-preventiva | qualquer | MANUT-PREV-SPLIT |
| manutencao-corretiva | qualquer | MANUT-CORR-SPLIT-CARGA |
| desinstalacao | qualquer | DESINSTALACAO-SPLIT |

### 3. Aplicar Ajustes

#### Distancia de Tubulacao

```
SE distancia_media > 5m
   metros_extras = distancia_media - 5
   PARA CADA item de instalacao:
      adicionar: metros_extras x ADICIONAL-METRO-TUBULACAO
```

#### Altura de Trabalho

```
SE altura_trabalho > 3m OU necessita_andaime
   PARA CADA item de instalacao:
      adicionar: 1 x ADICIONAL-ALTURA
```

#### Infraestrutura Eletrica

```
SE necessita_infra_eletrica
   PARA CADA equipamento:
      adicionar: 1 x INFRA-ELETRICA-SPLIT
```

### 4. Substituir Materiais Variaveis

Para itens com codigo "VAR" (variavel):

| Capacidade | Linha Liquida | Linha Gas |
|------------|---------------|-----------|
| 9K-12K | TUB-CU-1/4 | TUB-CU-3/8 |
| 18K | TUB-CU-1/4 | TUB-CU-1/2 |
| 24K | TUB-CU-3/8 | TUB-CU-5/8 |

### 5. Multiplicar por Quantidade

```
SE quantidade > 1:
   materiais = composicao.materiais x quantidade
   mao_obra = composicao.mao_obra x quantidade

   SE quantidade > 3:
      mao_obra = mao_obra x 0.9  # economia de escala 10%
```

### 6. Consolidar Materiais

Agrupar materiais iguais de todos os itens:

```
PARA CADA material em todos os itens:
   SE material.codigo ja existe em resumo:
      resumo[codigo].quantidade += material.quantidade
   SENAO:
      adicionar material ao resumo
```

---

## Output

### Formato: composicao.json

```json
{
  "projeto": "Nome do projeto",
  "data_composicao": "2026-01-02",
  "itens_orcamento": [
    {
      "id": 1,
      "descricao": "Instalacao split 12K - Recepcao",
      "composicao_base": "INST-SPLIT-12K",
      "quantidade": 1,
      "unidade": "un",
      "materiais": [
        {"codigo": "TUB-CU-1/4", "descricao": "Tubo cobre 1/4\"", "quantidade": 4, "unidade": "m"}
      ],
      "mao_de_obra": [
        {"categoria": "TECNICO-HVAC", "horas": 3}
      ]
    }
  ],
  "resumo_materiais": [
    {"codigo": "TUB-CU-1/4", "quantidade_total": 12, "unidade": "m"}
  ],
  "resumo_mao_obra": [
    {"categoria": "TECNICO-HVAC", "horas_totais": 9}
  ],
  "observacoes_composicao": [
    "Adicionados 3m extras de tubulacao"
  ]
}
```

---

## Tratamento de Casos Especiais

### Composicao Nao Encontrada

```
SE composicao nao existe na base:
   1. Buscar composicao mais proxima
   2. Registrar nos alertas
   3. Sugerir criacao de nova composicao
```

### Servico Customizado

Para servicos fora do padrao:
- Criar composicao estimada baseada em similares
- Marcar como "ESTIMATIVA - REVISAR"

---

*Especificacao da Skill Compositora - Sistema HVAC*

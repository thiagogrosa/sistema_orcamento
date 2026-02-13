# Skill Extratora: hvac-extrator

> **Modelo recomendado:** HAIKU (textos) | SONNET (PDFs) | OPUS (editais)
> **Responsabilidade:** Extrair escopo estruturado de documentos

---

## Objetivo

Interpretar documentos de entrada (textos, PDFs, editais) e gerar um JSON estruturado com todos os elementos necessarios para orcamentacao.

---

## Tipos de Entrada

| Tipo | Caracteristicas | Modelo |
|------|-----------------|--------|
| Texto simples | WhatsApp, e-mail, descricao curta | HAIKU |
| Relatorio PDF | Visita tecnica, fotos, medicoes | SONNET |
| Edital | Licitacao, especificacoes detalhadas | OPUS |
| Memorial | Projeto tecnico, calculos | SONNET |

---

## Processo de Extracao

### 1. Identificar Tipo de Documento

```
SE contem "pregao" ou "edital" ou "licitacao"
   → Tipo: edital
   → Modo: detalhado

SE contem medicoes ou referencias tecnicas especificas
   → Tipo: relatorio
   → Modo: tecnico

SENAO
   → Tipo: texto
   → Modo: rapido
```

### 2. Extrair Informacoes do Projeto

Buscar:
- Nome/identificador do projeto
- Nome do cliente
- Tipo de cliente (PJ, PF, Governo)
- Endereco
- Contato
- Data de visita
- Prazo de execucao

### 3. Extrair Itens de Servico

Para cada ambiente/equipamento identificado:
- Nome do ambiente
- Area em m2 (se informada)
- Carga termica (se informada ou calcular)
- Tipo de equipamento
- Capacidade em BTU
- Servico requerido
- Quantidade
- Observacoes especificas

### 4. Extrair Condicoes Gerais

- Distancia de tubulacao
- Necessidade de infra eletrica
- Altura de trabalho
- Acesso dificil
- Necessidade de andaime
- Horario especial

### 5. Gerar Alertas

Situacoes que requerem atencao:
- Informacao critica faltante
- Ambiguidade na especificacao
- Valores fora do padrao
- Servico nao coberto pela base

---

## Regras de Inferencia

### Calculo de Carga Termica

Quando nao especificada:

| Tipo Ambiente | BTU/m2 |
|---------------|--------|
| Residencial | 600 |
| Escritorio | 700 |
| Loja comercial | 800 |
| CPD/TI | 1000 |
| Cozinha industrial | 900 |

Ajustes:
- Muita incidencia solar: +20%
- Muitos equipamentos: +20%
- Pe direito alto (>3m): +15%

### Mapeamento de Capacidades

| BTU Calculado | Equipamento |
|---------------|-------------|
| Ate 10.000 | 9.000 BTU |
| 10.001-14.000 | 12.000 BTU |
| 14.001-20.000 | 18.000 BTU |
| 20.001-28.000 | 24.000 BTU |
| 28.001-36.000 | 30.000 BTU |
| >36.000 | Multi-split ou VRV |

### Identificacao de Tipo de Equipamento

- Residencial pequeno → split hi-wall
- Comercial pequeno → split hi-wall ou piso-teto
- Ambiente >50m2 ou pe direito >3m → cassete ou piso-teto
- Multiplos ambientes proximos → avaliar multi-split

### Servicos Adicionais

Identificar automaticamente:
- Distancia >5m → adicional tubulacao
- Altura >3m → adicional altura
- "Sem ponto eletrico" → infra eletrica
- "Remover equipamento" → desinstalacao

---

## Output

### Formato: escopo.json

Ver especificacao completa em [[interfaces/contratos#3-extrator-compositor]]

### Exemplo de Output

```json
{
  "projeto": {
    "nome": "Instalacao - Escritorio Contabil",
    "cliente": "Contabilidade Silva",
    "tipo_cliente": "PRIVADO-PJ"
  },
  "itens": [
    {
      "id": 1,
      "ambiente": "Recepcao",
      "area_m2": 20,
      "carga_termica_btu": 14000,
      "tipo_equipamento": "split-hi-wall",
      "capacidade_btu": 18000,
      "servico": "instalacao-completa",
      "quantidade": 1,
      "observacoes": "Carga calculada: 20m2 x 700 BTU/m2 = 14.000 BTU"
    }
  ],
  "condicoes_gerais": {
    "distancia_media_tubulacao_m": 5,
    "necessita_infra_eletrica": false,
    "altura_trabalho_m": 2.8
  },
  "alertas": []
}
```

---

## Tratamento de Ambiguidades

### Nivel 1: Inferivel

Quando a informacao pode ser inferida com seguranca:
- Fazer a inferencia
- Registrar nas observacoes do item

### Nivel 2: Provavel

Quando ha uma opcao mais provavel:
- Usar a opcao mais comum
- Registrar alternativa nos alertas

### Nivel 3: Critico

Quando nao e possivel inferir:
- Incluir nos alertas com prioridade alta
- Skill mestre deve pausar e perguntar

---

## Extracao de Editais

Atencao especial para:
- Numero do pregao/edital
- Objeto da licitacao
- Planilha de quantitativos
- Especificacoes tecnicas obrigatorias
- Exigencias de PMOC, ART
- Criterios de julgamento

---

*Especificacao da Skill Extratora - Sistema HVAC*

# Skill Mestre: hvac

> **Modelo recomendado:** OPUS
> **Responsabilidade:** Orquestrar o fluxo de orcamentacao

---

## Objetivo

Skill principal que recebe a solicitacao do usuario, analisa a entrada, decide o caminho a seguir e orquestra subagentes para executar cada etapa.

---

## Quando Usar

Chamada via `/hvac` seguido da solicitacao:

```bash
/hvac "instalar 2 splits 12000 BTU no escritorio"
/hvac -f relatorio-visita.pdf
/hvac "analisar edital" -f pregao-123.pdf
```

---

## Comportamento

### 1. Analisar Entrada

Detectar tipo de entrada:
- **Texto simples:** Descricao direta do servico
- **Arquivo PDF:** Relatorio de visita ou edital
- **Edital:** Documento de licitacao (requer analise mais profunda)

### 2. Decidir Caminho

```
SE texto simples E servico padrao (split)
   → Usar HAIKU para extracao rapida

SE PDF simples (relatorio de visita)
   → Usar SONNET para extracao

SE edital ou documento complexo
   → Usar OPUS para extracao detalhada

SE ambiguidade detectada
   → Perguntar ao usuario antes de continuar
```

### 3. Orquestrar Subagentes

Sequencia padrao:

```
1. Spawnar subagente EXTRATOR
   └─ Receber escopo.json

2. Validar escopo
   └─ Se alertas criticos → perguntar usuario

3. Spawnar subagente COMPOSITOR
   └─ Receber composicao.json

4. Spawnar subagente PRECIFICADOR
   └─ Receber precificado.json

5. Spawnar subagente OUTPUT
   └─ Gerar arquivos finais

6. Apresentar resultado ao usuario
```

### 4. Modo Interativo Adaptativo

- **Caso simples:** Executar tudo automaticamente
- **Caso com alertas:** Pausar e confirmar com usuario
- **Caso ambiguo:** Perguntar antes de cada etapa

---

## Spawning de Subagentes

### Modelo de Chamada

```
Task tool:
  subagent_type: "general-purpose"
  model: "haiku" | "sonnet" | "opus"
  prompt: |
    Voce e um agente especializado em [funcao].

    Leia a skill em: ~/.claude/skills/hvac-[skill]/SKILL.md

    Execute a tarefa com a seguinte entrada:
    [dados da etapa anterior]

    Retorne o resultado no formato JSON especificado na skill.
```

### Exemplo de Spawn

```javascript
// Spawnar extrator com haiku para texto simples
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `
    Leia a skill: /path/to/.claude/skills/hvac-extrator/SKILL.md

    Extraia o escopo da seguinte solicitacao:
    "${entrada_usuario}"

    Retorne escopo.json conforme especificado.
  `
})
```

---

## Decisao de Modelo por Contexto

| Situacao | Extrator | Compositor | Precificador | Output |
|----------|----------|------------|--------------|--------|
| Texto simples, split | haiku | haiku | haiku | sonnet |
| PDF relatorio | sonnet | haiku | haiku | sonnet |
| Edital licitacao | opus | sonnet | sonnet | sonnet |
| Multiplos servicos | sonnet | sonnet | sonnet | sonnet |

---

## Fluxo de Erros

### Erro em Subagente

```
SE subagente retorna erro
   → Analisar tipo de erro
   → SE recuperavel: tentar novamente com mais contexto
   → SE critico: informar usuario e pausar
```

### Dados Faltantes

```
SE dados obrigatorios faltando
   → Perguntar ao usuario
   → Aguardar resposta
   → Continuar fluxo
```

---

## Integracao com Asana

Quando orcamento for aprovado:

```
1. Usuario confirma aprovacao
2. Skill mestre chama skill de integracao Asana
3. Skill Asana usa Gemini CLI para acessar MCP
4. Tarefas criadas no projeto existente
```

---

## Outputs Finais

Apos conclusao, apresentar ao usuario:

```markdown
## Orcamento Gerado

**Cliente:** [nome]
**Valor Total:** R$ [valor]
**Validade:** [dias] dias

### Arquivos Gerados
- [PDF] proposta-comercial.pdf
- [XLSX] orcamento-detalhado.xlsx

### Alertas
- [lista de alertas se houver]

### Acoes Disponiveis
1. Abrir PDF
2. Enviar por e-mail
3. Criar tarefas no Asana
4. Gerar cotacao de materiais
```

---

## Metricas e Logs

Registrar para cada orcamento:
- Tempo total de processamento
- Modelo usado em cada etapa
- Tokens consumidos por subagente
- Erros e retentativas

---

## Arquivo SKILL.md

O arquivo `.claude/skills/hvac/SKILL.md` deve conter versao compacta destas instrucoes, otimizada para contexto minimo.

---

*Especificacao da Skill Mestre - Sistema HVAC*

# Comparacao de Abordagens - Gestao de Orcamentos

## Abordagem 1: Secoes (Kanban - Estilo Trello)

### Estrutura
- **9 secoes/colunas** representando etapas do fluxo
- **Tarefas** movem entre secoes conforme progridem
- Visualizacao: Board (Kanban) ou Lista

### Como Funciona
```
Entrada → Em Triagem → Fila → Elaboracao → Revisao → Enviado → Negociacao → Fechado/Perdido
  [Tarefa]     →          →        →          →         →           →
```

### Vantagens
✓ Visualizacao clara do pipeline
✓ Facil ver quantos orcamentos em cada etapa
✓ Bom para gestao de fluxo (quantos na fila, quantos em elaboracao)
✓ Familiar para quem vem do Trello
✓ Board visual tipo Kanban

### Desvantagens
✗ Perda de contexto ao mover entre secoes
✗ Historico de movimentacoes nao e tao claro
✗ Dificil rastrear quanto tempo em cada etapa
✗ Nao mostra "progresso parcial" de uma tarefa
✗ Responsavel pela tarefa pode ser apenas 1 pessoa

---

## Abordagem 2: Subtarefas (Recomendada)

### Estrutura
- **1 projeto simples** (pode ter 1 ou 2 secoes: "Em Andamento" e "Concluido")
- **Cada orcamento = 1 tarefa principal**
- **Etapas = subtarefas** dentro da tarefa principal
- Progresso automatico baseado em subtarefas concluidas

### Como Funciona
```
Orcamento: [INSTALACAO] Empresa ABC - BH
├── [ ] 1. Triagem
├── [ ] 2. Aprovacao para Elaboracao
├── [ ] 3. Elaboracao do Orcamento
├── [ ] 4. Revisao Interna
├── [ ] 5. Envio ao Cliente
├── [ ] 6. Negociacao (se necessario)
└── [ ] 7. Fechamento
```

### Vantagens
✓ **Historico automatico**: cada subtarefa registra quem completou e quando
✓ **Progresso visual**: barra de progresso mostra % de conclusao
✓ **Responsaveis por etapa**: cada subtarefa pode ter responsavel diferente
✓ **Rastreabilidade**: facil ver quanto tempo levou cada etapa
✓ **Menos movimentacao manual**: nao precisa mover entre secoes
✓ **Contexto preservado**: toda informacao fica na tarefa principal
✓ **Comentarios por etapa**: cada subtarefa pode ter discussoes proprias
✓ **Metricas faceis**: tempo entre conclusao de subtarefas
✓ **Checklists adicionais**: pode ter checklist dentro de cada subtarefa

### Desvantagens
✗ Menos visual em formato Board/Kanban
✗ Precisa abrir tarefa para ver em qual etapa esta
✗ Nao mostra "fila" de forma tao visual

---

## Comparacao Pratica

### Cenario: Orcamento Empresa ABC

#### Abordagem 1 (Secoes)
1. Crio tarefa "[INSTALACAO] Empresa ABC - BH" em "Entrada"
2. Coordenador move para "Em Triagem"
3. Apos triagem, move para "Fila de Trabalho"
4. Atribuo para Joao, move para "Em Elaboracao"
5. Joao termina, move para "Revisao"
6. Coordenador aprova, move para "Enviado"
7. Cliente pede ajuste, move para "Negociacao"
8. Cliente aprova, move para "Fechado"

**Historico:** 8 movimentacoes, dificil ver quem fez o que e quando

#### Abordagem 2 (Subtarefas)
1. Crio tarefa "[INSTALACAO] Empresa ABC - BH" em "Em Andamento"
2. Adiciono 7 subtarefas das etapas (pode ser template)
3. Coordenador completa: "1. Triagem" → registro automatico
4. Coordenador completa: "2. Aprovacao" e atribui subtarefa 3 para Joao
5. Joao completa: "3. Elaboracao" → registro automatico
6. Coordenador completa: "4. Revisao Interna"
7. Joao completa: "5. Envio ao Cliente"
8. Cliente pede ajuste → add comentario na subtarefa 6
9. Joao completa: "6. Negociacao"
10. Coordenador completa: "7. Fechamento"
11. Tarefa move para "Concluido"

**Historico:** Cada etapa tem data, hora e responsavel registrado automaticamente

---

## Estrutura Proposta (Abordagem 2)

### Projeto: "Orcamentos - Climatizacao"

**Secoes (simplificadas):**
1. **Em Andamento** - Orcamentos em processo
2. **Concluido** - Orcamentos fechados ou perdidos

### Tarefa Principal (Orcamento)

**Titulo:** `[TIPO] Cliente - Local`
**Exemplo:** `[INSTALACAO] Empresa ABC - Belo Horizonte`

**Campos na Descricao:**
```
DADOS DO ORCAMENTO

Cliente: Empresa ABC
Contato: Joao Silva
Telefone: (31) 99999-8888
Email: joao@empresaabc.com.br
Local: Belo Horizonte - MG
Prazo do cliente: 2025-02-15

---

DETALHES DA DEMANDA
Instalacao de split 18.000 BTUs em sala de reunioes

---

ORIGEM: Comercial
LICITACAO: Nao

---

CLASSIFICACAO
Tipo: Instalacao
Porte: Medio
```

**Tags:** `instalacao`, `medio`

**Prazo:** Data limite do cliente

---

### Subtarefas (Etapas do Processo)

#### Template de Subtarefas

1. **📋 Triagem**
   - Responsavel: Coordenador
   - Descricao: Avaliar viabilidade, prioridade e atribuir responsavel

2. **✅ Aprovacao para Elaboracao**
   - Responsavel: Coordenador
   - Descricao: Confirmar que tem todas informacoes necessarias

3. **⚙️ Elaboracao do Orcamento**
   - Responsavel: Atribuir ao elaborador
   - Descricao: Criar planilha, calcular custos, definir preco

4. **🔍 Revisao Interna**
   - Responsavel: Coordenador
   - Descricao: Revisar valores, margem, condicoes comerciais

5. **📤 Envio ao Cliente**
   - Responsavel: Elaborador ou Coordenador
   - Descricao: Enviar orcamento e confirmar recebimento

6. **🤝 Negociacao** (opcional)
   - Responsavel: Coordenador
   - Descricao: Tratar ajustes, descontos, mudancas de escopo
   - **Nota:** So completar se houver negociacao

7. **🏁 Fechamento**
   - Responsavel: Coordenador
   - Descricao: Registrar resultado (fechado/perdido), valor, motivo

---

### Checklist Dentro das Subtarefas

Exemplo na subtarefa **"3. Elaboracao do Orcamento"**:
```
[ ] Calcular materiais
[ ] Calcular mao de obra
[ ] Definir prazo de execucao
[ ] Criar planilha orcamentaria
[ ] Revisar calculos
[ ] Formatar documento
```

---

## Metricas com Abordagem 2

### Automaticas (via data de conclusao)
- Tempo de triagem: Data conclusao subtarefa 1 - Data criacao tarefa
- Tempo de elaboracao: Data conclusao subtarefa 3 - Data conclusao subtarefa 2
- Tempo total: Data conclusao subtarefa 7 - Data criacao tarefa
- Taxa de conversao: Tarefas com subtarefa 7 marcada "fechado" vs "perdido"

### Relatorios
- Orcamentos em cada etapa: contar quantas tarefas tem subtarefa X nao concluida
- Gargalos: qual subtarefa demora mais tempo
- Producao por pessoa: quantas subtarefas cada um completa

---

## Recomendacao

**Use Abordagem 2 (Subtarefas)** pelos seguintes motivos:

1. **Historico superior**: rastreabilidade completa
2. **Responsabilizacao clara**: quem fez cada etapa
3. **Metricas melhores**: tempo real de cada fase
4. **Menos trabalho manual**: nao precisa mover tarefas
5. **Escalavel**: facil adicionar mais etapas se necessario
6. **Templates**: pode criar template de tarefa com subtarefas pre-definidas

A Abordagem 1 (Secoes) e melhor apenas se voce precisa de:
- Visualizacao tipo Kanban para apresentacoes
- Gestao visual rapida de "fila" vs "em andamento"

**Sugestao:** Pode usar hibrido - 2-3 secoes principais + subtarefas dentro

---

## Estrutura Hibrida (Opcional)

Se quiser ter o melhor dos dois mundos:

**Secoes:**
1. **Novo** - Orcamentos ainda nao triados
2. **Em Andamento** - Orcamentos em processo (com subtarefas)
3. **Concluido** - Orcamentos finalizados

**Subtarefas:** Mesmas 7 etapas dentro de cada orcamento

Assim voce tem:
- Board visual simples (3 colunas)
- Rastreabilidade detalhada (subtarefas)

# Projeto Asana: Orcamentos - Climatizacao

## Contexto

**Setor:** Orcamentos de Climatizacao
**Equipe:** Coordenador + 1 funcionario (em breve +2)
**Volume:** 10-30 demandas/semana
**Plano Asana:** Gratuito

**Abordagem:** Subtarefas (cada orcamento = 1 tarefa com 7 subtarefas representando as etapas)

---

## Estrutura do Projeto

### Nome do Projeto
**"Orcamentos - Climatizacao"**

### Secoes (simplificadas)

| # | Secao | Descricao |
|---|-------|-----------|
| 1 | Em Andamento | Orcamentos em processo |
| 2 | Concluido | Orcamentos finalizados (fechados ou perdidos) |

**Por que simplificado?**
- O progresso e rastreado nas subtarefas, nao nas secoes
- Visualizacao mais limpa
- Menos movimentacao manual
- Historico automatico via subtarefas

---

## Estrutura de um Orcamento (Tarefa)

### Tarefa Principal

**Titulo:** `[TIPO] Cliente - Local`

**Tipos disponiveis:**
- `[INSTALACAO]` - Instalacao de AC
- `[MANUTENCAO]` - Manutencao preventiva/corretiva
- `[PROJETO]` - Projeto de climatizacao
- `[LIC][TIPO]` - Prefixo adicional para licitacoes

**Exemplos:**
- `[INSTALACAO] Empresa ABC - Belo Horizonte`
- `[LIC][INSTALACAO] Prefeitura - MG`
- `[MANUTENCAO] Condominio XYZ - SP`
- `[LIC][PROJETO] Governo Estadual - RJ`

---

### Template de Descricao

```
DADOS DO ORCAMENTO

Cliente: [Nome da empresa ou pessoa]
CNPJ/CPF: [Documento]
Contato: [Nome do contato]
Telefone: [(XX) XXXXX-XXXX]
Email: [email@cliente.com.br]
Endereco: [Rua, Numero - Bairro - Cidade/UF - CEP]
Local do Servico: [Se diferente]
Prazo do cliente: [DD/MM/AAAA]

---

DETALHES DA DEMANDA
[Descricao completa do que foi solicitado]

---

ORIGEM: [Comercial / Cliente direto / Diretoria / Engenharia]
LICITACAO: [Sim - Numero/Edital | Nao]

---

CLASSIFICACAO
Tipo: [Instalacao / Manutencao / Projeto]
Porte: [Pequeno / Medio / Grande]

---

OBSERVACOES
[Informacoes adicionais relevantes]
```

---

### 7 Subtarefas (Etapas do Processo)

Cada orcamento tem 7 subtarefas que representam as etapas:

| # | Subtarefa | Responsavel Tipico | Descricao |
|---|-----------|-------------------|-----------|
| 1 | 📋 Triagem | Coordenador | Avaliar viabilidade e prioridade |
| 2 | ✅ Aprovacao para Elaboracao | Coordenador | Confirmar liberacao |
| 3 | ⚙️ Elaboracao do Orcamento | Elaborador | Criar planilha e calcular |
| 4 | 🔍 Revisao Interna | Coordenador | Revisar valores e aprovar |
| 5 | 📤 Envio ao Cliente | Elaborador | Enviar e confirmar recebimento |
| 6 | 🤝 Negociacao | Coordenador/Elaborador | Tratar ajustes (se necessario) |
| 7 | 🏁 Fechamento | Coordenador | Registrar fechado ou perdido |

**Vantagens das Subtarefas:**
- ✅ Historico automatico (quem completou, quando)
- ✅ Progresso visual (barra de 0% a 100%)
- ✅ Responsavel diferente por etapa
- ✅ Metricas precisas de tempo por fase
- ✅ Contexto preservado (tudo na mesma tarefa)

---

## Tags

| Tag | Uso |
|-----|-----|
| `instalacao` | Tipo de servico |
| `manutencao` | Tipo de servico |
| `projeto` | Tipo de servico |
| `licitacao` | Origem via licitacao |
| `pequeno` | Porte |
| `medio` | Porte |
| `grande` | Porte |
| `urgente` | Prioridade alta |
| `cliente-estrategico` | Cliente importante |

---

## Como Criar um Novo Orcamento

### Metodo 1: Duplicar o Template (Recomendado)

1. Abra o projeto "Orcamentos - Climatizacao"
2. Encontre a tarefa: **"🔖 TEMPLATE - Como criar um orcamento"**
3. Clique com botao direito > "Duplicar tarefa"
4. Renomeie com: `[TIPO] Cliente - Local`
5. Preencha os campos da descricao
6. Adicione tags relevantes
7. Defina prazo (data limite do cliente)
8. Marque subtarefas conforme avanca

### Metodo 2: Criar Manualmente

1. Criar tarefa na secao "Em Andamento"
2. Titulo: `[TIPO] Cliente - Local`
3. Copiar template de descricao e preencher
4. Criar as 7 subtarefas manualmente (ou usar script)
5. Adicionar tags

### Metodo 3: Via IA (Automatizado)

1. Colar texto da demanda (email, anotacao)
2. IA extrai dados e gera JSON
3. IA cria tarefa com subtarefas via MCP Asana

---

## Fluxo de Trabalho

### Ciclo de Vida de um Orcamento

```
Criacao da Tarefa
       ↓
1. Triagem (coordenador avalia)
       ↓
2. Aprovacao (libera para elaborar)
       ↓
3. Elaboracao (elaborador cria orcamento)
       ↓
4. Revisao Interna (coordenador aprova)
       ↓
5. Envio ao Cliente (envia orcamento)
       ↓
6. Negociacao? (se cliente pedir ajustes)
       ↓
7. Fechamento (fechado ✅ ou perdido ❌)
       ↓
Mover para "Concluido"
```

### Progresso Visual

O Asana mostra automaticamente:
- **0/7** - Recebido, aguardando triagem
- **1/7** - Triado
- **2/7** - Aprovado para elaboracao
- **3/7** - Orcamento elaborado
- **4/7** - Revisado internamente
- **5/7** - Enviado ao cliente
- **6/7** - Negociado
- **7/7** - Concluido (fechado ou perdido)

---

## Responsabilidades

### Coordenador
- Fazer triagem de novas demandas
- Aprovar elaboracao
- Atribuir responsaveis
- Revisar orcamentos
- Aprovar fechamento
- Acompanhar metricas

### Elaborador (Junior/Pleno/Senior)
- Elaborar orcamento conforme atribuicao
- Enviar ao cliente
- Acompanhar negociacao
- Atualizar subtarefas conforme progresso

---

## Criterios de Priorizacao

1. **Prazo urgente** (< 3 dias)
2. **Cliente estrategico**
3. **Alto valor potencial**
4. **Licitacao com prazo**
5. **Ordem de chegada**

---

## Distribuicao por Complexidade

| Complexidade | Criterios | Responsavel |
|--------------|-----------|-------------|
| Simples | Pequeno porte, servico padrao | Novo funcionario |
| Media | Medio porte, especificidades | Funcionario experiente |
| Complexa | Grande porte, licitacao, cliente estrategico | Senior/Coordenador |

---

## Metricas

### Automaticas (via data de conclusao das subtarefas)

- **Tempo de triagem:** Conclusao subtarefa 1 - Data criacao
- **Tempo de elaboracao:** Conclusao subtarefa 3 - Conclusao subtarefa 2
- **Tempo de revisao:** Conclusao subtarefa 4 - Conclusao subtarefa 3
- **Tempo total:** Conclusao subtarefa 7 - Data criacao
- **Taxa de conversao:** Fechados / (Fechados + Perdidos)

### Relatorios

- Orcamentos por etapa: contar subtarefas nao concluidas
- Gargalos: qual subtarefa demora mais
- Producao por pessoa: subtarefas concluidas por responsavel
- Volume por periodo: tarefas criadas por semana/mes

---

## Guia de Uso - Equipe

### Como Trabalhar com as Subtarefas

1. **Ao receber atribuicao:**
   - Abra a tarefa
   - Leia a descricao completa
   - Leia a subtarefa atribuida a voce
   - Siga o checklist da subtarefa

2. **Durante o trabalho:**
   - Adicione comentarios na subtarefa conforme progride
   - Anexe arquivos relevantes
   - Mencione (@) colegas se precisar de algo

3. **Ao concluir:**
   - Marque a subtarefa como concluida
   - Asana registra automaticamente quem e quando
   - Proxima pessoa e notificada (se atribuida)

---

## Guia de Uso - Outros Setores

### Como Solicitar um Orcamento

**Opcao 1: Duplicar Template**
1. Acesse: https://app.asana.com/0/[PROJECT_ID]
2. Encontre tarefa "🔖 TEMPLATE"
3. Duplicar
4. Preencher campos
5. Adicionar tag do setor
6. Enviar (coordenador sera notificado)

**Opcao 2: Preencher Formulario**
[Se configurado futuramente]

**Informacoes Necessarias:**
- Consulte: `requisitos-solicitacao-orcamento.md`

---

## Integracao com IA (MCP Asana)

### Captura Automatica de Demandas

Fluxo automatizado:
1. Colar texto de email/anotacao
2. IA extrai dados estruturados (JSON)
3. IA cria tarefa no Asana via MCP
4. IA cria as 7 subtarefas
5. Tarefa pronta na secao "Em Andamento"

### Comandos Disponiveis

Ver: `agente-ai-instrucoes-asana.md`

---

## Arquivos Relacionados

| Arquivo | Descricao |
|---------|-----------|
| `COMPARACAO-ABORDAGENS.md` | Comparacao entre secoes vs subtarefas |
| `requisitos-solicitacao-orcamento.md` | Guia para outros setores |
| `agente-ai-instrucoes-asana.md` | Instrucoes para IA/MCP |
| `template-captura-orcamentos.md` | Templates de captura |
| `scripts/bootstrap/criar_template_guia.py` | Script para criar template no Asana |
| `scripts/legacy/criar_orcamento_exemplo_subtarefas.py` | Script de exemplo |

---

## Limitacoes do Plano Gratuito

- Campos personalizados: Limitado (usar tags e descricao)
- Timeline: Nao disponivel
- Automacoes: Nao disponivel
- Relatorios avancados: Nao disponivel (exportar CSV)
- Usuarios: Ate 10 (ok)
- **Templates nativos: Nao disponivel** (usar tarefa template para duplicar)

---

## Versao

**Versao:** 2.0 (Subtarefas)
**Data:** Janeiro/2025
**Anterior:** v1.0 (Secoes) - ver `orcamentos-climatizacao-asana-v1-secoes.md`

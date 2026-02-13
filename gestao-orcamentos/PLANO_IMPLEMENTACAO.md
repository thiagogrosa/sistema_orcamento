# Plano de Implementação - Sistema de Gestão de Orçamentos

**Data:** 30/01/2026
**Versão:** 1.0
**Status:** Em Implementação

---

## 📌 Contexto e Objetivos

### Situação Atual
- Sistema híbrido: Asana (plano gratuito) + Google Drive + Gmail
- Captura manual de demandas (copiar/colar emails)
- Uso intensivo de IA (Sonnet) para processar dados brutos
- Custo alto de tokens por operação
- Processos não documentados/padronizados

### Objetivos do Projeto
1. **Reduzir custos**: Minimizar uso de tokens substituindo IA por scripts onde possível
2. **Documentar processos**: Criar documentação clara de cada etapa
3. **Criar skills reutilizáveis**: Comandos padronizados para agentes mais baratos (Haiku)
4. **Preparar automação**: Estrutura pronta para execução automática futura
5. **Manter plano gratuito**: Todas soluções compatíveis com Asana Free

---

## 🏗️ Arquitetura Proposta

### Fluxo End-to-End Otimizado

```
┌─────────────────────────────────────────────────────────────┐
│ ENTRADA: Pasta no Google Drive                              │
│ Estrutura: AA_XXX_CLIENTE/                                  │
│   ├── emails_relacionados/ (opcional)                       │
│   ├── anotacoes.txt (opcional)                              │
│   └── anexos/ (opcional)                                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 1: COLETA DE DADOS (Gmail API - Python Script)        │
│ • Busca emails relacionados ao cliente/demanda              │
│ • Download de emails como .eml ou .txt                      │
│ • Extração de anexos (PDFs, imagens)                        │
│ • Salva na pasta da demanda                                 │
│                                                              │
│ Custo: 0 tokens (script puro)                               │
│ Tecnologia: Gmail API + Python                              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 2: PREPARAÇÃO (Script Python)                         │
│ • Remove HTML, assinaturas, threads duplicadas              │
│ • Extrai metadados óbvios (remetente, data, assunto)        │
│ • Detecta padrões conhecidos (CNPJ, telefone, email)        │
│ • Consolida tudo em arquivo .md estruturado                 │
│                                                              │
│ Custo: 0 tokens (regex + parsers)                           │
│ Output: dados_preparados.md (~500-1000 palavras)            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 3: EXTRAÇÃO INTELIGENTE (IA - Claude Haiku)           │
│ • Recebe texto limpo e estruturado                          │
│ • Extrai dados semânticos (cliente, tipo, escopo)           │
│ • Infere informações (porte, urgência)                      │
│ • Retorna JSON validado                                     │
│                                                              │
│ Custo: ~700 tokens por demanda                              │
│ Modelo: Haiku (fallback Sonnet se complexo)                 │
│ Output: orcamento.json                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 4: CRIAÇÃO NO ASANA (Script + MCP)                    │
│ • Cria tarefa principal no projeto                          │
│ • Cria 7 subtarefas (etapas do processo)                    │
│ • Adiciona tags apropriadas                                 │
│ • Define prazos e responsáveis                              │
│ • Anexa arquivos do Drive                                   │
│                                                              │
│ Custo: 0 tokens (API calls diretas)                         │
│ Tecnologia: MCP Asana Server                                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ SAÍDA: Tarefa criada no Asana + Relatório                   │
│ • Tarefa no projeto "Teste MCP" na seção "Entrada"          │
│ • Log detalhado do processamento                            │
│ • Mapeamento ID → task_gid salvo                            │
└─────────────────────────────────────────────────────────────┘
```

### Componentes do Sistema

| Componente | Tecnologia | Responsabilidade | Custo Tokens |
|------------|-----------|------------------|--------------|
| **Gmail Client** | Gmail API + Python | Buscar e baixar emails | 0 |
| **Data Preparer** | Python (regex, parsers) | Limpar e estruturar texto | 0 |
| **AI Extractor** | Claude Haiku/Sonnet | Extração semântica | ~700 |
| **Asana Library** | MCP Asana + Python | CRUD de tarefas | 0 |
| **Drive Sync** | Google Drive API | Sincronizar arquivos | 0 |
| **CLI Orchestrator** | Python Click | Interface de comandos | 0 |

---

## 💰 Análise de Custos

### Abordagem Atual (Tudo via IA Sonnet)

```
Processar email bruto com HTML:     ~2500 tokens input
Gerar prompt de criação:            ~1000 tokens input
Resposta da IA:                     ~500 tokens output
────────────────────────────────────────────────────
Total por demanda:                  ~4000 tokens
Custo com Sonnet ($3/$15 por M):    ~$0.024 por demanda

Volume: 30 demandas/semana
Custo semanal:  $0.72
Custo mensal:   $3.12
Custo anual:    $37.44
```

### Abordagem Proposta (Scripts + Haiku)

```
Script Gmail API:                   0 tokens
Script preparação:                  0 tokens
Haiku extração:                     ~700 tokens total
Script criação Asana:               0 tokens
────────────────────────────────────────────────────
Total por demanda:                  ~700 tokens
Custo com Haiku ($0.25/$1.25 por M): ~$0.0015 por demanda

Volume: 30 demandas/semana
Custo semanal:  $0.045
Custo mensal:   $0.195
Custo anual:    $2.34
```

### Comparação e Economia

| Métrica | Atual (Sonnet) | Proposto (Scripts + Haiku) | Economia |
|---------|----------------|---------------------------|----------|
| **Tokens/demanda** | ~4000 | ~700 | **82.5%** |
| **Custo/demanda** | $0.024 | $0.0015 | **93.75%** |
| **Custo anual** | $37.44 | $2.34 | **$35.10** |
| **Volume possível com $10** | ~416 demandas | ~6,666 demandas | **16x mais** |

**Benefício Principal:** Permite processar muito maior volume pelo mesmo custo

---

## 🎯 Benefícios da Nova Arquitetura

### 1. Redução Drástica de Custos
- 94% de economia em tokens
- Permite escalar volume sem aumentar custos proporcionalmente
- Viabiliza processamento automático contínuo

### 2. Documentação e Manutenibilidade
- Cada componente isolado e documentado
- Fácil entender o que cada script faz
- Pode ser auditado, testado e melhorado incrementalmente
- Novos desenvolvedores conseguem entender rapidamente

### 3. Skills Padronizadas e Reutilizáveis
- Comandos simples e consistentes
- Podem ser usados por diferentes agentes (Haiku, Sonnet, humanos)
- Documentação clara de quando usar cada comando
- Facilitam treinamento de novos membros da equipe

### 4. Uso Estratégico de IA
- **Scripts fazem:** Tarefas determinísticas (parsing, formatação, API calls)
- **IA Haiku faz:** Extração semântica de dados não-estruturados
- **IA Sonnet faz:** Apenas casos complexos/ambíguos (fallback automático)

### 5. Preparado para Automação
- Arquitetura modular permite execução manual ou automática
- Pode adicionar cron job sem refatorar código
- Watch folder para processamento em tempo real
- Notificações automáticas de processamento

### 6. Compatível com Plano Gratuito
- Todas soluções funcionam com Asana Free
- Usa APIs gratuitas (Gmail, Drive)
- Não depende de features pagas do Asana

---

## 📁 Estrutura de Arquivos Proposta

```
gestao-orcamentos/
│
├── README.md                       # Visão geral do projeto
├── CLAUDE.md                       # Contexto para IA (existente)
├── PLANO_IMPLEMENTACAO.md          # Este arquivo
├── ARQUITETURA.md                  # [TAREFA 1] Arquitetura técnica detalhada
├── GUIA_USUARIO.md                 # [TAREFA 9] Manual de uso
├── GUIA_DESENVOLVEDOR.md           # [TAREFA 9] Guia para contribuidores
├── TROUBLESHOOTING.md              # [TAREFA 9] Problemas e soluções
├── CUSTOS.md                       # [TAREFA 9] Análise de custos detalhada
│
├── src/                            # Código fonte Python
│   ├── __init__.py
│   ├── gmail_client.py             # [TAREFA 2] Cliente Gmail API
│   ├── prepare_data.py             # [TAREFA 3] Preparação de dados
│   ├── asana_lib.py                # [TAREFA 5] Biblioteca Asana
│   ├── sync_drive.py               # [TAREFA 8] Sincronização Drive
│   ├── cli.py                      # [TAREFA 6] Interface de linha de comando
│   └── utils.py                    # Utilitários compartilhados
│
├── prompts/                        # Templates de prompts para IA
│   ├── extracao_orcamento.txt      # [TAREFA 4] Prompt principal Haiku
│   ├── validacao_complexa.txt      # Prompt fallback Sonnet
│   └── complementacao_dados.txt    # Prompt para gaps de informação
│
├── skills/                         # Skills para Claude Code
│   └── skill_orcamentos.md         # [TAREFA 7] Skill padronizada
│
├── auto/                           # Automação futura
│   ├── scheduler.py                # [TAREFA 10] Agendador de tarefas
│   ├── watcher.py                  # Monitor de pasta (watch folder)
│   └── notifier.py                 # Sistema de notificações
│
├── config/                         # Configurações
│   ├── config.yaml                 # Configurações gerais
│   ├── ids_mapping.json            # Mapa Drive ID ↔ Asana task_gid
│   ├── gmail_credentials.json      # Credenciais Gmail (gitignored)
│   └── settings.local.json         # Settings locais (gitignored)
│
├── tests/                          # Testes e casos de exemplo
│   ├── casos_reais/                # Emails reais anonimizados
│   ├── test_gmail_client.py
│   ├── test_prepare_data.py
│   └── test_asana_lib.py
│
├── docs/                           # Documentação adicional
│   ├── fluxogramas/                # Diagramas de fluxo
│   ├── exemplos/                   # Screenshots e exemplos de uso
│   └── changelog.md                # Histórico de alterações
│
├── scripts/                        # Scripts auxiliares (existentes)
│   ├── criar-template-guia.py
│   ├── criar-orcamento-exemplo-subtarefas.py
│   └── setup-asana-project.py
│
├── lista/                          # Dados de demandas (existente)
│   ├── demandas-orcamentos.md
│   └── demandas-complementar-info.md
│
├── .env                            # Variáveis de ambiente (gitignored)
├── .gitignore
├── requirements.txt                # Dependências Python
└── pyproject.toml                  # Configuração do projeto Python
```

---

## 📋 Tarefas de Implementação

### Tarefa 1: Documentar arquitetura completa do sistema
**Arquivo:** `ARQUITETURA.md`

**Objetivo:** Criar documento técnico detalhado da arquitetura

**Conteúdo:**
- Visão geral da arquitetura
- Diagrama de componentes e fluxo de dados
- Decisões de design e trade-offs
- Especificação de cada componente
- Interfaces entre componentes
- Tratamento de erros e edge cases
- Estimativas de performance e custos
- Requisitos e dependências

**Output esperado:**
- Documento ARQUITETURA.md completo
- Diagramas em formato Mermaid ou ASCII
- Referências cruzadas com outros documentos

---

### Tarefa 2: Configurar Gmail API e autenticação OAuth
**Arquivo:** `src/gmail_client.py`

**Objetivo:** Setup completo da Gmail API com OAuth 2.0

**Passos:**
1. Criar projeto no Google Cloud Console
2. Habilitar Gmail API
3. Configurar tela de consentimento OAuth
4. Criar credenciais OAuth 2.0 (credentials.json)
5. Implementar fluxo de autenticação
6. Implementar refresh de tokens
7. Criar funções principais:
   - `buscar_emails(query, max_results)` - Busca emails por query
   - `baixar_email(email_id, format)` - Download de email específico
   - `salvar_anexos(email_id, output_dir)` - Extrai anexos
   - `get_thread(thread_id)` - Obtém thread completa

**Output esperado:**
- `src/gmail_client.py` funcional
- `docs/SETUP_GMAIL_API.md` com instruções de configuração
- Script de teste: `tests/test_gmail_client.py`

**Dependências:**
```
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

---

### Tarefa 3: Criar script de preparação de dados
**Arquivo:** `src/prepare_data.py`

**Objetivo:** Limpar e estruturar dados brutos em formato otimizado para IA

**Funcionalidades:**
1. **Limpeza de emails:**
   - Remover HTML e manter apenas texto
   - Remover assinaturas de email (detectar padrões comuns)
   - Remover threads antigas (manter só mensagem principal)
   - Remover disclaimers legais

2. **Extração de metadados:**
   - Remetente, destinatário, data, assunto
   - Detectar CNPJ/CPF (regex)
   - Detectar telefones (regex)
   - Detectar emails (regex)
   - Detectar CEP e endereços

3. **Consolidação:**
   - Gerar arquivo .md estruturado
   - Seções claras: Metadados, Conteúdo, Anexos
   - Formato consistente para IA processar

**Output esperado:**
- `src/prepare_data.py` com funções reutilizáveis
- Template `templates/dados_preparados.md`
- Testes com casos reais anonimizados

**Formato de saída (exemplo):**
```markdown
# Dados Preparados - Demanda

## Metadados Detectados
- **Remetente:** João Silva <joao@empresa.com>
- **Data:** 2026-01-25
- **Assunto:** Orçamento climatização sala
- **CNPJ:** 12.345.678/0001-90 (detectado)
- **Telefone:** (11) 98765-4321 (detectado)

## Conteúdo Principal
[texto limpo e relevante]

## Anexos Encontrados
- proposta_antiga.pdf (125 KB)
- planta_sala.jpg (450 KB)
```

---

### Tarefa 4: Criar prompt otimizado para extração com Haiku
**Arquivo:** `prompts/extracao_orcamento.txt`

**Objetivo:** Desenvolver prompt eficiente e testado para Haiku

**Requisitos do prompt:**
1. Conciso e direto (Haiku prefere prompts curtos)
2. Schema JSON claro e rigoroso
3. Regras de inferência bem definidas
4. Exemplos de entrada/saída (few-shot)
5. Tratamento de campos ausentes

**Estrutura do prompt:**
```
[SYSTEM]
Você é um extrator de dados de orçamentos de climatização.
Analise o texto e extraia informações estruturadas.

[SCHEMA JSON]
{
  "cliente": "string (obrigatório)",
  "cnpj_cpf": "string ou null",
  ...
}

[REGRAS]
- Se campo não encontrado, retorne null
- Infira tipo_servico baseado em palavras-chave
- Infira porte baseado em área ou quantidade
...

[EXEMPLOS]
Input: [exemplo 1]
Output: [json 1]
...

[TAREFA]
Analise o texto abaixo e extraia os dados:
{texto_preparado}
```

**Testes e validação:**
- Testar com 20 casos reais variados
- Comparar acurácia Haiku vs Sonnet
- Medir tokens consumidos
- Identificar casos que precisam Sonnet
- Documentar taxa de acerto por campo

**Output esperado:**
- `prompts/extracao_orcamento.txt` otimizado
- `prompts/extracao_orcamento_sonnet.txt` (fallback)
- Relatório de testes: `tests/relatorio_extracao.md`
- Métricas: tokens/demanda, acurácia, custo

---

### Tarefa 5: Criar biblioteca de funções para Asana
**Arquivo:** `src/asana_lib.py`

**Objetivo:** Centralizar todas operações do Asana em módulo reutilizável

**Funções principais:**

```python
# Criação
def criar_orcamento(json_data: dict) -> str:
    """Cria tarefa principal no Asana. Retorna task_id."""

def criar_subtarefas(task_id: str) -> list[str]:
    """Cria as 7 subtarefas padrão. Retorna lista de IDs."""

# Atualização
def atualizar_tarefa(task_id: str, campos: dict) -> bool:
    """Atualiza campos da tarefa."""

def avancar_etapa(task_id: str, etapa: int, observacao: str = None) -> bool:
    """Marca subtarefa N como concluída."""

# Fechamento
def registrar_fechamento(task_id: str, resultado: str, **kwargs) -> bool:
    """Registra fechamento (ganho/perdido) e move para Concluído."""

# Consulta
def buscar_tarefas(filtros: dict) -> list[dict]:
    """Busca tarefas com filtros."""

def obter_tarefa(task_id: str) -> dict:
    """Retorna detalhes completos da tarefa."""

# Anexos
def anexar_arquivo(task_id: str, file_path: str) -> bool:
    """Anexa arquivo à tarefa."""
```

**Características:**
- Usar MCP Asana internamente
- Logging detalhado de operações
- Tratamento robusto de erros
- Retry automático em caso de falha temporária
- Validação de inputs
- Type hints completos

**Output esperado:**
- `src/asana_lib.py` completo e documentado
- Testes unitários: `tests/test_asana_lib.py`
- Documentação de API: docstrings detalhadas

---

### Tarefa 6: Criar comando principal /processar-pasta
**Arquivo:** `src/cli.py`

**Objetivo:** Implementar interface de linha de comando que orquestra o pipeline

**Comandos principais:**

```bash
# Processar demanda completa
python cli.py processar-pasta 26_062

# Apenas buscar emails (sem criar tarefa)
python cli.py buscar-emails 26_062 --query "JBS Seara"

# Preparar dados (sem extração)
python cli.py preparar-dados 26_062

# Extrair dados (recebe .md preparado)
python cli.py extrair-dados 26_062/dados_preparados.md

# Criar tarefa (recebe JSON)
python cli.py criar-tarefa 26_062/orcamento.json

# Pipeline completo com confirmação
python cli.py processar-pasta 26_062 --confirm
```

**Pipeline do comando `processar-pasta`:**

```python
def processar_pasta(demanda_id: str, confirm: bool = False):
    """
    1. Validar que pasta existe no Drive
    2. Buscar emails relacionados (Gmail API)
    3. Preparar dados (limpeza)
    4. Extrair informações (IA Haiku)
    5. [SE confirm=True] Pedir confirmação do usuário
    6. Criar tarefa no Asana
    7. Anexar arquivos relevantes
    8. Gerar relatório de processamento
    9. Salvar mapeamento ID → task_gid
    """
```

**Features:**
- Progress bar para operações longas
- Logs coloridos e informativos
- Modo dry-run (simula sem executar)
- Modo verbose (debug)
- Salvamento de logs em arquivo
- Geração de relatório final

**Output esperado:**
- `src/cli.py` com Click framework
- Ajuda detalhada para cada comando
- Testes de integração: `tests/test_cli.py`

---

### Tarefa 7: Criar skill padronizada para Claude
**Arquivo:** `skills/skill_orcamentos.md`

**Objetivo:** Documentar skill reutilizável para diferentes agentes Claude

**Estrutura da skill:**

```markdown
# Skill: Gestão de Orçamentos

## Quando Usar
[Cenários em que esta skill é apropriada]

## Comandos Disponíveis
[Lista de comandos com exemplos]

## Fluxo de Trabalho Típico
[Passo-a-passo comum]

## Troubleshooting
[Problemas comuns e soluções]

## Exemplos de Uso
[Casos reais com input/output]

## Referências
[Links para scripts e docs]
```

**Conteúdo detalhado:**
- Instruções claras e concisas
- Exemplos práticos
- Quando usar cada comando
- Como interpretar outputs
- O que fazer em caso de erro
- Links para documentação técnica

**Testes:**
- Testar skill com agente Haiku
- Verificar se instruções são claras o suficiente
- Ajustar baseado em feedback de uso

**Output esperado:**
- `skills/skill_orcamentos.md` completa
- Testada com Haiku e Sonnet
- Exemplos de conversas com agente usando a skill

---

### Tarefa 8: Implementar sincronização Drive ↔ Asana
**Arquivo:** `src/sync_drive.py`

**Objetivo:** Manter Google Drive e Asana sincronizados automaticamente

**Funcionalidades:**

1. **Detectar novos PDFs:**
   - Monitorar pastas `03_Orcamento/` no Drive
   - Detectar arquivos `ORC_*.pdf`
   - Identificar tarefa correspondente (match por ID)
   - Anexar automaticamente no Asana

2. **Criar estrutura de pastas:**
   - Ao criar tarefa no Asana, criar pasta no Drive
   - Estrutura: `AA_XXX_CLIENTE/01_Projetos/02_Levantamento/...`
   - Salvar link da pasta no Asana

3. **Mapeamento de IDs:**
   - Manter arquivo `ids_mapping.json`
   - Formato: `{"26_004": {"task_gid": "...", "drive_folder_id": "..."}}`
   - Atualizar ao criar/mover tarefas

4. **Sincronização bidirecional:**
   - Drive → Asana: Anexar novos arquivos
   - Asana → Drive: Criar pastas para novas tarefas

**Comandos:**
```bash
# Sincronizar demanda específica
python cli.py sync-drive 26_004

# Sincronizar todas as demandas
python cli.py sync-drive --all

# Apenas detectar mudanças (não executar)
python cli.py sync-drive --check

# Criar estrutura de pastas para nova demanda
python cli.py criar-pasta-drive 26_062 "Cliente ABC"
```

**Output esperado:**
- `src/sync_drive.py` funcional
- `config/ids_mapping.json` atualizado automaticamente
- Logs de sincronização
- Testes: `tests/test_sync_drive.py`

---

### Tarefa 9: Criar documentação de uso e guias
**Arquivos:** `GUIA_USUARIO.md`, `GUIA_DESENVOLVEDOR.md`, `TROUBLESHOOTING.md`

**Objetivo:** Documentação completa para usuários finais e desenvolvedores

**GUIA_USUARIO.md:**
- Como instalar e configurar
- Como usar comandos básicos
- Fluxo de trabalho dia-a-dia
- Exemplos práticos com screenshots
- FAQ

**GUIA_DESENVOLVEDOR.md:**
- Arquitetura do código
- Como adicionar novos comandos
- Como modificar prompts de IA
- Como contribuir
- Padrões de código

**TROUBLESHOOTING.md:**
- Problemas comuns e soluções
- Erros de API e como resolver
- Logs e debugging
- Quando usar Sonnet vs Haiku
- Contatos de suporte

**CUSTOS.md:**
- Breakdown detalhado de custos por operação
- Comparativo de diferentes abordagens
- Como otimizar uso de tokens
- Projeções de custo por volume

**EXEMPLOS.md:**
- Casos reais de uso (anonimizados)
- Screenshots de cada etapa
- Outputs esperados
- Variações e edge cases

**Output esperado:**
- 5 arquivos markdown completos
- Diagramas e screenshots
- Links cruzados entre documentos
- Índice navegável

---

### Tarefa 10: Preparar para automação futura
**Arquivo:** `auto/scheduler.py`

**Objetivo:** Estruturar código para facilitar automação posterior

**Preparações:**

1. **Separar lógica de apresentação:**
   - CLI (cli.py) apenas interface
   - Lógica de negócio em módulos separados
   - Permite chamar funções sem CLI

2. **Modo batch:**
   - Processar múltiplas pastas de uma vez
   - Relatório consolidado
   - Continuar em caso de erro em uma pasta

3. **Sistema de notificações:**
   - Email quando processar demanda
   - Slack webhook (opcional)
   - Logs estruturados para auditoria

4. **Configuração via arquivo:**
   - `config/config.yaml` com todos parâmetros
   - Permite mudar comportamento sem alterar código
   - Diferentes perfis (dev, prod)

5. **Dry-run mode:**
   - Simular operações sem executar
   - Útil para testar antes de rodar automático
   - Gerar relatório do que seria feito

**Scheduler (para futuro):**
```python
# auto/scheduler.py
def main():
    """
    Executado via cron ou task scheduler.

    1. Verificar pastas novas no Drive
    2. Para cada pasta nova:
       - Processar automaticamente
       - Enviar notificação se sucesso
       - Log de erro se falha
    3. Gerar relatório diário
    """
```

**Watcher (para futuro):**
```python
# auto/watcher.py
def watch_folder(folder_path: str):
    """
    Monitora pasta do Drive em tempo real.
    Ao detectar arquivo novo, processa imediatamente.
    """
```

**Output esperado:**
- Código preparado mas não ativado
- `auto/scheduler.py` implementado
- `auto/watcher.py` implementado
- `docs/AUTOMACAO.md` com instruções de setup
- Exemplos de cron job e systemd service

---

## 🚀 Ordem de Implementação

### Fase 1: Fundação (Semana 1)
1. **Tarefa 1** - Documentar arquitetura completa
2. **Tarefa 2** - Setup Gmail API

### Fase 2: Pipeline de Dados (Semana 2)
3. **Tarefa 3** - Script de preparação de dados
4. **Tarefa 4** - Prompt otimizado Haiku

### Fase 3: Integração Asana (Semana 3)
5. **Tarefa 5** - Biblioteca Asana
6. **Tarefa 6** - CLI e orquestração

### Fase 4: Sincronização (Semana 4)
7. **Tarefa 8** - Sync Drive ↔ Asana
8. **Tarefa 7** - Skill padronizada

### Fase 5: Documentação e Futuro (Semana 5)
9. **Tarefa 9** - Documentação completa
10. **Tarefa 10** - Preparar automação

---

## ✅ Critérios de Sucesso

### Técnicos
- [ ] Redução de >90% no custo de tokens
- [ ] Pipeline completo funcional end-to-end
- [ ] Tempo de processamento <2 minutos por demanda
- [ ] Taxa de acerto >95% na extração de dados
- [ ] 100% das operações logadas e auditáveis

### Documentação
- [ ] Toda funcionalidade documentada
- [ ] Exemplos práticos de todos comandos
- [ ] Troubleshooting de problemas comuns
- [ ] Guias para usuários e desenvolvedores

### Usabilidade
- [ ] Comandos intuitivos e consistentes
- [ ] Mensagens de erro claras e acionáveis
- [ ] Confirmações em operações críticas
- [ ] Logs informativos e coloridos

### Manutenibilidade
- [ ] Código modular e testável
- [ ] Type hints em todas funções
- [ ] Testes unitários para componentes críticos
- [ ] Fácil adicionar novos comandos/features

---

## 📊 Métricas de Acompanhamento

### Durante Implementação
- Tarefas concluídas / Total
- Linhas de código escritas
- Cobertura de testes
- Documentação completa

### Pós-Implementação
- Tokens economizados por semana
- Tempo médio de processamento
- Taxa de erro por componente
- Satisfação dos usuários

---

## 🔄 Próximos Passos Após Conclusão

1. **Treinamento da equipe** - Onboarding nos novos comandos
2. **Período de testes** - 2 semanas usando em paralelo com processo manual
3. **Ajustes baseados em feedback** - Iterar com base no uso real
4. **Ativar automação** - Configurar cron para processamento automático
5. **Expansão** - Adicionar features avançadas (relatórios, dashboards)

---

## 📝 Notas e Considerações

### Limitações Conhecidas
- Plano gratuito do Asana limita algumas features (automações nativas)
- Gmail API tem quotas (verificar limites)
- Drive API tem limites de taxa (rate limiting)

### Dependências Externas
- Google Cloud (Gmail API, Drive API) - gratuito até certo volume
- Claude API (Haiku/Sonnet) - custo por uso
- Asana API - gratuito no plano atual

### Riscos e Mitigações
| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Mudanças na API do Gmail | Alto | Documentar versão, abstrair em wrapper |
| Custo inesperado de IA | Médio | Monitorar tokens, dry-run antes de escalar |
| Qualidade de extração baixa | Alto | Testes extensivos, fallback para Sonnet |
| Complexidade de manutenção | Médio | Documentação clara, código modular |

---

## 🤝 Contribuições e Feedback

Este é um projeto vivo e em evolução. Sugestões de melhorias são bem-vindas!

**Contato:** Coordenador do Setor de Orçamentos
**Última atualização:** 30/01/2026

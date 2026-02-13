# CLAUDE.md - Projeto Orcamentos Climatizacao

## Contexto do Projeto

Este projeto contem a documentacao e configuracoes para o sistema de gestao de orcamentos do Setor de Climatizacao, utilizando Asana como plataforma principal e integracao com IA via MCP.

**Responsavel:** Coordenador do Setor de Orcamentos
**Equipe:** 1 coordenador + 1 funcionario atual (em breve +2 novos)
**Ferramenta Principal:** Asana (plano gratuito)

---

## Arquivos do Projeto

| Arquivo | Descricao | Status |
|---------|-----------|--------|
| `orcamentos-climatizacao-asana.md` | Estrutura completa v2.0 (subtarefas) | Completo |
| `orcamentos-climatizacao-asana-v1-secoes.md` | Versao antiga (secoes) - referencia | Arquivo |
| `COMPARACAO-ABORDAGENS.md` | Comparacao secoes vs subtarefas | Completo |
| `agente-ai-instrucoes-asana.md` | Instrucoes para Agente AI usar MCP Asana | Precisa atualizar |
| `template-captura-orcamentos.md` | Templates para captura de demandas | Completo |
| `requisitos-solicitacao-orcamento.md` | Guia para outros setores solicitarem orcamentos | Completo |
| `criar-template-guia.py` | Script para criar tarefa template no Asana | Completo |
| `criar-orcamento-exemplo-subtarefas.py` | Script de exemplo com subtarefas | Completo |
| `lista/demandas-orcamentos.md` | Lista original de demandas pendentes | Completo |
| `lista/demandas-complementar-info.md` | Demandas com campos para preenchimento | Em uso |
| `pesquisa-gemini.md` | Prompt simplificado para Gemini (demandas urgentes) | Em uso |
| `configuracao-mcp-gmail.md` | Guia completo de configuracao MCP Gmail | Legado |
| `integracao-claude-gemini.md` | Documentacao da integracao Claude + Gemini CLI | Legado |
| `PLANO_SIMPLIFICACAO_GMAIL.md` | Plano de simplificacao Gmail (scripts Python) | Ativo |
| `gemini-tasks/` | Pasta com sistema estruturado de pesquisa Gmail | Ativo |
| `scripts/processar_demandas.py` | Processamento em lote de demandas via Gmail | Validado |
| `scripts/extrator_dados_email.py` | Extracao de dados de emails via regex | Validado |
| `scripts/atualizar_asana.py` | Preparador de plano de atualizacao (execucao via MCP) | Validado |
| `emails-extraidos/` | Emails baixados organizados por demanda | Em uso |
| `gemini-tasks/GEMINI.md` | Contexto e 50+ tarefas de pesquisa mapeadas | Em uso |
| `gemini-tasks/GEMINI-INSTRUCOES.md` | Instrucoes detalhadas para extracao | Em uso |
| `gemini-tasks/pesquisa-gmail-pendentes.md` | Lista completa de demandas pendentes | Em uso |
| `gemini-tasks/fila-pesquisa.json` | Sistema de fila e priorizacao | Em uso |
| `gemini-tasks/resultados-pesquisa-gmail.json` | Resultados estruturados das buscas | Em uso |

---

## Estrutura do Asana

### Workspace: armant.com.br
- **Workspace GID:** 1204197108826498

### Projetos Ativos

#### Projeto: "DEMANDAS DE ORCAMENTOS" (principal - em uso)
- **Project GID:** 1212920325558530
- **Secoes:**
  - Entrada (gid: 1212909431317491) - Demandas novas/sem proposta
  - Enviado (gid: 1212920431590044) - Propostas ja enviadas ao cliente
  - Em Negociacao - Propostas em negociacao
  - Fechado - Orcamentos ganhos
  - Perdido - Orcamentos perdidos
- **Total de demandas:** 69 tarefas (60 anteriores + 9 cadastradas em Fev/2026)
- **Sincronizacao:** Drive 2026 (67 pastas) <-> Asana (69 tarefas incluindo template e demandas 2025)

#### Projeto: "Comercial Privado" (referencia)
- **Project GID:** 1212016066751191
- **Status:** Todas as tarefas ativas foram migradas para o Teste MCP

### Padrao de Nomenclatura

**Padrao de Titulo:** `AA_XXX [TIPO] Cliente - Local`
- AA = ano (25 ou 26)
- XXX = numero sequencial
- Exemplo: `26_004 [PROJETO] JBS Seara - Nova Veneza/SC`

**Tipos:** INSTALACAO, MANUTENCAO, PROJETO, A_DEFINIR

**Tags:** instalacao, manutencao, projeto, licitacao, pequeno, medio, grande, urgente, cliente-estrategico

### Abordagem de Subtarefas (v2.0)

Cada orcamento = 1 tarefa principal + 7 subtarefas (etapas do processo)

**7 Subtarefas por Orcamento:**
1. Triagem
2. Aprovacao para Elaboracao
3. Elaboracao do Orcamento
4. Revisao Interna
5. Envio ao Cliente
6. Negociacao (se necessario)
7. Fechamento

**Vantagens da Abordagem:**
- Historico automatico (quem completou cada etapa e quando)
- Progresso visual (barra de 0-100%)
- Metricas precisas de tempo por fase
- Menos movimentacao manual

---

## Integracao com Google Drive

### Pasta de Orcamentos 2026
**Caminho (Mac):** `/Users/thiagorosa/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared drives/02Orcamentos/2026`
**Caminho (WSL):** `/mnt/g/Drives compartilhados/02Orcamentos/2026/`
**Montar Drive WSL:** `sudo mount -t drvfs G: /mnt/g`
**Importante:** Nome em pt-BR é "Drives compartilhados" (não "Shared drives")

**Estrutura de cada pasta:**
```
26_XXX_CLIENTE_SERVICO/
  01_Projetos/
  02_Levantamento/
  03_Orcamento/      <- PDFs de propostas (ORC_26_XXX_*.pdf)
  04_Cotacoes/
```

**IDs em uso no Drive:** 26_001 a 26_066 (67 pastas incluindo 26_000 template)
**Proximo ID disponivel:** 26_067

### Identificacao de Propostas
- Arquivos PDF com prefixo `ORC_` na pasta `03_Orcamento` indicam proposta gerada
- Sufixo `_R00`, `_R01` etc indica revisao da proposta
- Ultima revisao e a versao vigente

---

## Fluxos com IA

### Fluxo 1: Captura de Informacoes
- Usuario cola texto de email/anotacao
- IA extrai dados e gera JSON estruturado
- Usuario valida
- JSON pronto para insercao

### Fluxo 2: Insercao no Asana via MCP
- IA recebe JSON da demanda
- Aplica regras de formatacao
- Usa MCP Asana para criar tarefa com section_id adequado
- Tarefa criada na secao correspondente ao status

### Fluxo 3: Pesquisa de Informacoes via Chrome MCP
- IA acessa Gmail via Claude in Chrome
- Pesquisa e-mails por demanda
- Extrai dados de contato, escopo, prazos
- Atualiza tarefas no Asana

### Fluxo 4: Extracao de Informacoes de PDFs
- IA lista PDFs relevantes nas pastas do Drive
- Usa `pdftotext` (poppler) para extrair texto dos PDFs
- Analisa textos extraidos para encontrar:
  - Dados de contato (CNPJ, telefone, email, endereco)
  - Detalhes da demanda (escopo, equipamentos, valores)
  - Informacoes tecnicas (capacidades, marcas, modelos)
- Atualiza tarefas no Asana com informacoes extraidas

**Limitacoes:**
- PDFs que sao apenas portfolios genericos nao tem info util
- PDFs de imagem (scan) nao sao extraiveis (precisa OCR)
- Para informacoes faltantes, usar Fluxo 5 (Gemini)

### Fluxo 5: Pesquisa no Gmail via Scripts Python (ATIVO)
- Para demandas com informacoes incompletas apos extracao de PDFs
- Scripts Python acessam Gmail API diretamente (sem MCP externo)
- Processamento em lote: busca, download e extracao automatica
- Dados extraidos via regex (CNPJ, telefone, email, valores)
- Resultados salvos em JSON estruturado

**Pipeline:**
```
processar_demandas.py → gmail_client.py → Gmail API
                      → extrator_dados_email.py → JSON
                      → atualizar_asana.py → plano JSON → MCP Asana
```

**Comandos:**
```bash
source venv/bin/activate
python scripts/processar_demandas.py --id 26_049      # Uma demanda
python scripts/processar_demandas.py --prioridade alta # Por prioridade
python scripts/processar_demandas.py --dry-run         # Simular
python scripts/atualizar_asana.py                      # Gerar plano Asana
```

**Vantagens:**
- Zero Docker/MCP externo
- Conexao direta Python → Google API
- Processamento em lote automatizado
- Dados estruturados com consolidacao de multiplos emails

---

## Comandos MCP Asana

### Criar tarefa com secao
```
asana_create_task
- project_id: 1212920325558530
- section_id: [gid da secao]
- name: [titulo formatado AA_XXX [TIPO] Cliente - Local]
- notes: [descricao]
```

### Upload de anexo
```
asana_upload_attachment_for_object
- object_gid: [task gid]
- file_path: [caminho do arquivo]
```

### Hierarquia do projeto
```
asana_get_project_hierarchy
- project_id: 1212920325558530
- auto_paginate: true
```

---

## Pendencias e Proximos Passos

### Concluido
- [x] Criar projeto no Asana
- [x] Configurar MCP Server do Asana
- [x] Criar tarefa TEMPLATE/GUIA no Asana
- [x] Criar exemplo com subtarefas
- [x] Atualizar documentacao para abordagem v2.0 (subtarefas)
- [x] Comparar abordagens (secoes vs subtarefas)
- [x] Migrar demandas do Comercial Privado para Teste MCP (31 tarefas)
- [x] Padronizar IDs no formato AA_XXX
- [x] Sincronizar IDs com pastas do Google Drive
- [x] Criar documento de informacoes complementares (demandas-complementar-info.md)
- [x] Cadastrar 29 demandas do Drive que faltavam no Asana
- [x] Anexar PDFs de propostas (20 arquivos) nas tarefas da secao Enviado
- [x] Configurar Claude in Chrome para acesso ao Gmail
- [x] Identificar 9 demandas faltantes (Drive vs Asana)
- [x] Cadastrar 6 demandas com info completa do projeto Comercial Privado
- [x] Cadastrar 3 demandas com info basica (26_060, 26_061, 26_062)
- [x] Instalar poppler (pdftotext) para extracao de PDFs
- [x] Extrair texto de PDFs das demandas 26_061 e 26_062
- [x] Atualizar tarefas 26_061 e 26_062 com informacoes extraidas
- [x] Criar arquivo `pesquisa-gemini.md` para busca via Gemini

### Imediato
- [ ] Processar todas as 31 demandas da fila em lote (scripts/processar_demandas.py)
- [ ] Executar plano de atualizacao no Asana via MCP (plano-atualizacao-asana.json)
- [ ] Classificar demandas da secao Enviado (Negociacao / Fechado / Perdido)
- [ ] Atualizar `agente-ai-instrucoes-asana.md` para subtarefas
- [ ] Anexar PDFs das propostas nas tarefas (manual ou script)

### Futuro
- [ ] Criar documento tecnico detalhado (requisitos tecnicos aprofundados)
- [ ] Implementar metricas e dashboard
- [ ] Criar formulario de entrada no Asana (se migrar para plano pago)
- [ ] Automatizar relatorios semanais

---

## Configuracao dos MCPs

### MCP Asana
Configurado no projeto com `@cristip73/mcp-server-asana`.
Token de acesso pessoal configurado via variavel de ambiente.

Ferramentas disponiveis:
- `mcp__asana__asana_create_task` - Criar tarefas
- `mcp__asana__asana_get_project_hierarchy` - Hierarquia do projeto
- `mcp__asana__asana_add_task_to_section` - Mover tarefa para secao
- `mcp__asana__asana_upload_attachment_for_object` - Upload de anexos
- `mcp__asana__asana_search_tasks` - Pesquisar tarefas
- `mcp__asana__asana_update_task` - Atualizar tarefa

Tambem disponivel via Claude.ai connector:
- `mcp__claude_ai_Asana__asana_create_task` - Com suporte a section_id direto

### MCP Chrome (Claude in Chrome)
Extensao do Chrome que permite automacao de navegador.

**Configuracao importante (Mac):**
- Arquivo: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json`
- O `path` deve apontar para `~/.claude/chrome/chrome-native-host` (Claude Code)
- Se apontar para `/Applications/Claude.app/Contents/Helpers/chrome-native-host`, a conexao vai para o Claude Desktop
- **Nao rodar Claude Desktop e Claude Code simultaneamente** - causa conflito de conexao

Ferramentas disponiveis:
- `mcp__claude-in-chrome__tabs_context_mcp` - Contexto das abas
- `mcp__claude-in-chrome__navigate` - Navegar para URL
- `mcp__claude-in-chrome__computer` - Mouse, teclado, screenshots
- `mcp__claude-in-chrome__find` - Encontrar elementos na pagina
- `mcp__claude-in-chrome__read_page` - Ler conteudo da pagina
- `mcp__claude-in-chrome__form_input` - Preencher formularios
- `mcp__claude-in-chrome__get_page_text` - Extrair texto da pagina

### Gmail API (Scripts Python - ATIVO)
**Acesso:** Direto via `src/gmail_client.py` (sem MCP externo)
**Autenticacao:** OAuth 2.0 com token em `config/gmail_token.pickle`
**Escopo OAuth2:** `gmail.modify` (leitura, escrita, envio - SEM exclusão)
**Documentacao de escopos:** `docs/ESCOPOS_GMAIL_API.md`

**Pipeline de processamento:**
```bash
source venv/bin/activate
python scripts/processar_demandas.py --id 26_049
python scripts/atualizar_asana.py
```

**Documentacao completa:** `PLANO_SIMPLIFICACAO_GMAIL.md`

**Nota:** MCP Gmail via Gemini CLI (`@mcp-z/mcp-gmail`) foi descontinuado
por problemas de dependencias e complexidade. Documentacao legada em
`configuracao-mcp-gmail.md` e `integracao-claude-gemini.md`.

### Gmail (via Chrome MCP) [Legado]
Conta de trabalho: orcamentos2@armant.com.br (E-mail de Armant)
Acesso via navegacao no Gmail usando Claude in Chrome
**Nota:** Preferir MCP Gmail via Gemini CLI para buscas automatizadas

---

## Como Usar Este Projeto

### Para Criar Nova Demanda via IA

1. Abra conversa com Claude Code nesta pasta
2. Cole o texto da demanda (email, anotacao, etc)
3. Peca: "Extraia os dados e crie a tarefa no Asana"
4. IA processara e criara a tarefa

### Para Consultar Tarefas

1. Peca: "Liste as tarefas urgentes"
2. Peca: "Quais orcamentos estao em elaboracao?"
3. Peca: "Mova a tarefa X para Enviado"

### Para Registrar Fechamento/Perda

1. Peca: "Registre o fechamento da tarefa X, valor R$ Y"
2. Peca: "Registre a perda da tarefa X, motivo: preco"

---

## Informacoes do Setor

**Area:** Orcamentos de Climatizacao
**Servicos:** Instalacao, Manutencao, Projetos
**Origens de Demanda:** Comercial, Engenharia, Diretoria, Cliente Direto, Licitacoes
**Volume:** 10-30 demandas/semana
**Usuarios do Asana:** 5-10 pessoas

---

## Contato

Para duvidas sobre este projeto ou sobre a estrutura de orcamentos, contatar o coordenador do setor.

---

## Integracao Claude Code + Gemini CLI

### Fluxo de Pesquisa Gmail

O acesso ao Gmail para complementar informacoes das demandas e feito atraves do Gemini CLI com MCP Gmail.

**Arquivos de integracao:**
```
gemini-tasks/
  ├── GEMINI-INSTRUCOES.md          # Instrucoes para o Gemini
  ├── pesquisa-gmail-pendentes.md   # Lista de 31 tarefas de pesquisa
  ├── fila-pesquisa.json            # Fila de tarefas (status)
  ├── resultados-pesquisa-gmail.json # Resultados das pesquisas
  └── executar-pesquisa-gemini.sh   # Script auxiliar
```

### Como Funciona

1. **Claude Code** identifica tarefas no Asana que precisam de informacoes
2. **Claude Code** envia tarefa de pesquisa para **Gemini CLI**
3. **Gemini CLI** pesquisa no Gmail via MCP
4. **Gemini CLI** retorna JSON com dados extraidos
5. **Claude Code** atualiza a tarefa no Asana

### Formato de Comunicacao

**Claude Code -> Gemini:**
```
PESQUISA_GMAIL:
- ID: TASK_XXX
- Asana: 26_XXX
- Cliente: Nome
- Pesquisar: "termo1" OR "termo2"
- Extrair: cliente, cnpj, contato, detalhes
```

**Gemini -> Claude Code:**
```json
{
  "task_id": "TASK_XXX",
  "status": "encontrado",
  "dados": { ... }
}
```

### Status Atual

- **31 tarefas** na fila de pesquisa
- **10 prioridade alta** (dados criticos faltando)
- **17 prioridade media** (dados parciais)
- **4 prioridade baixa** (apenas classificacao)

---

## Padrões e Lições Aprendidas

### Formato de Notas do Asana
**IMPORTANTE:** O Asana renderiza markdown de forma limitada:
- ❌ **NÃO usar** markdown bold (`**texto**`) - renderiza como texto puro
- ✅ Usar seções em CAPS com separadores:
  - `═══════════════` para título principal
  - `-------------------` para subseções
- ✅ Campos sempre no formato: `Campo: Valor`
- ✅ Seções padrão: DADOS DO ORCAMENTO, DETALHES DA DEMANDA, ORIGEM, CLASSIFICACAO, ARQUIVOS, STATUS
- 📄 **Referência:** Ver tarefa 26_024 (GID 1213131774336781) como modelo

### Padrões de Clientes e Contatos
- **"Portilho"** = Matheus Portilho (funcionário Banrisul que solicita orçamentos, **NÃO é cliente**)
- **Email padrão Banrisul:** Engenharia_Mecanica_Agencias@banrisul.com.br
- **"Thomas Grazioli"** = solicitante interno frequente (operacional Armant)
- **Power Services** = Grupo Sigel (mesmo cliente, ref: 26_042)

### Limitações Técnicas (Plano Gratuito Asana)
- ❌ `asana_search_tasks` **requer plano premium**
- ✅ Usar `asana_typeahead_search` para busca no plano gratuito
- ✅ Typeahead funciona bem com nome parcial da tarefa
- ⚠️ MCP Asana não tem função "mover tarefa para seção" - movimentação deve ser feita manualmente na UI

### Processamento de Dados
- **Trello:** Arquivo JSON muito grande (17MB) - usar Python para processar, não jq
- **Trello Listas relevantes:** Caixa de Entrada, CORRETIVAS/OPERACIONAL, EM ANDAMENTO
- **Filtrar imagens** nos anexos Trello (.jpg, .png, .webp, etc.) - não adicionar ao Asana
- **Arquivos grandes:** Usar scripts Python para extrair informações, não ler diretamente

### Identificação de Propostas no Drive
- Arquivos PDF com prefixo `ORC_` na pasta `03_Orcamento/` indicam proposta gerada
- Sufixo `_R00`, `_R01`, etc. indica revisão da proposta
- Última revisão é a versão vigente
- Sempre verificar subpastas dentro de `03_Orcamento/` (ex: `PMOC/`, `ASSINAR/`)

---

## Historico de Alteracoes

| Data | Alteracao |
|------|-----------|
| Janeiro/2025 | Criacao inicial do projeto |
| Janeiro/2025 | Documentacao da estrutura Asana |
| Janeiro/2025 | Instrucoes para Agente AI |
| Janeiro/2025 | Template de captura |
| Janeiro/2025 | Guia de requisitos para solicitacao |
| Janeiro/2026 | Migracao de 31 demandas do Comercial Privado para Teste MCP |
| Janeiro/2026 | Padronizacao de IDs (AA_XXX) e sincronizacao com Google Drive |
| Janeiro/2026 | Cadastro de 29 demandas do Drive faltantes no Asana |
| Janeiro/2026 | Anexacao de 20 PDFs de propostas nas tarefas do Asana |
| Janeiro/2026 | Configuracao do Claude in Chrome para acesso ao Gmail |
| Janeiro/2026 | Atualizacao do CLAUDE.md com estrutura completa do projeto |
| Fevereiro/2026 | Criacao do fluxo Claude Code + Gemini CLI para pesquisa Gmail |
| Fevereiro/2026 | Validacao e atualizacao de 15 propostas na secao Entrada |
| Fevereiro/2026 | Criacao de 5 novas demandas (26_072 a 26_075) e 25_871 (FAURG) |
| Fevereiro/2026 | Adicao da secao "Padroes e Licoes Aprendidas" no CLAUDE.md |
| Fevereiro/2026 | Implementacao pipeline Gmail: processar_demandas.py + extrator_dados_email.py + atualizar_asana.py |
| Fevereiro/2026 | Descontinuacao MCPs Gmail externos em favor de scripts Python diretos |

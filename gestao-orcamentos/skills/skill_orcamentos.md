# Skill: Gestão de Orçamentos - Climatização

**Versão:** 1.0.0
**Atualizado:** 30/01/2026
**Compatível com:** Claude Haiku 4, Claude Sonnet 4.5, Claude Opus 4

---

## 📋 Propósito

Esta skill permite processar demandas de orçamentos do Setor de Climatização de forma automatizada:
- Buscar emails relacionados
- Preparar e limpar dados
- Extrair informações com IA
- Criar tarefas estruturadas no Asana

---

## 🎯 Quando Usar Esta Skill

Use esta skill quando o usuário:
- ✅ Mencionar "processar orçamento", "nova demanda", "criar tarefa"
- ✅ Fornecer ID de pasta (ex: "26_062")
- ✅ Pedir para buscar emails sobre orçamento
- ✅ Quiser extrair dados de emails/documentos
- ✅ Solicitar criação de tarefa no Asana

**Não use** para:
- ❌ Consultar tarefas existentes (use MCP Asana direto)
- ❌ Atualizar tarefas (use MCP Asana direto)
- ❌ Buscas genéricas não relacionadas a orçamentos

---

## 🚀 Fluxo de Trabalho Padrão

### Cenário 1: Processar Nova Demanda (Mais Comum)

**Input do usuário:**
> "Processar pasta 26_062"
> "Nova demanda 26_063"
> "Criar orçamento para pasta 26_064"

**Ação:**
```bash
python src/cli.py processar-pasta [ID] --confirm -v
```

**Passos executados automaticamente:**
1. Verifica pasta no Drive
2. Busca emails relacionados
3. Prepara dados (reduz 60-80% tokens)
4. Extrai com IA (Haiku, fallback Sonnet)
5. Valida JSON
6. Cria tarefa no Asana (+ 7 subtarefas)
7. Anexa PDFs
8. Exibe relatório

**Resposta ao usuário:**
```
✅ Demanda processada com sucesso!

📊 Resumo:
- Duração: 8.3s
- Emails encontrados: 3
- Custo IA: $0.0004
- Tarefa criada: [LINK_ASANA]

Cliente: [NOME]
Local: [CIDADE] - [UF]
Tipo: [TIPO_SERVICO]
```

---

### Cenário 2: Testar sem Criar Tarefa

**Input do usuário:**
> "Testar processamento da pasta 26_062"
> "Dry-run para 26_063"

**Ação:**
```bash
python src/cli.py processar-pasta [ID] --dry-run -v
```

**Resposta ao usuário:**
```
🔍 Modo de teste executado (sem alterações):

✓ Pasta encontrada
✓ Dados preparados
✓ Extração simulada

Cliente estimado: [NOME]
Local estimado: [CIDADE]

Para criar de verdade, use: processar-pasta [ID] --confirm
```

---

### Cenário 3: Buscar Emails Apenas

**Input do usuário:**
> "Buscar emails sobre 26_062"
> "Quais emails tenho sobre JBS Seara?"

**Ação:**
```bash
python src/cli.py buscar-emails [ID] --query "[TERMOS]"
```

**Resposta ao usuário:**
```
📧 Encontrados [N] emails:

1. [ASSUNTO_1]
   De: [REMETENTE]
   Data: [DATA]

2. [ASSUNTO_2]
   ...

Quer processar esses emails? Use: processar-pasta [ID]
```

---

### Cenário 4: Extrair Dados de Arquivo Específico

**Input do usuário:**
> "Extrair dados deste email: [caminho/arquivo.html]"
> "Processar este documento"

**Ação (em 2 etapas):**
```bash
# 1. Preparar dados
python src/cli.py preparar-dados [arquivo] -o preparado.md

# 2. Extrair com IA
python src/cli.py extrair-dados preparado.md -o orcamento.json
```

**Resposta ao usuário:**
```
✅ Dados extraídos:

Cliente: [NOME]
CNPJ/CPF: [DOCUMENTO]
Local: [CIDADE] - [UF]
Tipo de serviço: [TIPO]
Prazo: [DATA]

JSON salvo em: orcamento.json

Quer criar tarefa no Asana? Use: criar-tarefa orcamento.json
```

---

### Cenário 5: Criar Tarefa de JSON Pronto

**Input do usuário:**
> "Criar tarefa no Asana com este JSON: [caminho/orcamento.json]"

**Ação:**
```bash
python src/cli.py criar-tarefa [arquivo.json]
```

**Resposta ao usuário:**
```
✅ Tarefa criada no Asana!

Título: [TITULO_FORMATADO]
URL: [LINK_ASANA]

Subtarefas criadas:
- 🔍 Triagem
- ✅ Aprovação para Elaboração
- 📝 Elaboração do Orçamento
- 🔎 Revisão Interna
- 📤 Envio ao Cliente
- 🤝 Negociação
- 🏁 Fechamento

Tags aplicadas: [TAGS]
```

---

## 🛠️ Comandos Disponíveis

### 1. Pipeline Completo
```bash
python src/cli.py processar-pasta [ID] [OPÇÕES]
```

**Opções:**
- `--confirm` - Pedir confirmação antes de criar tarefa
- `--dry-run` - Simular sem executar
- `--sonnet` - Forçar uso do Sonnet (casos complexos)
- `--query "texto"` - Query customizada para busca de emails
- `-v` - Log detalhado

**Quando usar:**
- ✅ Nova demanda chegou
- ✅ Quer processar tudo de uma vez
- ✅ Pasta existe no Drive

### 2. Buscar Emails
```bash
python src/cli.py buscar-emails [ID] [OPÇÕES]
```

**Opções:**
- `--query "texto"` - Query customizada
- `--max-results N` - Limitar resultados (padrão: 10)

**Quando usar:**
- ✅ Quer apenas encontrar emails
- ✅ Não tem certeza se há emails sobre o assunto
- ✅ Quer confirmar query antes de processar

### 3. Preparar Dados
```bash
python src/cli.py preparar-dados [ARQUIVO/PASTA] -o [OUTPUT]
```

**Quando usar:**
- ✅ Tem email/documento bruto
- ✅ Quer limpar antes de processar
- ✅ Quer ver redução de tokens

**Output esperado:**
- Texto limpo em Markdown
- 60-80% menos tokens
- Metadados extraídos (CNPJ, telefones, etc)

### 4. Extrair Dados
```bash
python src/cli.py extrair-dados [ARQUIVO] [OPÇÕES]
```

**Opções:**
- `-o arquivo.json` - Salvar resultado
- `--sonnet` - Forçar Sonnet

**Quando usar:**
- ✅ Tem texto preparado
- ✅ Quer apenas extrair dados
- ✅ Já revisou preparação

**Modelo usado:**
- Padrão: Haiku ($0.0004/demanda)
- Fallback: Sonnet se Haiku falhar
- Forçado: Sonnet ($0.0015/demanda) com `--sonnet`

### 5. Criar Tarefa
```bash
python src/cli.py criar-tarefa [arquivo.json]
```

**Quando usar:**
- ✅ Já tem JSON validado
- ✅ Quer apenas criar no Asana
- ✅ Dados foram revisados manualmente

---

## 💡 Decisões Importantes

### Quando usar `--confirm`?

**Use:**
- ✅ Primeira vez processando uma demanda
- ✅ Não tem certeza dos dados
- ✅ Quer revisar antes de criar
- ✅ Demanda complexa/licitação

**Não use:**
- ❌ Scripts automáticos
- ❌ Processamento em lote
- ❌ Já validou dados

### Quando usar `--dry-run`?

**Use:**
- ✅ Testar sistema novo
- ✅ Verificar se pasta/emails existem
- ✅ Ver custo estimado antes de executar
- ✅ Debugging

**Não use:**
- ❌ Quando quer realmente criar tarefa
- ❌ Em produção

### Quando usar `--sonnet`?

**Use:**
- ✅ Licitação complexa com múltiplos documentos
- ✅ Haiku falhou na extração
- ✅ Dados muito ambíguos/incompletos
- ✅ Cliente estratégico (precisão máxima)

**Não use:**
- ❌ Por padrão (12x mais caro)
- ❌ Emails simples/diretos
- ❌ Se Haiku conseguiu extrair

**Custo:**
- Haiku: ~$0.0004/demanda
- Sonnet: ~$0.0015/demanda
- Diferença: 4x mais caro

---

## 🔍 Troubleshooting

### Problema: "Pasta não encontrada"

**Causa:** ID da pasta não existe no Drive

**Solução:**
1. Verificar se pasta existe:
   ```bash
   ls ~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared\ drives/02Orcamentos/2026/ | grep [ID]
   ```
2. Continuar sem pasta (busca só emails):
   ```bash
   python src/cli.py processar-pasta [ID] --query "termos específicos"
   ```
3. Criar pasta primeiro se necessário

**Resposta ao usuário:**
```
⚠️ Pasta [ID] não encontrada no Drive.

Opções:
1. Criar pasta no Drive primeiro
2. Continuar com busca de emails apenas
3. Verificar se ID está correto

Quer que eu busque emails mesmo sem pasta?
```

---

### Problema: "Gmail authentication failed"

**Causa:** Token OAuth expirado ou credenciais inválidas

**Solução:**
```bash
# Re-autenticar
python src/gmail_client.py --setup

# Testar conexão
python src/gmail_client.py --test
```

**Resposta ao usuário:**
```
❌ Erro de autenticação Gmail.

Por favor, execute:
1. python src/gmail_client.py --setup
2. Siga as instruções no navegador
3. Tente novamente

[Link para guia: docs/SETUP_GMAIL_API.md]
```

---

### Problema: "Validation failed" (extração)

**Causa:** IA não conseguiu extrair campos obrigatórios

**Solução automática:**
- Haiku falhou → tenta Sonnet automaticamente
- Sonnet falhou → reportar ao usuário

**Resposta ao usuário:**
```
⚠️ Não foi possível extrair todos os dados automaticamente.

Dados faltantes:
- [CAMPO_1]
- [CAMPO_2]

Opções:
1. Fornecer informações manualmente
2. Verificar se emails/documentos têm os dados
3. Processar parcialmente e completar depois

Quer que eu crie um JSON parcial para você revisar?
```

---

### Problema: Custo muito alto

**Causa:** Usando Sonnet quando poderia usar Haiku

**Diagnóstico:**
```bash
python src/cli.py processar-pasta [ID] -v | grep "Modelo:"
```

**Deve mostrar:** `Modelo: haiku-4`

**Se mostrar:** `Modelo: sonnet-4.5` → investigar por quê

**Solução:**
- Remover flag `--sonnet` se não necessária
- Melhorar preparação de dados
- Verificar se dados estão claros

**Resposta ao usuário:**
```
💰 Custo observado: $[VALOR]

Esperado: ~$0.0004 (Haiku)
Atual: ~$0.0015 (Sonnet)

O sistema está usando Sonnet porque:
[RAZÃO]

Para reduzir custos:
- Melhorar qualidade dos dados de entrada
- Remover flag --sonnet
- Usar preparação de dados primeiro
```

---

### Problema: "No emails found"

**Causa:** Query não encontrou emails relacionados

**Solução:**
1. Tentar query mais específica:
   ```bash
   python src/cli.py buscar-emails [ID] --query "cliente nome projeto"
   ```
2. Verificar se emails existem no Gmail
3. Processar sem emails (dados manuais)

**Resposta ao usuário:**
```
📧 Nenhum email encontrado com a query atual.

Query usada: "[QUERY]"

Sugestões:
1. Fornecer query mais específica: --query "termos exatos"
2. Buscar no Gmail manualmente
3. Processar com dados manuais (sem emails)

Quer tentar outra query?
```

---

## 📊 Métricas de Sucesso

Ao reportar ao usuário, sempre incluir:

```
📊 Métricas desta operação:

⏱️  Duração: [X.X]s
📧 Emails: [N] encontrados
📄 Arquivos: [N] processados
🎯 Tokens: [N] usados
💰 Custo: $[0.XXXX]
🤖 Modelo: [haiku-4 / sonnet-4.5]

✅ Taxa de sucesso: [%]
🔄 Fallbacks usados: [N]
```

**Métricas esperadas (normais):**
- Duração: 5-10s
- Emails: 1-5
- Arquivos: 1-3
- Tokens: 500-1000
- Custo: $0.0004-0.0015
- Modelo: haiku-4 (85-90% dos casos)

**Se métricas anormais:**
- Duração > 20s → investigar lentidão
- Tokens > 2000 → preparação pode melhorar
- Custo > $0.005 → revisar uso de Sonnet

---

## 🎓 Exemplos de Conversas

### Exemplo 1: Processamento Simples

**Usuário:** "Processar pasta 26_062"

**Você:**
```
Vou processar a demanda 26_062. Um momento...

[Executa: python src/cli.py processar-pasta 26_062 --confirm -v]

✅ Demanda processada com sucesso!

📊 Resumo:
- Cliente: JBS Seara - Unidade Nova Veneza
- Local: Nova Veneza - SC
- Tipo: Projeto de climatização
- Prazo: 2026-02-15
- Custo IA: $0.0004

Tarefa criada no Asana:
🔗 https://app.asana.com/0/1212920325558530/[TASK_ID]

Próximos passos:
1. ✅ Triagem (subtarefa 1)
2. Aprovar para elaboração (subtarefa 2)
```

---

### Exemplo 2: Teste Antes de Criar

**Usuário:** "Quero testar o processamento da pasta 26_063 antes de criar a tarefa"

**Você:**
```
Vou fazer um teste sem criar tarefa:

[Executa: python src/cli.py processar-pasta 26_063 --dry-run -v]

🔍 Resultado do teste:

✓ Pasta encontrada no Drive
✓ 2 emails encontrados
✓ Dados preparados (745 tokens)
✓ Extração estimada com Haiku

Dados identificados:
- Cliente: Empresa ABC Ltda
- Local: São Paulo - SP
- Tipo: Instalação
- Urgente: Não

Custo estimado: $0.0004

Tudo parece correto! Quer que eu crie a tarefa de verdade?
```

**Usuário:** "Sim, pode criar"

**Você:**
```
[Executa: python src/cli.py processar-pasta 26_063 --confirm]

✅ Tarefa criada!
🔗 [LINK]
```

---

### Exemplo 3: Busca de Emails

**Usuário:** "Quais emails tenho sobre a JBS Seara?"

**Você:**
```
Vou buscar emails sobre JBS Seara:

[Executa: python src/cli.py buscar-emails SEARA --query "JBS Seara" --max-results 10]

📧 Encontrados 4 emails:

1. "Solicitação orçamento - Climatização Nova Veneza"
   De: cesar@jbsseara.com
   Data: 2026-01-28

2. "Re: Solicitação orçamento - Dados complementares"
   De: cesar@jbsseara.com
   Data: 2026-01-29

3. "Urgente - Prazo do orçamento"
   De: cesar@jbsseara.com
   Data: 2026-01-30

4. "Projeto climatização - Memorial descritivo"
   De: engenharia@jbsseara.com
   Data: 2026-01-30

Quer que eu processe esses emails e crie uma demanda?
```

---

### Exemplo 4: Erro e Recuperação

**Usuário:** "Processar pasta 26_999"

**Você:**
```
[Executa: python src/cli.py processar-pasta 26_999 -v]

⚠️ Pasta 26_999 não encontrada no Drive.

Deixa eu buscar emails mesmo assim...

[Executa busca de emails]

❌ Nenhum email encontrado também.

Opções:
1. Verificar se o ID está correto (26_999)
2. Criar pasta no Drive primeiro
3. Fornecer dados manualmente para criar tarefa

Qual prefere?
```

**Usuário:** "O ID correto é 26_062"

**Você:**
```
Ah, entendi! Vou processar 26_062:

[Continua com processamento normal]
```

---

## 🔐 Considerações de Segurança

### Credenciais
- ❌ NUNCA mostrar tokens/credenciais ao usuário
- ❌ NUNCA logar senhas ou API keys
- ✅ Usar variáveis de ambiente (.env)
- ✅ Referenciar docs se configuração necessária

### Dados Sensíveis
- ⚠️ Emails podem conter dados sensíveis (CNPJ, CPF, telefones)
- ✅ Processar apenas dados necessários
- ✅ Não logar conteúdo completo de emails
- ✅ Respeitar privacidade do cliente

### Asana
- ✅ Criar tarefas apenas com confirmação (flag `--confirm`)
- ✅ Usar dry-run para testes
- ❌ Não criar duplicatas
- ❌ Não modificar tarefas existentes sem permissão

---

## 📚 Referências

### Documentação
- **Arquitetura:** `ARQUITETURA.md`
- **Plano:** `PLANO_IMPLEMENTACAO.md`
- **Setup Gmail:** `docs/SETUP_GMAIL_API.md`
- **Integração Asana:** `docs/INTEGRACAO_ASANA.md`
- **Custos IA:** `docs/COMPARACAO_CUSTOS_IA.md`
- **Exemplos:** `EXEMPLO_CLI.md`

### Scripts Python
- **CLI:** `src/cli.py` (orquestrador principal)
- **Gmail:** `src/gmail_client.py`
- **Preparação:** `src/prepare_data.py`
- **Extração IA:** `src/ai_extractor.py`
- **Asana:** `src/asana_lib.py`

### Testes
- **Todos:** `pytest tests/ -v`
- **CLI:** `pytest tests/test_cli.py -v`
- **Específico:** `pytest tests/test_[modulo].py -v`

---

## 🔄 Atualizações e Manutenção

**Versão atual:** 1.0.0

**Changelog:**
- 1.0.0 (30/01/2026): Versão inicial da skill
  - Pipeline completo implementado
  - 5 comandos disponíveis
  - Troubleshooting documentado
  - Exemplos de uso incluídos

**Próximas melhorias planejadas:**
- Sincronização automática Drive ↔ Asana
- Comando `sync-drive`
- Dashboards e relatórios
- Automação via cron jobs

---

**Última atualização:** 30/01/2026
**Mantido por:** Coordenador do Setor de Orçamentos
**Projeto:** Sistema de Gestão de Orçamentos - Climatização Armant

# Guia do Usuário - Sistema de Gestão de Orçamentos

**Versão:** 1.0.0
**Público-alvo:** Coordenador e equipe do Setor de Orçamentos
**Última atualização:** 30/01/2026

---

## 📋 Visão Geral

Este sistema automatiza o processamento de demandas de orçamentos, reduzindo drasticamente o tempo e custo de cada operação.

### O que o sistema faz?

```
Email do cliente → Sistema → Tarefa no Asana
     (5 min)         (8s)       (pronta!)
```

**Antes (manual):**
- ⏱️ 15-20 minutos por demanda
- 💰 Alto custo de IA
- 🔴 Sujeito a erros humanos

**Depois (automatizado):**
- ⏱️ 2 minutos por demanda (87.5% mais rápido)
- 💰 $0.0006 por demanda (97% mais barato)
- 🟢 Consistente e confiável

---

## 🚀 Quick Start

### Pré-requisitos

1. ✅ Python 3.10+ instalado
2. ✅ Acesso ao Gmail (orcamentos2@armant.com.br)
3. ✅ Acesso ao Asana (projeto Teste MCP)
4. ✅ Sistema configurado (ver seção Setup)

### Uso Básico

**Processar uma nova demanda:**

```bash
# 1. Abrir terminal no diretório do projeto
cd ~/dev/tools/armant/gestao-orcamentos

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Processar demanda
python src/cli.py processar-pasta 26_062 --confirm

# 4. Aguardar resultado (~8 segundos)
# 5. Tarefa criada no Asana!
```

---

## 📖 Fluxos de Trabalho

### Fluxo 1: Demanda Nova (Mais Comum)

**Situação:** Chegou email de cliente solicitando orçamento

**Passo-a-passo:**

1. **Criar pasta no Drive** (se ainda não existe)
   - Acessar: `Google Drive > 02Orcamentos > 2026`
   - Criar: `26_XXX_CLIENTE_SERVICO`
   - Onde XXX é o próximo número sequencial

2. **Processar demanda via sistema**
   ```bash
   python src/cli.py processar-pasta 26_XXX --confirm
   ```

3. **Sistema executa automaticamente:**
   - ✅ Busca emails relacionados no Gmail
   - ✅ Prepara e limpa dados
   - ✅ Extrai informações com IA
   - ✅ Cria tarefa no Asana com 7 subtarefas
   - ✅ Anexa PDFs encontrados

4. **Revisar no Asana:**
   - Abrir link fornecido pelo sistema
   - Verificar se dados estão corretos
   - Começar trabalho na subtarefa 1 (Triagem)

**Tempo total:** ~2 minutos (incluindo criação de pasta)

---

### Fluxo 2: Testar Antes de Criar

**Situação:** Não tem certeza se dados estão completos

**Passo-a-passo:**

1. **Executar em modo teste:**
   ```bash
   python src/cli.py processar-pasta 26_XXX --dry-run
   ```

2. **Revisar output:**
   - Cliente identificado
   - Local identificado
   - Tipo de serviço
   - Custo estimado

3. **Se correto, criar de verdade:**
   ```bash
   python src/cli.py processar-pasta 26_XXX --confirm
   ```

4. **Se incorreto:**
   - Buscar mais emails: `buscar-emails 26_XXX --query "termos"`
   - Ou fornecer dados manualmente

**Tempo total:** ~3 minutos (teste + criação)

---

### Fluxo 3: Buscar Informações sobre Cliente

**Situação:** Precisa encontrar emails sobre um cliente/projeto

**Passo-a-passo:**

1. **Buscar emails:**
   ```bash
   python src/cli.py buscar-emails TERMO --query "JBS Seara"
   ```

2. **Sistema retorna:**
   - Lista de emails encontrados
   - Assunto, remetente, data
   - ID de cada email

3. **Usar informações para:**
   - Processar demanda
   - Complementar dados
   - Contatar cliente

**Tempo total:** ~30 segundos

---

### Fluxo 4: Licitação Complexa

**Situação:** Licitação com múltiplos documentos

**Passo-a-passo:**

1. **Processar com Sonnet** (mais preciso):
   ```bash
   python src/cli.py processar-pasta 26_XXX --sonnet --confirm
   ```

2. **Custo será maior** (~$0.0015 vs $0.0004):
   - Justificado pela complexidade
   - Menor chance de erro
   - Vale a pena para licitações

3. **Revisar cuidadosamente:**
   - Número do edital
   - Prazo correto
   - Todos os requisitos

**Tempo total:** ~3 minutos

---

## 🛠️ Comandos Disponíveis

### Comando Principal: `processar-pasta`

**Descrição:** Pipeline completo de processamento

**Sintaxe:**
```bash
python src/cli.py processar-pasta [ID] [OPÇÕES]
```

**Opções:**
- `--confirm` - Pedir confirmação antes de criar (RECOMENDADO)
- `--dry-run` - Simular sem criar (para testes)
- `--sonnet` - Usar Sonnet em vez de Haiku (licitações)
- `--query "texto"` - Query customizada para Gmail
- `-v` - Log detalhado (para debugging)

**Exemplos:**
```bash
# Uso básico (recomendado)
python src/cli.py processar-pasta 26_062 --confirm

# Teste sem criar
python src/cli.py processar-pasta 26_062 --dry-run

# Licitação complexa
python src/cli.py processar-pasta 26_062 --sonnet --confirm

# Com query específica
python src/cli.py processar-pasta 26_062 --query "JBS Seara urgente"

# Debug detalhado
python src/cli.py processar-pasta 26_062 --confirm -v
```

---

### Comando: `buscar-emails`

**Descrição:** Buscar emails no Gmail

**Sintaxe:**
```bash
python src/cli.py buscar-emails [ID_OU_TERMO] [OPÇÕES]
```

**Opções:**
- `--query "texto"` - Query de busca customizada
- `--max-results N` - Limitar número de resultados (padrão: 10)

**Exemplos:**
```bash
# Buscar por ID de pasta
python src/cli.py buscar-emails 26_062

# Buscar por cliente
python src/cli.py buscar-emails TERMO --query "JBS Seara"

# Buscar emails recentes
python src/cli.py buscar-emails HOJE --query "orçamento after:2026/01/30"

# Limitar resultados
python src/cli.py buscar-emails 26_062 --max-results 5
```

**Dicas de Query Gmail:**
- `from:email@exemplo.com` - Do remetente específico
- `subject:orçamento` - Com assunto específico
- `after:2026/01/25` - Após data
- `has:attachment` - Com anexo
- Combinar: `from:cliente@email.com subject:orçamento after:2026/01/20`

---

### Comandos Avançados

**Preparar dados:**
```bash
python src/cli.py preparar-dados arquivo.html -o preparado.md
```

**Extrair com IA:**
```bash
python src/cli.py extrair-dados preparado.md -o orcamento.json
```

**Criar tarefa:**
```bash
python src/cli.py criar-tarefa orcamento.json
```

---

## 📊 Entendendo o Relatório

Após processar, o sistema exibe:

```
============================================================
📊 Relatório de Processamento
============================================================
⏱️  Duração: 8.3s                    ← Tempo total
📧 Emails encontrados: 3             ← Emails do Gmail
📄 Arquivos processados: 2           ← Arquivos da pasta Drive
🎯 Tokens usados: 687                ← Tokens enviados para IA
💰 Custo total: $0.0004              ← Custo da operação
✅ Tarefa criada: 1234567890123456   ← ID da tarefa
🔗 https://app.asana.com/0/.../...   ← Link direto
============================================================
```

**Valores normais:**
- ⏱️ Duração: 5-10s
- 📧 Emails: 1-5
- 📄 Arquivos: 1-3
- 🎯 Tokens: 500-1000
- 💰 Custo: $0.0004-0.0015

**Se valores anormais:**
- Duração > 20s → Possível lentidão de rede
- Tokens > 2000 → Muitos dados, considerar limpar manualmente
- Custo > $0.005 → Sistema usou Sonnet, verificar por quê

---

## 🎯 Boas Práticas

### ✅ Fazer

1. **Sempre usar `--confirm`** em produção
   - Permite revisar antes de criar
   - Evita criação de tarefas duplicadas

2. **Usar `--dry-run` quando incerto**
   - Testa sem fazer alterações
   - Verifica se dados serão extraídos corretamente

3. **Criar pasta no Drive primeiro**
   - Sistema funciona melhor com pasta organizada
   - Facilita anexar documentos depois

4. **Revisar tarefa criada no Asana**
   - Dados podem estar incompletos
   - Ajustar conforme necessário

5. **Manter pastas organizadas no Drive**
   - Padrão: `26_XXX_CLIENTE_SERVICO`
   - Facilita buscas futuras

### ❌ Evitar

1. **Não processar mesma demanda duas vezes**
   - Cria tarefas duplicadas no Asana
   - Se errou, deletar tarefa no Asana primeiro

2. **Não usar `--sonnet` por padrão**
   - 12x mais caro que Haiku
   - Reservar para casos complexos

3. **Não ignorar erros**
   - Se sistema reporta erro, investigar
   - Ler mensagem de erro com atenção

4. **Não desativar ambiente virtual**
   - Sempre ativar: `source venv/bin/activate`
   - Sistema não funciona sem dependências

5. **Não modificar código sem backup**
   - Sistema está funcionando
   - Mudanças podem quebrar funcionalidades

---

## 📅 Rotina Diária Recomendada

### Manhã (9h)

1. **Verificar emails novos:**
   ```bash
   python src/cli.py buscar-emails HOJE --query "orçamento after:$(date -d yesterday +%Y/%m/%d)"
   ```

2. **Para cada demanda nova:**
   - Criar pasta no Drive
   - Processar: `python src/cli.py processar-pasta 26_XXX --confirm`

**Tempo estimado:** 5-10 minutos para 3-5 demandas

---

### Tarde (14h)

1. **Revisar tarefas criadas de manhã**
   - Abrir Asana
   - Completar subtarefa 1 (Triagem)
   - Avançar para elaboração

2. **Processar demandas urgentes**
   - Se chegou email urgente
   - Processar imediatamente

**Tempo estimado:** Variável

---

### Fim do dia (17h)

1. **Verificar se há demandas pendentes**
   ```bash
   python src/cli.py buscar-emails HOJE --query "orçamento"
   ```

2. **Atualizar status no Asana**
   - Mover tarefas para seções corretas
   - Adicionar comentários

**Tempo estimado:** 5 minutos

---

## 🆘 Problemas Comuns

### "Pasta não encontrada"

**Causa:** ID da pasta não existe no Drive

**Solução:**
1. Verificar se pasta existe
2. Criar pasta se necessário
3. Ou processar sem pasta: `--query "termos específicos"`

---

### "Gmail authentication failed"

**Causa:** Token OAuth expirado

**Solução:**
```bash
python src/gmail_client.py --setup
# Seguir instruções no navegador
```

---

### "No emails found"

**Causa:** Query não encontrou emails

**Solução:**
1. Tentar query mais específica
2. Verificar se emails existem no Gmail
3. Processar com dados manuais

---

### "Validation failed"

**Causa:** IA não conseguiu extrair todos os dados

**Solução:**
1. Sistema tentará Sonnet automaticamente
2. Se Sonnet falhar, fornecer dados manualmente
3. Criar tarefa parcial e completar no Asana

---

### "Custo muito alto"

**Causa:** Sistema usando Sonnet em vez de Haiku

**Solução:**
1. Verificar: `python src/cli.py processar-pasta 26_XXX -v | grep "Modelo:"`
2. Se Sonnet, investigar por quê
3. Melhorar preparação de dados

---

### "ModuleNotFoundError"

**Causa:** Dependências não instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 📞 Suporte

### Para Problemas Técnicos

1. **Verificar documentação:**
   - `TROUBLESHOOTING.md` - Problemas comuns
   - `EXEMPLO_CLI.md` - Exemplos de uso
   - `README.md` - Visão geral

2. **Executar com debug:**
   ```bash
   python src/cli.py processar-pasta 26_XXX --confirm -v
   ```
   - Salvar output completo
   - Compartilhar com suporte

3. **Contatar desenvolvedor:**
   - Descrever problema
   - Incluir output do sistema
   - Mencionar o que estava tentando fazer

### Para Dúvidas de Uso

1. **Consultar este guia**
2. **Ver exemplos:** `EXEMPLO_CLI.md`
3. **Perguntar ao coordenador**

---

## 🎓 Recursos de Aprendizado

### Documentação Técnica

- **ARQUITETURA.md** - Como o sistema funciona internamente
- **PLANO_IMPLEMENTACAO.md** - Histórico de desenvolvimento
- **docs/COMPARACAO_CUSTOS_IA.md** - Análise de custos detalhada

### Guias Específicos

- **docs/SETUP_GMAIL_API.md** - Configurar Gmail API
- **docs/INTEGRACAO_ASANA.md** - Integrar com Asana
- **EXEMPLO_CLI.md** - 9 cenários de uso completos

### Para Desenvolvedores

- **GUIA_DESENVOLVEDOR.md** - Estender funcionalidades
- **skills/README.md** - Criar novas skills
- `tests/` - Exemplos de testes

---

## 📈 Métricas de Sucesso

### Acompanhar

- ⏱️ **Tempo médio por demanda:** Meta <2 min
- 💰 **Custo médio por demanda:** Meta <$0.001
- ✅ **Taxa de sucesso:** Meta >95%
- 🔄 **Fallback para Sonnet:** Meta <15%

### Reportar Mensalmente

- Total de demandas processadas
- Tempo total economizado
- Custo total de IA
- Problemas encontrados

---

**Última atualização:** 30/01/2026
**Versão do sistema:** 1.0.0
**Mantido por:** Coordenador do Setor de Orçamentos

# Exemplos de Uso do CLI

Este documento demonstra casos de uso reais do CLI.

---

## 🎯 Cenário 1: Processar Demanda Nova

**Situação:** Chegou email de cliente solicitando orçamento. Pasta `26_062` foi criada no Drive.

### Opção 1: Pipeline Completo (Recomendado)

```bash
# Executar pipeline completo
python src/cli.py processar-pasta 26_062 --confirm -v

# Output esperado:
============================================================
📁 Processando pasta: 26_062
============================================================

🔍 Verificando pasta 26_062...
✓ Pasta encontrada: /path/to/drive/26_062_EMPRESA_SERVICO

📧 Buscando emails relacionados...
   Query: EMPRESA SERVICO
✓ Encontrados 3 emails
   1. Solicitação de orçamento - Climatização
   2. Re: Solicitação de orçamento - Climatização
   3. Dados complementares para orçamento

🧹 Preparando dados...
   Encontrados 2 arquivos
   Processando: email_principal.html
   Processando: dados_complementares.txt
✓ Dados preparados (2 arquivos)

🤖 Extraindo informações com IA...
✓ Extração concluída
   Modelo: haiku-4
   Tokens: 687
   Custo: $0.0004

📋 Resumo do orçamento:
   Cliente: Empresa ABC Ltda
   Local: São Paulo - SP
   Tipo: instalacao
   Prazo: 2026-02-15

   Criar tarefa no Asana? (s/n): s

📝 Criando tarefa no Asana...
✓ Tarefa criada: 1234567890123456
   URL: https://app.asana.com/0/1212920325558530/1234567890123456

📎 Anexando arquivos...
   Anexando: ORC_26_062_R00.pdf

============================================================
📊 Relatório de Processamento
============================================================
⏱️  Duração: 8.3s
📧 Emails encontrados: 3
📄 Arquivos processados: 2
🎯 Tokens usados: 687
💰 Custo total: $0.0004
✅ Tarefa criada: 1234567890123456
🔗 https://app.asana.com/0/1212920325558530/1234567890123456
============================================================

✅ Pipeline concluído com sucesso!
```

---

## 🧪 Cenário 2: Testar sem Criar Tarefa (Dry-Run)

**Situação:** Quer testar o sistema sem criar tarefa real no Asana.

```bash
python src/cli.py processar-pasta 26_062 --dry-run -v

# Output:
🔍 Modo DRY-RUN ativado - nenhuma alteração será feita

📁 Processando pasta: 26_062

🔍 Verificando pasta 26_062...
✓ Pasta encontrada

📧 Buscando emails relacionados...
   [DRY-RUN] Pulando busca de emails

🧹 Preparando dados...
✓ Dados preparados

🤖 Extraindo informações com IA...
   [DRY-RUN] Pulando extração

📝 Criando tarefa no Asana...
   [DRY-RUN] Tarefa não será criada

📊 Relatório de Processamento
⏱️  Duração: 2.1s
📧 Emails encontrados: 0
📄 Arquivos processados: 0
🎯 Tokens usados: 0
💰 Custo total: $0.0000

✅ Pipeline concluído com sucesso!
```

---

## 🔍 Cenário 3: Buscar Emails sobre Demanda

**Situação:** Quer encontrar todos os emails relacionados a uma demanda.

```bash
python src/cli.py buscar-emails 26_062

# Output:
📧 Buscando emails para: 26_062
   Query: EMPRESA SERVICO

✓ Encontrados 3 emails:

1. Solicitação de orçamento - Climatização
   De: joao@empresa.com
   Data: 2026-01-28
   ID: 18cf2b9e123456789

2. Re: Solicitação de orçamento - Climatização
   De: maria@empresa.com
   Data: 2026-01-29
   ID: 18cf3a8f987654321

3. Dados complementares para orçamento
   De: joao@empresa.com
   Data: 2026-01-30
   ID: 18cf4b7g456789123
```

### Com Query Customizada

```bash
python src/cli.py buscar-emails 26_062 --query "urgente climatização JBS"

# Útil quando o nome da pasta não reflete bem o conteúdo
```

---

## 🧹 Cenário 4: Preparar Dados Manualmente

**Situação:** Tem emails brutos e quer limpá-los antes de processar.

### Arquivo Único

```bash
python src/cli.py preparar-dados email_bruto.html -o preparado.md

# Output:
🧹 Preparando dados: email_bruto.html

✓ Arquivo processado:
   Tokens: 3458 → 712
   Redução: 79.4%
   Salvo em: preparado.md
```

### Pasta Inteira

```bash
python src/cli.py preparar-dados pasta/26_062/emails

# Output:
🧹 Preparando dados: pasta/26_062/emails

✓ Pasta processada:
   Arquivos: 5
   Output: pasta/26_062/emails/dados_consolidados.md
   Redução média: 67.8%
```

---

## 🤖 Cenário 5: Extrair Dados com IA

**Situação:** Tem dados preparados e quer extrair informações estruturadas.

### Extração Padrão (Haiku)

```bash
python src/cli.py extrair-dados preparado.md -o orcamento.json

# Output:
🤖 Extraindo dados: preparado.md

✓ Extração concluída:
   Modelo: haiku-4
   Tokens: 712
   Custo: $0.0004
   Salvo em: orcamento.json
```

### Forçar Sonnet (Casos Complexos)

```bash
python src/cli.py extrair-dados preparado.md --sonnet -o orcamento.json

# Output:
🤖 Extraindo dados: preparado.md

✓ Extração concluída:
   Modelo: sonnet-4.5
   Tokens: 745
   Custo: $0.0115
   Salvo em: orcamento.json
```

### Ver Resultado no Terminal

```bash
python src/cli.py extrair-dados preparado.md

# Output (JSON no terminal):
📋 Dados extraídos:
{
  "cliente": "Empresa ABC Ltda",
  "cnpj_cpf": "12.345.678/0001-90",
  "contato": "João Silva",
  "telefone": "(11) 98765-4321",
  "email": "joao@abc.com",
  "local": "São Paulo - SP",
  "prazo": "2026-02-15",
  "tipo_servico": "instalacao",
  "eh_licitacao": false,
  "numero_edital": null,
  "porte": "medio",
  "origem": "comercial",
  "urgente": false,
  "cliente_estrategico": false,
  "descricao": "Instalação de sistema split 18.000 BTUs"
}
```

---

## 📝 Cenário 6: Criar Tarefa no Asana

**Situação:** Já tem JSON pronto e quer criar tarefa.

```bash
python src/cli.py criar-tarefa orcamento.json

# Output:
📝 Criando tarefa: orcamento.json

✓ Tarefa criada: 1234567890123456
🔗 https://app.asana.com/0/1212920325558530/1234567890123456
```

**O que é criado:**
- 1 tarefa principal: `26_XXX [INSTALACAO] Empresa ABC - São Paulo - SP`
- 7 subtarefas:
  1. 🔍 Triagem
  2. ✅ Aprovação para Elaboração
  3. 📝 Elaboração do Orçamento
  4. 🔎 Revisão Interna
  5. 📤 Envio ao Cliente
  6. 🤝 Negociação
  7. 🏁 Fechamento
- Tags: `instalacao`, `medio`
- Descrição formatada com todos os dados

---

## 🔧 Cenário 7: Debugging e Troubleshooting

### Ver Logs Detalhados

```bash
python src/cli.py processar-pasta 26_062 -v

# Mostra:
# - Detalhes de cada etapa
# - Erros completos com stack trace
# - Estatísticas de redução de tokens
# - Tempo de cada operação
```

### Testar Query de Email

```bash
python src/cli.py buscar-emails 26_062 --query "teste" -v

# Testa se a query retorna os emails esperados
```

### Validar Preparação

```bash
python src/cli.py preparar-dados email.html -o teste.md -v

# Ver quanto de redução conseguiu
```

---

## 📊 Cenário 8: Pipeline com Custos

**Situação:** Processar múltiplas demandas e rastrear custos.

```bash
# Processar 10 demandas
for id in 26_062 26_063 26_064 26_065 26_066 26_067 26_068 26_069 26_070 26_071; do
    echo "Processando $id..."
    python src/cli.py processar-pasta $id --confirm
    echo ""
done

# Custo esperado: 10 × $0.0004 = $0.004 (Haiku)
# Tempo esperado: 10 × 8s = 80s (~1.3 min)
```

---

## 🎓 Cenário 9: Workflow Típico Diário

**Situação:** Rotina diária de processamento de demandas.

```bash
# 1. Verificar emails novos
python src/cli.py buscar-emails HOJE --query "orçamento after:$(date -d yesterday +%Y/%m/%d)"

# 2. Para cada demanda nova, processar
python src/cli.py processar-pasta 26_XXX --confirm

# 3. Se incerto, usar dry-run primeiro
python src/cli.py processar-pasta 26_XXX --dry-run

# 4. Revisar tarefas criadas no Asana
# Acesse: https://app.asana.com/0/1212920325558530
```

---

## 💡 Dicas

### Quando usar `--confirm`
✅ **Use** quando quiser revisar antes de criar
❌ **Não use** em scripts automáticos

### Quando usar `--dry-run`
✅ **Use** para testar fluxo
✅ **Use** quando não tem certeza dos dados
❌ **Não use** em produção

### Quando usar `--sonnet`
✅ **Use** para licitações complexas
✅ **Use** quando Haiku falhou
❌ **Não use** por padrão (12x mais caro)

### Quando usar `-v` (verbose)
✅ **Use** para debugging
✅ **Use** para entender o que está acontecendo
❌ **Não use** em logs de produção (muito verboso)

---

## 📈 Métricas Esperadas

| Métrica | Valor Típico |
|---------|-------------|
| **Duração total** | 5-10s |
| **Emails encontrados** | 1-5 |
| **Arquivos processados** | 1-3 |
| **Tokens usados** | 500-1000 |
| **Custo por demanda** | $0.0004-0.0015 |
| **Taxa de sucesso Haiku** | 85-90% |
| **Taxa de fallback Sonnet** | 10-15% |

---

## 🆘 Troubleshooting

### Erro: "Pasta não encontrada"
```bash
# Verifique o caminho do Drive
ls ~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared\ drives/02Orcamentos/2026/

# Ou continue sem pasta (busca só emails)
python src/cli.py processar-pasta 26_062 --query "cliente xyz"
```

### Erro: "Gmail authentication failed"
```bash
# Re-autentique
python src/gmail_client.py --setup

# Teste conexão
python src/gmail_client.py --test
```

### Erro: "ModuleNotFoundError"
```bash
# Instale dependências
pip install -r requirements.txt

# Verifique ambiente virtual
which python
```

### Custo muito alto
```bash
# Verifique se está usando Haiku (padrão)
python src/cli.py processar-pasta 26_062 -v | grep "Modelo:"

# Deve mostrar: "Modelo: haiku-4"
# Se mostrar "sonnet", investigue por quê
```

---

**Última atualização:** 30/01/2026

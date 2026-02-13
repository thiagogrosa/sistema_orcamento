# Configuração MCP Gmail para Gemini CLI

## 📋 Passo a Passo

### 1. Criar Credenciais no Google Cloud Console

1. **Acesse:** https://console.cloud.google.com/
2. **Crie ou selecione um projeto** (ex: "Armant Orçamentos MCP")
3. **Habilite a Gmail API:**
   - Vá em "APIs & Services" > "Library"
   - Busque "Gmail API"
   - Clique em "Enable"

4. **Crie credenciais OAuth 2.0:**
   - Vá em "APIs & Services" > "Credentials"
   - Clique em "+ CREATE CREDENTIALS"
   - Selecione "OAuth client ID"
   - Tipo: **"Desktop app"** (para stdio/local)
   - Nome: "Gemini CLI Gmail MCP"
   - Clique em "Create"

5. **Copie as credenciais:**
   - Client ID: (ex: xxxxx.apps.googleusercontent.com)
   - Client Secret: (ex: GOCSPX-xxxxx)

6. **Configure OAuth consent screen:**
   - User Type: "External"
   - App name: "Gemini CLI Gmail"
   - User support email: seu email
   - Developer contact: seu email

7. **Adicione escopos OAuth2:**
   - Vá em "OAuth consent screen" > "Edit App"
   - "Add or Remove Scopes"
   - Adicione os seguintes escopos:

   **Escopos de Identificação (obrigatórios):**
   - `openid`
   - `https://www.googleapis.com/auth/userinfo.profile`
   - `https://www.googleapis.com/auth/userinfo.email`

   **Escopo do Gmail (escolha UM):**
   - ✅ **RECOMENDADO:** `https://www.googleapis.com/auth/gmail.modify`
     - Permite: Ler, escrever, enviar emails
     - NÃO permite: Excluir permanentemente
     - **Use este para segurança**

   - ⚠️ **NÃO RECOMENDADO:** `https://mail.google.com/`
     - Permite: Ler, escrever, enviar E EXCLUIR permanentemente
     - Muito permissivo para sistema de orçamentos

   - Salve

8. **Adicione usuários de teste:**
   - Em "Test users", clique em "+ ADD USERS"
   - Adicione: `orcamentos2@armant.com.br`
   - Salve

---

## 🔒 Entendendo os Escopos OAuth2

### Por que usar `gmail.modify` em vez de `mail.google.com`?

**Princípio de Menor Privilégio:**
Conceda apenas as permissões necessárias para o sistema funcionar.

| O que precisamos fazer | Escopo Necessário |
|------------------------|-------------------|
| ✅ Buscar emails | `gmail.modify` ou `mail.google.com` |
| ✅ Ler conteúdo | `gmail.modify` ou `mail.google.com` |
| ✅ Marcar como lido | `gmail.modify` ou `mail.google.com` |
| ✅ Adicionar labels | `gmail.modify` ou `mail.google.com` |
| ✅ Enviar emails | `gmail.modify` ou `mail.google.com` |
| ❌ Excluir permanentemente | Apenas `mail.google.com` |

**Conclusão:** `gmail.modify` atende 100% das necessidades sem o risco de exclusão acidental.

### Proteção Adicional

Com `gmail.modify`:
- ✅ Mesmo se houver um bug no código, emails não podem ser excluídos
- ✅ Proteção contra comandos maliciosos
- ✅ Conformidade com boas práticas de segurança
- ✅ Auditoria mais simples (sem ações destrutivas)

---

### 2. Configurar Variáveis de Ambiente

Crie ou edite o arquivo `~/.zshrc` (ou `~/.bashrc`):

```bash
# MCP Gmail Credentials
export GOOGLE_CLIENT_ID="seu-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="GOCSPX-seu-client-secret"
```

Depois, recarregue:
```bash
source ~/.zshrc
```

---

### 3. Adicionar MCP ao Gemini CLI

Execute:

```bash
gemini mcp add gmail npx -y @mcp-z/mcp-gmail
```

Verifique:
```bash
gemini mcp list
```

---

### 4. Testar Conexão

Execute o Gemini CLI:

```bash
gemini -p "Liste os últimos 5 emails da minha caixa de entrada"
```

**Na primeira execução:**
1. O browser abrirá automaticamente
2. Faça login com `orcamentos2@armant.com.br`
3. Autorize o acesso ao Gmail
4. O token será salvo automaticamente

---

## 🔧 Comandos Úteis

### Gerenciar MCP
```bash
# Listar MCPs
gemini mcp list

# Desabilitar MCP
gemini mcp disable gmail

# Habilitar MCP
gemini mcp enable gmail

# Remover MCP
gemini mcp remove gmail
```

### Usar Gemini CLI

**Modo interativo:**
```bash
gemini
```

**Modo prompt (headless):**
```bash
gemini -p "sua pergunta aqui"
```

**Com arquivo de contexto:**
```bash
cat pesquisa-gemini.md | gemini -p "Execute a tarefa descrita"
```

**YOLO mode (aceita tudo automaticamente):**
```bash
gemini -y -p "sua pergunta aqui"
```

---

## 🚀 Integração com Claude Code

### Opção 1: Via Bash Tool

O Claude Code pode chamar o Gemini CLI diretamente:

```bash
gemini -p "Busque no Gmail emails sobre Porto Seguro PMOC nos últimos 60 dias"
```

### Opção 2: Com arquivo de contexto

```bash
cat /caminho/pesquisa-gemini.md | gemini -p "Execute esta busca e retorne os resultados"
```

### Opção 3: Salvar resultado em arquivo

```bash
gemini -p "Busque info sobre Porto Seguro PMOC" > /tmp/resultado-gemini.txt
```

---

## 📝 Exemplo de Uso Completo

```bash
# 1. Criar prompt
cat > /tmp/busca-gmail.txt << 'EOF'
Busque no Gmail (orcamentos2@armant.com.br) emails sobre:
- Porto Seguro PMOC
- Período: Janeiro-Fevereiro 2026
- Retorne: contato, email, telefone, CNPJ, escopo
EOF

# 2. Executar busca
gemini -p "$(cat /tmp/busca-gmail.txt)"

# 3. Salvar resultado
gemini -p "$(cat /tmp/busca-gmail.txt)" > /tmp/resultado.txt
```

---

## ⚠️ Solução de Problemas

### Erro: "OAuth2 credentials not found"
- Verifique se as variáveis de ambiente estão configuradas:
  ```bash
  echo $GOOGLE_CLIENT_ID
  echo $GOOGLE_CLIENT_SECRET
  ```

### Erro: "Gmail API not enabled"
- Habilite a Gmail API no Google Cloud Console

### Erro: "Access blocked: This app's request is invalid"
- Adicione o email aos "Test users" no OAuth consent screen

### Erro: "Requested scopes don't match configured scopes"
- Verifique se adicionou todos os escopos corretos:
  - `openid`
  - `https://www.googleapis.com/auth/userinfo.profile`
  - `https://www.googleapis.com/auth/userinfo.email`
  - `https://www.googleapis.com/auth/gmail.modify` (NÃO use `mail.google.com`)

### Erro: "Insufficient permission" ao tentar excluir email
- **Isso é esperado!** O escopo `gmail.modify` não permite exclusão
- Isso é uma **proteção de segurança**
- Se realmente precisar excluir (não recomendado), use `mail.google.com`

### Token expirado
- Delete o token e refaça o OAuth:
  ```bash
  rm ~/.gemini/tokens/*
  gemini -p "teste"
  ```

### Mudou os escopos depois de configurar?
- Revogue o token atual e re-autentique:
  ```bash
  # 1. Revogue na Google Account
  # https://myaccount.google.com/permissions

  # 2. Delete tokens locais
  rm -rf ~/.gemini/tokens/

  # 3. Re-autentique
  gemini -p "teste"
  ```

---

## 📚 Recursos

- Documentação MCP Gmail: https://mcp-z.github.io/mcp-gmail
- Google Cloud Console: https://console.cloud.google.com/
- Gemini CLI Docs: (documentação oficial)

# Setup Gmail API - Guia Completo

Este guia mostra como configurar o acesso à Gmail API usando OAuth 2.0.

---

## 📋 Pré-requisitos

- Conta Google (de preferência a conta de trabalho: orcamentos2@armant.com.br)
- Acesso ao [Google Cloud Console](https://console.cloud.google.com)
- Python 3.10+ instalado

---

## 🔧 Passo 1: Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com
2. Clique em **"Select a project"** (topo da página)
3. Clique em **"New Project"**
4. Configure:
   - **Project name:** `Gestão Orçamentos Armant`
   - **Organization:** (deixe padrão)
5. Clique em **"Create"**
6. Aguarde a criação (leva ~30 segundos)

---

## 🔓 Passo 2: Habilitar Gmail API

1. No menu lateral, vá em: **APIs & Services** > **Library**
2. Busque por: `Gmail API`
3. Clique no resultado **Gmail API**
4. Clique em **"Enable"**
5. Aguarde ativação

---

## 🔑 Passo 3: Configurar OAuth Consent Screen

Antes de criar credenciais, é necessário configurar a tela de consentimento:

1. No menu lateral: **APIs & Services** > **OAuth consent screen**
2. Escolha: **External** (se não for Google Workspace) ou **Internal** (se for)
3. Clique em **"Create"**

### Configurar App Registration

**Página 1 - App information:**
- **App name:** `Gestão de Orçamentos`
- **User support email:** `orcamentos2@armant.com.br` (ou seu email)
- **App logo:** (opcional)
- **Application home page:** (deixe vazio)
- **Application privacy policy:** (deixe vazio)
- **Application terms of service:** (deixe vazio)
- **Authorized domains:** (deixe vazio)
- **Developer contact:** `orcamentos2@armant.com.br`

Clique em **"Save and Continue"**

**Página 2 - Scopes:**
- Clique em **"Add or Remove Scopes"**
- Busque e selecione:
  - `https://www.googleapis.com/auth/gmail.readonly`
  - `https://www.googleapis.com/auth/gmail.modify`
- Clique em **"Update"**
- Clique em **"Save and Continue"**

**Página 3 - Test users:**
- Clique em **"Add Users"**
- Adicione: `orcamentos2@armant.com.br` (ou o email que vai usar)
- Clique em **"Add"**
- Clique em **"Save and Continue"**

**Página 4 - Summary:**
- Revise as informações
- Clique em **"Back to Dashboard"**

---

## 🎫 Passo 4: Criar Credenciais OAuth 2.0

1. No menu lateral: **APIs & Services** > **Credentials**
2. Clique em **"+ Create Credentials"** (topo da página)
3. Selecione: **OAuth client ID**
4. Configure:
   - **Application type:** `Desktop app`
   - **Name:** `Gmail Client - Desktop`
5. Clique em **"Create"**

### Baixar Credenciais

1. Aparecerá um popup com as credenciais criadas
2. Clique em **"Download JSON"**
3. Salve o arquivo como `credentials.json`

---

## 📁 Passo 5: Copiar Credenciais para o Projeto

```bash
# Copiar arquivo baixado para a pasta config/
cp ~/Downloads/credentials.json gestao-orcamentos/config/gmail_credentials.json

# Verificar se arquivo existe
ls -l gestao-orcamentos/config/gmail_credentials.json
```

**IMPORTANTE:** Nunca commite este arquivo no git! Ele já está no `.gitignore`.

---

## 🚀 Passo 6: Executar Autenticação

Agora que tudo está configurado, execute o script de autenticação:

```bash
cd gestao-orcamentos

# Ativar ambiente virtual (se estiver usando)
source venv/bin/activate

# Executar setup
python src/gmail_client.py --setup
```

### O que vai acontecer:

1. O script vai abrir seu navegador
2. Você verá a tela de login do Google
3. Faça login com a conta: `orcamentos2@armant.com.br`
4. Aparecerá um aviso: **"Google hasn't verified this app"**
   - Clique em **"Advanced"** (ou "Avançado")
   - Clique em **"Go to Gestão de Orçamentos (unsafe)"**
   - Isso é normal para apps em desenvolvimento!
5. Revise as permissões solicitadas:
   - ✓ Read, compose, send, and permanently delete all your email from Gmail
   - ✓ See, edit, create, and delete all of your Google Drive files
6. Clique em **"Continue"** (ou "Continuar")
7. Você verá: **"The authentication flow has completed."**
8. Volte para o terminal

### No terminal você verá:

```
======================================================================
SETUP - Autenticação Gmail API
======================================================================

O navegador será aberto para você autorizar o acesso.
Após autorizar, volte para este terminal.

2026-01-30 15:30:00 - gmail_client - INFO - Iniciando fluxo de autenticação OAuth...
2026-01-30 15:30:15 - gmail_client - INFO - Autenticação concluída com sucesso
2026-01-30 15:30:15 - gmail_client - INFO - Salvando token em config/gmail_token.pickle

✓ Autenticação concluída com sucesso!
✓ Token salvo em: config/gmail_token.pickle

Você pode agora usar o cliente normalmente.
```

---

## ✅ Passo 7: Testar Conexão

Teste se tudo está funcionando:

```bash
# Buscar últimos 5 emails
python src/gmail_client.py --test

# Buscar emails específicos
python src/gmail_client.py --test --query "from:cliente@empresa.com"
```

### Output esperado:

```
======================================================================
TESTE - Busca de Emails
======================================================================

Buscando emails com query: is:inbox
2026-01-30 15:35:00 - gmail_client - INFO - Buscando emails: query='is:inbox', max=5
2026-01-30 15:35:02 - gmail_client - INFO - Encontrados 5 emails

✓ Encontrados 5 emails:

1. Orçamento climatização sala
   De: João Silva <joao@empresa.com>
   Data: Thu, 25 Jan 2026 14:30:00 -0300
   Snippet: Prezados, gostaria de solicitar um orçamento para instalação...

2. Re: Proposta 26_004
   De: Maria Santos <maria@jbs.com.br>
   Data: Wed, 24 Jan 2026 09:15:00 -0300
   Snippet: Boa tarde, conseguimos aprovar internamente...

[...]
```

---

## 🔄 Renovação Automática de Token

O token de acesso expira após algumas horas, mas o sistema renova automaticamente usando o **refresh token**.

**Você só precisa fazer login manual:**
- Na primeira vez (setup)
- Se deletar o arquivo `config/gmail_token.pickle`
- Se revogar acesso no Google (configurações de segurança)

---

## ❓ Troubleshooting

### Erro: "File not found: config/gmail_credentials.json"

**Causa:** Arquivo de credenciais não foi copiado para a pasta correta

**Solução:**
```bash
# Verificar se arquivo existe
ls config/gmail_credentials.json

# Se não existe, copiar do Downloads
cp ~/Downloads/credentials.json config/gmail_credentials.json
```

---

### Erro: "invalid_grant" durante autenticação

**Causa:** Token expirado ou inválido

**Solução:**
```bash
# Deletar token e refazer autenticação
rm config/gmail_token.pickle
python src/gmail_client.py --setup
```

---

### Erro: "Access blocked: This app's request is invalid"

**Causa:** Scopes incorretos ou app não verificado

**Solução:**
1. Vá em: https://console.cloud.google.com
2. **APIs & Services** > **OAuth consent screen**
3. Verifique se os scopes estão corretos
4. Adicione seu email em **Test users**
5. Tente novamente

---

### Erro: "Quota exceeded" durante uso

**Causa:** Limite de requisições da API excedido

**Solução:**
- Gmail API Free Tier: 1 bilhão requisições/dia (difícil exceder)
- Se exceder, aguarde 24h ou considere aumentar quota
- Verifique em: https://console.cloud.google.com/apis/api/gmail.googleapis.com/quotas

---

### Como revogar acesso manualmente?

Se quiser remover o acesso concedido:

1. Acesse: https://myaccount.google.com/permissions
2. Encontre: **Gestão de Orçamentos**
3. Clique em **"Remove Access"**
4. Para autenticar novamente:
   ```bash
   rm config/gmail_token.pickle
   python src/gmail_client.py --setup
   ```

---

## 🔐 Segurança

### Boas Práticas

✅ **SIM:**
- Manter `gmail_credentials.json` fora do git (já está no `.gitignore`)
- Manter `gmail_token.pickle` fora do git (já está no `.gitignore`)
- Usar apenas os scopes necessários
- Renovar credenciais a cada 6 meses

❌ **NÃO:**
- Compartilhar arquivo `credentials.json` publicamente
- Commitar credenciais no git
- Usar credenciais de produção em ambiente de desenvolvimento
- Dar acesso `gmail.modify` se só precisa ler (`gmail.readonly`)

### Scopes Usados

| Scope | Permissão | Usado Para |
|-------|-----------|------------|
| `gmail.readonly` | Ler emails | Buscar e baixar emails |
| `gmail.modify` | Modificar (sem deletar) | Marcar emails como lidos |

**Nota:** Não usamos `gmail.compose` (enviar) ou `gmail.metadata` (apenas metadados) por segurança.

---

## 📚 Referências

- [Gmail API - Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [Gmail API - Reference](https://developers.google.com/gmail/api/reference/rest)
- [OAuth 2.0 Scopes](https://developers.google.com/gmail/api/auth/scopes)
- [Google Cloud Console](https://console.cloud.google.com)

---

## 🆘 Suporte

Se continuar com problemas após seguir este guia:

1. Verifique logs em `logs/gmail_client.log`
2. Execute com modo verbose: `python src/gmail_client.py --test --verbose`
3. Consulte: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Última atualização:** 30/01/2026

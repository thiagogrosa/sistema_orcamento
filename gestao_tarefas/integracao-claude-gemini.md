# Integração Claude Code + Gemini CLI + MCP Gmail

## 🔄 Fluxo de Trabalho

```
┌─────────────────┐
│   Claude Code   │
│                 │
│  1. Extrai PDFs │──┐
│  2. Identifica  │  │
│     info falta  │  │
└─────────────────┘  │
                     │
                     ▼
              ┌──────────────┐
              │ Gemini CLI   │
              │ + MCP Gmail  │
              │              │
              │ 3. Busca no  │
              │    Gmail     │
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │  Resultado   │
              │   (texto)    │
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Claude Code  │
              │              │
              │ 4. Atualiza  │
              │    Asana     │
              └──────────────┘
```

---

## 📝 Formas de Invocar o Gemini CLI

### 1️⃣ Diretamente via Bash Tool

```bash
gemini -p "Busque no Gmail emails sobre Porto Seguro PMOC"
```

### 2️⃣ Com arquivo de contexto

```bash
cat pesquisa-gemini.md | gemini -p "Execute a tarefa descrita"
```

### 3️⃣ Via script automatizado

```bash
./scripts/buscar-info-gmail.sh 26_060
```

### 4️⃣ Com Task Tool (agente)

Claude Code pode chamar um agente especializado que:
- Lê o `pesquisa-gemini.md`
- Executa o Gemini CLI
- Processa o resultado
- Atualiza o Asana

---

## 🚀 Exemplo Prático Completo

### Cenário: Buscar info da demanda 26_060 (Porto Seguro)

**1. Claude Code identifica que falta info:**
```
Demanda 26_060 - Porto Seguro PMOC
Status: Sem informações de contato
```

**2. Claude Code prepara o prompt:**
```bash
PROMPT="Busque no Gmail (orcamentos2@armant.com.br) emails sobre:
- Porto Seguro PMOC
- Palavras-chave: Porto Seguro, PMOC, manutenção, climatização
- Período: últimos 60 dias
- Extraia: Cliente, CNPJ, Contato, Telefone, Email, Endereço, Escopo"
```

**3. Claude Code executa Gemini CLI:**
```bash
gemini -p "$PROMPT" > /tmp/resultado-26_060.txt
```

**4. Claude Code lê o resultado:**
```bash
cat /tmp/resultado-26_060.txt
```

**5. Claude Code atualiza Asana:**
```python
# Usando MCP Asana
asana_update_task(
    task_id="1213131819149336",
    notes="Cliente: Porto Seguro...[info extraída]"
)
```

---

## 🎯 Comandos que o Claude Code Pode Usar

### Buscar info de uma demanda específica

```bash
gemini -p "Busque no Gmail emails sobre Porto Seguro PMOC nos últimos 60 dias. Extraia nome do contato, telefone, email, CNPJ e escopo da demanda."
```

### Buscar múltiplas demandas

```bash
# Via script
./scripts/buscar-info-gmail.sh

# Ou direto
cat pesquisa-gemini.md | gemini -p "Execute todas as buscas descritas"
```

### Buscar e salvar resultado

```bash
gemini -p "$(cat pesquisa-gemini.md)" > resultados-gmail/busca-$(date +%Y%m%d-%H%M%S).txt
```

### Modo YOLO (auto-aprova tudo)

```bash
gemini -y -p "Busque info sobre Porto Seguro"
```

---

## 📋 Checklist de Configuração

- [ ] 1. Criar projeto no Google Cloud Console
- [ ] 2. Habilitar Gmail API
- [ ] 3. Criar credenciais OAuth 2.0 (Desktop app)
- [ ] 4. Configurar OAuth consent screen
- [ ] 5. Adicionar escopos necessários
- [ ] 6. Adicionar orcamentos2@armant.com.br como usuário de teste
- [ ] 7. Configurar variáveis de ambiente (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
- [ ] 8. Adicionar MCP Gmail ao Gemini CLI: `gemini mcp add gmail npx -y @mcp-z/mcp-gmail`
- [ ] 9. Testar primeira execução (fazer OAuth)
- [ ] 10. Verificar que funciona: `gemini -p "Liste 5 emails"`

---

## 🔒 Segurança

**Variáveis de Ambiente:**
- Nunca commitar `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` no git
- Usar `.env` local ou variáveis de ambiente do sistema

**Tokens:**
- Tokens OAuth são salvos em `~/.gemini/tokens/`
- Não compartilhar tokens

**Conta de Email:**
- Usar conta específica do projeto (orcamentos2@armant.com.br)
- Não usar conta pessoal

---

## 📊 Vantagens desta Abordagem

| Característica | Chrome MCP | Gemini CLI + MCP Gmail |
|---|---|---|
| **Setup** | Complexo | Médio |
| **Confiabilidade** | Depende de UI | API estável |
| **Velocidade** | Lento | Rápido |
| **Automação** | Difícil | Fácil |
| **Login** | Manual cada vez | OAuth persistente |
| **Busca** | Limitada | Poderosa (API Gmail) |
| **Resultado** | Screenshot/HTML | Texto estruturado |

---

## 🎓 Exemplos de Prompts para Gemini

### Busca simples
```
"Liste os últimos 10 emails da caixa de entrada"
```

### Busca com filtro
```
"Busque emails de janeiro 2026 que contenham 'Porto Seguro' e 'PMOC'"
```

### Extração estruturada
```
"Busque emails sobre Colombo Park Shopping e extraia:
- Nome do remetente
- Email
- Telefone (se mencionado)
- Assunto
- Data
- Resumo do conteúdo"
```

### Múltiplas buscas
```
"Execute 2 buscas:
1. Emails sobre Porto Seguro PMOC
2. Emails sobre Colombo Park Shopping
Para cada um, extraia dados de contato"
```

---

## 🛠️ Troubleshooting

### Gemini CLI não encontra o MCP
```bash
# Verificar lista
gemini mcp list

# Re-adicionar
gemini mcp remove gmail
gemini mcp add gmail npx -y @mcp-z/mcp-gmail
```

### Erro de autenticação
```bash
# Limpar tokens e refazer OAuth
rm -rf ~/.gemini/tokens/
gemini -p "teste"
```

### MCP não carrega
```bash
# Verificar variáveis de ambiente
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_CLIENT_SECRET

# Recarregar shell
source ~/.zshrc
```

---

## 📚 Próximos Passos

1. ✅ Criar credenciais no Google Cloud
2. ✅ Configurar MCP Gmail no Gemini CLI
3. ✅ Testar busca manual
4. ⏳ Integrar com Claude Code via Bash
5. ⏳ Criar wrapper/script automatizado
6. ⏳ Testar fluxo completo (PDF → Gemini → Asana)

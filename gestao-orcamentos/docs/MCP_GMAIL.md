# Gmail MCP Server - Guia de Integração

Este servidor expõe a lógica do `GmailClient` local através do **Model Context Protocol (MCP)**, permitindo que IAs (como Claude Desktop ou Gemini) interajam diretamente com sua caixa de entrada de e-mails.

## 🚀 Instalação

O servidor utiliza a biblioteca `mcp` com o wrapper `FastMCP`. Para instalar as dependências necessárias:

```bash
pip install "mcp[cli]"
```

## 🛠️ Ferramentas Disponíveis

Ao conectar este servidor, a IA terá acesso às seguintes ferramentas:

1.  `search_emails(query, max_results)`: Busca e-mails usando a sintaxe nativa do Gmail.
2.  `read_email_content(email_id)`: Retorna o texto completo de um e-mail para análise da IA.
3.  `list_threads(query)`: Lista conversas agrupadas.
4.  `mark_as_read(email_id)`: Marca um e-mail como lido.

## ⚙️ Configuração no Claude Desktop

Para usar este servidor no Claude Desktop, adicione o seguinte ao seu arquivo `claude_desktop_config.json`:

### macOS
O arquivo geralmente fica em: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gmail-armant": {
      "command": "/Users/thiagorosa/dev/tools/armant/gestao-orcamentos/venv_mcp/bin/python3.14",
      "args": [
        "/Users/thiagorosa/dev/tools/armant/gestao-orcamentos/src/mcp_server_gmail.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/thiagorosa/dev/tools/armant/gestao-orcamentos"
      }
    }
  }
}
```

> **Nota:** Certifique-se de que o caminho (path) para o script está correto e que você já realizou o setup das credenciais do Gmail seguindo o `docs/SETUP_GMAIL_API.md`.

## 🧪 Testando Localmente

Você pode testar se o servidor está funcionando corretamente rodando o modo inspector do MCP:

```bash
npx @modelcontextprotocol/inspector python3 src/mcp_server_gmail.py
```

## 🔒 Segurança e Autenticação

Este servidor utiliza as mesmas credenciais configuradas em `config/gmail_credentials.json`. 
- Ele **não** expõe sua senha.
- Ele utiliza o token OAuth salvo em `config/gmail_token.pickle`.
- Se o token expirar, o servidor tentará renová-lo automaticamente ou solicitará uma nova autorização (que abrirá o navegador na primeira execução).

---
*Este MCP foi criado exclusivamente para o projeto Gestão de Orçamentos.*

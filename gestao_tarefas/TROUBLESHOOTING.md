# Troubleshooting - Sistema de Gestão de Orçamentos

**Versão:** 1.0.0
**Última atualização:** 30/01/2026

---

## 📋 Índice

1. [Problemas de Instalação](#problemas-de-instalação)
2. [Erros de Autenticação](#erros-de-autenticação)
3. [Erros de Processamento](#erros-de-processamento)
4. [Problemas de Performance](#problemas-de-performance)
5. [Erros de API](#erros-de-api)
6. [Problemas de Dados](#problemas-de-dados)
7. [Problemas de Integração](#problemas-de-integração)

---

## 🔧 Problemas de Instalação

### ❌ `python: command not found`

**Erro:**
```bash
$ python src/cli.py
bash: python: command not found
```

**Causa:** Python não instalado ou comando é `python3`

**Solução:**
```bash
# Verificar se Python está instalado
python3 --version

# Usar python3 em vez de python
python3 src/cli.py processar-pasta 26_062

# Ou criar alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

---

### ❌ `ModuleNotFoundError: No module named 'anthropic'`

**Erro:**
```python
ModuleNotFoundError: No module named 'anthropic'
```

**Causa:** Dependências não instaladas ou ambiente virtual não ativado

**Solução:**
```bash
# 1. Verificar se ambiente virtual está ativado
which python
# Deve mostrar: /path/to/venv/bin/python

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Verificar instalação
pip list | grep anthropic
```

---

### ❌ `pip: command not found`

**Erro:**
```bash
$ pip install -r requirements.txt
bash: pip: command not found
```

**Causa:** pip não instalado

**Solução:**
```bash
# macOS
python3 -m ensurepip --upgrade

# Ubuntu/Debian
sudo apt-get install python3-pip

# Usar python3 -m pip
python3 -m pip install -r requirements.txt
```

---

### ❌ Erro de permissão ao instalar pacotes

**Erro:**
```
PermissionError: [Errno 13] Permission denied
```

**Causa:** Tentando instalar sem ambiente virtual ou sem permissões

**Solução:**
```bash
# NUNCA use sudo pip install
# Sempre usar ambiente virtual

# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar
source venv/bin/activate

# 3. Instalar
pip install -r requirements.txt
```

---

## 🔐 Erros de Autenticação

### ❌ Gmail: `invalid_grant`

**Erro:**
```
google.auth.exceptions.RefreshError: invalid_grant: Token has been expired or revoked
```

**Causa:** Token OAuth expirado ou revocado

**Solução:**
```bash
# 1. Deletar token antigo
rm config/gmail_token.json

# 2. Re-autenticar
python src/gmail_client.py --setup

# 3. Seguir instruções no navegador

# 4. Testar
python src/gmail_client.py --test
```

**Se persistir:**
1. Ir ao Google Cloud Console
2. APIs & Services > Credentials
3. Deletar credencial antiga
4. Criar nova credencial OAuth 2.0
5. Baixar novo `credentials.json`
6. Copiar para `config/gmail_credentials.json`
7. Re-autenticar

---

### ❌ Gmail: `403 Forbidden - Access Not Granted`

**Erro:**
```
googleapiclient.errors.HttpError: 403 Access Not Granted
```

**Causa:** Gmail API não habilitada ou credenciais incorretas

**Solução:**
```bash
# 1. Verificar se Gmail API está habilitada
# Google Cloud Console > APIs & Services > Library
# Buscar "Gmail API" > Habilitar

# 2. Verificar se credenciais são do projeto correto
# credentials.json deve ser do mesmo projeto onde API está habilitada

# 3. Re-autenticar
python src/gmail_client.py --setup
```

---

### ❌ Anthropic: `authentication_error`

**Erro:**
```
anthropic.APIError: authentication_error: Invalid API key
```

**Causa:** API key inválida ou não configurada

**Solução:**
```bash
# 1. Verificar se .env existe
ls -la .env

# 2. Ver conteúdo (sem expor key)
grep ANTHROPIC_API_KEY .env
# Deve mostrar: ANTHROPIC_API_KEY=sk-ant-...

# 3. Se não existe, criar
cp .env.example .env

# 4. Editar e adicionar key válida
nano .env
# ANTHROPIC_API_KEY=sk-ant-api03-sua-key-aqui

# 5. Testar
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OK' if os.getenv('ANTHROPIC_API_KEY') else 'ERRO')"
```

**Como obter API key:**
1. Acessar: https://console.anthropic.com/
2. Settings > API Keys
3. Create Key
4. Copiar e adicionar ao `.env`

---

### ❌ Asana: `Invalid token`

**Erro:**
```
asana.error.InvalidTokenError: Invalid token
```

**Causa:** Token expirado ou inválido

**Solução:**
```bash
# 1. Gerar novo token
# https://app.asana.com/0/my-apps

# 2. Atualizar .env
nano .env
# ASANA_ACCESS_TOKEN=0/seu-novo-token

# 3. Testar
python -c "from src.asana_lib import AsanaLib; a = AsanaLib(); print('OK')"
```

---

## 🔄 Erros de Processamento

### ❌ "Pasta não encontrada"

**Erro:**
```
⚠️  Pasta 26_062 não encontrada no Drive
```

**Causa:** Pasta não existe ou caminho incorreto

**Solução:**

**Opção 1 - Verificar se pasta existe:**
```bash
# Verificar no Drive
ls ~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared\ drives/02Orcamentos/2026/ | grep 26_062

# Se não encontrou, listar todas
ls ~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared\ drives/02Orcamentos/2026/
```

**Opção 2 - Criar pasta:**
```bash
# Criar pasta no Drive
mkdir -p ~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared\ drives/02Orcamentos/2026/26_062_CLIENTE_SERVICO
```

**Opção 3 - Processar sem pasta:**
```bash
# Usar query específica
python src/cli.py processar-pasta 26_062 --query "cliente nome projeto"
```

---

### ❌ "No emails found"

**Erro:**
```
📧 Nenhum email encontrado com a query atual
```

**Causa:** Query não encontrou emails ou emails não existem

**Solução:**

**1. Testar query diferente:**
```bash
# Query mais específica
python src/cli.py buscar-emails 26_062 --query "cliente@email.com"

# Query mais ampla
python src/cli.py buscar-emails 26_062 --query "orçamento"

# Por data
python src/cli.py buscar-emails 26_062 --query "after:2026/01/25"
```

**2. Verificar no Gmail manualmente:**
- Abrir Gmail: orcamentos2@armant.com.br
- Buscar por cliente/projeto
- Se encontrou, usar termos exatos da busca na query

**3. Processar com dados manuais:**
- Criar JSON manualmente
- Usar: `python src/cli.py criar-tarefa dados.json`

---

### ❌ "Validation failed" (extração IA)

**Erro:**
```
⚠️ Não foi possível extrair todos os dados automaticamente

Dados faltantes:
- local
- tipo_servico
```

**Causa:** IA não conseguiu extrair campos obrigatórios

**Solução:**

**O sistema tenta Sonnet automaticamente**, mas se falhar:

**1. Forçar Sonnet desde o início:**
```bash
python src/cli.py processar-pasta 26_062 --sonnet --confirm
```

**2. Extrair manualmente e revisar:**
```bash
# Preparar dados
python src/cli.py preparar-dados pasta/26_062/emails -o preparado.md

# Ver dados preparados
cat preparado.md

# Extrair
python src/cli.py extrair-dados preparado.md -o orcamento.json

# Revisar e editar JSON
nano orcamento.json
# Completar campos faltantes

# Criar tarefa
python src/cli.py criar-tarefa orcamento.json
```

**3. Melhorar dados de entrada:**
- Adicionar mais contexto nos emails
- Consolidar informações em um único documento
- Usar formato mais estruturado

---

### ❌ "JSONDecodeError"

**Erro:**
```python
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Causa:** IA retornou resposta mal formatada

**Solução:**

**1. Ver resposta bruta:**
```bash
python src/cli.py extrair-dados preparado.md -v 2>&1 | grep "Resposta"
```

**2. Tentar com Sonnet:**
```bash
python src/cli.py extrair-dados preparado.md --sonnet -o orcamento.json
```

**3. Se persistir, reportar bug:**
- Salvar `preparado.md`
- Salvar output completo
- Enviar para desenvolvedor

---

## ⚡ Problemas de Performance

### ❌ Processamento muito lento (> 30s)

**Sintomas:**
```
⏱️  Duração: 45.2s  ← Muito lento!
```

**Causas possíveis:**

**1. Rede lenta:**
```bash
# Testar velocidade
curl -o /dev/null https://api.anthropic.com

# Verificar latência
ping api.anthropic.com
```

**2. Muitos arquivos para processar:**
```bash
# Ver quantos arquivos
ls pasta/26_062/emails/*.html | wc -l

# Se > 10, limitar
python src/cli.py preparar-dados pasta/26_062/emails
# Editar prepare_data.py e limitar a 5 arquivos
```

**3. API rate limit:**
```bash
# Ver se está sendo throttled
python src/cli.py processar-pasta 26_062 -v 2>&1 | grep -i "rate"
```

**Solução:**
- Usar arquivos menores
- Processar fora de horário de pico
- Aguardar alguns minutos e tentar novamente

---

### ❌ Uso alto de memória

**Sintomas:**
- Sistema lento
- Python usando muita RAM

**Solução:**
```bash
# 1. Limitar tamanho de arquivos
# No prepare_data.py, adicionar limite:

def preparar_pasta(self, pasta_path: str) -> Dict:
    arquivos = list(Path(pasta_path).rglob("*.html"))
    # Limitar a 5 arquivos
    arquivos = arquivos[:5]
    # ...

# 2. Processar em lotes
for id in 26_062 26_063 26_064; do
    python src/cli.py processar-pasta $id
    sleep 5  # Pausa entre processos
done
```

---

## 🌐 Erros de API

### ❌ Anthropic: `rate_limit_error`

**Erro:**
```
anthropic.RateLimitError: Rate limit exceeded
```

**Causa:** Muitas requisições em pouco tempo

**Solução:**
```bash
# 1. Aguardar alguns minutos

# 2. Processar com delay entre operações
python src/cli.py processar-pasta 26_062
sleep 60  # 1 minuto
python src/cli.py processar-pasta 26_063

# 3. Verificar tier da conta
# https://console.anthropic.com/settings/limits
```

**Limites típicos:**
- Free tier: 5 RPM (requisições por minuto)
- Tier 1: 50 RPM
- Tier 2: 1000 RPM

---

### ❌ Gmail: `429 Too Many Requests`

**Erro:**
```
googleapiclient.errors.HttpError: 429 Quota exceeded
```

**Causa:** Cota da Gmail API excedida

**Solução:**
```bash
# 1. Verificar cota no Google Cloud Console
# APIs & Services > Gmail API > Quotas

# 2. Aguardar reset (diário ou por minuto)

# 3. Otimizar queries
python src/cli.py buscar-emails 26_062 --max-results 5
# Em vez de padrão 10

# 4. Solicitar aumento de cota (se necessário)
# Google Cloud Console > Quotas > Request Increase
```

---

### ❌ Network timeout

**Erro:**
```
requests.exceptions.Timeout: Request timed out
```

**Causa:** Conexão lenta ou API indisponível

**Solução:**
```bash
# 1. Verificar internet
ping 8.8.8.8

# 2. Verificar status das APIs
# https://status.anthropic.com
# https://status.cloud.google.com

# 3. Tentar novamente com timeout maior
# Editar código e aumentar timeout:
# client = Anthropic(timeout=120)  # 2 minutos

# 4. Usar retry automático
# Sistema já tem retry built-in, aguardar
```

---

## 📊 Problemas de Dados

### ❌ Caracteres estranhos no output

**Problema:**
```
Cliente: Empresa Ã‰tica Ltda  ← Deveria ser "Ética"
```

**Causa:** Encoding incorreto

**Solução:**
```bash
# 1. Verificar encoding do arquivo
file -I arquivo.html
# Deve mostrar: charset=utf-8

# 2. Converter se necessário
iconv -f ISO-8859-1 -t UTF-8 arquivo.html > arquivo_utf8.html

# 3. Usar UTF-8 ao salvar
# Python faz isso automaticamente com: open(file, 'w', encoding='utf-8')
```

---

### ❌ Dados extraídos incorretamente

**Problema:**
```json
{
  "cliente": "Atenciosamente",  ← Pegou assinatura
  "local": "São Paulo - SP (11) 1234-5678"  ← Pegou telefone junto
}
```

**Causa:** IA confundida ou dados ambíguos

**Solução:**

**1. Melhorar preparação:**
```bash
# Ver dados preparados
python src/cli.py preparar-dados email.html -o preparado.md
cat preparado.md

# Se assinatura não foi removida, melhorar regex em prepare_data.py
```

**2. Usar Sonnet:**
```bash
python src/cli.py processar-pasta 26_062 --sonnet
```

**3. Editar JSON manualmente:**
```bash
# Extrair
python src/cli.py extrair-dados preparado.md -o orcamento.json

# Corrigir
nano orcamento.json
# Ajustar campos

# Criar tarefa
python src/cli.py criar-tarefa orcamento.json
```

---

### ❌ CNPJ/CPF não detectado

**Problema:**
- Sistema não extrai CNPJ/CPF mesmo existindo no email

**Causa:** Formato não reconhecido pelo regex

**Solução:**

**1. Verificar formato:**
```python
# Formatos suportados:
# CNPJ: 12.345.678/0001-90 ou 12345678000190
# CPF: 123.456.789-00 ou 12345678900
```

**2. Adicionar formato ao regex:**
```python
# Em prepare_data.py, atualizar PATTERNS:
'cnpj': r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b',
```

**3. Extrair manualmente e adicionar ao JSON**

---

## 🔗 Problemas de Integração

### ❌ Tarefa não aparece no Asana

**Problema:**
- Sistema diz que criou tarefa
- Tarefa não aparece no Asana

**Causa:** Sistema em modo simulação

**Solução:**

**Verificar se API está configurada:**
```python
# Abrir src/asana_lib.py
# Ver se ASANA_ACCESS_TOKEN está no .env

# Testar
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ASANA_ACCESS_TOKEN'))"
```

**Se retornar None:**
1. Adicionar token ao `.env`
2. Ver `docs/INTEGRACAO_ASANA.md`
3. Conectar API real

---

### ❌ Anexos não são anexados

**Problema:**
- PDFs existem na pasta
- Não são anexados à tarefa

**Causa:** Modo simulação ou API não configurada

**Solução:**

**1. Verificar se PDFs existem:**
```bash
ls pasta/26_062/03_Orcamento/ORC_*.pdf
```

**2. Verificar logs:**
```bash
python src/cli.py processar-pasta 26_062 -v 2>&1 | grep -i "anexo"
```

**3. Conectar API Asana:**
- Ver `docs/INTEGRACAO_ASANA.md`
- Implementar método `anexar_arquivo`

---

### ❌ Subtarefas não criadas

**Problema:**
- Tarefa principal criada
- 7 subtarefas não aparecem

**Causa:** Modo simulação ou erro na criação

**Solução:**

**1. Verificar logs:**
```bash
python src/cli.py processar-pasta 26_062 -v 2>&1 | grep -i "subtarefa"
```

**2. Testar criação de subtarefa manualmente:**
```python
from src.asana_lib import AsanaLib

asana = AsanaLib()
# Conectar API real primeiro
asana.criar_orcamento({
    'cliente': 'Teste',
    'local': 'SP',
    'tipo_servico': 'instalacao',
    'origem': 'comercial',
    'descricao': 'Teste'
})
```

---

## 🆘 Problemas Não Listados

### Passos Gerais de Debug

**1. Executar com verbose:**
```bash
python src/cli.py processar-pasta 26_062 --confirm -v > debug.log 2>&1
```

**2. Verificar stack trace completo:**
```bash
cat debug.log | grep -A 20 "Traceback"
```

**3. Isolar o problema:**
```bash
# Testar Gmail separadamente
python src/gmail_client.py --test

# Testar preparação
python src/prepare_data.py email.html

# Testar extração
python src/ai_extractor.py preparado.md

# Testar Asana
python -c "from src.asana_lib import AsanaLib; a = AsanaLib(); print('OK')"
```

**4. Verificar ambiente:**
```bash
# Python version
python --version

# Dependências instaladas
pip list

# Variáveis de ambiente
env | grep -E "(ANTHROPIC|ASANA)"

# Espaço em disco
df -h
```

**5. Reportar bug:**
```
Título: [Breve descrição do problema]

Ambiente:
- OS: macOS/Linux/Windows
- Python: 3.10.x
- Versão do sistema: 1.0.0

Passos para reproduzir:
1. ...
2. ...
3. ...

Comportamento esperado:
...

Comportamento observado:
...

Logs (anexar debug.log):
[anexar arquivo]
```

---

## 📞 Suporte

### Antes de Pedir Ajuda

- [ ] Ler este documento completamente
- [ ] Executar com `-v` e salvar logs
- [ ] Isolar o problema (qual componente falha?)
- [ ] Tentar soluções sugeridas
- [ ] Buscar no histórico de issues (GitHub)

### Como Pedir Ajuda

**Incluir sempre:**
1. Output completo com `-v`
2. Comando exato executado
3. Versão do Python e do sistema
4. O que já tentou fazer

**Modelo de mensagem:**
```
Problema: [descrição breve]

Comando executado:
python src/cli.py processar-pasta 26_062 --confirm -v

Erro obtido:
[copiar erro exato]

Python version: 3.10.8
OS: macOS 14.1

Já tentei:
- Re-autenticar Gmail
- Reinstalar dependências
- [etc]

Logs completos em anexo.
```

---

## 🔄 Atualizações

Este documento é atualizado conforme novos problemas são descobertos.

**Como contribuir:**
1. Encontrou problema não listado?
2. Documentar problema e solução
3. Adicionar neste arquivo
4. Fazer Pull Request

---

**Última atualização:** 30/01/2026
**Versão do sistema:** 1.0.0
**Mantido por:** Equipe de Desenvolvimento

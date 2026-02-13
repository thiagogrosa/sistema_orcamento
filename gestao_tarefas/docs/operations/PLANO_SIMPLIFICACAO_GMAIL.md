# Plano de Simplificação: Integração Gmail via Scripts Python

## 1. Contexto e Objetivo
Atualmente, o projeto possui uma infraestrutura robusta em Python (`src/gmail_client.py`) capaz de autenticar e interagir com a API do Gmail de forma segura e eficiente.

Tentativas anteriores de utilizar servidores MCP externos (via Docker/Node.js) geraram complexidade desnecessária e falhas de conexão. O objetivo deste plano é formalizar a estratégia de **uso direto de scripts locais**, eliminando a dependência de containers e simplificando a arquitetura.

## 2. Decisão Arquitetural
- **Descontinuar:** Uso de MCPs de terceiros que exijam Docker ou runtimes complexos para tarefas simples de leitura de email.
- **Adotar:** Execução direta do "motor" Python já existente no projeto.
- **Manter:** O código do `src/mcp_server_gmail.py` será mantido no repositório apenas como uma alternativa futura de *MCP Local* (sem Docker), caso seja necessário interagir via chat em tempo real, mas não será o foco da automação principal.

## 3. Fluxo de Trabalho Implementado

### A. Autenticação
A autenticação OAuth 2.0 é gerenciada localmente pelo script, utilizando variáveis de ambiente (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`) e persistindo o token em `config/gmail_token.pickle`.

**Escopo:** `gmail.modify` (leitura, escrita, envio - SEM exclusão)

### B. Pipeline de Processamento

```
fila-pesquisa.json
       |
       v
processar_demandas.py  -->  gmail_client.py  -->  Gmail API
       |                                              |
       v                                              v
extrator_dados_email.py                      data/gmail/extracted/{ID}/
       |
       v
resultados-pesquisa-gmail.json
       |
       v
atualizar_asana.py  -->  Asana API
       |
       v
data/reports/plano_atualizacao_asana.json (ou execução direta)
```

### C. Scripts Disponíveis

| Script | Função | Status |
|--------|--------|--------|
| `scripts/ops/processar_demandas.py` | Processamento em lote de demandas | Validado |
| `scripts/ops/extrator_dados_email.py` | Extração de dados via regex | Validado |
| `scripts/ops/atualizar_asana.py` | Atualização de tarefas no Asana | Validado |
| `src/gmail_client.py` | Cliente Gmail (autenticação + busca) | Validado |
| `src/asana_lib.py` | Biblioteca Asana (criação de tarefas) | Parcial |

## 4. Como Usar

### Processar demandas em lote
```bash
source venv/bin/activate

# Processar todas as pendentes
python scripts/ops/processar_demandas.py

# Processar uma demanda específica
python scripts/ops/processar_demandas.py --id 26_049

# Filtrar por prioridade
python scripts/ops/processar_demandas.py --prioridade alta

# Limitar quantidade
python scripts/ops/processar_demandas.py --limite 5

# Simular sem executar
python scripts/ops/processar_demandas.py --dry-run
```

### Extrair dados de emails já baixados
```bash
# De um arquivo
python scripts/ops/extrator_dados_email.py email.txt

# De um diretório
python scripts/ops/extrator_dados_email.py data/gmail/extracted/26_049/
```

### Preparar atualização Asana
```bash
# Gerar plano completo
python scripts/ops/atualizar_asana.py

# Uma demanda específica
python scripts/ops/atualizar_asana.py --id 26_049
```

A execução do plano é feita via **MCP Asana no Claude Code** (interativo):
```
"Atualize as tarefas no Asana conforme data/reports/plano_atualizacao_asana.json"
```

**Por que MCP e não API direta?**
O Asana tem uso ativo (criar, inserir, validar) onde a interação via MCP
permite revisão humana antes de cada atualização. Scripts automáticos são
adequados para leitura (Gmail), mas para escrita no Asana o MCP é mais seguro.

## 5. Validação Realizada (07/02/2026)

### Teste completo com demanda 26_049 (Porto Seguro Vitória/ES)

**Resultados:**
- 20 emails encontrados no Gmail
- 5 emails baixados e processados
- Dados extraídos via regex:
  - CNPJ: 64.160.798/0001-11
  - Telefone: 27 98168-6629
  - Valor: R$ 2.927,20
  - Condições de pagamento: 50% na conclusão + 50% em 30 dias
  - 4 pessoas envolvidas identificadas
- Plano de atualização gerado com sucesso
- Emails salvos em `data/gmail/extracted/26_049/`

### Processamento em lote (dry-run)
- 9 demandas de alta prioridade testadas
- Queries geradas corretamente para cada demanda

## 6. Vantagens desta Abordagem
- **Zero Docker:** Redução drástica de consumo de recursos e complexidade de configuração.
- **Debug Simples:** Logs são gerados diretamente no terminal/arquivos locais.
- **Velocidade:** Conexão direta Python -> Google API sem intermediários.
- **Segurança:** Controle total sobre como as credenciais são acessadas e armazenadas localmente.
- **Batch Processing:** Processamento em lote sem intervenção humana.
- **Dados Estruturados:** Extração automatizada via regex com consolidação de múltiplos emails.

## 7. Limitações Conhecidas
- **Regex:** Extração por regex pode confundir dados (ex: CNPJ de fornecedor vs cliente)
- **Emails internos:** Emails entre colegas podem ter informações parciais
- **Demandas sem email:** Algumas demandas não possuem correspondência no Gmail (criadas via telefone, WhatsApp, etc.)
- **Python 3.9:** Avisos de deprecação das bibliotecas Google (funcional, mas considerar atualização)

## 8. Próximos Passos
- [ ] Processar todas as 31 demandas da fila em lote
- [ ] Executar plano de atualização no Asana via MCP
- [ ] Refinar extração de dados com padrões específicos do setor
- [ ] Criar relatório consolidado de progresso

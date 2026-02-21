# Plano de Verificação Real do Sistema

> **Objetivo:** Definir verificações executáveis que produzem saída observável e
> mensurável. Cada item tem um comando concreto, critério de sucesso e o que fazer
> se falhar.
>
> **Princípio:** Nenhuma afirmação sobre o sistema deve ser considerada válida sem
> ter passado por pelo menos uma verificação desta lista.

---

## 1. Verificações de Ambiente (pré-requisito)

### 1.1 Python e dependências

```bash
# Em cada módulo
cd /home/user/sistema_orcamento/gestao_tarefas
python --version          # Deve ser >= 3.11
pip list | grep -E "anthropic|google-auth|tenacity"

cd /home/user/sistema_orcamento/orcamento_hvac
pip list | grep -E "openpyxl|difflib"

cd /home/user/sistema_orcamento/gerador_propostas
pip list | grep -E "weasyprint|jinja2|reportlab"
```

**Critério de sucesso:** Sem ImportError ao importar os módulos principais.

```bash
python -c "from gestao_tarefas.src.gmail_client import GmailClient; print('OK')"
python -c "from gestao_tarefas.src.asana_lib import AsanaLib; print('OK')"
python -c "from orcamento_hvac.dados.composicoes import COMPOSICOES; print(len(COMPOSICOES), 'composicoes')"
```

---

## 2. Módulo gestao_tarefas

### 2.1 Executar suite de testes

```bash
cd /home/user/sistema_orcamento/gestao_tarefas
python -m pytest tests/ -v 2>&1 | tee /tmp/test_gestao_tarefas.txt
```

**O que capturar:**
- Quantos testes passam / falham / pulam
- Quais testes requerem credenciais reais (Gmail, Asana) vs. mocks
- Cobertura de cada módulo

**Critério mínimo:** Todos os testes que não requerem credenciais externas devem passar.

### 2.2 Verificar asana_lib em modo simulação

```bash
cd /home/user/sistema_orcamento/gestao_tarefas
python src/asana_lib.py --test --verbose 2>&1
```

**O que verificar:**
- Aparece o aviso `MODO SIMULAÇÃO` no log
- O ID retornado é um UUID aleatório (não um GID real do Asana)
- As 4 funções de formatação (`_formatar_titulo`, `_formatar_descricao`, `_determinar_tags`, `_gerar_comentario_fechamento`) produzem output correto

**Critério de sucesso:** Testes passam, aviso de simulação aparece, formatação está correta.

### 2.3 Verificar CLI em modo dry-run (sem credenciais)

```bash
cd /home/user/sistema_orcamento/gestao_tarefas
python src/cli.py --help
python src/cli.py processar-pasta 26_999 --dry-run --verbose 2>&1
```

**O que verificar:**
- CLI imprime ajuda sem erro
- Modo `--dry-run` executa sem chamar Gmail ou Asana
- Output de log aparece corretamente

### 2.4 Verificar gmail_client (requer OAuth token)

> **Pré-requisito:** Arquivo `config/gmail_token.pickle` deve existir com token válido.

```bash
cd /home/user/sistema_orcamento/gestao_tarefas
python src/gmail_client.py --test --query "is:inbox" 2>&1 | head -30
```

**O que capturar:**
- Autenticação OK ou erro de token
- Número de emails retornados
- Se retornar emails: confirmar que os campos (subject, from, date) são preenchidos

**Critério de sucesso:** Retorna lista de emails sem HttpError.

**Se falhar:** Verificar se `config/gmail_credentials.json` existe e executar
`python src/gmail_client.py --setup` para reautenticar.

### 2.5 Verificar ai_extractor (requer ANTHROPIC_API_KEY)

```bash
cd /home/user/sistema_orcamento/gestao_tarefas
echo "Solicitamos orçamento para instalação de 2 splits 12.000 BTU em escritório em São Paulo. Prazo: 30 dias. Contato: João Silva, joao@empresa.com, (11) 99999-0000." > /tmp/teste_extrator.txt
python src/cli.py extrair-dados /tmp/teste_extrator.txt 2>&1
```

**O que capturar:**
- JSON retornado contém `cliente`, `tipo_servico`, `local`
- Modelo usado (Haiku ou Sonnet)
- Tokens consumidos (informação observável, não comparativa)
- Custo em USD da chamada

**Critério de sucesso:** JSON válido com campos principais preenchidos.

---

## 3. Módulo orcamento_hvac

### 3.1 Executar suite de testes

```bash
cd /home/user/sistema_orcamento/orcamento_hvac
python -m pytest tests/ -v 2>&1 | tee /tmp/test_orcamento_hvac.txt
```

**O que capturar:**
- Quantos passam / falham
- Especificamente: `test_validar_composicoes.py` e `test_dados.py` devem passar sem credenciais externas
- Testes de stage (3, 5, 6) que mockam Asana devem passar sem credenciais

### 3.2 Executar validador de composições

```bash
cd /home/user/sistema_orcamento/orcamento_hvac
python validar_composicoes.py 2>&1
```

**O que verificar:**
- Número total de composições validadas
- Número de erros (deve ser 0 conforme relatório v2)
- Número de avisos (deve ser 0)
- Número de infos (similaridade — esperados ~44)
- Arquivos gerados: `relatorio-validacao-composicoes.md` e `.json`

**Comparar com:**
Relatório existente em `relatorio-validacao-composicoes.md` (gerado 12/02/2026):
- 94 composições, 0 erros, 0 avisos, 44 infos

### 3.3 Gerar planilha Excel (sem template VBA)

```bash
cd /home/user/sistema_orcamento/orcamento_hvac
python criar_planilha.py --help
python criar_planilha.py 2>&1 | head -30
```

**O que verificar:**
- Arquivo Excel é gerado sem erro
- Abas existem no arquivo gerado
- Dados das composições aparecem nas células corretas

**Limitação conhecida:** Fórmulas de arrays dinâmicos (LET, MAP, PROCX) só funcionam
se carregadas do `template.xlsm` — não são geradas pelo Python.

### 3.4 Verificar scraper (sem chamadas reais)

```bash
cd /home/user/sistema_orcamento/orcamento_hvac
python scraper_cli.py --help
# Testar com cache ou URL de teste controlada
python scraper_cli.py cache --list 2>&1
```

**O que verificar:**
- CLI funciona sem erro
- Se há cache existente, listar entradas
- Não executar scraping real neste passo (pode violar ToS dos sites)

---

## 4. Módulo gerador_propostas

### 4.1 Executar suite de testes

```bash
cd /home/user/sistema_orcamento/gerador_propostas
python -m pytest hvac/tests/ -v 2>&1 | tee /tmp/test_gerador_propostas.txt
```

**O que capturar:**
- Testes de compositor e precificador passam sem credenciais externas
- `test_gerador_pdf_manual.py` pode requerer weasyprint instalado

### 4.2 Executar pipeline com escopo de exemplo

```bash
cd /home/user/sistema_orcamento/gerador_propostas
# Verificar se existe escopo de exemplo
ls hvac/ *.json 2>/dev/null || find . -name "escopo*.json" | head -5

# Se existir, executar pipeline
python -m hvac.pipeline <caminho_escopo.json> /tmp/output_teste/ 2>&1
```

**O que verificar:**
- Pipeline executa sem ImportError
- Gera arquivos em `/tmp/output_teste/`
- Proposta contém seções básicas (cliente, itens, totais)

---

## 5. Verificações de Integração (requerem credenciais)

> Estas verificações só podem ser executadas com credenciais reais configuradas.
> Documentar o resultado — **não** usar o resultado para fazer afirmações
> comparativas sem contexto.

### 5.1 Gmail → extração completa

```bash
cd /home/user/sistema_orcamento/gestao_tarefas

# Buscar emails reais de uma demanda conhecida
python src/cli.py buscar-emails 26_062 --query "Porto Seguro" -v 2>&1

# Registrar: quantos emails retornados, quais assuntos
```

### 5.2 Pipeline completo em dry-run com pasta real

```bash
# Com uma pasta real de Drive montada localmente
python src/cli.py processar-pasta 26_062 --dry-run -v 2>&1
```

**O que registrar:**
- Pasta encontrada ou não
- Arquivos de email encontrados (quantidade)
- O pipeline chega até a etapa de extração IA
- Tarefa NÃO é criada (dry-run)

### 5.3 Criação real de tarefa Asana (ambiente de teste)

> **Atenção:** Executar apenas com projeto Asana de teste, não em produção.
> A `asana_lib.py` precisa ser atualizada para usar a API direta antes deste teste.

**Pré-condição:** Implementar `_criar_tarefa_asana()` com chamada real à API Asana.
**Verificar:** Task GID retornado existe de fato no projeto Asana.

---

## 6. Registro de Resultados

Para cada verificação executada, documentar em `analysis/resultados_verificacao.md`:

```markdown
## [DATA] Verificação: [NOME]

- **Comando executado:** `<comando>`
- **Ambiente:** Python X.Y, SO, dependências-chave
- **Resultado:** PASSOU / FALHOU / PARCIAL
- **Output relevante:** (trecho do output)
- **Observações:** (o que descobriu)
- **Próximo passo:** (se falhou)
```

---

## 7. O que NÃO medir sem metodologia adequada

Os itens abaixo requerem metodologia de benchmark antes de qualquer afirmação:

| Afirmação a verificar | Metodologia necessária |
|----------------------|------------------------|
| "X% redução de tempo" | Medir tempo de processo manual (N amostras) vs. tempo com sistema (N amostras equivalentes), mesmo tipo de demanda |
| "X% economia de custo" | Registrar custo de tokens por demanda processada por pelo menos 30 demandas reais |
| "Haiku é suficiente para Y% dos casos" | Comparar output Haiku vs. Sonnet para mesmo input em conjunto de amostras representativo |
| "X emails processados por hora" | Medir throughput real com rate limiting da Gmail API |

---

## 8. Prioridade de Execução

| Prioridade | Verificação | Dependência |
|------------|-------------|-------------|
| **Alta** | 2.1 Testes gestao_tarefas | Nenhuma |
| **Alta** | 3.1 Testes orcamento_hvac | Nenhuma |
| **Alta** | 3.2 Validador composições | Nenhuma |
| **Alta** | 4.1 Testes gerador_propostas | Nenhuma |
| **Média** | 2.2 asana_lib simulação | Nenhuma |
| **Média** | 2.3 CLI dry-run | Nenhuma |
| **Média** | 3.3 Gerador Excel | Nenhuma |
| **Baixa** | 2.4 Gmail real | OAuth token |
| **Baixa** | 2.5 AI extractor | ANTHROPIC_API_KEY |
| **Baixa** | 5.x Integração completa | Gmail + Anthropic + Asana |

# Guia do Desenvolvedor - Sistema de Gestão de Orçamentos

**Versão:** 1.0.0
**Público-alvo:** Desenvolvedores mantendo/estendendo o sistema
**Última atualização:** 30/01/2026

---

## 📋 Visão Geral

Este guia ajuda desenvolvedores a:
- Entender a arquitetura do sistema
- Adicionar novas funcionalidades
- Manter e debugar código existente
- Seguir padrões do projeto

---

## 🏗️ Arquitetura

### Estrutura do Código

```
src/
├── gmail_client.py      # Cliente Gmail API (OAuth 2.0)
├── prepare_data.py      # Limpeza de dados (regex, HTML)
├── ai_extractor.py      # Extração com IA (Haiku/Sonnet)
├── asana_lib.py         # Interface Asana (simulação/API)
└── cli.py               # Orquestrador principal

prompts/
└── extracao_orcamento_haiku.txt  # Prompt otimizado

skills/
├── skill_orcamentos.md  # Skill para agentes Claude
└── README.md            # Documentação de skills

tests/
├── test_gmail_client.py
├── test_prepare_data.py
├── test_ai_extractor.py
├── test_asana_lib.py
└── test_cli.py
```

### Fluxo de Dados

```
1. Gmail API
   └─> emails brutos (HTML, anexos)

2. DataPreparer
   └─> texto limpo (Markdown, -60-80% tokens)

3. AIExtractor
   └─> JSON estruturado (Pydantic validado)

4. AsanaLib
   └─> tarefa no Asana (+ 7 subtarefas)

5. CLI
   └─> orquestra tudo + relatórios
```

### Dependências

```python
# Core
anthropic      # Claude API
asana          # Asana API
google-auth-*  # Gmail OAuth

# Processamento
beautifulsoup4 # Parse HTML
html2text      # HTML → Markdown
pydantic       # Validação JSON

# Testes
pytest
pytest-mock
pytest-cov
```

---

## 🔧 Setup de Desenvolvimento

### 1. Clonar e Instalar

```bash
# Clonar repositório
git clone [repo_url]
cd gestao_tarefas

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Instalar ferramentas de dev
pip install black flake8 mypy pytest pytest-cov
```

### 2. Configurar Credenciais

```bash
# Copiar template
cp .env.example .env

# Editar .env
ANTHROPIC_API_KEY=sk-ant-...
ASANA_ACCESS_TOKEN=0/...
```

```bash
# Configurar Gmail API
python src/gmail_client.py --setup
# Seguir instruções OAuth
```

### 3. Rodar Testes

```bash
# Todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src --cov-report=html

# Teste específico
pytest tests/test_cli.py -v

# Testes de integração (requer auth)
pytest tests/ -v -m integration
```

### 4. Verificar Code Quality

```bash
# Formatar código
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

---

## 💻 Adicionando Funcionalidades

### Exemplo 1: Novo Modelo de IA

Adicionar suporte para Claude Opus.

**1. Atualizar `ai_extractor.py`:**

```python
class AIExtractor:
    MODELOS_DISPONIVEIS = {
        'haiku': 'claude-haiku-4-20250514',
        'sonnet': 'claude-sonnet-4-5-20250514',
        'opus': 'claude-opus-4-5-20251101',  # NOVO
    }

    CUSTOS = {
        'haiku': {'input': 0.25, 'output': 1.25},
        'sonnet': {'input': 3.00, 'output': 15.00},
        'opus': {'input': 15.00, 'output': 75.00},  # NOVO
    }

    def __init__(self, force_model: str = 'haiku'):
        """
        Args:
            force_model: 'haiku', 'sonnet', ou 'opus'
        """
        if force_model not in self.MODELOS_DISPONIVEIS:
            raise ValueError(f"Modelo {force_model} não suportado")

        self.modelo = force_model
        # ... resto
```

**2. Atualizar CLI (`cli.py`):**

```python
parser_processar.add_argument('--opus', action='store_true',
                             help='Forçar uso do Opus')

# No método processar_pasta:
if args.opus:
    self.ai_extractor = AIExtractor(force_model='opus')
elif args.sonnet:
    self.ai_extractor = AIExtractor(force_model='sonnet')
else:
    self.ai_extractor = AIExtractor(force_model='haiku')
```

**3. Atualizar skill (`skills/skill_orcamentos.md`):**

```markdown
### Quando usar `--opus`?

**Use:**
- ✅ Licitação internacional complexa
- ✅ Máxima precisão necessária

**Não use:**
- ❌ Por padrão (60x mais caro que Haiku)
```

**4. Adicionar testes:**

```python
def test_extrair_com_opus():
    """Deve extrair usando Opus."""
    extractor = AIExtractor(force_model='opus')
    resultado = extractor.extrair("texto teste")

    stats = extractor.get_estatisticas()
    assert stats['modelo'] == 'opus'
```

**5. Documentar:**
- Atualizar `COMPARACAO_CUSTOS_IA.md`
- Adicionar exemplo em `EXEMPLO_CLI.md`
- Atualizar `README.md`

---

### Exemplo 2: Novo Comando CLI

Adicionar comando para atualizar tarefas existentes.

**1. Criar método em `asana_lib.py`:**

```python
def atualizar_tarefa(
    self,
    task_id: str,
    dados: Dict
) -> bool:
    """
    Atualiza tarefa existente.

    Args:
        task_id: ID da tarefa
        dados: Dados para atualizar

    Returns:
        True se atualizado com sucesso
    """
    if not self.asana_client:
        logger.info(f"[SIMULAÇÃO] Atualizando tarefa {task_id}")
        return True

    try:
        self.asana_client.tasks.update(task_id, dados)
        logger.info(f"Tarefa atualizada: {task_id}")
        return True

    except Exception as e:
        logger.error(f"Erro ao atualizar: {e}")
        return False
```

**2. Adicionar comando no CLI (`cli.py`):**

```python
# No método __init__ da classe OrcamentoCLI:
def atualizar_tarefa(self, task_id: str, json_file: str):
    """Comando para atualizar tarefa."""
    logger.info(f"📝 Atualizando tarefa: {task_id}")

    if not os.path.exists(json_file):
        logger.error(f"❌ Arquivo não encontrado: {json_file}")
        return

    try:
        # Ler JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        # Atualizar
        sucesso = self.asana_lib.atualizar_tarefa(task_id, dados)

        if sucesso:
            logger.info(f"✓ Tarefa atualizada: {task_id}")
        else:
            logger.error("❌ Falha ao atualizar")

    except Exception as e:
        logger.error(f"❌ Erro: {e}")

# Na função main(), adicionar parser:
parser_atualizar = subparsers.add_parser('atualizar-tarefa',
                                        help='Atualizar tarefa existente')
parser_atualizar.add_argument('task_id', help='ID da tarefa')
parser_atualizar.add_argument('json_file', help='JSON com atualizações')

# No dispatcher:
elif args.command == 'atualizar-tarefa':
    cli.atualizar_tarefa(args.task_id, args.json_file)
    return 0
```

**3. Adicionar testes:**

```python
def test_atualizar_tarefa():
    """Deve atualizar tarefa."""
    asana = AsanaLib()

    sucesso = asana.atualizar_tarefa(
        "task_123",
        {"notes": "Atualização de teste"}
    )

    assert sucesso is True
```

**4. Documentar:**
- Adicionar em `GUIA_USUARIO.md`
- Adicionar exemplo em `EXEMPLO_CLI.md`
- Atualizar skill

---

### Exemplo 3: Nova Fonte de Dados

Adicionar suporte para Outlook além de Gmail.

**1. Criar `outlook_client.py`:**

```python
"""
Cliente para Outlook API

Similar ao gmail_client.py mas para Outlook/Microsoft Graph
"""

class OutlookClient:
    def __init__(self, credentials_file: str = "config/outlook_credentials.json"):
        self.credentials_file = credentials_file
        self.client = None

    def authenticate(self) -> bool:
        """Autenticar via Microsoft Graph."""
        # Implementar OAuth com Microsoft
        pass

    def buscar_emails(self, query: str, max_results: int = 10) -> List[Dict]:
        """Buscar emails no Outlook."""
        # Implementar busca
        pass

    # ... métodos similares ao GmailClient
```

**2. Adaptar CLI:**

```python
parser.add_argument('--outlook', action='store_true',
                   help='Usar Outlook em vez de Gmail')

# No código:
if args.outlook:
    self.email_client = OutlookClient()
else:
    self.email_client = GmailClient()
```

**3. Abstrair interface:**

```python
# email_interface.py
from abc import ABC, abstractmethod

class EmailClient(ABC):
    @abstractmethod
    def authenticate(self) -> bool:
        pass

    @abstractmethod
    def buscar_emails(self, query: str, max_results: int) -> List[Dict]:
        pass

# Fazer GmailClient e OutlookClient herdarem de EmailClient
```

---

## 🧪 Testes

### Estrutura de Testes

```python
# tests/test_modulo.py

import pytest
from unittest.mock import Mock, patch

class TestModuloInit:
    """Testes de inicialização."""

    def test_init_padrao(self):
        """Deve inicializar com valores padrão."""
        obj = MinhaClasse()
        assert obj.atributo is not None

class TestModuloMetodo1:
    """Testes do método1."""

    def setup_method(self):
        """Setup antes de cada teste."""
        self.obj = MinhaClasse()

    def test_metodo1_sucesso(self):
        """Deve executar com sucesso."""
        resultado = self.obj.metodo1("input")
        assert resultado == "esperado"

    @patch('modulo.dependencia_externa')
    def test_metodo1_com_mock(self, mock_dep):
        """Deve usar mock para dependência."""
        mock_dep.return_value = "valor_mock"
        resultado = self.obj.metodo1("input")
        assert resultado == "processado"

@pytest.mark.integration
class TestModuloIntegration:
    """Testes de integração (requer auth)."""

    @pytest.mark.skip(reason="Requer credenciais")
    def test_integracao_real(self):
        """Teste com API real."""
        pass
```

### Rodar Testes

```bash
# Todos
pytest tests/ -v

# Específico
pytest tests/test_cli.py::TestCLIInit::test_init_defaults -v

# Integração
pytest tests/ -v -m integration

# Coverage
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Mocks Úteis

```python
# Mock de API externa
@patch('anthropic.Anthropic')
def test_com_mock_anthropic(mock_anthropic):
    mock_client = Mock()
    mock_client.messages.create.return_value = Mock(
        content=[Mock(text='{"cliente": "Teste"}')]
    )
    mock_anthropic.return_value = mock_client

    # Testar código

# Mock de arquivo
@patch('builtins.open', mock_open(read_data='conteúdo'))
def test_com_mock_arquivo():
    # Testar leitura de arquivo

# Mock de Path
@patch('pathlib.Path.exists')
def test_com_mock_path(mock_exists):
    mock_exists.return_value = True
    # Testar lógica de arquivo
```

---

## 📝 Padrões de Código

### Style Guide

Seguimos PEP 8 com algumas customizações:

```python
# Imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Constantes
MAX_RESULTS = 10
DEFAULT_MODEL = 'haiku'

# Classes
class MinhaClasse:
    """Docstring da classe."""

    def __init__(self, param: str):
        """
        Inicializa classe.

        Args:
            param: Descrição do parâmetro
        """
        self.param = param

    def metodo_publico(self, arg: int) -> str:
        """
        Método público.

        Args:
            arg: Descrição

        Returns:
            Descrição do retorno

        Raises:
            ValueError: Quando arg inválido
        """
        if arg < 0:
            raise ValueError("arg deve ser positivo")

        return self._metodo_privado(arg)

    def _metodo_privado(self, arg: int) -> str:
        """Método privado."""
        return f"resultado_{arg}"

# Funções
def funcao_helper(param: str) -> Dict:
    """
    Função helper.

    Args:
        param: Descrição

    Returns:
        Descrição do retorno
    """
    return {"key": param}
```

### Type Hints

Sempre usar type hints:

```python
# ✅ Bom
def processar(texto: str, opcoes: Optional[Dict] = None) -> Dict:
    pass

# ❌ Ruim
def processar(texto, opcoes=None):
    pass
```

### Docstrings

Estilo Google:

```python
def funcao_complexa(
    param1: str,
    param2: int,
    param3: Optional[List] = None
) -> Dict[str, Any]:
    """
    Descrição curta em uma linha.

    Descrição mais detalhada em múltiplas linhas,
    explicando o que a função faz, como usar, etc.

    Args:
        param1: Descrição do param1
        param2: Descrição do param2
        param3: Descrição opcional

    Returns:
        Dicionário com:
            - key1: Descrição
            - key2: Descrição

    Raises:
        ValueError: Quando param1 vazio
        RuntimeError: Quando operação falha

    Examples:
        >>> funcao_complexa("teste", 42)
        {'resultado': 'sucesso'}
    """
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Níveis
logger.debug("Informação detalhada para debug")
logger.info("Informação geral")
logger.warning("Alerta - algo pode estar errado")
logger.error("Erro - operação falhou")
logger.critical("Erro crítico - sistema comprometido")

# Incluir contexto
logger.info(f"Processando arquivo: {filename}")
logger.error(f"Falha ao processar {id}: {error}", exc_info=True)
```

### Error Handling

```python
# Específico sobre o que pode falhar
try:
    resultado = operacao_arriscada()
except ValueError as e:
    logger.error(f"Valor inválido: {e}")
    return None
except IOError as e:
    logger.error(f"Erro de I/O: {e}")
    raise
except Exception as e:
    logger.error(f"Erro inesperado: {e}", exc_info=True)
    raise

# Não usar bare except
try:
    algo()
except:  # ❌ Ruim - captura tudo
    pass

# Usar finally para cleanup
try:
    arquivo = open("file.txt")
    processar(arquivo)
finally:
    arquivo.close()

# Ou usar context manager
with open("file.txt") as arquivo:
    processar(arquivo)
```

---

## 🔍 Debugging

### Logs Detalhados

```bash
# Ativar verbose
python src/cli.py processar-pasta 26_062 -v

# Ver só erros
python src/cli.py processar-pasta 26_062 2>&1 | grep ERROR

# Salvar log completo
python src/cli.py processar-pasta 26_062 -v > debug.log 2>&1
```

### Debugging com pdb

```python
# Adicionar breakpoint
import pdb; pdb.set_trace()

# Ou (Python 3.7+)
breakpoint()

# Comandos úteis no pdb:
# n - next line
# s - step into
# c - continue
# p var - print variable
# l - list code
# q - quit
```

### Debugging de APIs

```python
# Ver requisições HTTP
import logging
logging.getLogger('urllib3').setLevel(logging.DEBUG)

# Anthropic API
import anthropic
client = anthropic.Anthropic()
client.messages.create(..., extra_headers={'X-Debug': 'true'})

# Gmail API
service.users().messages().list(...).execute()
# Ver raw request/response no console
```

### Profiling de Performance

```python
# Time de execução
import time

start = time.time()
funcao()
print(f"Tempo: {time.time() - start:.2f}s")

# Profiling detalhado
import cProfile
cProfile.run('funcao()')

# Memory profiling
from memory_profiler import profile

@profile
def funcao():
    # código
    pass
```

---

## 🚀 Deploy e Produção

### Checklist Pré-Deploy

- [ ] Todos os testes passando
- [ ] Coverage > 80%
- [ ] Code quality (black, flake8, mypy)
- [ ] Documentação atualizada
- [ ] Credenciais configuradas
- [ ] Testes de integração validados
- [ ] Backup do sistema anterior

### Ambiente de Produção

```bash
# Criar ambiente limpo
python3 -m venv venv_prod
source venv_prod/bin/activate

# Instalar dependências exatas
pip install -r requirements.txt --no-cache-dir

# Configurar credenciais
cp .env.production .env

# Testar
python src/cli.py processar-pasta TEST --dry-run
```

### Monitoramento

```python
# Adicionar métricas
import time
from datetime import datetime

class Metrics:
    def __init__(self):
        self.operacoes = []

    def registrar(self, operacao: str, duracao: float, custo: float):
        self.operacoes.append({
            'timestamp': datetime.now(),
            'operacao': operacao,
            'duracao': duracao,
            'custo': custo
        })

    def relatorio_diario(self):
        total_ops = len(self.operacoes)
        total_custo = sum(op['custo'] for op in self.operacoes)
        # ...
```

---

## 📚 Recursos

### Documentação do Projeto

- `ARQUITETURA.md` - Arquitetura técnica
- `PLANO_IMPLEMENTACAO.md` - Plano de implementação
- `TROUBLESHOOTING.md` - Problemas comuns
- `EXEMPLO_CLI.md` - Exemplos de uso

### APIs Externas

- [Anthropic API](https://docs.anthropic.com/claude/reference)
- [Gmail API](https://developers.google.com/gmail/api)
- [Asana API](https://developers.asana.com/docs)

### Python

- [Python Docs](https://docs.python.org/3/)
- [PEP 8](https://peps.python.org/pep-0008/)
- [Pytest](https://docs.pytest.org/)

---

## 🤝 Contribuindo

### Workflow

1. **Criar branch:**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Desenvolver:**
   - Escrever código
   - Escrever testes
   - Atualizar docs

3. **Testar:**
   ```bash
   pytest tests/ -v
   black src/ tests/
   flake8 src/ tests/
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "feat: adicionar suporte para Outlook"
   ```

5. **Push e PR:**
   ```bash
   git push origin feature/nova-funcionalidade
   # Criar Pull Request
   ```

### Conventional Commits

```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
test: adicionar/atualizar testes
refactor: refatoração de código
chore: tarefas de manutenção
```

### Code Review

Checklist:
- [ ] Código segue style guide
- [ ] Testes adicionados e passando
- [ ] Documentação atualizada
- [ ] Sem warnings de linting
- [ ] Type hints presentes
- [ ] Logs adequados
- [ ] Error handling robusto

---

**Última atualização:** 30/01/2026
**Versão do sistema:** 1.0.0
**Mantido por:** Equipe de Desenvolvimento

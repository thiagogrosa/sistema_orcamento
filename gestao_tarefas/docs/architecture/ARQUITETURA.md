# Arquitetura Técnica - Sistema de Gestão de Orçamentos

**Versão:** 1.0
**Data:** 30/01/2026
**Status:** Em Desenvolvimento

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura de Alto Nível](#arquitetura-de-alto-nível)
3. [Componentes do Sistema](#componentes-do-sistema)
4. [Fluxo de Dados Detalhado](#fluxo-de-dados-detalhado)
5. [Decisões de Design](#decisões-de-design)
6. [Interfaces e Contratos](#interfaces-e-contratos)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Segurança](#segurança)
9. [Performance e Escalabilidade](#performance-e-escalabilidade)
10. [Requisitos e Dependências](#requisitos-e-dependências)

---

## 📖 Visão Geral

### Propósito do Sistema

O sistema automatiza o processo de captura, processamento e registro de demandas de orçamentos de climatização, integrando três plataformas principais:

- **Gmail** - Fonte de informações (emails de clientes)
- **Google Drive** - Armazenamento de documentos e dados brutos
- **Asana** - Sistema de gestão e acompanhamento de pipeline

### Problema que Resolve

**Antes (Processo Manual):**
1. Receber email/anotação com demanda
2. Copiar/colar manualmente informações em várias ferramentas
3. Buscar emails relacionados manualmente
4. Criar tarefa no Asana manualmente
5. Preencher todos os campos manualmente
6. Criar 7 subtarefas manualmente
7. Anexar arquivos manualmente

**Tempo:** ~15-20 minutos por demanda
**Erros:** Alto (campos esquecidos, inconsistências)
**Custo IA:** Alto (processar dados brutos com Sonnet)

**Depois (Processo Automatizado):**
1. Criar pasta no Drive com dados disponíveis
2. Executar comando: `/processar-pasta 26_062`
3. Sistema faz todo o resto automaticamente

**Tempo:** ~2 minutos por demanda
**Erros:** Baixo (processo padronizado)
**Custo IA:** 94% menor (apenas extração semântica com Haiku)

### Princípios Arquiteturais

1. **Separação de Responsabilidades**
   - Cada componente tem uma função clara e única
   - Scripts fazem processamento determinístico
   - IA faz apenas extração semântica

2. **Eficiência de Custos**
   - Minimizar uso de tokens de IA
   - Usar scripts para tarefas automatizáveis
   - Usar Haiku (barato) ao invés de Sonnet quando possível

3. **Modularidade**
   - Componentes independentes e reutilizáveis
   - Fácil substituir ou melhorar partes isoladas
   - Facilita testes e manutenção

4. **Observabilidade**
   - Logs detalhados em cada etapa
   - Métricas de performance e custo
   - Rastreabilidade completa de operações

5. **Escalabilidade**
   - Processa 1 demanda ou 100 com mesmo código
   - Preparado para automação futura
   - Não depende de intervenção manual

---

## 🏗️ Arquitetura de Alto Nível

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                          FONTES DE DADOS                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐              │
│  │   Gmail     │   │ Google      │   │  Arquivos   │              │
│  │   (API)     │   │  Drive      │   │  Locais     │              │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘              │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     CAMADA DE COLETA                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  GmailClient (src/gmail_client.py)                         │   │
│  │  • Autenticação OAuth 2.0                                  │   │
│  │  • Busca de emails por query                               │   │
│  │  • Download de mensagens (.eml, .txt)                      │   │
│  │  • Extração de anexos (PDFs, imagens)                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE PREPARAÇÃO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  DataPreparer (src/prepare_data.py)                        │   │
│  │  • Limpeza de HTML                                         │   │
│  │  • Remoção de assinaturas e threads                        │   │
│  │  • Extração de metadados (regex)                           │   │
│  │  • Detecção de CNPJ, telefones, emails, CEPs              │   │
│  │  • Consolidação em formato .md estruturado                 │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ↓ (texto limpo e estruturado)
┌─────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE EXTRAÇÃO (IA)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  AIExtractor (usa Claude API)                              │   │
│  │  • Prompt otimizado para Haiku                             │   │
│  │  • Extração semântica de campos                            │   │
│  │  • Inferência de informações (porte, urgência)             │   │
│  │  • Validação de schema JSON                                │   │
│  │  • Fallback para Sonnet em casos complexos                 │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ↓ (JSON estruturado)
┌─────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE INTEGRAÇÃO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  AsanaLibrary (src/asana_lib.py)                           │   │
│  │  • Criação de tarefas e subtarefas                         │   │
│  │  • Atualização de status e campos                          │   │
│  │  • Gestão de tags e prazos                                 │   │
│  │  • Upload de anexos                                        │   │
│  │  • Consultas e buscas                                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  DriveSync (src/sync_drive.py)                             │   │
│  │  • Criação de estrutura de pastas                          │   │
│  │  • Detecção de novos arquivos                              │   │
│  │  • Sincronização bidirecional                              │   │
│  │  • Mapeamento de IDs (Drive ↔ Asana)                       │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  CAMADA DE ORQUESTRAÇÃO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  CLI (src/cli.py)                                          │   │
│  │  • Interface de linha de comando                           │   │
│  │  • Coordenação do pipeline completo                        │   │
│  │  • Logging e progress bars                                 │   │
│  │  • Validações e confirmações                               │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         SAÍDAS                                      │
├─────────────────────────────────────────────────────────────────────┤
│  • Tarefa criada no Asana (com 7 subtarefas)                       │
│  • Arquivos anexados                                                │
│  • Logs detalhados                                                  │
│  • Relatório de processamento                                       │
│  • Mapeamento de IDs atualizado                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados Simplificado

```
Email/Drive → Coleta → Preparação → Extração IA → Criação Asana → ✓
   (dados)      (0 🪙)    (0 🪙)      (~700 🪙)      (0 🪙)

🪙 = tokens consumidos
```

---

## 🔧 Componentes do Sistema

### 1. GmailClient (src/gmail_client.py)

**Responsabilidade:** Interagir com Gmail API para buscar e baixar emails

**Funcionalidades:**
- Autenticação OAuth 2.0 com refresh automático de tokens
- Busca de emails por query complexa
- Download de emails em diferentes formatos (.eml, .txt, .html)
- Extração de anexos com metadados
- Gestão de threads e conversas

**Tecnologias:**
- `google-auth` - Autenticação
- `google-api-python-client` - Cliente da API
- `email` (stdlib) - Parse de mensagens .eml

**Interface Principal:**
```python
class GmailClient:
    def __init__(self, credentials_file: str):
        """Inicializa cliente com arquivo de credenciais OAuth."""

    def authenticate(self) -> bool:
        """Executa fluxo OAuth se necessário."""

    def buscar_emails(
        self,
        query: str,
        max_results: int = 10,
        include_spam: bool = False
    ) -> list[dict]:
        """
        Busca emails por query.

        Args:
            query: Query do Gmail (ex: "from:cliente@empresa.com subject:orçamento")
            max_results: Número máximo de resultados
            include_spam: Incluir spam/trash

        Returns:
            Lista de dicts com metadados dos emails encontrados
        """

    def baixar_email(
        self,
        email_id: str,
        output_dir: str,
        format: str = "txt"
    ) -> str:
        """
        Baixa email específico.

        Args:
            email_id: ID do email
            output_dir: Diretório de saída
            format: "txt", "html", "eml", ou "raw"

        Returns:
            Caminho do arquivo salvo
        """

    def extrair_anexos(
        self,
        email_id: str,
        output_dir: str
    ) -> list[str]:
        """
        Extrai anexos de um email.

        Returns:
            Lista de caminhos dos anexos salvos
        """
```

**Quota e Limites:**
- Gmail API: 1 bilhão de requisições/dia (gratuito)
- Rate limit: 250 requisições/segundo
- Mitigação: Retry com backoff exponencial

**Segurança:**
- Credenciais armazenadas em `config/gmail_credentials.json` (gitignored)
- Token de acesso com refresh automático
- Scopes mínimos necessários: `gmail.readonly`, `gmail.modify`

---

### 2. DataPreparer (src/prepare_data.py)

**Responsabilidade:** Limpar e estruturar dados brutos em formato otimizado

**Funcionalidades:**
- Remoção de HTML mantendo formatação legível
- Detecção e remoção de assinaturas de email
- Remoção de threads antigas (mantém só mensagem principal)
- Extração de metadados via regex (CNPJ, telefones, emails, CEPs)
- Consolidação em arquivo .md estruturado

**Tecnologias:**
- `beautifulsoup4` - Parse e limpeza de HTML
- `html2text` - Conversão HTML → Markdown
- `re` (stdlib) - Expressões regulares
- Custom parsers para padrões brasileiros

**Interface Principal:**
```python
class DataPreparer:
    def limpar_html(self, html: str) -> str:
        """Remove tags HTML e retorna texto limpo."""

    def remover_assinatura(self, texto: str) -> str:
        """Detecta e remove assinatura de email."""

    def extrair_metadados(self, texto: str) -> dict:
        """
        Extrai metadados via regex.

        Returns:
            {
                "cnpj": ["12.345.678/0001-90", ...],
                "telefones": ["(11) 98765-4321", ...],
                "emails": ["contato@empresa.com", ...],
                "ceps": ["01234-567", ...]
            }
        """

    def preparar_email(
        self,
        email_path: str,
        output_path: str
    ) -> dict:
        """
        Pipeline completo de preparação.

        Args:
            email_path: Caminho do arquivo .eml ou .html
            output_path: Onde salvar .md preparado

        Returns:
            {
                "texto_limpo": str,
                "metadados": dict,
                "anexos": list[str],
                "output_file": str
            }
        """
```

**Padrões Regex (Brasil):**
```python
PATTERNS = {
    "cnpj": r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
    "cpf": r"\d{3}\.\d{3}\.\d{3}-\d{2}",
    "telefone": r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "cep": r"\d{5}-?\d{3}",
    "data": r"\d{2}/\d{2}/\d{4}",
    "valor_monetario": r"R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?"
}
```

**Formato de Saída (.md):**
```markdown
# Dados Preparados - [ID da Demanda]

## Metadados do Email
- **De:** nome <email@empresa.com>
- **Para:** orcamentos2@armant.com.br
- **Data:** 2026-01-25 14:30
- **Assunto:** Orçamento climatização sala reuniões

## Metadados Detectados Automaticamente
- **CNPJ:** 12.345.678/0001-90
- **Telefones:** (11) 98765-4321, (11) 3456-7890
- **Emails:** contato@empresa.com, joao@empresa.com
- **CEP:** 01234-567
- **Valores:** R$ 15.000,00

## Conteúdo Principal
[Texto limpo do email, sem HTML, assinaturas ou threads]

## Anexos Encontrados
- proposta_v1.pdf (125 KB)
- planta_baixa.jpg (450 KB)
```

**Otimizações:**
- Texto limpo reduz tokens em ~60%
- Metadados extraídos por regex evitam IA processar dados estruturados
- Formato .md facilita leitura pela IA

---

### 3. AIExtractor (usa Claude API)

**Responsabilidade:** Extrair informações semânticas usando IA de forma eficiente

**Funcionalidades:**
- Processar texto preparado com prompt otimizado
- Extrair dados estruturados em JSON
- Inferir informações não explícitas (porte, urgência, tipo)
- Validar schema de saída
- Fallback automático para Sonnet em casos complexos

**Tecnologias:**
- `anthropic` SDK - Cliente oficial Claude
- Prompts versionados em `prompts/`
- Pydantic para validação de schema

**Estratégia de Modelos:**

| Situação | Modelo | Custo | Quando Usar |
|----------|--------|-------|-------------|
| **Padrão** | Haiku | $0.25/$1.25 por M | Texto preparado, dados claros |
| **Complexo** | Sonnet | $3/$15 por M | Ambiguidade, dados inconsistentes |
| **Validação** | Haiku | $0.25/$1.25 por M | Verificar JSON de saída |

**Lógica de Fallback:**
```python
def extrair_dados(texto_preparado: str) -> dict:
    # 1. Tentar com Haiku
    resultado_haiku = chamar_claude_haiku(texto_preparado)

    # 2. Validar resultado
    if validar_json(resultado_haiku):
        # 3. Verificar confiança
        confianca = calcular_confianca(resultado_haiku)

        if confianca > 0.85:
            return resultado_haiku  # Sucesso com Haiku

    # 4. Fallback para Sonnet
    resultado_sonnet = chamar_claude_sonnet(texto_preparado)
    return resultado_sonnet
```

**Prompt Otimizado (Haiku):**
```
Você é um extrator de dados de orçamentos de climatização.
Analise o texto preparado e extraia informações estruturadas.

IMPORTANTE:
- Retorne APENAS JSON válido, sem explicações
- Se campo não encontrado, use null
- Infira informações baseado em contexto

SCHEMA JSON:
{
  "cliente": "string (obrigatório)",
  "cnpj_cpf": "string ou null",
  "contato": "string ou null",
  "telefone": "string ou null",
  "email": "string ou null",
  "local": "string (obrigatório) - formato: Cidade - UF",
  "prazo": "string ou null - formato: YYYY-MM-DD",
  "tipo_servico": "instalacao|manutencao|projeto (obrigatório)",
  "eh_licitacao": "boolean",
  "numero_edital": "string ou null",
  "porte": "pequeno|medio|grande ou null",
  "origem": "comercial|cliente_direto|diretoria|engenharia",
  "descricao": "string (obrigatório) - resumo do que foi solicitado",
  "urgente": "boolean",
  "cliente_estrategico": "boolean"
}

REGRAS DE INFERÊNCIA:
- tipo_servico:
  * "instalacao" se mencionar: instalar, instalacao, novo sistema
  * "manutencao" se mencionar: manutencao, reparo, conserto, PMOC
  * "projeto" se mencionar: projeto, dimensionamento, as-built

- porte:
  * "pequeno" se: <= 100m² ou <= 3 equipamentos ou valor < R$10k
  * "medio" se: 100-500m² ou 3-10 equipamentos ou R$10k-50k
  * "grande" se: > 500m² ou > 10 equipamentos ou > R$50k

- urgente: true se mencionar: urgente, emergência, prazo < 7 dias

- eh_licitacao: true se mencionar: licitação, pregão, edital, concorrência

TEXTO PREPARADO:
{texto}

RESPONDA APENAS COM O JSON:
```

**Validação de Saída:**
```python
from pydantic import BaseModel, validator
from typing import Optional, Literal

class OrcamentoData(BaseModel):
    cliente: str
    cnpj_cpf: Optional[str] = None
    contato: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    local: str
    prazo: Optional[str] = None
    tipo_servico: Literal["instalacao", "manutencao", "projeto"]
    eh_licitacao: bool = False
    numero_edital: Optional[str] = None
    porte: Optional[Literal["pequeno", "medio", "grande"]] = None
    origem: Literal["comercial", "cliente_direto", "diretoria", "engenharia"]
    descricao: str
    urgente: bool = False
    cliente_estrategico: bool = False

    @validator("prazo")
    def validar_data(cls, v):
        if v:
            # Validar formato YYYY-MM-DD
            ...
        return v
```

**Métricas Coletadas:**
- Tokens de input/output por extração
- Tempo de processamento
- Taxa de sucesso Haiku vs Sonnet
- Taxa de campos null por tipo
- Custo total por dia/semana/mês

---

### 4. AsanaLibrary (src/asana_lib.py)

**Responsabilidade:** Gerenciar todas operações com Asana API

**Funcionalidades:**
- Criar tarefas principais e subtarefas
- Atualizar status, tags, prazos, responsáveis
- Mover tarefas entre seções
- Anexar arquivos
- Buscar e consultar tarefas
- Registrar fechamentos (ganho/perdido)

**Tecnologias:**
- MCP Asana Server (via Claude Code)
- Requests direto para API (fallback)
- Retry logic com backoff exponencial

**Constantes do Projeto:**
```python
# IDs do Asana (fixos)
WORKSPACE_ID = "1204197108826498"
PROJECT_ID = "1212920325558530"

# Seções
SECAO_ENTRADA = "1212909431317491"
SECAO_ENVIADO = "1212920431590044"
SECAO_CONCLUIDO = "[gid_a_definir]"

# Template de subtarefas (ordem reversa para Asana)
SUBTAREFAS_PADRAO = [
    {
        "nome": "🏁 7. Fechamento",
        "notes": "Registrar resultado: FECHADO (valor) ou PERDIDO (motivo)"
    },
    {
        "nome": "🤝 6. Negociacao (se necessario)",
        "notes": "Tratar ajustes de preco, escopo ou prazo"
    },
    {
        "nome": "📤 5. Envio ao Cliente",
        "notes": "Enviar orcamento e confirmar recebimento"
    },
    {
        "nome": "🔍 4. Revisao Interna",
        "notes": "Revisar valores, margem e condicoes"
    },
    {
        "nome": "⚙️ 3. Elaboracao do Orcamento",
        "notes": "Criar planilha e calcular valores"
    },
    {
        "nome": "✅ 2. Aprovacao para Elaboracao",
        "notes": "Confirmar informacoes completas"
    },
    {
        "nome": "📋 1. Triagem",
        "notes": "Avaliar viabilidade e prioridade"
    }
]
```

**Interface Principal:**
```python
class AsanaLib:
    def criar_orcamento(self, dados: dict) -> str:
        """
        Cria tarefa completa no Asana.

        Args:
            dados: Dict com campos do orçamento (output do AIExtractor)

        Returns:
            task_gid da tarefa criada

        Processo:
            1. Gerar título formatado
            2. Gerar descrição formatada
            3. Criar tarefa principal no projeto
            4. Criar 7 subtarefas (ordem reversa)
            5. Adicionar tags apropriadas
            6. Definir prazo
            7. Retornar task_gid
        """

    def criar_subtarefas(self, parent_task_id: str) -> list[str]:
        """Cria as 7 subtarefas padrão."""

    def avancar_etapa(
        self,
        task_id: str,
        etapa: int,
        observacao: str = None
    ) -> bool:
        """
        Marca subtarefa N como concluída.

        Args:
            task_id: ID da tarefa principal
            etapa: Número da etapa (1-7)
            observacao: Comentário opcional
        """

    def registrar_fechamento(
        self,
        task_id: str,
        resultado: Literal["fechado", "perdido"],
        valor: str = None,
        motivo: str = None,
        observacao: str = None
    ) -> bool:
        """
        Registra fechamento do orçamento.

        Processo:
            1. Adicionar comentário na tarefa com resultado
            2. Marcar subtarefa 7 como concluída
            3. Marcar tarefa principal como concluída
            4. Mover para seção "Concluído"
        """

    def anexar_arquivo(
        self,
        task_id: str,
        file_path: str,
        nome: str = None
    ) -> bool:
        """Anexa arquivo à tarefa."""

    def buscar_tarefas(self, filtros: dict) -> list[dict]:
        """
        Busca tarefas com filtros.

        Filtros possíveis:
            - completed: bool
            - tags: list[str]
            - assignee: str
            - due_on_before: str (YYYY-MM-DD)
            - due_on_after: str (YYYY-MM-DD)
        """
```

**Formatação de Título:**
```python
def formatar_titulo(dados: dict) -> str:
    """
    Formato: [PREFIXOS][TIPO] Cliente - Local

    Exemplos:
        - [INSTALACAO] Empresa ABC - Belo Horizonte
        - [LIC][PROJETO] Prefeitura XYZ - Porto Alegre
        - [MANUTENCAO] Condominio 123 - São Paulo
    """
    prefixos = []

    if dados["eh_licitacao"]:
        prefixos.append("[LIC]")

    tipo = dados["tipo_servico"].upper()
    prefixos.append(f"[{tipo}]")

    cliente = dados["cliente"]
    local = dados["local"]

    return f"{' '.join(prefixos)} {cliente} - {local}"
```

**Formatação de Descrição:**
```python
def formatar_descricao(dados: dict) -> str:
    """
    Template padrão de descrição conforme documentação.
    """
    return f"""DADOS DO ORCAMENTO

Cliente: {dados['cliente']}
CNPJ/CPF: {dados['cnpj_cpf'] or 'N/A'}
Contato: {dados['contato'] or 'N/A'}
Telefone: {dados['telefone'] or 'N/A'}
Email: {dados['email'] or 'N/A'}
Local: {dados['local']}
Prazo do cliente: {formatar_data(dados['prazo'])}

---

DETALHES DA DEMANDA
{dados['descricao']}

---

ORIGEM: {dados['origem'].replace('_', ' ').title()}
LICITACAO: {'Sim - ' + dados['numero_edital'] if dados['eh_licitacao'] else 'Nao'}

---

CLASSIFICACAO
Tipo: {dados['tipo_servico'].title()}
Porte: {dados['porte'].title() if dados['porte'] else 'A definir'}
"""
```

**Gestão de Tags:**
```python
def determinar_tags(dados: dict) -> list[str]:
    """
    Retorna lista de nomes de tags a adicionar.

    Regras:
        - Sempre: tag do tipo_servico
        - Sempre: tag do porte (se definido)
        - Se eh_licitacao: tag "licitacao"
        - Se urgente: tag "urgente"
        - Se cliente_estrategico: tag "cliente-estrategico"
    """
    tags = []

    # Tipo
    tags.append(dados["tipo_servico"])

    # Porte
    if dados["porte"]:
        tags.append(dados["porte"])

    # Flags
    if dados["eh_licitacao"]:
        tags.append("licitacao")

    if dados["urgente"]:
        tags.append("urgente")

    if dados["cliente_estrategico"]:
        tags.append("cliente-estrategico")

    return tags
```

**Retry Logic:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def _api_call(self, method: str, endpoint: str, **kwargs):
    """
    Wrapper para chamadas API com retry automático.

    Estratégia:
        - Até 3 tentativas
        - Espera exponencial: 2s, 4s, 8s
        - Retry em erros 5xx ou timeout
        - Falha imediata em erros 4xx
    """
```

---

### 5. DriveSync (src/sync_drive.py)

**Responsabilidade:** Sincronizar arquivos entre Drive e Asana

**Funcionalidades:**
- Criar estrutura de pastas no Drive para nova demanda
- Detectar novos PDFs em pastas de orçamentos
- Anexar automaticamente PDFs nas tarefas correspondentes
- Manter mapeamento bidirecional de IDs
- Sincronização sob demanda ou automática

**Estrutura de Pastas (Drive):**
```
/2026/
  ├── 26_001_CLIENTE_A/
  │   ├── 01_Projetos/
  │   ├── 02_Levantamento/
  │   ├── 03_Orcamento/        ← PDFs de propostas aqui
  │   │   ├── ORC_26_001_R00.pdf
  │   │   └── ORC_26_001_R01.pdf
  │   ├── 04_Cotacoes/
  │   └── emails_processados/  ← Emails baixados pelo sistema
  │
  ├── 26_002_CLIENTE_B/
  │   └── ...
```

**Mapeamento de IDs (config/ids_mapping.json):**
```json
{
  "26_001": {
    "asana_task_gid": "1234567890123456",
    "drive_folder_id": "1abcdefghijklmnop",
    "created_at": "2026-01-15T10:30:00Z",
    "last_sync": "2026-01-20T14:22:00Z",
    "pdfs_anexados": [
      "ORC_26_001_R00.pdf",
      "ORC_26_001_R01.pdf"
    ]
  },
  "26_002": {
    ...
  }
}
```

**Interface Principal:**
```python
class DriveSync:
    def criar_pasta_demanda(
        self,
        demanda_id: str,
        nome_cliente: str
    ) -> str:
        """
        Cria estrutura de pastas no Drive.

        Args:
            demanda_id: Ex: "26_062"
            nome_cliente: Ex: "Empresa ABC"

        Returns:
            folder_id do Drive

        Processo:
            1. Criar pasta principal: AA_XXX_CLIENTE/
            2. Criar subpastas: 01_Projetos, 02_Levantamento, etc
            3. Criar pasta emails_processados/
            4. Atualizar ids_mapping.json
            5. Retornar folder_id
        """

    def detectar_novos_pdfs(
        self,
        demanda_id: str = None
    ) -> dict[str, list[str]]:
        """
        Detecta PDFs novos em pastas 03_Orcamento.

        Args:
            demanda_id: ID específico ou None para todos

        Returns:
            {
                "26_001": ["ORC_26_001_R02.pdf"],
                "26_004": ["ORC_26_004_R00.pdf"]
            }
        """

    def anexar_pdfs_asana(
        self,
        demanda_id: str,
        pdfs: list[str]
    ) -> bool:
        """
        Baixa PDFs do Drive e anexa no Asana.

        Processo:
            1. Buscar task_gid em ids_mapping
            2. Para cada PDF:
               a. Baixar do Drive para temp
               b. Anexar no Asana via AsanaLib
               c. Limpar arquivo temp
            3. Atualizar lista de pdfs_anexados
            4. Atualizar last_sync
        """

    def sync_demanda(self, demanda_id: str) -> dict:
        """
        Sincronização completa de uma demanda.

        Returns:
            {
                "pdfs_novos": int,
                "pdfs_anexados": int,
                "erros": list[str]
            }
        """

    def sync_all(self) -> dict:
        """Sincroniza todas as demandas."""
```

**Detecção de Mudanças:**
```python
def _get_file_hash(self, file_id: str) -> str:
    """Retorna MD5 hash do arquivo para detectar modificações."""

def _is_new_pdf(self, demanda_id: str, filename: str) -> bool:
    """Verifica se PDF já foi anexado anteriormente."""
    mapping = self._load_mapping()
    if demanda_id not in mapping:
        return True

    pdfs_anexados = mapping[demanda_id].get("pdfs_anexados", [])
    return filename not in pdfs_anexados
```

---

### 6. CLI Orchestrator (src/cli.py)

**Responsabilidade:** Interface de linha de comando e coordenação do pipeline

**Framework:** Click (Python CLI framework)

**Comandos Disponíveis:**

```bash
# Pipeline completo
gestao-orcamentos processar-pasta 26_062 [--confirm] [--dry-run]

# Etapas individuais
gestao-orcamentos buscar-emails 26_062 --query "JBS Seara"
gestao-orcamentos preparar-dados 26_062
gestao-orcamentos extrair-dados 26_062/dados_preparados.md
gestao-orcamentos criar-tarefa 26_062/orcamento.json

# Sincronização Drive
gestao-orcamentos sync-drive 26_062
gestao-orcamentos sync-drive --all

# Consultas
gestao-orcamentos listar-tarefas --urgente
gestao-orcamentos ver-tarefa 26_004

# Utilitários
gestao-orcamentos validar-json orcamento.json
gestao-orcamentos estatisticas --periodo semana
```

**Pipeline do Comando Principal:**

```python
@click.command()
@click.argument("demanda_id")
@click.option("--confirm", is_flag=True, help="Pedir confirmação antes de criar tarefa")
@click.option("--dry-run", is_flag=True, help="Simular sem executar")
@click.option("--verbose", "-v", is_flag=True, help="Modo verbose")
def processar_pasta(demanda_id: str, confirm: bool, dry_run: bool, verbose: bool):
    """
    Processa demanda completa do Drive até criação no Asana.

    Etapas:
        1. Validar pasta Drive existe
        2. Buscar emails relacionados
        3. Preparar dados
        4. Extrair informações (IA)
        5. [Opcional] Confirmar com usuário
        6. Criar tarefa no Asana
        7. Sincronizar arquivos
        8. Gerar relatório
    """
    logger = setup_logger(verbose)

    with Progress() as progress:
        task = progress.add_task(
            f"[cyan]Processando {demanda_id}...",
            total=7
        )

        # Etapa 1: Validação
        progress.update(task, description="[1/7] Validando pasta...")
        if not validar_pasta_drive(demanda_id):
            logger.error(f"Pasta {demanda_id} não encontrada no Drive")
            return

        progress.advance(task)

        # Etapa 2: Buscar emails
        progress.update(task, description="[2/7] Buscando emails...")
        gmail = GmailClient()
        emails = gmail.buscar_emails_demanda(demanda_id)
        logger.info(f"Encontrados {len(emails)} emails")

        if not dry_run:
            for email in emails:
                gmail.baixar_email(email["id"], f"drive/{demanda_id}/emails/")

        progress.advance(task)

        # Etapa 3: Preparar dados
        progress.update(task, description="[3/7] Preparando dados...")
        preparer = DataPreparer()
        dados_preparados = preparer.preparar_pasta(f"drive/{demanda_id}")
        logger.info(f"Dados preparados: {dados_preparados['output_file']}")

        progress.advance(task)

        # Etapa 4: Extração IA
        progress.update(task, description="[4/7] Extraindo dados (IA)...")
        extractor = AIExtractor()
        dados_json = extractor.extrair(dados_preparados["texto_limpo"])
        logger.info(f"Tokens usados: {extractor.last_tokens_used}")

        # Salvar JSON
        json_path = f"drive/{demanda_id}/orcamento.json"
        if not dry_run:
            with open(json_path, "w") as f:
                json.dump(dados_json, f, indent=2, ensure_ascii=False)

        progress.advance(task)

        # Etapa 5: Confirmação (opcional)
        if confirm and not dry_run:
            print("\n" + "="*60)
            print("DADOS EXTRAÍDOS:")
            print(json.dumps(dados_json, indent=2, ensure_ascii=False))
            print("="*60)

            if not click.confirm("\nCriar tarefa no Asana com estes dados?"):
                logger.warning("Operação cancelada pelo usuário")
                return

        progress.advance(task)

        # Etapa 6: Criar no Asana
        progress.update(task, description="[6/7] Criando no Asana...")
        if not dry_run:
            asana = AsanaLib()
            task_gid = asana.criar_orcamento(dados_json)
            logger.success(f"Tarefa criada: {task_gid}")
        else:
            logger.info("[DRY-RUN] Tarefa não foi criada")
            task_gid = "dry_run_task_id"

        progress.advance(task)

        # Etapa 7: Sincronizar arquivos
        progress.update(task, description="[7/7] Sincronizando Drive...")
        if not dry_run:
            sync = DriveSync()
            sync.sync_demanda(demanda_id)

        progress.advance(task)

    # Relatório final
    print_relatorio(demanda_id, task_gid, extractor.last_tokens_used, dry_run)
```

**Logging e Progress:**

```python
def setup_logger(verbose: bool):
    """Configura logger com cores e níveis."""
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    return logging.getLogger("gestao-orcamentos")

def print_relatorio(demanda_id, task_gid, tokens, dry_run):
    """Imprime relatório final formatado."""
    from rich.console import Console
    from rich.table import Table

    console = Console()

    table = Table(title=f"Relatório - {demanda_id}")
    table.add_column("Item", style="cyan")
    table.add_column("Valor", style="green")

    table.add_row("Status", "✓ Concluído" if not dry_run else "🔍 Dry-run")
    table.add_row("Tarefa Asana", task_gid)
    table.add_row("Tokens usados", str(tokens))
    table.add_row("Custo estimado", f"${tokens * 0.0015 / 1000:.4f}")

    console.print(table)
```

---

## 🔄 Fluxo de Dados Detalhado

### Cenário: Processar Nova Demanda

**Input inicial:**
- Pasta no Drive: `26_062_EMPRESA_XYZ/`
- Contém: emails em `.eml`, anotações em `.txt`, PDFs

**Passo a Passo:**

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. COLETA (GmailClient)                                          │
├──────────────────────────────────────────────────────────────────┤
│ Input:  demanda_id = "26_062"                                    │
│         query = "from:cliente@empresa.com subject:climatização"  │
│                                                                  │
│ Processo:                                                        │
│  • Autenticar com Gmail API                                      │
│  • Buscar emails com query                                       │
│  • Para cada email:                                              │
│    - Baixar corpo (.txt)                                         │
│    - Baixar anexos (se houver)                                   │
│    - Salvar em: drive/26_062/emails_processados/                 │
│                                                                  │
│ Output: 3 arquivos .txt + 2 PDFs salvos                          │
│ Custo:  0 tokens                                                 │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 2. PREPARAÇÃO (DataPreparer)                                     │
├──────────────────────────────────────────────────────────────────┤
│ Input:  drive/26_062/emails_processados/*.txt                    │
│         drive/26_062/anotacoes.txt                               │
│                                                                  │
│ Processo:                                                        │
│  • Ler todos arquivos .txt                                       │
│  • Para cada arquivo:                                            │
│    - Remover HTML se presente                                    │
│    - Detectar e remover assinatura                               │
│    - Extrair metadados via regex:                                │
│      * CNPJ: 12.345.678/0001-90                                  │
│      * Telefone: (51) 99999-8888                                 │
│      * Email: contato@empresa.com                                │
│  • Consolidar em um único .md estruturado                        │
│  • Adicionar metadados detectados                                │
│                                                                  │
│ Output: drive/26_062/dados_preparados.md (~800 palavras)         │
│ Custo:  0 tokens                                                 │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 3. EXTRAÇÃO (AIExtractor com Haiku)                              │
├──────────────────────────────────────────────────────────────────┤
│ Input:  dados_preparados.md                                      │
│                                                                  │
│ Processo:                                                        │
│  • Ler conteúdo do .md                                           │
│  • Montar prompt otimizado para Haiku                            │
│  • Chamar Claude API:                                            │
│    - Model: claude-haiku-4-20250514                              │
│    - Max tokens: 1000                                            │
│    - Temperature: 0 (determinístico)                             │
│  • Receber resposta JSON                                         │
│  • Validar com Pydantic schema                                   │
│  • Se validação falhar:                                          │
│    - Tentar novamente com Sonnet                                 │
│  • Salvar JSON validado                                          │
│                                                                  │
│ Output: drive/26_062/orcamento.json                              │
│ Custo:  ~700 tokens (~$0.0015)                                   │
│                                                                  │
│ JSON de saída:                                                   │
│ {                                                                │
│   "cliente": "Empresa XYZ Ltda",                                 │
│   "cnpj_cpf": "12.345.678/0001-90",                              │
│   "contato": "João Silva",                                       │
│   "telefone": "(51) 99999-8888",                                 │
│   "email": "joao@empresa.com",                                   │
│   "local": "Porto Alegre - RS",                                  │
│   "prazo": "2026-02-15",                                         │
│   "tipo_servico": "instalacao",                                  │
│   "eh_licitacao": false,                                         │
│   "numero_edital": null,                                         │
│   "porte": "medio",                                              │
│   "origem": "comercial",                                         │
│   "descricao": "Instalação de sistema split...",                 │
│   "urgente": true,                                               │
│   "cliente_estrategico": false                                   │
│ }                                                                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 4. CRIAÇÃO ASANA (AsanaLib)                                      │
├──────────────────────────────────────────────────────────────────┤
│ Input:  orcamento.json                                           │
│                                                                  │
│ Processo:                                                        │
│  1. Formatar título:                                             │
│     "[INSTALACAO] Empresa XYZ Ltda - Porto Alegre"               │
│                                                                  │
│  2. Formatar descrição (template padrão)                         │
│                                                                  │
│  3. Criar tarefa principal via MCP:                              │
│     POST /tasks                                                  │
│     {                                                            │
│       "name": "[INSTALACAO] Empresa XYZ...",                     │
│       "notes": "DADOS DO ORCAMENTO\n...",                        │
│       "projects": ["1212920325558530"],                          │
│       "due_on": "2026-02-15"                                     │
│     }                                                            │
│     → Retorna task_gid: "1234567890123456"                       │
│                                                                  │
│  4. Criar 7 subtarefas (ordem reversa):                          │
│     POST /tasks/{task_gid}/subtasks × 7                          │
│                                                                  │
│  5. Adicionar tags:                                              │
│     POST /tasks/{task_gid}/addTag                                │
│     - instalacao                                                 │
│     - medio                                                      │
│     - urgente                                                    │
│                                                                  │
│  6. Atualizar ids_mapping.json:                                  │
│     "26_062": {"asana_task_gid": "1234567890123456", ...}        │
│                                                                  │
│ Output: Tarefa criada no Asana (ID: 1234567890123456)            │
│ Custo:  0 tokens (API calls)                                     │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 5. SINCRONIZAÇÃO (DriveSync)                                     │
├──────────────────────────────────────────────────────────────────┤
│ Input:  demanda_id = "26_062"                                    │
│                                                                  │
│ Processo:                                                        │
│  • Verificar pasta 03_Orcamento/ no Drive                        │
│  • Detectar PDFs: [proposta_v1.pdf]                              │
│  • Baixar PDF para temp                                          │
│  • Anexar no Asana:                                              │
│    POST /tasks/{task_gid}/attachments                            │
│  • Atualizar ids_mapping com lista de PDFs anexados              │
│  • Limpar arquivo temp                                           │
│                                                                  │
│ Output: 1 PDF anexado na tarefa                                  │
│ Custo:  0 tokens                                                 │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 6. RELATÓRIO FINAL                                               │
├──────────────────────────────────────────────────────────────────┤
│ ✓ Demanda 26_062 processada com sucesso                          │
│                                                                  │
│ Tarefa Asana:  1234567890123456                                  │
│ Link: https://app.asana.com/0/1212920325558530/1234567890123456  │
│                                                                  │
│ Tokens usados:    700                                            │
│ Custo estimado:   $0.0015                                        │
│ Tempo total:      ~90 segundos                                   │
│                                                                  │
│ Arquivos processados:                                            │
│  • 3 emails baixados                                             │
│  • 1 anotação processada                                         │
│  • 1 PDF anexado                                                 │
│                                                                  │
│ Próximos passos:                                                 │
│  → Coordenador faz triagem (subtarefa 1)                         │
└──────────────────────────────────────────────────────────────────┘
```

### Comparação de Custos - Exemplo Real

**Demanda típica:**
- 3 emails com ~500 palavras cada
- 1 anotação com ~200 palavras
- Total texto bruto: ~1700 palavras = ~2300 tokens

**Abordagem Antiga (tudo IA):**
```
Prompt com texto bruto:      2300 tokens input
Instruções e exemplos:       1000 tokens input
Resposta JSON:                500 tokens output
────────────────────────────────────────────────
Total:                       3800 tokens
Custo (Sonnet):              $0.023
```

**Abordagem Nova (scripts + Haiku):**
```
Script limpa dados:             0 tokens
Script extrai metadados:        0 tokens
Texto preparado:              500 tokens input (70% redução!)
Prompt otimizado:             150 tokens input
Resposta JSON:                 50 tokens output
────────────────────────────────────────────────
Total:                        700 tokens
Custo (Haiku):               $0.0015
────────────────────────────────────────────────
Economia:                    93.5% ($0.0215 por demanda)
```

---

## 🎯 Decisões de Design

### 1. Por que Scripts ao invés de IA para Preparação?

**Decisão:** Usar scripts Python com regex para limpeza e extração de metadados

**Justificativa:**
- **Custo:** Regex é gratuito, IA custa por token
- **Velocidade:** Regex processa em milissegundos, API tem latência
- **Determinismo:** Regex é 100% consistente, IA pode variar
- **Dados estruturados:** CNPJ, telefone, email são padrões conhecidos

**Trade-off aceito:**
- Menos flexível que IA (precisa manter regexes atualizadas)
- Não entende contexto (ex: "ligação do João" não extrai nome)

**Mitigação:**
- IA complementa gaps de informação na etapa seguinte
- Regex cobre 90%+ dos casos comuns

---

### 2. Por que Haiku ao invés de Sonnet por padrão?

**Decisão:** Usar Haiku como modelo primário, Sonnet como fallback

**Justificativa:**
- **Custo:** Haiku é 12x mais barato que Sonnet
- **Velocidade:** Haiku é ~2x mais rápido
- **Adequação:** Texto preparado é simples, Haiku consegue processar
- **Escala:** Permite processar 12x mais demandas pelo mesmo custo

**Trade-off aceito:**
- Haiku pode errar mais em casos complexos/ambíguos
- Precisamos validar output com mais rigor

**Mitigação:**
- Validação rigorosa com Pydantic
- Fallback automático para Sonnet se validação falhar
- Monitorar taxa de sucesso e ajustar threshold

---

### 3. Por que MCP Asana e não API direto?

**Decisão:** Usar MCP Asana Server como camada primária

**Justificativa:**
- **Integração nativa:** Já funciona dentro do Claude Code
- **Menos código:** Não precisa gerenciar autenticação/tokens
- **Consistência:** Mesma interface que IA usa
- **Futuro:** Se MCP evoluir, ganhamos features grátis

**Trade-off aceito:**
- Dependência de ferramenta externa (MCP)
- Se MCP cair, precisamos fallback para API direta

**Mitigação:**
- Implementar wrapper com fallback para requests direto
- Abstrair chamadas MCP em AsanaLib (fácil trocar implementação)

---

### 4. Por que Mapeamento JSON ao invés de Banco de Dados?

**Decisão:** Usar arquivo `ids_mapping.json` para mapear IDs

**Justificativa:**
- **Simplicidade:** JSON é fácil ler, editar, versionar (git)
- **Sem dependências:** Não precisa instalar/configurar DB
- **Volume baixo:** ~100 demandas/mês = arquivo pequeno (~50KB)
- **Portabilidade:** Fácil fazer backup, compartilhar

**Trade-off aceito:**
- Não escala para milhões de registros
- Leitura/escrita não é atômica (race conditions possíveis)
- Sem queries complexas

**Mitigação:**
- Lock file durante escrita
- Se volume crescer muito (>10k demandas), migrar para SQLite
- Backup automático do JSON

---

### 5. Por que Estrutura Modular?

**Decisão:** Separar funcionalidades em módulos independentes

**Justificativa:**
- **Testabilidade:** Fácil testar cada componente isoladamente
- **Manutenibilidade:** Mudanças em um módulo não afetam outros
- **Reutilização:** Funções podem ser usadas em diferentes contextos
- **Clareza:** Cada arquivo tem propósito único e claro

**Exemplo:**
```
# Ruim (tudo em um arquivo)
gestao_orcamentos.py (3000 linhas)

# Bom (modular)
src/
  gmail_client.py        (300 linhas)
  prepare_data.py        (250 linhas)
  asana_lib.py           (400 linhas)
  sync_drive.py          (350 linhas)
  cli.py                 (500 linhas)
```

---

### 6. Por que CLI ao invés de GUI?

**Decisão:** Interface de linha de comando (CLI)

**Justificativa:**
- **Automação:** Fácil chamar de scripts, cron jobs
- **Eficiência:** Usuários técnicos preferem CLI
- **Simplicidade:** Menos código que GUI
- **Integrável:** Pode ser usado por outras ferramentas

**Trade-off aceito:**
- Menos amigável para usuários não-técnicos
- Curva de aprendizado inicial

**Mitigação:**
- Ajuda detalhada (`--help`)
- Exemplos claros na documentação
- Skills padronizadas para Claude usar CLI

---

## 🔌 Interfaces e Contratos

### Contrato de Dados: JSON de Orçamento

**Schema completo:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["cliente", "local", "tipo_servico", "descricao"],
  "properties": {
    "cliente": {
      "type": "string",
      "description": "Nome completo do cliente (empresa ou pessoa)",
      "minLength": 3,
      "examples": ["Empresa ABC Ltda", "João da Silva"]
    },
    "cnpj_cpf": {
      "type": ["string", "null"],
      "pattern": "^(\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}|\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2})$",
      "description": "CNPJ ou CPF formatado"
    },
    "contato": {
      "type": ["string", "null"],
      "description": "Nome da pessoa de contato"
    },
    "telefone": {
      "type": ["string", "null"],
      "pattern": "^\\(?\\d{2}\\)?\\s?\\d{4,5}-?\\d{4}$",
      "description": "Telefone no formato brasileiro"
    },
    "email": {
      "type": ["string", "null"],
      "format": "email",
      "description": "Email de contato"
    },
    "local": {
      "type": "string",
      "pattern": "^.+ - [A-Z]{2}$",
      "description": "Local no formato: Cidade - UF",
      "examples": ["Porto Alegre - RS", "Belo Horizonte - MG"]
    },
    "prazo": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Data limite no formato YYYY-MM-DD"
    },
    "tipo_servico": {
      "type": "string",
      "enum": ["instalacao", "manutencao", "projeto"],
      "description": "Tipo de serviço solicitado"
    },
    "eh_licitacao": {
      "type": "boolean",
      "default": false,
      "description": "Se é processo licitatório"
    },
    "numero_edital": {
      "type": ["string", "null"],
      "description": "Número do edital se licitação"
    },
    "porte": {
      "type": ["string", "null"],
      "enum": ["pequeno", "medio", "grande", null],
      "description": "Porte estimado do projeto"
    },
    "origem": {
      "type": "string",
      "enum": ["comercial", "cliente_direto", "diretoria", "engenharia"],
      "description": "Origem da demanda"
    },
    "descricao": {
      "type": "string",
      "minLength": 10,
      "description": "Descrição detalhada do que foi solicitado"
    },
    "urgente": {
      "type": "boolean",
      "default": false,
      "description": "Se possui urgência alta"
    },
    "cliente_estrategico": {
      "type": "boolean",
      "default": false,
      "description": "Se é cliente estratégico"
    }
  }
}
```

### Interface: GmailClient ↔ DataPreparer

**Output do GmailClient:**
```python
{
    "emails_baixados": [
        {
            "id": "18d1f2a3b4c5d6e7",
            "subject": "Orçamento climatização",
            "from": "joao@empresa.com",
            "date": "2026-01-25T14:30:00Z",
            "arquivo": "drive/26_062/emails/email_001.txt",
            "anexos": ["drive/26_062/emails/anexo_001.pdf"]
        }
    ],
    "total": 3
}
```

**Input esperado pelo DataPreparer:**
- Arquivos `.txt` salvos em pasta específica
- Um arquivo por email
- Formato UTF-8

### Interface: DataPreparer ↔ AIExtractor

**Output do DataPreparer:**
```markdown
# Dados Preparados - 26_062

## Metadados do Email
- **De:** João Silva <joao@empresa.com>
- **Para:** orcamentos2@armant.com.br
- **Data:** 2026-01-25 14:30
- **Assunto:** Orçamento climatização sala reuniões

## Metadados Detectados
- **CNPJ:** 12.345.678/0001-90
- **Telefones:** (51) 99999-8888
- **Emails:** joao@empresa.com

## Conteúdo Principal
[Texto limpo]
```

**Input esperado pelo AIExtractor:**
- Arquivo `.md` no formato acima
- Máximo ~2000 palavras (para caber em contexto Haiku)
- UTF-8 encoding

### Interface: AIExtractor ↔ AsanaLib

**Output do AIExtractor:**
```python
{
    "cliente": "Empresa XYZ",
    "cnpj_cpf": "12.345.678/0001-90",
    ...
}
# Schema validado com Pydantic
```

**Input esperado pelo AsanaLib:**
- Dict Python com todos campos do schema
- Campos obrigatórios presentes
- Formatos validados

---

## ⚠️ Tratamento de Erros

### Estratégia Geral

1. **Fail Fast:** Validar inputs no início de cada função
2. **Logging Detalhado:** Registrar contexto do erro
3. **Retry Inteligente:** Tentar novamente em erros temporários
4. **Fallback Gracioso:** Continuar com funcionalidade reduzida se possível
5. **User-Friendly:** Mensagens claras e acionáveis

### Hierarquia de Exceções

```python
class GestaoOrcamentosError(Exception):
    """Exceção base do sistema."""
    pass

class GmailAPIError(GestaoOrcamentosError):
    """Erro ao comunicar com Gmail API."""
    pass

class DataPreparationError(GestaoOrcamentosError):
    """Erro durante preparação de dados."""
    pass

class AIExtractionError(GestaoOrcamentosError):
    """Erro durante extração com IA."""
    pass

class AsanaAPIError(GestaoOrcamentosError):
    """Erro ao comunicar com Asana API."""
    pass

class ValidationError(GestaoOrcamentosError):
    """Erro de validação de dados."""
    pass
```

### Casos de Erro Comuns

#### 1. Gmail API - Quota Excedida

**Erro:**
```
google.api_core.exceptions.TooManyRequests: 429 Quota exceeded
```

**Tratamento:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception_type(TooManyRequests)
)
def buscar_emails(query):
    ...
```

**Ação:** Esperar e tentar novamente com backoff exponencial

#### 2. IA - Resposta Inválida

**Erro:**
```
Resposta da IA não é JSON válido ou não passa validação Pydantic
```

**Tratamento:**
```python
try:
    dados = extrair_com_haiku(texto)
    validar_schema(dados)
except (JSONDecodeError, ValidationError) as e:
    logger.warning(f"Haiku falhou: {e}")
    logger.info("Tentando com Sonnet...")
    dados = extrair_com_sonnet(texto)
    validar_schema(dados)  # Se falhar aqui, propaga exceção
```

**Ação:** Fallback para modelo mais robusto

#### 3. Asana - Tarefa Não Encontrada

**Erro:**
```
AsanaAPIError: Task not found (404)
```

**Tratamento:**
```python
def buscar_tarefa(task_id: str):
    try:
        return asana_client.tasks.get_task(task_id)
    except NotFound:
        logger.error(f"Tarefa {task_id} não encontrada")
        # Buscar em ids_mapping se foi movida/renomeada
        mapping = load_ids_mapping()
        # ...
        raise AsanaAPIError(f"Tarefa {task_id} não encontrada no Asana")
```

**Ação:** Informar usuário e sugerir verificar no Asana

#### 4. Drive - Arquivo Não Existe

**Erro:**
```
FileNotFoundError: Pasta drive/26_062 não encontrada
```

**Tratamento:**
```python
def validar_pasta_drive(demanda_id: str):
    pasta = f"drive/{demanda_id}"
    if not os.path.exists(pasta):
        raise ValidationError(
            f"Pasta {pasta} não encontrada. "
            f"Crie a pasta ou verifique se o ID está correto."
        )
```

**Ação:** Mensagem clara de como resolver

#### 5. Rede - Timeout

**Erro:**
```
requests.exceptions.Timeout
```

**Tratamento:**
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(5),
    retry=retry_if_exception_type(Timeout)
)
def chamada_api_com_timeout():
    return requests.get(url, timeout=30)
```

**Ação:** Retry automático com timeout maior

### Logging de Erros

```python
import logging
from rich.logging import RichHandler

logger = logging.getLogger("gestao-orcamentos")

try:
    processar_demanda(demanda_id)
except GestaoOrcamentosError as e:
    logger.error(
        f"Erro ao processar demanda {demanda_id}",
        exc_info=True,
        extra={
            "demanda_id": demanda_id,
            "error_type": type(e).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )
    # Salvar em arquivo de erro para debug
    with open(f"logs/erro_{demanda_id}.log", "w") as f:
        f.write(traceback.format_exc())
```

---

## 🔐 Segurança

### Credenciais e Secrets

**Armazenamento:**
```
config/
  ├── gmail_credentials.json      # OAuth credentials (gitignored)
  ├── gmail_token.json            # Access token (gitignored)
  └── settings.local.json         # Config local (gitignored)

.env                              # Variáveis de ambiente (gitignored)
```

**.gitignore:**
```
config/gmail_credentials.json
config/gmail_token.json
config/settings.local.json
.env
*.log
drive/*/emails_processados/
```

**Variáveis de Ambiente:**
```bash
# .env
ASANA_ACCESS_TOKEN=...
CLAUDE_API_KEY=...
GOOGLE_DRIVE_ROOT=/Users/.../GoogleDrive/.../2026
```

### Permissões de APIs

**Gmail API - Scopes mínimos:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Ler emails
    'https://www.googleapis.com/auth/gmail.modify'     # Marcar como lido
]
```

**Asana API - Personal Access Token:**
- Criar em: https://app.asana.com/0/my-apps
- Permissões: Leitura + Escrita no workspace
- Rotação: A cada 6 meses

**Google Drive API:**
- Acesso limitado às pastas específicas
- Sem permissão de deletar

### Dados Sensíveis

**Anonimização em Logs:**
```python
def sanitize_log(data: dict) -> dict:
    """Remove dados sensíveis antes de logar."""
    sensitive_fields = ["cnpj_cpf", "telefone", "email"]

    sanitized = data.copy()
    for field in sensitive_fields:
        if field in sanitized and sanitized[field]:
            # Mascarar parcialmente
            sanitized[field] = mask_value(sanitized[field])

    return sanitized

def mask_value(value: str) -> str:
    """Mascara valor mantendo primeiros e últimos caracteres."""
    if len(value) <= 4:
        return "***"
    return f"{value[:2]}***{value[-2:]}"
```

**Exemplo:**
```python
# Antes de logar
logger.info(f"Dados extraídos: {sanitize_log(dados)}")

# Output
# CNPJ: 12***90 (ao invés de 12.345.678/0001-90)
# Email: jo***om (ao invés de joao@empresa.com)
```

### Validação de Inputs

**Prevenção de Injection:**
```python
def validar_demanda_id(demanda_id: str):
    """Valida formato do ID de demanda."""
    pattern = r'^\d{2}_\d{3}$'
    if not re.match(pattern, demanda_id):
        raise ValidationError(
            f"ID inválido: {demanda_id}. "
            f"Formato esperado: AA_XXX (ex: 26_062)"
        )

def validar_query_gmail(query: str):
    """Sanitiza query para Gmail API."""
    # Remover caracteres potencialmente perigosos
    forbidden = [';', '|', '&', '$', '`']
    for char in forbidden:
        if char in query:
            raise ValidationError(
                f"Caractere não permitido na query: {char}"
            )
```

---

## ⚡ Performance e Escalabilidade

### Métricas de Performance

**Tempo de Processamento (Target):**

| Etapa | Tempo Esperado | Gargalo |
|-------|----------------|---------|
| 1. Coleta Gmail | 5-10s | Latência API |
| 2. Preparação | 1-2s | Processamento local |
| 3. Extração IA | 3-5s | Latência Claude API |
| 4. Criação Asana | 3-5s | Latência Asana API |
| 5. Sync Drive | 2-4s | Download/Upload arquivos |
| **Total** | **14-26s** | APIs externas |

**Volume Suportado:**

| Métrica | Atual | Com Otimização | Limite Teórico |
|---------|-------|----------------|----------------|
| Demandas/dia | 30 | 100 | 1000+ |
| Emails processados/dia | 90 | 300 | 5000 |
| Tokens/dia | 21k | 70k | 1M |
| Custo/dia | $0.045 | $0.15 | $2.50 |

### Otimizações Implementadas

#### 1. Batch Processing de Emails

```python
def buscar_emails_batch(queries: list[str]) -> dict:
    """Busca múltiplas queries em uma chamada."""
    # Ao invés de N chamadas API
    # Fazer 1 chamada com query complexa
    combined_query = " OR ".join(f"({q})" for q in queries)
    return gmail.buscar_emails(combined_query)
```

**Ganho:** 5x menos chamadas API

#### 2. Cache de Resultados

```python
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=100)
@ttl_cache(ttl=timedelta(hours=1))
def get_asana_tags() -> dict:
    """Cache de tags do Asana (não mudam frequentemente)."""
    return asana.tags.get_tags_for_workspace(WORKSPACE_ID)
```

**Ganho:** Evita chamadas repetidas

#### 3. Processamento Paralelo

```python
from concurrent.futures import ThreadPoolExecutor

def processar_multiplas_demandas(demanda_ids: list[str]):
    """Processa demandas em paralelo."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(processar_demanda, did)
            for did in demanda_ids
        ]

        for future in as_completed(futures):
            try:
                resultado = future.result()
                logger.info(f"Sucesso: {resultado}")
            except Exception as e:
                logger.error(f"Erro: {e}")
```

**Ganho:** 4-5x mais rápido para múltiplas demandas

#### 4. Compressão de Dados Preparados

```python
def comprimir_texto(texto: str) -> str:
    """Remove redundâncias mantendo informação."""
    # Remover linhas vazias consecutivas
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    # Remover espaços múltiplos
    texto = re.sub(r' {2,}', ' ', texto)

    # Truncar em 2000 palavras (suficiente para extração)
    palavras = texto.split()
    if len(palavras) > 2000:
        texto = ' '.join(palavras[:2000]) + "\n[...truncado]"

    return texto
```

**Ganho:** ~30% redução de tokens

### Limites e Bottlenecks

#### Gmail API

**Quotas (gratuitas):**
- 1 bilhão requisições/dia (ok)
- 250 requisições/segundo (ok)

**Bottleneck:** Latência de rede (~300-500ms por chamada)

**Mitigação:**
- Batch requests quando possível
- Cache de resultados
- Buscar apenas emails necessários (query específica)

#### Claude API

**Quotas (pagas):**
- Haiku: Sem limite definido
- Rate limit: ~50 requisições/segundo

**Bottleneck:** Latência (2-4s por extração)

**Mitigação:**
- Processar múltiplas demandas em paralelo
- Usar Haiku (mais rápido que Sonnet)
- Reduzir tamanho do input (preparação eficiente)

#### Asana API

**Quotas (gratuitas):**
- 1500 requisições/minuto por workspace
- ~100 requisições para criar 1 orçamento completo

**Bottleneck:** Criar subtarefas sequencialmente (7 chamadas)

**Mitigação:**
- Considerar criar subtarefas em paralelo (se API permitir)
- Usar batch endpoints se disponíveis

### Escalabilidade Futura

**Cenário: 10x mais demandas (300/dia)**

Necessário:
1. **Infraestrutura:**
   - VPS ou cloud para rodar scheduler 24/7
   - Banco de dados (SQLite → PostgreSQL)

2. **Código:**
   - Fila de processamento (Celery + Redis)
   - Workers paralelos
   - Monitoramento e alertas

3. **Custos:**
   - Claude API: ~$1.50/dia
   - Infraestrutura: ~$10-20/mês (VPS básico)
   - Total: ~$60-80/mês

**Retorno:** Economiza ~20-30 horas/mês de trabalho manual

---

## 📦 Requisitos e Dependências

### Requisitos de Sistema

**Python:** 3.10+

**Sistema Operacional:** macOS, Linux, Windows (WSL recomendado)

**Espaço em Disco:** ~500 MB (código + dependências + dados)

**Memória RAM:** Mínimo 2GB livre

**Conexão Internet:** Necessária (acesso a APIs)

### Dependências Python

**requirements.txt:**
```txt
# Core
anthropic>=0.30.0              # Claude API
click>=8.1.0                   # CLI framework
requests>=2.31.0               # HTTP requests
python-dotenv>=1.0.0           # .env support

# Gmail API
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
google-api-python-client>=2.100.0

# Processamento de dados
beautifulsoup4>=4.12.0         # HTML parsing
html2text>=2020.1.16           # HTML → Markdown
pydantic>=2.0.0                # Validação de schema

# Asana (se não usar MCP)
asana>=3.2.0                   # Cliente oficial Asana

# CLI e UX
rich>=13.5.0                   # Terminal formatado
rich-click>=1.7.0              # Click + Rich

# Retry e robustez
tenacity>=8.2.3                # Retry logic

# Testes (opcional)
pytest>=7.4.0
pytest-cov>=4.1.0
```

### Serviços Externos

| Serviço | Custo | Quota | Necessário Para |
|---------|-------|-------|-----------------|
| **Gmail API** | Gratuito | 1B req/dia | Buscar emails |
| **Google Drive API** | Gratuito | 20k req/dia | Acessar arquivos |
| **Asana API** | Gratuito (plano free) | 1500 req/min | Criar tarefas |
| **Claude API** | Pago | Haiku: $0.25/$1.25 por M tokens | Extração de dados |

### Configuração Inicial

**1. Google Cloud (Gmail + Drive):**
```bash
# Criar projeto em: https://console.cloud.google.com
# Habilitar APIs: Gmail API, Drive API
# Criar credenciais OAuth 2.0
# Baixar credentials.json → config/gmail_credentials.json
```

**2. Asana:**
```bash
# Criar Personal Access Token em:
# https://app.asana.com/0/my-apps

# Adicionar em .env:
echo "ASANA_ACCESS_TOKEN=..." >> .env
```

**3. Claude API:**
```bash
# Obter API key em: https://console.anthropic.com

# Adicionar em .env:
echo "CLAUDE_API_KEY=..." >> .env
```

**4. Variáveis de Ambiente (.env):**
```bash
# APIs
ASANA_ACCESS_TOKEN=0/abc123def456...
CLAUDE_API_KEY=sk-ant-api03-...

# Configuração
GOOGLE_DRIVE_ROOT=/Users/.../GoogleDrive/.../2026
ASANA_PROJECT_ID=1212920325558530
ASANA_WORKSPACE_ID=1204197108826498

# Opcional
LOG_LEVEL=INFO
DRY_RUN=false
```

### Instalação

```bash
# 1. Clonar repositório
git clone [repo_url]
cd gestao-orcamentos

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar credenciais
cp .env.example .env
# Editar .env com suas credenciais

# 5. Configurar Gmail
python src/gmail_client.py --setup
# Seguir fluxo OAuth no navegador

# 6. Testar instalação
python src/cli.py --version
python src/cli.py test-conexoes
```

---

## 🔄 Próximos Passos

Após completar esta arquitetura, os próximos passos são:

1. **Implementar cada componente** (Tarefas 2-6)
2. **Testar integração end-to-end**
3. **Documentar uso** (Tarefa 9)
4. **Criar skills para Claude** (Tarefa 7)
5. **Preparar automação** (Tarefa 10)

---

**Documento vivo - será atualizado conforme implementação progride**

**Última atualização:** 30/01/2026

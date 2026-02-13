# Integração com Asana - Guia Completo

Este guia explica como integrar a AsanaLib com o Asana real, seja via MCP (Model Context Protocol) ou API direta.

---

## 📋 Situação Atual

A AsanaLib (`src/asana_lib.py`) está implementada com **interface completa** mas em **modo simulação**. Isso significa:

✅ **Implementado:**
- Formatação de títulos e descrições
- Lógica de tags e metadados
- Estrutura de subtarefas
- Validações e tratamento de erros
- Testes unitários completos

⏳ **Pendente:**
- Conexão real com API/MCP do Asana
- Criação efetiva de tarefas
- Upload de anexos
- Buscas e atualizações

---

## 🔌 Opções de Integração

### Opção 1: MCP Asana (Recomendado para Claude Code)

**Quando usar:**
- Rodando dentro do Claude Code
- MCP Asana já configurado
- Prefere não gerenciar credenciais manualmente

**Vantagens:**
- ✅ Integração nativa com Claude
- ✅ Sem necessidade de gerenciar tokens manualmente
- ✅ Funciona automaticamente se MCP configurado

**Desvantagens:**
- ❌ Só funciona dentro do Claude Code
- ❌ Não pode ser usado em scripts Python standalone

---

### Opção 2: API Direta do Asana (Mais Flexível)

**Quando usar:**
- Scripts Python standalone
- Automação via cron jobs
- Integração em outros sistemas
- Maior controle sobre requisições

**Vantagens:**
- ✅ Funciona em qualquer ambiente Python
- ✅ Mais controle e flexibilidade
- ✅ Pode ser usado em produção

**Desvantagens:**
- ❌ Requer gerenciar Personal Access Token
- ❌ Mais código para implementar

---

## 🚀 Implementação - Opção 1: MCP Asana

### Passo 1: Verificar MCP Disponível

O MCP Asana só está disponível quando rodando dentro do Claude Code. Para verificar:

```python
# Dentro do Claude Code, MCPs são acessíveis via tool calls
# Não há SDK Python direto para MCP
```

### Passo 2: Usar MCP via Claude Code

Quando usando Claude Code, você pode invocar ferramentas MCP diretamente:

```python
# Exemplo conceitual (real implementação depende de Claude Code SDK)
from claude_code import mcp

# Criar tarefa via MCP
response = mcp.call_tool(
    "mcp__claude_ai_Asana__asana_create_task",
    {
        "name": "Nova Tarefa",
        "notes": "Descrição",
        "projects": [PROJECT_ID]
    }
)
```

### Passo 3: Adaptar AsanaLib para MCP

Modificar `src/asana_lib.py` para usar MCP:

```python
def _criar_tarefa_asana(self, task_data: Dict) -> str:
    """Cria tarefa via MCP."""
    from claude_code import mcp

    response = mcp.call_tool(
        "mcp__claude_ai_Asana__asana_create_task",
        task_data
    )

    return response["gid"]
```

---

## 🚀 Implementação - Opção 2: API Direta (Recomendado)

### Passo 1: Obter Personal Access Token

1. Acesse: https://app.asana.com/0/my-apps
2. Clique em **"+ Create new token"**
3. Dê um nome: `gestao-orcamentos`
4. Copie o token (guarde com segurança!)
5. Adicione ao `.env`:
   ```bash
   ASANA_ACCESS_TOKEN=0/abc123def456...
   ```

### Passo 2: Instalar SDK do Asana

```bash
pip install asana
```

(Já está no `requirements.txt`)

### Passo 3: Implementar Métodos na AsanaLib

Modificar `src/asana_lib.py`:

```python
import asana

class AsanaLib:
    def __init__(self, ...):
        # ... código existente ...

        # Adicionar cliente Asana
        self.asana_token = os.environ.get("ASANA_ACCESS_TOKEN")
        if self.asana_token:
            self.asana_client = asana.Client.access_token(self.asana_token)
            logger.info("Cliente Asana API inicializado")
        else:
            self.asana_client = None
            logger.warning("ASANA_ACCESS_TOKEN não configurado - modo simulação")

    def _criar_tarefa_asana(self, task_data: Dict) -> str:
        """Cria tarefa via API direta."""
        if not self.asana_client:
            # Fallback para modo simulação
            import uuid
            return str(uuid.uuid4())[:16]

        try:
            # Criar tarefa via API
            result = self.asana_client.tasks.create(task_data)
            task_gid = result["gid"]
            logger.info(f"Tarefa criada no Asana: {task_gid}")
            return task_gid

        except Exception as e:
            logger.error(f"Erro ao criar tarefa via API: {e}")
            raise AsanaLibError(f"Falha na API Asana: {e}")

    def _criar_subtarefas(self, parent_task_id: str) -> List[str]:
        """Cria subtarefas via API."""
        if not self.asana_client:
            return [str(uuid.uuid4())[:16] for _ in SUBTAREFAS_PADRAO]

        subtarefas_ids = []

        for subtarefa in SUBTAREFAS_PADRAO:
            try:
                result = self.asana_client.tasks.create_subtask_for_task(
                    parent_task_id,
                    {
                        "name": subtarefa["nome"],
                        "notes": subtarefa["notes"]
                    }
                )
                subtarefas_ids.append(result["gid"])
                logger.debug(f"Subtarefa criada: {subtarefa['nome']}")

            except Exception as e:
                logger.error(f"Erro ao criar subtarefa: {e}")
                # Continuar com as outras

        return subtarefas_ids

    def _adicionar_tags(self, task_id: str, tags: List[str]) -> bool:
        """Adiciona tags via API."""
        if not self.asana_client:
            return True

        try:
            # Primeiro, obter ou criar tags
            for tag_name in tags:
                # Buscar tag existente
                tag_gid = self._obter_ou_criar_tag(tag_name)

                # Adicionar tag à tarefa
                self.asana_client.tasks.add_tag_for_task(
                    task_id,
                    {"tag": tag_gid}
                )

            logger.info(f"Tags adicionadas: {', '.join(tags)}")
            return True

        except Exception as e:
            logger.error(f"Erro ao adicionar tags: {e}")
            return False

    def _obter_ou_criar_tag(self, tag_name: str) -> str:
        """Obtém GID de tag existente ou cria nova."""
        # Verificar cache
        if tag_name in self._cache_tags:
            return self._cache_tags[tag_name]

        # Buscar tag no workspace
        tags = self.asana_client.tags.get_tags_for_workspace(
            self.workspace_id,
            opt_fields=["name", "gid"]
        )

        for tag in tags:
            if tag["name"] == tag_name:
                self._cache_tags[tag_name] = tag["gid"]
                return tag["gid"]

        # Tag não existe, criar
        new_tag = self.asana_client.tags.create_tag_for_workspace(
            self.workspace_id,
            {"name": tag_name}
        )

        tag_gid = new_tag["gid"]
        self._cache_tags[tag_name] = tag_gid
        return tag_gid

    def _marcar_concluida(self, task_id: str) -> bool:
        """Marca tarefa como concluída."""
        if not self.asana_client:
            return True

        try:
            self.asana_client.tasks.update(
                task_id,
                {"completed": True}
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao marcar como concluída: {e}")
            return False

    def _adicionar_comentario(self, task_id: str, texto: str) -> bool:
        """Adiciona comentário à tarefa."""
        if not self.asana_client:
            return True

        try:
            self.asana_client.stories.create_story_for_task(
                task_id,
                {"text": texto}
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar comentário: {e}")
            return False

    def anexar_arquivo(self, task_id: str, file_path: str, nome: Optional[str] = None) -> bool:
        """Anexa arquivo à tarefa."""
        if not self.asana_client:
            return True

        if not os.path.exists(file_path):
            raise AsanaLibError(f"Arquivo não encontrado: {file_path}")

        try:
            # Nome do arquivo
            filename = nome or os.path.basename(file_path)

            # Upload via API
            with open(file_path, 'rb') as file:
                self.asana_client.attachments.create_attachment_for_task(
                    task_id,
                    file=file,
                    file_name=filename
                )

            logger.info(f"Arquivo anexado: {filename}")
            return True

        except Exception as e:
            logger.error(f"Erro ao anexar arquivo: {e}")
            raise AsanaLibError(f"Falha ao anexar arquivo: {e}")

    def buscar_tarefas(self, filtros: Optional[Dict] = None) -> List[Dict]:
        """Busca tarefas no projeto."""
        if not self.asana_client:
            return []

        try:
            params = {
                "project": self.project_id,
                "opt_fields": ["name", "notes", "completed", "due_on", "tags"]
            }

            # Aplicar filtros
            if filtros:
                if "completed" in filtros:
                    params["completed_since"] = "now" if filtros["completed"] else None

            # Buscar tarefas
            tasks = list(self.asana_client.tasks.find_all(params))

            return tasks

        except Exception as e:
            logger.error(f"Erro ao buscar tarefas: {e}")
            return []
```

### Passo 4: Testar Integração

```bash
# Configurar token no .env
echo "ASANA_ACCESS_TOKEN=seu_token_aqui" >> .env

# Testar criação
python3 -c "
from src.asana_lib import AsanaLib

asana = AsanaLib()

dados_teste = {
    'cliente': '[TESTE] Empresa Teste',
    'local': 'São Paulo - SP',
    'tipo_servico': 'instalacao',
    'origem': 'comercial',
    'descricao': 'Teste de integração - pode deletar'
}

task_id = asana.criar_orcamento(dados_teste)
print(f'Tarefa criada: {task_id}')
print(f'Link: https://app.asana.com/0/{asana.project_id}/{task_id}')
"
```

---

## 📊 Comparação de Abordagens

| Aspecto | MCP Asana | API Direta |
|---------|-----------|------------|
| **Setup** | Automático no Claude Code | Requer token e código |
| **Flexibilidade** | Limitada ao Claude Code | Total |
| **Controle** | Menos controle | Controle total |
| **Produção** | Não recomendado | ✅ Recomendado |
| **Desenvolvimento** | ✅ Ótimo | Bom |
| **Manutenção** | Baixa | Média |

---

## 🎯 Recomendação

Para este projeto, **recomendamos API Direta**:

1. ✅ Mais flexível e testável
2. ✅ Funciona em qualquer ambiente
3. ✅ Preparado para automação (cron jobs)
4. ✅ Maior controle sobre operações
5. ✅ SDK oficial do Asana bem documentado

---

## 📚 Recursos

- [Asana API Documentation](https://developers.asana.com/docs)
- [Asana Python SDK](https://github.com/Asana/python-asana)
- [Asana API Explorer](https://developers.asana.com/explorer)
- [Asana Personal Access Tokens](https://app.asana.com/0/my-apps)

---

## 🆘 Troubleshooting

### Erro: "Invalid token"

**Causa:** Token expirado ou inválido

**Solução:**
1. Gere novo token em https://app.asana.com/0/my-apps
2. Atualize `.env` com novo token
3. Reinicie aplicação

### Erro: "Project not found"

**Causa:** PROJECT_ID incorreto ou sem permissão

**Solução:**
1. Verifique PROJECT_ID em `src/asana_lib.py`
2. Confirme que tem acesso ao projeto no Asana
3. Use `asana_client.projects.get_project(PROJECT_ID)` para testar

### Erro: "Rate limit exceeded"

**Causa:** Muitas requisições em pouco tempo

**Solução:**
- Asana Free Tier: 1500 requisições/minuto
- Adicione delays entre operações se criar muitas tarefas
- Considere usar batch operations

---

**Última atualização:** 30/01/2026

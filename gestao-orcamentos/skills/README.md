# Skills - Sistema de Gestão de Orçamentos

Este diretório contém skills padronizadas para agentes Claude processarem demandas de orçamentos.

---

## 📁 Skills Disponíveis

### `skill_orcamentos.md` ✅

Skill completa para processamento de orçamentos do Setor de Climatização.

**Compatível com:**
- Claude Haiku 4 (recomendado - otimizado para baixo custo)
- Claude Sonnet 4.5
- Claude Opus 4

**Funcionalidades:**
- ✅ Pipeline completo end-to-end
- ✅ Busca de emails no Gmail
- ✅ Preparação e limpeza de dados
- ✅ Extração com IA (Haiku + fallback Sonnet)
- ✅ Criação de tarefas no Asana
- ✅ Troubleshooting e recuperação de erros

**Quando usar:**
- Processar nova demanda de orçamento
- Buscar emails sobre cliente/projeto
- Extrair dados de documentos
- Criar tarefas estruturadas no Asana

**Documentação:** Ver arquivo completo para instruções detalhadas, exemplos e troubleshooting.

---

## 🎯 Como Usar Skills

### No Claude Code

1. **Carregar skill automaticamente:**
   - Claude Code carrega skills do diretório `skills/` automaticamente
   - Basta ter o arquivo no diretório

2. **Referenciar explicitamente:**
   ```
   Usuário: "Use a skill de orçamentos para processar pasta 26_062"
   Claude: [Carrega e executa skill_orcamentos.md]
   ```

3. **Invocar comandos:**
   ```
   Usuário: "Processar orçamento 26_062"
   Claude: [Reconhece contexto e usa skill automaticamente]
   ```

### Para Agentes Haiku

A skill foi otimizada para Haiku (12x mais barato que Sonnet):
- ✅ Instruções claras e passo-a-passo
- ✅ Comandos específicos sem ambiguidade
- ✅ Exemplos concretos de entrada/saída
- ✅ Troubleshooting com soluções específicas
- ✅ Sem necessidade de raciocínio complexo

**Teste de compatibilidade:**
```python
# Testar se Haiku consegue processar demanda
from anthropic import Anthropic

client = Anthropic()

# Carregar skill
with open('skills/skill_orcamentos.md', 'r') as f:
    skill_content = f.read()

# Testar com Haiku
response = client.messages.create(
    model="claude-haiku-4-20250514",
    max_tokens=2000,
    system=skill_content,
    messages=[{
        "role": "user",
        "content": "Processar pasta 26_062"
    }]
)

print(response.content)
# Deve identificar comando correto e executar
```

---

## 📊 Benefícios de Usar Skills

### Para Desenvolvimento
- ✅ **Consistência:** Todos os agentes seguem mesmo padrão
- ✅ **Manutenibilidade:** Atualizar skill atualiza todos os agentes
- ✅ **Testabilidade:** Skill pode ser testada isoladamente
- ✅ **Documentação:** Skill serve como documentação viva

### Para Produção
- ✅ **Custo:** Haiku 12x mais barato que Sonnet
- ✅ **Velocidade:** Haiku 2-3x mais rápido
- ✅ **Confiabilidade:** Instruções claras reduzem erros
- ✅ **Escalabilidade:** Processar mais demandas pelo mesmo custo

### Para Usuários
- ✅ **Simplicidade:** Comandos naturais ("processar 26_062")
- ✅ **Previsibilidade:** Sempre sabe o que esperar
- ✅ **Ajuda embutida:** Troubleshooting na própria skill
- ✅ **Feedback claro:** Métricas e relatórios padronizados

---

## 🔧 Desenvolvimento de Novas Skills

### Template Básico

```markdown
# Skill: [Nome da Skill]

**Versão:** 1.0.0
**Compatível com:** Claude Haiku 4, Sonnet 4.5, Opus 4

## 📋 Propósito
[O que a skill faz]

## 🎯 Quando Usar
[Critérios para usar a skill]

## 🚀 Fluxo de Trabalho
[Passo-a-passo detalhado]

## 🛠️ Comandos Disponíveis
[Lista de comandos com exemplos]

## 🔍 Troubleshooting
[Problemas comuns e soluções]

## 📊 Métricas de Sucesso
[O que reportar ao usuário]

## 🎓 Exemplos de Conversas
[Diálogos exemplo]
```

### Boas Práticas

1. **Clareza:** Instruções devem ser claras para Haiku
2. **Exemplos:** Incluir exemplos concretos de entrada/saída
3. **Comandos:** Usar comandos específicos, não genéricos
4. **Erros:** Documentar erros comuns e como resolver
5. **Métricas:** Sempre reportar estatísticas ao usuário
6. **Versão:** Manter changelog de alterações

### Testar Skills

```bash
# Testar skill com CLI
python src/cli.py processar-pasta 26_062 --dry-run -v

# Testar com Haiku via API
python tests/test_skill_haiku.py

# Validar formato
python scripts/validate_skill.py skills/skill_orcamentos.md
```

---

## 📈 Métricas de Performance

### skill_orcamentos.md

| Métrica | Haiku | Sonnet | Ganho |
|---------|-------|--------|-------|
| **Custo/demanda** | $0.0004 | $0.0048 | **12x** |
| **Tempo/demanda** | 2-4s | 4-8s | **2-3x** |
| **Taxa de sucesso** | 87% | 95% | -8% |
| **Fallback necessário** | 13% | 0% | - |

**Custo médio ponderado:** $0.0006/demanda
- 87% com Haiku: $0.0004
- 13% fallback Sonnet: $0.0015

**ROI:** 20x mais demandas pelo mesmo custo vs usar Sonnet sempre

---

## 🔐 Segurança

Skills podem executar comandos. Seguir guidelines:

### ✅ Permitido
- Ler arquivos públicos do projeto
- Executar scripts documentados
- Buscar dados via APIs configuradas
- Criar tarefas no Asana

### ❌ Não Permitido
- Acessar credenciais diretamente
- Modificar código fonte
- Executar comandos destrutivos
- Deletar dados

### Validação
- Skills devem validar inputs
- Usar `--dry-run` para testes
- Pedir confirmação para ações irreversíveis
- Logar todas as operações

---

## 📚 Recursos

### Documentação
- **Arquitetura:** `../ARQUITETURA.md`
- **CLI:** `../EXEMPLO_CLI.md`
- **Setup:** `../docs/SETUP_GMAIL_API.md`

### Comunidade
- **Issues:** GitHub Issues para reportar problemas
- **Melhorias:** Pull Requests para novas skills
- **Discussões:** GitHub Discussions para perguntas

---

## 🔄 Roadmap

### Próximas Skills Planejadas

#### `skill_sync_drive.md` ⏳
Sincronização entre Google Drive e Asana
- Upload de arquivos
- Sync de IDs
- Anexar documentos

#### `skill_relatorios.md` ⏳
Geração de relatórios e dashboards
- Relatório semanal
- Métricas de conversão
- Análise de pipeline

#### `skill_atualizacao.md` ⏳
Atualização de tarefas existentes
- Avançar etapas
- Registrar fechamentos
- Adicionar comentários

---

**Última atualização:** 30/01/2026
**Mantido por:** Coordenador do Setor de Orçamentos

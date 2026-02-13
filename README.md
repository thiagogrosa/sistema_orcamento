# Sistema de Orçamento HVAC

Sistema completo para gestão de orçamentos de climatização.

## Estrutura

| Pasta | Descrição |
|-------|-----------|
| `orcamento_hvac/` | Sistema principal de orçamentos (cálculo, composição de preços, propostas) |
| `gerador_propostas/` | Gerador de layout de propostas em PDF |
| `gestao_tarefas/` | Integração com Asana e Google Drive |

## Módulos

### Orçamento HVAC (orcamento_hvac/)
- **dados/**: Catálogos de materiais, mão de obra, ferramentas, equipamentos
- **abas/**: Módulos de geração das abas do Excel
- **automations/**: Scripts de automação (geração de propostas, integrações)
- **tests/**: Testes automatizados
- **standards/**: Migrações de banco, workflows

### Gerador de Propostas (gerador_propostas/)
- Geração de propostas comerciais em PDF com formatação profissional
- Integração com o sistema de orçamentos

### Gestão de Tarefas (gestao_tarefas/)
- Integração com Asana para gestão de tarefas de orçamento
- Sincronização com Google Drive

---

**Desenvolvido com OpenClaw + IA**

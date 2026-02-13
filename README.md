# Sistema de Orçamento HVAC

Sistema completo para gestão de orçamentos de climatização.

## Estrutura

| Pasta | Descrição |
|-------|-----------|
| `planilha/` | Sistema principal de orçamentos (geração, composição de preços, propostas) |
| `gemini_hvac_layout/` | Gerador de layout de propostas em PDF |
| `gestao-orcamentos/` | Integração com Asana e Google Drive |

## Módulos

### Planilha (planilha/)
- **dados/**: Catálogos de materiais, mão de obra, ferramentas, equipamentos
- **abas/**: Módulos de geração das abas do Excel
- **automations/**: Scripts de automação (geração de propostas, integrações)
- **tests/**: Testes automatizados
- **standards/**: Migrações de banco, workflows

### PDF Layout (gemini_hvac_layout/)
- Geração de propostas comerciais em PDF com formatação profissional
- Integração com o sistema de orçamentos

### Gestão (gestao-orcamentos/)
- Integração com Asana para gestão de tarefas de orçamento
- Sincronização com Google Drive

---

**Desenvolvido com OpenClaw + IA**

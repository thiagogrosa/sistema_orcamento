# Gerador de Propostas PDF

Sistema de geração de propostas comerciais em PDF para projetos HVAC.

## Visão Geral

Gera propostas profissionais em PDF com formatação padronizada, usando dados de precificação do sistema de orçamentos.

## Tecnologias

- **Python 3.12+**
- **Jinja2** — Templates HTML
- **WeasyPrint** — Conversão HTML/CSS para PDF
- **openpyxl** — Planilhas Excel

## Estrutura

```
gerador_propostas/
├── bases/           # Catálogos (materiais, MO, composições, BDI)
├── config/          # Empresa, condições comerciais, exclusões
├── hvac/            # Core da aplicação
│   ├── generators/  # Lógica de geração (PDF, Excel)
│   └── utils/       # Utilitários
├── templates/html/  # Templates visuais
├── tests/           # Dados de teste
└── output/         # PDFs gerados
```

## Uso

### Ambiente Virtual
```bash
source .venv/bin/activate
```

### Gerar PDF de Teste
```bash
./gerar_teste_pdf.sh
```

### Via Python
```bash
python -m hvac.gerador_pdf dados_teste.json output/proposta.pdf
```

## Integração

Este módulo é usado pelo `orcamento_hvac` através do script:
- `orcamento_hvac/automations/scripts/export_proposal_pdf.py`

## Requisitos

```bash
pip install -r requirements.txt
```

Consulte `requirements.txt` para dependências completas.

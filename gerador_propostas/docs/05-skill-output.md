# Skill Output: hvac-output

> **Modelo recomendado:** SONNET (formatacao)
> **Responsabilidade:** Gerar documentos finais

---

## Objetivo

Gerar documentos de orcamento em diferentes formatos:
- PDF com identidade visual (proposta comercial)
- Excel detalhado (analise interna)
- Texto resumido (resposta rapida)

---

## Formatos de Saida

### 1. PDF Proposta Comercial

**Arquivo:** `ORC-[CLIENTE]-[DATA].pdf`

**Estrutura:**

```
┌────────────────────────────────────────────────────┐
│                    CABECALHO                        │
│  Logo | Nome Empresa | Contato | CNPJ              │
├────────────────────────────────────────────────────┤
│               PROPOSTA COMERCIAL                    │
│                  No [sequencial]                    │
├────────────────────────────────────────────────────┤
│  CLIENTE                                            │
│  Nome: [cliente]                                    │
│  Endereco: [endereco]                               │
│  Contato: [contato]                                 │
├────────────────────────────────────────────────────┤
│  ESCOPO DOS SERVICOS                                │
│  [Descricao do escopo em texto]                     │
├────────────────────────────────────────────────────┤
│  ITENS DO ORCAMENTO                                 │
│  ┌─────┬────────────────────┬─────┬───────────────┐ │
│  │Item │ Descricao          │ Qtd │ Valor         │ │
│  ├─────┼────────────────────┼─────┼───────────────┤ │
│  │ 1   │ Instalacao 12K     │  1  │ R$ 1.310,18   │ │
│  │ 2   │ Instalacao 18K     │  1  │ R$ 1.520,45   │ │
│  ├─────┼────────────────────┼─────┼───────────────┤ │
│  │     │            TOTAL   │     │ R$ 2.830,63   │ │
│  └─────┴────────────────────┴─────┴───────────────┘ │
├────────────────────────────────────────────────────┤
│  CONDICOES COMERCIAIS                               │
│  • Validade: 15 dias                                │
│  • Forma de pagamento: [definir]                    │
│  • Prazo de execucao: [definir]                     │
│  • Garantia: 90 dias para servicos                  │
├────────────────────────────────────────────────────┤
│  OBSERVACOES                                        │
│  [Observacoes relevantes]                           │
├────────────────────────────────────────────────────┤
│                     RODAPE                          │
│  Data | Assinatura Empresa | Assinatura Cliente    │
└────────────────────────────────────────────────────┘
```

**Identidade Visual:**
- Usar templates em `templates/proposta/`
- Cores e logo da empresa
- Fonte profissional

### 2. Excel Detalhado

**Arquivo:** `ORC-[CLIENTE]-[DATA]-interno.xlsx`

**Abas:**

| Aba | Conteudo | Visibilidade |
|-----|----------|--------------|
| Resumo | Dados cliente, valor total | Cliente |
| Itens | Tabela de itens precificados | Cliente |
| Composicao | Materiais e MO por item | Interno |
| Materiais | Lista consolidada de compras | Interno |
| Mao de Obra | Horas por categoria | Interno |
| Custos | Analise de custos e margens | Interno |

**Aba Resumo:**
```
| Campo              | Valor              |
|--------------------|-------------------|
| Cliente            | [nome]            |
| Data               | [data]            |
| Validade           | [dias]            |
| Valor Total        | R$ [valor]        |
| Forma Pagamento    | [definir]         |
| Prazo Execucao     | [definir]         |
```

**Aba Itens:**
```
| Item | Descricao | Qtd | Un | Valor Unit. | Valor Total |
|------|-----------|-----|----|-------------|-------------|
| 1    | Inst 12K  | 1   | un | R$ 1.310,18 | R$ 1.310,18 |
```

**Aba Composicao (interno):**
```
| Item | Material/MO | Descricao | Qtd | Un | Custo Unit. | Custo Total |
|------|-------------|-----------|-----|----|-------------|-------------|
| 1    | TUB-CU-1/4  | Tubo...   | 4   | m  | R$ 28,50    | R$ 114,00   |
```

### 3. Texto Resumido

**Arquivo:** `ORC-[CLIENTE]-[DATA]-resumo.md`

**Formato:**
```markdown
## Orcamento - [Cliente]
**Data:** [data]
**Validade:** [dias] dias

### Servicos
- [Item 1]: R$ [valor]
- [Item 2]: R$ [valor]

### Total: R$ [valor]

### Condicoes
- Pagamento: [definir]
- Prazo: [definir]
- Garantia: 90 dias
```

---

## Formatacao de Valores

### Moeda Brasileira

```
Valor: R$ 1.234,56
Usar ponto como separador de milhar
Usar virgula como separador decimal
Sempre 2 casas decimais
```

### Datas

```
Formato: DD/MM/YYYY
Exemplo: 02/01/2026
```

### Nomes de Arquivos

```
Padrao: ORC-[CLIENTE]-[DATA]-[TIPO].[EXT]

CLIENTE: Primeiras palavras, sem espacos, maiusculo
DATA: YYYYMMDD
TIPO: (vazio para PDF), "interno" para Excel, "resumo" para MD

Exemplos:
- ORC-CONTABILIDADE-SILVA-20260102.pdf
- ORC-CONTABILIDADE-SILVA-20260102-interno.xlsx
- ORC-CONTABILIDADE-SILVA-20260102-resumo.md
```

---

## Niveis de Detalhe

### Para Cliente (Externo)

Mostrar apenas:
- Descricao do item
- Quantidade
- Valor total

Ocultar:
- Composicao de custos
- Margens
- Custos unitarios de materiais

### Para Analise Interna

Mostrar tudo:
- Composicoes completas
- Custos e margens
- Fornecedores
- Notas e alertas

### Para Licitacao (Governo)

Formato conforme edital:
- BDI detalhado se exigido
- Planilha de custos e formacao de precos
- Declaracoes exigidas

---

## Geracao de PDF

### Metodo Recomendado

1. Gerar HTML com template
2. Converter para PDF via ferramenta CLI

**Ferramentas sugeridas:**
- `wkhtmltopdf`
- `puppeteer` (headless Chrome)
- `weasyprint`

### Estrutura de Templates

```
templates/proposta/
├── template.html      # Template principal
├── cabecalho.html     # Cabecalho reutilizavel
├── rodape.html        # Rodape reutilizavel
├── estilos.css        # Estilos CSS
└── logo.png           # Logo da empresa
```

---

## Locais de Saida

### Padrao

Salvar em pasta de saida do projeto:
```
hvac_claude_code/output/
├── 2026-01/
│   ├── ORC-CLIENTE1-20260102.pdf
│   ├── ORC-CLIENTE1-20260102-interno.xlsx
│   └── ...
```

### Google Drive

Se configurado, salvar tambem em:
```
Google Drive/Orcamentos HVAC/2026/01/
```

---

*Especificacao da Skill Output - Sistema HVAC*

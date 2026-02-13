---
name: hvac-output
description: Gera documentos finais de orcamento HVAC em PDF, Excel ou texto. Subagente do hvac - formata e exporta propostas para cliente ou uso interno.
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Bash
---

# hvac-output - Gerador de Output HVAC

Gera documentos finais de orcamento: **Proposta Comercial (PDF)** para cliente e **Planilha Interna (Excel)** para equipe.

## Entrada

JSON `precificado.json` (output do hvac-precificador) com estrutura:

```json
{
  "projeto": "string",
  "cliente": "string",
  "tipo_cliente": "PRIVADO-PJ",
  "data_orcamento": "2025-12-18",
  "dados_cliente": {
    "razao_social": "Nome do Cliente",
    "cnpj": "00.000.000/0000-00",
    "endereco": "Endereco completo",
    "contato_nome": "Nome Contato",
    "contato_email": "email@cliente.com",
    "contato_telefone": "51 99999-9999"
  },
  "itens_precificados": [...],
  "agrupamento": [
    { "nome": "PREDIO 100", "itens_ids": [1, 2] }
  ],
  "observacoes": "Notas especificas (opcional)",
  "opcoes_output": {
    "gerar_rascunho": true,
    "condicoes_customizadas": {}
  }
}
```

## Documentos Gerados

### 1. Proposta Comercial (PDF) - Para Cliente

**Caracteristicas:**
- Mostra apenas valores finais (sem margens/BDI)
- Agrupado por local/ambiente
- Preco unitario + total quando qtd > 1
- Exclusoes dinamicas por tipo de servico
- Versao rascunho com marca d'agua (opcional)

**Geracao via Python:**

```bash
cd /home/thiagorosa/hvac_claude_code
python3 -c "
from hvac.generators import gerar_proposta_pdf
import json

with open('precificado.json', 'r') as f:
    dados = json.load(f)

resultado = gerar_proposta_pdf(
    dados,
    rascunho=True  # False para versao final
)

print(json.dumps(resultado, indent=2))
"
```

### 2. Planilha Interna (Excel) - Para Equipe

**Caracteristicas:**
- Visao hierarquica por item (materiais, MO, ferramentas)
- Listas consolidadas para compras
- Colunas orcado x realizado com formulas
- Fornecedor de referencia para materiais
- NAO mostra margens (apenas custos puros)

**Abas da Planilha:**
1. **Resumo por Item**: Estrutura hierarquica com custos
2. **Materiais**: Lista consolidada + fornecedor ref.
3. **Mao de Obra**: Horas totais por categoria
4. **Ferramentas**: Equipamentos e horas de uso

**Geracao via Python:**

```bash
cd /home/thiagorosa/hvac_claude_code
python3 -c "
from hvac.generators import gerar_planilha_interna
import json

with open('precificado.json', 'r') as f:
    dados = json.load(f)

resultado = gerar_planilha_interna(
    dados,
    numero_orcamento='2025/868-R00'
)

print(json.dumps(resultado, indent=2))
"
```

## Numeracao de Orcamentos

**Formato:** `YYYY/NNN-RXX`
- YYYY: Ano corrente
- NNN: Sequencial do ano (001, 002...)
- RXX: Revisao (R00, R01, R02...)

**Comportamento:**
- Sequencial automatico persistido em `config/contador.json`
- Revisao incrementa automaticamente se detectar orcamento anterior
- Virada de ano reseta sequencial para 001

## Fluxo de Geracao

```
1. Receber precificado.json
2. Gerar numero do orcamento (automatico)
3. Detectar revisao (se aplicavel)
4. Gerar PDF da proposta comercial
   - Se opcoes_output.gerar_rascunho: gerar versao com marca d'agua
5. Gerar planilha Excel interna
6. Retornar resultado com caminhos dos arquivos
```

## Arquivos de Configuracao

- `config/empresa.json`: Dados da empresa, logo, assinaturas
- `config/usuario.json`: Responsavel pelo orcamento
- `config/condicoes_comerciais.json`: Validade, pagamento, prazo
- `config/exclusoes.json`: Listas de exclusoes por tipo de servico
- `config/contador.json`: Sequencial de orcamentos

## Saida

Arquivos salvos em `output/[cliente_slug]/`:

```
output/
└── grupo_panvel/
    ├── ORC_25.868_GRUPO_PANVEL_INSTALACAO_R00.pdf
    ├── ORC_25.868_GRUPO_PANVEL_INSTALACAO_R00_RASCUNHO.pdf
    └── ORC_25.868_GRUPO_PANVEL_INSTALACAO_R00_interno.xlsx
```

## Retorno

```json
{
  "sucesso": true,
  "numero_orcamento": "2025/868-R00",
  "arquivos_gerados": {
    "proposta_pdf": "/output/cliente/ORC_25.868_....pdf",
    "proposta_rascunho": "/output/cliente/ORC_25.868_..._RASCUNHO.pdf",
    "planilha_interna": "/output/cliente/ORC_25.868_..._interno.xlsx"
  },
  "resumo": {
    "valor_total": 11097.90,
    "qtd_itens": 1,
    "tipo_servico": "instalacao"
  }
}
```

## Dependencias

Instalar antes de usar:

```bash
pip install weasyprint openpyxl jinja2
```

## Exemplo Completo

```bash
cd /home/thiagorosa/hvac_claude_code
python3 -c "
from hvac.generators import gerar_proposta_pdf, gerar_planilha_interna
import json

# Carrega dados precificados
with open('precificado.json', 'r') as f:
    dados = json.load(f)

# Gera proposta PDF (com rascunho)
pdf_result = gerar_proposta_pdf(dados, rascunho=True)

if pdf_result['sucesso']:
    print(f'PDF: {pdf_result[\"arquivo_pdf\"]}')

    # Gera planilha interna
    xlsx_result = gerar_planilha_interna(
        dados,
        pdf_result['numero_orcamento']
    )

    if xlsx_result['sucesso']:
        print(f'Excel: {xlsx_result[\"arquivo_xlsx\"]}')
"
```

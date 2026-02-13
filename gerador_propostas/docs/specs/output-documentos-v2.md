# Especificacao: Sistema de Output de Documentos HVAC v2

> Gerado em: 2026-01-05
> Status: Aguardando aprovacao

---

## 1. Visao Geral

O sistema de output deve gerar **dois documentos distintos** a partir do orcamento precificado:

| Documento | Publico | Conteudo | Formato |
|-----------|---------|----------|---------|
| **Proposta Comercial** | Cliente | Valores finais por servico (sem margens) | PDF |
| **Planilha Interna** | Equipe | Custos detalhados + controle orcado x realizado | Excel (.xlsx) |

---

## 2. Proposta Comercial (Cliente)

### 2.1 Estrutura do Documento

```
┌─────────────────────────────────────────────────────────────┐
│ CABECALHO                                                   │
│ - Logo Armant                                               │
│ - Dados empresa (endereco, CNPJ, telefone, email)           │
│ - Numero do orcamento: YYYY/NNN-RXX                         │
│ - Data: Porto Alegre, DD de MMMM de YYYY                    │
├─────────────────────────────────────────────────────────────┤
│ DADOS DO CLIENTE                                            │
│ - Nome/Razao Social                                         │
│ - CNPJ/CPF                                                  │
│ - Endereco completo                                         │
│ - Contato (nome / email / telefone)                         │
│ - Ref.: Descricao do servico                                │
├─────────────────────────────────────────────────────────────┤
│ 1. ORCAMENTO (tabela)                                       │
│ - Agrupado por local/ambiente                               │
│ - Colunas: ITEM | DESCRICAO | UN | QTD | VLR UNIT | TOTAL   │
│ - Subtotais por grupo                                       │
│ - TOTAL GERAL                                               │
├─────────────────────────────────────────────────────────────┤
│ DESTAQUES (checkmarks)                                      │
│ ✓ Empresa registrada no CREA/RS                             │
│ ✓ Todas as tubulacoes em cobre                              │
│ ✓ 01 ano de garantia dos servicos                           │
│ ✓ Mais de 10.000 equipamentos instalados                    │
│ ✓ Mao de obra qualificada                                   │
├─────────────────────────────────────────────────────────────┤
│ 2. RESPONSAVEL                                              │
│ - Nome / email / telefone (do config do usuario)            │
├─────────────────────────────────────────────────────────────┤
│ 3. INVESTIMENTO                                             │
│ - Valor por extenso                                         │
├─────────────────────────────────────────────────────────────┤
│ 4. SERVICOS NAO INCLUIDOS                                   │
│ - Lista dinamica baseada no tipo de servico                 │
├─────────────────────────────────────────────────────────────┤
│ 5. OBSERVACOES (opcional)                                   │
│ - Campo livre para notas especificas                        │
├─────────────────────────────────────────────────────────────┤
│ 6. PRAZO DE ENTREGA                                         │
│ - Valor do config (default: "A combinar")                   │
├─────────────────────────────────────────────────────────────┤
│ 7. CONDICOES DE PAGAMENTO                                   │
│ - Valor do config (default por tipo cliente)                │
├─────────────────────────────────────────────────────────────┤
│ 8. VALIDADE DA PROPOSTA                                     │
│ - Valor do config (default: 10 dias)                        │
├─────────────────────────────────────────────────────────────┤
│ ASSINATURAS                                                 │
│ - Engenheiro responsavel (nome, cargo, CREA)                │
│ - Socio administrador (nome, cargo)                         │
├─────────────────────────────────────────────────────────────┤
│ RODAPE                                                      │
│ - Dados empresa + logos (ASBRAV, ABRAVA)                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Regras de Exibicao

**Tabela de Orcamento:**
- Itens agrupados por local/ambiente (ex: "PREDIO 100", "SALA REUNIOES")
- Quando `quantidade > 1`: mostrar valor unitario e valor total
- Quando `quantidade = 1`: mostrar apenas valor total
- Subtotal por grupo
- Total geral ao final

**Valores:**
- Exibir apenas preco final (custo + BDI ja aplicado)
- NAO mostrar: custo de materiais, mao de obra, BDI, margens
- Formato monetario: R$ X.XXX,XX

**Numeracao:**
- Formato: `YYYY/NNN-RXX`
- YYYY: ano corrente
- NNN: sequencial do ano (001, 002, ...)
- RXX: revisao (R00, R01, R02...)
- Persistido em `config/contador.json`

**Revisoes:**
- Sistema detecta orcamentos existentes para mesmo cliente/escopo
- Incrementa automaticamente R00 → R01 → R02

**Versao Rascunho:**
- Marca d'agua "RASCUNHO" diagonal no PDF
- Para aprovacao interna antes de envio ao cliente

### 2.3 Exclusoes por Tipo de Servico

```json
{
  "instalacao": [
    "Decoracao (Gesso)",
    "Bomba de drenagem",
    "Abertura de canaletas",
    "Ponto/ramal de dreno",
    "Ponto/ramal de forca 220v",
    "Trabalho fora do horario comercial",
    "Montagem e fornecimento de andaimes",
    "Acabamento em massa corrida e pintura",
    "Servicos de alvenaria (abertura e fechamento)",
    "Calha plastica e/ou eletrocalhas de acabamento"
  ],
  "manutencao_preventiva": [
    "Pecas e componentes",
    "Recarga de gas refrigerante",
    "Servicos de instalacao",
    "Trabalho fora do horario comercial"
  ],
  "manutencao_corretiva": [
    "Pecas e componentes nao diagnosticados",
    "Servicos de instalacao",
    "Trabalho fora do horario comercial"
  ],
  "desinstalacao": [
    "Transporte de equipamentos",
    "Destinacao de residuos",
    "Fechamento de furos/vao",
    "Trabalho fora do horario comercial"
  ]
}
```

### 2.4 Geracao do PDF

**Abordagem:** HTML → PDF (via weasyprint ou playwright)

**Processo:**
1. Carregar template HTML com CSS (estilo Armant)
2. Preencher variaveis com dados do orcamento
3. Renderizar para PDF
4. Se rascunho: adicionar marca d'agua

**Arquivos de template:**
- `templates/html/proposta_base.html`
- `templates/html/proposta_styles.css`
- `templates/html/logo_armant.png`

---

## 3. Planilha Interna (Equipe)

### 3.1 Estrutura do Excel

**Aba 1: Resumo por Item (visao hierarquica)**

| Coluna | Descricao |
|--------|-----------|
| A | Item (1, 1.1, 1.1.1...) |
| B | Descricao |
| C | Tipo (SERVICO / MATERIAL / MAO_OBRA / FERRAMENTA) |
| D | Unidade |
| E | Quantidade |
| F | Custo Unitario Orcado |
| G | Custo Total Orcado |
| H | Custo Unitario Real |
| I | Custo Total Real |
| J | Diferenca (R$) |
| K | Diferenca (%) |

**Estrutura hierarquica:**
```
1   PREDIO 100                                    GRUPO
1.1   Instalacao cassete 60.000 BTU              SERVICO     pç    1    8.000    8.000
1.1.1   Tubo cobre 3/8"                          MATERIAL    m    15      45      675
1.1.2   Tubo cobre 5/8"                          MATERIAL    m    15      65      975
1.1.3   Tecnico HVAC                             MAO_OBRA    h     8     120      960
1.1.4   Vacuometro                               FERRAMENTA  h     2      15       30
...
```

**Aba 2: Lista Consolidada de Materiais**

| Coluna | Descricao |
|--------|-----------|
| A | Codigo |
| B | Descricao |
| C | Unidade |
| D | Qtd Total |
| E | Custo Unit Orcado |
| F | Custo Total Orcado |
| G | Fornecedor Referencia |
| H | Custo Unit Real |
| I | Custo Total Real |
| J | Diferenca |

**Aba 3: Lista Consolidada de Mao de Obra**

| Coluna | Descricao |
|--------|-----------|
| A | Categoria |
| B | Horas Totais |
| C | Custo/Hora Orcado |
| D | Custo Total Orcado |
| E | Custo/Hora Real |
| F | Custo Total Real |
| G | Diferenca |

**Aba 4: Lista Consolidada de Ferramentas**

| Coluna | Descricao |
|--------|-----------|
| A | Codigo |
| B | Descricao |
| C | Horas Uso |
| D | Custo/Hora Orcado |
| E | Custo Total Orcado |
| F | Custo/Hora Real |
| G | Custo Total Real |
| H | Diferenca |

### 3.2 Regras da Planilha

**Cabecalho (todas as abas):**
- Referencia: `ORC YYYY/NNN-RXX`
- Cliente: nome
- Data geracao: DD/MM/YYYY

**Formulas Excel:**
- Custo Total = Quantidade × Custo Unitario
- Diferenca (R$) = Custo Real - Custo Orcado
- Diferenca (%) = (Diferenca / Custo Orcado) × 100
- Totais por grupo e geral com SOMA()

**Colunas editaveis:**
- Custo Unitario Real
- Custo Total Real (com formula, mas pode sobrescrever)

**Colunas protegidas:** Nenhuma (acesso livre)

**Fornecedor Referencia:**
- Extraido da base de materiais
- Campo `fornecedor_referencia` ou primeiro fornecedor da lista

### 3.3 Visibilidade de Margens

A planilha interna **NAO** deve mostrar:
- BDI aplicado
- Preco de venda
- Margens de lucro

Apenas custos puros para controle operacional.

---

## 4. Configuracoes

### 4.1 config/empresa.json

```json
{
  "razao_social": "ARMANT SOLUCOES EM CLIMATIZACAO LTDA",
  "endereco": "Avenida Polonia, 764 | Bairro Sao Geraldo | Porto Alegre | RS",
  "cnpj": "13.591.585/0001-03",
  "telefone": "(51) 3085.8050",
  "email": "armant@armant.com.br",
  "crea": "206773",
  "logo_path": "templates/html/logo_armant.png",
  "assinaturas": [
    {
      "nome": "Rodrigo G. Donni",
      "cargo": "Engenheiro Mecanico",
      "registro": "CREA RS 131427",
      "assinatura_img": "templates/html/assinatura_rodrigo.png"
    },
    {
      "nome": "Daniel Albuquerque",
      "cargo": "Socio Administrador",
      "registro": null,
      "assinatura_img": "templates/html/assinatura_daniel.png"
    }
  ],
  "destaques": [
    "Empresa registrada no CREA/RS 206773 - ASBRAV",
    "Todas as tubulacoes em cobre",
    "01 (Um) ano de garantia dos servicos de instalacao",
    "Mais de 10.000 equipamentos instalados",
    "Mao de obra qualificada"
  ]
}
```

### 4.2 config/usuario.json

```json
{
  "nome": "Thiago Rosa",
  "email": "orcamentos2@armant.com.br",
  "telefone": "51 98043-4758"
}
```

### 4.3 config/condicoes_comerciais.json

```json
{
  "default": {
    "validade_dias": 10,
    "prazo_execucao": "A combinar",
    "forma_pagamento": "Entrada de 40% e saldo na conclusao dos servicos",
    "garantia": "01 (Um) ano de garantia dos servicos de instalacao",
    "nota_prazo": "Devido a alta demanda, o prazo para atendimentos esta maior do que o normal."
  },
  "por_tipo_cliente": {
    "PRIVADO-PJ": {},
    "PRIVADO-PF": {
      "forma_pagamento": "50% de entrada e 50% na conclusao"
    },
    "GOVERNO": {
      "validade_dias": 60,
      "forma_pagamento": "Conforme edital"
    }
  }
}
```

### 4.4 config/contador.json

```json
{
  "ano_corrente": 2025,
  "ultimo_sequencial": 867,
  "historico": {
    "2024": 523,
    "2025": 867
  }
}
```

---

## 5. Fluxo de Geracao

### 5.1 Entrada (do Precificador)

Recebe `precificado.json` com estrutura atual + novos campos:

```json
{
  "projeto": "string",
  "cliente": "string",
  "tipo_cliente": "PRIVADO-PJ",
  "data_orcamento": "2025-12-18",
  "validade_dias": 10,

  "dados_cliente": {
    "razao_social": "Grupo Panvel Farmacias",
    "cnpj": "92.665.611/0322-90",
    "endereco": "Av. Industrial Belgraf, 865...",
    "contato_nome": "Paulo Ficks",
    "contato_email": "pficks@grupopanvel.com.br",
    "contato_telefone": "51 3481-9885"
  },

  "itens_precificados": [...],

  "agrupamento": [
    {
      "nome": "PREDIO 100",
      "itens_ids": [1]
    }
  ],

  "observacoes": "string | null",

  "opcoes_output": {
    "gerar_rascunho": true,
    "condicoes_customizadas": {
      "prazo_execucao": "15 dias uteis"
    }
  }
}
```

### 5.2 Processo

```
precificado.json
       │
       ▼
┌──────────────────┐
│  SKILL OUTPUT    │
│                  │
│ 1. Ler configs   │
│ 2. Gerar numero  │
│ 3. Montar dados  │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌─────────┐
│ HTML  │ │ EXCEL   │
│ →PDF  │ │ .xlsx   │
└───┬───┘ └────┬────┘
    │          │
    ▼          ▼
output/[cliente]/
├── ORC_YYYY.NNN_CLIENTE_SERVICO_RXX.pdf
├── ORC_YYYY.NNN_CLIENTE_SERVICO_RXX_RASCUNHO.pdf (se solicitado)
└── ORC_YYYY.NNN_CLIENTE_SERVICO_RXX_interno.xlsx
```

### 5.3 Saida

```json
{
  "sucesso": true,
  "numero_orcamento": "2025/868-R00",
  "arquivos_gerados": {
    "proposta_pdf": "/output/panvel/ORC_25.868_PANVEL_INSTALACAO_R00.pdf",
    "proposta_rascunho": "/output/panvel/ORC_25.868_PANVEL_INSTALACAO_R00_RASCUNHO.pdf",
    "planilha_interna": "/output/panvel/ORC_25.868_PANVEL_INSTALACAO_R00_interno.xlsx"
  },
  "resumo": {
    "valor_total": 11097.90,
    "qtd_itens": 1,
    "tipo_servico": "instalacao"
  }
}
```

---

## 6. Dependencias Tecnicas

### 6.1 Python

```
weasyprint>=60.0      # HTML → PDF
openpyxl>=3.1.0       # Geracao Excel
jinja2>=3.1.0         # Templates HTML
num2words>=0.5.12     # Valor por extenso
```

### 6.2 Sistema

- Fontes: Arial/Helvetica (para PDF)
- Nenhuma dependencia de LibreOffice

---

## 7. Casos de Borda

### 7.1 Orcamento sem agrupamento
- Se nao houver `agrupamento`, listar itens sequencialmente sem grupos

### 7.2 Revisao de orcamento existente
- Buscar em `output/` por arquivos com mesmo cliente
- Se encontrar, incrementar revisao (R00 → R01)
- Manter historico de revisoes

### 7.3 Virada de ano
- Quando ano muda, resetar sequencial para 001
- Atualizar `ano_corrente` no contador

### 7.4 Material sem fornecedor na base
- Deixar coluna "Fornecedor Referencia" em branco
- Nao gerar erro

### 7.5 Orcamento so manutencao (sem materiais)
- Gerar planilha com aba de materiais vazia ou oculta
- Proposta funciona normalmente

---

## 8. Metricas de Sucesso

- [ ] PDF gerado visualmente similar ao template atual
- [ ] Planilha com formulas funcionando corretamente
- [ ] Numeracao sequencial persistida entre sessoes
- [ ] Deteccao automatica de revisoes
- [ ] Exclusoes dinamicas por tipo de servico
- [ ] Tempo de geracao < 5 segundos

---

## 9. Proximos Passos

1. **Criar estrutura de configs** (`config/*.json`)
2. **Implementar templates HTML** baseados no PDF atual
3. **Atualizar skill hvac-output** com nova logica
4. **Criar funcoes de geracao** (PDF e Excel)
5. **Integrar com precificador** (ajustar contrato de entrada)
6. **Testar com orcamento real**

---

*Especificacao gerada via entrevista - Sistema HVAC*

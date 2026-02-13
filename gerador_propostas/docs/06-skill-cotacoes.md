# Skill Cotacoes: hvac-cotacoes

> **Modelo recomendado:** SONNET
> **Responsabilidade:** Gerenciar cotacoes, fornecedores e precos

---

## Objetivo

Automatizar o processo de atualizacao de precos atraves de:
- Geracao de e-mails de cotacao para fornecedores
- Web scraping de precos em sites
- Atualizacao das bases de precos
- Gestao do cadastro de fornecedores

---

## Funcionalidades

### 1. Geracao de E-mails de Cotacao

Gerar e-mails para solicitar cotacoes de materiais.

**Entrada:**
```json
{
  "materiais": [
    {"codigo": "TUB-CU-1/4", "quantidade": 100, "unidade": "m"},
    {"codigo": "TUB-CU-3/8", "quantidade": 80, "unidade": "m"}
  ],
  "prazo_resposta": 3,
  "observacoes": "Cotacao para obra em Porto Alegre"
}
```

**Processo:**
1. Agrupar materiais por categoria
2. Identificar fornecedores por categoria
3. Gerar e-mail para cada fornecedor

**Template de E-mail:**
```
Assunto: Solicitacao de Cotacao - [Categoria] - [Data]

Prezados,

Solicitamos cotacao para os seguintes materiais:

| Item | Descricao | Quantidade | Unidade |
|------|-----------|------------|---------|
| 1    | Tubo cobre 1/4" | 100 | m |
| 2    | Tubo cobre 3/8" | 80 | m |

Informacoes adicionais:
- Prazo para resposta: [prazo] dias uteis
- Local de entrega: [cidade]
- Observacoes: [obs]

Favor informar:
- Preco unitario
- Prazo de entrega
- Condicoes de pagamento
- Validade da cotacao

Atenciosamente,
[Assinatura]
```

### 2. Web Scraping de Precos

Consultar precos em sites de fornecedores e marketplaces.

**Fontes Configuradas:**

| Fonte | Tipo | Uso |
|-------|------|-----|
| Frigelar | Fornecedor | Materiais HVAC |
| Refrinao | Fornecedor | Materiais HVAC |
| Mercado Livre | Marketplace | Referencia |
| SINAPI | Governamental | Licitacoes |

**Processo:**
1. Receber lista de materiais para atualizar
2. Para cada material, buscar nas fontes
3. Coletar precos encontrados
4. Calcular media ou menor preco
5. Atualizar base de precos

**Cuidados:**
- Respeitar robots.txt
- Limitar frequencia de requisicoes
- Tratar erros de conexao
- Validar dados extraidos

### 3. Cadastro de Fornecedores

**Estrutura:** `bases/fornecedores.json`

```json
{
  "fornecedores": [
    {
      "id": "FRIG-001",
      "nome": "Frigelar Distribuidora",
      "categorias": ["cobre", "isolamento", "gas", "ferramentas"],
      "contatos": [
        {
          "nome": "Joao Silva",
          "email": "joao@frigelar.com.br",
          "telefone": "(51) 3333-4444",
          "tipo": "comercial"
        }
      ],
      "endereco": "Rua X, 123 - Porto Alegre/RS",
      "observacoes": "Bom preco em cobre, entrega rapida",
      "avaliacao": 4.5,
      "ultima_cotacao": "2025-12-15"
    }
  ]
}
```

**Operacoes:**
- Adicionar novo fornecedor
- Atualizar dados de contato
- Registrar cotacao recebida
- Avaliar fornecedor

### 4. Atualizacao de Precos

Atualizar base de precos com novos valores.

**Entrada:**
```json
{
  "atualizacoes": [
    {
      "codigo": "TUB-CU-1/4",
      "preco": 32.50,
      "fonte": "COTACAO-FRIG-20260102",
      "fornecedor": "FRIG-001"
    }
  ]
}
```

**Processo:**
1. Validar dados de entrada
2. Fazer backup da base atual
3. Atualizar precos
4. Atualizar data_cotacao
5. Registrar historico

**Historico de Precos:**
```json
{
  "TUB-CU-1/4": {
    "historico": [
      {"data": "2025-12-01", "preco": 28.50, "fonte": "COTACAO-2025-12"},
      {"data": "2026-01-02", "preco": 32.50, "fonte": "COTACAO-FRIG-20260102"}
    ]
  }
}
```

---

## Fluxo de Atualizacao Mensal

```
1. Listar materiais com cotacao > 30 dias
2. Agrupar por categoria/fornecedor
3. Gerar e-mails de cotacao
4. Enviar (manual ou automatico)
5. Aguardar respostas
6. Processar respostas recebidas
7. Atualizar base de precos
8. Gerar relatorio de variacao
```

---

## Integracao com Orcamento

Quando um orcamento for gerado:

```
1. Identificar materiais sem preco
2. Identificar materiais desatualizados (>90 dias)
3. Se muitos itens pendentes:
   → Sugerir geracao de cotacao antes de prosseguir
4. Se poucos itens:
   → Prosseguir com alerta
```

---

## Relatorios

### Relatorio de Precos Desatualizados

```markdown
## Precos para Atualizar

### Criticos (>180 dias)
| Material | Ultimo Preco | Ultima Cotacao |
|----------|--------------|----------------|
| GAS-R22  | R$ 280,00    | 2025-06-15     |

### Atencao (>90 dias)
| Material | Ultimo Preco | Ultima Cotacao |
|----------|--------------|----------------|
| TUB-CU-1/4 | R$ 28,50   | 2025-10-01     |
```

### Relatorio de Variacao

```markdown
## Variacao de Precos - Janeiro 2026

| Material | Preco Anterior | Preco Atual | Variacao |
|----------|----------------|-------------|----------|
| TUB-CU-1/4 | R$ 28,50     | R$ 32,50    | +14,0%   |
| GAS-R410A  | R$ 120,00    | R$ 115,00   | -4,2%    |
```

---

## Integracao Asana (via Gemini CLI)

Quando orcamento aprovado:

```
1. Receber solicitacao de criacao de tarefas
2. Chamar Gemini CLI com MCP do Asana
3. Criar tarefas no projeto existente:
   - Compra de materiais
   - Agendamento da instalacao
   - Execucao
   - Vistoria final
```

**Porque Gemini CLI:**
- Isolar contexto do MCP
- Nao consumir tokens do Claude
- MCP do Asana ja configurado no Gemini

---

*Especificacao da Skill Cotacoes - Sistema HVAC*

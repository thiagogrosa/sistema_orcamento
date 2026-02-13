---
name: hvac-cotacoes
description: Gerencia cotacoes de fornecedores e atualiza precos de materiais HVAC. Use para gerar e-mails de cotacao, atualizar precos ou listar materiais desatualizados.
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, WebFetch
---

# hvac-cotacoes - Gestao de Cotacoes HVAC

Gerencia cotacoes de fornecedores e atualizacao de precos.

## Funcionalidades

### 1. Gerar E-mail de Cotacao

**Entrada:**
```json
{
  "materiais": [{"codigo": "TUB_14_FLEX", "quantidade": 100}],
  "prazo_resposta_dias": 3,
  "observacoes": "Entrega em Porto Alegre"
}
```

**Saida:** Texto de e-mail formatado

```
Assunto: Solicitacao de Cotacao - [Categoria] - DD/MM/YYYY

Prezados,

Solicitamos cotacao para os materiais abaixo:

| Item | Descricao | Qtd | Unidade |
|------|-----------|-----|---------|
| 1 | Tubo cobre 1/4" flexivel | 100 | M |

Prazo para resposta: 3 dias uteis
Local de entrega: Porto Alegre/RS

Favor informar:
- Preco unitario
- Prazo de entrega
- Condicoes de pagamento
- Validade da cotacao

Atenciosamente,
[Empresa]
```

### 2. Atualizar Precos

**Entrada:**
```json
{
  "atualizacoes": [
    {"codigo": "TUB_14_FLEX", "preco": 20.00, "fonte": "COTACAO-FORN-20260102"}
  ]
}
```

**Processo:**
1. Ler `bases/materiais.json`
2. Atualizar precos informados
3. Atualizar `data_atualizacao`
4. Salvar arquivo

### 3. Listar Precos Desatualizados

**Saida:**
```markdown
## Precos para Atualizar

### Criticos (>180 dias)
| Material | Preco | Ultima Atualizacao |
|----------|-------|-------------------|

### Atencao (>90 dias)
| Material | Preco | Ultima Atualizacao |
|----------|-------|-------------------|
```

### 4. Relatorio de Variacao

Comparar precos atuais com anteriores:
```markdown
## Variacao de Precos

| Material | Anterior | Atual | Variacao |
|----------|----------|-------|----------|
| TUB_14_FLEX | R$ 18,00 | R$ 20,00 | +11,1% |
```

## Bases de Dados

- `bases/materiais.json` - precos de materiais
- `bases/fornecedores.json` - cadastro de fornecedores (criar se necessario)

## Integracao Asana

Quando orcamento aprovado, chamar Gemini CLI:
```bash
gemini "Criar tarefa no Asana: [descricao]"
```

Tarefas a criar:
- Compra de materiais
- Agendamento instalacao
- Execucao
- Vistoria final

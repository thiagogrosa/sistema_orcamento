# Instruções para Gemini CLI - Pesquisa Gmail

## Contexto

Você está auxiliando o setor de orçamentos da empresa Armant (climatização).
A conta de email é: **orcamentos2@armant.com.br**

O objetivo é buscar informações em emails para complementar demandas de orçamento que estão incompletas no Asana.

---

## Como Executar

### 1. Receber tarefa do Claude Code

O Claude Code vai enviar uma tarefa no formato:

```
PESQUISA_GMAIL:
- ID: TASK_XXX
- Asana: 26_XXX
- Cliente: Nome do Cliente
- Pesquisar: "termo1" OR "termo2"
- Período: últimos X meses
- Extrair: lista de campos
```

### 2. Acessar Gmail via MCP

Use as ferramentas MCP do Gmail para:
1. Pesquisar emails com os termos fornecidos
2. Ler o conteúdo dos emails encontrados
3. Extrair as informações solicitadas

### 3. Retornar Resultado

Retorne SEMPRE neste formato JSON:

```json
{
  "task_id": "TASK_XXX",
  "asana_id": "26_XXX",
  "status": "encontrado" | "parcial" | "nao_encontrado",
  "emails_analisados": 5,
  "dados": {
    "cliente": "Nome completo da empresa",
    "cnpj": "XX.XXX.XXX/XXXX-XX",
    "contato_nome": "Nome da pessoa de contato",
    "contato_telefone": "(XX) XXXXX-XXXX",
    "contato_email": "email@cliente.com",
    "endereco": "Endereço completo com CEP",
    "local_servico": "Se diferente do endereço",
    "tipo_servico": "Instalação | Manutenção | Projeto | PMOC",
    "detalhes": "Descrição detalhada do que foi solicitado",
    "prazo": "DD/MM/AAAA",
    "porte": "Pequeno | Médio | Grande",
    "origem": "Comercial | Cliente direto | Diretoria | Engenharia",
    "licitacao": "Sim - Edital XX | Não",
    "observacoes": "Qualquer info adicional relevante"
  },
  "emails_fonte": [
    {
      "data": "2026-01-15",
      "assunto": "Orçamento climatização",
      "de": "cliente@email.com",
      "resumo": "Breve resumo do conteúdo relevante"
    }
  ],
  "campos_nao_encontrados": ["cnpj", "prazo"]
}
```

---

## Regras de Extração

### Identificação de Tipo de Serviço

| Palavras-chave | Tipo |
|---------------|------|
| instalação, obra, VRF, split, equipamento novo | Instalação |
| manutenção, corretiva, preventiva, reparo, conserto | Manutenção |
| PMOC, contrato, plano de manutenção | Manutenção (PMOC) |
| projeto, dimensionamento, laudo, ART | Projeto |
| higienização, limpeza | Manutenção (Higienização) |
| filtro, peça, turbina, placa | Manutenção (Peças) |

### Identificação de Porte

| Critério | Porte |
|----------|-------|
| 1-5 equipamentos, serviço simples | Pequeno |
| 6-50 equipamentos, obra média | Médio |
| 50+ equipamentos, obra grande, shopping, indústria | Grande |
| PMOC com muitas unidades | Grande |

### Extração de Contatos

- Buscar assinatura do email para nome/telefone/cargo
- CNPJ pode estar em assinatura ou corpo do email
- Verificar CC para contatos adicionais

---

## Fluxo de Trabalho

```
Claude Code                          Gemini CLI
    |                                    |
    |--- Envia TASK_XXX ---------------->|
    |                                    |
    |                            [Pesquisa Gmail]
    |                            [Extrai dados]
    |                                    |
    |<-- Retorna JSON -------------------|
    |                                    |
[Atualiza Asana]                         |
[Próxima task]                           |
```

---

## Exemplo Completo

**Entrada (do Claude Code):**
```
PESQUISA_GMAIL:
- ID: TASK_001
- Asana: 26_038
- Cliente: Semapi RS
- Pesquisar: "Semapi" OR "higienização"
- Período: últimos 6 meses
- Extrair: cliente, cnpj, contato, endereco, detalhes, prazo
```

**Saída (do Gemini):**
```json
{
  "task_id": "TASK_001",
  "asana_id": "26_038",
  "status": "encontrado",
  "emails_analisados": 3,
  "dados": {
    "cliente": "Semapi Serviços de Manutenção Predial Ltda",
    "cnpj": "12.345.678/0001-90",
    "contato_nome": "João Silva",
    "contato_telefone": "(51) 99999-8888",
    "contato_email": "joao.silva@semapi.com.br",
    "endereco": "Av. Ipiranga, 1000 - Porto Alegre/RS",
    "tipo_servico": "Manutenção (Higienização)",
    "detalhes": "Higienização de 25 equipamentos split em escritório comercial",
    "prazo": "15/02/2026",
    "porte": "Médio",
    "origem": "Cliente direto",
    "licitacao": "Não"
  },
  "emails_fonte": [
    {
      "data": "2026-01-20",
      "assunto": "Solicitação de orçamento - Higienização AC",
      "de": "joao.silva@semapi.com.br",
      "resumo": "Solicitação para higienização de 25 splits no escritório sede"
    }
  ],
  "campos_nao_encontrados": []
}
```

---

## Arquivo de Tarefas

As tarefas completas estão em:
`/root/thiagorosa/gestao-orcamentos/gemini-tasks/pesquisa-gmail-pendentes.md`

Salvar resultados em:
`/root/thiagorosa/gestao-orcamentos/gemini-tasks/resultados-pesquisa-gmail.json`

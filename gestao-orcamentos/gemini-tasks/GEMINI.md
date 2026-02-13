# Contexto para Gemini CLI - Pesquisa de Emails

## Sua Missão

Você é um assistente especializado em extrair informações de emails para complementar dados de orçamentos de climatização.

**Empresa:** Armant - Setor de Orçamentos de Climatização
**Conta Gmail:** orcamentos2@armant.com.br
**Objetivo:** Pesquisar emails e extrair informações para atualizar tarefas no Asana

---

## Como Trabalhar

### 1. Acesso ao Gmail

Use o MCP do Gmail para pesquisar emails na conta `orcamentos2@armant.com.br`.

### 2. Fluxo de Trabalho

Para cada tarefa de pesquisa:
1. Execute a busca com os termos especificados
2. Leia os emails encontrados
3. Extraia as informações solicitadas
4. Retorne no formato JSON especificado

### 3. Arquivo de Saída

Salve os resultados em: `resultados-pesquisa-gmail.json`

---

## Tarefas de Pesquisa (Prioridade Alta)

Execute as pesquisas na ordem abaixo. Comece pelas de prioridade ALTA.

### TASK_001: 26_038 Semapi RS - Higienização
```
Pesquisar: "Semapi"
Período: últimos 6 meses
Extrair: cliente, CNPJ, contato, endereço, quantidade de equipamentos, detalhes, prazo
```

### TASK_002: 26_041 Zanon Advogados - Corretiva
```
Pesquisar: "Zanon Advogados" OR "Zanon"
Período: últimos 6 meses
Extrair: CNPJ, contato, endereço, tipo de serviço, detalhes, prazo
```

### TASK_003: 26_049 Porto Seguro - Vitória/ES
```
Pesquisar: "Porto Seguro" AND "Vitória"
Período: últimos 6 meses
Extrair: contato local, endereço em Vitória/ES, tipo de serviço, detalhes, prazo
```

### TASK_004: 26_023 Easy Planning CAU/SC
```
Pesquisar: "Easy Planning" OR "CAU SC"
Período: últimos 6 meses
Extrair: nome completo, CNPJ, contato, endereço, tipo de serviço, detalhes
```

### TASK_005: 26_055 Mútua RS - PMOC
```
Pesquisar: "Mútua" OR "MUTUA" OR "Caixa de Assistência dos Profissionais do CREA"
Período: últimos 6 meses
Extrair: contato, endereços das unidades, quantidade de equipamentos, detalhes do PMOC, prazo
```

### TASK_006: 26_047 Banrisul - Ag Morrinhos do Sul
```
Pesquisar: "Banrisul" AND "Morrinhos do Sul"
Período: últimos 6 meses
Extrair: contato Banrisul, endereço da agência, tipo de serviço, detalhes técnicos
```

### TASK_007: 26_043 Banrisul - Ag Faxinal do Soturno
```
Pesquisar: "Banrisul" AND "Faxinal do Soturno"
Período: últimos 6 meses
Extrair: contato, endereço da agência, tipo de serviço, detalhes técnicos
```

### TASK_008: 25_837 Clínica Bertol Marques
```
Pesquisar: "Bertol Marques" OR "Clínica Bertol"
Período: últimos 12 meses
Extrair: nome completo da clínica, CNPJ, contato, endereço, tipo de serviço, detalhes
```

### TASK_009: 26_053 Edifício Mondrian Boldinc
```
Pesquisar: "Mondrian" OR "Boldinc"
Período: últimos 6 meses
Extrair: cliente (condomínio/construtora?), contato, endereço, tipo de serviço, detalhes
```

### TASK_010: 26_044 LFDA - Manutenção
```
Pesquisar: "LFDA"
Período: últimos 6 meses
Extrair: nome completo, CNPJ, contato, endereço, tipo de manutenção, detalhes
```

### TASK_011: 26_054 Teatro Paschoal e Casa Arte NH
```
Pesquisar: "Teatro Paschoal" OR "Casa de Arte" AND "Novo Hamburgo"
Período: últimos 6 meses
Extrair: contato, endereço completo, tipo de serviço, detalhes
```

### TASK_012: 26_056 TRE São Leopoldo
```
Pesquisar: "TRE" AND "São Leopoldo"
Período: últimos 6 meses
Extrair: contato do TRE, endereço, tipo de serviço, detalhes técnicos
```

### TASK_013: 26_058 Hospital Dom Vicente - Obra
```
Pesquisar: "Hospital Dom Vicente" OR "Dom Vicente Scherer" OR "Santa Casa"
Período: últimos 6 meses
Extrair: contato, endereço/local da obra, detalhes da instalação, porte do projeto
```

---

## Tarefas de Pesquisa (Prioridade Média)

### TASK_014: 26_018 Cyrela Duo Concept
```
Pesquisar: "Cyrela" AND "Duo Concept"
Extrair: contato Cyrela, CNPJ, detalhes do sistema VRF, porte
```

### TASK_015: 26_040 Almeida Junior - Shoppings SC
```
Pesquisar: "Almeida Junior" AND "Shopping"
Extrair: contato, quais shoppings, detalhes da corretiva, equipamentos
```

### TASK_016: 26_036 Cassi - POA Norte
```
Pesquisar: "Cassi" AND "POA Norte"
Extrair: endereço completo, contato, detalhes da instalação, porte
```

### TASK_017: 26_010 Neo BPO - PMOC
```
Pesquisar: "Neo BPO" OR "NeoBPO"
Extrair: CNPJ, contato, endereços, quantidade de equipamentos, detalhes do PMOC
```

### TASK_018: 25_784 Melnick Even PDV
```
Pesquisar: "Melnick" AND "PDV"
Período: últimos 12 meses
Extrair: endereço do PDV, contato, detalhes da corretiva
```

### TASK_019: 26_008 BRDE - PMOC
```
Pesquisar: "BRDE" AND "PMOC"
Extrair: contato, endereços, quantidade de equipamentos, escopo do PMOC
```

### TASK_020: 26_011 Arezzo - Reserva Caxias/RJ
```
Pesquisar: "Arezzo" AND "Reserva"
Extrair: contato Arezzo, endereço completo, detalhes da instalação
```

### TASK_021: 26_014/26_015 Expansão Imóveis
```
Pesquisar: "Expansão Imóveis"
Extrair: contato, endereço, detalhes do serviço concluído e limpeza química
```

### TASK_022: 26_027 FIERGS - Bento Gonçalves
```
Pesquisar: "FIERGS" AND "Bento Gonçalves"
Extrair: contato FIERGS, endereço da obra, detalhes da instalação
```

### TASK_023: 26_031 Ambaar POA - PMOC
```
Pesquisar: "Ambaar" AND "PMOC"
Extrair: contato, endereço, quantidade de equipamentos, detalhes da renovação
```

### TASK_024: 26_033 Senac Penha - Condensadoras
```
Pesquisar: "Senac" AND "Penha"
Extrair: contato Senac, endereço em Penha/SC, quantidade e modelos de condensadoras
```

### TASK_025: 26_006 PROEE Krystal - Obra
```
Pesquisar: "PROEE" AND "Krystal"
Extrair: contato PROEE, local exato da obra, prazo, detalhes
```

### TASK_026: 25_860 BB Abelardo Luz - SC
```
Pesquisar: "Banco do Brasil" AND "Abelardo Luz"
Período: últimos 12 meses
Extrair: contato BB, endereço da agência, tipo de serviço, detalhes
```

### TASK_027: 26_048 CEO Instituto Olhos Marcon
```
Pesquisar: "Marcon" OR "Instituto de Olhos"
Extrair: porte do contrato, quantidade de equipamentos, frequência das preventivas
```

---

## Tarefas de Pesquisa (Prioridade Baixa)

### TASK_028: Banrisul - Várias Agências
Pesquisar separadamente para definir tipo de serviço:
- "Banrisul" AND "Ivoti"
- "Banrisul" AND "Pareci Novo"
- "Banrisul" AND "Chuí"
- "Banrisul" AND "Joinville"
- "Banrisul" AND "Tramandaí"
- "Banrisul" AND "Canoas"
- "Banrisul" AND "Coronel Pilar"
- "Banrisul" AND "Pelotas"
- "Banrisul" AND "Sureg Centro"

```
Extrair para cada: tipo de serviço (instalação, manutenção, troca?), detalhes técnicos
```

### TASK_029: 26_029 TRE - Pedro Osório
```
Pesquisar: "TRE" AND "Pedro Osório"
Extrair: tipo de serviço, detalhes
```

### TASK_030: 26_060 Porto Seguro - PMOC
```
Pesquisar: "Porto Seguro" AND "PMOC" (excluir Vitória)
Extrair: contato completo, endereço, locais do PMOC
```

### TASK_031: 26_062 Colombo Park Shopping - PMOC
```
Pesquisar: "Colombo Park Shopping" OR "Colombo Shopping"
Extrair: contato do shopping, escopo exato solicitado
```

---

## Formato de Saída JSON

Para cada tarefa pesquisada, adicione ao arquivo `resultados-pesquisa-gmail.json`:

```json
{
  "task_id": "TASK_001",
  "asana_id": "26_038",
  "status": "encontrado",
  "emails_analisados": 3,
  "dados": {
    "cliente": "Nome completo da empresa",
    "cnpj": "XX.XXX.XXX/XXXX-XX",
    "contato_nome": "Nome da pessoa",
    "contato_telefone": "(XX) XXXXX-XXXX",
    "contato_email": "email@cliente.com",
    "endereco": "Endereço completo com CEP",
    "local_servico": "Se diferente do endereço",
    "tipo_servico": "Instalação | Manutenção | Projeto | PMOC",
    "detalhes": "Descrição do que foi solicitado",
    "prazo": "DD/MM/AAAA",
    "porte": "Pequeno | Médio | Grande",
    "origem": "Comercial | Cliente direto | Diretoria | Engenharia",
    "observacoes": "Informações adicionais"
  },
  "emails_fonte": [
    {
      "data": "2026-01-15",
      "assunto": "Assunto do email",
      "de": "remetente@email.com",
      "resumo": "Breve resumo do conteúdo relevante"
    }
  ],
  "campos_nao_encontrados": ["cnpj", "prazo"]
}
```

### Valores possíveis para status:
- `"encontrado"` - Todas as informações principais encontradas
- `"parcial"` - Algumas informações encontradas
- `"nao_encontrado"` - Nenhum email relevante encontrado

---

## Regras para Identificar Tipo de Serviço

| Palavras-chave no email | Tipo de Serviço |
|------------------------|-----------------|
| instalação, obra, VRF, split novo, equipamento novo | Instalação |
| manutenção, corretiva, preventiva, reparo, conserto | Manutenção |
| PMOC, contrato, plano de manutenção | Manutenção (PMOC) |
| projeto, dimensionamento, laudo, ART | Projeto |
| higienização, limpeza | Manutenção (Higienização) |
| filtro, peça, turbina, placa | Manutenção (Peças) |

## Regras para Identificar Porte

| Critério | Porte |
|----------|-------|
| 1-5 equipamentos, serviço simples, residencial | Pequeno |
| 6-50 equipamentos, obra média, escritório | Médio |
| 50+ equipamentos, shopping, indústria, hospital | Grande |

---

## Dicas para Extração

1. **Assinatura do email**: Geralmente contém nome, telefone, cargo e às vezes CNPJ
2. **CC do email**: Pode ter contatos adicionais importantes
3. **Anexos mencionados**: Podem indicar projetos, planilhas de equipamentos
4. **Histórico de respostas**: Emails anteriores na thread podem ter mais detalhes
5. **Pedidos de orçamento**: Costumam ter prazo, escopo e especificações

---

## Resumo das Tarefas

| Prioridade | Quantidade | Foco |
|------------|------------|------|
| ALTA | 13 | Dados críticos faltando |
| MÉDIA | 14 | Dados parciais faltando |
| BAIXA | 4 | Apenas tipo/classificação |
| **TOTAL** | **31** | |

---

## Ao Finalizar

1. Salve todos os resultados em `resultados-pesquisa-gmail.json`
2. Informe quantas tarefas foram encontradas/parciais/não encontradas
3. Liste as tarefas que precisam de busca manual (sem emails)

O Claude Code vai usar esses resultados para atualizar as tarefas no Asana.

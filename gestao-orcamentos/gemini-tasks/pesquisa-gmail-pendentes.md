# Tarefas de Pesquisa no Gmail para Gemini CLI

**Data de Geração:** 2026-02-05 (ATUALIZADO após validação Drive)
**Conta Gmail:** orcamentos2@armant.com.br
**Objetivo:** Buscar informações complementares para demandas de orçamento no Asana

---

## Instruções para o Gemini

1. Acesse o Gmail via MCP
2. Para cada tarefa abaixo, pesquise emails relacionados
3. Extraia as informações solicitadas
4. Retorne os dados no formato JSON especificado ao final

---

## PRIORIDADE ALTA (Dados críticos faltando)

### TASK_001: 26_038 Semapi RS - Higienização
**Pesquisar:** "Semapi" (subject: OR body:)
**Período:** últimos 6 meses
**Extrair:**
- Nome completo do cliente/empresa
- CNPJ
- Contato (nome, telefone, email)
- Endereço completo
- Quantidade de equipamentos
- Detalhes do serviço solicitado
- Prazo mencionado

---

### TASK_002: 26_041 Zanon Advogados - Corretiva
**Pesquisar:** "Zanon Advogados" OR "Zanon" (subject:)
**Período:** últimos 6 meses
**Extrair:**
- CNPJ
- Contato (nome, telefone, email)
- Endereço completo
- Tipo de serviço (corretiva de quê?)
- Detalhes do problema/solicitação
- Prazo mencionado

---

### TASK_003: 26_049 Porto Seguro - Vitória/ES
**Pesquisar:** "Porto Seguro" AND "Vitória" OR "Porto Seguro" AND "ES"
**Período:** últimos 6 meses
**Extrair:**
- Contato local (nome, telefone, email)
- Endereço completo em Vitória/ES
- Tipo de serviço (instalação, manutenção, projeto?)
- Detalhes da demanda
- Prazo

---

### TASK_004: 26_023 Easy Planning CAU/SC
**Pesquisar:** "Easy Planning" OR "CAU SC"
**Período:** últimos 6 meses
**Extrair:**
- Nome completo da empresa
- CNPJ
- Contato (nome, telefone, email)
- Endereço
- Tipo de serviço
- Detalhes da demanda

---

### TASK_005: 26_055 Mútua RS - PMOC (CORRIGIDO)
**Pesquisar:** "Mútua" OR "MUTUA" OR "Caixa de Assistência dos Profissionais do CREA"
**Período:** últimos 6 meses
**Extrair:**
- Contato Mútua (nome, telefone, email)
- Endereço(s) das unidades
- Quantidade de equipamentos
- Detalhes do PMOC
- Prazo

---

### TASK_006: 26_047 Banrisul - Ag Morrinhos do Sul
**Pesquisar:** "Banrisul" AND "Morrinhos do Sul"
**Período:** últimos 6 meses
**Extrair:**
- Contato do Banrisul (nome, telefone, email)
- Endereço da agência
- Tipo de serviço (instalação, manutenção?)
- Detalhes técnicos

---

### TASK_007: 26_043 Banrisul - Ag Faxinal do Soturno
**Pesquisar:** "Banrisul" AND "Faxinal do Soturno"
**Período:** últimos 6 meses
**Extrair:**
- Contato do Banrisul
- Endereço da agência
- Tipo de serviço
- Detalhes técnicos

---

### TASK_008: 25_837 Clínica Bertol Marques
**Pesquisar:** "Bertol Marques" OR "Clínica Bertol"
**Período:** últimos 12 meses
**Extrair:**
- Nome completo da clínica
- CNPJ
- Contato (nome, telefone, email)
- Endereço
- Tipo de serviço
- Detalhes

---

### TASK_009: 26_053 Edifício Mondrian Boldinc
**Pesquisar:** "Mondrian" OR "Boldinc"
**Período:** últimos 6 meses
**Extrair:**
- Cliente (condomínio? construtora?)
- Contato (nome, telefone, email)
- Endereço
- Tipo de serviço
- Detalhes

---

### TASK_010: 26_044 LFDA - Manutenção
**Pesquisar:** "LFDA"
**Período:** últimos 6 meses
**Extrair:**
- Nome completo da empresa
- CNPJ
- Contato
- Endereço
- Tipo de manutenção
- Detalhes

---

### TASK_011: 26_054 Teatro Paschoal e Casa Arte NH (CORRIGIDO)
**Pesquisar:** "Teatro Paschoal" OR "Casa de Arte" AND "Novo Hamburgo"
**Período:** últimos 6 meses
**Extrair:**
- Contato (nome, telefone, email)
- Endereço completo
- Tipo de serviço
- Detalhes da demanda

---

### TASK_012: 26_056 TRE São Leopoldo (CORRIGIDO)
**Pesquisar:** "TRE" AND "São Leopoldo"
**Período:** últimos 6 meses
**Extrair:**
- Contato do TRE (nome, telefone, email)
- Endereço
- Tipo de serviço
- Detalhes técnicos

---

### TASK_013: 26_058 Hospital Dom Vicente (CORRIGIDO)
**Pesquisar:** "Hospital Dom Vicente" OR "Dom Vicente Scherer" OR "Santa Casa"
**Período:** últimos 6 meses
**Extrair:**
- Contato (nome, telefone, email)
- Endereço/local da obra
- Detalhes da instalação
- Porte do projeto

---

## PRIORIDADE MÉDIA (Dados parciais faltando)

### TASK_014: 26_018 Cyrela Duo Concept - POA
**Pesquisar:** "Cyrela" AND "Duo Concept"
**Período:** últimos 6 meses
**Extrair:**
- Contato Cyrela (nome, telefone, email)
- CNPJ
- Detalhes do sistema VRF
- Porte do projeto

---

### TASK_015: 26_040 Almeida Junior - Shoppings SC
**Pesquisar:** "Almeida Junior" AND ("Balneário" OR "Shopping")
**Período:** últimos 6 meses
**Extrair:**
- Contato (nome, telefone, email)
- Quais shoppings (Balneário, outros?)
- Detalhes da manutenção corretiva
- Equipamentos envolvidos

---

### TASK_016: 26_036 Cassi - POA Norte (Instalação)
**Pesquisar:** "Cassi" AND "POA Norte" AND "instalação"
**Período:** últimos 6 meses
**Extrair:**
- Endereço completo POA Norte
- Contato
- Detalhes da instalação
- Porte

---

### TASK_017: 26_010 Neo BPO - PMOC
**Pesquisar:** "Neo BPO" OR "NeoBPO"
**Período:** últimos 6 meses
**Extrair:**
- CNPJ
- Contato
- Endereço(s)
- Quantidade de equipamentos
- Detalhes do PMOC

---

### TASK_018: 25_784 Melnick Even PDV - Corretiva
**Pesquisar:** "Melnick" AND "PDV"
**Período:** últimos 12 meses
**Extrair:**
- Endereço do PDV
- Contato
- Detalhes da corretiva
- Proposta anterior (para reenvio)

---

### TASK_019: 26_008 BRDE - PMOC
**Pesquisar:** "BRDE" AND "PMOC"
**Período:** últimos 6 meses
**Extrair:**
- Contato
- Endereço(s)
- Quantidade de equipamentos
- Escopo do PMOC

---

### TASK_020: 26_011 Arezzo - Reserva Caxias/RJ
**Pesquisar:** "Arezzo" AND ("Reserva" OR "Caxias")
**Período:** últimos 6 meses
**Extrair:**
- Contato Arezzo
- Endereço completo
- Detalhes da instalação
- Projetos arquitetônicos mencionados

---

### TASK_021: 26_014/26_015 Expansão Imóveis
**Pesquisar:** "Expansão Imóveis"
**Período:** últimos 6 meses
**Extrair:**
- Contato
- Endereço
- Detalhes do serviço concluído (26_014)
- Detalhes da limpeza química (26_015)

---

### TASK_022: 26_027 FIERGS - Bento Gonçalves
**Pesquisar:** "FIERGS" AND "Bento Gonçalves"
**Período:** últimos 6 meses
**Extrair:**
- Contato FIERGS
- Endereço da obra
- Detalhes da instalação

---

### TASK_023: 26_031 Ambaar POA - Renovação PMOC
**Pesquisar:** "Ambaar" AND "PMOC"
**Período:** últimos 6 meses
**Extrair:**
- Contato
- Endereço
- Quantidade de equipamentos
- Detalhes da renovação

---

### TASK_024: 26_033 Senac Penha - Condensadoras
**Pesquisar:** "Senac" AND "Penha"
**Período:** últimos 6 meses
**Extrair:**
- Contato Senac
- Endereço em Penha/SC
- Quantidade e modelos de condensadoras
- Detalhes técnicos

---

### TASK_025: 26_006 PROEE Krystal - Obra
**Pesquisar:** "PROEE" AND "Krystal"
**Período:** últimos 6 meses
**Extrair:**
- Contato PROEE
- Local exato da obra
- Prazo
- Detalhes

---

### TASK_026: 25_860 BB Abelardo Luz - SC
**Pesquisar:** "Banco do Brasil" AND "Abelardo Luz"
**Período:** últimos 12 meses
**Extrair:**
- Contato BB
- Endereço da agência
- Tipo de serviço
- Detalhes

---

### TASK_027: 26_048 CEO Instituto Olhos Marcon
**Pesquisar:** "Marcon" OR "Instituto de Olhos" OR "Oftalmologia"
**Período:** últimos 6 meses
**Extrair:**
- Porte do contrato
- Quantidade de equipamentos
- Frequência das preventivas

---

## PRIORIDADE BAIXA (Classificação/tipo faltando)

### TASK_028: Banrisul - Várias Agências (definir tipo de serviço)
**Pesquisar:** Para cada agência, buscar email específico
- "Banrisul" AND "Ivoti"
- "Banrisul" AND "Pareci Novo"
- "Banrisul" AND "Chuí"
- "Banrisul" AND "Joinville"
- "Banrisul" AND "Tramandaí"
- "Banrisul" AND "Canoas"
- "Banrisul" AND "Coronel Pilar"
- "Banrisul" AND "Pelotas"
- "Banrisul" AND "Sureg Centro"
**Extrair para cada:**
- Tipo de serviço (instalação, manutenção, troca?)
- Detalhes técnicos

---

### TASK_029: 26_029 TRE - Pedro Osório
**Pesquisar:** "TRE" AND "Pedro Osório"
**Período:** últimos 6 meses
**Extrair:**
- Tipo de serviço
- Detalhes

---

### TASK_030: 26_060 Porto Seguro - PMOC
**Pesquisar:** "Porto Seguro" AND "PMOC" NOT "Vitória"
**Período:** últimos 6 meses
**Extrair:**
- Contato completo
- Endereço
- Local(is) do PMOC

---

### TASK_031: 26_062 Colombo Park Shopping - PMOC
**Pesquisar:** "Colombo Park Shopping" OR "Colombo Shopping"
**Período:** últimos 6 meses
**Extrair:**
- Contato do shopping (gerência/manutenção)
- Escopo exato solicitado

---

## Formato de Retorno Esperado

Para cada TASK, retornar JSON no formato:

```json
{
  "task_id": "TASK_XXX",
  "asana_id": "26_XXX",
  "encontrado": true/false,
  "emails_analisados": 5,
  "dados_extraidos": {
    "cliente": "Nome completo",
    "cnpj": "XX.XXX.XXX/XXXX-XX",
    "contato_nome": "Nome",
    "contato_telefone": "(XX) XXXXX-XXXX",
    "contato_email": "email@exemplo.com",
    "endereco": "Endereço completo",
    "tipo_servico": "Instalação/Manutenção/Projeto/PMOC",
    "detalhes": "Descrição do serviço solicitado",
    "prazo": "DD/MM/AAAA",
    "porte": "Pequeno/Médio/Grande",
    "observacoes": "Informações adicionais relevantes"
  },
  "emails_referencia": [
    {
      "data": "DD/MM/AAAA",
      "assunto": "Assunto do email",
      "remetente": "email@exemplo.com"
    }
  ]
}
```

---

## Resumo Atualizado

| Prioridade | Quantidade | Descrição |
|------------|------------|-----------|
| ALTA | 13 | Dados críticos faltando (inclui 3 tarefas corrigidas) |
| MÉDIA | 14 | Dados parciais faltando |
| BAIXA | 4 | Apenas tipo/classificação faltando |
| **TOTAL** | **31** | Tarefas a pesquisar |

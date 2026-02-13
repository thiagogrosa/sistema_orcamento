# Pesquisa de Informações no Gmail - Gemini

## Contexto do Projeto

Você está auxiliando no sistema de gestão de orçamentos do Setor de Climatização da Armant. Estamos sincronizando demandas entre pastas do Google Drive e tarefas no Asana.

**Conta de email:** orcamentos2@armant.com.br

---

## Sua Tarefa

Buscar no Gmail informações de contato e detalhes de demandas específicas que estão incompletas no Asana.

---

## Demandas que Precisam de Informações

### 1️⃣ 26_060 - Porto Seguro PMOC

**O que já sabemos:**
- Cliente: Porto Seguro
- Tipo: PMOC (Plano de Manutenção, Operação e Controle)
- Pasta no Drive: `26_060_PORTO_SEGURO_PMOC`

**O que precisamos encontrar:**
- Nome completo do cliente/estabelecimento
- CNPJ
- Nome do contato
- Telefone do contato
- Email do contato
- Endereço completo
- Cidade/Estado
- Detalhes da demanda (escopo do PMOC)
- Prazo solicitado
- Data da solicitação

**Palavras-chave para busca:**
- "Porto Seguro" + "PMOC"
- "Porto Seguro" + "manutenção"
- "Porto Seguro" + "climatização"
- Data aproximada: Janeiro-Fevereiro 2026

---

### 2️⃣ 26_062 - Colombo Park Shopping PMOC

**O que já sabemos:**
- Cliente: Colombo Park Shopping
- CNPJ: 17.244.360/0001-31
- Endereço: Rua Dorval Ceccon, 664, Colombo – PR, CEP: 83.405-030
- Sistema: 3 Chillers (490 TR total), 7 Fan Coils
- Existe PMOC anterior feito pelo Grupo Associar

**O que precisamos encontrar:**
- Nome do contato no shopping (gerente de manutenção ou responsável)
- Telefone do contato
- Email do contato
- Escopo exato solicitado (renovação de PMOC? Novo contrato? Troca de fornecedor?)
- Prazo solicitado
- Data da solicitação
- Se há edital/cotação formal

**Palavras-chave para busca:**
- "Colombo Park Shopping"
- "Colombo" + "Shopping" + "PMOC"
- "Colombo" + "Paraná" + "climatização"
- Data aproximada: Janeiro-Fevereiro 2026

---

## Formato de Resposta Esperado

Para cada demanda encontrada, forneça as informações no seguinte formato:

```
### Demanda: [ID - Nome]

**Email encontrado:**
- De: [remetente]
- Data: [data]
- Assunto: [assunto do email]

**Informações Extraídas:**

Cliente: [nome completo]
CNPJ: [número do CNPJ]
Contato: [nome da pessoa]
Telefone: [telefone com DDD]
Email: [email do contato]
Endereço: [endereço completo]
Local: [cidade/estado]

**Detalhes da Demanda:**
[Descrição do que foi solicitado]

**Prazo:**
[Prazo solicitado pelo cliente, se mencionado]

**Observações Adicionais:**
[Qualquer informação relevante: licitação, urgência, concorrentes, etc.]
```

---

## Instruções de Busca

1. **Período de busca:** Janeiro-Fevereiro 2026 (prioridade), mas verificar também Dezembro 2025

2. **Caixas de email para verificar:**
   - Caixa de entrada principal
   - Pasta/Label específica se houver (ex: "[1. Incluir/Solicitação]")
   - Enviados (caso a solicitação tenha vindo por telefone e enviamos confirmação)

3. **Prioridade:**
   - Emails COM as informações de contato completas
   - Emails que mencionem número de ID (26_060, 26_062)
   - Emails recentes (últimos 60 dias)

4. **Se não encontrar email direto:**
   - Buscar threads de conversação relacionadas
   - Verificar se há menção em outros emails
   - Informar que não foi encontrado

---

## Notas Importantes

- Alguns emails podem estar em threads longas - leia a conversa completa
- Preste atenção em anexos mencionados que possam ter informações
- Se houver múltiplos emails sobre a mesma demanda, compile as informações
- Indique o grau de confiança das informações (certo/provável/incerto)

---

## Após a Busca

Depois de encontrar as informações, retorne APENAS os dados extraídos no formato especificado acima. Não é necessário tomar nenhuma ação adicional - essas informações serão usadas para atualizar as tarefas no Asana.

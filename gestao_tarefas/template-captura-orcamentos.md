# Template de Captura de Orcamentos

Este documento descreve como capturar informacoes de demandas dispersas (emails, anotacoes, etc.) e transforma-las em um formato processavel pela IA para insercao no Asana.

---

## Fluxo de Captura

```
Fonte (email, anotacao, etc.)
          |
          v
   Captura em texto livre
          |
          v
   IA processa e extrai dados
          |
          v
   JSON estruturado
          |
          v
   IA insere no Asana via MCP
```

---

## Como Usar

### Passo 1: Copie a informacao original

Cole o texto do email, foto da anotacao, ou descreva a demanda em texto livre.

### Passo 2: Envie para a IA com o prompt de extracao

### Passo 3: IA gera JSON estruturado

### Passo 4: IA insere no Asana

---

## Prompt de Extracao

Use este prompt para a IA extrair os dados:

```
Analise o texto abaixo e extraia as informacoes para criar uma tarefa de orcamento de climatizacao.

TEXTO:
[COLAR TEXTO AQUI]

---

Extraia as seguintes informacoes e retorne em JSON:

{
  "cliente": "nome da empresa ou pessoa",
  "contato": "nome do contato se houver",
  "telefone": "telefone se houver",
  "email": "email se houver",
  "local": "cidade e estado",
  "prazo": "data no formato YYYY-MM-DD, se nao informada coloque null",
  "tipo_servico": "instalacao | manutencao | projeto (inferir do contexto)",
  "eh_licitacao": true ou false,
  "numero_edital": "numero se for licitacao",
  "porte": "pequeno | medio | grande (inferir pelo contexto ou deixar null)",
  "origem": "comercial | cliente_direto | diretoria | engenharia (inferir do contexto)",
  "descricao": "resumo do que foi solicitado",
  "urgente": true ou false (se mencionar urgencia),
  "cliente_estrategico": false (a menos que explicitamente mencionado)
}

Regras:
- Se nao conseguir inferir tipo_servico, pergunte ao usuario
- Se o prazo nao estiver explicito, deixe null
- Se parecer licitacao (mencionar edital, pregao, etc), marque eh_licitacao = true
- Infira o porte pelo tamanho do projeto mencionado
```

---

## Exemplos de Captura

### Exemplo 1: Email do Comercial

**Texto original:**
```
Oi pessoal,

Recebi contato do Shopping Center Norte de SP pedindo orcamento para instalacao de
sistema de climatizacao no novo andar que estao construindo. Sao aproximadamente
2000m2. O contato e a Maria (maria@shoppingnorte.com.br, 11 98765-4321).
Eles querem o orcamento ate dia 25 desse mes.

Abs,
Carlos - Comercial
```

**JSON extraido pela IA:**
```json
{
  "cliente": "Shopping Center Norte",
  "contato": "Maria",
  "telefone": "11 98765-4321",
  "email": "maria@shoppingnorte.com.br",
  "local": "Sao Paulo - SP",
  "prazo": "2025-01-25",
  "tipo_servico": "instalacao",
  "eh_licitacao": false,
  "numero_edital": null,
  "porte": "grande",
  "origem": "comercial",
  "descricao": "Instalacao de sistema de climatizacao em novo andar do shopping, aproximadamente 2000m2",
  "urgente": false,
  "cliente_estrategico": false
}
```

---

### Exemplo 2: Anotacao em Papel

**Texto transcrito:**
```
Prefeitura Uberlandia
Pregao 045/2025
Manutencao preventiva
Prazo edital: 15/02
Ligar p/ confirmar docs
```

**JSON extraido pela IA:**
```json
{
  "cliente": "Prefeitura de Uberlandia",
  "contato": null,
  "telefone": null,
  "email": null,
  "local": "Uberlandia - MG",
  "prazo": "2025-02-15",
  "tipo_servico": "manutencao",
  "eh_licitacao": true,
  "numero_edital": "Pregao 045/2025",
  "porte": null,
  "origem": "licitacao",
  "descricao": "Manutencao preventiva - licitacao. Pendente: ligar para confirmar documentacao",
  "urgente": false,
  "cliente_estrategico": false
}
```

---

### Exemplo 3: Mensagem Direta do Cliente

**Texto original:**
```
Boa tarde!

Sou o Marcos da Clinica Saude Total aqui de Ribeirao Preto. Estamos precisando
de um projeto de climatizacao para nossa nova unidade que vai abrir em marco.
Sao 3 andares, aproximadamente 800m2 no total.

Voces conseguem enviar um orcamento essa semana? E urgente pois precisamos
fechar o fornecedor ate sexta.

Meu telefone: 16 99999-8888
Email: marcos@clinicasaudetotal.com.br

Obrigado!
```

**JSON extraido pela IA:**
```json
{
  "cliente": "Clinica Saude Total",
  "contato": "Marcos",
  "telefone": "16 99999-8888",
  "email": "marcos@clinicasaudetotal.com.br",
  "local": "Ribeirao Preto - SP",
  "prazo": "2025-01-24",
  "tipo_servico": "projeto",
  "eh_licitacao": false,
  "numero_edital": null,
  "porte": "medio",
  "origem": "cliente_direto",
  "descricao": "Projeto de climatizacao para nova unidade da clinica. 3 andares, aproximadamente 800m2. Abertura prevista para marco",
  "urgente": true,
  "cliente_estrategico": false
}
```

---

### Exemplo 4: Demanda da Diretoria

**Texto original:**
```
Thiago,

O diretor pediu para priorizar o orcamento do Banco ABC. Eles querem trocar
todo o sistema de ar do predio da matriz em BH. Projeto grande.

Falar com o Gerente de Facilities deles - Roberto.
```

**JSON extraido pela IA:**
```json
{
  "cliente": "Banco ABC",
  "contato": "Roberto (Gerente de Facilities)",
  "telefone": null,
  "email": null,
  "local": "Belo Horizonte - MG",
  "prazo": null,
  "tipo_servico": "projeto",
  "eh_licitacao": false,
  "numero_edital": null,
  "porte": "grande",
  "origem": "diretoria",
  "descricao": "Substituicao completa do sistema de ar condicionado do predio da matriz",
  "urgente": false,
  "cliente_estrategico": true
}
```

---

## Captura em Lote

Para processar varias demandas de uma vez:

```
Analise os textos abaixo e extraia as informacoes de cada demanda separadamente.
Retorne um array JSON com todas as demandas.

DEMANDA 1:
[texto]

DEMANDA 2:
[texto]

DEMANDA 3:
[texto]

---

Retorne:
[
  { demanda 1 em JSON },
  { demanda 2 em JSON },
  { demanda 3 em JSON }
]
```

---

## Campos Obrigatorios vs Opcionais

### Obrigatorios (IA deve perguntar se nao conseguir inferir)
- cliente
- local
- tipo_servico

### Opcionais (podem ser null)
- contato
- telefone
- email
- prazo
- numero_edital
- porte
- descricao

### Inferidos pela IA
- eh_licitacao (baseado em mencoes de edital, pregao, licitacao)
- origem (baseado no contexto)
- urgente (baseado em mencoes de urgencia, prazo curto)
- cliente_estrategico (geralmente false, a menos que explicito)

---

## Dicas para Captura Eficiente

1. **Emails:** Encaminhe para um email dedicado ou copie o texto
2. **Anotacoes:** Tire foto e use OCR ou transcreva manualmente
3. **Mensagens WhatsApp:** Copie o texto da conversa relevante
4. **Ligacoes:** Anote os pontos principais durante ou apos a ligacao

---

## Proximos Passos Apos Captura

1. IA gera o JSON estruturado
2. Usuario valida/ajusta se necessario
3. IA executa criacao no Asana via MCP
4. Tarefa criada na secao "Entrada"
5. Coordenador faz triagem normalmente

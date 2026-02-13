# Guia de Configuracao Manual do Projeto Asana

Este guia descreve como configurar manualmente o projeto "Teste MCP" no Asana.

**Project ID:** 1212920325558530
**URL:** https://app.asana.com/0/1212920325558530

---

## Opcao 1: Script Automatico (Recomendado)

### Requisitos
- Python 3.x instalado
- Token de acesso do Asana

### Passos

1. Instale a biblioteca requests:
```bash
pip install requests
```

2. Configure o token (opcional):
```bash
export ASANA_ACCESS_TOKEN="seu_token_aqui"
```

3. Execute o script:
```bash
python setup-asana-project.py
```

4. Se nao configurou o token, cole quando solicitado

---

## Opcao 2: Configuracao Manual via Interface

### 1. Criar Secoes (Colunas)

No projeto "Teste MCP", crie as seguintes secoes **nesta ordem**:

1. **Entrada** - Demandas novas aguardando triagem
2. **Em Triagem** - Avaliando viabilidade e prioridade
3. **Fila de Trabalho** - Aprovado para elaboracao, aguardando
4. **Em Elaboracao** - Orcamento sendo feito
5. **Revisao/Aprovacao** - Aguardando aprovacao interna
6. **Enviado** - Orcamento enviado ao cliente
7. **Em Negociacao** - Cliente pediu ajustes/desconto
8. **Fechado** - Orcamento aprovado/virou contrato
9. **Perdido** - Nao fechou

**Como criar:**
- Clique em "+ Adicionar secao" no topo de cada coluna
- Digite o nome da secao
- Repita para todas as 9 secoes

---

### 2. Criar Tags

No projeto, crie as seguintes tags:

**Tipo de Servico:**
- `instalacao` (cor: azul)
- `manutencao` (cor: verde)
- `projeto` (cor: roxo)

**Origem:**
- `licitacao` (cor: vermelho)

**Porte:**
- `pequeno` (cor: azul claro)
- `medio` (cor: amarelo)
- `grande` (cor: laranja)

**Prioridade:**
- `urgente` (cor: vermelho)
- `cliente-estrategico` (cor: rosa)

**Como criar:**
- Clique no nome do projeto > "Personalizar" > "Campos"
- Adicione um campo de tag
- Crie cada tag com seu nome e cor

---

### 3. Criar Tarefas de Exemplo

#### Exemplo 1: Instalacao

**Titulo:** `[INSTALACAO] Empresa ABC - Belo Horizonte`

**Secao:** Entrada

**Tags:** instalacao, medio

**Descricao:**
```
DADOS DO ORCAMENTO

Cliente: Empresa ABC
Contato: Joao Silva
Telefone: (31) 99999-8888
Email: joao@empresaabc.com.br
Local: Belo Horizonte - MG
Prazo do cliente: 2025-02-15

---

DETALHES DA DEMANDA
Instalacao de split 18.000 BTUs em sala de reunioes

---

ORIGEM: Comercial
LICITACAO: Nao

---

CLASSIFICACAO
Tipo: Instalacao
Porte: Medio
```

---

#### Exemplo 2: Licitacao de Projeto

**Titulo:** `[LIC][PROJETO] Prefeitura de Uberlandia - Uberlandia`

**Secao:** Entrada

**Tags:** projeto, licitacao, grande, urgente

**Descricao:**
```
DADOS DO ORCAMENTO

Cliente: Prefeitura de Uberlandia
Contato: Departamento de Compras
Local: Uberlandia - MG
Prazo do cliente: 2025-02-28

---

DETALHES DA DEMANDA
Projeto de climatizacao para edificio publico

---

ORIGEM: Licitacao
LICITACAO: Sim - Pregao 045/2025

---

CLASSIFICACAO
Tipo: Projeto
Porte: Grande
```

---

#### Exemplo 3: Manutencao

**Titulo:** `[MANUTENCAO] Condominio XYZ - Sao Paulo`

**Secao:** Entrada

**Tags:** manutencao, pequeno

**Descricao:**
```
DADOS DO ORCAMENTO

Cliente: Condominio XYZ
Contato: Sindico - Maria
Telefone: (11) 98888-7777
Email: sindico@condxyz.com.br
Local: Sao Paulo - SP
Prazo do cliente: 2025-02-10

---

DETALHES DA DEMANDA
Manutencao preventiva em 5 equipamentos split

---

ORIGEM: Cliente direto
LICITACAO: Nao

---

CLASSIFICACAO
Tipo: Manutencao
Porte: Pequeno
```

---

## Opcao 3: Via MCP Asana (Claude Desktop App)

Se voce estiver usando o Claude Desktop App com MCP configurado:

1. Abra o Claude Desktop App
2. Cole o conteudo do arquivo `asana-setup-config.json`
3. Peca ao Claude: "Configure meu projeto Asana usando esses dados via MCP"

---

## Verificacao

Apos configurar, verifique:

- [ ] 9 secoes criadas na ordem correta
- [ ] 9 tags criadas
- [ ] 3 tarefas de exemplo criadas
- [ ] Visualizacao Board funcionando
- [ ] Visualizacao Lista funcionando

---

## Proximos Passos

Apos configurar:

1. Testar o fluxo movendo tarefas entre secoes
2. Testar adicionar/remover tags
3. Criar uma demanda real
4. Configurar MCP para automacao

---

## Suporte

Para duvidas, consulte:
- `orcamentos-climatizacao-asana.md` - Documentacao completa
- `agente-ai-instrucoes-asana.md` - Instrucoes para automacao

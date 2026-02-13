# Projeto Asana: Orcamentos - Climatizacao

## Contexto

**Setor:** Orcamentos de Climatizacao
**Equipe:** Coordenador + 1 funcionario (em breve +2)
**Volume:** 10-30 demandas/semana
**Plano Asana:** Gratuito

---

## Estrutura do Projeto

### Nome do Projeto
**"Orcamentos - Climatizacao"**

### Secoes (9 etapas do fluxo)

| # | Secao | Descricao | Cor |
|---|-------|-----------|-----|
| 1 | Entrada | Demandas novas aguardando triagem | Cinza |
| 2 | Em Triagem | Avaliando viabilidade e prioridade | Amarelo |
| 3 | Fila de Trabalho | Aprovado para elaboracao, aguardando | Azul claro |
| 4 | Em Elaboracao | Orcamento sendo feito | Azul |
| 5 | Revisao/Aprovacao | Aguardando aprovacao interna | Roxo |
| 6 | Enviado | Orcamento enviado ao cliente | Verde claro |
| 7 | Em Negociacao | Cliente pediu ajustes/desconto | Laranja |
| 8 | Fechado | Orcamento aprovado/virou contrato | Verde |
| 9 | Perdido | Nao fechou | Vermelho |

---

## Padrao de Titulo das Tarefas

```
[TIPO] Cliente - Local          -> Para demandas diretas
[LIC][TIPO] Cliente - Local     -> Para licitacoes
```

**Tipos disponiveis:**
- `[INSTALACAO]` - Instalacao de AC
- `[MANUTENCAO]` - Manutencao preventiva/corretiva
- `[PROJETO]` - Projeto de climatizacao
- `[LIC]` - Prefixo adicional para licitacoes

**Exemplos:**
- `[INSTALACAO] Empresa ABC - BH`
- `[LIC][INSTALACAO] Prefeitura - MG`
- `[MANUTENCAO] Condominio XYZ - SP`
- `[LIC][PROJETO] Governo Estadual - RJ`

---

## Template de Descricao

```
DADOS DO ORCAMENTO

Cliente:
Contato:
Email:
Local:
Prazo do cliente:

---

DETALHES DA DEMANDA
[Descrever o que foi solicitado]

---

ORIGEM
[ ] Comercial/Vendas
[ ] Cliente direto
[ ] Diretoria
[ ] Engenharia

LICITACAO?
[ ] Sim - Numero/Edital: _______________
[ ] Nao

---

CLASSIFICACAO
Tipo: [Instalacao / Manutencao / Projeto]
Porte: [Pequeno / Medio / Grande]

---

HISTORICO/OBSERVACOES
[Anotacoes durante o processo]
```

---

## Tags

| Tag | Uso |
|-----|-----|
| `instalacao` | Tipo de servico |
| `manutencao` | Tipo de servico |
| `projeto` | Tipo de servico |
| `licitacao` | Origem via licitacao |
| `pequeno` | Porte |
| `medio` | Porte |
| `grande` | Porte |
| `urgente` | Prioridade alta |
| `cliente-estrategico` | Cliente importante |

---

## Criterios de Priorizacao

1. **Prazo de entrega** - Data limite do cliente
2. **Cliente estrategico** - Clientes importantes
3. **Ordem de chegada** - FIFO para demais casos

---

## Distribuicao de Trabalho

| Complexidade | Criterios | Responsavel |
|--------------|-----------|-------------|
| Simples | Porte pequeno, servico padrao | Novos funcionarios |
| Medio | Porte medio, especificidades | Funcionario atual |
| Complexo | Porte grande, licitacoes, prazos apertados | Coordenador |

---

## Fluxo de Trabalho

```
Entrada -> Triagem -> Fila -> Elaboracao -> Revisao -> Enviado
                                                          |
                                        Negociacao <------+
                                              |
                                  Fechado  ou  Perdido
```

---

## Guia de Uso - Equipe de Orcamentos

### Como Criar Nova Demanda

1. Abrir projeto "Orcamentos - Climatizacao"
2. Criar tarefa na secao "Entrada"
3. Titulo: `[TIPO] Cliente - Local`
4. Descricao: Preencher template
5. Tags: Adicionar tags relevantes
6. Prazo: Data limite do cliente
7. Salvar

### Responsabilidades por Secao

| Secao | Quem | O que fazer |
|-------|------|-------------|
| Entrada | Qualquer | Registrar nova demanda |
| Triagem | Coordenador | Avaliar viabilidade, prioridade |
| Fila | Coordenador | Atribuir responsavel |
| Elaboracao | Responsavel | Elaborar orcamento |
| Revisao | Coordenador | Revisar e aprovar |
| Enviado | Responsavel | Confirmar envio |
| Negociacao | Responsavel | Acompanhar |
| Fechado | Coordenador | Registrar fechamento |
| Perdido | Coordenador | Registrar perda |

---

## Guia de Uso - Outros Setores

### Como Solicitar Orcamento

1. Acessar projeto "Orcamentos - Climatizacao"
2. Criar tarefa em "Entrada"
3. Titulo: `[TIPO] Cliente - Local`
4. Preencher template da descricao
5. Definir prazo
6. Equipe de orcamentos processara

---

## Fase 2 - Melhorias Futuras

### Metricas
- Taxa de conversao: Fechados / (Fechados + Perdidos)
- Tempo medio: Data entrada ate envio
- Volume por periodo: Contagem por semana/mes

### Motivos de Perda
- Preco
- Prazo
- Concorrencia
- Desistencia
- Escopo
- Outro

### Formulario Asana
- Criar formulario de entrada para outros setores

---

## Fase 3 - MCP Asana

- Criar tarefas via IA
- Mover tarefas automaticamente
- Consultar status e metricas
- Gerar relatorios

---

## Limitacoes Plano Gratuito

- Campos personalizados: Limitado (usar tags e descricao)
- Timeline: Nao disponivel
- Automacoes: Nao disponivel
- Relatorios avancados: Nao disponivel
- Usuarios: Ate 10 (ok para o cenario atual)

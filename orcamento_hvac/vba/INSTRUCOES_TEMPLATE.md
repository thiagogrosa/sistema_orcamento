# Instruções para Criar o Template Excel com VBA

## Passo 1: Criar o Arquivo Template

1. Abra o Excel
2. Crie um novo arquivo em branco
3. Salve como **`template.xlsm`** (Pasta de Trabalho Habilitada para Macro)
   - Arquivo > Salvar Como > Tipo: "Pasta de Trabalho Habilitada para Macro do Excel (*.xlsm)"
   - Salve na pasta do projeto: `/Users/thiagorosa/dev/tools/armant/planilha/`

## Passo 2: Criar as Abas

Renomeie e crie as seguintes abas (na ordem):

| # | Nome da Aba | Cor Sugerida |
|---|-------------|--------------|
| 1 | INSTRUCOES | Cinza |
| 2 | PROMPTS | Cinza |
| 3 | NEGOCIO | Verde |
| 4 | MATERIAIS | Azul |
| 5 | MAO_DE_OBRA | Verde claro |
| 6 | FERRAMENTAS | Amarelo |
| 7 | EQUIPAMENTOS | Azul claro |
| 8 | COMPOSICOES | Azul escuro |
| 9 | CLIENTE | Verde escuro |
| 10 | ESCOPO | Laranja |

## Passo 3: Adicionar Headers (Linha 1)

### MATERIAIS (Aba 4)
| Col | Header | Largura |
|-----|--------|---------|
| A | Código | 18 |
| B | Categoria | 15 |
| C | Descrição | 50 |
| D | Unidade | 10 |
| E | Preço (R$) | 14 |
| F | Atualizado Em | 14 |
| G | Validade (dias) | 14 |
| H | Seleção | 65 (OCULTA) |

### MAO_DE_OBRA (Aba 5)
| Col | Header | Largura |
|-----|--------|---------|
| A | Código | 15 |
| B | Categoria | 18 |
| C | Descrição | 45 |
| D | Unidade | 10 |
| E | Custo (R$) | 14 |
| F | Atualizado Em | 14 |
| G | Validade (dias) | 14 |
| H | Seleção | 55 (OCULTA) |

### FERRAMENTAS (Aba 6)
| Col | Header | Largura |
|-----|--------|---------|
| A | Código | 18 |
| B | Categoria | 18 |
| C | Descrição | 40 |
| D | Valor Aquisição | 16 |
| E | Vida Útil (H) | 14 |
| F | Custo/Hora | 12 |
| G | Atualizado Em | 14 |
| H | Validade (dias) | 14 |
| I | Seleção | 55 (OCULTA) |

### EQUIPAMENTOS (Aba 7)
| Col | Header | Largura |
|-----|--------|---------|
| A | Código | 18 |
| B | Categoria | 18 |
| C | Descrição | 45 |
| D | Capacidade | 12 |
| E | Unidade | 10 |
| F | Preço (R$) | 14 |
| G | Atualizado Em | 14 |
| H | Validade (dias) | 14 |
| I | Seleção | 60 (OCULTA) |

### COMPOSICOES (Aba 8)
| Col | Header | Largura |
|-----|--------|---------|
| A | Código | 18 |
| B | Descrição | 55 |
| C | Tipo | 8 |
| D | Cód. Item | 18 |
| E | Un | 8 |
| F | Qtd Base | 12 |
| G | Qtd Var | 12 |
| H | Preço Unit. | 14 |
| I | Sub. Base | 12 |
| J | Sub. Var | 12 |
| K | Mult. | 10 |
| L | Base c/ Margem | 14 |
| M | Var c/ Margem | 14 |
| N | Seleção | 65 (OCULTA) |
| O | Desc. Pré | 45 |
| P | Desc. Pós | 35 |
| Q | Unid. Sing | 12 (OCULTA) |
| R | Unid. Plur | 12 (OCULTA) |

## Passo 4: Formatar Headers

Para cada aba de dados:
1. Selecione a linha 1 (headers)
2. Aplique:
   - Cor de fundo: Azul (#2E86AB ou RGB 46, 134, 171)
   - Cor da fonte: Branco
   - Negrito
   - Centralizado
   - Bordas finas
3. Congele painéis: Exibir > Congelar Painéis > Congelar Linha Superior

## Passo 5: Ocultar Colunas de Seleção

- MATERIAIS: Ocultar coluna H
- MAO_DE_OBRA: Ocultar coluna H
- FERRAMENTAS: Ocultar coluna I
- EQUIPAMENTOS: Ocultar coluna I
- COMPOSICOES: Ocultar colunas N, Q, R

## Passo 6: Criar Intervalos Nomeados

1. Vá em Fórmulas > Gerenciador de Nomes > Novo
2. Crie os seguintes nomes (apontando para placeholder):

| Nome | Refere-se a |
|------|-------------|
| LISTA_MAT | =MATERIAIS!$H$2:$H$2 |
| LISTA_MO | =MAO_DE_OBRA!$H$2:$H$2 |
| LISTA_FER | =FERRAMENTAS!$I$2:$I$2 |
| LISTA_EQP | =EQUIPAMENTOS!$I$2:$I$2 |
| LISTA_COMP | =COMPOSICOES!$N$2:$N$2 |

(O Python vai atualizar esses intervalos após preencher os dados)

## Passo 7: Adicionar Código VBA

### 7.1 Abrir o Editor VBA
- Pressione `Alt + F11`

### 7.2 Importar os Módulos
1. No menu: Arquivo > Importar Arquivo...
2. Selecione o arquivo `modMacros.bas` desta pasta
3. Clique em Abrir
4. Repita para importar `modImportCSV.bas` (módulo de importação de CSVs)

### 7.3 Criar o UserForm
Como o UserForm precisa ser criado manualmente:

1. No VBAProject, clique com botão direito em "Forms"
2. Selecione "Inserir" > "UserForm"
3. Renomeie para **frmNovaComposicao** (na janela Propriedades, campo Name)
4. Configure as propriedades do form:
   - Caption: Nova Composição
   - Width: 400
   - Height: 340

5. Adicione os controles (da Caixa de Ferramentas):

**Labels:**
| Nome | Caption | Left | Top | Width |
|------|---------|------|-----|-------|
| lblCodigo | Código: | 12 | 18 | 70 |
| lblDescricao | Descrição: | 12 | 48 | 70 |
| lblDescPre | Desc. Pré: | 12 | 78 | 70 |
| lblDescPos | Desc. Pós: | 12 | 108 | 70 |
| lblUnidSing | Unid. Sing: | 12 | 138 | 70 |
| lblUnidPlur | Unid. Plur: | 155 | 138 | 70 |
| lblCopiarDe | Copiar de: | 12 | 168 | 70 |

**TextBoxes:**
| Nome | Left | Top | Width | Height | Descrição |
|------|------|-----|-------|--------|-----------|
| txtCodigo | 90 | 15 | 280 | 20 | Código da composição |
| txtDescricao | 90 | 45 | 280 | 20 | Descrição |
| txtDescPre | 90 | 75 | 280 | 20 | Texto antes da variável |
| txtDescPos | 90 | 105 | 280 | 20 | Texto após a variável |
| txtUnidSing | 90 | 135 | 130 | 20 | Unidade singular (ex: "metro") |
| txtUnidPlur | 240 | 135 | 130 | 20 | Unidade plural (ex: "metros") |
| txtBusca | 90 | 165 | 280 | 20 | Campo de busca (filtra lista) |

**ListBox:**
| Nome | Left | Top | Width | Height | Descrição |
|------|------|-----|-------|--------|-----------|
| lstComposicoes | 90 | 190 | 280 | 80 | Lista de composições para copiar |

> **Nota**: A busca filtra em tempo real enquanto digita. Funciona em qualquer parte do texto (ex: digitar "split" encontra "Instalação Split 12K").

**CommandButtons:**
| Nome | Caption | Left | Top | Width | Height |
|------|---------|------|-----|-------|--------|
| btnCriar | Criar | 90 | 280 | 100 | 28 |
| btnCancelar | Cancelar | 200 | 280 | 100 | 28 |

6. Copie o código do arquivo `frmNovaComposicao.frm` para o code-behind do form:
   - Dê duplo-clique no form
   - Cole o código (apenas a parte após `Option Explicit`)

## Passo 8: Adicionar Botões nas Abas (Opcional)

Para facilitar o uso, adicione botões de formulário:

### Na aba COMPOSICOES:
1. Desenvolvedor > Inserir > Controles de Formulário > Botão
2. Desenhe o botão no canto superior direito
3. Quando aparecer a janela "Atribuir Macro", selecione:
   - Para botão "Nova Composição": `NovaComposicao`
   - Para botão "Atualizar Totais": `AtualizarTotaisComposicao`
   - Para botão "Atualizar Seleção": `AtualizarSelecao`

### Nas abas de catálogo:
- Adicione um botão "Atualizar Seleção" vinculado à macro `AtualizarSelecao`

## Passo 9: Testar

1. Salve o arquivo (`Ctrl + S`)
2. Feche e reabra o arquivo
3. Habilite macros se solicitado
4. Teste:
   - Vá para aba MATERIAIS e rode `AtualizarSelecao` (via botão ou Alt+F8)
   - Vá para aba COMPOSICOES e rode `NovaComposicao`

## Passo 10: Salvar Template Final

1. Delete qualquer dado de teste
2. Mantenha apenas headers na linha 1
3. Salve como `template.xlsm` na pasta do projeto

---

## Estrutura Final do Projeto VBA

```
VBAProject (template.xlsm)
├── Microsoft Excel Objects
│   ├── ThisWorkbook
│   ├── Planilha1 (INSTRUCOES)
│   ├── Planilha2 (PROMPTS)
│   ├── Planilha3 (NEGOCIO)
│   ├── Planilha4 (MATERIAIS)
│   ├── Planilha5 (MAO_DE_OBRA)
│   ├── Planilha6 (FERRAMENTAS)
│   ├── Planilha7 (EQUIPAMENTOS)
│   ├── Planilha8 (COMPOSICOES)
│   ├── Planilha9 (CLIENTE)
│   └── Planilha10 (ESCOPO)
├── Formulários
│   └── frmNovaComposicao
└── Módulos
    ├── modMacros
    └── modImportCSV
```

## Macros de Importação CSV

O módulo `modImportCSV` permite atualizar os catálogos a partir de arquivos CSV externos.
A validade é controlada **por item**, não por catálogo.

### Arquivos CSV Esperados

Os arquivos CSV devem seguir o padrão: `{catalogo}_{YYYY-MM-DD}.csv`

Exemplo:
- `materiais_2025-12-30.csv`
- `mao_de_obra_2025-12-30.csv`

O sistema importa automaticamente o arquivo mais recente de cada tipo.

### Colunas de Validade

Cada item nos CSVs possui:
- **ATUALIZADO_EM**: Data da última atualização (formato YYYY-MM-DD)
- **VALIDADE_DIAS**: Número de dias de validade

Após importação, itens são destacados:
- **Vermelho claro**: Item vencido
- **Amarelo claro**: Item expirando (≤3 dias)
- **Sem cor**: Item OK

### Macros Disponíveis

| Macro | Descrição |
|-------|-----------|
| `ImportarTodosCatalogos` | Importa todos os 4 catálogos de uma vez |
| `VerificarValidade` | Verifica se algum item está vencido (por item) |
| `AbrirPastaCSV` | Abre a pasta de CSVs no Windows Explorer |

### Configuração

A aba NEGOCIO (linha 56+) contém a configuração de importação:
- **A57**: Caminho para a pasta com os arquivos CSV (padrão: `.\dados_csv\`)
- **B58**: Timestamp da última importação
- **B59**: Status (OK, Atenção ou VENCIDO com contagem de itens)

### Botões Recomendados na Aba NEGOCIO

1. **Importar Catálogos** → Macro: `ImportarTodosCatalogos`
2. **Verificar Validade** → Macro: `VerificarValidade`
3. **Abrir Pasta CSV** → Macro: `AbrirPastaCSV`

## Atalhos de Teclado (Opcional)

Para atribuir atalhos às macros:
1. Desenvolvedor > Macros
2. Selecione a macro
3. Clique em "Opções..."
4. Atribua um atalho (ex: Ctrl+Shift+S para AtualizarSelecao)

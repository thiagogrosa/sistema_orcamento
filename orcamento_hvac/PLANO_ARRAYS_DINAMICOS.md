# Plano: Implementar Fórmulas de Arrays Dinâmicos

**STATUS: IMPLEMENTADO** (Dez/2025)

## Objetivo
Substituir fórmulas repetitivas (uma por linha) por fórmulas de spill únicas que "derramam" automaticamente, reduzindo manutenção e evitando erros de usuário.

## Funções Confirmadas (Excel 365 PT-BR)
- `LET` / `LAMBDA` / `MAP` (nomes em inglês)
- `PROCX` (XLOOKUP)
- `EMPILHARV` (VSTACK)
- Separador: `;`
- Operador `#` para referência de spill

## Limitação Crítica
**O openpyxl não gera arquivos válidos com essas fórmulas** - o Excel remove as fórmulas ao abrir.

**Solução**: Fórmulas criadas manualmente no `template.xlsm`, script Python só preenche dados.

---

## Problema: Totais das Composições

### Estrutura da aba COMPOSICOES:
```
Linha 2:  [COMP_001 | Descrição | (vazio) | ... | TOTAL J | TOTAL K | ... | TOTAL M | TOTAL N]  ← CABEÇALHO
Linha 3:  [(vazio)  | (vazio)   | MAT     | ... | valor   | valor   | ... | valor   | valor  ]  ← ITEM
Linha 4:  [(vazio)  | (vazio)   | MO      | ... | valor   | valor   | ... | valor   | valor  ]  ← ITEM
...
Linha 10: [COMP_002 | Descrição | (vazio) | ... | TOTAL J | TOTAL K | ... | TOTAL M | TOTAL N]  ← CABEÇALHO
```

### Problema com Spill:
- Fórmulas de spill preenchem TODAS as linhas (incluindo cabeçalhos)
- Linhas de cabeçalho precisam de SOMA, não de cálculo individual
- Spill "ocupa" a célula, impedindo outra fórmula

### Solução Implementada: Fórmulas Inteligentes

**NOTA**: A solução original propunha colunas auxiliares R, S, T. Na implementação final,
optou-se por fórmulas que detectam headers diretamente nas colunas J, K, M, N:

- Cada fórmula verifica se a linha é cabeçalho (coluna A preenchida)
- **Headers**: Calcula SOMA dos itens até o próximo header usando MÍNIMO(FILTRO(...))
- **Itens**: Calcula valor individual (Qtd × Preço)

**Vantagem**: Não precisa de colunas auxiliares - totais calculados diretamente em J, K, M, N

### Coluna Auxiliar: Composição Pai

Para calcular SUMIFS, cada linha de item precisa saber a qual composição pertence.

**Nova Coluna R: Código da Composição Pai** (fórmula spill em R2)
```excel
=LET(
  codigos;A2:A500;
  MAP(codigos;LAMBDA(c;
    SE(c<>"";c;
      PROCX(VERDADEIRO;INDICE(A$1:A1<>"";0;0);A$1:A1;"";-1)
    )
  ))
)
```

Explicação: Para cada linha, se A tem código (é cabeçalho), usa esse código. Senão, busca o último código não-vazio acima.

**Alternativa mais simples** (se a fórmula acima não funcionar):
Usar coluna R preenchida pelo Python com o código da composição pai para cada item.

### Colunas de Totais Dinâmicos (nas linhas de CABEÇALHO)

**Coluna S: Total Base c/ Margem** (fórmula spill em S2)
```excel
=LET(
  codigos;A2:A500;
  col_pai;R2#;
  valores;M2#;
  MAP(codigos;LAMBDA(cod;
    SE(cod="";"";SOMASES(valores;col_pai;cod))
  ))
)
```

**Coluna T: Total Var c/ Margem** (fórmula spill em T2)
```excel
=LET(
  codigos;A2:A500;
  col_pai;R2#;
  valores;N2#;
  MAP(codigos;LAMBDA(cod;
    SE(cod="";"";SOMASES(valores;col_pai;cod))
  ))
)
```

### Atualização do ESCOPO

O ESCOPO agora busca totais nas colunas S e T (em vez de M e N nas linhas de cabeçalho):
```excel
base;INDICE(COMPOSICOES!$S:$S;lin);
var;INDICE(COMPOSICOES!$T:$T;lin);
```

---

## Arquivos a Modificar

| Arquivo | Mudança |
|---------|---------|
| `template.xlsm` | Adicionar fórmulas de spill (manual) |
| `abas/composicoes.py` | Remover geração de fórmulas nas colunas E, F, I, L |
| `abas/escopo.py` | Remover geração de fórmulas nas colunas D, G |
| `vba/modMacros.bas` | Atualizar `FormatarLinhaItem` para não inserir fórmulas de spill |
| `CLAUDE.md` | Documentar nova arquitetura |

---

## Fase 1: Template - Fórmulas de Spill

### 1.1 COMPOSICOES!L2 - Multiplicador (PRIORIDADE ALTA)

```excel
=LET(
  tipos;C2:C500;
  tab_tipo;NEGOCIO!$A$42:$A$45;
  tab_mult;NEGOCIO!$B$42:$B$45;
  MAP(tipos;LAMBDA(t;SE(t="";"";PROCX(t;tab_tipo;tab_mult;1))))
)
```

**Resultado**: Uma fórmula em L2 que preenche automaticamente L2:L500 baseado no tipo em C.

### 1.2 COMPOSICOES!I2 - Preço Unitário

```excel
=LET(
  tipos;C2:C500;
  codigos;D2:D500;
  MAP(tipos;codigos;LAMBDA(t;c;
    SE(OU(t="";c="");"";
      LET(
        cod;SEERRO(ESQUERDA(c;PROCURAR(" - ";c)-1);c);
        idx;CORRESP(t;{"MAT";"MO";"FER";"EQP"};0);
        SEERRO(ESCOLHER(idx;
          PROCX(cod;MATERIAIS!$A:$A;MATERIAIS!$E:$E);
          PROCX(cod;MAO_DE_OBRA!$A:$A;MAO_DE_OBRA!$E:$E);
          PROCX(cod;FERRAMENTAS!$A:$A;FERRAMENTAS!$F:$F);
          PROCX(cod;EQUIPAMENTOS!$A:$A;EQUIPAMENTOS!$F:$F));"")
      )
    )
  ))
)
```

### 1.3 COMPOSICOES!E2 - Descrição Item

Similar a I2, mas busca coluna C (descrição) de cada tabela.

### 1.4 COMPOSICOES!F2 - Unidade

Similar, mas FER retorna "H" fixo.

### 1.5 COMPOSICOES!J2 - Subtotal Base
```excel
=LET(qtd;G2:G500;preco;I2#;MAP(qtd;preco;LAMBDA(q;p;SE(OU(q="";p="");"";q*p))))
```

### 1.6 COMPOSICOES!K2 - Subtotal Variável
```excel
=LET(qtd;H2:H500;preco;I2#;MAP(qtd;preco;LAMBDA(q;p;SE(OU(q="";p="");"";q*p))))
```

### 1.7 COMPOSICOES!M2 - Base com Margem
```excel
=LET(base;J2#;mult;L2#;MAP(base;mult;LAMBDA(b;m;SE(OU(b="";m="");"";b*m))))
```

### 1.8 COMPOSICOES!N2 - Variável com Margem
```excel
=LET(var;K2#;mult;L2#;MAP(var;mult;LAMBDA(v;m;SE(OU(v="";m="");"";v*m))))
```

---

## Fase 2: Template - Aba ESCOPO

### 2.1 ESCOPO!G10 - Preço (linha 10 é início da tabela)

**ATUALIZADO**: Busca totais nas colunas S e T (totais dinâmicos)

```excel
=LET(
  tipos;B10:B39;
  codigos;C10:C39;
  vars;F10:F39;
  tab_tipo;NEGOCIO!$A$42:$A$45;
  tab_mult;NEGOCIO!$B$42:$B$45;
  MAP(tipos;codigos;vars;LAMBDA(tp;cd;vr;
    SE(OU(tp="";cd="");"";
      SE(tp="COMP";
        LET(
          cod;SEERRO(ESQUERDA(cd;PROCURAR(" - ";cd)-1);cd);
          lin;CORRESP(cod;COMPOSICOES!$A:$A;0);
          base;INDICE(COMPOSICOES!$S:$S;lin);
          var;INDICE(COMPOSICOES!$T:$T;lin);
          base+var*SE(vr="";0;vr));
        LET(
          cod;SEERRO(ESQUERDA(cd;PROCURAR(" - ";cd)-1);cd);
          mult;PROCX(tp;tab_tipo;tab_mult;1);
          idx;CORRESP(tp;{"MAT";"MO";"FER";"EQP"};0);
          preco;ESCOLHER(idx;
            PROCX(cod;MATERIAIS!$A:$A;MATERIAIS!$E:$E;"");
            PROCX(cod;MAO_DE_OBRA!$A:$A;MAO_DE_OBRA!$E:$E;"");
            PROCX(cod;FERRAMENTAS!$A:$A;FERRAMENTAS!$F:$F;"");
            PROCX(cod;EQUIPAMENTOS!$A:$A;EQUIPAMENTOS!$F:$F;""));
          preco*mult)
      )
    )
  ))
)
```

**Mudança chave**: `$M:$M` → `$S:$S` e `$N:$N` → `$T:$T`

### 2.2 ESCOPO!D10 - Descrição

Similar, buscando descrições e montando texto dinâmico para COMP.

---

## Fase 3: Script Python

### 3.1 `abas/composicoes.py`

**Remover geração de fórmulas** nas linhas:
- 171-175: `formula_desc` (coluna E)
- 178-181: `formula_un` (coluna F)
- 198-201: `formula_preco` (coluna I)
- 204-207: `formula_subtotal_base` (coluna J)
- 210-213: `formula_subtotal_var` (coluna K)
- 216-219: `formula_mult` (coluna L)
- 223-226: `formula_base_margem` (coluna M)
- 229-232: `formula_var_margem` (coluna N)

**Manter apenas preenchimento de dados**:
- Coluna A/B: Código e Descrição (cabeçalhos)
- Coluna C: Tipo (itens)
- Coluna D: Código do item (itens)
- Coluna G: Qtd Base (itens)
- Coluna H: Qtd Var (itens)
- Coluna P/Q: Desc Pre/Pos (cabeçalhos)

### 3.2 `abas/escopo.py`

**Remover geração de fórmulas** nas linhas:
- 151-155: `formula_desc` (coluna D)
- 172-175: `formula_preco` (coluna G)

---

## Fase 4: VBA

### 4.1 `vba/modMacros.bas` - Função `FormatarLinhaItem`

Atualizar para **NÃO inserir fórmulas** nas colunas E, F, I, L (já são spill).

### 4.2 Nova função `RecalcularSpill()`

```vba
Sub RecalcularSpill()
    Application.CalculateFull
End Sub
```

---

## Resultado Esperado

| Antes | Depois |
|-------|--------|
| ~8.000 fórmulas geradas (8 colunas × 500 linhas × 2 funções) | 13 fórmulas de spill total |
| Cada linha editável pelo usuário | Áreas de spill protegidas contra edição |
| Mudança de lógica = editar código Python | Mudança de lógica = editar 1 célula no template |
| Totais calculados por SUM fixo | Totais calculados dinamicamente por SUMIFS |
| Funciona em qualquer Excel | Requer Excel 365/2021 |

**Fórmulas de spill criadas**:
- COMPOSICOES: E2, F2, I2, J2, K2, L2, M2, N2 (8 fórmulas de valores)
- COMPOSICOES: R2, S2, T2 (3 fórmulas de totais dinâmicos)
- ESCOPO: D10, G10 (2 fórmulas)

**Nova estrutura de colunas COMPOSICOES**:
| Col | Conteúdo | Tipo |
|-----|----------|------|
| A-B | Código/Descrição | Dados (Python) |
| C-D | Tipo/Cód.Item | Dados (Python) |
| E-F | Desc.Item/Unidade | Spill (lookup) |
| G-H | Qtd Base/Var | Dados (Python) |
| I | Preço Unit. | Spill (lookup) |
| J-K | Sub.Base/Var | Spill (cálculo) |
| L | Multiplicador | Spill (lookup) |
| M-N | Base/Var c/ Margem | Spill (cálculo) |
| O | Seleção | Dados (Python) |
| P-Q | Desc.Pre/Pos | Dados (Python) |
| R | Comp.Pai | Spill (auxiliar) |
| S-T | Totais c/ Margem | Spill (SUMIFS) |

---

## Sequência de Implementação

### Fase 1: Template - Fórmulas de Valores (manual no Excel)
1. [ ] Abrir `template.xlsm` no Excel
2. [ ] COMPOSICOES!L2 - Fórmula de Multiplicador
3. [ ] COMPOSICOES!I2 - Fórmula de Preço Unitário
4. [ ] COMPOSICOES!E2 - Fórmula de Descrição Item
5. [ ] COMPOSICOES!F2 - Fórmula de Unidade
6. [ ] COMPOSICOES!J2 - Fórmula de Subtotal Base
7. [ ] COMPOSICOES!K2 - Fórmula de Subtotal Variável
8. [ ] COMPOSICOES!M2 - Fórmula de Base c/ Margem
9. [ ] COMPOSICOES!N2 - Fórmula de Var c/ Margem
10. [ ] Testar: valores de itens calculando corretamente

### Fase 2: Template - Fórmulas de Totais Dinâmicos
11. [ ] COMPOSICOES!R2 - Fórmula de Composição Pai (auxiliar)
12. [ ] COMPOSICOES!S2 - Fórmula de Total Base c/ Margem (SUMIFS)
13. [ ] COMPOSICOES!T2 - Fórmula de Total Var c/ Margem (SUMIFS)
14. [ ] Testar: totais das composições calculando corretamente
15. [ ] Ocultar coluna R (auxiliar)

### Fase 3: Template - Aba ESCOPO
16. [ ] ESCOPO!G10 - Fórmula de Preço (usando S e T)
17. [ ] ESCOPO!D10 - Fórmula de Descrição
18. [ ] Testar: ESCOPO buscando totais corretos
19. [ ] Salvar template.xlsm

### Fase 4: Script Python
20. [ ] Modificar `abas/composicoes.py` - remover fórmulas (E, F, I, J, K, L, M, N)
21. [ ] Adicionar coluna R nos headers (ou deixar vazio para spill)
22. [ ] Modificar `abas/escopo.py` - remover fórmulas (D, G)
23. [ ] Testar geração: `python3 criar_planilha.py`

### Fase 5: VBA e Documentação
24. [ ] Atualizar `vba/modMacros.bas` - FormatarLinhaItem
25. [ ] Atualizar `CLAUDE.md` com nova arquitetura de colunas
26. [ ] Testar fluxo completo: Python → Excel → Totais corretos

---

## Decisão Pendente

**Coluna R (Composição Pai)**: Escolher abordagem:
- [ ] Fórmula dinâmica (PROCX) - mais complexo mas 100% dinâmico
- [ ] Python preenche - mais simples e confiável

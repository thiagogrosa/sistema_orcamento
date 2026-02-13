# Teste Manual de Arrays Dinâmicos no Excel 365

O openpyxl não consegue gerar arquivos válidos com fórmulas modernas.
Use o arquivo `Teste_Manual.xlsx` para testar as fórmulas digitando-as manualmente.

---

## Funções Modernas (mantêm nome em inglês)

| Função | Nome no Excel PT-BR |
|--------|---------------------|
| LET | LET |
| LAMBDA | LAMBDA |
| MAP | MAP |
| XLOOKUP | PROCX |
| VSTACK | ? (testar) |
| HSTACK | ? (testar) |
| CHOOSE | ESCOLHER |
| MATCH | CORRESP |
| IF | SE |
| OR | OU |
| SUM | SOMA |

**Separador de argumentos no PT-BR:** `;` (ponto-e-vírgula)

---

## Instruções

1. Abra `Teste_Manual.xlsx`
2. Vá para cada aba de teste
3. Digite a fórmula indicada na célula amarela
4. Anote se funcionou ou deu erro

---

## Teste 1: LET

**Aba:** TESTE_LET
**Célula:** B2 (amarela)
**Digite:**
```
=LET(x;10;x*2)
```
**Esperado:** 20

---

## Teste 2: LAMBDA

**Aba:** TESTE_LAMBDA
**Célula:** B2
**Digite:**
```
=LAMBDA(x;x*2)(5)
```
**Esperado:** 10

---

## Teste 3: PROCX

**Aba:** TESTE_PROCX
**Célula:** D2
**Digite:**
```
=PROCX("MO";A2:A5;B2:B5)
```
**Esperado:** 1,50

---

## Teste 4: MAP com LAMBDA

**Aba:** TESTE_MAP
**Célula:** B2
**Digite:**
```
=MAP(A2:A5;LAMBDA(x;x*10))
```
**Esperado:** 10, 20, 30, 40 (spill automático em B2:B5)

---

## Teste 5: LET + MAP + PROCX (caso real)

**Aba:** TESTE_COMPLETO
**Célula:** C2
**Digite:**
```
=LET(tipos;A2:A7;tab_tipo;TESTE_PROCX!A2:A5;tab_mult;TESTE_PROCX!B2:B5;MAP(tipos;LAMBDA(t;SE(t="";"";PROCX(t;tab_tipo;tab_mult;1)))))
```
**Esperado:** Multiplicadores correspondentes com spill

---

## Teste 6: VSTACK

**Aba:** TESTE_VSTACK
**Célula:** C2
**Digite (testar ambos nomes):**
```
=VSTACK(A2:A4;B2:B4)
```
Se não funcionar, tente:
```
=EMPILHARV(A2:A4;B2:B4)
```
**Esperado:** 1,2,3,10,20,30 (vertical)

---

## Teste 7: Operador # (Spill Reference)

**Aba:** TESTE_MAP (após teste 4 funcionar)
**Célula:** D2
**Digite:**
```
=SOMA(B2#)
```
**Esperado:** 100 (soma de 10+20+30+40)

---

## Resultados

Após testar, preencha:

| Teste | Função | Funciona? | Nome correto |
|-------|--------|-----------|--------------|
| 1 | LET | | |
| 2 | LAMBDA | | |
| 3 | PROCX | | |
| 4 | MAP | | |
| 5 | LET+MAP+PROCX | | |
| 6 | VSTACK | | |
| 7 | Operador # | | |

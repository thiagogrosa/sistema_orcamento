# Diff resumido - Sprint 1 de composições

Branch: `feature/sprint1-expansao-composicoes`
Commit: `99e5fad`

## Arquivos alterados
- `dados/composicoes.py`
- `validar_composicoes.py` (novo)
- `relatorio-validacao-composicoes.md` (novo)
- `composicoes-atuais.md`
- `composicoes-atuais-agrupadas.md`

## Novas composições adicionadas

- `COMP_INST_HW_36K` — Instalação Split Hi-Wall 36.000 BTUs
- `COMP_INST_HW_48K` — Instalação Split Hi-Wall 48.000 BTUs
- `COMP_INST_HW_60K` — Instalação Split Hi-Wall 60.000 BTUs
- `COMP_ELE_9_12K` — Alimentação elétrica 220V monofásica 9-12K
- `COMP_ELE_18_24K` — Alimentação elétrica 220V monofásica 18-24K
- `COMP_ELE_30_36K` — Alimentação elétrica 220V monofásica 30-36K
- `COMP_ELE_48_60K` — Alimentação elétrica 220V monofásica 48-60K

## Validação automática criada
- Script: `validar_composicoes.py`
- Regras: código órfão, quantidades negativas, composição sem itens
- Resultado atual: **72 composições | 0 erros | 0 avisos**

## Como revisar rapidamente
```bash
git checkout feature/sprint1-expansao-composicoes
git show --stat
python3 validar_composicoes.py
```

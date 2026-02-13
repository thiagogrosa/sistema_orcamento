# Planilha de Custos HVAC

Projeto Python para geração de planilha Excel (`.xlsm`) de custos HVAC, validação de composições e apoio a coleta de dados.

## Status atual (12/02/2026)
- Branch ativa principal de evolução: `feature/validacao-avancada-composicoes`
- Validador avançado operacional com relatório `.md` + `.json`
- Cobertura mínima das composições tratada (warnings de cobertura mínima: **0**)
- Testes do validador: passando (incluindo regressão de cobertura)

## Requisitos
- Python 3.11+ (recomendado: 3.12+)
- Excel (para uso de `template.xlsm` e macros VBA)

## Setup rápido
```bash
cd /data/.openclaw/workspace/planilha
./setup.sh
source .venv/bin/activate
```

Se quiser forçar outro diretório de ambiente virtual:
```bash
VENV_DIR=.venv312 ./setup.sh
```

## Dados de entrada (fontes do projeto)
- Catálogos e composições:
  - `dados/composicoes.py`
  - `dados/materiais.py`
  - `dados/mao_de_obra.py`
  - `dados/ferramentas.py`
  - `dados/equipamentos.py`
- CSVs auxiliares:
  - `dados_csv/*.csv`
- Template Excel:
  - `template.xlsm`

## Comandos principais
```bash
# Validar composições (gera relatório md + json)
python validar_composicoes.py

# Gerar planilha
python criar_planilha.py

# Ver ajuda do CLI de scraping
python scraper_cli.py --help

# Rodar testes
pytest -q
```

## Exemplos práticos
### 1) Validar base e revisar relatório
```bash
python validar_composicoes.py
# Saídas esperadas:
# - relatorio-validacao-composicoes.md
# - relatorio-validacao-composicoes.json
```

### 2) Gerar planilha final
```bash
python criar_planilha.py
# Saída esperada: arquivo .xlsm gerado a partir do template
```

### 3) Rodar somente testes do validador
```bash
pytest -q tests/test_validar_composicoes.py
```

## Dependências
Este projeto usa um único arquivo de dependências: `requirements.txt`.

Contém:
- pacotes de runtime
- pacotes de teste (ex.: `pytest`)

## Estrutura do projeto
```text
abas/        # Geração/preenchimento das abas da planilha
dados/       # Catálogos e composições base
dados_csv/   # Dados auxiliares em CSV
scraping/    # Sistema modular de scraping
tests/       # Testes automatizados
vba/         # Módulos VBA e instruções do template
notes/       # Análises, planos e artefatos de execução
```

## Known issues / observações
- Dependências de API externa (Asana/Google/etc.) não são necessárias para validação local, mas bloqueiam rollout completo da automação.
- A qualidade de descrição ainda pode gerar ruído em regras de similaridade (`DESCRIPTION_HIGH_SIMILARITY`) e requer refinamento por família.
- Evitar armazenar chaves/tokens em arquivos do repositório; usar apenas variáveis de ambiente.

## Fluxo recomendado de trabalho
1. `./setup.sh`
2. `pytest -q`
3. `python validar_composicoes.py`
4. `python criar_planilha.py`
5. Commitar resultados relevantes (código + artefatos necessários)

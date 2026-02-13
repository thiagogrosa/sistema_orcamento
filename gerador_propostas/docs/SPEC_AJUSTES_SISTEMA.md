# Spec: Ajustes do Sistema de Orcamentacao HVAC

**Data:** 2026-01-04
**Status:** Aprovado para implementacao

---

## 1. Contexto

O sistema atual de skills HVAC foi criado com algumas divergencias em relacao ao GUIA_ESTRUTURA_DADOS.md. Este documento define os ajustes necessarios para alinhar ambos.

---

## 2. Decisoes Arquiteturais

### 2.1 Arquitetura Hibrida

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE (Claude/Opus)                     │
│  - Interpreta entrada do usuario (NLP)                      │
│  - Questiona informacoes faltantes                          │
│  - Confirma ajustes necessarios                             │
│  - Gera input estruturado para scripts                      │
│  - Apresenta resultado final ao usuario                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ JSON
┌─────────────────────────────────────────────────────────────┐
│                    SCRIPTS (Python)                         │
│  - Compositor: escopo.json → composicao.json                │
│  - Precificador: composicao.json → precificado.json         │
│  - Output: precificado.json → PDF/Excel                     │
└─────────────────────────────────────────────────────────────┘
```

**Beneficios:**
- Reducao de consumo de tokens (calculos deterministicos via script)
- Rastreabilidade (arquivos JSON intermediarios)
- Testabilidade (scripts podem ser executados standalone)

### 2.2 Formato de Execucao dos Scripts

**Modelo:** Modulos Python com CLI wrapper

```python
# hvac/compositor.py
def processar(escopo: dict) -> dict:
    """Funcao principal - importavel para testes"""
    ...

if __name__ == "__main__":
    # CLI wrapper para uso pelo agente
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    ...
```

**Uso pelo agente:**
```bash
python -m hvac.compositor --input output/2026-01/escopo.json --output output/2026-01/composicao.json
```

### 2.3 I/O de Dados

**Metodo:** Arquivos JSON

**Estrutura de diretorios:**
```
output/
└── YYYY-MM/
    ├── ORC-CLIENTE-YYYYMMDD-001/
    │   ├── escopo.json
    │   ├── composicao.json
    │   ├── precificado.json
    │   └── proposta.pdf
    └── ORC-CLIENTE-YYYYMMDD-002/
        └── ...
```

---

## 3. Ajustes nas Bases de Dados

### 3.1 composicoes.json

| Campo Atual | Campo Novo | Acao |
|-------------|------------|------|
| `qtd_por_metro` | `qtd_var` | Renomear |
| `descricao_variavel.prefixo` | Manter | Compativel com guia |
| `descricao_variavel.sufixo` | Manter | Compativel com guia |
| `descricao_variavel.unidade_singular` | Manter | Compativel com guia |
| `descricao_variavel.unidade_plural` | Manter | Compativel com guia |

**Nota:** Composicoes SEM `descricao_variavel` usam apenas o campo `descricao` estatico.

### 3.2 bdi.json

**Antes (por cliente):**
```json
{
  "bdi": {
    "PRIVADO_PJ": {"percentual": 0.35},
    "PRIVADO_PF": {"percentual": 0.40}
  }
}
```

**Depois (por tipo de insumo):**
```json
{
  "bdi": {
    "MAT": {"descricao": "Materiais", "percentual": 0.35},
    "MO": {"descricao": "Mao de Obra", "percentual": 0.40},
    "FER": {"descricao": "Ferramentas", "percentual": 0.30},
    "EQP": {"descricao": "Equipamentos", "percentual": 0.25}
  }
}
```

### 3.3 Demais Bases

- **materiais.json**: OK (campos extras `data_atualizacao`, `validade_dias` sao uteis)
- **mao_de_obra.json**: Verificar estrutura
- **ferramentas.json**: Verificar estrutura
- **equipamentos.json**: Verificar estrutura

---

## 4. Ajustes nas Skills

### 4.1 hvac (Skill Mestre)

**Ajustes:**
- Atualizar fluxo para chamar scripts Python via Bash
- Remover logica de calculo (delegar aos scripts)
- Manter logica de orquestracao e interacao com usuario

### 4.2 hvac-extrator

**Ajustes:**
- Renomear `metros_linha` para `variavel` (generico)
- Adicionar campo `unidade_variavel` para indicar tipo (M, M2, UN, etc.)
- Manter sistema de `confirmacoes_pendentes`

**Novo schema de saida:**
```json
{
  "itens": [{
    "variavel": 8,
    "unidade_variavel": "M",
    ...
  }]
}
```

### 4.3 hvac-compositor

**Ajustes:**
- Transformar em wrapper que chama script Python
- Skill apenas prepara input e interpreta output

### 4.4 hvac-precificador

**Ajustes:**
- Transformar em wrapper que chama script Python
- Atualizar para usar BDI por tipo de insumo

### 4.5 hvac-output

**Manter como esta** - geracao de documentos continua no agente

### 4.6 hvac-cotacoes

**Manter como esta** - gerenciamento de cotacoes continua no agente

---

## 5. Scripts Python a Criar

### 5.1 Estrutura do Pacote

```
hvac/
├── __init__.py
├── compositor.py      # Escopo → Composicao
├── precificador.py    # Composicao → Precificado
├── utils/
│   ├── __init__.py
│   ├── loader.py      # Carrega bases JSON
│   └── calculator.py  # Funcoes de calculo
└── tests/
    ├── test_compositor.py
    └── test_precificador.py
```

### 5.2 compositor.py

**Entrada:** `escopo.json`
**Saida:** `composicao.json`

**Funcionalidades:**
- Ler composicoes.json
- Para cada item do escopo, expandir composicao
- Calcular quantidades: `qtd_base + (qtd_var × variavel)`
- Consolidar materiais, MO e ferramentas
- Gerar descricoes usando `descricao_variavel` quando disponivel

### 5.3 precificador.py

**Entrada:** `composicao.json`
**Saida:** `precificado.json`

**Funcionalidades:**
- Ler bases de precos (materiais, mao_de_obra, ferramentas)
- Ler bdi.json (por tipo de insumo)
- Calcular custo direto por categoria
- Aplicar BDI por tipo: `preco_venda = custo × (1 + bdi[tipo])`
- Gerar resumo financeiro
- Gerar alertas (precos desatualizados, etc.)

---

## 6. Metricas de Sucesso

| Metrica | Meta | Como Medir |
|---------|------|------------|
| Precisao | ±5% vs calculo manual | Comparar 10 orcamentos |
| Tempo | < 30s para orcamento completo | Medir tempo total |
| Tokens | -50% vs tudo via agente | Comparar custo API |

---

## 7. Plano de Implementacao

### Fase 1: Ajuste de Bases
1. [ ] Renomear `qtd_por_metro` → `qtd_var` em composicoes.json
2. [ ] Reestruturar bdi.json para BDI por insumo
3. [ ] Validar estrutura das demais bases

### Fase 2: Scripts Python
4. [ ] Criar estrutura do pacote hvac/
5. [ ] Implementar compositor.py
6. [ ] Implementar precificador.py
7. [ ] Criar testes unitarios

### Fase 3: Ajuste de Skills
8. [ ] Atualizar hvac-extrator (schema de saida)
9. [ ] Atualizar hvac-compositor (wrapper para script)
10. [ ] Atualizar hvac-precificador (wrapper para script)
11. [ ] Atualizar hvac (skill mestre - fluxo)

### Fase 4: Validacao
12. [ ] Testar fluxo completo com caso real
13. [ ] Comparar com calculo manual
14. [ ] Ajustar conforme necessario

---

## 8. Compatibilidade Futura

- Sistema Excel descrito no GUIA sera compatibilizado posteriormente
- Bases JSON sao a fonte de verdade
- Excel pode ser gerado como output adicional

---

## 9. Observacoes

- Implementacao em paralelo (bases + scripts + skills)
- Priorizar funcionalidade sobre perfeicao
- Iterar apos primeira versao funcional

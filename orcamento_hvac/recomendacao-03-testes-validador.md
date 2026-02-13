# Recomendação 03 - Testes Automáticos do Validador de Composições

## Objetivo
Garantir que o validador de composições continue confiável ao longo da evolução do catálogo, evitando regressões silenciosas.

## Motivação
Sem testes automatizados, ajustes no validador ou na base podem introduzir falhas que só aparecem tardiamente na operação.

## Escopo dos testes

### 1) Casos válidos (happy path)
- Composição correta deve passar sem erro.
- Relatórios (Markdown/JSON) devem ser gerados corretamente.

### 2) Casos inválidos esperados
- Código órfão deve gerar erro.
- Quantidade negativa deve gerar erro.
- Composição sem itens deve gerar erro.
- Estrutura inválida de item deve gerar erro.

### 3) Regras avançadas (quando habilitadas)
- Inconsistência de unidade variável.
- Outlier de quantidade.
- Duplicidade de código/descrição.
- Cobertura mínima para composições vendáveis.

## Estrutura sugerida
- `tests/test_validar_composicoes.py`
- `tests/fixtures/composicoes_validas.py`
- `tests/fixtures/composicoes_invalidas.py`

## Estratégia de implementação
1. Refatorar `validar_composicoes.py` para funções puras e testáveis.
2. Criar fixtures mínimas para cada regra.
3. Implementar testes unitários por regra.
4. Implementar teste de integração do relatório final.

## Execução local
```bash
python3 validar_composicoes.py
pytest -q tests/test_validar_composicoes.py
```

## Critério de aceite
- Todos os testes passam na base atual.
- Casos críticos cobertos por testes automatizados.
- Toda regra nova passa a exigir teste correspondente.

## Próximo passo
Implementar em branch dedicada:
`feature/validacao-avancada-composicoes`

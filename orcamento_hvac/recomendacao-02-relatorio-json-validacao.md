# Recomendação 02 - Relatório JSON de Validação

## Objetivo
Complementar o relatório Markdown com saída JSON para permitir automação, integração com pipelines e rastreabilidade estruturada.

## Problema atual
- O relatório em Markdown é excelente para leitura humana.
- Para automação, parsing de texto é frágil e custoso.

## Proposta
Gerar dois formatos em toda execução de validação:
1. `relatorio-validacao-composicoes.md` (humano)
2. `relatorio-validacao-composicoes.json` (máquina)

## Benefícios

### 1) Automação em CI/CD
Permite regras automáticas como:
- falhar pipeline se houver erro bloqueante
- aprovar com warnings quando dentro de limite

### 2) Integração com ferramentas
Facilita consumo por:
- scripts de monitoramento
- dashboards internos
- bots de notificação

### 3) Histórico e comparação
Estrutura JSON simplifica comparação entre execuções para detectar:
- aumento de alertas
- novas regressões
- tendência de qualidade da base

### 4) Governança de regras
Cada finding pode carregar:
- código da regra
- severidade
- composição afetada
- recomendação de correção

## Estrutura sugerida (schema inicial)
```json
{
  "meta": {
    "gerado_em": "2026-02-11T21:00:00-03:00",
    "total_composicoes": 94,
    "versao_regras": "v1"
  },
  "resumo": {
    "erros": 0,
    "avisos": 2,
    "infos": 5
  },
  "findings": [
    {
      "severidade": "alerta",
      "regra": "OUTLIER_QTD_VAR",
      "composicao": "COMP_INST_HW_24K",
      "item": "MAT:SOL_PRATA",
      "mensagem": "qtd_var acima da faixa recomendada",
      "acao_sugerida": "revisar coeficiente técnico"
    }
  ]
}
```

## Regras operacionais sugeridas
- **Erro:** bloqueia aprovação técnica
- **Alerta:** permite seguir, mas exige revisão
- **Info:** não bloqueia, apenas registra melhoria

## Entregáveis de implementação
1. Atualizar `validar_composicoes.py` para exportar JSON
2. Definir códigos de regra padronizados
3. Escrever documentação rápida do schema
4. Ajustar relatório Markdown para referenciar o JSON

## Critério de aceite
- Arquivo JSON sempre gerado junto ao Markdown
- Schema estável e versionado (`versao_regras`)
- Findings com severidade e regra identificável
- JSON legível e válido (UTF-8, sem ambiguidade)

## Próximo passo
Implementar em branch dedicada:
`feature/validacao-avancada-composicoes`

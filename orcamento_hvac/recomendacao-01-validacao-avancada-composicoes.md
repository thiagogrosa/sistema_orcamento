# Recomendação 01 - Validação Avançada de Composições

## Objetivo
Evoluir a validação atual para prevenir erros silenciosos de orçamento e aumentar a confiabilidade da base de composições.

## Escopo da validação avançada

### 1) Consistência de unidade variável
Validar coerência entre:
- `unid_sing` / `unid_plur`
- presença de itens com `qtd_var > 0`
- tipo de composição (fixa vs variável)

Regras sugeridas:
- Se a composição é variável, deve ter `unid_sing` e `unid_plur` preenchidos.
- Se há `unid_sing/unid_plur`, deve existir ao menos um item com `qtd_var > 0`.
- Se a composição é fixa, itens não devem depender de variável sem justificativa.

### 2) Detecção de outliers de quantidade
Identificar valores fora de faixa em `qtd_base` e `qtd_var`, por tipo de item (MAT/MO/FER/EQP).

Regras sugeridas:
- Faixas mínimas/máximas por família de item (ex.: solda, fita, mão de obra por metro).
- Flag de alerta para valores extremos, sem bloquear imediatamente.
- Lista de exceções permitidas por composição.

### 3) Duplicidade de composições
Detectar:
- códigos duplicados
- descrições idênticas ou quase idênticas para códigos diferentes
- composições com estrutura praticamente igual (potencial redundância)

Regras sugeridas:
- código deve ser único (erro bloqueante)
- descrição muito parecida gera alerta para revisão
- similaridade estrutural alta gera aviso (não bloqueante)

### 4) Cobertura mínima para composições vendáveis
Para composições de instalação vendáveis, validar presença (direta ou por regra explícita) de blocos críticos:
- elétrica
- dreno
- acabamento

Regras sugeridas:
- composição vendável sem cobertura mínima gera alerta/erro conforme criticidade
- permitir exclusões explícitas e documentadas

## Níveis de severidade
- **Erro (bloqueante):** impede publicação/uso da base
- **Alerta (não bloqueante):** exige revisão, mas permite seguir
- **Info:** observação para melhoria futura

## Entregáveis de implementação
1. Evolução do script `validar_composicoes.py` com regras avançadas
2. Relatório Markdown (`relatorio-validacao-composicoes.md`) com erros/alertas por composição
3. Relatório JSON para automação futura (CI)
4. Suite de testes para evitar regressão

## Critério de aceite
- Zero códigos órfãos
- Zero códigos duplicados
- Zero quantidades negativas
- Alertas de outlier e cobertura mínima reportados com clareza
- Regras documentadas e rastreáveis

## Próximo passo
Implementar em branch dedicada:
`feature/validacao-avancada-composicoes`

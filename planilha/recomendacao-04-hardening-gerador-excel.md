# Recomendação 04 - Hardening do Gerador de Planilha Excel

## Objetivo
Transformar o gerador de planilha em um processo confiável de produção, com validações antes e depois da geração, reduzindo risco operacional para o time de orçamentos.

## Contexto
As bases (materiais, mão de obra, ferramentas, equipamentos e composições) evoluem com frequência. O Excel precisa refletir essas mudanças automaticamente, com segurança e rastreabilidade.

## Escopo da recomendação

### Fase A - Gate pré-geração (entrada)
Adicionar validações obrigatórias antes de criar o Excel:
- integridade entre bases (sem códigos órfãos)
- duplicidades de código/descrição
- faixas técnicas de quantidade
- cobertura mínima de composições vendáveis

Se houver erro bloqueante, **não gerar** planilha.

### Fase B - Hardening da geração
Aprimorar o fluxo de `criar_planilha.py` e módulos de abas para garantir:
- Data Validation consistente (dropdowns corretos)
- Named ranges atualizados dinamicamente
- fórmulas críticas corretamente aplicadas
- proteção de células de fórmula (inputs liberados)
- padronização de usabilidade (filtros, congelamento, formatos)

### Fase C - Auditoria pós-geração
Criar auditoria automática da planilha gerada:
- abas obrigatórias presentes
- fórmulas esperadas nas colunas-chave
- validações de dados aplicadas
- named ranges válidos
- ausência de referências quebradas (ex.: `#REF!`)

Saída:
- `relatorio-auditoria-planilha.md`
- `relatorio-auditoria-planilha.json`

### Fase D - Testes e estabilidade
Cobrir com testes:
- smoke test de geração completa
- testes de auditoria
- testes de regressão de fórmulas/validações

## Entregáveis
1. Scripts de validação pré-geração e auditoria pós-geração
2. Relatórios em Markdown e JSON
3. Ajustes no gerador para robustez operacional
4. Testes automatizados para impedir regressão

## Critério de aceite
- geração bloqueia em erros críticos de base
- planilha gerada passa na auditoria sem erros
- execução reprodutível
- relatórios legíveis para humano e máquina

## Deve ser 1 sprint ou dividido?
**Recomendação:** dividir em 2 sprints para reduzir risco.

### Sprint 4A (fundação)
- Gate pré-geração
- Auditoria pós-geração (escopo mínimo)
- Relatórios md/json

### Sprint 4B (robustez operacional)
- Hardening avançado de fórmulas/validações
- Proteção de células e usabilidade
- Testes de regressão do gerador

## Ordem recomendada entre as 4 recomendações

1. **Recomendação 01 - Validação avançada de composições**
   - Garante qualidade semântica e técnica da base.
2. **Recomendação 03 - Testes automatizados do validador**
   - Evita regressão enquanto a regra evolui.
3. **Recomendação 02 - Relatório JSON de validação**
   - Habilita automação/CI e integração com outros fluxos.
4. **Recomendação 04 - Hardening do gerador Excel**
   - Aplica robustez operacional no ponto final de uso do time.

## Observação estratégica
Mesmo sendo a quarta recomendação, o Sprint 4A pode iniciar em paralelo após um baseline estável da Recomendação 01.

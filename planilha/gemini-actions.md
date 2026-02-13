# Próximos Passos Sugeridos - Gemini CLI

Com base na análise do repositório e nos planos de implementação (Arrays Dinâmicos e Web Scraping), seguem os próximos passos recomendados:

## 1. Integração do Web Scraper com o Sistema CSV
O sistema de scraping foi adicionado recentemente, mas precisa alimentar automaticamente a pasta `dados_csv/` para que as macros VBA possam importar os preços atualizados.
*   **Ação:** Ajustar o `scraper_cli.py` ou criar um script de ponte para exportar os dados raspados diretamente no formato `{catalogo}_{YYYY-MM-DD}.csv`.
*   **Objetivo:** Automatizar o fluxo "Scraping -> CSV -> Excel".

## 2. Refinamento do Modo Template (Python vs Excel)
Considerando que o `openpyxl` não suporta a escrita de fórmulas modernas (LET, LAMBDA), o código Python deve ser revisado.
*   **Ação:** Verificar `abas/composicoes.py` e `abas/escopo.py` para garantir que não estão tentando escrever fórmulas de spill, deixando essa tarefa exclusivamente para o `template.xlsm`.
*   **Objetivo:** Evitar que o Excel remova fórmulas ao abrir o arquivo gerado.

## 3. Padronização da Aba ESCOPO
Existe uma divergência de nomenclatura entre `ORCAMENTO` e `ESCOPO` nos documentos de plano e na implementação real.
*   **Ação:** Renomear referências internas e garantir que as fórmulas de spill na aba `ESCOPO` (F7, G7) busquem os totais das colunas S e T da aba `COMPOSICOES`.
*   **Objetivo:** Consistência arquitetural e funcionamento correto dos totais.

## 4. Expansão dos Scrapers
A pasta `scraping/scrapers/` ainda possui apenas exemplos.
*   **Ação:** Implementar scrapers reais para os principais fornecedores de HVAC identificados no catálogo.
*   **Objetivo:** Tornar o sistema de coleta de preços funcional para o dia a dia.

## 5. Implementação de Testes de Integridade
Com a migração para arrays dinâmicos e importação de CSVs, a validação dos dados tornou-se crítica.
*   **Ação:** Criar testes unitários para os validadores em `scraping/validator.py` e para a estrutura dos dicionários em `dados/`.
*   **Objetivo:** Garantir que erros de formatação nos dados não quebrem a geração da planilha.

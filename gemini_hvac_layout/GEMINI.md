# GEMINI.md - Contexto do Projeto Gemini HVAC Layout

Este documento fornece uma visão geral técnica e operacional do projeto `gemini_hvac_layout`, destinado à geração automatizada de orçamentos profissionais para sistemas de climatização (HVAC).

---

## 1. Visão Geral do Projeto

O sistema é uma ferramenta de orçamentação baseada em Python que transforma dados de precificação (materiais, mão de obra, ferramentas) em propostas comerciais em PDF altamente estilizadas e planilhas internas de controle.

### Principais Tecnologias
*   **Linguagem:** Python 3.12+
*   **Motor de Template:** Jinja2 (HTML dinâmico)
*   **Gerador de PDF:** WeasyPrint (Conversão HTML/CSS para PDF)
*   **Manipulação de Planilhas:** openpyxl (Geração de relatórios Excel)
*   **Bases de Dados:** Arquivos JSON estruturados

---

## 2. Estrutura do Diretório

*   `bases/`: Catálogos de insumos (materiais, mão de obra, equipamentos) e regras de BDI.
*   `imported_bases/`: Definições de classes e modelos de dados (Python) para as bases.
*   `config/`: Parâmetros da empresa, dados do usuário, condições comerciais e exclusões técnicas.
*   `hvac/`: Core da aplicação.
    *   `generators/`: Lógica de geração de documentos (PDF e Excel).
    *   `utils/`: Utilitários de formatação, cálculo e carregamento de dados.
*   `skills/`: Instruções e definições para agentes especializados (migrado do projeto original).
*   `templates/html/`: Templates `proposta_base.html` e `proposta_styles.css` que definem a identidade visual.
*   `tests/`: Arquivos JSON de entrada para simulação de orçamentos (ex: `dados_teste_panvel.json`).
*   `dist_original/`: Pacote de distribuição contendo os arquivos otimizados para reincorporação no projeto principal.
*   `output/`: PDFs e planilhas gerados (organizados por cliente).

---

## 3. Comandos e Execução

### Ambiente Virtual
O projeto utiliza um ambiente virtual local para gerenciar dependências:
```bash
source .venv/bin/activate
```

### Geração de Documentos
*   **Gerar PDF de Teste (Padrão):**
    ```bash
    ./gerar_teste_pdf.sh
    ```
*   **Gerar Múltiplas Versões (Stress Test de Layout):**
    ```bash
    ./gerar_todos_testes.sh
    ```

### Dependências Principais
As bibliotecas necessárias são: `weasyprint`, `jinja2`, `openpyxl`, `fpdf2`.

---

## 4. Convenções de Desenvolvimento

*   **Identidade Visual:** Rigorosa adesão às cores Azul (#0A94D6) e Verde (#00A859).
*   **Tratamento de Dados:** Propostas comerciais devem sempre utilizar a data atual da geração, ignorando datas históricas nos arquivos de entrada.
*   **Layout de PDF:** Utilização da classe `.bloco-fechamento` para evitar que assinaturas e termos comerciais sejam separados por quebras de página.
*   **Imagens:** Logotipos e assinaturas devem ser convertidos para Base64 antes da renderização para garantir portabilidade no PDF.

---

## 5. Fluxo de Trabalho de Orçamentação

1.  O usuário fornece um JSON em `tests/` com o escopo e itens precificados.
2.  O sistema carrega as configurações de `config/` e `bases/`.
3.  A lógica em `hvac/generators/proposta_pdf.py` processa o template HTML.
4.  O PDF é gerado em `output/{slug_cliente}/` com numeração sequencial automática gerada por `config/contador.json`.

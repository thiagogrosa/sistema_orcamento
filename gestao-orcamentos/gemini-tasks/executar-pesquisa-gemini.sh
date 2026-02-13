#!/bin/bash
# Script para executar pesquisa no Gmail via Gemini CLI
# Uso: ./executar-pesquisa-gemini.sh [task_id]

TASKS_DIR="/root/thiagorosa/gestao-orcamentos/gemini-tasks"
TASKS_FILE="$TASKS_DIR/pesquisa-gmail-pendentes.md"
RESULTS_FILE="$TASKS_DIR/resultados-pesquisa-gmail.json"

# Se não existir arquivo de resultados, criar vazio
if [ ! -f "$RESULTS_FILE" ]; then
    echo "[]" > "$RESULTS_FILE"
fi

# Prompt base para o Gemini
PROMPT_BASE="Você é um assistente especializado em extrair informações de emails.

CONTEXTO:
- Conta Gmail: orcamentos2@armant.com.br
- Empresa: Armant - Setor de Orçamentos de Climatização
- Objetivo: Complementar informações de demandas de orçamento

TAREFA:
Acesse o Gmail via MCP e pesquise emails conforme as instruções.
Extraia as informações solicitadas e retorne em formato JSON.

INSTRUÇÕES DETALHADAS:
"

# Função para executar pesquisa de uma task específica
executar_task() {
    local task_id=$1
    echo "Executando pesquisa: $task_id"

    # Aqui seria a chamada ao Gemini CLI
    # gemini -p "$PROMPT_BASE" -f "$TASKS_FILE" --task "$task_id"

    echo "Pesquisa $task_id enviada ao Gemini CLI"
}

# Se task_id foi passado, executar apenas essa
if [ -n "$1" ]; then
    executar_task "$1"
else
    echo "Uso: $0 <task_id>"
    echo "Exemplo: $0 TASK_001"
    echo ""
    echo "Tasks disponíveis:"
    grep "^### TASK_" "$TASKS_FILE" | sed 's/### /  - /'
fi

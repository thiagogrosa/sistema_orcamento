#!/bin/bash
# Script para regenerar PDF de teste
# Uso: ./gerar_teste_pdf.sh [numero_orcamento] [revisao]

NUMERO=$1
REVISAO=$2
INPUT_FILE=${3:-"tests/dados_teste_panvel.json"}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Usa python do sistema por padrão (mais estável neste ambiente)
# Para forçar venv: export PYTHON_BIN=/caminho/venv/bin/python3
PYTHON_BIN="${PYTHON_BIN:-python3}"

# Executa a geração e captura o caminho do PDF
PDF_PATH=$($PYTHON_BIN -c "
from hvac.generators import gerar_proposta_pdf
import json
import os
import sys

numero = '$NUMERO' if '$NUMERO' else None
revisao = '$REVISAO' if '$REVISAO' else None
input_file = '$INPUT_FILE'

with open(input_file) as f:
    dados = json.load(f)

os.makedirs('output/testes', exist_ok=True)

pdf = gerar_proposta_pdf(dados, rascunho=True, numero_orcamento=numero, revisao=revisao)
print(pdf['arquivo_pdf'])
")

if [ -f "$PDF_PATH" ]; then
    echo -e "\n=== PDF Gerado ==="
    echo "Arquivo: $PDF_PATH"
    
    # Se estiver em WSL com PowerShell disponível, tenta abrir no Chrome
    if command -v powershell.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
        WIN_PATH=$(wslpath -w "$PDF_PATH")
        powershell.exe -Command "Start-Process chrome -ArgumentList '$WIN_PATH'" 2>/dev/null || true
        echo "Abrindo no Chrome..."
    fi
else
    echo "Erro: PDF não foi gerado corretamente."
    exit 1
fi


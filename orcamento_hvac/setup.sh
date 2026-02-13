#!/usr/bin/env bash
set -euo pipefail

# Script de configuracao inicial - Projeto Planilha HVAC
# Prepara ambiente para geracao de planilhas e scraping.

echo "==============================================="
echo "Iniciando configuracao do ambiente..."
echo "==============================================="

# 1. Selecionar Python (prioriza versoes mais novas)
if command -v python3.12 >/dev/null 2>&1; then
    PYTHON_BIN="python3.12"
elif command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
else
    echo "Erro: Python 3 nao encontrado. Instale Python 3.11+ (recomendado 3.12)."
    exit 1
fi

VENV_DIR="${VENV_DIR:-venv}"
echo "Python selecionado: $($PYTHON_BIN --version)"

# 2. Criar pastas necessarias
echo "Criando estrutura de pastas..."
mkdir -p dados_csv
mkdir -p scraping/cache
mkdir -p scraping/logs

# 3. Criar ambiente virtual
if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual ($VENV_DIR)..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    echo "Ambiente virtual ja existe: $VENV_DIR"
fi

# 4. Instalar dependencias
echo "Instalando dependencias via pip..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
if [ -f "requirements.txt" ]; then
    "$VENV_DIR/bin/pip" install -r requirements.txt
else
    echo "Aviso: requirements.txt nao encontrado. Instalando dependencias basicas..."
    "$VENV_DIR/bin/pip" install openpyxl requests beautifulsoup4 lxml pytest
fi

# 5. Tornar CLI executavel
if [ -f "scraper_cli.py" ]; then
    chmod +x scraper_cli.py
fi

echo ""
echo "==============================================="
echo "Configuracao concluida com sucesso!"
echo "==============================================="
echo "Para comecar, ative o ambiente virtual:"
echo "source $VENV_DIR/bin/activate"
echo ""
echo "Comandos uteis:"
echo "- Gerar planilha: $VENV_DIR/bin/python criar_planilha.py"
echo "- Rodar scraper:  $VENV_DIR/bin/python scraper_cli.py --help"
echo "- Rodar testes:   $VENV_DIR/bin/pytest -q"
echo "==============================================="

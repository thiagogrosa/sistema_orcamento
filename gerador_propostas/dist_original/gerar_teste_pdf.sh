#!/bin/bash
# Script para regenerar PDF de teste apos editar template
# Uso: ./gerar_teste_pdf.sh

cd /root/thiagorosa/gemini_hvac_layout

# Usa o ambiente virtual do projeto
.venv/bin/python3 -c "
from hvac.generators import gerar_proposta_pdf
import json
import os

with open('tests/dados_teste_panvel.json') as f:
    dados = json.load(f)

# Garante que a pasta de output existe
os.makedirs('output/testes', exist_ok=True)

pdf = gerar_proposta_pdf(dados, rascunho=True)
print(f'\n=== PDF Gerado ===\nArquivo: {pdf['arquivo_pdf']}\nRascunho: {pdf.get('arquivo_rascunho', 'N/A')}')
"


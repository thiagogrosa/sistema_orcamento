#!/bin/bash
# Script para gerar todas as versões de teste do PDF

cd /root/thiagorosa/gemini_hvac_layout

for n in 2 3 4 5
do
    echo "Gerando versão com $n itens..."
    .venv/bin/python3 <<EOF
from hvac.generators import gerar_proposta_pdf
import json
import os

with open('tests/dados_teste_panvel_x$n.json') as f:
    dados = json.load(f)

os.makedirs('output/testes_multiplus', exist_ok=True)
pdf = gerar_proposta_pdf(dados, rascunho=False)
print(f"Sucesso: {pdf['arquivo_pdf']}")
EOF
done
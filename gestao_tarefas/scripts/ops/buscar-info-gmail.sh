#!/bin/bash
# Script para buscar informações no Gmail via Gemini CLI
# Uso: ./buscar-info-gmail.sh [demanda_id]

set -e

DEMANDA_ID="${1:-}"
PROJETO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTADO_DIR="$PROJETO_DIR/resultados-gmail"

# Criar diretório de resultados
mkdir -p "$RESULTADO_DIR"

# Se não forneceu ID, buscar todas as demandas pendentes
if [ -z "$DEMANDA_ID" ]; then
    echo "Buscando informações para todas as demandas pendentes..."

    # Ler o arquivo pesquisa-gemini.md e executar
    PROMPT=$(cat "$PROJETO_DIR/pesquisa-gemini.md")

    echo "Executando Gemini CLI..."
    echo ""

    gemini -p "$PROMPT" | tee "$RESULTADO_DIR/busca-completa-$(date +%Y%m%d-%H%M%S).txt"

else
    # Buscar demanda específica
    echo "Buscando informações para demanda: $DEMANDA_ID"

    case "$DEMANDA_ID" in
        "26_060")
            PROMPT="Busque no Gmail (orcamentos2@armant.com.br) emails sobre Porto Seguro PMOC.
Período: Janeiro-Fevereiro 2026 (últimos 60 dias).
Extraia: Cliente, CNPJ, Contato, Telefone, Email, Endereço, Cidade/Estado, Escopo, Prazo.
Retorne no formato estruturado."
            ;;
        "26_062")
            PROMPT="Busque no Gmail (orcamentos2@armant.com.br) emails sobre Colombo Park Shopping.
Período: Janeiro-Fevereiro 2026 (últimos 60 dias).
Extraia: Nome do contato, Telefone, Email, Escopo solicitado, Prazo.
Retorne no formato estruturado."
            ;;
        *)
            PROMPT="Busque no Gmail (orcamentos2@armant.com.br) emails sobre $DEMANDA_ID.
Período: últimos 60 dias.
Extraia todas as informações de contato e escopo do projeto."
            ;;
    esac

    echo "Executando Gemini CLI..."
    echo ""

    gemini -p "$PROMPT" | tee "$RESULTADO_DIR/busca-$DEMANDA_ID-$(date +%Y%m%d-%H%M%S).txt"
fi

echo ""
echo "✅ Busca concluída!"
echo "📁 Resultado salvo em: $RESULTADO_DIR"

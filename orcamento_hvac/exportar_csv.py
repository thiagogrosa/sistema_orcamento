#!/usr/bin/env python3
"""
Exporta dados Python para CSV com validade por item.

Gera arquivos CSV na pasta dados_csv/ a partir dos dados em dados/*.py.
Esses CSVs serão mantidos pelo setor de suprimentos e importados
via macro VBA na planilha de orçamentos.

Convenção de nome: {catalogo}_{YYYY-MM-DD}.csv
O sistema importará o arquivo mais recente de cada tipo.

Uso: python3 exportar_csv.py
"""
import os
import csv
from datetime import datetime

from dados import MATERIAIS, MAO_DE_OBRA, FERRAMENTAS, EQUIPAMENTOS

# Diretório de saída
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'dados_csv')

# Configurações CSV
CSV_DELIMITER = ';'
CSV_ENCODING = 'utf-8-sig'  # UTF-8 com BOM para Excel

# Data de hoje para nome do arquivo
TODAY = datetime.now().strftime('%Y-%m-%d')


def exportar_materiais():
    """Exporta catálogo de materiais com validade por item."""
    filename = f'materiais_{TODAY}.csv'
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(['CODIGO', 'CATEGORIA', 'DESCRICAO', 'UNIDADE', 'PRECO',
                         'ATUALIZADO_EM', 'VALIDADE_DIAS'])
        for item in MATERIAIS:
            # item: (codigo, categoria, descricao, unidade, preco, data_atualizacao, validade_dias)
            writer.writerow(item)
    return len(MATERIAIS), filename


def exportar_mao_de_obra():
    """Exporta catálogo de mão de obra com validade por item."""
    filename = f'mao_de_obra_{TODAY}.csv'
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(['CODIGO', 'CATEGORIA', 'DESCRICAO', 'UNIDADE', 'CUSTO',
                         'ATUALIZADO_EM', 'VALIDADE_DIAS'])
        for item in MAO_DE_OBRA:
            # item: (codigo, categoria, descricao, unidade, custo, data_atualizacao, validade_dias)
            writer.writerow(item)
    return len(MAO_DE_OBRA), filename


def exportar_ferramentas():
    """Exporta catálogo de ferramentas com validade por item."""
    filename = f'ferramentas_{TODAY}.csv'
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(['CODIGO', 'CATEGORIA', 'DESCRICAO', 'VALOR_AQUISICAO',
                         'VIDA_UTIL_HORAS', 'ATUALIZADO_EM', 'VALIDADE_DIAS'])
        for item in FERRAMENTAS:
            # item: (codigo, categoria, descricao, valor_aquisicao, vida_util, data_atualizacao, validade_dias)
            writer.writerow(item)
    return len(FERRAMENTAS), filename


def exportar_equipamentos():
    """Exporta catálogo de equipamentos com validade por item."""
    filename = f'equipamentos_{TODAY}.csv'
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(['CODIGO', 'CATEGORIA', 'DESCRICAO', 'CAPACIDADE_BTU',
                         'UNIDADE', 'PRECO', 'ATUALIZADO_EM', 'VALIDADE_DIAS'])
        for item in EQUIPAMENTOS:
            # item: (codigo, categoria, descricao, capacidade, unidade, preco, data_atualizacao, validade_dias)
            writer.writerow(item)
    return len(EQUIPAMENTOS), filename


def main():
    """Executa exportação de todos os catálogos."""
    # Garantir que o diretório existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print('Exportando catálogos para CSV...')
    print(f'Diretório: {OUTPUT_DIR}')
    print(f'Data: {TODAY}')
    print()

    # Exportar cada catálogo
    count, filename = exportar_materiais()
    print(f'  {filename}: {count} itens')

    count, filename = exportar_mao_de_obra()
    print(f'  {filename}: {count} itens')

    count, filename = exportar_ferramentas()
    print(f'  {filename}: {count} itens')

    count, filename = exportar_equipamentos()
    print(f'  {filename}: {count} itens')

    print()
    print('Exportação concluída!')
    print()
    print('Estrutura do CSV:')
    print('- Cada item possui ATUALIZADO_EM (data) e VALIDADE_DIAS')
    print('- Nome do arquivo inclui data para histórico')
    print('- O VBA importará o arquivo mais recente de cada tipo')
    print()
    print('Próximos passos:')
    print('1. Revise os arquivos CSV gerados')
    print('2. Distribua para o setor de suprimentos')
    print('3. Use a macro VBA para importar na planilha')


if __name__ == '__main__':
    main()

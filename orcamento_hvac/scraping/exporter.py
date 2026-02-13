"""
Exportação de dados coletados para CSV.
"""
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from .config import CSV_DELIMITER, CSV_ENCODING, OUTPUT_DIR


class DataExporter:
    """Exporta dados coletados para CSV."""

    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_products(
        self,
        products: List[Dict[str, Any]],
        filename: str = None,
        include_timestamp: bool = True
    ) -> str:
        """
        Exporta lista de produtos para CSV.

        Args:
            products: Lista de dicts com produtos
            filename: Nome do arquivo (sem extensão)
            include_timestamp: Se deve incluir timestamp no nome

        Returns:
            Caminho do arquivo gerado
        """
        if not products:
            raise ValueError("Lista de produtos vazia")

        # Gerar nome do arquivo
        if filename is None:
            filename = 'produtos_scraped'

        if include_timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            filename = f"{filename}_{timestamp}"

        filepath = self.output_dir / f"{filename}.csv"

        # Determinar todas as chaves presentes
        all_keys = set()
        for product in products:
            all_keys.update(product.keys())

        # Ordenar chaves (campos principais primeiro)
        priority_keys = ['name', 'price', 'url', 'source', 'scraped_at']
        sorted_keys = [k for k in priority_keys if k in all_keys]
        sorted_keys.extend(sorted(all_keys - set(sorted_keys)))

        # Escrever CSV
        with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=sorted_keys,
                delimiter=CSV_DELIMITER,
                extrasaction='ignore'
            )

            writer.writeheader()
            writer.writerows(products)

        return str(filepath)

    def export_to_import_format(
        self,
        products: List[Dict[str, Any]],
        category: str,
        validade_dias: int = 30
    ) -> str:
        """
        Exporta produtos no formato compatível com importação do sistema.
        DEPRECATED: Use export_to_system_format() para exportar para dados_csv/
        """
        return self.export_to_system_format(products, category, validade_dias)

    def export_to_system_format(
        self,
        products: List[Dict[str, Any]],
        category: str,
        validade_dias: int = None,
        codigo_prefix: str = None
    ) -> str:
        """
        Exporta produtos no formato compatível com o sistema de importação VBA.

        O arquivo é salvo em dados_csv/ com nome {category}_{YYYY-MM-DD}.csv

        Args:
            products: Lista de produtos scraped
            category: Tipo do catálogo (materiais, mao_de_obra, ferramentas, equipamentos)
            validade_dias: Dias de validade (padrão depende da categoria)
            codigo_prefix: Prefixo para códigos gerados (ex: 'MAT_ML' para MercadoLivre)

        Returns:
            Caminho do arquivo gerado
        """
        if not products:
            raise ValueError("Lista de produtos vazia")

        # Validar categoria
        valid_categories = ['materiais', 'mao_de_obra', 'ferramentas', 'equipamentos']
        if category not in valid_categories:
            raise ValueError(f"Categoria inválida: {category}. Use: {', '.join(valid_categories)}")

        # Validades padrão por categoria
        default_validades = {
            'materiais': 7,
            'mao_de_obra': 30,
            'ferramentas': 90,
            'equipamentos': 30
        }
        if validade_dias is None:
            validade_dias = default_validades[category]

        # Prefixos padrão por categoria
        default_prefixes = {
            'materiais': 'MAT',
            'mao_de_obra': 'MO',
            'ferramentas': 'FER',
            'equipamentos': 'EQP'
        }
        if codigo_prefix is None:
            codigo_prefix = default_prefixes[category]

        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{category}_{date_str}"
        filepath = self.output_dir / f"{filename}.csv"

        # Schemas por categoria
        schemas = {
            'materiais': {
                'headers': ['CODIGO', 'CATEGORIA', 'DESCRICAO', 'UNIDADE', 'PRECO',
                           'ATUALIZADO_EM', 'VALIDADE_DIAS'],
                'row_builder': lambda i, p: {
                    'CODIGO': f"{codigo_prefix}_{i+1:04d}",
                    'CATEGORIA': p.get('category', 'Diversos'),
                    'DESCRICAO': p.get('name', 'N/A')[:100],
                    'UNIDADE': p.get('unit', 'UN'),
                    'PRECO': p.get('price', 0),
                    'ATUALIZADO_EM': date_str,
                    'VALIDADE_DIAS': validade_dias
                }
            },
            'mao_de_obra': {
                'headers': ['CODIGO', 'CATEGORIA', 'DESCRICAO', 'UNIDADE', 'CUSTO',
                           'ATUALIZADO_EM', 'VALIDADE_DIAS'],
                'row_builder': lambda i, p: {
                    'CODIGO': f"{codigo_prefix}_{i+1:04d}",
                    'CATEGORIA': p.get('category', 'Instalação'),
                    'DESCRICAO': p.get('name', 'N/A')[:100],
                    'UNIDADE': p.get('unit', 'H'),
                    'CUSTO': p.get('price', 0),
                    'ATUALIZADO_EM': date_str,
                    'VALIDADE_DIAS': validade_dias
                }
            },
            'ferramentas': {
                'headers': ['CODIGO', 'CATEGORIA', 'DESCRICAO', 'VALOR_AQUISICAO',
                           'VIDA_UTIL_HORAS', 'ATUALIZADO_EM', 'VALIDADE_DIAS'],
                'row_builder': lambda i, p: {
                    'CODIGO': f"{codigo_prefix}_{i+1:04d}",
                    'CATEGORIA': p.get('category', 'Diversos'),
                    'DESCRICAO': p.get('name', 'N/A')[:100],
                    'VALOR_AQUISICAO': p.get('price', 0),
                    'VIDA_UTIL_HORAS': p.get('vida_util', 2000),
                    'ATUALIZADO_EM': date_str,
                    'VALIDADE_DIAS': validade_dias
                }
            },
            'equipamentos': {
                'headers': ['CODIGO', 'CATEGORIA', 'DESCRICAO', 'CAPACIDADE_BTU',
                           'UNIDADE', 'PRECO', 'ATUALIZADO_EM', 'VALIDADE_DIAS'],
                'row_builder': lambda i, p: {
                    'CODIGO': f"{codigo_prefix}_{i+1:04d}",
                    'CATEGORIA': p.get('category', 'Split'),
                    'DESCRICAO': p.get('name', 'N/A')[:100],
                    'CAPACIDADE_BTU': p.get('btu', 0),
                    'UNIDADE': p.get('unit', 'UN'),
                    'PRECO': p.get('price', 0),
                    'ATUALIZADO_EM': date_str,
                    'VALIDADE_DIAS': validade_dias
                }
            }
        }

        schema = schemas[category]
        headers = schema['headers']
        row_builder = schema['row_builder']

        rows = [row_builder(i, product) for i, product in enumerate(products)]

        # Escrever CSV com UTF-8 BOM
        with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=CSV_DELIMITER)
            writer.writeheader()
            writer.writerows(rows)

        return str(filepath)

    def export_price_history(
        self,
        price_history: Dict[str, List[Dict[str, Any]]],
        filename: str = 'historico_precos'
    ) -> str:
        """
        Exporta histórico de preços.

        Args:
            price_history: Dict {product_url: [list of price records]}
            filename: Nome do arquivo

        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d')
        filepath = self.output_dir / f"{filename}_{timestamp}.csv"

        rows = []
        for url, records in price_history.items():
            for record in records:
                rows.append({
                    'url': url,
                    'name': record.get('name', 'N/A'),
                    'price': record.get('price', 0),
                    'source': record.get('source', 'N/A'),
                    'scraped_at': record.get('scraped_at', '')
                })

        if not rows:
            raise ValueError("Histórico vazio")

        with open(filepath, 'w', newline='', encoding=CSV_ENCODING) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['url', 'name', 'price', 'source', 'scraped_at'],
                delimiter=CSV_DELIMITER
            )
            writer.writeheader()
            writer.writerows(rows)

        return str(filepath)

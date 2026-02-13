#!/usr/bin/env python3
"""
CLI para sistema de web scraping de preços HVAC.

Uso:
    python3 scraper_cli.py search "tubo cobre 1/4" --max 5
    python3 scraper_cli.py search "split inverter" --export --category equipamentos
    python3 scraper_cli.py search "tubo cobre" --export --category materiais --prefix MAT_ML
    python3 scraper_cli.py url https://exemplo.com/produto
    python3 scraper_cli.py cache --stats
    python3 scraper_cli.py cache --clear

Exportação para Sistema:
    Use --category para exportar no formato compatível com dados_csv/
    O arquivo será salvo como {category}_{YYYY-MM-DD}.csv
"""
import sys
import argparse
import json
import logging
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from scraping.scrapers import SCRAPERS
from scraping.cache_manager import CacheManager
from scraping.exporter import DataExporter
from scraping.validator import DataValidator


def setup_logging(verbose: bool = False):
    """Configura logging para CLI."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=level
    )


def cmd_search(args):
    """Comando de busca."""
    print(f"Buscando por: '{args.query}'")
    print(f"Máximo de resultados: {args.max}")
    print(f"Scraper: {args.scraper}")
    print()

    # Selecionar scraper
    if args.scraper not in SCRAPERS:
        print(f"Erro: Scraper '{args.scraper}' não encontrado")
        print(f"Scrapers disponíveis: {', '.join(SCRAPERS.keys())}")
        return 1

    scraper_class = SCRAPERS[args.scraper]
    scraper = scraper_class(use_cache=not args.no_cache)

    try:
        with scraper:
            results = scraper.search(args.query, max_results=args.max)

            print(f"\n{'='*60}")
            print(f"Encontrados {len(results)} produtos")
            print(f"{'='*60}\n")

            for i, product in enumerate(results, 1):
                print(f"{i}. {product['name']}")
                print(f"   Preço: R$ {product['price']:.2f}")
                print(f"   URL: {product['url']}")
                print(f"   Fonte: {product['source']}")
                print()

            # Exportar se solicitado
            if args.export:
                exporter = DataExporter()
                if args.category:
                    # Exportar no formato do sistema (para dados_csv/)
                    filepath = exporter.export_to_system_format(
                        results,
                        category=args.category,
                        codigo_prefix=args.prefix
                    )
                    print(f"\n✓ Exportado para sistema: {filepath}")
                else:
                    # Exportar CSV genérico
                    filepath = exporter.export_products(results, filename=args.query.replace(' ', '_'))
                    print(f"\n✓ Resultados exportados para: {filepath}")

            # Estatísticas
            if args.stats:
                print(f"\n{'='*60}")
                print("Estatísticas:")
                print(f"{'='*60}")
                stats = scraper.get_stats()
                for key, value in stats.items():
                    print(f"  {key}: {value}")

            return 0

    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário")
        return 130
    except Exception as e:
        print(f"\nErro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_url(args):
    """Comando para scrape de URL específica."""
    print(f"Scraping URL: {args.url}")
    print()

    # Selecionar scraper
    if args.scraper not in SCRAPERS:
        print(f"Erro: Scraper '{args.scraper}' não encontrado")
        print(f"Scrapers disponíveis: {', '.join(SCRAPERS.keys())}")
        return 1

    scraper_class = SCRAPERS[args.scraper]
    scraper = scraper_class(use_cache=not args.no_cache)

    try:
        with scraper:
            product = scraper.scrape_url(args.url)

            if not product:
                print("✗ Falha ao extrair produto")
                return 1

            print(f"{'='*60}")
            print("Produto encontrado:")
            print(f"{'='*60}\n")

            # Exibir JSON formatado
            print(json.dumps(product, indent=2, ensure_ascii=False))

            # Exportar se solicitado
            if args.export:
                exporter = DataExporter()
                if hasattr(args, 'category') and args.category:
                    filepath = exporter.export_to_system_format(
                        [product],
                        category=args.category,
                        codigo_prefix=getattr(args, 'prefix', None)
                    )
                    print(f"\n✓ Exportado para sistema: {filepath}")
                else:
                    filepath = exporter.export_products([product])
                    print(f"\n✓ Produto exportado para: {filepath}")

            return 0

    except Exception as e:
        print(f"\nErro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_cache(args):
    """Gerenciamento de cache."""
    cache = CacheManager()

    if args.stats:
        stats = cache.get_stats()
        print("Estatísticas do Cache:")
        print(f"{'='*60}")
        print(f"  Total de arquivos: {stats['total_files']}")
        print(f"  Tamanho total: {stats['total_size_mb']:.2f} MB")
        print(f"  Idade média: {stats['avg_age_hours']:.1f} horas")
        print(f"  Mais antigo: {stats['oldest_hours']:.1f} horas")
        print(f"  Mais recente: {stats['newest_hours']:.1f} horas")

    elif args.clear:
        if args.expired:
            removed = cache.clear_expired()
            print(f"✓ {removed} cache(s) expirado(s) removido(s)")
        else:
            if input("Remover TODOS os caches? (s/N): ").lower() == 's':
                removed = cache.clear_all()
                print(f"✓ {removed} cache(s) removido(s)")
            else:
                print("Operação cancelada")

    else:
        print("Use --stats para ver estatísticas ou --clear para limpar")

    return 0


def cmd_validate(args):
    """Valida arquivo CSV de produtos."""
    validator = DataValidator()

    print(f"Validando arquivo: {args.file}")
    print()

    try:
        import csv
        with open(args.file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            products = list(reader)

        print(f"Total de produtos: {len(products)}")

        valid_count = 0
        error_count = 0
        errors = []

        for i, product in enumerate(products, 1):
            # Converter price para float
            if 'price' in product:
                try:
                    product['price'] = float(product['price'])
                except ValueError:
                    errors.append(f"Linha {i}: Preço inválido")
                    error_count += 1
                    continue

            is_valid, errs = validator.validate_product(product)
            if is_valid:
                valid_count += 1
            else:
                error_count += 1
                errors.append(f"Linha {i}: {', '.join(errs)}")

        print(f"\n{'='*60}")
        print(f"Válidos: {valid_count}")
        print(f"Inválidos: {error_count}")
        print(f"{'='*60}\n")

        if errors and args.verbose:
            print("Erros encontrados:")
            for error in errors[:20]:  # Mostrar no máximo 20 erros
                print(f"  {error}")
            if len(errors) > 20:
                print(f"  ... e mais {len(errors) - 20} erros")

        return 0 if error_count == 0 else 1

    except Exception as e:
        print(f"Erro ao validar arquivo: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Sistema de Web Scraping para Preços HVAC',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Modo verbose (debug)')

    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Comando: search
    parser_search = subparsers.add_parser('search', help='Buscar produtos')
    parser_search.add_argument('query', help='Termo de busca')
    parser_search.add_argument('--max', type=int, default=10,
                              help='Número máximo de resultados (padrão: 10)')
    parser_search.add_argument('--scraper', default='exemplo',
                              help='Scraper a usar (padrão: exemplo)')
    parser_search.add_argument('--no-cache', action='store_true',
                              help='Não usar cache')
    parser_search.add_argument('--export', action='store_true',
                              help='Exportar resultados para CSV')
    parser_search.add_argument('--category', choices=['materiais', 'mao_de_obra', 'ferramentas', 'equipamentos'],
                              help='Exportar no formato do sistema (para dados_csv/)')
    parser_search.add_argument('--prefix', default=None,
                              help='Prefixo para códigos (ex: MAT_ML)')
    parser_search.add_argument('--stats', action='store_true',
                              help='Mostrar estatísticas')

    # Comando: url
    parser_url = subparsers.add_parser('url', help='Scrape de URL específica')
    parser_url.add_argument('url', help='URL do produto')
    parser_url.add_argument('--scraper', default='exemplo',
                           help='Scraper a usar (padrão: exemplo)')
    parser_url.add_argument('--no-cache', action='store_true',
                           help='Não usar cache')
    parser_url.add_argument('--export', action='store_true',
                           help='Exportar resultado para CSV')
    parser_url.add_argument('--category', choices=['materiais', 'mao_de_obra', 'ferramentas', 'equipamentos'],
                           help='Exportar no formato do sistema')
    parser_url.add_argument('--prefix', default=None,
                           help='Prefixo para códigos')

    # Comando: cache
    parser_cache = subparsers.add_parser('cache', help='Gerenciar cache')
    parser_cache.add_argument('--stats', action='store_true',
                             help='Mostrar estatísticas do cache')
    parser_cache.add_argument('--clear', action='store_true',
                             help='Limpar cache')
    parser_cache.add_argument('--expired', action='store_true',
                             help='Apenas caches expirados (com --clear)')

    # Comando: validate
    parser_validate = subparsers.add_parser('validate', help='Validar arquivo CSV')
    parser_validate.add_argument('file', help='Arquivo CSV para validar')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    setup_logging(args.verbose)

    # Executar comando
    if args.command == 'search':
        return cmd_search(args)
    elif args.command == 'url':
        return cmd_url(args)
    elif args.command == 'cache':
        return cmd_cache(args)
    elif args.command == 'validate':
        return cmd_validate(args)


if __name__ == '__main__':
    sys.exit(main())

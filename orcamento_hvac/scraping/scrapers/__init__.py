"""
Scrapers específicos por site.

Scrapers disponíveis:
- ExemploScraper: Template para criar novos scrapers
- JsonLdScraper: Scraper genérico baseado em JSON-LD/Schema.org
- MercadoLivreScraper: Scraper para Mercado Livre Brasil
"""

from .exemplo_scraper import ExemploScraper
from .jsonld_scraper import JsonLdScraper
from .mercadolivre_scraper import MercadoLivreScraper

__all__ = [
    'ExemploScraper',
    'JsonLdScraper',
    'MercadoLivreScraper',
]

# Mapeamento de nomes para classes (para uso no CLI)
SCRAPERS = {
    'exemplo': ExemploScraper,
    'jsonld': JsonLdScraper,
    'mercadolivre': MercadoLivreScraper,
    'ml': MercadoLivreScraper,  # Alias
}

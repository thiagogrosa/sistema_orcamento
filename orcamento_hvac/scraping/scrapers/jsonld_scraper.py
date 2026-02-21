"""
Scraper genérico baseado em JSON-LD / Schema.org.

Este scraper funciona com a maioria dos sites de e-commerce modernos que
implementam dados estruturados (schema.org/Product). É uma boa primeira
tentativa antes de criar scrapers específicos.

Funciona bem com:
- Shopify stores
- WooCommerce
- Magento
- VTEX (muito usado no Brasil)
- E outros que implementam schema.org
"""
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, quote, urlparse

from bs4 import BeautifulSoup
from ..base_scraper import BaseScraper


class JsonLdScraper(BaseScraper):
    """
    Scraper que extrai dados de marcação JSON-LD (schema.org/Product).

    Este é o método mais confiável para sites modernos, pois os dados
    estruturados seguem um padrão bem definido.
    """

    def __init__(self, use_cache: bool = True):
        super().__init__(name='jsonld', use_cache=use_cache)

    def _extract_jsonld(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extrai todos os blocos JSON-LD de uma página.

        Returns:
            Lista de objetos JSON-LD encontrados
        """
        scripts = soup.find_all('script', type='application/ld+json')
        data = []

        for script in scripts:
            try:
                content = script.string
                if content:
                    parsed = json.loads(content)
                    # Pode ser objeto único ou array
                    if isinstance(parsed, list):
                        data.extend(parsed)
                    else:
                        data.append(parsed)
            except (json.JSONDecodeError, TypeError):
                continue

        return data

    def _find_product_data(self, jsonld_list: List[Dict]) -> Optional[Dict]:
        """
        Encontra dados de produto nos blocos JSON-LD.

        Procura por objetos com @type "Product" ou "ProductGroup".
        """
        for item in jsonld_list:
            # Verificar tipo diretamente
            item_type = item.get('@type', '')
            if isinstance(item_type, list):
                item_type = item_type[0] if item_type else ''

            if item_type in ('Product', 'ProductGroup'):
                return item

            # Verificar em @graph (comum em WordPress/Yoast)
            if '@graph' in item:
                for graph_item in item['@graph']:
                    graph_type = graph_item.get('@type', '')
                    if isinstance(graph_type, list):
                        graph_type = graph_type[0] if graph_type else ''
                    if graph_type in ('Product', 'ProductGroup'):
                        return graph_item

        return None

    def _extract_price_from_offers(self, offers: Any) -> Optional[float]:
        """Extrai preço de offers (pode ser objeto ou array)."""
        if not offers:
            return None

        # Se é array, pegar primeira oferta
        if isinstance(offers, list):
            offers = offers[0] if offers else None

        if not offers:
            return None

        # Tentar diferentes campos de preço
        price = offers.get('price') or offers.get('lowPrice') or offers.get('highPrice')

        if price is not None:
            try:
                return float(price)
            except (ValueError, TypeError):
                pass

        return None

    def extract_product_info(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai informações de produto usando JSON-LD.
        """
        try:
            jsonld_data = self._extract_jsonld(soup)
            product_data = self._find_product_data(jsonld_data)

            if not product_data:
                self.logger.warning(f"JSON-LD Product não encontrado em {url}")
                return None

            # Extrair nome
            name = product_data.get('name')
            if not name:
                self.logger.warning(f"Nome não encontrado em JSON-LD: {url}")
                return None

            # Extrair preço
            offers = product_data.get('offers')
            price = self._extract_price_from_offers(offers)

            if price is None:
                self.logger.warning(f"Preço não encontrado em JSON-LD: {url}")
                return None

            # Extrair fonte (domínio)
            domain = urlparse(url).netloc.replace('www.', '')
            source = domain.split('.')[0].title()

            # Montar produto
            product = {
                'name': name[:200] if name else 'N/A',
                'price': price,
                'url': url,
                'source': source,
                'scraped_at': datetime.now().isoformat(),
            }

            # Campos opcionais
            if 'description' in product_data:
                product['description'] = product_data['description'][:500]

            if 'sku' in product_data:
                product['sku'] = product_data['sku']

            if 'image' in product_data:
                img = product_data['image']
                if isinstance(img, list):
                    img = img[0] if img else None
                if isinstance(img, dict):
                    img = img.get('url') or img.get('@id')
                product['image_url'] = img

            if 'brand' in product_data:
                brand = product_data['brand']
                if isinstance(brand, dict):
                    brand = brand.get('name')
                product['brand'] = brand

            # Disponibilidade
            if offers:
                if isinstance(offers, list):
                    offers = offers[0]
                availability = offers.get('availability', '')
                product['in_stock'] = 'InStock' in str(availability)

            return product

        except Exception as e:
            self.logger.error(f"Erro ao extrair JSON-LD de {url}: {e}")
            return None

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Busca não implementada para scraper genérico.

        Este scraper é usado principalmente para URLs diretas de produtos.
        Para busca, use um scraper específico do site ou forneça URLs.
        """
        self.logger.warning("JsonLdScraper não implementa busca. Use URLs diretas.")
        return []

    def scrape_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape múltiplas URLs de produtos.

        Args:
            urls: Lista de URLs de produtos

        Returns:
            Lista de produtos extraídos com sucesso
        """
        results = []

        for url in urls:
            product = self.scrape_url(url)
            if product:
                results.append(product)

        return results

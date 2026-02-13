"""
Scraper de exemplo/template.

Este é um template que demonstra como criar scrapers específicos.
Para criar um novo scraper:
1. Copie este arquivo
2. Renomeie para o site alvo (ex: leroy_scraper.py)
3. Implemente os métodos extract_product_info e search
4. Ajuste BASE_URL e SEARCH_URL
"""
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, quote

from bs4 import BeautifulSoup
from ..base_scraper import BaseScraper


class ExemploScraper(BaseScraper):
    """
    Scraper de exemplo.

    Demonstra a estrutura básica que todos os scrapers devem seguir.
    """

    # URLs base do site
    BASE_URL = "https://www.exemplo.com.br"
    SEARCH_URL = "https://www.exemplo.com.br/busca?q={query}"

    def __init__(self, use_cache: bool = True):
        super().__init__(name='exemplo', use_cache=use_cache)

    def extract_product_info(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai informações de produto de uma página.

        IMPORTANTE: Ajuste os seletores CSS para o site específico.
        Use o DevTools do navegador para identificar os seletores corretos.
        """
        try:
            # Exemplo de extração - AJUSTAR PARA SITE ESPECÍFICO

            # Nome do produto (buscar por classes comuns)
            name_elem = soup.select_one('.product-name, .product-title, h1[itemprop="name"]')
            if not name_elem:
                self.logger.warning(f"Nome não encontrado em {url}")
                return None
            name = name_elem.get_text(strip=True)

            # Preço (buscar por classes comuns)
            price_elem = soup.select_one(
                '.price, .product-price, [itemprop="price"], .sale-price'
            )
            if not price_elem:
                self.logger.warning(f"Preço não encontrado em {url}")
                return None

            price_text = price_elem.get_text(strip=True)
            price = self.validator.clean_price_string(price_text)

            if price is None:
                self.logger.warning(f"Preço inválido: {price_text}")
                return None

            # Imagem (opcional)
            image_elem = soup.select_one('.product-image img, [itemprop="image"]')
            image_url = None
            if image_elem:
                image_url = image_elem.get('src') or image_elem.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(self.BASE_URL, image_url)

            # SKU/Código (opcional)
            sku_elem = soup.select_one('[itemprop="sku"], .product-code')
            sku = sku_elem.get_text(strip=True) if sku_elem else None

            # Disponibilidade (opcional)
            availability_elem = soup.select_one('.availability, [itemprop="availability"]')
            in_stock = True
            if availability_elem:
                availability_text = availability_elem.get_text(strip=True).lower()
                in_stock = 'disponível' in availability_text or 'estoque' in availability_text

            # Montar produto
            product = {
                'name': name,
                'price': price,
                'url': url,
                'source': 'Exemplo',
                'scraped_at': datetime.now().isoformat(),
                'image_url': image_url,
                'sku': sku,
                'in_stock': in_stock
            }

            return product

        except Exception as e:
            self.logger.error(f"Erro ao extrair produto de {url}: {e}")
            return None

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Busca produtos por termo.

        IMPORTANTE: Ajustar para estrutura de busca do site específico.
        """
        results = []

        try:
            # Montar URL de busca
            search_url = self.SEARCH_URL.format(query=quote(query))
            self.logger.info(f"Buscando: {query}")

            # Buscar página de resultados
            html = self.fetch(search_url)
            if not html:
                return results

            soup = self.parse_html(html)

            # Encontrar links de produtos - AJUSTAR SELETORES
            product_links = soup.select('.product-item a, .product-link, .item-link')[:max_results]

            for link in product_links:
                href = link.get('href')
                if not href:
                    continue

                # Construir URL absoluta
                product_url = urljoin(self.BASE_URL, href)

                # Scrape do produto
                product = self.scrape_url(product_url)
                if product:
                    results.append(product)

                if len(results) >= max_results:
                    break

            self.logger.info(f"Encontrados {len(results)} produtos para '{query}'")

        except Exception as e:
            self.logger.error(f"Erro na busca por '{query}': {e}")

        return results

    def get_category(self, category_url: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Busca produtos de uma categoria específica.

        Args:
            category_url: URL da categoria
            max_results: Número máximo de produtos

        Returns:
            Lista de produtos
        """
        results = []

        try:
            html = self.fetch(category_url)
            if not html:
                return results

            soup = self.parse_html(html)

            # Encontrar links de produtos
            product_links = soup.select('.product-item a, .product-link')[:max_results]

            for link in product_links:
                href = link.get('href')
                if not href:
                    continue

                product_url = urljoin(self.BASE_URL, href)
                product = self.scrape_url(product_url)

                if product:
                    results.append(product)

                if len(results) >= max_results:
                    break

        except Exception as e:
            self.logger.error(f"Erro ao buscar categoria {category_url}: {e}")

        return results

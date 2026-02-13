"""
Scraper para Mercado Livre Brasil.

O Mercado Livre é uma das maiores plataformas de e-commerce do Brasil
e é muito usado para compra de materiais e equipamentos HVAC.

NOTA: Este scraper é para uso educacional e pesquisa de preços.
Respeite os termos de uso do Mercado Livre e os rate limits.
"""
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, quote

from bs4 import BeautifulSoup
from ..base_scraper import BaseScraper


class MercadoLivreScraper(BaseScraper):
    """
    Scraper para Mercado Livre Brasil.

    Extrai informações de produtos a partir de páginas de busca
    e páginas individuais de produtos.
    """

    BASE_URL = "https://www.mercadolivre.com.br"
    SEARCH_URL = "https://lista.mercadolivre.com.br/{query}"

    # Categorias HVAC comuns
    HVAC_CATEGORIES = {
        'ar_condicionado': 'ar-condicionado-split',
        'tubo_cobre': 'tubo-cobre-refrigeracao',
        'bomba_vacuo': 'bomba-vacuo-refrigeracao',
        'gas_refrigerante': 'gas-refrigerante',
        'isolamento': 'isolamento-termico',
    }

    def __init__(self, use_cache: bool = True):
        super().__init__(name='mercadolivre', use_cache=use_cache)

    def _clean_price(self, price_text: str) -> Optional[float]:
        """Limpa string de preço do ML."""
        if not price_text:
            return None

        # Remover "R$", pontos de milhar, trocar vírgula por ponto
        price_text = price_text.replace('R$', '').strip()
        price_text = price_text.replace('.', '').replace(',', '.')

        # Extrair apenas números e ponto decimal
        match = re.search(r'[\d]+(?:\.[\d]{1,2})?', price_text)
        if match:
            try:
                return float(match.group())
            except ValueError:
                pass

        return None

    def extract_product_info(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai informações de produto de uma página do ML.
        """
        try:
            # Nome do produto
            name_elem = (
                soup.select_one('h1.ui-pdp-title') or
                soup.select_one('.item-title__primary') or
                soup.select_one('[data-testid="pdp-title"]')
            )
            if not name_elem:
                self.logger.warning(f"Nome não encontrado em {url}")
                return None

            name = name_elem.get_text(strip=True)

            # Preço - várias tentativas de seletores
            price = None

            # Tentar preço principal
            price_elem = (
                soup.select_one('.andes-money-amount__fraction') or
                soup.select_one('.price-tag-fraction') or
                soup.select_one('[data-testid="price-part"]')
            )

            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Verificar centavos
                cents_elem = soup.select_one('.andes-money-amount__cents')
                if cents_elem:
                    price_text += ',' + cents_elem.get_text(strip=True)
                price = self._clean_price(price_text)

            # Tentar meta tag
            if price is None:
                meta_price = soup.select_one('meta[itemprop="price"]')
                if meta_price:
                    price = self._clean_price(meta_price.get('content', ''))

            if price is None:
                self.logger.warning(f"Preço não encontrado em {url}")
                return None

            # Imagem
            image_url = None
            img_elem = (
                soup.select_one('.ui-pdp-image') or
                soup.select_one('.gallery-image')
            )
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src')

            # Vendedor
            seller = None
            seller_elem = soup.select_one('.ui-pdp-seller__link-trigger')
            if seller_elem:
                seller = seller_elem.get_text(strip=True)

            # Disponibilidade
            in_stock = True
            stock_elem = soup.select_one('.ui-pdp-stock-information')
            if stock_elem:
                stock_text = stock_elem.get_text(strip=True).lower()
                in_stock = 'esgotado' not in stock_text and 'indisponível' not in stock_text

            # Montar produto
            product = {
                'name': name[:200],
                'price': price,
                'url': url,
                'source': 'MercadoLivre',
                'scraped_at': datetime.now().isoformat(),
                'in_stock': in_stock,
            }

            if image_url:
                product['image_url'] = image_url
            if seller:
                product['seller'] = seller

            return product

        except Exception as e:
            self.logger.error(f"Erro ao extrair produto ML de {url}: {e}")
            return None

    def _extract_search_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extrai produtos diretamente da página de busca (mais eficiente).
        """
        products = []

        # Selecionar itens de resultado
        items = soup.select('.ui-search-result, .ui-search-layout__item')

        for item in items:
            try:
                # Link do produto
                link_elem = item.select_one('a.ui-search-link, a.ui-search-item__group__element')
                if not link_elem:
                    continue

                url = link_elem.get('href', '')
                if not url or '/produto/' not in url.lower() and '/MLB' not in url:
                    # Pode ser um link de categoria, pular
                    continue

                # Nome
                name_elem = item.select_one('.ui-search-item__title, .ui-search-item__group__element')
                if not name_elem:
                    continue
                name = name_elem.get_text(strip=True)

                # Preço
                price_elem = item.select_one('.andes-money-amount__fraction, .price-tag-fraction')
                if not price_elem:
                    continue

                price_text = price_elem.get_text(strip=True)
                cents_elem = item.select_one('.andes-money-amount__cents')
                if cents_elem:
                    price_text += ',' + cents_elem.get_text(strip=True)

                price = self._clean_price(price_text)
                if price is None:
                    continue

                # Imagem (opcional)
                image_url = None
                img_elem = item.select_one('img.ui-search-result-image__element')
                if img_elem:
                    image_url = img_elem.get('data-src') or img_elem.get('src')

                product = {
                    'name': name[:200],
                    'price': price,
                    'url': url,
                    'source': 'MercadoLivre',
                    'scraped_at': datetime.now().isoformat(),
                }

                if image_url:
                    product['image_url'] = image_url

                products.append(product)

            except Exception as e:
                self.logger.debug(f"Erro ao extrair item de busca: {e}")
                continue

        return products

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Busca produtos no Mercado Livre.

        Args:
            query: Termo de busca
            max_results: Número máximo de resultados

        Returns:
            Lista de produtos encontrados
        """
        results = []

        try:
            # Formatar query para URL (substituir espaços por hífens)
            query_formatted = query.replace(' ', '-')
            search_url = self.SEARCH_URL.format(query=quote(query_formatted))

            self.logger.info(f"Buscando ML: {query}")

            html = self.fetch(search_url)
            if not html:
                return results

            soup = self.parse_html(html)

            # Tentar extração direta da página de busca (mais rápido)
            results = self._extract_search_results(soup)

            # Limitar resultados
            results = results[:max_results]

            # Validar produtos
            valid_results = []
            for product in results:
                is_valid, _ = self.validator.validate_product(product)
                if is_valid:
                    valid_results.append(product)
                    self.stats['products_valid'] += 1

            self.stats['products_found'] += len(results)
            self.logger.info(f"Encontrados {len(valid_results)} produtos válidos para '{query}'")

            return valid_results

        except Exception as e:
            self.logger.error(f"Erro na busca ML por '{query}': {e}")
            return results

    def search_category(self, category: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Busca produtos por categoria HVAC pré-definida.

        Args:
            category: Chave da categoria (ar_condicionado, tubo_cobre, etc.)
            max_results: Número máximo de resultados

        Returns:
            Lista de produtos
        """
        if category not in self.HVAC_CATEGORIES:
            self.logger.error(f"Categoria desconhecida: {category}")
            self.logger.info(f"Categorias disponíveis: {list(self.HVAC_CATEGORIES.keys())}")
            return []

        search_term = self.HVAC_CATEGORIES[category]
        return self.search(search_term, max_results)

"""
Classe base para scrapers de sites de e-commerce.
"""
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .config import (
    DEFAULT_HEADERS, REQUEST_DELAY_SECONDS, MAX_RETRIES,
    TIMEOUT_SECONDS, LOGS_DIR
)
from .cache_manager import CacheManager
from .validator import DataValidator


class BaseScraper(ABC):
    """Classe base abstrata para scrapers."""

    def __init__(self, name: str, use_cache: bool = True):
        """
        Args:
            name: Nome identificador do scraper
            use_cache: Se deve usar cache de requisições
        """
        self.name = name
        self.use_cache = use_cache
        self.cache = CacheManager() if use_cache else None
        self.validator = DataValidator()
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        # Configurar logging
        self.logger = logging.getLogger(f"scraper.{name}")
        self._setup_logging()

        # Estatísticas
        self.stats = {
            'requests': 0,
            'cache_hits': 0,
            'errors': 0,
            'products_found': 0,
            'products_valid': 0
        }

    def _setup_logging(self):
        """Configura logging para o scraper."""
        import os
        os.makedirs(LOGS_DIR, exist_ok=True)

        handler = logging.FileHandler(
            os.path.join(LOGS_DIR, f'{self.name}.log'),
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def fetch(self, url: str, use_cache: bool = True) -> Optional[str]:
        """
        Busca conteúdo HTML de uma URL com cache e retry.

        Args:
            url: URL para buscar
            use_cache: Se deve usar cache

        Returns:
            HTML content ou None se erro
        """
        # Validar URL
        is_valid, error = self.validator.validate_url(url)
        if not is_valid:
            self.logger.error(f"URL inválida: {error}")
            return None

        # Tentar cache primeiro
        if use_cache and self.cache:
            cached = self.cache.get(url, self.name)
            if cached:
                self.stats['cache_hits'] += 1
                self.logger.info(f"Cache hit: {url}")
                return cached['data'].get('html')

        # Fazer requisição com retry
        for attempt in range(MAX_RETRIES):
            try:
                self.logger.info(f"Fetching {url} (attempt {attempt + 1}/{MAX_RETRIES})")

                response = self.session.get(
                    url,
                    timeout=TIMEOUT_SECONDS,
                    allow_redirects=True
                )
                response.raise_for_status()

                html = response.text
                self.stats['requests'] += 1

                # Salvar em cache
                if self.cache:
                    self.cache.set(url, self.name, {'html': html})

                # Rate limiting
                time.sleep(REQUEST_DELAY_SECONDS)

                return html

            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                self.stats['errors'] += 1

                if attempt < MAX_RETRIES - 1:
                    time.sleep(REQUEST_DELAY_SECONDS * (attempt + 1))
                else:
                    self.logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Converte HTML em objeto BeautifulSoup."""
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def extract_product_info(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai informações de produto de uma página.

        Deve retornar dict com:
        - name: str
        - price: float
        - url: str
        - scraped_at: str (ISO format)
        - source: str (nome do site)
        - additional fields (opcional)

        Args:
            soup: BeautifulSoup da página
            url: URL da página

        Returns:
            Dict com informações ou None se erro
        """
        pass

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Busca produtos por termo de pesquisa.

        Args:
            query: Termo de busca
            max_results: Número máximo de resultados

        Returns:
            Lista de dicts com informações de produtos
        """
        pass

    def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape completo de uma URL.

        Args:
            url: URL do produto

        Returns:
            Dict com informações ou None se erro
        """
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)
        product = self.extract_product_info(soup, url)

        if not product:
            return None

        # Validar produto
        is_valid, errors = self.validator.validate_product(product)
        if not is_valid:
            self.logger.error(f"Produto inválido: {errors}")
            return None

        self.stats['products_found'] += 1
        self.stats['products_valid'] += 1

        return product

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do scraper."""
        stats = self.stats.copy()

        if stats['requests'] > 0:
            stats['cache_hit_rate'] = stats['cache_hits'] / (stats['requests'] + stats['cache_hits'])
            stats['error_rate'] = stats['errors'] / stats['requests']
        else:
            stats['cache_hit_rate'] = 0
            stats['error_rate'] = 0

        if stats['products_found'] > 0:
            stats['validation_rate'] = stats['products_valid'] / stats['products_found']
        else:
            stats['validation_rate'] = 0

        return stats

    def reset_stats(self):
        """Reseta estatísticas."""
        self.stats = {k: 0 for k in self.stats}

    def close(self):
        """Fecha sessão HTTP."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

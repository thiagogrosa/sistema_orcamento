"""
Validação de dados coletados por scraping.
"""
import re
from typing import List, Dict, Any, Optional
from statistics import mean, stdev

from .config import PRICE_MIN, PRICE_MAX, OUTLIER_FACTOR


class DataValidator:
    """Valida dados coletados por scrapers."""

    @staticmethod
    def validate_price(price: float) -> tuple[bool, Optional[str]]:
        """
        Valida se um preço está dentro dos limites aceitáveis.

        Returns:
            (is_valid, error_message)
        """
        if not isinstance(price, (int, float)):
            return False, "Preço deve ser numérico"

        if price < PRICE_MIN:
            return False, f"Preço muito baixo (mínimo: R$ {PRICE_MIN:.2f})"

        if price > PRICE_MAX:
            return False, f"Preço muito alto (máximo: R$ {PRICE_MAX:.2f})"

        return True, None

    @staticmethod
    def validate_url(url: str) -> tuple[bool, Optional[str]]:
        """Valida formato de URL."""
        if not isinstance(url, str):
            return False, "URL deve ser string"

        # Regex básico para validar URL
        url_pattern = re.compile(
            r'^https?://'  # http:// ou https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # porta opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if not url_pattern.match(url):
            return False, "Formato de URL inválido"

        return True, None

    @staticmethod
    def validate_product(product: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valida estrutura completa de produto.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Campos obrigatórios
        required_fields = ['name', 'price', 'url', 'scraped_at']
        for field in required_fields:
            if field not in product:
                errors.append(f"Campo obrigatório ausente: {field}")

        # Validar preço
        if 'price' in product:
            is_valid, error = DataValidator.validate_price(product['price'])
            if not is_valid:
                errors.append(error)

        # Validar URL
        if 'url' in product:
            is_valid, error = DataValidator.validate_url(product['url'])
            if not is_valid:
                errors.append(error)

        # Validar nome
        if 'name' in product and not product['name'].strip():
            errors.append("Nome do produto vazio")

        return len(errors) == 0, errors

    @staticmethod
    def detect_outliers(prices: List[float], factor: float = OUTLIER_FACTOR) -> List[int]:
        """
        Detecta outliers em lista de preços usando desvio padrão.

        Args:
            prices: Lista de preços
            factor: Número de desvios padrão para considerar outlier

        Returns:
            Índices dos outliers detectados
        """
        if len(prices) < 3:
            return []  # Precisa de pelo menos 3 valores

        avg = mean(prices)
        std = stdev(prices)

        if std == 0:
            return []  # Todos os valores são iguais

        outliers = []
        for i, price in enumerate(prices):
            z_score = abs((price - avg) / std)
            if z_score > factor:
                outliers.append(i)

        return outliers

    @staticmethod
    def clean_price_string(price_str: str) -> Optional[float]:
        """
        Limpa string de preço e converte para float.

        Exemplos:
            "R$ 1.234,56" -> 1234.56
            "1234.56" -> 1234.56
            "R$1.234,56 à vista" -> 1234.56
        """
        if not isinstance(price_str, str):
            return None

        # Remove tudo exceto dígitos, vírgula e ponto
        cleaned = re.sub(r'[^\d,.]', '', price_str)

        if not cleaned:
            return None

        # Determinar se usa vírgula ou ponto como decimal
        # Formato brasileiro: 1.234,56
        # Formato internacional: 1,234.56

        if ',' in cleaned and '.' in cleaned:
            # Ambos presentes - determinar qual é decimal
            last_comma = cleaned.rfind(',')
            last_dot = cleaned.rfind('.')

            if last_comma > last_dot:
                # Formato brasileiro
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                # Formato internacional
                cleaned = cleaned.replace(',', '')

        elif ',' in cleaned:
            # Apenas vírgula - assumir formato brasileiro
            cleaned = cleaned.replace(',', '.')

        # else: apenas ponto ou nenhum - já está correto

        try:
            price = float(cleaned)
            return price if price > 0 else None
        except ValueError:
            return None

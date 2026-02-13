"""
Testes para o módulo de validação do scraping.
"""
import pytest
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scraping.validator import DataValidator


class TestValidatePrice:
    """Testes para validação de preços."""

    def test_valid_price(self):
        """Preço válido deve passar."""
        is_valid, error = DataValidator.validate_price(100.0)
        assert is_valid is True
        assert error is None

    def test_price_too_low(self):
        """Preço abaixo do mínimo deve falhar."""
        is_valid, error = DataValidator.validate_price(0.5)
        assert is_valid is False
        assert "muito baixo" in error

    def test_price_too_high(self):
        """Preço acima do máximo deve falhar."""
        is_valid, error = DataValidator.validate_price(100000.0)
        assert is_valid is False
        assert "muito alto" in error

    def test_price_not_numeric(self):
        """Preço não numérico deve falhar."""
        is_valid, error = DataValidator.validate_price("100")
        assert is_valid is False
        assert "numérico" in error

    def test_price_at_limits(self):
        """Preço nos limites deve passar."""
        # Mínimo
        is_valid, _ = DataValidator.validate_price(1.0)
        assert is_valid is True

        # Máximo
        is_valid, _ = DataValidator.validate_price(50000.0)
        assert is_valid is True


class TestValidateUrl:
    """Testes para validação de URLs."""

    def test_valid_http_url(self):
        """URL HTTP válida deve passar."""
        is_valid, error = DataValidator.validate_url("http://example.com/product")
        assert is_valid is True
        assert error is None

    def test_valid_https_url(self):
        """URL HTTPS válida deve passar."""
        is_valid, error = DataValidator.validate_url("https://www.example.com/product?id=123")
        assert is_valid is True

    def test_invalid_url_no_protocol(self):
        """URL sem protocolo deve falhar."""
        is_valid, error = DataValidator.validate_url("www.example.com")
        assert is_valid is False

    def test_invalid_url_not_string(self):
        """URL não string deve falhar."""
        is_valid, error = DataValidator.validate_url(123)
        assert is_valid is False
        assert "string" in error


class TestValidateProduct:
    """Testes para validação de produto completo."""

    def test_valid_product(self):
        """Produto válido deve passar."""
        product = {
            'name': 'Tubo de Cobre 1/4"',
            'price': 18.00,
            'url': 'https://example.com/tubo',
            'scraped_at': '2025-12-30T10:00:00'
        }
        is_valid, errors = DataValidator.validate_product(product)
        assert is_valid is True
        assert len(errors) == 0

    def test_missing_required_field(self):
        """Produto sem campo obrigatório deve falhar."""
        product = {
            'name': 'Tubo de Cobre',
            'price': 18.00,
            # 'url' faltando
            'scraped_at': '2025-12-30T10:00:00'
        }
        is_valid, errors = DataValidator.validate_product(product)
        assert is_valid is False
        assert any('url' in e.lower() for e in errors)

    def test_empty_name(self):
        """Produto com nome vazio deve falhar."""
        product = {
            'name': '   ',
            'price': 18.00,
            'url': 'https://example.com/tubo',
            'scraped_at': '2025-12-30T10:00:00'
        }
        is_valid, errors = DataValidator.validate_product(product)
        assert is_valid is False
        assert any('vazio' in e.lower() for e in errors)


class TestCleanPriceString:
    """Testes para limpeza de strings de preço."""

    def test_brazilian_format(self):
        """Formato brasileiro R$ 1.234,56 deve funcionar."""
        assert DataValidator.clean_price_string("R$ 1.234,56") == 1234.56

    def test_brazilian_format_simple(self):
        """Formato brasileiro simples R$ 100,00 deve funcionar."""
        assert DataValidator.clean_price_string("R$ 100,00") == 100.00

    def test_international_format(self):
        """Formato internacional 1,234.56 deve funcionar."""
        assert DataValidator.clean_price_string("1,234.56") == 1234.56

    def test_with_text(self):
        """Preço com texto deve extrair valor."""
        assert DataValidator.clean_price_string("R$ 99,90 à vista") == 99.90

    def test_no_cents(self):
        """Preço sem centavos deve funcionar."""
        assert DataValidator.clean_price_string("R$ 100") == 100.0

    def test_invalid_string(self):
        """String sem número deve retornar None."""
        assert DataValidator.clean_price_string("sem preço") is None

    def test_empty_string(self):
        """String vazia deve retornar None."""
        assert DataValidator.clean_price_string("") is None


class TestDetectOutliers:
    """Testes para detecção de outliers."""

    def test_no_outliers(self):
        """Lista sem outliers deve retornar vazia."""
        prices = [10.0, 11.0, 10.5, 10.8, 11.2]
        outliers = DataValidator.detect_outliers(prices)
        assert len(outliers) == 0

    def test_with_outlier_with_custom_factor(self):
        """Lista com outlier deve detectar com fator mais sensível."""
        prices = [10.0, 11.0, 10.5, 100.0, 10.8]  # 100.0 é outlier
        outliers = DataValidator.detect_outliers(prices, factor=1.5)
        assert 3 in outliers

    def test_with_outlier_default_factor(self):
        """No fator padrão (3.0), a amostra curta não acusa outlier."""
        prices = [10.0, 11.0, 10.5, 100.0, 10.8]
        outliers = DataValidator.detect_outliers(prices)
        assert len(outliers) == 0

    def test_insufficient_data(self):
        """Menos de 3 valores deve retornar vazia."""
        prices = [10.0, 11.0]
        outliers = DataValidator.detect_outliers(prices)
        assert len(outliers) == 0

    def test_all_same(self):
        """Todos valores iguais deve retornar vazia."""
        prices = [10.0, 10.0, 10.0, 10.0]
        outliers = DataValidator.detect_outliers(prices)
        assert len(outliers) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

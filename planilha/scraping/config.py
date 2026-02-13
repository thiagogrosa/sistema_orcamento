"""
Configurações do sistema de web scraping.
"""
import os
from datetime import timedelta

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), 'dados_csv')

# Cache
CACHE_EXPIRY_HOURS = 24
CACHE_FORMAT = 'json'

# Rate Limiting
REQUEST_DELAY_SECONDS = 2  # Delay entre requisições
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Headers HTTP
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)

DEFAULT_HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Validação de preços
PRICE_MIN = 1.0  # Preço mínimo aceitável
PRICE_MAX = 50000.0  # Preço máximo aceitável
OUTLIER_FACTOR = 3.0  # Fator para detecção de outliers (desvio padrão)

# CSV Export
CSV_DELIMITER = ';'
CSV_ENCODING = 'utf-8-sig'

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

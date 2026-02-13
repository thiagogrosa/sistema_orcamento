# Sistema de Web Scraping para Preços HVAC

Sistema modular de web scraping para coleta automatizada de preços de materiais, equipamentos e peças de ar-condicionado.

## 🎯 Características

- **Arquitetura Modular**: Fácil adicionar novos scrapers para sites diferentes
- **Sistema de Cache**: Evita requisições repetidas (configurável)
- **Rate Limiting**: Respeita servidores com delays entre requisições
- **Validação de Dados**: Detecta preços inválidos e outliers
- **Exportação CSV**: Formato compatível com sistema de orçamentos
- **Logging Completo**: Rastreamento de todas as operações
- **CLI Intuitivo**: Interface de linha de comando fácil de usar

## 📁 Estrutura

```
scraping/
├── __init__.py              # Módulo principal
├── config.py                # Configurações globais
├── base_scraper.py          # Classe base para scrapers
├── cache_manager.py         # Gerenciamento de cache
├── validator.py             # Validação de dados
├── exporter.py              # Exportação para CSV
├── README.md                # Este arquivo
├── scrapers/                # Scrapers específicos
│   ├── __init__.py
│   └── exemplo_scraper.py   # Template/exemplo
├── cache/                   # Cache de requisições (auto-gerado)
└── logs/                    # Logs de operação (auto-gerado)
```

## 🚀 Instalação

### Dependências

```bash
pip install requests beautifulsoup4
```

### Configuração

As configurações estão em `scraping/config.py`:

- `CACHE_EXPIRY_HOURS`: Validade do cache (padrão: 24h)
- `REQUEST_DELAY_SECONDS`: Delay entre requisições (padrão: 2s)
- `PRICE_MIN/MAX`: Limites de validação de preços
- `OUTLIER_FACTOR`: Fator para detecção de outliers

## 📖 Uso

### CLI - Interface de Linha de Comando

```bash
# Buscar produtos
python3 scraper_cli.py search "tubo cobre 1/4" --max 10

# Scrape de URL específica
python3 scraper_cli.py url https://exemplo.com/produto/123

# Buscar e exportar para CSV
python3 scraper_cli.py search "split 12k" --export

# Ver estatísticas do cache
python3 scraper_cli.py cache --stats

# Limpar cache expirado
python3 scraper_cli.py cache --clear --expired

# Limpar todo o cache
python3 scraper_cli.py cache --clear

# Validar arquivo CSV
python3 scraper_cli.py validate produtos.csv

# Modo verbose (debug)
python3 scraper_cli.py search "bomba vacuo" -v
```

### Python API

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper
from scraping.exporter import DataExporter

# Criar scraper
scraper = ExemploScraper(use_cache=True)

# Buscar produtos
produtos = scraper.search("compressor 12k", max_results=5)

# Scrape de URL específica
produto = scraper.scrape_url("https://exemplo.com/produto/123")

# Exportar para CSV
exporter = DataExporter()
filepath = exporter.export_products(produtos)
print(f"Exportado para: {filepath}")

# Ver estatísticas
stats = scraper.get_stats()
print(f"Requisições: {stats['requests']}")
print(f"Cache hits: {stats['cache_hits']}")

# Fechar scraper
scraper.close()
```

### Usando Context Manager (recomendado)

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper

with ExemploScraper() as scraper:
    produtos = scraper.search("sensor temperatura")
    print(f"Encontrados: {len(produtos)} produtos")
```

## 🛠️ Criando Novo Scraper

### Passo 1: Copiar Template

```bash
cd scraping/scrapers/
cp exemplo_scraper.py leroy_scraper.py
```

### Passo 2: Implementar Métodos

```python
from bs4 import BeautifulSoup
from ..base_scraper import BaseScraper

class LeroyScraper(BaseScraper):
    BASE_URL = "https://www.leroymerlin.com.br"
    SEARCH_URL = "https://www.leroymerlin.com.br/busca?q={query}"

    def __init__(self, use_cache: bool = True):
        super().__init__(name='leroy', use_cache=use_cache)

    def extract_product_info(self, soup: BeautifulSoup, url: str):
        """Extrai info do produto - AJUSTAR SELETORES"""
        name = soup.select_one('.product-title').get_text(strip=True)
        price_text = soup.select_one('.price-value').get_text(strip=True)
        price = self.validator.clean_price_string(price_text)

        return {
            'name': name,
            'price': price,
            'url': url,
            'source': 'Leroy Merlin',
            'scraped_at': datetime.now().isoformat()
        }

    def search(self, query: str, max_results: int = 10):
        """Busca produtos - AJUSTAR PARA O SITE"""
        # Implementar lógica de busca
        pass
```

### Passo 3: Identificar Seletores CSS

Use DevTools do navegador (F12):
1. Inspecione elemento desejado
2. Clique com botão direito → Copy → Copy selector
3. Simplifique o seletor se necessário

**Exemplos de seletores comuns:**
- Nome: `.product-name`, `.product-title`, `h1[itemprop="name"]`
- Preço: `.price`, `.product-price`, `[itemprop="price"]`
- Imagem: `.product-image img`, `[itemprop="image"]`
- Links: `.product-item a`, `.product-link`

### Passo 4: Testar

```bash
python3 scraper_cli.py search "teste" --scraper leroy -v
```

## 📊 Validação de Dados

### Validação Automática

O sistema valida automaticamente:
- ✅ Formato de URLs
- ✅ Preços dentro de limites (R$ 1 - R$ 50.000)
- ✅ Campos obrigatórios presentes
- ✅ Detecção de outliers (valores muito discrepantes)

### Validação Manual

```python
from scraping.validator import DataValidator

validator = DataValidator()

# Validar preço
is_valid, error = validator.validate_price(1234.56)

# Validar produto completo
product = {
    'name': 'Tubo Cobre',
    'price': 25.50,
    'url': 'https://...',
    'scraped_at': '2026-01-21'
}
is_valid, errors = validator.validate_product(product)

# Detectar outliers
prices = [10.0, 12.0, 11.5, 50.0, 13.0]
outliers = validator.detect_outliers(prices)
print(f"Outliers nos índices: {outliers}")  # [3]

# Limpar string de preço
price = validator.clean_price_string("R$ 1.234,56")
print(price)  # 1234.56
```

## 💾 Sistema de Cache

### Como Funciona

- Cache automático de todas as requisições HTTP
- Chave única baseada em URL + scraper
- Expiração configurável (padrão: 24 horas)
- Formato JSON com metadata

### Gerenciamento

```python
from scraping.cache_manager import CacheManager

cache = CacheManager()

# Obter estatísticas
stats = cache.get_stats()
print(f"Total: {stats['total_files']} arquivos")
print(f"Tamanho: {stats['total_size_mb']:.2f} MB")

# Limpar expirados
removed = cache.clear_expired(max_age_hours=48)
print(f"Removidos: {removed}")

# Limpar tudo
cache.clear_all()
```

## 📤 Exportação de Dados

### Formato Padrão

```python
from scraping.exporter import DataExporter

exporter = DataExporter()

# Exportar produtos (formato completo)
filepath = exporter.export_products(
    products=produtos,
    filename='compressores',
    include_timestamp=True
)
```

CSV gerado:
```csv
name;price;url;source;scraped_at;image_url;sku;in_stock
Compressor 12K;950.00;https://...;Leroy;2026-01-21T10:30:00;...;SKU123;True
```

### Formato para Importação

```python
# Formato compatível com sistema de orçamentos
filepath = exporter.export_to_import_format(
    products=produtos,
    category='materiais',  # ou 'equipamentos'
    validade_dias=30
)
```

CSV gerado (compatível com importação VBA):
```csv
CODIGO;CATEGORIA;DESCRICAO;UNIDADE;PRECO;ATUALIZADO_EM;VALIDADE_DIAS
MAT_SCRAPED_0001;Diversos;Compressor;UN;950.00;2026-01-21;30
```

### Histórico de Preços

```python
# Coletar ao longo do tempo
price_history = {
    'https://site.com/produto1': [
        {'name': 'Produto', 'price': 100.0, 'scraped_at': '2026-01-01'},
        {'name': 'Produto', 'price': 95.0, 'scraped_at': '2026-01-15'},
    ]
}

filepath = exporter.export_price_history(price_history)
```

## 🔧 Configurações Avançadas

### Rate Limiting Personalizado

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper
from scraping import config

# Ajustar delay global
config.REQUEST_DELAY_SECONDS = 5  # 5 segundos entre requisições

scraper = ExemploScraper()
```

### Headers Customizados

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper

scraper = ExemploScraper()
scraper.session.headers.update({
    'Custom-Header': 'Value',
    'Authorization': 'Bearer token'
})
```

### Timeout e Retries

Configurado em `config.py`:
```python
TIMEOUT_SECONDS = 30  # Timeout por requisição
MAX_RETRIES = 3       # Tentativas em caso de falha
```

## 📝 Logging

### Arquivos de Log

Cada scraper gera seu próprio arquivo:
- `scraping/logs/exemplo.log`
- `scraping/logs/leroy.log`

### Níveis de Log

- **INFO**: Operações normais (requisições, produtos encontrados)
- **WARNING**: Avisos (cache miss, campos não encontrados)
- **ERROR**: Erros (requisição falhou, validação falhou)

### Visualizar Logs

```bash
# Últimas 50 linhas
tail -n 50 scraping/logs/exemplo.log

# Seguir em tempo real
tail -f scraping/logs/exemplo.log

# Filtrar erros
grep ERROR scraping/logs/*.log
```

## ⚠️ Boas Práticas

### Respeite os Servidores

1. **Use cache sempre que possível** (padrão: 24h)
2. **Configure delay adequado** (mínimo: 2 segundos)
3. **Não faça scraping em massa** sem necessidade
4. **Respeite robots.txt** do site
5. **Use User-Agent identificável**

### Sites que Podem Bloquear

Alguns sites têm proteção anti-scraping:
- Captcha
- Rate limiting agressivo
- Bloqueio de IPs
- JavaScript obrigatório

**Soluções:**
- Usar APIs oficiais quando disponível
- Selenium/Playwright para sites com JavaScript
- Proxies rotativos (cuidado com legalidade)
- Respeitar ToS (Terms of Service)

### Legalidade

- ✅ Dados públicos geralmente são OK
- ✅ Uso pessoal/interno geralmente é OK
- ❌ Revenda de dados pode ser ilegal
- ❌ Violar ToS pode resultar em bloqueio
- ⚖️ Consulte advogado se houver dúvida

## 🐛 Troubleshooting

### Erro: "Nome não encontrado"

**Causa**: Seletor CSS incorreto

**Solução**:
1. Abra a página no navegador
2. Inspecione o elemento (F12)
3. Teste seletores no Console: `document.querySelector('.product-name')`
4. Atualize scraper com seletor correto

### Erro: "Preço inválido"

**Causa**: Formato de preço não reconhecido

**Solução**:
```python
# Ver o texto bruto
price_text = soup.select_one('.price').get_text(strip=True)
print(f"Preço bruto: {price_text}")

# Ajustar regex em validator.clean_price_string() se necessário
```

### Cache não funciona

**Verificar**:
```bash
ls -lh scraping/cache/
```

Se vazio, pode ser:
- `use_cache=False` no scraper
- Erros ao salvar cache (permissões)
- Cache sendo limpo automaticamente

### Site retorna HTML diferente

**Causa**: Site detectou scraper e retornou página diferente

**Soluções**:
1. Verificar User-Agent (usar navegador real)
2. Adicionar cookies de sessão
3. Usar Selenium para JavaScript

## 📚 Exemplos Completos

### Exemplo 1: Busca e Exportação

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper
from scraping.exporter import DataExporter

# Buscar tubos de cobre
with ExemploScraper() as scraper:
    tubos = scraper.search("tubo cobre", max_results=20)

    # Filtrar por preço
    tubos_filtrados = [t for t in tubos if t['price'] < 100.0]

    # Exportar
    exporter = DataExporter()
    filepath = exporter.export_to_import_format(
        products=tubos_filtrados,
        category='materiais',
        validade_dias=7  # Preços variam rápido
    )

    print(f"✓ {len(tubos_filtrados)} tubos exportados para {filepath}")
```

### Exemplo 2: Comparação de Preços

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper
# from scraping.scrapers.leroy_scraper import LeroyScraper  # quando implementado

query = "compressor 12k btu"
all_products = []

scrapers = [
    ExemploScraper(),
    # LeroyScraper(),
]

for scraper in scrapers:
    with scraper:
        products = scraper.search(query, max_results=5)
        all_products.extend(products)

# Agrupar por nome similar
from collections import defaultdict
by_name = defaultdict(list)
for product in all_products:
    # Simplificar nome para agrupamento
    simple_name = product['name'].lower()[:30]
    by_name[simple_name].append(product)

# Mostrar comparação
for name, products in by_name.items():
    if len(products) > 1:
        print(f"\n{name}:")
        for p in sorted(products, key=lambda x: x['price']):
            print(f"  R$ {p['price']:>8.2f} - {p['source']}")
```

### Exemplo 3: Monitoramento de Preço

```python
import json
from datetime import datetime
from scraping.scrapers.exemplo_scraper import ExemploScraper

# Arquivo de histórico
HISTORY_FILE = 'price_history.json'

# Carregar histórico
try:
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
except FileNotFoundError:
    history = {}

# URLs para monitorar
urls_to_monitor = [
    'https://exemplo.com/compressor-12k',
    'https://exemplo.com/bomba-vacuo',
]

with ExemploScraper() as scraper:
    for url in urls_to_monitor:
        product = scraper.scrape_url(url)

        if product:
            if url not in history:
                history[url] = []

            history[url].append({
                'price': product['price'],
                'date': datetime.now().isoformat()
            })

            # Verificar variação
            if len(history[url]) > 1:
                old_price = history[url][-2]['price']
                new_price = product['price']
                diff = ((new_price - old_price) / old_price) * 100

                if abs(diff) > 5:  # Variação > 5%
                    print(f"⚠️  {product['name']}")
                    print(f"   Variação: {diff:+.1f}%")
                    print(f"   Antigo: R$ {old_price:.2f}")
                    print(f"   Novo: R$ {new_price:.2f}")

# Salvar histórico
with open(HISTORY_FILE, 'w') as f:
    json.dump(history, f, indent=2)
```

## 🤝 Contribuindo

Para adicionar suporte a novos sites:

1. Copie `exemplo_scraper.py`
2. Implemente os métodos abstratos
3. Teste com o CLI
4. Documente seletores e peculiaridades
5. Adicione ao `__init__.py`

## 📄 Licença

Sistema interno - uso restrito ao projeto de orçamentos HVAC.

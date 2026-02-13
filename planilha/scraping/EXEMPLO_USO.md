# Exemplos de Uso - Sistema de Web Scraping

## 🚀 Guia Rápido de Início

### 1. Setup Inicial

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Verificar instalação
python3 scraper_cli.py cache --stats
```

### 2. Primeiro Teste

```bash
# Ajuda do CLI
python3 scraper_cli.py --help

# Ver estatísticas do cache (vazio inicialmente)
python3 scraper_cli.py cache --stats
```

## 📝 Exemplos Práticos

### Exemplo 1: Atualizar Preços de Materiais

```python
#!/usr/bin/env python3
from scraping.scrapers.exemplo_scraper import ExemploScraper
from scraping.exporter import DataExporter

tubos = ["tubo cobre 1/4", "tubo cobre 3/8", "tubo cobre 1/2"]
todos_produtos = []

with ExemploScraper() as scraper:
    for termo in tubos:
        produtos = scraper.search(termo, max_results=3)
        todos_produtos.extend(produtos)

if todos_produtos:
    exporter = DataExporter()
    filepath = exporter.export_to_import_format(
        products=todos_produtos,
        category='materiais',
        validade_dias=7
    )
    print(f"✓ Exportado: {filepath}")
```

### Exemplo 2: Monitorar Preço

```python
#!/usr/bin/env python3
import json
from datetime import datetime
from scraping.scrapers.exemplo_scraper import ExemploScraper

HISTORY_FILE = 'historico.json'
URL = 'https://exemplo.com/split-12k'

# Carregar histórico
try:
    with open(HISTORY_FILE, 'r') as f:
        hist = json.load(f)
except:
    hist = {}

with ExemploScraper() as scraper:
    produto = scraper.scrape_url(URL)

    if produto:
        preco_atual = produto['price']

        if URL in hist:
            preco_anterior = hist[URL]['preco']
            variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

            if abs(variacao) > 5:
                print(f"⚠️ Variação: {variacao:+.1f}%")

        hist[URL] = {
            'preco': preco_atual,
            'data': datetime.now().isoformat()
        }

with open(HISTORY_FILE, 'w') as f:
    json.dump(hist, f, indent=2)
```

### Exemplo 3: Comparar Fornecedores

```python
#!/usr/bin/env python3
from scraping.scrapers.exemplo_scraper import ExemploScraper
from statistics import mean

PRODUTO = "bomba de vacuo"

todos_precos = []
resultados = []

scrapers = [
    ('Exemplo', ExemploScraper()),
]

for nome, scraper in scrapers:
    with scraper:
        produtos = scraper.search(PRODUTO, max_results=3)

        for p in produtos:
            todos_precos.append(p['price'])
            resultados.append({
                'fonte': nome,
                'nome': p['name'],
                'preco': p['price']
            })

if todos_precos:
    print(f"Preço médio: R$ {mean(todos_precos):.2f}")
    print(f"Mínimo: R$ {min(todos_precos):.2f}")
    print(f"Máximo: R$ {max(todos_precos):.2f}")

    print("\nMelhores preços:")
    for r in sorted(resultados, key=lambda x: x['preco'])[:3]:
        print(f"  R$ {r['preco']:.2f} - {r['fonte']}")
```

## 🔧 Dicas

### Identificar Seletores CSS

```javascript
// Console do navegador (F12):
document.querySelector('.product-name')
document.querySelectorAll('.product-item')
```

### Debug de Scraper

```python
from scraping.scrapers.exemplo_scraper import ExemploScraper

scraper = ExemploScraper()
html = scraper.fetch('https://exemplo.com/produto')

# Salvar para análise
with open('/tmp/page.html', 'w') as f:
    f.write(html)

soup = scraper.parse_html(html)
print(soup.select_one('.product-name'))

scraper.close()
```

## 📅 Automação com Cron

```bash
# Executar diariamente às 2h
crontab -e

# Adicionar:
0 2 * * * cd /root/thiago/planilha && source venv/bin/activate && python3 scripts/atualizar_precos.py >> logs/cron.log 2>&1
```

## 🎓 Próximos Passos

1. Implementar scrapers reais para sites específicos
2. Testar em produção com buscas reais
3. Automatizar com cron
4. Monitorar logs regularmente
5. Expandir para mais sites

Consulte `scraping/README.md` para documentação completa.

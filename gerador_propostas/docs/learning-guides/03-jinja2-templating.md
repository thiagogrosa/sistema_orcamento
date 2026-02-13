# Jinja2 Templating Guide

**Purpose**: Learn how Jinja2 templates work and how data becomes HTML in this HVAC project.

---

## Table of Contents
1. [What is Jinja2?](#what-is-jinja2)
2. [Basic Syntax](#basic-syntax)
3. [Variables](#variables)
4. [Filters](#filters)
5. [Control Structures](#control-structures)
6. [Comments](#comments)
7. [Whitespace Control](#whitespace-control)
8. [Using Jinja2 in Python](#using-jinja2-in-python)
9. [Real Examples from This Project](#real-examples-from-this-project)
10. [Common Patterns](#common-patterns)

---

## What is Jinja2?

**Jinja2** is a template engine for Python.

**Think of it like**:
- A **mail merge** - You have a letter template with placeholders, and you fill them with actual data
- **Mad Libs** - A story with blanks that you fill in
- **HTML + Variables** - Write HTML once, fill with different data each time

**Example**:

**Template**:
```html
<h1>Hello, {{ name }}!</h1>
<p>You are {{ age }} years old.</p>
```

**Data** (Python dictionary):
```python
data = {"name": "João", "age": 30}
```

**Result**:
```html
<h1>Hello, João!</h1>
<p>You are 30 years old.</p>
```

---

## Basic Syntax

Jinja2 uses special delimiters to distinguish template code from regular HTML:

| Delimiter | Purpose | Example |
|-----------|---------|---------|
| `{{ }}` | **Output variable** | `{{ name }}` |
| `{% %}` | **Control statement** | `{% if active %}` |
| `{# #}` | **Comment** (not in output) | `{# TODO: fix #}` |

---

## Variables

### Simple Variables

**Template**:
```html
<h1>{{ titulo }}</h1>
<p>Cliente: {{ cliente }}</p>
<p>Valor: {{ valor }}</p>
```

**Python**:
```python
data = {
    "titulo": "Orçamento #1024",
    "cliente": "Grupo Panvel",
    "valor": 12500.50
}
```

**Output**:
```html
<h1>Orçamento #1024</h1>
<p>Cliente: Grupo Panvel</p>
<p>Valor: 12500.5</p>
```

### Accessing Dictionary Values

**Template**:
```html
<p>Empresa: {{ empresa.razao_social }}</p>
<p>CNPJ: {{ empresa.cnpj }}</p>
<p>Cidade: {{ empresa.endereco.cidade }}</p>
```

**Python**:
```python
data = {
    "empresa": {
        "razao_social": "ARMANT LTDA",
        "cnpj": "13.591.585/0001-03",
        "endereco": {
            "cidade": "Porto Alegre"
        }
    }
}
```

**Output**:
```html
<p>Empresa: ARMANT LTDA</p>
<p>CNPJ: 13.591.585/0001-03</p>
<p>Cidade: Porto Alegre</p>
```

**From your code** (`templates/html/proposta_base.html:49-51`):
```html
<span class="rodape-empresa">{{ empresa.razao_social }}</span>
<span class="separador">|</span>
<span>CNPJ: {{ empresa.cnpj }}</span>
```

### Accessing List Items

**Template**:
```html
<p>Primeiro item: {{ itens[0] }}</p>
<p>Segundo item: {{ itens[1] }}</p>
```

**Python**:
```python
data = {
    "itens": ["Tubo", "Cabo", "Fita"]
}
```

**Output**:
```html
<p>Primeiro item: Tubo</p>
<p>Segundo item: Cabo</p>
```

---

## Filters

Filters modify variables. Use the pipe symbol `|`.

### Common Filters

**Template**:
```html
<!-- String manipulation -->
<p>{{ name | upper }}</p>           <!-- JOÃO -->
<p>{{ name | lower }}</p>           <!-- joão -->
<p>{{ name | title }}</p>           <!-- João Silva -->
<p>{{ name | capitalize }}</p>      <!-- João silva -->

<!-- Numbers -->
<p>{{ price | round(2) }}</p>       <!-- 12.35 -->
<p>{{ price | int }}</p>            <!-- 12 -->

<!-- Default values -->
<p>{{ nota | default("Sem notas") }}</p>  <!-- If nota is None/empty -->

<!-- Length -->
<p>Total: {{ itens | length }} itens</p>

<!-- Join -->
<p>{{ categorias | join(", ") }}</p>      <!-- "A, B, C" -->
```

### Built-in Filters Reference

| Filter | Purpose | Example | Result |
|--------|---------|---------|--------|
| `upper` | Uppercase | `{{ "text" \| upper }}` | `TEXT` |
| `lower` | Lowercase | `{{ "TEXT" \| lower }}` | `text` |
| `title` | Title Case | `{{ "hello world" \| title }}` | `Hello World` |
| `capitalize` | Capitalize first | `{{ "hello" \| capitalize }}` | `Hello` |
| `trim` | Remove whitespace | `{{ "  text  " \| trim }}` | `text` |
| `length` | Count items | `{{ [1,2,3] \| length }}` | `3` |
| `default(x)` | Default if empty | `{{ None \| default("N/A") }}` | `N/A` |
| `round(n)` | Round number | `{{ 3.14159 \| round(2) }}` | `3.14` |
| `int` | Convert to integer | `{{ "123" \| int }}` | `123` |
| `float` | Convert to float | `{{ "12.5" \| float }}` | `12.5` |
| `join(sep)` | Join list | `{{ ["a","b"] \| join("-") }}` | `a-b` |
| `replace(old, new)` | Replace text | `{{ "Hi John" \| replace("John", "Jane") }}` | `Hi Jane` |
| `urlencode` | URL encoding | `{{ "a b c" \| urlencode }}` | `a%20b%20c` |

### Chaining Filters

You can apply multiple filters:

**Template**:
```html
<p>{{ nome | trim | upper }}</p>
<!-- First trim whitespace, then uppercase -->
```

**From your code** (`templates/html/proposta_base.html:54`):
```html
<a href="https://www.google.com/maps/search/?api=1&query={{ (empresa.endereco.logradouro + ' ' + empresa.endereco.bairro + ' ' + empresa.endereco.cidade + ' ' + empresa.endereco.estado + ' ' + empresa.endereco.cep)|urlencode }}">
```
This creates a Google Maps link by combining address parts and URL-encoding them.

---

## Control Structures

### If Statements

**Basic if**:
```html
{% if usuario_logado %}
    <p>Bem-vindo, {{ usuario_nome }}!</p>
{% endif %}
```

**If-else**:
```html
{% if quantidade > 0 %}
    <p>Em estoque</p>
{% else %}
    <p>Esgotado</p>
{% endif %}
```

**If-elif-else**:
```html
{% if nota >= 9 %}
    <p>Excelente</p>
{% elif nota >= 7 %}
    <p>Bom</p>
{% elif nota >= 5 %}
    <p>Regular</p>
{% else %}
    <p>Insuficiente</p>
{% endif %}
```

**Checking if variable exists**:
```html
{% if logo_base64 %}
    <img src="data:image/png;base64,{{ logo_base64 }}">
{% endif %}
```

**From your code** (`templates/html/proposta_base.html:19-23`):
```html
{% if logo_secundario_base64 %}
<img src="data:image/png;base64,{{ logo_secundario_base64 }}" alt="Armant" class="header-logo-compact">
{% else %}
<img src="data:image/png;base64,{{ logo_base64 }}" alt="Armant" class="header-logo-compact">
{% endif %}
```
If secondary logo exists, use it; otherwise use primary logo.

**From your code** (`templates/html/proposta_base.html:40-42`):
```html
{% if rascunho %}
<div class="watermark-text">RASCUNHO</div>
{% endif %}
```
Only show "RASCUNHO" watermark if `rascunho` variable is True.

### For Loops

**Basic loop**:
```html
<ul>
{% for item in itens %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

**Output**:
```html
<ul>
    <li>Tubo</li>
    <li>Cabo</li>
    <li>Fita</li>
</ul>
```

**Loop over dictionaries**:
```html
{% for codigo, material in materiais.items() %}
    <p>{{ codigo }}: {{ material.descricao }}</p>
{% endfor %}
```

**Loop with index**:
```html
{% for item in itens %}
    <p>{{ loop.index }}. {{ item }}</p>
    <!-- loop.index starts at 1 -->
    <!-- loop.index0 starts at 0 -->
{% endfor %}
```

**Output**:
```html
<p>1. Tubo</p>
<p>2. Cabo</p>
<p>3. Fita</p>
```

**Loop variables** (available inside `{% for %}`):

| Variable | Description |
|----------|-------------|
| `loop.index` | Current iteration (1-indexed) |
| `loop.index0` | Current iteration (0-indexed) |
| `loop.first` | True if first iteration |
| `loop.last` | True if last iteration |
| `loop.length` | Total number of items |

**Example**:
```html
<table>
{% for item in itens %}
    <tr class="{% if loop.first %}first-row{% endif %}">
        <td>{{ loop.index }}</td>
        <td>{{ item.descricao }}</td>
    </tr>
{% endfor %}
</table>
```

**Empty loop handling**:
```html
<ul>
{% for item in itens %}
    <li>{{ item }}</li>
{% else %}
    <li>Nenhum item encontrado</li>
{% endfor %}
</ul>
```
The `{% else %}` block runs if the list is empty.

---

## Comments

### Jinja2 Comments

**Template**:
```html
{# This comment will NOT appear in the output #}
<p>Visible text</p>

{#
  Multi-line comment
  Also not in output
#}
```

**Output**:
```html
<p>Visible text</p>
```

### HTML Comments (Still Appear)

**Template**:
```html
<!-- This HTML comment WILL appear in output -->
<p>Visible text</p>
```

**Output**:
```html
<!-- This HTML comment WILL appear in output -->
<p>Visible text</p>
```

---

## Whitespace Control

Jinja2 can create extra whitespace. Control it with `-`:

**Template without whitespace control**:
```html
{% for item in itens %}
    <li>{{ item }}</li>
{% endfor %}
```

**Output** (notice blank lines):
```html

    <li>Tubo</li>

    <li>Cabo</li>

```

**Template with whitespace control**:
```html
{% for item in itens -%}
    <li>{{ item }}</li>
{%- endfor %}
```

**Output** (compact):
```html
<li>Tubo</li><li>Cabo</li>
```

- `{%-` - Remove whitespace **before** tag
- `-%}` - Remove whitespace **after** tag

---

## Using Jinja2 in Python

### Basic Usage

```python
from jinja2 import Template

# Create template
template_string = "<h1>Hello, {{ name }}!</h1>"
template = Template(template_string)

# Render with data
output = template.render(name="João")
print(output)  # <h1>Hello, João!</h1>
```

### Loading Templates from Files

```python
from jinja2 import Environment, FileSystemLoader

# Set up environment
env = Environment(loader=FileSystemLoader('templates/html'))

# Load template
template = env.get_template('proposta_base.html')

# Prepare data
data = {
    "numero_orcamento": "1024",
    "cliente": "Grupo Panvel",
    "empresa": {
        "razao_social": "ARMANT LTDA",
        "cnpj": "13.591.585/0001-03"
    },
    "itens": [...]
}

# Render
html_output = template.render(**data)  # ** unpacks dictionary

# Save to file
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_output)
```

**From your code** (`hvac/generators/proposta_pdf.py` - simplified):
```python
from jinja2 import Environment, FileSystemLoader

def gerar_proposta_pdf(dados, arquivo_saida):
    # Set up Jinja2
    env = Environment(loader=FileSystemLoader('templates/html'))
    template = env.get_template('proposta_base.html')

    # Prepare template data
    template_data = {
        "numero_orcamento": dados.get("numero_orcamento"),
        "cliente": dados.get("cliente"),
        "empresa": carregar_json("config/empresa.json"),
        "itens_precificados": dados.get("itens_precificados", []),
        # ... more data ...
    }

    # Render HTML
    html_content = template.render(**template_data)

    # Convert to PDF (using WeasyPrint)
    from weasyprint import HTML
    HTML(string=html_content, base_url='templates/html/').write_pdf(arquivo_saida)
```

---

## Real Examples from This Project

### 1. Conditional Logo Display

**Template** (`templates/html/proposta_base.html:67-73`):
```html
<div class="footer-logos">
    {% if logo_abrava_base64 %}
    <img src="data:image/png;base64,{{ logo_abrava_base64 }}" class="footer-logo">
    {% endif %}
    {% if logo_asbrav_base64 %}
    <img src="data:image/png;base64,{{ logo_asbrav_base64 }}" class="footer-logo">
    {% endif %}
</div>
```

**Explanation**:
- Only shows ABRAVA logo if `logo_abrava_base64` variable exists
- Only shows ASBRAV logo if `logo_asbrav_base64` variable exists
- Allows flexible logo configuration

### 2. Dynamic Header

**Template** (`templates/html/proposta_base.html:26-27`):
```html
<div class="header-num-orc-compact">ORÇAMENTO {{ numero_orcamento }}</div>
<div class="header-data-compact">{{ cidade }}, {{ data_extenso }}</div>
```

**Python data**:
```python
{
    "numero_orcamento": "1024",
    "cidade": "Porto Alegre",
    "data_extenso": "18 de dezembro de 2025"
}
```

**Output**:
```html
<div class="header-num-orc-compact">ORÇAMENTO 1024</div>
<div class="header-data-compact">Porto Alegre, 18 de dezembro de 2025</div>
```

### 3. Company Footer

**Template** (`templates/html/proposta_base.html:49-64`):
```html
<div class="footer-info">
    <div style="margin-bottom: 2px;">
        <span class="rodape-empresa">{{ empresa.razao_social }}</span>
        <span class="separador">|</span>
        <span>CNPJ: {{ empresa.cnpj }}</span>
    </div>
    <div style="margin-bottom: 2px;">
        <a href="https://www.google.com/maps/search/?api=1&query={{ (empresa.endereco.logradouro + ' ' + empresa.endereco.bairro + ' ' + empresa.endereco.cidade + ' ' + empresa.endereco.estado + ' ' + empresa.endereco.cep)|urlencode }}">
            {{ empresa.endereco.logradouro }} - {{ empresa.endereco.bairro }}, {{ empresa.endereco.cidade }} - {{ empresa.endereco.estado }}, {{ empresa.endereco.cep }}
        </a>
    </div>
    <div>
        <strong>{{ empresa.telefone }}</strong>
        <span class="separador">|</span>
        {{ empresa.email }}
        <span class="separador">|</span>
        {{ empresa.site }}
    </div>
</div>
```

**Explanation**:
- Accesses nested `empresa.endereco.logradouro` etc.
- Creates Google Maps link by concatenating address parts
- Uses `| urlencode` filter to make address URL-safe
- All data comes from `config/empresa.json`

### 4. Looping Through Items (Hypothetical Example)

While not visible in the snippet, the template likely has:

```html
<table class="items-table">
    {% for item in itens_precificados %}
    <tr>
        <td>{{ loop.index }}</td>
        <td>{{ item.descricao }}</td>
        <td>{{ item.quantidade }}</td>
        <td>{{ item.unidade }}</td>
        <td>R$ {{ item.valor_unitario }}</td>
        <td>R$ {{ item.valor_total }}</td>
    </tr>
    {% endfor %}
</table>
```

---

## Common Patterns

### 1. Safe Default Values

```html
<p>Observação: {{ observacao | default("Nenhuma observação") }}</p>
```

### 2. Conditional CSS Classes

```html
<div class="item {% if item.urgente %}urgente{% endif %}">
    {{ item.descricao }}
</div>
```

### 3. Number Formatting

```html
<!-- In Python, prepare formatted value -->
{% set preco_formatado = "R$ {:,.2f}".format(preco).replace(",", "X").replace(".", ",").replace("X", ".") %}
<p>Preço: {{ preco_formatado }}</p>

<!-- Or pass already-formatted from Python -->
<p>Preço: {{ preco_formatado }}</p>
```

**Better approach**: Format in Python before passing to template.

### 4. Nested Loops

```html
{% for categoria, itens in agrupados.items() %}
    <h3>{{ categoria }}</h3>
    <ul>
    {% for item in itens %}
        <li>{{ item.descricao }}</li>
    {% endfor %}
    </ul>
{% endfor %}
```

### 5. Setting Variables in Template

```html
{% set total = 0 %}
{% for item in itens %}
    {% set total = total + item.preco %}
{% endfor %}
<p>Total: {{ total }}</p>
```

**Note**: Better to calculate totals in Python, not in template.

---

## Quick Reference

### Syntax Summary

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ var }}` | Output variable | `{{ nome }}` |
| `{% statement %}` | Control flow | `{% if x %}...{% endif %}` |
| `{# comment #}` | Comment | `{# TODO #}` |
| `{{ var \| filter }}` | Apply filter | `{{ nome \| upper }}` |
| `{% if cond %}...{% endif %}` | Conditional | `{% if ativo %}Sim{% endif %}` |
| `{% for x in list %}...{% endfor %}` | Loop | `{% for i in items %}{{ i }}{% endfor %}` |

### Common Filters

```html
{{ text | upper }}              <!-- UPPERCASE -->
{{ text | lower }}              <!-- lowercase -->
{{ text | title }}              <!-- Title Case -->
{{ text | trim }}               <!-- Remove whitespace -->
{{ number | round(2) }}         <!-- Round to 2 decimals -->
{{ value | default("N/A") }}    <!-- Default if empty -->
{{ list | length }}             <!-- Count items -->
{{ list | join(", ") }}         <!-- Join with separator -->
{{ url | urlencode }}           <!-- URL encode -->
```

### Loop Variables

```html
{% for item in items %}
    {{ loop.index }}      <!-- 1, 2, 3, ... -->
    {{ loop.index0 }}     <!-- 0, 1, 2, ... -->
    {{ loop.first }}      <!-- True on first iteration -->
    {{ loop.last }}       <!-- True on last iteration -->
    {{ loop.length }}     <!-- Total items -->
{% endfor %}
```

---

## Debugging Tips

### 1. Print Variables

```html
<pre>{{ variable }}</pre>
<!-- Shows variable content for debugging -->
```

### 2. Check Type

```html
{{ variable.__class__.__name__ }}
<!-- Shows: str, dict, list, etc. -->
```

### 3. Dump All Variables

```html
<pre>
{% for key, value in data.items() %}
{{ key }}: {{ value }}
{% endfor %}
</pre>
```

### 4. Check if Variable Exists

```html
{% if variable is defined %}
    Variable exists!
{% else %}
    Variable is not defined!
{% endif %}
```

---

## Best Practices

### ✅ Do:
1. **Keep logic in Python** - Templates should be simple
2. **Format data before passing** - Don't do complex formatting in templates
3. **Use meaningful variable names** - `cliente_nome` not `cn`
4. **Handle missing data** - Use `| default()` or `{% if %}`

### ❌ Don't:
1. **Don't put business logic in templates** - No calculations, data processing
2. **Don't nest too deeply** - Complex nested loops are hard to read
3. **Don't use inline styles excessively** - Use CSS classes
4. **Don't forget to escape HTML** - Jinja2 auto-escapes, but be aware

---

## Next Steps

Now that you understand Jinja2:
1. ✅ Open `templates/html/proposta_base.html` and read through it
2. ✅ Identify all `{{ variables }}` and see where they come from
3. ✅ Find all `{% if %}` and `{% for %}` blocks
4. ✅ Try modifying text in the template and regenerate PDF
5. ✅ Move on to HTML/CSS guide to understand the layout structure

**Practice Exercise**: Try to add a new field to `config/empresa.json` and display it in the template footer!

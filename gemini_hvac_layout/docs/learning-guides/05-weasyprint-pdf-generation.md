# WeasyPrint PDF Generation Guide

**Purpose**: Learn how WeasyPrint converts HTML+CSS to PDF in this HVAC project.

---

## Table of Contents
1. [What is WeasyPrint?](#what-is-weasyprint)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Converting HTML to PDF](#converting-html-to-pdf)
5. [Working with CSS](#working-with-css)
6. [Embedding Images](#embedding-images)
7. [Page Layout and Print CSS](#page-layout-and-print-css)
8. [How This Project Uses WeasyPrint](#how-this-project-uses-weasyprint)
9. [Common Issues and Solutions](#common-issues-and-solutions)
10. [Debugging PDFs](#debugging-pdfs)

---

## What is WeasyPrint?

**WeasyPrint** is a Python library that converts HTML and CSS into PDF documents.

**Think of it as**:
- A "print to PDF" function for Python
- A way to create professional PDFs from web templates
- Like a headless browser that only outputs PDF

**Key Features**:
- Supports modern HTML5 and CSS3
- Handles complex layouts, tables, images
- Supports print-specific CSS (`@page`, running headers/footers)
- Embeds fonts and images
- Produces high-quality, print-ready PDFs

**In this project**: WeasyPrint takes your Jinja2-rendered HTML template and CSS file, and generates the professional HVAC proposal PDF.

---

## Installation

### Prerequisites

WeasyPrint requires some system dependencies.

**On Ubuntu/Debian**:
```bash
sudo apt-get install python3-dev python3-pip libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**On macOS**:
```bash
brew install cairo pango gdk-pixbuf libffi
```

**On Windows**:
Download GTK+ for Windows: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

### Install WeasyPrint

```bash
pip install weasyprint
```

**Your project** (`hvac/generators/proposta_pdf.py:158-164`):
```python
try:
    from weasyprint import HTML, CSS
except ImportError:
    return {
        "sucesso": False,
        "erro": "weasyprint nao instalado. Execute: pip install weasyprint"
    }
```
The code checks if WeasyPrint is installed before using it.

---

## Basic Usage

### Simple Example: String to PDF

```python
from weasyprint import HTML

# Create PDF from HTML string
html_string = "<h1>Hello, World!</h1><p>This is a PDF.</p>"
HTML(string=html_string).write_pdf("output.pdf")
```

**Result**: Creates `output.pdf` with "Hello, World!" heading and a paragraph.

### From File to PDF

```python
from weasyprint import HTML

# Create PDF from HTML file
HTML(filename="template.html").write_pdf("output.pdf")
```

### From URL to PDF

```python
from weasyprint import HTML

# Create PDF from website
HTML(url="https://example.com").write_pdf("output.pdf")
```

---

## Converting HTML to PDF

### Basic HTML to PDF

```python
from weasyprint import HTML

html = """
<!DOCTYPE html>
<html>
<head>
    <title>My PDF</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20mm;
        }
        h1 {
            color: blue;
        }
    </style>
</head>
<body>
    <h1>Invoice</h1>
    <p>Total: $1,250.00</p>
</body>
</html>
"""

HTML(string=html).write_pdf("invoice.pdf")
```

### With External CSS

```python
from weasyprint import HTML, CSS

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Styled PDF</title>
</head>
<body>
    <h1>Heading</h1>
    <p class="highlight">Important text</p>
</body>
</html>
"""

css = """
body {
    font-family: Arial;
    margin: 20mm;
}
.highlight {
    background: yellow;
    font-weight: bold;
}
"""

HTML(string=html).write_pdf("output.pdf", stylesheets=[CSS(string=css)])
```

**From your code** (`hvac/generators/proposta_pdf.py:329-331`):
```python
# Gera PDF
html = HTML(string=html_content, base_url=str(template_dir))
css = CSS(string=css_content)
html.write_pdf(str(output_path), stylesheets=[css])
```

**Explanation**:
- `HTML(string=html_content)` - Creates HTML object from string
- `base_url=str(template_dir)` - Base path for resolving relative URLs (images, CSS)
- `CSS(string=css_content)` - Creates CSS object from string
- `html.write_pdf(...)` - Generates the PDF
- `stylesheets=[css]` - Applies CSS to the HTML

---

## Working with CSS

### Loading CSS Files

```python
from weasyprint import HTML, CSS

html = HTML(filename="template.html")
css = CSS(filename="styles.css")

html.write_pdf("output.pdf", stylesheets=[css])
```

### Multiple CSS Files

```python
from weasyprint import HTML, CSS

html = HTML(filename="template.html")
css1 = CSS(filename="base.css")
css2 = CSS(filename="custom.css")

html.write_pdf("output.pdf", stylesheets=[css1, css2])
```

### Inline CSS in HTML

```python
html = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    ...
</body>
</html>
"""

# WeasyPrint automatically loads linked stylesheets if base_url is set
HTML(string=html, base_url="path/to/templates/").write_pdf("output.pdf")
```

---

## Embedding Images

### Using Image Files

```python
html = """
<html>
<body>
    <img src="logo.png" alt="Logo" width="200">
</body>
</html>
"""

# Need base_url to resolve relative paths
HTML(string=html, base_url="path/to/images/").write_pdf("output.pdf")
```

### Using Base64 Embedded Images

**This is what your project uses!**

```python
import base64

# Load image and convert to base64
with open("logo.png", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode("utf-8")

html = f"""
<html>
<body>
    <img src="data:image/png;base64,{logo_data}" alt="Logo">
</body>
</html>
"""

HTML(string=html).write_pdf("output.pdf")
```

**From your code** (`hvac/generators/proposta_pdf.py:32-38`):
```python
def carregar_logo_base64(logo_path: str) -> Optional[str]:
    """Carrega logo como base64 para embedar no HTML"""
    full_path = BASE_DIR / logo_path
    if full_path.exists():
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None
```

**Explanation**:
1. Open image file in **binary mode** (`"rb"`)
2. Read file contents
3. Encode as base64
4. Decode to UTF-8 string
5. Embed in HTML as `data:image/png;base64,{data}`

**Why use base64?**
- Image is embedded directly in HTML (no external files)
- PDF is self-contained
- No broken image links

---

## Page Layout and Print CSS

### @page Rule

```css
@page {
    size: A4;              /* Paper size */
    margin: 20mm 15mm;     /* Top/bottom, left/right */
}
```

**Supported sizes**: `A4`, `A3`, `Letter`, `Legal`, or custom (e.g., `210mm 297mm`)

**From your template** (`proposta_styles.css:1-12`):
```css
@page {
    size: A4;
    margin: 20mm 15mm 30mm 15mm;

    @top-center {
        content: element(header);
    }

    @bottom-center {
        content: element(footer);
    }
}
```

### Running Headers and Footers

**CSS**:
```css
@page {
    @top-center {
        content: element(header);
    }
    @bottom-center {
        content: element(footer);
    }
}

header {
    position: running(header);
}

footer {
    position: running(footer);
}
```

**HTML**:
```html
<header>
    <p>Company Name | Quote #123</p>
</header>

<footer>
    <p>Page 1 of 3 | www.company.com</p>
</footer>

<div>
    Main content here...
</div>
```

**Result**: Header and footer appear on every page.

**From your template** (`proposta_styles.css:82-89`):
```css
header#page-header {
    position: running(header);
    display: block;
    width: 180mm;
    border-bottom: 1.2px solid var(--primary-color);
    padding-bottom: 5px;
    margin: 0;
}
```

### Page Breaks

```css
/* Force page break before element */
.new-section {
    page-break-before: always;
}

/* Force page break after element */
.end-section {
    page-break-after: always;
}

/* Avoid page break inside element */
.keep-together {
    page-break-inside: avoid;
}
```

**Example**:
```html
<div class="section">
    <p>Content on page 1</p>
</div>

<div class="section" style="page-break-before: always;">
    <p>This starts on page 2</p>
</div>
```

### Different First Page

```css
@page :first {
    margin-top: 10mm;  /* Smaller margin on first page */
    @top-center {
        content: none;  /* No header on first page */
    }
}
```

**From your template** (`proposta_styles.css:14-19`):
```css
@page :first {
    margin-top: 10mm;
    @top-center {
        content: none;
    }
}
```
First page has no header and smaller top margin.

---

## How This Project Uses WeasyPrint

### Complete Workflow

**1. Load Jinja2 Template**:
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/html'))
template = env.get_template('proposta_base.html')
```

**2. Prepare Data**:
```python
template_data = {
    "numero_orcamento": "1024",
    "cliente": "Grupo Panvel",
    "empresa": carregar_json("config/empresa.json"),
    "logo_base64": carregar_logo_base64("templates/html/logo_armant.png"),
    "itens_precificados": [...]
}
```

**3. Render HTML**:
```python
html_content = template.render(**template_data)
```

**4. Load CSS**:
```python
css_path = Path("templates/html/proposta_styles.css")
css_content = css_path.read_text(encoding="utf-8")
```

**5. Generate PDF**:
```python
from weasyprint import HTML, CSS

html = HTML(string=html_content, base_url="templates/html/")
css = CSS(string=css_content)
html.write_pdf("output/proposta.pdf", stylesheets=[css])
```

### Simplified Code from Your Project

**From** `hvac/generators/proposta_pdf.py:326-331`:
```python
# Gera PDF
html = HTML(string=html_content, base_url=str(template_dir))
css = CSS(string=css_content)
html.write_pdf(str(output_path), stylesheets=[css])
```

**Complete function signature** (`proposta_pdf.py:128-135`):
```python
def gerar_proposta_pdf(
    precificado: Dict[str, Any],
    rascunho: bool = False,
    numero_orcamento: Optional[str] = None,
    revisao: Optional[str] = None,
    output_path: Optional[str] = None,
    configs: Optional[Dict] = None
) -> Dict[str, Any]:
```

**Parameters**:
- `precificado` - Dictionary with quote data (from pipeline)
- `rascunho` - If True, adds "RASCUNHO" watermark
- `numero_orcamento` - Quote number (auto-generated if not provided)
- `revisao` - Revision number (e.g., "R01")
- `output_path` - Where to save PDF (auto-generated if not provided)
- `configs` - Configuration dictionaries (empresa, usuario, etc.)

**Returns**:
```python
{
    "sucesso": True,
    "numero_orcamento": "1024",
    "arquivo_pdf": "output/Grupo_Panvel/ORC-1024_Grupo_Panvel.pdf",
    "arquivo_rascunho": "output/Grupo_Panvel/ORC-1024_Grupo_Panvel_RASCUNHO.pdf"
}
```

---

## Common Issues and Solutions

### Issue 1: Images Not Showing

**Problem**: Images in PDF are broken or missing.

**Solution**: Set `base_url` parameter.

```python
# ❌ Wrong - relative paths won't resolve
HTML(string=html).write_pdf("output.pdf")

# ✅ Correct - base_url helps resolve paths
HTML(string=html, base_url="path/to/templates/").write_pdf("output.pdf")

# ✅ Better - use base64 embedded images (no external files needed)
html = f'<img src="data:image/png;base64,{logo_base64}">'
```

### Issue 2: CSS Not Applied

**Problem**: PDF has no styling.

**Solution**: Pass CSS to `stylesheets` parameter.

```python
# ❌ Wrong - CSS not applied
html = HTML(string=html_content)
html.write_pdf("output.pdf")

# ✅ Correct - pass CSS
css = CSS(string=css_content)
html.write_pdf("output.pdf", stylesheets=[css])
```

### Issue 3: Fonts Not Showing

**Problem**: Custom fonts don't appear in PDF.

**Solution**: Use `@font-face` in CSS or link to Google Fonts.

**Google Fonts** (your template uses this):
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

**Local fonts**:
```css
@font-face {
    font-family: 'CustomFont';
    src: url('fonts/custom.ttf') format('truetype');
}

body {
    font-family: 'CustomFont', Arial, sans-serif;
}
```

### Issue 4: PDF Colors Look Washed Out

**Problem**: Colors in PDF don't match CSS.

**Solution**: Add print color adjustment CSS.

```css
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```

**From your template** (`proposta_styles.css:21-26`):
```css
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```

### Issue 5: Content Cut Off

**Problem**: Text or tables cut off at page boundaries.

**Solution**: Use `page-break-inside: avoid`.

```css
.item-row {
    page-break-inside: avoid;  /* Keep row together on same page */
}

table {
    page-break-inside: auto;   /* Allow table to break across pages */
}

tr {
    page-break-inside: avoid;  /* But keep rows together */
}
```

---

## Debugging PDFs

### 1. Generate HTML First

Before generating PDF, save the rendered HTML to debug it:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/html'))
template = env.get_template('proposta_base.html')

html_content = template.render(**data)

# Save HTML for debugging
with open("debug_output.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Open in browser to check layout
# Then generate PDF
from weasyprint import HTML, CSS
html = HTML(string=html_content, base_url="templates/html/")
html.write_pdf("output.pdf", stylesheets=[CSS(filename="templates/html/proposta_styles.css")])
```

### 2. Check CSS Separately

Open the HTML file in a browser to see if CSS is working:

1. Save HTML with inline CSS link
2. Open in Chrome/Firefox
3. Check if styling looks correct
4. If yes, issue is WeasyPrint-specific
5. If no, issue is in your HTML/CSS

### 3. Test with Simple HTML

```python
from weasyprint import HTML

# Minimal test
HTML(string="<h1>Test</h1>").write_pdf("test.pdf")

# If this works, WeasyPrint is installed correctly
# If not, reinstall WeasyPrint and dependencies
```

### 4. Check WeasyPrint Version

```bash
python -c "import weasyprint; print(weasyprint.__version__)"
```

Your project uses WeasyPrint 67.0.

---

## Advanced Features

### Custom Page Sizes

```css
@page {
    size: 210mm 297mm;  /* Custom size */
    margin: 20mm;
}
```

### Page Counters

```css
@page {
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
    }
}
```

### Bookmarks (PDF Table of Contents)

```html
<h1 style="bookmark-level: 1">Chapter 1</h1>
<h2 style="bookmark-level: 2">Section 1.1</h2>
<h2 style="bookmark-level: 2">Section 1.2</h2>
```

WeasyPrint automatically creates PDF bookmarks from headings with `bookmark-level`.

---

## Quick Reference

### Basic PDF Generation

```python
from weasyprint import HTML, CSS

# From string
HTML(string="<h1>Hello</h1>").write_pdf("output.pdf")

# From file
HTML(filename="template.html").write_pdf("output.pdf")

# With CSS
HTML(string=html).write_pdf("output.pdf", stylesheets=[CSS(string=css)])

# With base URL
HTML(string=html, base_url="/path/to/templates/").write_pdf("output.pdf")
```

### Common CSS for Print

```css
@page {
    size: A4;
    margin: 20mm;
}

@media print {
    body {
        print-color-adjust: exact;
    }
}

.no-break {
    page-break-inside: avoid;
}

.new-page {
    page-break-before: always;
}
```

### Embedding Images

```python
import base64

# Convert image to base64
with open("logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

# Use in HTML
html = f'<img src="data:image/png;base64,{logo_b64}">'
```

---

## Next Steps

Now that you understand WeasyPrint:
1. ✅ Run `./gerar_teste_pdf.sh` and examine the output PDF
2. ✅ Modify the HTML template and regenerate to see changes
3. ✅ Try changing CSS colors and see them in PDF
4. ✅ Look at `hvac/generators/proposta_pdf.py` to see the complete implementation
5. ✅ Move on to openpyxl guide to learn Excel generation

**Practice Exercise**: Try modifying `proposta_styles.css` to change the page margins from 20mm to 30mm and regenerate the PDF!

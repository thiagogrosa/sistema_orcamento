# HTML & CSS Basics Guide

**Purpose**: Learn HTML and CSS fundamentals to understand and modify the proposal template.

---

## Table of Contents
1. [HTML Fundamentals](#html-fundamentals)
2. [CSS Fundamentals](#css-fundamentals)
3. [CSS Selectors](#css-selectors)
4. [Box Model](#box-model)
5. [Common CSS Properties](#common-css-properties)
6. [Print-Specific CSS](#print-specific-css)
7. [Understanding the Proposal Template](#understanding-the-proposal-template)
8. [Modifying the Template](#modifying-the-template)

---

## HTML Fundamentals

### What is HTML?

**HTML** = **H**yper**T**ext **M**arkup **L**anguage

- Defines the **structure** of web pages (and PDFs in this project)
- Uses **tags** to mark up content
- Like a skeleton - it provides structure, not styling

### Basic HTML Structure

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Page Title</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Main Heading</h1>
    <p>This is a paragraph.</p>
</body>
</html>
```

**Parts**:
- `<!DOCTYPE html>` - Tells browser this is HTML5
- `<html>` - Root element, wraps everything
- `<head>` - Metadata (not visible on page)
- `<body>` - Visible content
- `<title>` - Page title (appears in browser tab)

### HTML Tags

Tags come in pairs (opening and closing):

```html
<tagname>Content goes here</tagname>
  ↑                            ↑
opening                    closing (with /)
```

**Self-closing tags** (no content):
```html
<img src="logo.png" alt="Logo">
<br>  <!-- line break -->
<hr>  <!-- horizontal rule -->
```

### Common HTML Elements

#### Headings
```html
<h1>Main Heading</h1>       <!-- Largest -->
<h2>Section Heading</h2>
<h3>Sub-section</h3>
<h4>Sub-sub-section</h4>
<h5>Smaller</h5>
<h6>Smallest</h6>
```

#### Text Elements
```html
<p>This is a paragraph.</p>
<strong>Bold text</strong>
<em>Italic text</em>
<span>Inline container (for styling)</span>
<br>  <!-- Line break -->
```

#### Links
```html
<a href="https://example.com">Click here</a>
<a href="mailto:email@example.com">Email us</a>
```

**From your template** (`proposta_base.html:54-56`):
```html
<a href="https://www.google.com/maps/search/?api=1&query={{ (empresa.endereco.logradouro + ' ' + empresa.endereco.bairro + ' ' + empresa.endereco.cidade + ' ' + empresa.endereco.estado + ' ' + empresa.endereco.cep)|urlencode }}" class="footer-link">
    {{ empresa.endereco.logradouro }} - {{ empresa.endereco.bairro }}, {{ empresa.endereco.cidade }} - {{ empresa.endereco.estado }}, {{ empresa.endereco.cep }}
</a>
```

#### Images
```html
<img src="path/to/image.png" alt="Description">

<!-- Base64 embedded image -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="Logo">
```

**From your template** (`proposta_base.html:20`):
```html
<img src="data:image/png;base64,{{ logo_secundario_base64 }}" alt="Armant" class="header-logo-compact">
```

#### Lists
```html
<!-- Unordered list (bullets) -->
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>

<!-- Ordered list (numbers) -->
<ol>
    <li>First</li>
    <li>Second</li>
    <li>Third</li>
</ol>
```

#### Tables
```html
<table>
    <thead>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Row 1, Col 1</td>
            <td>Row 1, Col 2</td>
        </tr>
        <tr>
            <td>Row 2, Col 1</td>
            <td>Row 2, Col 2</td>
        </tr>
    </tbody>
</table>
```

**From your template** (`proposta_base.html:16-30`):
```html
<table class="header-table">
    <tr>
        <td class="header-td-logo">
            {% if logo_secundario_base64 %}
            <img src="data:image/png;base64,{{ logo_secundario_base64 }}" alt="Armant" class="header-logo-compact">
            {% else %}
            <img src="data:image/png;base64,{{ logo_base64 }}" alt="Armant" class="header-logo-compact">
            {% endif %}
        </td>
        <td class="header-td-info">
            <div class="header-num-orc-compact">ORÇAMENTO {{ numero_orcamento }}</div>
            <div class="header-data-compact">{{ cidade }}, {{ data_extenso }}</div>
        </td>
    </tr>
</table>
```

#### Containers
```html
<div>Block-level container (takes full width)</div>
<span>Inline container (only takes content width)</span>

<header>Header section</header>
<footer>Footer section</footer>
<section>Content section</section>
<article>Independent content</article>
```

### HTML Attributes

Attributes provide additional information:

```html
<tag attribute="value">Content</tag>
```

**Common attributes**:
```html
<img src="logo.png" alt="Company Logo" width="200">
     ↑   ↑         ↑   ↑            ↑     ↑
   attr value    attr value       attr  value

<a href="https://example.com" class="link-button" id="main-link">
   ↑    ↑                       ↑      ↑          ↑   ↑
  attr  value                 attr    value      attr value

<div class="container primary" id="main-content" style="color: red;">
```

**Important attributes**:
- `class` - For CSS styling (can have multiple)
- `id` - Unique identifier (only one per page)
- `src` - Source for images/scripts
- `href` - URL for links
- `style` - Inline CSS (avoid when possible)
- `alt` - Alternative text for images

---

## CSS Fundamentals

### What is CSS?

**CSS** = **C**ascading **S**tyle **S**heets

- Defines the **appearance** of HTML elements
- Controls colors, fonts, spacing, layout, etc.
- Like clothing for the HTML skeleton

### CSS Syntax

```css
selector {
    property: value;
    property: value;
}
```

**Example**:
```css
h1 {
    color: blue;
    font-size: 24px;
    font-weight: bold;
}
```

### Three Ways to Apply CSS

#### 1. External Stylesheet (Best Practice)

**HTML**:
```html
<head>
    <link rel="stylesheet" href="styles.css">
</head>
```

**styles.css**:
```css
body {
    font-family: Arial;
    color: black;
}
```

**From your template** (`proposta_base.html:9`):
```html
<link rel="stylesheet" href="proposta_styles.css">
```

#### 2. Internal Stylesheet

```html
<head>
    <style>
        body {
            font-family: Arial;
            color: black;
        }
    </style>
</head>
```

#### 3. Inline Styles (Use Sparingly)

```html
<p style="color: red; font-size: 14px;">Red text</p>
```

**From your template** (`proposta_base.html:48`):
```html
<div style="margin-bottom: 2px;">
```

---

## CSS Selectors

### Basic Selectors

```css
/* Element selector - applies to ALL <p> tags */
p {
    color: black;
}

/* Class selector - applies to class="intro" */
.intro {
    font-size: 16px;
}

/* ID selector - applies to id="main" */
#main {
    background: white;
}

/* Multiple selectors */
h1, h2, h3 {
    color: blue;
}
```

**From your template CSS** (`proposta_styles.css:44-50`):
```css
body {
    font-family: 'Montserrat', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 8.8pt;
    line-height: 1.35;
    color: var(--black);
    background: var(--white);
}
```

### Descendant Selectors

```css
/* Selects <p> inside <div> */
div p {
    color: blue;
}

/* Selects <span> with class "highlight" inside <p> */
p span.highlight {
    background: yellow;
}
```

### Pseudo-classes

```css
/* Link states */
a:hover {
    color: red;
}

/* First/last child */
li:first-child {
    font-weight: bold;
}

li:last-child {
    border-bottom: none;
}
```

**From your template CSS** (`proposta_styles.css:14-19`):
```css
@page :first {
    margin-top: 10mm;
    @top-center {
        content: none;
    }
}
```
This targets only the first page.

---

## Box Model

Every HTML element is a rectangular box with:

```
┌─────────────────────────────────┐
│         Margin (outside)        │
│  ┌──────────────────────────┐  │
│  │   Border                 │  │
│  │  ┌───────────────────┐  │  │
│  │  │   Padding         │  │  │
│  │  │  ┌────────────┐  │  │  │
│  │  │  │  Content   │  │  │  │
│  │  │  └────────────┘  │  │  │
│  │  └───────────────────┘  │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

**CSS Properties**:
```css
.box {
    /* Content size */
    width: 200px;
    height: 100px;

    /* Padding (inside, around content) */
    padding: 10px;              /* All sides */
    padding: 10px 20px;         /* Top/bottom, left/right */
    padding: 10px 20px 15px 25px; /* Top, right, bottom, left */
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 15px;
    padding-left: 25px;

    /* Border */
    border: 1px solid black;
    border-top: 2px solid red;
    border-bottom: 1px dashed blue;

    /* Margin (outside, spacing from other elements) */
    margin: 20px;               /* All sides */
    margin: 10px auto;          /* Top/bottom 10px, left/right auto (centers) */
    margin-top: 10px;
    margin-bottom: 20px;
}
```

**From your template CSS** (`proposta_styles.css:38-42`):
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```
This resets all margins and paddings to 0, ensuring consistent spacing.

---

## Common CSS Properties

### Colors

```css
.element {
    /* Named colors */
    color: red;
    background-color: white;

    /* Hex colors */
    color: #FF0000;        /* Red */
    color: #0A94D6;        /* Armant Blue */

    /* RGB */
    color: rgb(255, 0, 0); /* Red */

    /* RGBA (with transparency) */
    color: rgba(0, 0, 0, 0.5);  /* 50% transparent black */
}
```

**From your template CSS** (`proposta_styles.css:28-36`):
```css
:root {
    --primary-color: #0A94D6;
    --secondary-color: #00A859;
    --black: #000000;
    --white: #FFFFFF;
    --text-dark: #000000;
    --text-muted: #333333;
    --border-color: #0A94D6;
}
```

**Using CSS variables**:
```css
body {
    color: var(--black);
    background: var(--white);
}

.header {
    border-bottom: 1px solid var(--primary-color);
}
```

### Text Styling

```css
.text {
    /* Font */
    font-family: 'Montserrat', Arial, sans-serif;
    font-size: 16px;
    font-weight: bold;      /* or 100-900 */
    font-style: italic;

    /* Text properties */
    color: black;
    text-align: center;     /* left, right, center, justify */
    text-decoration: underline; /* none, underline, line-through */
    text-transform: uppercase;  /* lowercase, capitalize */
    line-height: 1.5;       /* Space between lines */
    letter-spacing: 2px;    /* Space between letters */
}
```

**From your template CSS** (`proposta_styles.css:69-79`):
```css
.watermark-text {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 120pt;
    font-weight: 900;
    color: rgba(0, 0, 0, 0.03);
    z-index: -999;
    pointer-events: none;
}
```

### Borders

```css
.box {
    /* Shorthand: width style color */
    border: 1px solid black;

    /* Individual sides */
    border-top: 2px solid red;
    border-bottom: 1px dashed blue;

    /* Individual properties */
    border-width: 2px;
    border-style: solid;  /* solid, dashed, dotted, none */
    border-color: blue;

    /* Rounded corners */
    border-radius: 5px;
}
```

**From your template CSS** (`proposta_styles.css:86`):
```css
border-bottom: 1.2px solid var(--primary-color);
```

### Display and Layout

```css
.element {
    /* Display type */
    display: block;        /* Takes full width */
    display: inline;       /* Only takes content width */
    display: inline-block; /* Block features, inline flow */
    display: none;         /* Hide element */

    /* Visibility */
    visibility: hidden;    /* Hidden but takes space */
    opacity: 0.5;          /* 50% transparent */
}
```

### Positioning

```css
.element {
    position: static;      /* Default, normal flow */
    position: relative;    /* Relative to normal position */
    position: absolute;    /* Relative to parent */
    position: fixed;       /* Relative to viewport */

    /* Positioning properties (with non-static position) */
    top: 10px;
    right: 20px;
    bottom: 30px;
    left: 40px;

    /* Stacking order */
    z-index: 10;           /* Higher = on top */
}
```

**From your template CSS** (`proposta_styles.css:53-62`):
```css
.watermark-container {
    position: fixed;
    top: 50%;
    left: 70%; /* Descentralizado para efeito estético */
    transform: translate(-50%, -50%);
    z-index: -1000;
    pointer-events: none;
    width: 140%; /* Maior que o documento */
    opacity: 0.05; /* Mais sutil por ser maior */
}
```

**Explanation**:
- `position: fixed` - Stays in same place even when scrolling
- `top: 50%; left: 70%` - Position from top and left
- `transform: translate(-50%, -50%)` - Centers the element
- `z-index: -1000` - Behind all content
- `opacity: 0.05` - Very transparent (5% visible)

---

## Print-Specific CSS

### @page Rule (PDF Layout)

**From your template CSS** (`proposta_styles.css:1-12`):
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

**Explanation**:
- `size: A4` - Paper size
- `margin: 20mm 15mm 30mm 15mm` - Top, right, bottom, left margins
- `@top-center` - Places header at top of every page
- `@bottom-center` - Places footer at bottom of every page

**First page different** (`proposta_styles.css:14-19`):
```css
@page :first {
    margin-top: 10mm;
    @top-center {
        content: none;
    }
}
```
First page has smaller top margin and no header.

### Print Media Query

**From your template CSS** (`proposta_styles.css:21-26`):
```css
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```

**Explanation**:
- `@media print` - Only applies when printing/generating PDF
- `print-color-adjust: exact` - Preserves exact colors (prevents browser from changing colors)

### Running Headers/Footers

**From your template CSS** (`proposta_styles.css:82-89`):
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

**Explanation**:
- `position: running(header)` - Makes this element a running header
- Paired with `@page { @top-center { content: element(header); } }`
- Header appears on every page (except first, which has `content: none`)

---

## Understanding the Proposal Template

### Template Structure Overview

```
┌────────────────────────────────────┐
│ [First Page Only]                  │
│ • Large Logo                       │
│ • Quote Number                     │
│ • Date                             │
├────────────────────────────────────┤
│ [Every Page]                       │
│ • Watermark (behind content)       │
│ • "RASCUNHO" text (if draft)       │
├────────────────────────────────────┤
│ [Header - Pages 2+]                │
│ • Small Logo + Quote # + Date      │
├────────────────────────────────────┤
│ [Main Content Area]                │
│ • Client info                      │
│ • Items table                      │
│ • Terms and conditions             │
│ • Signatures                       │
├────────────────────────────────────┤
│ [Footer - Every Page]              │
│ • Company name, CNPJ               │
│ • Address (clickable map link)     │
│ • Phone, email, website            │
│ • Association logos                │
└────────────────────────────────────┘
```

### Key Template Sections

#### 1. Page Header (Repeated on Pages 2+)

**HTML** (`proposta_base.html:15-31`):
```html
<header id="page-header">
    <table class="header-table">
        <tr>
            <td class="header-td-logo">
                <img src="..." class="header-logo-compact">
            </td>
            <td class="header-td-info">
                <div class="header-num-orc-compact">ORÇAMENTO {{ numero_orcamento }}</div>
                <div class="header-data-compact">{{ cidade }}, {{ data_extenso }}</div>
            </td>
        </tr>
    </table>
</header>
```

**CSS**:
```css
header#page-header {
    position: running(header);  /* Makes it a running header */
    width: 180mm;
    border-bottom: 1.2px solid var(--primary-color);
}
```

#### 2. Watermark

**HTML** (`proposta_base.html:34-42`):
```html
<div class="watermark-container">
    {% if marca_dagua_base64 %}
    <img src="data:image/png;base64,{{ marca_dagua_base64 }}" class="watermark-img">
    {% endif %}
</div>

{% if rascunho %}
<div class="watermark-text">RASCUNHO</div>
{% endif %}
```

**CSS**:
```css
.watermark-container {
    position: fixed;        /* Fixed position */
    top: 50%;
    left: 70%;
    transform: translate(-50%, -50%);
    z-index: -1000;         /* Behind all content */
    opacity: 0.05;          /* Very transparent */
}

.watermark-text {
    position: fixed;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 120pt;
    color: rgba(0, 0, 0, 0.03);  /* Almost invisible */
}
```

#### 3. Footer (Repeated on Every Page)

**HTML** (`proposta_base.html:45-75`):
```html
<footer>
    <div class="footer-content">
        <div class="footer-info">
            <div>
                <span class="rodape-empresa">{{ empresa.razao_social }}</span>
                <span class="separador">|</span>
                <span>CNPJ: {{ empresa.cnpj }}</span>
            </div>
            <!-- Address, phone, email, website -->
        </div>
        <div class="footer-logos">
            <!-- Association logos -->
        </div>
    </div>
</footer>
```

---

## Modifying the Template

### Common Modifications

#### 1. Change Colors

**Edit** `proposta_styles.css` lines 28-36:
```css
:root {
    --primary-color: #0A94D6;    /* Change to your brand color */
    --secondary-color: #00A859;   /* Change to your accent color */
}
```

#### 2. Change Font

**Edit** `proposta_base.html` line 8:
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Edit** `proposta_styles.css` line 45:
```css
body {
    font-family: 'Roboto', Arial, sans-serif;
}
```

#### 3. Adjust Margins

**Edit** `proposta_styles.css` line 3:
```css
@page {
    size: A4;
    margin: 20mm 15mm 30mm 15mm;  /* Top, right, bottom, left */
}
```

#### 4. Change Font Size

**Edit** `proposta_styles.css` line 46:
```css
body {
    font-size: 8.8pt;  /* Increase or decrease */
}
```

#### 5. Hide Watermark

**Edit** `proposta_styles.css`:
```css
.watermark-container {
    display: none;  /* Add this line */
}
```

---

## Quick Reference

### Common CSS Units

| Unit | Description | Example |
|------|-------------|---------|
| `px` | Pixels (absolute) | `16px` |
| `pt` | Points (print) | `12pt` |
| `%` | Percentage of parent | `50%` |
| `em` | Relative to font size | `1.5em` |
| `rem` | Relative to root font | `2rem` |
| `mm` | Millimeters (print) | `20mm` |

### Color Formats

```css
color: red;                     /* Named color */
color: #FF0000;                 /* Hex */
color: rgb(255, 0, 0);          /* RGB */
color: rgba(255, 0, 0, 0.5);    /* RGBA (with transparency) */
```

### Common Properties

```css
/* Text */
color, font-size, font-weight, font-family, text-align

/* Box Model */
width, height, padding, margin, border

/* Background */
background-color, background-image

/* Display */
display, visibility, opacity

/* Position */
position, top, left, bottom, right, z-index
```

---

## Next Steps

Now that you understand HTML/CSS:
1. ✅ Open `templates/html/proposta_base.html` and identify all sections
2. ✅ Open `templates/html/proposta_styles.css` and find color definitions
3. ✅ Try changing `--primary-color` and regenerate PDF
4. ✅ Experiment with font sizes
5. ✅ Move on to WeasyPrint guide to understand PDF generation

**Practice Exercise**: Try changing the primary color from blue (#0A94D6) to your favorite color and regenerate the test PDF!

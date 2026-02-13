# openpyxl Excel Generation Guide

**Purpose**: Learn how to create and manipulate Excel files with Python using openpyxl.

---

## Table of Contents
1. [What is openpyxl?](#what-is-openpyxl)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Working with Cells](#working-with-cells)
5. [Styling Cells](#styling-cells)
6. [Working with Rows and Columns](#working-with-rows-and-columns)
7. [Formulas and Calculations](#formulas-and-calculations)
8. [How This Project Uses openpyxl](#how-this-project-uses-openpyxl)
9. [Quick Reference](#quick-reference)

---

## What is openpyxl?

**openpyxl** is a Python library for reading and writing Excel 2010+ files (.xlsx, .xlsm).

**What you can do**:
- Create new Excel workbooks
- Add/modify worksheets
- Write data to cells
- Apply formatting (colors, fonts, borders)
- Create formulas
- Set column widths, row heights
- Merge cells
- Read existing Excel files

**In this project**: openpyxl generates internal cost breakdown spreadsheets for tracking budgeted vs. actual costs.

---

## Installation

```bash
pip install openpyxl
```

**Check installation**:
```python
import openpyxl
print(openpyxl.__version__)  # Should show version number
```

---

## Basic Usage

### Creating a New Workbook

```python
from openpyxl import Workbook

# Create new workbook
wb = Workbook()

# Get active worksheet
ws = wb.active

# Write to cell
ws['A1'] = 'Hello'
ws['B1'] = 'World'

# Save workbook
wb.save('output.xlsx')
```

**Result**: Creates `output.xlsx` with "Hello" in A1 and "World" in B1.

### Reading an Existing Workbook

```python
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')

# Get worksheet
ws = wb.active  # or wb['SheetName']

# Read cell
value = ws['A1'].value
print(value)

# Modify and save
ws['A2'] = 'New value'
wb.save('modified.xlsx')
```

### Working with Multiple Sheets

```python
from openpyxl import Workbook

wb = Workbook()

# Create new sheets
ws1 = wb.active
ws1.title = "Summary"  # Rename active sheet

ws2 = wb.create_sheet("Details")  # Create new sheet
ws3 = wb.create_sheet("Materials", 0)  # Insert at position 0

# Access sheets by name
summary = wb["Summary"]
details = wb["Details"]

# List all sheet names
print(wb.sheetnames)  # ['Materials', 'Summary', 'Details']

wb.save('multi_sheet.xlsx')
```

---

## Working with Cells

### Writing to Cells

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Method 1: By cell reference
ws['A1'] = 'Name'
ws['B1'] = 'Age'
ws['C1'] = 'City'

# Method 2: By row and column (1-indexed)
ws.cell(row=1, column=1, value='Name')
ws.cell(row=1, column=2, value='Age')

# Method 3: Using variables
row = 2
col = 1
ws.cell(row, col, 'João')
ws.cell(row, col+1, 30)
ws.cell(row, col+2, 'Porto Alegre')

wb.save('output.xlsx')
```

**From your code** (`hvac/generators/planilha_interna.py` - pattern):
```python
# Write header
ws.cell(row=1, column=1, value='Descrição')
ws.cell(row=1, column=2, value='Quantidade')
ws.cell(row=1, column=3, value='Valor Unit.')
```

### Writing Data in Loops

```python
wb = Workbook()
ws = wb.active

# Write headers
headers = ['Name', 'Age', 'City']
for col_num, header in enumerate(headers, 1):
    ws.cell(1, col_num, header)

# Write data rows
data = [
    ['João', 30, 'Porto Alegre'],
    ['Maria', 25, 'São Paulo'],
    ['Pedro', 35, 'Rio de Janeiro']
]

for row_num, row_data in enumerate(data, 2):  # Start at row 2
    for col_num, cell_value in enumerate(row_data, 1):
        ws.cell(row_num, col_num, cell_value)

wb.save('output.xlsx')
```

### Reading Cells

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Read single cell
value = ws['A1'].value

# Read by row/column
value = ws.cell(row=1, column=1).value

# Iterate through rows
for row in ws.iter_rows(min_row=2, max_row=10, values_only=True):
    print(row)  # Tuple of cell values

# Iterate through columns
for col in ws.iter_cols(min_col=1, max_col=3, values_only=True):
    print(col)
```

---

## Styling Cells

### Fonts

```python
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active

# Apply font to cell
ws['A1'] = 'Bold Red Text'
ws['A1'].font = Font(bold=True, color='FF0000', size=14)

# Different font styles
ws['A2'] = 'Italic'
ws['A2'].font = Font(italic=True)

ws['A3'] = 'Bold Italic'
ws['A3'].font = Font(bold=True, italic=True, size=12)

wb.save('styled.xlsx')
```

**From your code** (`hvac/generators/planilha_interna.py:50`):
```python
estilo_cabecalho.font = Font(bold=True, color="FFFFFF", size=10)
```

### Fill (Background Color)

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill

wb = Workbook()
ws = wb.active

# Blue background
ws['A1'] = 'Blue Background'
ws['A1'].fill = PatternFill(start_color="00A0E3", end_color="00A0E3", fill_type="solid")

# Yellow background
ws['A2'] = 'Yellow Background'
ws['A2'].fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

wb.save('colored.xlsx')
```

**From your code** (`hvac/generators/planilha_interna.py:51`):
```python
estilo_cabecalho.fill = PatternFill(start_color=AZUL_ARMANT, end_color=AZUL_ARMANT, fill_type="solid")
```

**Color constants in your project**:
```python
AZUL_ARMANT = "00A0E3"
CINZA_CLARO = "F0F0F0"
CINZA_MEDIO = "E0E0E0"
VERDE_POSITIVO = "C6EFCE"
VERMELHO_NEGATIVO = "FFC7CE"
```

### Borders

```python
from openpyxl import Workbook
from openpyxl.styles import Border, Side

wb = Workbook()
ws = wb.active

# Define border style
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# Apply to cell
ws['A1'] = 'Bordered Cell'
ws['A1'].border = thin_border

wb.save('bordered.xlsx')
```

**Border styles**: `'thin'`, `'medium'`, `'thick'`, `'dashed'`, `'dotted'`, `'double'`

**From your code** (`hvac/generators/planilha_interna.py:39-44`):
```python
borda_fina = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
```

### Alignment

```python
from openpyxl import Workbook
from openpyxl.styles import Alignment

wb = Workbook()
ws = wb.active

# Center align
ws['A1'] = 'Centered'
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

# Right align
ws['A2'] = 'Right Aligned'
ws['A2'].alignment = Alignment(horizontal='right')

# Wrap text
ws['A3'] = 'This is a very long text that should wrap'
ws['A3'].alignment = Alignment(wrap_text=True)

wb.save('aligned.xlsx')
```

**Horizontal options**: `'left'`, `'center'`, `'right'`, `'justify'`
**Vertical options**: `'top'`, `'center'`, `'bottom'`

**From your code** (`hvac/generators/planilha_interna.py:52`):
```python
estilo_cabecalho.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
```

### Named Styles (Reusable Styles)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, NamedStyle

wb = Workbook()
ws = wb.active

# Create named style
header_style = NamedStyle(name="header")
header_style.font = Font(bold=True, color="FFFFFF", size=12)
header_style.fill = PatternFill(start_color="0070C0", end_color="0070C0", fill_type="solid")
header_style.border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
header_style.alignment = Alignment(horizontal='center', vertical='center')

# Add to workbook
wb.add_named_style(header_style)

# Apply to cells
ws['A1'] = 'Name'
ws['A1'].style = 'header'

ws['B1'] = 'Age'
ws['B1'].style = 'header'

wb.save('styled_header.xlsx')
```

**From your code** (`hvac/generators/planilha_interna.py:49-55`):
```python
estilo_cabecalho = NamedStyle(name="cabecalho")
estilo_cabecalho.font = Font(bold=True, color="FFFFFF", size=10)
estilo_cabecalho.fill = PatternFill(start_color=AZUL_ARMANT, end_color=AZUL_ARMANT, fill_type="solid")
estilo_cabecalho.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
estilo_cabecalho.border = borda_fina
wb.add_named_style(estilo_cabecalho)
```

---

## Working with Rows and Columns

### Column Width and Row Height

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Set column width
ws.column_dimensions['A'].width = 30  # Width in characters
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 20

# Set row height
ws.row_dimensions[1].height = 25  # Height in points

ws['A1'] = 'Wide column'
ws['B1'] = 'Medium'
ws['C1'] = 'Also wide'

wb.save('sized.xlsx')
```

**Using column letters**:
```python
from openpyxl.utils import get_column_letter

for col_num in range(1, 10):
    col_letter = get_column_letter(col_num)
    ws.column_dimensions[col_letter].width = 15
```

### Appending Rows

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Append rows
ws.append(['Name', 'Age', 'City'])
ws.append(['João', 30, 'Porto Alegre'])
ws.append(['Maria', 25, 'São Paulo'])

wb.save('appended.xlsx')
```

### Merging Cells

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Merge cells
ws.merge_cells('A1:C1')
ws['A1'] = 'Merged Header'

# Merge by range
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=3)
ws['A2'] = 'Another merged cell'

wb.save('merged.xlsx')
```

---

## Formulas and Calculations

### Writing Formulas

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Data
ws['A1'] = 'Item'
ws['B1'] = 'Price'
ws['C1'] = 'Quantity'
ws['D1'] = 'Total'

ws['A2'] = 'Tube'
ws['B2'] = 25.50
ws['C2'] = 10

# Formula (Excel will calculate)
ws['D2'] = '=B2*C2'

# Sum formula
ws['A3'] = 'Grand Total'
ws['D3'] = '=SUM(D2:D2)'  # In real use, range would be larger

wb.save('formulas.xlsx')
```

**Important**:
- Formulas are strings starting with `=`
- Excel calculates them when you open the file
- Python doesn't evaluate formulas

### Number Formatting

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Currency format
ws['A1'] = 1250.50
ws['A1'].number_format = 'R$ #,##0.00'

# Percentage
ws['A2'] = 0.15
ws['A2'].number_format = '0.00%'

# Date
from datetime import date
ws['A3'] = date(2025, 12, 18)
ws['A3'].number_format = 'DD/MM/YYYY'

wb.save('formatted_numbers.xlsx')
```

---

## How This Project Uses openpyxl

### Project Structure

**File**: `hvac/generators/planilha_interna.py`

**Purpose**: Generates internal cost tracking spreadsheet with:
- Hierarchical item structure
- Consolidated material/labor lists
- Budgeted vs. actual cost tracking

### Key Components

**1. Create Styles** (`planilha_interna.py:36-80`):
```python
def criar_estilos(wb: Workbook) -> Dict[str, NamedStyle]:
    """Cria estilos padronizados para a planilha"""

    # Define border
    borda_fina = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Header style
    estilo_cabecalho = NamedStyle(name="cabecalho")
    estilo_cabecalho.font = Font(bold=True, color="FFFFFF", size=10)
    estilo_cabecalho.fill = PatternFill(start_color=AZUL_ARMANT, end_color=AZUL_ARMANT, fill_type="solid")
    estilo_cabecalho.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    estilo_cabecalho.border = borda_fina
    wb.add_named_style(estilo_cabecalho)

    # Group style
    estilo_grupo = NamedStyle(name="grupo")
    estilo_grupo.font = Font(bold=True, size=10)
    estilo_grupo.fill = PatternFill(start_color=CINZA_MEDIO, end_color=CINZA_MEDIO, fill_type="solid")
    estilo_grupo.border = borda_fina
    wb.add_named_style(estilo_grupo)

    # More styles...
    return {"cabecalho": estilo_cabecalho, "grupo": estilo_grupo, ...}
```

**2. Create Workbook and Worksheet**:
```python
wb = Workbook()
ws = wb.active
ws.title = "Orçamento Detalhado"
```

**3. Write Headers**:
```python
headers = ['Descrição', 'Unidade', 'Quantidade', 'Valor Unit.', 'Valor Total']
for col_num, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_num, value=header)
    cell.style = 'cabecalho'
```

**4. Write Data with Styling**:
```python
row_num = 2
for item in itens:
    ws.cell(row_num, 1, item['descricao']).style = 'item'
    ws.cell(row_num, 2, item['unidade']).style = 'item'
    ws.cell(row_num, 3, item['quantidade']).style = 'item'
    ws.cell(row_num, 4, item['valor_unitario']).style = 'item'
    ws.cell(row_num, 5, f"=C{row_num}*D{row_num}").style = 'item'  # Formula
    row_num += 1
```

**5. Adjust Column Widths**:
```python
ws.column_dimensions['A'].width = 50
ws.column_dimensions['B'].width = 10
ws.column_dimensions['C'].width = 12
ws.column_dimensions['D'].width = 15
ws.column_dimensions['E'].width = 15
```

**6. Save Workbook**:
```python
output_path = Path("output") / "planilha_interna.xlsx"
wb.save(output_path)
```

### Complete Workflow

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, NamedStyle

def gerar_planilha_interna(precificado, output_path=None):
    """Generate internal cost tracking spreadsheet."""

    # 1. Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Custos Detalhados"

    # 2. Create styles
    estilos = criar_estilos(wb)

    # 3. Write headers
    headers = ['Descrição', 'Qtd', 'Valor Unit.', 'Total']
    for col, header in enumerate(headers, 1):
        ws.cell(1, col, header).style = 'cabecalho'

    # 4. Write data
    row = 2
    for item in precificado['itens_precificados']:
        ws.cell(row, 1, item['descricao'])
        ws.cell(row, 2, item['quantidade'])
        ws.cell(row, 3, item['valor_unitario'])
        ws.cell(row, 4, f"=B{row}*C{row}")  # Formula
        row += 1

    # 5. Adjust widths
    ws.column_dimensions['A'].width = 50

    # 6. Save
    wb.save(output_path)

    return {"sucesso": True, "arquivo": output_path}
```

---

## Quick Reference

### Basic Operations

```python
from openpyxl import Workbook, load_workbook

# Create workbook
wb = Workbook()
ws = wb.active

# Write data
ws['A1'] = 'Hello'
ws.cell(1, 2, 'World')

# Read data
value = ws['A1'].value
value = ws.cell(1, 1).value

# Save
wb.save('output.xlsx')

# Load existing
wb = load_workbook('file.xlsx')
```

### Styling

```python
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

# Font
cell.font = Font(bold=True, color='FF0000', size=14)

# Fill
cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

# Border
cell.border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# Alignment
cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
```

### Sheets

```python
# Create sheet
ws = wb.create_sheet("NewSheet")

# Rename sheet
ws.title = "Renamed"

# Access by name
ws = wb["SheetName"]

# List sheets
print(wb.sheetnames)
```

### Columns and Rows

```python
# Column width
ws.column_dimensions['A'].width = 30

# Row height
ws.row_dimensions[1].height = 25

# Merge cells
ws.merge_cells('A1:C1')

# Append row
ws.append(['Col1', 'Col2', 'Col3'])
```

---

## Next Steps

Now that you understand openpyxl:
1. ✅ Look at `hvac/generators/planilha_interna.py` for the complete implementation
2. ✅ Try generating a simple Excel file with Python
3. ✅ Experiment with different styles and formats
4. ✅ Move on to Bash scripting guide to learn automation

**Practice Exercise**: Create a simple Excel file with a header row (blue background, white bold text) and 3 data rows!

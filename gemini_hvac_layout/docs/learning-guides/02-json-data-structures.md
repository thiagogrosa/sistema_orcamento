# JSON Data Structures Guide

**Purpose**: Learn how JSON works and understand all the data files in this HVAC project.

---

## Table of Contents
1. [What is JSON?](#what-is-json)
2. [JSON Syntax Rules](#json-syntax-rules)
3. [JSON Data Types](#json-data-types)
4. [Working with JSON in Python](#working-with-json-in-python)
5. [Project Data Structure: Base Files](#project-data-structure-base-files)
6. [Project Data Structure: Configuration Files](#project-data-structure-configuration-files)
7. [Project Data Structure: Test/Input Files](#project-data-structure-testinput-files)
8. [Common Patterns](#common-patterns)
9. [Validating and Debugging JSON](#validating-and-debugging-json)

---

## What is JSON?

**JSON** = **J**ava**S**cript **O**bject **N**otation

- A text format for storing and exchanging data
- Human-readable (you can open and edit in any text editor)
- Language-independent (works with Python, JavaScript, Java, etc.)
- Based on key-value pairs

**Example**:
```json
{
  "nome": "João Silva",
  "idade": 30,
  "ativo": true
}
```

---

## JSON Syntax Rules

### 1. **Structure**
- Data is in **key-value pairs**: `"key": value`
- Data is separated by **commas**: `,`
- **Curly braces** `{}` hold objects
- **Square brackets** `[]` hold arrays
- Keys **must be strings** in double quotes

### 2. **Valid JSON vs. Invalid**

✅ **Valid JSON**:
```json
{
  "nome": "Tubo",
  "preco": 25.50,
  "disponivel": true,
  "categorias": ["Material", "Tubulacao"]
}
```

❌ **Invalid JSON** (common mistakes):
```json
{
  nome: "Tubo",              // ❌ Key must have quotes
  "preco": 25,50,            // ❌ No comma in numbers (use 25.50)
  "disponivel": True,        // ❌ Must be lowercase: true
  "categorias": ['Material'] // ❌ Must use double quotes
}
```

### 3. **Comments**
- **JSON does not support comments!**
- If you need comments, you can add a `"_comment"` field:
```json
{
  "_comment": "This is a workaround for commenting",
  "preco": 25.50
}
```

### 4. **Trailing Commas**
❌ **Not allowed**:
```json
{
  "nome": "Tubo",
  "preco": 25.50,  // ❌ Last item cannot have comma
}
```

✅ **Correct**:
```json
{
  "nome": "Tubo",
  "preco": 25.50
}
```

---

## JSON Data Types

### 1. **String** (text)
```json
{
  "descricao": "Tubo de cobre 1/4\" flexivel",
  "unidade": "M",
  "codigo": "TUB_14_FLEX"
}
```
- Always in **double quotes**
- Escape special characters: `\"` for quotes, `\\` for backslash

### 2. **Number** (integer or decimal)
```json
{
  "quantidade": 10,
  "preco": 25.50,
  "margem": 0.15,
  "negativo": -5
}
```
- No quotes around numbers
- Use `.` for decimals (not `,`)

### 3. **Boolean** (true/false)
```json
{
  "disponivel": true,
  "descontinuado": false
}
```
- Must be lowercase: `true` or `false`
- No quotes

### 4. **Null** (no value)
```json
{
  "observacao": null,
  "data_entrega": null
}
```
- Represents "no value" or "empty"
- Must be lowercase: `null`

### 5. **Object** (key-value pairs)
```json
{
  "endereco": {
    "logradouro": "Avenida Polônia, 764",
    "bairro": "São Geraldo",
    "cidade": "Porto Alegre",
    "estado": "RS",
    "cep": "90230-090"
  }
}
```
- Objects inside objects (nesting)
- Each object in `{}`

### 6. **Array** (list of values)
```json
{
  "categorias": ["Material", "Tubulacao", "Eletrica"],
  "precos": [10.50, 25.00, 42.75],
  "disponivel_em": ["RS", "SC", "PR"]
}
```
- Arrays in `[]`
- Can contain any type (strings, numbers, objects, etc.)

### 7. **Array of Objects**
```json
{
  "materiais": [
    {
      "codigo": "TUB_14",
      "descricao": "Tubo 1/4\"",
      "preco": 18.00
    },
    {
      "codigo": "TUB_38",
      "descricao": "Tubo 3/8\"",
      "preco": 28.00
    }
  ]
}
```

---

## Working with JSON in Python

### Loading JSON Files

```python
import json

# Method 1: Read JSON file
with open("bases/materiais.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)  # Returns dict or list

# Method 2: Parse JSON string
json_string = '{"nome": "João", "idade": 30}'
dados = json.loads(json_string)  # Returns dict

# Accessing data
print(dados["nome"])        # "João"
print(dados.get("idade"))   # 30
```

**From your code** (`hvac/utils/loader.py:20`):
```python
def carregar_json(caminho):
    """Loads a JSON file."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
```

### Saving JSON Files

```python
import json

dados = {
    "nome": "João Silva",
    "idade": 30,
    "ativo": True
}

# Method 1: Write to file
with open("saida.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=2, ensure_ascii=False)
    # indent=2: pretty formatting with 2-space indentation
    # ensure_ascii=False: allow Portuguese characters (á, ç, ã, etc.)

# Method 2: Convert to JSON string
json_string = json.dumps(dados, indent=2, ensure_ascii=False)
print(json_string)
```

### Common Operations

```python
import json

# Load JSON
with open("bases/materiais.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Access nested data
material = dados["materiais"]["TUB_14_FLEX"]
preco = material["preco"]  # 18.00

# Modify data
material["preco"] = 20.00

# Add new material
dados["materiais"]["TUB_NEW"] = {
    "categoria": "Tubulacao",
    "descricao": "Tubo novo",
    "unidade": "M",
    "preco": 15.00
}

# Save back to file
with open("bases/materiais.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)
```

---

## Project Data Structure: Base Files

### 1. **materiais.json** - Materials Catalog

**Location**: `bases/materiais.json`

**Structure**:
```json
{
  "materiais": {
    "TUB_14_FLEX": {
      "categoria": "Tubulacao",
      "descricao": "Tubo de cobre 1/4\" flexivel",
      "unidade": "M",
      "preco": 18.00,
      "data_atualizacao": "2025-12-30",
      "validade_dias": 7
    },
    "TUB_38_FLEX": {
      "categoria": "Tubulacao",
      "descricao": "Tubo de cobre 3/8\" flexivel",
      "unidade": "M",
      "preco": 28.00,
      "data_atualizacao": "2025-12-30",
      "validade_dias": 7
    }
  }
}
```

**Field Meanings**:
- `TUB_14_FLEX` - **Material code** (unique identifier, used as key)
- `categoria` - **Category** (for grouping and applying different margins)
- `descricao` - **Description** (appears in proposal)
- `unidade` - **Unit** (M = meter, UN = unit, PC = piece, etc.)
- `preco` - **Unit price** in Brazilian Reais (R$)
- `data_atualizacao` - **Last update date** (for price tracking)
- `validade_dias` - **Days until price expires**

**How to use**:
```python
from hvac.utils.loader import carregar_json

materiais = carregar_json("bases/materiais.json")
tubo = materiais["materiais"]["TUB_14_FLEX"]
preco = tubo["preco"]  # 18.00
descricao = tubo["descricao"]  # "Tubo de cobre 1/4\" flexivel"
```

### 2. **mao_de_obra.json** - Labor Rates

**Structure**:
```json
{
  "mao_de_obra": {
    "INSTALADOR_CLIMA": {
      "categoria": "Profissional",
      "descricao": "Instalador de ar-condicionado",
      "unidade": "H",
      "preco_hora": 85.00,
      "encargos_percentual": 0.82
    },
    "ELETRICISTA": {
      "categoria": "Profissional",
      "descricao": "Eletricista",
      "unidade": "H",
      "preco_hora": 90.00,
      "encargos_percentual": 0.82
    }
  }
}
```

**Field Meanings**:
- `preco_hora` - **Hourly rate**
- `encargos_percentual` - **Labor charges** (taxes, benefits, etc. - 82% additional)
- `unidade` - "H" = hours

### 3. **equipamentos.json** - HVAC Equipment

**Structure**:
```json
{
  "equipamentos": {
    "CASSETE_60K_INVERTER": {
      "categoria": "Equipamento",
      "descricao": "Ar-condicionado tipo cassete inverter 60.000 BTU/h",
      "unidade": "UN",
      "potencia_btu": 60000,
      "tipo": "cassete",
      "tecnologia": "inverter",
      "preco": 8500.00,
      "marca": "Midea",
      "modelo": "MCD-60HRN1-Q0E0"
    }
  }
}
```

**Field Meanings**:
- `potencia_btu` - **Cooling capacity** in BTUs
- `tipo` - **Type** (cassete, split, etc.)
- `tecnologia` - **Technology** (inverter, on-off)

### 4. **composicoes.json** - Service Compositions

**Structure**:
```json
{
  "composicoes": {
    "INST_CASSETE_60K": {
      "categoria": "Composicao",
      "descricao": "Instalacao completa cassete 60k BTU",
      "unidade": "CJ",
      "componentes": [
        {
          "tipo": "MATERIAL",
          "codigo": "TUB_38_FLEX",
          "quantidade": 40
        },
        {
          "tipo": "MATERIAL",
          "codigo": "TUB_58_FLEX",
          "quantidade": 40
        },
        {
          "tipo": "MAO_DE_OBRA",
          "codigo": "INSTALADOR_CLIMA",
          "quantidade": 8
        }
      ]
    }
  }
}
```

**How it works**:
- A **composition** is a bundle of materials and labor
- The `compositor.py` expands compositions into individual items
- Example: "INST_CASSETE_60K" expands into 40m of 3/8" tube + 40m of 5/8" tube + 8 hours of labor

### 5. **bdi.json** - Markup/Margin Rules

**Structure**:
```json
{
  "Tubulacao": 0.25,
  "Eletrica": 0.30,
  "Equipamento": 0.15,
  "Profissional": 0.20,
  "DEFAULT": 0.20
}
```

**BDI** = "Benefícios e Despesas Indiretas" (Indirect Benefits and Expenses)

**Field Meanings**:
- Key = **Category** (matches `categoria` from other files)
- Value = **Markup percentage** (0.25 = 25% profit margin)
- `DEFAULT` = **Fallback** if category not found

**How it works**:
```python
# If item has categoria="Tubulacao" and custo=100.00
# Margin = 0.25 (25%)
# valor_venda = 100.00 * (1 + 0.25) = 125.00
```

---

## Project Data Structure: Configuration Files

### 1. **empresa.json** - Company Information

**Location**: `config/empresa.json`

**Structure**:
```json
{
  "razao_social": "ARMANT SOLUÇÕES EM CLIMATIZAÇÃO LTDA",
  "nome_fantasia": "Armant",
  "endereco": {
    "logradouro": "Avenida Polônia, 764",
    "bairro": "São Geraldo",
    "cidade": "Porto Alegre",
    "estado": "RS",
    "cep": "90230-090"
  },
  "endereco_linha": "Avenida Polônia, 764 | Bairro São Geraldo | Porto Alegre | RS",
  "cnpj": "13.591.585/0001-03",
  "telefone": "(51) 3085.8050",
  "email": "armant@armant.com.br",
  "site": "www.armant.com.br",
  "crea": "206773",
  "logo_path": "templates/html/logo_armant.png",
  "assinaturas": [
    {
      "nome": "Rodrigo G. Donni",
      "cargo": "Engenheiro Mecânico",
      "registro": "CREA-RS 131427",
      "assinatura_img": "templates/html/assinatura_rodrigo.png"
    },
    {
      "nome": "Daniel Albuquerque",
      "cargo": "Sócio Administrador",
      "registro": "CREA-RS 206773",
      "assinatura_img": "templates/html/assinatura_daniel.png"
    }
  ],
  "destaques": [
    "Empresa registrada no CREA-RS 206773 - ASBRAV.",
    "Todas as tubulações em cobre.",
    "01 (Um) ano de garantia dos serviços de instalação.",
    "Mais de 10.000 equipamentos instalados.",
    "Mão de obra qualificada."
  ]
}
```

**Field Meanings**:
- `razao_social` - **Legal company name**
- `nome_fantasia` - **Trade name**
- `endereco` - **Nested object** with address components
- `assinaturas` - **Array of objects** (multiple signatories)
- `destaques` - **Array of strings** (company highlights)

**Accessing nested data**:
```python
empresa = carregar_json("config/empresa.json")
cnpj = empresa["cnpj"]                      # "13.591.585/0001-03"
cidade = empresa["endereco"]["cidade"]       # "Porto Alegre"
primeiro_assinante = empresa["assinaturas"][0]["nome"]  # "Rodrigo G. Donni"
destaque1 = empresa["destaques"][0]          # "Empresa registrada..."
```

### 2. **condicoes_comerciais.json** - Commercial Terms

**Structure**:
```json
{
  "default": {
    "validade_dias": 10,
    "prazo_execucao": "A combinar.",
    "forma_pagamento": "Entrada de 40% e saldo na conclusão dos serviços.",
    "garantia": "01 (Um) ano de garantia dos serviços de instalação."
  },
  "por_tipo_cliente": {
    "PRIVADO-PJ": {
      "forma_pagamento": "Entrada de 40% e saldo na conclusão."
    },
    "PRIVADO-PF": {
      "forma_pagamento": "50% de entrada e 50% na conclusão.",
      "validade_dias": 7
    },
    "GOVERNO": {
      "validade_dias": 60,
      "forma_pagamento": "Conforme edital."
    }
  }
}
```

**How it works**:
1. System loads `default` values
2. If client has `tipo_cliente`, it overrides with values from `por_tipo_cliente`
3. Example: GOVERNO client gets 60 days validity instead of 10

### 3. **contador.json** - Quote Number Sequencer

**Structure**:
```json
{
  "proximo_numero": 1024
}
```

**How it works**:
- Auto-incremented each time a proposal is generated
- Creates sequential quote numbers (1024, 1025, 1026, etc.)
- **Important**: This file is in `.gitignore` (not tracked in git)

---

## Project Data Structure: Test/Input Files

### Input File Format

**Location**: `tests/dados_teste_panvel.json`

**Structure**:
```json
{
  "projeto": "Instalacao de Ar-Condicionado",
  "cliente": "Grupo Panvel Farmacias",
  "tipo_cliente": "PRIVADO-PJ",
  "data_orcamento": "2025-12-18",
  "validade_dias": 10,
  "dados_cliente": {
    "razao_social": "Grupo Panvel Farmacias",
    "cnpj": "92.665.611/0322-90",
    "endereco": "Av. Industrial Belgraf, 865 - Bairro Industrial, Eldorado do Sul - RS, 92990-000",
    "contato_nome": "Paulo Ficks",
    "contato_email": "pficks@grupopanvel.com.br",
    "contato_telefone": "51 3481-9885"
  },
  "referencia": "Instalacao de Ar-Condicionado",
  "itens_precificados": [
    {
      "id": 1,
      "descricao": "Instalacao de equipamento tipo cassete de 60.000 BTU/h...",
      "composicao": "INST-CASSETE-60K",
      "quantidade": 1,
      "unidade": "pc",
      "tipo_servico": "instalacao-completa",
      "materiais": [
        {
          "codigo": "TUB-CU-3/8",
          "descricao": "Tubo cobre 3/8\"",
          "quantidade": 40,
          "unidade": "m",
          "preco_unitario": 45.00,
          "custo": 1800.00
        }
      ],
      "mao_de_obra": [
        {
          "codigo": "INSTALADOR",
          "descricao": "Instalador",
          "quantidade": 8,
          "unidade": "h",
          "preco_unitario": 85.00,
          "custo": 680.00
        }
      ],
      "subtotal_materiais": 5360.00,
      "subtotal_mao_de_obra": 680.00,
      "subtotal": 6040.00
    }
  ],
  "total_materiais": 5360.00,
  "total_mao_de_obra": 680.00,
  "total_geral": 6040.00
}
```

**This is the INPUT to the pipeline**:
1. Contains client info, project details
2. Lists all items with materials and labor already calculated
3. Has subtotals and grand total
4. Pipeline generates PDF from this data

---

## Common Patterns

### 1. **Using Codes as Keys** (instead of arrays)

❌ **Less efficient** (need to loop to find):
```json
{
  "materiais": [
    {"codigo": "TUB_14", "preco": 18.00},
    {"codigo": "TUB_38", "preco": 28.00}
  ]
}
```

✅ **Better** (direct access):
```json
{
  "materiais": {
    "TUB_14": {"preco": 18.00},
    "TUB_38": {"preco": 28.00}
  }
}
```

**Why?** Direct access is O(1) instead of O(n):
```python
# Direct access (fast)
preco = materiais["materiais"]["TUB_14"]["preco"]

# vs. searching through array (slow)
for m in materiais["materiais"]:
    if m["codigo"] == "TUB_14":
        preco = m["preco"]
```

### 2. **Default Values Pattern**

```json
{
  "DEFAULT": 0.20,
  "Tubulacao": 0.25,
  "Eletrica": 0.30
}
```

**Used with `.get()` in Python**:
```python
bdi = bdi_config.get(categoria, bdi_config.get("DEFAULT", 0.15))
# If categoria not found, use DEFAULT
# If DEFAULT not found, use 0.15
```

### 3. **Nested Configuration Pattern**

```json
{
  "default": {
    "setting1": "value1",
    "setting2": "value2"
  },
  "overrides": {
    "TYPE_A": {
      "setting1": "override_value"
    }
  }
}
```

**Usage**:
```python
# Load defaults
config = data["default"].copy()

# Apply overrides if type matches
if client_type in data["overrides"]:
    config.update(data["overrides"][client_type])
```

### 4. **Array of Objects Pattern**

```json
{
  "componentes": [
    {"tipo": "MATERIAL", "codigo": "TUB_14", "quantidade": 10},
    {"tipo": "MAO_DE_OBRA", "codigo": "INSTALADOR", "quantidade": 2}
  ]
}
```

**Processing**:
```python
for componente in composicao["componentes"]:
    tipo = componente["tipo"]
    codigo = componente["codigo"]
    qtd = componente["quantidade"]
    # ... process each component ...
```

---

## Validating and Debugging JSON

### 1. **JSON Validation Tools**

**Online validators**:
- https://jsonlint.com/
- https://jsonformatter.curiousconcept.com/

**VS Code**:
- Built-in JSON validation
- Shows errors with red squiggly lines
- Auto-formats with `Shift + Alt + F`

### 2. **Common JSON Errors**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unexpected token }` | Extra comma before closing brace | Remove trailing comma |
| `Expecting property name` | Key without quotes | Add quotes: `"key"` |
| `Unexpected token '` | Single quotes used | Use double quotes |
| `Unexpected number` | Comma in number | Use dot: `25.50` not `25,50` |

### 3. **Python JSON Debugging**

```python
import json

try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON Error on line {e.lineno}, column {e.colno}")
    print(f"Message: {e.msg}")
    # Example: "JSON Error on line 15, column 20"
    #          "Message: Expecting ',' delimiter"
```

### 4. **Pretty-Print JSON in Python**

```python
import json

# Load messy JSON
with open("data.json", "r") as f:
    data = json.load(f)

# Print formatted
print(json.dumps(data, indent=2, ensure_ascii=False))

# Or save formatted
with open("data_formatted.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

---

## Quick Reference

### JSON to Python Type Mapping

| JSON | Python | Example |
|------|--------|---------|
| object `{}` | `dict` | `{"key": "value"}` |
| array `[]` | `list` | `[1, 2, 3]` |
| string | `str` | `"text"` |
| number | `int` or `float` | `42` or `3.14` |
| true/false | `True`/`False` | `True` |
| null | `None` | `None` |

### File Paths in This Project

| File | Purpose |
|------|---------|
| `bases/materiais.json` | Materials catalog |
| `bases/mao_de_obra.json` | Labor rates |
| `bases/equipamentos.json` | HVAC equipment catalog |
| `bases/composicoes.json` | Service compositions (bundles) |
| `bases/bdi.json` | Profit margins by category |
| `config/empresa.json` | Company information |
| `config/condicoes_comerciais.json` | Payment terms, warranty |
| `config/contador.json` | Quote number sequencer |
| `tests/dados_teste_*.json` | Example input files |

### Essential Operations

```python
# Load JSON
with open("file.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Save JSON
with open("file.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Access nested data
value = data["level1"]["level2"]["level3"]
value = data.get("key", "default")

# Loop through objects
for key, value in data.items():
    print(f"{key}: {value}")

# Loop through arrays
for item in data["items"]:
    print(item)
```

---

## Next Steps

Now that you understand JSON:
1. ✅ Open `bases/materiais.json` and examine the structure
2. ✅ Try modifying a price and see how it affects the output PDF
3. ✅ Create a new test file based on `dados_teste_panvel.json`
4. ✅ Move on to the Jinja2 guide to see how data becomes HTML

**Practice Exercise**: Try to find where `TUB_14_FLEX` is used in the code. Search with `grep` or your IDE!

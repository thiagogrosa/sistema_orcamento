# Python Fundamentals Guide

**Purpose**: Learn the Python syntax and concepts used throughout the HVAC project.

---

## Table of Contents
1. [Variables and Data Types](#variables-and-data-types)
2. [Functions](#functions)
3. [Data Structures](#data-structures)
4. [Control Flow](#control-flow)
5. [Modules and Imports](#modules-and-imports)
6. [Classes and Objects](#classes-and-objects)
7. [File Operations](#file-operations)
8. [Common Patterns in This Project](#common-patterns-in-this-project)

---

## Variables and Data Types

### Basic Variables
Variables store data. Python automatically determines the type.

```python
# Numbers
quantidade = 5                    # Integer (whole number)
preco = 1250.50                  # Float (decimal number)
margem = 0.15                    # Float (percentage as decimal)

# Strings (text)
nome = "Cassete 60000 BTUs"      # Double quotes
descricao = 'Ar condicionado'    # Single quotes (same thing)
unidade = "UN"                   # Unit abbreviation

# Booleans (True/False)
instalado = True
em_garantia = False

# None (represents "no value")
observacao = None
```

**From your code** (`hvac/precificador.py:45`):
```python
categoria = item.get("categoria", "DEFAULT")
valor_venda = item.get("valor_venda", 0)
descricao = item.get("descricao", "")
```

### String Operations

```python
# Concatenation (joining strings)
nome_completo = "João" + " " + "Silva"  # "João Silva"

# F-strings (formatted strings) - MOST USED IN YOUR PROJECT
nome = "Armant"
cnpj = "13.591.585/0001-03"
texto = f"Empresa: {nome}, CNPJ: {cnpj}"
# Result: "Empresa: Armant, CNPJ: 13.591.585/0001-03"

# String methods
texto = "  HVAC SYSTEM  "
texto.strip()          # Remove spaces: "HVAC SYSTEM"
texto.lower()          # Lowercase: "  hvac system  "
texto.upper()          # Uppercase: "  HVAC SYSTEM  "
texto.replace("HVAC", "AC")  # Replace: "  AC SYSTEM  "
```

**From your code** (`hvac/generators/utils.py:8`):
```python
def formatar_moeda(valor):
    """Formats a number as Brazilian currency."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    # Example: 1250.50 → "R$ 1.250,50"
```

---

## Functions

Functions are reusable blocks of code.

### Basic Function Syntax

```python
def nome_da_funcao(parametro1, parametro2):
    """This is a docstring - describes what the function does."""
    # Function body
    resultado = parametro1 + parametro2
    return resultado

# Calling the function
total = nome_da_funcao(10, 20)  # total = 30
```

### Function with Default Parameters

```python
def calcular_preco(valor_base, margem=0.15):
    """Calculate price with default 15% margin."""
    return valor_base * (1 + margem)

# Can call with or without the second parameter
preco1 = calcular_preco(100)        # Uses default: 115.0
preco2 = calcular_preco(100, 0.20)  # Custom margin: 120.0
```

**From your code** (`hvac/precificador.py:88`):
```python
def aplicar_bdi(item, bdi_config):
    """
    Applies BDI (markup) to an item.

    Args:
        item: Dictionary with item data
        bdi_config: Dictionary with margin rules

    Returns:
        Modified item with valor_venda added
    """
    categoria = item.get("categoria", "DEFAULT")
    valor_custo = item.get("valor_custo", 0)

    # Get margin for this category
    bdi = bdi_config.get(categoria, bdi_config.get("DEFAULT", 0.15))

    # Calculate selling price
    valor_venda = valor_custo * (1 + bdi)

    # Add to item
    item["valor_venda"] = valor_venda
    return item
```

### Lambda Functions (Short Anonymous Functions)

```python
# Regular function
def dobrar(x):
    return x * 2

# Lambda (same thing, one line)
dobrar = lambda x: x * 2

# Often used with map, filter, sorted
numeros = [1, 2, 3, 4, 5]
dobrados = list(map(lambda x: x * 2, numeros))  # [2, 4, 6, 8, 10]
```

---

## Data Structures

### Lists (Ordered Collections)

```python
# Creating lists
materiais = ["Tubo", "Cabo", "Isolamento"]
precos = [10.50, 5.25, 8.00]
vazia = []

# Accessing elements (0-indexed)
primeiro = materiais[0]    # "Tubo"
segundo = materiais[1]     # "Cabo"
ultimo = materiais[-1]     # "Isolamento" (negative = from end)

# Adding elements
materiais.append("Fita")           # Add to end
materiais.insert(0, "Parafuso")    # Insert at position 0

# Removing elements
materiais.remove("Cabo")           # Remove by value
item = materiais.pop()             # Remove and return last item
item = materiais.pop(0)            # Remove and return item at index 0

# List comprehensions (create new lists)
numeros = [1, 2, 3, 4, 5]
quadrados = [n * n for n in numeros]           # [1, 4, 9, 16, 25]
pares = [n for n in numeros if n % 2 == 0]     # [2, 4]
```

**From your code** (`hvac/compositor.py:75`):
```python
def expandir_composicao(item, bases):
    """Expands a composition into its component items."""
    composicoes = bases["composicoes"]

    # Find the composition
    composicao = next(
        (c for c in composicoes if c["codigo"] == item["codigo"]),
        None
    )

    if not composicao:
        return [item]  # Return as single-item list

    # Expand components
    componentes = []
    for comp in composicao.get("componentes", []):
        # Create new item for each component
        novo_item = {
            "tipo": comp["tipo"],
            "codigo": comp["codigo"],
            "quantidade": comp["quantidade"] * item.get("quantidade", 1)
        }
        componentes.append(novo_item)

    return componentes
```

### Dictionaries (Key-Value Pairs)

```python
# Creating dictionaries
material = {
    "codigo": "MAT-001",
    "descricao": "Tubo de cobre 1/2\"",
    "unidade": "M",
    "preco": 25.50
}

# Accessing values
codigo = material["codigo"]              # "MAT-001" (KeyError if not found)
preco = material.get("preco")            # 25.50
preco = material.get("preco", 0)         # 0 if "preco" doesn't exist (safe)

# Adding/modifying values
material["quantidade"] = 10              # Add new key
material["preco"] = 26.00               # Modify existing key

# Checking if key exists
if "codigo" in material:
    print("Código exists!")

# Dictionary methods
chaves = material.keys()                 # dict_keys(['codigo', 'descricao', ...])
valores = material.values()              # dict_values(['MAT-001', 'Tubo...', ...])
items = material.items()                 # [('codigo', 'MAT-001'), ...]

# Looping through dictionaries
for chave, valor in material.items():
    print(f"{chave}: {valor}")
```

**From your code** (`hvac/utils/loader.py:12`):
```python
_cache = {}  # Global cache dictionary

def carregar_bases():
    """Loads all base JSON files into a dictionary."""
    if _cache:
        return _cache  # Return cached data if already loaded

    bases = {
        "materiais": carregar_json("bases/materiais.json"),
        "mao_de_obra": carregar_json("bases/mao_de_obra.json"),
        "ferramentas": carregar_json("bases/ferramentas.json"),
        "equipamentos": carregar_json("bases/equipamentos.json"),
        "composicoes": carregar_json("bases/composicoes.json"),
        "bdi": carregar_json("bases/bdi.json")
    }

    _cache.update(bases)  # Store in cache
    return bases
```

### Tuples (Immutable Lists)

```python
# Tuples use parentheses, can't be modified after creation
coordenadas = (10, 20)
assinatura = ("Rodrigo G. Donni", "Engenheiro Mecânico")

# Accessing like lists
x = coordenadas[0]  # 10
y = coordenadas[1]  # 20

# Tuple unpacking
nome, cargo = assinatura
# nome = "Rodrigo G. Donni"
# cargo = "Engenheiro Mecânico"
```

---

## Control Flow

### If/Elif/Else Statements

```python
# Basic if statement
if temperatura > 25:
    print("Está quente")

# If-else
if quantidade > 0:
    print("Em estoque")
else:
    print("Sem estoque")

# If-elif-else (multiple conditions)
if categoria == "EQUIPAMENTO":
    margem = 0.25
elif categoria == "MATERIAL":
    margem = 0.15
elif categoria == "MAO_DE_OBRA":
    margem = 0.10
else:
    margem = 0.20  # Default

# Ternary operator (one-line if-else)
status = "Ativo" if instalado else "Inativo"
# Same as:
# if instalado:
#     status = "Ativo"
# else:
#     status = "Inativo"
```

**From your code** (`hvac/precificador.py:45`):
```python
def aplicar_bdi(item, bdi_config):
    categoria = item.get("categoria", "DEFAULT")
    valor_custo = item.get("valor_custo", 0)

    # Get margin based on category
    if categoria in bdi_config:
        bdi = bdi_config[categoria]
    else:
        bdi = bdi_config.get("DEFAULT", 0.15)  # Fallback to default

    valor_venda = valor_custo * (1 + bdi)
    item["valor_venda"] = valor_venda
    return item
```

### For Loops

```python
# Loop through list
materiais = ["Tubo", "Cabo", "Fita"]
for material in materiais:
    print(material)

# Loop with index
for i, material in enumerate(materiais):
    print(f"{i}: {material}")
    # 0: Tubo
    # 1: Cabo
    # 2: Fita

# Loop through dictionary
preco_dict = {"Tubo": 25.50, "Cabo": 10.00}
for item, preco in preco_dict.items():
    print(f"{item}: R$ {preco}")

# Range loop (repeat N times)
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):     # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (step by 2)
    print(i)
```

**From your code** (`hvac/compositor.py:25`):
```python
def expandir_escopo(dados_escopo, bases):
    """Expands all items in the scope."""
    itens_expandidos = []

    for item in dados_escopo.get("itens", []):
        # Check if it's a composition
        if item.get("tipo") == "COMPOSICAO":
            componentes = expandir_composicao(item, bases)
            itens_expandidos.extend(componentes)
        else:
            itens_expandidos.append(item)

    return itens_expandidos
```

### While Loops

```python
# Basic while loop
contador = 0
while contador < 5:
    print(contador)
    contador += 1  # Same as: contador = contador + 1

# While with break
while True:
    resposta = input("Continue? (s/n): ")
    if resposta == "n":
        break  # Exit loop

# While with continue
contador = 0
while contador < 10:
    contador += 1
    if contador % 2 == 0:  # If even
        continue  # Skip rest of loop, go to next iteration
    print(contador)  # Only prints odd numbers
```

---

## Modules and Imports

### Importing Modules

```python
# Import entire module
import json
data = json.loads('{"nome": "João"}')

# Import specific functions
from json import loads, dumps
data = loads('{"nome": "João"}')

# Import with alias
import json as j
data = j.loads('{"nome": "João"}')

# Import everything (not recommended)
from json import *
```

**From your code** (`hvac/pipeline.py:1-10`):
```python
"""Main pipeline for HVAC proposal generation."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from hvac.compositor import expandir_escopo
from hvac.precificador import aplicar_precificacao
from hvac.generators.proposta_pdf import gerar_proposta_pdf
from hvac.generators.planilha_interna import gerar_planilha_interna
from hvac.utils.loader import carregar_bases
from hvac.utils.metricas import Metricas
```

### Module Structure

Your project has this import structure:
```
hvac/
├── __init__.py          # Makes "hvac" a package
├── pipeline.py          # Can be imported as: from hvac.pipeline import executar_pipeline
├── compositor.py        # from hvac.compositor import expandir_escopo
├── precificador.py      # from hvac.precificador import aplicar_precificacao
├── generators/
│   ├── __init__.py
│   ├── proposta_pdf.py  # from hvac.generators.proposta_pdf import gerar_proposta_pdf
│   └── utils.py         # from hvac.generators.utils import formatar_moeda
└── utils/
    ├── __init__.py
    ├── loader.py        # from hvac.utils.loader import carregar_bases
    └── metricas.py      # from hvac.utils.metricas import Metricas
```

---

## Classes and Objects

### Basic Class Structure

```python
class Material:
    """Represents a construction material."""

    # Constructor (runs when creating new object)
    def __init__(self, codigo, descricao, preco):
        self.codigo = codigo          # Instance variable
        self.descricao = descricao
        self.preco = preco

    # Instance method
    def calcular_custo(self, quantidade):
        return self.preco * quantidade

    # String representation
    def __repr__(self):
        return f"Material({self.codigo}, {self.descricao})"

# Creating objects (instances)
tubo = Material("MAT-001", "Tubo de cobre", 25.50)
cabo = Material("MAT-002", "Cabo elétrico", 10.00)

# Accessing attributes
print(tubo.codigo)        # "MAT-001"
print(tubo.descricao)     # "Tubo de cobre"

# Calling methods
custo = tubo.calcular_custo(5)  # 127.50
```

**From your code** (`hvac/utils/metricas.py:5`):
```python
class Metricas:
    """Tracks execution metrics for pipeline stages."""

    def __init__(self):
        self.tempos = {}       # Dictionary to store timing data
        self.contadores = {}   # Dictionary to store counts

    def iniciar_tempo(self, etapa):
        """Start timing a stage."""
        import time
        self.tempos[etapa] = {"inicio": time.time()}

    def finalizar_tempo(self, etapa):
        """End timing a stage."""
        import time
        if etapa in self.tempos:
            self.tempos[etapa]["fim"] = time.time()
            inicio = self.tempos[etapa]["inicio"]
            fim = self.tempos[etapa]["fim"]
            self.tempos[etapa]["duracao"] = fim - inicio

    def incrementar_contador(self, nome):
        """Increment a counter."""
        if nome not in self.contadores:
            self.contadores[nome] = 0
        self.contadores[nome] += 1

    def obter_relatorio(self):
        """Get metrics report."""
        return {
            "tempos": self.tempos,
            "contadores": self.contadores
        }

# Using the class
metricas = Metricas()
metricas.iniciar_tempo("compositor")
# ... do work ...
metricas.finalizar_tempo("compositor")
relatorio = metricas.obter_relatorio()
```

### Class Inheritance

```python
class Item:
    """Base class for all items."""
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class Material(Item):
    """Material inherits from Item."""
    def __init__(self, codigo, descricao, unidade):
        super().__init__(codigo, descricao)  # Call parent constructor
        self.unidade = unidade

class Equipamento(Item):
    """Equipment inherits from Item."""
    def __init__(self, codigo, descricao, potencia):
        super().__init__(codigo, descricao)
        self.potencia = potencia

# Both have codigo and descricao from Item
mat = Material("MAT-001", "Tubo", "M")
equip = Equipamento("EQ-001", "Cassete 60k BTU", 60000)
```

---

## File Operations

### Reading Files

```python
# Reading text files
with open("arquivo.txt", "r") as arquivo:
    conteudo = arquivo.read()  # Read entire file
    # File automatically closes after "with" block

# Reading line by line
with open("arquivo.txt", "r") as arquivo:
    for linha in arquivo:
        print(linha.strip())  # strip() removes newline

# Reading JSON
import json
with open("config.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)  # Returns dictionary/list
```

**From your code** (`hvac/utils/loader.py:20`):
```python
def carregar_json(caminho):
    """Loads a JSON file and returns its contents."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
```

### Writing Files

```python
# Writing text files
with open("saida.txt", "w") as arquivo:
    arquivo.write("Primeira linha\n")
    arquivo.write("Segunda linha\n")

# Appending to files
with open("saida.txt", "a") as arquivo:
    arquivo.write("Linha adicional\n")

# Writing JSON
import json
dados = {"nome": "João", "idade": 30}
with open("dados.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=2, ensure_ascii=False)
```

### Path Operations

```python
from pathlib import Path

# Creating paths
caminho = Path("bases/materiais.json")
caminho = Path("bases") / "materiais.json"  # Same thing

# Checking existence
if caminho.exists():
    print("File exists")

# Getting parts
pasta = caminho.parent          # Path("bases")
nome = caminho.name             # "materiais.json"
extensao = caminho.suffix       # ".json"
nome_sem_ext = caminho.stem     # "materiais"

# Creating directories
Path("output/pdfs").mkdir(parents=True, exist_ok=True)
# parents=True: create parent directories too
# exist_ok=True: don't error if already exists

# Reading/writing with Path
conteudo = caminho.read_text(encoding="utf-8")
caminho.write_text("novo conteudo", encoding="utf-8")
```

---

## Common Patterns in This Project

### 1. Dictionary.get() for Safe Access

```python
# Without .get() - can cause KeyError
categoria = item["categoria"]  # ERROR if "categoria" doesn't exist

# With .get() - returns None if not found
categoria = item.get("categoria")

# With .get() and default value
categoria = item.get("categoria", "DEFAULT")  # Returns "DEFAULT" if not found
```

### 2. List Comprehensions for Filtering/Transforming

```python
# Transform list
precos = [10, 20, 30, 40]
com_margem = [p * 1.15 for p in precos]  # [11.5, 23.0, 34.5, 46.0]

# Filter list
apenas_grandes = [p for p in precos if p > 20]  # [30, 40]

# Both
grandes_com_margem = [p * 1.15 for p in precos if p > 20]  # [34.5, 46.0]
```

**From your code** (`hvac/precificador.py:15`):
```python
def aplicar_precificacao(itens, bases):
    """Apply pricing to all items."""
    # Apply cost calculation to all items
    itens_com_custo = [calcular_custo_item(item, bases) for item in itens]

    # Apply BDI to all items
    bdi_config = bases.get("bdi", {})
    itens_com_venda = [aplicar_bdi(item, bdi_config) for item in itens_com_custo]

    return itens_com_venda
```

### 3. The next() Function for Finding Items

```python
# Find first item matching condition
materiais = [
    {"codigo": "MAT-001", "descricao": "Tubo"},
    {"codigo": "MAT-002", "descricao": "Cabo"},
]

# Find material with code MAT-002
material = next(
    (m for m in materiais if m["codigo"] == "MAT-002"),
    None  # Default if not found
)
# Returns: {"codigo": "MAT-002", "descricao": "Cabo"}
```

**From your code** (`hvac/compositor.py:75`):
```python
composicao = next(
    (c for c in composicoes if c["codigo"] == item["codigo"]),
    None
)
```

### 4. F-strings for Formatting

```python
# Basic f-string
nome = "João"
idade = 30
texto = f"Nome: {nome}, Idade: {idade}"

# With expressions
preco = 100
texto = f"Preço com desconto: R$ {preco * 0.9:.2f}"
# "Preço com desconto: R$ 90.00"

# Format specifiers
numero = 1234.567
f"{numero:,.2f}"     # "1,234.57" (thousands separator, 2 decimals)
f"{numero:.0f}"      # "1235" (no decimals, rounded)
f"{numero:10.2f}"    # "   1234.57" (padded to 10 chars)
```

### 5. Type Hints (Documentation)

```python
from typing import Dict, List, Optional, Any

# Function with type hints
def calcular_total(itens: List[Dict[str, Any]], margem: float = 0.15) -> float:
    """
    Calculate total price with margin.

    Args:
        itens: List of item dictionaries
        margem: Profit margin (default 15%)

    Returns:
        Total price as float
    """
    total = sum(item.get("preco", 0) for item in itens)
    return total * (1 + margem)

# Type hints don't enforce types, they're just documentation
# But they help IDEs give you better autocomplete
```

**From your code** (`hvac/pipeline.py:15`):
```python
def executar_pipeline(
    arquivo_escopo: str,
    arquivo_saida: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute the complete HVAC proposal generation pipeline.

    Args:
        arquivo_escopo: Path to scope JSON file
        arquivo_saida: Path for output PDF
        config: Optional configuration dictionary

    Returns:
        Dictionary with pipeline results and metrics
    """
    # ... implementation ...
```

---

## Quick Reference: Common Operations

### String Formatting
```python
valor = 1250.50
f"R$ {valor:,.2f}"                    # "R$ 1,250.50"
f"{valor:.0f}"                        # "1251"
f"Valor: R$ {valor:>10,.2f}"          # Right-aligned in 10 chars
```

### List Operations
```python
lista = [1, 2, 3, 4, 5]
lista.append(6)                       # [1, 2, 3, 4, 5, 6]
lista.extend([7, 8])                  # [1, 2, 3, 4, 5, 6, 7, 8]
lista[0:3]                            # [1, 2, 3] (slice)
lista[-1]                             # 8 (last item)
len(lista)                            # 8 (length)
sum(lista)                            # 36 (sum of all)
max(lista)                            # 8 (maximum)
min(lista)                            # 1 (minimum)
```

### Dictionary Operations
```python
d = {"a": 1, "b": 2}
d.get("a")                            # 1
d.get("c", 0)                         # 0 (default)
d.keys()                              # ["a", "b"]
d.values()                            # [1, 2]
d.items()                             # [("a", 1), ("b", 2)]
d.update({"c": 3})                    # {"a": 1, "b": 2, "c": 3}
```

### File Paths
```python
from pathlib import Path
p = Path("bases/materiais.json")
p.exists()                            # True/False
p.parent                              # Path("bases")
p.name                                # "materiais.json"
p.suffix                              # ".json"
p.stem                                # "materiais"
```

---

## Next Steps

Now that you understand Python fundamentals:
1. ✅ Read the actual code files in `hvac/` directory
2. ✅ Trace through `hvac/pipeline.py` to see how everything connects
3. ✅ Modify values in `bases/*.json` and see what changes
4. ✅ Add `print()` statements to understand data flow
5. ✅ Move on to the JSON guide to understand data structures

**Practice Exercise**: Try to read and understand `hvac/utils/loader.py` - it's only 30 lines and uses most concepts from this guide!

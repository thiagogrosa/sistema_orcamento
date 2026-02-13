# Bash Scripting Basics Guide

**Purpose**: Learn Bash scripting to automate tasks in this HVAC project.

---

## Table of Contents
1. [What is Bash?](#what-is-bash)
2. [Basic Syntax](#basic-syntax)
3. [Variables](#variables)
4. [Command Line Arguments](#command-line-arguments)
5. [Conditionals](#conditionals)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Running Commands](#running-commands)
9. [Understanding Project Scripts](#understanding-project-scripts)
10. [Quick Reference](#quick-reference)

---

## What is Bash?

**Bash** = **B**ourne **A**gain **SH**ell

- Command-line interpreter for Unix/Linux
- Used to run commands and automate tasks
- Scripts end in `.sh` extension
- In this project: Automates PDF generation

---

## Basic Syntax

### Hello World Script

**File**: `hello.sh`
```bash
#!/bin/bash
# This is a comment

echo "Hello, World!"
```

### Running the Script

```bash
# Method 1: Make executable and run
chmod +x hello.sh
./hello.sh

# Method 2: Run with bash
bash hello.sh
```

### Important First Line

```bash
#!/bin/bash
```
This is called a "shebang" - tells the system to use bash to run this script.

---

## Variables

### Creating and Using Variables

```bash
#!/bin/bash

# Create variable (no spaces around =)
name="João"
age=30
city="Porto Alegre"

# Use variable with $
echo "Name: $name"
echo "Age: $age"
echo "City: $city"
```

**Output**:
```
Name: João
Age: 30
City: Porto Alegre
```

### Variable Rules

```bash
# ✅ Correct
name="João"
AGE=30
_city="POA"

# ❌ Wrong - spaces around =
name = "João"

# ❌ Wrong - spaces in value (need quotes)
name=João Silva     # Only "João" is stored
name="João Silva"   # Correct
```

### Special Variables

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
echo "Last command exit status: $?"
```

**Run**:
```bash
./script.sh arg1 arg2
```

**Output**:
```
Script name: ./script.sh
First argument: arg1
Second argument: arg2
All arguments: arg1 arg2
Number of arguments: 2
```

---

## Command Line Arguments

**From your code** (`gerar_teste_pdf.sh:5-7`):
```bash
NUMERO=$1
REVISAO=$2
INPUT_FILE=${3:-"tests/dados_teste_panvel.json"}
```

**Explanation**:
- `$1` - First argument (quote number)
- `$2` - Second argument (revision)
- `${3:-"default"}` - Third argument, or "default" if not provided

**Usage examples**:
```bash
./gerar_teste_pdf.sh                                    # All defaults
./gerar_teste_pdf.sh 1025                               # Custom number
./gerar_teste_pdf.sh 1025 R01                          # Custom number and revision
./gerar_teste_pdf.sh 1025 R01 tests/dados_custom.json  # All custom
```

---

## Conditionals

### If Statement

```bash
#!/bin/bash

age=18

if [ $age -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi
```

### If-Elif-Else

```bash
#!/bin/bash

score=85

if [ $score -ge 90 ]; then
    echo "A"
elif [ $score -ge 80 ]; then
    echo "B"
elif [ $score -ge 70 ]; then
    echo "C"
else
    echo "F"
fi
```

### Comparison Operators

**Numbers**:
```bash
[ $a -eq $b ]    # Equal
[ $a -ne $b ]    # Not equal
[ $a -gt $b ]    # Greater than
[ $a -ge $b ]    # Greater than or equal
[ $a -lt $b ]    # Less than
[ $a -le $b ]    # Less than or equal
```

**Strings**:
```bash
[ "$a" = "$b" ]   # Equal
[ "$a" != "$b" ]  # Not equal
[ -z "$a" ]       # Empty string
[ -n "$a" ]       # Not empty string
```

**Files**:
```bash
[ -f "$file" ]    # File exists
[ -d "$dir" ]     # Directory exists
[ -r "$file" ]    # File is readable
[ -w "$file" ]    # File is writable
[ -x "$file" ]    # File is executable
```

**From your code** (`gerar_teste_pdf.sh:31`):
```bash
if [ -f "$PDF_PATH" ]; then
    echo "PDF Gerado"
else
    echo "Erro: PDF não foi gerado"
    exit 1
fi
```

**Explanation**:
- `[ -f "$PDF_PATH" ]` - Check if file exists
- `exit 1` - Exit script with error code 1

---

## Loops

### For Loop

```bash
#!/bin/bash

# Loop through list
for name in João Maria Pedro
do
    echo "Hello, $name"
done
```

**Output**:
```
Hello, João
Hello, Maria
Hello, Pedro
```

### For Loop with Numbers

```bash
#!/bin/bash

# Loop from 1 to 5
for i in 1 2 3 4 5
do
    echo "Number: $i"
done

# Or using range
for i in {1..5}
do
    echo "Number: $i"
done
```

**From your code** (`gerar_todos_testes.sh:6-11`):
```bash
for n in 2 3 4 5
do
    echo "Gerando versão com $n itens..."
    # Generate PDF for each n
done
```

### While Loop

```bash
#!/bin/bash

counter=1
while [ $counter -le 5 ]
do
    echo "Count: $counter"
    counter=$((counter + 1))
done
```

---

## Functions

### Basic Function

```bash
#!/bin/bash

# Define function
greet() {
    echo "Hello, $1!"
}

# Call function
greet "João"
greet "Maria"
```

**Output**:
```
Hello, João!
Hello, Maria!
```

### Function with Return Value

```bash
#!/bin/bash

add() {
    result=$(($1 + $2))
    echo $result
}

sum=$(add 10 20)
echo "Sum: $sum"
```

---

## Running Commands

### Basic Commands

```bash
#!/bin/bash

# Run command
echo "Current directory:"
pwd

echo "List files:"
ls -la

echo "Date:"
date
```

### Capturing Command Output

```bash
#!/bin/bash

# Capture output in variable
current_dir=$(pwd)
echo "You are in: $current_dir"

file_count=$(ls -1 | wc -l)
echo "Number of files: $file_count"
```

**From your code** (`gerar_teste_pdf.sh:12-29`):
```bash
# Capture Python script output
PDF_PATH=$(.venv/bin/python3 -c "
from hvac.generators import gerar_proposta_pdf
import json

# ... Python code ...

print(pdf['arquivo_pdf'])
")
```

**Explanation**:
- `$(command)` - Runs command and captures output
- `.venv/bin/python3` - Python from virtual environment
- `-c "code"` - Run Python code directly (without file)
- Result stored in `PDF_PATH` variable

### Multiline Python in Bash

**From your code** (`gerar_todos_testes.sh:9-20`):
```bash
.venv/bin/python3 <<EOF
from hvac.generators import gerar_proposta_pdf
import json

with open('tests/dados_teste_panvel_x$n.json') as f:
    dados = json.load(f)

pdf = gerar_proposta_pdf(dados, rascunho=False)
print(f"Sucesso: {pdf['arquivo_pdf']}")
EOF
```

**Explanation**:
- `<<EOF` - Start of "here document" (multiline input)
- Python code goes here
- `EOF` - End of here document
- `$n` - Bash variable accessible in Python code

---

## Understanding Project Scripts

### Script 1: `gerar_teste_pdf.sh`

**Purpose**: Generate a single test PDF with optional quote number and revision.

**Usage**:
```bash
./gerar_teste_pdf.sh [numero] [revisao] [input_file]
```

**Code breakdown**:

```bash
#!/bin/bash
# 1. Get command line arguments
NUMERO=$1
REVISAO=$2
INPUT_FILE=${3:-"tests/dados_teste_panvel.json"}

# 2. Change to project directory
cd /root/thiagorosa/gemini_hvac_layout

# 3. Run Python code and capture PDF path
PDF_PATH=$(.venv/bin/python3 -c "
from hvac.generators import gerar_proposta_pdf
import json

# Load input file
with open('$INPUT_FILE') as f:
    dados = json.load(f)

# Generate PDF
pdf = gerar_proposta_pdf(dados, rascunho=True, numero_orcamento='$NUMERO', revisao='$REVISAO')

# Print path (captured by bash)
print(pdf['arquivo_pdf'])
")

# 4. Check if PDF was created
if [ -f "$PDF_PATH" ]; then
    echo "PDF Gerado: $PDF_PATH"

    # 5. Open in Chrome (WSL-specific)
    WIN_PATH=$(wslpath -w "$PDF_PATH")
    powershell.exe -Command "Start-Process chrome -ArgumentList '$WIN_PATH'"
else
    echo "Erro: PDF não foi gerado"
    exit 1
fi
```

**Key techniques**:
1. Command-line arguments (`$1`, `$2`, `${3:-default}`)
2. Inline Python (`-c "code"`)
3. Output capture (`PDF_PATH=$(...)`)
4. File existence check (`[ -f "$file" ]`)
5. Conditional execution (`if/else`)
6. WSL-Windows integration (`wslpath`, `powershell.exe`)

### Script 2: `gerar_todos_testes.sh`

**Purpose**: Generate PDFs for all test variants (x2, x3, x4, x5 items).

**Code breakdown**:

```bash
#!/bin/bash

# 1. Change to project directory
cd /root/thiagorosa/gemini_hvac_layout

# 2. Loop through test variants
for n in 2 3 4 5
do
    echo "Gerando versão com $n itens..."

    # 3. Run Python with heredoc
    .venv/bin/python3 <<EOF
from hvac.generators import gerar_proposta_pdf
import json
import os

# Load test file (using $n from bash)
with open('tests/dados_teste_panvel_x$n.json') as f:
    dados = json.load(f)

# Create output directory
os.makedirs('output/testes_multiplus', exist_ok=True)

# Generate PDF
pdf = gerar_proposta_pdf(dados, rascunho=False)
print(f"Sucesso: {pdf['arquivo_pdf']}")
EOF
done
```

**Key techniques**:
1. For loop (`for n in 2 3 4 5`)
2. Here document (`<<EOF` ... `EOF`)
3. Variable interpolation in heredoc (`$n`)
4. Multiple PDF generation in loop

---

## Common Bash Commands

### File Operations

```bash
# Create directory
mkdir output
mkdir -p output/subdir/nested  # Create parent dirs too

# Change directory
cd /path/to/directory

# Copy file
cp source.txt destination.txt
cp -r source_dir/ dest_dir/     # Copy directory

# Move/rename
mv old_name.txt new_name.txt
mv file.txt /new/location/

# Remove
rm file.txt
rm -r directory/                # Remove directory
rm -f file.txt                  # Force remove (no confirmation)

# Check if file exists
if [ -f "file.txt" ]; then
    echo "File exists"
fi
```

### Text Processing

```bash
# Print to screen
echo "Hello, World!"

# Print with newline interpretation
echo -e "Line 1\nLine 2"

# Read file
cat file.txt

# Search in files
grep "pattern" file.txt
grep -r "pattern" directory/    # Recursive search

# Word/line count
wc -l file.txt                  # Count lines
wc -w file.txt                  # Count words
```

### Variables and Strings

```bash
# String concatenation
first="João"
last="Silva"
full="$first $last"
echo $full  # João Silva

# String length
name="João"
echo ${#name}  # 4

# Default value
value=${VAR:-"default"}  # Use "default" if VAR is empty
```

---

## Quick Reference

### Basic Script Template

```bash
#!/bin/bash

# Script description
# Usage: ./script.sh [arg1] [arg2]

# Variables
ARG1=$1
ARG2=${2:-"default_value"}

# Main logic
echo "Processing..."

# Check result
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed"
    exit 1
fi
```

### Common Patterns

```bash
# Run Python script
python3 script.py

# Run Python from virtual environment
.venv/bin/python3 script.py

# Inline Python
python3 -c "print('Hello')"

# Capture output
result=$(command)

# Check if file exists
if [ -f "file.txt" ]; then
    echo "Exists"
fi

# Loop through files
for file in *.txt
do
    echo "Processing $file"
done

# Make script executable
chmod +x script.sh

# Run script
./script.sh
```

### Common Variables

```bash
$0      # Script name
$1-$9   # Arguments 1-9
$@      # All arguments
$#      # Number of arguments
$?      # Exit status of last command
$$      # Process ID
$HOME   # Home directory
$PWD    # Current directory
```

---

## Next Steps

Now that you understand Bash:
1. ✅ Try running `./gerar_teste_pdf.sh` in your project
2. ✅ Modify the script to add `echo` statements for debugging
3. ✅ Create a simple script that lists all JSON files in `tests/`
4. ✅ Review the master learning guide index

**Practice Exercise**: Create a bash script that counts how many JSON files are in the `bases/` directory!

```bash
#!/bin/bash
count=$(ls -1 bases/*.json | wc -l)
echo "Number of JSON files: $count"
```

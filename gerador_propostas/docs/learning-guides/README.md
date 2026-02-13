# HVAC Project Learning Guides

**Complete learning path to understand and work with this HVAC proposal generation system.**

---

## 🎯 Purpose

These guides teach you **all the technologies and concepts** needed to understand, modify, and extend this codebase. Each guide is comprehensive, practical, and includes real examples from the project.

---

## 📚 Learning Path

### **Recommended Order (For Beginners)**

Follow this sequence if you're new to programming or these technologies:

1. **[Python Fundamentals](01-python-fundamentals.md)** ⭐ START HERE
   - Variables, functions, data structures
   - Control flow (if/for/while)
   - Modules and imports
   - Classes and objects
   - File operations
   - **Time**: 2-4 hours

2. **[JSON Data Structures](02-json-data-structures.md)**
   - JSON syntax and rules
   - Data types (objects, arrays, strings, numbers)
   - Working with JSON in Python
   - Understanding all project data files
   - **Time**: 1-2 hours

3. **[HTML & CSS Basics](04-html-css-basics.md)**
   - HTML structure and elements
   - CSS styling and selectors
   - Box model
   - Print-specific CSS
   - Understanding the proposal template
   - **Time**: 2-3 hours

4. **[Jinja2 Templating](03-jinja2-templating.md)**
   - Template syntax (variables, loops, conditionals)
   - Filters and functions
   - How data becomes HTML
   - Real examples from the proposal template
   - **Time**: 1-2 hours

5. **[WeasyPrint PDF Generation](05-weasyprint-pdf-generation.md)**
   - Converting HTML+CSS to PDF
   - Embedding images
   - Page layout and print CSS
   - How the project generates PDFs
   - **Time**: 1-2 hours

6. **[openpyxl Excel Generation](06-openpyxl-excel-generation.md)**
   - Creating Excel files with Python
   - Working with cells, rows, columns
   - Styling and formatting
   - Formulas and calculations
   - **Time**: 1-2 hours

7. **[Bash Scripting Basics](07-bash-scripting-basics.md)**
   - Shell scripting fundamentals
   - Variables and arguments
   - Conditionals and loops
   - Running commands
   - Understanding project automation scripts
   - **Time**: 1-2 hours

**Total Learning Time**: 10-17 hours (can be spread over days/weeks)

---

## 🚀 Quick Start Paths

### **Path 1: Just Want to Generate PDFs**
1. [Python Fundamentals](01-python-fundamentals.md) - Sections: Variables, Functions, File Operations
2. [JSON Data Structures](02-json-data-structures.md) - Sections: Project Data Structure
3. [Bash Scripting](07-bash-scripting-basics.md) - Sections: Understanding Project Scripts

### **Path 2: Want to Modify the Proposal Template**
1. [HTML & CSS Basics](04-html-css-basics.md)
2. [Jinja2 Templating](03-jinja2-templating.md)
3. [JSON Data Structures](02-json-data-structures.md) - to understand data sources

### **Path 3: Want to Customize the Code**
1. [Python Fundamentals](01-python-fundamentals.md)
2. [JSON Data Structures](02-json-data-structures.md)
3. [WeasyPrint PDF Generation](05-weasyprint-pdf-generation.md)

---

## 📖 Guide Summaries

### 01. Python Fundamentals
**What you'll learn**:
- Python syntax, variables, and data types
- Functions and control flow
- Lists, dictionaries, and tuples
- Modules and imports
- Classes and objects
- File operations
- Common patterns used in this project

**Key topics**: `variables`, `functions`, `dictionaries`, `loops`, `classes`, `file I/O`

---

### 02. JSON Data Structures
**What you'll learn**:
- JSON syntax and data types
- Working with JSON in Python
- All project data files explained:
  - `bases/materiais.json` - Materials catalog
  - `bases/mao_de_obra.json` - Labor rates
  - `bases/equipamentos.json` - Equipment
  - `bases/composicoes.json` - Service bundles
  - `config/empresa.json` - Company info
  - `tests/dados_teste_*.json` - Test data
- Common patterns and validating JSON

**Key topics**: `JSON`, `data structures`, `configuration`, `catalogs`

---

### 03. Jinja2 Templating
**What you'll learn**:
- Template syntax: `{{ variables }}`, `{% statements %}`
- Control structures: `if`, `for`, `filters`
- How data flows from Python to HTML
- Real examples from `proposta_base.html`
- Best practices for templates

**Key topics**: `templates`, `Jinja2`, `HTML generation`, `data rendering`

---

### 04. HTML & CSS Basics
**What you'll learn**:
- HTML structure and elements
- CSS selectors and properties
- Box model (margin, padding, border)
- Print-specific CSS (`@page`, running headers/footers)
- Understanding `proposta_base.html` and `proposta_styles.css`
- How to modify the proposal layout

**Key topics**: `HTML`, `CSS`, `layout`, `styling`, `print CSS`

---

### 05. WeasyPrint PDF Generation
**What you'll learn**:
- Converting HTML+CSS to PDF
- Embedding images with base64
- Page layout and margins
- Running headers and footers
- How `proposta_pdf.py` generates PDFs
- Debugging PDF issues

**Key topics**: `PDF generation`, `WeasyPrint`, `base64 images`, `page layout`

---

### 06. openpyxl Excel Generation
**What you'll learn**:
- Creating Excel workbooks with Python
- Writing data to cells
- Styling (fonts, colors, borders, alignment)
- Column widths and row heights
- Formulas and number formatting
- How `planilha_interna.py` generates cost tracking sheets

**Key topics**: `Excel`, `openpyxl`, `spreadsheets`, `styling`, `formulas`

---

### 07. Bash Scripting Basics
**What you'll learn**:
- Shell script fundamentals
- Variables and command-line arguments
- Conditionals and loops
- Running Python from Bash
- Understanding `gerar_teste_pdf.sh` and `gerar_todos_testes.sh`
- Automation patterns

**Key topics**: `bash`, `shell scripts`, `automation`, `command line`

---

## 🎓 Learning Tips

### **For Complete Beginners**
1. **Start with Python Fundamentals** - It's the foundation for everything
2. **Don't skip the examples** - Type them out, don't just read
3. **Use the practice exercises** - They reinforce learning
4. **Take breaks** - Don't try to learn everything in one day
5. **Experiment** - Modify the example code and see what happens

### **For Those with Some Experience**
1. **Skim familiar topics** - Focus on project-specific examples
2. **Jump to relevant sections** - Use the table of contents
3. **Read the "From your code" examples** - See how it's actually used
4. **Try modifying the project** - Best way to learn

### **For Advanced Users**
1. **Use as reference** - Quick lookup for syntax
2. **Focus on project patterns** - See how pieces connect
3. **Read the actual code** - Guides reference line numbers

---

## 🛠️ Hands-On Practice

After reading the guides, try these exercises:

### **Beginner Exercises**
1. Modify a price in `bases/materiais.json` and regenerate PDF
2. Change the primary color in `proposta_styles.css` to your favorite color
3. Add a new field to `config/empresa.json` and display it in the footer
4. Run `./gerar_teste_pdf.sh` and examine the output PDF

### **Intermediate Exercises**
1. Add a new material to `bases/materiais.json` and use it in a test file
2. Modify the proposal template to add a new section
3. Create a custom Bash script that generates PDFs for all test files
4. Adjust the page margins and see how it affects layout

### **Advanced Exercises**
1. Create a new composition in `composicoes.json` with custom components
2. Add a new style to the Excel generator (`planilha_interna.py`)
3. Implement a new filter in Jinja2 for custom formatting
4. Create a custom data validation function for input files

---

## 📁 Project Structure Reference

```
gemini_hvac_layout/
├── hvac/                      # Core Python package
│   ├── pipeline.py           # Main orchestration (covered in Python guide)
│   ├── compositor.py         # Expands compositions (Python guide)
│   ├── precificador.py       # Applies pricing (Python guide)
│   ├── generators/           # Document generators
│   │   ├── proposta_pdf.py  # PDF generation (WeasyPrint guide)
│   │   ├── planilha_interna.py  # Excel generation (openpyxl guide)
│   │   └── utils.py         # Helper functions (Python guide)
│   └── utils/               # Utilities
│       ├── loader.py        # JSON loading (JSON guide)
│       └── metricas.py      # Metrics tracking (Python guide)
│
├── templates/html/           # HTML/CSS templates
│   ├── proposta_base.html   # Main template (HTML & Jinja2 guides)
│   └── proposta_styles.css  # Styling (HTML/CSS guide)
│
├── bases/                    # Data catalogs (JSON guide)
│   ├── materiais.json
│   ├── mao_de_obra.json
│   ├── equipamentos.json
│   ├── composicoes.json
│   └── bdi.json
│
├── config/                   # Configuration (JSON guide)
│   ├── empresa.json
│   ├── condicoes_comerciais.json
│   └── contador.json
│
├── tests/                    # Test data (JSON guide)
│   └── dados_teste_*.json
│
├── gerar_teste_pdf.sh       # Test PDF generator (Bash guide)
└── gerar_todos_testes.sh    # Batch PDF generator (Bash guide)
```

---

## 🔍 Quick Search Guide

Looking for specific information? Use this index:

### **Concepts**
- **Variables**: Python guide → Variables and Data Types
- **Functions**: Python guide → Functions
- **Dictionaries**: Python guide → Data Structures → Dictionaries
- **Lists**: Python guide → Data Structures → Lists
- **Classes**: Python guide → Classes and Objects
- **JSON**: JSON guide → JSON Syntax Rules
- **Templates**: Jinja2 guide → Basic Syntax
- **Styling**: HTML/CSS guide → CSS Fundamentals
- **PDF**: WeasyPrint guide → Converting HTML to PDF
- **Excel**: openpyxl guide → Basic Usage
- **Scripts**: Bash guide → Understanding Project Scripts

### **File Types**
- **`.py` files**: Python guide
- **`.json` files**: JSON guide
- **`.html` files**: HTML/CSS guide + Jinja2 guide
- **`.css` files**: HTML/CSS guide
- **`.sh` files**: Bash guide
- **`.pdf` files**: WeasyPrint guide
- **`.xlsx` files**: openpyxl guide

### **Common Tasks**
- **Modify prices**: JSON guide → Project Data Structure → materiais.json
- **Change colors**: HTML/CSS guide → Understanding the Proposal Template
- **Add new field to template**: Jinja2 guide + HTML/CSS guide
- **Generate PDF**: Bash guide → Understanding Project Scripts
- **Read code**: Python guide → Common Patterns
- **Debug JSON**: JSON guide → Validating and Debugging JSON
- **Fix PDF issues**: WeasyPrint guide → Common Issues and Solutions

---

## 💡 Additional Resources

### **Official Documentation**
- [Python Docs](https://docs.python.org/3/)
- [JSON Specification](https://www.json.org/)
- [Jinja2 Docs](https://jinja.palletsprojects.com/)
- [WeasyPrint Docs](https://doc.courtbouillon.org/weasyprint/)
- [openpyxl Docs](https://openpyxl.readthedocs.io/)
- [Bash Reference](https://www.gnu.org/software/bash/manual/)

### **Online Tools**
- [JSONLint](https://jsonlint.com/) - Validate JSON
- [RegExr](https://regexr.com/) - Test regex patterns
- [Can I Use](https://caniuse.com/) - CSS browser support
- [Python Tutor](http://pythontutor.com/) - Visualize code execution

### **Practice Platforms**
- [Codecademy](https://www.codecademy.com/) - Interactive Python course
- [HackerRank](https://www.hackerrank.com/) - Programming challenges
- [LeetCode](https://leetcode.com/) - Algorithm practice

---

## 🤝 Contributing

Found an error in the guides? Want to add clarification?

1. Note the guide file and section
2. Suggest the improvement
3. Provide example if applicable

---

## 📞 Getting Help

**Stuck on something?**

1. **Re-read the relevant section** - Often answers are there
2. **Check the Quick Reference** - Each guide has one
3. **Look at the real code** - Guides reference actual line numbers
4. **Try the practice exercises** - Hands-on learning helps
5. **Search the official docs** - Links provided above

---

## ✅ Completion Checklist

Track your learning progress:

- [ ] Read Python Fundamentals guide
- [ ] Read JSON Data Structures guide
- [ ] Read Jinja2 Templating guide
- [ ] Read HTML & CSS Basics guide
- [ ] Read WeasyPrint PDF Generation guide
- [ ] Read openpyxl Excel Generation guide
- [ ] Read Bash Scripting Basics guide
- [ ] Generated a test PDF successfully
- [ ] Modified a JSON file and saw the change
- [ ] Changed template styling
- [ ] Created a custom bash script
- [ ] Understand the complete pipeline flow

**Congratulations when all checked! You now understand the entire HVAC project stack! 🎉**

---

## 🎯 Next Steps After Completing Guides

1. **Explore the codebase** - Read through actual implementation files
2. **Make modifications** - Start with small changes
3. **Create new features** - Add functionality you need
4. **Optimize** - Improve performance or structure
5. **Document** - Add comments or documentation for your changes

---

**Happy Learning! 📚✨**

*These guides were created to make this project accessible to learners at all levels. Take your time, practice, and enjoy the journey!*

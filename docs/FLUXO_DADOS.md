# Sistema de Orçamento HVAC - Fluxo de Dados

```mermaid
flowchart TB
    subgraph Entrada["📥 ENTRADA"]
        direction LR
        E1[Email/WhatsApp]
        E2[Arquivo Word]
        E3[Dados Manual]
    end

    subgraph Gestao["gestao_tarefas"]
        direction TB
        G1[📧 Coleta de Dados]
        G2[📝 Preparação]
        G3[📋 Tarefas Asana]
        G4[☁️ Sync Drive]
    end

    subgraph Orcamento["orcamento_hvac"]
        direction TB
        O1[📊 Dados]
        O2[🧮 Cálculo Custos]
        O3[📄 Proposta/Markdown]
        O4[📊 Automations]
    end

    subgraph Gerador["gerador_propostas"]
        direction TB
        GR1[🎨 Templates]
        GR2[📑 Geração PDF]
        GR3[📤 Output]
    end

    subgraph Saida["📤 SAÍDA"]
        direction LR
        S1[📄 Proposta PDF]
        S2[📋 Pacote Execução]
        S3[📊 Registro Orçamento]
    end

    %% Fluxos principais
    Entrada --> Gestao
    Gestao -->|payload| Orcamento
    Orcamento -->|dados precificados| Gerador
    Gerador --> Saida

    %% Conexões secundárias
    Gestao -.->|arquivos| Drive
    Orcamento -.->|armazena| Drive
    
    %% Feedback loops
    Saida -.->|revisão| Orcamento
    Orcamento -.->|atualiza| Gestao
```

---

## Descrição do Fluxo

### 1. Entrada (Coleta)
- **Email/WhatsApp**: Mensagens de clientes
- **Arquivo Word**: Propostas manuais anteriores
- **Dados Manual**: Entrada direta do orçamentista

### 2. gestao_tarefas
- **Coleta**: Extrai dados de emails/mensagens
- **Preparação**: Limpa e estrutura dados
- **Tarefas Asana**: Cria workflow de orçamento
- **Sync Drive**: Sincroniza documentos

### 3. orcamento_hvac
- **Dados**: Catálogos (materiais, composições, etc)
- **Cálculo**: Aplica custos + markups
- **Proposta**: Gera documentos Markdown
- **Automations**: Scripts de geração (v2, etc)

### 4. gerador_propostas
- **Templates**: Layout visual (HTML/CSS)
- **Geração PDF**: Converte para PDF profissional
- **Output**: Arquivos finais

---

## Arquivos de Integração

| De | Para | Arquivo |
|----|------|---------|
| orcamento_hvac | gerador_propostas | `automations/scripts/export_proposal_pdf.py` |
| gestao_tarefas | orcamento_hvac | `automations/scripts/integrate_gestao_orcamentos_v1.py` |

---

## Formato de Dados Entre Módulos

```json
// Payload: orcamento_hvac → gerador_propostas
{
  "projeto": "Expansão Chiller Bloco C",
  "cliente": "Hospital Vida Sul",
  "itens_precificados": [...],
  "resumo_financeiro": { "valor_total": 665073.53 }
}
```

---

## Fluxo Detalhado (Automations)

```mermaid
flowchart LR
    A[generate_proposal_v2.py] --> B[01_cliente_proposta.md]
    A --> C[02_registro_orcamento.md]
    A --> D[03_pacote_execucao.md]
    B --> E[export_proposal_pdf.py]
    E --> F[PDF Final]
```

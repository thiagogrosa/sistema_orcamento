# Guia de Implementação: Novo Layout de Orçamento HVAC

Este documento detalha as mudanças realizadas no layout e na lógica de geração de PDFs para a reincorporação no projeto original.

---

## 1. Mudanças Visuais (Identidade Armant)

*   **Paleta de Cores Oficial:**
    *   **Azul (#0A94D6):** Cor primária usada na estrutura (bordas, linhas de guia, separadores, fundos de títulos) e em textos específicos (Título Principal e Razão Social no Rodapé).
    *   **Verde (#00A859):** Cor secundária usada em acentos (marcadores de lista "▪" e "✓", bordas de destaque).
    *   **Texto:** 100% Preto Puro (#000000) para máxima legibilidade em impressões.
*   **Design de Seções:**
    *   Organização em **Grade Simétrica** (duas colunas) para os termos comerciais, exclusões e qualificações.
    *   **Quadro de Investimento:** Novo bloco de destaque para o valor total, incluindo o valor por extenso.
*   **Marca d'água:** Implementada como uma marca d'água técnica rotacionada em 45º no fundo das páginas, substituindo o texto simples no topo.

---

## 2. Estrutura de Informações

*   **Dados do Cliente:** Reorganizados em duas colunas (Esquerda: Dados Jurídicos | Direita: Contato Direto). Incluídos campos de **E-mail** e **Telefone**.
*   **Novas Seções Numeradas:**
    *   **Seção 2:** Qualificações e Diferenciais (integrada ao fluxo de quebra de página).
    *   **Seção 5:** Elaboração e Atendimento (identificação do responsável com e-mail e telefone).
*   **Rodapé:** Estruturado em 3 linhas para evitar o aspecto "apertado", garantindo clareza nos dados de endereço e contatos fixos da empresa.

---

## 3. Melhorias Técnicas (Python/Jinja2)

*   **Data Automática:** O gerador agora utiliza sempre a data atual (`date.today()`) para a emissão do documento, ignorando datas legadas no JSON.
*   **Assinaturas Digitais:**
    *   Conversão automática de imagens (`.png`) para **Base64** no contexto do Jinja2.
    *   Tamanho ampliado em 80% (máximo de 100px de altura).
    *   **Proteção de Quebra:** Implementada a div `.bloco-fechamento` com `page-break-inside: avoid`, garantindo que as assinaturas nunca fiquem sozinhas em uma página.
*   **Utils:** Correção da acentuação nos meses (ex: "março") na função `data_por_extenso`.

---

## 4. Como Aplicar

1.  Substituir os arquivos em `templates/html/` pelos novos `.html` e `.css`.
2.  Substituir `hvac/generators/proposta_pdf.py` e `hvac/generators/utils.py` para ativar a nova lógica de data e processamento de imagens.
3.  Certificar-se de que as dependências `weasyprint` e `jinja2` estão atualizadas no ambiente.

---
*Implementação finalizada em 07/01/2026.*

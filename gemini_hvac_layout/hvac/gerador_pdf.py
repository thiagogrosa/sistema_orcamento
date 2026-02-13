#!/usr/bin/env python3
"""
Gerador de PDF para orcamentos HVAC
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from fpdf import FPDF


class OrcamentoPDF(FPDF):
    """PDF personalizado para orcamentos HVAC"""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'PROPOSTA COMERCIAL', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')


def formatar_moeda(valor: float) -> str:
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_pdf(precificado: dict, equipamento: dict = None, output_path: str = None) -> str:
    """
    Gera PDF do orcamento

    Args:
        precificado: Dados do orcamento precificado
        equipamento: Dados do equipamento (opcional)
        output_path: Caminho para salvar o PDF

    Returns:
        Caminho do arquivo gerado
    """
    pdf = OrcamentoPDF()
    pdf.add_page()

    # Dados do cabecalho
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Cliente: {precificado.get('cliente', 'N/A')}", new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, f"Projeto: {precificado.get('projeto', 'N/A')}", new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, f"Data: {datetime.now().strftime('%d/%m/%Y')}", new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, f"Validade: {precificado.get('validade_dias', 15)} dias", new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)

    # Linha separadora
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Titulo da tabela
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'ITENS DO ORCAMENTO', new_x='LMARGIN', new_y='NEXT')

    # Cabecalho da tabela
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(15, 8, '#', border=1, fill=True, align='C')
    pdf.cell(130, 8, 'Descricao', border=1, fill=True)
    pdf.cell(45, 8, 'Valor', border=1, fill=True, align='R', new_x='LMARGIN', new_y='NEXT')

    # Itens
    pdf.set_font('Helvetica', '', 10)
    subtotal_servicos = 0

    for item in precificado.get('itens_precificados', []):
        pdf.cell(15, 8, str(item.get('id', '')), border=1, align='C')

        # Truncar descricao se muito longa
        desc = item.get('descricao', '')[:60]
        pdf.cell(130, 8, desc, border=1)

        valor = item.get('preco_total', 0)
        subtotal_servicos += valor
        pdf.cell(45, 8, formatar_moeda(valor), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Subtotal servicos
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(145, 8, 'Subtotal Servicos', border=1, align='R')
    pdf.cell(45, 8, formatar_moeda(subtotal_servicos), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Equipamento (se houver)
    valor_equipamento = 0
    if equipamento:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(15, 8, str(len(precificado.get('itens_precificados', [])) + 1), border=1, align='C')

        desc_eqp = equipamento.get('descricao', 'Equipamento')[:60]
        pdf.cell(130, 8, desc_eqp + ' (fornecimento)', border=1)

        preco_base = equipamento.get('preco_unitario', 0)
        valor_equipamento = preco_base * 1.25  # BDI 25%
        pdf.cell(45, 8, formatar_moeda(valor_equipamento), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Total geral
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(200, 220, 255)
    total_geral = subtotal_servicos + valor_equipamento
    pdf.cell(145, 12, 'VALOR TOTAL', border=1, fill=True, align='R')
    pdf.cell(45, 12, formatar_moeda(total_geral), border=1, fill=True, align='R', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(10)

    # Resumo financeiro
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'COMPOSICAO DE CUSTOS', new_x='LMARGIN', new_y='NEXT')

    resumo = precificado.get('resumo_financeiro', {})

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(60, 7, 'Categoria', border=1, fill=True)
    pdf.cell(40, 7, 'Custo', border=1, fill=True, align='R')
    pdf.cell(25, 7, 'BDI', border=1, fill=True, align='C')
    pdf.cell(40, 7, 'Total', border=1, fill=True, align='R', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 9)

    # Materiais
    pdf.cell(60, 7, 'Materiais', border=1)
    pdf.cell(40, 7, formatar_moeda(resumo.get('total_materiais', 0)), border=1, align='R')
    pdf.cell(25, 7, '35%', border=1, align='C')
    total_mat = resumo.get('total_materiais', 0) + resumo.get('bdi_materiais', 0)
    pdf.cell(40, 7, formatar_moeda(total_mat), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Mao de obra
    pdf.cell(60, 7, 'Mao de Obra', border=1)
    pdf.cell(40, 7, formatar_moeda(resumo.get('total_mao_obra', 0)), border=1, align='R')
    pdf.cell(25, 7, '40%', border=1, align='C')
    total_mo = resumo.get('total_mao_obra', 0) + resumo.get('bdi_mao_obra', 0)
    pdf.cell(40, 7, formatar_moeda(total_mo), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Ferramentas
    pdf.cell(60, 7, 'Ferramentas', border=1)
    pdf.cell(40, 7, formatar_moeda(resumo.get('total_ferramentas', 0)), border=1, align='R')
    pdf.cell(25, 7, '30%', border=1, align='C')
    total_fer = resumo.get('total_ferramentas', 0) + resumo.get('bdi_ferramentas', 0)
    pdf.cell(40, 7, formatar_moeda(total_fer), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    # Equipamento
    if equipamento:
        preco_base = equipamento.get('preco_unitario', 0)
        pdf.cell(60, 7, 'Equipamento', border=1)
        pdf.cell(40, 7, formatar_moeda(preco_base), border=1, align='R')
        pdf.cell(25, 7, '25%', border=1, align='C')
        pdf.cell(40, 7, formatar_moeda(valor_equipamento), border=1, align='R', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(10)

    # Condicoes comerciais
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'CONDICOES COMERCIAIS', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 6,
        "- Pagamento: A combinar\n"
        "- Prazo de execucao: A combinar\n"
        "- Garantia: 90 dias nos servicos de instalacao\n"
        "- Validade da proposta: " + str(precificado.get('validade_dias', 15)) + " dias\n"
        "- Nao inclui: obras civis adicionais, pintura, gesso"
    )

    pdf.ln(10)

    # Observacoes
    if precificado.get('alertas'):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 8, 'OBSERVACOES:', new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 9)
        for alerta in precificado.get('alertas', []):
            pdf.cell(0, 6, f"- {alerta}", new_x='LMARGIN', new_y='NEXT')

    # Salvar
    if output_path is None:
        output_path = "orcamento.pdf"

    pdf.output(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Gera PDF do orcamento HVAC")
    parser.add_argument("--input", "-i", required=True, help="Arquivo precificado.json")
    parser.add_argument("--output", "-o", required=True, help="Arquivo PDF de saida")
    parser.add_argument("--equipamento", "-e", help="Arquivo escopo.json com dados do equipamento")

    args = parser.parse_args()

    # Carregar precificado
    with open(args.input, 'r', encoding='utf-8') as f:
        precificado = json.load(f)

    # Carregar equipamento se informado
    equipamento = None
    if args.equipamento:
        with open(args.equipamento, 'r', encoding='utf-8') as f:
            escopo = json.load(f)
            equipamento = escopo.get('equipamento')

    # Gerar PDF
    output = gerar_pdf(precificado, equipamento, args.output)
    print(f"PDF gerado: {output}")


if __name__ == "__main__":
    main()

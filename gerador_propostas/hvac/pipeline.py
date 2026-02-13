#!/usr/bin/env python3
"""
Pipeline completo de orcamento HVAC com rastreamento de metricas
"""

import argparse
import json
import sys
from pathlib import Path

from .compositor import processar as processar_compositor
from .precificador import processar as processar_precificador
from .utils.loader import carregar_bases
from .utils.metricas import RastreadorMetricas, formatar_metricas


def executar_pipeline(
    escopo_path: str,
    output_dir: str,
    gerar_pdf: bool = False,
    verbose: bool = True
) -> dict:
    """
    Executa pipeline completo de orcamento

    Args:
        escopo_path: Caminho para escopo.json
        output_dir: Diretorio de saida
        gerar_pdf: Se deve gerar PDF
        verbose: Se deve exibir output

    Returns:
        Dicionario com resultado e metricas
    """
    escopo_path = Path(escopo_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iniciar rastreamento
    rastreador = RastreadorMetricas(orcamento_id=output_dir.name)

    # Carregar bases uma vez
    if verbose:
        print("Carregando bases de dados...")
    bases = carregar_bases()

    # 1. Carregar escopo
    if verbose:
        print(f"Lendo escopo: {escopo_path}")
    with open(escopo_path, 'r', encoding='utf-8') as f:
        escopo = json.load(f)

    rastreador.registrar_arquivo("escopo", escopo_path)

    # 2. Executar compositor
    if verbose:
        print("Executando compositor...")
    rastreador.iniciar_etapa()

    composicao = processar_compositor(escopo, bases)

    rastreador.finalizar_etapa("compositor")

    composicao_path = output_dir / "composicao.json"
    with open(composicao_path, 'w', encoding='utf-8') as f:
        json.dump(composicao, f, ensure_ascii=False, indent=2)

    rastreador.registrar_arquivo("composicao", composicao_path)

    # 3. Executar precificador
    if verbose:
        print("Executando precificador...")
    rastreador.iniciar_etapa()

    precificado = processar_precificador(composicao, bases)

    rastreador.finalizar_etapa("precificador")

    precificado_path = output_dir / "precificado.json"
    with open(precificado_path, 'w', encoding='utf-8') as f:
        json.dump(precificado, f, ensure_ascii=False, indent=2)

    rastreador.registrar_arquivo("precificado", precificado_path)
    rastreador.registrar_resultado(precificado)

    # 4. Gerar PDF (opcional)
    if gerar_pdf:
        try:
            from .gerador_pdf import gerar_pdf as gerar_pdf_func

            if verbose:
                print("Gerando PDF...")
            rastreador.iniciar_etapa()

            equipamento = escopo.get('equipamento')
            pdf_path = output_dir / "proposta.pdf"
            gerar_pdf_func(precificado, equipamento, str(pdf_path))

            rastreador.finalizar_etapa("pdf")
            rastreador.registrar_arquivo("pdf", pdf_path)
        except ImportError:
            if verbose:
                print("Aviso: fpdf2 nao instalado, PDF nao gerado")

    # 5. Finalizar metricas
    metricas = rastreador.finalizar()

    metricas_path = output_dir / "metricas.json"
    metricas.salvar(metricas_path)

    if verbose:
        print(formatar_metricas(metricas))

        resumo = precificado['resumo_financeiro']
        print(f"\n{'='*50}")
        print(f"VALOR TOTAL: R$ {resumo['valor_total']:,.2f}")
        print(f"{'='*50}")
        print(f"\nArquivos salvos em: {output_dir}")

    return {
        "precificado": precificado,
        "metricas": metricas.to_dict()
    }


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo de orcamento HVAC"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Arquivo escopo.json"
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help="Diretorio de saida"
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Gerar PDF da proposta"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Modo silencioso"
    )

    args = parser.parse_args()

    resultado = executar_pipeline(
        escopo_path=args.input,
        output_dir=args.output_dir,
        gerar_pdf=args.pdf,
        verbose=not args.quiet
    )

    if args.quiet:
        print(json.dumps(resultado["metricas"], indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Compositor HVAC - Transforma escopo em composicao de materiais/MO/ferramentas

Entrada: escopo.json
Saida: composicao.json
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict

from .utils.loader import carregar_bases, obter_composicao, obter_item


def gerar_descricao(composicao: Dict, variavel: float) -> str:
    """
    Gera descricao formatada usando descricao_variavel se disponivel

    Args:
        composicao: Dados da composicao
        variavel: Valor da variavel (ex: metros de linha)

    Returns:
        Descricao formatada
    """
    desc_var = composicao.get("descricao_variavel")

    if not desc_var:
        return composicao.get("descricao", "")

    prefixo = desc_var.get("prefixo", "")
    sufixo = desc_var.get("sufixo", "")

    # Escolhe singular ou plural
    if variavel == 1:
        unidade = desc_var.get("unidade_singular", "")
    else:
        unidade = desc_var.get("unidade_plural", "")

    # Formata numero (inteiro se possivel)
    if variavel == int(variavel):
        var_str = str(int(variavel))
    else:
        var_str = f"{variavel:.1f}"

    return f"{prefixo}{var_str} {unidade}{sufixo}".strip()


def calcular_quantidade(item: Dict, variavel: float) -> float:
    """
    Calcula quantidade total de um item

    Formula: qtd_base + (qtd_var × variavel)

    Args:
        item: Item da composicao com qtd_base e qtd_var
        variavel: Valor da variavel

    Returns:
        Quantidade total calculada
    """
    qtd_base = item.get("qtd_base", 0)
    qtd_var = item.get("qtd_var", 0)
    return qtd_base + (qtd_var * variavel)


def expandir_composicao(
    codigo_comp: str,
    variavel: float,
    quantidade: int,
    bases: Dict
) -> Optional[Dict[str, Any]]:
    """
    Expande uma composicao em seus itens com quantidades calculadas

    Args:
        codigo_comp: Codigo da composicao (ex: COMP_INST_9K)
        variavel: Valor da variavel (ex: metros de linha)
        quantidade: Quantidade de vezes que a composicao sera executada
        bases: Bases de dados carregadas

    Returns:
        Dicionario com a composicao expandida ou None se nao encontrada
    """
    composicao = obter_composicao(bases, codigo_comp)
    if not composicao:
        return None

    resultado = {
        "codigo": codigo_comp,
        "descricao": gerar_descricao(composicao, variavel),
        "quantidade": quantidade,
        "variavel": variavel,
        "materiais": [],
        "mao_de_obra": [],
        "ferramentas": [],
        "equipamentos": []
    }

    for item in composicao.get("itens", []):
        tipo = item.get("tipo")
        codigo = item.get("codigo")
        qtd_unitaria = calcular_quantidade(item, variavel)
        qtd_total = qtd_unitaria * quantidade

        if qtd_total <= 0:
            continue

        # Busca dados do item na base correspondente
        dados_item = obter_item(bases, tipo, codigo)
        if not dados_item:
            print(f"Aviso: Item {codigo} ({tipo}) nao encontrado na base", file=sys.stderr)
            dados_item = {"descricao": f"[NAO ENCONTRADO] {codigo}"}

        item_expandido = {
            "codigo": codigo,
            "descricao": dados_item.get("descricao", ""),
            "quantidade": round(qtd_total, 2),
            "unidade": dados_item.get("unidade", "UN")
        }

        # Adiciona na categoria correta
        if tipo == "MAT":
            resultado["materiais"].append(item_expandido)
        elif tipo == "MO":
            resultado["mao_de_obra"].append(item_expandido)
        elif tipo == "FER":
            resultado["ferramentas"].append(item_expandido)
        elif tipo == "EQP":
            resultado["equipamentos"].append(item_expandido)

    return resultado


def consolidar_itens(lista_itens: List[Dict]) -> List[Dict]:
    """
    Consolida itens repetidos somando quantidades

    Args:
        lista_itens: Lista de itens (podem ter codigos repetidos)

    Returns:
        Lista consolidada com quantidades somadas
    """
    consolidado = defaultdict(lambda: {"quantidade": 0, "descricao": "", "unidade": ""})

    for item in lista_itens:
        codigo = item["codigo"]
        consolidado[codigo]["quantidade"] += item["quantidade"]
        consolidado[codigo]["descricao"] = item["descricao"]
        consolidado[codigo]["unidade"] = item["unidade"]

    return [
        {
            "codigo": codigo,
            "descricao": dados["descricao"],
            "quantidade": round(dados["quantidade"], 2),
            "unidade": dados["unidade"]
        }
        for codigo, dados in sorted(consolidado.items())
    ]


def processar(escopo: Dict[str, Any], bases: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Processa um escopo e gera a composicao completa

    Args:
        escopo: Dicionario com o escopo do orcamento
        bases: Bases de dados (carrega automaticamente se nao informado)

    Returns:
        Dicionario com a composicao gerada
    """
    if bases is None:
        bases = carregar_bases()

    projeto = escopo.get("projeto", {})

    resultado = {
        "projeto": projeto.get("nome", "Sem nome"),
        "cliente": projeto.get("cliente"),
        "data_composicao": date.today().isoformat(),
        "itens_orcamento": [],
        "resumo_materiais": [],
        "resumo_mao_obra": [],
        "resumo_ferramentas": [],
        "resumo_equipamentos": [],
        "observacoes": []
    }

    # Acumuladores para consolidacao
    todos_materiais = []
    toda_mao_obra = []
    todas_ferramentas = []
    todos_equipamentos = []

    # Processa cada item do escopo
    for idx, item in enumerate(escopo.get("itens", []), start=1):
        codigo_comp = item.get("composicao")
        variavel = item.get("variavel", 0)
        quantidade = item.get("quantidade", 1)

        if not codigo_comp:
            resultado["observacoes"].append(f"Item {idx}: sem composicao definida")
            continue

        comp_expandida = expandir_composicao(codigo_comp, variavel, quantidade, bases)

        if not comp_expandida:
            resultado["observacoes"].append(f"Item {idx}: composicao {codigo_comp} nao encontrada")
            continue

        # Adiciona item expandido
        resultado["itens_orcamento"].append({
            "id": idx,
            "descricao": item.get("descricao", comp_expandida["descricao"]),
            "composicao": codigo_comp,
            "quantidade": quantidade,
            "variavel": variavel,
            "materiais": comp_expandida["materiais"],
            "mao_de_obra": comp_expandida["mao_de_obra"],
            "ferramentas": comp_expandida["ferramentas"],
            "equipamentos": comp_expandida["equipamentos"]
        })

        # Acumula para consolidacao
        todos_materiais.extend(comp_expandida["materiais"])
        toda_mao_obra.extend(comp_expandida["mao_de_obra"])
        todas_ferramentas.extend(comp_expandida["ferramentas"])
        todos_equipamentos.extend(comp_expandida["equipamentos"])

    # Consolida resumos
    resultado["resumo_materiais"] = consolidar_itens(todos_materiais)
    resultado["resumo_mao_obra"] = consolidar_itens(toda_mao_obra)
    resultado["resumo_ferramentas"] = consolidar_itens(todas_ferramentas)
    resultado["resumo_equipamentos"] = consolidar_itens(todos_equipamentos)

    return resultado


def main():
    """CLI principal"""
    parser = argparse.ArgumentParser(
        description="Compositor HVAC - Transforma escopo em composicao"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Arquivo JSON de entrada (escopo)"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Arquivo JSON de saida (composicao)"
    )
    parser.add_argument(
        "--bases-dir",
        help="Diretorio das bases de dados (opcional)"
    )

    args = parser.parse_args()

    # Carrega escopo
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Erro: Arquivo de entrada nao encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        escopo = json.load(f)

    # Carrega bases
    bases_dir = Path(args.bases_dir) if args.bases_dir else None
    bases = carregar_bases(bases_dir)

    # Processa
    composicao = processar(escopo, bases)

    # Salva resultado
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(composicao, f, ensure_ascii=False, indent=2)

    print(f"Composicao gerada: {output_path}")


if __name__ == "__main__":
    main()

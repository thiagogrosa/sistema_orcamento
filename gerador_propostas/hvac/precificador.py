#!/usr/bin/env python3
"""
Precificador HVAC - Aplica precos e BDI para gerar orcamento final

Entrada: composicao.json
Saida: precificado.json
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .utils.loader import carregar_bases, obter_item, obter_bdi


# Dias para considerar preco desatualizado
DIAS_ALERTA_PRECO = 90
DIAS_CRITICO_PRECO = 180


def obter_preco_item(bases: Dict, tipo: str, codigo: str) -> Tuple[float, Optional[str]]:
    """
    Obtem o preco/custo de um item

    Args:
        bases: Bases de dados
        tipo: Tipo do item (MAT, MO, FER, EQP)
        codigo: Codigo do item

    Returns:
        Tupla (preco, data_atualizacao)
    """
    item = obter_item(bases, tipo, codigo)
    if not item:
        return 0.0, None

    # Campo de preco varia por tipo
    if tipo == "MAT":
        preco = item.get("preco", 0.0)
    elif tipo == "MO":
        preco = item.get("custo_hora", 0.0)
    elif tipo == "FER":
        preco = item.get("custo_hora", 0.0)
    elif tipo == "EQP":
        preco = item.get("comercial", {}).get("preco", 0.0)
    else:
        preco = 0.0

    data_atualizacao = item.get("data_atualizacao")
    return preco, data_atualizacao


def verificar_preco_desatualizado(data_str: Optional[str]) -> Optional[str]:
    """
    Verifica se um preco esta desatualizado

    Args:
        data_str: Data de atualizacao em formato ISO (YYYY-MM-DD)

    Returns:
        None se OK, "alerta" ou "critico" se desatualizado
    """
    if not data_str:
        return "critico"

    try:
        data = datetime.fromisoformat(data_str).date()
        dias = (date.today() - data).days

        if dias > DIAS_CRITICO_PRECO:
            return "critico"
        elif dias > DIAS_ALERTA_PRECO:
            return "alerta"
        return None
    except ValueError:
        return "critico"


def precificar_lista(
    itens: List[Dict],
    tipo: str,
    bases: Dict,
    alertas: List[str]
) -> Tuple[List[Dict], float]:
    """
    Precifica uma lista de itens

    Args:
        itens: Lista de itens com codigo e quantidade
        tipo: Tipo dos itens (MAT, MO, FER, EQP)
        bases: Bases de dados
        alertas: Lista para adicionar alertas

    Returns:
        Tupla (lista_precificada, custo_total)
    """
    resultado = []
    custo_total = 0.0

    for item in itens:
        codigo = item["codigo"]
        quantidade = item["quantidade"]

        preco_unit, data_atualizacao = obter_preco_item(bases, tipo, codigo)
        custo = preco_unit * quantidade

        # Verifica desatualizacao
        status = verificar_preco_desatualizado(data_atualizacao)
        if status:
            alertas.append(f"Preco {status}: {codigo} ({tipo}) - atualizado em {data_atualizacao or 'N/A'}")

        resultado.append({
            "codigo": codigo,
            "descricao": item.get("descricao", ""),
            "quantidade": quantidade,
            "unidade": item.get("unidade", "UN"),
            "preco_unitario": round(preco_unit, 2),
            "custo": round(custo, 2)
        })

        custo_total += custo

    return resultado, custo_total


def processar(composicao: Dict[str, Any], bases: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Processa uma composicao e gera o orcamento precificado

    Args:
        composicao: Dicionario com a composicao
        bases: Bases de dados (carrega automaticamente se nao informado)

    Returns:
        Dicionario com o orcamento precificado
    """
    if bases is None:
        bases = carregar_bases()

    alertas = []

    resultado = {
        "projeto": composicao.get("projeto", "Sem nome"),
        "cliente": composicao.get("cliente"),
        "data_orcamento": date.today().isoformat(),
        "validade_dias": 15,
        "itens_precificados": [],
        "resumo_financeiro": {
            "total_materiais": 0.0,
            "total_mao_obra": 0.0,
            "total_ferramentas": 0.0,
            "total_equipamentos": 0.0,
            "custo_direto": 0.0,
            "bdi_materiais": 0.0,
            "bdi_mao_obra": 0.0,
            "bdi_ferramentas": 0.0,
            "bdi_equipamentos": 0.0,
            "total_bdi": 0.0,
            "valor_total": 0.0
        },
        "alertas": []
    }

    # Obtem percentuais de BDI
    bdi_mat = obter_bdi(bases, "MAT")
    bdi_mo = obter_bdi(bases, "MO")
    bdi_fer = obter_bdi(bases, "FER")
    bdi_eqp = obter_bdi(bases, "EQP")

    # Totais acumulados
    total_mat = 0.0
    total_mo = 0.0
    total_fer = 0.0
    total_eqp = 0.0

    # Processa cada item do orcamento
    for item in composicao.get("itens_orcamento", []):
        # Precifica cada categoria
        mat_prec, custo_mat = precificar_lista(item.get("materiais", []), "MAT", bases, alertas)
        mo_prec, custo_mo = precificar_lista(item.get("mao_de_obra", []), "MO", bases, alertas)
        fer_prec, custo_fer = precificar_lista(item.get("ferramentas", []), "FER", bases, alertas)
        eqp_prec, custo_eqp = precificar_lista(item.get("equipamentos", []), "EQP", bases, alertas)

        custo_direto = custo_mat + custo_mo + custo_fer + custo_eqp

        # Calcula BDI por categoria
        bdi_val_mat = custo_mat * bdi_mat
        bdi_val_mo = custo_mo * bdi_mo
        bdi_val_fer = custo_fer * bdi_fer
        bdi_val_eqp = custo_eqp * bdi_eqp
        bdi_total = bdi_val_mat + bdi_val_mo + bdi_val_fer + bdi_val_eqp

        preco_total = custo_direto + bdi_total

        resultado["itens_precificados"].append({
            "id": item.get("id"),
            "descricao": item.get("descricao", ""),
            "composicao": item.get("composicao"),
            "quantidade": item.get("quantidade", 1),
            "variavel": item.get("variavel", 0),
            "materiais": mat_prec,
            "mao_de_obra": mo_prec,
            "ferramentas": fer_prec,
            "equipamentos": eqp_prec,
            "custo_materiais": round(custo_mat, 2),
            "custo_mao_obra": round(custo_mo, 2),
            "custo_ferramentas": round(custo_fer, 2),
            "custo_equipamentos": round(custo_eqp, 2),
            "custo_direto": round(custo_direto, 2),
            "bdi": round(bdi_total, 2),
            "preco_total": round(preco_total, 2)
        })

        # Acumula totais
        total_mat += custo_mat
        total_mo += custo_mo
        total_fer += custo_fer
        total_eqp += custo_eqp

    # Calcula resumo financeiro
    custo_direto_total = total_mat + total_mo + total_fer + total_eqp

    bdi_total_mat = total_mat * bdi_mat
    bdi_total_mo = total_mo * bdi_mo
    bdi_total_fer = total_fer * bdi_fer
    bdi_total_eqp = total_eqp * bdi_eqp
    bdi_total = bdi_total_mat + bdi_total_mo + bdi_total_fer + bdi_total_eqp

    valor_total = custo_direto_total + bdi_total

    resultado["resumo_financeiro"] = {
        "total_materiais": round(total_mat, 2),
        "total_mao_obra": round(total_mo, 2),
        "total_ferramentas": round(total_fer, 2),
        "total_equipamentos": round(total_eqp, 2),
        "custo_direto": round(custo_direto_total, 2),
        "bdi_materiais": round(bdi_total_mat, 2),
        "bdi_mao_obra": round(bdi_total_mo, 2),
        "bdi_ferramentas": round(bdi_total_fer, 2),
        "bdi_equipamentos": round(bdi_total_eqp, 2),
        "total_bdi": round(bdi_total, 2),
        "valor_total": round(valor_total, 2),
        "percentuais_bdi": {
            "MAT": f"{bdi_mat * 100:.0f}%",
            "MO": f"{bdi_mo * 100:.0f}%",
            "FER": f"{bdi_fer * 100:.0f}%",
            "EQP": f"{bdi_eqp * 100:.0f}%"
        }
    }

    # Remove alertas duplicados
    resultado["alertas"] = list(set(alertas))

    return resultado


def main():
    """CLI principal"""
    parser = argparse.ArgumentParser(
        description="Precificador HVAC - Aplica precos e BDI"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Arquivo JSON de entrada (composicao)"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Arquivo JSON de saida (precificado)"
    )
    parser.add_argument(
        "--bases-dir",
        help="Diretorio das bases de dados (opcional)"
    )

    args = parser.parse_args()

    # Carrega composicao
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Erro: Arquivo de entrada nao encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        composicao = json.load(f)

    # Carrega bases
    bases_dir = Path(args.bases_dir) if args.bases_dir else None
    bases = carregar_bases(bases_dir)

    # Processa
    precificado = processar(composicao, bases)

    # Salva resultado
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(precificado, f, ensure_ascii=False, indent=2)

    # Exibe resumo
    resumo = precificado["resumo_financeiro"]
    print(f"Orcamento precificado: {output_path}")
    print(f"  Custo direto: R$ {resumo['custo_direto']:,.2f}")
    print(f"  BDI total:    R$ {resumo['total_bdi']:,.2f}")
    print(f"  VALOR TOTAL:  R$ {resumo['valor_total']:,.2f}")

    if precificado["alertas"]:
        print(f"\n  Alertas: {len(precificado['alertas'])}")


if __name__ == "__main__":
    main()

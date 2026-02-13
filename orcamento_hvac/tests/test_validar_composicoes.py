"""Testes do validador de composições (regras básicas + avançadas)."""

import json
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validar_composicoes import (
    SEVERITY_ERROR,
    SEVERITY_WARNING,
    gerar_relatorio_json,
    validar_dataset,
)


BASE_MAT = [("MAT_OK", "CAT", "Desc", "UN", 1.0, "", 10)]
BASE_MO = [("MO_OK", "CAT", "Desc", "H", 1.0, "", 10)]
BASE_FER = [("FER_OK", "CAT", "Desc", "UN", 1.0, "", 10)]
BASE_EQP = [("EQP_OK", "CAT", "Desc", "UN", 1.0, "", 10)]


def _run(composicoes):
    return validar_dataset(composicoes, BASE_MAT, BASE_MO, BASE_FER, BASE_EQP)


def test_happy_path_sem_erros():
    comps = [
        {
            "codigo": "COMP_INST_TST",
            "descricao": "Instalação de teste",
            "unid_sing": "metro",
            "unid_plur": "metros",
            "itens": [
                ("MAT", "MAT_OK", 1, 0),
                ("MAT", "MAT_OK", 0, 1.2),
                ("MO", "MO_OK", 1, 0.1),
            ],
        }
    ]

    findings = _run(comps)
    erros = [f for f in findings if f["severidade"] == SEVERITY_ERROR]
    assert erros == []


def test_detecta_codigo_orfao_e_qtd_negativa():
    comps = [
        {
            "codigo": "COMP_A",
            "descricao": "Comp A",
            "itens": [("MAT", "INEXISTENTE", -1, 0)],
        }
    ]

    findings = _run(comps)
    regras = {f["regra"] for f in findings}
    assert "ORPHAN_ITEM_CODE" in regras
    assert "NEGATIVE_QUANTITY" in regras


def test_detecta_estrutura_item_invalida():
    comps = [{"codigo": "COMP_A", "descricao": "Comp A", "itens": [("MAT", "MAT_OK")]}]
    findings = _run(comps)
    assert any(f["regra"] == "INVALID_ITEM_STRUCTURE" for f in findings)


def test_detecta_inconsistencia_unidade_variavel():
    comps = [
        {
            "codigo": "COMP_VAR",
            "descricao": "Comp variavel",
            "unid_sing": "",
            "unid_plur": "",
            "itens": [("MAT", "MAT_OK", 0, 2)],
        }
    ]
    findings = _run(comps)
    assert any(f["regra"] == "VARIABLE_UNIT_MISSING" for f in findings)


def test_detecta_outlier():
    comps = [
        {
            "codigo": "COMP_OUT",
            "descricao": "Comp outlier",
            "itens": [("MO", "MO_OK", 999, 0)],
        }
    ]
    findings = _run(comps)
    assert any(f["regra"] == "OUTLIER_QTD_BASE" and f["severidade"] == SEVERITY_WARNING for f in findings)


def test_detecta_codigo_duplicado():
    comps = [
        {"codigo": "COMP_DUP", "descricao": "A", "itens": [("MAT", "MAT_OK", 1, 0)]},
        {"codigo": "COMP_DUP", "descricao": "B", "itens": [("MAT", "MAT_OK", 1, 0)]},
    ]
    findings = _run(comps)
    assert any(f["regra"] == "DUPLICATE_COMPOSITION_CODE" for f in findings)


def test_gera_relatorio_json(tmp_path):
    comps = [{"codigo": "COMP_A", "descricao": "Comp A", "itens": [("MAT", "MAT_OK", 1, 0)]}]
    findings = _run(comps)

    out = tmp_path / "validacao.json"
    gerar_relatorio_json(out, comps, findings)

    data = json.loads(out.read_text(encoding="utf-8"))
    assert "meta" in data
    assert "resumo" in data
    assert "findings" in data
    assert data["meta"]["total_composicoes"] == 1


def test_cobertura_minima_nao_aplica_para_comp_nao_instalacao():
    comps = [
        {
            "codigo": "COMP_DESINST_TST",
            "descricao": "Desinstalação de teste",
            "itens": [("MAT", "MAT_OK", 1, 0), ("MO", "MO_OK", 1, 0)],
        }
    ]
    findings = _run(comps)
    regras = {f["regra"] for f in findings}
    assert "MISSING_MIN_COVERAGE_ELETRICA" not in regras
    assert "MISSING_MIN_COVERAGE_DRENO" not in regras
    assert "MISSING_MIN_COVERAGE_ACABAMENTO" not in regras


def test_cobertura_minima_detecta_faltas_em_comp_instalacao():
    comps = [
        {
            "codigo": "COMP_INST_TST2",
            "descricao": "Instalação de teste sem dreno",
            "unid_sing": "metro",
            "unid_plur": "metros",
            "itens": [
                ("MAT", "CAB_PP_15", 1, 0),  # elétrica presente
                ("MAT", "ACA_FITA_TER", 1, 0),  # acabamento presente
                ("MO", "MO_OK", 1, 0),
            ],
        }
    ]

    findings = validar_dataset(
        comps,
        BASE_MAT + [("CAB_PP_15", "CAT", "Desc", "M", 1.0, "", 1), ("ACA_FITA_TER", "CAT", "Desc", "M", 1.0, "", 1)],
        BASE_MO,
        BASE_FER,
        BASE_EQP,
    )

    regras = {f["regra"] for f in findings}
    assert "MISSING_MIN_COVERAGE_DRENO" in regras
    assert "MISSING_MIN_COVERAGE_ELETRICA" not in regras
    assert "MISSING_MIN_COVERAGE_ACABAMENTO" not in regras

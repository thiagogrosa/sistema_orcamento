#!/usr/bin/env python3
"""
Validador de integridade das composições (v2).

Checks básicos:
1) Código de item existe na base correspondente (MAT/MO/FER/EQP)
2) Quantidades negativas
3) Composição sem itens
4) Estrutura inválida de item

Checks avançados:
5) Consistência de unidade variável
6) Outliers de quantidade por tipo de item
7) Duplicidade de código/descrição e alta similaridade estrutural
8) Cobertura mínima (elétrica, dreno, acabamento) para composições vendáveis
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from dados import COMPOSICOES, EQUIPAMENTOS, FERRAMENTAS, MAO_DE_OBRA, MATERIAIS

RULES_VERSION = "v2"

SEVERITY_ERROR = "erro"
SEVERITY_WARNING = "alerta"
SEVERITY_INFO = "info"

OUTLIER_LIMITS = {
    "MAT": {"qtd_base": 500.0, "qtd_var": 200.0},
    "MO": {"qtd_base": 24.0, "qtd_var": 8.0},
    "FER": {"qtd_base": 24.0, "qtd_var": 8.0},
    "EQP": {"qtd_base": 10.0, "qtd_var": 2.0},
}


def _codigos_base(registros):
    codigos = set()
    for item in registros:
        if isinstance(item, (list, tuple)) and item:
            codigos.add(item[0])
        elif isinstance(item, dict) and "codigo" in item:
            codigos.add(item["codigo"])
    return codigos


def _norm_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _extract_capacity_k(codigo: str) -> str | None:
    m = re.search(r"(\d+K)", str(codigo or ""))
    return m.group(1) if m else None


def _family_signature(codigo: str) -> str:
    code = str(codigo or "")

    # Normalize known aliases/families to reduce false positives in valid variants.
    if code.startswith("COMP_INST_HW_") or code == "COMP_INST_9K":
        return "COMP_INST_HW"
    if code.startswith("COMP_INST_CS1_") or code.startswith("COMP_INST_CS4_"):
        return "COMP_INST_CS"

    parts = code.split("_")
    if not parts:
        return code
    # remove trailing capacity token when present
    if parts and re.fullmatch(r"\d+K", parts[-1] or ""):
        parts = parts[:-1]
    return "_".join(parts)


def _accepted_variant_reason(cod_a: str, cod_b: str) -> str | None:
    cap_a = _extract_capacity_k(cod_a)
    cap_b = _extract_capacity_k(cod_b)
    fam_a = _family_signature(cod_a)
    fam_b = _family_signature(cod_b)

    # Same normalized family with different capacity is acceptable.
    if fam_a == fam_b and cap_a and cap_b and cap_a != cap_b:
        return f"variante de capacidade ({cap_a} vs {cap_b})"

    # Cassette 1-way vs 4-way with same capacity is acceptable variant by topology.
    if cap_a and cap_b and cap_a == cap_b:
        a_cs = cod_a.startswith("COMP_INST_CS1_") or cod_a.startswith("COMP_INST_CS4_")
        b_cs = cod_b.startswith("COMP_INST_CS1_") or cod_b.startswith("COMP_INST_CS4_")
        if a_cs and b_cs and cod_a.split("_")[2] != cod_b.split("_")[2]:
            return f"variante de topologia de cassete (mesma capacidade {cap_a})"

    return None


def _add_finding(
    findings: list[dict[str, Any]],
    severidade: str,
    regra: str,
    composicao: str,
    mensagem: str,
    item: str | None = None,
    acao_sugerida: str | None = None,
):
    registro: dict[str, Any] = {
        "severidade": severidade,
        "regra": regra,
        "composicao": composicao,
        "mensagem": mensagem,
    }
    if item:
        registro["item"] = item
    if acao_sugerida:
        registro["acao_sugerida"] = acao_sugerida
    findings.append(registro)


def validar_dataset(composicoes, materiais, mao_de_obra, ferramentas, equipamentos):
    bases = {
        "MAT": _codigos_base(materiais),
        "MO": _codigos_base(mao_de_obra),
        "FER": _codigos_base(ferramentas),
        "EQP": _codigos_base(equipamentos),
    }

    findings: list[dict[str, Any]] = []
    codigos_vistos: dict[str, str] = {}
    descricoes: dict[str, list[str]] = {}
    estruturas: list[tuple[str, set[tuple[str, str]], str]] = []

    for comp in composicoes:
        codigo_comp = comp.get("codigo", "<sem_codigo>")
        descricao = comp.get("descricao", "")
        itens = comp.get("itens", [])

        if codigo_comp in codigos_vistos:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "DUPLICATE_COMPOSITION_CODE",
                codigo_comp,
                f"código de composição duplicado (também em {codigos_vistos[codigo_comp]})",
                acao_sugerida="manter códigos únicos por composição",
            )
        else:
            codigos_vistos[codigo_comp] = codigo_comp

        desc_norm = _norm_text(descricao)
        if desc_norm:
            descricoes.setdefault(desc_norm, []).append(codigo_comp)

        if not itens:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "EMPTY_COMPOSITION",
                codigo_comp,
                "composição sem itens",
                acao_sugerida="incluir ao menos um item válido",
            )
            continue

        has_var_item = False
        estrutura_atual: set[tuple[str, str]] = set()
        codigos_itens = []

        for i, item in enumerate(itens, start=1):
            try:
                tipo, codigo, qtd_base, qtd_var = item
            except Exception:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "INVALID_ITEM_STRUCTURE",
                    codigo_comp,
                    "item com estrutura diferente de (tipo,codigo,qtd_base,qtd_var)",
                    item=f"item#{i}",
                    acao_sugerida="corrigir estrutura da tupla do item",
                )
                continue

            estrutura_atual.add((str(tipo), str(codigo)))
            codigos_itens.append(str(codigo))

            if tipo not in bases:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "INVALID_ITEM_TYPE",
                    codigo_comp,
                    f"tipo inválido '{tipo}'",
                    item=f"item#{i}",
                )
                continue

            if codigo not in bases[tipo]:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "ORPHAN_ITEM_CODE",
                    codigo_comp,
                    f"código órfão {tipo}:{codigo}",
                    item=f"item#{i}",
                    acao_sugerida="ajustar código ou cadastrar item na base",
                )

            if qtd_base < 0 or qtd_var < 0:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "NEGATIVE_QUANTITY",
                    codigo_comp,
                    f"quantidade negativa ({qtd_base}, {qtd_var})",
                    item=f"item#{i} {tipo}:{codigo}",
                )

            if qtd_base == 0 and qtd_var == 0:
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "ZERO_QUANTITY_ITEM",
                    codigo_comp,
                    "item com quantidades zeradas",
                    item=f"item#{i} {tipo}:{codigo}",
                )

            if qtd_var > 0:
                has_var_item = True

            limits = OUTLIER_LIMITS.get(tipo, {})
            if qtd_base > limits.get("qtd_base", float("inf")):
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "OUTLIER_QTD_BASE",
                    codigo_comp,
                    f"qtd_base fora da faixa esperada ({qtd_base})",
                    item=f"item#{i} {tipo}:{codigo}",
                    acao_sugerida="revisar coeficiente técnico",
                )

            if qtd_var > limits.get("qtd_var", float("inf")):
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "OUTLIER_QTD_VAR",
                    codigo_comp,
                    f"qtd_var fora da faixa esperada ({qtd_var})",
                    item=f"item#{i} {tipo}:{codigo}",
                    acao_sugerida="revisar coeficiente variável",
                )

        has_units = bool((comp.get("unid_sing") or "").strip()) and bool((comp.get("unid_plur") or "").strip())
        if has_var_item and not has_units:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "VARIABLE_UNIT_MISSING",
                codigo_comp,
                "composição variável sem unid_sing/unid_plur",
                acao_sugerida="preencher unidade singular/plural",
            )
        if has_units and not has_var_item:
            _add_finding(
                findings,
                SEVERITY_WARNING,
                "UNITS_WITHOUT_VARIABLE_ITEMS",
                codigo_comp,
                "unid_sing/unid_plur preenchidos sem item com qtd_var > 0",
                acao_sugerida="remover unidade variável ou ajustar itens",
            )

        # Cobertura mínima: aplica apenas para composições de instalação (COMP_INST*),
        # evitando falsos positivos em cenários como desinstalação.
        vendavel = str(codigo_comp).startswith("COMP_INST") and not str(codigo_comp).startswith("COMP_DESINST")
        if vendavel:
            texto_itens = " ".join(codigos_itens)

            # Tokens ampliados para reduzir falsos positivos sem perder sinal operacional.
            has_eletrica = any(tok in texto_itens for tok in ["CAB", "ELE", "FIO", "DISJ"])
            has_dreno = any(tok in texto_itens for tok in ["DRE", "DRENO", "DRN"])
            has_acab = any(tok in texto_itens for tok in ["ACA_", "ACAB", "GRELHA", "FITA"])

            if not has_eletrica:
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "MISSING_MIN_COVERAGE_ELETRICA",
                    codigo_comp,
                    "composição vendável sem indício de cobertura elétrica",
                )
            if not has_dreno:
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "MISSING_MIN_COVERAGE_DRENO",
                    codigo_comp,
                    "composição vendável sem indício de cobertura de dreno",
                )
            if not has_acab:
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "MISSING_MIN_COVERAGE_ACABAMENTO",
                    codigo_comp,
                    "composição vendável sem indício de acabamento",
                )

        estruturas.append((codigo_comp, estrutura_atual, desc_norm))

    for desc_norm, cods in descricoes.items():
        if len(cods) > 1:
            for cod in cods:
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "DUPLICATE_DESCRIPTION_EXACT",
                    cod,
                    f"descrição idêntica a outras composições: {', '.join(c for c in cods if c != cod)}",
                    acao_sugerida="consolidar ou diferenciar descrições",
                )

    for i in range(len(estruturas)):
        cod_a, itens_a, desc_a = estruturas[i]
        for j in range(i + 1, len(estruturas)):
            cod_b, itens_b, desc_b = estruturas[j]
            if cod_a == cod_b:
                continue

            sim_desc = 0.0
            sim_struct = 0.0

            if desc_a and desc_b:
                sim_desc = SequenceMatcher(None, desc_a, desc_b).ratio()

            if itens_a and itens_b:
                inter = len(itens_a.intersection(itens_b))
                union = len(itens_a.union(itens_b))
                sim_struct = inter / union if union else 0.0

            # Similaridade de descrição com guarda de variantes por família/capacidade.
            if sim_desc >= 0.95 and sim_struct >= 0.80:
                reason = _accepted_variant_reason(cod_a, cod_b)
                if reason:
                    _add_finding(
                        findings,
                        SEVERITY_INFO,
                        "DESCRIPTION_SIMILARITY_ACCEPTED_VARIANT",
                        cod_a,
                        f"descrição semelhante a {cod_b}, mas {reason}",
                    )
                else:
                    _add_finding(
                        findings,
                        SEVERITY_WARNING,
                        "DESCRIPTION_HIGH_SIMILARITY",
                        cod_a,
                        f"descrição muito parecida com {cod_b} (similaridade={sim_desc:.2f}, jaccard={sim_struct:.2f})",
                    )

            if sim_struct >= 0.90:
                _add_finding(
                    findings,
                    SEVERITY_INFO,
                    "STRUCTURE_HIGH_SIMILARITY",
                    cod_a,
                    f"estrutura muito semelhante à composição {cod_b} (jaccard={sim_struct:.2f})",
                )

    return findings


def _summarize(findings: list[dict[str, Any]]):
    return {
        "erros": sum(1 for f in findings if f["severidade"] == SEVERITY_ERROR),
        "avisos": sum(1 for f in findings if f["severidade"] == SEVERITY_WARNING),
        "infos": sum(1 for f in findings if f["severidade"] == SEVERITY_INFO),
    }


def validar_composicoes():
    findings = validar_dataset(COMPOSICOES, MATERIAIS, MAO_DE_OBRA, FERRAMENTAS, EQUIPAMENTOS)
    erros = [f"{f['composicao']}: {f['mensagem']}" for f in findings if f["severidade"] == SEVERITY_ERROR]
    avisos = [f"{f['composicao']}: {f['mensagem']}" for f in findings if f["severidade"] == SEVERITY_WARNING]
    return erros, avisos


def gerar_relatorio_markdown(path: Path, composicoes, findings):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resumo = _summarize(findings)

    linhas = [
        "# Relatório de Validação de Composições",
        "",
        f"Gerado em: {ts}",
        "",
        "## Resumo",
        f"- Total de composições: {len(composicoes)}",
        f"- Erros: {resumo['erros']}",
        f"- Avisos: {resumo['avisos']}",
        f"- Infos: {resumo['infos']}",
        "",
    ]

    for severidade, titulo in [
        (SEVERITY_ERROR, "Erros"),
        (SEVERITY_WARNING, "Avisos"),
        (SEVERITY_INFO, "Infos"),
    ]:
        linhas.append(f"## {titulo}")
        subset = [f for f in findings if f["severidade"] == severidade]
        if not subset:
            linhas.append(f"- Nenhum {severidade}")
            linhas.append("")
            continue

        for f in subset:
            item = f" | {f['item']}" if "item" in f else ""
            acao = f" | ação: {f['acao_sugerida']}" if "acao_sugerida" in f else ""
            linhas.append(f"- [{f['regra']}] {f['composicao']}{item}: {f['mensagem']}{acao}")
        linhas.append("")

    linhas.append("## Critérios aplicados")
    linhas.append("- Integridade de referências (MAT/MO/FER/EQP)")
    linhas.append("- Estrutura de item e quantidades negativas")
    linhas.append("- Coerência de unidade variável")
    linhas.append("- Outliers de quantidade")
    linhas.append("- Duplicidade/similaridade de composições")
    linhas.append("- Cobertura mínima (elétrica, dreno, acabamento)")
    linhas.append("")
    linhas.append("## Saída JSON")
    linhas.append("- Arquivo: relatorio-validacao-composicoes.json")
    linhas.append(f"- Versão de regras: {RULES_VERSION}")

    path.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def gerar_relatorio_json(path: Path, composicoes, findings):
    resumo = _summarize(findings)
    payload = {
        "meta": {
            "gerado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
            "total_composicoes": len(composicoes),
            "versao_regras": RULES_VERSION,
        },
        "resumo": resumo,
        "findings": findings,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    findings = validar_dataset(COMPOSICOES, MATERIAIS, MAO_DE_OBRA, FERRAMENTAS, EQUIPAMENTOS)

    base_dir = Path(__file__).parent
    out_md = base_dir / "relatorio-validacao-composicoes.md"
    out_json = base_dir / "relatorio-validacao-composicoes.json"

    gerar_relatorio_markdown(out_md, COMPOSICOES, findings)
    gerar_relatorio_json(out_json, COMPOSICOES, findings)

    resumo = _summarize(findings)
    print(f"Composições validadas: {len(COMPOSICOES)}")
    print(f"Erros: {resumo['erros']}")
    print(f"Avisos: {resumo['avisos']}")
    print(f"Infos: {resumo['infos']}")
    print(f"Relatório MD: {out_md}")
    print(f"Relatório JSON: {out_json}")

    raise SystemExit(1 if resumo["erros"] else 0)


if __name__ == "__main__":
    main()

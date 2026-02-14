#!/usr/bin/env python3
"""
Gerador de propostas baseado em COMPOSIÇÕES.
Cada composição já inclui materiais + mão de obra + ferramentas.
O sistema aplica BDI (Markup por tipo) + markup comercial.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import date
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
BASES_DIR = ROOT.parent / "gerador_propostas" / "bases"


def money(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def load_bases():
    bases = {}
    for nome in ["materiais", "mao_de_obra", "ferramentas", "equipamentos", "composicoes", "bdi"]:
        path = BASES_DIR / f"{nome}.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                bases[nome] = data.get(nome, data)
    return bases


def get_bdi(bases: Dict, tipo: str) -> float:
    bdi = bases.get("bdi", {})
    return bdi.get(tipo, {}).get("percentual", 0.0)


def get_item_price(bases: Dict, tipo: str, codigo: str, apply_bdi: bool = True) -> float:
    base_name = {"MAT": "materiais", "MO": "mao_de_obra", "FER": "ferramentas", "EQP": "equipamentos"}.get(tipo)
    if not base_name or base_name not in bases:
        return 0.0
    item = bases[base_name].get(codigo, {})
    if not item:
        return 0.0
    if tipo == "MAT":
        cost = item.get("preco", 0.0)
    elif tipo == "MO":
        cost = item.get("custo_hora", 0.0)
    elif tipo == "FER":
        cost = item.get("custo_hora", 0.0)
    elif tipo == "EQP":
        cost = item.get("comercial", {}).get("preco", 0.0)
    else:
        cost = 0.0
    if apply_bdi:
        bdi_pct = get_bdi(bases, tipo)
        cost = cost * (1 + bdi_pct)
    return cost


def calculate_composition_cost(bases: Dict, comp_code: str, qty: float, variable_meters: float = 0) -> Dict:
    comps = bases.get("composicoes", {})
    comp = comps.get(comp_code, {})
    itens = comp.get("itens", [])
    total_cost = 0.0
    items_detail = []
    for item in itens:
        tipo = item.get("tipo")
        codigo = item.get("codigo")
        qtd_base = item.get("qtd_base", 0)
        qtd_var = item.get("qtd_var", 0)
        item_qty = qtd_base * qty + qtd_var * variable_meters
        unit_price = get_item_price(bases, tipo, codigo)
        item_cost = item_qty * unit_price
        total_cost += item_cost
        items_detail.append({"tipo": tipo, "codigo": codigo, "qtd": round(item_qty, 2), "unit_price": round(unit_price, 2), "cost": round(item_cost, 2)})
    return {"code": comp_code, "description": comp.get("descricao", ""), "qty": qty, "items": items_detail, "cost": round(total_cost, 2)}


def main(input_json: str, out_dir: str):
    with open(input_json) as f:
        data = json.load(f)
    bases = load_bases()
    compositions = data.get("compositions", [])
    composition_costs = []
    total_cost = 0.0
    for comp in compositions:
        result = calculate_composition_cost(bases, comp["code"], comp.get("qty", 1), comp.get("variable_meters", 0))
        composition_costs.append(result)
        total_cost += result["cost"]
    cfg = data.get("commercial", {})
    mult = (1 + cfg.get("tax_pct", 9.5)/100) * (1 + cfg.get("overhead_pct", 7.0)/100) * (1 + cfg.get("margin_pct", 12.0)/100)
    final_price = total_cost * mult
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    customer = data.get("customer", {})
    project = data.get("project", {})
    client_lines = ["# Proposta Comercial", "", f"Proposta: {data.get('proposal_id')}", f"Data: {date.today().isoformat()}", "", f"Cliente: {customer.get('name')}", f"CNPJ: {customer.get('cnpj')}", f"Contato: {customer.get('contact')}", f"Telefone: {customer.get('phone')}", f"Email: {customer.get('email')}", "", f"Projeto: {project.get('title')}", f"Local: {project.get('location')}", "", "## Escopo", project.get("objective", ""), "", "## Serviços Propostos"]
    for comp in composition_costs:
        price = comp["cost"] * mult
        client_lines.append(f"- **{comp['description']}** ({comp['qty']}x): R$ {money(price)}")
    client_lines += ["", f"**VALOR TOTAL: R$ {money(final_price)}**", "", "## Condições Comerciais", f"- Pagamento: {cfg.get('payment_terms')}", f"- Garantia: {cfg.get('warranty')}", f"- Validade: {cfg.get('validity_days')} dias", f"- Prazo execução: {project.get('deadline_days')} dias", "", "## Exclusões"]
    for ex in data.get("exclusions", []):
        client_lines.append(f"- {ex}")
    record_lines = ["# Registro de Orçamento (Setor de Orçamentos)", "", f"Proposta: {data.get('proposal_id')}", f"Data: {date.today().isoformat()}", "", "## Parâmetros", f"- Impostos: {cfg.get('tax_pct')}%", f"- Overhead: {cfg.get('overhead_pct')}%", f"- Margem: {cfg.get('margin_pct')}%", f"- BDI: MAT 60%, MO 123%, FER 60%, EQP 50%", f"- Multiplicador total: {mult:.4f}x", "", "## Composições (com BDI)", "| Código | Descrição | Qtd | Custo+BDI | Preço |", "|--------|-----------|-----|-----------|-------|"]
    for comp in composition_costs:
        price = comp["cost"] * mult
        record_lines.append(f"| {comp['code']} | {comp['description']} | {comp['qty']} | R$ {money(comp['cost'])} | R$ {money(price)} |")
    record_lines += ["", f"**Total Custo (c/ BDI): R$ {money(total_cost)}**", f"**Total Preço: R$ {money(final_price)}**"]
    (out / "01_cliente_proposta.md").write_text("\n".join(client_lines) + "\n")
    (out / "02_registro_orcamento.md").write_text("\n".join(record_lines) + "\n")
    summary = {"proposal_id": data.get("proposal_id"), "total_cost": round(total_cost, 2), "final_price": round(final_price, 2), "multiplier": round(mult, 4), "compositions_count": len(compositions)}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(f"Gerado em: {out}")
    print(f"- Custo total (c/ BDI): R$ {money(total_cost)}")
    print(f"- Preço final: R$ {money(final_price)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: generate_proposal_from_compositions.py <input.json> <out_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

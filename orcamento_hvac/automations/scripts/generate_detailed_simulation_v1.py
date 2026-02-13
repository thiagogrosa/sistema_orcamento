#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import date


def money(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main(input_json: str, out_dir: str):
    data = json.loads(Path(input_json).read_text(encoding="utf-8"))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    materials = data["materials"]
    services = data["services"]

    mat_rows = []
    mat_total = 0.0
    for m in materials:
        total = m["qty"] * m["unit_cost"]
        mat_total += total
        mat_rows.append((m, total))

    srv_rows = []
    srv_total = 0.0
    for s in services:
        total = s["qty"] * s["unit_price"]
        srv_total += total
        srv_rows.append((s, total))

    direct_cost = mat_total + srv_total
    tax = direct_cost * (data["commercial"]["tax_pct"] / 100.0)
    overhead = direct_cost * (data["commercial"]["overhead_pct"] / 100.0)
    subtotal = direct_cost + tax + overhead
    margin = subtotal * (data["commercial"]["margin_pct"] / 100.0)
    final_price = subtotal + margin

    client_lines = [
        f"# Proposta Comercial Detalhada",
        "",
        f"Proposta: {data['proposal_id']}",
        f"Data: {date.today().isoformat()}",
        f"Cliente: {data['customer']['name']} ({data['customer']['cnpj']})",
        f"Contato: {data['customer']['contact']} | {data['customer']['email']} | {data['customer']['phone']}",
        f"Projeto: {data['project']['title']} - {data['project']['location']}",
        "",
        "## Objetivo",
        data['project']['objective'],
        "",
        "## Lista de Materiais",
    ]
    for m, total in mat_rows:
        client_lines.append(f"- [{m['code']}] {m['description']} | {m['qty']} {m['unit']} x R$ {money(m['unit_cost'])} = R$ {money(total)}")

    client_lines += ["", "## Lista de Serviços"]
    for s, total in srv_rows:
        client_lines.append(f"- [{s['id']}] {s['description']} | {s['qty']} {s['unit']} x R$ {money(s['unit_price'])} = R$ {money(total)}")

    client_lines += [
        "",
        "## Resumo Financeiro",
        f"- Materiais: R$ {money(mat_total)}",
        f"- Serviços: R$ {money(srv_total)}",
        f"- Custo direto: R$ {money(direct_cost)}",
        f"- Impostos ({data['commercial']['tax_pct']}%): R$ {money(tax)}",
        f"- Overhead ({data['commercial']['overhead_pct']}%): R$ {money(overhead)}",
        f"- Margem ({data['commercial']['margin_pct']}%): R$ {money(margin)}",
        f"- PREÇO FINAL: R$ {money(final_price)}",
        "",
        "## Condições Comerciais",
        f"- Pagamento: {data['commercial']['payment_terms']}",
        f"- Garantia: {data['commercial']['warranty']}",
        f"- Validade proposta: {data['commercial']['validity_days']} dias",
        f"- Prazo estimado execução: {data['project']['deadline_days']} dias",
        "",
        "## Exclusões",
    ]
    for ex in data["exclusions"]:
        client_lines.append(f"- {ex}")

    exec_lines = [
        "# Pacote de Execução Detalhado",
        "",
        f"Proposta: {data['proposal_id']}",
        f"Projeto: {data['project']['title']}",
        "",
        "## BOM (Bill of Materials)",
    ]
    for m, total in mat_rows:
        exec_lines.append(f"- {m['code']} | {m['description']} | Qtd: {m['qty']} {m['unit']} | Custo total: R$ {money(total)}")

    exec_lines += ["", "## Plano de Serviços"]
    for s, total in srv_rows:
        exec_lines.append(f"- {s['id']} | {s['description']} | Esforço: {s['qty']} {s['unit']} | Custo total: R$ {money(total)}")

    exec_lines += [
        "",
        "## Marcos de Entrega",
        "- M1: Engenharia e mobilização",
        "- M2: Instalação e interligações",
        "- M3: Comissionamento e treinamento",
        "",
        "## Riscos e Mitigações",
        "- Risco: janela de parada curta | Mitigação: plano de intervenção noturna",
        "- Risco: atraso de fornecimento | Mitigação: compra antecipada dos itens críticos",
    ]

    pricing = {
        "proposal_id": data["proposal_id"],
        "materials_total": round(mat_total, 2),
        "services_total": round(srv_total, 2),
        "direct_cost": round(direct_cost, 2),
        "tax_value": round(tax, 2),
        "overhead_value": round(overhead, 2),
        "subtotal_before_margin": round(subtotal, 2),
        "margin_value": round(margin, 2),
        "final_price": round(final_price, 2)
    }

    (out / "client_proposal_detailed.md").write_text("\n".join(client_lines)+"\n", encoding="utf-8")
    (out / "execution_package_detailed.md").write_text("\n".join(exec_lines)+"\n", encoding="utf-8")
    (out / "pricing_output_detailed.json").write_text(json.dumps(pricing, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: generate_detailed_simulation_v1.py <input_json> <out_dir>")
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])

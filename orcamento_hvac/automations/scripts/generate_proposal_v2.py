#!/usr/bin/env python3
"""
Gerador de propostas comerciais v2
-----------------------------------------
3 DOCUMENTOS GERADOS:
1. PROPOSTA CLIENTE (prices finais, fechado)
2. REGISTRO ORÇAMENTO (custos, multiplicadores, breakdown)
3. PACOTE EXECUÇÃO (descrição + 2 listas: custo por servico + materiais)
"""
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
    cfg = data["commercial"]

    # --- CALCULAR CUSTOS E PREÇOS ---
    # 1. Custos diretos de materiais
    mat_cost_total = 0.0
    mat_items = []
    for m in materials:
        cost = m["qty"] * m["unit_cost"]
        mat_cost_total += cost
        mat_items.append({
            "code": m["code"],
            "description": m["description"],
            "unit": m["unit"],
            "qty": m["qty"],
            "unit_cost": m["unit_cost"],
            "total_cost": cost
        })

    # 2. Custos diretos de serviços (sem margem ainda)
    srv_cost_total = 0.0
    srv_items = []
    for s in services:
        cost = s["qty"] * s["unit_price"]
        srv_cost_total += cost
        srv_items.append({
            "id": s["id"],
            "description": s["description"],
            "unit": s["unit"],
            "qty": s["qty"],
            "unit_cost": s["unit_price"],  # custo base (sem markup)
            "total_cost": cost
        })

    # 3. Calcular markups e preços finais
    tax_pct = cfg["tax_pct"] / 100.0
    overhead_pct = cfg["overhead_pct"] / 100.0
    margin_pct = cfg["margin_pct"] / 100.0

    # Multiplicador total = (1 + taxa) * (1 + overhead) * (1 + margem)
    mult_total = (1 + tax_pct) * (1 + overhead_pct) * (1 + margin_pct)

    # Preços para o cliente (com margem já aplicada)
    mat_price_total = mat_cost_total * mult_total
    srv_price_total = srv_cost_total * mult_total
    final_price = mat_price_total + srv_price_total

    # Itens de serviço com preço para cliente
    srv_price_items = []
    for s in services:
        price = s["unit_price"] * mult_total
        srv_price_items.append({
            "id": s["id"],
            "description": s["description"],
            "qty": s["qty"],
            "unit": s["unit"],
            "unit_price": round(price, 2),
            "total_price": round(price * s["qty"], 2)
        })

    # ========== DOCUMENTO 1: PROPOSTA CLIENTE ==========
    client_lines = [
        "# Proposta Comercial",
        "",
        f"Proposta: {data['proposal_id']}",
        f"Data: {date.today().isoformat()}",
        "",
        f"Cliente: {data['customer']['name']}",
        f"CNPJ: {data['customer']['cnpj']}",
        f"Contato: {data['customer']['contact']}",
        f"Telefone: {data['customer']['phone']}",
        f"Email: {data['customer']['email']}",
        "",
        f"Projeto: {data['project']['title']}",
        f"Local: {data['project']['location']}",
        "",
        "## Escopo",
        data['project']['objective'],
        "",
        "## Serviços Propostos",
    ]

    for s in srv_price_items:
        client_lines.append(f"- **{s['description']}**: R$ {money(s['total_price'])}")

    client_lines += [
        "",
        f"**VALOR TOTAL: R$ {money(final_price)}**",
        "",
        "## Condições Comerciais",
        f"- Pagamento: {cfg['payment_terms']}",
        f"- Garantia: {cfg['warranty']}",
        f"- Validade: {cfg['validity_days']} dias",
        f"- Prazo execução: {data['project']['deadline_days']} dias",
        "",
        "## Exclusões",
    ]
    for ex in data["exclusions"]:
        client_lines.append(f"- {ex}")

    # ========== DOCUMENTO 2: REGISTRO ORÇAMENTO ==========
    record_lines = [
        "# Registro de Orçamento (Setor de Orçamentos)",
        "",
        f"Proposta: {data['proposal_id']}",
        f"Data: {date.today().isoformat()}",
        "",
        "## Parâmetros Utilizados",
        f"- Alíquota de Impostos: {cfg['tax_pct']}%",
        f"- Overhead: {cfg['overhead_pct']}%",
        f"- Margem: {cfg['margin_pct']}%",
        f"- Multiplicador Total: {mult_total:.4f}x",
        "",
        "## Custos x Preços - Serviços",
        "| Serviço | Qtd | Und | Custo Unit. | Custo Total | Preço Unit. | Preço Total |",
        "|---------|-----|-----|-------------|-------------|--------------|-------------|",
    ]
    for s in srv_items:
        p = srv_price_items.pop(0)
        record_lines.append(
            f"| {s['description']} | {s['qty']} | {s['unit']} | R$ {money(s['unit_cost'])} | R$ {money(s['total_cost'])} | R$ {money(p['unit_price'])} | R$ {money(p['total_price'])} |"
        )

    record_lines += [
        "",
        f"**Total Custo Serviços: R$ {money(srv_cost_total)}**",
        f"**Total Preço Serviços: R$ {money(srv_price_total)}**",
        "",
        "## Custos x Preços - Materiais",
        "| Código | Descrição | Qtd | Und | Custo Unit. | Custo Total | Preço Unit. |",
        "|--------|------------|-----|-----|-------------|-------------|--------------|",
    ]
    for m in mat_items:
        price = m["unit_cost"] * mult_total
        record_lines.append(
            f"| {m['code']} | {m['description']} | {m['qty']} | {m['unit']} | R$ {money(m['unit_cost'])} | R$ {money(m['total_cost'])} | R$ {money(price)} |"
        )

    record_lines += [
        "",
        f"**Total Custo Materiais: R$ {money(mat_cost_total)}**",
        f"**Total Preço Materiais: R$ {money(mat_price_total)}**",
        "",
        "## Resumo Consolidado",
        f"| Item | Custo | Preço |",
        f"|------|-------|-------|",
        f"| Serviços | R$ {money(srv_cost_total)} | R$ {money(srv_price_total)} |",
        f"| Materiais | R$ {money(mat_cost_total)} | R$ {money(mat_price_total)} |",
        f"| **TOTAL** | **R$ {money(srv_cost_total + mat_cost_total)}** | **R$ {money(final_price)}** |",
    ]

    # ========== DOCUMENTO 3: PACOTE EXECUÇÃO ==========
    exec_lines = [
        "# Pacote de Execução",
        "",
        f"Proposta: {data['proposal_id']}",
        f"Projeto: {data['project']['title']}",
        "",
        "## Descrição do Projeto",
        data['project']['objective'],
        "",
        "## Requisitos e Observações",
        "- Janela de intervenção: conforme disponibilidade do cliente",
        "- Necessário acesso às áreas antes da execução",
        "- Equipamentos devem estar disponíveis no local",
        "",
        "## Lista A: Custo por Serviço/Composição",
        "| # | Serviço | Qtd | Und | Custo Unit. | Custo Total |",
        "|---|---------|-----|-----|-------------|-------------|",
    ]
    for i, s in enumerate(srv_items, 1):
        exec_lines.append(
            f"| {i} | {s['description']} | {s['qty']} | {s['unit']} | R$ {money(s['unit_cost'])} | R$ {money(s['total_cost'])} |"
        )

    exec_lines += [
        "",
        f"**Total Mão de Obra/Serviços: R$ {money(srv_cost_total)}**",
        "",
        "## Lista B: Materiais e Insumos (para Suprimentos)",
        "| Código | Descrição | Qtd | Und | Custo Unit. | Custo Total |",
        "|--------|------------|-----|-----|-------------|-------------|",
    ]
    for m in mat_items:
        exec_lines.append(
            f"| {m['code']} | {m['description']} | {m['qty']} | {m['unit']} | R$ {money(m['unit_cost'])} | R$ {money(m['total_cost'])} |"
        )

    exec_lines += [
        "",
        f"**Total Materiais: R$ {money(mat_cost_total)}**",
        "",
        "## Total Geral (Custo Execução)",
        f"**R$ {money(srv_cost_total + mat_cost_total)}**",
    ]

    # --- ESCREVER ARQUIVOS ---
    (out / "01_cliente_proposta.md").write_text("\n".join(client_lines)+"\n", encoding="utf-8")
    (out / "02_registro_orcamento.md").write_text("\n".join(record_lines)+"\n", encoding="utf-8")
    (out / "03_pacote_execucao.md").write_text("\n".join(exec_lines)+"\n", encoding="utf-8")

    # JSON de referência rápida
    summary = {
        "proposal_id": data["proposal_id"],
        "final_price": round(final_price, 2),
        "total_cost": round(srv_cost_total + mat_cost_total, 2),
        "multiplier": round(mult_total, 4),
        "documents": [
            "01_cliente_proposta.md",
            "02_registro_orcamento.md",
            "03_pacote_execucao.md"
        ]
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    print(f"Gerado em: {out}")
    print(f"- 01_cliente_proposta.md (R$ {money(final_price)})")
    print(f"- 02_registro_orcamento.md (custos + markup)")
    print(f"- 03_pacote_execucao.md (Listas A + B)")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: generate_proposal_v2.py <input_json> <out_dir>")
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])

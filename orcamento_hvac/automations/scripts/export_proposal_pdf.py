#!/usr/bin/env python3
"""
Export proposal to PDF.
PDF should contain ONLY the client-facing proposal (services with final prices),
NOT the detailed materials list (that goes to execution team).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
GEMINI_ROOT = ROOT.parent / "gerador_propostas"


def _build_precificado_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build payload for PDF generator.
    
    IMPORTANT: PDF goes to CLIENT, so it should only contain:
    - Services (with final price - already includes markup)
    - Total value
    
    NOT included (internal only):
    - Detailed materials list (goes to execution team)
    - Cost breakdown (goes to budgeting team)
    """
    # Extract customer data
    customer = payload.get("customer", {})
    customer_name = customer.get("name", "Cliente")
    
    # Extract project data
    project = payload.get("project", {})
    project_title = project.get("title", "Projeto HVAC")
    
    # Extract commercial terms
    commercial = payload.get("commercial", {})
    payment_terms = commercial.get("payment_terms", "A combinar")
    warranty = commercial.get("warranty", "Conforme contrato")
    deadline_days = project.get("deadline_days", 0)
    
    # Extract services ONLY (materials are internal)
    services = payload.get("services", [])
    
    # Calculate final price
    services_total = sum(s.get("qty", 0) * s.get("unit_price", 0) for s in services)
    
    # Apply markup
    tax_pct = commercial.get("tax_pct", 9.5) / 100.0
    overhead_pct = commercial.get("overhead_pct", 7.0) / 100.0
    margin_pct = commercial.get("margin_pct", 12.0) / 100.0
    mult_total = (1 + tax_pct) * (1 + overhead_pct) * (1 + margin_pct)
    
    final_price = services_total * mult_total
    
    # Build items list from services ONLY (client sees services, not materials)
    itens_precificados = []
    agrupamento = []
    current_id = 1
    
    # Add services with final price (already includes markup)
    if services:
        for svc in services:
            price = svc.get("unit_price", 0) * mult_total
            itens_precificados.append({
                "id": current_id,
                "descricao": svc.get("description", svc.get("id", "Serviço")),
                "composicao": svc.get("id", "CUSTOM"),
                "quantidade": svc.get("qty", 1),
                "unidade": svc.get("unit", "un"),
                "tipo_servico": "servico",
                "preco_unitario": round(price, 2),
                "preco_total": round(price * svc.get("qty", 1), 2)
            })
            current_id += 1
        
        agrupamento.append({
            "nome": "SERVIÇOS",
            "itens_ids": list(range(1, len(services) + 1))
        })

    # Build payload for PDF generator
    return {
        "projeto": project_title,
        "cliente": customer_name,
        "tipo_cliente": "PRIVADO-PJ",
        "dados_cliente": {
            "razao_social": customer_name,
            "cnpj": customer.get("cnpj", ""),
            "endereco": project.get("location", ""),
            "contato_nome": customer.get("contact", ""),
            "contato_email": customer.get("email", ""),
            "contato_telefone": customer.get("phone", ""),
        },
        "referencia": project_title,
        "itens_precificados": itens_precificados,
        "agrupamento": agrupamento,
        "resumo_financeiro": {
            "valor_total": round(final_price, 2)
        },
        "opcoes_output": {
            "gerar_rascunho": False,
            "condicoes_customizadas": {
                "forma_pagamento": payment_terms,
                "prazo_execucao": f"{deadline_days} dias" if deadline_days else "A combinar",
                "garantia": warranty,
            }
        }
    }


def export_pdf(payload: Dict[str, Any], output_pdf_path: str | None = None) -> Dict[str, Any]:
    sys.path.insert(0, str(GEMINI_ROOT))
    from hvac.generators import gerar_proposta_pdf  # type: ignore

    precificado = _build_precificado_from_payload(payload)
    out = output_pdf_path or str(
        ROOT / "runtime" / "demo_outputs" / "pdf" / f"{payload.get('proposal_id', 'PROPOSTA')}.pdf"
    )

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    return gerar_proposta_pdf(precificado, output_path=out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: export_proposal_pdf.py <payload.json> [output.pdf]")
        raise SystemExit(1)

    payload_path = Path(sys.argv[1])
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = export_pdf(payload, output_pdf)
    print(json.dumps(result, ensure_ascii=False, indent=2))

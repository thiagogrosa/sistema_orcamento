#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
GEMINI_ROOT = ROOT.parent / "gemini_hvac_layout"


def _build_precificado_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    final_price = float(payload.get("final_price", 0) or 0)
    customer = payload.get("customer_name", "Cliente")
    project_title = payload.get("project_title", "Projeto HVAC")
    scope = payload.get("scope_summary", "Escopo não informado")

    # Estrutura mínima compatível com gerador de PDF do gemini_hvac_layout
    return {
        "projeto": project_title,
        "cliente": customer,
        "tipo_cliente": "PRIVADO-PJ",
        "dados_cliente": {
            "razao_social": customer,
            "cnpj": payload.get("cnpj", ""),
            "endereco": payload.get("address", ""),
            "contato_nome": payload.get("contact_name", ""),
            "contato_email": payload.get("contact_email", ""),
            "contato_telefone": payload.get("contact_phone", ""),
        },
        "referencia": project_title,
        "itens_precificados": [
            {
                "id": 1,
                "descricao": scope,
                "composicao": "CUSTOM-ITEM",
                "quantidade": 1,
                "unidade": "pc",
                "tipo_servico": "instalacao-completa",
                "preco_total": final_price,
            }
        ],
        "agrupamento": [
            {
                "nome": "SERVICOS",
                "itens_ids": [1]
            }
        ],
        "resumo_financeiro": {
            "valor_total": final_price
        },
        "opcoes_output": {
            "gerar_rascunho": False,
            "condicoes_customizadas": {
                "forma_pagamento": payload.get("payment_terms", "A combinar"),
                "prazo_execucao": payload.get("execution_deadline", "A combinar"),
                "garantia": payload.get("warranty", "Conforme contrato"),
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
        print("usage: export_proposal_pdf_via_gemini_hvac_layout.py <payload.json> [output.pdf]")
        raise SystemExit(1)

    payload_path = Path(sys.argv[1])
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = export_pdf(payload, output_pdf)
    print(json.dumps(result, ensure_ascii=False, indent=2))

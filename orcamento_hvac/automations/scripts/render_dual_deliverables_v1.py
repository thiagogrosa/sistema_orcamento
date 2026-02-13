#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "standards" / "templates"


def _render_template(raw: str, payload: Dict[str, str]) -> str:
    out = raw
    for k, v in payload.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def render_client_proposal(payload: Dict[str, str]) -> str:
    template = (TEMPLATES_DIR / "client_proposal_template.md").read_text(encoding="utf-8")
    return _render_template(template, payload)


def render_execution_package(payload: Dict[str, str]) -> str:
    template = (TEMPLATES_DIR / "execution_package_template.md").read_text(encoding="utf-8")
    return _render_template(template, payload)


def render_both(payload: Dict[str, str]) -> Dict[str, str]:
    return {
        "client_proposal": render_client_proposal(payload),
        "execution_package": render_execution_package(payload),
    }


if __name__ == "__main__":
    sample = {
        "proposal_id": "PROP-2026-0001",
        "customer_name": "ACME",
        "project_title": "HVAC Retrofit",
        "date": "2026-02-13",
        "scope_summary": "Install and commission split systems.",
        "subtotal": "10000.00",
        "taxes": "1200.00",
        "final_price": "11200.00",
        "notes": "Validity: 15 days.",
        "owner": "Operations",
        "delivery_checklist": "- BOM\n- Schedule\n- Safety",
        "direct_cost": "8000.00",
        "overhead": "10%",
        "margin": "15%",
        "internal_notes": "Prioritize week 1 delivery.",
    }
    out = render_both(sample)
    print(out["client_proposal"])
    print("---")
    print(out["execution_package"])

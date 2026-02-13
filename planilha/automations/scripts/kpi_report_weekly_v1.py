#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class KpiInput:
    proposals_total: int
    proposals_won: int
    proposals_lost: int
    avg_cycle_days: float
    avg_margin_pct: float
    loss_reasons: Dict[str, int]


@dataclass
class KpiOutput:
    conversion_rate_pct: float
    loss_rate_pct: float
    avg_cycle_days: float
    avg_margin_pct: float
    top_loss_reason: str
    totals: Dict[str, int]


def _pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100.0, 2)


def build_weekly_kpi(inp: KpiInput) -> KpiOutput:
    top_reason = "none"
    if inp.loss_reasons:
        top_reason = max(inp.loss_reasons.items(), key=lambda kv: kv[1])[0]

    return KpiOutput(
        conversion_rate_pct=_pct(inp.proposals_won, inp.proposals_total),
        loss_rate_pct=_pct(inp.proposals_lost, inp.proposals_total),
        avg_cycle_days=round(inp.avg_cycle_days, 2),
        avg_margin_pct=round(inp.avg_margin_pct, 2),
        top_loss_reason=top_reason,
        totals={
            "proposals_total": inp.proposals_total,
            "proposals_won": inp.proposals_won,
            "proposals_lost": inp.proposals_lost,
        },
    )


def to_markdown(out: KpiOutput) -> str:
    return (
        "# Weekly KPI Report (v1)\n\n"
        f"- Conversion rate: {out.conversion_rate_pct}%\n"
        f"- Loss rate: {out.loss_rate_pct}%\n"
        f"- Average cycle: {out.avg_cycle_days} days\n"
        f"- Average margin: {out.avg_margin_pct}%\n"
        f"- Top loss reason: {out.top_loss_reason}\n\n"
        "## Totals\n"
        f"- Total proposals: {out.totals['proposals_total']}\n"
        f"- Won: {out.totals['proposals_won']}\n"
        f"- Lost: {out.totals['proposals_lost']}\n"
    )


def to_dict(out: KpiOutput):
    return asdict(out)

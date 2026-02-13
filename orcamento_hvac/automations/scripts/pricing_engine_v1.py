#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class PricingInput:
    direct_cost: float
    tax_pct: float
    overhead_pct: float
    fixed_cost: float
    margin_pct: float
    policy_version: str = "v1"


@dataclass
class PricingOutput:
    base_cost: float
    tax_value: float
    overhead_value: float
    subtotal_before_margin: float
    margin_value: float
    final_price: float
    policy_version: str


def _pct(value: float, pct: float) -> float:
    return value * (pct / 100.0)


def calculate_price(inp: PricingInput) -> PricingOutput:
    base_cost = inp.direct_cost + inp.fixed_cost
    tax_value = _pct(base_cost, inp.tax_pct)
    overhead_value = _pct(base_cost, inp.overhead_pct)
    subtotal = base_cost + tax_value + overhead_value
    margin_value = _pct(subtotal, inp.margin_pct)
    final_price = subtotal + margin_value

    return PricingOutput(
        base_cost=round(base_cost, 2),
        tax_value=round(tax_value, 2),
        overhead_value=round(overhead_value, 2),
        subtotal_before_margin=round(subtotal, 2),
        margin_value=round(margin_value, 2),
        final_price=round(final_price, 2),
        policy_version=inp.policy_version,
    )


def to_dict(out: PricingOutput):
    return asdict(out)


if __name__ == "__main__":
    sample = PricingInput(
        direct_cost=10000,
        tax_pct=12,
        overhead_pct=8,
        fixed_cost=500,
        margin_pct=15,
    )
    print(to_dict(calculate_price(sample)))

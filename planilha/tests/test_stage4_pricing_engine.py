from automations.scripts.pricing_engine_v1 import PricingInput, calculate_price


def test_pricing_engine_deterministic_case_1():
    inp = PricingInput(
        direct_cost=10000.0,
        tax_pct=12.0,
        overhead_pct=8.0,
        fixed_cost=500.0,
        margin_pct=15.0,
        policy_version="v1",
    )
    out = calculate_price(inp)

    assert out.base_cost == 10500.0
    assert out.tax_value == 1260.0
    assert out.overhead_value == 840.0
    assert out.subtotal_before_margin == 12600.0
    assert out.margin_value == 1890.0
    assert out.final_price == 14490.0
    assert out.policy_version == "v1"


def test_pricing_engine_deterministic_case_2():
    inp = PricingInput(
        direct_cost=70000.0,
        tax_pct=10.0,
        overhead_pct=7.0,
        fixed_cost=2500.0,
        margin_pct=12.0,
        policy_version="v1.1",
    )
    out = calculate_price(inp)

    assert out.base_cost == 72500.0
    assert out.tax_value == 7250.0
    assert out.overhead_value == 5075.0
    assert out.subtotal_before_margin == 84825.0
    assert out.margin_value == 10179.0
    assert out.final_price == 95004.0
    assert out.policy_version == "v1.1"

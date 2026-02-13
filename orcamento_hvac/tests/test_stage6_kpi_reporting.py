import json
from pathlib import Path

from automations.scripts.kpi_report_weekly_v1 import KpiInput, build_weekly_kpi, to_markdown

ROOT = Path(__file__).resolve().parents[1]


def test_stage6_kpi_script_exists():
    assert (ROOT / "automations/scripts/kpi_report_weekly_v1.py").exists()


def test_stage6_kpi_metrics_and_snapshot():
    raw = json.loads((ROOT / "tests/fixtures/stage6_kpi_input.json").read_text(encoding="utf-8"))
    inp = KpiInput(**raw)
    out = build_weekly_kpi(inp)

    assert out.conversion_rate_pct == 40.0
    assert out.loss_rate_pct == 35.0
    assert out.avg_cycle_days == 12.45
    assert out.avg_margin_pct == 14.3
    assert out.top_loss_reason == "budget_rejected"

    rendered = to_markdown(out)
    expected = (ROOT / "tests/snapshots/stage6_kpi_report_snapshot.md").read_text(encoding="utf-8")
    assert rendered == expected

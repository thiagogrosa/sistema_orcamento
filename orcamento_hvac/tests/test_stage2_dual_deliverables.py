import json
from pathlib import Path

from automations.scripts.render_dual_deliverables_v1 import render_both

ROOT = Path(__file__).resolve().parents[1]


def test_stage2_templates_exist():
    assert (ROOT / "standards/templates/client_proposal_template.md").exists()
    assert (ROOT / "standards/templates/execution_package_template.md").exists()


def test_stage2_render_matches_snapshots():
    payload = json.loads((ROOT / "tests/fixtures/sample_payload_stage2.json").read_text(encoding="utf-8"))
    out = render_both(payload)

    expected_client = (ROOT / "tests/snapshots/client_proposal_stage2_snapshot.md").read_text(encoding="utf-8")
    expected_exec = (ROOT / "tests/snapshots/execution_package_stage2_snapshot.md").read_text(encoding="utf-8")

    assert out["client_proposal"] == expected_client
    assert out["execution_package"] == expected_exec

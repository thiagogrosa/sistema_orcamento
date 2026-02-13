import json
from pathlib import Path

from automations.scripts.asana_adapter_v1 import AsanaAdapterV1, FakeAsanaBackend
from automations.scripts.proposal_lifecycle_v1 import ProposalLifecycleV1

ROOT = Path(__file__).resolve().parents[1]


def test_stage3_workflow_files_exist():
    assert (ROOT / "standards/workflow/proposal_status_map_v1.json").exists()
    assert (ROOT / "standards/workflow/proposal_reason_taxonomy_v1.json").exists()


def test_valid_transition_logs_event_and_syncs_asana_mock():
    backend = FakeAsanaBackend()
    adapter = AsanaAdapterV1(backend=backend)
    lifecycle = ProposalLifecycleV1(adapter=adapter)

    event = lifecycle.transition(
        proposal_id="PROP-2026-0042",
        from_status="draft",
        to_status="review",
        reason_code="technical_review_needed",
    )

    assert event.to_status == "review"
    assert len(lifecycle.events) == 1
    assert len(backend.events) == 1
    assert backend.events[0].proposal_id == "PROP-2026-0042"


def test_invalid_transition_raises_error():
    lifecycle = ProposalLifecycleV1()
    try:
        lifecycle.transition(
            proposal_id="PROP-2026-0042",
            from_status="draft",
            to_status="won",
            reason_code="closed_success",
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "invalid transition" in str(exc)


def test_reason_taxonomy_has_expected_category():
    taxonomy = json.loads((ROOT / "standards/workflow/proposal_reason_taxonomy_v1.json").read_text(encoding="utf-8"))
    assert "technical" in taxonomy["categories"]
    assert "technical_review_needed" in taxonomy["categories"]["technical"]

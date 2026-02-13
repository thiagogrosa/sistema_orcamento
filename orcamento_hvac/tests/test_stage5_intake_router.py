import json
from pathlib import Path

from automations.scripts.intake_router_v1 import IntakeRouterV1

ROOT = Path(__file__).resolve().parents[1]


def _load_dataset():
    p = ROOT / "tests/fixtures/stage5_intake_dataset.json"
    return json.loads(p.read_text(encoding="utf-8"))


def test_stage5_router_file_exists():
    assert (ROOT / "automations/scripts/intake_router_v1.py").exists()


def test_stage5_ingest_and_retrieve_by_proposal():
    router = IntakeRouterV1()
    ds = _load_dataset()

    for row in ds:
        if row["source_type"] == "asana":
            router.ingest_asana(row["proposal_id"], row["customer"], row["payload_ref"])
        elif row["source_type"] == "drive":
            router.ingest_drive(row["proposal_id"], row["customer"], row["payload_ref"])
        elif row["source_type"] == "email":
            router.ingest_email(row["proposal_id"], row["customer"], row["payload_ref"])

    res = router.retrieve(proposal_id="PROP-2026-0042")
    assert len(res) == 2
    assert {r["source_type"] for r in res} == {"asana", "drive"}


def test_stage5_retrieve_by_customer_and_source():
    router = IntakeRouterV1()
    router.ingest_asana("PROP-2026-0042", "Cliente Exemplo Ltda", "120900001")
    router.ingest_drive("PROP-2026-0042", "Cliente Exemplo Ltda", "1ABCDriveFile")
    router.ingest_email("PROP-2026-0099", "Outro Cliente SA", "msg-991")

    customer_res = router.retrieve(customer="Outro Cliente SA")
    assert len(customer_res) == 1
    assert customer_res[0]["source_type"] == "email"

    drive_res = router.retrieve(source_type="drive")
    assert len(drive_res) == 1
    assert drive_res[0]["payload_ref"] == "1ABCDriveFile"

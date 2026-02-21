from pathlib import Path

from automations.scripts.proposal_id_v1 import build_proposal_id, validate_proposal_id


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "standards" / "db" / "migration_stage1_core_proposal_domain_v1.sql"
STATUS_MAP = ROOT / "standards" / "workflow" / "proposal_status_map_v1.json"


def test_build_proposal_id_format():
    assert build_proposal_id(7, 2026) == "PROP-2026-0007"


def test_validate_proposal_id():
    assert validate_proposal_id("PROP-2026-0001")
    assert not validate_proposal_id("PROP-26-0001")
    assert not validate_proposal_id("PROP-2026-0000")
    assert not validate_proposal_id("ABC-2026-0001")


def test_stage1_artifacts_exist():
    assert MIGRATION.exists()
    assert STATUS_MAP.exists()


def test_migration_contains_required_tables():
    sql = MIGRATION.read_text(encoding="utf-8")
    required = [
        "CREATE TABLE IF NOT EXISTS proposals",
        "CREATE TABLE IF NOT EXISTS proposal_items",
        "CREATE TABLE IF NOT EXISTS proposal_status_history",
        "CREATE TABLE IF NOT EXISTS proposal_pricing",
        "CREATE TABLE IF NOT EXISTS proposal_files",
    ]
    for item in required:
        assert item in sql

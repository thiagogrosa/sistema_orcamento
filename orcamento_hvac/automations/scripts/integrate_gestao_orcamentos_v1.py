#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
GESTAO_ROOT = ROOT.parent / "gestao-orcamentos"
sys.path.insert(0, str(GESTAO_ROOT / "src"))

from prepare_data import DataPreparer  # type: ignore
from asana_lib import AsanaLib  # type: ignore
from sync_drive import DriveSync  # type: ignore


def run_integration(
    email_input_path: str,
    output_prepared_md: str,
    proposta_payload: Dict[str, Any],
    pasta_id_drive: str = "26_999",
) -> Dict[str, Any]:
    # 1) Coleta/preparo de informações (gestao-orcamentos)
    preparer = DataPreparer()
    prep_result = preparer.preparar_email(email_input_path, output_prepared_md)

    # 2) Gestão de proposta no Asana (modo simulado da AsanaLib)
    asana = AsanaLib()
    task_id = asana.criar_orcamento(proposta_payload)

    # 3) Mapeamento Drive <-> Asana e sync por demanda
    mapping_file = str(ROOT / "runtime" / "integration" / "ids_mapping_v1.json")
    drive_base = str(ROOT / "runtime" / "integration" / "drive_mock")
    sync = DriveSync(drive_base=drive_base, mapping_file=mapping_file)
    sync.registrar_mapeamento(pasta_id_drive, task_id)
    sync_stats = sync.sincronizar_demanda(pasta_id_drive)

    return {
        "prepared_data": {
            "output_file": prep_result.get("output_file"),
            "reducao_percentual": prep_result.get("reducao_percentual"),
            "metadados": prep_result.get("metadados", {}),
        },
        "asana": {
            "task_id": task_id,
            "project_id": asana.project_id,
            "url": f"https://app.asana.com/0/{asana.project_id}/{task_id}",
        },
        "drive_sync": sync_stats,
    }


def main() -> None:
    if len(sys.argv) < 4:
        print(
            "usage: integrate_gestao_orcamentos_v1.py "
            "<email_input.txt|html> <output_prepared.md> <proposta_payload.json> [pasta_id]"
        )
        raise SystemExit(1)

    email_input = sys.argv[1]
    output_prepared = sys.argv[2]
    proposta_json = sys.argv[3]
    pasta_id = sys.argv[4] if len(sys.argv) > 4 else "26_999"

    payload = json.loads(Path(proposta_json).read_text(encoding="utf-8"))
    result = run_integration(email_input, output_prepared, payload, pasta_id_drive=pasta_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class IntakeRecord:
    proposal_id: str
    customer: str
    source_type: str
    payload_type: str
    payload_ref: str


class IntakeRouterV1:
    def __init__(self) -> None:
        self._records: List[IntakeRecord] = []

    def ingest_asana(self, proposal_id: str, customer: str, task_gid: str) -> IntakeRecord:
        rec = IntakeRecord(proposal_id, customer, "asana", "task", task_gid)
        self._records.append(rec)
        return rec

    def ingest_drive(self, proposal_id: str, customer: str, file_id: str) -> IntakeRecord:
        rec = IntakeRecord(proposal_id, customer, "drive", "file", file_id)
        self._records.append(rec)
        return rec

    def ingest_email(self, proposal_id: str, customer: str, message_id: str) -> IntakeRecord:
        rec = IntakeRecord(proposal_id, customer, "email", "message", message_id)
        self._records.append(rec)
        return rec

    def all_records(self) -> List[IntakeRecord]:
        return list(self._records)

    def retrieve(self, *, proposal_id: str | None = None, customer: str | None = None, source_type: str | None = None) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for r in self._records:
            if proposal_id is not None and r.proposal_id != proposal_id:
                continue
            if customer is not None and r.customer != customer:
                continue
            if source_type is not None and r.source_type != source_type:
                continue
            out.append(
                {
                    "proposal_id": r.proposal_id,
                    "customer": r.customer,
                    "source_type": r.source_type,
                    "payload_type": r.payload_type,
                    "payload_ref": r.payload_ref,
                }
            )
        return out

#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from automations.scripts.asana_adapter_v1 import AsanaAdapterV1

ROOT = Path(__file__).resolve().parents[2]
STATUS_MAP_PATH = ROOT / "standards/workflow/proposal_status_map_v1.json"


@dataclass
class LifecycleEvent:
    proposal_id: str
    from_status: str | None
    to_status: str
    reason_code: str | None


class ProposalLifecycleV1:
    def __init__(self, adapter: AsanaAdapterV1 | None = None) -> None:
        raw = json.loads(STATUS_MAP_PATH.read_text(encoding="utf-8"))
        self.allowed_transitions: Dict[str, List[str]] = raw["allowed_transitions"]
        self.adapter = adapter or AsanaAdapterV1()
        self.events: List[LifecycleEvent] = []

    def can_transition(self, from_status: str, to_status: str) -> bool:
        return to_status in self.allowed_transitions.get(from_status, [])

    def transition(
        self,
        proposal_id: str,
        from_status: str | None,
        to_status: str,
        reason_code: str | None = None,
    ) -> LifecycleEvent:
        if from_status is not None and not self.can_transition(from_status, to_status):
            raise ValueError(f"invalid transition: {from_status} -> {to_status}")

        event = LifecycleEvent(
            proposal_id=proposal_id,
            from_status=from_status,
            to_status=to_status,
            reason_code=reason_code,
        )
        self.events.append(event)
        self.adapter.sync_transition(proposal_id, from_status, to_status, reason_code)
        return event

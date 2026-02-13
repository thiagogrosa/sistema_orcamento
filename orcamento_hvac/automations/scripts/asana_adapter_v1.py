#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AsanaEvent:
    proposal_id: str
    from_status: str | None
    to_status: str
    reason_code: str | None


class FakeAsanaBackend:
    def __init__(self) -> None:
        self.events: List[AsanaEvent] = []

    def record_status_transition(self, event: AsanaEvent) -> Dict[str, str]:
        self.events.append(event)
        return {
            "ok": "true",
            "proposal_id": event.proposal_id,
            "to_status": event.to_status,
        }


class AsanaAdapterV1:
    def __init__(self, backend: FakeAsanaBackend | None = None) -> None:
        self.backend = backend or FakeAsanaBackend()

    def sync_transition(
        self,
        proposal_id: str,
        from_status: str | None,
        to_status: str,
        reason_code: str | None,
    ) -> Dict[str, str]:
        event = AsanaEvent(
            proposal_id=proposal_id,
            from_status=from_status,
            to_status=to_status,
            reason_code=reason_code,
        )
        return self.backend.record_status_transition(event)

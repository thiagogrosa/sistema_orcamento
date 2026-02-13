#!/usr/bin/env python3
"""Proposal ID generator/validator.

Format: PROP-YYYY-NNNN
- YYYY: year (4 digits)
- NNNN: sequence (4 digits, zero-padded)
"""

from __future__ import annotations

import re
from datetime import datetime

PATTERN = re.compile(r"^PROP-(\d{4})-(\d{4})$")


def build_proposal_id(sequence: int, year: int | None = None) -> str:
    if sequence < 1 or sequence > 9999:
        raise ValueError("sequence must be between 1 and 9999")
    y = year if year is not None else datetime.now().year
    if y < 2000 or y > 9999:
        raise ValueError("year must be a 4-digit number >= 2000")
    return f"PROP-{y:04d}-{sequence:04d}"


def validate_proposal_id(value: str) -> bool:
    m = PATTERN.match(value)
    if not m:
        return False
    year = int(m.group(1))
    seq = int(m.group(2))
    if year < 2000:
        return False
    if seq < 1:
        return False
    return True


if __name__ == "__main__":
    sample = build_proposal_id(1)
    print(sample)
    print(validate_proposal_id(sample))

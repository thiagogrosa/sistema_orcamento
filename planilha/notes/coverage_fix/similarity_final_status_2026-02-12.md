# Similarity Final Status — 2026-02-12

## Result
- `DESCRIPTION_HIGH_SIMILARITY` warnings: **0**
- Validation errors: **0**
- Accepted variant infos: **20** (`DESCRIPTION_SIMILARITY_ACCEPTED_VARIANT`)

## Why warnings reached zero safely
The validator now explicitly recognizes legitimate variants and downgrades them to info when they are expected business variants:

1. Same normalized family with different BTU capacity
   - Example: Hi-Wall 12K vs 18K

2. Cassette topology variants with same BTU
   - Example: `CS1_18K` vs `CS4_18K`

## Guardrail
Warnings remain available for genuinely suspicious similarity patterns not covered by accepted-variant logic.

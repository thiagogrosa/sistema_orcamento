# Access Matrix — Required Integrations for Budgeting System (v1)

Scope: implementation with mocked tests now, real credentials later.

## 1) Asana
- Variables:
  - `ASANA_ACCESS_TOKEN`
  - `ASANA_WORKSPACE_ID`
  - `ASANA_PROJECT_ID_MAIN`
- Purpose:
  - proposal lifecycle tracking
  - owners/status/reasons visibility
  - stakeholder management view
- Needed for:
  - real task create/update/sync
  - state transition mirroring

## 2) Google OAuth (Drive/Calendar/Gmail lanes)
- Variables:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_REFRESH_TOKEN`
- Purpose:
  - read/write proposal files in Drive
  - pull context from calendar/email workflows (when enabled)
- Needed for:
  - real ingestion and document linking

## 3) Model providers
- Variables (at least one additional):
  - `MINIMAX_API_KEY` or `OPENAI_API_KEY`
  - `GEMINI_API_KEY` (already present)
- Purpose:
  - analysis, drafting, extraction, fallback routing
- Needed for:
  - real AI execution in production lanes

## 4) Storage/runtime
- Variables:
  - `APP_DATA_DIR`
  - `SQLITE_DB_PATH`
- Purpose:
  - persistent DB and runtime artifacts
- Needed for:
  - stable production execution and audits

## 5) Optional YouTube lane
- Variable:
  - `YOUTUBE_API_KEY`
- Purpose:
  - ingest YouTube metadata/transcripts via API routes
- Needed for:
  - video-source enrichment (optional)

---

## Mock strategy while access is missing
For each integration above, tests use:
1. Fake adapters (same interface as real connector)
2. Deterministic fixtures (`tests/fixtures/*.json`)
3. Contract tests that validate payload shape and expected responses
4. Snapshot tests for final generated outputs

This allows full development and verification before real credentials are provided.

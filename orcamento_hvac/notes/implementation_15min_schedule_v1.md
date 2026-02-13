# 15-Minute Sprint Schedule — System Implementation (v1)

Branch: `feature/system-implementation-15min-sprints`
Cadence: one implementation block every 15 minutes.
Goal: reach 100% verification pass in the requirements matrix + improved tests, using realistic mock/fake integrations where real access is missing.

## Execution model
- Work in 15-minute blocks.
- At end of each block: commit + short handoff note.
- Every 10 messages: context rotation with mandatory handoff.
- No blocking on external credentials: use mock providers and deterministic fixtures.

## Stage plan (15-minute blocks)

### Stage 1 — Core proposal domain
1. Add DB migration for proposal tables (`proposals`, `proposal_items`, `proposal_status_history`, `proposal_pricing`, `proposal_files`).
2. Add Proposal ID generator/validator (`PROP-YYYY-NNNN`).
3. Add tests for table existence and ID format.

### Stage 2 — Dual deliverables templates
4. Create `client_proposal_template.md` and `execution_package_template.md`.
5. Implement render script from same input payload.
6. Add snapshot tests for both outputs.

### Stage 3 — Lifecycle + Asana mapping (mocked)
7. Add status map + reason taxonomy file.
8. Create Asana adapter interface with fake backend.
9. Add tests for state transitions and event logging.

### Stage 4 — Pricing engine
10. Implement pricing engine v1 (direct cost + tax + overhead + fixed + margin).
11. Add deterministic test cases with expected output values.
12. Add policy-version tracking test.

### Stage 5 — Intake/retrieval (mocked connectors)
13. Implement intake router interfaces for Asana/Drive/Email.
14. Provide fake datasets and parser fixtures.
15. Add retrieval tests by proposal_id/customer/type.

### Stage 6 — KPI/reporting baseline
16. Implement weekly KPI script with fixtures.
17. Add tests for conversion/cycle/margin/loss-reason metrics.
18. Add report output snapshot test.

### Stage 7 — Verification hardening
19. Re-run requirements matrix; close failed checks.
20. Improve test coverage around edge cases.
21. Final run: all tests + full verification report.

## Completion criteria
- Requirements verification: 10/10 PASS.
- Automated tests passing.
- Mocked integration tests passing for all external access points.
- Clear artifacts under `notes/` + release notes + PR-ready summary.

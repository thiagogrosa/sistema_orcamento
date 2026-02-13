# Approval Gates v1

## Objective
Define mandatory human approvals before commercial commitment.

## Gates

1. Technical Readiness Gate
- Required status: `priced`
- Required artifacts: execution package generated, scope reviewed
- Decision owners: Engineering + Operations

2. Commercial Gate
- Required status: `approval_pending`
- Required artifacts: pricing breakdown, margin compliance, policy version recorded
- Decision owners: Budget Coordination

3. Final Send Gate
- Required status: `approved`
- Required artifacts: client proposal rendered, approval record, change log
- Decision owners: Budget Coordination + Sales

## Rejection handling
- Every rejection MUST include reason code from taxonomy and next action.

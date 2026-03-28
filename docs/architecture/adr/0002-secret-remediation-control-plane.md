# ADR-0002 - Secret Remediation Control Plane for Exposed Repository Keys

## Status

- Proposed

## Date

- 2026-03-28

## Owners

- @3design (primary)
- @4plan, @8ql, @9git (reviewers)

## Context

A private key artifact was committed to repository state/history. The project requires immediate containment,
credential rotation, durable secret-scanning guardrails, and a scheduled history rewrite with auditable validation.
A single-step rewrite is high risk for coordination failures; a phased but fail-closed architecture is required.

## Decision

Adopt a phased remediation control plane with four enforced phases:
1. Containment (remove active secret, rotate/revoke credentials, enforce local+CI guardrails).
2. Verification (deterministic scan reports and rotation gate checks).
3. Rewrite (scheduled freeze-window history rewrite across refs/tags).
4. Stabilization (post-rewrite contributor migration and regression guardrails).

Progression between phases is contract-gated by explicit interfaces:
- Secret scanning service
- Rotation checkpoint gate
- CI guardrail policy
- Rewrite coordinator

## Alternatives considered

### Alternative A - Path-only cleanup and forward guardrails

- Summary: Remove active secret and enforce future scanning without rewriting history.
- Why not chosen: Leaves historical exposure discoverable and weakens long-term security/compliance posture.

### Alternative B - Immediate full history rewrite (single-step)

- Summary: Perform rotation, cleanup, and rewrite in one immediate operation.
- Why not chosen: High coordination and disruption risk for active contributors; elevated execution-failure probability.

## Consequences

### Positive

- Immediate risk reduction with fail-closed controls.
- High-assurance end state after rewrite verification across refs/tags.
- Clear audit trail via checkpointed phase gates and deterministic scan reports.

### Negative / Trade-offs

- Operational overhead due to phased governance and checkpoint management.
- Temporary residual history risk until rewrite phase completes.
- Additional documentation/process burden on contributors and release maintainers.

## Implementation impact

- Affected components:
  - Secret scanning integration points (pre-commit and CI workflows)
  - Rotation evidence/checkpoint documentation flow
  - Rewrite runbook and validation procedures
  - Project lane/status governance artifacts
- Migration/rollout notes:
  - Day-0 containment and guardrails first
  - Scheduled rewrite freeze window second
  - Contributor migration communication required after rewrite
- Backward compatibility notes:
  - History rewrite is intentionally non-backward compatible for commit hashes
  - Contributor branches require reset/rebase/reclone guidance

## Validation and monitoring

- Tests or checks required:
  - Secret scan pass/fail checks for tree, refs, and history profiles
  - Rotation checkpoint completeness gate before rewrite
  - Merge-blocking CI status checks for secret scanning
- Runtime signals or metrics to monitor:
  - Finding counts by severity over time
  - Rotation checkpoint completion ratio
  - Rewrite post-verify zero-match status across refs/tags
- Rollback triggers:
  - Rewrite preflight failure
  - Post-rewrite verification mismatch
  - Missing rotation evidence for required dependent systems

## Related links

- Related project artifact(s):
  - docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.design.md
  - docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.think.md
- Related architecture docs:
  - docs/architecture/adr/0001-architecture-decision-record-template.md
- Supersedes/Superseded-by (if any):
  - None

# private-key-remediation - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-28_

## Selected Option
Option C - Phased containment first, then scheduled history rewrite.

Rationale:
1. Contains active incident risk immediately (rotation + active-tree cleanup + guardrails).
2. Preserves high-assurance outcome by requiring a bounded history rewrite window.
3. Reduces coordination failure risk versus a single big-bang rewrite.

## Branch Gate And Policy Validation
- Expected branch (from project plan): `prj0000090-private-key-remediation`
- Observed branch: `prj0000090-private-key-remediation`
- Branch gate result: PASS
- Naming standards check (`docs/project/naming_standards.md`): PASS (artifact names remain snake_case/kebab-case compatible and project ID naming unchanged)
- Code of conduct check (`docs/project/code_of_conduct.md`): PASS (documentation-only, no policy conflicts)

## Problem Statement And Goals
Private key material was committed to repository state/history. Compromise must be assumed.

Goals:
1. Stop further leakage immediately.
2. Rotate and verify all affected credentials with explicit checkpoints.
3. Purge secret material from repository history in a controlled window.
4. Enforce durable local and CI guardrails that fail closed.

## Architecture
### High-Level Control Plane
The remediation workflow is modeled as a control plane with bounded phases:

1. Containment Phase (Day 0)
- Remove secret artifact from active tree.
- Rotate/revoke implicated keys and dependent credentials.
- Enable local pre-commit secret scan and mandatory CI scan.

2. Verification Phase (Day 0 to Day 1)
- Run deterministic scans on working tree and current refs.
- Validate rotation checkpoints before rewrite window opens.

3. Rewrite Phase (Scheduled freeze window)
- Freeze merges.
- Rewrite git history to remove secret signatures from all refs/tags.
- Force-push rewritten refs and run full-history verification scan.

4. Post-Rewrite Stabilization (Day 2+)
- Publish contributor migration instructions.
- Require clean validation signals before lane advancement.

### Control-Plane Components
- Secret Scan Orchestrator: executes scan profiles (tree, refs, full-history).
- Rotation Checkpoint Registry: records and gates credential-rotation completeness.
- Rewrite Coordinator: enforces freeze window preconditions and post-rewrite validation.
- CI Guardrail Adapter: wires deterministic, merge-blocking secret scans.
- Governance Reporter: emits auditable status summary for project artifacts and lane transitions.

### Data Flow
1. Trigger remediation run.
2. Run tree/ref scan profile.
3. If detection exists, block progression and require containment actions.
4. Record rotation checkpoint evidence.
5. Open rewrite window only when checkpoint contract reaches COMPLETE.
6. Execute history rewrite and verify all refs/tags.
7. Publish handoff bundle for @4plan implementation scheduling.

## Interfaces & Contracts
### 1) Secret scanning contract
Interface: `SecretScanService`

Methods:
- `scan_tree(profile: TreeScanProfile) -> ScanReport`
- `scan_refs(profile: RefScanProfile) -> ScanReport`
- `scan_history(profile: HistoryScanProfile) -> ScanReport`

Contract rules:
- Returns deterministic findings keyed by signature ID and ref/path.
- Exit behavior is fail-closed when scanner execution fails.
- Must support baseline suppression file with explicit expiration dates.

### 2) Key-rotation checkpoint contract
Interface: `RotationCheckpointService`

Methods:
- `begin_incident(incident_id: str, key_fingerprint: str) -> RotationCheckpoint`
- `record_rotation_step(incident_id: str, system_id: str, evidence_uri: str) -> RotationCheckpoint`
- `evaluate_gate(incident_id: str) -> RotationGateDecision`

Contract rules:
- Gate status values: `BLOCKED`, `PARTIAL`, `COMPLETE`.
- Rewrite phase cannot start unless gate status is `COMPLETE`.
- Every dependent credential system must provide evidence URI for audit.

### 3) CI guardrail contract
Interface: `SecretGuardrailPolicy`

Methods:
- `validate_pr(secret_scan_report: ScanReport, branch: str) -> GuardrailDecision`
- `validate_push(secret_scan_report: ScanReport, branch: str) -> GuardrailDecision`

Contract rules:
- Any `HIGH` or `CRITICAL` secret finding blocks merge.
- Branch protection requires scan job success as mandatory status check.
- Local hook bypass is tolerated only if CI still fails closed.

### 4) Rewrite coordination contract
Interface: `HistoryRewriteCoordinator`

Methods:
- `preflight(incident_id: str) -> RewritePreflightReport`
- `execute(incident_id: str, scope: RewriteScope) -> RewriteResult`
- `post_verify(incident_id: str) -> RewriteVerificationReport`

Contract rules:
- `preflight` requires rotation gate `COMPLETE`.
- `post_verify` must confirm zero matches across all refs and tags.
- Any verification error reverts status to `BLOCKED` pending retry plan.

## Data Contracts
### `ScanReport`
- `run_id: str`
- `profile: str` (`tree` | `refs` | `history`)
- `started_at: datetime`
- `finished_at: datetime`
- `findings: list[SecretFinding]`
- `tool_exit_code: int`
- `status: str` (`PASS` | `FAIL` | `ERROR`)

### `RotationGateDecision`
- `incident_id: str`
- `status: str` (`BLOCKED` | `PARTIAL` | `COMPLETE`)
- `missing_systems: list[str]`
- `evidence_count: int`

### `GuardrailDecision`
- `status: str` (`ALLOW` | `BLOCK`)
- `reasons: list[str]`
- `required_checks: list[str]`

## Acceptance Criteria (Traceability)
| AC ID | Requirement | Verification Signal | Owner Phase |
|---|---|---|---|
| AC-001 | Active tree contains no private key artifact or equivalent secret payload | Tree scan returns `PASS`; file removed/replaced | Containment |
| AC-002 | All impacted credentials are rotated and checkpointed | `RotationGateDecision.status = COMPLETE` with evidence for each dependent system | Verification |
| AC-003 | CI enforces merge-blocking secret scan | Required status check present and failing findings block PR | Containment |
| AC-004 | History rewrite purges secret signatures from all refs/tags | Full-history scan returns zero matches post rewrite | Rewrite |
| AC-005 | Contributor migration steps are documented and communicated | Migration runbook exists and is linked in project artifacts | Stabilization |
| AC-006 | Guardrails remain durable after remediation | Regression structure checks pass for pre-commit + CI policy wiring | Stabilization |

## Interface To Planned Task Traceability
Task IDs are design-owned placeholders that @4plan must convert into executable plan tasks.

| Interface / Contract | Planned Task ID | Planned Implementation Scope | Linked AC IDs |
|---|---|---|---|
| `SecretScanService` + `ScanReport` | P90-T01 | Define scanner runner abstraction, scan profiles, deterministic findings schema | AC-001, AC-004, AC-006 |
| `RotationCheckpointService` + `RotationGateDecision` | P90-T02 | Implement rotation checkpoint registry and gating evaluation logic | AC-002, AC-004 |
| `SecretGuardrailPolicy` + `GuardrailDecision` | P90-T03 | Wire pre-commit and CI fail-closed guardrail decisions | AC-003, AC-006 |
| `HistoryRewriteCoordinator` | P90-T04 | Implement preflight/execute/post-verify orchestration contract and freeze checks | AC-004 |
| Governance Reporter outputs | P90-T05 | Update project/kanban/registry artifacts from validated control-plane outcomes | AC-005, AC-006 |

## Non-Functional Requirements
- Performance: tree/ref scans complete within CI budget; full-history scan duration is deterministic and reported.
- Security: fail-closed behavior for scanner errors, strict rotation gate before rewrite, zero-tolerance for high/critical findings.
- Reliability: idempotent checkpoint recording and rerunnable scan profiles.
- Auditability: each phase emits immutable run IDs and evidence references.
- Testability: all contracts expose deterministic status enums suitable for unit/integration assertions.

## ADR
- Draft ADR required due to architecture-impacting control-plane decision:
	- `docs/architecture/adr/0002-secret-remediation-control-plane.md`

## Open Questions For @4plan
1. Which concrete scanner toolchain is canonical for both local and CI (`gitleaks` only vs layered detectors)?
2. Where should rotation checkpoint evidence be stored (repo artifact vs external secure system reference-only)?
3. Which rewrite mechanism is approved in this repository (`git filter-repo` policy details and fallback)?

## Handoff
- Handoff target: @4plan
- Handoff readiness: READY
- Blocking issues: None

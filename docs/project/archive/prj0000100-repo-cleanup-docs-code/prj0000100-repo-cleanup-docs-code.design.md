# prj0000100-repo-cleanup-docs-code - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-29_

## Selected Option
Option B - Governance-First Incremental Cleanup.

Rationale summary:
- Highest score in @2think decision matrix for governance fit, impact, and maintainability.
- Reduces drift risk by making governance artifacts first-class and continuously updated.
- Keeps blast radius controlled through wave-based cleanup and explicit containment gates.

## Problem Statement and Goals
This project must clean repository docs/code incrementally while preventing policy drift. The design must ensure:
- deterministic updates to code anchor index metadata,
- deterministic local-search-first behavior,
- deterministic internet access gating to an explicit allowlist,
- low-risk rollback for broad cleanup operations.

## Architecture
### High-level Architecture (Governance-First)
1. Governance Control Layer (policy and schema contracts)
- `.github/agents/data/codestructure.md` as canonical code anchor index.
- `.github/agents/data/allowed_websites.md` as canonical internet allowlist.
- agent guidance enforces local-search-first workflow before internet lookup.

2. Incremental Cleanup Wave Layer (execution)
- Wave 1: Governance baseline lock and artifact normalization.
- Wave 2: Documentation consistency cleanup.
- Wave 3: Focused code hygiene cleanup (non-destructive).
- Wave 4: Project/tracking artifact synchronization and closure checks.

3. Verification and Containment Layer
- Per-wave exit gates validate schema integrity, policy compliance, and scope boundaries.
- Containment controls pause and revert wave-specific changes when drift/risk signals appear.

### Data Flow
1. Proposed cleanup change identified.
2. Local repository search performed first to gather evidence.
3. If external lookup required, domain gate checks against allowlist.
4. Changed code/doc anchors reflected in code structure index.
5. Wave exit checks confirm AC and interface contract compliance.

## Components and Responsibilities
| Component | Responsibility | Owner Lane |
|---|---|---|
| Governance Artifacts | Canonical policy/schema data for indexing and internet gate | @3design -> @4plan -> @6code |
| Cleanup Wave Executor | Performs bounded cleanup steps by wave scope | @6code |
| Verification Gate | Enforces per-wave validation and acceptance evidence | @5test/@7exec |
| Lifecycle Tracker | Keeps project artifacts and milestone states synchronized | @4plan/@9git |

## Interfaces and Contracts
### IFC-01: Code Structure Index Contract (`codestructure.md`)
Purpose: keep code anchors discoverable and auditable for changed symbols.

Schema contract (canonical table):
| Field | Type | Rule |
|---|---|---|
| `file` | string path | repository-relative path to source file |
| `line` | integer | 1-based anchor line number |
| `code` | string | exact anchor code snippet (import/global/class/function signature) |

Required markdown shape:
1. Header section: `# Code Structure Index`.
2. Guidance statement requiring updates on import/global/class/function changes.
3. Table header exactly: `| file | line | code |`.

Update protocol:
1. Determine changed files in active wave scope.
2. For each changed import/global/class/function anchor, insert or update one row.
3. Ensure line points to current location at change time.
4. Remove stale rows for deleted anchors in touched files.
5. Keep rows unique on (`file`, `line`, `code`) tuple.

### IFC-02: Local Search First Contract
Purpose: guarantee deterministic local evidence gathering before internet usage.

Policy contract:
1. MUST run local search first for repository questions/changes.
2. Preferred local tools: `search_subagent`, `rg`-equivalent repository search.
3. Internet fetch/search is allowed only when local search is insufficient for required evidence.
4. Every internet action must include explicit rationale tied to unresolved local evidence gap.

Compliance signal:
- Wave log/checkpoint records show local-search step before any internet access step.

### IFC-03: Internet Search Gate Contract (`allowed_websites.md`)
Purpose: enforce fail-closed external domain control.

Policy source:
- `.github/agents/data/allowed_websites.md` is the sole allowlist authority.

Gate behavior:
1. Parse allowed domains from `## Allowed Domains` list.
2. Permit internet fetch/search only when target domain matches allowlist entry.
3. If no match: block action and return policy violation message.
4. If policy file is missing/malformed: fail closed (block internet action).

Current required domains baseline:
- `wikipedia.org`
- `github.com`
- plus existing documented domains in the policy file.

## Non-Functional Requirements
| NFR ID | Constraint | Target |
|---|---|---|
| NFR-01 | Safety containment | Wave-scoped changes only; no broad uncontrolled refactors |
| NFR-02 | Performance | Governance checks add minimal overhead and no meaningful slowdown in normal cleanup flow |
| NFR-03 | Security | Internet access must be allowlist-gated with fail-closed behavior |
| NFR-04 | Reliability | Governance artifacts remain parseable and synchronized after each wave |
| NFR-05 | Maintainability | Contracts are explicit, version-stable, and easy for downstream agents to execute |
| NFR-06 | Auditability | Each wave produces evidence for local-first and gate compliance |

## Acceptance Criteria Table
| AC ID | Requirement | Design Coverage |
|---|---|---|
| AC-01 | Canonical lifecycle artifacts exist and follow templates | This design defines actionable sections/contracts for @4plan handoff and milestone gating |
| AC-02 | Project tracking updated consistently | Lifecycle tracker component and traceability tasks include project overview synchronization |
| AC-03 | `codestructure.md` schema and seeded anchors maintained | IFC-01 defines schema and update protocol |
| AC-04 | `allowed_websites.md` includes explicit allowed domains including wikipedia.org and github.com | IFC-03 defines allowlist authority and baseline domain expectation |
| AC-05 | Local search first and internet only for allowlisted domains | IFC-02 + IFC-03 define mandatory policy and gate behavior |

## Interface-to-Task Traceability
Planned implementation task IDs are pre-allocated for @4plan decomposition.

| Trace ID | Interface/Contract | Planned Task ID | Planned Task Outcome |
|---|---|---|---|
| TR-01 | IFC-01 Code Structure Index Contract | P4-T01 | Enforce schema header/table and row uniqueness/update protocol |
| TR-02 | IFC-01 Code Structure Index Contract | P4-T02 | Add per-wave index delta checklist and stale-anchor cleanup step |
| TR-03 | IFC-02 Local Search First Contract | P4-T03 | Add workflow gate requiring local search evidence before external lookup |
| TR-04 | IFC-03 Internet Search Gate Contract | P4-T04 | Add allowlist parser/check and fail-closed block behavior |
| TR-05 | IFC-03 Internet Search Gate Contract | P4-T05 | Add compliance validation step against allowed domains list |
| TR-06 | NFR/Containment Controls | P4-T06 | Define wave rollback procedure and stop-the-line triggers |
| TR-07 | Lifecycle Tracker Requirements | P4-T07 | Define milestone/status update sequence including M2 completion rule |

## Rollback and Containment Strategy
### Risk Model
Broad cleanup can create hidden regressions (stale anchors, policy drift, scope bleed, unintended file churn). Containment must be wave-local and reversible.

### Containment Controls
1. Wave boundary lock:
- Changes limited to pre-declared wave scope list.
- Out-of-scope changes trigger stop-the-line review.

2. Governance drift lock:
- If `codestructure.md` or `allowed_websites.md` contract checks fail, do not advance wave.

3. Fail-closed internet gate:
- Any allowlist uncertainty blocks internet usage until corrected.

### Rollback Procedure
1. Detect failure condition (schema mismatch, policy violation, scope bleed, or unverifiable anchors).
2. Freeze current wave progression.
3. Revert only the failing wave delta (not prior validated waves).
4. Re-run wave entry checklist and contract checks.
5. Resume only after explicit validation pass.

## Assumptions
- Branch remains `prj0000100-repo-cleanup-docs-code` for all lifecycle steps.
- Cleanup remains non-destructive and within project scope boundary.
- No production feature additions are introduced as part of this cleanup effort.

## Open Questions for @4plan
No blocking open questions. @4plan should decompose TR-01..TR-07 into execution tasks and tests without altering contract intent.

# prj0000100-repo-cleanup-docs-code - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## Root Cause Analysis
- Cleanup debt accumulates because non-dot file hygiene is distributed across many folders with no single enforced cadence, so low-risk consistency work is repeatedly deferred behind feature/security work.
- Discoverability is poor because repository governance metadata is split across multiple artifacts and is partially manual; examples include code anchor indexing in `.github/agents/data/codestructure.md` and internet policy guidance in `.github/agents/data/allowed_websites.md`.
- Current state relies on policy text more than deterministic guardrails, which causes drift between intended behavior (local search first, allowed-domain internet usage) and day-to-day execution.
- Prior projects show this pattern recurring: policy/documentation quality improves when artifacts are explicit and auditable, then regresses when updates are not operationalized into routine workflow gates.

## Constraint Map
- Branch must remain `prj0000100-repo-cleanup-docs-code`.
- Work must stay in project scope boundaries from `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.
- This phase is options analysis only (no production code edits).
- Naming and conduct must align with `docs/project/naming_standards.md` and `docs/project/code_of_conduct.md`.
- Governance goals are explicit:
	- keep `.github/agents/data/codestructure.md` updated with imports/globals/classes/functions and line numbers,
	- enforce local search first and internet usage only for allowed domains in `.github/agents/data/allowed_websites.md`.

## Prior-Art Evidence
- `docs/project/prj0000074/prj0000074.think.md` (meta-governance cleanup patterns and risk of drift without durable process hooks).
- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md` (deterministic policy guardrails via explicit checks).
- `docs/project/prj0000052/project-management.think.md` (single-source-of-truth discipline for lifecycle/state discoverability).
- `.github/agents/data/2think.memory.md` (recurring lesson: re-validate assumptions and codify durable gates).
- `.github/agents/data/codestructure.md` and `.github/agents/data/allowed_websites.md` (project-specific governance artifacts).

## Options
### Option A - Manual Sweep Then Document
Approach:
- Perform a broad, one-pass manual review/cleanup of non-dot files, then update docs and governance artifacts at the end.

Research coverage:
- Literature review: `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`, `docs/project/kanban.md`.
- Alternative enumeration: contrasted with governance-first and tooling-assisted approaches.
- Constraint mapping: project scope boundary and branch gate requirements.
- Stakeholder impact: high burden on @6code/@7exec for large review window.
- Risk enumeration: listed below.

Tradeoffs:
- Fast visible cleanup initially.
- High coordination overhead and easy to miss late governance updates.
- Discoverability gains are delayed to end-of-pass.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy / validation signal |
|---|---|---|---|
| Missed code anchors in code structure index | H | M | Run structured diff review for `.github/agents/data/codestructure.md` against changed files and spot-check anchor line validity |
| Policy text updated but behavior not adopted | M | H | Validate session workflow evidence shows local-first search before any internet action |
| Large-scope review fatigue causes inconsistent quality | M | M | Enforce per-folder completion checklist with reviewer sign-off signal in project artifacts |

### Option B - Governance-First Incremental Cleanup
Approach:
- Start by locking governance workflow expectations (codestructure and allowed-websites policy handling), then execute incremental cleanup waves by domain (docs, tooling, src-old hygiene, project artifacts), updating governance artifacts continuously.

Research coverage:
- Literature review: `.github/agents/data/codestructure.md`, `.github/agents/data/allowed_websites.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.
- Prior-art search: `docs/project/prj0000074/prj0000074.think.md`, `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`, `docs/project/prj0000052/project-management.think.md`.
- Constraint mapping: no broad unrelated refactors; branch and scope boundaries remain strict.
- Stakeholder impact: balanced load across @3design, @4plan, @5test, @6code, @7exec.
- Risk enumeration: listed below.

Tradeoffs:
- Slightly slower initial visual progress than a pure sweep.
- Strong governance fit and lower rework risk.
- Improves discoverability early by treating index/policy artifacts as first-class deliverables.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy / validation signal |
|---|---|---|---|
| Governance process not consistently followed in later waves | M | H | Add recurring verification checkpoints per wave: codestructure delta completeness + allowed-domain policy adherence log |
| Increment boundaries chosen poorly, causing duplicated touchpoints | M | M | Require wave definition table (scope, owner, exit signal) in project artifacts before execution |
| Drift between docs intent and cleanup implementation | L | H | Gate each wave on artifact sync review (`project.md`, think/design/plan updates, governance files) |

### Option C - Tooling-Assisted Inventory + Semi-Automated Governance Sync
Approach:
- Build/extend helper scripts to inventory non-dot files and generate suggested codestructure/policy deltas, then perform cleanup based on generated reports.

Research coverage:
- Literature review: current governance files and project lifecycle artifacts.
- Alternative enumeration: manual-first vs governance-first vs tooling-assisted.
- Prior-art search: `docs/project/prj0000074/prj0000074.design.md` (meta quality improvements), `docs/architecture/archive/DIRECTORY_STRUCTURE.md` (structure mapping reference).
- Constraint mapping: higher setup overhead and possible scope creep for this project phase.
- Stakeholder impact: heavier on @6code/@7exec; delayed value for docs stakeholders.
- Risk enumeration: listed below.

Tradeoffs:
- Potential long-term efficiency gains.
- Higher immediate effort and complexity for this project timeline.
- Risk of spending time on tooling rather than cleanup outcomes.

Risk-to-testability mapping:
| Failure mode | Likelihood | Impact | Testability strategy / validation signal |
|---|---|---|---|
| Tool output diverges from required governance schema | M | H | Validate generated output strictly against required table/schema expectations before acceptance |
| Automation introduces false confidence and misses edge cases | M | M | Mandatory human verification sample across each major directory |
| Tooling work expands beyond cleanup project intent | H | M | Scope checkpoint: reject automation work not directly reducing current cleanup backlog |

## Decision Matrix
Scoring scale: 1 (worst) to 5 (best). Weighted score = score x weight.

| Criterion | Weight | Option A | Option B | Option C |
|---|---:|---:|---:|---:|
| Risk (lower delivery/regression risk) | 25 | 2 (50) | 4 (100) | 2 (50) |
| Effort (efficient within current scope/timeline) | 15 | 3 (45) | 4 (60) | 2 (30) |
| Impact (cleanup + discoverability improvement) | 25 | 3 (75) | 5 (125) | 4 (100) |
| Governance fit (codestructure + allowed-sites + local-first policy) | 20 | 2 (40) | 5 (100) | 3 (60) |
| Maintainability (durable operating model after project) | 15 | 2 (30) | 5 (75) | 4 (60) |
| Total | 100 | 240 | 460 | 300 |

## Recommendation
**Option B - Governance-First Incremental Cleanup**

Rationale:
- It maximizes governance fit and maintainability while keeping delivery risk materially lower than a broad manual sweep or tooling-heavy detour.
- It directly addresses root causes (drift, poor discoverability, inconsistent update cadence) by making governance updates continuous, not end-loaded.
- It aligns with historical prior art that favored deterministic, auditable gates over one-off manual campaigns:
	- `docs/project/prj0000074/prj0000074.think.md`
	- `docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md`
	- `docs/project/prj0000052/project-management.think.md`

Risk-to-testability mapping for selected option:
| Key risk | Likelihood | Impact | Validation signal |
|---|---|---|---|
| Wave-by-wave governance drift | M | H | Each wave closes only when `.github/agents/data/codestructure.md` and policy usage evidence are updated and reviewed |
| Scope bleed into unrelated refactors | M | M | Scope checklist pass against project boundary before approving next wave |
| Discoverability improvements not retained | L | H | Artifact audit confirms lifecycle files and governance docs remain current at each lane transition |

## Open Questions
1. Which domain order should @3design lock first for wave sequencing: docs -> governance -> code hygiene, or governance -> docs -> code hygiene?
2. What is the explicit wave exit checklist format to be reused by @4plan/@5test/@6code (minimum fields and approver)?
3. Should a follow-up project be pre-created for tooling automation (Option C subset) after baseline cleanup is stable?

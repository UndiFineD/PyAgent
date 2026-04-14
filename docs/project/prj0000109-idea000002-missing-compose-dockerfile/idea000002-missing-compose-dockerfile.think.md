# idea000002-missing-compose-dockerfile - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-31_

## Root Cause Analysis
- Historical root defect (captured in idea intake): `deploy/compose.yaml` referenced a non-existent Dockerfile path, breaking clean-checkout compose runs.
- Current-state discovery: repository now points `deploy/compose.yaml` to `deploy/Dockerfile.pyagent`, and `tests/deploy/test_compose_dockerfile_paths.py` already validates Dockerfile path contracts.
- Primary remaining gap for this project: resolve how to handle the now-partially-stale idea while preserving deployment reliability and avoiding scope drift into full compose topology redesign.

Evidence:
- `deploy/compose.yaml`
- `deploy/Dockerfile.pyagent`
- `tests/deploy/test_compose_dockerfile_paths.py`
- `docs/project/ideas/idea000002-missing-compose-dockerfile.md`
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`

## Research Coverage
### Literature Review
- Idea and project artifacts confirm the original defect and intended remediation path.
- Prior project `prj0000091` already documented and delivered a fix strategy centered on deploy-local Dockerfile normalization.

### Alternative Enumeration
- Option A: Treat as resolved and close with evidence-only refresh.
- Option B: Add incremental governance hardening around existing fix (contract-level validation and ownership/documentation normalization).
- Option C: Consolidate dual compose topology into a single canonical parameterized model.

### Prior-Art Search
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md`
- `docs/project/ideas/idea000010-docker-compose-consolidation.md`
- `docs/project/prj0000076/prj0000076.think.md`

### Constraint Mapping
- Branch must remain `prj0000109-idea000002-missing-compose-dockerfile`.
- Scope limited to this project artifact plus required `@2think` memory/log updates.
- Must comply with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Avoid implementation planning depth that belongs to `@4plan` and avoid code changes.

### Stakeholder Impact
- Deploy/onboarding users: affected by compose reliability and command predictability.
- `@3design` and `@4plan`: depend on clear recommendation boundary between defect closure and broader compose consolidation.
- CI/quality owners: impacted by whether guardrails remain deterministic and discoverable.

### Risk Enumeration Method
- Each option includes at least 3 failure modes with likelihood/impact ratings and explicit validation signal mapping.

### Approved External Pattern References
- Docker Compose build spec (GitHub mirror): relative `build.dockerfile` and `build.context` semantics, portability constraints.
	- https://github.com/docker/docs/blob/main/content/reference/compose-file/build.md
- Docker multiple-compose merge behavior (GitHub mirror): path resolution and merge precedence concerns.
	- https://github.com/docker/docs/blob/main/content/manuals/compose/how-tos/multiple-compose-files/merge.md

## Constraint Snapshot
- Technical: preserve working `deploy/compose.yaml` contract unless replacement has lower operational risk.
- Scope: do not perform full deploy architecture redesign in this project unless justified by material reliability gain.
- Time: prefer option with fast handoff readiness to `@3design`.
- Governance: recommendation must include prior-art links and risk-to-testability mapping.

## Options
### Option A - Evidence-only closure (treat issue as already resolved)
Approach:
- Keep deploy files unchanged.
- Update project-level documentation to mark the defect as historically resolved by prior project.

Research task coverage used:
- Literature review
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

SWOT:
- Strengths: minimal effort; zero runtime blast radius; immediate throughput.
- Weaknesses: may under-address ambiguity from dual compose files.
- Opportunities: close stale backlog item cleanly with historical traceability.
- Threats: future regressions if guardrails become stale or are bypassed.

Security and delivery risks (risk -> likelihood/impact -> testability signal):
- Silent contract drift in compose references -> M/M -> run `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py`.
- Misleading project closure without ownership clarity -> M/M -> docs consistency check across project artifacts and idea registry.
- Accidental reintroduction via unrelated deploy edits -> M/H -> `docker compose -f deploy/compose.yaml config` in CI smoke stage.

Pros:
- Lowest implementation complexity.
- No additional architectural commitments.

Cons:
- Does not reduce known compose topology ambiguity (`deploy/compose.yaml` vs `deploy/docker-compose.yaml`).
- Relies on existing safeguards without improving governance clarity.

### Option B - Incremental hardening around existing fix (recommended)
Approach:
- Preserve current deploy-local Dockerfile contract.
- Strengthen explicit acceptance/ownership/validation contracts in project artifacts so the fix remains durable and auditable.
- Defer compose topology consolidation to idea000010 lane.

Research task coverage used:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

SWOT:
- Strengths: best balance of reliability, scope control, and governance quality.
- Weaknesses: does not eliminate dual-compose complexity in this project.
- Opportunities: codify stable boundary between defect remediation and broader consolidation roadmap.
- Threats: partial improvements can be misinterpreted as full compose architecture completion.

Security and delivery risks (risk -> likelihood/impact -> testability signal):
- Regression in Dockerfile path validity -> L/H -> deterministic unit contract test for compose dockerfile paths.
- Drift between docs and deploy reality -> M/M -> docs-policy validation plus artifact cross-reference check.
- Scope creep into compose consolidation -> M/M -> diff-scope gate: only project folder and `@2think` memory/log files changed.

Pros:
- Keeps known-working runtime contract intact.
- Improves handoff quality and acceptance traceability.
- Aligns with prior-art decision from `prj0000091` while avoiding duplication.

Cons:
- Leaves full topology consolidation for later workstream.
- Requires disciplined documentation governance to deliver value.

### Option C - Full compose topology consolidation now
Approach:
- Merge or rationalize `deploy/compose.yaml` and `deploy/docker-compose.yaml` under one canonical strategy in this project.

Research task coverage used:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

SWOT:
- Strengths: largest long-term simplification potential.
- Weaknesses: highest analysis and implementation complexity; broad blast radius.
- Opportunities: resolve idea000010 adjacency while touching deploy stack.
- Threats: increased risk of runtime regression across distinct service topologies.

Security and delivery risks (risk -> likelihood/impact -> testability signal):
- Service behavior regressions from merge precedence/path handling -> M/H -> exhaustive compose config snapshots with `docker compose config` for each intended profile.
- Environment-specific breakage (GPU/ollama/fleet variants) -> M/H -> matrix startup smoke tests per topology.
- Governance overreach against project scope boundary -> H/M -> branch scope guard and review checklist should fail if unrelated deploy assets change.

Pros:
- Potentially removes dual-compose ambiguity in one pass.

Cons:
- Violates minimal-blast-radius intent of this idea.
- Higher probability of schedule slippage and unintended outages.

## Acceptance Criteria Mapping
| Acceptance Criterion | Option A | Option B | Option C |
|---|---|---|---|
| AC-001 Preserve valid compose Dockerfile path on clean checkout | Meets via no change | Meets and reinforces | Meets if executed correctly |
| AC-002 Keep project scope bounded to this defect lane | Strong | Strong | Weak (high scope expansion risk) |
| AC-003 Provide explicit, testable regression signals | Medium (reuses existing only) | Strong (explicit governance + existing tests) | Medium/Strong but costly |
| AC-004 Maintain clear handoff to `@3design` without over-planning | Medium | Strong | Weak |
| AC-005 Align with prior-art decisions and roadmap sequencing | Medium | Strong | Medium |

## Decision Matrix
Scoring scale: 1 (poor) to 5 (strong).

| Criterion | Weight | Option A | Option B | Option C |
|---|---:|---:|---:|---:|
| Reliability preservation | 0.30 | 4 | 5 | 3 |
| Scope control | 0.25 | 5 | 5 | 1 |
| Delivery speed | 0.15 | 5 | 4 | 1 |
| Governance/testability clarity | 0.20 | 3 | 5 | 3 |
| Strategic alignment with prior-art | 0.10 | 3 | 5 | 3 |
| Weighted total | 1.00 | 4.10 | 4.90 | 2.10 |

## Recommendation
**Select Option B - Incremental hardening around existing fix.**

Rationale:
- Prior-art already solved the direct path defect (`prj0000091`), so repeating implementation-level change is unnecessary.
- Option B best satisfies reliability and governance gates while keeping this project within branch/scope constraints.
- It explicitly preserves separation of concerns: this project addresses defect-lane closure quality; compose-topology consolidation remains in idea000010 scope.

Prior-art references informing recommendation:
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md`
- `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md`
- `docs/project/ideas/idea000010-docker-compose-consolidation.md`

Risk-to-testability summary for recommended option:
- Path regression risk -> validate with targeted compose Dockerfile path tests.
- Documentation drift risk -> validate with docs policy + cross-artifact consistency review.
- Scope creep risk -> validate by strict changed-file diff against allowed project files.

## Open Questions
- Should `@3design` explicitly mark this project as governance-hardening only (no deploy file edits) unless new contradictory evidence appears?
- Should acceptance criteria include an explicit non-goal statement deferring compose consolidation to idea000010?
- Should `@3design` require a periodic guard (for example CI smoke selector) beyond existing unit-level path tests?

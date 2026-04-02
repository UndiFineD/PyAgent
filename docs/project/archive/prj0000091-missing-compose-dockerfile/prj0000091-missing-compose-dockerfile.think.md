# missing-compose-dockerfile - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
- Primary defect: `deploy/compose.yaml` configures `dockerfile: src/infrastructure/docker/Dockerfile` with `context: ..`, but `src/infrastructure/` does not exist in repository.
- Secondary contributor: deploy topology is ambiguous because both `deploy/compose.yaml` and `deploy/docker-compose.yaml` exist with different targets and no single normalized convention.
- Prior-art confirms this is known and unresolved:
	- `docs/project/ideas/idea000002-missing-compose-dockerfile.md`
	- `docs/project/prj0000076/prj0000076.think.md`
	- `docs/project/ideas/idea000010-docker-compose-consolidation.md`

## Constraint Mapping
- Must remain in project scope: deploy compose/Dockerfile path resolution and project docs only.
- Must preserve one-project-one-branch governance: expected branch `prj0000091-missing-compose-dockerfile` validated.
- Must optimize for clean-checkout reliability: no hidden local prerequisites.
- Must minimize blast radius: avoid broad deploy stack redesign in this project.
- Must stay maintainable for downstream @3design/@4plan implementation.

## Options
### Option A - Adjust compose path to an existing Dockerfile
Approach:
- Update `deploy/compose.yaml` `dockerfile` value to one of the existing files under `deploy/` (for example `deploy/Dockerfile.coder-node`), keeping `context: ..`.

Evidence and research coverage:
- Literature review: `docs/project/ideas/idea000002-missing-compose-dockerfile.md`
- Alternative enumeration context: `deploy/compose.yaml`, `deploy/Dockerfile.coder-node`, `deploy/Dockerfile.SQLAgent`
- Constraint mapping: `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.project.md`
- Stakeholder impact: `docs/project/prj0000076/prj0000076.think.md` (clean-checkout onboarding impact)
- Prior-art references: `docs/project/prj0000076/prj0000076.think.md`, `docs/project/ideas/idea000010-docker-compose-consolidation.md`

Pros:
- Fastest implementation path.
- No new Dockerfile artifact to maintain.
- Easy rollback (single-line compose change).

Cons:
- Reliability risk if selected Dockerfile is semantically wrong for `pyagent` service runtime.
- Can couple unrelated image purpose into compose target.
- May preserve layout inconsistency and technical debt.

Risk-to-testability mapping:
- Wrong image entrypoint/runtime assumptions (H): validate with clean-checkout `docker compose -f deploy/compose.yaml config` plus container start smoke test.
- Missing dependencies in chosen Dockerfile (M): run app startup command health smoke in container.
- Hidden behavior drift for existing users (M): compare resulting container env/cmd against expected `pyagent` runtime contract.

Effort:
- Low.

Rollback:
- Revert compose file path change; no artifact migration required.

### Option B - Add missing Dockerfile at referenced path
Approach:
- Create `src/infrastructure/docker/Dockerfile` so current compose reference remains valid.

Evidence and research coverage:
- Literature review: `docs/project/ideas/idea000002-missing-compose-dockerfile.md`
- Alternative enumeration context: current reference in `deploy/compose.yaml` and existing Dockerfiles in `deploy/`
- Prior-art search: `docs/project/kanban.md` entry for `prj0000012` deployment operations; `data/projects.json` `prj0000012`
- Constraint mapping: in-scope guidance in `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.project.md`
- Stakeholder impact: contributors using default compose onboarding path

Pros:
- Preserves current compose contract exactly.
- Very clear fix for clean checkout: referenced file now exists.
- Reduces immediate friction for users invoking existing command paths.

Cons:
- Introduces new `src/infrastructure/` path that currently does not exist and may conflict with naming/layout expectations.
- Higher chance of creating duplicate Docker build logic across `deploy/` and `src/infrastructure/`.
- Future consolidation burden likely increases.

Risk-to-testability mapping:
- New path diverges from established deploy file placement (M): lint/path convention check and documentation alignment review.
- Dockerfile implementation drifts from other deploy images (M): build and diff review of base image/dependency layers.
- Future ownership ambiguity (L/M): require explicit ownership note in design artifact and release notes.

Effort:
- Medium.

Rollback:
- Remove newly added Dockerfile and revert any docs references.

### Option C - Normalize deploy docker layout with minimal blast radius
Approach:
- Keep compose in `deploy/` and point `deploy/compose.yaml` to a normalized Dockerfile path inside `deploy/` dedicated to this service (for example a new `deploy/Dockerfile.pyagent` or an explicitly selected existing deploy Dockerfile).
- Define as a minimal normalization only (no full compose consolidation in this project).

Evidence and research coverage:
- Literature review: `docs/project/ideas/idea000002-missing-compose-dockerfile.md`
- Prior-art search: `docs/project/ideas/idea000010-docker-compose-consolidation.md` and `docs/project/kanban.md` `prj0000012`
- Constraint mapping: project scope boundary in `docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.project.md`
- Stakeholder impact: clean-checkout users, deploy maintainers, downstream `@3design`/`@4plan`
- Risk enumeration grounded by dual-compose ambiguity noted in `docs/project/prj0000076/prj0000076.think.md`

Pros:
- Best maintainability signal: deploy artifacts stay co-located.
- Improves reliability on clean checkout without introducing non-existent top-level paths.
- Creates clean runway for later `idea-010` consolidation with constrained blast radius.

Cons:
- Slightly more effort than one-line path fix.
- Requires careful naming/ownership choice for normalized Dockerfile target.
- Needs explicit non-goal statement to avoid unplanned full consolidation.

Risk-to-testability mapping:
- Introduce new normalized Dockerfile but miss runtime needs (M): clean-checkout build+run smoke in compose.
- Regression from accidental compose semantics change (M): `docker compose config` diff check before/after.
- Scope creep into full consolidation (L/M): enforce file-level scope check and explicit non-goals in design/plan.

Effort:
- Medium.

Rollback:
- Revert compose path change and remove newly added normalized Dockerfile if created.

## Decision Matrix
| Criterion | Option A: point to existing Dockerfile | Option B: add missing Dockerfile at referenced path | Option C: normalize deploy layout (minimal) |
|---|---|---|---|
| Clean-checkout reliability | Medium | High | High |
| Maintainability | Low/Medium | Medium | High |
| Blast radius | Low | Medium | Medium |
| Implementation speed | High | Medium | Medium |
| Alignment with prior-art and future consolidation | Medium | Low/Medium | High |
| Rollback simplicity | High | Medium | Medium |

## Recommendation
**Option C - Normalize deploy docker layout with minimal blast radius**

Rationale:
- It provides reliable clean-checkout behavior while keeping deployment assets in the deploy domain.
- It avoids introducing a brand-new `src/infrastructure/` tree purely to satisfy one reference.
- It aligns with historical prior-art showing dual compose ambiguity and preserves a clean incremental path toward future consolidation work.

Historical prior-art citations:
- `docs/project/prj0000076/prj0000076.think.md`
- `docs/project/ideas/idea000010-docker-compose-consolidation.md`
- `docs/project/kanban.md` (released `prj0000012` deployment-operations context)

## Open Questions
- For @3design: Should normalized target be a new dedicated `deploy/Dockerfile.pyagent` or a documented reuse of an existing deploy Dockerfile?
- For @3design: Is minimal guardrail validation implemented as a lightweight compose path existence check or as a compose config smoke check in CI?
- For @3design: Which compose file is canonical for onboarding in docs after this fix (`deploy/compose.yaml` vs other topology variants)?

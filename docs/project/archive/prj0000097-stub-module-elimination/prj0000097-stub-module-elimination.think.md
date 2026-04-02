# prj0000097-stub-module-elimination - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## Root Cause Analysis
The original idea assumption (six empty stub packages) is now stale. All six target packages under `src/` have implemented `__init__.py` files, but maturity is uneven.

Primary root causes:
1. Historical placeholder strategy from earlier project work introduced import-only packages as scaffolding and then partially evolved them.
2. Current topology mixes top-level compatibility packages (`runtime`, `runtime_py`, `memory`, `cort`) with `src.core.*` modules that expose overlapping concepts.
3. Existing tests still reward importability and thin API compatibility, not clear ownership boundaries.

## Package Audit Findings (Idea 11 Targets)
| Target package | Actual state | Conflict / overlap risk | Evidence |
|---|---|---|---|
| `src/rl/` | Implemented but minimal (`validate()` only) | Placeholder-grade module with low functional ownership; imported by smoke test only | `src/rl/__init__.py`, `tests/test_rl_package.py` |
| `src/speculation/` | Implemented but minimal (`validate()` only) | Placeholder-grade module with low functional ownership; imported by smoke test only | `src/speculation/__init__.py`, `tests/test_speculation_package.py` |
| `src/cort/` | Implemented (`ChainOfThought`, `ThoughtNode`) | Uses top-level `context_manager` import and lives outside `src.core` conventions, but has active integration use | `src/cort/__init__.py`, `tests/test_cort.py`, `tests/integration/test_context_and_skills.py` |
| `src/runtime_py/` | Implemented wrapper/fallback runtime helpers | Name-adjacent with `runtime`; intentionally avoids extension shadowing, but path semantics are sensitive | `src/runtime_py/__init__.py`, `tests/runtime/test_watch_file.py`, `tests/runtime/test_http_server.py` |
| `src/runtime/` | Implemented compatibility shim (`spawn_task`, `set_timeout`, queue, shutdown) | Concept overlap with `src/core/runtime.py` and compiled runtime extension naming | `src/runtime/__init__.py`, `src/core/runtime.py`, `tests/runtime/test_spawn_task.py` |
| `src/memory/` | Implemented `MemoryStore` + `validate()` | Type/function overlap with `src/core/memory.py` and `src/core/memory/` package | `src/memory/__init__.py`, `src/core/memory.py`, `src/core/memory/AutoMemCore.py`, `tests/test_memory_package.py` |

Conclusion: none of the six are empty-module stubs anymore. Two (`rl`, `speculation`) are still thin placeholders; four (`cort`, `runtime_py`, `runtime`, `memory`) are active compatibility/runtime layers.

## Options
### Option A - Full Elimination and Core Consolidation
Problem statement:
- Remove all six top-level packages and migrate call sites to canonical `src.core.*` modules (or other explicit homes).

Proposed approach:
- Decommission `src/rl`, `src/speculation`, `src/cort`, `src/runtime_py`, `src/runtime`, `src/memory`.
- Rewrite imports and tests to only use consolidated modules.

Research coverage:
- Literature review: `docs/project/ideas/idea000011-stub-module-elimination.md`, `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.project.md`
- Prior-art search: `docs/project/prj0000007/plan.md`, `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md`
- Constraint mapping: branch/scope guard from project overview + naming policy in `docs/project/naming_standards.md`
- Stakeholder impact: runtime tests, integration tests, @3design/@6code migration blast radius
- Risk enumeration: below

Pros:
- Clear architecture ownership and less namespace ambiguity.
- Maximum long-term cleanup value.

Cons:
- Highest short-term break risk (imports, tests, extension compatibility).
- Larger migration project than idea-11 strict scope likely allows in one slice.

Risk and testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Runtime import breakage for subprocess tests | H | H | Run `tests/runtime/*` import and behavior suites in CI |
| Hidden third-party/internal import dependencies | M | H | Add temporary import telemetry and failing compatibility tests |
| Regression in ChainOfThought integration path | M | M | Execute `tests/test_cort.py` and integration suite with focused markers |

Rollback:
- Restore package directories and compatibility exports from pre-change commit; re-enable import smoke tests while migration plan is redesigned.

### Option B - Compatibility Freeze (No Removal)
Problem statement:
- Keep all six packages but formalize them as compatibility surface and stop treating them as stubs.

Proposed approach:
- Keep package names and APIs as-is.
- Add explicit ownership notes and guard tests that prevent reverting to empty modules.

Research coverage:
- Literature review: idea/project docs above
- Constraint mapping: strict scope in project overview; no broad refactor
- Stakeholder impact: lowest impact to @6code and current test users
- Risk enumeration: below
- Prior-art: `docs/project/prj0000007/plan.md`, `docs/project/prj0000024/plan.md`

Pros:
- Minimal disruption.
- Fastest route to stable CI.

Cons:
- Leaves naming overlap unresolved (`memory`, `runtime` vs `src.core.*`).
- Delays true elimination objective from idea 11.

Risk and testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Architectural drift persists and deepens | H | M | Add static checks tracking duplicate concept modules |
| Developers continue importing wrong surface | M | M | Add lint/import policy tests for allowed modules |
| Future deprecation cost increases | M | M | Track package usage trend via grep-based CI report |

Rollback:
- No functional rollback needed; only remove added governance docs/tests if they prove noisy.

### Option C - Targeted Stub Elimination (Recommended)
Problem statement:
- Separate truly placeholder packages from active compatibility modules, then eliminate only the placeholder tier first.

Proposed approach:
- Phase 1: classify targets into
	- Active compatibility/runtime: `cort`, `runtime_py`, `runtime`, `memory` (retain)
	- Placeholder-grade: `rl`, `speculation` (deprecate then remove in controlled step)
- Phase 2: migrate any `rl`/`speculation` callsites/tests to explicit successor contract (or explicitly archive if no owner).

Research coverage:
- Literature review: current target files + tests
- Prior-art search: `docs/project/prj0000007/plan.md`, `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md`, `docs/architecture/archive/agents.md`
- Constraint mapping: project branch/scope rules in `prj0000097-stub-module-elimination.project.md`
- Stakeholder impact: limited to two placeholder packages for first slice, lower blast radius
- Risk enumeration: below

Pros:
- Preserves working runtime compatibility while still delivering real elimination progress.
- Fits strict idea-11 scope with a minimal testable first slice.
- Creates clear handoff path for @3design and @6code.

Cons:
- Requires explicit design decision about successor ownership for `rl` and `speculation`.
- Leaves larger `runtime`/`memory` consolidation for a later project.

Risk and testability mapping:
| Risk | Likelihood | Impact | Testability strategy |
|---|---|---|---|
| Removing `rl`/`speculation` breaks import smoke tests immediately | H | M | Update/replace `tests/test_rl_package.py` and `tests/test_speculation_package.py` with deprecation or successor tests |
| No agreed successor API leads to orphaned tests | M | M | Add design-time acceptance criteria in @3design artifact before @6code changes |
| Implicit package consumers outside tests are missed | M | H | Repo-wide import scan gate before and after change (`rg` import map) |

Rollback:
- Recreate `rl`/`speculation` minimal modules with previous validate behavior; restore smoke tests from prior commit.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Scope fit to Idea 11 | 3 | 2 | 5 |
| Delivery risk (lower is better) | 1 | 5 | 4 |
| Architectural clarity gained | 5 | 2 | 4 |
| Testability of first slice | 2 | 4 | 5 |
| Rollback safety | 2 | 5 | 4 |
| Total | 13 | 18 | 22 |

## Recommendation
**Option C - Targeted Stub Elimination**

Rationale:
- It is the only option that keeps strict scope to idea 11 while acknowledging current reality: the six targets are not uniformly stubs.
- It delivers a minimal, testable slice by focusing elimination on placeholder-grade packages (`rl`, `speculation`) first.
- It preserves active compatibility layers (`cort`, `runtime_py`, `runtime`, `memory`) to avoid unnecessary runtime regressions.

First minimal, testable slice for @3design and @6code:
1. Design contract: mark `rl` and `speculation` as deprecated placeholder packages with explicit successor/retirement decision.
2. Test contract: replace pure import-smoke assertions for those two packages with either
	 - deprecation-warning assertions (if short-lived compatibility retained), or
	 - successor import/behavior assertions (if removed).
3. Validation gate: run repo-wide import scan and targeted tests to prove no unresolved imports remain.

Risk-to-testability gate for handoff:
- Every planned removal risk must map to an executable validation signal (import scan + targeted pytest files) before @6code proceeds.

## Open Questions
1. What is the explicit successor surface for `rl` and `speculation` (merge into existing module, archive, or new owned package)?
2. Should `runtime` remain a compatibility shim long-term, or is there a follow-up project to converge on `src.core.runtime`?
3. Should `memory` top-level remain as lightweight runtime helper while `src.core.memory*` handles advanced memory concerns?
4. Do we need a temporary compatibility window (one release) before fully deleting placeholder packages?

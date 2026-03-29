# prj0000099-stub-module-elimination - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## Root Cause Analysis
The original objective assumed stub-only package surfaces that still needed elimination work.
Current evidence shows these targets are already implemented and exported package surfaces, not empty init stubs:
- `src/rl/__init__.py`
- `src/speculation/__init__.py`
- `src/cort/__init__.py`
- `src/runtime_py/__init__.py`
- `src/runtime/__init__.py`
- `src/memory/__init__.py`

Focused validation tests are green (5 passed):
- `tests/test_rl_package.py`
- `tests/test_speculation_package.py`
- `tests/test_cort.py`
- `tests/test_memory_package.py`
- `tests/test_runtime.py`

## Options
### Option A - Execute Additional Elimination Refactor Now
Problem statement:
- Proceed with package elimination/consolidation despite current package implementations already existing.

Pros:
- May reduce long-term namespace overlap sooner.

Cons:
- Creates avoidable churn if project objective was strictly "remove empty stub modules".
- Higher regression risk against currently passing package tests.

Research coverage:
- Literature review: `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md`
- Constraint mapping: branch/scope constraints from project artifact and naming policy in `docs/project/naming_standards.md`
- Stakeholder impact: package consumers and test ownership (`tests/test_*_package.py`)
- Risk enumeration: see matrix below

Risk-to-testability mapping:
- Import/API regression (M/H) -> run `tests/test_rl_package.py`, `tests/test_speculation_package.py`, `tests/test_cort.py`, `tests/test_memory_package.py`, `tests/test_runtime.py`
- Unintended behavior change (M/M) -> add behavior-level assertions before/after refactor in package tests
- Scope creep beyond objective (H/M) -> enforce changed-files scope review against project boundary

### Option B - Minimal-Change Closure with Validation Artifacts (Recommended)
Problem statement:
- Close project as objective-satisfied when no empty init stubs remain and focused package tests pass.

Pros:
- Matches observed repository state with least risk.
- Produces auditable closure evidence without unnecessary code churn.

Cons:
- Defers any broader architectural consolidation to future scoped project(s).

Research coverage:
- Literature review: `docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.project.md`
- Prior-art search: `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md`, `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md`
- Constraint mapping: expected branch/scope from project artifact
- Stakeholder impact: lowest blast radius; documentation and governance artifacts only
- Risk enumeration: see mapping below

Risk-to-testability mapping:
- False closure if hidden stubs remain (L/H) -> verify target package files contain real exports/implementations
- Undetected import breakage (L/H) -> keep focused package tests as required closure artifact
- Evidence drift after closure (M/M) -> preserve artifact references in think + 2think memory entries

### Option C - Hybrid Closure + Immediate Follow-up Consolidation Proposal
Problem statement:
- Mark this project complete for stub elimination objective, but immediately spawn a new project for package ownership consolidation.

Pros:
- Preserves objective integrity while capturing forward work.

Cons:
- Slightly more process overhead than pure closure.

Research coverage:
- Literature review: current package/test artifacts
- Prior-art search: `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md`, `docs/architecture/archive/agents.md`
- Constraint mapping: no code changes in current scope unless objective gap exists
- Stakeholder impact: moderate (adds next-project planning work)
- Risk enumeration: see mapping below

Risk-to-testability mapping:
- Project boundary confusion (M/M) -> require explicit project split and acceptance criteria
- Premature consolidation without design (M/H) -> gate on @3design artifact in new project
- Duplicate effort across projects (M/M) -> ensure prior-art linkage in new project bootstrap

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Objective fit (stub elimination only) | 2 | 5 | 4 |
| Delivery risk (lower churn is better) | 2 | 5 | 4 |
| Evidence quality / auditability | 3 | 5 | 4 |
| Scope discipline | 2 | 5 | 4 |
| Total | 9 | 20 | 16 |

## Recommendation
**Option B - Minimal-change closure with validation artifacts.**

Rationale:
- Target packages already contain real exports/implementations and are not empty init stubs.
- Focused package tests are passing (5/5), providing direct validation of package surface viability.
- Additional refactor in this project would exceed the minimum needed to satisfy the stated objective.

Validation artifacts to retain in closure record:
- Package evidence: `src/rl/__init__.py`, `src/speculation/__init__.py`, `src/cort/__init__.py`, `src/runtime_py/__init__.py`, `src/runtime/__init__.py`, `src/memory/__init__.py`
- Test evidence: `tests/test_rl_package.py`, `tests/test_speculation_package.py`, `tests/test_cort.py`, `tests/test_memory_package.py`, `tests/test_runtime.py`
- Prior-art references: `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md`, `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md`

## Open Questions
1. Should a follow-up project be created to handle broader package ownership consolidation (outside this objective)?

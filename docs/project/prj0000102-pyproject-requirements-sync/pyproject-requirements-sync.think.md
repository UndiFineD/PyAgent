# pyproject-requirements-sync - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## Root Cause Analysis
1. Dual dependency authorities exist today:
	- `pyproject.toml` defines install metadata for build/editable installs.
	- `requirements.txt` defines a separate runtime install path.
2. Version drift is already present in high-impact packages:
	- `openai` is `>=1.60.0` in `pyproject.toml` vs `==2.14.0` in `requirements.txt`.
	- `pydantic` is `>=2.10.0` in `pyproject.toml` vs `==2.12.5` in `requirements.txt`.
	- Additional packages in one manifest are absent from the other.
3. Guardrails are incomplete for dependency governance:
	- `requirements-ci.txt` includes duplicate entries (`pytest-xdist>=3.6` appears twice), which indicates missing structural validation on dependency manifests.
4. Process gap:
	- No canonical, documented source-of-truth policy for how `pyproject.toml`, `requirements.txt`, and CI constraints must stay aligned.

## Constraint Mapping
- Must stay on branch `prj0000102-pyproject-requirements-sync`.
- Must remain docs-only in this @2think stage.
- Must align with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Must produce handoff-ready guidance for @3design without changing runtime/build code.
- Must preserve one-project-one-branch scope from project overview.

## Options
### Option A - Pyproject as Canonical Source + Generated Requirements
Approach:
- Treat `[project.dependencies]` in `pyproject.toml` as canonical runtime source.
- Generate `requirements.txt` from pyproject metadata (tool-based generation in later stages).
- Keep a lightweight policy test that fails on drift between generated output and committed file.

Research coverage:
- Literature review: `pyproject.toml`, `requirements.txt`, `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.project.md`.
- Alternative enumeration: compared against constraints-first and lockfile-first approaches.
- Prior-art search: `docs/project/prj0000076/prj0000076.think.md`, `docs/architecture/archive/8testing-quality.md`.
- Constraint mapping: branch/scope gates in `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.project.md`.
- Stakeholder impact: affects @3design/@4plan/@5test, release operators, local developers.
- Risk enumeration: see risk table below.

SWOT:
- Strength: one source of truth reduces drift class directly.
- Weakness: requires robust generator conventions to avoid surprise diffs.
- Opportunity: aligns with packaging standards where project metadata drives dependencies.
- Threat: tool misconfiguration can silently emit wrong pins if unvalidated.

Security and operability risks (with testability mapping):
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Generator emits incomplete transitive constraints | M | H | Deterministic generation + diff check in CI | Golden-file compare test + CI drift gate |
| Canonical metadata accepts permissive ranges causing runtime drift | M | M | Define pinning policy (critical libs pinned) | Policy test scanning specifiers |
| Local/offline install path diverges from CI install path | M | M | Standardize install commands in docs and CI | Smoke install job using generated requirements |

Workspace evidence:
- `pyproject.toml`
- `requirements.txt`
- `requirements-ci.txt`

### Option B - Requirements as Canonical Source + Mirror Into Pyproject
Approach:
- Keep `requirements.txt` as canonical runtime manifest.
- Update `pyproject.toml` dependencies from `requirements.txt` in a mirrored flow.
- Maintain docs and policy tests validating mirror consistency.

Research coverage:
- Literature review: dependency mismatch from current manifests.
- Alternative enumeration: opposite source-of-truth compared to Option A.
- Prior-art search: policy-driven docs tests and archive testing quality guidance.
- Constraint mapping: build metadata remains required in pyproject even if mirrored.
- Stakeholder impact: Python package maintainers + CI owners.
- Risk enumeration: see below.

SWOT:
- Strength: intuitive for teams used to pip-first workflows.
- Weakness: conflicts with modern packaging center-of-gravity around pyproject metadata.
- Opportunity: faster short-term adoption if existing scripts already parse requirements.
- Threat: wheel/build metadata can lag runtime requirements and break publish/install paths.

Security and operability risks (with testability mapping):
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Published metadata diverges from installed runtime dependencies | M | H | Enforce two-way parity check before release | Packaging metadata parity test |
| Human-edited requirements introduce duplicate/conflicting lines | H | M | Normalize/sort + duplicate detection | Structural lint test for requirements files |
| Build backend dependencies become inconsistent with runtime constraints | M | M | Separate documented policy for build vs runtime deps | Build install smoke test in clean venv |

Workspace evidence:
- `requirements.txt`
- `pyproject.toml`
- `docs/project/ideas/idea000014-pyproject-requirements-sync.md`

### Option C - Constraints-First Baseline With Split Responsibility
Approach:
- Keep top-level dependencies in both pyproject and requirements, but centralize versions in a shared `constraints.txt` (to be designed/implemented later).
- CI and local installs use constraints injection (`-c constraints.txt`).
- Drift checks ensure both manifests reference compatible versions with constraints authority.

Research coverage:
- Literature review: pip guidance on requirements and constraints usage.
- Alternative enumeration: hybrid approach preserving both manifests.
- Prior-art search: quality governance docs emphasizing structure tests.
- Constraint mapping: docs-only stage now; file/model additions later in @3design/@4plan.
- Stakeholder impact: devs, CI maintainers, release engineering.
- Risk enumeration: see below.

SWOT:
- Strength: minimizes immediate disruption by preserving current files.
- Weakness: introduces a third artifact, increasing governance complexity.
- Opportunity: can support org-wide version governance cleanly.
- Threat: partial adoption can create three-way drift instead of two-way drift.

Security and operability risks (with testability mapping):
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Three-manifest model creates silent inconsistency | H | H | Mandatory resolver/parity checks across all manifests | Multi-file consistency test |
| Constraints over-pin security fixes and delay patch uptake | M | M | Security exception workflow + scheduled refresh | Vulnerability scan + stale-pin report |
| Installer command fragmentation across teams | M | M | Standardized documented commands in README/dev docs | Command audit in CI scripts/docs tests |

Workspace evidence:
- `requirements.txt`
- `pyproject.toml`
- `docs/architecture/archive/8testing-quality.md`

## Decision Matrix
| Criterion | Option A: Pyproject Canonical | Option B: Requirements Canonical | Option C: Constraints-First Hybrid |
|---|---|---|---|
| Drift elimination effectiveness | High | Medium | Medium |
| Packaging standards alignment | High | Low | Medium |
| Operational simplicity (long term) | High | Medium | Low |
| Migration effort (short term) | Medium | Medium | High |
| Security governance clarity | High | Medium | Medium |
| Testability of invariants | High | Medium | Medium |

## Recommendation
**Recommend Option A (Pyproject canonical + generated requirements).**

Rationale:
- Best aligns with the current packaging model where project metadata is first-class for build/install.
- Removes the root cause (dual, manually managed authorities) instead of compensating for it.
- Provides cleanest testability model: one canonical manifest + generated artifact + deterministic diff check.

Historical prior-art references:
- `docs/project/prj0000076/prj0000076.think.md` (identified this exact weakness as idea-014 and emphasized governance-backed prevention).
- `docs/architecture/archive/8testing-quality.md` (reinforces structure/CI policy checks as the sustainable control plane).

Risk-to-testability summary for recommendation:
- Generation drift risk -> golden-file parity test in docs/CI workflow.
- Overly permissive specifier risk -> policy check for critical-package pin strategy.
- Install-path inconsistency risk -> clean-venv smoke install with generated requirements.

## Security and Operability Notes
- Security posture improves when dependency authority is singular and auditable.
- Operability improves when onboarding/install docs call one canonical dependency path.
- Residual risk remains around generator reliability and policy exceptions; these must become explicit in @3design interfaces.

## Open Questions
1. Should @3design require exact pins for security-sensitive packages (`openai`, `pydantic`, auth/crypto stack), while allowing ranges for lower-risk libraries?
2. Which generation mechanism should be preferred for this repository context (`pip-compile` workflow vs custom script vs `uv` export path), and what is the rollback if generator output regresses?
3. Is `requirements.txt` intended for production deployment, developer bootstrap, or both? This changes strictness and update cadence.
4. Should optional/heavy dependencies (e.g., ML/vector stack) move into explicit extras during design, or remain in core dependencies for now?
5. What CI gate is authoritative for drift prevention: docs policy test extension, dedicated dependency parity test, or both?

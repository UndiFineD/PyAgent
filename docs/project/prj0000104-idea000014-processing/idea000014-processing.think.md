# idea000014-processing - Options

_Status: HANDED_OFF_
_Analyst: @2think | Updated: 2026-03-30_

## Root Cause Analysis
1. The repository currently keeps two runtime dependency authorities in parallel:
	- `pyproject.toml` (`[project.dependencies]`) for packaging metadata.
	- `requirements.txt` for direct pip installs and CI base inclusion.
2. This dual-authority model has already produced drift risk and maintenance overhead:
	- Prior-art analysis for this same topic in `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md` recorded concrete version divergence and process gaps.
	- `requirements-ci.txt` depends on `requirements.txt`, so any drift propagates into CI behavior.
3. Governance controls exist for branch/scope and project docs, but no dedicated, enforced dependency parity control currently exists in the project.

## Constraint Mapping
- Expected/observed branch must remain `prj0000104-idea000014-processing`.
- @2think work is docs-only and must not modify implementation code.
- Project scope is bounded to project artifacts and @2think memory/log updates.
- Must comply with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Recommendation must include prior-art evidence and explicit risk-to-testability mapping.

## Research Evidence Summary
- Literature review (repo): `pyproject.toml`, `requirements.txt`, `requirements-ci.txt`, `install.ps1`, `.github/workflows/ci.yml`.
- Alternative enumeration: canonical-`pyproject`, canonical-`requirements`, and constraints-first hybrid.
- Prior-art search: `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md`, `docs/project/prj0000076/prj0000076.think.md`, `docs/architecture/archive/8testing-quality.md`.
- Constraint mapping: `docs/project/prj0000104-idea000014-processing/idea000014-processing.project.md`, `.github/agents/governance/shared-governance-checklist.md`.
- Stakeholder impact: @3design/@4plan/@5test, CI maintainers, release maintainers, developers using local bootstrap scripts.
- Risk enumeration: risk matrix included per option with likelihood/impact and validation signals.
- Approved internet references: `https://pypi.org/project/pip-tools/`, `https://docs.python.org/3/installing/index.html`.

## Options
### Option A - `pyproject.toml` canonical, generated `requirements.txt`
Approach summary:
- Treat `[project.dependencies]` in `pyproject.toml` as the single source of truth.
- Generate and commit `requirements.txt` deterministically from pyproject metadata (tooling selected in @3design).
- Add a parity gate that fails when committed requirements output differs from generated output.

Benefits:
- Directly removes the dual-authority root cause.
- Aligns with modern packaging standards and reusable metadata workflows.
- Creates clear, auditable governance: one authoring location and one generated artifact.

Risks and tradeoffs:
- Requires deterministic generation and clear contributor workflow.
- Potential friction when contributors edit `requirements.txt` manually.
- Tool choice lock-in (pip-tools vs uv-export style workflow) needs design decision.

Migration and compatibility impact:
- Moderate migration effort (authoring workflow changes).
- Compatible with current install pattern because `requirements.txt` remains present.
- CI and bootstrap scripts can keep consuming `requirements.txt` with no immediate invocation changes.

Research coverage (task types used):
- Literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

SWOT:
- Strength: highest drift-prevention potential.
- Weakness: requires disciplined generation workflow.
- Opportunity: unify packaging and install governance.
- Threat: generator misconfiguration can cause hidden dependency omission.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Generated output is nondeterministic across environments | M | H | Pin tool version and define generation environment policy | Repeat generation twice in CI and compare outputs |
| Critical package specifiers remain overly permissive | M | M | Define pin/range policy for security-sensitive packages | Policy test that scans disallowed comparator patterns |
| Manual edits to generated file bypass source-of-truth | M | M | Pre-commit/CI parity check | Parity command exits non-zero on diff |

Concrete validation strategy (commands/tests):
```powershell
python -m piptools compile -o requirements.txt pyproject.toml
git diff --exit-code -- requirements.txt
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

### Option B - `requirements.txt` canonical, mirrored into `pyproject.toml`
Approach summary:
- Keep `requirements.txt` as the authoring source.
- Reflect dependency entries into `[project.dependencies]` via scripted sync.
- Add parity checks from requirements to pyproject.

Benefits:
- Familiar for pip-first contributor workflows.
- Short-term lower retraining for teams already editing requirements files.

Risks and tradeoffs:
- Weaker packaging-standards alignment because pyproject becomes derivative.
- Higher chance that package metadata lags runtime edits.
- Mirroring process can be brittle for extras/markers.

Migration and compatibility impact:
- Moderate migration effort.
- High compatibility with existing bootstrap flow.
- Potential future friction with tools expecting pyproject-native dependency management.

Research coverage (task types used):
- Literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

SWOT:
- Strength: low disruption for current requirements-first behavior.
- Weakness: leaves packaging metadata as secondary copy.
- Opportunity: quick short-term operational standardization.
- Threat: release/build metadata drift.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Pyproject metadata drifts from runtime requirements | M | H | Strict mirror policy and parity test | Sync check compares parsed dependency sets |
| Duplicate/conflicting requirement lines accumulate | H | M | Add structural lint check | Duplicate-entry test fails on repeated packages |
| Extras and environment markers are lost in mirroring | M | M | Marker-aware sync mapping | Round-trip parse-and-compare test |

Concrete validation strategy (commands/tests):
```powershell
python scripts/deps/sync_requirements_to_pyproject.py --check
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python -m pytest -q tests/test_zzc_flake8_config.py
```

### Option C - Constraints-first hybrid (`constraints.txt` authority)
Approach summary:
- Keep both `pyproject.toml` and `requirements.txt` as declared surfaces.
- Introduce `constraints.txt` as version authority and enforce installs with `-c constraints.txt`.
- Validate that all manifests stay compatible with constraints.

Benefits:
- Preserves current file roles with minimal immediate behavioral disruption.
- Enables layered environments and controlled rollout by constraints.

Risks and tradeoffs:
- Introduces third dependency artifact and greater governance complexity.
- Higher cognitive load for contributors and reviewers.
- Increased chance of partial adoption and tri-source drift.

Migration and compatibility impact:
- Highest migration complexity of the three options.
- Could be compatible with current install commands after script updates.
- Requires broader contributor guidance and CI updates.

Research coverage (task types used):
- Literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

SWOT:
- Strength: supports advanced layered dependency management.
- Weakness: three-file governance burden.
- Opportunity: explicit environment-specific control plane.
- Threat: inconsistent command adoption across contributors.

Risk-to-testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Three-manifest inconsistency appears silently | H | H | Mandatory tri-parity checks | CI job validates pyproject/requirements/constraints coherence |
| Constraints become stale and block security updates | M | M | Scheduled refresh policy with exception path | Security scan flags vulnerable constrained versions |
| Developers bypass constraints locally | M | M | Standardize install docs and enforce in bootstrap script | Command contract test on install script behavior |

Concrete validation strategy (commands/tests):
```powershell
python -m piptools compile --all-build-deps --all-extras --output-file=constraints.txt --strip-extras pyproject.toml
python scripts/deps/validate_constraints_coherence.py --check
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Root-cause elimination | High | Medium | Medium |
| Long-term maintainability | High | Medium | Low |
| Packaging standards alignment | High | Low | Medium |
| Migration complexity | Medium | Medium | High |
| Blast radius risk | Medium | Medium | High |
| Testability clarity | High | Medium | Medium |

## Recommendation
**Recommend Option A (`pyproject.toml` canonical + generated `requirements.txt`).**

Rationale:
- Option A best addresses the identified root cause (two manually edited authorities).
- Option A keeps compatibility with existing CI/bootstrap paths while improving governance correctness.
- Option A provides the cleanest enforcement model: generation command + parity check + policy tests.

Historical prior-art references:
- `docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md`
- `docs/project/prj0000076/prj0000076.think.md`
- `docs/architecture/archive/8testing-quality.md`

Reject reasons for alternatives:
- Reject Option B: keeps packaging metadata secondary and increases risk of publish/install divergence.
- Reject Option C: adds unnecessary complexity for this project size; risk and governance overhead exceed expected benefit.

## Open Questions For @3design
1. Which generator path is the design baseline for this repository (`pip-tools` compile flow, `uv`-based export, or another deterministic mechanism)?
2. What package specifier policy is required for security-sensitive dependencies (exact pins vs bounded ranges)?
3. Should optional heavy dependencies be moved into extras during this effort, or deferred to a separate project?
4. Which parity gate location is authoritative: pre-commit only, CI only, or both?
5. Which installation path is canonical for contributor docs after migration (`pip install -e .`, `pip-sync`, or both with explicit purpose)?

## Handoff Notes
- Branch gate validated: observed branch equals expected branch `prj0000104-idea000014-processing`.
- Analysis remained docs-only and in project scope.
- Ready for @3design to select interface and workflow details for Option A implementation.

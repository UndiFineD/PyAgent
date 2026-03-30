# idea000014-processing - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-30_

## Selected Option
Option A is selected: `pyproject.toml` is the canonical dependency authority and `requirements.txt` is a deterministic generated artifact.

Rationale:
- Eliminates dual-manual-authority drift at the root cause.
- Preserves compatibility with current install and CI flows that consume `requirements.txt`.
- Enables strict parity enforcement with clear pass/fail behavior.

## Policy And Branch Gates
- Code of conduct policy: satisfied; design language and collaboration expectations align with `docs/project/code_of_conduct.md`.
- Naming policy: satisfied; all newly proposed file names use `snake_case` and stay lowercase per `docs/project/naming_standards.md`.
- Branch validation: expected branch `prj0000104-idea000014-processing` matches observed branch.

## Architecture And Flow Summary
The design introduces a single authoring source and a deterministic generation/parity loop.

```text
Author edits pyproject.toml [project.dependencies]
	-> generator script compiles requirements.txt deterministically
	-> parity checker compares regenerated output to committed requirements.txt
	-> local pre-commit hook (fast fail)
	-> CI parity gate (authoritative fail)
	-> downstream install paths continue using requirements.txt
```

Primary components:
- Dependency source: `pyproject.toml`.
- Generated runtime lock surface: `requirements.txt`.
- Generator interface (scripted CLI): deterministic compile/export command wrapper.
- Parity validator interface (scripted CLI): check-only mode that fails on diff.
- Policy tests: repository tests ensuring docs/workflow integrity and dependency parity behavior.

## Source Of Truth And Data Decisions
1. Canonical dependency data source:
	 - `pyproject.toml` `[project.dependencies]` is the only manually edited runtime dependency list.
2. Derived artifact:
	 - `requirements.txt` is generated and committed; manual edits are disallowed by policy and parity gates.
3. CI include chain:
	 - `requirements-ci.txt` remains layered on `requirements.txt`; no separate authority introduced.
4. Optional dependencies:
	 - Heavy optional groups are deferred to a separate project unless already present as extras.

## Deterministic Generation Strategy
Baseline strategy (default):
- Use `pip-tools` compile flow through a repository-owned wrapper command (e.g., `scripts/deps/generate_requirements.py`) that standardizes:
	- tool version expectations,
	- ordering normalization,
	- newline/encoding behavior,
	- and command flags.

Determinism controls:
- Pin generator toolchain version in development/CI environment inputs.
- Execute generator in a clean, reproducible environment.
- Verify no-op stability by running generation twice in CI and asserting identical output bytes.

## Parity Validation Design
Where enforced:
- Local: pre-commit hook (advisory-fast-fail for contributors).
- CI: required parity job (authoritative merge gate).

How enforced:
- Regenerate `requirements.txt` from `pyproject.toml` in check mode.
- Compare generated output with committed `requirements.txt`.
- Fail with actionable diff and remediation command when mismatch is found.

Authoritative rule:
- CI parity gate is the source of truth for branch protection.
- Pre-commit improves feedback speed but is not the final authority.

## Interfaces And Contracts

### Contract C1: Generate Requirements
- Interface ID: `IFACE-C1`
- Invoker: developer and CI generation job.
- Input contract:
	- `pyproject.toml` exists and parses.
	- Python environment contains approved generator toolchain.
- Output contract:
	- Writes normalized `requirements.txt` deterministically.
	- Exit code `0` on success, non-zero on invalid source or generation error.

### Contract C2: Check Dependency Parity
- Interface ID: `IFACE-C2`
- Invoker: pre-commit hook and CI parity job.
- Input contract:
	- Existing committed `requirements.txt`.
	- Generated check output from current `pyproject.toml`.
- Output contract:
	- Exit code `0` when byte-equivalent parity holds.
	- Exit code non-zero with diff summary and regeneration command when mismatch exists.

### Contract C3: Install Path Compatibility
- Interface ID: `IFACE-C3`
- Invoker: bootstrap scripts and CI install steps.
- Input contract:
	- `requirements.txt` remains present and consumable by pip install flows.
- Output contract:
	- Existing installation commands remain functional without migration breakage.

### Contract C4: Parity Tests
- Interface ID: `IFACE-C4`
- Invoker: test runner (`pytest`) and CI test stage.
- Input contract:
	- Test fixtures include representative dependency declarations.
	- Parity script/check function accessible to tests.
- Output contract:
	- Tests fail if parity workflow regresses, including drift or nondeterminism.

## Failure Modes And Rollback
| Failure mode | Detection | Immediate response | Rollback approach |
|---|---|---|---|
| Generator produces nondeterministic output | Double-run parity in CI shows output delta | Block merge, capture env/tool versions | Revert generator/tooling changes and restore last known deterministic command config |
| Contributor manually edits `requirements.txt` | Pre-commit or CI parity mismatch | Fail with regeneration instructions | Regenerate from canonical source and recommit |
| Toolchain mismatch between local and CI | CI parity failure with local pass | Publish required toolchain version in docs and enforce via env setup | Pin/rollback tool versions to previously passing set |
| Missing or malformed dependency entries in `pyproject.toml` | Generator non-zero exit or test failure | Fail fast and report parse/validation issue | Revert problematic dependency edit and reapply incrementally |
| Install pipeline regression | Install compatibility checks fail in CI | Halt rollout; keep prior requirements artifact in branch history | Revert affected install-script/parity changes while retaining project docs |

Rollback principle:
- Roll back by commit-level reversion of generation/parity changes; do not hand-edit derived artifacts as a recovery mechanism.

## Open Questions From @2think Resolved With Defaults
1. Generator baseline
	 - Default: `pip-tools` compile via repository wrapper command.
2. Security-sensitive specifier policy
	 - Default: allow bounded ranges generally; require explicit pinning for security-critical packages identified by security policy or incident response.
3. Optional heavy dependencies to extras
	 - Default: deferred to a follow-up project unless migration is required to preserve current behavior.
4. Parity gate authority location
	 - Default: both local and CI checks enabled; CI is authoritative.
5. Canonical installation path
	 - Default: support both `pip install -e .` (development/package context) and requirements-based install (runtime/CI), with documented intent per path.

## Acceptance Criteria
| AC ID | Requirement | Verification evidence |
|---|---|---|
| AC-001 | `pyproject.toml` is documented as the only manually edited runtime dependency source. | Design/plan/docs updates reference canonical source unambiguously. |
| AC-002 | `requirements.txt` is generated deterministically from `pyproject.toml`. | Generation command exists and produces byte-stable output across repeated CI runs. |
| AC-003 | Parity mismatch between source and generated artifact fails CI. | CI job exits non-zero on forced mismatch and reports remediation command. |
| AC-004 | Local contributor workflow exposes fast parity feedback. | Pre-commit (or equivalent local check command) is documented and executable. |
| AC-005 | Existing install workflows that consume `requirements.txt` remain operational. | CI install stage and bootstrap command contract checks pass. |
| AC-006 | Nondeterminism and manual-edit failure modes are explicitly guarded. | Tests/checks cover drift, nondeterminism, and malformed source scenarios. |
| AC-007 | Open questions from @2think are resolved or intentionally deferred with defaults. | This design records defaults and deferrals with rationale. |

## Interface-To-Task Traceability For @4plan
| Interface/Contract ID | Planned task IDs for @4plan decomposition | Notes |
|---|---|---|
| IFACE-C1 | T-001, T-002, T-003 | Implement generator wrapper and deterministic command settings |
| IFACE-C2 | T-004, T-005, T-006 | Implement parity checker and CI gate wiring |
| IFACE-C3 | T-007, T-008 | Preserve/update install scripts and compatibility checks |
| IFACE-C4 | T-009, T-010, T-011 | Add parity and nondeterminism tests plus fixtures |
| AC-001..AC-007 | T-001..T-011 | Ensure every AC is mapped in plan task acceptance checks |

## ADR Impact
- No new ADR is required at this stage because this decision applies within project-level dependency workflow boundaries and does not alter system-wide architecture.
- If @4plan expands scope to repository-wide dependency governance policy beyond this project, create/update an ADR under `docs/architecture/adr/` and link it from downstream artifacts.

## Handoff Readiness
Design is implementation-ready for @4plan:
- Selected option is concrete.
- Interfaces and contracts are explicit and testable.
- Acceptance criteria and traceability are present.
- Failure handling and rollback paths are defined.

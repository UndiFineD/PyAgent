# mypy-strict-enforcement - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-04_

## Selected Option
Option B - Progressive blocking allowlist (selected from think artifact).

Rationale:
- Delivers enforceable type-safety improvement without immediate full-repo churn.
- Resolves current dual-config ambiguity (`mypy.ini` permissive vs `[tool.mypy]` strict in `pyproject.toml`) through explicit command-level contract and phased gates.
- Matches repository prior-art for bounded, deterministic enforcement slices.

## Scope
In scope:
- Progressive strict enforcement beginning with an explicit phase-1 `src/core` allowlist.
- CI strategy that starts as warning and upgrades to required after defined stability signals.
- Config governance contract for which mypy configuration is authoritative per command.
- Failure handling and rollback strategy for strict-gate instability.

Out of scope:
- Full-repository strict mode in this project.
- Large refactors outside the phase-scoped allowlist.
- Test strategy definition (owned by @5test), beyond executable acceptance signals and selectors.

## Non-Goals
- Rewriting all legacy modules to satisfy strict typing immediately.
- Removing all gradual-adoption relaxations in one change.
- Blocking delivery for non-allowlist packages during phase 1.

## Architecture
### High-Level Design
The rollout uses two explicit typing lanes:

1. Informational lane (warning-only):
- Runs broad mypy coverage for visibility and trend reporting.
- Never blocks merge while rollout is in warning mode.

2. Strict lane (blocking by phase):
- Runs mypy strict checks only for a curated allowlist.
- Becomes required in CI after warn-phase acceptance criteria are satisfied.

Both lanes must invoke deterministic commands with explicit config source (`--config-file`) so behavior is independent of tool defaults.

### Config Authority Contract
- Baseline contract:
	- Existing permissive baseline in `mypy.ini` remains available for non-blocking/broad contexts.
	- Strict lane is anchored to `pyproject.toml` (`[tool.mypy]`) via explicit command invocation.
- Rule:
	- Any strict-lane command must declare config source and allowlist target in the command itself.
	- Config precedence must be asserted by docs tests before required gating.

### Target Module Allowlist (Phase 1)
Phase-1 strict blocking allowlist (initial):
- `src/core/base/mixins/base_behavior_mixin.py`
- `src/core/base/mixins/host_contract.py`
- `src/core/base/mixins/shim_registry.py`
- `src/core/agent_registry.py`
- `src/core/agent_state_manager.py`

Selection criteria:
- Core orchestration relevance.
- Moderate dependency surface vs. larger feature packages.
- High value for downstream correctness.

### Rollout Phases
Phase 0 - Contract and visibility:
- Define deterministic mypy commands for warning lane and strict-lane allowlist.
- Add docs/test checks for command/config/allowlist contract.

Phase 1 - Warn-first strict lane:
- Execute strict lane on allowlist in CI as non-blocking signal.
- Capture defect counts and trend over consecutive runs.

Phase 2 - Required strict lane (allowlist only):
- Promote strict lane from warning to required after stability threshold is met.
- Keep broad informational lane non-blocking.

Phase 3 - Controlled allowlist expansion:
- Add adjacent `src/core` modules only after acceptance criteria remain green.
- Each expansion is gated by same warn -> required progression.

Phase 4 - Policy convergence review:
- Assess path to reduce config divergence and expand strict coverage beyond initial scope.

### CI Gating Strategy (Warn -> Required)
- Warn mode:
	- Strict lane runs on pull_request and push, reports violations, does not fail checks.
- Promotion gate:
	- Promote strict lane to required after N consecutive green strict-lane runs (default N=5) and no unresolved config-contract failures.
- Required mode:
	- Strict lane is a required status check for target branch PRs.
- Broad lane:
	- Remains warning-only until separately promoted by future project scope.

### Failure Handling and Rollback Strategy
Failure classes:
- F1: Config contract failure (wrong config picked, allowlist drift).
- F2: Strict-lane regression in allowlist module(s).
- F3: CI instability/noise (intermittent non-determinism).

Disposition:
- F1: Immediate rollback to warning mode and restore last known-good config contract.
- F2: Keep required gate active, hotfix target module typing issues, allow temporary module-level scoped exception only with explicit tracking issue and expiry.
- F3: Temporarily downgrade strict lane to warning mode with incident note, then re-promote after N new green runs.

Rollback rules:
- Never reintroduce blanket `ignore_errors = true` for strict-lane modules.
- Rollback is lane-level (required -> warning), not policy abandonment.
- Every rollback must include owner, reason, and re-promotion condition.

## Interfaces & Contracts
| Interface ID | Contract | Input | Output | Owner (next) |
|---|---|---|---|---|
| IFACE-MYPY-001 | Strict lane command contract | config source, phase allowlist | deterministic mypy exit status + log | @4plan/@6code |
| IFACE-MYPY-002 | Warning lane command contract | broad target set | non-blocking diagnostics artifact | @4plan/@7exec |
| IFACE-MYPY-003 | Allowlist registry contract | phase list of module paths | immutable phase snapshot + drift failure on unreviewed removal | @4plan/@5test |
| IFACE-MYPY-004 | Promotion gate contract | consecutive green runs + incident state | lane mode transition decision | @4plan/@7exec |
| IFACE-MYPY-005 | Rollback contract | failure class + evidence | required->warning transition + re-entry criteria | @4plan/@7exec |
| IFACE-MYPY-006 | Config precedence assertion contract | strict command definition | pass/fail signal proving expected config authority | @5test/@7exec |

## Planned Implementation Tasks (for @4plan decomposition)
| Task ID | Description | Primary artifacts |
|---|---|---|
| TSK-MYPY-01 | Define strict/warn command surfaces and canonical invocation docs | docs/project/prj0000127-mypy-strict-enforcement/*, CI workflow refs |
| TSK-MYPY-02 | Implement phase-1 allowlist contract and drift protection checks | docs/project/prj0000127-mypy-strict-enforcement/*, tests/docs/* |
| TSK-MYPY-03 | Add warn-mode strict lane in CI with emitted diagnostics | .github/workflows/ci.yml |
| TSK-MYPY-04 | Add promotion criteria tracking and required-gate toggle process | docs/project/prj0000127-mypy-strict-enforcement/* |
| TSK-MYPY-05 | Implement rollback operational runbook and failure taxonomy checks | docs/project/prj0000127-mypy-strict-enforcement/* |
| TSK-MYPY-06 | Add config precedence assertions for strict command behavior | tests/docs/* |

## Interface-to-Task Traceability
| Interface ID | Task IDs | Trace note |
|---|---|---|
| IFACE-MYPY-001 | TSK-MYPY-01, TSK-MYPY-03 | Defines and enforces strict blocking command behavior |
| IFACE-MYPY-002 | TSK-MYPY-01, TSK-MYPY-03 | Preserves non-blocking visibility lane |
| IFACE-MYPY-003 | TSK-MYPY-02 | Prevents silent allowlist erosion |
| IFACE-MYPY-004 | TSK-MYPY-04 | Governs warn->required promotion decision |
| IFACE-MYPY-005 | TSK-MYPY-05 | Governs deterministic rollback and re-entry |
| IFACE-MYPY-006 | TSK-MYPY-06 | Verifies config authority behavior in CI |

## Acceptance Criteria
| AC ID | Acceptance criterion | Executable signal |
|---|---|---|
| AC-MYPY-001 | Design defines explicit scope and non-goals for phased strict enforcement | Presence of Scope and Non-Goals sections in design artifact |
| AC-MYPY-002 | Phase-1 strict allowlist names concrete existing `src/core` modules | Allowlist entries resolve to real files in repository |
| AC-MYPY-003 | Warn->required CI promotion gate is explicit and thresholded | CI docs/plan include N-consecutive-green promotion rule |
| AC-MYPY-004 | Failure taxonomy and rollback rules are documented and bounded | Rollback section includes F1/F2/F3 and re-promotion conditions |
| AC-MYPY-005 | Interfaces are mapped to planned implementation tasks | Interface-to-task traceability table exists and is complete |
| AC-MYPY-006 | Project milestone M2 is updated to DONE after design completion | `mypy-strict-enforcement.project.md` Milestones table shows M2 DONE |
| AC-MYPY-007 | Docs workflow policy validation passes after artifact updates | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` passes |

## Non-Functional Requirements
- Performance:
	- Strict lane runtime overhead must remain bounded to CI practical limits by using phase allowlists.
- Security:
	- No loosening of repository security posture; type checks must not bypass required security checks.
- Testability:
	- Every phase transition is tied to deterministic pass/fail selectors and logged evidence.
- Operability:
	- Lane mode (warn/required) and rollback state must be observable from CI and project docs.

## Open Questions
1. Should phase-1 strict lane run on both pull_request and push, or pull_request only during initial warn mode?
2. Should allowlist expansion be constrained to one package per promotion cycle to reduce rollback blast radius?
3. Is a separate CI job preferred for strict lane visibility, or should strict checks be folded into existing quick job structure?

## Handoff
- Target agent: @4plan
- Design readiness: actionable
- Required downstream use:
	- Convert Task IDs into concrete implementation/test tasks with owners.
	- Preserve AC IDs and executable signals as plan verification anchors.


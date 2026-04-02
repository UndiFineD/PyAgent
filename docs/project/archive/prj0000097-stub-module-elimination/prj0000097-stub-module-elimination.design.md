# prj0000097-stub-module-elimination - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-29_

## Selected Option
Option C from @2think, narrowed to Slice 1: eliminate placeholder behavior in `src/rl` and
`src/speculation` without touching `runtime`, `memory`, or `cort`.

Rationale:
- These two modules are still placeholder-grade (`validate()`-only shape).
- They have tiny, isolated import usage in tests, so migration blast radius is low.
- This slice creates real behavior and real assertions, enabling clean handoff to @4plan,
	@5test, and @6code.

## Architecture
### Slice Boundary
In scope:
- `src/rl/__init__.py`
- `src/speculation/__init__.py`
- tests that currently validate only importability of those modules

Out of scope:
- `src/runtime*`, `src/memory*`, `src/cort*`
- any broad package consolidation or cross-domain refactor

### High-Level Flow
1. Keep module paths stable (`import rl`, `import speculation`) for this slice.
2. Add one concrete deterministic API per module.
3. Keep `validate()` temporarily as deprecated compatibility shim.
4. Replace import-smoke tests with behavior and deprecation tests.
5. Add import-scan guard that fails on new external usage before removal window closes.

## Interfaces & Contracts
### IFC-RL-001: RL Deterministic Return Contract
Location:
- `src/rl/__init__.py`

Public API:
```python
def discounted_return(rewards: list[float], gamma: float = 0.99) -> float: ...
```

Contract:
- Deterministic pure function.
- Computes discounted sum: $\sum_{t=0}^{n-1} rewards[t] * gamma^t$.
- Empty `rewards` returns `0.0`.
- `gamma` must satisfy `0.0 <= gamma <= 1.0`; otherwise raise `ValueError`.
- Any non-finite reward (`NaN`, `inf`, `-inf`) raises `ValueError`.

### IFC-RL-002: RL Legacy Shim Contract
Location:
- `src/rl/__init__.py`

Public API:
```python
def validate() -> bool: ...
```

Contract:
- Retained only for compatibility in Slice 1.
- Emits `DeprecationWarning` with actionable migration message:
	`Use rl.discounted_return(); validate() will be removed in Slice 2.`
- Returns `True` to preserve basic call compatibility.

### IFC-SPC-001: Speculation Candidate Selection Contract
Location:
- `src/speculation/__init__.py`

Public API:
```python
def select_candidate(scores: dict[str, float], threshold: float = 0.0) -> str | None: ...
```

Contract:
- Deterministic pure function.
- Filters keys where `score >= threshold`.
- Returns candidate with highest score.
- Tie-breaker is lexicographic ascending key for deterministic output.
- Returns `None` when no candidate meets threshold or when `scores` is empty.
- Any non-finite score raises `ValueError`.

### IFC-SPC-002: Speculation Legacy Shim Contract
Location:
- `src/speculation/__init__.py`

Public API:
```python
def validate() -> bool: ...
```

Contract:
- Retained only for compatibility in Slice 1.
- Emits `DeprecationWarning` with actionable migration message:
	`Use speculation.select_candidate(); validate() will be removed in Slice 2.`
- Returns `True` to preserve basic call compatibility.

### Migration and Deprecation Stance
Slice 1:
- Keep module names and import paths stable.
- Replace placeholder behavior with deterministic functional behavior.
- Mark `validate()` in both modules as deprecated.

Slice 2 (follow-up project):
- Remove `validate()` from both modules.
- Keep concrete APIs, or remove entire modules only if ownership is reassigned and all
	imports are migrated with passing guard tests.

Deprecation policy:
- At least one release cycle with warning visibility in tests.
- No silent behavior change in legacy shim.

### Interface-to-Task Traceability
| Interface ID | Planned Task ID (@4plan) | Implementation Owner | Test Owner |
|---|---|---|---|
| IFC-RL-001 | PLN-001-rl-discounted-return | @6code | @5test |
| IFC-RL-002 | PLN-002-rl-validate-deprecation | @6code | @5test |
| IFC-SPC-001 | PLN-003-speculation-select-candidate | @6code | @5test |
| IFC-SPC-002 | PLN-004-speculation-validate-deprecation | @6code | @5test |
| Import guard policy | PLN-005-rl-speculation-import-scan | @6code | @5test |

### Exact Test Targets and Failure Modes
Planned test targets for Slice 1:
- `tests/rl/test_discounted_return.py`
- `tests/rl/test_rl_deprecation.py`
- `tests/speculation/test_select_candidate.py`
- `tests/speculation/test_speculation_deprecation.py`
- `tests/guards/test_rl_speculation_import_scope.py`

Failure modes that must be explicitly asserted:
- Invalid `gamma` (<0 or >1) does not raise `ValueError`.
- Non-finite rewards/scores are accepted.
- Tie-breaking in `select_candidate()` is non-deterministic.
- `validate()` does not emit `DeprecationWarning`.
- New imports of `rl` or `speculation` appear outside approved compatibility tests.

## Non-Functional Requirements
- Performance:
	- `discounted_return()` and `select_candidate()` are O(n) in input size.
	- No I/O, no network calls, no global state.
- Security:
	- Strict input validation for numeric finiteness and parameter bounds.
	- No dynamic import/eval behavior.
- Testability:
	- Functions are pure and deterministic.
	- Warning behavior is assertable through `pytest.warns`.
	- Import scope guard is assertable through repository scan test.

## Open Questions
- None blocking Slice 1.
- Follow-up decision for Slice 2:
	- retain `rl` and `speculation` as stable thin utility modules, or
	- migrate functions into a consolidated owner package and remove top-level modules.

## Acceptance Criteria
| AC ID | Requirement | Verify ID | Failure Mode |
|---|---|---|---|
| AC-001 | RL discounted return is correct, including empty input. | V-RL-RET | Wrong value or wrong empty behavior. |
| AC-002 | RL rejects bad `gamma` and non-finite rewards. | V-RL-RET | Invalid input passes or wrong exception type. |
| AC-003 | Speculation threshold and top-key selection are correct. | V-SPC-SEL | Wrong candidate/threshold. |
| AC-004 | Speculation tie-break is lexicographic and stable. | V-SPC-SEL | Tie result changes across runs. |
| AC-005 | Legacy `validate()` shims warn and stay callable. | V-RL-DEP, V-SPC-DEP | Warning missing or call breaks. |
| AC-006 | Import guard blocks new `rl`/`speculation` imports. | V-IMP-GRD | Unauthorized imports pass. |
| AC-007 | Import-smoke tests are replaced by behavior/deprecation tests. | V-TST-INV | Import-smoke remains primary. |
| AC-008 | Slice 1 does not edit `runtime`/`memory`/`cort` impl files. | V-DIFF-SCP | Out-of-scope files changed. |

### Verification ID Map
| Verify ID | Exact Test Target |
|---|---|
| V-RL-RET | `tests/rl/test_discounted_return.py` |
| V-RL-DEP | `tests/rl/test_rl_deprecation.py` |
| V-SPC-SEL | `tests/speculation/test_select_candidate.py` |
| V-SPC-DEP | `tests/speculation/test_speculation_deprecation.py` |
| V-IMP-GRD | `tests/guards/test_rl_speculation_import_scope.py` |
| V-TST-INV | `tests/` inventory diff replacing old import-smoke tests |
| V-DIFF-SCP | Diff scope review in @6code/@8ql |

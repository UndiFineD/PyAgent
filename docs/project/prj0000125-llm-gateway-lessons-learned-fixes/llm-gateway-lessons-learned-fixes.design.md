# llm-gateway-lessons-learned-fixes — Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-04_

## Branch Gate

| Check | Result |
|---|---|
| Expected branch | `prj0000125-llm-gateway-lessons-learned-fixes` |
| Observed branch (`git branch --show-current`) | `prj0000125-llm-gateway-lessons-learned-fixes` |
| Gate | **PASS** |

## Input Artifacts

| File | Purpose |
|---|---|
| `docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.think.md` | Lessons baseline — 5 themes, 4 waves, priority matrix |
| `docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.project.md` | Scope boundary and branch plan |
| `src/core/gateway/gateway_core.py` | Current `GatewayCore` implementation |
| `tests/core/gateway/test_gateway_core_orchestration.py` | Existing orchestration tests with non-deterministic assertion |
| `tests/core/gateway/test_gateway_core.py` | `validate()` quality-contract test |
| `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md` | Existing ADR for gateway |
| `docs/project/naming_standards.md` | Naming precedence rules |
| `src/core/gateway/__init__.py` | Package exports |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | Source project milestones (drift confirmed) |

## Architecture Decision Summary

Four targeted remediation waves against the gateway slice delivered in prj0000124 (PR #287):

| Wave | Label | Priority | Type |
|---|---|---|---|
| A | Runtime Correctness | CRITICAL | Source code fix |
| B | Test Determinism | HIGH | Test fix |
| C | Docs/Governance Truth Sync | HIGH | Artifact update |
| D | Naming Convention Decision | MEDIUM | Design record only |

No topology changes. No rename campaigns. Scope limited to fail-closed contract completion, deterministic test evidence, and state truth alignment.

---

## Wave A — Runtime Correctness Design

### A1 Budget-Denied Fail-Closed Interface

**Current gap:** `GatewayCore.handle()` calls `self._budget_manager.reserve(envelope)` but never checks whether the reservation was approved or denied. If the budget service returns `{"allowed": False}` the gateway silently continues to provider execution — a policy bypass.

**Required behavior:**

After `reservation = self._budget_manager.reserve(envelope)`, the gateway must evaluate the result:

```python
if not reservation.get("allowed", True):
    result = self._build_budget_denied_result(envelope, reservation)
    # emit telemetry protected by degraded-telemetry guard (see A3)
    return result
```

**Return envelope for budget-denied path:**

```python
{
    "request_id": envelope.get("request_id"),
    "correlation_id": envelope.get("correlation_id"),
    "status": "denied",
    "decision": {"allow": False, "decision": "deny", "reason": "budget_denied"},
    "route": None,
    "provider_response": None,
    "error": {"error_code": "budget_denied", "category": "budget"},
    "budget": reservation,           # the denied reservation dict
    "cache": {"hit": False},
    "tool_audit": [],
    "telemetry": {"degraded": False},
}
```

**AC-A1 (ID: AC-A1):** `pytest tests/core/gateway/test_gateway_core_orchestration.py -k "budget_denied"`
— test must confirm `provider_runtime` was not called when budget `allowed=False`.

---

### A2 Provider Exception Fail-Closed Interface

**Current gap:** `await self._provider_runtime.execute(route, envelope)` is unguarded. Any uncaught exception propagates to the caller and leaves the budget reservation dangling (neither committed nor failed).

**Required behavior:**

Wrap provider call in a try/except block:

```python
try:
    response = await self._provider_runtime.execute(route, envelope)
except Exception as exc:
    budget_commit = self._budget_manager.commit_failure(
        reservation,
        {"error_code": "provider_exception", "category": "provider"},
    )
    result = self._build_provider_exception_result(envelope, route, budget_commit, str(exc))
    # emit telemetry protected by degraded-telemetry guard (see A3)
    return result
```

**Budget commit state on provider exception:** `failed` — `commit_failure()` must always be called; never `commit_success()` and never omission.

**Return envelope for provider-exception path:**

```python
{
    "request_id": envelope.get("request_id"),
    "correlation_id": envelope.get("correlation_id"),
    "status": "failed",
    "decision": pre_decision,    # pre-policy passed
    "route": route,
    "provider_response": None,
    "error": {"error_code": "provider_exception", "category": "provider", "detail": str(exc)},
    "budget": budget_commit,     # status == "failed"
    "cache": {"hit": False},
    "tool_audit": [],
    "telemetry": {"degraded": False},
}
```

**AC-A2 (ID: AC-A2):** `pytest tests/core/gateway/test_gateway_core_orchestration.py -k "provider_exception"`
— test must confirm `result["status"] == "failed"`, `result["budget"]["status"] == "failed"`,
and the exception does not propagate to the test caller.

---

### A3 Degraded Telemetry Handling

**Current gap:** `self._telemetry_emitter.emit_result(result)` is called bare. If emit raises, the exception propagates to the caller — the user never receives the response.

**Required behavior:**

Wrap `emit_result` (at the final return point) in a try/except:

```python
try:
    self._telemetry_emitter.emit_result(result)
except Exception:
    result = dict(result)           # shallow copy to avoid in-place mutation
    result["telemetry"] = {"degraded": True}
# return result regardless
return result
```

The gateway MUST return `result` to the caller regardless of telemetry outcome.

**Metadata contract:** When `emit_result` raises, `result["telemetry"]["degraded"]` must be `True`. All other result fields remain unchanged.

Note: `emit_request_start` and `emit_decision` failures earlier in the flow should also be guarded; however, since they precede the return point and do not affect the response, wrapping them in bare try/except (no re-raise) is acceptable. The critical guard is on the final `emit_result`.

**AC-A3 (ID: AC-A3):** `pytest tests/core/gateway/test_gateway_core_orchestration.py -k "degraded_telemetry"`
— test must confirm result is returned when `emit_result` raises, and `result["telemetry"]["degraded"] is True`.

---

## Wave B — Test Determinism Design

### B1 Shared Chronological Event Log Pattern

**Non-determinism root cause** in `test_fail_closed_budget_reserve_occurs_before_provider_execute`:

```python
# CURRENT (BROKEN): concatenation of two separate per-stub lists
call_order = budget_manager.calls + provider_runtime.calls
assert call_order.index("budget_reserve") < call_order.index("provider_execute")
```

This assertion is structurally trivially-true. `budget_manager.calls` always appears before `provider_runtime.calls` in the concatenated list regardless of actual execution order. An implementation that called `provider_runtime.execute()` before `budget_manager.reserve()` would still pass the test.

**Design: inject a single `event_log: list[str]` into all stubs.**

All stub `__init__` methods accept `event_log: list[str]` and append to that shared list.

**Fixture pattern (canonical):**

```python
@pytest.fixture
def event_log() -> list[str]:
    """Shared chronological event log for cross-stub ordering assertions."""
    return []


@pytest.fixture
def make_gateway(event_log: list[str]):
    """Factory fixture that wires all stubs to the shared event_log."""
    def _factory(
        pre_allow: bool = True,
        post_allow: bool = True,
        budget_allowed: bool = True,
    ) -> GatewayCore:
        return GatewayCore(
            policy_engine=_PolicyEngineStub(event_log, pre_allow, post_allow),
            router=_RouterStub(),
            provider_runtime=_ProviderRuntimeStub(event_log),
            budget_manager=_BudgetManagerStub(event_log, budget_allowed),
            semantic_cache=_SemanticCacheStub(event_log),
            fallback_manager=_FallbackManagerStub(),
            telemetry_emitter=_TelemetryEmitterStub(event_log),
            tool_skill_catcher=_ToolCatcherStub(event_log),
        )
    return _factory
```

**Stub constructor pattern:**

```python
class _BudgetManagerStub:
    def __init__(self, event_log: list[str], allowed: bool = True) -> None:
        self._event_log = event_log
        self._allowed = allowed

    def reserve(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self._event_log.append("budget_reserve")
        return {"reservation_id": "rsv-1", "allowed": self._allowed}

    def commit_success(self, reservation, usage) -> dict[str, Any]:
        self._event_log.append("budget_commit_success")
        return {"status": "committed", "reservation_id": reservation["reservation_id"]}

    def commit_failure(self, reservation, error) -> dict[str, Any]:
        self._event_log.append("budget_commit_failure")
        return {"status": "failed", "reservation_id": reservation["reservation_id"]}
```

**Canonical ordering assertion (post-refactor):**

```python
@pytest.mark.asyncio
async def test_fail_closed_budget_reserve_occurs_before_provider_execute(
    gateway_envelope: dict[str, Any],
    event_log: list[str],
    make_gateway,
) -> None:
    gateway = make_gateway()
    await gateway.handle(gateway_envelope)

    assert "budget_reserve" in event_log
    assert "provider_execute" in event_log
    # Chronological guarantee: same list, real-time append order.
    assert event_log.index("budget_reserve") < event_log.index("provider_execute")
```

**Guarantee:** All stubs write to `event_log` synchronously within the single in-process async call. Index position reflects true execution order.

**AC-B1 (ID: AC-B1):** `pytest tests/core/gateway/test_gateway_core_orchestration.py -v`
— no test uses `stub_a.calls + stub_b.calls` for ordering assertions; all ordering assertions use the shared `event_log` fixture.

---

### B2 Closure Selector Discipline

Mandatory pytest selectors before @4plan handoff:

```powershell
# Quality contract
pytest tests/core/gateway/test_gateway_core.py -v

# Orchestration contract (all waves)
pytest tests/core/gateway/test_gateway_core_orchestration.py -v

# Docs policy (must not regress)
pytest tests/docs/test_agent_workflow_policy_docs.py -q
```

**AC-B2 (ID: AC-B2):** All three selectors pass with zero failures.

---

## Wave C — Docs Truth Sync Design

### C1 prj0000124 Artifact Sync Targets

`docs/project/prj0000124-llm-gateway/llm-gateway.project.md` shows all milestones as `NOT_STARTED` and lane as "Discovery" — inconsistent with PR #287 merge state.

| File | Field | Current (stale) | Correct (final) |
|---|---|---|---|
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M1 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M2 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M3 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M4 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M5 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M6 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M7 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | M8 Status | `NOT_STARTED` | `DONE` |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | Lane/Status sentence | Discovery | Done — merged via PR #287; remediation tracked in prj0000125 |

**AC-C1 (ID: AC-C1):** `rg "NOT_STARTED" docs/project/prj0000124-llm-gateway/` returns zero matches.

---

### C2 ADR 0009 Update Strategy

File: `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md`

Action: Append a new section `## Part 2 — prj0000125 Remediation` with three subsections:

1. **Released implementation (prj0000124):** Policy-first orchestration, budget reserve/commit, semantic cache lookup/write, fallback manager (stub), tool catcher, telemetry emitter — delivered in green slice and merged via PR #287.
2. **Remediation scope (prj0000125):** Waves A–D — runtime-only contract completion (budget-denied path, provider-exception handling, degraded-telemetry guard), test determinism (shared event log), docs truth sync (prj0000124 milestones), naming convention decision. No topology change.
3. **Naming convention decision (Wave D):** `gateway_core.py` — snake_case, compliant with `docs/project/naming_standards.md`. No rename warranted. Decision closed.

Status of ADR 0009 remains **Accepted**.

**AC-C2 (ID: AC-C2):** `python scripts/architecture_governance.py validate` exits with zero blocking errors.

---

## Wave D — Naming Convention Decision

### D1 gateway_core.py Naming Verdict

**Evidence from `docs/project/naming_standards.md` (verbatim):**

> **Modules/Files**
> Standard: Strict `snake_case`.
> Requirement: Filenames must be lowercase with underscores separating words (e.g., `coder_agent.py`, `identity_mixin.py`).
> Rationale: Enforced workspace-wide to align with PEP 8 and ensure cross-platform import stability.

**Conflict acknowledged:** The project `copilot-instructions.md` states "Always use `PascalCase` for filenames."

**Precedence rule:** `docs/project/naming_standards.md` is the explicit, titled, versioned repository naming standard. It is authoritative. The copilot-instructions file provides general code-generation defaults and does not supersede an explicit naming standard document.

**Ruling:** `gateway_core.py` (snake_case) is **COMPLIANT** with `docs/project/naming_standards.md`.

**Rename verdict:** **NO RENAME WARRANTED.**
- No runtime import break evidence.
- No filesystem case-sensitivity issue detected.
- Current import in `src/core/gateway/__init__.py`: `from .gateway_core import GatewayCore` — works on all platforms.
- Renaming would cause `__init__.py` import break requiring coordinated change with no functional benefit.

**Decision: CLOSED.**

**AC-D1 (ID: AC-D1):** `rg "from .gateway_core import" src/core/gateway/` returns exactly one match (`__init__.py`). No import break. Decision recorded.

---

## Interface Contract

Public surface of `GatewayCore` after all waves (no signature changes — only `handle()` internals):

```python
class GatewayCore:
    """Coordinate policy, budget, provider, and side-effect sequencing."""

    def __init__(
        self,
        *,
        policy_engine: Any,
        router: Any,
        provider_runtime: Any,
        budget_manager: Any,
        semantic_cache: Any,
        fallback_manager: Any,
        telemetry_emitter: Any,
        tool_skill_catcher: Any,
    ) -> None: ...  # constructor signature: UNCHANGED

    async def handle(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """Execute fail-closed request orchestration.

        Lifecycle (post-remediation, steps in execution order):
          1. emit_request_start(envelope)                [always; emit errors swallowed]
          2. evaluate_pre_request -> if !allow: denied   [policy fail-closed]
          3. budget_manager.reserve                      [NEW A1: if !allowed: budget_denied]
          4. semantic_cache.lookup
          5. router.route
          6. emit_decision
          7. provider_runtime.execute                    [NEW A2: exception -> failed + commit_failure]
          8. evaluate_post_response -> if !allow: denied + commit_failure
          9. commit_success + cache_write + tool_audit
         10. emit_result                                 [NEW A3: exception -> degraded=True, still return]
         11. return result

        Returns dict with guaranteed keys:
          status: Literal['success', 'denied', 'failed']
          decision: dict
          route: dict | None
          provider_response: dict | None
          error: dict | None
          budget: dict
          cache: dict
          tool_audit: list[dict]
          telemetry: {'degraded': bool}
        """
```

**Result envelope `status` contract:**

| `status` | Condition |
|---|---|
| `"success"` | Pre-policy allow, budget allowed, provider succeeded, post-policy allow |
| `"denied"` | Pre-policy deny, budget denied (NEW: A1), or post-policy deny |
| `"failed"` | Provider raised exception (NEW: A2) |

---

## Acceptance Criteria

| ID | Wave | Criterion | Validation command |
|---|---|---|---|
| AC-A1 | A | budget_denied path blocks provider execution | `pytest tests/core/gateway/test_gateway_core_orchestration.py -k budget_denied` |
| AC-A2 | A | provider_exception returns status=failed, budget.status=failed, no propagation | `pytest tests/core/gateway/test_gateway_core_orchestration.py -k provider_exception` |
| AC-A3 | A | degraded telemetry: response returned, telemetry.degraded=True | `pytest tests/core/gateway/test_gateway_core_orchestration.py -k degraded_telemetry` |
| AC-B1 | B | Ordering assertions use shared event_log fixture exclusively | `pytest tests/core/gateway/test_gateway_core_orchestration.py -v` |
| AC-B2 | B | All three mandatory selectors pass zero failures | `pytest tests/core/gateway/ tests/docs/test_agent_workflow_policy_docs.py -q` |
| AC-C1 | C | prj0000124 milestones all show DONE | `rg NOT_STARTED docs/project/prj0000124-llm-gateway/` -> zero matches |
| AC-C2 | C | ADR 0009 passes architecture governance | `python scripts/architecture_governance.py validate` -> no blocking errors |
| AC-D1 | D | gateway_core.py naming decision recorded; no rename | `rg from .gateway_core import src/core/gateway/` -> one match in __init__.py |

---

## ADR Impact

**ADR 0009** (`docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md`):
- Status: remains **Accepted** — no topology revision.
- Required amendment: add `## Part 2 - prj0000125 Remediation` section.
- No new ADR required: remediation is a contract-completion pass on the accepted architecture, not a new architectural decision.

---

## Risks and Mitigations

| Wave | Risk | Mitigation |
|---|---|---|
| A1 | `reserve()` contract varies — `allowed` key may be absent | `reservation.get('allowed', True)` — absent key defaults to allow (backward compat safe). |
| A2 | Narrow exception types (asyncio.CancelledError etc.) should not be swallowed | Catch `Exception` only; let `BaseException` subclasses not derived from `Exception` propagate. |
| A3 | Shallow-copy mutation risk if error recovery mutates result in-place | Use `result = dict(result)` before setting `result['telemetry']`. |
| B1 | Existing `self.calls` lists used in non-ordering assertions may break if removed | Retain `self.calls` on stubs for non-ordering checks; supplement with `_event_log` for ordering. |
| C1 | kanban.json / data/projects.json lane for prj0000124 may also be stale | Run `python scripts/project_registry_governance.py validate` after C1 updates. |
| D1 | Future agents re-introduce rename pressure from copilot-instructions.md | Naming verdict recorded in ADR 0009 Part 2 and this design doc as a closed decision. |

---

## Out of Scope

Explicitly deferred:

1. Broad gateway redesign: cache architecture, fallback topology expansion, memory-system refactor.
2. Repo-wide markdown lint / legacy cleanup unrelated to prj0000124/prj0000125 truth sync.
3. Any filename/module rename campaign beyond the D1 recorded decision.
4. Service-mode gateway (Phase 3 per ADR 0009).
5. Rust hot-path acceleration (Phase 3 per ADR 0009).
6. Legacy project (prj0000005-prj0000041) doc upgrades.

---

## Handoff to @4plan

**Wave ordering and dependencies:**

```
Wave A (runtime fixes)  ->  Wave B (test refactor)  ->  Wave C (docs sync)  ->  Wave D (closed)
```

- **Wave A** must be implemented first: B1 test additions require A1/A2/A3 behaviours to exist.
- **Wave B** test changes depend on Wave A implementation being in place.
- **Wave C** doc updates are independent of A and B but should follow implementation to confirm final state.
- **Wave D** is a design-record-only wave — resolved at design phase. @4plan should mark it closed with no implementation tasks.

**Files for @4plan implementation task list:**

| File | Wave | Action |
|---|---|---|
| `src/core/gateway/gateway_core.py` | A1, A2, A3 | Modify `handle()` — budget-denied check, provider-exception guard, emit_result guard |
| `tests/core/gateway/test_gateway_core_orchestration.py` | B1 | Refactor stubs to accept event_log; add 3 new test functions for A1/A2/A3; fix ordering test |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | C1 | Update all milestones to DONE; update status/lane |
| `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md` | C2 | Append Part 2 section |

**Target agent:** @4plan
**Design status at handoff:** DONE
**Open questions at handoff:** None blocking implementation.

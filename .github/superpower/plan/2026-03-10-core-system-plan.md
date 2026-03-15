# PyAgent Core System Implementation Plan

Date: 2026-03-10

Goal: Implement a minimal, test-driven Core subsystem for PyAgent (runtime, task queue, agent registry, memory, observability) with self-validation, CI gates, and scaffolding to guide future core development.

Architecture: Core modules live under `src/core/<component>/`. Each core exposes a typed public API and a `validate()` self-check. A meta-test (`tests/test_core_quality.py`) enforces quality gates in CI.

Tech stack: Python 3.11+, pytest, ruff (linter), mypy (type-checker), GitHub Actions for CI.

---

Overview & constraints
- Follow TDD strictly: write failing test → run test → implement minimal code → run test until passing.
- This plan is a blueprint only. Implementation (file creation / edits) requires explicit handoff to the executor agent.
- Files already present in workspace that are relevant: `tests/test_core_quality.py`, `src/core/scaffold/__init__.py`.

---

Top-level checklist
- Read core design and gather context (`.github/superpower/brainstorm/design/core_design.md`).
- Present an executable, TDD-first implementation plan to the user.
- User approved the plan (2026-03-10).
- Save this plan as `.github/superpower/plan/2026-03-10-core-system-plan.md`.
- [blocked] Implement core modules (Runtime, TaskQueue, AgentRegistry, MemoryStore, Observability) — blocked until user authorizes execution.
- [blocked] Write per-core tests and iterate to passing — blocked until implementation step is executed.
- [blocked] Add CI workflow `.github/workflows/core-quality.yml` enforcing ruff/mypy/pytest — blocked.
- [blocked] Create docs `docs/CORE_DESIGN_GUIDE.md` and `docs/TEST_QUALITY.md` — blocked.
- [blocked] Run full test suite and verify meta-tests pass — blocked.
- [blocked] Open PR (branch: `feature/async-runtime`) with the implemented changes — blocked.

---

Detailed TDD tasks (one action per test/implementation step)

TASK A — Runtime
- A.1: Write failing test `tests/test_core_runtime.py` that imports `src.core.runtime` and requires `Runtime` and `validate()`.
- A.2: Implement minimal `src/core/runtime.py`:
  - `Runtime` dataclass with an `async def start()` no-op returning after `await asyncio.sleep(0)`.
  - `validate()` checks that `Runtime().start` is callable and import is side-effect free.

TASK B — TaskQueue
- B.1: Write failing test `tests/test_core_task_queue.py` that imports `src.core.task_queue` and requires `TaskQueue` and `validate()`.
- B.2: Implement minimal `src/core/task_queue.py`:
  - `TaskQueue` wrapper around `asyncio.Queue` with `put` and `get` coroutines.
  - `validate()` smoke-check for `put` and `get` presence.

TASK C — AgentRegistry
- C.1: Write failing test `tests/test_core_agent_registry.py` verifying `AgentRegistry` and `validate()`.
- C.2: Implement minimal `src/core/agent_registry.py`:
  - `AgentRegistry` with `register(name, obj)` and `get(name)`.
  - `validate()` registers an object and asserts retrieval.

TASK D — MemoryStore
- D.1: Write failing test `tests/test_core_memory.py` verifying `MemoryStore` and `validate()`.
- D.2: Implement minimal `src/core/memory.py`:
  - `MemoryStore` with `set(key, value)` and `get(key, default)`.
  - `validate()` ensures stored values are retrievable.

TASK E — Observability
- E.1: Write failing test `tests/test_core_observability.py` verifying `emit_metric` or `Observability` and `validate()`.
- E.2: Implement minimal `src/core/observability.py`:
  - `emit_metric(name, value, labels=None)` prints structured JSON to stdout for now.
  - `validate()` emits a test metric.

TASK F — Meta-tests and verification
- F.1: Ensure `tests/test_core_quality.py` (meta-tests) asserts for existence of core modules, presence of `validate()` functions, and absence of circular dependencies (static analysis approach).
- F.2: After implementing A–E, run `pytest -q` to verify all tests including meta-tests pass.

TASK G — CI workflow
- G.1: Add `.github/workflows/core-quality.yml`:
  - Steps: checkout, setup-python 3.11, pip install -r requirements-ci.txt, run `ruff src tests`, run `mypy src`, run `pytest -q`.
  - Trigger: push and pull_request.

TASK H — Docs
- H.1: Create `docs/CORE_DESIGN_GUIDE.md` explaining architecture, async rules, plugin/registration model, validate hooks, and when to move code to `rust_core/`.
- H.2: Create `docs/TEST_QUALITY.md` documenting the meta-tests, required checks for new cores, and CI enforcement rules.

---

Commands to run locally (copy-paste)

Single test run (replace file names as needed):

```powershell
pytest -q tests/test_core_runtime.py
pytest -q tests/test_core_task_queue.py
pytest -q tests/test_core_agent_registry.py
pytest -q tests/test_core_memory.py
pytest -q tests/test_core_observability.py
pytest -q tests/test_core_quality.py
```

Run full suite:

```powershell
pytest -q
```

CI-equivalent commands (for local verification):

```powershell
python -m pip install -r requirements-ci.txt
ruff src tests
mypy src
pytest -q
```

---

Notes and rationale
- Keep modules minimal and import-safe; `validate()` must be cheap and safe to call in CI.
- Avoid blocking operations on the asyncio event loop; prefer `asyncio.sleep(0)` for minimal async no-ops and offload heavy CPU to `rust_core/` when thresholds are reached.
- The plan enforces interface decoupling so future refactors can move heavy logic into Rust without changing public Python APIs.

---

Next steps (hand-off)
- This plan is saved at: `.github/superpower/plan/2026-03-10-core-system-plan.md`.
- To proceed with implementation (creating src/core/* modules, tests, CI file, docs), run the handoff to the execution agent (superpower-execute) or instruct me to proceed and I will create the implementation patches.

If you want me to proceed and apply the implementation (create the source files, tests, and CI), reply "execute" and I will perform the changes in a single patch set and run verification checks.


---

Plan saved by: automated plan generator

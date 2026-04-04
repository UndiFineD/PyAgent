# 2think Memory

This file captures option exploration outputs, 
tradeoff analysis, and recommended directions.

---

## prj0000100 - repo-cleanup-docs-code
_Date: 2026-03-29 | Branch: prj0000100-repo-cleanup-docs-code_

task_id: prj0000100
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.think.md
Recommendation: Option B - Governance-first incremental cleanup with wave-based artifact synchronization
Handoff target: @3design
Rationale summary:
- Root cause is governance drift and discoverability gaps, not only raw cleanup volume.
- Option B scored highest in weighted matrix (460) across risk, effort, impact, governance fit, and maintainability.
- Recommendation preserves scope discipline while operationalizing required governance artifacts (`codestructure.md` and `allowed_websites.md`) from the first wave.

Prior-art references used:
- docs/project/prj0000074/prj0000074.think.md
- docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md
- docs/project/prj0000052/project-management.think.md

Lesson schema:
- Pattern: Governance-first sequencing reduces cleanup rework and improves discoverability for multi-surface repo hygiene projects.
- Root cause: Cleanup efforts drift when policy artifacts are treated as end-of-project documentation rather than continuous operational checkpoints.
- Prevention: Require per-wave closure signals proving governance artifact sync and scope-boundary checks before progressing.
- First seen: 2026-03-29.
- Seen in: prj0000100-repo-cleanup-docs-code.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000099 - stub-module-elimination
_Date: 2026-03-29 | Branch: prj0000099-stub-module-elimination_

task_id: prj0000099
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.think.md
Recommendation: Option B - Minimal-change closure with validation artifacts (no additional code changes needed for current objective)
Handoff target: @3design
Rationale summary:
- Target packages already expose real implementations/exports and are not empty init stubs.
- Focused package tests passed (5/5), validating current objective state.
- Extra refactor would add scope and regression risk without improving objective fulfillment.

Prior-art references used:
- docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md
- docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md

Lesson schema:
- Pattern: Revalidate elimination objective against current package implementation state before proposing refactors.
- Root cause: Project intent lagged repository evolution from stubs to implemented package surfaces.
- Prevention: Require package evidence + focused test evidence gate before proposing any additional elimination code changes.
- First seen: 2026-03-29.
- Seen in: prj0000099-stub-module-elimination.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000097 - stub-module-elimination
_Date: 2026-03-29 | Branch: prj0000097-stub-module-elimination_

task_id: prj0000097
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md
Recommendation: Option C - Targeted Stub Elimination (remove placeholder-grade packages first; retain active compatibility modules)
Handoff target: @3design
Rationale summary:
- Discovery showed idea assumption was stale: all six target packages are implemented, but maturity differs.
- `rl` and `speculation` are placeholder-grade and best suited for first elimination slice.
- `cort`, `runtime_py`, `runtime`, and `memory` are active compatibility/runtime surfaces and should be stabilized before any broad consolidation.

Prior-art references used:
- docs/project/prj0000007/plan.md
- docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.plan.md
- docs/architecture/archive/agents.md

Lesson schema:
- Pattern: Re-validate idea assumptions against current source state before planning deprecation/removal work.
- Root cause: Historical placeholder packages evolved unevenly, leaving mixed maturity under a single "stub" label.
- Prevention: Add package maturity classification (placeholder vs active compatibility) as a mandatory pre-plan checkpoint.
- First seen: 2026-03-29.
- Seen in: prj0000097-stub-module-elimination.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000098 - backend-health-check-endpoint
_Date: 2026-03-29 | Branch: prj0000098-backend-health-check-endpoint_

task_id: prj0000098
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md
Recommendation: Option A - Additive probe endpoints (`/health` unchanged, add `/readyz` + `/livez`) with focused contract tests.
Handoff target: @3design
Rationale summary:
- Discovery confirmed idea drift: `GET /health` already exists and is intentionally unauthenticated/exempt from rate limiting.
- Primary gap is missing readiness/liveness split, not missing health endpoint.
- Minimal additive endpoints provide fastest safe path with deterministic tests and low blast radius.

Prior-art references used:
- docs/project/prj0000054/backend-authentication.design.md
- docs/project/prj0000064/rate-limiting-middleware.design.md
- tests/test_backend_worker.py
- tests/test_rate_limiting.py

Lesson schema:
- Pattern: Re-validate idea assumptions against current source before selecting architecture options.
- Root cause: Idea metadata lagged repository state (`/health` present; only `/readyz` and `/livez` missing).
- Prevention: Add mandatory assumption-diff checkpoint (`idea claims` vs `current code/tests`) at start of @2think.
- First seen: 2026-03-29.
- Seen in: prj0000097-stub-module-elimination; prj0000098-backend-health-check-endpoint.
- Recurrence count: 2.
- Promotion status: promoted to hard rule.

---

## prj0000088 - ai-fuzzing-security
_Date: 2026-03-27 | Branch: prj0000088-ai-fuzzing-security_

task_id: prj0000088
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md
Recommendation: Option A - Deterministic Local Mutation Engine (Rule-Based, No Model Runtime)
Handoff target: @3design
Rationale summary:
- Aligns directly to minimal v1 scope with local deterministic mutation strategies.
- Enforces no-external-call guardrails with bounded execution and explicit allowlists.
- Minimizes blast radius while preserving a clean extension seam for optional local-model mutators in later phases.

---

## prj0000091 - missing-compose-dockerfile
_Date: 2026-03-28 | Branch: prj0000091-missing-compose-dockerfile_

task_id: prj0000091
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md
Recommendation: Option C - Normalize deploy docker layout with minimal blast radius
Handoff target: @3design
Rationale summary:
- Root cause confirmed: `deploy/compose.yaml` points to non-existent `src/infrastructure/docker/Dockerfile`.
- Option C gives clean-checkout reliability while preserving deploy-domain file organization.
- Avoids introducing a new cross-domain `src/infrastructure` tree solely to satisfy one compose reference.

Lesson schema:
- Pattern: For broken deployment paths, prefer deploy-domain normalization over ad hoc cross-tree file creation.
- Root cause: Compose referenced a path with no repository-backed ownership or validation guard.
- Prevention: Add deterministic compose-path existence validation and keep build artifacts co-located under deploy/.
- First seen: 2026-03-28.
- Seen in: prj0000091-missing-compose-dockerfile.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000090 - private-key-remediation
_Date: 2026-03-28 | Branch: prj0000090-private-key-remediation_

task_id: prj0000090
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.think.md
Recommendation: Option C - Phased containment first, then scheduled history rewrite
Handoff target: @3design
Rationale summary:
- Security-first day-0 containment: immediate key rotation/revocation plus active-tree key removal.
- Durable hygiene: mandatory local/CI secret scanning and all-refs verification after history rewrite.
- Lower coordination risk than big-bang rewrite while still converging to full-history remediation.

Lesson schema:
- Pattern: For committed-secret incidents, prefer phased containment plus scheduled full-history cleanup.
- Root cause: Secret present in repository without dedicated secret-scanning gates.
- Prevention: Merge-blocking CI secret scan, local pre-commit secret scan, and periodic history verification.
- First seen: 2026-03-28.
- Seen in: prj0000090-private-key-remediation.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000086 - universal-agent-shell
_Date: 2026-03-27 | Branch: prj0000086-universal-agent-shell_

task_id: prj0000086
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000086-universal-agent-shell/universal-agent-shell.think.md
Recommendation: Option B - Universal Shell Facade with controlled legacy fallback (minimal safe v1)
Handoff target: @3design
Rationale summary:
- Delivers dynamic core resolution by intent in v1 without replacing all specialized agents.
- Uses allowlisted intent migration with immediate fallback to specialized routing.
- Preserves delivery safety while creating a clear contract for design and phased rollout.

---

## prj0000085 — shadow-mode-replay
_Date: 2026-03-27 | Branch: prj0000085-shadow-mode-replay_

task_id: prj0000085
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.think.md
Recommendation: Option B — ReplayEnvelope event model + thin orchestrator (medium scope, low runtime regression risk)
Handoff target: @3design
Rationale summary:
- Separates replay contract from live execution hot path.
- Reuses ContextTransaction/StorageTransaction/ProcessTransaction/MemoryTransaction primitives.
- Aligns with structured logging prior art while adding deterministic schema/version controls.

---

## prj0000087 - n8n-workflow-bridge
_Date: 2026-03-27 | Status: DONE | Branch: prj0000087-n8n-workflow-bridge_

**task_id:** prj0000087
**Recommendation:** Option B - stdlib-only HTTP integration layer + event adapter with optional API-key auth.
**Artifact:** `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md`
**Handoff target:** @3design

Decision rationale summary:
- Meets the bi-directional n8n goal while staying inside a minimal safe v1 scope.
- Reuses existing backend auth/rate-limit/logging patterns instead of introducing new trust paths.
- Preserves low dependency risk (stdlib-only integration layer) and keeps upgrade path open for durable retries later.

---

## prj0000075 ci-simplification — 2026-03-25
Option selected: Keep `ci.yml` only; delete `core-quality.yml`, `pm.yml`, `quality.yml`, `testing-infra.yml` — pre-commit already covers ruff/mypy; ci.yml is the sole non-redundant workflow (Rust build gate + sharded tests)
Artifact: docs/project/prj0000075/prj0000075.think.md
Status: DONE — handoff to @3design

---

## prj0000052 — project-management
_Date: 2026-03-24 | Status: DONE | Branch: prj0000052-project-management_

**task_id:** prj0000052
**Recommendation:** Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop)
**Artifact:** `docs/project/prj0000052/project-management.think.md`
**Handoff target:** @3design (on command from @0master only — DO NOT auto-handoff)

Options explored:
- A: Read-only Kanban, static `data/projects.json`, `GET /api/projects` file-read — RECOMMENDED
- B: Editable Kanban with PATCH endpoint — breaks git-as-source-of-truth, out of scope
- C: DB-backed Kanban (SQLite) — explicitly out of scope per project.md

Research coverage:
- 7-lane structure with PRINCE2 mapping and entry/exit criteria (Area 1)
- React component architecture using existing NebulaOS theme (Area 2)
- Full JSON schema + complete 62-entry project classification (Area 3)
- FastAPI endpoint design consistent with existing app.py patterns (Area 4)
- Minimal agent file update proposals for 0master and 1project (Area 5)
- kanban.md markdown template with full format specification (Area 6)

Key design decisions for @3design:
- 7 lanes confirmed correct (mirrors the 10-agent pipeline segments)
- `pr` field is integer|null (not string), for URL construction
- Budget tier `unknown` is valid enum for Ideas lane only
- `ProjectManager.tsx` uses existing `bg-os-bg`/`text-os-text` etc. CSS vars
- `_PROJECTS` module-level list loaded at import time (not on first request)
- Lane filter via `?lane=` query param on the single `/api/projects` endpoint

Open questions documented in think.md for @3design to resolve.

---

## prj0000047 — conky-real-metrics
_Date: 2026-03-23 | Status: DONE | Branch: prj0000047-conky-real-metrics_

**task_id:** prj0000047
**Recommendation:** Option A — REST Polling via `GET /api/metrics/system` in FastAPI.
**Artifact:** `docs/project/prj0000047/conky-real-metrics.think.md`
**Handoff target:** @3design

Options explored:
- A: REST polling (FastAPI + psutil module-level diff state) — RECOMMENDED
- B: WebSocket push via existing `/ws` — over-engineered, couples chat+metrics
- C: Vite dev-only middleware (Node→Python subprocess) — dev-only, fragile
- D: SSE StreamingResponse — no benefit over polling at 1–2 s on localhost

Key constraints for @3design:
- Network KB/s needs module-level counter state (first call returns zeroes)
- Network interface filtering (loopback/docker) decision needed
- Poll interval: component = 1 s, acceptance criteria default = 2 s (confirm)
- Memory display: % bar vs absolute MB decision needed

---

## prj0000092 - mypy-strict-enforcement
_Date: 2026-03-28 | Branch: prj0000092-mypy-strict-enforcement_

task_id: prj0000092
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md
Recommendation: Option B - Progressive strict lane in stable src/core slices (blocking, scoped)
Handoff target: @3design
Rationale summary:
- Balances enforcement strength with sprint-safe delivery risk by keeping scope to explicit `src/core` slices.
- Reuses deterministic guardrail patterns from existing CI/structure meta-tests.
- Avoids large refactors while still creating a blocking non-regression contract.

Prior-art references used:
- docs/project/prj0000076/prj0000076.think.md
- docs/project/prj0000075/prj0000075.think.md
- tests/test_zzb_mypy_config.py
- tests/structure/test_ci_yaml.py

Lesson schema:
- Pattern: Use scoped blocking strict lanes before broad mypy strict rollout.
- Root cause: Global permissive mypy config turned type checks into non-enforcing signals.
- Prevention: Enforce deterministic CI + structure guards for explicit strict-lane allowlists.
- First seen: 2026-03-28.
- Seen in: prj0000092-mypy-strict-enforcement.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000093 - projectmanager-ideas-autosync
_Date: 2026-03-28 | Branch: prj0000093-projectmanager-ideas-autosync_

task_id: prj0000093
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.think.md
Recommendation: Option A - Backend authoritative exclusion API + frontend consumption
Handoff target: @3design
Rationale summary:
- Minimal-risk additive architecture: backend owns implemented-exclusion semantics and frontend consumes a stable API.
- Default implemented definition selected as active-or-released lanes (Discovery/Design/In Sprint/Review/Released), excluding Archived.
- Avoids frontend logic duplication and avoids process-heavy generated registry workflows.

Prior-art references used:
- docs/project/prj0000052/project-management.think.md
- docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md
- docs/project/kanban.md
- data/projects.json

Lesson schema:
- Pattern: For governance-derived filtering logic in Project Manager, centralize semantics in backend APIs and keep frontend as consumer.
- Root cause: Exclusion behavior and "implemented" semantics were implicit across markdown metadata and lane registry, causing ambiguity.
- Prevention: Define explicit backend contract with lane-based default semantics and contract tests for parser/lane matrix behavior.
- First seen: 2026-03-28.
- Seen in: prj0000093-projectmanager-ideas-autosync.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

## prj0000096 - coverage-minimum-enforcement
_Date: 2026-03-28 | Branch: prj0000096-coverage-minimum-enforcement_

task_id: prj0000096
Lifecycle: OPEN -> IN_PROGRESS -> DONE
Artifact: docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md
Recommendation: Option B - Staged Ratchet to Target Baseline
Handoff target: @3design
Rationale summary:
- Root cause is enforcement drift: legacy non-enforcing threshold history plus current CI path without active coverage gate.
- Staged ratchet balances immediate non-regression enforcement with controlled rollout risk.
- Recommendation is anchored to prior-art governance patterns from strict-lane projects and deterministic quality-gate architecture.

Prior-art references used:
- docs/project/prj0000094-idea-003-mypy-strict-enforcement/prj0000094-idea-003-mypy-strict-enforcement.think.md
- docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md
- docs/project/prj0000075/prj0000075.think.md
- docs/architecture/archive/8testing-quality.md

Lesson schema:
- Pattern: For quality gates with low current enforcement fidelity, prefer staged ratchet rollout over immediate high-threshold cutover.
- Root cause: Configuration may exist without blocking CI integration, creating false confidence in policy enforcement.
- Prevention: Bind threshold source-of-truth to a blocking CI command and enforce anti-softening checks in structure tests.
- First seen: 2026-03-28.
- Seen in: prj0000096-coverage-minimum-enforcement.
- Recurrence count: 1.
- Promotion status: monitor (promote to hard rule at recurrence >= 2).

---

# @1think Design Brief — Phase 1: Foundation & Infrastructure
_Date: 2026-03-16_
_Analyst: @1think | Feeds: @2plan_

---

## 1. Problem Statement

Phase 1 must deliver a **stable, trustworthy core** 
that every downstream phase can build
on without revisiting basic assumptions. 
Four distinct problems must be solved together:

1. **Transaction fragmentation.** Only `MemoryTransaction` exists
   (`src/MemoryTransactionManager.py`). `StorageTransaction`, `ProcessTransaction`, and
   `ContextTransaction` are referenced throughout design docs 
   but are completely absent from the codebase. 
   Code that needs file-system atomicity, subprocess guarding, 
   or context-lineage tracking today has no contract to program against.

2. **Project structure ambiguity and circular-import risk.** 
   `src/core/base/` contains only `__init__.py`; 
   the mixin layer mandated by the architecture does not exist yet.
   Three overlapping "runtime" locations exist simultaneously:
   `src/core/runtime.py`, `src/runtime/`, and `src/runtime_py/`. 
   The transaction manager lives at the `src/` root level 
   rather than in a dedicated package. These structural gaps 
   invite circular imports and make module ownership unclear.

3. **No canonical ContextWindow for LLM token budgeting.** 
   `src/context_manager/` contains only a word-count-based 
   `ContextManager`. No class tracks token budgets,
   manages eviction policies, 
   or provides the single surface that all agents should use
   when constructing LLM prompts. 
   The design docs call for a `ContextWindow` class but none exists.

4. **CI enforces only pytest.** `ci.yml` runs `pytest -q` but does not gate on `ruff`,
   `mypy`, or coverage thresholds. Several specialist CI workflows exist
   (`ci-python-lint.yml`, `quality.yml`, etc.) but their relationship to the main gate
   is unclear. The async-loop checker (`tests/test_async_loops.py`) is mentioned in
   designs and must reliably block synchronous iteration in all PRs.

**Done looks like:**
- `pytest`, `ruff`, and `mypy` all pass on every PR.
- All four transaction types are importable and usable with `async with`.
- Zero circular-import errors running `python -c "import src"` from repo root.
- A single `ContextWindow` class is used in every location that builds LLM prompts.
- Coverage threshold ≥ 80% enforced in CI.

---

## 2. Existing Assets (Do NOT Re-Create)

| Asset | Location | What it provides |
|---|---|---|
| `MemoryTransaction` | `src/MemoryTransactionManager.py` | Thread-lock + `async with` protocol; the model for all other transaction types |
| `Runtime` (dataclass) | `src/core/runtime.py` | Async no-op `start()` + `validate()` hook — DO NOT fork |
| `TaskQueue` | `src/core/task_queue.py` | `asyncio.Queue` wrapper with typed `put`/`get` |
| `MemoryStore` | `src/core/memory.py` | Key-value in-memory store with `set`/`get` |
| `AgentStateManager` | `src/core/agent_state_manager.py` | Stub with `validate()`; extend, do not replace |
| `AgentRegistry` | `src/core/agent_registry.py` | Registration + lookup; assumed populated per core-system plan |
| `Observability` | `src/core/observability.py` | Structured metric emitter; keep as-is |
| `ContextManager` | `src/context_manager/__init__.py` | Word-count windowing; keep for backward-compat, wrap with ContextWindow |
| `conftest.py` | repo root | Fully typed with Protocols; `_SessionWithExitStatus`, `_PytestItemLike` defined |
| CI workflows | `.github/workflows/` | `ci.yml`, `quality.yml`, `ci-python-lint.yml`, `ci-python-quality.yml` exist |
| `pyproject.toml` | repo root | `ruff`, `mypy`, `pytest` configs; `maturin` build backend |
| Async-loop rule | design doc + tests | `tests/test_async_loops.py` concept established; sync loops forbidden |

---

## 3. Design Areas

---

### 3.1 Transaction Unification

#### Problem
Three of four transaction managers are absent. Callers in future phases will need
deterministic side-effect contracts for file I/O (storage), subprocess execution
(process), and context-lineage tracking (context). Without a shared base, each
manager will diverge in interface.

#### Options

| Criterion | Option A — Co-locate in single file | Option B — `src/transactions/` package | Option C — Domain-local files |
|---|---|---|---|
| Interface consistency | Hard to enforce | Easy — shared `BaseTransaction` | Risky — drift |
| Discoverability | Poor | High | Medium |
| Circular-import risk | Low | Low | **High** (e.g. StorageTx in `storage/` imports from `core/`, `core/` imports `storage/`) |
| PascalCase module rule | Awkward | Clean | Clean |
| Rust acceleration path | Difficult | Easy — one location to add FFI | Scattered |
| Matching existing pattern | `MemoryTransactionManager.py` in `src/` root — inconsistent with domain packages | Re-homes all managers to one canonical location | Keeps `Mem*` in place, adds others elsewhere |

**Option A** packs four unrelated classes into one file — violates SRP.  
**Option C** is the origin of circular-import risk (a `StorageTransaction` in a
`storage/` domain package will need to import from `core/` which itself might
import from `storage/`).  
**Option B** is cleanest: a dedicated `src/transactions/` package with one
PascalCase file per type and a shared `BaseTransaction`.

#### Recommendation — Option B: `src/transactions/` package

Create `src/transactions/` with:

```
src/transactions/
├── __init__.py                   # re-exports all four types
├── BaseTransaction.py            # ABC with tid, __aenter__, __aexit__, commit, rollback
├── MemoryTransactionManager.py   # move existing class here, keep src/MemoryTransactionManager.py as shim
├── StorageTransactionManager.py  # new: atomic file ops via tmp-write + rename
├── ProcessTransactionManager.py  # new: subprocess guard with stdout/stderr capture + rollback signal
└── ContextTransactionManager.py  # new: context-lineage UUID injection + parent stack
```

**Rationale:**  
- Single import surface: `from src.transactions import StorageTransaction`  
- Shared `BaseTransaction` ABC enforces the `tid`, `commit()`, `rollback()`, `async with` contract  
- `MemoryTransactionManager.py` at `src/` root becomes a one-line re-export shim (backward compat)  
- Rust acceleration: all four managers can later delegate to `rust_core/transactions` via PyO3 without touching callers

---

### 3.2 Project Structure & Import Hygiene

#### Problem
`src/core/base/` is essentially empty — the mixin layer does not exist. The duplicate
runtime locations (`src/core/runtime.py`, `src/runtime/`, `src/runtime_py/`) create
ambiguity. No `__all__` guards exist on `src/__init__.py` or `src/core/__init__.py`.

#### Options

| Criterion | Option A — Flatten to `src/core/` | Option B — Pure domain packages | Option C — Layered: core + domain + shims |
|---|---|---|---|
| Aligns with architecture doc | Partial — loses domain separation | No — mixin layer unclear | **Yes** |
| Preserves existing working code | Requires moving | Requires moving | Minimal changes |
| Eliminates duplicate runtime | Needs consolidation | Needs consolidation | Rename/deprecate `src/runtime/` and `src/runtime_py/` |
| Mixin layer achievable | Possible | No natural home | `src/core/base/mixins/` as empty scaffold |
| Import clarity | Medium | Low | **High** with explicit `__all__` |

**Option C** is the only approach that respects existing module ownership while making
the required changes surgical.

#### Recommendation — Option C: Layered with surgical consolidation

**Actions (in order):**

1. **Mixin scaffold** — create `src/core/base/mixins/__init__.py` as empty
   placeholder so the architecture reference is honoured. First mixin (`LoggingMixin`)
   can be a stub.

2. **Eliminate runtime ambiguity** — `src/core/runtime.py` is the canonical Runtime.
   `src/runtime/` and `src/runtime_py/` should be audited: if they contain substantive
   code, route it back to `src/core/runtime.py`; if empty stubs, delete them and add a
   deprecation shim in their `__init__.py` pointing at the canonical location.

3. **Add `__all__` guards** to `src/__init__.py`, `src/core/__init__.py`, and
   `src/core/base/__init__.py` to prevent wildcard-import leakage.

4. **Import hygiene test** — add `tests/structure/test_no_circular_imports.py` that
   imports every public module via `importlib` and asserts no `ImportError`.

5. **Move `MemoryTransactionManager.py`** from `src/` root into the new
   `src/transactions/` package (see 3.1) and leave a one-line backward-compat shim.

**Directory target state:**

```
src/
├── __init__.py                    # __all__ guard
├── transactions/                  # NEW — all four transaction types
├── core/
│   ├── __init__.py                # __all__ guard
│   ├── base/
│   │   ├── __init__.py
│   │   └── mixins/
│   │       └── __init__.py       # NEW stub — LoggingMixin placeholder
│   ├── runtime.py                 # CANONICAL runtime
│   ├── agent_registry.py
│   ├── agent_state_manager.py
│   ├── memory.py
│   ├── observability.py
│   └── task_queue.py
├── context_manager/               # EXISTING — keep, wrap with ContextWindow
├── ...domain packages unchanged...
```

---

### 3.3 LLM Context Consolidation

#### Problem
`ContextManager` does token counting by whitespace splitting — not tiktoken-aware,
has no budget enforcement, and is named generically. Agents constructing prompts need
a class that: (a) counts tokens accurately, (b) enforces a per-call budget,
(c) tracks what was evicted, and (d) is the single canonical class used everywhere.

#### Options

| Criterion | Option A — Rename ContextManager → ContextWindow | Option B — New ContextWindow wraps ContextManager | Option C — Migrate ContextManager fully into ContextWindow |
|---|---|---|---|
| Backward compat | **Breaking** — any importer of `ContextManager` breaks | **Safe** — ContextManager preserved | Safe if shim added |
| Token accuracy | Must add tiktoken | Add tiktoken to wrapper | Must add tiktoken |
| Test surface | Existing tests break | Existing tests unaffected | Existing tests adapt |
| Separation of concerns | Conflates windowing with budgeting | Clean split | Clean but heavier migration |
| Complexity | Low | **Low** | Medium |

**Option B** is the cleanest for Phase 1 because it does not break existing consumers
and adds the new capability on a clean surface.

#### Recommendation — Option B: New `ContextWindow` wraps `ContextManager`

Create `src/context_manager/ContextWindow.py` (PascalCase module per convention):

```python
class ContextWindow:
    """Canonical token-budgeted LLM context surface.

    Wraps ContextManager for storage, adds accurate token counting via
    tiktoken (with word-count fallback if tiktoken is unavailable) and
    enforces a per-call token budget.
    """

    def __init__(
        self,
        max_tokens: int,
        model: str = "gpt-4o",
        reserve_output_tokens: int = 512,
    ) -> None: ...

    async def push(self, role: str, content: str) -> None: ...
    # enforces budget; evicts oldest messages when limit approached

    def snapshot(self) -> list[dict[str, str]]: ...
    # returns OpenAI-compatible messages list

    @property
    def remaining_tokens(self) -> int: ...

    def token_count(self, text: str) -> int: ...
    # tiktoken if available, else len(text.split()) * 1.3 heuristic
```

**`src/context_manager/__init__.py` re-exports:**
```python
from .ContextWindow import ContextWindow
from .ContextManager import ContextManager  # backward compat
__all__ = ["ContextWindow", "ContextManager"]
```

**Migration mandate for @2plan:** any new code in Phase 1+ must use `ContextWindow`,
not `ContextManager` directly. `ContextManager` becomes an internal implementation
detail.

---

### 3.4 Testing Infrastructure & CI

#### Problem
The main `ci.yml` only runs `pytest -q`. Ruff and mypy are not CI-gated. Coverage has
no enforced threshold. The async-loop checker is described in docs but its presence
and reliability must be confirmed. Multiple specialist workflows exist but their
relationship to merge-blocking is undefined.

#### Options

| Criterion | Option A — Patch `ci.yml` add ruff + mypy | Option B — Dedicated `quality.yml` runs all gates | Option C — Matrix across Python versions |
|---|---|---|---|
| Time to implement | Fastest | Fast | Slowest |
| Risk of over-engineering | Low | Low | **High for Phase 1** |
| Separates concerns | No | **Yes** | Yes |
| `quality.yml` already exists | N/A | Extend it | Would fork it |
| Coverage threshold | Needs adding | Add `--cov-fail-under=80` | Add to matrix |

Phase 1 goal is a green baseline, not a perfect CI system. Option C (matrix) is
Phase 4 work. Option A patches the wrong workflow (test-only workflow should only
test). **Option B** is right: `quality.yml` becomes the authoritative quality gate.

#### Recommendation — Option B: Authoritative `quality.yml` + fix `conftest.py` async loop test

**`quality.yml` job structure:**

```yaml
jobs:
  lint:
    steps: [ruff check src tests, ruff format --check src tests]
  type-check:
    steps: [mypy src --ignore-missing-imports]
  test:
    steps: [pytest -q --cov=src --cov-fail-under=80 --cov-report=term-missing]
  async-audit:
    steps: [pytest tests/test_async_loops.py -v]
```

**conftest.py requirements (already partially met):**
- `_SessionWithExitStatus` and `_PytestItemLike` Protocols — already present ✓
- `_patched_spec` return type `ModuleSpec | None` — verify and fix
- `_patched_module` return type `ModuleType` — verify and fix
- `session.exitstatus` typed-safe assignment — verify and fix

**pytest.ini additions:**
```ini
asyncio_mode = auto
addopts = --tb=short
```

**Async loop checker — confirm or create `tests/test_async_loops.py`:**  
Performs AST scan of `src/` for `for`/`while` not inside an `async def` body.
Must fail if any blocking loop found outside axiomatic sync utilities.

---

## 4. Interfaces and Contracts

These are the concrete class signatures @2plan must use when spec-writing tasks.
Names, module paths, and method signatures are **binding** for Phase 1.

### 4.1 `BaseTransaction` (ABC)

```python
# src/transactions/BaseTransaction.py
from __future__ import annotations
import abc
from typing import Any, Optional

class BaseTransaction(abc.ABC):
    def __init__(self, tid: Optional[Any] = None) -> None:
        self.tid = tid

    async def __aenter__(self) -> "BaseTransaction": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
```

### 4.2 `StorageTransaction`

```python
# src/transactions/StorageTransactionManager.py
class StorageTransaction(BaseTransaction):
    """Atomic file-system operations: write to .tmp then rename on commit."""

    async def write(self, path: Path, content: str | bytes) -> None: ...
    async def delete(self, path: Path) -> None: ...
    async def mkdir(self, path: Path) -> None: ...
    async def commit(self) -> None: ...   # applies all pending ops
    async def rollback(self) -> None: ... # removes .tmp files, reverts deletes
```

### 4.3 `ProcessTransaction`

```python
# src/transactions/ProcessTransactionManager.py
class ProcessTransaction(BaseTransaction):
    """Subprocess guard: captures stdout/stderr; sends SIGTERM on rollback."""

    async def run(
        self, cmd: list[str], *, cwd: Path | None = None, timeout: float = 30.0
    ) -> tuple[int, str, str]: ...   # (returncode, stdout, stderr)
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...  # terminates any live subprocesses
```

### 4.4 `ContextTransaction`

```python
# src/transactions/ContextTransactionManager.py
import uuid

class ContextTransaction(BaseTransaction):
    """Context lineage: assigns UUID, tracks parent stack, prevents recursion."""

    transaction_id: uuid.UUID        # auto-assigned PascalCase UUID
    parent_id: uuid.UUID | None

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    @classmethod
    def current(cls) -> "ContextTransaction | None": ...  # contextvar accessor
```

### 4.5 `ContextWindow`

```python
# src/context_manager/ContextWindow.py
class ContextWindow:
    def __init__(
        self,
        max_tokens: int,
        model: str = "gpt-4o",
        reserve_output_tokens: int = 512,
    ) -> None: ...

    async def push(self, role: str, content: str) -> None: ...
    def snapshot(self) -> list[dict[str, str]]: ...
    @property
    def remaining_tokens(self) -> int: ...
    def token_count(self, text: str) -> int: ...
    def clear(self) -> None: ...
```

### 4.6 Mixin scaffold

```python
# src/core/base/mixins/__init__.py
# Placeholder — Phase 2 will add LoggingMixin, ObservabilityMixin, etc.
__all__: list[str] = []
```

### 4.7 `src/transactions/__init__.py` re-exports

```python
from .BaseTransaction import BaseTransaction
from .MemoryTransactionManager import MemoryTransaction
from .StorageTransactionManager import StorageTransaction
from .ProcessTransactionManager import ProcessTransaction
from .ContextTransactionManager import ContextTransaction

__all__ = [
    "BaseTransaction",
    "MemoryTransaction",
    "StorageTransaction",
    "ProcessTransaction",
    "ContextTransaction",
]
```

---

## 5. Risks and Open Questions

| Risk / Question | Severity | Mitigation |
|---|---|---|
| `src/runtime/` and `src/runtime_py/` contain live code | **HIGH** | @2plan must audit both directories before deleting. If live code exists, route to `src/core/runtime.py` first. Do not delete without confirming all tests pass. |
| `tiktoken` is in `requirements.txt` but adds 50 MB — may break some envs | Medium | `ContextWindow.token_count()` must fall back gracefully when `tiktoken` is not available. Import guard: `try: import tiktoken; HAS_TIKTOKEN = True except ImportError: HAS_TIKTOKEN = False` |
| `MemoryTransaction` is `threading.RLock`-based but other transactions must be fully async | Medium | `BaseTransaction` ABC must use `asyncio.Lock` as default. `MemoryTransaction` may need updating if it must work under `asyncio` mode. Addass a shim `async with` that wraps the sync lock. |
| `conftest.py` monkey-patches `importlib` — fragile under Python version changes | Medium | Maintain the existing Protocol-based typing approach. Do not change monkey-patch logic. Gate with `test_conftest_typing_contract.py`. |
| Circular import between `src/transactions/ContextTransactionManager.py` and any module that imports `uuid` at global scope — unlikely but verify | Low | Ensure `ContextTransaction` does not import from `src/core/` at module-level beyond stdlib. |
| Coverage threshold of 80% may be unachievable on Day 1 given many stub modules | Medium | Start at 70% in `quality.yml`, raise to 80% in a follow-up task within Phase 1 sprint after stub modules are replaced. Document threshold in `pytest.ini`. |
| `asyncio_mode = auto` in `pytest.ini` may conflict with existing sync tests | Low | Audit existing tests for bare `def test_*()` that use async fixtures. Mark any incompatibles with `@pytest.mark.asyncio` explicitly. |
| **OPEN**: Is there a `tests/test_async_loops.py` file present? | Unknown | @2plan must run `Get-ChildItem tests -Recurse -Filter test_async_loops.py` to confirm. If missing, creating it is a Phase 1 task. |
| **OPEN**: Do `ci-python-lint.yml` and `quality.yml` already enforce ruff/mypy? | Unknown | @2plan must read both files before adding duplicate steps to avoid double-running. |

---

## 6. Handoff to @2plan

The following tasks must be planned **in this order** (dependencies noted).

### Tier 0 — Unblocking (must be done before anything else)
1. **Fix `conftest.py` typing contract** — verify all four Protocol fixes are in place per
   `2026-03-08-conftest-typing-fixes-plan.md`. Run `tests/test_conftest_typing_contract.py`.
   This unblocks all other CI gates.

### Tier 1 — Transaction Package (no external dependencies)
2. **Create `src/transactions/BaseTransaction.py`** — async ABC as specified in §4.1.
3. **Move `MemoryTransaction`** from `src/MemoryTransactionManager.py` to
   `src/transactions/MemoryTransactionManager.py`. Leave shim at old path.
4. **Implement `StorageTransaction`** (`src/transactions/StorageTransactionManager.py`)
   with `write`, `delete`, `mkdir`, `commit`, `rollback` — tmp-write + atomic rename.
5. **Implement `ProcessTransaction`** (`src/transactions/ProcessTransactionManager.py`)
   with `run`, `commit`, `rollback` — asyncio subprocess + SIGTERM on rollback.
6. **Implement `ContextTransaction`** (`src/transactions/ContextTransactionManager.py`)
   with UUID lineage, `contextvars` stack, recursion guard.
7. **Write tests for all four** under `tests/transactions/` — one file per manager,
   aim for 100% coverage of public methods.

### Tier 2 — ContextWindow (depends on Tier 0)
8. **Create `ContextWindow`** at `src/context_manager/ContextWindow.py` per §4.5.
   - `tiktoken` import guard required.
   - `push()` must be `async`.
   - `snapshot()` returns `list[dict[str, str]]` (OpenAI message format).
9. **Update `src/context_manager/__init__.py`** to re-export both `ContextWindow`
   and `ContextManager`.
10. **Write tests** under `tests/context_manager/test_context_window.py`.

### Tier 3 — Project Structure Hygiene (depends on Tier 1 for src/transactions/)
11. **Create `src/core/base/mixins/__init__.py`** stub.
12. **Audit `src/runtime/` and `src/runtime_py/`** — map vs. `src/core/runtime.py`.
    Consolidate or deprecate. Add shim `__init__.py` with deprecation warnings if code is live.
13. **Add `__all__` guards** to `src/__init__.py`, `src/core/__init__.py`,
    `src/core/base/__init__.py`.
14. **Add `tests/structure/test_no_circular_imports.py`** — dynamic import sanity
    checker for all public `src/` modules.

### Tier 4 — CI Hardening (depends on Tier 1, 2, 3 all passing locally)
15. **Audit `quality.yml`** and `ci-python-lint.yml` for existing ruff/mypy steps.
16. **Update `quality.yml`** to enforce:
    - `ruff check src tests`
    - `mypy src --ignore-missing-imports`
    - `pytest --cov=src --cov-fail-under=70` (start at 70, raise to 80 after Tier 1–3 stubs replaced)
    - `pytest tests/test_async_loops.py -v` (async audit)
17. **Confirm or create `tests/test_async_loops.py`** AST scanner.
18. **Add `asyncio_mode = auto`** to `pytest.ini` and resolve any sync-test conflicts.

---

_Design brief complete. @2plan may begin sprint planning from Tier 0._

---

## Auto-handoff

Once deep analysis and option exploration are complete, 
the next agent to run is **@3design**. 
The agent should continue the workflow using `agent/runSubagent`, e.g.

```text
agent/runSubagent --agent @3design
```

This ensures a clean handoff from analysis (2think) 
into design (3design) and keeps the agent workflow chain explicit.

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @2think |
| **source** | @1project |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Explored 4 options for incremental checkpoint writes and 5 new per-agent artifact files. Recommended Option A: Step-Gated Full Overwrite — add one checkpoint rule per agent Operating Procedure to rewrite artifact after each numbered step. Zero Python code changes; instruction-only. |
| **handoff_target** | @3design |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/agent-doc-frequency.think.md |
| **key_decision** | Option A (Step-Gated Full Overwrite): one sentence per agent's Operating Procedure; no StorageTransaction dependency; matches existing write pattern |
| **open_questions_for_3design** | Template authority (inline vs ARTIFACT_TEMPLATES.md); initialization ownership; checkpoint granularity; whether existing 4 artifact types also get the checkpoint rule |

---

## 2026-04-04 rollover from current.2think.memory.md

Archived prior `current.2think.memory.md` project entries before starting `prj0000122-jwt-refresh-token-support`.

- `prj0000120-openapi-spec-generation` — recommended script-first committed backend OpenAPI spec with drift verification.
- `prj0000118-amd-npu-feature-documentation` — recommended canonical docs plus maintainer verification checklist.
- `prj0000117-rust-sub-crate-unification` — recommended root-workspace unification anchored at `rust_core/Cargo.toml`.
- `prj0000116-rust-criterion-benchmarks` — recommended minimal Criterion harness plus lightweight CI smoke benchmark.
- `prj0000115-ci-security-quality-workflow-consolidation` — recommended hybrid fast-path + scheduled heavyweight security scans.
- `prj0000110-idea000004-quality-workflow-branch-trigger` — recommended targeted branch-governance quality gating over workflow sprawl.
- `prj0000108-idea000019-crdt-python-ffi-bindings` — recommended integrating CRDT APIs into the existing `rust_core` PyO3 module.
- `prj0000105-idea000016-mixin-architecture-base` — recommended incremental migration to `src/core/base/mixins/` with compatibility shims.
- `prj0000104-idea000014-processing` — recommended `pyproject.toml` as canonical dependency source with generated `requirements.txt`.
- `prj0000106-idea000080-smart-prompt-routing-system` — recommended hybrid routing with deterministic guardrails and bounded adaptive classification.
- `prj0000107-idea000015-specialized-agent-library` — recommended typed adapter layer over universal shell primitives.
- `prj0000109-idea000002-missing-compose-dockerfile` — recommended incremental hardening around the existing deploy-local Dockerfile fix.

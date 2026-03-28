# prj0000095-source-stub-remediation - Options

_Status: IN_PROGRESS_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
Source-level placeholder and temporary patterns accumulated in package entry points and selected runtime modules due to staged delivery of major subsystems (transport, multimodal, memory, importer, provider adapters). The accumulation caused two risks:
1) import-time health checks and helper APIs were no-ops and did not assert real wiring;
2) runtime behavior in several high-impact paths used deterministic fake logic instead of concrete implementations.

## Scan Methodology
Scope and constraints used for this project:
- Included: source runtime paths under `src/`, `backend/`, `rust_core/`.
- Excluded: all dot-directories (`**/.*/**`), all tests (`tests/**`), all project docs (`docs/**`) for discovery scans.
- Pattern classes searched:
	- explicit placeholders: `placeholder`, `NotImplemented`, `temporary`, `mock`, `fake implementation`
	- review markers: `TODO`, `FIXME`, `HACK`, `STUB`
	- structural no-op patterns where context suggested provisional behavior.

False-positive handling:
- Marker vocabulary embedded in scanner/analysis code (for example classification lists) was treated as non-actionable.
- Abstract base class `pass` statements in intentional interfaces were treated as non-actionable.

## Options
### Option A - rust_core-first remediation pipeline
Description:
- Prioritize Rust substitutions for all candidate stubs, then expose Python wrappers.

Pros:
- Best long-term performance and consistency with rust_core preference.
- Reduces Python-side behavioral drift for throughput-critical code.

Cons:
- High integration cost for modules not yet designed around stable Rust contracts.
- Risk of blocking delivery on pyo3/Tokio bridge decisions.

Assessment:
- Best for deeper follow-up project(s), not ideal for fast risk burn-down of mixed-confidence placeholders.

### Option B - Python-first targeted remediation
Description:
- Replace source placeholders/no-ops in runtime files directly with concrete Python behavior.

Pros:
- Fastest path to remove user-visible stubs and temporary logic.
- Low coordination overhead and easy test validation.

Cons:
- May defer Rust parity work.
- Some checks can remain import-level instead of full capability-level when extension is absent.

Assessment:
- Strong delivery speed, but insufficient alone for modules that are explicitly Rust-backed.

### Option C - Hybrid phased remediation
Description:
- Remediate high-impact runtime paths now with concrete implementations.
- Prefer Rust-backed capability checks where practical.
- Remove compatibility aliases where they only preserve legacy placeholders.
- Defer only high-risk cross-language bridge items requiring architectural decisions.

Pros:
- Balances risk reduction, compatibility, and velocity.
- Aligns with rust_core preference without forcing unsafe rushed integrations.

Cons:
- Requires disciplined deferred-items tracking.
- Produces mixed implementation language in the short term.

Assessment:
- Best fit for this project scope and acceptance criteria.

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Performance | High | Medium | High |
| Maintainability | Medium | Medium | High |
| Delivery Risk | Medium/High | Low | Low/Medium |
| Integration Cost | High | Low | Medium |

## Recommendation
**Option C - Hybrid phased remediation**

Reasoning:
- Removes concrete runtime stubs now in backend and src entry points.
- Removes compatibility-only placeholder wrappers because backward compatibility is explicitly out of scope.
- Keeps Rust-first direction for transport/runtime integration while deferring only unsafe bridge-level work.

## Implemented Remediation Set (This Pass)
High-impact runtime changes already completed in this project:
- `backend/ws_handler.py`: replaced fake token streaming with payload-derived deterministic chunk streaming.
- `src/importer/downloader.py`: replaced placeholder downloader path with clone-first behavior and controlled fallback.
- `src/core/agent_state_manager.py`: replaced no-op/stub validation behavior with concrete state validation logic.
- `src/core/providers/FlmChatAdapter.py`: replaced no-op validation with concrete adapter/factory checks.

Package placeholder hardening completed:
- `src/memory/__init__.py`: real `MemoryStore` + `validate()` with compatibility alias.
- `src/multimodal/__init__.py`: concrete processor round-trip validation + compatibility alias.
- `src/transport/__init__.py`: concrete wrapper/capability validation + compatibility alias.
- `src/rl/__init__.py`: lightweight module-readiness validation + compatibility alias.
- `src/speculation/__init__.py`: lightweight module-readiness validation + compatibility alias.

Additional Rust-first remediation waves completed:
- `rust_core/src/connectivity.rs`: replaced provisional connectivity checks with concrete protocol/URL/payload validation logic.
- `rust_core/src/distributed.rs`: replaced mock two-choice selection with deterministic two-candidate load-balancing and input validation.
- `rust_core/src/inference/verification.rs`: replaced mock batch verification heuristic with softmax-based acceptance and probability edge-case handling.
- `rust_core/src/async_transport.rs`: replaced placeholder channel-handle behavior with structured capacity/channel-id/direction handles.
- `rust_core/src/utils/math.rs`: replaced dummy p-value approximation with normal-CDF-based two-sided significance and made counter-add overflow-safe.
- `rust_core/src/transport/channel/quic.rs`: replaced scaffolding-only module behavior with concrete capability and runtime metadata functions.
- `rust_core/src/inference/engine.rs`: replaced warmup-size mock behavior with deterministic bucketed warmup tuples for graph capture planning.
- `rust_core/src/async_transport.rs`: removed stale placeholder wording now that structured channel handles are implemented.
- `rust_core/src/neural/transformer.rs`: replaced mock-style response-generation flow with deterministic prompt-derived embeddings and output summary metrics.

Follow-up priority wave (rust > python > typescript):
- Rust: build completed (`cargo build`) and additional scan performed; no higher-confidence Rust runtime stubs remained beyond compatibility alias naming and literal-template placeholders.
- Python: `src/core/task_queue.py` promoted from scaffold-level wrapper to full queue lifecycle utility with concrete helpers and stronger validation.
- TypeScript: `web/apps/AutoMemBenchmark.tsx` removed synthetic demo benchmark generation fallback and now reports real backend errors when data cannot be fetched/run.

Latest rust > python > typescript remediation wave:
- Rust: replaced three runtime scaffold implementations with concrete deterministic behavior:
	- `rust_core/src/inference/attention.rs` no longer returns query passthrough; it now applies compressed-signal fallback scoring.
	- `rust_core/src/multimodal/grammar.rs` no longer returns an empty token set; it now performs prefix-constrained candidate selection with safe fallback.
	- `rust_core/src/hardware.rs` no longer returns fixed TensorRT placeholders; it now validates engine handles and performs row normalization fallback inference.
- Python:
	- `src/core/memory/AutoMemCore.py` replaced silent AGE exception pass with persisted `graph_sync`/`graph_sync_error` metadata fallback.
	- `src/transactions/StorageTransactionManager.py` replaced pass-body coroutine scaffold with explicit cooperative async yield.
- TypeScript:
	- `web/components/Login.tsx` removed fake OAuth timeout simulation in favor of direct async callback execution with proper loading cleanup.

PostgreSQL-backed web data-method implementation:
- Added `backend/automem_benchmark_store.py` as a real persistence/execution layer:
	- runs benchmarks via `src.core.memory.BenchmarkRunner`
	- persists benchmark runs in `automem_benchmark_runs` (JSONB payload)
	- maintains real KV latest snapshot in `automem_kv` (`benchmark_latest` key)
	- now exposes concrete data methods for run history and KV CRUD (`get_run`, `list_runs`, `kv_get`, `kv_set`, `kv_delete`)
- Added concrete web API routes in `backend/app.py` for:
	- `GET /api/automem/benchmark/latest` (+ `/api/v1/...`)
	- `POST /api/automem/benchmark/run` (+ `/api/v1/...`)
	- `GET /api/automem/benchmark/runs` and `GET /api/automem/benchmark/runs/{run_id}` (+ `/api/v1/...`)
	- `GET/PUT/DELETE /api/automem/kv/{key}` (+ `/api/v1/...`)
- This replaces planned/temporary benchmark data paths for `web/apps/AutoMemBenchmark.tsx` with real PostgreSQL-backed methods.

Schema hardening and bootstrap outcomes:
- Added a controlled benchmark preflight in `backend/automem_benchmark_store.py` that reports actionable missing-schema diagnostics instead of opaque 500 errors.
- Added optional `bootstrap_schema` execution path to create minimal benchmark tables/indexes and required function defaults.
- Bootstrap is now capability-aware:
	- if `pgvector` exists, `memories.embedding` uses `vector(1536)` and runner uses vector distance operator.
	- if `pgvector` is unavailable, schema falls back to `double precision[]` and runner uses L2 scan SQL fallback.
	- LTREE benchmark path now runs only when `ltree` is available.
- Fixed persistence edge cases discovered during live validation:
	- normalize ISO `completed_at` strings to `datetime` before asyncpg TIMESTAMPTZ binds.
	- decode JSONB payloads robustly across asyncpg codec modes for `/latest` and `/runs` endpoints.

## Validation Snapshot
Focused tests for placeholder callers and related package behavior:
- `tests/test_core_helpers.py`
- `tests/test_multimodal_package.py`
- `tests/test_transport_package.py`
- `tests/core/test_core.py`
- `tests/agents/test_agents.py`

Result: `62 passed, 0 failed`.

Additional validation:
- Focused Python checks for registry/helper compatibility remain green after follow-up fixes.
- Repeated `cargo check` runs for `rust_core` passed after each Rust remediation wave.
- Rust build completed successfully via `cargo build`.
- Web frontend build completed successfully via `npm run build`.
- Backend import validation passed after route/store integration (`import backend.app`).
- Additional rust-first validation wave succeeded:
	- `cargo build` in `rust_core` completed successfully after attention/grammar/hardware replacements.
	- `python -m py_compile src/core/memory/AutoMemCore.py src/transactions/StorageTransactionManager.py` completed successfully.
	- `pytest -q tests/test_AutoMemCore.py tests/test_StorageTransactionManager.py` passed (`30 passed`).
	- `npm run build` in `web` completed successfully after login flow replacement.
- Live endpoint verification now passes end-to-end with `AUTOMEM_POSTGRES_DSN=postgresql://pyuser:pyuser@localhost:5432/automem_db`:
	- `POST /api/automem/benchmark/run` with `bootstrap_schema=true` -> 200
	- `GET /api/automem/benchmark/latest` -> 200
	- `GET /api/automem/benchmark/runs?limit=3` -> 200
	- `GET /api/automem/benchmark/runs/does-not-exist` -> 404 (expected)
- Follow-up scaffold/mock scan now only reports non-actionable template/compatibility markers plus intentional `NotImplemented` protocol semantics.

## Latest Pass Delta (Rust > Python > TypeScript)
- Rust-first execution completed with fresh build baseline and post-change build validation.
- Rust runtime changes:
	- `rust_core/src/inference/distributed.rs`: replaced remaining mock scoring with concrete capability/latency/size scoring and added `num_packs > 0` validation.
	- `rust_core/src/hardware.rs`: removed final placeholder fallback wording and standardized unsupported-path status handling.
	- `rust_core/src/multimodal/audio.rs`: replaced lightweight mel DFT path with concrete FFT-backed mel extraction via `rustfft`.
- Python runtime changes (no-backward-compatibility mode): removed legacy `placeholder()` alias wrappers from package surfaces:
	- `src/memory/__init__.py`
	- `src/multimodal/__init__.py`
	- `src/transport/__init__.py`
	- `src/rl/__init__.py`
	- `src/speculation/__init__.py`
- TypeScript scan found no runtime scaffold/provisional targets requiring changes in this pass.
- Validation evidence from this pass:
	- `cargo build` in `rust_core` passed before and after changes.
	- `python -m py_compile` passed on all changed Python files.
	- Focused marker scan over changed Rust/Python files returned no matches.
	- Additional focused pass: `cargo build` passed after adding `rustfft` and migrating `audio.rs`; marker scan over scoped package/runtime surfaces confirms no remaining `placeholder()` compatibility exports in `src/**/__init__.py`.

## Focused Rust Async Runtime Delta
- Implemented concrete runtime behavior in `rust_core/src/async_runtime.rs`:
	- `spawn_task` now validates coroutine inputs, resolves active loop safely, schedules via loop `create_task`, and returns the created task handle.
	- `set_timeout` now validates finite/non-negative delay, validates coroutine input, schedules delayed task creation on the resolved loop, and returns the asyncio timer handle.
	- Added loop-resolution fallback (`get_running_loop` then `get_event_loop`) to support both active and bootstrap contexts.
	- Added guardrail validation for queue size bounds in `create_queue`.
	- Added Rust runtime hot-path keepalive scheduling and delay mirror for safer concrete partial Tokio integration.
- Validation evidence for this focused pass:
	- `Push-Location rust_core; cargo build; Pop-Location` passed.
	- `Push-Location rust_core; cargo check --features async-transport --lib; Pop-Location` passed.
	- Focused marker scan for scaffold/provisional tokens in `rust_core/src/async_runtime.rs` returned no matches.

## AutoMem Benchmark Dual-Backend Delta
- Root cause confirmed for current user issue:
	- benchmark execution pipeline was PostgreSQL-only in practice.
	- frontend chart grouping keyed by method only, so same method names across backends collide/overwrite.
	- vector and ltree fallback behavior could silently alter observable behavior by method naming/omission.
	- bootstrap extension creation catch logic regressed to a narrow exception set, allowing extension availability errors (for example PostgreSQL `FeatureNotSupportedError`) to abort schema bootstrap unexpectedly.
- Implemented decision:
	- keep method keys stable across backends (`hnsw_vector`, `ltree_subtree`, etc.) and carry fallback/unavailable context in result `status` + `metadata` + report `errors`.
	- run both backends by default in store/API layer with partial-backend failure tolerance so one failed backend does not hide the other.
	- merge both backend reports into one persisted payload with preserved `results[*].backend` identity.
	- frontend series identity now uses `backend::method` and labels render as `Backend · Method`.
- Validation observations:
	- local API invocation returned both backend identities in one run (`['memory', 'postgres']`).
	- search method keys remained stable while fallback details were explicitly surfaced (`postgres:hnsw_vector` fallback and explicit `ltree_subtree` note).
	- frontend build passed with backend-aware chart grouping and note rendering.

## Regression Fix Note (2026-03-28)
- Updated `backend/automem_benchmark_store.py` to tolerate optional-extension availability errors during bootstrap for `vector`, `ltree`, and `uuid-ossp`.
- Approach: treat extension availability/privilege SQLSTATEs and known asyncpg exception classes as tolerable, continue bootstrap, and rely on preflight/schema checks for explicit diagnostics.
- Validation evidence:
	- `python -m py_compile backend/automem_benchmark_store.py backend/app.py src/core/memory/BenchmarkRunner.py` succeeded.
	- FastAPI TestClient `POST /api/automem/benchmark/run` with `{'row_counts':[50],'backends':['postgres','memory'],'bootstrap_schema':True}` returned 200 and result payload included both backends (`memory`, `postgres`).

## Open Questions
- Should the deferred rust_core async bridge implementation be split into a dedicated project with ADR coverage (pyo3 async runtime contract)?
- Should stale tests that still assert package-level `placeholder()` APIs be updated in the next @5test/@6code cycle?

## Deferred Items
1) Optional enhancement: wire `bootstrap_schema` to canonical migration execution so bootstrap and production schema governance share one path.
2) Stale tests that assert compatibility-only `placeholder()` package APIs require follow-up updates under the test-writing phase.

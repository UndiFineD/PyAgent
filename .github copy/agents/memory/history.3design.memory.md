# 3design Memory

This file records finalized design decisions, 
architecture diagrams, and key interface contracts.

## Auto-handoff (Design → Plan)

Once a design is finalized, the next agent in the workflow is **@4plan**.  
The designer agent should invoke **@4plan** via `agent/runSubagent` 
so the planning work is started automatically 
and the work is correctly attributed.

When calling `agent/runSubagent`, include a clear task description 
and any relevant context/links to the design decisions 
so the planning agent can continue without having to re-derive 
the design intent.

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-18 |
| **status** | DONE |
| **summary** | Designed checkpoint rule (Step-Gated Full Overwrite) for all 9 agent artifact files. Templates inline per agent. @1project pre-creates all 9 stubs. Checkpoint rule applies to all artifact types. Documents updated before next runSubagent call. |

---

## prj0000052 - project-management

| Field | Value |
|---|---|
| **task_id** | prj0000052-project-management |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-24 |
| **updated_at** | 2026-03-24 |
| **status** | DONE |
| **branch** | prj0000052-project-management |
| **artifact** | docs/project/prj0000052/project-management.design.md |
| **selected_option** | Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop) |
| **summary** | Full design for 6 deliverables: (1) docs/project/kanban.md with all 62 projects in 7 lanes; (2) data/projects.json with complete 62-entry array; (3) web/apps/ProjectManager.tsx React Kanban component; (4) backend/app.py GET /api/projects endpoint + ProjectModel; (5) 0master.agent.md + 1project.agent.md additions; (6) web/App.tsx + web/types.ts registration. Status: DONE — report back to @0master (no @4plan handoff). |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj030-agent-doc-frequency/agent-doc-frequency.design.md |
---

## prj0000045 - transaction-managers-full

| Field | Value |
|---|---|
| **task_id** | prj0000045-transaction-managers-full |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-22 |
| **updated_at** | 2026-03-22 |
| **status** | HANDED_OFF |
| **branch_gate** | WARN — designed on `main`; expected `prj0000045-transaction-managers-full` |
| **selected_option** | Option B — `src/transactions/` package with BaseTransaction ABC |
| **key_decisions** | Dual-API coexistence (single class, two constructor modes); Fernet encryption (cryptography pkg, HKDF per-user key, user_id=None skips); httpx remote sync with dry_run=True for tests; ContextTransaction UUID lineage auto-wired from contextvar stack; ContextWindow LLM handoff deferred to follow-on project |
| **interface_contracts** | See design.md §Interfaces & Contracts; 5 open questions documented for @4plan |
| **shim_strategy** | 3 new src/core/ shims + 1 replacement src/MemoryTransactionManager.py shim |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000045/transaction-managers-full.design.md |

---

## prj0000047 - conky-real-metrics

| Field | Value |
|---|---|
| **task_id** | prj0000047-conky-real-metrics |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-23 |
| **updated_at** | 2026-03-23 |
| **status** | DONE |
| **branch_gate** | PASS — `prj0000047-conky-real-metrics` |
| **selected_option** | Option A — REST Polling `GET /api/metrics/system` (psutil, module-level delta state) |
| **key_decisions** | 2s poll interval; `useSystemMetrics(2000)` custom hook; stay-on-last-values error strategy + OFFLINE badge; no Vite dev plugin needed (existing /api proxy sufficient); memory surfaces used_mb/total_mb/percent; disk I/O row added to UI; interface filter by name prefix (lo, docker, veth, br-, virbr, tun, tap, loopback, isatap, teredo) |
| **interface_contracts** | `SystemMetrics` TS interface; `SystemMetricsResponse` Pydantic model; `useSystemMetrics` hook; `_is_physical_iface()` helper; module-level `_prev_net` + `_prev_disk` delta state |
| **vite_config_change** | None required |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000047/conky-real-metrics.design.md |

---

## prj0000086 - universal-agent-shell

| Field | Value |
|---|---|
| **task_id** | prj0000086-universal-agent-shell |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **branch_gate** | PASS — `prj0000086-universal-agent-shell` |
| **selected_option** | Option B — Universal Shell Facade with Controlled Legacy Fallback |
| **design_path** | Minimal facade module under `src/core/universal/` with `UniversalIntentRouter.py`, `UniversalCoreRegistry.py`, `UniversalAgentShell.py`, `exceptions.py`, `__init__.py` |
| **interface_contracts** | `TaskEnvelope`, `RoutingDecision`, `DispatchResult`, async `CoreHandler.execute(envelope)`, one-shot fallback policy |
| **assumptions** | Allowlist-gated core routing, single fallback attempt, deterministic normalization, constructor-injected dependencies |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md |

---

## prj0000088 - ai-fuzzing-security

| Field | Value |
|---|---|
| **task_id** | prj0000088-ai-fuzzing-security |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **branch_gate** | PASS - `prj0000088-ai-fuzzing-security` |
| **selected_option** | Option A - Deterministic Local Mutation Engine |
| **design_path** | `src/core/fuzzing/` contracts for `FuzzCase`, `FuzzMutator`, `FuzzCorpus`, `FuzzEngineCore`, `FuzzSafetyPolicy`, `FuzzResult`, `exceptions`, and `__init__` |
| **interface_contracts** | Deterministic replay key, mutation operator protocol, policy limits, campaign run/build/execute API, typed result aggregation and exception hierarchy |
| **assumptions** | Local-only targets, allowlist enforcement, no external network paths, seed-based deterministic scheduling |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.design.md |

---

## prj0000090 - private-key-remediation

| Field | Value |
|---|---|
| **task_id** | prj0000090-private-key-remediation |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | HANDED_OFF |
| **branch_gate** | PASS - `prj0000090-private-key-remediation` |
| **selected_option** | Option C - phased containment + scheduled history rewrite |
| **design_path** | Secret-remediation control plane with phase gates: containment, verification, rewrite, stabilization |
| **interface_contracts** | `SecretScanService`, `RotationCheckpointService`, `SecretGuardrailPolicy`, `HistoryRewriteCoordinator` |
| **adr** | docs/architecture/adr/0002-secret-remediation-control-plane.md |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.design.md |
| **Pattern** | For exposed secrets, prefer phased fail-closed remediation control plane over ad-hoc cleanup |
| **Root cause** | Secret material can be removed from active tree while remaining in history without explicit rewrite gate |
| **Prevention** | Enforce rotation checkpoint gate + mandatory CI secret scan + post-rewrite zero-match verification |
| **First seen** | 2026-03-28 |
| **Seen in** | prj0000090-private-key-remediation |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000091 - missing-compose-dockerfile

| Field | Value |
|---|---|
| **task_id** | prj0000091-missing-compose-dockerfile |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000091-missing-compose-dockerfile` |
| **selected_option** | Option C - normalize deploy Docker layout with minimal blast radius |
| **design_path** | Keep compose canonical in `deploy/compose.yaml`; set `build.dockerfile` to `deploy/Dockerfile.pyagent`; add deterministic compose Dockerfile path guard test |
| **interface_contracts** | IFC-01 Compose Build Contract; IFC-02 Dockerfile Contract; IFC-03 Regression Guard Contract |
| **assumptions** | `deploy/compose.yaml` remains project-scope canonical compose file; full compose consolidation deferred |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md |
| **Pattern** | For missing deploy file references, co-locate runtime artifacts under deploy domain and enforce static path guards |
| **Root cause** | Compose referenced a non-existent Dockerfile path (`src/infrastructure/docker/Dockerfile`) |
| **Prevention** | Add deterministic test that parses compose build dockerfile entries and asserts path existence |
| **First seen** | 2026-03-28 |
| **Seen in** | prj0000091-missing-compose-dockerfile |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000092 - mypy-strict-enforcement

| Field | Value |
|---|---|
| **task_id** | prj0000092-mypy-strict-enforcement |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000092-mypy-strict-enforcement` |
| **selected_option** | Option B - progressive strict lane in stable `src/core` slices |
| **design_path** | Locked phase-1 allowlist with dedicated strict-lane config + blocking CI + structure/smoke guards |
| **interface_contracts** | IFC-01 Strict Lane Config, IFC-02 CI Blocking Contract, IFC-03 Structure Guard Contract, IFC-04 Strict Failure Smoke Contract |
| **assumptions** | Keep global permissive mypy behavior in phase-1; strict enforcement applies only to explicit allowlist; CI lane runs once per workflow |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.design.md |
| **Pattern** | Introduce strict typing via a narrow, deterministic allowlist lane before broadening scope |
| **Root cause** | Existing global mypy config suppresses actionable enforcement and CI lacked a blocking type gate |
| **Prevention** | Lock allowlist in config + structure tests and enforce blocking CI command invariants |
| **First seen** | 2026-03-28 |
| **Seen in** | prj0000092-mypy-strict-enforcement |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000093 - projectmanager-ideas-autosync

| Field | Value |
|---|---|
| **task_id** | prj0000093-projectmanager-ideas-autosync |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000093-projectmanager-ideas-autosync` |
| **selected_option** | Option A - backend-authoritative ideas API consumed by frontend |
| **design_path** | Additive `GET /api/ideas` contract with backend-implemented filtering/sorting; `ProjectManager.tsx` consumes unimplemented ideas feed in read-only panel |
| **interface_contracts** | IFC-01 Ideas endpoint contract; IFC-02 idea-to-project mapping strategy; IFC-03 frontend integration contract; IFC-04 backend/frontend test contracts |
| **assumptions** | Idea mapping is sourced from `Planned project mapping:` line and project IDs use `prj\d{7}`; default implemented mode is active_or_released |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.design.md |
| **Pattern** | For governance data shown in UI, centralize exclusion/filter semantics in backend and make frontend a consumer |
| **Root cause** | Ideas existed only as markdown with no API contract, causing no deterministic implementation-status filtering |
| **Prevention** | Define explicit endpoint parameters + stable sorting + parser tests and UI failure isolation tests |
| **First seen** | 2026-03-28 |
| **Seen in** | prj0000093-projectmanager-ideas-autosync |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000096 - coverage-minimum-enforcement

| Field | Value |
|---|---|
| **task_id** | prj0000096-coverage-minimum-enforcement |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-28 |
| **updated_at** | 2026-03-28 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000096-coverage-minimum-enforcement` |
| **selected_option** | Option B - staged ratchet to target baseline |
| **design_path** | Staged CI coverage ratchet with single source-of-truth threshold and blocking gate in existing workflow |
| **interface_contracts** | IFC-01 CI Coverage Gate, IFC-02 Threshold Source-of-Truth, IFC-03 Structure Guard, IFC-04 Workflow-Count Compatibility |
| **assumptions** | First slice stage is 40; no new workflow files; ratchet promotions require explicit evidence in project test artifact |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.design.md |

---

## prj0000100 - repo-cleanup-docs-code

| Field | Value |
|---|---|
| **task_id** | prj0000100-repo-cleanup-docs-code |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000100-repo-cleanup-docs-code` |
| **selected_option** | Option B - Governance-First Incremental Cleanup |
| **design_path** | Canonical governance-first cleanup design with explicit contracts for code structure index, local-search-first policy, and internet allowlist gate |
| **interface_contracts** | IFC-01 Code Structure Index Contract; IFC-02 Local Search First Contract; IFC-03 Internet Search Gate Contract |
| **assumptions** | Branch remains project branch; cleanup is wave-scoped and non-destructive; policy artifacts are canonical authorities |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.design.md |
| **Pattern** | For broad cleanup work, lock governance contracts first and execute incremental waves with explicit containment gates |
| **Root cause** | Policy drift and discoverability gaps occur when governance artifacts are updated late or inconsistently |
| **Prevention** | Enforce contract-first wave exits: code index delta checks, local-first evidence, and fail-closed allowlist gate |
| **First seen** | 2026-03-29 |
| **Seen in** | prj0000100-repo-cleanup-docs-code |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |
| **Pattern** | Enforce quality gates by ratcheting from a low-risk baseline using one authoritative threshold key |
| **Root cause** | Coverage threshold existed in config but was not wired into blocking CI path |
| **Prevention** | Keep threshold in one config location and guard CI contract with structure tests |
| **First seen** | 2026-03-28 |
| **Seen in** | prj0000096-coverage-minimum-enforcement |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000097 - stub-module-elimination

| Field | Value |
|---|---|
| **task_id** | prj0000097-stub-module-elimination |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000097-stub-module-elimination` |
| **selected_option** | Option C - targeted stub elimination, Slice 1 (`rl` + `speculation`) |
| **design_path** | Keep module paths stable; replace placeholder behavior; deprecate `validate()` shims |
| **interface_contracts** | IFC-RL-001/002, IFC-SPC-001/002, and import-scan guard contract |
| **assumptions** | No runtime/memory/cort refactor; one-release deprecation window before shim removal |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.design.md |
| **Pattern** | Replace placeholder modules with one deterministic behavior contract before shim removal |
| **Root cause** | `rl` and `speculation` exposed only import-level `validate()` placeholders |
| **Prevention** | Require behavior-first ACs, deprecation tests, and import-scope guards |
| **First seen** | 2026-03-29 |
| **Seen in** | prj0000097-stub-module-elimination |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000098 - backend-health-check-endpoint

| Field | Value |
|---|---|
| **task_id** | prj0000098-backend-health-check-endpoint |
| **owner_agent** | @3design |
| **source** | @2think |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000098-backend-health-check-endpoint` |
| **selected_option** | Option A - additive probe endpoints in backend/app.py (minimal-first) |
| **design_path** | Keep existing /health unchanged; add /livez and /readyz contracts; keep scope to backend/app.py + health-check tests |
| **interface_contracts** | IFC-HC-001 (/health), IFC-HC-002 (/livez), IFC-HC-003 (/readyz) including status codes, payloads, and non-auth/non-rate-limit expectations |
| **assumptions** | No broad backend refactor; no external dependency probe in first-slice readiness check; probe endpoints remain unversioned |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.design.md |
| **Pattern** | Add health semantics via minimal additive endpoints while preserving existing probe compatibility |
| **Root cause** | Only /health existed, so liveness and readiness semantics were conflated and operational contracts were incomplete |
| **Prevention** | Define explicit per-endpoint contracts (status/payload/auth/rate-limit) and enforce via focused regression tests |
| **First seen** | 2026-03-29 |
| **Seen in** | prj0000098-backend-health-check-endpoint |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## prj0000099 - stub-module-elimination

| Field | Value |
|---|---|
| **task_id** | prj0000099-stub-module-elimination |
| **owner_agent** | @3design |
| **source** | User reality update |
| **created_at** | 2026-03-29 |
| **updated_at** | 2026-03-29 |
| **status** | DONE |
| **lifecycle** | OPEN -> IN_PROGRESS -> DONE |
| **branch_gate** | PASS - `prj0000099-stub-module-elimination` |
| **selected_option** | Validation-First Closure |
| **design_path** | No default functional code changes; close via evidence gates for package API non-emptiness and focused tests green |
| **interface_contracts** | IFC-VAL-01 (API evidence), IFC-VAL-02 (focused tests), IFC-VAL-03 (conditional minimal remediation) |
| **assumptions** | Target stubs are already eliminated; remediation is only triggered by failed evidence checks |
| **handoff_target** | @4plan |
| **artifact_paths** | docs/project/prj0000099-stub-module-elimination/prj0000099-stub-module-elimination.design.md |
| **Pattern** | When implementation already satisfies intent, close with validation-first evidence gates instead of adding churn |
| **Root cause** | Project artifacts lagged behind repository reality after prior elimination work completed |
| **Prevention** | Re-baseline design to present-state evidence checks before scheduling new implementation tasks |
| **First seen** | 2026-03-29 |
| **Seen in** | prj0000099-stub-module-elimination |
| **Recurrence count** | 1 |
| **Promotion status** | Candidate |

---

## 2026-04-04 rollover from current.3design.memory.md

# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-03
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000120-openapi-spec-generation
	state: DONE
	selected_design_path: Option A (script-first committed backend-only OpenAPI artifact with narrow drift enforcement)
	assumptions:
		- `backend/app.py` remains the sole phase-one schema authority and no runtime route behavior change is required.
		- `docs/api/` remains the narrative publication surface, with generated JSON treated as a publishable static asset instead of generated Markdown.
		- Lightweight CI in `.github/workflows/ci.yml` can absorb one narrow pytest selector without expanding into a full docs build lane.
	interface_contract_notes:
		- IFACE-OAS-001 backend-only schema authority contract.
		- IFACE-OAS-002 explicit generator script ownership contract.
		- IFACE-OAS-003 committed artifact path and deterministic serialization contract.
		- IFACE-OAS-004 read-only drift pytest contract.
		- IFACE-OAS-005 lightweight CI enforcement contract.
		- IFACE-OAS-006 docs publication consumer-only contract.
		- IFACE-OAS-007 phase-one exclusion contract for secondary FastAPI apps.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0007-script-first-backend-openapi-artifact-governance.md
	lesson:
		Pattern: API contract publication lanes stay implementable when generation ownership, verification ownership, and docs publication ownership are assigned to separate surfaces.
		Root cause: OpenAPI efforts become brittle when scripts, tests, CI, and docs builds all try to own generation at once.
		Prevention: Require a single generator entrypoint, a read-only drift test, a narrow CI selector, and explicit publication boundaries in the canonical design artifact.
		First seen: 2026-04-03
		Seen in: prj0000120-openapi-spec-generation
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000118-amd-npu-feature-documentation
	state: DONE
	selected_design_path: Option B (canonical docs plus maintainer verification checklist)
	assumptions:
		- Canonical runtime guidance remains in `docs/performance/HARDWARE_ACCELERATION.md`, with project artifacts providing governance traceability.
		- `rust_core/Cargo.toml` feature declaration and `rust_core/src/hardware.rs` fallback semantics are the authoritative repository evidence for this lane.
		- CI automation for AMD NPU remains deferred until repeated maintainer evidence justifies a dedicated follow-on project.
	interface_contract_notes:
		- IFACE-AMD-001 canonical documentation location contract.
		- IFACE-AMD-002 feature activation command contract.
		- IFACE-AMD-003 unsupported fallback (`-1`) interpretation contract.
		- IFACE-AMD-004 environment gate contract.
		- IFACE-AMD-005 validation evidence schema contract.
		- IFACE-AMD-006 deferred CI automation contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Docs-only hardware feature projects stay actionable when unsupported behavior semantics and evidence schema are both mandatory acceptance gates.
		Root cause: Feature documentation efforts often stop at activation prose and omit fallback interpretation plus auditable validation proof requirements.
		Prevention: Require AC table with IFACE mapping, explicit supported/unsupported matrix, and evidence template fields before @4plan handoff.
		First seen: 2026-04-03
		Seen in: prj0000118-amd-npu-feature-documentation
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000117-rust-sub-crate-unification
	state: DONE
	selected_design_path: Option B (root Cargo workspace unification with root package retained)
	assumptions:
		- `rust_core/Cargo.toml` remains the canonical manifest path for `maturin` and CI benchmark smoke.
		- Workspace migration is delivered as an atomic slice with lockfile convergence and targeted command updates.
		- Root-owned patch governance must preserve the existing p2p security override behavior.
	interface_contract_notes:
		- IFACE-WS-001 build command continuity contract.
		- IFACE-WS-002 package-scoped workspace command contract.
		- IFACE-WS-003 benchmark smoke compatibility contract.
		- IFACE-WS-004 single-lockfile governance contract.
		- IFACE-WS-005 root-owned patch governance contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.design.md
		chunked_artifacts: none
		adr_artifact: pending @4plan/@8ql confirmation
	lesson:
		Pattern: Rust workspace migrations stay actionable when lockfile policy, command continuity, and patch-ownership contracts are specified together.
		Root cause: Unification tasks fail when teams migrate manifests without explicit command and lockfile contracts.
		Prevention: Require AC table plus IFACE-to-task traceability that binds workspace shape to deterministic validation commands.
		First seen: 2026-04-03
		Seen in: prj0000117-rust-sub-crate-unification
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000116-rust-criterion-benchmarks
	state: DONE
	selected_design_path: Option B (minimal Rust Criterion harness plus lightweight CI smoke benchmark)
	assumptions:
		- Initial scope targets one or two bounded pure functions in `rust_core` stats modules.
		- CI benchmark lane is smoke-only in v1 (no regression-threshold enforcement).
		- `cargo bench` remains the canonical command entrypoint for local validation.
	interface_contract_notes:
		- IFACE-BENCH-001 benchmark file and deterministic naming contract.
		- IFACE-BENCH-002 local command entrypoint contract (`cargo bench --bench stats_baseline`).
		- IFACE-BENCH-003 CI smoke command contract (`--noplot`, exit-success gate).
		- IFACE-BENCH-004 artifact contract (`rust_core/target/criterion/**`).
		- IFACE-BENCH-005 minimal scope boundary contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Benchmark governance lands cleanly when CI introduces harness-health smoke checks before any threshold enforcement.
		Root cause: Immediate threshold gating in early benchmark adoption creates flakiness and slows rollout.
		Prevention: Lock smoke-only pass criteria, explicit naming contracts, and AC/IFACE traceability in the design artifact.
		First seen: 2026-04-03
		Seen in: prj0000116-rust-criterion-benchmarks
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
	state: DONE
	selected_design_path: Option B (targeted project-branch governance gate with main-focused full-suite triggers retained)
	assumptions:
		- Existing `ci.yml` and `security.yml` remain authoritative full-suite workflows centered on `main`.
		- Governance gate reuses canonical policy entrypoints (`scripts/enforce_branch.py` and docs policy pytest selector).
		- This lane stays docs-scoped with no production workflow code edits by `@3design`.
	interface_contract_notes:
		- IFACE-QWB-001 project branch trigger contract.
		- IFACE-QWB-002 governance execution contract.
		- IFACE-QWB-003 docs policy validation contract.
		- IFACE-QWB-004 required-check identity contract.
		- IFACE-QWB-005 scope boundary contract.
		- IFACE-QWB-006 least-privilege permissions contract.
		- IFACE-QWB-007 downstream handoff traceability contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Governance-trigger designs stay executable when they separate lightweight branch-policy gates from full quality suites and encode required-check identity as an explicit contract.
		Root cause: Branch-trigger requests can drift into noisy CI expansion when gate scope and required-check semantics are not specified.
		Prevention: Define trigger boundary, fail-closed governance checks, and AC/IFACE traceability before planning.
		First seen: 2026-04-01
		Seen in: prj0000110-idea000004-quality-workflow-branch-trigger
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000109-idea000002-missing-compose-dockerfile
	state: DONE
	selected_design_path: Option B (incremental governance hardening around already-fixed compose Dockerfile path contract)
	assumptions:
		- `deploy/compose.yaml` and `deploy/Dockerfile.pyagent` remain the current runtime contract baseline.
		- This lane remains documentation-and-governance scoped with no deploy runtime edits.
		- Compose topology consolidation is deferred to the dedicated consolidation lane.
	interface_contract_notes:
		- IFACE-DC-001 compose file to Dockerfile path contract.
		- IFACE-DC-002 defect-lane scope guard contract.
		- IFACE-DC-003 regression signal contract.
		- IFACE-DC-004 handoff contract for @4plan traceability.
		- IFACE-DC-005 testability contract for @5test risk mapping.
		- IFACE-DC-006 non-goal boundary contract (no consolidation in this lane).
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Defect-lane design artifacts stay actionable when they explicitly lock non-goals and map interfaces to planned task IDs.
		Root cause: Stale or already-fixed defect lanes can drift into unnecessary implementation scope without explicit boundary contracts.
		Prevention: Encode non-goal boundaries, AC IDs, and interface-to-task traceability directly in the canonical design artifact before handoff.
		First seen: 2026-03-31
		Seen in: prj0000109-idea000002-missing-compose-dockerfile
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
	state: DONE
	selected_design_path: Option B (integrate CRDT FFI into existing rust_core PyO3 module with migration fallback gate)
	assumptions:
		- Existing rust_core PyO3/maturin path remains the canonical extension delivery channel.
		- Python merge facade in src/core/crdt_bridge.py remains contract-stable through migration.
		- Subprocess path is temporary fallback only and removed after parity/performance gates pass.
	interface_contract_notes:
		- IFACE-CRDT-001 stable Python merge facade and routing gate contract.
		- IFACE-CRDT-002 PyO3 boundary validation and typed response contract.
		- IFACE-CRDT-003 canonical payload codec round-trip equivalence contract.
		- IFACE-CRDT-004 deterministic CRDT merge engine contract.
		- IFACE-CRDT-005 Rust-to-Python error taxonomy mapping contract.
		- IFACE-CRDT-006 redacted observability contract for parity/latency outcomes.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md
	lesson:
		Pattern: FFI migration designs stay implementable when boundary contracts and parity rollback gates are defined before planning.
		Root cause: CRDT subprocess integrations accumulate latency and reliability risk when boundary contracts are implicit.
		Prevention: Lock Python facade, PyO3 boundary, codec, error taxonomy, and parity gates with AC IDs prior to @4plan handoff.
		First seen: 2026-03-31
		Seen in: prj0000108-idea000019-crdt-python-ffi-bindings
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000107-idea000015-specialized-agent-library
	state: DONE
	selected_design_path: Option B (hybrid specialization manifests + runtime adapters over universal shell)
	assumptions:
		- Specialization manifests are the authoritative source for adapter input contracts.
		- Runtime orchestration remains shell-driven while domain logic is bound through explicit `*Core` interfaces.
		- Policy allowlist and fail-closed fallback are mandatory release gates for specialization execution.
	interface_contract_notes:
		- IFACE-SAL-001 specialization registry schema/version resolution contract.
		- IFACE-SAL-002 deterministic manifest-to-shell adapter mapping contract.
		- IFACE-SAL-003 deny-by-default capability authorization contract.
		- IFACE-SAL-004 specialization-to-core binding contract.
		- IFACE-SAL-005 deterministic fail-closed fallback contract.
		- IFACE-SAL-006 redacted specialization telemetry contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md
	lesson:
		Pattern: Hybrid specialization designs stay actionable when adapter contracts, policy gates, and parity hooks are defined together.
		Root cause: Specialized-agent intent can stall when manifests and runtime orchestration are not connected by explicit interface contracts.
		Prevention: Lock adapter, policy, and fallback interfaces with AC IDs and interface-to-task traceability before @4plan handoff.
		First seen: 2026-03-30
		Seen in: prj0000107-idea000015-specialized-agent-library
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000106-idea000080-smart-prompt-routing-system
	state: DONE
	selected_design_path: Option B (hybrid guardrails + semantic classifier + bounded deterministic tie-break)
	assumptions:
		- Deterministic guardrails retain absolute precedence over classifier/tie-break outcomes.
		- Route decisions are promoted from shadow to active mode only after parity and latency gates pass.
		- Existing deterministic path remains available as operational fallback.
	interface_contract_notes:
		- IFACE-SPR-001 routing facade contract for total decision coverage.
		- IFACE-SPR-002 guardrail precedence invariant.
		- IFACE-SPR-003 classifier confidence + schema contract.
		- IFACE-SPR-004 deterministic tie-break + timeout contract.
		- IFACE-SPR-005 fail-closed fallback contract.
		- IFACE-SPR-006 redacted provenance telemetry contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md
	lesson:
		Pattern: Hybrid decision systems need explicit guardrail precedence and deterministic tie-break rules to stay testable.
		Root cause: Ambiguous prompt routing without staged control boundaries causes nondeterministic behavior and weak safety guarantees.
		Prevention: Enforce stage-order invariants, fixed tie-break determinism, and fail-closed fallback with provenance checks.
		First seen: 2026-03-30
		Seen in: prj0000106-idea000080-smart-prompt-routing-system
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000105-idea000016-mixin-architecture-base
	state: DONE
	selected_design_path: Option B (incremental migration with compatibility shims)
	assumptions:
		- Canonical base mixin namespace is introduced before broad host adoption.
		- Legacy shims are explicitly time-boxed to migration waves W1-W3.
		- @4plan will keep decomposition to roughly 10 code files and 10 test files as requested by workflow.
	interface_contract_notes:
		- IFACE-MX-001 canonical export determinism under src/core/base/mixins/.
		- IFACE-MX-002 host protocol requirements and validation hook contract.
		- IFACE-MX-003 legacy compatibility shim contract with deprecation signaling.
		- IFACE-MX-004 behavioral parity contract old vs canonical import paths.
		- IFACE-MX-005 shim expiry fail-closed governance gate.
		- IFACE-MX-006 migration observability event contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Explicit AC IDs plus interface-to-task traceability in design artifacts reduces @4plan ambiguity and rework.
		Root cause: Prior workflow stalls happen when architecture contracts exist without executable decomposition mapping.
		Prevention: Always include AC table and IFACE-to-task mapping block before @4plan handoff.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base
		Recurrence count: 2
		Promotion status: Promoted to hard rule

- task_id: prj0000104-idea000014-processing
	state: DONE
	selected_design_path: Option A (`pyproject.toml` canonical + deterministic generated `requirements.txt`)
	assumptions:
		- CI parity gate is authoritative and pre-commit is fast feedback.
		- Existing requirements-based install paths remain supported.
		- Heavy optional dependency extras migration is deferred.
	interface_contract_notes:
		- IFACE-C1 generation contract defined for deterministic output.
		- IFACE-C2 parity check contract defined for local/CI enforcement.
		- IFACE-C3 install compatibility contract preserves existing flows.
		- IFACE-C4 parity test contract covers drift/nondeterminism.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000104-idea000014-processing/idea000014-processing.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Design handoff quality improves when acceptance criteria and interface-to-task traceability are both explicit.
		Root cause: Prior handoffs can stall when interfaces are defined but not mapped to executable plan tasks.
		Prevention: Always include AC table with IDs and explicit IFACE-to-task mapping in the canonical design file.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing
		Recurrence count: 1
		Promotion status: Candidate


--- Appended from current ---

# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000122-jwt-refresh-token-support
	state: DONE
	selected_design_path: Option A (API-key bootstrap + file-backed refresh-session store + opaque rotating refresh tokens + short-lived access JWTs)
	assumptions:
		- Phase one targets the current single-instance backend deployment shape.
		- `PYAGENT_API_KEY` is the only bootstrap credential for managed sessions in this slice.
		- Legacy direct API-key and direct bearer-JWT auth paths remain backward compatible.
	interface_contract_notes:
		- IFACE-JRT-001 bootstrap endpoint contract.
		- IFACE-JRT-002 access JWT claim contract.
		- IFACE-JRT-003 opaque refresh-token hashing contract.
		- IFACE-JRT-004 file-backed persistence contract.
		- IFACE-JRT-005 single-use rotation contract.
		- IFACE-JRT-006 logout revocation contract.
		- IFACE-JRT-007 HTTP compatibility contract.
		- IFACE-JRT-008 WebSocket handshake-only auth contract.
		- IFACE-JRT-009 short-TTL bounded revocation contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0008-backend-managed-refresh-sessions-for-jwt-renewal.md
	lesson:
		Pattern: Backend auth upgrades stay implementation-ready when bootstrap identity and persistence durability are resolved explicitly before planning.
		Root cause: Refresh-token projects stall when teams leave initial session creation or storage durability as follow-up questions.
		Prevention: Lock the bootstrap credential, persistence boundary, revocation semantics, and IFACE-to-task traceability in the canonical design artifact before @4plan handoff.
		First seen: 2026-04-04
		Seen in: prj0000122-jwt-refresh-token-support
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000125-llm-gateway-lessons-learned-fixes
	state: DONE
	branch: prj0000125-llm-gateway-lessons-learned-fixes
	selected_design_path: 4-wave targeted remediation (A=runtime, B=tests, C=docs, D=naming record)
	assumptions:
		- No topology changes. Phase-one gateway architecture from prj0000124 is the baseline.
		- budget_manager.reserve() returns dict with "allowed" key; absent key treated as True.
		- Exception handling catches Exception subclasses only; BaseException non-Exception types propagate.
		- naming_standards.md takes precedence over copilot-instructions.md for module naming.
	interface_contract_notes:
		- handle() lifecycle: emit_start -> pre_policy -> budget_reserve (A1) -> cache/route/emit_decision -> provider_execute (A2) -> post_policy -> commit/cache_write/tool -> emit_result (A3) -> return
		- Result status: "success" | "denied" (pre-policy, budget, post-policy) | "failed" (provider exception)
		- telemetry.degraded=True set when emit_result raises; response still returned
		- Shared event_log fixture for all stub chronological ordering assertions
		- gateway_core.py: snake_case compliant with naming_standards.md; no rename
	key_decisions:
		- A1: budget_denied path: reservation.get("allowed", True) sentinel; fail-closed with budget_denied error envelope
		- A2: provider_exception: catch Exception, call commit_failure, return status="failed" envelope
		- A3: degraded telemetry: wrap emit_result, set telemetry.degraded=True on exception, always return
		- B1: replace stub_a.calls + stub_b.calls concatenation with shared event_log: list[str] injected into all stubs
		- C1: prj0000124 milestones all updated to DONE; status lane set to Done
		- C2: ADR 0009 Part 2 section appended; status Accepted unchanged
		- D1: gateway_core.py is COMPLIANT with naming_standards.md; NO RENAME
	handoff:
		target_agent: @4plan
		wave_order: A -> B -> C -> D(closed)
		canonical_artifact: docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.design.md
		adr_artifact: docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md (Part 2 appended)
		commit_sha: 1c16acfde6
	lesson:
		Pattern: Post-merge remediation projects require explicit fail-closed path audits before any implementation handoff.
		Root cause: Phase-one gateway slices ship happy-path contracts but leave budget-denied, exception, and telemetry-failure paths as implicit.
		Prevention: Require explicit fail-closed path table in design acceptance criteria with one pytest selector per path before @4plan handoff.
		First seen: 2026-04-04
		Seen in: prj0000125-llm-gateway-lessons-learned-fixes
		Recurrence count: 1
		Promotion status: Candidate

	state: DONE
	selected_design_path: Option C (Hybrid Split-Plane Gateway: Python control plane + Python-implemented Rust-ready data-plane contracts)
	assumptions:
		- Phase one remains in-process and prioritizes contract stability over deployment topology expansion.
		- Existing provider/routing/resilience/back-end modules are wrapped via explicit gateway interfaces instead of rewritten.
		- Fail-closed behavior is mandatory at policy/auth/budget/tool gates.
	interface_contract_notes:
		- IFACE-GW-001 GatewayCore orchestration contract.
		- IFACE-GW-002 GatewayPolicyEngine pre/post/tool policy contract.
		- IFACE-GW-003 GatewayRouter route-plan contract.
		- IFACE-GW-004 ProviderRuntimeAdapter execution contract.
		- IFACE-GW-005 GatewayBudgetManager reserve/commit contract.
		- IFACE-GW-006 GatewaySemanticCache lookup/write contract.
		- IFACE-GW-007 GatewayFallbackManager fallback-chain contract.
		- IFACE-GW-008 GatewayTelemetryEmitter correlation contract.
		- IFACE-GW-009 ToolSkillCatcher interception contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000124-llm-gateway/llm-gateway.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md
	lesson:
		Pattern: Split-plane gateway projects move faster when contracts are pinned to existing integration points and tied to explicit @4plan task IDs.
		Root cause: Planning drift appears when interface contracts are defined without concrete ownership mapping to integration modules.
		Prevention: Require interface-to-task traceability and acceptance-criteria IDs in the canonical design artifact before handoff.
		First seen: 2026-04-04
		Seen in: prj0000124-llm-gateway
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000127-mypy-strict-enforcement
	state: DONE
	branch: prj0000127-mypy-strict-enforcement
	selected_design_path: Option B (progressive blocking allowlist with warn->required CI promotion)
	assumptions:
		- Strict lane will be command-scoped to explicit config source and phase allowlist.
		- Broad mypy visibility lane remains non-blocking during early rollout.
		- Phase-1 module set is intentionally narrow to keep CI stability.
	interface_contract_notes:
		- IFACE-MYPY-001 strict lane command contract.
		- IFACE-MYPY-002 warning lane command contract.
		- IFACE-MYPY-003 allowlist registry contract.
		- IFACE-MYPY-004 promotion gate contract.
		- IFACE-MYPY-005 rollback contract.
		- IFACE-MYPY-006 config precedence assertion contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Progressive type-enforcement efforts stay executable when warn/required lane contracts, rollback rules, and allowlist drift checks are designed together.
		Root cause: Teams often define strictness goals without deterministic promotion and rollback mechanics, causing gate flapping and ad-hoc bypasses.
		Prevention: Require AC table + interface-to-task traceability + explicit failure taxonomy in design before @4plan handoff.
		First seen: 2026-04-04
		Seen in: prj0000127-mypy-strict-enforcement
		Recurrence count: 1
		Promotion status: Candidate


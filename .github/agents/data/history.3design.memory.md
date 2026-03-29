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

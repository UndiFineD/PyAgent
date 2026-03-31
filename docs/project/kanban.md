# PyAgent Project Kanban Board

_Last updated: 2026-03-31 | Total projects: 109 | Auto-synced by project_registry_governance.py (Discovery: 0, Review: 7, Released: 100)_

## How to use this board

This file is the **single source of truth** for all PyAgent projects across their full
lifecycle. It is maintained in source control alongside `data/projects.json` and updated
on every lane transition. Read this file before allocating a new project ID or starting
work on an existing project.

### Lanes

| Lane | Purpose | Entry trigger | Agent owner |
|---|---|---|---|
| Ideas | Proposed, not yet scoped | @0master adds placeholder | @0master |
| Discovery | Options exploration (@2think active) | @1project creates folder | @1project + @2think |
| Design | Architecture via @3design | .think.md is DONE | @3design |
| In Sprint | Active implementation (@4plan–@6code) | .design.md is DONE | @4plan–@6code |
| Review | PR open, awaiting merge | Branch pushed, PR opened | @9git |
| Released | Merged to main | PR merged | — |
| Archived | Stalled, cancelled, or superseded | @0master decision | @0master |

### How to advance a project

1. Update `data/projects.json` — change the `"lane"` field.
2. Move the row in this file from the old lane section to the new lane section.
3. Commit both files on the project-specific branch (or on main for Released/Archived transitions).
4. All Ideas → Discovery transitions must be authorised by `@0master` alongside project ID allocation.

### Governance rules

- `@0master` owns the `prjNNNNNNN` ID namespace. IDs are never reused.
- Budget tier and priority must be set before a project leaves the Ideas lane.
- Ideas placeholders use real IDs allocated by `@0master` before the project has a folder.
- The board is also queryable programmatically via `GET /api/projects` in the backend.

---

## Ideas

Projects proposed but not yet formally scoped.

Use the ordered implementation queue in the Future Ideas section to decide which idea
is promoted next into a `prjNNNNNNN` placeholder in this lane.

| ID | Name | Summary | Priority | Budget | Tags | Updated |
|---|---|---|---|---|---|---|
| prj0000103 | pending-definition | Allocated project ID pending formal project definition and branch assignment. | P3 | unknown | placeholder, project-id-allocation | 2026-03-30 |


---

## Discovery

Active options exploration — @2think is working or has completed .think.md.

| ID | Name | Summary | Branch | Priority | Budget | Tags | Updated |
|---|---|---|---|---|---|---|---|

---

## Design

@3design producing authoritative .design.md.

| ID | Name | Summary | Branch | Priority | Budget | Tags | Updated |
|---|---|---|---|---|---|---|---|

---

## In Sprint

Active implementation — @4plan through @6code are working.

| ID | Name | Summary | Branch | Priority | Budget | Updated |
|---|---|---|---|---|---|---|


---

## Review

PR open, awaiting merge.

| ID | Name | Branch | PR | Priority | Budget | Updated |
|---|---|---|---|---|---|---|
| prj0000100 | repo-cleanup-docs-code | prj0000100-repo-cleanup-docs-code | [#247](https://github.com/UndiFineD/PyAgent/pull/247) | P2 | L | 2026-03-29 |
| prj0000095 | source-stub-remediation | prj0000095-source-stub-remediation | pending | P2 | M | 2026-03-28 |


| prj0000094 | idea-003 - mypy-strict-enforcement | — | pending | P3 | S | 2026-03-29 |
| prj0000093 | projectmanager-ideas-autosync | prj0000093-projectmanager-ideas-autosync | pending | P2 | M | 2026-03-29 |
| prj0000101 | idea-013 - backend-health-check-endpoint | — | pending | P3 | S | 2026-03-30 |
| prj0000104 | idea000014-processing | prj0000104-idea000014-processing | pending | P2 | S | 2026-03-30 |
| prj0000109 | idea000002-missing-compose-dockerfile | prj0000109-idea000002-missing-compose-dockerfile | pending | P1 | S | 2026-03-31 |
---

## Released

All projects merged to main branch.

| ID | Name | Summary | Branch | PR | Priority | Budget | Released |
|---|---|---|---|---|---|---|---|
| prj0000099 | stub-module-elimination | Validation-first closure for stub-module-elimination with lifecycle artifacts completed and baseline pre-commit remediation integrated into @8ql/@9git handoff policy. | merged | [#245](https://github.com/UndiFineD/PyAgent/pull/245) | P2 | M | 2026-03-29 |
| prj0000097 | stub-module-elimination | Plan and execute elimination of stub modules and placeholders | merged | [#243](https://github.com/UndiFineD/PyAgent/pull/243) | P2 | M | 2026-03-29 |
| prj0000096 | coverage-minimum-enforcement | Enforce meaningful baseline coverage threshold in CI and prevent regression from effectively disabled coverage gate | merged | [#242](https://github.com/UndiFineD/PyAgent/pull/242) | P2 | M | 2026-03-29 |
| prj0000092 | mypy-strict-enforcement | Progressive mypy strictness enforcement starting in src/core with deterministic guardrails and phased rollout governance | merged | [#237](https://github.com/UndiFineD/PyAgent/pull/237) | P1 | M | 2026-03-28 |
| prj0000091 | missing-compose-dockerfile | Fix deploy compose reference to non-existent Dockerfile and restore clean-checkout compose viability | merged | [#235](https://github.com/UndiFineD/PyAgent/pull/235) [#236](https://github.com/UndiFineD/PyAgent/pull/236) | P1 | S | 2026-03-28 |
| prj0000090 | private-key-remediation | Remediate committed private key exposure, rotate compromised credentials, and add secret-scan guardrails in commit/CI workflows | merged | [#233](https://github.com/UndiFineD/PyAgent/pull/233) [#234](https://github.com/UndiFineD/PyAgent/pull/234) | P1 | M | 2026-03-28 |
| prj0000089 | agent-learning-loop | Agent learning-loop governance rollout across all role definitions plus quality-gate test remediations; pytest maxfail run stabilized | merged | [#231](https://github.com/UndiFineD/PyAgent/pull/231) | P2 | M | 2026-03-27 |
| prj0000088 | ai-fuzzing-security | Deterministic local fuzzing core with guarded mutation strategies, corpus scheduling, and safety policy; 99.06% cov | merged | [#230](https://github.com/UndiFineD/PyAgent/pull/230) | P3 | M | 2026-03-27 |
| prj0000087 | n8n-workflow-bridge | Bi-directional n8n bridge core with config, event adaptation, HTTP client, and mixin orchestration; 99.11% cov | merged | [#229](https://github.com/UndiFineD/PyAgent/pull/229) | P3 | M | 2026-03-27 |
| prj0000086 | universal-agent-shell | Universal shell facade v1 for intent routing, core registry, and shell orchestration; 96.26% cov | merged | [#228](https://github.com/UndiFineD/PyAgent/pull/228) | P2 | XL | 2026-03-27 |
| prj0000085 | shadow-mode-replay | Shadow execution + deterministic replay core with envelope/store/orchestrator and mixin integration; 98.34% cov | merged | [#227](https://github.com/UndiFineD/PyAgent/pull/227) | P3 | M | 2026-03-27 |
| prj0000084 | immutable-audit-trail | Append-only hashchain audit core with deterministic hashing, verification, and mixin integration; 99.36% cov | merged | [#226](https://github.com/UndiFineD/PyAgent/pull/226) | P2 | M | 2026-03-27 |
| prj0000083 | llm-circuit-breaker | Per-provider circuit breaker core with fallback routing and resilient call guardrails; 96.35% cov | merged | [#225](https://github.com/UndiFineD/PyAgent/pull/225) | P3 | S | 2026-03-27 |
| prj0000082 | agent-execution-sandbox | SandboxMixin + SandboxedStorageTransaction: path/network allowlist enforcement for agents; 32 tests 100% cov | merged | [#224](https://github.com/UndiFineD/PyAgent/pull/224) | P2 | S | 2026-03-26 |
| prj0000081 | mcp-server-ecosystem | MCP server hot-load registry with security sandboxing; McpClient JSON-RPC stdio, McpRegistry lifecycle, McpSandbox hardened spawn, McpToolAdapter; 33/33 tests 89.4% cov | merged | [#223](https://github.com/UndiFineD/PyAgent/pull/223) | P3 | L | 2026-03-26 |
| prj0000080 | cort-reasoning-pipeline | Chain-of-Recursive-Thoughts: N-round recursive self-critique with M temperature-variant alternatives; pure-heuristic EvaluationEngine; 33/33 tests 97.4% cov | merged | [#221](https://github.com/UndiFineD/PyAgent/pull/221) | P2 | M | 2026-03-26 |
| prj0000079 | automem-hybrid-search | AutoMem 9-component hybrid memory search (Vector+Graph+Temporal+Lexical+HNSW+AGE+LTREE+BRIN+Hash) on PostgreSQL; NebulaOS benchmark dashboard; app auto-discovery registry | merged | [#220](https://github.com/UndiFineD/PyAgent/pull/220) | P2 | L | 2026-03-26 |
| prj0000072 | websocket-reconnect-logic | Auto-reconnect with exponential backoff and jitter for frontend WebSocket drops; connection state indicator in NebulaOS | merged | [#209](https://github.com/UndiFineD/PyAgent/pull/209) | P3 | S | 2026-03-25 |
| prj0000044 | transaction-managers-stubs | CI stubs for StorageTransactionManager, ProcessTransactionManager, ContextTransactionManager — unblock test suite collection | merged | [#136](https://github.com/UndiFineD/PyAgent/pull/136) | P2 | S | 2026-03-22 |
| prj0000043 | p2p-security-deps | Upgrade libp2p 0.49→0.56 to remediate 6 Dependabot CVEs in P2P Rust stack | merged | — | P2 | M | 2026-03-23 |
| prj0000078 | pm-swot-risk-ui | Add SWOT Analysis and Risk Register toolbar buttons to Project Manager; `?raw` Vite import; modal overlay | merged | [#219](https://github.com/UndiFineD/PyAgent/pull/219) | P3 | S | 2026-03-26 |
| prj0000076 | future-ideas-kanban | Full workspace audit: 38 SWOT-prioritised future ideas added to kanban.md across 9 areas | merged | [#218](https://github.com/UndiFineD/PyAgent/pull/218) | P3 | M | 2026-03-26 |
| prj0000077 | ci-backend-deps | Add psutil, PyJWT, python-json-logger to requirements.txt; fix CodeQL QL query; fix kanban test counts | merged | [#216](https://github.com/UndiFineD/PyAgent/pull/216) [#217](https://github.com/UndiFineD/PyAgent/pull/217) | P1 | XS | 2026-03-26 |
| prj0000075 | ci-simplification | Delete 4 redundant workflows; expand CI to 10 shards; add security.yml CodeQL; fix yamux, picomatch, CodeQL, flake8 | merged | [#215](https://github.com/UndiFineD/PyAgent/pull/215) | P2 | S | 2026-03-26 |
| prj0000074 | workspace-meta-improvements | Moved agent memory/logs to .github/agents/data/, enforced docstrings policy, restructured docs/architecture, added SWOT+risk to kanban, expanded @2think depth | merged | [#212](https://github.com/UndiFineD/PyAgent/pull/212) | P2 | L | 2026-03-25 |
| prj0000073 | api-documentation | Hand-crafted API reference covering all backend REST endpoints, WebSocket protocol, authentication flows, and error codes in docs/api/ | merged | [#210](https://github.com/UndiFineD/PyAgent/pull/210) | P2 | M | 2026-03-25 |
| prj0000071 | dark-mode-accessibility | WCAG 2.1 AA remediation for NebulaOS dark theme: aria-labels, focus rings, contrast fix | merged | [#211](https://github.com/UndiFineD/PyAgent/pull/211) | P4 | S | 2026-03-25 |
| prj0000070 | opentelemetry-tracing | Distributed tracing with OpenTelemetry SDK across all backend requests | merged | #208 | P4 | M | 2026-03-25 |
| prj0000069 | ci-test-parallelization | Split pytest suite into parallel CI matrix buckets | merged | #207 | P3 | S | 2026-03-25 |
| prj0000068 | agent-timeout-watchdog | Per-agent execution timeout with graceful shutdown and dead-letter queue | merged | #206 | P3 | M | 2026-03-25 |
| prj0000067 | rust-file-watcher | Rust-powered filesystem watcher integrated into rust_core | merged | #205 | P4 | M | 2026-03-25 |
| prj0000066 | api-versioning | Versioned API routing (/api/v1/) with double include_router | merged | #204 | P3 | S | 2026-03-25 |
| prj0000065 | agent-memory-persistence | Persist agent conversation context across sessions | merged | #203 | P3 | M | 2026-03-25 |
| prj0000064 | rate-limiting-middleware | Token-bucket rate limiting middleware on all FastAPI REST endpoints | merged | #202 | P3 | S | 2026-03-25 |
| prj0000063 | structured-logging | JSON structured logging with correlation IDs across all backend requests | merged | #201 | P4 | S | 2026-03-25 |
| prj0000062 | live-agent-execution-in-codebuilder | Wire 10-agent pipeline to CodeBuilder UI with streaming logs | merged | #200 | P4 | unknown | 2026-03-25 |
| prj0000061 | theme-system | Light mode and retro terminal theme for NebulaOS | merged | #199 | P4 | unknown | 2026-03-25 |
| prj0000060 | flm-token-throughput-dashboard | Real-time tokens-per-second charts fed from FLM telemetry | merged | #198 | P4 | unknown | 2026-03-25 |
| prj0000059 | plugin-marketplace-browser | In-NebulaOS panel for discovering and managing third-party agent plugins | merged | #197 | P4 | unknown | 2026-03-25 |
| prj0000058 | mobile-responsive-nebula-os | CSS responsive breakpoints and touch-friendly NebulaOS shell | merged | #196 | P4 | unknown | 2026-03-25 |
| prj0000057 | agent-orchestration-graph | Visual DAG panel in NebulaOS showing live task flow | merged | #195 | P4 | unknown | 2026-03-25 |
| prj0000056 | rust-async-transport-activation | Enable async-transport feature in rust_core for QUIC-over-Tokio | merged | #194 | P4 | unknown | 2026-03-25 |
| prj0000055 | websocket-e2e-encryption | X25519 ECDH + AES-256-GCM per-session forward secrecy on WebSocket | merged | #193 | P2 | M | 2026-03-25 |
| prj0000054 | backend-authentication | API-key and JWT authentication for all REST and WebSocket endpoints | merged | #192 | P2 | M | 2026-03-25 |
| prj0000053 | hmac-webhook-verification | HMAC-SHA256 signature validation for GitHub webhook payloads | merged | #191 | P2 | S | 2026-03-25 |
| prj0000052 | project-management | Kanban lifecycle board, projects.json registry, and /api/projects endpoint | merged | #190 | P2 | L | 2026-03-25 |
| prj0000051 | readme-update | Comprehensive README rewrite with NebulaOS screenshot and Future Roadmap | merged | #189 | P2 | M | 2026-03-22 |
| prj0000050 | install-script | Cross-platform install.ps1 environment bootstrap for dev onboarding | merged | #188 | P2 | S | 2026-03-20 |
| prj0000049 | dependabot-security-fixes | Apply Dependabot-flagged security fixes across Python and JS dependencies | merged | #187 | P2 | S | 2026-03-18 |
| prj0000048 | taskbar-config | Taskbar always-visible toggle in NebulaOS settings modal | merged | #186 | P2 | S | 2026-03-15 |
| prj0000047 | conky-real-metrics | Wire NebulaOS Conky panel to live /api/metrics/system endpoint with charts | merged | #185 | P2 | M | 2026-03-15 |
| prj0000045 | transaction-managers-full | Full implementation of all four transaction managers | merged | #137 | P2 | L | 2026-03-10 |
| prj0000042 | agent-workflow-polish | Agent workflow refinements: error handling improvements and state logging | merged | — | P3 | S | 2026-01-01 |
| prj0000041 | flm-benchmark | FLM benchmark harness: latency, throughput, and accuracy scoring | merged | — | P3 | M | 2026-01-01 |
| prj0000040 | flm-integration | FLM OpenAI-compatible chat adapter and deterministic tool-call loop | merged | — | P3 | M | 2026-01-01 |
| prj0000039 | conftest-typing-fixes | Fix conftest.py type annotations to unblock full test suite execution | merged | — | P3 | S | 2026-01-01 |
| prj0000038 | project-management-v1 | Initial project management tooling: folder structure, stub generator, registry | merged | — | P3 | M | 2026-01-01 |
| prj0000037 | tools-crdt-security | CRDT security tooling: P2P security deps, libp2p integration, encryption layer | merged | — | P3 | M | 2026-01-01 |
| prj0000036 | standards-release | Release process: semver policy, changelog format, tagging convention | merged | — | P3 | XS | 2026-01-01 |
| prj0000035 | standards-ci | CI workflow design standards: job naming, matrix strategy, artifact retention | merged | — | P3 | S | 2026-01-01 |
| prj0000034 | standards-docs | Documentation standards: structure, markdown lint rules, header requirements | merged | — | P3 | XS | 2026-01-01 |
| prj0000033 | standards-security | OWASP alignment, input validation policy, allowlist patterns, and SBOM process | merged | — | P3 | S | 2026-01-01 |
| prj0000032 | standards-test-style | pytest conventions, fixture patterns, test coverage targets, and naming rules | merged | — | P3 | XS | 2026-01-01 |
| prj0000031 | standards-commit-style | Conventional commits standard, commit message template, and pre-commit hook | merged | — | P3 | XS | 2026-01-01 |
| prj0000030 | standards-code-style | Python/Rust/TS style guide: max-line 120, PascalCase modules, flake8 config | merged | — | P3 | XS | 2026-01-01 |
| prj0000029 | performance-docs | Performance benchmarking methodology, baseline results, and optimization notes | merged | — | P3 | S | 2026-01-01 |
| prj0000028 | api-reference | Auto-generated and hand-curated API reference docs for backend and core | merged | — | P3 | S | 2026-01-01 |
| prj0000027 | onboarding-docs | Developer onboarding guide: environment setup, first PR walkthrough | merged | — | P3 | S | 2026-01-01 |
| prj0000026 | architecture-adr-template | Architecture Decision Record template and initial ADR for async runtime | merged | — | P3 | S | 2026-01-01 |
| prj0000025 | contributing-guide | CONTRIBUTING.md with PR workflow, DCO, and branch naming instructions | merged | — | P3 | S | 2026-01-01 |
| prj0000024 | code-of-conduct | Contributor Code of Conduct (Contributor Covenant v2.1) | merged | — | P3 | XS | 2026-01-01 |
| prj0000023 | naming-standards | PascalCase module naming convention, file-rename tracker, and migration guide | merged | — | P3 | S | 2026-01-01 |
| prj0000022 | external-repos-tracking | External repository tracking list and dependency provenance notes | merged | — | P3 | S | 2026-01-01 |
| prj0000021 | project-management-governance | PRINCE2/agile hybrid governance model, project doc conventions, and audit trail | merged | — | P3 | M | 2026-01-01 |
| prj0000020 | github-import | GitHub import system: webhook handler, repo sync, and PR ingestion | merged | — | P3 | M | 2026-01-01 |
| prj0000019 | future-roadmap | Research notes and long-horizon planning artifacts for roadmap items | merged | — | P3 | S | 2026-01-01 |
| prj0000018 | documentation-assets | MkDocs config, Mermaid/PlantUML diagram assets, and doc build scripts | merged | — | P3 | M | 2026-01-01 |
| prj0000017 | dev-tools-utilities | Shared utilities for dev tools: path helpers, config loaders, formatters | merged | — | P3 | M | 2026-01-01 |
| prj0000016 | dev-tools-structure | File layout and modular structure for src/tools/ package | merged | — | P3 | M | 2026-01-01 |
| prj0000015 | dev-tools-implementation | Full implementation of code improvement pipeline tools | merged | — | P3 | M | 2026-01-01 |
| prj0000014 | dev-tools-capabilities | Expanded dev tool capabilities: static analysis, complexity metrics | merged | — | P3 | M | 2026-01-01 |
| prj0000013 | dev-tools-autonomy | Autonomous dev tooling: dependency audit, self-healing scripts | merged | — | P3 | M | 2026-01-01 |
| prj0000012 | deployment-operations | Docker compose, Dockerfile, and provisioning scripts for production deploy | merged | — | P3 | M | 2026-01-01 |
| prj0000011 | core-project-structure | Canonical src/ layout, __init__.py ordering, and import path standardization | merged | — | P3 | M | 2026-01-01 |
| prj0000010 | context-management | ContextManager windowing, SkillsRegistry, and integration smoke tests | merged | — | P3 | M | 2026-01-01 |
| prj0000009 | community-collaboration | Community contribution guidelines, issue templates, and team governance docs | merged | — | P3 | M | 2026-01-01 |
| prj0000008 | agent-workflow | Task state machine, WorkflowEngine, and agent handoff protocol | merged | — | P3 | M | 2026-01-01 |
| prj0000007 | advanced-research | Research notes, long-horizon planning artifacts, and literature review | merged | — | P3 | M | 2026-01-01 |
| prj0000006 | unified-transaction-manager | MemoryTransaction, StorageTransaction, ProcessTransaction, ContextTransaction managers | merged | — | P3 | M | 2026-01-01 |
| prj0000005 | llm-swarm-architecture | Multi-agent swarm coordination: AgentRegistry, TaskScheduler, SwarmMemory | merged | — | P3 | M | 2026-01-01 |
| prj0000004 | llm-context-consolidation | Unified LLM context window management and ContextManager implementation | merged | — | P3 | M | 2026-01-01 |
| prj0000003 | hybrid-llm-security | Hybrid LLM security core: Rust encryption, transactions, key rotation | merged | — | P3 | M | 2026-01-01 |
| prj0000002 | core-system | Core runtime modules: task_queue, agent_registry, memory, observability scaffold | merged | — | P3 | M | 2026-01-01 |
| prj0000001 | async-runtime | Tokio-backed async helpers and PyO3 bindings for non-blocking agent ops | merged | — | P3 | M | 2026-01-01 |

| prj0000098 | backend-health-check-endpoint | Initialize project from idea000013 to design and deliver backend health-check endpoint governance and implementation planning | merged | [#244](https://github.com/UndiFineD/PyAgent/pull/244) | P2 | M | 2026-03-29 |
| prj0000102 | idea-014 - pyproject-requirements-sync | This idea focuses on pyproject requirements sync in area 9 – Dependencies. The current signal indicates priority P2, impact M, and urgency M. The SWOT tag is W (Weakness in current implementation). | merged | [#251](https://github.com/UndiFineD/PyAgent/pull/251) [#252](https://github.com/UndiFineD/PyAgent/pull/252) | P3 | S | 2026-03-30 |
| prj0000105 | idea-016 - mixin-architecture-base | This idea focuses on mixin architecture base in area 1 – Python agents. The current signal indicates priority P3, impact H, and urgency M. The SWOT tag is W (Weakness in current implementation). | merged | [#258](https://github.com/UndiFineD/PyAgent/pull/258) | P3 | S | 2026-03-30 |
| prj0000106 | idea000080-smart-prompt-routing-system | Initialize workflow artifacts for idea000080 smart prompt routing system and hand off to @2think discovery. | merged | [#259](https://github.com/UndiFineD/PyAgent/pull/259) | P2 | M | 2026-03-30 |
| prj0000107 | idea000015-specialized-agent-library | Initialize workflow artifacts for idea000015 specialized agent library and hand off to @2think discovery. | merged | [#260](https://github.com/UndiFineD/PyAgent/pull/260) | P2 | M | 2026-03-31 |
| prj0000108 | idea000019-crdt-python-ffi-bindings | Initialize workflow artifacts for idea000019 crdt-python-ffi-bindings and hand off to @2think discovery. | merged | [#261](https://github.com/UndiFineD/PyAgent/pull/261) | P3 | S | 2026-03-31 |
---

## Archived

Stalled, cancelled, or superseded projects.

| ID | Name | Summary | Reason | Updated |
|---|---|---|---|---|
| prj0000046 | flm-tps-benchmark | Per-provider tokens-per-second metrics harness for FLM endpoint evaluation | FLM server offline; superseded by prj0000060 (FLM Token Throughput Dashboard) | 2026-03-24 |

---

## Summary Metrics

| Lane | Count |
|---|---|
| Ideas | 1 |
| Discovery | 0 |
| Design | 0 |
| In Sprint | 0 |
| Review | 7 |
| Released | 100 |
| Archived | 1 |
| **Total** | **109** |

---

## Risk Register

Active risks for the PyAgent project. Update on every sprint start.

| ID | Risk | Likelihood | Impact | Status | Mitigation |
|---|---|---|---|---|---|
| RSK-001 | Agent branch mismatch causes commits on wrong branch | M | H | Mitigated | Pre-commit hook `scripts/enforce_branch.py`; branch gate in all agent definitions |
| RSK-002 | Stale architecture docs mislead agents | H | M | Open | prj0000074: restructure docs/architecture/ to ≤8 numbered files; @6code updates on each PR |
| RSK-003 | WCAG regressions introduced in future UI work | M | M | Mitigated | `tests/web/test_a11y_checklist.py` runs in CI |
| RSK-004 | WebSocket reconnect loses messages during reconnect window | L | M | Mitigated | prj0000072 exponential-backoff + state recovery |
| RSK-005 | JWT secret left at default (`dev`) in production | H | H | Open | `PYAGENT_JWT_SECRET` env var required; backend warns if unset; add CI secret-scanning rule |

---

## SWOT Analysis

Global SWOT for the PyAgent project as of 2026-03-25.

| | **Helpful** | **Harmful** |
|---|---|---|
| **Internal** | **Strengths** | **Weaknesses** |
| | Multi-agent swarm with clear role separation | Agent workflow artifacts are manual; no automated quality gate |
| | Transactional safety (rollback on failure) | Architecture docs historically bloated with stubs and generated files |
| | Rust-accelerated hot paths via PyO3 | No ruff D-code enforcement; docstrings are inconsistent |
| | Rich project tracking (kanban + projects.json + API) | Pre-commit hook not enforced in all CI paths |
| **External** | **Opportunities** | **Threats** |
| | AI tooling improving rapidly — agents can be upgraded with new models | LLM API drift may break tool call contracts |
| | WCAG compliance creates accessible, production-ready UI for demos | Open-source forks may diverge without upstream sync policy |
| | Rust FFI bridge enables near-native performance at Python ergonomics | Key contributor concentration risk (single-repo autonomy) |
| | Community interest in multi-agent workflow tooling growing | Dependabot alerts require timely remediation (1 high open) |
## Future Ideas

Implementation queue sourced from docs/project/ideas/, ordered by importance for execution planning.
Promote ideas from this queue into the Ideas lane as prjNNNNNNN placeholders before Discovery handoff.

Total idea files ordered: 78

| Rank | Idea | Importance | Source file |
|---|---|---|---|
| 1 | idea-001 - private-key-in-repo | Critical | docs/project/ideas/idea000001-private-key-in-repo.md |
| 2 | idea-002 - missing-compose-dockerfile | Critical | docs/project/ideas/idea000002-missing-compose-dockerfile.md |
| 3 | idea-003 - mypy-strict-enforcement | Critical | docs/project/ideas/idea000003-mypy-strict-enforcement.md |
| 4 | idea-004 - quality-workflow-branch-trigger | Critical | docs/project/ideas/idea000004-quality-workflow-branch-trigger.md |
| 5 | idea-005 - rust-ci-workflow | Critical | docs/project/ideas/idea000005-rust-ci-workflow.md |
| 6 | idea-006 - codeql-ci-integration | Critical | docs/project/ideas/idea000006-codeql-ci-integration.md |
| 7 | idea-007 - security-scanning-ci | Critical | docs/project/ideas/idea000007-security-scanning-ci.md |
| 8 | idea-009 - requirements-ci-deduplication | Critical | docs/project/ideas/idea000009-requirements-ci-deduplication.md |
| 9 | idea-013 - backend-health-check-endpoint | Critical | docs/project/ideas/idea000013-backend-health-check-endpoint.md |
| 10 | idea-008 - coverage-minimum-enforcement | High | docs/project/ideas/idea000008-coverage-minimum-enforcement.md |
| 11 | idea-010 - docker-compose-consolidation | High | docs/project/ideas/idea000010-docker-compose-consolidation.md |
| 12 | idea-011 - stub-module-elimination | High | docs/project/ideas/idea000011-stub-module-elimination.md |
| 13 | idea-012 - dependabot-renovate | High | docs/project/ideas/idea000012-dependabot-renovate.md |
| 14 | idea-014 - pyproject-requirements-sync | High | docs/project/ideas/idea000014-pyproject-requirements-sync.md |
| 15 | idea-015 - specialized-agent-library | High | docs/project/ideas/idea000015-specialized-agent-library.md |
| 16 | idea-027 - windows-ci-matrix | High | docs/project/ideas/idea000027-windows-ci-matrix.md |
| 17 | idea-031 - automated-api-docs-ci | High | docs/project/ideas/idea000031-automated-api-docs-ci.md |
| 18 | idea-051 - loop-analysis-ci-gate | High | docs/project/ideas/idea000051-loop-analysis-ci-gate.md |
| 19 | idea-055 - e2e-encryption | High | docs/project/ideas/idea000055-e2e-encryption.md |
| 20 | idea-058 - improvement-audit-plan | High | docs/project/ideas/idea000058-improvement-audit-plan.md |
| 21 | idea-060 - onboarding | High | docs/project/ideas/idea000060-onboarding.md |
| 22 | idea-066 - setup | High | docs/project/ideas/idea000066-setup.md |
| 23 | idea-068 - test-quality | High | docs/project/ideas/idea000068-test-quality.md |
| 24 | idea-070 - transaction-manager-architecture | High | docs/project/ideas/idea000070-transaction-manager-architecture.md |
| 25 | idea-071 - v4-release-status | High | docs/project/ideas/idea000071-v4-release-status.md |
| 26 | idea-078 - installation-docs | High | docs/project/ideas/idea000078-installation-docs.md |
| 27 | idea-016 - mixin-architecture-base | Medium | docs/project/ideas/idea000016-mixin-architecture-base.md |
| 28 | idea-017 - rust-criterion-benchmarks | Medium | docs/project/ideas/idea000017-rust-criterion-benchmarks.md |
| 29 | idea-018 - rust-sub-crate-unification | Medium | docs/project/ideas/idea000018-rust-sub-crate-unification.md |
| 30 | idea-019 - crdt-python-ffi-bindings | Medium | docs/project/ideas/idea000019-crdt-python-ffi-bindings.md |
| 31 | idea-020 - amd-npu-feature-documentation | Medium | docs/project/ideas/idea000020-amd-npu-feature-documentation.md |
| 32 | idea-021 - openapi-spec-generation | Medium | docs/project/ideas/idea000021-openapi-spec-generation.md |
| 33 | idea-022 - jwt-refresh-token-support | Medium | docs/project/ideas/idea000022-jwt-refresh-token-support.md |
| 34 | idea-023 - tailwind-config-missing | Medium | docs/project/ideas/idea000023-tailwind-config-missing.md |
| 35 | idea-024 - frontend-e2e-tests | Medium | docs/project/ideas/idea000024-frontend-e2e-tests.md |
| 36 | idea-025 - global-state-management | Medium | docs/project/ideas/idea000025-global-state-management.md |
| 37 | idea-026 - frontend-url-routing | Medium | docs/project/ideas/idea000026-frontend-url-routing.md |
| 38 | idea-028 - property-based-test-expansion | Medium | docs/project/ideas/idea000028-property-based-test-expansion.md |
| 39 | idea-029 - backend-integration-test-suite | Medium | docs/project/ideas/idea000029-backend-integration-test-suite.md |
| 40 | idea-030 - adr-backfill | Medium | docs/project/ideas/idea000030-adr-backfill.md |
| 41 | idea-032 - changelog-automation | Medium | docs/project/ideas/idea000032-changelog-automation.md |
| 42 | idea-033 - pre-commit-ruff-version-drift | Medium | docs/project/ideas/idea000033-pre-commit-ruff-version-drift.md |
| 43 | idea-034 - projects-json-schema-validation | Medium | docs/project/ideas/idea000034-projects-json-schema-validation.md |
| 44 | idea-035 - torch-optional-dependency-split | Medium | docs/project/ideas/idea000035-torch-optional-dependency-split.md |
| 45 | idea-039 - p2p-swarm-consensus-completion | Medium | docs/project/ideas/idea000039-p2p-swarm-consensus-completion.md |
| 46 | idea-040 - resource-synergy-cross-node-scheduling | Medium | docs/project/ideas/idea000040-resource-synergy-cross-node-scheduling.md |
| 47 | idea-041 - kv-v2-cache-rollout | Medium | docs/project/ideas/idea000041-kv-v2-cache-rollout.md |
| 48 | idea-042 - semantic-cache-invalidation-engine | Medium | docs/project/ideas/idea000042-semantic-cache-invalidation-engine.md |
| 49 | idea-043 - neural-context-pruning-heuristics | Medium | docs/project/ideas/idea000043-neural-context-pruning-heuristics.md |
| 50 | idea-044 - zero-downtime-resharding-protocol | Medium | docs/project/ideas/idea000044-zero-downtime-resharding-protocol.md |
| 51 | idea-045 - governance-safety-hub-implementation | Medium | docs/project/ideas/idea000045-governance-safety-hub-implementation.md |
| 52 | idea-046 - distributed-checkpointing-recovery | Medium | docs/project/ideas/idea000046-distributed-checkpointing-recovery.md |
| 53 | idea-047 - neural-scam-phishing-detection | Medium | docs/project/ideas/idea000047-neural-scam-phishing-detection.md |
| 54 | idea-048 - global-trace-synthesis-dashboard | Medium | docs/project/ideas/idea000048-global-trace-synthesis-dashboard.md |
| 55 | idea-049 - ucp-agentic-commerce-adapter | Medium | docs/project/ideas/idea000049-ucp-agentic-commerce-adapter.md |
| 56 | idea-050 - inference-speculative-decoding-runtime | Medium | docs/project/ideas/idea000050-inference-speculative-decoding-runtime.md |
| 57 | idea-052 - auto-fix | Medium | docs/project/ideas/idea000052-auto-fix.md |
| 58 | idea-053 - comparison-vllm-old | Medium | docs/project/ideas/idea000053-comparison-vllm-old.md |
| 59 | idea-054 - core-design-guide | Medium | docs/project/ideas/idea000054-core-design-guide.md |
| 60 | idea-056 - e2e-implementation-summary | Medium | docs/project/ideas/idea000056-e2e-implementation-summary.md |
| 61 | idea-057 - fleet-auto-doc | Medium | docs/project/ideas/idea000057-fleet-auto-doc.md |
| 62 | idea-061 - phase41-vllm-patterns | Medium | docs/project/ideas/idea000061-phase41-vllm-patterns.md |
| 63 | idea-062 - progress-dashboard | Medium | docs/project/ideas/idea000062-progress-dashboard.md |
| 64 | idea-063 - release-notes-template | Medium | docs/project/ideas/idea000063-release-notes-template.md |
| 65 | idea-065 - rust-ready | Medium | docs/project/ideas/idea000065-rust-ready.md |
| 66 | idea-067 - streaming-website | Medium | docs/project/ideas/idea000067-streaming-website.md |
| 67 | idea-069 - tools | Medium | docs/project/ideas/idea000069-tools.md |
| 68 | idea-073 - standards-docs | Medium | docs/project/ideas/idea000073-standards-docs.md |
| 69 | idea-076 - performance-docs | Medium | docs/project/ideas/idea000076-performance-docs.md |
| 70 | idea-036 - rl-module-implementation | Low | docs/project/ideas/idea000036-rl-module-implementation.md |
| 71 | idea-037 - docs-work-folder-cleanup | Low | docs/project/ideas/idea000037-docs-work-folder-cleanup.md |
| 72 | idea-038 - chromadb-optional-extra | Low | docs/project/ideas/idea000038-chromadb-optional-extra.md |
| 73 | idea-059 - improvement-research | Low | docs/project/ideas/idea000059-improvement-research.md |
| 74 | idea-064 - research-notes | Low | docs/project/ideas/idea000064-research-notes.md |
| 75 | idea-072 - work-docs | Low | docs/project/ideas/idea000072-work-docs.md |
| 76 | idea-074 - research-docs | Low | docs/project/ideas/idea000074-research-docs.md |
| 77 | idea-075 - prompt-docs | Low | docs/project/ideas/idea000075-prompt-docs.md |
| 78 | idea-077 - key-docs | Low | docs/project/ideas/idea000077-key-docs.md |

### Priority distribution

| Importance | Count |
|---|---|
| Critical | 9 |
| High | 17 |
| Medium | 43 |
| Low | 9 |

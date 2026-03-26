# PyAgent Project Kanban Board

_Last updated: 2026-03-26 | Total projects: 88_

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

| ID | Name | Summary | Priority | Budget | Tags | Updated |
|---|---|---|---|---|---|---|
| prj0000079 | automem-hybrid-search | AutoMem 9-component hybrid memory search (Vector+Graph+Temporal+Lexical) with FalkorDB & Qdrant; 90%+ LoCoMo benchmark target | P2 | L | memory, search, rust | 2026-03-26 |
| prj0000080 | cort-reasoning-pipeline | Chain-of-Recursive-Thoughts: multi-round recursive reasoning with dynamic evaluation engine and temperature-variant alternative generation | P2 | M | reasoning, ai, core | 2026-03-26 |
| prj0000081 | mcp-server-ecosystem | MCP server hot-load registry with security sandboxing; enables agents to dynamically connect to 500+ community MCP servers | P3 | L | tools, mcp, ecosystem | 2026-03-26 |
| prj0000082 | agent-execution-sandbox | SandboxMixin: restrict each agent's file and network access to approved path sets; integrated with StateTransaction validation | P2 | S | security, sandbox, core | 2026-03-26 |
| prj0000083 | llm-circuit-breaker | Per-provider LLM request circuit breaker with configurable failure thresholds, exponential backoff, and fallback model routing | P3 | S | resilience, llm, infrastructure | 2026-03-26 |
| prj0000084 | immutable-audit-trail | Append-only hashchain audit log for all BFT-approved and security-critical operations; tamper-evident with cryptographic chaining | P2 | M | security, audit, compliance | 2026-03-26 |
| prj0000085 | shadow-mode-replay | Shadow execution mode (side-effect-free parallel agent runs) + deterministic session replay from structured logs for debug | P3 | M | testing, debug, observability | 2026-03-26 |
| prj0000086 | universal-agent-shell | UniversalAgent shell: dynamically load CoderCore/SecurityCore/etc. by intent; consolidate 50+ specialized agent classes | P2 | XL | architecture, agents, refactor | 2026-03-26 |
| prj0000087 | n8n-workflow-bridge | Bi-directional n8n integration: agents trigger automation chains via n8n API and act as intelligent decision nodes in workflows | P3 | M | automation, integration, n8n | 2026-03-26 |
| prj0000088 | ai-fuzzing-security | Brainstorm AI fuzzing engine: learning-based path discovery, multi-cycle security testing, local Ollama model integration | P3 | M | security, testing, ai | 2026-03-26 |

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
| prj0000072 | websocket-reconnect-logic | prj0000072-websocket-reconnect-logic | [#209](https://github.com/UndiFineD/PyAgent/pull/209) | P3 | S | 2026-03-25 |
| prj0000043 | p2p-security-deps | prj0000043-p2p-security-deps | open | P2 | M | 2026-03-24 |
| prj0000044 | transaction-managers-stubs | prj0000044-transaction-managers-stubs | #136 | P2 | S | 2026-03-24 |

---

## Released

All projects merged to main branch.

| ID | Name | Summary | Branch | PR | Priority | Budget | Released |
|---|---|---|---|---|---|---|---|
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
| Ideas | 0 |
| Discovery | 0 |
| Design | 0 |
| In Sprint | 0 |
| Review | 3 |
| Released | 74 |
| Archived | 1 |
| **Total** | **78** |

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

Ideas surfaced by the @2think workspace audit (prj0000076, 2026-03-26).
38 total ideas across 9 areas. P1/P2 include SWOT classification.
These are not active projects — they are candidates for future sprints.

| ID | Area | Name | Priority | Impact | Urgency | SWOT | Description |
|---|---|---|---|---|---|---|---|
| idea-001 | 8 – Data/Deploy | private-key-in-repo | P1 | H | H | T | `rust_core/2026-03-11-keys.priv` is a private cryptographic key committed to the repository. Any clone leaks the secret; rotate immediately and add a pre-commit secret-scan hook. |
| idea-002 | 8 – Data/Deploy | missing-compose-dockerfile | P1 | H | H | W | `deploy/compose.yaml` references `src/infrastructure/docker/Dockerfile` which does not exist. This makes the primary compose target fully broken on clean checkout. |
| idea-003 | 1 – Python agents | mypy-strict-enforcement | P1 | H | H | W | `mypy.ini` sets `strict = False` and `ignore_errors = True`, rendering all type annotations decorative. Progressive mypy strictness should be enabled starting with the `src/core/` package. |
| idea-004 | 7 – CI | quality-workflow-branch-trigger | P2 | H | H | W | `quality.yml` only triggers on `prj0000026-*` branch pattern (an archived project) plus `main`. All PRs to any `prj*` branch skip the quality gate entirely. |
| idea-005 | 7 – CI | rust-ci-workflow | P2 | H | H | W | No GitHub Actions workflow runs `cargo clippy`, `cargo test`, or `cargo audit` for `rust_core/`. Rust regressions are only caught indirectly through Python FFI tests. |
| idea-006 | 7 – CI | codeql-ci-integration | P2 | H | H | O | A `codeql/` directory containing custom Python and Rust queries exists but is never executed in CI. Wiring it into a CodeQL workflow would activate static security analysis for free. |
| idea-007 | 7 – CI | security-scanning-ci | P2 | H | H | T | No `pip-audit`, `safety`, or Dependabot/Renovate integration exists. `pip_audit_results.json` is committed manually (stale). Automated vuln scanning should run on every push to `main`. |
| idea-008 | 5 – Tests | coverage-minimum-enforcement | P2 | H | H | W | `quality.yml` passes `--cov-fail-under=1`, which is effectively no threshold. Setting a meaningful baseline (≥70%) and iteratively raising it would prevent coverage regressions. |
| idea-009 | 9 – Dependencies | requirements-ci-deduplication | P2 | M | H | W | `pytest-xdist>=3.6` appears twice in `requirements-ci.txt`. Duplicate lines indicate the file is not mechanically validated; add a structure test to catch this. |
| idea-010 | 8 – Data/Deploy | docker-compose-consolidation | P2 | M | H | W | Two independent Docker Compose files exist (`deploy/compose.yaml` and `deploy/docker-compose.yaml`) with different service topologies. Consolidate into one parameterised file. |
| idea-011 | 1 – Python agents | stub-module-elimination | P2 | H | M | W | At least 6 modules (`src/rl/`, `src/speculation/`, `src/cort/`, `src/runtime_py/`, `src/runtime/`, `src/memory/`) contain only an empty `__init__.py`. These should be implemented or removed. |
| idea-012 | 7 – CI | dependabot-renovate | P2 | M | M | O | No automated dependency update bot (Dependabot or Renovate) is configured. Adding `.github/dependabot.yml` would auto-raise PRs for Python, npm, and Rust dependency bumps. |
| idea-013 | 3 – Backend | backend-health-check-endpoint | P2 | M | H | W | No `/health`, `/readyz`, or `/livez` endpoint is visible in `backend/app.py`. Container orchestrators require a health endpoint to manage service availability. |
| idea-014 | 9 – Dependencies | pyproject-requirements-sync | P2 | M | M | W | `pyproject.toml` and `requirements.txt` pin different versions for several packages. Two divergent install paths create "works on my machine" failures. |
| idea-015 | 1 – Python agents | specialized-agent-library | P3 | H | M | O | `src/agents/` contains only `BaseAgent.py`. The `docs/AGENTS.md` catalogue lists many specialized agents that have no Python-side implementation — only `.agent.md` definitions consumed by Copilot. |
| idea-016 | 1 – Python agents | mixin-architecture-base | P3 | H | M | W | `copilot-instructions.md` mandates a mixin architecture in `src/core/base/mixins/`, but that directory does not exist. `src/core/base/__init__.py` is a near-empty placeholder. |
| idea-017 | 2 – Rust core | rust-criterion-benchmarks | P3 | H | M | O | `performance/metrics_bench.py` benchmarks Rust through Python. No Rust-side `criterion` benchmarks exist, making it impossible to detect performance regressions at the Rust layer. |
| idea-018 | 2 – Rust core | rust-sub-crate-unification | P3 | M | M | W | `rust_core/crdt/`, `rust_core/p2p/`, and `rust_core/security/` are standalone Cargo crates with separate `Cargo.lock` files. Consider a Cargo workspace to unify the dependency graph. |
| idea-019 | 2 – Rust core | crdt-python-ffi-bindings | P3 | H | M | O | The CRDT sub-crate (`rust_core/crdt/`) builds a standalone binary but exposes no PyO3 bindings. `src/core/crdt_bridge.py` implies FFI was planned but not completed. |
| idea-020 | 2 – Rust core | amd-npu-feature-documentation | P3 | M | L | O | `Cargo.toml` includes an `amd_npu` feature flag but no documentation, test, or CI coverage exists for it. Documenting activation steps would make this a usable capability. |
| idea-021 | 3 – Backend | openapi-spec-generation | P3 | H | M | O | FastAPI auto-generates an OpenAPI spec at runtime but no `openapi.json` is committed or built in CI. `docs/api/index.md` is a mkdocstrings placeholder never rendered, making the API undiscoverable. |
| idea-022 | 3 – Backend | jwt-refresh-token-support | P3 | M | M | O | `backend/auth.py` supports API key + single JWT but no refresh token or session rotation. Long-lived sessions with non-expiring JWTs are a security risk for a multi-agent system. |
| idea-023 | 4 – Frontend | tailwind-config-missing | P3 | M | H | W | The web app uses `tailwind-merge` and `clsx` but has no `tailwind.config.ts`. Without a config, JIT purge paths are undefined and design tokens cannot be centrally managed. |
| idea-024 | 4 – Frontend | frontend-e2e-tests | P3 | H | M | W | The frontend has only 2 Vitest unit tests covering ~2% of 10 app windows and 6 components. No Playwright or Cypress E2E suite exists. |
| idea-025 | 4 – Frontend | global-state-management | P3 | H | M | O | Each of the 10 app windows manages its own local state. No Zustand/Redux store exists for cross-window coordination (shared WebSocket session, unified notifications). |
| idea-026 | 4 – Frontend | frontend-url-routing | P3 | M | L | O | Navigation between app windows is purely DOM/event driven with no URL routing. Adding React Router would enable deep-linking, browser history, and shareable window states. |
| idea-027 | 5 – Tests | windows-ci-matrix | P3 | H | M | W | All 5 CI workflows run exclusively on `ubuntu-latest`. Since the primary developer OS is Windows and the app distributes a `.pyd` Rust extension, a Windows runner is needed in CI. |
| idea-028 | 5 – Tests | property-based-test-expansion | P3 | M | M | O | `hypothesis` is a declared CI dependency but coverage of edge cases in transaction managers, CRDT, and crypto modules is minimal. Systematic property-based tests would raise confidence. |
| idea-029 | 5 – Tests | backend-integration-test-suite | P3 | H | M | W | `tests/integration/` contains only one file. The backend's WebSocket, auth, rate limiter, and session management have no multi-component integration tests. |
| idea-030 | 6 – Docs | adr-backfill | P3 | M | M | O | Only an ADR template exists. Major architectural decisions (transaction manager, Rust FFI, P2P CRDT, E2E encryption, maturin build) are undocumented in ADR format. |
| idea-031 | 6 – Docs | automated-api-docs-ci | P3 | M | M | W | `docs/api/index.md` contains only a mkdocstrings placeholder. MkDocs is in `requirements-ci.txt` but no CI job runs `mkdocs build`, so the published API reference is never built. |
| idea-032 | 6 – Docs | changelog-automation | P3 | M | L | O | `CHANGELOG.md` is edited manually. Configuring `release-please` or `conventional-changelog` tied to the `feat`/`fix` commit convention would automate release notes. |
| idea-033 | 7 – CI | pre-commit-ruff-version-drift | P3 | M | M | W | `.pre-commit-config.yaml` pins ruff at `v0.15.5` while `requirements-ci.txt` pins `ruff==0.15.6`. The local pre-commit hook uses a different lint binary than CI. |
| idea-034 | 8 – Data/Deploy | projects-json-schema-validation | P3 | M | M | W | `data/projects.json` is the source of truth for 76 projects but has no JSON Schema. Malformed entries can silently corrupt the Kanban board; a schema test in CI would prevent this. |
| idea-035 | 9 – Dependencies | torch-optional-dependency-split | P3 | M | M | W | `torch>=2.5.0` is listed in `pyproject.toml` main dependencies but absent from `requirements.txt`. Torch is ~2GB and should be an optional `[ai]` extra to avoid forcing the download. |
| idea-036 | 1 – Python agents | rl-module-implementation | P4 | H | L | O | `src/rl/` stub was planned as a reinforcement-learning module for agent self-optimization. Implementing even a basic reward-shaping layer would support autonomous quality improvement cycles. |
| idea-037 | 6 – Docs | docs-work-folder-cleanup | P4 | L | L | W | `docs/work/` contains 10+ stale working documents that are no longer current. These should be archived to `docs/archive/` or deleted. |
| idea-038 | 9 – Dependencies | chromadb-optional-extra | P4 | M | L | W | `chromadb>=0.5.0` is listed in `pyproject.toml` main dependencies but not in `requirements.txt`. ChromaDB pulls in heavy ML dependencies and should be an optional `[vector]` extra. |

### Future Ideas — Quick Reference

| Priority | Count | IDs |
|---|---|---|
| P1 – Critical / blocking | 3 | idea-001, idea-002, idea-003 |
| P2 – High value | 11 | idea-004 – idea-014 |
| P3 – Moderate | 21 | idea-015 – idea-035 |
| P4 – Nice to have | 3 | idea-036 – idea-038 |
| **Total** | **38** | |

| Area | Count |
|---|---|
| 1 – Python agents & tools | 5 |
| 2 – Rust core | 4 |
| 3 – FastAPI backend | 3 |
| 4 – React/Vite frontend | 4 |
| 5 – Test suite | 4 |
| 6 – Documentation | 4 |
| 7 – CI / agent definitions | 5 |
| 8 – Data models & deploy | 4 |
| 9 – Dependency hygiene | 5 |
| **Total** | **38** |

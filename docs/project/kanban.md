# PyAgent Project Kanban Board

_Last updated: 2026-03-26 | Total projects: 77_

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
| prj0000076 | future-ideas-kanban | Full workspace audit to surface future improvement ideas; add SWOT-prioritised idea table to kanban.md with priority, impact, urgency, and description | P3 | M | planning, kanban, roadmap | 2026-03-25 |

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
| Ideas | 1 |
| Discovery | 0 |
| Design | 0 |
| In Sprint | 1 |
| Review | 3 |
| Released | 70 |
| Archived | 1 |
| **Total** | **76** |

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

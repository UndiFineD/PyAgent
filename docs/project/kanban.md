# PyAgent Project Kanban Board

_Last updated: 2026-03-24 | Total projects: 62_

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
| prj0000054 | backend-authentication | Add API-key or JWT authentication to all REST and WebSocket endpoints | P4 | unknown | security, backend | 2026-03-24 |
| prj0000055 | websocket-e2e-encryption | Wire the documented E2E encryption architecture into production WebSocket transport using Noise_XX | P4 | unknown | security, websocket, rust | 2026-03-24 |
| prj0000056 | rust-async-transport-activation | Enable async-transport feature in rust_core to activate QUIC-over-Tokio for faster inter-agent messaging | P4 | unknown | rust, transport, async | 2026-03-24 |
| prj0000057 | agent-orchestration-graph | Visual DAG panel in NebulaOS showing live task flow and agent status across all 10 pipeline stages | P4 | unknown | ui, nebula, agents | 2026-03-24 |
| prj0000058 | mobile-responsive-nebula-os | Add CSS responsive breakpoints and touch-friendly interaction patterns to the NebulaOS shell | P4 | unknown | ui, nebula, mobile | 2026-03-24 |
| prj0000059 | plugin-marketplace-browser | In-NebulaOS panel for discovering, installing, and managing third-party agent plugins | P4 | unknown | ui, nebula, plugins | 2026-03-24 |
| prj0000060 | flm-token-throughput-dashboard | Real-time tokens-per-second charts fed from FLM telemetry in NebulaOS | P4 | unknown | ui, nebula, llm, flm | 2026-03-24 |
| prj0000061 | theme-system | Light mode and retro terminal theme for NebulaOS with theme selector and persisted preference | P4 | unknown | ui, nebula, themes | 2026-03-24 |
| prj0000062 | live-agent-execution-in-codebuilder | Wire the 10-agent pipeline to CodeBuilder UI with streaming per-agent log output and progress indicators | P4 | unknown | ui, nebula, agents, codebuilder | 2026-03-24 |

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
| prj0000053 | hmac-webhook-verification | prj0000053-hmac-webhook-verification | [#191](https://github.com/UndiFineD/PyAgent/pull/191) | P2 | S | 2026-03-24 |
| prj0000052 | project-management | prj0000052-project-management | [#190](https://github.com/UndiFineD/PyAgent/pull/190) | P2 | L | 2026-03-24 |
| prj0000043 | p2p-security-deps | prj0000043-p2p-security-deps | open | P2 | M | 2026-03-24 |
| prj0000044 | transaction-managers-stubs | prj0000044-transaction-managers-stubs | #136 | P2 | S | 2026-03-24 |

---

## Released

All projects merged to main branch.

| ID | Name | Summary | Branch | PR | Priority | Budget | Released |
|---|---|---|---|---|---|---|---|
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
| Ideas | 10 |
| Discovery | 0 |
| Design | 0 |
| In Sprint | 1 |
| Review | 2 |
| Released | 48 |
| Archived | 1 |
| **Total** | **62** |

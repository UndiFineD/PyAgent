# project-management — Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-24_

---

## Selected Option

**Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop)**

Rationale: The project.md acceptance criteria and explicit out-of-scope constraints all
point to Option A. The source of truth (git) is a design feature, not a limitation: every
lane transition is a reviewed, attributable, reversible commit. All 6 research areas in
the think doc converge on this option. Zero complexity overhead, full reversibility, no
schema migration risk.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  SOURCE OF TRUTH                                                     │
│  ┌───────────────┐        ┌──────────────────┐                      │
│  │ kanban.md     │◄──────►│ data/projects.json│  (both in git)      │
│  └──────┬────────┘        └────────┬─────────┘                      │
│         │ human/agent reading      │ loaded at startup               │
└─────────┼──────────────────────────┼─────────────────────────────────┘
          │                          │
          ▼                          ▼
┌──────────────────┐     ┌───────────────────────────────┐
│ Agent memory     │     │  backend/app.py                │
│ (.md knowledge)  │     │  GET /api/projects?lane=…      │
└──────────────────┘     │  ProjectModel (Pydantic)       │
                         └───────────────┬───────────────┘
                                         │ HTTP JSON
                                         ▼
                         ┌───────────────────────────────┐
                         │  web/apps/ProjectManager.tsx   │
                         │  ProjectManager component      │
                         │  ├─ FilterBar                  │
                         │  ├─ KanbanBoard                │
                         │  │   └─ LaneColumn × 7         │
                         │  │       └─ ProjectCard × N    │
                         │  └─ (expand-on-click detail)   │
                         └───────────────────────────────┘
                                         │ registered in
                         ┌───────────────▼───────────────┐
                         │  web/App.tsx + web/types.ts    │
                         │  AppId 'projectmanager' added  │
                         │  openApp switch case added     │
                         │  Menu button added             │
                         └───────────────────────────────┘
```

**Data flow** (read-only):
1. `data/projects.json` is loaded once at backend startup into `_PROJECTS`.
2. `GET /api/projects` returns the full list (optionally filtered by `?lane=`).
3. `ProjectManager.tsx` calls this endpoint on mount, renders 7 columns.
4. No writes from UI. Lane changes require editing `data/projects.json` + `kanban.md` and committing.

**Agent integration**:
- `0master.agent.md` gains a `### Project lifecycle board` subsection documenting kanban.md.
- `1project.agent.md` gains a lifecycle board step under `**Project doc conventions**` and
  in the operating procedure.

---

## Interfaces & Contracts

### 1. `data/projects.json` — Complete file

All 62 entries. For projects prj0000001–prj0000042 (pre-folder era), `branch` is `"merged"`
(sentinel for "was merged, no explicit branch tracked") and `pr` is `null` unless a PR
number is known. `created` date is synthetic `"2026-01-01"` for those entries.

**Sentinel value decision**:
- `"branch": "merged"` — historical signal that the branch was merged; no specific branch name tracked.
- `"pr": null` for pre-folder projects means PR number not tracked.
- Known PR numbers: prj0000044=136, prj0000045=137, prj0000047=185, prj0000048=186,
  prj0000049=187, prj0000050=188, prj0000051=189.
- `prj0000043` (P2P security deps) has `"pr": null` — PR is open but no number confirmed
  in local git history. @6code must check GitHub before finalizing.
- `"created": "2026-01-01"` is a synthetic placeholder for projects pre-dating the folder convention.

**Full JSON content** (write verbatim to `data/projects.json`):

```json
[
  {"id":"prj0000001","name":"async-runtime","lane":"Released","summary":"Tokio-backed async helpers and PyO3 bindings for non-blocking agent ops","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core","async","rust"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000002","name":"core-system","lane":"Released","summary":"Core runtime modules: task_queue, agent_registry, memory, observability scaffold","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000003","name":"hybrid-llm-security","lane":"Released","summary":"Hybrid LLM security core: Rust encryption, transactions, key rotation","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["security","llm","rust"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000004","name":"llm-context-consolidation","lane":"Released","summary":"Unified LLM context window management and ContextManager implementation","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["llm","context"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000005","name":"llm-swarm-architecture","lane":"Released","summary":"Multi-agent swarm coordination: AgentRegistry, TaskScheduler, SwarmMemory","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["swarm","architecture"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000006","name":"unified-transaction-manager","lane":"Released","summary":"MemoryTransaction, StorageTransaction, ProcessTransaction, ContextTransaction managers","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core","transactions"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000007","name":"advanced-research","lane":"Released","summary":"Research notes, long-horizon planning artifacts, and literature review","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["docs","research"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000008","name":"agent-workflow","lane":"Released","summary":"Task state machine, WorkflowEngine, and agent handoff protocol","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core","workflow"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000009","name":"community-collaboration","lane":"Released","summary":"Community contribution guidelines, issue templates, and team governance docs","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["docs","community"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000010","name":"context-management","lane":"Released","summary":"ContextManager windowing, SkillsRegistry, and integration smoke tests","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core","context"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000011","name":"core-project-structure","lane":"Released","summary":"Canonical src/ layout, __init__.py ordering, and import path standardization","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["core","structure"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000012","name":"deployment-operations","lane":"Released","summary":"Docker compose, Dockerfile, and provisioning scripts for production deploy","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["deploy","ops"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000013","name":"dev-tools-autonomy","lane":"Released","summary":"Autonomous dev tooling: dependency audit, self-healing scripts","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["tools","autonomy"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000014","name":"dev-tools-capabilities","lane":"Released","summary":"Expanded dev tool capabilities: static analysis, complexity metrics","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["tools"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000015","name":"dev-tools-implementation","lane":"Released","summary":"Full implementation of code improvement pipeline tools","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["tools"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000016","name":"dev-tools-structure","lane":"Released","summary":"File layout and modular structure for src/tools/ package","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["tools","structure"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000017","name":"dev-tools-utilities","lane":"Released","summary":"Shared utilities for dev tools: path helpers, config loaders, formatters","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["tools","utils"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000018","name":"documentation-assets","lane":"Released","summary":"MkDocs config, Mermaid/PlantUML diagram assets, and doc build scripts","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["docs"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000019","name":"future-roadmap","lane":"Released","summary":"Research notes and long-horizon planning artifacts for roadmap items","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","planning"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000020","name":"github-import","lane":"Released","summary":"GitHub import system: webhook handler, repo sync, and PR ingestion","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["github","import"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000021","name":"project-management-governance","lane":"Released","summary":"PRINCE2/agile hybrid governance model, project doc conventions, and audit trail","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["governance","docs"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000022","name":"external-repos-tracking","lane":"Released","summary":"External repository tracking list and dependency provenance notes","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","tracking"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000023","name":"naming-standards","lane":"Released","summary":"PascalCase module naming convention, file-rename tracker, and migration guide","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["standards","naming"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000024","name":"code-of-conduct","lane":"Released","summary":"Contributor Code of Conduct (Contributor Covenant v2.1)","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["docs","community"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000025","name":"contributing-guide","lane":"Released","summary":"CONTRIBUTING.md with PR workflow, DCO, and branch naming instructions","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","community"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000026","name":"architecture-adr-template","lane":"Released","summary":"Architecture Decision Record template and initial ADR for async runtime","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","architecture"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000027","name":"onboarding-docs","lane":"Released","summary":"Developer onboarding guide: environment setup, first PR walkthrough","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","onboarding"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000028","name":"api-reference","lane":"Released","summary":"Auto-generated and hand-curated API reference docs for backend and core","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","api"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000029","name":"performance-docs","lane":"Released","summary":"Performance benchmarking methodology, baseline results, and optimization notes","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["docs","performance"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000030","name":"standards-code-style","lane":"Released","summary":"Python/Rust/TS style guide: max-line 120, PascalCase modules, flake8 config","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["standards","style"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000031","name":"standards-commit-style","lane":"Released","summary":"Conventional commits standard, commit message template, and pre-commit hook","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["standards","git"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000032","name":"standards-test-style","lane":"Released","summary":"pytest conventions, fixture patterns, test coverage targets, and naming rules","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["standards","testing"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000033","name":"standards-security","lane":"Released","summary":"OWASP alignment, input validation policy, allowlist patterns, and SBOM process","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["standards","security"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000034","name":"standards-docs","lane":"Released","summary":"Documentation standards: structure, markdown lint rules, header requirements","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["standards","docs"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000035","name":"standards-ci","lane":"Released","summary":"CI workflow design standards: job naming, matrix strategy, artifact retention","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["standards","ci"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000036","name":"standards-release","lane":"Released","summary":"Release process: semver policy, changelog format, tagging convention","branch":"merged","pr":null,"priority":"P3","budget_tier":"XS","tags":["standards","release"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000037","name":"tools-crdt-security","lane":"Released","summary":"CRDT security tooling: P2P security deps, libp2p integration, encryption layer","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["security","crdt","rust"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000038","name":"project-management-v1","lane":"Released","summary":"Initial project management tooling: folder structure, stub generator, registry","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["governance","tools"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000039","name":"conftest-typing-fixes","lane":"Released","summary":"Fix conftest.py type annotations to unblock full test suite execution","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["testing","types"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000040","name":"flm-integration","lane":"Released","summary":"FLM (Fastflow Language Model) OpenAI-compatible chat adapter and tool-call loop","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["llm","flm"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000041","name":"flm-benchmark","lane":"Released","summary":"FLM benchmark harness: latency, throughput, and accuracy scoring","branch":"merged","pr":null,"priority":"P3","budget_tier":"M","tags":["llm","benchmark","flm"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000042","name":"agent-workflow-polish","lane":"Released","summary":"Agent workflow refinements: error handling improvements and state logging","branch":"merged","pr":null,"priority":"P3","budget_tier":"S","tags":["core","workflow"],"created":"2026-01-01","updated":"2026-03-24"},
  {"id":"prj0000043","name":"p2p-security-deps","lane":"Review","summary":"Upgrade libp2p 0.49 to 0.56 to remediate 6 Dependabot CVEs in P2P stack","branch":"prj0000043-p2p-security-deps","pr":null,"priority":"P2","budget_tier":"M","tags":["security","crdt","rust"],"created":"2026-03-10","updated":"2026-03-24"},
  {"id":"prj0000044","name":"transaction-managers-stubs","lane":"Review","summary":"CI stubs for missing transaction manager modules to unblock test suite","branch":"prj0000044-transaction-managers-stubs","pr":136,"priority":"P2","budget_tier":"S","tags":["core","transactions","ci"],"created":"2026-03-10","updated":"2026-03-24"},
  {"id":"prj0000045","name":"transaction-managers-full","lane":"Released","summary":"Full implementation of all four transaction managers (Memory, Storage, Process, Context)","branch":"merged","pr":137,"priority":"P2","budget_tier":"L","tags":["core","transactions"],"created":"2026-03-10","updated":"2026-03-24"},
  {"id":"prj0000046","name":"flm-tps-benchmark","lane":"Archived","summary":"Per-provider tokens-per-second metrics harness for FLM endpoint evaluation","branch":"prj0000046-flm-tps-benchmark","pr":null,"priority":"P3","budget_tier":"M","tags":["llm","benchmark","flm"],"created":"2026-03-10","updated":"2026-03-24"},
  {"id":"prj0000047","name":"conky-real-metrics","lane":"Released","summary":"Wire NebulaOS Conky panel to live /api/metrics/system endpoint with charts","branch":"merged","pr":185,"priority":"P2","budget_tier":"M","tags":["ui","nebula","metrics"],"created":"2026-03-15","updated":"2026-03-24"},
  {"id":"prj0000048","name":"taskbar-config","lane":"Released","summary":"Taskbar always-visible toggle in NebulaOS settings modal with localStorage persistence","branch":"merged","pr":186,"priority":"P2","budget_tier":"S","tags":["ui","nebula"],"created":"2026-03-15","updated":"2026-03-24"},
  {"id":"prj0000049","name":"dependabot-security-fixes","lane":"Released","summary":"Apply Dependabot-flagged security fixes across Python and JS dependencies","branch":"merged","pr":187,"priority":"P2","budget_tier":"S","tags":["security","ci"],"created":"2026-03-18","updated":"2026-03-24"},
  {"id":"prj0000050","name":"install-script","lane":"Released","summary":"Cross-platform install.ps1 environment bootstrap for dev onboarding","branch":"merged","pr":188,"priority":"P2","budget_tier":"S","tags":["tools","onboarding"],"created":"2026-03-20","updated":"2026-03-24"},
  {"id":"prj0000051","name":"readme-update","lane":"Released","summary":"Comprehensive README rewrite with NebulaOS screenshot, full component overview, and Future Roadmap","branch":"merged","pr":189,"priority":"P2","budget_tier":"M","tags":["docs"],"created":"2026-03-22","updated":"2026-03-24"},
  {"id":"prj0000052","name":"project-management","lane":"In Sprint","summary":"Kanban lifecycle board, data/projects.json, ProjectManager NebulaOS app, and /api/projects endpoint","branch":"prj0000052-project-management","pr":null,"priority":"P2","budget_tier":"L","tags":["governance","ui","nebula","backend"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000053","name":"hmac-webhook-verification","lane":"Ideas","summary":"Secure GitHub webhook payloads with HMAC-SHA256 signature validation in src/github_app.py","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["security","github"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000054","name":"backend-authentication","lane":"Ideas","summary":"Add API-key or JWT authentication to all REST and WebSocket endpoints","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["security","backend"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000055","name":"websocket-e2e-encryption","lane":"Ideas","summary":"Wire the documented E2E encryption architecture into production WebSocket transport using Noise_XX","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["security","websocket","rust"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000056","name":"rust-async-transport-activation","lane":"Ideas","summary":"Enable async-transport feature in rust_core to activate QUIC-over-Tokio for faster inter-agent messaging","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["rust","transport","async"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000057","name":"agent-orchestration-graph","lane":"Ideas","summary":"Visual DAG panel in NebulaOS showing live task flow and agent status across all 10 pipeline stages","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","agents"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000058","name":"mobile-responsive-nebula-os","lane":"Ideas","summary":"Add CSS responsive breakpoints and touch-friendly interaction patterns to the NebulaOS shell","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","mobile"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000059","name":"plugin-marketplace-browser","lane":"Ideas","summary":"In-NebulaOS panel for discovering, installing, and managing third-party agent plugins","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","plugins"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000060","name":"flm-token-throughput-dashboard","lane":"Ideas","summary":"Real-time tokens-per-second charts fed from FLM telemetry in NebulaOS","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","llm","flm"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000061","name":"theme-system","lane":"Ideas","summary":"Light mode and retro terminal theme for NebulaOS with theme selector and persisted preference","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","themes"],"created":"2026-03-24","updated":"2026-03-24"},
  {"id":"prj0000062","name":"live-agent-execution-in-codebuilder","lane":"Ideas","summary":"Wire the 10-agent pipeline to CodeBuilder UI with streaming per-agent log output and progress indicators","branch":null,"pr":null,"priority":"P4","budget_tier":"unknown","tags":["ui","nebula","agents","codebuilder"],"created":"2026-03-24","updated":"2026-03-24"}
]
```

---

### 2. `docs/project/kanban.md` — Complete file content

**@6code must write this file with exactly this structure.** This is the canonical
content — not a template. All 62 entries are populated.

````markdown
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
| prj0000053 | hmac-webhook-verification | Secure GitHub webhook payloads with HMAC-SHA256 signature validation in src/github_app.py | P4 | unknown | security, github | 2026-03-24 |
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
| prj0000052 | project-management | Kanban lifecycle board, data/projects.json, ProjectManager NebulaOS app, /api/projects endpoint | prj0000052-project-management | P2 | L | 2026-03-24 |

---

## Review

PR open, awaiting merge.

| ID | Name | Branch | PR | Priority | Budget | Updated |
|---|---|---|---|---|---|---|
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
````

---

### 3. `web/apps/ProjectManager.tsx` — Complete TypeScript Component

**@6code must create this file.** File location: `web/apps/ProjectManager.tsx`

**Styling context**:
- `Conky.tsx` inner style: `bg-black/80 text-green-400 font-mono` (terminal-themed inner).
- `AgentChat.tsx` outer style: `bg-os-bg text-os-text`, header `bg-os-window border-b border-os-border`.
- CSS vars in use across existing apps: `bg-os-bg`, `bg-os-window`, `border-os-border`,
  `text-os-text`, `text-os-text/60`, `text-os-accent`, `hover:bg-os-border`, `bg-os-bg`.
- `ProjectManager` uses `AgentChat`-style outer shell (not Conky terminal-green style).

```tsx
/**
 * ProjectManager — NebulaOS app showing all PyAgent projects as a Kanban board.
 *
 * Data source: GET /api/projects (backend/app.py)
 * Lane transitions are git-only (this panel is read-only).
 */
import React, { useState, useEffect } from 'react';
import {
  GitBranch, ExternalLink, Search, Loader2, AlertTriangle, ChevronDown, ChevronUp, Tag
} from 'lucide-react';
import { cn } from '../utils';

// ── Types ────────────────────────────────────────────────────────────────────

type Lane = 'Ideas' | 'Discovery' | 'Design' | 'In Sprint' | 'Review' | 'Released' | 'Archived';
type Priority = 'P1' | 'P2' | 'P3' | 'P4';
type BudgetTier = 'XS' | 'S' | 'M' | 'L' | 'XL' | 'unknown';

interface Project {
  id: string;
  name: string;
  lane: Lane;
  summary: string;
  branch: string | null;
  pr: number | null;
  priority: Priority;
  budget_tier: BudgetTier;
  tags: string[];
  created: string;
  updated: string;
}

// ── Constants ────────────────────────────────────────────────────────────────

const LANES: Lane[] = ['Ideas', 'Discovery', 'Design', 'In Sprint', 'Review', 'Released', 'Archived'];

// Inline hex colors — use with style={{ }} for dynamic lane coloring
const LANE_COLORS: Record<Lane, string> = {
  'Ideas':     '#3b82f6',  // blue-500
  'Discovery': '#8b5cf6',  // violet-500
  'Design':    '#6366f1',  // indigo-500
  'In Sprint': '#fbbf24',  // amber-400
  'Review':    '#fb923c',  // orange-400
  'Released':  '#10b981',  // emerald-500
  'Archived':  '#6b7280',  // gray-500
};

const PRIORITY_COLORS: Record<Priority, string> = {
  P1: '#ef4444',  // red-500
  P2: '#fb923c',  // orange-400
  P3: '#60a5fa',  // blue-400
  P4: '#9ca3af',  // gray-400
};

const GITHUB_PR_BASE = 'https://github.com/UndiFineD/PyAgent/pull';

// ── ProjectCard ──────────────────────────────────────────────────────────────

const ProjectCard: React.FC<{ project: Project }> = ({ project }) => {
  const [expanded, setExpanded] = useState(false);
  const laneColor = LANE_COLORS[project.lane];
  const priorityColor = PRIORITY_COLORS[project.priority];

  return (
    <div
      className="bg-os-window border border-os-border rounded-lg p-3 mb-2 cursor-pointer hover:border-os-accent/50 transition-colors"
      onClick={() => setExpanded(e => !e)}
    >
      {/* Lane badge + ID chip + Priority + Budget */}
      <div className="flex items-center gap-2 mb-2 flex-wrap">
        <span
          className="text-[10px] font-semibold px-2 py-0.5 rounded-full text-black"
          style={{ backgroundColor: laneColor }}
        >
          {project.lane}
        </span>
        <span className="font-mono text-[10px] text-os-text/50 bg-os-bg border border-os-border rounded px-1.5 py-0.5">
          {project.id}
        </span>
        <span
          className="ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded"
          style={{ color: priorityColor, borderColor: priorityColor, border: `1px solid ${priorityColor}` }}
        >
          {project.priority}
        </span>
        <span className="text-[10px] text-os-text/50 bg-os-bg border border-os-border rounded px-1.5 py-0.5">
          {project.budget_tier}
        </span>
      </div>

      {/* Name */}
      <div className="font-semibold text-sm text-os-text mb-1 leading-tight">
        {project.name}
      </div>

      {/* Summary */}
      <div className={cn('text-xs text-os-text/60 leading-relaxed', !expanded && 'line-clamp-2')}>
        {project.summary}
      </div>

      {/* Expanded detail */}
      {expanded && (
        <div className="mt-3 space-y-2 border-t border-os-border pt-2">
          {project.branch && project.branch !== 'merged' && (
            <div className="flex items-center gap-1.5 text-xs text-os-text/70">
              <GitBranch size={12} className="shrink-0" />
              <span className="font-mono truncate">{project.branch}</span>
            </div>
          )}
          {project.branch === 'merged' && (
            <div className="flex items-center gap-1.5 text-xs text-emerald-400">
              <GitBranch size={12} className="shrink-0" />
              <span className="font-mono">merged</span>
            </div>
          )}
          {project.pr !== null && (
            <div className="flex items-center gap-1.5 text-xs">
              <ExternalLink size={12} className="shrink-0 text-os-text/50" />
              <a
                href={`${GITHUB_PR_BASE}/${project.pr}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-os-accent hover:underline"
                onClick={e => e.stopPropagation()}
              >
                PR #{project.pr}
              </a>
            </div>
          )}
          {project.tags.length > 0 && (
            <div className="flex items-center gap-1 flex-wrap">
              <Tag size={11} className="text-os-text/40 shrink-0" />
              {project.tags.map(tag => (
                <span key={tag} className="text-[10px] bg-os-bg border border-os-border rounded px-1.5 py-0.5 text-os-text/60">
                  {tag}
                </span>
              ))}
            </div>
          )}
          <div className="text-[10px] text-os-text/40 font-mono">
            created: {project.created} · updated: {project.updated}
          </div>
        </div>
      )}

      <div className="flex justify-center mt-1">
        {expanded ? <ChevronUp size={12} className="text-os-text/30" /> : <ChevronDown size={12} className="text-os-text/30" />}
      </div>
    </div>
  );
};

// ── LaneColumn ───────────────────────────────────────────────────────────────

const LaneColumn: React.FC<{ lane: Lane; projects: Project[] }> = ({ lane, projects }) => {
  const color = LANE_COLORS[lane];
  return (
    <div className="min-w-[240px] w-64 flex flex-col shrink-0">
      <div
        className="flex items-center justify-between px-3 py-2 rounded-t-lg mb-2 text-black"
        style={{ backgroundColor: color }}
      >
        <span className="text-xs font-bold uppercase tracking-wide">{lane}</span>
        <span className="text-xs font-mono bg-black/20 rounded-full px-2 py-0.5">{projects.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto min-h-0 max-h-[calc(100vh-240px)]">
        {projects.length === 0
          ? <div className="text-[10px] text-os-text/30 text-center py-4 italic">empty</div>
          : projects.map(p => <ProjectCard key={p.id} project={p} />)
        }
      </div>
    </div>
  );
};

// ── FilterBar ────────────────────────────────────────────────────────────────

interface FilterBarProps {
  selectedLane: Lane | null;
  onLaneChange: (lane: Lane | null) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ selectedLane, onLaneChange, searchQuery, onSearchChange }) => (
  <div className="flex items-center gap-3 px-3 py-2 bg-os-window border-b border-os-border flex-wrap">
    <div className="flex items-center gap-1 flex-wrap">
      <button
        onClick={() => onLaneChange(null)}
        className={cn(
          'text-xs px-2 py-1 rounded transition-colors border',
          selectedLane === null
            ? 'bg-os-accent text-white border-os-accent'
            : 'border-os-border text-os-text/60 hover:bg-os-border'
        )}
      >
        All
      </button>
      {LANES.map(lane => (
        <button
          key={lane}
          onClick={() => onLaneChange(selectedLane === lane ? null : lane)}
          className={cn(
            'text-xs px-2 py-1 rounded transition-colors border text-black font-medium',
            selectedLane === lane ? 'opacity-100' : 'opacity-40 hover:opacity-70'
          )}
          style={{ backgroundColor: LANE_COLORS[lane], borderColor: LANE_COLORS[lane] }}
        >
          {lane}
        </button>
      ))}
    </div>
    <div className="flex items-center gap-1.5 bg-os-bg border border-os-border rounded px-2 py-1 ml-auto">
      <Search size={12} className="text-os-text/40 shrink-0" />
      <input
        type="text"
        placeholder="Search name or ID…"
        value={searchQuery}
        onChange={e => onSearchChange(e.target.value)}
        className="bg-transparent text-xs text-os-text outline-none w-44 placeholder:text-os-text/30"
      />
    </div>
  </div>
);

// ── ProjectManager ───────────────────────────────────────────────────────────

export const ProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLane, setSelectedLane] = useState<Lane | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('/api/projects')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Project[]) => { setProjects(data); setLoading(false); })
      .catch(err => { setError(String(err.message)); setLoading(false); });
  }, []);

  // Derived filter — no useEffect needed
  const filtered = projects.filter(p => {
    const matchLane = selectedLane === null || p.lane === selectedLane;
    const q = searchQuery.toLowerCase();
    const matchSearch = !q || p.name.toLowerCase().includes(q) || p.id.includes(q);
    return matchLane && matchSearch;
  });

  // Group by lane for column rendering
  const byLane = Object.fromEntries(LANES.map(l => [l, [] as Project[]])) as Record<Lane, Project[]>;
  for (const p of filtered) byLane[p.lane]?.push(p);

  if (loading) return (
    <div className="flex items-center justify-center h-full bg-os-bg text-os-text">
      <Loader2 size={24} className="animate-spin text-os-accent" />
      <span className="ml-2 text-sm">Loading projects…</span>
    </div>
  );

  if (error) return (
    <div className="flex flex-col items-center justify-center h-full bg-os-bg text-os-text gap-3">
      <AlertTriangle size={28} className="text-amber-400" />
      <span className="text-sm text-os-text/70">Failed to load projects</span>
      <span className="text-xs font-mono text-os-text/40">{error}</span>
    </div>
  );

  return (
    <div className="flex flex-col h-full bg-os-bg text-os-text">
      <div className="flex items-center justify-between px-3 py-2 bg-os-window border-b border-os-border text-sm">
        <span className="font-semibold">Project Manager</span>
        <span className="text-xs text-os-text/50 font-mono">{projects.length} projects</span>
      </div>
      <FilterBar
        selectedLane={selectedLane}
        onLaneChange={setSelectedLane}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />
      <div className="flex-1 overflow-x-auto overflow-y-hidden p-3">
        <div className="flex gap-3 h-full">
          {LANES.map(lane => (
            <LaneColumn key={lane} lane={lane} projects={byLane[lane]} />
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

### 4. `backend/app.py` — Exact Code Additions

Two insertion points. Both are **additions only** — no existing code is changed.

**Insertion point A**: After the line `_AGENTS_DIR = _PROJECT_ROOT / ".github" / "agents"`
and before the line `_VALID_AGENT_IDS = frozenset({...`. Insert:

```python
# ── Project data ─────────────────────────────────────────────────────────────
_PROJECTS_FILE = _PROJECT_ROOT / "data" / "projects.json"


def _load_projects() -> list[dict]:
    """Load data/projects.json at module startup. Returns [] on missing/corrupt file."""
    if not _PROJECTS_FILE.exists():
        logger.warning("data/projects.json not found at %s", _PROJECTS_FILE)
        return []
    try:
        return json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load data/projects.json: %s", exc)
        return []


_PROJECTS: list[dict] = _load_projects()
```

**Insertion point B**: After the closing of `write_agent_doc` and **before** the
`@app.websocket("/ws")` decorator. Insert:

```python
# ── Project models + endpoint ─────────────────────────────────────────────────

from typing import Literal, Optional as _Opt  # noqa: E402


Lane = Literal["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
_PriorityLit = Literal["P1", "P2", "P3", "P4"]
_BudgetLit = Literal["XS", "S", "M", "L", "XL", "unknown"]


class ProjectModel(BaseModel):
    """Single project entry from data/projects.json."""

    id: str
    name: str
    lane: Lane
    summary: str
    branch: _Opt[str] = None
    pr: _Opt[int] = None
    priority: _PriorityLit = "P3"
    budget_tier: _BudgetLit = "M"
    tags: list[str] = []
    created: _Opt[str] = None
    updated: _Opt[str] = None


@app.get("/api/projects", response_model=list[ProjectModel])
async def get_projects(lane: _Opt[str] = None) -> list[ProjectModel]:
    """Return all projects from data/projects.json, optionally filtered by lane."""
    if not _PROJECTS and not _PROJECTS_FILE.exists():
        raise HTTPException(status_code=500, detail="data/projects.json not found")
    valid: list[ProjectModel] = []
    for entry in _PROJECTS:
        try:
            valid.append(ProjectModel(**entry))
        except Exception as exc:  # pydantic ValidationError
            logger.warning("Skipping malformed project entry %s: %s", entry.get("id"), exc)
    if lane:
        return [p for p in valid if p.lane == lane]
    return valid
```

**Note for @6code**: The aliased imports (`Optional as _Opt`, `Literal`) avoid any
conflict with the top-level `from __future__ import annotations`. If `Optional` is already
imported at the top of `app.py`, use the existing name and do not add a second import.
Verify the current import block before inserting.

---

### 5. Agent File Additions — Exact Text

#### `0master.agent.md`

**Where to insert**: In `## Where to find key information (for this repo)`, after the
three-bullet block ending with `` - `docs/agents/` — agent memory + plan artifacts ``.

```markdown
### Project lifecycle board
- `docs/project/kanban.md` — single source of truth for project status across all
  lifecycle lanes (Ideas → Discovery → Design → In Sprint → Review → Released → Archived).
  - Read this before allocating a new `prjNNNNNNN` to confirm the next available ID.
  - Update this after any lane transition.
  - The board is also queryable via `GET /api/projects` in the backend.
```

**Where to insert (step 3a)**: In `## How the master agent operates`, after step 3
(`**Assign the project boundary**…`). Append immediately after that numbered line:

```markdown
3a. **Update kanban.md** after allocating a project ID: add the new project to the
    `Ideas` or `Discovery` lane in `docs/project/kanban.md` and commit the change (or
    include it in the first commit on the project branch). Update `data/projects.json`
    to match.
```

#### `1project.agent.md`

**Where to insert**: In `**Project doc conventions**`, after the final bullet point
(`- **Optional chunked plan files**: ...`). Append:

```markdown
- **Lifecycle board**: When a new project is created, ensure `docs/project/kanban.md`
  has an entry in the correct lane. New projects without started discovery go in `Ideas`;
  projects handed off to `@2think` advance to `Discovery`. Move the row when the lane
  changes, and always update `data/projects.json` to match.
```

**Where to insert (step 1a)**: In `## Operating procedure`, after step 1 ends (the
`"Create or validate project folder"` block). Insert a new step 1a:

```markdown
1a. **Update kanban.md and data/projects.json**
    - Move the project entry from `Ideas` to `Discovery` in `docs/project/kanban.md`.
    - If no entry exists yet (project was not pre-registered by `@0master`), create a
      new row in `Discovery` with the assigned `prjNNNNNNN`, name, summary, priority,
      and `budget_tier`.
    - Update `data/projects.json`: set `"lane": "Discovery"` for this project entry
      (add the entry if missing).
    - Commit both files on the project-specific branch alongside the project folder
      creation commit.
```

---

### 6. `web/App.tsx` + `web/types.ts` — Exact Changes

#### `web/types.ts`

Current (line 3):
```typescript
export type AppId = 'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder';
```

Replace with:
```typescript
export type AppId = 'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder' | 'projectmanager';
```

#### `web/App.tsx` — Three targeted changes

**Change 1 — Add import** (after the existing app imports, e.g. after `import { CodeBuilder }...`):
```typescript
import { ProjectManager } from './apps/ProjectManager';
```

**Change 2 — Add switch case** (after `case 'codebuilder':` block, before the closing
brace of the switch):
```typescript
      case 'projectmanager':
        component = <ProjectManager />;
        title = 'Project Manager';
        width = 1100;
        height = 650;
        break;
```

**Change 3 — Add menu button** (in the dropdown Applications section, after the
`AgentFlow Builder` button):
```tsx
                    <button onClick={() => openApp('projectmanager')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <Monitor size={16} className="text-indigo-400" /> Project Manager
                    </button>
```

`Monitor` is already imported in `App.tsx`. If `lucide-react@^0.577.0` exports
`LayoutKanban`, @6code may substitute it — but `Monitor` is the safe guaranteed option.

---

## Non-Functional Requirements

- **Performance**: `data/projects.json` loaded once at module startup (~10–30ms for 62
  entries, <5KB file). No per-request I/O. Pydantic validation cost is negligible.

- **Security**: GET-only endpoint. No user input is interpolated into file paths or
  queries. `ProjectModel` Pydantic validation ensures only valid enum values reach the
  client. Malformed entries are soft-skipped with a warning log — not surfaced as HTTP errors.
  No SSRF vectors (no user-controlled URLs). No write surfaces.

- **Testability**: `tests/structure/test_project_manager.py` (created by @5test) must validate:
  1. `data/projects.json` is parseable JSON.
  2. Every entry has all required fields: `id`, `name`, `lane`, `summary`, `priority`, `budget_tier`.
  3. Every `id` matches `^prj[0-9]{7}$`.
  4. Every `lane` is one of 7 valid values.
  5. No duplicate IDs.
  6. Count equals 62 (51 existing + 10 Ideas + prj0000052 in sprint).

---

## Open Questions

1. **prj0000043 PR number**: Local git history shows no PR number for `p2p-security-deps`.
   @6code must check `https://github.com/UndiFineD/PyAgent/pulls` before finalizing
   `data/projects.json`. Fill in the integer PR number or leave `null` if unconfirmed.

2. **`typing.Optional` import collision**: `app.py` may already import `Optional` at
   the top level. @6code must check before inserting the project endpoint block. Merge
   into the existing import; do not duplicate it.

3. **`LayoutKanban` icon**: Verify `lucide-react@^0.577.0` exports `LayoutKanban` before
   using it in `App.tsx`. Fall back to `Monitor` if not available.

4. **`line-clamp-2` Tailwind class**: Verify `tailwind.config.*` enables the
   `line-clamp` plugin or that the JIT engine includes it. If not available, substitute
   `overflow-hidden` with a fixed `max-h` equivalent.

5. **kanban.md test scope**: Confirm `tests/test_readme.py` `test_project_history_count`
   does NOT glob-scan all `.md` files (should be README.md-specific). If it does,
   the `prjNNNNNNN` references in `kanban.md` will inflate the count — @5test must
   scope the test to `README.md` only.

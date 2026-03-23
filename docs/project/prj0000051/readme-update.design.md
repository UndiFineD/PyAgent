---
project: prj0000051
role: "@3design"
status: COMPLETE
date: 2026-03-23
handoff_to: "@4plan"
inputs: readme-update.think.md
---

# readme-update.design.md — Design Blueprint for prj0000051

Structural and content design for the new `README.md`. This is the authoritative blueprint for
`@4plan` and `@6code`. All section lengths, emphasis notes, and grouping decisions are made here.

---

## 1. Approved H2/H3 Outline (Final Structure)

```
# PyAgent

## What is PyAgent?
## Quick Start
### Prerequisites
### Install
### Start
## NebulaOS — The Frontend
### Apps
### Technology
## Backend
### REST API
### WebSocket Protocol
## Rust Core — The Zero-Loop Engine
### Sub-modules
### Performance
## Architecture Decisions
## Project History (prj0000001–prj0000051)
## Future Roadmap
## Development Reference
### Running Tests
### Linting and Type Checking
### Workflows / CI
## License
```

Total estimated word count: **~2 000–2 400 words** (prose only, excluding code blocks and tables).

---

## 2. Section-by-Section Design Notes

---

### `# PyAgent` (title only)

No intro blurb under the title. The H1 stands alone. Place a one-line **status badge row** here
(CI badge, version badge, license badge). Badges should reference the actual GitHub Actions
workflow files and pyproject.toml version.

---

### `## What is PyAgent?`  
**Target: 200–300 words (single long paragraph)**

This is the most important section. Readers must immediately understand what they have in front of
them. Write one flowing narrative paragraph (do NOT bullet-list this section) covering:

1. **Identity & codename**: PyAgent v4.0.0-VOYAGER — a production-ready autonomous multi-agent
   swarm system for continuous, self-directed code improvement.
2. **The agent pipeline**: 10 specialized agents (`@0master` through `@9git`) that collaborate in
   a numbered pipeline — each with a distinct role: orchestrator, project manager, thinker,
   architect, planner, test writer, developer, executor, security scanner, git/GitHub.
3. **51-project history**: Every improvement is tracked as a `prjNNNNNNN` project; 51 projects
   have been executed to date, covering everything from async runtime to NebulaOS UI to the
   Rust acceleration core.
4. **The three-tier platform**: Python swarm logic + a Rust-accelerated core (41% performance
   gain, 30+ PyO3 sub-modules) + a browser-based OS-like frontend (NebulaOS).
5. **Transactional safety**: Four transaction managers (Storage, Memory, Process, Context) ensure
   every mutation is atomic and rollback-capable. The Rust layer uses X25519/ChaCha20-Poly1305
   encryption and Noise_XX transport.

Tone: confident, technical, specific — not marketing fluff. Cite the real numbers (666 tests,
51 projects, 41% gain, 317 tests for TMs alone) to ground the narrative.

---

### `## Quick Start`  
**Target: 80–120 words of prose + code blocks**

Brief framing sentence: the only thing needed to get the full stack running on a developer machine
is `install.ps1` then `start.ps1`.

#### `### Prerequisites`

Bullet list — be exact about what is *required* vs *recommended*:
- Python ≥ 3.12 (**required** — install aborts without it)
- Git (**recommended** — warned if absent)
- Rust / cargo (**recommended** — without it, the Rust core is not built; pass `-SkipRust` to suppress)
- Node.js / npm (**recommended** — without it, the Vite frontend is not built; pass `-SkipWeb` to suppress)

#### `### Install`

Show the one-liner plus the common flag variants in a PowerShell code block:

```powershell
.\install.ps1                    # Full install (Python + Rust + npm)
.\install.ps1 -SkipRust -SkipWeb # Python only — fastest
.\install.ps1 -Force             # Recreate .venv from scratch
.\install.ps1 -CI                # Non-interactive (CI pipelines)
```

Short paragraph: explain what `install.ps1` actually does — creates `.venv`, installs
`requirements.txt`, runs `maturin develop --release` in `rust_core/`, and runs
`npm install` in `web/`. Six colour-coded status lines at the end confirm each phase.

#### `### Start`

One-liner plus variants:

```powershell
.\start.ps1              # Start everything (runtime + backend + Vite)
.\start.ps1 -NoVite      # Backend only
.\start.ps1 status       # Check what is running
.\start.ps1 stop         # Shut everything down
.\start.ps1 restart      # Bounce all services
```

One paragraph: describe what gets started — Rust runtime binary, FastAPI/WebSocket backend,
Vite dev server. Explain the `.env` requirement (copy from `.env.template` before first run).
Mention service management via `.pyagent.pids` and automatic port-conflict resolution.

Access points after start:
- NebulaOS UI: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Health: `http://localhost:8000/health`

---

### `## NebulaOS — The Frontend`  
**Target: 200–250 words + two tables**

Open with a punchy single sentence: NebulaOS is the PyAgent UI — a browser-based OS-like shell
built on Vite + React + TypeScript, styled with Tailwind CSS, shipping with six built-in apps,
three themes, a taskbar, and a fully functional multi-agent IDE.

Describe the windowing system and taskbar: windows are draggable and resizable; the taskbar
auto-hides after 2 s (configurable via Settings modal, persisted to `localStorage`); the Start
menu provides app launchers, theme toggle, and logout.

Themes: `dark` (deep navy — default), `light`, `retro`.

Entry: `web/index.html` → `web/index.tsx` → `web/App.tsx`. Served at
`http://localhost:5173`.

#### `### Apps`

A table of all six apps (App | File | What it does). Emphasize CodeBuilder and Conky as the most
feature-rich:
- **CodeBuilder**: 10-agent pipeline, per-agent LLM selector (FLM / GPT-4.1 / GPT-5 Mini / Grok /
  Raptor), streaming Chat tab, Logs tab, Agent Doc tab with Markdown renderer + edit/preview toggle.
- **AgentChat**: full-screen streaming chat that renders `taskStarted` / `taskDelta` / `taskComplete`
  WebSocket deltas.
- **Conky**: real system monitor — polls `/api/metrics/system` every second, shows CPU %, memory,
  per-NIC network KB/s, disk read/write KB/s, 30-point sparkline charts.
- Calculator, Editor, Paint: standard desktop utilities.

#### `### Technology`

One-paragraph summary: Vite + React + TypeScript, Tailwind from CDN, custom CSS variables for OS
colour tokens (`--os-bg`, `--os-window`, etc.), `OsConfig` stored in `localStorage` under
key `nebula-os-config`.

---

### `## Backend`  
**Target: 150–200 words + two tables**

One paragraph: the backend is a FastAPI + WebSocket worker (`backend/app.py`) that bridges
NebulaOS to the Python swarm and Rust core. CORS is configured to allow `http://localhost:5173`
and `http://localhost:3000`. All mutable endpoints validate `agent_id` against an immutable
`frozenset` of 10 known agents — blocking path-traversal attacks.

#### `### REST API`

Full table of all 7 REST endpoints (Method | Path | Purpose) — include the security note inline
with the agent-log/agent-doc rows.

#### `### WebSocket Protocol`

Table of the 4 backend→frontend message types (type | fields | meaning) and note that
frontend→backend JSON is dispatched to `ws_handler.handle_message()`.

Mention the Fleet Load Balancer distinction: `python -m src.interface.ui.web.py_agent_web` is the
full fleet entry point; `backend/app.py` is the lightweight dev worker used by NebulaOS.

---

### `## Rust Core — The Zero-Loop Engine`  
**Target: 200–250 words + one table**

Lead with the **no-sync-loops policy**: `test_async_loops.py` statically audits every Python
source file at CI time and fails the build if any synchronous loop is found blocking the event
loop. All I/O, network, and subprocess calls are `async`. This is the defining performance
constraint of the entire codebase.

Explain what Rust does and why: computationally hot paths — metrics calculation, diff patching,
text search, encryption, KV cache, CRDT merge, transport — are delegated to the `rust_core`
PyO3 extension. It is compiled with `maturin develop --release` into a `cp313-win_amd64.pyd`.
The documented performance gain is **41% vs. pure Python**.

#### `### Sub-modules`

A readable list (not a giant inline CSV) — group them logically:
- **Crypto & Transport**: `security`, `transport`, `connectivity`
- **Memory & Storage**: `memory`, `fs`, `kv`
- **Compute & Inference**: `inference`, `neural`, `quantlora`, `attention`, `multimodal`
- **Metrics & Analysis**: `metrics`, `stats`, `analysis`
- **Scheduling & Agents**: `scheduling`, `registry`, `agents`, `distributed`
- **Utilities**: `text`, `search`, `formula`, `template`, `config`, `utils`, `validation`,
  `workspace`, `hardware`, `time`, `shell`, `mux`, `auction`, `base`

Total: 30+ named sub-modules under `#[pymodule] fn rust_core`.

#### `### Performance`

Bullet list of specific performance mechanisms:
- Native Myers diff engine for code patching
- DFA-based regex FSM for LLM structured output decoding (vectorized bitmask)
- Rust-accelerated KV cache RDMA transfer logic (disaggregated prefill/decode)
- `rayon` data-parallelism for array operations
- `dashmap` lock-free concurrent hash map
- `zeroize` for secure key material wiping

Key Cargo dependencies worth calling out: `tokio`, `quinn` (QUIC), `chacha20poly1305`,
`x25519-dalek`, `ed25519-dalek`, `snow` (Noise_XX), `rayon`, `ndarray`, `prometheus`.

---

### `## Architecture Decisions`  
**Target: 250–300 words — 8 numbered items**

Present as a numbered list (not a table). Each item: bold title + 1–2 sentence explanation.
These must be the exact 8 decisions from think.md section 8:

1. **Mixin-Based Agent Composition** — small focused mixins (`ReflectionMixin`, `KnowledgeMixin`,
   `IdentityMixin`, `PersistenceMixin`, …) rather than deep inheritance hierarchies; new behaviours
   are added by composing mixins, not subclassing.
2. **Core/Agent Separation** — domain logic in `*Core` classes (e.g., `CoderCore`); the Agent
   class handles only LLM orchestration and state. This boundary lets a Python core be replaced by
   Rust without touching the orchestration layer.
3. **Rust FFI Bridge for Hot Paths** — any identified hot loop is moved to `rust_core/` behind a
   thin PyO3 boundary; the Python API stays stable across the migration.
4. **No-Sync-Loops Policy (CI-Enforced)** — `test_async_loops.py` blocks any synchronous loop
   from entering the codebase; all I/O, network, and subprocess code must be `async`.
5. **Four Transaction Managers for Atomicity** — Storage, Memory, Process, and Context transactions
   ensure every mutation is atomic and rollback-capable. 317 tests cover these alone.
6. **UUID-Based Task Tracking** — tasks, memory entries, and work items carry UUID v4 identifiers
   for lineage, attribution, and deduplication across the swarm.
7. **Project Numbering Discipline** — every body of work gets a `prjNNNNNNN` ID allocated by
   `@0master`; branch name, project folder, and ID must agree. `@9git` rejects mixed-project
   changes; enforced by `test_enforce_branch.py`.
8. **Security-First Input Validation** — `agent_id` validated against an immutable `frozenset` at
   every REST endpoint and WebSocket handler; Rust transport uses Noise_XX, Ed25519, and X25519
   formal cryptographic protocols.

---

### `## Project History (prj0000001–prj0000051)`  
**Target: 50–80 words of intro + 4-group table**

Brief intro (2 sentences): "PyAgent has been built project-by-project over 51 tracked
improvements. Each group below represents a distinct phase of the platform's development."

Use a **Markdown table with four grouped sections** (render as four consecutive tables, each with
its own group header in bold above it, or use horizontal rules as separators). One row per
project: `prjID | Short Name | One-line Description`.

Note on absent folders: "prj0000043 and prj0000044 have branch allocations but no project
folder — this is a pre-existing gap recorded in master memory."

#### Group 1 — Foundation (prj0000001–prj0000010)

| Project | Name | Summary |
|---|---|---|
| prj0000001 | async-runtime | Eliminate all synchronous loops; Tokio-backed async runtime with PyO3 bindings (215+ tests) |
| prj0000002 | core-system | Core modules: runtime bootstrap, task_queue, agent_registry, memory, observability |
| prj0000003 | hybrid-llm-security | Rust encryption pipeline: ChaCha20-Poly1305 + X25519, key rotation, Python integration |
| prj0000004 | llm-context-consolidation | Single ContextWindow with token budget tracking |
| prj0000005 | llm-swarm-architecture | Swarm core: AgentRegistry, TaskScheduler, SwarmMemory, swarm metrics |
| prj0000006 | unified-transaction-manager | StorageTransaction + MemoryTransaction + ProcessTransaction pipeline (205 tests, 100% coverage) |
| prj0000007 | advanced-research | Five importable research packages (speculation, multimodal, rl, memory, runtime) |
| prj0000008 | agent-workflow | TaskState, Task, TaskQueue, WorkflowEngine, Chain-of-Recursive-Thought (CoRT) |
| prj0000009 | community-collaboration | FastAPI community chat, MCP tool registration, GitHub webhook integration |
| prj0000010 | context-management | ContextManager + SkillsRegistry with token windowing and skill discovery |

#### Group 2 — Core Implementation (prj0000011–prj0000020)

| Project | Name | Summary |
|---|---|---|
| prj0000011 | core-project-structure | Clean directory layout, module boundaries, import hygiene enforcement |
| prj0000012 | deployment-operations | Docker Compose (`deploy/`), provisioning scripts, container definitions |
| prj0000013 | dev-tools-autonomy | Self-directed code analysis and improvement workflow design |
| prj0000014 | dev-tools-capabilities | Dependency auditing, complexity analysis, metrics collection tooling |
| prj0000015 | dev-tools-implementation | `docs/helpers` developer tooling implementation |
| prj0000016 | dev-tools-structure | Directory scaffolding for `src/tools/` hierarchy |
| prj0000017 | dev-tools-utilities | Tool utilities package: CLI helpers, shared formatters, output adapters |
| prj0000018 | documentation-assets | MkDocs site, Mermaid/PlantUML diagram generation, autodoc tooling |
| prj0000019 | future-roadmap | Vision templates, milestone generator CLI, prioritization framework |
| prj0000020 | github-import | GitHub repository importer skeleton; webhook handling (HMAC verification open gap) |

#### Group 3 — Governance + Quality (prj0000021–prj0000042)

| Project | Name | Summary |
|---|---|---|
| prj0000021 | project-management-governance | PM risk matrix, governance templates, project tracking framework |
| prj0000022 | swarm-architecture | Swarm core: AgentRegistry, TaskScheduler, SwarmMemory, distributed metrics |
| prj0000023 | testing-infrastructure | CI enforcement, async-loop checker, pytest fixture improvements |
| prj0000024 | async-runtime-2 | Second async runtime wave — additional consolidation and test coverage |
| prj0000025 | core-system-2 | Additional core system modules and documentation |
| prj0000026 | test-coverage-quality | Python + Rust test coverage quality improvements |
| prj0000027 | encrypted-memory-blocks | X25519 ECDH + ChaCha20-Poly1305 memory block encryption (20 tasks) |
| prj0000028 | transport-t1 | Ed25519 identity, Noise_XX handshake, loopback transport, QUIC scaffold |
| prj0000029 | llm-ui-backend-worker | FastAPI WebSocket backend worker, WebRTC via aiortc |
| prj0000030 | agent-doc-frequency | Frequency analytics for agent doc reads/writes |
| prj0000031 | streaming-website | Real-time streaming website — live Vite output |
| prj0000032 | agents | Specialized agent implementations in `src/agents/` |
| prj0000033 | chat | ChatRoom, message models, streaming pipeline |
| prj0000034 | context-manager | Advanced context manager improvements, slot management |
| prj0000035 | multimodal | Multimodal capabilities package (vision, audio, video inputs) |
| prj0000036 | plugins | Plugin system: discovery, registration, runtime loading |
| prj0000037 | tools | `src/tools/`: tool registry, CLI wrappers, run_full_pipeline |
| prj0000038 | python-function-coverage | Function-level coverage tracking and gap reporting |
| prj0000039 | conftest-typing-fixes | Fix CI-blocking type annotation errors in `conftest.py` |
| prj0000040 | core-system-3 | Third core system wave: additional runtime integrations |
| prj0000041 | flm | FLM integration: all 18 tasks complete, OpenAI-compatible adapter, tool-call loop |
| prj0000042 | tools-crdt-security | CRDT bridge (`src/` ↔ `rust_core/crdt/`) + security tooling |

#### Group 4 — Recent Features (prj0000043–prj0000051)

| Project | Name | Summary |
|---|---|---|
| prj0000043 | p2p-security-deps | *(branch allocated, no folder)* libp2p 0.49→0.56 upgrade, initial Dependabot CVE fixes |
| prj0000044 | transaction-managers | *(branch allocated, no folder)* Stub TM interfaces for CI |
| prj0000045 | transaction-managers-full | Full four transaction managers with BaseTransaction ABC (317 tests, PR #137 merged) |
| prj0000046 | codebuilder-ui-redesign | Full CodeBuilder rewrite: 10-agent pipeline, per-agent LLM selector, Logs + Agent Doc tabs (PR #184) |
| prj0000047 | conky-real-metrics | Conky system monitor with real CPU/memory/network/disk metrics via psutil (PR #185 merged) |
| prj0000048 | taskbar-config | NebulaOS taskbar always-visible toggle; OS config persisted to localStorage (PR #186 merged) |
| prj0000049 | dependabot-security-fixes | 6 CVEs resolved: libp2p, yamux, ring, idna, ed25519-dalek, curve25519-dalek, snow (PR #187 merged) |
| prj0000050 | install-script | `install.ps1` one-command setup: Python venv, pip, maturin Rust build, npm (PR #188) |
| prj0000051 | readme-update | Replace thin README with comprehensive, accurate documentation (this project) |

---

### `## Future Roadmap`  
**Target: 120–160 words + a numbered list**

Brief intro (1 sentence): "The following ten projects are the highest-value opportunities
identified from gaps in the current codebase and architecture."

Then a numbered list — each item: bold project ID + name + 1-sentence description.
(See Section 4 of this design document for the canonical list.)

---

### `## Development Reference`  
**Target: 150–200 words**

#### `### Running Tests`

```powershell
.\.venv\Scripts\python.exe -m pytest -q          # Full suite (666 tests)
.\.venv\Scripts\python.exe -m pytest tests/ -v   # Verbose
.\.venv\Scripts\python.exe -m pytest tests/security/ # Security subset
```

Note 666 tests, organized in: `agents/`, `ci/`, `core/`, `docs/`, `fixtures/`,
`integration/`, `observability/`, `runtime/`, `security/`, `structure/`, `tools/`.

Mention the notable enforcer tests: `test_async_loops.py` (no sync loops), `test_enforce_branch.py`
(branch governance), CodeQL gate (`test_zzd/e/f/g`).

#### `### Linting and Type Checking`

```powershell
.\.venv\Scripts\python.exe -m flake8 .
.\.venv\Scripts\python.exe -m mypy src/
```

Max line length: 120 (configured in `pyproject.toml`).

#### `### Workflows / CI`

Brief list of GitHub Actions workflows (or reference `.github/workflows/`). Note that CI runs
flake8, mypy, pytest, and the CodeQL security gates on every push.

---

### `## License`  
**Target: 20–30 words**

Apache-2.0. One line pointing to `LICENSE` file and copyright year range.

---

## 3. Project Grouping Plan

Four groups across the 51 projects (detailed rationale):

| Group | Range | Theme | Count |
|---|---|---|---|
| Foundation | prj0000001–prj0000010 | Core infrastructure, async runtime, security, swarm, transactions | 10 |
| Core Implementation | prj0000011–prj0000020 | Project structure, deployment, dev tools, docs, GitHub import | 10 |
| Governance + Quality | prj0000021–prj0000042 | Governance, quality, security hardening, FLM, CRDT, UI bootstrap | 22 |
| Recent Features | prj0000043–prj0000051 | Transaction managers full, CodeBuilder redesign, Conky, taskbar, Dependabot, install script | 9 |

**Why 22 in Group 3?** The middle wave of the project was the longest consolidation period — CI
health, security tooling, specialized agents, streaming, plugins, CRDT, and FLM all landed here.
Splitting it further would make the table harder to read.

---

## 4. Ten Future Project Ideas (Canonical Definition)

These are the 10 projects `@6code` should write verbatim into the Roadmap section.

1. **prj0000052 — HMAC Webhook Verification**: Implement HMAC-SHA256 signature verification for
   all GitHub webhook events — the open gap from prj0000020.

2. **prj0000053 — Backend Authentication**: Add OAuth2 / API-key auth via FastAPI `Depends` to
   all `/api/` REST endpoints; no auth currently exists.

3. **prj0000054 — WebSocket E2E Encryption**: Wire the existing Rust Noise_XX / ChaCha20-Poly1305
   transport to the `/ws` session so agent conversation payloads are encrypted in transit.

4. **prj0000055 — Rust async-transport Activation**: Enable the `async-transport` Cargo feature
   (tokio + quinn + tokio-tungstenite) in the release build; run the QUIC layer end-to-end;
   add integration tests.

5. **prj0000056 — Agent Orchestration Visual Graph**: Add a NebulaOS app rendering the live swarm
   topology — active agents, task lineage, parent-child chains — via WebSocket + React
   force-directed graph.

6. **prj0000057 — Mobile-Responsive NebulaOS**: Add touch event support, a mobile-optimised app
   drawer, and responsive breakpoints so the UI is usable on phones and tablets.

7. **prj0000058 — Plugin Marketplace Browser**: Build a NebulaOS app for browsing, installing,
   and activating plugins from a local or remote registry — a UI for the existing `src/plugins/`
   system (prj0000036).

8. **prj0000059 — FLM Token Throughput Dashboard**: Persist FLM TPS benchmark runs to SQLite,
   expose `GET /api/benchmarks`, and render a throughput-over-time sparkline in Conky or a new
   NebulaOS app.

9. **prj0000060 — Theme Polish (Light + Retro)**: Produce full accessible colour sets for the
   `light` and `retro` themes and apply them consistently across all apps; the current palette is
   minimal.

10. **prj0000061 — Real Agent Execution from CodeBuilder**: Wire `ws_handler.handle_message()` to
    `WorkflowEngine` / the task queue so CodeBuilder conversations actually execute real agent
    pipelines and stream back results.

---

## 5. Writing Constraints for @6code

- Max line length in Markdown: **120 characters** (wrapping at 120 for prose lines prevents
  excessive horizontal scroll in raw view)
- Use fenced PowerShell code blocks (` ```powershell `) not generic ` ``` ` for all shell commands
- Keep all tables **pipe-aligned** (visual alignment preferred, but not enforced)
- The `What is PyAgent?` section must be a **single paragraph** — do not break it into bullets
- The Architecture Decisions section must use **numbered list** — do not use a table
- Do NOT add commentary in the Project History rows — keep to the one-line descriptions from
  think.md
- Badges row under H1: use actual shields.io URL patterns referencing `.github/workflows/`

---

## 6. Handoff Summary for @0master

### Final approved H2 list

```
## What is PyAgent?
## Quick Start
## NebulaOS — The Frontend
## Backend
## Rust Core — The Zero-Loop Engine
## Architecture Decisions
## Project History (prj0000001–prj0000051)
## Future Roadmap
## Development Reference
## License
```

### The 10 future project names

| # | ID | Short Name |
|---|---|---|
| 1 | prj0000052 | HMAC Webhook Verification |
| 2 | prj0000053 | Backend Authentication |
| 3 | prj0000054 | WebSocket E2E Encryption |
| 4 | prj0000055 | Rust async-transport Activation |
| 5 | prj0000056 | Agent Orchestration Visual Graph |
| 6 | prj0000057 | Mobile-Responsive NebulaOS |
| 7 | prj0000058 | Plugin Marketplace Browser |
| 8 | prj0000059 | FLM Token Throughput Dashboard |
| 9 | prj0000060 | Theme Polish (Light + Retro) |
| 10 | prj0000061 | Real Agent Execution from CodeBuilder |

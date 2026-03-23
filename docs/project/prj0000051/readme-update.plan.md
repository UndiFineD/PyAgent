---
project: prj0000051
role: "@4plan"
status: COMPLETE
date: 2026-03-23
handoff_to: "@6code"
inputs:
  - readme-update.think.md
  - readme-update.design.md
---

# readme-update.plan.md — Implementation Plan for prj0000051

Concrete tasks for `@6code` and acceptance criteria for `@5test`.
One deliverable: complete replacement of `README.md` in the repo root.

---

## Task Overview

| # | Task | Owner | File(s) touched |
|---|---|---|---|
| 1 | Write `README.md` — all sections per design blueprint | @6code | `README.md` |
| 2 | Verify structural test passes | @5test | `tests/` (read-only) |

Total tasks: **2**

---

## Task 1 — Write `README.md`

**Owner:** @6code
**File:** `README.md` (repo root — full replacement)

Write the complete file from scratch using the section order and content constraints below.
Do **not** preserve any text from the current thin `README.md`.

---

### Writing Constraints

- Max line length for prose: **120 characters** (hard rule — matches `pyproject.toml` settings)
- All shell commands use fenced ` ```powershell ` blocks — not generic ` ``` `
- Tables must be pipe-delimited; visual alignment preferred
- `## What is PyAgent?` must be a **single flowing paragraph** — no bullets
- `## Architecture Decisions` must use a **numbered list** — not a table
- Project History rows: one-line descriptions only — no added commentary
- Badges row under H1: use `shields.io` URL patterns referencing `.github/workflows/`

---

### Section-by-Section Content Specification

---

#### `# PyAgent` (H1)

Place a badge row immediately below the title. Three badges:

```markdown
![CI](https://github.com/<owner>/PyAgent/actions/workflows/python-core.yml/badge.svg)
![Version](https://img.shields.io/badge/version-4.0.0--VOYAGER-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
```

No intro blurb under H1 — badges then straight into `## What is PyAgent?`.

---

#### `## What is PyAgent?`

**One single paragraph, 200–300 words.** Must contain all of the following facts:

- PyAgent v4.0.0-VOYAGER — production-ready autonomous multi-agent swarm system
- Continuous self-directed code improvement: plan → design → test → code → validate → scan → merge
- 10 specialized agents `@0master` through `@9git`, each with a distinct role:
  orchestrator, project manager, thinker, architect, planner, test writer, developer,
  executor, security scanner, git/GitHub
- Every improvement tracked as a `prjNNNNNNN` project; 51 projects executed to date
- Three-tier platform: Python swarm logic + Rust-accelerated core + NebulaOS browser shell
- Rust core: 41% performance gain vs pure Python; 30+ PyO3 sub-modules
- 666 tests; 317 tests cover the four transaction managers alone
- Four transaction managers (Storage, Memory, Process, Context) — every mutation atomic
  and rollback-capable
- Rust layer: X25519/ChaCha20-Poly1305 encryption + Noise_XX transport
- Language stack: Python 3.12+ · Rust (maturin/PyO3) · TypeScript

Tone: confident and technical — cite real numbers, no marketing language.

---

#### `## Quick Start`

Brief framing sentence: the full dev stack runs with `.\install.ps1` then `.\start.ps1`.

##### `### Prerequisites`

Bullet list — required vs recommended:

```
- Python >= 3.12  **required** — install.ps1 aborts without it
- Git             recommended — warned if absent
- Rust / cargo    recommended — Rust core not built without it; pass -SkipRust to suppress
- Node.js / npm   recommended — Vite frontend not built without it; pass -SkipWeb to suppress
```

##### `### Install`

PowerShell code block with four variants:

```powershell
.\install.ps1                    # Full install (Python + Rust + npm)
.\install.ps1 -SkipRust -SkipWeb # Python only — fastest
.\install.ps1 -Force             # Recreate .venv from scratch
.\install.ps1 -CI                # Non-interactive (CI pipelines)
```

Follow with one short paragraph describing what `install.ps1` does:
- Creates/reuses `.venv`
- Installs `requirements.txt` (then `requirements-ci.txt` unless `-SkipDev`)
- Runs `maturin develop --release` inside `rust_core/`
- Runs `npm install` inside `web/`
- Prints six colour-coded status lines confirming each phase

##### `### Start`

One-liner plus variants:

```powershell
.\start.ps1              # Start everything (runtime + backend + Vite)
.\start.ps1 -NoVite      # Backend only, no frontend
.\start.ps1 status       # Check what is running
.\start.ps1 stop         # Shut everything down
.\start.ps1 restart      # Bounce all services
```

One paragraph explaining:
- Copy `.env.template` → `.env` before first run
- Starts: Rust standalone runtime binary, FastAPI/WebSocket backend, Vite dev server
- Uses `.pyagent.pids` for graceful stop/status
- Automatic port-conflict detection and resolution

Access points after start:
```
NebulaOS UI:  http://localhost:5173
Backend API:  http://localhost:8000
Health check: http://localhost:8000/health
```

---

#### `## NebulaOS — The Frontend`

Opening sentence (required exact facts):
> NebulaOS is the PyAgent UI — a browser-based OS-like shell built on Vite + React + TypeScript,
> styled with Tailwind CSS, shipping with six built-in apps, three themes, a taskbar, and a fully
> functional multi-agent IDE.

Then describe the windowing/taskbar system:
- Windows are draggable and resizable via `web/components/Window.tsx`
- Taskbar auto-hides after 2 s of inactivity
- Settings modal provides always-visible toggle — config persisted to `localStorage` under
  key `nebula-os-config`
- Start menu: app launchers, theme toggle, logout

Themes: `dark` (deep navy — default), `light`, `retro`.

Entry: `web/index.html` → `web/index.tsx` → `web/App.tsx`. Served at `http://localhost:5173`.

##### `### Apps`

Table — six rows:

| App | File | Description |
|---|---|---|
| **CodeBuilder** | `web/apps/CodeBuilder.tsx` | Multi-agent IDE: 10-agent pipeline, per-agent LLM selector (FLM / GPT-4.1 / GPT-5 Mini / Grok / Raptor), streaming Chat tab, Logs tab, Agent Doc tab with Markdown renderer + edit/preview toggle |
| **AgentChat** | `web/apps/AgentChat.tsx` | Full-screen streaming chat; renders `taskStarted` / `taskDelta` / `taskComplete` WebSocket deltas |
| **Conky** | `web/apps/Conky.tsx` | System monitor — polls `/api/metrics/system` every second; CPU %, memory (used/total/%), per-NIC network KB/s, disk read/write KB/s, 30-point sparkline charts |
| **Calculator** | `web/apps/Calculator.tsx` | Standard desktop calculator |
| **Editor** | `web/apps/Editor.tsx` | Simple text editor; shows Welcome.md on first login |
| **Paint** | `web/apps/Paint.tsx` | Pixel / canvas drawing app |

##### `### Technology`

One paragraph:
- Vite + React + TypeScript, Tailwind CSS loaded from CDN
- Custom CSS variables for OS colour tokens: `--os-bg`, `--os-window`, `--os-header`,
  `--os-text`, `--os-border`, `--os-accent`
- `OsConfig` stored in `localStorage` under key `nebula-os-config`
- `AppId` union type: `'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder'`

---

#### `## Backend`

Opening paragraph (required facts):
- FastAPI + WebSocket worker: `backend/app.py`
  (`FastAPI(title="PyAgent Backend Worker", version="0.1.0")`)
- CORS allow-list: `http://localhost:5173` and `http://localhost:3000`
- All mutable endpoints validate `agent_id` against an immutable `frozenset` of 10 known
  agent IDs — blocks path-traversal attacks
- Companion files: `backend/session_manager.py`, `backend/ws_handler.py`, `backend/models.py`

##### `### REST API`

Table — seven rows (6 REST + 1 WS):

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| GET | `/api/metrics/system` | Real-time CPU %, memory, per-NIC network KB/s, disk read/write KB/s, timestamp |
| GET | `/api/agent-log/{agent_id}` | Read `docs/agents/<agent_id>.log.md` (agent_id allowlist-validated) |
| PUT | `/api/agent-log/{agent_id}` | Overwrite `docs/agents/<agent_id>.log.md` (agent_id allowlist-validated) |
| GET | `/api/agent-doc/{agent_id}` | Read `.github/agents/<agent_id>.agent.md` (agent_id allowlist-validated) |
| PUT | `/api/agent-doc/{agent_id}` | Overwrite `.github/agents/<agent_id>.agent.md` (agent_id allowlist-validated) |
| WS | `/ws` | Real-time streaming; session managed by `SessionManager` |

##### `### WebSocket Protocol`

Table — four backend→frontend message types:

| Type | Key fields | Meaning |
|---|---|---|
| `taskStarted` | `task_id` | A new agent task has begun |
| `taskDelta` | `task_id`, `delta` | Streaming token chunk from active task |
| `taskComplete` | `task_id` | Task finished |
| `error` | `message` | Error occurred |

Note: frontend→backend JSON is dispatched to `ws_handler.handle_message()`.

Note: the Fleet Load Balancer entry point is distinct —
`python -m src.interface.ui.web.py_agent_web --port 8000`. `backend/app.py` is the
lightweight dev worker used by NebulaOS.

---

#### `## Rust Core — The Zero-Loop Engine`

Lead with the no-sync-loops policy:
> `tests/test_async_loops.py` statically audits every Python source file at CI time and fails the
> build if any synchronous loop is found blocking the event loop. All I/O, network, and subprocess
> calls are `async`. This is the defining performance constraint of the entire codebase.

Then explain what Rust does and why:
- Hot paths (metrics, diff patching, text search, encryption, KV cache, CRDT merge, transport)
  delegated to `rust_core/` PyO3 extension
- Compiled with `maturin develop --release` → `rust_core.cp313-win_amd64.pyd`
- **41% performance gain** vs pure Python (documented in `project/PyAgent.md`)

##### `### Sub-modules`

Grouped list (not inline CSV) — 30+ named sub-modules under `#[pymodule] fn rust_core`:

**Crypto & Transport:** `security`, `transport`, `connectivity`
**Memory & Storage:** `memory`, `fs`, `kv`
**Compute & Inference:** `inference`, `neural`, `quantlora`, `attention`, `multimodal`
**Metrics & Analysis:** `metrics`, `stats`, `analysis`
**Scheduling & Agents:** `scheduling`, `registry`, `agents`, `distributed`
**Utilities:** `text`, `search`, `formula`, `template`, `config`, `utils`, `validation`,
`workspace`, `hardware`, `time`, `shell`, `mux`, `auction`, `base`

##### `### Performance`

Bullet list — specific mechanisms:
- Native Myers diff engine for code patching
- DFA-based regex FSM for LLM structured output decoding (vectorized bitmask)
- Rust-accelerated KV cache RDMA transfer logic (disaggregated prefill/decode)
- `rayon` data-parallelism for array operations
- `dashmap` lock-free concurrent hash map
- `zeroize` for secure key-material wiping in memory

Key Cargo dependencies: `tokio`, `quinn` (QUIC), `chacha20poly1305`, `x25519-dalek`,
`ed25519-dalek`, `snow` (Noise_XX), `rayon`, `ndarray`, `prometheus`.

---

#### `## Architecture Decisions`

**Numbered list, 8 items — no table.** Each item: bold title + 1–2 sentence explanation.

1. **Mixin-Based Agent Composition** — Agents are built from small, focused mixins
   (`ReflectionMixin`, `KnowledgeMixin`, `IdentityMixin`, `PersistenceMixin`, …) rather than deep
   class hierarchies. New behaviours are added by composing mixins, not subclassing.

2. **Core/Agent Separation** — Domain logic lives in `*Core` classes (e.g., `CoderCore`); the
   `Agent` class handles only LLM orchestration and state management. This boundary allows a Python
   core to be replaced by Rust without touching the orchestration layer.

3. **Rust FFI Bridge for Hot Paths** — Any identified hot loop is moved to `rust_core/` behind a
   thin PyO3 boundary. The Python API stays stable across the migration.

4. **No-Sync-Loops Policy (CI-Enforced)** — `test_async_loops.py` blocks any synchronous loop
   from entering the codebase; all I/O, network, and subprocess code must be `async`.

5. **Four Transaction Managers for Atomicity** — Every mutation uses one of:
   `StorageTransaction` (filesystem), `MemoryTransaction` (in-process state),
   `ProcessTransaction` (subprocesses), or `ContextTransaction` (LLM context lineage).
   317 tests cover these four managers alone.

6. **UUID-Based Task Tracking** — Tasks, memory entries, and work items carry UUID v4 identifiers
   for lineage, attribution, and deduplication across the swarm.

7. **Project Numbering Discipline** — Every body of work gets a `prjNNNNNNN` ID allocated by
   `@0master` before work begins. Branch name, project folder, and ID must agree. `@9git` rejects
   mixed-project changes; enforced by `test_enforce_branch.py`.

8. **Security-First Input Validation** — `agent_id` validated against an immutable `frozenset`
   at every REST endpoint and WebSocket handler — preventing path-traversal and injection. The Rust
   transport uses Noise_XX, Ed25519, and X25519 formal cryptographic protocols.

---

#### `## Project History (prj0000001–prj0000051)`

Two-sentence intro:
> PyAgent has been built project-by-project over 51 tracked improvements. Each group below
> represents a distinct phase of the platform's development.

Note on absent folders (required sentence):
> prj0000043 and prj0000044 have branch allocations but no project folder — this is a
> pre-existing gap recorded in master memory.

Four table groups — exact content:

**Group 1 — Foundation (prj0000001–prj0000010)**

| Project | Name | Summary |
|---|---|---|
| prj0000001 | async-runtime | Eliminate all synchronous loops; Tokio-backed async runtime with PyO3 bindings (215+ tests) |
| prj0000002 | core-system | Core modules: runtime bootstrap, task_queue, agent_registry, memory, observability |
| prj0000003 | hybrid-llm-security | Rust encryption pipeline: ChaCha20-Poly1305 + X25519, key rotation, Python integration |
| prj0000004 | llm-context-consolidation | Single ContextWindow with token budget tracking |
| prj0000005 | llm-swarm-architecture | Swarm core: AgentRegistry, TaskScheduler, SwarmMemory, swarm metrics |
| prj0000006 | unified-transaction-manager | StorageTransaction + MemoryTransaction + ProcessTransaction pipeline (205 tests, 100% coverage) |
| prj0000007 | advanced-research | Five importable research packages: speculation, multimodal, rl, memory, runtime |
| prj0000008 | agent-workflow | TaskState, Task, TaskQueue, WorkflowEngine, Chain-of-Recursive-Thought (CoRT) |
| prj0000009 | community-collaboration | FastAPI community chat, MCP tool registration, GitHub webhook integration |
| prj0000010 | context-management | ContextManager + SkillsRegistry with token windowing and skill discovery |

**Group 2 — Core Implementation (prj0000011–prj0000020)**

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

**Group 3 — Governance + Quality (prj0000021–prj0000042)**

| Project | Name | Summary |
|---|---|---|
| prj0000021 | project-management-governance | PM risk matrix, governance templates, project tracking framework |
| prj0000022 | swarm-architecture | Swarm core: AgentRegistry, TaskScheduler, SwarmMemory, distributed metrics |
| prj0000023 | testing-infrastructure | CI enforcement, async-loop checker test, pytest fixture improvements |
| prj0000024 | async-runtime-2 | Second async runtime wave — additional consolidation and test coverage |
| prj0000025 | core-system-2 | Additional core system modules and documentation |
| prj0000026 | test-coverage-quality | Python + Rust test coverage quality improvements |
| prj0000027 | encrypted-memory-blocks | X25519 ECDH + ChaCha20-Poly1305 memory block encryption (20 tasks) |
| prj0000028 | transport-t1 | Ed25519 identity, Noise_XX handshake, loopback transport, QUIC scaffold |
| prj0000029 | llm-ui-backend-worker | FastAPI WebSocket backend worker, WebRTC via aiortc |
| prj0000030 | agent-doc-frequency | Frequency analytics for agent doc reads/writes |
| prj0000031 | streaming-website | Real-time streaming website — live Vite output |
| prj0000032 | agents | Specialized agent implementations in `src/agents/` |
| prj0000033 | chat | Chat system: ChatRoom, message models, streaming pipeline |
| prj0000034 | context-manager | Advanced context manager improvements, slot management |
| prj0000035 | multimodal | Multimodal capabilities package (vision, audio, video inputs) |
| prj0000036 | plugins | Plugin system: discovery, registration, runtime loading |
| prj0000037 | tools | `src/tools/`: tool registry, CLI wrappers, run_full_pipeline |
| prj0000038 | python-function-coverage | Function-level coverage tracking and gap reporting |
| prj0000039 | conftest-typing-fixes | Fix CI-blocking type annotation errors in `conftest.py` |
| prj0000040 | core-system-3 | Third core system wave: additional runtime integrations |
| prj0000041 | flm | FLM integration: all 18 tasks complete, OpenAI-compatible adapter, tool-call loop |
| prj0000042 | tools-crdt-security | CRDT bridge (`src/` ↔ `rust_core/crdt/`) + security tooling |

**Group 4 — Recent Features (prj0000043–prj0000051)**

| Project | Name | Summary |
|---|---|---|
| prj0000043 | p2p-security-deps | *(branch allocated, no folder)* libp2p 0.49→0.56 upgrade, 6 Dependabot CVE fixes |
| prj0000044 | transaction-managers | *(branch allocated, no folder)* Stub StorageTransaction/ProcessTransaction/ContextTransaction for CI |
| prj0000045 | transaction-managers-full | Full four transaction managers with BaseTransaction ABC (317 tests, PR #137 merged) |
| prj0000046 | codebuilder-ui-redesign | Full CodeBuilder rewrite: 10-agent pipeline, per-agent LLM selector, Logs tab, Agent Doc tab with Markdown viewer/editor (PR #184) |
| prj0000047 | conky-real-metrics | Conky system monitor with real-time CPU/memory/network/disk metrics via psutil (PR #185 merged) |
| prj0000048 | taskbar-config | NebulaOS taskbar always-visible toggle; OS config persisted to localStorage (PR #186 merged) |
| prj0000049 | dependabot-security-fixes | 6 CVEs resolved: libp2p, yamux, ring, idna, ed25519-dalek, curve25519-dalek, snow (PR #187 merged) |
| prj0000050 | install-script | `install.ps1` developer setup: Python venv, pip, maturin Rust build, npm (PR #188) |
| prj0000051 | readme-update | Replace thin `README.md` with comprehensive, accurate documentation (this project) |

---

#### `## Future Roadmap`

One-sentence intro:
> The following ten projects are the highest-value opportunities identified from gaps in the
> current codebase and architecture.

Numbered list — write verbatim:

1. **prj0000052 — HMAC Webhook Verification**: Implement HMAC-SHA256 signature verification for
   all GitHub webhook events — the open gap from prj0000020.
2. **prj0000053 — Backend Authentication**: Add OAuth2 / API-key auth via FastAPI `Depends` to all
   `/api/` REST endpoints; no auth layer currently exists.
3. **prj0000054 — WebSocket E2E Encryption**: Wire the existing Rust Noise_XX /
   ChaCha20-Poly1305 transport to the `/ws` session so agent conversation payloads are
   encrypted in transit.
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
   expose `GET /api/benchmarks`, and render throughput-over-time sparklines in NebulaOS.
9. **prj0000060 — Theme Polish (Light + Retro)**: Produce full accessible colour sets for the
   `light` and `retro` themes; apply consistently across all apps and components.
10. **prj0000061 — Real Agent Execution from CodeBuilder**: Wire `ws_handler.handle_message()` to
    `WorkflowEngine` / the task queue so CodeBuilder conversations execute real agent pipelines
    and stream back results.

---

#### `## Development Reference`

##### `### Running Tests`

```powershell
.\.venv\Scripts\python.exe -m pytest -q            # Full suite (666 tests)
.\.venv\Scripts\python.exe -m pytest tests/ -v     # Verbose
.\.venv\Scripts\python.exe -m pytest tests/security/  # Security subset
```

Mention:
- 666 tests collected (as of 2026-03-23)
- Test subdirectories: `agents/`, `ci/`, `core/`, `docs/`, `fixtures/`, `integration/`,
  `observability/`, `runtime/`, `security/`, `structure/`, `tools/`
- Notable enforcer tests: `test_async_loops.py` (no sync loops), `test_enforce_branch.py`
  (branch governance), CodeQL gate (`test_zzd_codeql_python.py`, `test_zze_codeql_javascript.py`,
  `test_zzf_codeql_rust.py`, `test_zzg_codeql_sarif_gate.py`)

##### `### Linting and Type Checking`

```powershell
.\.venv\Scripts\python.exe -m flake8 .
.\.venv\Scripts\python.exe -m mypy src/
```

Max line length: **120** (configured in `pyproject.toml`).

##### `### Workflows / CI`

Reference `.github/workflows/`. On every push, CI runs:
- `python-core.yml` — flake8, mypy, pytest
- `rust.yml` — `cargo test` + `cargo clippy`
- `smoke.yml` — fast smoke gate
- CodeQL security analysis (gate tests `test_zzd` through `test_zzg`)

---

#### `## License`

One sentence:

> Distributed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.
> Copyright 2024–2026 PyAgent Authors.

---

## Task 2 — Acceptance Criteria for @5test

### Structural checks (automated)

| # | Check | Pass condition |
|---|---|---|
| AC-01 | File exists | `README.md` exists at repo root |
| AC-02 | H1 title | First non-empty line is `# PyAgent` |
| AC-03 | Badges row present | Lines 2–6 contain at least one `shields.io` badge |
| AC-04 | All 10 required H2 headings present | See approved H2 list below |
| AC-05 | `## What is PyAgent?` is a single paragraph | No blank line within the section before next H2; no unordered list items in that section |
| AC-06 | `## Architecture Decisions` uses numbered list | Section contains `1.` … `8.` items; no `\|` table rows |
| AC-07 | Project History has exactly 51 rows | Count of `prj000` occurrences across all four groups equals 51 |
| AC-08 | Absent-folder note present | Lines containing `prj0000043` and `prj0000044` include the word `folder` |
| AC-09 | Future Roadmap has exactly 10 items | Numbered list items `1.` through `10.` each containing `prj000005` |
| AC-10 | No prose line exceeds 120 characters | `(Get-Content README.md \| Where-Object { $_.Length -gt 120 }).Count` = 0 |
| AC-11 | PowerShell blocks use language tag | All shell command fences use ` ```powershell ` |
| AC-12 | Key numbers present | File contains: `666`, `51`, `41%`, `317`, `v4.0.0`, `VOYAGER` |
| AC-13 | install.ps1 flag variants present | File contains `-SkipRust`, `-SkipWeb`, `-Force`, `-CI` |
| AC-14 | start.ps1 variants present | File contains `-NoVite`, `status`, `stop`, `restart` |
| AC-15 | Conky endpoint referenced | File contains `/api/metrics/system` |
| AC-16 | No stubs present | Zero occurrences of `TODO`, `FIXME`, `TBD` (case-insensitive) |

### Required H2 headings (AC-04 checklist)

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

### Manual review checklist (for @5test human review, not automated)

- [ ] `## What is PyAgent?` reads as one coherent paragraph (no subheadings, no bullets)
- [ ] All five LLM provider names present: FLM, GPT-4.1, GPT-5 Mini, Grok, Raptor
- [ ] All six NebulaOS apps listed in the Apps table: CodeBuilder, AgentChat, Conky,
      Calculator, Editor, Paint
- [ ] WebSocket protocol table has all four message types: `taskStarted`, `taskDelta`,
      `taskComplete`, `error`
- [ ] All eight Architecture Decisions present and numbered 1–8
- [ ] Rust sub-module groups cover: Crypto & Transport, Memory & Storage,
      Compute & Inference, Metrics & Analysis, Scheduling & Agents, Utilities
- [ ] `## License` present and references Apache-2.0 and `LICENSE` file
- [ ] No text copied verbatim from the old README that is incorrect or outdated

---

## Handoff Summary for @0master

**Tasks:** 2 (Task 1 = write `README.md`; Task 2 = verify acceptance criteria)

**Acceptance criteria summary:**
- 16 automated structural checks (AC-01 through AC-16) — all must pass
- 8-point manual review checklist — @5test gate before @9git merge
- `@5test` runs the automated checks; manual checklist is optional human gate

**Key numbers that must appear in the final README:**
`v4.0.0-VOYAGER`, `10 agents`, `51 projects`, `666 tests`, `41%`, `317 tests`,
`30+ sub-modules`, `4 transaction managers`

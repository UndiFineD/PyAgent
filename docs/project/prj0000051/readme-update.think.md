---
project: prj0000051
role: "@2think"
status: COMPLETE
date: 2026-03-23
handoff_to: "@3design"
---

# readme-update.think.md — Research Document for prj0000051

Raw research and fact-gathering for the README rewrite. Intended as input material for `@3design`.

---

## 1. PyAgent Identity

What PyAgent actually is — four core truths:

- **Autonomous multi-agent swarm system for code improvement**: PyAgent is v4.0.0-VOYAGER — a
  production-ready platform where 10 specialized AI agents (@0master through @9git) collaborate in
  a numbered pipeline to plan, design, test, code, validate, security-scan, and merge improvements
  to real codebases. Each project is tracked by a `prjNNNNNNN` identifier; 51 projects have been
  executed to date.

- **Rust-accelerated Python platform**: Computationally intensive operations (metrics, diffs, text
  search, encryption, neural inference helpers, KV cache, scheduling, CRDT merge, transport) are
  delegated to a `rust_core` PyO3 extension compiled with maturin. The Rust core exposes 30+
  named sub-modules to Python. The documented performance gain is 41% vs. pure Python baselines.

- **OS-like frontend shell ("NebulaOS")**: A Vite/React/TypeScript desktop-like interface running
  in the browser. The page title is literally *NebulaOS*. It provides a windowing system, a
  taskbar, a login screen, themes (dark/light/retro), and multiple built-in apps — including a
  system-monitor widget (Conky) with live CPU/memory/network/disk metrics and a full multi-agent
  IDE (CodeBuilder) with per-agent LLM selection.

- **Transactionally safe, security-hardened runtime**: Every filesystem mutation goes through one
  of four transaction managers (`StorageTransaction`, `MemoryTransaction`, `ProcessTransaction`,
  `ContextTransaction`). Agent identity is validated via an allowlist. Input validation prevents
  path-traversal attacks. The Rust core uses X25519 ECDH + ChaCha20-Poly1305 for memory
  encryption, Ed25519 identity, and the Noise_XX handshake for secure transport.

---

## 2. Frontend — NebulaOS

### Technology stack
- **Vite + React + TypeScript**, served at `http://localhost:5173` (configurable via `.env`)
- **Tailwind CSS** loaded from CDN; custom CSS variables for OS color tokens (`--os-bg`,
  `--os-window`, `--os-header`, `--os-text`, `--os-border`, `--os-accent`)
- Themes: `dark` (deep navy, default), `light`, `retro`
- Entry point: `web/index.html` (title: **NebulaOS**) → `web/index.tsx` → `web/App.tsx`

### Core system (App.tsx)
| Feature | Detail |
|---|---|
| Login screen | `web/components/Login.tsx` — guards the desktop |
| Windowing | `web/components/Window.tsx` — draggable, resizable, minimize/maximize |
| Taskbar | Auto-hide after 2 s of inactivity; configurable always-visible pin via Settings |
| Start menu | Hamburger menu with app launchers, theme toggle, logout |
| Clock | Live 1-second clock in the taskbar |
| OS Config | `osConfig` persisted to `localStorage` under key `nebula-os-config` |
| Settings modal | Taskbar always-visible toggle; opened from taskbar Settings icon |

### Built-in apps (`web/apps/`)
| App | File | Description |
|---|---|---|
| **CodeBuilder** | `CodeBuilder.tsx` | Multi-agent IDE — 10 agents selectable, per-agent LLM chooser (FLM/GPT-4.1/GPT-5 Mini/Grok/Raptor), Chat tab, Logs tab, Agent Doc tab with Markdown renderer + edit/preview toggle |
| **AgentChat** | `AgentChat.tsx` | Full-screen streaming chat; connects to backend WebSocket; renders streaming `taskStarted`/`taskDelta`/`taskComplete` deltas |
| **Conky** | `Conky.tsx` | System monitor widget — polls `GET /api/metrics/system` every second; shows CPU %, memory (used/total/%), per-NIC network KB/s, disk read/write KB/s, 30-point sparkline charts; graceful offline state |
| **Calculator** | `Calculator.tsx` | Standard desktop calculator |
| **Editor** | `Editor.tsx` | Simple text editor; initial Welcome.md window shown on first login |
| **Paint** | `Paint.tsx` | Pixel/canvas drawing app |

### Shared components (`web/components/`)
| Component | Purpose |
|---|---|
| `Login.tsx` | Login gate before desktop is shown |
| `Window.tsx` | Window chrome — title bar, drag, resize, minimize, maximize |
| `AiPanel.tsx` | AI assistance panel |
| `VideoPanel.tsx` | Video/stream panel |
| `VoiceInput.tsx` | Microphone voice input component |

### Key types (`web/types.ts`)
- `AppId`: `'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder'`
- `WindowState`: position, dimensions, z-index, minimized/maximized flags
- `Theme`: id in `'dark' | 'light' | 'retro'`
- `OsConfig`: `{ taskbarAlwaysVisible: boolean }`

### LLM providers in CodeBuilder
`flm` (FLM default), `gpt41` (GPT-4.1), `gpt5mini` (GPT-5 Mini), `grok` (Grok Code Fast 1),
`raptor` (Raptor Mini preview)

### Agent pipeline in CodeBuilder
10 agents with distinct roles and color coding:
| ID | Name | Role | Color |
|---|---|---|---|
| 0master | @0master | Orchestrator | purple |
| 1project | @1project | Project Manager | blue |
| 2think | @2think | Options Explorer | cyan |
| 3design | @3design | Architect | indigo |
| 4plan | @4plan | Planner (TDD) | sky |
| 5test | @5test | QA / Red Phase | yellow |
| 6code | @6code | Developer | green |
| 7exec | @7exec | Runtime Validator | orange |
| 8ql | @8ql | Security Scanner | red |
| 9git | @9git | Git / GitHub | slate |

---

## 3. Backend

### Framework & entry
- **FastAPI** `backend/app.py` — `FastAPI(title="PyAgent Backend Worker", version="0.1.0")`
- CORS: allow-list `http://localhost:5173` and `http://localhost:3000`
- Companion files: `backend/session_manager.py`, `backend/ws_handler.py`, `backend/models.py`
- Started via `start.ps1` (or directly with `uvicorn backend.app:app --reload`)

### REST endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| GET | `/api/metrics/system` | Real-time system metrics: CPU %, memory (used/total/%), per-NIC network KB/s (filtered: no lo/docker/veth/br-), disk read/write KB/s, timestamp |
| GET | `/api/agent-log/{agent_id}` | Read `docs/agents/<agent_id>.log.md` |
| PUT | `/api/agent-log/{agent_id}` | Overwrite `docs/agents/<agent_id>.log.md` |
| GET | `/api/agent-doc/{agent_id}` | Read `.github/agents/<agent_id>.agent.md` |
| PUT | `/api/agent-doc/{agent_id}` | Overwrite `.github/agents/<agent_id>.agent.md` |

**Security note:** `agent_id` is validated against a frozen set allowlist
(`0master, 1project, 2think, 3design, 4plan, 5test, 6code, 7exec, 8ql, 9git`) — prevents
path-traversal attacks.

### WebSocket endpoint
| Path | Purpose |
|---|---|
| `WS /ws` | Real-time streaming; session managed by `SessionManager` |

**Message protocol (backend → frontend):**
- `{"type": "taskStarted", "task_id": "..."}` — new agent task begins
- `{"type": "taskDelta", "task_id": "...", "delta": "..."}` — streaming token chunk
- `{"type": "taskComplete", "task_id": "..."}` — task finished
- `{"type": "error", "message": "..."}` — error occurred

**Message protocol (frontend → backend):** JSON dispatched to `ws_handler.handle_message()`

### Fleet Load Balancer reference
The `project/PyAgent.md` quick-start documents:
```powershell
python -m src.interface.ui.web.py_agent_web --port 8000
```
This is the full Fleet Load Balancer entry point (distinct from the `backend/` worker).
The `backend/app.py` is the current active, tested component used by NebulaOS.

---

## 4. Rust Core

### Overview
- Location: `rust_core/`
- Built with `maturin` (PyO3 0.24.1) into `rust_core.cp313-win_amd64.pyd`
- Crate type: `cdylib` (Python extension module)
- Entry: `rust_core/src/lib.rs` — registers 30+ sub-modules under `#[pymodule] fn rust_core`

### Sub-modules registered to Python
`agents`, `analysis`, `attention`, `auction`, `base`, `config`, `connectivity`, `distributed`,
`formula` (+ top-level `evaluate_formula`), `fs`, `hardware`, `inference`, `kv`, `memory`,
`metrics`, `multimodal`, `mux`, `neural`, `quantlora`, `registry`, `scheduling`, `search`,
`security`, `shell`, `stats`, `template`, `text`, `time`, `transport`, `utils`, `validation`,
`workspace`, `distributed`,
`infrastructure::services::dev::scripts::run_fleet_self_improvement`

### Key dependencies (Cargo.toml)
| Crate | Purpose |
|---|---|
| `pyo3 = "0.24.1"` | Python bindings |
| `tokio` (optional, `async-transport`) | Async runtime |
| `quinn` (optional) | QUIC transport |
| `tokio-tungstenite` (optional) | WebSocket over Tokio |
| `chacha20poly1305` | ChaCha20-Poly1305 AEAD encryption |
| `x25519-dalek` | X25519 Diffie-Hellman key exchange |
| `ed25519-dalek` | Ed25519 signatures |
| `snow` | Noise protocol framework (Noise_XX) |
| `rayon` | Data-parallelism |
| `ndarray` + `rayon` | Vectorized array computation |
| `dashmap` | Concurrent hash map |
| `zeroize` | Secure memory zeroing |
| `uuid v1` | UUID v4 generation |
| `prometheus` | Metrics exposure |
| `evalexpr` | Expression evaluation |
| `sysinfo` | Hardware/system info |

### Feature flags
- `extension-module`: PyO3 extension (default build)
- `async-transport`: activates tokio + quinn + tokio-tungstenite for QUIC/WS transport
- `amd_npu`: AMD NPU acceleration (stub)

### Performance story
- 41% performance gain vs. pure Python (documented in `project/PyAgent.md`)
- Native Myers diff engine for code patching
- DFA-based regex FSM for LLM structured output decoding (vectorized bitmask)
- Rust-accelerated KV cache RDMA transfer logic (disaggregated prefill/decode)
- Auto-loaded via `dotenv()` from `.env` on import

---

## 5. install.ps1 Summary

**File:** `install.ps1` — full developer setup script (added in prj0000050, PR #188)

### Parameters
| Flag | Effect |
|---|---|
| `-SkipRust` | Skip Rust toolchain check and `maturin develop` build |
| `-SkipWeb` | Skip Node/npm check and `web/node_modules` installation |
| `-SkipDev` | Skip `requirements-ci.txt` (dev/CI tooling) |
| `-CI` | Non-interactive mode; missing optional tools emit warnings, not prompts |
| `-Force` | Force recreation of `.venv` even if already exists |

### Installation phases
1. **Prerequisites check** — Python ≥ 3.12 (required, aborts if missing), Git (warn), Rust/cargo
   (warn unless `-SkipRust`), Node/npm (warn unless `-SkipWeb`)
2. **Python virtual environment** — creates/reuses `.venv`; activates it
3. **Pip install** — `requirements.txt` first, then `requirements-ci.txt` (unless `-SkipDev`)
4. **Maturin build** — `maturin develop --release` in `rust_core/` (skipped if no cargo or
   `-SkipRust`)
5. **npm install** — `npm install` in `web/` (skipped if no npm or `-SkipWeb`)
6. **Summary** — prints color-coded completion summary of each phase's status

### Example invocations
```powershell
.\install.ps1                    # Full installation
.\install.ps1 -SkipRust -SkipWeb # Python only
.\install.ps1 -Force             # Recreate .venv and reinstall everything
.\install.ps1 -CI                # Non-interactive (CI pipelines)
```

---

## 6. start.ps1 Summary

**File:** `start.ps1` — PyAgent dev stack manager

### Commands
| Command | Action |
|---|---|
| `start` (default) | Start all services |
| `stop` | Stop all running services (by PID file) |
| `restart` | Stop then start all services |
| `status` | Show which services are currently running |
| `help` | Show command reference |

### Flags
- `-NoVite`: skip the Vite dev server (backend-only mode)

### Services managed
| Service | Description | Port env var |
|---|---|---|
| `runtime` | Rust standalone binary (auto-launched when built at `rust_core\runtime\target\release\runtime.exe`) | `RUNTIME_PORT` |
| `backend` | Python FastAPI/WebSocket worker | `BACKEND_PORT` |
| `vite` | Vite dev server | `VITE_PORT` |

### Key behaviors
- Reads `.env` file (requires `.env.template` → `.env` copy before first run)
- Writes PID file `.pyagent.pids` for graceful stop/status
- Port conflict detection: finds process on port, kills it, waits 400 ms, proceeds
- Clean port-free helpers added in prj0000046

### Example invocations
```powershell
.\start.ps1              # Start everything
.\start.ps1 stop         # Shut everything down
.\start.ps1 status       # Check what's running
.\start.ps1 -NoVite      # Backend only, no frontend
.\start.ps1 restart      # Restart all services
```

---

## 7. Project History — All 51 Projects

Note: prj0000043 and prj0000044 are absent from `docs/project/` inventory. This is a
pre-existing gap recorded in the master memory — they have allocated branches but no
corresponding project folder.

| # | Short Name | One-line Description |
|---|---|---|
| prj0000001 | async-runtime | Eliminate all synchronous loops; implement Tokio-backed async runtime with PyO3 bindings (215+ tests passing) |
| prj0000002 | core-system | Core infrastructure modules: runtime bootstrap, task_queue, agent_registry, memory, observability |
| prj0000003 | hybrid-llm-security | Rust encryption pipeline: ChaCha20-Poly1305 + X25519, Python integration, key rotation |
| prj0000004 | llm-context-consolidation | Consolidate LLM context into a single ContextWindow with token budget tracking |
| prj0000005 | llm-swarm-architecture | Swarm infrastructure: AgentRegistry, TaskScheduler, SwarmMemory, swarm metrics |
| prj0000006 | unified-transaction-manager | StorageTransaction + MemoryTransaction + ProcessTransaction full pipeline (205 tests, 100% coverage) |
| prj0000007 | advanced-research | Five skeleton research packages (importable): speculation, multimodal, rl, memory, runtime |
| prj0000008 | agent-workflow | TaskState, Task, TaskQueue, WorkflowEngine, Chain-of-Recursive-Thought (CoRT) |
| prj0000009 | community-collaboration | FastAPI community chat, MCP tool registration, GitHub webhook integration |
| prj0000010 | context-management | ContextManager + SkillsRegistry with token windowing and skill discovery |
| prj0000011 | core-project-structure | Clean directory layout, module boundaries, import hygiene enforcement |
| prj0000012 | deployment-operations | Docker Compose (`deploy/`), provisioning scripts, container definitions |
| prj0000013 | dev-tools-autonomy | Autonomy tool design: self-directed code analysis and improvement workflows |
| prj0000014 | dev-tools-capabilities | Tool capabilities: dependency auditing, complexity analysis, metrics collection |
| prj0000015 | dev-tools-implementation | docs/helpers implementation for developer tooling |
| prj0000016 | dev-tools-structure | Directory scaffolding for `src/tools/` hierarchy |
| prj0000017 | dev-tools-utilities | Tool utilities package: CLI helpers, shared formatters, output adapters |
| prj0000018 | documentation-assets | MkDocs site, Mermaid/PlantUML diagram generation, autodoc tooling |
| prj0000019 | future-roadmap | Vision templates, milestone generator CLI, prioritization framework |
| prj0000020 | github-import | GitHub repository importer skeleton; webhook handling (HMAC verification open gap) |
| prj0000021 | project-management-governance | PM risk matrix, governance templates, project tracking framework |
| prj0000022 | swarm-architecture | Swarm core: AgentRegistry, TaskScheduler, SwarmMemory, distributed metrics |
| prj0000023 | testing-infrastructure | CI enforcement, async-loop checker test, pytest fixture improvements |
| prj0000024 | async-runtime-2 | Second async runtime wave — additional consolidation and test coverage |
| prj0000025 | core-system-2 | Additional core system modules and documentation |
| prj0000026 | test-coverage-quality | Python + Rust test coverage quality improvements |
| prj0000027 | encrypted-memory-blocks | X25519 ECDH + ChaCha20-Poly1305 memory block encryption (20 tasks) |
| prj0000028 | transport-t1 | Ed25519 identity, Noise_XX handshake, loopback transport, QUIC scaffold |
| prj0000029 | llm-ui-backend-worker | FastAPI WebSocket backend worker, WebRTC via aiortc |
| prj0000030 | agent-doc-frequency | Track how often each agent doc is read/written; frequency analytics |
| prj0000031 | streaming-website | Real-time streaming website — COMPLETE, serving live Vite output |
| prj0000032 | agents | Specialized agent implementations in `src/agents/` |
| prj0000033 | chat | Chat system: ChatRoom, message models, streaming pipeline |
| prj0000034 | context-manager | Advanced context manager improvements, slot management |
| prj0000035 | multimodal | Multimodal capabilities package (vision, audio, video inputs) |
| prj0000036 | plugins | Plugin system: discovery, registration, runtime loading |
| prj0000037 | tools | `src/tools/` directory: tool registry, CLI wrappers, run_full_pipeline |
| prj0000038 | python-function-coverage | Python function-level coverage tracking and gap reporting |
| prj0000039 | conftest-typing-fixes | Fix CI-blocking type annotation errors in `conftest.py` |
| prj0000040 | core-system-3 | Third core system wave: additional runtime integrations |
| prj0000041 | flm | FLM (Fastflow LLM) integration: all 18 tasks complete, OpenAI-compatible adapter, tool-call loop |
| prj0000042 | tools-crdt-security | CRDT bridge (`src/` ↔ `rust_core/crdt/`) + security tooling (DONE, PR open) |
| prj0000043 | p2p-security-deps | *(folder absent)* libp2p 0.49→0.56 upgrade, 6 Dependabot CVE fixes (branch allocated) |
| prj0000044 | transaction-managers | *(folder absent)* Stub StorageTransaction/ProcessTransaction/ContextTransaction for CI |
| prj0000045 | transaction-managers-full | Full four transaction managers with BaseTransaction ABC (317 tests, PR #137 MERGED) |
| prj0000046 | codebuilder-ui-redesign | Full CodeBuilder rewrite: 10-agent pipeline, per-agent LLM selector, Logs tab, Agent Doc tab with Markdown viewer/editor (PR #184) |
| prj0000047 | conky-real-metrics | Conky system monitor with real-time CPU/memory/network/disk metrics via psutil (PR #185 MERGED) |
| prj0000048 | taskbar-config | NebulaOS taskbar always-visible toggle in Settings modal; OS config persisted to localStorage (PR #186 MERGED) |
| prj0000049 | dependabot-security-fixes | 6 CVEs resolved: libp2p 0.49→0.56, yamux, ring, idna, ed25519-dalek, curve25519-dalek, snow (PR #187 MERGED) |
| prj0000050 | install-script | `install.ps1` developer setup script: Python venv, pip, maturin Rust build, npm web deps (PR #188 open) |
| prj0000051 | readme-update | Replace thin `README.md` with comprehensive, accurate documentation (this project) |

---

## 8. Key Architecture Decisions

1. **Mixin-based agent composition (Synaptic Modularization)**: Agents are built from small,
   focused mixins (`ReflectionMixin`, `KnowledgeMixin`, `IdentityMixin`, `PersistenceMixin`, etc.)
   rather than deep class hierarchies. New behaviours are added by composing mixins, not
   subclassing.

2. **Core/Agent separation**: Domain logic lives in `*Core` classes (e.g., `CoderCore`); the Agent
   class handles only orchestration, LLM prompting, and state management. This boundary enables
   the Python core to be replaced by a Rust implementation without changing the orchestration layer.

3. **Rust FFI bridge for performance-critical paths**: Any path identified as a hot loop
   (high-frequency or CPU-heavy) is moved to `rust_core/` behind a thin PyO3 boundary. The Python
   API stays stable across the migration.

4. **No-sync-loops policy** (enforced by test): `test_async_loops.py` statically audits all Python
   source files and fails CI if any synchronous loops block the event loop. All I/O, network, and
   subprocess calls must be `async`.

5. **Four transaction managers for atomicity**: Every state mutation uses one of:
   - `StorageTransaction` — filesystem changes with rollback on failure
   - `MemoryTransaction` — in-process memory / agent state
   - `ProcessTransaction` — subprocess / external process execution
   - `ContextTransaction` — LLM context lineage tracking (prevents infinite recursion, task attribution)

6. **UUID-based task tracking**: Tasks, memory entries, and work items carry UUID identifiers for
   lineage, attribution, and deduplication across the swarm.

7. **Project numbering discipline**: Every body of work gets a `prjNNNNNNN` identifier allocated by
   `@0master` before work begins. Branch name, project folder, and ID must agree. `@9git`
   rejects mixed-project changes. Enforced by `test_enforce_branch.py`.

8. **Security-first input validation**: Agent IDs validated against an immutable `frozenset` at
   every REST endpoint and WebSocket handler — preventing path traversal and injection. The Rust
   transport uses Noise_XX, Ed25519, and X25519 formal cryptographic protocols.

---

## 9. Test Infrastructure

### Scale
- **666 tests collected** (as of 2026-03-23, `pytest --collect-only -q`)
- Located in `tests/` flat directory + subdirectories: `agents/`, `ci/`, `core/`, `docs/`,
  `fixtures/`, `integration/`, `observability/`, `runtime/`, `security/`, `structure/`, `tools/`

### Notable test categories
| Category | Representative tests | Purpose |
|---|---|---|
| Async-loop enforcement | `test_async_loops.py` | Blocks any sync loops from entering codebase |
| Security | `tests/security/`, `test_security_bridge.py`, `test_security_rotation.py` | Encryption, key rotation, CRDT bridge |
| Structural | `tests/structure/`, `test_compile.py`, `test_repo_layout_scaffold.py` | Module layout, naming, import hygiene |
| CodeQL gate | `test_zzd_codeql_python.py`, `test_zze_codeql_javascript.py`, `test_zzf_codeql_rust.py`, `test_zzg_codeql_sarif_gate.py` | Static security analysis gate |
| Lint/type | `test_zza_lint_config.py`, `test_zzb_mypy_config.py`, `test_zzc_flake8_config.py` | Ruff/mypy/flake8 config health |
| CI gate | `tests/ci/` | CI policy checks |
| Backend | `test_backend_worker.py`, `test_backend_system_metrics.py`, `test_backend_ws_handler.py` | FastAPI/WebSocket backend |
| Rust | `test_rust_core.py`, `test_rust_crdt_merge.py`, `test_rust_p2p_binary.py` | PyO3 extension smoke tests |
| Transaction managers | `test_transaction_managers.py`, `test_StorageTransactionManager.py`, etc. | All four TMs |
| Project governance | `test_enforce_branch.py`, `test_quality_yaml.py` | Branch policy, doc quality |

---

## 10. Future Project Ideas

Based on gaps and open items found during research:

1. **prj0000052 — HMAC Webhook Verification**: `src/github_app.py` webhook signature verification
   is noted as an open gap from prj0000020. Implement HMAC-SHA256 verification for all GitHub
   webhook events to prevent spoofed payloads. (High security value, low scope.)

2. **prj0000053 — Backend Authentication**: The REST endpoints (`/api/agent-log/`,
   `/api/agent-doc/`) have no authentication layer. Add OAuth2/API-key auth via FastAPI `Depends`
   so the backend cannot be called by unauthorized clients.

3. **prj0000054 — WebSocket E2E Encryption**: `docs/E2E_ENCRYPTION.md` documents a plan for
   end-to-end encryption of WebSocket messages. Wire the existing Rust transport (Noise_XX,
   ChaCha20-Poly1305) to the `/ws` session so agent conversation payloads are encrypted in transit.

4. **prj0000055 — Rust async-transport Activation**: `async-transport` is a Cargo feature flag
   (tokio + quinn + tokio-tungstenite) currently disabled by default. Activate it in the release
   build; run the QUIC transport layer end-to-end; add integration tests.

5. **prj0000056 — Agent Orchestration Visual Graph**: Add a NebulaOS app (or CodeBuilder tab) that
   renders the live swarm topology — which agents are active, task lineage, parent-child chains —
   using WebSocket streaming + a React force-directed graph.

6. **prj0000057 — Mobile-Responsive NebulaOS**: The current UI is desktop-only (assumes pointer
   events, assumes drag). Add touch event support, a mobile-optimised layout (app drawer instead
   of taskbar), and responsive breakpoints for tablets and phones.

7. **prj0000058 — Plugin Marketplace Browser**: The `plugins` system (`src/plugins/`, prj0000036)
   exists but has no UI. Build a NebulaOS app for browsing, installing, and activating plugins
   from a local or remote registry — similar to a browser extension store.

8. **prj0000059 — FLM Token Throughput Dashboard**: The FLM TPS benchmark script
   (`scripts/FlmTpsBenchmark.py`, prj0000046) runs offline. Build a persistent
   throughput-over-time dashboard: store runs to SQLite, expose `GET /api/benchmarks`, render
   sparklines in NebulaOS Conky or a new app.

9. **prj0000060 — Dark/Light/Retro Theme Polish**: CSS variable values exist for all three themes
   but the `light` and `retro` palettes are minimal. A design pass should produce full accessible
   colour sets and apply them consistently across all apps and components.

10. **prj0000061 — Real Agent Execution from CodeBuilder**: CodeBuilder today communicates over
    WebSocket but the backend does not route messages to live agents. Wire
    `ws_handler.handle_message()` to `WorkflowEngine` / the task queue so CodeBuilder conversations
    actually execute agent pipelines and stream back real results.

---

## Key Facts Summary for @3design

| Fact | Value |
|---|---|
| Codename | VOYAGER |
| Version | 4.0.0 |
| Language | Python 3.12+ / Rust (maturin/PyO3) / TypeScript |
| Frontend | NebulaOS — Vite + React + TypeScript |
| Backend | FastAPI + WebSocket |
| Rust modules | 30+ exported sub-modules |
| Tests | 666 collected |
| Projects completed | 51 (prj0000001–prj0000051) |
| Performance gain | 41% vs pure Python |
| Agent pipeline | 10 agents (@0master–@9git) |
| Transaction managers | 4 (Storage, Memory, Process, Context) |
| Open gaps | HMAC webhook auth, backend auth, E2E WS encryption, async-transport activation |
| Themes | dark (default), light, retro |
| NebulaOS apps | CodeBuilder, AgentChat, Conky, Calculator, Editor, Paint |
| Install command | `.\install.ps1` |
| Start command | `.\start.ps1` |

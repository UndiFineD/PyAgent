#!/usr/bin/env python3
"""Temporary script — writes the new README.md for prj0000051. Delete after use."""
from pathlib import Path

README = r"""# PyAgent

![Build](https://github.com/UndiFineD/PyAgent/actions/workflows/python-core.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)
![Rust](https://img.shields.io/badge/rust-stable-orange)

*v4.0.0-VOYAGER — Autonomous multi-agent software development platform*

## What is PyAgent?

PyAgent is a fully autonomous, multi-agent software development platform built around a ten-stage
pipeline — @0master through @9git — that conceives, implements, tests, security-reviews, and merges
code changes entirely without human bottlenecks. Codenamed **v4.0.0-VOYAGER**, it runs a coordinated
swarm of ten specialised agents: a master coordinator that assigns and tracks numbered projects
(prjNNNNNNN), a project setup agent, a deep-research agent, a design agent, a planning agent, a
test-first agent, a coding agent, an execution agent, a security and CodeQL agent, and a git handoff
agent that stages, commits, pushes, and opens pull requests. The platform is built on a Python +
Rust + TypeScript stack: the core logic lives in `src/` as async-first Python agents and mixins; the
high-throughput operations — encryption, file diffing, metrics calculation, and transport — live in
`rust_core/`, a PyO3 crate compiled with maturin that brings a 41% performance gain over the prior
synchronous approach; and the user-facing shell is **NebulaOS**, a Vite + React + TypeScript
desktop-style UI with apps such as CodeBuilder, AgentChat, and Conky. Behind the UI sits a
FastAPI/WebSocket backend that provides the REST API and real-time agent streaming. Everything is
tested: the repository now carries 666 collected tests across unit, structural, security, and CI
categories, covering the 51 projects that have been delivered since the platform was conceived. The
317 tests added for the four transaction managers alone demonstrate the depth of coverage the swarm
demands of its own output. PyAgent's mission is simple: write code, test it, review it, and merge
it — autonomously, repeatably, and safely.

## Quick Start

### Prerequisites

- Windows (PowerShell 5.1+)
- Python >= 3.12
- Rust toolchain (`rustup` — for the Rust extension)
- Node.js >= 18 (optional — for the NebulaOS frontend)

### Install everything

```powershell
.\install.ps1
```

Skip specific components:

```powershell
.\install.ps1 -SkipRust          # Python only, no maturin build
.\install.ps1 -SkipWeb           # No npm / web dependencies
.\install.ps1 -SkipDev           # No dev/CI tools (ruff, mypy, pytest extras)
.\install.ps1 -Force             # Recreate .venv from scratch
.\install.ps1 -CI                # Non-interactive mode for CI pipelines
```

`install.ps1` creates `.venv`, upgrades pip, installs `requirements.txt`,
`backend/requirements.txt`, and (unless `-SkipDev`) `requirements-ci.txt`, runs
maturin to build the Rust extension, runs the scaffold script, and installs
`web/node_modules`. A summary is printed at the end.

### Start the full dev stack

```powershell
.\start.ps1
```

Control individual services:

```powershell
.\start.ps1 stop                 # Stop all running services
.\start.ps1 restart              # Stop then start
.\start.ps1 status               # Show which services are running
.\start.ps1 start -NoVite        # Backend + Rust runtime only
```

Services started:

| Service | Stack | Default port |
|---|---|---|
| Rust runtime | `rust_core` standalone binary | `RUNTIME_PORT` |
| Python backend | FastAPI / Uvicorn | `BACKEND_PORT` |
| Frontend | Vite dev server | `VITE_PORT` (5173) |

## NebulaOS — The Frontend

NebulaOS is an operating-system-style desktop shell built with Vite, React, and TypeScript in
`web/`. It provides a window manager, a taskbar with an always-visible toggle, desktop wallpaper,
and a suite of built-in applications. The metaphor is deliberate: developers interact with
PyAgent the way they interact with an OS — by launching apps, inspecting system state, and
composing workflows — rather than through raw CLI commands.

The React component tree is rooted at `web/src/App.tsx`. Each app runs inside a draggable,
resizable window managed by the desktop shell. The taskbar persists across all window states
and can be pinned or auto-hidden via the NebulaOS Settings modal (added in prj0000048).
Real-time system metrics are streamed from the FastAPI backend into Conky via the
`/api/metrics/system` endpoint, which was wired to `psutil` in prj0000047.

| App | Description |
|---|---|
| **CodeBuilder** | 10-agent autonomous IDE with a per-agent LLM provider selector |
|   | (supports OpenAI, Anthropic, Gemini, local Ollama, and FLM), |
|   | an Agent Docs tab with live Markdown editing, and a streaming Logs pane |
| **AgentChat** | Real-time streaming WebSocket chat with token-by-token rendering |
| **Conky** | Live system metrics dashboard: CPU, memory, disk, and network I/O |
|   | powered by `psutil` via the backend `/api/metrics/system` endpoint |
| **Calculator** | Standard four-function calculator |
| **Editor** | Plain-text and code editor |
| **Paint** | Simple canvas drawing app |

## Backend

The backend is a FastAPI application in `backend/` that exposes both REST and WebSocket
endpoints to the NebulaOS frontend and to external tooling. It is designed as a
**Fleet Load Balancer** node: multiple instances can run behind a reverse proxy, each
worker handling streaming agent sessions independently.

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check — returns `{"status": "ok"}` |
| GET | `/api/agent-doc/{id}` | Fetch an agent definition markdown file |
| PUT | `/api/agent-doc/{id}` | Update an agent definition file |
| GET | `/api/metrics/system` | Live CPU / memory / network I/O (Conky feed) |
| WS | `/ws` | Bidirectional agent chat and task streaming |

```powershell
# Start the backend
uvicorn backend.app:app --reload

# Health check
Invoke-RestMethod http://localhost:8000/health
```

The WebSocket endpoint (`/ws`) carries four message types: `task_start`, `log_line`,
`result`, and `error`. The CodeBuilder and AgentChat apps both consume this stream.

## Rust Core — The Zero-Loop Engine

The `rust_core/` directory is a PyO3 crate that compiles to a native Python extension via
maturin. It embeds a full Tokio async runtime so that every operation — encryption,
file watching, HTTP serving, inter-agent message passing — runs on a work-stealing
thread pool with no blocking synchronous loops anywhere in the hot path.

The **no-sync-loops policy** is enforced at the CI level: `tests/test_async_loops.py`
scans all production Python source files and fails the build the moment a blocking
`for` or `while` loop appears outside an explicitly allowlisted location. This is the
same guarantee Node.js developers rely on — an event loop that never stalls — applied
equally to Python and Rust code. The 41% performance gain measured in
`performance/metrics_bench.py` is a direct result of this architecture choice.

Key modules exported by `rust_core`:

- **Encryption**: ChaCha20-Poly1305 authenticated encryption, X25519 key exchange,
  Ed25519 signing, and Noise_XX transport handshake
- **Transaction managers**: StorageTransaction, MemoryTransaction,
  ProcessTransaction, ContextTransaction (PyO3-backed)
- **File operations**: bulk diff/patch, complexity analysis, atomic file replacement
- **Async primitives**: `spawn`, `on`, `emit`, `watch_file`, channels, timers

```powershell
# Build the Rust extension
maturin develop --manifest-path rust_core/Cargo.toml
```

```python
from rust_core import spawn, on, emit, watch_file

spawn(my_async_task())
on("data", lambda payload: process(payload))
emit("data", {"key": "value"})
watch_file("config.json", lambda path: reload_config(path))
```

The PyO3 bindings are thin wrappers; if an operation ever needs more Rust
throughput, it can be rewritten in-place without touching any Python call-site.

## Architecture Decisions

1. **Mixin composition** — `BaseAgent` delegates shared behaviours (persistence,
   memory, identity, auditing) to mixins in `src/core/base/mixins/`, keeping agent
   classes focused on orchestration and LLM prompting rather than plumbing.

2. **Core/Agent separation** — domain logic lives in `*Core` classes (e.g.,
   `CoderCore`) that contain no AI prompting, so they can be accelerated with Rust
   FFI or replaced with a faster implementation without touching orchestration code.

3. **Rust FFI for hot paths** — all high-throughput operations (metrics calculation,
   bulk file replacement, encryption, complexity analysis) live in `rust_core/` and
   are exposed to Python via PyO3 bindings compiled with maturin.

4. **No-sync-loops policy** — `tests/test_async_loops.py` runs in CI and fails the
   build whenever a blocking `for`/`while` loop appears in production code, enforcing
   async-first development across the entire codebase.

5. **Four transaction managers** — `StorageTransaction`, `MemoryTransaction`,
   `ProcessTransaction`, and `ContextTransaction` wrap every file-system and process
   change, enabling atomic rollback on failure and full auditability of every
   mutation the swarm makes.

6. **UUID-based operation tracking** — every task, context window, memory operation,
   and agent handoff is labelled with a UUID, enabling complete lineage tracing across
   the swarm and preventing duplicate execution.

7. **prjNNNNNNN governance** — all work is organised into numbered projects that
   follow the full 10-agent pipeline, ensuring every change has a design rationale,
   a test plan, a security review, and a PR before it reaches `main`.

8. **Security allowlist validation** — all AI-generated tool calls pass through an
   allowlist checker before execution, providing a defence-in-depth layer against
   prompt injection and tool abuse by any agent in the swarm.

## Project History (prj0000001–prj0000051)

PyAgent has been built iteratively through 51 focused projects, each following the
full 10-agent pipeline from @0master through @9git.

### Foundation (prj0000001–prj0000010)

| Project | Name | Delivered |
|---|---|---|
| prj0000001 | Async Runtime | Tokio-backed async helpers replacing synchronous loops |
| prj0000002 | Core System | BaseAgent + mixin architecture, agent state manager |
| prj0000003 | Hybrid LLM Security | Rust encryption core: ChaCha20-Poly1305, X25519, Ed25519 |
| prj0000004 | LLM Context Consolidation | Unified context window management across all agents |
| prj0000005 | LLM Swarm Architecture | Multi-agent coordination topology and task routing |
| prj0000006 | Unified Transaction Manager | StorageTransaction + MemoryTransaction base impl |
| prj0000007 | Advanced Research | Deep analysis framework and alternative-exploration templates |
| prj0000008 | Agent Workflow | 10-stage pipeline formalised: @0master through @9git |
| prj0000009 | Community Collaboration | CONTRIBUTING.md, CODE_OF_CONDUCT.md, governance docs |
| prj0000010 | Context Management | ContextTransaction, task lineage, recursion prevention |

### Core Implementation (prj0000011–prj0000020)

| Project | Name | Delivered |
|---|---|---|
| prj0000011 | Core Project Structure | Canonical `src/` layout, package boundaries |
| prj0000012 | Deployment Operations | `compose.yaml`, `Dockerfile.*`, provisioning scripts |
| prj0000013 | Dev Tools Autonomy | Autonomous self-improvement tool scaffolding |
| prj0000014 | Dev Tools Capabilities | Tool registry and capability model |
| prj0000015 | Dev Tools Implementation | Concrete tool implementations (file, search, exec) |
| prj0000016 | Dev Tools Structure | Tool loader and plugin architecture |
| prj0000017 | Dev Tools Utilities | Shared utility library for all agent tools |
| prj0000018 | Documentation Assets | `docs/` hierarchy, templates, and style guide |
| prj0000019 | Future Roadmap | Research notes and long-horizon planning artifacts |
| prj0000020 | GitHub Import | Repo cloning + per-file architecture doc generation |

### Governance & Quality (prj0000021–prj0000042)

| Project | Name | Delivered |
|---|---|---|
| prj0000021 | Project Management Governance | Risk register, budget model, milestone tracker |
| prj0000022 | External Repos Tracking | `.external/` import registry and tracking |
| prj0000023 | Naming Standards | PascalCase module naming guide, import conventions |
| prj0000024 | Code of Conduct | Contributor covenant and enforcement procedures |
| prj0000025 | Contributing Guide | PR process, branch hygiene, review checklist |
| prj0000026 | Architecture ADR Template | Architecture Decision Record template and first ADRs |
| prj0000027 | Onboarding Docs | Developer onboarding guide and environment setup |
| prj0000028 | API Reference | REST and WebSocket API reference documentation |
| prj0000029 | Performance Docs | Benchmark methodology and results archive |
| prj0000030 | Standards: Code Style | Ruff + mypy configuration, 120-char line limit |
| prj0000031 | Standards: Commit Style | Conventional commits, scope taxonomy |
| prj0000032 | Standards: Test Style | Test naming, fixture conventions, coverage targets |
| prj0000033 | Standards: Security | OWASP checklist, SAST tooling integration |
| prj0000034 | Standards: Docs | Markdown style, link hygiene, ADR format |
| prj0000035 | Standards: CI | GitHub Actions workflow structure and naming |
| prj0000036 | Standards: Release | SemVer policy, changelog format, tag naming |
| prj0000037 | Tools CRDT Security | CRDT data structures and security audit on shared state |
| prj0000038 | Project Management | Governance model, risk register, milestone polish |
| prj0000039 | Conftest Typing Fixes | pytest config, type annotation fixes, import guards |
| prj0000040 | FLM Integration | FLM provider routing and integration scaffolding |
| prj0000041 | FLM Benchmark | FLM provider TPS benchmarking framework |
| prj0000042 | Agent Workflow Polish | Orchestration refinements, handoff rule clarifications |

### Recent Features (prj0000043–prj0000051)

| Project | Name | Delivered |
|---|---|---|
| prj0000043 | P2P Security Deps | `libp2p` 0.49→0.56: resolved 6 CVEs (yamux, ring, idna, |
|   |   | ed25519-dalek, curve25519-dalek, snow); full security test suite |
| prj0000044 | Transaction Manager Stubs | CI stubs for missing StorageTransaction/ProcessTransaction |
| prj0000045 | Transaction Managers Full | Full impl of all four transaction managers; 317 tests pass |
| prj0000046 | FLM TPS Benchmark | `scripts/FlmTpsBenchmark.py` — per-provider tokens/sec metrics |
| prj0000047 | Conky Real Metrics | Live CPU / memory / network I/O via `psutil` in NebulaOS |
| prj0000048 | Taskbar Config | Always-visible taskbar toggle in NebulaOS Settings modal |
| prj0000049 | Dependabot Security Fixes | Dependabot CVEs resolved; libp2p bump; 7-test security suite |
| prj0000050 | Install Script | `.\install.ps1` — one-command developer setup (Python, Rust, Node) |
| prj0000051 | README Update | This document — comprehensive rewrite covering all components |

## Future Roadmap

The following ten projects are proposed as the next iteration of PyAgent's growth.
Each maps to a planned workstream that will follow the full 10-agent pipeline.

1. **HMAC Webhook Verification** — Secure GitHub webhook payloads with HMAC-SHA256
   signature validation in `src/github_app.py` (a noted gap since the GitHub import
   project).

2. **Backend Authentication** — Add API-key or JWT authentication to all REST and
   WebSocket endpoints, integrated with the existing security allowlist checker.

3. **WebSocket E2E Encryption** — Wire the documented E2E encryption architecture
   (`docs/E2E_ENCRYPTION.md`) into production WebSocket transport using the Noise_XX
   protocol already available in `rust_core`.

4. **Rust async-transport Activation** — Enable the `async-transport` feature in
   `rust_core` to activate QUIC-over-Tokio for faster, multiplexed inter-agent
   message passing.

5. **Agent Orchestration Graph** — Add a visual directed-acyclic-graph panel to
   NebulaOS showing the live task flow and agent status across all 10 pipeline stages
   in real time.

6. **Mobile-Responsive NebulaOS** — Add CSS responsive breakpoints and touch-friendly
   interaction patterns to the NebulaOS shell so it works on tablets and modern
   mobile browsers.

7. **Plugin Marketplace Browser** — Build an in-NebulaOS application-store panel for
   discovering, installing, and managing third-party agent plugins without restarting
   the dev stack.

8. **FLM Token Throughput Dashboard** — Real-time tokens-per-second charts fed from
   FLM telemetry, surfaced in the NebulaOS Conky dock or a dedicated metrics panel.

9. **Theme System** — Light mode and a retro terminal (green-on-black) theme for
   NebulaOS, with a theme selector in the Settings modal and persisted preference
   storage.

10. **Live Agent Execution in CodeBuilder** — Wire the 10-agent pipeline directly to
    the CodeBuilder UI so tasks run in-browser with streaming per-agent log output
    and progress indicators.

## Development Reference

### Running tests

```powershell
python -m pytest -q                       # full suite (666 tests)
python -m pytest tests/structure/ -v      # structural / doc checks only
python -m pytest tests/security/ -v       # security checks only
python -m pytest tests/ci/ -v             # CI workflow validation only
```

### Code quality

```powershell
ruff check src/                           # lint (max-line-length = 120)
mypy src/ --ignore-missing-imports        # type checking
```

### CI workflows

GitHub Actions workflows live in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|---|---|---|
| `smoke.yml` | push / PR | Fast import smoke test |
| `python-core.yml` | push / PR | pytest with coverage |
| `rust.yml` | push / PR | cargo build + test |
| `docs.yml` | push / PR | Docs structure validation |

### Architecture documentation

| Path | Contents |
|---|---|
| `docs/architecture/ARCHITECTURE.md` | System overview |
| `docs/architecture/adr/` | Architecture Decision Records |
| `docs/agents/` | Per-agent memory and coordination notes |
| `docs/project/prjNNNNNNN/` | Per-project plans, tests, code, and git notes |

## License

Copyright 2026 PyAgent Authors.
Licensed under the [Apache License, Version 2.0](LICENSE).
"""

dest = Path(__file__).parent.parent / "README.md"
dest.write_text(README.lstrip(), encoding="utf-8")
print(f"Written {dest} ({dest.stat().st_size} bytes)")

# 0 — Architecture Overview

This file is the **top-level architecture overview** for PyAgent. It exists to help agents and
contributors quickly understand the high-level system structure and where to look for decisions.

## Core architecture pillars

- **Swarm-based agents**: specialized agents collaborate via a shared runtime and task orchestration.
- **Transactional safety**: all file/system changes use transaction managers
  (`StorageTransaction`, `MemoryTransaction`, `ProcessTransaction`).
- **Rust acceleration**: high-throughput operations live in `rust_core/` and are exposed via PyO3.
- **Async runtime**: the system runs on a Rust/Tokio scheduler; all Python code is expected to be
  async-friendly.

## Primary directory layout

| Path | Purpose |
|---|---|
| `src/` | Python agent orchestration, inference, and core logic |
| `src/core/fuzzing/` | Deterministic local fuzzing core (policy, corpus, mutator, case scheduling) |
| `rust_core/` | High-throughput Rust kernels (diff/patch, metrics, parsing) via PyO3 |
| `backend/` | FastAPI WebSocket + REST backend worker |
| `web/` | Vite/React NebulaOS frontend |
| `data/` | Machine-readable registries (projects.json, agent_registry.json) |
| `docs/` | All human- and agent-readable documentation |
| `.github/agents/` | Agent definitions, memory files, and log files |
| `tests/` | Full test suite (unit, integration, structure, docs) |

## When to update

- When a new architectural pattern is adopted (e.g., new runtime model, new transaction
  semantics, new agent coordination approach).
- When the core directory layout changes in ways that affect how agents locate key components.
- **After each code change:** `@6code` must update the relevant section here if the change
  affects system architecture.

## Where to find more detail

- Agent system: `docs/architecture/1agents.md`
- Agent workflow phases: `docs/architecture/2workflow.md`
- Project portfolio: `docs/architecture/3projects.md`
- Architecture Decision Records: `docs/architecture/adr/`
- Deep-dive archives: `docs/architecture/archive/`

## Recording decisions (ADR)

When making a new architecture decision, create or update an ADR in `docs/architecture/adr/`.
A template is available at `docs/architecture/adr/0001-architecture-decision-record-template.md`.

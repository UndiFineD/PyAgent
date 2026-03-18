# Architecture

This file is the **top-level architecture overview** for PyAgent. It exists to help agents and contributors quickly understand the high-level system structure and where to look for decisions.

## Core architecture pillars
- **Swarm-based agents**: specialized agents collaborate via a shared runtime and task orchestration.
- **Transactional safety**: all file/system changes use transaction managers (`StorageTransaction`, `MemoryTransaction`, `ProcessTransaction`).
- **Rust acceleration**: high-throughput operations live in `rust_core/` and are exposed via PyO3.
- **Async runtime**: the system runs on a Rust/Tokio scheduler; all Python code is expected to be async-friendly.

## When to update
- When a new architectural pattern is adopted (e.g., new runtime model, new transaction semantics, new agent coordination approach).
- When the core directory layout changes in ways that affect how agents locate key components.

## Where to find more detail
- Reference docs (archival deep dives): `docs/architecture/archive/`
- Project-level plans: `docs/project/prjXXX-*`
- Agent-focused snapshot: `docs/architecture/PyAgent.md`

## Recording decisions (ADR)
When making a new architecture decision, create or update an Architecture Decision Record (ADR) in:
- `docs/architecture/adr/`

A template is available at:
- `docs/architecture/adr/0001-architecture-decision-record-template.md`

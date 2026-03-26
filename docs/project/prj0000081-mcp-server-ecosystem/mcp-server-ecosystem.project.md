# mcp-server-ecosystem — Project Overview

_Status: HANDED_OFF_
_Owner: @1project | Updated: 2026-03-26_

## Project Identity
**Project ID:** prj0000081
**Short name:** mcp-server-ecosystem
**Project folder:** `docs/project/prj0000081-mcp-server-ecosystem/`

## Project Overview
The MCP Server Ecosystem project delivers a hot-load registry that enables PyAgent
agents to dynamically connect to 500+ community MCP (Model Context Protocol) servers at
runtime — without restarting the agent process. Each MCP server connection is isolated
inside a security sandbox that restricts filesystem, network, and subprocess access to a
declared capability manifest. Agents invoke MCP-hosted tools through the existing
`src/tools/` dispatch layer, so no agent code changes are required. The registry
exposes list, enable, disable, and introspect operations so operators can manage the
available tool set while the system is running.

MCP is the Anthropic-authored open standard (https://spec.modelcontextprotocol.io/)
that lets AI models interact with external tool providers over a structured JSON-RPC
protocol. The community ecosystem includes hundreds of pre-built MCP servers covering
databases, browsers, code execution, file systems, and third-party APIs.

## Goal & Scope

**Goal:** Build a production-grade hot-load MCP server registry with per-server security
sandboxing, integrated into PyAgent's tool dispatch and observable via a management API.

**In scope:**
- `src/mcp/` — new top-level MCP subsystem package containing:
  - `McpRegistry.py` — hot-load registry: discover, load, reload, unload MCP server definitions
  - `McpSandbox.py` — per-server capability sandbox (filesystem, network, subprocess restrictions)
  - `McpClient.py` — async JSON-RPC 2.0 client over stdio / HTTP transports
  - `McpToolAdapter.py` — adapts MCP ToolDefinition → PyAgent ToolSpec for `tool_registry.py`
  - `McpServerConfig.py` — dataclass for server config (name, command, env, capabilities)
  - `McpHealthMonitor.py` — liveness checks, restart policy, circuit-breaker per server
  - `__init__.py` — module init and public API
- `tests/unit/test_McpRegistry.py` — unit tests for hot-load lifecycle
- `tests/unit/test_McpSandbox.py` — unit tests for sandboxing enforcement
- `tests/unit/test_McpClient.py` — unit tests for JSON-RPC client
- `tests/unit/test_McpToolAdapter.py` — unit tests for tool schema adaptation
- All project documentation stubs in this folder

**Out of scope:**
- Changes to existing agent classes (agents use `tool_registry.py` as-is)
- Building or hosting new MCP servers (registry consumes community servers only)
- GUI management panel (management API only, no UI changes)
- Persistent cross-session MCP state storage (in-memory registry with config-file reload)
- MCP OAuth / token management beyond env-var injection into sandboxed server env

## Branch Plan
**Expected branch:** `prj0000081-mcp-server-ecosystem`
**Scope boundary:** `docs/project/prj0000081-mcp-server-ecosystem/`,
`src/mcp/`, `tests/unit/test_Mcp*.py`, plus `docs/project/kanban.md` and
`data/projects.json` for lifecycle updates.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch is `prj0000081-mcp-server-ecosystem` and the changed files stay inside
the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Scope Boundary Decision: `src/mcp/` not `src/tools/mcp/`

The MCP subsystem is a distinct infrastructure layer, not a single tool plugin. It owns
its own registry lifecycle, protocol transport, sandbox enforcement, and health
monitoring. Placing it at `src/mcp/` (peer of `src/core/`, `src/transport/`,
`src/memory/`) correctly signals first-class subsystem status. The integration point
with `src/tools/` is a thin adapter (`McpToolAdapter.py`) that translates MCP tool
schemas into the existing `ToolSpec` format — `src/tools/` itself remains unchanged.

## Key Components

| File | Purpose |
|---|---|
| `src/mcp/McpRegistry.py` | Hot-load lifecycle: discover servers from config, spawn stdio/HTTP processes, reload without restart |
| `src/mcp/McpSandbox.py` | Per-server capability manifest enforcement; restricts filesystem paths, network hosts, subprocess spawning |
| `src/mcp/McpClient.py` | Async JSON-RPC 2.0 client over stdio and HTTP transports; handles initialize handshake, tool/resource calls |
| `src/mcp/McpToolAdapter.py` | Converts MCP ToolDefinition (JSON Schema input) → PyAgent ToolSpec; registers/deregisters with `tool_registry.py` |
| `src/mcp/McpServerConfig.py` | Pydantic dataclass: name, command, args, env, transport, capabilities, sandbox_policy |
| `src/mcp/McpHealthMonitor.py` | Per-server liveness polling, restart-on-failure with exponential backoff, circuit-breaker |
| `src/mcp/__init__.py` | Exports `McpRegistry`, `McpClient`, `McpSandbox`, `McpToolAdapter`, `McpServerConfig` |

## Architecture Integration

- **Async-first**: all transport I/O uses `asyncio`; server processes are monitored via `asyncio.subprocess`.
- **PascalCase modules**: all filenames follow project convention.
- **Tool dispatch unchanged**: agents call `tool_registry.dispatch()` as before; `McpToolAdapter` injects MCP tools transparently.
- **Transaction safety**: registry mutations go through `StorageTransaction` / `MemoryTransaction` per project convention.
- **Context lineage**: each MCP call opens a `ContextTransaction` to prevent infinite tool-call recursion.
- **Security-by-default**: sandbox denies all filesystem/network access unless explicitly allow-listed in the server's config manifest.

## Acceptance Criteria

1. Registry loads ≥1 MCP server from a YAML/JSON config file at startup and on `reload()`.
2. A sandboxed MCP server that attempts to read an un-allowed filesystem path is blocked (tested).
3. An agent can invoke a tool exposed by an MCP server via the existing `tool_registry.dispatch()` interface.
4. `McpHealthMonitor` detects a crashed server and restarts it within 5 seconds (tested).
5. `registry.list_servers()` returns current status (running / stopped / crashed) for all registered servers.
6. Full unit-test coverage ≥ 90% across all `src/mcp/*.py` modules.
7. `flake8` and `mypy --strict` pass clean on all new modules.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Project setup | @1project | DONE |
| M2 | Options explored | @2think | |
| M3 | Design confirmed | @3design | |
| M4 | Plan finalized | @4plan | |
| M5 | Tests written | @5test | |
| M6 | Code implemented | @6code | |
| M7 | Integration validated | @7exec | |
| M8 | Security clean | @8ql | |
| M9 | Committed | @9git | |

## Agent Memory Links
- `.github/agents/data/1project.memory.md`
- `.github/agents/data/2think.memory.md` (populated on @2think handoff)

## Status
_Last updated: 2026-03-26_
Project folder created on branch `prj0000081-mcp-server-ecosystem`. All 9 stub files
initialised. Handing off to @2think for deep options analysis covering community MCP
registries, PyAgent tool-dispatch integration, security threat model, and at least 3
implementation approaches with trade-offs.

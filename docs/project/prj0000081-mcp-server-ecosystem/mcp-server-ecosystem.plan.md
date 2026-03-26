# mcp-server-ecosystem — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-26_

---

## Overview

Build the `src/mcp/` package: a subprocess + stdio transport MCP client ecosystem that
lets any `BaseAgent` discover and call tools exposed by external MCP servers, with
hot-reload, security-hardened env sandboxing, SHA-256 pinning, and background health
monitoring.

Eight new source files are created (`src/mcp/`), two functions added to an existing
file (`src/tools/tool_registry.py`), one root-level config file added
(`mcp_servers.yml`), and four unit test files produced (`tests/unit/test_Mcp*.py`).

**Key design constraints encoded in this plan:**

- `BaseAgent.run()` is already `async def` — no async migration work required.
- `deregister_tool()` must use copy-on-write dict swap; never `del _REGISTRY[key]`.
- `McpSandbox.spawn()` must never use `shell=True`.
- `_masked_env` must be produced at spawn-time; all log calls use it exclusively.
- `McpToolAdapter` closures must never call `asyncio.run()` internally.
- In-flight drain uses counter + `asyncio.Event` (not `asyncio.Semaphore`).
- `McpClient` must support ≥10 concurrent outstanding JSON-RPC requests (correlation
  by `id`).

---

## Phase 1 — Foundations  (data layer, exceptions, registry extension)

### T01 — Extend `tool_registry.py` with `deregister_tool` + `async_run_tool`

| Field | Value |
|---|---|
| **Files touched** | `src/tools/tool_registry.py` |
| **Depends on** | — (no dependencies) |
| **Complexity** | S |

**Acceptance criteria:**

1. `deregister_tool(name: str) -> None` added: performs `global _REGISTRY; _REGISTRY = {k: v for k,v in _REGISTRY.items() if k != name}`. Raises `KeyError` if `name` not registered.
2. `async_run_tool(name: str, args: list[str] | None = None) -> int` added: awaits coroutine result directly; never calls `asyncio.run()`. Falls back to sync execution for non-async tools.
3. Both new functions exported from module top-level.
4. Existing `run_tool()`, `register_tool()`, `list_tools()`, `get_tool()` unchanged.
5. `ruff check src/tools/tool_registry.py` → 0 errors.
6. `mypy src/tools/tool_registry.py --ignore-missing-imports` → 0 errors.

---

### T02 — Implement `src/mcp/exceptions.py` (13-type hierarchy)

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/exceptions.py` |
| **Depends on** | — (no dependencies) |
| **Complexity** | S |

**Acceptance criteria:**

1. File contains exactly 13 exception classes, all deriving from `McpError(Exception)`:
   `McpConfigError`, `McpServerNotFound`, `McpServerNotEnabled`,
   `McpServerAlreadyEnabled`, `McpServerCrashed`, `McpCallTimeout`,
   `McpProtocolError`, `McpToolError`, `McpPinMismatch`, `McpPathForbidden`,
   `McpSecretNotFound`, `McpToolNameCollision`.
2. Each exception class has the project Apache 2.0 file header and `PascalCase` filename.
3. All 13 names are importable: `from src.mcp.exceptions import McpError, McpConfigError, ...` succeeds.
4. `ruff check src/mcp/exceptions.py` → 0 errors.

---

### T03 — Implement `src/mcp/McpServerConfig.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpServerConfig.py` |
| **Depends on** | T02 (imports `McpConfigError`) |
| **Complexity** | S |

**Acceptance criteria:**

1. `McpServerConfig` is a `@dataclass` with all 13 fields specified in the design:
   `name`, `command`, `env_vars`, `secret_refs`, `allowed_paths`, `allowed_hosts`,
   `timeout_seconds`, `restart_policy`, `sha256_pin`, `transport`, `startup_mode`,
   `enabled`, `heartbeat_interval_seconds`, `max_restart_attempts`.
2. `from_dict(data: dict) -> McpServerConfig` class method: constructs instance from a
   plain dict (as produced by PyYAML). Raises `McpConfigError` for missing required
   fields (`name`, `command`) or invalid `restart_policy` values.
3. All fields have defaults matching the design document (e.g. `transport="stdio"`,
   `startup_mode="eager"`, `enabled=True`, `heartbeat_interval_seconds=30.0`,
   `max_restart_attempts=3`).
4. `ruff check` + `mypy` → 0 errors.

---

### T04 — Create `mcp_servers.yml` (root of repo)

| Field | Value |
|---|---|
| **Files touched** | `mcp_servers.yml` |
| **Depends on** | T03 (config schema must be defined first) |
| **Complexity** | S |

**Acceptance criteria:**

1. File located at `<repo_root>/mcp_servers.yml`.
2. Contains exactly the two server definitions from the design: `filesystem` and
   `github`.
3. `filesystem` entry: `command: ["npx", "-y", "@modelcontextprotocol/server-filesystem",
   "/workspace"]`, `allowed_paths: ["/workspace"]`, all defaults as per design.
4. `github` entry: `command: ["npx", "-y", "@modelcontextprotocol/server-github"]`,
   `env_vars: {GITHUB_API_URL: "https://api.github.com"}`,
   `secret_refs: ["GITHUB_TOKEN"]`, `allowed_hosts: ["api.github.com"]`.
5. YAML is valid (parseable with `pyyaml.safe_load`).
6. `McpServerConfig.from_dict()` successfully parses both entries without raising.

---

### T05 — Implement `src/mcp/__init__.py` (public re-exports)

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/__init__.py` |
| **Depends on** | T02, T03 (and logically after T06–T10, but import block is written now) |
| **Complexity** | S |

**Acceptance criteria:**

1. Exports exactly the symbols listed in the design:
   `McpRegistry`, `McpServerConfig`, `McpClient`, `McpToolDefinition`, `McpToolResult`,
   `McpSandbox`, `McpToolAdapter`, `McpHealthMonitor`, and all 13 exception types.
2. Uses `TYPE_CHECKING` guard or conditional imports so that importing `src.mcp` does
   not crash if a sub-module is not yet written — each import is wrapped in a `try/except
   ImportError` with a `_TODO` stub. **This is an exception to the no-stubs rule:** the
   `__init__.py` itself contains no logic; it only re-exports. The actual modules it
   imports are fully implemented before this task is considered done.
   *(In practice T05 is written alongside T10 completion so all modules exist.)*
3. `from src.mcp import McpRegistry` succeeds when all Phase 1–4 tasks are done.
4. `ruff check src/mcp/__init__.py` → 0 errors.

> **Note:** T05 is committed as part of Phase 4 completion when all sub-modules exist.
> It is defined here so @5test knows the public API surface.

---

## Phase 2 — Core runtime (subprocess sandbox + async JSON-RPC client)

### T06 — Implement `src/mcp/McpSandbox.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpSandbox.py` |
| **Depends on** | T02 (exceptions), T03 (McpServerConfig) |
| **Complexity** | M |

**Acceptance criteria:**

1. `McpSandbox` class implements `spawn()`, `terminate()`, `validate_path()`,
   `build_env()` exactly as specified in the design interfaces.
2. `build_env(config)` is a pure function (no subprocess spawn, no side effects).
   Returns `(env: dict[str, str], masked_env: dict[str, str])` — a 2-tuple so callers
   store both. Masked env replaces every secret value with `"[REDACTED]"`.
3. `spawn()` calls `build_env()` and stores `masked_env` on the instance; all
   subsequent log calls use `masked_env`, never the live env.
4. `spawn()` uses `asyncio.create_subprocess_exec` (never `shell=True`).
   `stdin=asyncio.subprocess.PIPE`, `stdout=asyncio.subprocess.PIPE`,
   `stderr=asyncio.subprocess.PIPE`.
5. SHA-256 pinning: if `config.sha256_pin` is set, compute `hashlib.sha256` of
   `config.command[0]` binary bytes; raise `McpPinMismatch` before spawning if
   mismatch.
6. `terminate()` sends `process.terminate()`, awaits up to 5 s, then calls
   `process.kill()`; always awaits `process.wait()`.
7. `validate_path()` resolves symlinks (`Path.resolve()`); raises `McpPathForbidden`
   if the resolved absolute path does not start with any `allowed_paths` entry
   (also resolved). Empty `allowed_paths` → deny all.
8. `secret_refs` in `config` absent from `os.environ` → raises `McpSecretNotFound`.
9. `ruff check` + `mypy` → 0 errors.

---

### T07 — Implement `src/mcp/McpClient.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpClient.py` |
| **Depends on** | T02 (exceptions), T03 (McpServerConfig) |
| **Complexity** | L |

**Acceptance criteria:**

1. `McpClient` implements `initialize()`, `list_tools()`, `call_tool()`, `ping()`,
   `close()` as specified.
2. JSON-RPC 2.0 wire format: newline-delimited JSON over `process.stdin` /
   `process.stdout`. Each request/response is one line (`\n` terminated).
3. Message correlation: maintains `_pending: dict[int, asyncio.Future]` keyed by
   request `id`. A single background `asyncio.Task` reads lines from stdout and
   resolves futures. Supports ≥10 concurrent outstanding requests.
4. `call_tool()` wraps entire call in `asyncio.wait_for(timeout=config.timeout_seconds)`;
   raises `McpCallTimeout` on expiry.
5. Malformed JSON line → raises `McpProtocolError`.
6. `process.returncode is not None` at call time → raises `McpServerCrashed`.
7. `ping()` never raises; returns `False` on timeout or process exit.
8. `McpToolDefinition` dataclass: `name: str`, `description: str`,
   `input_schema: dict`.
9. `McpToolResult` dataclass: `content: list[dict]`, `is_error: bool = False`.
10. `initialize()` sends method `initialize` with `protocolVersion`, `capabilities`,
    `clientInfo`; awaits `initialized` notification.
11. `close()` closes stdin writer; does not terminate process.
12. `ruff check` + `mypy` → 0 errors.

---

## Phase 3 — Registry + tool adapter

### T08 — Implement `src/mcp/McpRegistry.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpRegistry.py` |
| **Depends on** | T02, T03, T06, T07 |
| **Complexity** | L |

**Acceptance criteria:**

1. `McpRegistry` implements `load_config()`, `enable()`, `disable()`, `reload()`,
   `list_servers()`, `get_client()`, `get_status()` exactly as per design interfaces.
2. `McpServerStatus` enum: `STOPPED | STARTING | RUNNING | DRAINING | RESTARTING`.
3. `load_config(path)` reads YAML via `pyyaml.safe_load`; constructs
   `list[McpServerConfig]` via `McpServerConfig.from_dict()`; raises `McpConfigError`
   on validation failure. Idempotent merge: re-calling does not disable already-running
   servers.
4. `enable(name)` sequence: `McpSandbox.spawn()` → `McpClient.initialize()` →
   `McpToolAdapter.register_server_tools()`. Sets status `STARTING` → `RUNNING`.
5. `disable(name)` drain procedure:
   a. Set status to `DRAINING`.
   b. New tool calls see status `DRAINING` and raise `McpServerNotEnabled` immediately.
   c. Track `_in_flight_count` (int) + `asyncio.Event` that fires at count=0.
   d. Await drain event with `disable_drain_timeout_seconds` (default 10 s) deadline.
   e. After drain (or timeout): call `McpToolAdapter.deregister_server_tools(name)`,
      then `McpSandbox.terminate(process)`.
6. `reload(name)` is `await self.disable(name); await self.enable(name)` guarded by
   a per-server `asyncio.Lock`.
7. `get_client(name)` raises `McpServerNotEnabled` when status ≠ `RUNNING`.
8. `list_servers()` returns a snapshot (copy) of configs; mutation does not affect
   registry.
9. `ruff check` + `mypy` → 0 errors.

---

### T09 — Implement `src/mcp/McpToolAdapter.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpToolAdapter.py` |
| **Depends on** | T01, T02, T03, T07 |
| **Complexity** | M |

**Acceptance criteria:**

1. `McpToolAdapter.__init__(registry_ref: dict)` stores a reference to the passed
   registry dict (default: `tool_registry._REGISTRY`).
2. `register_server_tools(server_name, client, sandbox, config) -> int`:
   - Calls `await client.list_tools()` to fetch `list[McpToolDefinition]`.
   - For each definition: calls `tool_definition_to_spec()` → `(name, main, desc)`.
   - Checks for collision: if `name` already in `tool_registry._REGISTRY` and is NOT
     an MCP tool, raises `McpToolNameCollision`.
   - Calls `register_tool(name, async_main, desc)`.
   - Returns count of tools registered.
3. Each registered `async_main` closure:
   - Increments `McpRegistry._in_flight_count` for the server on entry.
   - Checks server status; raises `McpServerNotEnabled` if `DRAINING` or `STOPPED`.
   - Calls `sandbox.validate_path()` for any argument matching a path parameter.
   - Calls `await client.call_tool(tool_name, arguments)`.
   - Decrements `_in_flight_count` and fires drain event if count reaches 0, always
     (in a `finally` block).
4. `deregister_server_tools(server_name) -> int`:
   - Removes all tools whose name starts with `f"mcp::{server_name}::"` using
     `deregister_tool()` (copy-on-write).
   - Returns count removed.
5. `tool_definition_to_spec(server_name, defn)` is a `@staticmethod` returning
   `(f"mcp::{server_name}::{defn.name}", async_closure, description)`.
6. `ruff check` + `mypy` → 0 errors.

---

## Phase 4 — Health monitor + integration wire-up + tests

### T10 — Implement `src/mcp/McpHealthMonitor.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/McpHealthMonitor.py` |
| **Depends on** | T02, T08 |
| **Complexity** | M |

**Acceptance criteria:**

1. `McpHealthMonitor` implements `start(registry)`, `stop()`, `get_health(server_name)`
   as per design.
2. `McpServerHealth` enum: `HEALTHY | DEGRADED | DOWN`.
3. `start()` launches one `asyncio.Task` per enabled server. Each task:
   - Loops: sleep `config.heartbeat_interval_seconds` (default 30 s) → call
     `client.ping()`.
   - On `ping()` returning `False`: log `WARNING`; call `registry.reload(name)`.
   - Counts consecutive failures; applies `restart_policy`:
     - `"never"` → log `CRITICAL`; leave server disabled; stop polling.
     - `"on-failure"` → exponential backoff, stop after `max_restart_attempts`.
     - `"always"` → exponential backoff, retry indefinitely.
4. `stop()` cancels all background tasks and awaits cancellation.
5. `get_health(name)` is synchronous; returns current `McpServerHealth` from an
   internal dict. Returns `DOWN` for unknown names.
6. `ruff check` + `mypy` → 0 errors.

---

### T11 — Finalise `src/mcp/__init__.py`

| Field | Value |
|---|---|
| **Files touched** | `src/mcp/__init__.py` |
| **Depends on** | T02–T10 (all modules must exist) |
| **Complexity** | S |

**Acceptance criteria:**

1. All symbols from T05 acceptance criteria are importable without error.
2. `python -c "from src.mcp import McpRegistry, McpSandbox, McpClient, McpToolAdapter,
   McpHealthMonitor, McpServerConfig, McpError"` exits 0.
3. `ruff check src/mcp/__init__.py` → 0 errors.

---

### T12 — Write all four test files (33 test cases)

| Field | Value |
|---|---|
| **Files touched** | `tests/unit/test_McpRegistry.py`, `tests/unit/test_McpClient.py`, `tests/unit/test_McpSandbox.py`, `tests/unit/test_McpToolAdapter.py` |
| **Depends on** | T01–T11 (all implementation complete) |
| **Complexity** | L |

**Acceptance criteria:**

1. **`test_McpRegistry.py`** — 9 test cases (all must pass):
   - `test_load_config_valid`, `test_load_config_invalid_schema`,
     `test_enable_starts_subprocess`, `test_enable_already_enabled_raises`,
     `test_disable_drains_before_terminate`, `test_disable_force_kills_after_drain_timeout`,
     `test_reload_calls_disable_then_enable`, `test_get_client_not_enabled_raises`,
     `test_list_servers_returns_snapshot`.
2. **`test_McpClient.py`** — 8 test cases:
   - `test_initialize_sends_correct_request`, `test_list_tools_parses_response`,
     `test_call_tool_roundtrip`, `test_call_tool_timeout_raises`,
     `test_call_tool_crashed_process`, `test_call_tool_malformed_json_raises`,
     `test_ping_returns_false_on_timeout`, `test_concurrent_calls_correlated`.
3. **`test_McpSandbox.py`** — 10 test cases:
   - `test_build_env_only_declared_vars`, `test_build_env_secret_refs_injected`,
     `test_build_env_secret_ref_missing_raises`, `test_build_env_masked_no_secret_values`,
     `test_sha256_pin_valid_passes`, `test_sha256_pin_mismatch_raises`,
     `test_validate_path_within_allowed`, `test_validate_path_outside_allowed_raises`,
     `test_validate_path_symlink_escape_raises`, `test_terminate_kills_after_timeout`.
4. **`test_McpToolAdapter.py`** — 6 test cases:
   - `test_register_server_tools_namespaces_correctly`, `test_registered_tool_callable`,
     `test_deregister_removes_all_server_tools`,
     `test_deregister_does_not_affect_other_servers`,
     `test_tool_name_collision_raises`, `test_copy_on_write_safety`.
5. All tests use pytest; async tests use `@pytest.mark.asyncio`.
6. No test spawns a real subprocess or network call; all use injected fakes /
   `unittest.mock.AsyncMock`.
7. `pytest tests/unit/test_Mcp*.py -v --tb=short` → ≥33 passed, 0 failed.

---

## Task Dependency Graph

```
T01 ──────────────────────────────────────────► T09
T02 ──► T03 ──► T06 ──► T08 ──► T10 ──► T11 ──► T12
         │       │        │                │
         │       └────────┘                │
         └──────────────────► T09 ─────────┘
T03 ──► T04
T07 ──► T08 ──► T09
T01..T10 ── all complete ──► T11 ──► T12
```

Parallelisable: **T01** and **T02** can be worked simultaneously.
**T06** and **T07** can be worked simultaneously after T02+T03.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Foundations | T01, T02, T03, T04 | ☐ |
| M2 | Core runtime | T06, T07 | ☐ |
| M3 | Registry + adapter | T08, T09 | ☐ |
| M4 | Health + wire-up + tests | T10, T11, T12 | ☐ |

---

## Blockers and Notes for @5test and @6code

### B1 — `build_env()` return type change (BLOCKER for @6code)

The design specifies `build_env(config) -> dict[str, str]` but acceptance criteria for
T06 require it returns a 2-tuple `(env, masked_env)`. **@6code must use the 2-tuple
signature.** The design interface is a simplification; the plan is authoritative here.
`spawn()` stores `self._masked_env` from the tuple.

### B2 — In-flight counter placement (BLOCKER for @6code)

`McpRegistry._in_flight_count` is per-server and must live on the registry, not the
sandbox or client. `McpToolAdapter` closures receive a reference to the registry's
per-server counter and event via constructor injection (`register_server_tools` takes
`in_flight_count_ref` and `drain_event_ref` parameters — or the adapter holds a
registry reference). @6code must decide and document the injection pattern before
writing T08/T09.

### B3 — `mcp_servers_test.yml` fixture (@5test and @6code)

Unit tests must NOT require real `npx` commands or `GITHUB_TOKEN` in the environment.
`test_McpRegistry.py` must use a `@pytest.fixture` that creates an in-memory
`McpServerConfig` directly (bypassing YAML). `test_McpSandbox.py` `test_sha256_pin_*`
tests write a temp binary file with known content. No fixture YAML file is needed for
the unit test suite; `mcp_servers.yml` is for integration/manual use only.

### B4 — `McpClient` reader task cancellation on `close()`  

`McpClient.close()` must cancel the background line-reader task and await its
cancellation before closing the stdin writer. If the reader is not cancelled first,
closing stdin may cause a `BrokenPipeError` on the pending read. @6code must handle
`asyncio.CancelledError` in the reader loop without raising.

### B5 — `McpRegistry.reload()` lock scope  

The per-server `asyncio.Lock` in `reload()` must also guard concurrent `enable()` and
`disable()` calls on the same server name to prevent TOCTOU races (e.g. two concurrent
`enable()` calls both see status=STOPPED and both attempt to spawn). @6code should use
a single `_server_lock: dict[str, asyncio.Lock]` keyed by server name.

### B6 — `tests/structure/` regression gate  

The existing structure tests at `tests/structure/` count source files and validate
directory layout. Adding `src/mcp/` will be picked up by those tests. @5test must run
`pytest tests/structure/ -q` before and after the sprint and verify the count still
reflects the new files correctly (the tests may need a whitelist update, not a count
fix — verify which).

### B7 — `BaseAgent.run()` async migration  

`BaseAgent.run()` is already declared `async def` in `src/agents/BaseAgent.py` and
`CortAgent` already implements `async def run()`. No async migration is needed. The
only known agent subclass is `CortAgent` — it is already async-compatible.

---

## Open Question Resolutions

| # | Question | Resolution |
|---|---|---|
| OQ1 | `BaseAgent` async migration scope | No work needed: `BaseAgent.run()` is already `async def`; `CortAgent` already implements it async. |
| OQ2 | `mcp_servers.yml` at test time | Unit tests use in-memory `McpServerConfig` fixtures; no YAML file needed in test suite. See B3. |
| OQ3 | Management REST API scope | Deferred. No `backend/app.py` glue in this sprint. |

---

## Validation Commands

```powershell
# Activate venv first
& .venv\Scripts\Activate.ps1

# Lint
& .venv\Scripts\python.exe -m ruff check src/mcp/ src/tools/tool_registry.py tests/unit/test_Mcp*.py

# Type check
& .venv\Scripts\python.exe -m mypy src/mcp/ --ignore-missing-imports

# Unit tests (MCP only)
& .venv\Scripts\python.exe -m pytest tests/unit/test_Mcp*.py -v --tb=short

# Structure regression gate (must still pass)
& .venv\Scripts\python.exe -m pytest tests/structure/ -q
```

---

## Project-level Acceptance Criteria

| # | Criterion | Verifiable by |
|---|---|---|
| AC1 | All `tests/unit/test_Mcp*.py` pass (≥33 test cases, 0 failures) | `pytest tests/unit/test_Mcp*.py` |
| AC2 | `ruff check src/mcp/ src/tools/tool_registry.py` → 0 errors | ruff |
| AC3 | `tests/structure/` → still passing (no regressions) | `pytest tests/structure/ -q` |
| AC4 | `McpRegistry` can load a config, enable a mock server, list tools via `McpClient`, and have those tools appear in `tool_registry` under `mcp::*` namespace | Integration smoke test in `test_McpRegistry.py` |
| AC5 | `McpSandbox._masked_env` replaces all `secret_refs` values with `"[REDACTED]"` | `test_McpSandbox.py::test_build_env_masked_no_secret_values` |
| AC6 | Hot-reload (`McpRegistry.reload()`) completes without permanently losing tool registrations | `test_McpRegistry.py::test_reload_calls_disable_then_enable` |

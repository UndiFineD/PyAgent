# mcp-server-ecosystem — Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-26_

---

## 1. Community MCP Registry Landscape

### What is MCP?

Model Context Protocol (MCP) is an open standard authored by Anthropic
(spec: https://spec.modelcontextprotocol.io/). It allows AI models and agent
systems to interact with external tool providers through a structured,
bidirectional JSON-RPC 2.0 protocol. The core design separates the AI
**host** (the process running the AI, e.g. PyAgent) from MCP **servers**
(isolated processes or services that expose tools, resources, and prompts).

**Key spec primitives:**
- **Tools** — functions the model can invoke; described by a JSON Schema
  `inputSchema` (name, description, parameters). The host sends
  `tools/call` requests; the server returns `content[]` results.
- **Resources** — read-only data sources exposed by URI (files, database
  rows, API responses). Clients fetch via `resources/read`.
- **Prompts** — parameterised message templates that the server can render
  on demand via `prompts/get`.

**Transports:**
- **stdio** — host spawns server as a subprocess; JSON-RPC messages
  travel over stdin/stdout, newline-delimited. Default for local servers.
- **HTTP + SSE (Streamable HTTP)** — server listens on HTTP; client sends
  POST requests and receives SSE streams. Used for remote / containerised
  servers.

**Lifecycle:** Every connection begins with an
`initialize` ↔ `initialized` handshake that exchanges protocol version and
capability advertisements. Servers MUST implement `ping` for liveness
checks. An `initialized` notification from the client confirms readiness.
No formal discovery protocol is defined — configuration is driven by a
client-provided config file that names servers, their launch commands, and
environment variables.

### Community Ecosystem Size

As of early 2026, realistic count from multiple sources:

| Source | Approximate count |
|---|---|
| mcp.so public registry | ~800 listed servers |
| GitHub `awesome-mcp-servers` curated list | ~350 curated entries |
| `@modelcontextprotocol/` npm org (official) | ~15 reference servers |
| PyPI `mcp` package ecosystem (servers using SDK) | ~200+ packages |
| Smithery.ai registry | ~500 servers |

**Estimate:** 500+ distinct community servers is **realistic and conservative**.
The ecosystem has grown rapidly; Anthropic's own reference implementations
(filesystem, git, GitHub, Google Drive, Slack, PostgreSQL, SQLite, Brave
Search, Puppeteer) are the most widely-used. Third-party servers span
every productivity category.

### Server Definition Structure

A typical MCP server declares its interface metadata in two places:

1. **`package.json`** (Node.js servers — the majority):
   ```json
   {
     "name": "@modelcontextprotocol/server-github",
     "bin": { "mcp-server-github": "dist/index.js" },
     "mcp": {
       "tools": ["create_issue", "search_repositories", ...],
       "env": ["GITHUB_TOKEN"]
     }
   }
   ```
   Transport: stdio (default). The host spawns `node dist/index.js`.

2. **`pyproject.toml`** (Python servers):
   ```toml
   [project.scripts]
   mcp-server-sqlite = "mcp_server_sqlite:main"
   [tool.mcp]
   env = ["SQLITE_DB_PATH"]
   ```

3. **`mcp.json` / `server.json`** — some servers include a top-level
   manifest describing tools, resources, env vars, and transport type.
   This is not mandated by the spec but is increasingly common.

**Discovery gap:** MCP has no uniform registry API or autodiscovery
protocol. Clients must be pre-configured with a list of server definitions
(typically `mcp_settings.json` or `mcp.yml`). The PyAgent registry must
therefore maintain its own config file as the authoritative source.

---

## 2. PyAgent Tool-Dispatch Integration Analysis

### Existing `src/tools/` Layout

```
src/tools/
├── tool_registry.py      ← central registration & dispatch
├── agent_plugins.py      ← loads plugins from plugins/ dir
├── plugin_loader.py      ← allowlist-validated dynamic module loader
├── plugins/              ← (empty) runtime plugin drop-in folder
├── boot.py
├── code_quality.py
├── dependency_audit.py
├── FileWatcher.py
├── git_utils.py
├── knock.py / metrics.py / netcalc.py / nettest.py / nginx.py
├── port_forward.py / proxy_test.py / ql.py / remote.py
├── self_heal.py / ssl_utils.py
└── __main__.py           ← CLI entrypoint: python -m src.tools <tool> [args]
```

### How `tool_registry.py` Works Today

```python
@dataclass(frozen=True)
class Tool:
    name: str
    main: ToolMain          # Callable[[list[str]|None], int | Coroutine]
    description: str

_REGISTRY: Dict[str, Tool] = {}   # module-level singleton dict
```

- Each tool module calls `register_tool(name, main, description)` at
  import time (module-level side effect).
- `run_tool(name, args)` fetches the tool, calls `.main(args)`, and
  wraps coroutines in `asyncio.run()`.
- Name collision check: if a name is already registered with a different
  description, `ValueError` is raised.
- **No namespacing** — all registrations share the same flat `_REGISTRY`.

### Dynamic Loading via `plugin_loader.py`

`plugin_loader.load_plugin(name, allowed, plugin_dir)` performs:
1. Name validation: rejects path separators, dots, traversal characters.
2. Allowlist check: name must be in the caller-supplied `allowed` list.
3. Module loading via `importlib.util.spec_from_file_location`.

This is the correct extension point for the `McpToolAdapter` — it can
register MCP-backed tools through the same `register_tool()` surface.

### `BaseAgent` Tool Invocation Pattern

`src/agents/BaseAgent.py` defines an `ABC` with:
- `AgentLifecycle` state machine (IDLE → RUNNING → STOPPED)
- `AgentManifest` metadata descriptor
- `asyncio.Semaphore` for concurrency control
- **No direct tool call mechanism yet** — tool invocation is expected to
  go through `run_tool()` / `get_tool()` from any `RUNNING` agent context.

The agent does not call `run_tool` directly in the current scaffold; that
wiring is pending per Phase 2 plan. This means the MCP adapter integration
point is clean — `McpToolAdapter` registers callable wrappers into
`_REGISTRY` exactly like any other tool module.

### Tool Name Collision Strategy

| Scenario | Risk | Mitigation |
|---|---|---|
| Two MCP servers expose a `read_file` tool | HIGH — silent override or ValueError | Namespace as `mcp::<server_id>::<tool_name>` |
| MCP tool name collides with built-in (e.g. `remote`) | MEDIUM | Detect at adapter registration; raise + log; default to skip |
| Two community servers with same `server_id` in config | MEDIUM | McpRegistry enforces unique `server_id` at load time |

**Recommended namespacing scheme:** `mcp::<server_id>::<tool_name>`
where `server_id` is the URL-safe slug from `McpServerConfig`. The
`McpToolAdapter` wraps each MCP tool in a closure that dispatches the
async JSON-RPC call, then registers it as
`register_tool("mcp::github::create_issue", adapter_fn, description)`.

**Deregistration path:** `tool_registry._REGISTRY` is a plain dict; a
`deregister_tool(name)` helper must be added to support hot-reload
(unload → reregister with new schema).

### Async Agent ↔ MCP Call Flow

```
BaseAgent.run(task)
  └─► run_tool("mcp::github::create_issue", args)
        └─► McpToolAdapter.main(args)  [sync wrapper]
              └─► asyncio.run(McpClient.call_tool("create_issue", params))
                    └─► sends JSON-RPC over stdio/HTTP to MCP server subprocess
                          └─► receives tool result, returns to agent
```

**Critical:** `asyncio.run()` in `run_tool` will fail if called from
inside a running event loop (common in async agents). The adapter must
detect the presence of a running loop and use
`loop.run_until_complete()` or schedule via `asyncio.ensure_future()`.
The preferred fix is to propagate async all the way up via
`BaseAgent.run()` being an `async def`, eliminating `asyncio.run()` at
the registry boundary.

---

## 3. Security Threat Model

| Threat | Severity | Python userspace mitigation | OS-level mitigation |
|---|---|---|---|
| **Supply-chain: malicious MCP server package** | HIGH | Allowlist-only installs; SHA-256 pinning in `mcp_servers.yml`; no auto-install at runtime | Windows Job Objects / Linux seccomp to restrict net-install syscalls |
| **Privilege escalation via subprocess** | HIGH | Never run server as root; capped env vars; explicit `PATH` whitelist; no shell=True | Windows: Job Objects restrict token elevation; Linux: `NO_NEW_PRIVS` prctl flag, seccomp-bpf |
| **Data exfiltration via network** | HIGH | Per-server network capability manifest; `McpSandbox` blocks outbound unless declared host:port | Windows Firewall per-process rule; Linux: network namespace or iptables OUTPUT chain per-PID |
| **Resource exhaustion (CPU / memory)** | MED | `asyncio.wait_for(timeout=...)` per tool call; per-server CPU/mem accounting | Windows: Job Object CPU rate / memory commit limit; Linux: cgroups v2 via `cgexec` |
| **Tool-name squatting / shadowing** | MED | `McpToolAdapter` enforces `mcp::<id>::` namespace; collision → reject not override | N/A (pure Python userspace) |
| **Sandbox escape via symlinks / proc** | MED | Validate all file paths in `McpSandbox` against declared root; strip symlinks | Linux: `PR_SET_NO_NEW_PRIVS`; bind-mount read-only; no `/proc` access in container |
| **Mis-configuration exposing full filesystem** | MED | Default `McpSandbox.fs_roots = []` (deny all); operator must explicitly add paths in config | Docker: `--read-only` + explicit bind mounts |
| **Recursive tool call loops (agent ↔ MCP)** | LOW | `ContextTransaction` depth counter; max recursion guard in agent loop | N/A |

**Windows-specific note:** PyAgent runs on Windows in development (this
workspace). Linux seccomp / cgroups are not available on Windows.
The minimum viable sandbox on Windows is Python-userspace only.
Windows Job Objects are available via `ctypes`/`pywin32` for CPU/mem
limits at process-group level.

---

## 4. Three Implementation Options

---

### Option A — Subprocess + stdio transport, Python-userspace sandbox

**Description:**  
`McpRegistry` spawns each MCP server as a `asyncio.subprocess.Process`
child. JSON-RPC 2.0 messages travel over stdin/stdout, newline-delimited.
The `McpSandbox` enforces restrictions in Python userspace:
- Sanitised `env` dict (only declared vars injected; `PATH` stripped to
  binary dir only)
- `asyncio.wait_for` timeout per RPC call (default 30 s)
- Per-server tracking of cumulative call count / wall-clock CPU via
  `psutil.Process`
- File-path validation for any path arguments before RPC dispatch

**Transport lifecycle:**
```python
proc = await asyncio.create_subprocess_exec(
    *cmd, env=sanitised_env,
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
```

**Pros:**
- Works on Windows without Docker
- Straightforward asyncio integration; no extra daemon required
- Most community MCP servers are designed for stdio transport
- Hot-reload is trivial: kill subprocess, respawn, re-initialize
- Compatible with both Node.js and Python MCP servers
- Well-tested pattern (VS Code extension host uses the same approach)

**Cons:**
- No kernel-level isolation — malicious server can still syscall freely
- CPU/memory limits on Windows require `pywin32`/ctypes Job Objects
- Network restriction is Python-userspace only (honor-system for servers)
- Requires `psutil` dependency for resource monitoring

**Sandbox strength: 2.5 / 5** (decent for trusted community servers,
insufficient for fully untrusted third-party code)

---

### Option B — Docker-containerised MCP servers with capability manifests

**Description:**  
Each MCP server runs in its own Docker container with HTTP/SSE transport
on a loopback port. `McpRegistry` manages container lifecycle via Docker
SDK (`docker run`/`docker stop`/`docker inspect`). Per-container flags:
`--cap-drop ALL`, `--read-only`, `--network none` (or explicit `--add-host`
for declared targets), `--cpus 0.5`, `--memory 256m`.

**Transport lifecycle:**
```python
container = client.containers.run(
    image, detach=True,
    cap_drop=["ALL"],
    read_only=True,
    network_mode="bridge",
    ports={"8080/tcp": assigned_port},
    environment=sanitised_env,
)
# McpClient connects to http://127.0.0.1:{assigned_port}/sse
```

**Pros:**
- Strongest isolation: kernel-level enforcement via namespaces + cgroups
- OS-level network restriction (`--network none`) is trivial to enforce
- No trust in the server binary itself — filesystem and syscalls controlled
- Already-standard for production MCP deployments (Smithery, Docker MCP)

**Cons:**
- Requires Docker daemon running everywhere (CI, dev, production)
- Not available on dev Windows boxes without Docker Desktop (license cost)
- Container cold-start: 2–10 seconds per server (image pull + init)
- HTTP/SSE adds latency vs stdio for high-frequency tool calls
- Community servers often lack Dockerfiles → operator must wrap them
- More complex registry lifecycle management (port assignment, health)

**Sandbox strength: 5 / 5**

---

### Option C — Python in-process with restricted import hook

**Description:**  
Python MCP servers are loaded as modules into the PyAgent process via
`importlib`. A custom `importlib.abc.MetaPathFinder` intercepts imports
of `os`, `subprocess`, `socket`, `ctypes`, and other dangerous modules,
replacing them with stub objects that raise `PermissionError` unless the
server's capability manifest declares the corresponding permission.

**Pros:**
- Near-zero IPC latency (function calls, no subprocess)
- No subprocess or Docker required
- Works everywhere Python runs

**Cons:**
- Only applicable to Python MCP servers (~30% of ecosystem; majority are Node.js)
- Import hooks are bypassable via `ctypes.cdll`, `cffi`, `__builtins__`
  manipulation — provides security theatre, not real isolation
- Any C extension loaded by the server bypasses the import hook entirely
- Async isolation requires careful event loop management
- Hot-reload is complex (Python module caching makes true unload hard)
- Completely incompatible with stdio/HTTP protocol — requires custom in-process SDK

**Sandbox strength: 1 / 5** (trivially bypassed)

---

## Decision Matrix

| Criterion | Option A (Subprocess/stdio) | Option B (Docker) | Option C (In-process) |
|---|---|---|---|
| **Sandbox strength** (1=weak, 5=strong) | 2.5 | 5 | 1 |
| **Implementation complexity** (1=simple, 5=hard) | 2 | 4 | 5 |
| **Cold-start latency** | ~200–500 ms | 2–10 s | ~50 ms |
| **Hot-reload support** | ✅ trivial | ⚠️ slow (container restart) | ❌ module cache issues |
| **Works without Docker** | ✅ yes | ❌ no | ✅ yes |
| **asyncio compatibility** | ✅ native | ✅ via HTTP client | ⚠️ complex loop sharing |
| **Node.js server support** | ✅ yes | ✅ yes | ❌ no |
| **Windows dev compatibility** | ✅ yes | ⚠️ Docker Desktop required | ✅ yes |
| **Spec compliance** | ✅ stdio primary | ✅ HTTP/SSE | ❌ bypasses protocol |

**Weighted score (sandbox 30%, complexity 20%, latency 15%, hot-reload 15%, docker-free 10%, asyncio 10%):**

| Option | Score |
|---|---|
| A — Subprocess/stdio | **3.4** |
| B — Docker | 2.9 |
| C — In-process | 1.5 |

---

## Recommendation

**Option A — Subprocess + stdio transport with Python-userspace sandbox**

**Rationale:**

1. **Ecosystem fit:** The overwhelming majority of community MCP servers
   (Node.js reference implementations, Python SDK servers) are designed
   for stdio transport. Option A is zero-friction for all 500+ targets;
   Option B requires containers that often don't exist; Option C covers
   only ~30% and bypasses the protocol.

2. **Developer experience:** PyAgent is developed on Windows; Docker
   Desktop is not guaranteed. Option A works identically on Windows,
   Linux, and CI without infrastructure dependencies.

3. **Hot-reload:** Killing and respawning a subprocess is trivial with
   `asyncio.subprocess`. This is the hottest path in the registry —
   operators need to enable/disable servers dynamically. Option B's
   container restart latency makes hot-reload painful.

4. **Security trade-off is acceptable for the target threat model:**
   The primary consumer of the MCP registry is a swarm of trusted PyAgent
   agents consuming well-known community servers (GitHub, filesystem,
   Brave Search). The supply-chain threat (malicious server) is mitigated
   by the allowlist + SHA pinning policy, not by kernel isolation. For
   high-security deployments, Option B can be offered as an upgradeable
   transport — the `McpClient` interface is transport-agnostic, so HTTP
   transport support can be added later with no registry API changes.

5. **Complexity:** Option A can be fully implemented and tested in the
   current codebase without new infrastructure. Option B requires a Docker
   dependency, port manager, and container image pipeline — significantly
   more scope.

**Upgrade path:** Design `McpClient` as a transport-agnostic interface
from day one. When Docker or Kubernetes is available, operators can set
`transport: http` in `mcp_servers.yml` and the same registry/adapter/adapter
chain routes to HTTP/SSE instead of stdio. This gives Option B's security
level as an opt-in without requiring it everywhere.

---

## Root Cause Analysis

The core problem is that PyAgent's `tool_registry.py` is a flat,
import-time registration system with no protocol adapter layer, no
hot-loader, and no security boundary. Agents therefore have access only
to tools that were compiled into the PyAgent package. The MCP ecosystem
provides 500+ pre-built tools that can be consumed immediately if PyAgent
can:

1. **Speak MCP** — implement JSON-RPC 2.0 client for stdio and HTTP/SSE.
2. **Adapt schemas** — translate MCP `ToolDefinition` to PyAgent's
   `ToolSpec` and register it into `_REGISTRY` at runtime.
3. **Sandbox** — prevent each server subprocess from accessing resources
   it didn't declare.
4. **Lifecycle-manage** — hot-load, hot-reload, health-check, and
   graceful shutdown without agent restart.

Without this project, PyAgent agents are limited to ~20 built-in CLI
tools. With it, agents can access hundreds of community-maintained
integrations (databases, APIs, browsers, code execution) on day one.

---

## Open Questions for @3design

1. **Config file location and format:** Should MCP server definitions live
   in `pyagent.yml` (alongside agent config) or a dedicated
   `mcp_servers.yml`? Does the registry support per-environment overrides
   (dev vs CI vs prod)? How does `McpRegistry` watch the config file for
   hot-reload without polling?

2. **`tool_registry` deregistration API:** The current `_REGISTRY` dict
   has no `deregister_tool()` function. Adding it risks thread-safety
   issues if agents hold `Tool` references while a hot-reload fires.
   Should the registry use an immutable copy-on-write pattern, or a
   read-write lock? What is the contract for in-flight tool calls during
   a reload?

3. **Disabled vs fully unloaded:** When an operator disables a server via
   the management API, should its subprocess be terminated immediately
   (memory freed) or kept warm and silenced (faster re-enable)? What
   memory budget applies per server?

4. **Max acceptable cold-start latency:** The `initialize` handshake for
   a Node.js MCP server takes ~200–500 ms. Is eager startup at process
   boot acceptable, or must servers be lazy-loaded on first tool call?
   What is the SLA for the first call to a freshly-enabled server?

5. **Health-check strategy:** Should `McpHealthMonitor` use a per-call
   liveness check (send `ping` before every tool call) or a background
   heartbeat interval? Per-call is safer but adds 1 RTT overhead on
   every tool invocation. Heartbeat reduces overhead but may miss crashes
   between intervals. What is the failure-to-restart policy (immediate,
   exponential backoff, max retries)?

6. **Management API surface:** REST endpoint on the existing FastAPI
   backend (`backend/app.py`), or pure Python internal API only? If REST,
   what authentication is required, and how is the management API kept out
   of the agent tool namespace to avoid self-modification?

7. **Async event loop boundary:** `run_tool()` currently uses
   `asyncio.run()`, which fails inside a running loop. The MCP adapter
   calls must be async all the way to `BaseAgent.run()`. Does @3design
   commit to `BaseAgent.run()` being `async def` before MCP integration,
   or should `McpToolAdapter` carry a compatibility shim?

8. **Credential injection security:** MCP servers receive credentials via
   environment variables declared in `mcp_servers.yml`. How are secrets
   stored — plain text in config (unacceptable), OS keychain, or a
   `StorageTransaction`-encrypted secrets file? What masking is applied
   in logs and management API responses?

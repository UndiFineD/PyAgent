# mcp-server-ecosystem — Quality & Security Review

_Agent: @8ql | Date: 2026-03-26 | Branch: prj0000081-mcp-server-ecosystem_
_Status: DONE_

## Scope
| File | Change type |
|------|-------------|
| src/mcp/McpSandbox.py | Created |
| src/mcp/McpClient.py | Created |
| src/mcp/McpRegistry.py | Created |
| src/mcp/McpServerConfig.py | Created |
| src/mcp/McpToolAdapter.py | Created |
| src/mcp/exceptions.py | Created |
| src/mcp/__init__.py | Created |
| src/tools/tool_registry.py | Modified (added deregister_tool, async_run_tool) |
| mcp_servers.yml | Created |

## Part A — Security Findings

### A01 — Subprocess Injection (OWASP A03) — McpSandbox.py
- `config.command` passed as `*config.command` list to `asyncio.create_subprocess_exec` (no shell=True). **PASS ✅**
- `build_env()` starts from empty `{"PATH": binary_dir}` dict — never copies `os.environ`. **PASS ✅**
- Secret values are read from `os.environ` and masked as `"[REDACTED]"` in `masked_env` before any log use. **PASS ✅**
- SHA-256 pin verified via `hashlib.sha256` **before** `create_subprocess_exec` is called. **PASS ✅**
- `validate_path()` resolves symlinks via `Path.resolve()` before prefix check — immune to `../` traversal. **PASS ✅**

### A02 — Client Input Validation (OWASP A03) — McpClient.py
- `json.JSONDecodeError` caught in `_read_loop`; malformed lines discarded without crash. **PASS ✅**
- Response IDs retrieved via `msg.get("id")` then used as dict key; no type injection possible. **PASS ✅**
- `_response_cache` is bounded in practice (populated only during narrow future-registration race window; entries consumed by `_rpc_call`). **LOW risk — documented only.**

### A03 — Registry Lifecycle (OWASP A04) — McpRegistry.py
- `enable()` and `disable()` acquire `self._lock` (asyncio.Lock) for status transitions. **PASS ✅**
- `enable()` raises `McpServerAlreadyEnabled` for duplicate calls. **PASS ✅**
- `reload()` is sequential (`disable` then `enable`) — safe under single-coroutine model. **PASS ✅**
- Registry growth bounded by config entries; `load_config()` overwrites on same name. **PASS ✅**

### A04 — Secret Leakage (mcp_servers.yml)
- Both entries have `enabled: false`. **PASS ✅**
- No secret values stored; `secret_refs: []` (name-only references). **PASS ✅**

### A05 — tool_registry.py new functions
- `deregister_tool` uses copy-on-write dict swap — safe under concurrent reads. **PASS ✅**
- `async_run_tool` raises `KeyError` on missing tool name. **PASS ✅**

| ID | Severity | File | Line | Rule | Description | Status |
|----|----------|------|------|------|-------------|--------|
| QL-01 | HIGH | src/mcp/McpClient.py | 124 | ARCH-001 | `asyncio.get_event_loop().create_future()` in `initialize()` — deprecated in Python 3.10+; inconsistent with `_rpc_call()` which correctly uses `get_running_loop()` | **FIXED** — replaced with `asyncio.get_running_loop().create_future()` |
| QL-02 | LOW | src/mcp/McpClient.py | — | INFO | `_response_cache` could grow unbounded under adversarial server flooding random IDs (DoS vector). Bounded in normal operation. | **DOCUMENTED** |

## Part B — Quality Gaps
| # | Type | Description | Responsible agent | Blocking? |
|---|------|-------------|-------------------|-----------|
| QG-01 | Info | `mcp_servers.yml` `allowed_hosts` is declared in config but not enforced at subprocess network level (future enforcement in health monitor). | @6code (T-future) | No |

## Part C — Lessons Written
| Pattern | Agent memory file | Recurrence | Promoted to agent rule? |
|---------|------------------|-----------|------------------------|
| `asyncio.get_event_loop()` in async methods | .github/agents/data/6code.memory.md | 1 | No (threshold not yet reached) |

## Part D — Ruff S-Rules
```
ruff check --select S src/mcp/ src/tools/tool_registry.py
→ All checks passed!
```
**Result: CLEAN ✅**

## Part E — Architecture Compliance
| Check | Result |
|-------|--------|
| McpSandbox does NOT inherit from any core agent class | ✅ PASS |
| McpClient uses `asyncio.get_running_loop()` (not `get_event_loop()`) | ✅ PASS (fixed) |
| PascalCase filenames throughout src/mcp/ | ✅ PASS |
| No `print()` calls in src/mcp/ | ✅ PASS |

## OWASP Coverage
| Category | Status | Notes |
|----------|--------|-------|
| A01 Access Control | PASS | Registry guards via lock + status enum |
| A02 Cryptographic Failures | PASS | SHA-256 binary pinning implemented |
| A03 Injection | PASS | Subprocess uses exec (list), not shell; path resolved before allowlist check |
| A04 Insecure Design | PASS (post-fix) | `get_event_loop` deprecation resolved |
| A05 Security Misconfiguration | PASS | All servers `enabled: false` by default |
| A06 Vulnerable Components | PASS | pip-audit baseline unchanged; no new findings |
| A07 Auth Failures | N/A | Module does not handle auth |
| A08 Software Integrity | PASS | SHA-256 pin support for binary verification |
| A09 Security Logging | PASS | Secret masking via `masked_env` before any log output |
| A10 SSRF | PARTIAL | `allowed_hosts` declared in config; network-level enforcement deferred to health monitor |

## Tests
- All 33 unit tests in `tests/unit/test_Mcp*.py` pass after fix. ✅

## Verdict
| Gate | Status |
|------|--------|
| Security — ruff S-rules | ✅ PASS |
| Security — pip-audit new findings | ✅ PASS (0 new) |
| Security — Workflow injection | ✅ PASS (no workflow files changed) |
| Security — HIGH/CRITICAL findings | ✅ PASS (QL-01 fixed before handoff) |
| Plan vs delivery | ✅ PASS |
| AC vs test coverage | ✅ PASS (33/33 tests passing, 89.4% coverage) |
| Docs vs implementation | ✅ PASS |
| Architecture compliance | ✅ PASS (post-fix) |
| **Overall** | **✅ CLEAR → @9git** |

# mcp-server-ecosystem — Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-26_

## Test Plan

Scope: Four unit test modules covering `McpRegistry`, `McpClient`, `McpSandbox`, and
`McpToolAdapter`. All 33 tests use in-memory fixtures and `unittest.mock` stubs —
no real subprocess, no real YAML file, no network.

Framework: `pytest` + `pytest-asyncio` (strict mode). Async tests decorated with
`@pytest.mark.asyncio`.

Red-phase strategy: Tests import directly from `src.mcp.*`. At collection time all
four modules fail with `ModuleNotFoundError` — that is the expected red-phase
outcome. Once `@6code` creates `src/mcp/`, all tests must pass without modification.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-REG-01 | load_config populates servers | tests/unit/test_McpRegistry.py | RED |
| TC-REG-02 | enable calls sandbox spawn + client initialize | tests/unit/test_McpRegistry.py | RED |
| TC-REG-03 | disable drains in-flight before terminate | tests/unit/test_McpRegistry.py | RED |
| TC-REG-04 | reload cycles disable then enable in order | tests/unit/test_McpRegistry.py | RED |
| TC-REG-05 | get_client raises McpServerNotEnabled | tests/unit/test_McpRegistry.py | RED |
| TC-REG-06 | enable twice is idempotent | tests/unit/test_McpRegistry.py | RED |
| TC-REG-07 | list_servers returns immutable snapshot | tests/unit/test_McpRegistry.py | RED |
| TC-REG-08 | concurrent enable+disable is safe | tests/unit/test_McpRegistry.py | RED |
| TC-REG-09 | reload unknown server raises McpServerNotFound | tests/unit/test_McpRegistry.py | RED |
| TC-CLI-01 | initialize sends initialize JSON-RPC request | tests/unit/test_McpClient.py | RED |
| TC-CLI-02 | initialize parses capabilities response | tests/unit/test_McpClient.py | RED |
| TC-CLI-03 | list_tools returns 2 McpToolDefinition objects | tests/unit/test_McpClient.py | RED |
| TC-CLI-04 | call_tool round-trip returns correct content | tests/unit/test_McpClient.py | RED |
| TC-CLI-05 | call_tool timeout raises McpCallTimeout | tests/unit/test_McpClient.py | RED |
| TC-CLI-06 | call_tool protocol error raises McpProtocolError | tests/unit/test_McpClient.py | RED |
| TC-CLI-07 | close cancels reader task before stdin close | tests/unit/test_McpClient.py | RED |
| TC-CLI-08 | correlation id matches response | tests/unit/test_McpClient.py | RED |
| TC-SBX-01 | build_env inherits allowed vars (PATH, LANG) | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-02 | build_env strips disallowed vars (HOME, AWS_*) | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-03 | masked_env replaces secrets with [REDACTED] | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-04 | validate_path allows declared paths | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-05 | validate_path blocks undeclared paths | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-06 | validate_path blocks symlink escape | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-07 | spawn uses sanitised env not os.environ | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-08 | terminate sends SIGTERM then SIGKILL | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-09 | spawn raises McpSandboxError on missing command | tests/unit/test_McpSandbox.py | RED |
| TC-SBX-10 | sha256 pin mismatch raises McpPinMismatch | tests/unit/test_McpSandbox.py | RED |
| TC-ADP-01 | register adds namespaced mcp::fs::* tools | tests/unit/test_McpToolAdapter.py | RED |
| TC-ADP-02 | deregister removes only that server's tools | tests/unit/test_McpToolAdapter.py | RED |
| TC-ADP-03 | tool_schema_conversion maps MCP types | tests/unit/test_McpToolAdapter.py | RED |
| TC-ADP-04 | async_run_tool dispatches to McpClient.call_tool | tests/unit/test_McpToolAdapter.py | RED |
| TC-ADP-05 | name collision raises McpToolNameCollision | tests/unit/test_McpToolAdapter.py | RED |
| TC-ADP-06 | deregister nonexistent server is noop | tests/unit/test_McpToolAdapter.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| ALL | RED ✓ | `ModuleNotFoundError: No module named 'src.mcp'` — 4/4 modules, 0 collected, 4 collection errors |

## Unresolved Failures
All 33 tests fail at collection with `ModuleNotFoundError: No module named 'src.mcp'`.
This is the intended red-phase state — correct failure reason confirmed.
Lint: `ruff check` → 0 errors across all four test files.
Next step: hand off to `@6code` to implement `src/mcp/`.

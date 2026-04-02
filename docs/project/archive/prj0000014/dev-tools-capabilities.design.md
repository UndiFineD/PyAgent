# dev-tools-capabilities — Design

_Status: COMPLETE_
_Designer: @3design | Updated: 2026-03-22_

## Module Interfaces

### `git_utils.py`
```python
def create_feature_branch(name: str, base: str = "main") -> bool: ...
def changed_files(base: str = "main") -> list[str]: ...
def update_changelog(entry: str, changelog_path: str = "CHANGELOG.md") -> None: ...
def main(args: list[str] | None = None) -> int: ...
```

### `remote.py`
```python
def run_ssh_command(host, command, user=None, port=22) -> CompletedProcess: ...
def upload_file(host, local_path, remote_path, user=None, port=22) -> int: ...
def upload_files(host, local_paths, remote_dir, user=None, port=22) -> list[int]: ...
def main(args: list[str] | None = None) -> int: ...
```
**Key constraint**: all subprocess calls use explicit arg lists — no `shell=True`.

### `ssl_utils.py`
```python
def check_expiry(host: str, port: int = 443) -> dict: ...
def verify_pem_file(path: str) -> dict: ...
def main(args: list[str] | None = None) -> int: ...
```

### `netcalc.py`
```python
def main(args: list[str] | None = None) -> int: ...  # cidr subcommand
```
Uses `ipaddress` stdlib — no deps.

### `nettest.py`
```python
async def _check_host(host, port, timeout) -> bool: ...
async def main(args: list[str] | None = None) -> int: ...
```
Uses `asyncio.open_connection` — no external network in tests (mocked).

### `nginx.py` / `proxy_test.py` / `port_forward.py` / `knock.py` / `boot.py`
Each exposes a `main(args)` entrypoint and uses only stdlib.

## Interface Decisions
- All modules register with `tool_registry.register_tool()` at import.
- All `main()` functions accept `list[str] | None` for testability.
- No module-level I/O; all side effects inside function bodies.

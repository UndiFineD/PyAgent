# dev-tools-autonomy — Design

_Status: COMPLETE_
_Designer: @3design | Updated: 2026-03-22_

## Selected Design

### Module Interfaces

#### `src/tools/dependency_audit.py`
```python
def check_dependencies() -> list[dict]: ...
# Returns list of {"name": str, "version": str, "status": "ok"|"outdated"|"missing"}
```

#### `src/tools/metrics.py`
```python
def analyze_file(path: str) -> dict: ...
# Returns {"lines": int, "functions": int, "classes": int, "complexity": int}

def analyze_directory(root: str) -> list[dict]: ...
```

#### `src/tools/self_heal.py`
```python
def run_heal(root: str) -> list[str]: ...
# Returns list of actions taken (created files, removed caches, etc.)
```

#### `src/tools/plugin_loader.py`
```python
def load_plugin(name: str, allowed: list[str]) -> Any: ...
# name must be in allowed list; raises ValueError otherwise
```

## Interface Decisions
- All functions accept explicit root/path args for testability.
- No module-level I/O; all side effects inside function bodies.
- `plugin_loader` enforces an `allowed` allowlist — no arbitrary import injection.
- `metrics.py` uses `ast.parse` (not regex or eval) for safe code analysis.

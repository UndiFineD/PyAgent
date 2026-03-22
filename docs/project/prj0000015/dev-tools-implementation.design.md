# dev-tools-implementation — Design

_Status: COMPLETE_
_Designer: @3design | Updated: 2026-03-22_

## Public API (`src/tools/common.py`)

```python
def load_config(path: str) -> Any:
    """Load JSON (.json) or TOML (.toml) config file."""

def get_logger(name: str, level: int = logging.WARNING) -> logging.Logger:
    """Return idempotent named logger with StreamHandler."""

def ensure_dir(path: str | os.PathLike) -> Path:
    """mkdir -p equivalent; returns Path."""

def retry(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> T:
    """Call fn up to max_attempts times, sleeping delay seconds between tries."""

def format_table(rows: list[list[Any]], headers: list[str]) -> str:
    """Fixed-width text table renderer."""
```

## TOML Detection Pattern
```python
try:
    import tomllib          # stdlib Python 3.11+
except ModuleNotFoundError:
    try:
        import tomli as tomllib   # backport
    except ModuleNotFoundError:
        tomllib = None            # deferred RuntimeError on use
```

## Interface Invariants
- `load_config` dispatches on file extension (`.toml` → TOML, else → JSON).
- `retry` re-raises the *last* exception after all attempts exhausted.
- `format_table` strips trailing whitespace from each rendered row.
- All functions are pure (no module-level side effects).

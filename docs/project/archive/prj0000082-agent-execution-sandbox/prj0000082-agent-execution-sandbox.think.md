# prj0000082 — agent-execution-sandbox — Think

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-26_

---

## Codebase Observations

### BaseAgent and existing mixins

**File:** `src/agents/BaseAgent.py`

`BaseAgent` is an abstract class with lifecycle states (`IDLE`, `RUNNING`, `STOPPED`), a semaphore for
concurrency, and an abstract `run(task)` method. It holds no storage-transaction reference. There are no
mixins composed into `BaseAgent` today — mixin composition is demonstrated by `CortAgent(BaseAgent, CortMixin)`
in `src/core/reasoning/CortAgent.py`.

**Pattern in use (CortMixin):**
```python
class CortMixin:
    async def reason_with_cort(self, prompt: str, **kwargs) -> CortResult:
        core: CortCore = self._cort_core   # accessing attribute provided by owner class
        return await core.run(prompt)

class CortAgent(BaseAgent, CortMixin): ...
```

The mixin accesses a private attribute (`_cort_core`) that the owning class must set. This is the
established convention: **mixins access `self._<core>` attributes; the concrete class initialises them.**

`src/core/base/mixins/` **does not exist yet** — the directory must be created as part of this project.

### StorageTransaction interface (relevant hooks)

**File:** `src/transactions/StorageTransactionManager.py`

`StorageTransaction` supports two modes:
- **Legacy (single-file):** `stage()` → `commit()` / auto-commits on `__exit__`.
- **Multi-op async:** `write(path, content)`, `delete(path)`, `mkdir(path)` → `acommit()`.

Key method signatures for hooking:
```python
async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None
async def delete(self, path: Path) -> None
async def mkdir(self, path: Path) -> None
def commit(self) -> None          # legacy single-file commit; self._target is the path
```

**Current gap:** No validation hook. The `write()` method queues ops directly into `self._ops` without
any path-check callback. The same pattern is true for `delete()` and `mkdir()`.

The `src/core/StorageTransactionManager.py` is a shim that re-exports from `src/transactions/`.

### Prior art — McpSandbox (path-allowlist enforcement)

**Files:** `src/mcp/McpSandbox.py`, `src/mcp/McpServerConfig.py`, `src/mcp/exceptions.py`

`McpSandbox` already implements the exact enforcement pattern needed:
```python
def _is_subpath(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False

def validate_path(self, path: str, config: McpServerConfig) -> Path:
    resolved = Path(path).resolve()   # symlinks resolved → escape-proof
    if not any(_is_subpath(resolved, Path(a).resolve()) for a in config.allowed_paths):
        raise McpPathForbidden(...)
    return resolved
```

`McpServerConfig` already has `allowed_paths: list[str]` and `allowed_hosts: list[str]` fields.
`McpPathForbidden` lives under `McpSandboxError` in a clean exception hierarchy.

**This is directly reusable as the model for `SandboxMixin`.**

### Existing validation patterns

- `ContextTransaction` (in `src/transactions/ContextTransactionManager.py`) uses `contextvars` for
  per-task isolation — relevant if sandbox config needs to be task-scoped (out of scope for Budget S).
- `MemoryTransaction` uses `threading.RLock` and lazy `asyncio.Lock` on the same class — dual
  sync/async protocol is the norm in this codebase.
- `UnifiedTransactionManager` provides a begin/execute/rollback contract but is not yet wired to
  agents — no hook point there for Budget S.

---

## Options Analysis

### Option A: `SandboxedStorageTransaction` subclass + `SandboxMixin`

**Summary:** Subclass `StorageTransaction` to override `write()`, `delete()`, `mkdir()`, and `commit()`
to call `validate_path()` before any op is queued or executed. `SandboxMixin` provides a factory method
`sandbox_tx()` that returns `SandboxedStorageTransaction(config=self._sandbox_config)`. Raises
`SandboxViolationError` on any forbidden path or host.

**Approach:**
```
src/core/sandbox/
    SandboxConfig.py        — dataclass: allowed_paths, allowed_hosts, agent_id
    SandboxViolationError.py — exception hierarchy
    SandboxedStorageTransaction.py — StorageTransaction subclass with path validation
src/core/base/mixins/
    SandboxMixin.py         — mixin providing sandbox_tx(), validate_host()
```

**Implementation sketch:**
```python
@dataclass
class SandboxConfig:
    allowed_paths: list[Path]
    allowed_hosts: list[str]
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class SandboxedStorageTransaction(StorageTransaction):
    def __init__(self, config: SandboxConfig, target=None):
        super().__init__(target)
        self._config = config

    async def write(self, path, content, *, user_id=None):
        _validate_path(path, self._config)   # raises SandboxViolationError
        await super().write(path, content, user_id=user_id)

    async def delete(self, path):
        _validate_path(path, self._config)
        await super().delete(path)

    def commit(self):   # legacy mode: validate self._target
        if self._target is not None:
            _validate_path(self._target, self._config)
        super().commit()
```

**Pros:**
- Directly mirrors `McpSandbox.validate_path()` pattern — no new patterns to learn.
- Symlink-resolved check prevents `../etc/passwd` escapes (already proven in McpSandbox).
- Zero modifications to existing `StorageTransaction` or `BaseAgent` — only new files.
- Transactional: violation raises before any op is queued → rollback is implicit.
- Clean MRO: `SandboxedStorageTransaction` is a real subclass, passes isinstance checks.
- Budget S compatible: ~120 lines production code + ~80 lines tests.
- Can be adopted gradually: existing agents remain unaffected until they opt in.

**Cons:**
- Only guards I/O that goes through `StorageTransaction`. Raw `open()` / `pathlib.write_bytes()` calls
  in agent code bypass enforcement — documented limitation, not a defect.
- `SandboxMixin` requires callers to use `self.sandbox_tx()` factory instead of instantiating
  `StorageTransaction` directly; discipline required.

**Risk:** Medium — bypass possible for code that doesn't use `StorageTransaction`, but acceptable for
Budget S. Enforcement coverage increases as more code migrates to the transaction layer.
**Effort:** S (~2 hours end-to-end)

---

### Option B: Filesystem proxy via `__builtins__` / `sys.modules` monkey-patch

**Summary:** Override `builtins.open`, `pathlib.Path.open`, and `os.open` in the agent's scope to
intercept all file I/O regardless of abstraction layer. Raise `SandboxViolationError` for forbidden paths.

**Pros:**
- Catches all file I/O, including direct `open()` calls.
- No changes needed to `StorageTransaction` or existing agents.

**Cons:**
- Monkey-patching `builtins` is a recognised Python anti-pattern; CPython 3.11+ may cache the
  original `open` in C-level fast paths, breaking the intercept silently.
- `pathlib.Path.open` is a C-extension wrapper in PyPy and CPython optimised builds; monkey-patching
  at class level is fragile across Python versions.
- Thread-safety: replacing process-global refs without a lock creates data races in asyncio coroutines.
- Testing is complex: teardown must restore originals atomically; test isolation breaks.
- An attacker (or buggy agent) can trivially import `io.open` or use `os.open()` directly to bypass.
- Security consensus: runtime monkey-patching is not a reliable security boundary.

**Risk:** High — fragile, hard to test, bypassable.
**Effort:** M (implementation is medium but testing/maintenance is high ongoing cost)

---

### Option C: OS-level isolation (subprocess + Windows Job Object)

**Summary:** Spawn each agent in an isolated subprocess. On Windows, apply a Job Object to restrict
filesystem/network access. On Linux, use `seccomp(2)` or namespace isolation.

**Pros:**
- True, kernel-enforced isolation.
- Cannot be bypassed by Python code regardless of abstraction.
- Industry standard for high-assurance sandboxing.

**Cons:**
- Massive architectural change: every `BaseAgent.run()` would become an IPC call.
- Async coordination (asyncio, event loops) breaks across subprocess boundaries without an explicit
  IPC protocol (e.g., protobuf over stdin/stdout, or a local gRPC channel).
- Windows Job Objects require Win32 API (`ctypes` or `pywin32`), adding a platform-specific
  dependency not in `requirements.txt`.
- Latency and overhead: process spawn for every agent task is expensive at swarm scale.
- Completely out of scope for Budget S — estimated L/XL effort.

**Risk:** Low (security-wise) but High (delivery risk, scope explosion).
**Effort:** XL — far exceeds Budget S. Appropriate for a future Budget L security milestone.

---

### Option D: Decorator / context-manager enforcement (`@sandboxed`)

**Summary:** Annotate every agent method that performs I/O with a `@sandboxed(config)` decorator that
inspects arguments, resolves `Path` parameters, and validates them against `allowed_paths` before
allowing the call.

**Pros:**
- Enforcement is explicit and auditable at the call site.
- No changes to `StorageTransaction` or transaction internals.

**Cons:**
- Every method interacting with filesystem must be explicitly annotated — easy to forget, creating
  silent gaps.
- Path arguments must be identifiable by position or keyword name; no standard convention exists yet
  in this codebase.
- Decorators that inspect arbitrary `**kwargs` for `Path` objects have poor type-checking support
  and increase mypy false-positive rate.
- Network call arguments (URLs, hostnames) are rarely passed as explicit `Path`-typed params, so
  host checking requires a separate parallel decorator.
- `@sandboxed` applied to async methods produces a coroutine-compatible wrapper but adds stack
  frames that complicate tracebacks.

**Risk:** Medium-High — enforcement gaps due to forgotten annotations; maintenance burden grows with
codebase size.
**Effort:** M (initial), but ongoing cost is H as codebase grows.

---

### Option E (bonus): Hook via `StorageTransaction.write` override in agent `__init_subclass__`

**Summary:** Use Python's `__init_subclass__` hook in `BaseAgent` to automatically wrap `StorageTransaction`
instantiation if the subclass sets `_sandbox_config`. Avoids requiring explicit mixin composition.

**Pros:** Zero-annotation adoption — subclasses automatically get sandbox enforcement.

**Cons:**
- `__init_subclass__` modifying class-level behaviour is an implicit, hard-to-trace convention.
- Dynamically replacing instance factory methods is fragile for subclasses that also override
  `StorageTransaction` construction.
- Testing requires carefully constructed metaclass fixtures.

**Risk:** Medium — adoption is easier but debuggability is worse than Option A.
**Effort:** M — similar code, harder to reason about.

---

## Decision Matrix

| Criterion                     | Opt A (Tx subclass) | Opt B (Monkey-patch) | Opt C (OS-level) | Opt D (Decorator) | Opt E (__init_subclass__) |
|-------------------------------|:------------------:|:-------------------:|:----------------:|:-----------------:|:-------------------------:|
| Aligns with existing patterns | ✅ High             | ❌ Low              | ⚠️ N/A           | ⚠️ Medium        | ⚠️ Medium                |
| Reuses McpSandbox prior art   | ✅ Yes              | ❌ No               | ❌ No            | ⚠️ Partial       | ❌ No                     |
| Budget S compatible           | ✅ Yes              | ⚠️ Maybe           | ❌ No            | ✅ Yes           | ✅ Yes                    |
| Security reliability          | ⚠️ Medium          | ❌ Low              | ✅ High          | ⚠️ Medium        | ⚠️ Medium                |
| Testability                   | ✅ High             | ❌ Low              | ⚠️ Medium        | ✅ High          | ⚠️ Medium                |
| Zero regressions              | ✅ Yes (new files)  | ❌ Risky            | ❌ Risky         | ✅ Yes           | ⚠️ Risk if BaseAgent touched |
| Mypy / type-annotation support| ✅ Full             | ❌ Poor             | ⚠️ N/A           | ⚠️ Partial       | ❌ Poor                   |
| Effort (Budget S)             | S                  | M                  | XL               | M                 | M                         |
| Risk                          | Medium             | High               | Low/High         | Medium-High       | Medium                    |

---

## Recommendation

**Recommended option:** Option A — `SandboxedStorageTransaction` subclass + `SandboxMixin`

**Rationale:** Option A directly reuses the `validate_path()` and `_is_subpath()` pattern already
proven in `McpSandbox` (same symlink-resolved allowlist check, same `_is_subpath()` utility). It
introduces only new files (`src/core/sandbox/`, `src/core/base/mixins/`) without touching any existing
module, guaranteeing zero regressions in the 129+ structure tests. The enforcement fires at the exact
point where I/O ops are queued in `StorageTransaction.write()` / `delete()` / `mkdir()`, making the
rollback implicit — the op never reaches the queue. This is the smallest change that delivers a real,
testable security boundary aligned with Budget S and the existing mixin architecture.

---

## Open Questions for @3design

1. Should `SandboxConfig.allowed_paths` accept `str` (like `McpServerConfig`) or `pathlib.Path`?
   Using `Path` is type-safer but requires callers to convert strings; using `str` matches the MCP
   prior art. Suggest `list[Path]` with a `from_strings()` classmethod.
2. Should `SandboxViolationError` derive from `McpSandboxError` (for ecosystem consistency) or stand
   alone as `SandboxViolationError(RuntimeError)`? Standalone avoids importing from `src.mcp` into
   `src.core.sandbox` (cleaner dependency arrow).
3. Should `validate_host()` in `SandboxMixin` perform DNS resolution to detect canonical hostname
   aliasing, or keep it as a simple string-prefix/exact match for Budget S?
4. Is a `wildcard_host = "*"` sentinel (matching `McpServerConfig`) the right API, or should
   "allow all hosts" be expressed as `allowed_hosts=[]` with a separate `allow_all_hosts: bool` flag?
5. Does `@3design` want `SandboxedStorageTransaction` to also wrap the legacy single-file `commit()`
   path (validating `self._target`), or only the multi-op async path for Budget S?

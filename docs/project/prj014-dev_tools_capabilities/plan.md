# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Turn the expanded capabilities design into concrete, test-driven modules and CLI helpers under `src/tools` with accompanying documentation and CI integration.

**Architecture:**
Each capability described in the design will correspond to one or more Python modules
in `src/tools`.  The modules will export functions that can also be executed from
the command line via `if __name__ == "__main__"` blocks.  Shared logic lives in
`src/tools/common.py` (already created), and each module has a unit test under
`tests/tools/`.  A high–level catalog document (`docs/tools.md`) will be kept up to
date as new utilities are added.

Utility modules:

* `git_utils.py` – wrappers for git/gh operations and pre-commit helpers.
* `remote.py` – SSH/FTP helpers based on `paramiko`.
* `ssl_utils.py` – certificate generation and expiry checking.
* `netcalc.py` + `nettest.py` – CIDR/address calculations and dual‑stack tests.
* `nginx.py` + `proxy_test.py` – config rendering and live proxy validation.
* `port_forward.py` + `knock.py` – firewall rule manipulation and knock client.
* `boot.py` – polyglot project bootstrapper.

CI will continue to run all tests; a new lint job may optionally verify the
`docs/tools.md` header, though the earlier plan already added one.

---

### Task 1: Add unit tests for each new module

Create a new test file `tests/tools/test_capabilities_modules.py` that ensures
all modules importable and expose the core API described in the design.  Example:

```python
import importlib.util
import sys

MODULES = [
    "tools.git_utils",
    "tools.remote",
    "tools.ssl_utils",
    "tools.netcalc",
    "tools.nettest",
    "tools.nginx",
    "tools.proxy_test",
    "tools.port_forward",
    "tools.knock",
    "tools.boot",
]


def test_modules_importable(tmp_path):
    # use existing setup to create src layout
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))
    sys.path.insert(0, str(tmp_path / "src"))

    for name in MODULES:
        spec = importlib.util.find_spec(name)
        assert spec is not None, f"cannot find {name}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        # each module must have a __main__ entrypoint callable
        assert hasattr(module, "main")
        assert callable(getattr(module, "main"))
```

Run the test to confirm failure before implementation.

### Task 2: Implement skeleton modules

For each capability, create a minimal module matching the API in the test.
Example for `git_utils.py`:

```python
"""Git and GitHub helper utilities."""

from __future__ import annotations

import subprocess
from typing import List


def main(args: List[str] | None = None) -> int:
    """CLI entrypoint.  `args` defaults to `sys.argv[1:]`."""
    # placeholder implementation
    print("git_utils placeholder")
    return 0
```

Repeat for the other nine modules with placeholder logic and a `main()`.

### Task 3: Add CLI support and help

Each module's `main()` should use `argparse` to expose a `--help` message
and a stub command (e.g. `--version` or `--run-test`).  For now the parser may
be empty; tests only verify the existence of `main`.

### Task 4: Update documentation catalog

Add entries for the new capability modules to `docs/tools.md` describing their
purpose (copying from the expanded design).  Add a lint test to verify the
document is still present (already covered by earlier plan).  Optionally extend
`tests/tools/test_tools_docs.py` to look for each new module name in the file.

### Task 5: Validate in CI

Run full pytest suite to ensure all tests pass; the new importability test will
fail until the modules exist.  No CI config changes needed.

### Task 6: Commit changes

Stage and commit all new modules, tests, and documentation updates with message:

```
feat(tools): implement capability skeletons and import tests
```

push the branch when ready.

---

After these tasks the capabilities design will be translated into actual code
artifacts and the repository will be ready for iterative improvement of each
utility.  At that point the implementation plan will have been executed and we
can circle back to expand individual modules with real functionality.  Hand off
to agent/runSubagent when ready to implement.
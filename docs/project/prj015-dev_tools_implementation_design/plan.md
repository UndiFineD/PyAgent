# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Fulfill the implementation considerations for development tools by adding documentation, ensuring modular helpers, and incorporating the tests into CI.

**Architecture:**
Utilities live under `src/tools/` with tests in `tests/tools/`.  A new documentation page will describe each tool and usage.  A shared helper module (`src/tools/common.py`) will provide config/logging primitives for reuse.  CI already runs all Python tests (`pytest -q`), so no changes are necessary there.

**Tech Stack:** Python 3.11, pytest, Markdown for docs.

---

### Task 1: Document tools catalogue

**Step 1: Write failing test**
- File: `tests/tools/test_tools_docs.py`
- Code:
  ```python
  def test_tools_document_exist() -> None:
      """`docs/tools.md` should exist and begin with a header."""
      import os
      path = os.path.join("docs", "tools.md")
      assert os.path.isfile(path)
      with open(path) as f:
          first = f.readline().strip()
      assert first.startswith("#")
  ```

**Step 2: Run test and watch failure**
- Command: `pytest tests/tools/test_tools_docs.py -q`
- Expect: failure (file missing)

**Step 3: Create documentation file**
- File: `docs/tools.md`
- Initial content:
  ```markdown
  # Development Tools

  This document catalogs the helper utilities bundled in `src/tools`.
  Each module exposes functions that may be invoked from the command line or
  imported by other scripts.  Future entries should include:

  * `dependency_audit` – scan dependency manifests for outdated or vulnerable packages.
  * `metrics` – collect code complexity and coverage metrics.
  * `agent_plugins` – plugin loader framework.
  * `self_heal` – misconfiguration detection and remediation.

  CLI utilities support `--help` output and follow standard exit codes.  See
  individual module docstrings for usage examples.
  ```

**Step 4: Run documentation test again**
- Command: `pytest tests/tools/test_tools_docs.py -q`
- Expect: pass

### Task 2: Create common helper module

**Step 1: Write failing test**
- File: `tests/tools/test_common_helpers.py`
- Code:
  ```python
  def test_common_helpers_importable(tmp_path):
      # structure must exist for import path
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))
      import importlib.util, sys, os
      sys.path.insert(0, str(tmp_path / "src"))
      spec = importlib.util.find_spec("tools.common")
      assert spec is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)  # type: ignore
      assert hasattr(module, "load_config")
      assert callable(module.load_config)
  ```

**Step 2: Run test to confirm failure**
- Command: `pytest tests/tools/test_common_helpers.py -q`

**Step 3: Add module skeleton**
- File: `src/tools/common.py`
- Code:
  ```python
  """Shared helper functions used by development utilities."""

  from typing import Any, Dict
  import json
  import logging

  def load_config(path: str) -> Dict[str, Any]:
      """Load JSON or TOML configuration file from disk."""
      # placeholder uses json only for now
      with open(path, "r", encoding="utf-8") as f:
          return json.load(f)

  def get_logger(name: str) -> logging.Logger:
      logger = logging.getLogger(name)
      if not logger.handlers:
          handler = logging.StreamHandler()
          handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
          logger.addHandler(handler)
      return logger
  ```

**Step 4: Re-run the helper test**
- Command: `pytest tests/tools/test_common_helpers.py -q`

### Task 3: Ensure CLI help support (manual spot check)

**Step 1:** Open one of the tool modules (e.g. `dependency_audit.py`) and add
`if __name__ == "__main__":` block that prints usage or calls an `argparse`
parser.  The following example may be included in each module eventually.


### Task 4: Update CI workflow (no change required)

- CI already runs `pytest -q` which includes the newly added tests.
- No file modifications needed unless we want to limit to `tests/tools`; not
  required now.

### Task 5: Commit documentation and helper

- `git add docs/tools.md src/tools/common.py tests/tools/test_tools_docs.py tests/tools/test_common_helpers.py`
- `git commit -m "docs: add tools catalog + common helper"`
- `git push`

---

Once these tasks are implemented, the implementation considerations will be
satisfied and we can proceed to flesh out real utilities based on the earlier
sketch.  Hand off to superpower-execute when ready to execute the plan.
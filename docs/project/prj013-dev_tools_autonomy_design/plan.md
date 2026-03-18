# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Build the scaffolding for self‑improving development tools: 
  dependency auditor, code‑metrics collector, plugin framework 
  and self‑healing helper.  Establish TDD tests and update the setup helper 
  to ensure necessary files/directories exist.

**Architecture:**
- Simple Python modules live under `src/tools/*.py` exposing a small API.
- Tests under `tests/tools/` exercise each API function; 
  they run the existing `scripts/setup_structure.create_core_structure` 
  helper to prepare directory layout.
- `scripts/setup_structure.py` will be extended so new files/dirs 
  are created automatically in fresh workspaces.

**Tech Stack:** Python, pytest.

---

### Task 1: Dependency audit skeleton

**Step 1: Write failing test**
- File: `tests/tools/test_dependency_audit.py`
- Code:
  ```python
  from pathlib import Path

  def test_dependency_audit_returns_list(tmp_path: Path) -> None:
      """`check_dependencies` should exist and return a list (empty or not)."""
      # ensure layout
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))

      import importlib.util, sys
      sys.path.insert(0, str(tmp_path / "src"))
      spec = importlib.util.find_spec("tools.dependency_audit")
      assert spec is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)  # type: ignore
      assert hasattr(module, "check_dependencies")
      result = module.check_dependencies()
      assert isinstance(result, list)
  ```

**Step 2: Run test and observe failure**
- Command: `pytest tests/tools/test_dependency_audit.py -q`
- Expected: import error because module missing

**Step 3: Implement skeleton module**
- File: `src/tools/dependency_audit.py`
- Code:
  ```python
  """Simple utility to audit project dependencies."""

  from typing import List

  def check_dependencies() -> List[str]:
      # placeholder implementation; real logic will scan toml/json files
      return []
  ```

**Step 4: Run the single test again to ensure it passes**
- Command: `pytest tests/tools/test_dependency_audit.py -q`
- Expected: pass

### Task 2: Code‑metrics collector skeleton

**Step 1: Write failing test**
- File: `tests/tools/test_metrics_collector.py`
- Code:
  ```python
  def test_metrics_collector_api(tmp_path):
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))

      import importlib.util, sys
      sys.path.insert(0, str(tmp_path / "src"))
      spec = importlib.util.find_spec("tools.metrics")
      assert spec is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)  # type: ignore
      assert hasattr(module, "collect_metrics")
      assert callable(module.collect_metrics)
  ```

**Step 2: Run test to confirm failure**
- Command: `pytest tests/tools/test_metrics_collector.py -q`

**Step 3: Add skeleton file**
- File: `src/tools/metrics.py`
- Code:
  ```python
  """Compute code metrics for the repository."""

  from typing import Dict

  def collect_metrics() -> Dict[str, int]:
      # placeholder returns empty metrics map
      return {}
  ```

**Step 4: Re-run the single test**
- Command: `pytest tests/tools/test_metrics_collector.py -q`

### Task 3: Plugin loader framework

**Step 1: Write failing test**
- File: `tests/tools/test_plugin_loader.py`
- Code:
  ```python
  def test_plugin_loader_creates_directory(tmp_path):
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))

      # ensure plugin directory exists after import
      import importlib.util, sys, os
      sys.path.insert(0, str(tmp_path / "src"))
      spec = importlib.util.find_spec("tools.agent_plugins")
      assert spec is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)  # type: ignore
      assert os.path.isdir(str(tmp_path / "src" / "tools" / "plugins"))
  ```

**Step 2: Run test and watch failure**
- Command: `pytest tests/tools/test_plugin_loader.py -q`

**Step 3: Create module & plugin dir**
- File: `src/tools/agent_plugins.py`
- Code:
  ```python
  import os
  from pathlib import Path

  PLUGIN_DIR = Path(__file__).parent / "plugins"
  PLUGIN_DIR.mkdir(exist_ok=True)

  def load_plugins():
      # placeholder; real loader would import modules dynamically
      return []
  ```

Also update `scripts/setup_structure.py` to create `src/tools/plugins` path
(as part of the list added in previous plan). It already creates `src/tools`, but plugin subdir will be automatically created by module because of `mkdir` call—still we can add for completeness.

**Step 4: Re-run plugin loader test and subset**
- Commands:
  ```powershell
  pytest tests/tools/test_plugin_loader.py -q
  ```

### Task 4: Self‑healing helper stub

**Step 1: Write failing test**
- File: `tests/tools/test_self_healing.py`
- Code:
  ```python
  def test_self_healing_detects(tmp_path):
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))

      import importlib.util, sys
      sys.path.insert(0, str(tmp_path / "src"))
      spec = importlib.util.find_spec("tools.self_heal")
      assert spec is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)  # type: ignore
      assert hasattr(module, "detect_misconfig")
      info = module.detect_misconfig()
      assert isinstance(info, dict)
  ```

**Step 2: Run test to see failure**
- Command: `pytest tests/tools/test_self_healing.py -q`

**Step 3: Add stub module**
- File: `src/tools/self_heal.py`
- Code:
  ```python
  """Self‑healing helper utilities."""

  from typing import Dict

  def detect_misconfig() -> Dict[str, str]:
      # placeholder returns nothing wrong
      return {}
  ```

**Step 4: Run the test again**
- Command: `pytest tests/tools/test_self_healing.py -q`

### Task 5: Commit new modules and tests

- `git add src/tools/dependency_audit.py src/tools/metrics.py src/tools/agent_plugins.py src/tools/self_heal.py tests/tools/*.py`
- `git commit -m "feat: add autonomy scaffolding for dev tools"`
- `git push`

### Task 6: Verify entire tools test suite

- Command: `pytest tests/tools -q` (once all tests exist)
- Expected: all pass.

### Task 7: (Optional) update `scripts/setup_structure.py` if plugin dir not covered

- Already ensures `src/tools` and touches README; 
  the plugin module mkdir handles plugins dir, 
  but you may also add to paths for explicit creation.

---

With these tasks completed, the autonomy design document 
will have concrete skeletons ready for iteration.  
Hand off to superpower-execute when you want to implement them.  
Let me know if you want to break this into smaller plans 
or include more features!
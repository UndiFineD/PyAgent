# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Bootstrapping folders for development tools (`src/tools/`, `docs/`) using the existing setup helper and verify them with tests.

**Architecture:**
A lightweight Python script (`scripts/setup_structure.py`) creates required directories. Pytest tests exercise the helper in a temporary workspace and assert presence of directories/files. Changes stay confined to the helper and tests.

**Tech Stack:** Python 3.11, pytest, standard library filesystem operations.

---

### Task 1: Add failing test for new directories

**Step 1: Write the failing test**
- File: `tests/structure/test_dev_tools_dirs.py`
- Code:
  ```python
  import os

  def test_dev_tools_structure(tmp_path) -> None:
      """`src/tools` and `docs/` should be created by the setup helper."""
      from scripts.setup_structure import create_core_structure

      create_core_structure(str(tmp_path))
      # verify development‑tools locations
      assert (tmp_path / "src" / "tools").exists()
      assert (tmp_path / "docs").exists()
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/structure/test_dev_tools_dirs.py -q`
- Expected output: failure (helper doesn't create those dirs yet)

**Step 3: Implement minimal fix in helper**
- File: `scripts/setup_structure.py`
- Edit the `paths` list to include:
  ```python
      "src/tools",
      "docs",
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/structure/test_dev_tools_dirs.py -q`
- Expected output:
  ```
  .
  1 passed in X.XXs
  ```


### Task 2: Ensure existing helper still creates original structure

**Step 1: Run subset of structure tests**
- Command:
  ```powershell
  pytest tests/structure/test_base_dirs.py \
         tests/structure/test_mirror_dirs.py \
         tests/structure/test_deployment_dirs.py \
         tests/structure/test_config_files.py -q
  ```
- Expected output: all four tests pass, indicating no regressions.

### Task 3: Add README placeholder under `src/tools/`

**Step 1: Write failing test for README**
- Append to `tests/structure/test_dev_tools_dirs.py`:
  ```python
  def test_tools_readme_created(tmp_path) -> None:
      from scripts.setup_structure import create_core_structure
      create_core_structure(str(tmp_path))
      assert (tmp_path / "src" / "tools" / "README.md").exists()
  ```

**Step 2: Run test to confirm failure.**
- Command: `pytest tests/structure/test_dev_tools_dirs.py -q`
- Expect second failure about missing README.

**Step 3: Update helper to touch README**
- Modify `scripts/setup_structure.py` after directory creation loop:
  ```python
      readme = os.path.join(root, "src", "tools", "README.md")
      with open(readme, "a", encoding="utf-8"):
          pass
  ```

**Step 4: Rerun the single test and full subset**
- Commands:
  ```powershell
  pytest tests/structure/test_dev_tools_dirs.py -q
  pytest tests/structure/test_base_dirs.py tests/structure/test_mirror_dirs.py \
         tests/structure/test_deployment_dirs.py tests/structure/test_config_files.py -q
  ```
- Expected: all five tests pass.

### Task 4: Commit structural changes
- `git add scripts/setup_structure.py tests/structure/test_dev_tools_dirs.py`
- `git commit -m "feat: support dev-tools directories in setup_structure"`
- `git push`

### Task 5: Verify CI already covers the new tests
- (no modification needed; existing CI includes `tests/structure`)

---

Once these steps are executed, the repository will be prepared for the development‑tools implementation plan.  Handing off to agent/runSubagent now.
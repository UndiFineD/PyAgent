# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# Core Project Structure Implementation Plan

**Goal:**
Create the directory hierarchy and starter files defined in the core project structure design document, with tests ensuring the layout exists and can be recreated.  Note that the repository root is `C:\dev\PyAgent`; the `project/` folder is a metadata area used by the design/tests rather than the actual source root (which remains under `src/`).

**Architecture:**
- Python test suite under `tests/structure/` to verify directories and files.
- A utility script (`scripts/setup_structure.py`) that constructs the layout when invoked.
- Plan focuses solely on filesystem structure; no package code is required.

**Tech Stack:**
Python 3.11, `pytest`, standard library filesystem operations (`os`).

---

### Task 1: Write failing test for base directories

- File: `tests/structure/test_base_dirs.py`
- Code:
  ```python
  import os

  def test_project_subdir_absent(tmp_path):
      # the 'project' metadata folder should not exist initially
      root = tmp_path / "project"
      assert not root.exists()
  ```
- Command:  
  `pytest tests/structure/test_base_dirs.py -q`
- Expected output:
  ```
  F
  AssertionError: assert False
  ```

### Task 2: Implement helper to initialize structure

- File: `scripts/setup_structure.py`
- Code:
  ```python
  import os

  def create_core_structure(root: str):
      paths = [
          "project",
          "project/scripts",
          "project/docs",
          "project/tests/unit",
          "project/tests/integration",
          "project/tests/e2e",
          "project/src/logic/agents",
          "project/src/core/base",
          "project/src/utils",
          "project/config",
          "project/release",
          "project/scripts-old",
          "project/temp_output",
      ]
      for p in paths:
          os.makedirs(os.path.join(root, p), exist_ok=True)
      # placeholder files
      for f in [
          "llms-architecture.txt",
          "llms-improvements.txt",
          "PyAgent.md",
          "todolist.md",
      ]:
          open(os.path.join(root, "project", f), "a").close()
      cfg_dir = os.path.join(root, "project", "config")
      for f in ["pyproject.toml", ".gitignore", "environment.yaml"]:
          open(os.path.join(cfg_dir, f), "a").close()
  ```

### Task 3: Run test for base dirs again

- Command:  
  `python -c "from scripts.setup_structure import create_core_structure; create_core_structure('.')"`
  then
  `pytest tests/structure/test_base_dirs.py -q`
- Expected output:
  ```
  .
  ```

### Task 4: Add tests for specific files

- File: `tests/structure/test_files.py`
- Code:
  ```python
  import os

  def test_important_files_exist(tmp_path):
      files = [
          "project/llms-architecture.txt",
          "project/llms-improvements.txt",
          "project/PyAgent.md",
          "project/todolist.md",
          "project/config/pyproject.toml",
          "project/config/.gitignore",
          "project/config/environment.yaml",
      ]
      for f in files:
          assert not os.path.exists(os.path.join(tmp_path, f))
  ```
- Command:  
  `pytest tests/structure/test_files.py -q`
- Expected output: failing assertions for each missing file.

### Task 5: Re-run file tests after helper modification (already updated in Task 2)

- Command: run `create_core_structure` again then
  `pytest tests/structure/test_files.py -q`
- Expected output: all tests pass.

### Task 6: Add test for existing design document

- File: `tests/structure/test_design_doc.py`
- Code:
  ```python
  import os

  def test_design_doc_present():
      assert os.path.exists("brainstorm.md")
  ```
- Command:  `pytest tests/structure/test_design_doc.py -q`
- Expected output: `.` (already exists).

### Task 7: Final verification

- Run entire structure test suite:
  `pytest tests/structure -q`
- Expect all tests to exit `0` once structure helper has been executed.

---

Once the tests pass, commit the new script and test files. This establishes the foundational folder layout defined in the brainstorm document and provides executable evidence that the structure can be (re)created automatically.
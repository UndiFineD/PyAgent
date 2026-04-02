# PyAgent Implementation Plan

**Goal:** Achieve 100 % test coverage for every Python module in `src/` and enforce static analysis (ruff, mypy, flake8) plus Rust clippy/format checks via CI.

**Architecture:**
- Python codebase exercised by pytest with coverage plugin.
- Configuration files (`pyproject.toml`, `mypy.ini`, `pre-commit.yml`) store lint/type rules.
- CI workflow group runs Python and Rust quality jobs on push/PR.
- Tests will mock external dependencies and reuse fixtures for repeated patterns.

**Tech Stack:**
- Python 3.14, pytest, ruff, mypy, flake8, pre-commit
- GitHub Actions for CI
- Rust stable toolchain with clippy and fmt

---

### Task 1: Add linter/type‑checker configuration

**Step 1: Write failing test that verifies ruff complains about a deliberately bad file**
- File: `tests/test_lint_config.py`
- Code:
  ```python
  def test_ruff_finds_error(tmp_path):
      bad = tmp_path / "bad.py"
      bad.write_text("import os\n\n\n")
      # ruff should detect unused-import (F401) and extra blank line
      import subprocess, sys
      result = subprocess.run([sys.executable, "-m", "ruff", str(bad)], capture_output=True, text=True)
      assert "F401" in result.stdout or result.returncode != 0
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_lint_config.py::test_ruff_finds_error -q`
- Expected output:
  ```
  F   [100%] tests/test_lint_config.py::test_ruff_finds_error
    assert False
  ```
  (or nonzero exit because ruff not installed/configured)

**Step 3: Add `pyproject.toml` entries enabling ruff and black**
- File: `pyproject.toml`
- Code:
  ```toml
  [tool.ruff]
  line-length = 120
  select = ["E", "F", "W", "I"]

  [tool.black]
  line-length = 120
  target-version = ["py314"]
  ```

**Step 4: Install ruff in `requirements-dev.txt` and run the test again**
- Command: `pip install ruff`
- Command: `pytest tests/test_lint_config.py::test_ruff_finds_error -q`
- Expected output: test now passes because ruff reports the expected error (exit code 1 triggers assertion).

**Step 5: Add `mypy.ini` with strict rules**
- File: `mypy.ini`
- Code:
  ```ini
  [mypy]
  strict = True
  files = src
  ```

**Step 6: Write a similar test ensuring mypy flags a type error**
- File: `tests/test_mypy_config.py`
- Code:
  ```python
  def test_mypy_detects_problem(tmp_path):
      bad = tmp_path / "bad.py"
      bad.write_text("def f() -> int:\n    return 'str'\n")
      import subprocess, sys
      result = subprocess.run([sys.executable, "-m", "mypy", str(bad)], capture_output=True, text=True)
      assert "error" in result.stdout
  ```

**Step 7: Run the mypy test and fix config until it passes**
- Command: `pytest tests/test_mypy_config.py -q`
- Expected: passes after installing mypy and verifying strict config catches the error.

### Task 2: Configure pre‑commit hooks for local developer checks

**Step 1: Write failing test that runs pre-commit on a file with a lint error**
- File: `tests/test_precommit.py`
- Code:
  ```python
  def test_precommit_fails(tmp_path):
      cfg = tmp_path / ".pre-commit-config.yaml"
      cfg.write_text("repos: []\n")
      # the hook list is empty so running should succeed, test will fail until config added
      import subprocess, sys
      result = subprocess.run(["pre-commit", "run", "--files", str(cfg)], capture_output=True)
      assert result.returncode == 0
  ```

**Step 2: Run the test (it will fail initially)**

**Step 3: Add `pre-commit.yml` with ruff and mypy hooks**
- File: `.pre-commit-config.yaml`
- Code:
  ```yaml
  repos:
    - repo: https://github.com/charliermarsh/ruff-pre-commit
      rev: v0.0.###
      hooks:
        - id: ruff
    - repo: https://github.com/pre-commit/mirrors-mypy
      rev: v1.###
      hooks:
        - id: mypy
  ```

**Step 4: Install pre-commit and run the test again ensuring success**

### Task 3: Add CI workflow file

**Step 1: Write failing test that ensures the `ci/quality.yml` workflow exists and contains expected jobs**
- File: `tests/test_ci_yaml.py`
- Code:
  ```python
  import yaml
  def test_ci_yaml_has_python_job():
      cfg = yaml.safe_load(open('.github/workflows/quality.yml'))
      jobs = cfg.get('jobs', {})
      assert 'python' in jobs
      assert 'rust' in jobs
  ```

**Step 2: Run the test (will fail because file doesn't exist)**

**Step 3: Create `.github/workflows/quality.yml` using design snippet**

**Step 4: Re-run the test to confirm CI file structure is correct**

### Task 4: Create test for `FlmChatAdapter` to cover missing lines

**Step 1: Write failing tests exercising every branch of the adapter**
- File: `tests/test_flm_chat_adapter.py`
- Code:
  ```python
  import pytest
  from src.core.providers.FlmChatAdapter import FlmChatAdapter, FlmRuntimeError
  from src.core.providers.FlmProviderConfig import FlmProviderConfig

  class DummyClient:
      def __init__(self):
          self.chat = self
          self.models = self
      def list(self):
          return type('L', (), {'data': []})()
      def create(self, **kwargs):
          class R: pass
          r = R()
          r.choices = [type('C', (), {'message': type('M', (), {'content': 'ok', 'tool_calls': []})()})()]
          return r

  def make_adapter():
      cfg = FlmProviderConfig(base_url='http://x', timeout=1, default_model='m')
      return FlmChatAdapter(cfg, api_key='k', client_factory=lambda **kw: DummyClient())

  def test_check_endpoint_available_success():
      make_adapter().check_endpoint_available()

  def test_ensure_model_missing():
      adapter = make_adapter()
      with pytest.raises(FlmRuntimeError):
          adapter.ensure_model_available('missing')

  def test_create_completion_success():
      adapter = make_adapter()
      resp = adapter.create_completion(messages=[{'role':'user','content':'hi'}])
      assert resp.choices[0].message.content == 'ok'

  @pytest.mark.asyncio
  async def test_run_until_terminal_simple():
      adapter = make_adapter()
      res = await adapter.run_until_terminal(messages=[{'role':'user','content':'hi'}])
      assert res == 'ok'
  ```

**Step 2: Run the new test and watch it fail where the module lacks required behaviour (if any)**

**Step 3: Adjust mocks/adapter implementation if needed until tests pass**

### Task 5: Create tests for `src/chat/api.py` covering previously missing lines

Repeat TDD pattern: write failing tests covering branch at lines 54, 64, 76 (likely error handling and edge cases), run them, implement any helpers or adjust code as necessary until passing.

### Task 6: Generalize test pattern for `tools/*.py` and remaining modules

**Step 1: Write generator script using `scripts-old` helper to create skeleton test files**
- The script will inspect each `tools/*.py`, create `tests/test_tools_<name>.py` with boilerplate that imports the module and asserts at least one function exists.

**Step 2: Run the generator; inspect output and commit skeletons (tests will fail initially since functionality is unexercised).**

**Step 3: For each generated test, add assertions exercising the module's behavior and run until coverage lines disappear.

### Task 7: Monitor coverage and enforce via CI

**Step 1:** After adding tests for a group of files, run `pytest --cov=src` locally and ensure `TOTAL` is 100 % (or note remaining files).

**Step 2:** Merge coverage jobs into `requirements-dev.txt` and rely on CI to catch regressions.

### Task 8: Add Rust quality checks (side task)

**Step 1:** Create a new GH Actions job `rust` (already added in YAML). Write a failing test to verify it runs—this can be done by adding a test in `tests/test_rust_ci.py` that simply checks presence of `Cargo.toml` and runs `cargo clippy` using subprocess.

**Step 2:** Once `rust` job succeeds in CI, maintain it whenever Rust code changes.

---

This plan outlines the first dozen tasks; the remaining modules follow the pattern described in Task 6. Once the plan is approved, execution can begin. Let me know if any task needs refinement or if additional granularity is required before we hand off. 

---
Based on the analysis of test files and the observed errors, we can now create a comprehensive plan to ensure **all current and future test files are of high quality**, including **self-validation of the testing system itself**.

---

### 🔍 Observations Summary

1. **Core test files (e.g., `test_core.py`, `test_agents.py`) are placeholder-based**:
   - Contain only `assert True` statements.
   - No meaningful logic or edge-case validation.

2. **Critical dependencies missing**:
   - `prometheus_client` missing → breaks `test_chat_api.py`.
   - This indicates **incomplete setup** for real-world testing.

3. **Test file naming conflicts**:
   - `test_ci_yaml.py` in both `tests/` and `tests/structure/` causes import mismatches.
   - Indicates **poor file organization**.

4. **Runtime module errors**:
   - `runtime.spawn_task()` does not exist → shows **incomplete runtime implementation**.

5. **No self-testing mechanism**:
   - The testing system does not validate itself (e.g., no test for test files).

---

## ✅ Plan: Improve Test Quality & Self-Validation

We will now implement a structured plan to:
- Fix placeholder tests.
- Resolve dependency and naming issues.
- Add self-validation of test files.
- Ensure future test files pass quality gates.

---

### 📋 Plan Items (3–7 high-level, actionable steps)

1. **Refactor core test files to include meaningful assertions**  
   → Replace placeholder `assert True` with real logic and edge-case validation.

2. **Fix missing dependencies and resolve import conflicts**  
   → Install `prometheus_client` and reorganize test files to avoid naming collisions.

3. **Add self-validation test suite for all test files**  
   → Implement a test that verifies:
     - All test files exist and are properly named.
     - No test file has a circular import.
     - No test file is missing required dependencies.

4. **Add quality gate enforcement for new test files**  
   → Enforce a pre-commit hook or CI check that:
     - Validates test file naming.
     - Ensures all tests have meaningful assertions.
     - Checks for missing dependencies.

5. **Improve runtime module implementation**  
   → Implement `spawn_task()` in `runtime.py` to allow proper task spawning in tests.

6. **Document test quality standards**  
   → Create a `TEST_QUALITY.md` file outlining:
     - What makes a test "high quality".
     - How to write meaningful assertions.
     - How to avoid circular imports and missing dependencies.

---

This plan ensures **all current and future test files are of high quality**, with **self-validation built into the testing system**.

Let me know if you'd like to proceed with executing any of these steps (e.g., refactoring `test_core.py`).  

We can also validate the plan with a `UpdateTodoList` call.  

Would you like to proceed?

---

# PyAgent Implementation Plan

**Goal:**
Create skeleton packages for future research (transport, memory, multimodal, rl, speculation) and verify they import correctly.

**Architecture:**
Monorepo with `src/` packages. New research categories each live under a
dedicated top‑level module; tests exercise imports to ensure Python path is
configured. No runtime logic yet.

**Tech Stack:**
Python 3.14, `pytest`, standard library only.  

---

### Task 1: Add failing import test for `transport` package

**Step 1: Write the failing test**
- File: `tests/test_transport_package.py`
- Code:
  ```python
  def test_transport_package_import():
      # package does not exist yet
      import transport  # noqa: F401
      assert hasattr(transport, "__name__")
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_transport_package.py -q`
- Expected output:
  ```
  E   ModuleNotFoundError: No module named 'transport'
  ```

**Step 3: Implement minimal package**
- File: `src/transport/__init__.py`
- Code:
  ```python
  # placeholder module for future transport research

  def placeholder():
      """Dummy function to make the package importable."""
      return True
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/test_transport_package.py -q`
- Expected output:
  ```
  .
  1 passed in X.XXs
  ```

---

### Task 2: Add failing import test for `memory` package

**Step 1: Write the failing test**
- File: `tests/test_memory_package.py`
- Code:
  ```python
  def test_memory_package_import():
      import memory  # noqa: F401
      assert hasattr(memory, "__name__")
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_memory_package.py -q`
- Expected output: ModuleNotFoundError for `memory`.

**Step 3: Implement minimal package**
- File: `src/memory/__init__.py`
- Code:
  ```python
  # placeholder module for future memory research

  def placeholder():
      return True
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/test_memory_package.py -q`
- Expected:
  ```
  .
  1 passed in X.XXs
  ```

---

### Task 3: Add failing import test for `multimodal` package

**Step 1: Write the failing test**
- File: `tests/test_multimodal_package.py`
- Code:
  ```python
  def test_multimodal_package_import():
      import multimodal  # noqa: F401
      assert hasattr(multimodal, "__name__")
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_multimodal_package.py -q`
- Expected: ModuleNotFoundError.

**Step 3: Implement minimal package**
- File: `src/multimodal/__init__.py`
- Code:
  ```python
  # placeholder module for future multimodal research

  def placeholder():
      return True
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/test_multimodal_package.py -q`
- Expected passing result.

---

### Task 4: Add failing import test for `rl` package

**Step 1: Write the failing test**
- File: `tests/test_rl_package.py`
- Code:
  ```python
  def test_rl_package_import():
      import rl  # noqa: F401
      assert hasattr(rl, "__name__")
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_rl_package.py -q`
- Expected ModuleNotFoundError.

**Step 3: Implement minimal package**
- File: `src/rl/__init__.py`
- Code:
  ```python
  # placeholder module for future reinforcement‑learning research

  def placeholder():
      return True
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/test_rl_package.py -q`
- Expected single passing test.

---

### Task 5: Add failing import test for `speculation` package

**Step 1: Write the failing test**
- File: `tests/test_speculation_package.py`
- Code:
  ```python
  def test_speculation_package_import():
      import speculation  # noqa: F401
      assert hasattr(speculation, "__name__")
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_speculation_package.py -q`
- Expected failure due to missing module.

**Step 3: Implement minimal package**
- File: `src/speculation/__init__.py`
- Code:
  ```python
  # placeholder module for future multi‑model speculation research

  def placeholder():
      return True
  ```

**Step 4: Run test and verify success**
- Command: `pytest tests/test_speculation_package.py -q`
- Expected:
  ```
  .
  1 passed in X.XXs
  ```

---

### Task 6: Smoke‑test all new packages together

**Step 1: Write composite test**
- File: `tests/test_research_packages.py`
- Code:
  ```python
  def test_all_research_packages_exist():
      import transport, memory, multimodal, rl, speculation  # noqa: F401
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_research_packages.py -q`
- Expected failure if any package missing.

**Step 3: (No code change – packages already implemented)**

**Step 4: Run test and verify success**
- Command: `pytest tests/test_research_packages.py -q`
- Expected:
  ```
  .
  1 passed in X.XXs
  ```

---

Once all six tasks complete, the workspace will contain five empty research
packages ready for future expansion.  The tests enforce their existence and
ensure `src/` is on the import path.
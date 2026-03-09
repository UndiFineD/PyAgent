# Context Management Implementation Plan

**Goal:**
Build the foundational libraries for handling large agent contexts and
dynamic tool/skill registration as outlined in the future roadmap design.

**Architecture:**
A Python package `src/context_manager/` provides a simple in‑memory
fragmenting context manager and a `src/skills_registry/` module scans
`.agents/skills` for YAML/JSON metadata.  Each module has accompanying
pytest tests.  The context manager will later be called from agents but we
start with standalone unit tests.

**Tech Stack:**
Python 3.14, pytest, `pathlib`, `yaml` (PyYAML) for metadata parsing,
`typing` for signatures.

---

### Task 1: ContextManager API skeleton

**Step 1: Write failing test**
- File: `tests/test_context_manager.py`
- Code:
  ```python
  def test_context_manager_basic(tmp_path):
      from context_manager import ContextManager
  
      cm = ContextManager(max_tokens=10)
      cm.push("hello world")
      assert cm.snapshot() == "hello world"
  ```

**Step 2: Run and confirm import failure.**

**Step 3: Implement stub**
- File: `src/context_manager/__init__.py`
  ```python
  class ContextManager:
      def __init__(self, max_tokens: int):
          self._data = []
          self.max_tokens = max_tokens
  
      def push(self, text: str) -> None:
          self._data.append(text)
  
      def snapshot(self) -> str:
          return "".join(self._data)
  ```

**Step 4: Run test and see it pass.**

---

### Task 2: Windowing behaviour

**Step 1:** Extend `tests/test_context_manager.py` with a second test
checking that pushing multiple strings exceeding `max_tokens` prunes older
segments.

**Step 2:** Run and observe failure.

**Step 3:** Update `ContextManager.push` to trim tokens (simple word count
for now).

**Step 4:** Re-run tests until they pass.

---

### Task 3: Skill registry scanning

**Step 1:** Write failing test in `tests/test_skills_registry.py` that creates
a temporary `.agents/skills` folder, drops a dummy `foo.yaml` with
`name: foo`, and asserts `registry.list_skills()` returns `['foo']`.

**Step 2:** Run test to confirm failure.

**Step 3:** Implement `src/skills_registry/__init__.py` with a function that
walks the given directory and parses each YAML file to collect `name`.

**Step 4:** Run test until passing.

---

### Task 4: Integration smoke test

**Step 1:** Add `tests/test_system_integration.py` ensuring both modules
can be imported and used together (e.g. create a ContextManager instance and
a registry pointing at an empty temp dir).

**Step 2:** Run and watch failure if any.

**Step 3:** Implement any missing exports to make import succeed.

**Step 4:** Verify test passes.

---

Once these tasks are complete the repository will contain working
context‑management and skill‑registration libraries with tests guarding the
basic behaviours referenced in the roadmap design.

## Implementation Status

The context manager and skills registry packages have already been
implemented and are exercised by unit tests:

* `tests/test_context_manager.py` verifies basic push/snapshot behaviour and
  windowing logic, and passes against `src/context_manager/__init__.py`.
* `tests/test_skills_registry.py` confirms that YAML files under
  `.agents/skills` are discovered; the registry in `src/skills_registry/__init__.py`
  satisfies the test.
* `tests/test_system_integration.py` imports both modules together, which also
  succeeds.

All of the plan’s numbered tasks have been executed and the code is committed.

After all tests pass, commit the new modules and tests.
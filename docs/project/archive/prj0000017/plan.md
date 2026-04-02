# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Execute the full utilities design by verifying structure, documenting
capabilities, scaffolding modules, and supporting autonomy features.  This plan
brings together the separate design documents into a cohesive set of test‑driven
steps.

**Architecture:**
Modules live under `src/tools/` with a shared `common.py` helper.  Tests reside in
`tests/tools/`; CI already runs `pytest -q` on all Python tests.  Documentation
is maintained in `docs/tools.md`, which the tests validate.  Autonomy code such
as `self_heal` is treated the same as other utilities but may run on a schedule.

**Tech Stack:** Python 3.11, pytest, Markdown, argparse for CLI helpers.

---

### Task 1: Assert repository structure

**Step 1: Write a failing test**
- File: `tests/tools/test_structure_layout.py`
- Code:
  ```python
  import os

  def test_tools_directories_exist() -> None:
      assert os.path.isdir("src/tools"), "src/tools directory missing"
      assert os.path.isdir("tests/tools"), "tests/tools directory missing"
      assert os.path.isfile(os.path.join("docs", "tools.md"))
  ```

**Step 2: Run the test**
- Command: `pytest tests/tools/test_structure_layout.py -q`
- Expect: failure until `src/tools`/`tests/tools` are present (they already are, so
  success should occur immediately).

*Note:* structure script (`scripts/setup_structure.py`) is used by other tests
and already creates these directories, so this test mainly codifies the design.

### Task 2: Extend capability importability test

**Step 1: Modify existing test**
- File: `tests/tools/test_capabilities_modules.py`
- Add `tools.self_heal` to `MODULES`, and adjust loop logic so that if the
  module name ends with `self_heal` the assertion checks for a
  `detect_misconfig` callable rather than a `main()` entrypoint.

**Step 2: Run the test**
- Command: `pytest tests/tools/test_capabilities_modules.py -q`
- Expect: failure because `self_heal` currently lacks `main` (and
  corresponding logic).

### Task 3: Add CLI support to autonomy module

**Step 1: Update `src/tools/self_heal.py`**
- Add a `main()` function that prints a placeholder message and returns 0.
- Retain existing `detect_misconfig()` function.

**Step 2: Re-run capability test**
- Command: `pytest tests/tools/test_capabilities_modules.py -q`
- Expect: pass, confirming importability improvements.

### Task 4: Update documentation catalog

**Step 1: Edit `docs/tools.md`**
- Move `self_heal` from the "future entries" list into the skeleton list.
- Ensure the description explains its autonomy purpose.

**Step 2: Extend docs test**
- Modify `tests/tools/test_tools_docs.py` to assert presence of `self_heal` in
  the file contents (the earlier change already added this, but include it in
  the plan for completeness).

**Step 3: Run docs test**
- Command: `pytest tests/tools/test_tools_docs.py -q`
- Expect: pass after edits.

### Task 5: Validate the full toolkit tests

**Step 1:** Run the entire `tests/tools` suite to confirm all tests succeed.
- Command: `pytest tests/tools -q`
- Expected output: `7 passed` (may increase as tests grow).

### Task 6: Commit and push changes

- Stage all new/modified files:
  ```powershell
  git add src/tools/*.py docs/tools.md tests/tools/*.py
  ```
- Commit with message:
  `feat(tools): scaffold utilities, structure tests, and docs`.
- Push to remote.

---

Executing this plan will align the repository with the comprehensive
`dev_tools_utilities_design.md` document: the structure is enforced, every
capability has a placeholder module and import test, autonomy code is included,
and the documentation mirrors the actual codebase.  Once complete, further
plans can expand individual utilities with meaningful logic.

Hand off to **agent/runSubagent** when ready to implement these steps.
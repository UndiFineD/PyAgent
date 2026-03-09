# Future Roadmap Implementation Plan

**Goal:**
Translate the high‑level roadmap design into concrete planning artifacts and
utilities: vision statement, milestone documents, prioritization templates,
R&D tracking, and basic benchmarking scaffolds.

**Architecture:**
Documents will live under `project/roadmap.md` or `.github/roadmap/` while
supporting helpers and benchmarks will reside in a new `src/roadmap/`
package and `src/benchmarks/` as appropriate.  All code will be minimal stub
utilities that are exercised by the tests included in this plan.

**Tech Stack:**
Markdown for documents, Python 3.14 with `pytest` for utility tests, and
standard libraries (`pathlib`, `json`).

---

### Task 1: Create vision statement template

**Step 1: Write failing test**
- File: `tests/test_vision_template.py`
- Code:
  ```python
  def test_vision_template_exists(tmp_path):
      from roadmap import vision
  
      # template function should return a non-empty string
      text = vision.get_template()
      assert isinstance(text, str) and "Vision" in text
  ```

**Step 2: Run test and watch failure**
- Command: `python -m pytest tests/test_vision_template.py -q`
- Expected failure: `ModuleNotFoundError` or `ImportError`.

**Step 3: Implement template stub**
- File: `src/roadmap/vision.py`
- Code:
  ```python
  def get_template():
      return "# Vision\n\n<describe project vision here>\n"
  ```

**Step 4: Run test and ensure it passes**
- Command: `python -m pytest tests/test_vision_template.py -q`
- Expected output: `1 passed`.

---

### Task 2: Milestone document generator

**Step 1: Failing test**
- File: `tests/test_milestone_generator.py`
- Code:
  ```python
  def test_generate_milestones(tmp_path):
      from roadmap import milestones
  
      out = tmp_path / "roadmap.md"
      milestones.create(out, ["Q1: start", "Q2: scale"])
      text = out.read_text()
      assert "Q1" in text and "Q2" in text
  ```

**Step 2: Run to observe failure.**

**Step 3: Implement stub in `src/roadmap/milestones.py`**
  ```python
  def create(path, items):
      with open(path, "w", encoding="utf-8") as f:
          f.write("# Technology Roadmap\n\n")
          for item in items:
              f.write(f"- {item}\n")
  ```

**Step 4: Run test until it passes.**

---

### Task 3: Prioritization framework skeleton

**Step 1:** Add `tests/test_prioritization.py` verifying existence of a
`score_feature` function that returns numeric value for a dict input.

**Step 2:** Execute and confirm failure.

**Step 3:** Implement `src/roadmap/prioritization.py` with simple RICE
formula stub:
  ```python
  def score_feature(attrs):
      return attrs.get("impact", 0) / max(attrs.get("effort", 1), 1)
  ```

**Step 4:** Re-run test until passing.

---

### Task 4: Innovation tracker initial API

**Step 1:** Write `tests/test_innovation_tracker.py` calling
`roadmap.innovation.record_experiment(name)` and asserting the name is
stored in a JSON file under `tmp_path`.

**Step 2:** Observe failure.

**Step 3:** Implement `src/roadmap/innovation.py` with minimal persistence:
  ```python
  import json, pathlib
  def record_experiment(name, db_path="experiments.json"):
      db = []
      p = pathlib.Path(db_path)
      if p.exists():
          db = json.loads(p.read_text())
      db.append({"name": name})
      p.write_text(json.dumps(db))
      return p
  ```

**Step 4:** Rerun test until it passes.

---

### Task 5: Benchmark scaffolding

**Step 1:** Create `tests/test_benchmarks.py` that imports
`benchmarks.simple` and executes a `run()` function returning
`{"latency": 0}`.

**Step 2:** Failure expected initially.

**Step 3:** Add `src/benchmarks/simple.py` with the stubbed run function.

**Step 4:** Run test to ensure success.

---

### Task 6: Document orchestration script

**Step 1:** Add `tests/test_roadmap_cli.py` verifying `roadmap.cli.generate()`
creates a file in a given directory.

**Step 2:** Run and confirm failure.

**Step 3:** Implement trivial CLI in `src/roadmap/cli.py` invoking the vision
and milestones modules and writing combined output.

**Step 4:** Rerun test until it passes.

---

After completing these six tasks, we will have a minimal set of planning
artifacts and helper utilities that satisfy the expanded roadmap design. 
Each component will be covered by a test, ensuring the project always
contains a starting point for vision, milestones, prioritization, innovation
logs, and performance benchmarks.

Once the plan is running green, commit the new files and push to the
repository.

## Implementation Status

All six roadmap tasks described above have already been carried out and the
corresponding code checked in:

* `src/roadmap/vision.py` provides a vision template; `tests/test_vision_template.py`
  passes.
* `src/roadmap/milestones.py` generates milestone documents; covered by
  `tests/test_milestone_generator.py`.
* `src/roadmap/prioritization.py` contains a simple scoring function; the
  prioritization test passes.
* `src/roadmap/innovation.py` records experiments to JSON and is exercised by
  `tests/test_innovation_tracker.py`.
* Benchmark scaffolding exists in `src/benchmarks/simple.py` and its test is
  green.
* A CLI driver `src/roadmap/cli.py` implements `generate()` and is verified
  by `tests/test_roadmap_cli.py`.

With these utilities and their tests in place, the future roadmap plan has
already produced a live set of artifacts and can be extended in later
phases.
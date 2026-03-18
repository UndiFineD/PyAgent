# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:** Implement the documentation & assets design by creating required
Markdown files, auto‑doc infrastructure, diagrams, and validation tests.

**Architecture:**
Documentation lives under `docs/` with subfolders for `api`,
`architecture`, `setup`, and `assets`.  Auto-generated reference docs are built
from source code in `src/` using Sphinx or MkDocs; configuration files live in
`docs/` as well.  Asset source files (Mermaid/PlantUML) are compiled to images
via a simple script in `scripts/` and checked into the repo.

**Tech Stack:**
- Python 3.11
- pytest for doc‑presence tests
- MkDocs (preferred) or Sphinx for API docs
- Mermaid/PlantUML for diagrams
- Conventional commit parser for changelog script

---

### Task 1: Presence tests for each doc type

**Step 1:** Add `tests/docs/test_docs_exist.py` with tests:
```python
import os

FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/setup.md",
    "docs/onboarding.md",
    "docs/tools.md",
    "docs/release_notes_template.md",
]

DIAGRAMS = [
    "docs/architecture/overview.mmd",
]


def test_document_files_exist():
    for f in FILES:
        assert os.path.isfile(f), f"{f} missing"


def test_diagram_sources_exist():
    for f in DIAGRAMS:
        assert os.path.isfile(f), f"{f} missing"
```

**Step 2:** Run and observe failure after creation of files.

### Task 2: Scaffold basic docs

**Step 1:** Create top‑level docs in repository root:
- `README.md` with project summary and quick-start snippet.
- `CONTRIBUTING.md` with checklist and link to testing commands.
- `docs/release_notes_template.md` containing Keep‑a‑Changelog skeleton.

**Step 2:** Add guide files under `docs/`:
- `setup.md` – environment setup instructions using `scripts/setup_structure.py` and README commands.
- `onboarding.md` – narrative walkthrough of repo layout, running tests, writing docs.

### Task 3: Initialize MkDocs API docs

**Step 1:** Add `docs/mkdocs.yml` with basic configuration:
```yaml
site_name: PyAgent
nav:
  - Home: index.md
  - API:
      - Reference: api/index.md

plugins:
  - search
  - mkdocstrings

extra:
  version: "0.1.0"
```

**Step 2:** Create `docs/api/index.md` containing
`::: PyAgent` placeholder for mkdocstrings.  Ensure `pyproject.toml` lists
`mkdocs` and `mkdocstrings` in dev dependencies.

**Step 3:** Add CI job or Makefile target to run `mkdocs build` and verify no
errors (optional for now).  A simple test may import mkdocs build function and
assert it completes.

### Task 4: Add diagram sources and build script

**Step 1:** Create `docs/architecture/overview.mmd` with a minimal Mermaid
component diagram referencing `src/core`, `src/tools`, `rust_core`.

**Step 2:** Add `scripts/compile_diagrams.py` that scans `docs/architecture` for
`.mmd` or `.puml` files and renders `.svg` via the Mermaid CLI or PlantUML jar.
Write a corresponding pytest `tests/docs/test_diagrams_compile.py` that runs the
script and asserts output files exist.

### Task 5: Changelog helper script

**Step 1:** Implement `scripts/changelog.py` which reads `git log --oneline
--no-merges --grep='^feat\|^fix'` and appends a formatted entry to
`docs/release_notes_template.md` or `RELEASE_NOTES.md`.

**Step 2:** Add tests `tests/docs/test_changelog_script.py` verifying the
script produces expected output given a dummy git log (use a temporary repo or
mock subprocess).

### Task 6: Documentation CI integration

- Add `ci-docs.yml` or update existing workflow to run the `tests/docs` suite
  along with building docs (`mkdocs build` and diagram compilation) and fail
  if any step errors.

### Task 7: Commit and push

Stage all new docs, scripts, and tests, then commit with message:

```
docs: add documentation scaffolding, tests, and assets pipeline
```

Push changes to `main`.

---

Completing these tasks will satisfy the documentation design: every artifact is
created, an automated process checks their presence/format, and the repository
is structured to generate reference material from code.  Afterward, authors can
expand each guide with more content and the pipeline will catch missing files.

Hand off to **superpower-execute** when you're ready to turn this plan into
actual code.
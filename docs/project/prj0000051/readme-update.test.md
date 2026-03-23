---
project: prj0000051
role: "@5test"
status: COMPLETE
date: 2026-03-23
handoff_to: "@6code"
---

# readme-update.test.md — Test Plan & Baseline for prj0000051

Structural tests for the updated `README.md`.  Written before `@6code` authors the file (TDD).

---

## Test File

`tests/structure/test_readme.py`

---

## Test Count

**44 test items** across 18 named test functions:

| # | Function | Parametrize | Items |
|---|---|---|---|
| 1 | `test_readme_exists` | — | 1 |
| 2 | `test_readme_h1` | — | 1 |
| 3 | `test_required_h2_headings` | 10 headings | 10 |
| 4 | `test_what_is_single_paragraph` | — | 1 |
| 5 | `test_key_numbers_present` | 6 tokens | 6 |
| 6 | `test_install_flags_documented` | 5 flags | 5 |
| 7 | `test_start_commands_documented` | 4 sub-commands | 4 |
| 8 | `test_project_history_count` | — | 1 |
| 9 | `test_future_roadmap_count` | — | 1 |
| 10 | `test_no_todo_fixme` | — | 1 |
| 11 | `test_powershell_fences` | — | 1 |
| 12 | `test_architecture_decisions_numbered` | — | 1 |
| 13 | `test_rust_keywords` | 3 keywords | 3 |
| 14 | `test_nebula_apps` | 3 apps | 3 |
| 15 | `test_backend_endpoints` | 2 endpoints | 2 |
| 16 | `test_install_ps1_mentioned` | — | 1 |
| 17 | `test_start_ps1_mentioned` | — | 1 |
| 18 | `test_line_length` | — | 1 |
| **Total** | | | **44** |

---

## Acceptance Criteria Coverage

| Plan AC | Test | Description |
|---|---|---|
| AC-01 | `test_readme_exists` | File exists with correct H1 |
| AC-02 | `test_readme_h1` | First non-empty line is `# PyAgent` |
| AC-04 | `test_required_h2_headings` (×10) | All 10 required H2 headings present |
| AC-05 | `test_what_is_single_paragraph` | No bullets or subheadings in What is PyAgent? |
| AC-06 | `test_architecture_decisions_numbered` | Numbered list items 1–8 in Architecture Decisions |
| AC-07 | `test_project_history_count` | Exactly 51 `prj0000NNN` occurrences |
| AC-09 | `test_future_roadmap_count` | Exactly 10 numbered items under Future Roadmap |
| AC-10 | `test_line_length` | No line exceeds 120 chars (soft / xfail) |
| AC-11 | `test_powershell_fences` | No ` ```bash ` fences |
| AC-12 | `test_key_numbers_present` (×6) | `666`, `51`, `41%`, `317`, `v4.0.0`, `VOYAGER` |
| AC-13 | `test_install_flags_documented` (×5) | `-SkipRust`, `-SkipWeb`, `-SkipDev`, `-CI`, `-Force` |
| AC-14 | `test_start_commands_documented` (×4) | `start`, `stop`, `restart`, `status` |
| AC-16 | `test_no_todo_fixme` | No TODO/FIXME/TBD stubs |
| — | `test_rust_keywords` (×3) | `Tokio`, `PyO3`, `maturin` |
| — | `test_nebula_apps` (×3) | `CodeBuilder`, `AgentChat`, `Conky` |
| — | `test_backend_endpoints` (×2) | `/health`, `/ws` |
| — | `test_install_ps1_mentioned` | `install.ps1` referenced |
| — | `test_start_ps1_mentioned` | `start.ps1` referenced |

---

## Sentinel Design

`_FILE_MISSING` is `True` when:
- `README.md` does not exist, **or**
- The first line is not exactly `# PyAgent`

This causes **all 43 content tests to skip** while `test_readme_exists` fails, giving
a clean TDD red/skip baseline.  When `@6code` writes the updated README (first line
`# PyAgent`), the sentinel flips, all 43 content tests run, and `test_readme_exists`
passes as well.

---

## Baseline Result

Run command:
```powershell
cd C:\Dev\PyAgent
& .venv\Scripts\Activate.ps1
python -m pytest tests/structure/test_readme.py -v
```

Result (branch `prj0000051-readme-update`, before README is updated):

```
collected 44 items

FAILED  tests/structure/test_readme.py::test_readme_exists
        AssertionError: Expected first line '# PyAgent', got: '# PyAgent Project'

SKIPPED tests/structure/test_readme.py::test_readme_h1
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## What is PyAgent?]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Quick Start]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## NebulaOS — The Frontend]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Backend]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Rust Core — The Zero-Loop Engine]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Architecture Decisions]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Project History]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Future Roadmap]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## Development Reference]
SKIPPED tests/structure/test_readme.py::test_required_h2_headings[## License]
... (32 more SKIPPED)

1 failed, 43 skipped in 6.37s
```

**Summary: 1 FAILED (`test_readme_exists`), 43 SKIPPED — baseline confirmed.**

---

## Pass Criteria for @6code

After the updated README is written, running the same command must produce:

- `test_readme_exists` — **PASS**
- All 43 content tests — **PASS** (or `xfail` for `test_line_length` if any line
  exceeds 120 chars, which is a soft warning, not a hard failure)
- **0 FAIL**

---

## Issues / Notes

None.  The sentinel design cleanly separates "file not yet written" from "file
written but failing checks".  No changes to `pytest.ini` or `conftest.py` were
required.

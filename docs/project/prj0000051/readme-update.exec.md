# prj0000051 — README Update — Exec Notes

## Validation results

| Check | Result |
|---|---|
| `test_readme_exists` | PASS |
| README structural tests (44 total) | 44/44 PASS |
| doc policy tests | 2/2 PASS (after fixing project.md and git.md) |
| Full test suite | 700 total — 698 passed, 2 skipped, 0 failed |

## Commands run

```powershell
python scripts/write_readme.py
python -m pytest tests/structure/test_readme.py -v
python -m pytest tests/ -q
```

## Issues resolved

1. `test_project_history_count` failed (63 != 51): Section range headers
   `### Foundation (prj0000001–prj0000010)` matched the `prj0000\d{3}` regex.
   Fixed by using plain group names and removing inline prj ID mentions.

2. `test_project_overviews_use_modern_template_or_carry_legacy_exception` failed:
   `readme-update.project.md` was missing `## Project Overview`, `**Goal:**`,
   `**In scope:**`, `**Out of scope:**`, `**Expected branch:**`, `**Scope boundary:**`.
   Fixed by rewriting to the full modern template format.

3. `test_git_summaries_use_modern_branch_plan_format_or_carry_legacy_exception` failed:
   `readme-update.git.md` was missing `## Branch Plan`, `**Expected branch:**`,
   `**Observed branch:**`, `**Project match:**`, `## Branch Validation`,
   `## Scope Validation`, `## Failure Disposition`, `## Lessons Learned`.
   Fixed by rewriting to the modern git.md template format.

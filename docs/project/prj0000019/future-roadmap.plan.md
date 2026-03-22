# future-roadmap — Think / Design / Plan / Test / Code / Exec / QL / Git

_Consolidated artifact for prj0000019._

## Think
`src/roadmap/cli.py` had `generate()` but no `main(argv)` — it could not be run from the command line. `vision.get_template()` returned a placeholder. Argparse with subcommands (`generate`, `vision`, `milestones`) is the idiomatic pattern used across the rest of the codebase.

## Design
CLI structure:
```
python -m src.roadmap generate --out <dir>
python -m src.roadmap vision
python -m src.roadmap milestones --out <file> [items...]
```

`generate()` now calls `outdir.mkdir(parents=True, exist_ok=True)` to create the output dir automatically.

## Plan
| # | Task | Done |
|---|------|------|
| 1 | Add `main(argv)` + `_build_parser()` to `cli.py` | ✅ |
| 2 | Add `if __name__ == "__main__"` guard to `cli.py` | ✅ |
| 3 | Enrich `vision.get_template()` with PyAgent-specific content | ✅ |
| 4 | Add 4 new tests to `test_roadmap_cli.py` | ✅ |
| 5 | Write 9 doc artifacts | ✅ |

## Test Results
`5 passed` ✅

## Code Notes
- `generate()` now creates the output directory automatically.
- `main(["vision"])` prints to stdout — covered by `capsys` fixture.
- No external dependencies added.

## Exec
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/test_roadmap_cli.py -v
# 5 passed ✅
```

## Security (QL)
No injection risks. `generate()` writes to a caller-supplied path — appropriate for internal use only. No user-controlled content written without sanitisation.

## Git
**Expected branch:** `prj0000019-future-roadmap`
**Observed branch:** `prj0000019-future-roadmap` ✅

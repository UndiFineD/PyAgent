# github-import — Git Notes

_Status: COMPLETE_
_Git: @9git | Updated: 2026-03-22_

## Branch Plan
**Expected branch:** `prj0000020-github-import`
**Observed branch:** `prj0000020-github-import`
**Project match:** ✅ YES

## Branch Validation
Branch `prj0000020-github-import` matches project identifier `prj0000020`. Branched from `main`. No naming violations.

## Scope Validation
- `src/github_app.py` ✅
- `src/importer/downloader.py` ✅
- `src/importer/config.py` ✅
- `tests/test_github_app.py` ✅
- `tests/test_importer_flow.py` ✅
- `docs/project/prj0000020/*.md` ✅

## Failure Disposition
If branch mismatch: STOP. Switch to `prj0000020-github-import` then re-validate.

## Lessons Learned
- HMAC webhook signature verification must be added in a follow-on sprint (documented in `github-import.ql.md`).
- Explicit `subprocess` arg lists (no `shell=True`) are required for all git invocations — prevents command injection.

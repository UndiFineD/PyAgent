# dev-tools-capabilities — Git Notes

_Status: COMPLETE_
_Git: @9git | Updated: 2026-03-22_

## Branch Plan

**Expected branch:** `prj0000014-dev-tools-capabilities`
**Observed branch:** `prj0000014-dev-tools-capabilities`
**Project match:** ✅ YES

## Branch Validation
- Branch created from `main`.
- All commits scoped to `src/tools/remote.py`, `src/tools/ssl_utils.py`, `src/tools/git_utils.py`, and `docs/project/prj0000014/`.
- No cross-project files modified.

## Scope Validation
Files touched:
- `src/tools/remote.py` ✅ in-scope
- `src/tools/ssl_utils.py` ✅ in-scope
- `src/tools/git_utils.py` ✅ in-scope
- `docs/project/prj0000014/*.md` ✅ in-scope

## Failure Disposition
If branch mismatch detected: STOP — do not commit. Switch to `prj0000014-dev-tools-capabilities` then re-validate.

## Lessons Learned
- Security fix (shell=True → explicit list) should always be paired with a test that asserts `shell` kwarg is falsy — prevents regression.
- TLS expiry check is only meaningful in integration tests, not unit tests. Keep unit tests monkeypatched.

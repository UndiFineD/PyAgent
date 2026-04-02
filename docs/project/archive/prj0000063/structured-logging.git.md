# structured-logging — Git Notes
_Owner: @9git | Status: DONE_

## Branch Plan

**Expected branch:** `prj0000063-structured-logging`
**Observed branch:** `prj0000063-structured-logging`
**Project match:** YES

## Branch Validation

Branch follows the `prjNNNNNNN-<short-name>` naming convention. ✅
Branch created from latest `main` after `git pull origin main`. ✅
All commits on this branch are scoped to prj0000063 files only. ✅

## Scope Validation

Changes confined to:
- `docs/project/prj0000063/` — 9 project artifact files
- `backend/logging_config.py` — new JSON logging module
- `backend/app.py` — CorrelationIdMiddleware + structured health log
- `backend/requirements.txt` — add python-json-logger>=2.0.0
- `tests/test_structured_logging.py` — 5 unit/integration tests
- `data/projects.json` — lane + pr update for prj0000063
- `docs/project/kanban.md` — prj0000063 moved to Review

No out-of-scope files modified. ✅

## Failure Disposition

All 5 `test_structured_logging.py` tests: PASS ✅
Pre-existing failures unrelated to this project:
- `test_projects_json_entry_count` — count mismatch (pre-existing)
- `test_kanban_total_rows` — count mismatch (pre-existing)
- `test_all_sarif_files_are_fresh` — stale SARIF (pre-existing)

## Commits

1. `docs(prj0000063): @1project — 9 artifacts, kanban update`
2. `feat(prj0000063): @6code — JSON structured logging + correlation ID middleware`
3. `test(prj0000063): @5test — 5 structured logging tests`
4. `docs(prj0000063): close — pr=N, kanban Review`

## Pull Request

- **PR Number:** 201
- **PR URL:** https://github.com/UndiFineD/PyAgent/pull/201
- **Base:** `main`
- **Head:** `prj0000063-structured-logging`
- **Title:** `feat: JSON structured logging with correlation IDs (prj0000063)`

## Lessons Learned

- `python-json-logger`'s `JsonFormatter` only emits `extra` fields that appear in
  the format string pattern. All custom fields (`correlation_id`, `endpoint`) must
  be listed in the format string.
- `BaseHTTPMiddleware` is already a transitive FastAPI/Starlette dependency — no
  new package required beyond `python-json-logger`.

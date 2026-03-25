# structured-logging — Plan
_Owner: @4plan | Status: DONE_

## Task Breakdown

| # | Task | Owner | Status |
|---|---|---|---|
| T-01 | Create `prj0000063` branch from `main` | @9git | DONE |
| T-02 | Create `docs/project/prj0000063/` with 9 artifacts | @1project | DONE |
| T-03 | Install `python-json-logger` and add to `backend/requirements.txt` | @6code | DONE |
| T-04 | Implement `backend/logging_config.py` | @6code | DONE |
| T-05 | Add `CorrelationIdMiddleware` and structured health log to `backend/app.py` | @6code | DONE |
| T-06 | Create `tests/test_structured_logging.py` (5 tests) | @5test | DONE |
| T-07 | Run `pytest tests/test_structured_logging.py` — all pass | @5test | DONE |
| T-08 | Run full suite `pytest tests/ -q` — no new failures | @5test | DONE |
| T-09 | Update `data/projects.json` — lane → Review, pr → N | @1project | DONE |
| T-10 | Commit in 3 scoped commits | @9git | DONE |
| T-11 | Push branch, open PR | @9git | DONE |
| T-12 | Add close commit (git.md + kanban Review) | @9git | DONE |
| T-13 | Return to `main` | @9git | DONE |

## Commit Strategy

1. `docs(prj0000063): @1project — 9 artifacts, kanban update`
2. `feat(prj0000063): @6code — JSON structured logging + correlation ID middleware`
3. `test(prj0000063): @5test — 5 structured logging tests`
4. `docs(prj0000063): close — pr=N, kanban Review` (close commit)

## Risk Register

| Risk | Mitigation |
|---|---|
| Existing tests break due to app import changes | Import `backend.app` lazily in tests; use `pytest-httpx` mock |
| Double-initialisation of logger | Guard `if logger.handlers: return logger` in `setup_logging` |
| python-json-logger API incompatibility | Pin `>=2.0.0`, use `jsonlogger.JsonFormatter` (stable class) |

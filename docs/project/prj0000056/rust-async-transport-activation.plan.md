# rust-async-transport-activation — Plan

_Owner: @4plan | Status: DONE | Updated: 2026-03-25_

## Task Breakdown

| # | Task | Agent | Status |
|---|---|---|---|
| 1 | Create branch `prj0000056-rust-async-transport-activation` | @9git | ✅ |
| 2 | Create `docs/project/prj0000056/` with 9 artifacts | @1project | ✅ |
| 3 | Implement `rust_core/src/async_transport.rs` | @6code | ✅ |
| 4 | Update `rust_core/src/lib.rs`: mod + register | @6code | ✅ |
| 5 | Attempt `cargo build` — verify compilation | @7exec | ✅ |
| 6 | Create `tests/test_async_transport.py` (5+ tests) | @5test | ✅ |
| 7 | Run `pytest tests/test_async_transport.py -v` | @7exec | ✅ |
| 8 | Run full `pytest tests/ -q` suite | @7exec | ✅ |
| 9 | Update `data/projects.json` | @1project | ✅ |
| 10 | Update `docs/project/kanban.md` | @1project | ✅ |
| 11 | Commit docs, code, tests in 3 separate commits | @9git | ✅ |
| 12 | Push branch, create PR | @9git | ✅ |
| 13 | Update git.md with PR number, move kanban to Review | @9git | ✅ |
| 14 | Final commit + push, checkout main | @9git | ✅ |

## Dependencies

- tokio already declared optional in `Cargo.toml` (no Cargo change needed)
- PyO3 wrapper must compile without `async-transport` feature
- Python tests must skip gracefully if `.pyd`/`.so` not present

## Success Criteria

- `cargo build` exits 0 (or known-skip if `maturin` not in CI)
- `pytest tests/test_async_transport.py` passes (all or all skipped)
- Full pytest suite shows no regressions
- PR open on GitHub

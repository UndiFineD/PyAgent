# automem-hybrid-search

**Project ID:** `prj0000079-automem-hybrid-search`

## Links

- Plan: `plan.md`
- Design: **MISSING** (`brainstorm.md`)

## Tasks

- [ ] `schema.sql` applies cleanly (`psql -f schema.sql`) on a fresh PG 16 DB
- [ ] All 7 index types present: B-tree, HNSW, GIN, GiST, SP-GiST (ltree), BRIN, Hash
- [ ] `AutoMemCore.hybrid_search()` returns scored results within 50 ms on 100k rows
- [ ] Benchmark component renders live charts for: read, write, sort, search, each by ≥3 methods
- [ ] CI passes (no import errors, no type errors blocking mypy partial check)

## Status

0 of 5 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\agents\research.rs`
  - `rust_core\src\agents\search.rs`
  - `rust_core\src\search.rs`
  - `rust_core\src\text\search.rs`
  - `rust_core\src\utils\search.rs`
  - `src\core\memory\AutoMemCore.py`
  - `tests\test_AutoMemCore.py`
  - `tests\test_research_packages.py`

## Missing design

Design file not found: `brainstorm.md`
# prj0000079 — automem-hybrid-search

## Overview

Implement the AutoMem 9-component hybrid memory search layer for PyAgent on a
**single PostgreSQL database** (no polyglot services). Every scoring dimension
maps to a native PostgreSQL capability:

| # | Component | Weight | PG mechanism |
|---|---|---|---|
| 1 | Vector | 25% | `pgvector` HNSW index |
| 2 | Graph | 25% | `Apache AGE` — openCypher graph |
| 3 | Temporal decay | 15% | `BRIN` + window functions |
| 4 | Keyword | 15% | `GIN` on `TEXT[]` keywords array |
| 5 | Lexical / full-text | 10% | `GIN` on `tsvector`, trigram `pg_trgm` |
| 6 | Importance | 5% | B-tree index on `importance FLOAT` |
| 7 | Confidence | 5% | B-tree index on `confidence FLOAT` |
| 8 | Hierarchy (parent-child) | structural | `LTREE` extension + GiST index |
| 9 | Recency / frequency | structural | B-tree on `last_accessed`, `access_count` |

The `LTREE` hierarchy (component 8) and recency (component 9) are structural
accelerators, not scored; they allow routing and pruning before scoring runs.

## Deliverables

| Path | What |
|---|---|
| `docs/project/prj0000079-automem-hybrid-search/postgres-setup.md` | PostgreSQL 16 install guide (Windows / Debian / Docker) |
| `src/core/memory/schema.sql` | Full DDL: tables, extensions, indexes, triggers, views |
| `src/core/memory/AutoMemCore.py` | 9-component scorer + CRUD operations |
| `src/core/memory/BenchmarkRunner.py` | Random-sample benchmark engine |
| `web/apps/AutoMemBenchmark.tsx` | Live benchmark dashboard (Recharts) |

## Branch Plan

- **Branch**: `prj0000079-automem-hybrid-search`
- **Base**: `main` at `bf1164781`
- **Scope boundary**: `src/core/memory/`, `docs/project/prj0000079-*/`, `web/apps/AutoMemBenchmark.tsx`
- **Must not touch**: other agents, other web apps, kanban lane transitions on a separate project branch

## Acceptance Criteria

- [ ] `schema.sql` applies cleanly (`psql -f schema.sql`) on a fresh PG 16 DB
- [ ] All 7 index types present: B-tree, HNSW, GIN, GiST, SP-GiST (ltree), BRIN, Hash
- [ ] `AutoMemCore.hybrid_search()` returns scored results within 50 ms on 100k rows
- [ ] Benchmark component renders live charts for: read, write, sort, search, each by ≥3 methods
- [ ] CI passes (no import errors, no type errors blocking mypy partial check)

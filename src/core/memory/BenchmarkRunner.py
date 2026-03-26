#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""BenchmarkRunner — measures AutoMem index performance across all 9 index types.

Populates the database with random sample memories and records latencies for:
    - WRITE  (INSERT via AutoMemCore.store)
    - READ   (single-key lookup: B-tree, Hash)
    - SORT   (ORDER BY indexed column: B-tree)
    - SEARCH (vector HNSW, full-text GIN, keyword GIN, LTREE subtree, BRIN)

Results are serialised as JSON so AutoMemBenchmark.tsx can poll them.
"""

from __future__ import annotations

import asyncio
import json
import math
import random
import string
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

try:
    import asyncpg  # type: ignore[import]
    _HAS_ASYNCPG = True
except ImportError:
    _HAS_ASYNCPG = False

# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------

@dataclass
class OperationResult:
    """Single benchmark measurement."""
    operation:  str          # 'write' | 'read' | 'sort' | 'search'
    method:     str          # 'btree' | 'hash' | 'hnsw' | 'gin_tsv' | …
    rows:       int          # table size at time of measurement
    latency_ms: float
    rows_returned: int = 0

@dataclass
class BenchmarkReport:
    """Full report returned to the frontend."""
    run_id:       str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    total_rows:   int = 0
    results:      list[OperationResult] = field(default_factory=list)
    errors:       list[str]             = field(default_factory=list)
    completed_at: Optional[str]         = None

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)


# ---------------------------------------------------------------------------
# Random data generators
# ---------------------------------------------------------------------------

WORD_POOL = [
    "agent", "memory", "task", "context", "query", "search", "result",
    "vector", "graph", "token", "session", "embedding", "latency", "index",
    "chunk", "score", "weight", "decay", "keyword", "cluster",
]

def _random_content(length: int = 120) -> str:
    words = random.choices(WORD_POOL, k=length // 6)  # noqa: S311
    return " ".join(words) + " " + "".join(
        random.choices(string.ascii_lowercase, k=10)  # noqa: S311
    )

def _random_embedding(dim: int = 1536) -> list[float]:
    """Unit-normalised random embedding."""
    v = [random.gauss(0, 1) for _ in range(dim)]
    mag = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / mag for x in v]

def _random_keywords(n: int = 4) -> list[str]:
    return random.sample(WORD_POOL, min(n, len(WORD_POOL)))

def _random_importance() -> float:
    return round(random.random(), 4)  # noqa: S311


# ---------------------------------------------------------------------------
# BenchmarkRunner
# ---------------------------------------------------------------------------

class BenchmarkRunner:
    """Runs a full benchmark sweep against the AutoMem PostgreSQL schema.

    Usage (async)::

        async with BenchmarkRunner(dsn, row_counts=[100, 1_000, 10_000]) as bench:
            report = await bench.run()
            print(report.to_json())
    """

    def __init__(
        self,
        dsn:        str,
        row_counts: Optional[list[int]] = None,
        embed_dim:  int = 1536,
    ) -> None:
        if not _HAS_ASYNCPG:
            raise ImportError("asyncpg required — pip install asyncpg pgvector")
        self._dsn        = dsn
        self._row_counts = row_counts or [100, 500, 1_000, 5_000]
        self._dim        = embed_dim
        self._pool: Any  = None
        self._report     = BenchmarkReport()

    async def __aenter__(self) -> "BenchmarkRunner":
        self._pool = await asyncpg.create_pool(self._dsn, min_size=2, max_size=8)
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._pool:
            await self._pool.close()

    # ------------------------------------------------------------------
    # WRITE — bulk insert with random data
    # ------------------------------------------------------------------

    async def _bench_writes(self, n: int) -> list[uuid.UUID]:
        inserted_ids: list[uuid.UUID] = []
        async with self._pool.acquire() as conn:
            # Ensure bench agent
            await conn.execute(
                "INSERT INTO automem_agents(agent_id,agent_name) "
                "VALUES('bench','Bench') ON CONFLICT DO NOTHING"
            )
            t0 = time.perf_counter()
            for _ in range(n):
                row = await conn.fetchrow(
                    """
                    INSERT INTO memories
                        (agent_id, content, embedding, keywords, importance, confidence)
                    VALUES
                        ($1, $2, $3::vector, $4, $5, $6)
                    RETURNING id
                    """,
                    "bench",
                    _random_content(),
                    f"[{','.join(str(x) for x in _random_embedding(self._dim))}]",
                    _random_keywords(),
                    _random_importance(),
                    round(random.random(), 4),  # noqa: S311
                )
                inserted_ids.append(row["id"])
            elapsed_ms = (time.perf_counter() - t0) * 1000

        self._report.results.append(OperationResult(
            operation="write",
            method="btree_insert",
            rows=n,
            latency_ms=round(elapsed_ms / n, 3),
            rows_returned=n,
        ))
        self._report.total_rows += n
        return inserted_ids

    # ------------------------------------------------------------------
    # READ — single-row by primary key  (B-tree UUID pk)
    # ------------------------------------------------------------------

    async def _bench_read_btree(self, sample_ids: list[uuid.UUID]) -> None:
        k = min(50, len(sample_ids))
        ids = random.sample(sample_ids, k)
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            for mid in ids:
                await conn.fetchrow("SELECT id,content FROM memories WHERE id=$1", mid)
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="read",
            method="btree_pk",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms / k, 3),
            rows_returned=k,
        ))

    # ------------------------------------------------------------------
    # READ — hash index equality
    # ------------------------------------------------------------------

    async def _bench_read_hash(self) -> None:
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            for _ in range(50):
                await conn.fetch(
                    "SELECT id FROM memories WHERE agent_id=$1 LIMIT 10",
                    "bench",
                )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="read",
            method="hash_agent_id",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms / 50, 3),
            rows_returned=10,
        ))

    # ------------------------------------------------------------------
    # SORT — B-tree ORDER BY
    # ------------------------------------------------------------------

    async def _bench_sort(self) -> None:
        queries = {
            "btree_importance_desc": (
                "SELECT id,importance FROM memories "
                "WHERE agent_id='bench' ORDER BY importance DESC LIMIT 20"
            ),
            "btree_created_desc": (
                "SELECT id,created_at FROM memories "
                "WHERE agent_id='bench' ORDER BY created_at DESC LIMIT 20"
            ),
            "btree_access_count": (
                "SELECT id,access_count FROM memories "
                "WHERE agent_id='bench' ORDER BY access_count DESC LIMIT 20"
            ),
        }
        async with self._pool.acquire() as conn:
            for method, sql in queries.items():
                t0 = time.perf_counter()
                rows = await conn.fetch(sql)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                self._report.results.append(OperationResult(
                    operation="sort",
                    method=method,
                    rows=self._report.total_rows,
                    latency_ms=round(elapsed_ms, 3),
                    rows_returned=len(rows),
                ))

    # ------------------------------------------------------------------
    # SEARCH — vector HNSW
    # ------------------------------------------------------------------

    async def _bench_search_hnsw(self) -> None:
        qv = _random_embedding(self._dim)
        qv_str = f"[{','.join(str(x) for x in qv)}]"
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            rows = await conn.fetch(
                """
                SELECT id, embedding <=> $1::vector AS dist
                FROM memories
                WHERE agent_id='bench'
                ORDER BY dist LIMIT 10
                """,
                qv_str,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="search",
            method="hnsw_vector",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # SEARCH — full-text GIN (tsvector)
    # ------------------------------------------------------------------

    async def _bench_search_gin_tsv(self) -> None:
        term = random.choice(WORD_POOL)  # noqa: S311
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            rows = await conn.fetch(
                """
                SELECT id, ts_rank_cd(tsv, plainto_tsquery('english',$1)) AS r
                FROM memories
                WHERE agent_id='bench'
                  AND tsv @@ plainto_tsquery('english',$1)
                ORDER BY r DESC LIMIT 10
                """,
                term,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="search",
            method="gin_fulltext",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # SEARCH — keyword GIN array
    # ------------------------------------------------------------------

    async def _bench_search_gin_keywords(self) -> None:
        kw = random.choice(WORD_POOL)  # noqa: S311
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            rows = await conn.fetch(
                """
                SELECT id FROM memories
                WHERE agent_id='bench'
                  AND keywords @> ARRAY[$1]
                LIMIT 10
                """,
                kw,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="search",
            method="gin_keywords",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # SEARCH — BRIN range scan
    # ------------------------------------------------------------------

    async def _bench_search_brin(self) -> None:
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            rows = await conn.fetch(
                """
                SELECT id FROM memories
                WHERE agent_id='bench'
                  AND created_at > NOW() - INTERVAL '7 days'
                LIMIT 20
                """,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="search",
            method="brin_timestamp",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # SEARCH — full sequential scan (baseline comparison)
    # ------------------------------------------------------------------

    async def _bench_search_seqscan(self) -> None:
        term = random.choice(WORD_POOL)  # noqa: S311
        async with self._pool.acquire() as conn:
            await conn.execute("SET enable_seqscan = on; SET enable_indexscan = off;")
            t0 = time.perf_counter()
            rows = await conn.fetch(
                "SELECT id FROM memories WHERE content ILIKE $1 LIMIT 10",
                f"%{term}%",
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
            await conn.execute("SET enable_indexscan = on;")
        self._report.results.append(OperationResult(
            operation="search",
            method="full_seqscan",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # SEARCH — LTREE subtree  (hierarchy / parent-child)
    # ------------------------------------------------------------------

    async def _bench_search_ltree(self) -> None:
        async with self._pool.acquire() as conn:
            root = await conn.fetchrow(
                "SELECT path FROM memories WHERE agent_id='bench' AND path IS NOT NULL LIMIT 1"
            )
            if root is None or root["path"] is None:
                return
            root_path = str(root["path"])
            # Find the top-level label (root.labelX)
            parts = root_path.split(".")
            search_path = ".".join(parts[:2]) if len(parts) > 1 else root_path
            t0 = time.perf_counter()
            rows = await conn.fetch(
                "SELECT id FROM memories WHERE path <@ $1::ltree LIMIT 20",
                search_path,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._report.results.append(OperationResult(
            operation="search",
            method="ltree_subtree",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        ))

    # ------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------

    async def _cleanup(self) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE agent_id='bench'")

    # ------------------------------------------------------------------
    # MAIN RUN
    # ------------------------------------------------------------------

    async def run(self, cleanup_after: bool = True) -> BenchmarkReport:
        """Execute the full benchmark sweep across all row-count tiers."""
        all_ids: list[uuid.UUID] = []

        for target_rows in self._row_counts:
            # Insert enough new rows to reach the tier
            current = len(all_ids)
            needed  = target_rows - current
            if needed > 0:
                new_ids = await self._bench_writes(needed)
                all_ids.extend(new_ids)

            # Read benchmarks
            await self._bench_read_btree(all_ids)
            await self._bench_read_hash()

            # Sort benchmarks
            await self._bench_sort()

            # Search benchmarks
            await self._bench_search_hnsw()
            await self._bench_search_gin_tsv()
            await self._bench_search_gin_keywords()
            await self._bench_search_brin()
            await self._bench_search_seqscan()
            await self._bench_search_ltree()

        import datetime as _dt
        self._report.completed_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

        if cleanup_after:
            await self._cleanup()

        return self._report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

async def _main() -> None:
    import sys
    dsn = sys.argv[1] if len(sys.argv) > 1 else "postgresql://postgres@localhost/automem"
    rows = [100, 500, 1_000] if len(sys.argv) < 3 else [int(x) for x in sys.argv[2:]]
    async with BenchmarkRunner(dsn, row_counts=rows) as bench:
        report = await bench.run(cleanup_after=False)
    print(report.to_json())

if __name__ == "__main__":
    asyncio.run(_main())

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
import datetime as _dt
import json
import math
import random
import string
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

asyncpg: Any = None
try:
    import asyncpg as _asyncpg  # type: ignore[import]

    asyncpg = _asyncpg
    _has_asyncpg = True
except ImportError:
    _has_asyncpg = False

# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------


def _metadata_factory() -> dict[str, Any]:
    """Return an empty metadata dictionary with explicit typing."""
    return {}


def _operation_results_factory() -> list["OperationResult"]:
    """Return an empty typed list for operation results."""
    return []


def _errors_factory() -> list[str]:
    """Return an empty typed list for report errors."""
    return []


@dataclass
class OperationResult:
    """Single benchmark measurement."""

    backend: str  # 'postgres' | 'memory'
    operation: str  # 'write' | 'read' | 'sort' | 'search'
    method: str  # 'btree' | 'hash' | 'hnsw' | 'gin_tsv' | …
    rows: int  # table size at time of measurement
    latency_ms: float
    rows_returned: int = 0
    status: str = "ok"  # 'ok' | 'fallback' | 'unavailable'
    metadata: dict[str, Any] = field(default_factory=_metadata_factory)


@dataclass
class BenchmarkReport:
    """Full report returned to the frontend."""

    run_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    total_rows: int = 0
    results: list[OperationResult] = field(default_factory=_operation_results_factory)
    errors: list[str] = field(default_factory=_errors_factory)
    completed_at: Optional[str] = None

    def to_json(self, indent: int = 2) -> str:
        """Serialize the benchmark report to JSON."""
        return json.dumps(asdict(self), indent=indent, default=str)


# ---------------------------------------------------------------------------
# Random data generators
# ---------------------------------------------------------------------------

WORD_POOL = [
    "agent",
    "memory",
    "task",
    "context",
    "query",
    "search",
    "result",
    "vector",
    "graph",
    "token",
    "session",
    "embedding",
    "latency",
    "index",
    "chunk",
    "score",
    "weight",
    "decay",
    "keyword",
    "cluster",
]


def _random_content(length: int = 120) -> str:
    """Generate random content text for memory entries."""
    words = random.choices(WORD_POOL, k=length // 6)  # noqa: S311
    return (
        " ".join(words)
        + " "
        + "".join(
            random.choices(string.ascii_lowercase, k=10)  # noqa: S311
        )
    )


def _random_embedding(dim: int = 1536) -> list[float]:
    """Unit-normalised random embedding."""
    v = [random.gauss(0, 1) for _ in range(dim)]
    mag = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / mag for x in v]


def _random_keywords(n: int = 4) -> list[str]:
    """Generate a random set of keywords for GIN array testing."""
    return random.sample(WORD_POOL, min(n, len(WORD_POOL)))


def _random_importance() -> float:
    """Generate a random importance value between 0 and 1."""
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
        dsn: str | None = None,
        row_counts: Optional[list[int]] = None,
        embed_dim: int = 1536,
        backend: str = "postgres",
    ) -> None:
        backend_mode = backend.strip().lower()
        if backend_mode not in {"postgres", "memory"}:
            raise ValueError(f"Unsupported benchmark backend: {backend}")
        if backend_mode == "postgres" and not _has_asyncpg:
            raise ImportError("asyncpg required — pip install asyncpg pgvector")
        self._backend = backend_mode
        self._dsn = dsn or "postgresql://postgres@localhost/automem"
        self._row_counts = row_counts or [100, 500, 1_000, 5_000]
        self._dim = embed_dim
        self._pool: Any = None
        self._report = BenchmarkReport()
        self._supports_vector = False
        self._supports_ltree = False
        self._mem_rows: list[dict[str, Any]] = []

    async def __aenter__(self) -> "BenchmarkRunner":
        """Enter the async context manager."""
        if self._backend == "memory":
            self._supports_vector = False
            self._supports_ltree = False
            return self

        self._pool = await asyncpg.create_pool(self._dsn, min_size=2, max_size=8)

        # Detect schema capabilities so the benchmark can run without optional extensions.
        async with self._pool.acquire() as conn:
            embedding_type = await conn.fetchval(
                """
                SELECT format_type(a.atttypid, a.atttypmod)
                FROM pg_attribute a
                JOIN pg_class c ON c.oid = a.attrelid
                WHERE c.relname = 'memories'
                  AND a.attname = 'embedding'
                  AND a.attnum > 0
                  AND NOT a.attisdropped
                """
            )
            path_type = await conn.fetchval(
                """
                SELECT format_type(a.atttypid, a.atttypmod)
                FROM pg_attribute a
                JOIN pg_class c ON c.oid = a.attrelid
                WHERE c.relname = 'memories'
                  AND a.attname = 'path'
                  AND a.attnum > 0
                  AND NOT a.attisdropped
                """
            )

        self._supports_vector = str(embedding_type).startswith("vector")
        self._supports_ltree = str(path_type) == "ltree"
        return self

    async def __aexit__(self, *_: Any) -> None:
        """Exit the async context manager."""
        if self._pool:
            await self._pool.close()

    def _append_result(
        self,
        *,
        operation: str,
        method: str,
        rows: int,
        latency_ms: float,
        rows_returned: int,
        status: str = "ok",
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Append one operation result with backend identity.

        Args:
            operation: Operation family.
            method: Method key used by the frontend.
            rows: Number of rows in scope.
            latency_ms: Measured latency in milliseconds.
            rows_returned: Result row count.
            status: Result status.
            metadata: Optional metadata for fallbacks/unavailable markers.

        """
        self._report.results.append(
            OperationResult(
                backend=self._backend,
                operation=operation,
                method=method,
                rows=rows,
                latency_ms=latency_ms,
                rows_returned=rows_returned,
                status=status,
                metadata=metadata or {},
            )
        )

    def _append_unavailable(self, operation: str, method: str, reason: str) -> None:
        """Record an explicit unavailable benchmark entry.

        Args:
            operation: Operation family.
            method: Benchmark method key.
            reason: Human-readable reason for unavailability.

        """
        self._append_result(
            operation=operation,
            method=method,
            rows=self._report.total_rows,
            latency_ms=0.0,
            rows_returned=0,
            status="unavailable",
            metadata={"reason": reason},
        )
        self._report.errors.append(f"{self._backend}:{method}: {reason}")

    # ------------------------------------------------------------------
    # WRITE — bulk insert with random data
    # ------------------------------------------------------------------

    async def _bench_writes(self, n: int) -> list[uuid.UUID]:
        """Benchmark bulk writes with random data."""
        inserted_ids: list[uuid.UUID] = []
        async with self._pool.acquire() as conn:
            # Ensure bench agent
            await conn.execute(
                "INSERT INTO automem_agents(agent_id,agent_name) VALUES('bench','Bench') ON CONFLICT DO NOTHING"
            )
            t0 = time.perf_counter()
            for _ in range(n):
                embedding = _random_embedding(self._dim)
                if self._supports_vector:
                    insert_sql = """
                        INSERT INTO memories
                            (agent_id, content, embedding, keywords, importance, confidence)
                        VALUES
                            ($1, $2, $3::vector, $4, $5, $6)
                        RETURNING id
                        """
                    embedding_value: Any = f"[{','.join(str(x) for x in embedding)}]"
                else:
                    insert_sql = """
                        INSERT INTO memories
                            (agent_id, content, embedding, keywords, importance, confidence)
                        VALUES
                            ($1, $2, $3, $4, $5, $6)
                        RETURNING id
                        """
                    embedding_value = embedding

                row = await conn.fetchrow(
                    insert_sql,
                    "bench",
                    _random_content(),
                    embedding_value,
                    _random_keywords(),
                    _random_importance(),
                    round(random.random(), 4),  # noqa: S311
                )
                inserted_ids.append(row["id"])
            elapsed_ms = (time.perf_counter() - t0) * 1000

        self._append_result(
            operation="write",
            method="btree_insert",
            rows=n,
            latency_ms=round(elapsed_ms / n, 3),
            rows_returned=n,
        )
        self._report.total_rows += n
        return inserted_ids

    # ------------------------------------------------------------------
    # READ — single-row by primary key  (B-tree UUID pk)
    # ------------------------------------------------------------------

    async def _bench_read_btree(self, sample_ids: list[uuid.UUID]) -> None:
        """Benchmark single-row reads by primary key (B-tree UUID pk)."""
        k = min(50, len(sample_ids))
        ids = random.sample(sample_ids, k)
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            for mid in ids:
                await conn.fetchrow("SELECT id,content FROM memories WHERE id=$1", mid)
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._append_result(
            operation="read",
            method="btree_pk",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms / k, 3),
            rows_returned=k,
        )

    # ------------------------------------------------------------------
    # READ — hash index equality
    # ------------------------------------------------------------------

    async def _bench_read_hash(self) -> None:
        """Benchmark hash index equality queries."""
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            for _ in range(50):
                await conn.fetch(
                    "SELECT id FROM memories WHERE agent_id=$1 LIMIT 10",
                    "bench",
                )
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._append_result(
            operation="read",
            method="hash_agent_id",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms / 50, 3),
            rows_returned=10,
        )

    # ------------------------------------------------------------------
    # SORT — B-tree ORDER BY
    # ------------------------------------------------------------------

    async def _bench_sort(self) -> None:
        """Benchmark B-tree ORDER BY queries."""
        queries = {
            "btree_importance_desc": (
                "SELECT id,importance FROM memories WHERE agent_id='bench' ORDER BY importance DESC LIMIT 20"
            ),
            "btree_created_desc": (
                "SELECT id,created_at FROM memories WHERE agent_id='bench' ORDER BY created_at DESC LIMIT 20"
            ),
            "btree_access_count": (
                "SELECT id,access_count FROM memories WHERE agent_id='bench' ORDER BY access_count DESC LIMIT 20"
            ),
        }
        async with self._pool.acquire() as conn:
            for method, sql in queries.items():
                t0 = time.perf_counter()
                rows = await conn.fetch(sql)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                self._append_result(
                    operation="sort",
                    method=method,
                    rows=self._report.total_rows,
                    latency_ms=round(elapsed_ms, 3),
                    rows_returned=len(rows),
                )

    # ------------------------------------------------------------------
    # SEARCH — vector HNSW
    # ------------------------------------------------------------------

    async def _bench_search_hnsw(self) -> None:
        """Benchmark HNSW vector similarity search."""
        qv = _random_embedding(self._dim)
        async with self._pool.acquire() as conn:
            t0 = time.perf_counter()
            metadata: dict[str, Any] = {}
            status = "ok"
            if self._supports_vector:
                qv_str = f"[{','.join(str(x) for x in qv)}]"
                rows = await conn.fetch(
                    """
                    SELECT id, embedding <=> $1::vector AS dist
                    FROM memories
                    WHERE agent_id='bench'
                    ORDER BY dist LIMIT 10
                    """,
                    qv_str,
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT id,
                           (
                               SELECT SUM(POWER(a - b, 2))
                               FROM unnest(embedding, $1::double precision[]) AS t(a, b)
                           ) AS dist
                    FROM memories
                    WHERE agent_id = 'bench'
                    ORDER BY dist ASC NULLS LAST
                    LIMIT 10
                    """,
                    qv,
                )
                status = "fallback"
                metadata = {
                    "fallback": "vector_l2_scan",
                    "reason": "pgvector extension unavailable; using array L2 scan",
                }
                self._report.errors.append("postgres:hnsw_vector: pgvector unavailable; used vector_l2_scan fallback")
            elapsed_ms = (time.perf_counter() - t0) * 1000
        self._append_result(
            operation="search",
            method="hnsw_vector",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
            status=status,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # SEARCH — full-text GIN (tsvector)
    # ------------------------------------------------------------------

    async def _bench_search_gin_tsv(self) -> None:
        """Benchmark full-text search using GIN index on tsvector."""
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
        self._append_result(
            operation="search",
            method="gin_fulltext",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        )

    # ------------------------------------------------------------------
    # SEARCH — keyword GIN array
    # ------------------------------------------------------------------

    async def _bench_search_gin_keywords(self) -> None:
        """Benchmark keyword search using GIN index on array."""
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
        self._append_result(
            operation="search",
            method="gin_keywords",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        )

    # ------------------------------------------------------------------
    # SEARCH — BRIN range scan
    # ------------------------------------------------------------------

    async def _bench_search_brin(self) -> None:
        """Benchmark range queries using BRIN index on timestamp."""
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
        self._append_result(
            operation="search",
            method="brin_timestamp",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        )

    # ------------------------------------------------------------------
    # SEARCH — full sequential scan (baseline comparison)
    # ------------------------------------------------------------------

    async def _bench_search_seqscan(self) -> None:
        """Benchmark full sequential scan (baseline comparison)."""
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
        self._append_result(
            operation="search",
            method="full_seqscan",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        )

    # ------------------------------------------------------------------
    # SEARCH — LTREE subtree  (hierarchy / parent-child)
    # ------------------------------------------------------------------

    async def _bench_search_ltree(self) -> None:
        """Benchmark LTREE subtree queries for hierarchy / parent-child relationships."""
        if not self._supports_ltree:
            self._append_unavailable("search", "ltree_subtree", "ltree type unavailable in schema")
            return

        async with self._pool.acquire() as conn:
            root = await conn.fetchrow("SELECT path FROM memories WHERE agent_id='bench' AND path IS NOT NULL LIMIT 1")
            if root is None or root["path"] is None:
                self._append_unavailable(
                    "search",
                    "ltree_subtree",
                    "no non-null path rows available for subtree query",
                )
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
        self._append_result(
            operation="search",
            method="ltree_subtree",
            rows=self._report.total_rows,
            latency_ms=round(elapsed_ms, 3),
            rows_returned=len(rows),
        )

    async def _run_memory(self, cleanup_after: bool) -> BenchmarkReport:
        """Execute benchmark tiers against an in-memory dataset."""
        for target_rows in self._row_counts:
            current = len(self._mem_rows)
            needed = target_rows - current
            if needed > 0:
                t0 = time.perf_counter()
                for _ in range(needed):
                    memory_id = uuid.uuid4()
                    content = _random_content()
                    self._mem_rows.append(
                        {
                            "id": memory_id,
                            "agent_id": "bench",
                            "content": content,
                            "embedding": _random_embedding(self._dim),
                            "keywords": _random_keywords(),
                            "importance": _random_importance(),
                            "confidence": round(random.random(), 4),  # noqa: S311
                            "created_at": _dt.datetime.now(_dt.timezone.utc),
                            "access_count": random.randint(0, 500),  # noqa: S311
                            "path": f"bench.root.{memory_id.hex[:8]}",
                        }
                    )
                elapsed_ms = (time.perf_counter() - t0) * 1000
                self._report.total_rows = len(self._mem_rows)
                self._append_result(
                    operation="write",
                    method="btree_insert",
                    rows=needed,
                    latency_ms=round(elapsed_ms / max(needed, 1), 3),
                    rows_returned=needed,
                )

            sample_count = min(50, len(self._mem_rows))
            sample_rows = random.sample(self._mem_rows, sample_count) if sample_count else []
            t0 = time.perf_counter()
            for row in sample_rows:
                _ = row["id"]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="read",
                method="btree_pk",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms / max(sample_count, 1), 3),
                rows_returned=sample_count,
            )

            t0 = time.perf_counter()
            hash_hits = [row for row in self._mem_rows if row["agent_id"] == "bench"][:10]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="read",
                method="hash_agent_id",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(hash_hits),
            )

            for method, key, reverse in (
                ("btree_importance_desc", "importance", True),
                ("btree_created_desc", "created_at", True),
                ("btree_access_count", "access_count", True),
            ):
                t0 = time.perf_counter()
                sorted_rows = sorted(
                    self._mem_rows,
                    key=lambda row, sort_key=key: row[sort_key],
                    reverse=reverse,
                )[:20]
                elapsed_ms = (time.perf_counter() - t0) * 1000
                self._append_result(
                    operation="sort",
                    method=method,
                    rows=len(self._mem_rows),
                    latency_ms=round(elapsed_ms, 3),
                    rows_returned=len(sorted_rows),
                )

            qv = _random_embedding(self._dim)
            t0 = time.perf_counter()
            vector_rows = sorted(
                self._mem_rows,
                key=lambda row, query=qv: sum((a - b) ** 2 for a, b in zip(row["embedding"], query, strict=False)),
            )[:10]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="search",
                method="hnsw_vector",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(vector_rows),
                status="fallback",
                metadata={
                    "fallback": "vector_l2_scan",
                    "reason": "in-memory backend uses exact L2 scan baseline",
                },
            )

            term = random.choice(WORD_POOL)  # noqa: S311
            t0 = time.perf_counter()
            fulltext_rows = [row for row in self._mem_rows if term in row["content"]][:10]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="search",
                method="gin_fulltext",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(fulltext_rows),
            )

            keyword = random.choice(WORD_POOL)  # noqa: S311
            t0 = time.perf_counter()
            keyword_rows = [row for row in self._mem_rows if keyword in row["keywords"]][:10]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="search",
                method="gin_keywords",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(keyword_rows),
            )

            cutoff = _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=7)
            t0 = time.perf_counter()
            recent_rows = [row for row in self._mem_rows if row["created_at"] > cutoff][:20]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="search",
                method="brin_timestamp",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(recent_rows),
            )

            like_term = random.choice(WORD_POOL)  # noqa: S311
            t0 = time.perf_counter()
            seq_rows = [row for row in self._mem_rows if like_term in row["content"]][:10]
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._append_result(
                operation="search",
                method="full_seqscan",
                rows=len(self._mem_rows),
                latency_ms=round(elapsed_ms, 3),
                rows_returned=len(seq_rows),
            )

            path_root = self._mem_rows[0]["path"] if self._mem_rows else ""
            if not path_root:
                self._append_unavailable("search", "ltree_subtree", "no path values available")
            else:
                parent = ".".join(str(path_root).split(".")[:2])
                t0 = time.perf_counter()
                subtree_rows = [row for row in self._mem_rows if str(row["path"]).startswith(parent)][:20]
                elapsed_ms = (time.perf_counter() - t0) * 1000
                self._append_result(
                    operation="search",
                    method="ltree_subtree",
                    rows=len(self._mem_rows),
                    latency_ms=round(elapsed_ms, 3),
                    rows_returned=len(subtree_rows),
                    status="fallback",
                    metadata={
                        "fallback": "path_prefix_scan",
                        "reason": "in-memory backend uses prefix scan baseline",
                    },
                )

        self._report.completed_at = _dt.datetime.now(_dt.timezone.utc).isoformat()
        if cleanup_after:
            self._mem_rows.clear()
        return self._report

    # ------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------

    async def _cleanup(self) -> None:
        """Cleanup benchmark data from the database."""
        async with self._pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE agent_id='bench'")

    # ------------------------------------------------------------------
    # MAIN RUN
    # ------------------------------------------------------------------

    async def run(self, cleanup_after: bool = True) -> BenchmarkReport:
        """Execute the full benchmark sweep across all row-count tiers."""
        if self._backend == "memory":
            return await self._run_memory(cleanup_after)

        all_ids: list[uuid.UUID] = []

        for target_rows in self._row_counts:
            # Insert enough new rows to reach the tier
            current = len(all_ids)
            needed = target_rows - current
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


def validate() -> bool:
    """Validate that the BenchmarkRunner module is correctly configured.

    Returns:
        True when the module can be imported and the runner class is accessible.

    """
    assert BenchmarkRunner is not None
    return True

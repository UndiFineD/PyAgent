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
"""PostgreSQL-backed AutoMem benchmark persistence and execution helpers."""

from __future__ import annotations

import datetime as dt
import json
import os
import uuid
from typing import Any

try:
    import asyncpg as _asyncpg  # type: ignore[import]
    asyncpg: Any = _asyncpg
except ImportError:  # pragma: no cover
    asyncpg = None  # type: ignore[assignment]


class AutoMemBenchmarkStore:
    """Persist and retrieve benchmark reports using PostgreSQL."""

    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = dsn or os.getenv("AUTOMEM_POSTGRES_DSN", "postgresql://postgres@localhost/automem")
        self._pool: Any = None

    @staticmethod
    def _decode_json_value(value: Any) -> Any:
        """Return decoded JSON for asyncpg json/jsonb values across codec modes."""
        if isinstance(value, str):
            return json.loads(value)
        return value

    @staticmethod
    def _is_tolerable_extension_error(exc: BaseException) -> bool:
        """Return whether extension creation failure can be tolerated.

        Tolerated failures cover optional-extension availability and permission
        constraints so benchmark preflight can report capability status explicitly.
        """
        if not isinstance(exc, Exception):
            return False

        sqlstate = getattr(exc, "sqlstate", None)
        if sqlstate in {"0A000", "42501", "42704", "58P01"}:
            return True

        return exc.__class__.__name__ in {
            "FeatureNotSupportedError",
            "InsufficientPrivilegeError",
            "UndefinedFileError",
            "UndefinedObjectError",
        }

    async def _ensure_pool(self) -> Any:
        if asyncpg is None:
            raise RuntimeError("asyncpg is required for AutoMem benchmark persistence")
        if self._pool is None:
            create_pool = asyncpg.create_pool
            self._pool = await create_pool(self._dsn, min_size=1, max_size=4)
            await self._ensure_schema()
        return self._pool

    async def _ensure_schema(self) -> None:
        assert self._pool is not None  # noqa: S101
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS automem_benchmark_runs (
                    run_id TEXT PRIMARY KEY,
                    total_rows INTEGER NOT NULL,
                    completed_at TIMESTAMPTZ NULL,
                    payload JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS automem_kv (
                    key TEXT PRIMARY KEY,
                    value JSONB NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_automem_benchmark_runs_created_at
                ON automem_benchmark_runs(created_at DESC)
                """
            )

    async def _bootstrap_minimal_benchmark_schema(self) -> None:
        """Create minimal tables/extensions required by BenchmarkRunner.

        This bootstrap is intentionally minimal and only targets the relations
        needed for benchmark execution in development environments.
        """
        assert self._pool is not None  # noqa: S101
        async with self._pool.acquire() as conn:
            # Best-effort extension setup; failures are tolerated and surfaced by preflight.
            for extension in ("pgcrypto", "vector", "ltree"):
                try:
                    await conn.execute(f"CREATE EXTENSION IF NOT EXISTS {extension}")
                except Exception as exc:
                    if not self._is_tolerable_extension_error(exc):
                        raise
                    # Continue and let preflight produce actionable diagnostics.
                    continue

            has_vector = bool(
                await conn.fetchval("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'vector')")
            )
            has_ltree = bool(
                await conn.fetchval("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ltree')")
            )

            has_gen_random_uuid = bool(await conn.fetchval("SELECT to_regprocedure('gen_random_uuid()') IS NOT NULL"))
            uuid_default_expr: str
            if has_gen_random_uuid:
                uuid_default_expr = "gen_random_uuid()"
            else:
                # Fallback for environments where pgcrypto is unavailable.
                try:
                    await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
                except Exception as exc:
                    if not self._is_tolerable_extension_error(exc):
                        raise
                has_uuid_generate_v4 = bool(
                    await conn.fetchval("SELECT to_regprocedure('uuid_generate_v4()') IS NOT NULL")
                )
                if not has_uuid_generate_v4:
                    raise RuntimeError(
                        "Unable to bootstrap benchmark schema: neither gen_random_uuid() nor "
                        "uuid_generate_v4() is available in this PostgreSQL instance"
                    )
                uuid_default_expr = "uuid_generate_v4()"

            embedding_column = (
                "embedding vector(1536) NOT NULL"
                if has_vector
                else "embedding DOUBLE PRECISION[] NOT NULL"
            )
            path_column = "path ltree NULL" if has_ltree else "path TEXT NULL"

            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS automem_agents (
                    agent_id TEXT PRIMARY KEY,
                    agent_name TEXT NOT NULL
                )
                """
            )

            await conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS memories (
                    id UUID PRIMARY KEY DEFAULT {uuid_default_expr},
                    agent_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    {embedding_column},
                    keywords TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
                    importance DOUBLE PRECISION NOT NULL DEFAULT 0.0,
                    confidence DOUBLE PRECISION NOT NULL DEFAULT 0.0,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    access_count INTEGER NOT NULL DEFAULT 0,
                    tsv tsvector GENERATED ALWAYS AS (
                        to_tsvector('english', coalesce(content, ''))
                    ) STORED,
                    {path_column},
                    CONSTRAINT fk_memories_agent_id
                        FOREIGN KEY (agent_id) REFERENCES automem_agents(agent_id)
                )
                """
            )

            # Minimal benchmark-supporting indexes.
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_agent_id
                ON memories(agent_id)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_importance_desc
                ON memories(importance DESC)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_created_desc
                ON memories(created_at DESC)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_access_count_desc
                ON memories(access_count DESC)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_tsv_gin
                ON memories USING GIN(tsv)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_keywords_gin
                ON memories USING GIN(keywords)
                """
            )
            await conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_mem_created_brin
                ON memories USING BRIN(created_at)
                """
            )

    async def _benchmark_schema_missing_objects(self) -> list[str]:
        """Return missing required benchmark schema objects."""
        assert self._pool is not None  # noqa: S101
        required_tables = ("automem_agents", "memories")
        required_columns = {
            "memories": (
                "id",
                "agent_id",
                "content",
                "embedding",
                "keywords",
                "importance",
                "confidence",
                "created_at",
                "access_count",
                "tsv",
                "path",
            )
        }
        missing: list[str] = []

        async with self._pool.acquire() as conn:
            for table in required_tables:
                exists = await conn.fetchval("SELECT to_regclass($1)", table)
                if exists is None:
                    missing.append(f"table:{table}")

            if "table:memories" not in missing:
                present_cols = await conn.fetch(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = current_schema()
                      AND table_name = 'memories'
                    """
                )
                present = {str(row["column_name"]) for row in present_cols}
                for column in required_columns["memories"]:
                    if column not in present:
                        missing.append(f"column:memories.{column}")

            # Type checks for vector and tsv columns to avoid opaque runtime errors.
            if "table:memories" not in missing:
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
                embedding_type_str = str(embedding_type) if embedding_type is not None else ""
                if not (embedding_type_str.startswith("vector") or embedding_type_str == "double precision[]"):
                    missing.append("type:memories.embedding(vector|double precision[])")

                tsv_type = await conn.fetchval(
                    """
                    SELECT format_type(a.atttypid, a.atttypmod)
                    FROM pg_attribute a
                    JOIN pg_class c ON c.oid = a.attrelid
                    WHERE c.relname = 'memories'
                      AND a.attname = 'tsv'
                      AND a.attnum > 0
                      AND NOT a.attisdropped
                    """
                )
                if tsv_type is None or str(tsv_type) != "tsvector":
                    missing.append("type:memories.tsv(tsvector)")

        return missing

    async def save_report(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Persist one benchmark payload and update the latest-report KV key."""
        pool = await self._ensure_pool()
        run_id = str(payload.get("run_id", ""))
        if not run_id:
            raise RuntimeError("Benchmark payload missing run_id")

        total_rows = int(payload.get("total_rows", 0))
        completed_at = payload.get("completed_at")
        if isinstance(completed_at, str) and completed_at:
            normalised = completed_at.replace("Z", "+00:00")
            completed_at = dt.datetime.fromisoformat(normalised)

        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO automem_benchmark_runs(run_id, total_rows, completed_at, payload)
                VALUES($1, $2, $3, $4::jsonb)
                ON CONFLICT (run_id)
                DO UPDATE SET
                    total_rows = EXCLUDED.total_rows,
                    completed_at = EXCLUDED.completed_at,
                    payload = EXCLUDED.payload
                """,
                run_id,
                total_rows,
                completed_at,
                json.dumps(payload),
            )
            await conn.execute(
                """
                INSERT INTO automem_kv(key, value, updated_at)
                VALUES('benchmark_latest', $1::jsonb, NOW())
                ON CONFLICT (key)
                DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
                """,
                json.dumps(payload),
            )
        return payload

    async def latest_report(self) -> dict[str, Any] | None:
        """Return latest report from KV cache, falling back to runs table."""
        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            kv_row = await conn.fetchrow("SELECT value FROM automem_kv WHERE key='benchmark_latest'")
            if kv_row is not None and kv_row["value"] is not None:
                value = self._decode_json_value(kv_row["value"])
                if isinstance(value, dict):
                    return value
                raise RuntimeError("Invalid benchmark_latest payload shape in automem_kv")

            run_row = await conn.fetchrow(
                """
                SELECT payload
                FROM automem_benchmark_runs
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            if run_row is None:
                return None
            value = self._decode_json_value(run_row["payload"])
            if isinstance(value, dict):
                return value
            raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")

    async def get_run(self, run_id: str) -> dict[str, Any] | None:
        """Return one persisted benchmark run by run_id."""
        run_id = run_id.strip()
        if not run_id:
            raise ValueError("run_id must not be blank")

        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT payload
                FROM automem_benchmark_runs
                WHERE run_id = $1
                """,
                run_id,
            )
            if row is None:
                return None
            value = self._decode_json_value(row["payload"])
            if isinstance(value, dict):
                return value
            raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")

    async def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        """Return most recent benchmark runs (newest first)."""
        safe_limit = max(1, min(int(limit), 200))
        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT payload
                FROM automem_benchmark_runs
                ORDER BY created_at DESC
                LIMIT $1
                """,
                safe_limit,
            )
            result: list[dict[str, Any]] = []
            for row in rows:
                value = self._decode_json_value(row["payload"])
                if isinstance(value, dict):
                    result.append(value)
                else:
                    raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")
            return result

    async def kv_get(self, key: str) -> Any | None:
        """Read a value from automem_kv by key."""
        key = key.strip()
        if not key:
            raise ValueError("key must not be blank")

        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT value
                FROM automem_kv
                WHERE key = $1
                """,
                key,
            )
            if row is None:
                return None
            return self._decode_json_value(row["value"])

    async def kv_set(self, key: str, value: Any) -> Any:
        """Upsert a JSON-serialisable value in automem_kv."""
        key = key.strip()
        if not key:
            raise ValueError("key must not be blank")

        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO automem_kv(key, value, updated_at)
                VALUES($1, $2::jsonb, NOW())
                ON CONFLICT (key)
                DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
                """,
                key,
                json.dumps(value),
            )
        return value

    async def kv_delete(self, key: str) -> bool:
        """Delete a key from automem_kv and report whether it existed."""
        key = key.strip()
        if not key:
            raise ValueError("key must not be blank")

        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            status = await conn.execute("DELETE FROM automem_kv WHERE key = $1", key)
        return status.endswith("1")

    async def run_benchmark(
        self,
        row_counts: list[int] | None = None,
        *,
        backends: list[str] | None = None,
        bootstrap_schema: bool = False,
    ) -> dict[str, Any]:
        """Execute selected benchmark backends and persist one merged report.

        Args:
            row_counts: Optional row-count tiers for the benchmark runner.
            backends: Optional backend selection. Defaults to postgres + memory.
            bootstrap_schema: When True, attempt creating the minimal benchmark
                schema before validation.

        Raises:
            RuntimeError: If no selected backend completed successfully.

        """
        rows = row_counts or [100, 500, 1_000]
        requested_backends = backends or ["postgres", "memory"]
        selected_backends = [backend.strip().lower() for backend in requested_backends if backend.strip()]
        if not selected_backends:
            selected_backends = ["postgres", "memory"]

        allowed_backends = {"postgres", "memory"}
        invalid_backends = sorted(set(selected_backends) - allowed_backends)
        if invalid_backends:
            invalid = ", ".join(invalid_backends)
            raise ValueError(f"Unsupported benchmark backends: {invalid}")

        from src.core.memory.BenchmarkRunner import BenchmarkRunner

        backend_payloads: list[dict[str, Any]] = []
        backend_errors: list[str] = []

        if "postgres" in selected_backends:
            try:
                await self._ensure_pool()
                if bootstrap_schema:
                    await self._bootstrap_minimal_benchmark_schema()

                missing = await self._benchmark_schema_missing_objects()
                if missing:
                    detail = ", ".join(missing)
                    raise RuntimeError(
                        "Benchmark schema is incomplete. Missing: "
                        f"{detail}. "
                        "Run with bootstrap_schema=true or apply canonical AutoMem migrations."
                    )

                async with BenchmarkRunner(self._dsn, row_counts=rows, backend="postgres") as runner:
                    postgres_report = await runner.run(cleanup_after=True)
                backend_payloads.append(json.loads(postgres_report.to_json(indent=0)))
            except (ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
                backend_errors.append(f"postgres: {exc}")

        if "memory" in selected_backends:
            try:
                async with BenchmarkRunner(None, row_counts=rows, backend="memory") as runner:
                    memory_report = await runner.run(cleanup_after=True)
                backend_payloads.append(json.loads(memory_report.to_json(indent=0)))
            except (ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
                backend_errors.append(f"memory: {exc}")

        if not backend_payloads:
            raise RuntimeError("Benchmark run failed for all selected backends: " + "; ".join(backend_errors))

        merged_results: list[dict[str, Any]] = []
        merged_errors: list[str] = []
        max_total_rows = 0
        latest_completed_at = dt.datetime.now(dt.timezone.utc).isoformat()

        for payload in backend_payloads:
            merged_results.extend(payload.get("results", []))
            merged_errors.extend(payload.get("errors", []))
            max_total_rows = max(max_total_rows, int(payload.get("total_rows", 0)))
            completed_at = payload.get("completed_at")
            if isinstance(completed_at, str) and completed_at:
                latest_completed_at = completed_at

        merged_errors.extend(backend_errors)
        merged_payload: dict[str, Any] = {
            "run_id": str(uuid.uuid4())[:8],
            "total_rows": max_total_rows,
            "results": merged_results,
            "errors": merged_errors,
            "completed_at": latest_completed_at,
            "backends": selected_backends,
        }
        return await self.save_report(merged_payload)


automem_benchmark_store = AutoMemBenchmarkStore()

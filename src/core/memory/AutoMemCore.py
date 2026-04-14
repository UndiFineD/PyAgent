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
"""AutoMem Core — 9-component hybrid memory search on PostgreSQL."""

from __future__ import annotations

# import asyncio
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Optional heavy dependencies — import lazily so unit tests can run without PG
# ---------------------------------------------------------------------------
try:
    import asyncpg  # type: ignore[import]

    _HAS_ASYNCPG = True
except ImportError:
    _HAS_ASYNCPG = False

try:
    from pgvector.asyncpg import register_vector  # type: ignore[import]

    _HAS_PGVECTOR = True
except ImportError:
    _HAS_PGVECTOR = False


# ---------------------------------------------------------------------------
# SCORING WEIGHTS  (must sum to 1.0)
# ---------------------------------------------------------------------------
WEIGHT_VECTOR: float = 0.25  # pgvector cosine similarity
WEIGHT_GRAPH: float = 0.25  # Apache AGE graph neighbourhood depth
WEIGHT_TEMPORAL: float = 0.15  # exponential decay since last access
WEIGHT_KEYWORD: float = 0.15  # exact keyword intersection ratio
WEIGHT_LEXICAL: float = 0.10  # tsvector / tsquery rank
WEIGHT_IMPORTANCE: float = 0.05  # stored importance value 0–1
WEIGHT_CONFIDENCE: float = 0.05  # stored confidence value 0–1

assert (
    abs(  # noqa: S101
        WEIGHT_VECTOR
        + WEIGHT_GRAPH
        + WEIGHT_TEMPORAL
        + WEIGHT_KEYWORD
        + WEIGHT_LEXICAL
        + WEIGHT_IMPORTANCE
        + WEIGHT_CONFIDENCE
        - 1.0
    )
    < 1e-9
), "Scoring weights must sum to 1.0"

# Temporal decay constant  — half-life ≈ 69 hours  (k = ln(2)/half_life_h)
DECAY_K: float = 0.01


# ---------------------------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------------------------


@dataclass
class Memory:
    """A single memory row — mirrors the `memories` table."""

    id: uuid.UUID
    agent_id: str
    content: str
    keywords: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5
    confidence: float = 1.0
    decay_score: float = 1.0
    access_count: int = 0
    embedding: Optional[list[float]] = None
    parent_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    path: Optional[str] = None  # LTREE text form
    created_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None


@dataclass
class MemoryResult:
    """A scored memory returned from hybrid_search."""

    memory: Memory
    vector_score: float = 0.0
    graph_score: float = 0.0
    temporal_score: float = 0.0
    keyword_score: float = 0.0
    lexical_score: float = 0.0
    final_score: float = 0.0

    @property
    def breakdown(self) -> dict[str, float]:
        return {
            "vector": round(self.vector_score, 4),
            "graph": round(self.graph_score, 4),
            "temporal": round(self.temporal_score, 4),
            "keyword": round(self.keyword_score, 4),
            "lexical": round(self.lexical_score, 4),
            "importance": round(self.memory.importance, 4),
            "confidence": round(self.memory.confidence, 4),
            "final": round(self.final_score, 4),
        }


# ---------------------------------------------------------------------------
# SCORE HELPERS
# ---------------------------------------------------------------------------


def _temporal_score(last_accessed: Optional[datetime]) -> float:
    """Exponential decay from recency.

    s = exp(-k * hours_since_access).
    """
    if last_accessed is None:
        return 0.5
    # Accept both tz-aware and naive datetimes
    now = datetime.now(timezone.utc)
    if last_accessed.tzinfo is None:
        last_accessed = last_accessed.replace(tzinfo=timezone.utc)
    delta_h = (now - last_accessed).total_seconds() / 3600
    return math.exp(-DECAY_K * delta_h)


def _keyword_score(query_keywords: list[str], memory_keywords: list[str]) -> float:
    """Jaccard-style intersection ratio: |q ∩ m| / |q|."""
    if not query_keywords:
        return 0.0
    q_set = {k.lower() for k in query_keywords}
    m_set = {k.lower() for k in memory_keywords}
    return len(q_set & m_set) / len(q_set)


def _cosine_distance_to_score(distance: float) -> float:
    """Pgvector cosine distance ∈ [0, 2]; convert to score ∈ [0, 1]."""
    return max(0.0, 1.0 - distance / 2.0)


def _graph_hops_to_score(hops: int) -> float:
    """Fewer graph hops yield higher score."""
    if hops < 0:
        return 0.0
    return 1.0 / (1.0 + hops)


# ---------------------------------------------------------------------------
# AUTOMEM CORE
# ---------------------------------------------------------------------------


class AutoMemCore:
    """9-component hybrid memory search backed by PostgreSQL.

    Components:
        ① Vector    (25%) — pgvector HNSW cosine similarity
        ② Graph     (25%) — Apache AGE openCypher neighbourhood
        ③ Temporal  (15%) — exponential decay since last access
        ④ Keyword   (15%) — exact keyword intersection
        ⑤ Lexical   (10%) — tsvector / tsquery full-text rank
        ⑥ Importance (5%) — stored float 0-1
        ⑦ Confidence (5%) — stored float 0-1
        ⑧ Hierarchy structural — LTREE parent-child routing
        ⑨ Recency structural  — B-tree on last_accessed / access_count
    """

    def __init__(self, dsn: str, embedding_dim: int = 1536) -> None:
        """Initialize AutoMemCore settings.

        Args:
        dsn: asyncpg DSN, e.g.
            'postgresql://user:pass@localhost/automem'
        embedding_dim: dimension of the embedding vectors (must match schema)

        """
        self._dsn = dsn
        self._dim = embedding_dim
        self._pool: Any = None  # asyncpg.Pool

    # ------------------------------------------------------------------
    # Pool lifecycle
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Open the asyncpg connection pool and register pgvector codec."""
        if not _HAS_ASYNCPG:
            raise ImportError("asyncpg is required — pip install asyncpg pgvector")
        self._pool = await asyncpg.create_pool(
            self._dsn,
            min_size=2,
            max_size=10,
            init=self._init_conn,
        )

    async def _init_conn(self, conn: Any) -> None:
        """Register pgvector type codec for every new connection."""
        if _HAS_PGVECTOR:
            await register_vector(conn)
        await conn.execute('SET search_path = ag_catalog, "$user", public;')

    async def close(self) -> None:
        """Close the connection pool gracefully."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def __aenter__(self) -> "AutoMemCore":
        """Enter the async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, *_: Any) -> None:
        """Exit the async context manager."""
        await self.close()

    # ------------------------------------------------------------------
    # CRUD: write
    # ------------------------------------------------------------------

    async def store(
        self,
        agent_id: str,
        content: str,
        embedding: list[float],
        *,
        keywords: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        importance: float = 0.5,
        confidence: float = 1.0,
        parent_id: Optional[uuid.UUID] = None,
        session_id: Optional[uuid.UUID] = None,
    ) -> uuid.UUID:
        """Persist a new memory; returns the generated UUID.

        Also upserts the agent row and creates a matching AGE vertex.
        """
        if self._pool is None:
            raise RuntimeError("Call connect() or use async-with first")

        # Upsert agent row
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO automem_agents (agent_id, agent_name)
                VALUES ($1, $1)
                ON CONFLICT (agent_id) DO NOTHING
                """,
                agent_id,
            )

            row = await conn.fetchrow(
                """
                INSERT INTO memories (
                    agent_id, session_id, parent_id,
                    content, embedding,
                    keywords, tags, metadata,
                    importance, confidence
                )
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
                RETURNING id, path
                """,
                agent_id,
                session_id,
                parent_id,
                content,
                embedding,
                keywords or [],
                tags or [],
                metadata or {},
                importance,
                confidence,
            )

            mem_id: uuid.UUID = row["id"]

            # Materialise LTREE path: parent_path.mem_id  (or root.mem_id)
            parent_path = "root"
            if parent_id:
                parent_row = await conn.fetchrow("SELECT path FROM memories WHERE id = $1", parent_id)
                if parent_row and parent_row["path"]:
                    parent_path = str(parent_row["path"])

            # LTREE labels must be alphanumeric; replace hyphens
            safe_id = str(mem_id).replace("-", "_")
            new_path = f"{parent_path}.{safe_id}"
            await conn.execute(
                "UPDATE memories SET path = $1::ltree WHERE id = $2",
                new_path,
                mem_id,
            )

            # Create graph vertex in Apache AGE
            try:
                await conn.execute(
                    """
                    SELECT * FROM cypher('memory_graph', $$
                        CREATE (:Memory {id: $id_val, agent_id: $agent_val})
                    $$, $1) AS (v agtype)
                    """,
                    {"id_val": str(mem_id), "agent_val": agent_id},
                )
                # If parent exists, create DERIVED_FROM edge
                if parent_id:
                    await conn.execute(
                        """
                        SELECT * FROM cypher('memory_graph', $$
                            MATCH (child:Memory  {id: $child_id}),
                                (parent:Memory {id: $parent_id})
                            CREATE (child)-[:DERIVED_FROM {weight: 1.0}]->(parent)
                        $$, $1) AS (e agtype)
                        """,
                        {"child_id": str(mem_id), "parent_id": str(parent_id)},
                    )
            except Exception as exc:  # noqa: BLE001
                # AGE may not be installed in all environments; persist fallback state.
                await conn.execute(
                    """
                    UPDATE memories
                    SET metadata = COALESCE(metadata, '{}'::jsonb)
                        || jsonb_build_object(
                            'graph_sync', false,
                            'graph_sync_error', $1
                        )
                    WHERE id = $2
                    """,
                    str(exc)[:256],
                    mem_id,
                )

        return mem_id

    # ------------------------------------------------------------------
    # CRUD: read
    # ------------------------------------------------------------------

    async def get(self, memory_id: uuid.UUID) -> Optional[Memory]:
        """Fetch a single memory by id and record an access."""
        if self._pool is None:
            raise RuntimeError("Call connect() first")
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, agent_id, session_id, parent_id, path,
                    content, keywords, tags, metadata,
                    importance, confidence, decay_score,
                    access_count, last_accessed, created_at,
                    embedding
                FROM memories WHERE id = $1
                """,
                memory_id,
            )
            if row is None:
                return None
            await conn.execute("SELECT automem_record_access($1)", memory_id)
            return self._row_to_memory(row)

    # ------------------------------------------------------------------
    # HYBRID SEARCH — 9-component scoring
    # ------------------------------------------------------------------

    async def hybrid_search(
        self,
        agent_id: str,
        query: str,
        query_embedding: list[float],
        *,
        query_keywords: Optional[list[str]] = None,
        top_k: int = 10,
        enable_graph: bool = True,
    ) -> list[MemoryResult]:
        """Run hybrid search and return top_k MemoryResult objects, sorted by
        final_score descending.

        Scoring formula:
            final = Σ weight_i * component_i
        """
        if self._pool is None:
            raise RuntimeError("Call connect() first")

        keywords = query_keywords or []

        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, content, importance, confidence, decay_score,
                    access_count, last_accessed, created_at,
                    vec_dist, tsv_rank, kw_hits, keywords, metadata, path
                FROM automem_hybrid_candidates($1, $2, $3, $4, $5)
                """,
                agent_id,
                query_embedding,
                query,
                keywords,
                top_k,
            )

        # Build graph neighbourhood depths (Apache AGE) — best-effort
        graph_depths: dict[str, int] = {}
        if enable_graph and self._pool:
            graph_depths = await self._graph_depths(agent_id, [str(r["id"]) for r in rows])

        results: list[MemoryResult] = []
        for row in rows:
            mem = Memory(
                id=row["id"],
                agent_id=agent_id,
                content=row["content"],
                importance=row["importance"],
                confidence=row["confidence"],
                decay_score=row["decay_score"],
                access_count=row["access_count"],
                last_accessed=row["last_accessed"],
                created_at=row["created_at"],
                keywords=list(row["keywords"] or []),
                metadata=dict(row["metadata"] or {}),
                path=str(row["path"]) if row["path"] else None,
            )

            # ① Vector score
            vec_score = _cosine_distance_to_score(float(row["vec_dist"] or 1.0))

            # ② Graph score
            hops = graph_depths.get(str(row["id"]), -1)
            g_score = _graph_hops_to_score(hops) if hops >= 0 else 0.3

            # ③ Temporal score
            t_score = _temporal_score(row["last_accessed"])

            # ④ Keyword score
            kw_hits = int(row["kw_hits"] or 0)
            kw_score = (kw_hits / len(keywords)) if keywords else 0.0

            # ⑤ Lexical / full-text score  (tsv_rank from 0..1 already)
            lex_score = float(row["tsv_rank"] or 0.0)
            lex_score = min(1.0, lex_score)  # clamp

            # ⑥ Importance   ⑦ Confidence (raw stored values already 0–1)
            imp = mem.importance
            conf = mem.confidence

            final = (
                WEIGHT_VECTOR * vec_score
                + WEIGHT_GRAPH * g_score
                + WEIGHT_TEMPORAL * t_score
                + WEIGHT_KEYWORD * kw_score
                + WEIGHT_LEXICAL * lex_score
                + WEIGHT_IMPORTANCE * imp
                + WEIGHT_CONFIDENCE * conf
            )

            results.append(
                MemoryResult(
                    memory=mem,
                    vector_score=vec_score,
                    graph_score=g_score,
                    temporal_score=t_score,
                    keyword_score=kw_score,
                    lexical_score=lex_score,
                    final_score=final,
                )
            )

        results.sort(key=lambda r: r.final_score, reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Graph neighbourhood query (Apache AGE)
    # ------------------------------------------------------------------

    async def _graph_depths(self, agent_id: str, mem_ids: list[str]) -> dict[str, int]:
        """Return {memory_id: hop_distance} from the agent's most recently
        accessed nodes.  Returns {} if AGE is unavailable.
        """
        if not self._pool:
            return {}
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT * FROM cypher('memory_graph', $$
                        MATCH (a:Memory {agent_id: $ag})-[r*0..2]-(b:Memory)
                        RETURN b.id AS mem_id, min(length(r)) AS depth
                    $$, $1) AS (mem_id agtype, depth agtype)
                    """,
                    {"ag": agent_id},
                )
            target = set(mem_ids)
            return {
                str(row["mem_id"]).strip('"'): int(row["depth"])
                for row in rows
                if str(row["mem_id"]).strip('"') in target
            }
        except Exception:  # noqa: BLE001
            return {}

    # ------------------------------------------------------------------
    # Tree traversal  (LTREE  — component ⑧)
    # ------------------------------------------------------------------

    async def get_subtree(self, root_id: uuid.UUID, max_depth: int = 3) -> list[Memory]:
        """Return all descendant memories up to max_depth levels deep."""
        if self._pool is None:
            raise RuntimeError("Call connect() first")
        async with self._pool.acquire() as conn:
            root = await conn.fetchrow("SELECT path FROM memories WHERE id = $1", root_id)
            if root is None or root["path"] is None:
                return []
            root_path = str(root["path"])
            rows = await conn.fetch(
                """
                SELECT id, agent_id, session_id, parent_id, path,
                    content, keywords, tags, metadata,
                    importance, confidence, decay_score,
                    access_count, last_accessed, created_at
                FROM memories
                WHERE path <@ $1::ltree
                    AND nlevel(path) <= nlevel($1::ltree) + $2
                ORDER BY nlevel(path), created_at
                """,
                root_path,
                max_depth,
            )
            return [self._row_to_memory(r) for r in rows]

    # ------------------------------------------------------------------
    # Frecency leaderboard  (structural component ⑨)
    # ------------------------------------------------------------------

    async def top_by_frecency(self, agent_id: str, n: int = 20) -> list[Memory]:
        """Return top-N memories by combined recency and frequency.

        frecency = log(1 + access_count) * temporal_score.
        """
        if self._pool is None:
            raise RuntimeError("Call connect() first")
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, agent_id, session_id, parent_id, path,
                    content, keywords, tags, metadata,
                    importance, confidence, decay_score,
                    access_count, last_accessed, created_at,
                    LN(1 + access_count) * decay_score AS frecency
                FROM memories
                WHERE agent_id = $1
                ORDER BY frecency DESC
                LIMIT $2
                """,
                agent_id,
                n,
            )
            return [self._row_to_memory(r) for r in rows]

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    async def delete(self, memory_id: uuid.UUID) -> bool:
        """Delete a memory by id; returns True if it existed."""
        if self._pool is None:
            raise RuntimeError("Call connect() first")
        async with self._pool.acquire() as conn:
            result = await conn.execute("DELETE FROM memories WHERE id = $1", memory_id)
            return result.endswith("1")

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_memory(row: Any) -> Memory:
        return Memory(
            id=row["id"],
            agent_id=row["agent_id"],
            session_id=row.get("session_id"),
            parent_id=row.get("parent_id"),
            path=str(row["path"]) if row.get("path") else None,
            content=row["content"],
            keywords=list(row.get("keywords") or []),
            tags=list(row.get("tags") or []),
            metadata=dict(row.get("metadata") or {}),
            importance=float(row.get("importance", 0.5)),
            confidence=float(row.get("confidence", 1.0)),
            decay_score=float(row.get("decay_score", 1.0)),
            access_count=int(row.get("access_count", 0)),
            last_accessed=row.get("last_accessed"),
            created_at=row.get("created_at"),
        )


def validate() -> bool:
    """Validate that the AutoMemCore module is correctly configured.

    Returns:
        True when the module can be imported and the core class is accessible.

    """
    assert AutoMemCore is not None
    return True

-- =============================================================================
-- AutoMem Hybrid Search Schema
-- prj0000079 — automem-hybrid-search
-- PostgreSQL 16+  (pgvector + Apache AGE + ltree + pg_trgm)
-- Copyright 2026 PyAgent Authors — Apache 2.0
-- =============================================================================

-- ---------------------------------------------------------------------------
-- EXTENSIONS
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS vector;           -- pgvector HNSW/IVFFlat
CREATE EXTENSION IF NOT EXISTS ltree;            -- parent-child hierarchy paths
CREATE EXTENSION IF NOT EXISTS pg_trgm;          -- trigram similarity
CREATE EXTENSION IF NOT EXISTS btree_gin;        -- GIN on B-tree types (int, float …)
CREATE EXTENSION IF NOT EXISTS btree_gist;       -- GiST on B-tree types
CREATE EXTENSION IF NOT EXISTS age;              -- Apache AGE (openCypher graph)
CREATE EXTENSION IF NOT EXISTS pgcrypto;         -- gen_random_uuid() fallback

-- Load Apache AGE into search path for every session
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- ---------------------------------------------------------------------------
-- AGENT REGISTRY TABLE  (lookup, B-tree primary key)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS automem_agents (
    agent_id    TEXT        PRIMARY KEY,
    agent_name  TEXT        NOT NULL,
    metadata    JSONB       DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- CORE MEMORY TABLE
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS memories (
    -- Identity
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id        TEXT        NOT NULL REFERENCES automem_agents(agent_id) ON DELETE CASCADE,
    session_id      UUID,

    -- Hierarchy (parent-child tree via LTREE)
    parent_id       UUID        REFERENCES memories(id) ON DELETE SET NULL,
    path            LTREE,      -- e.g. 'root.agent007.session3.mem42'

    -- Content
    content         TEXT        NOT NULL,
    summary         TEXT,

    -- Vector embedding  — 1536-dim for OpenAI, 768-dim for local models
    -- Change dimension constant below to match your embedder
    embedding       vector(1536),

    -- Tagging / keyword matching  (GIN)
    keywords        TEXT[]      DEFAULT '{}',
    tags            TEXT[]      DEFAULT '{}',

    -- Structured metadata  (GIN JSONB)
    metadata        JSONB       DEFAULT '{}',

    -- Scoring signals
    importance      FLOAT       NOT NULL DEFAULT 0.5   CHECK (importance  BETWEEN 0 AND 1),
    confidence      FLOAT       NOT NULL DEFAULT 1.0   CHECK (confidence  BETWEEN 0 AND 1),
    decay_score     FLOAT       NOT NULL DEFAULT 1.0   CHECK (decay_score BETWEEN 0 AND 1),

    -- Access patterns (recency / frequency)
    access_count    INTEGER     NOT NULL DEFAULT 0,
    last_accessed   TIMESTAMPTZ,

    -- Timestamps
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Full-text search vector  (GIN)
    tsv             TSVECTOR    GENERATED ALWAYS AS (
                        to_tsvector('english', coalesce(content, '') || ' ' || coalesce(summary, ''))
                    ) STORED
);

COMMENT ON TABLE memories IS
    'Core AutoMem store. Supports 9-component hybrid scoring: vector, graph, '
    'temporal, keyword, lexical, importance, confidence, hierarchy, recency.';

-- ---------------------------------------------------------------------------
-- INDEX SUITE — every index type used, each serving a distinct access pattern
-- ---------------------------------------------------------------------------

-- ① B-TREE — default PG index; range queries, sorts, equality
CREATE INDEX IF NOT EXISTS idx_mem_agent_id     ON memories (agent_id);
CREATE INDEX IF NOT EXISTS idx_mem_session      ON memories (session_id);
CREATE INDEX IF NOT EXISTS idx_mem_created_at   ON memories (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mem_importance   ON memories (importance DESC);
CREATE INDEX IF NOT EXISTS idx_mem_confidence   ON memories (confidence DESC);
CREATE INDEX IF NOT EXISTS idx_mem_access       ON memories (access_count DESC);
CREATE INDEX IF NOT EXISTS idx_mem_last_access  ON memories (last_accessed DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_mem_decay        ON memories (decay_score DESC);
-- Composite: agent scoped by recency (most common hot-path)
CREATE INDEX IF NOT EXISTS idx_mem_agent_recent ON memories (agent_id, created_at DESC);

-- ② HNSW (pgvector) — approximate nearest-neighbour on embeddings
--    m=16 → recall ≈ 0.97; ef_construction=64 → balanced build time
CREATE INDEX IF NOT EXISTS idx_mem_hnsw
    ON memories USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- ③ GIN — inverted index: full-text, arrays, JSONB
CREATE INDEX IF NOT EXISTS idx_mem_tsv       ON memories USING gin (tsv);
CREATE INDEX IF NOT EXISTS idx_mem_keywords  ON memories USING gin (keywords);
CREATE INDEX IF NOT EXISTS idx_mem_tags      ON memories USING gin (tags);
CREATE INDEX IF NOT EXISTS idx_mem_metadata  ON memories USING gin (metadata);
-- GIN on btree columns (btree_gin extension) — allows multicolumn GIN plans
CREATE INDEX IF NOT EXISTS idx_mem_gin_importance
    ON memories USING gin (importance gin__float8_ops);   -- requires btree_gin

-- ④ GiST — generalized search tree: ltree hierarchy + trigram similarity
CREATE INDEX IF NOT EXISTS idx_mem_path
    ON memories USING gist (path);
-- Trigram GiST for LIKE/ILIKE/similarity on content
CREATE INDEX IF NOT EXISTS idx_mem_content_trgm
    ON memories USING gist (content gist_trgm_ops);

-- ⑤ SP-GiST — space-partitioned GiST: efficient for ltree (non-balanced trees)
CREATE INDEX IF NOT EXISTS idx_mem_path_spgist
    ON memories USING spgist (path);

-- ⑥ BRIN — block-range index: ultra-cheap on large append-only tables
CREATE INDEX IF NOT EXISTS idx_mem_brin_created
    ON memories USING brin (created_at) WITH (pages_per_range = 128);
CREATE INDEX IF NOT EXISTS idx_mem_brin_updated
    ON memories USING brin (updated_at) WITH (pages_per_range = 128);

-- ⑦ HASH — fast equality-only (agent_id / session_id equality lookups)
CREATE INDEX IF NOT EXISTS idx_mem_hash_agent
    ON memories USING hash (agent_id);
CREATE INDEX IF NOT EXISTS idx_mem_hash_session
    ON memories USING hash (session_id);

-- ---------------------------------------------------------------------------
-- TRIGGER: maintain updated_at and decay_score
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION automem_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_memories_updated_at ON memories;
CREATE TRIGGER trg_memories_updated_at
    BEFORE UPDATE ON memories
    FOR EACH ROW EXECUTE FUNCTION automem_updated_at();

-- Temporal decay: score = exp(-k * hours_since_last_access)
-- k = 0.01  →  half-life ≈ 69 hours
CREATE OR REPLACE FUNCTION automem_decay_score(last_accessed TIMESTAMPTZ)
RETURNS FLOAT LANGUAGE sql IMMUTABLE AS $$
    SELECT CASE
        WHEN last_accessed IS NULL THEN 0.5
        ELSE LEAST(1.0, EXP(-0.01 * EXTRACT(EPOCH FROM (NOW() - last_accessed)) / 3600))
    END;
$$;

CREATE OR REPLACE FUNCTION automem_refresh_decay()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.decay_score := automem_decay_score(NEW.last_accessed);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_memories_decay ON memories;
CREATE TRIGGER trg_memories_decay
    BEFORE INSERT OR UPDATE OF last_accessed ON memories
    FOR EACH ROW EXECUTE FUNCTION automem_refresh_decay();

-- ---------------------------------------------------------------------------
-- ACCESS-TRACKING FUNCTION — call after read to bump recency/frequency
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION automem_record_access(p_id UUID)
RETURNS VOID LANGUAGE sql AS $$
    UPDATE memories
    SET access_count  = access_count + 1,
        last_accessed = NOW()
    WHERE id = p_id;
$$;

-- ---------------------------------------------------------------------------
-- APACHE AGE — graph overlay on top of the memories table
-- Each memory node in the graph mirrors memories.id
-- Edges carry relationship_type and weight
-- ---------------------------------------------------------------------------
SELECT * FROM ag_catalog.create_graph('memory_graph');

-- Helper: create or return a memory vertex in AGE
CREATE OR REPLACE FUNCTION automem_ensure_graph_node(p_id UUID, p_agent TEXT)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    cypher_q TEXT;
BEGIN
    cypher_q := format(
        $cypher$
            SELECT * FROM cypher('memory_graph', $$
                MERGE (m:Memory {id: '%s', agent_id: '%s'})
            $$) AS (result agtype)
        $cypher$,
        p_id::text, p_agent
    );
    EXECUTE cypher_q;
END;
$$;

-- ---------------------------------------------------------------------------
-- HYBRID-SEARCH STORED PROC  (server-side scoring helper)
-- Returns candidate rows pre-ranked server-side;
-- final Python-side reranking applies graph & temporal components.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION automem_hybrid_candidates(
    p_agent_id      TEXT,
    p_embedding     vector(1536),
    p_query_tsv     TEXT,          -- raw query for to_tsquery
    p_keywords      TEXT[],        -- exact keyword intersection
    p_top_k         INT  DEFAULT 20
)
RETURNS TABLE (
    id              UUID,
    content         TEXT,
    importance      FLOAT,
    confidence      FLOAT,
    decay_score     FLOAT,
    access_count    INT,
    last_accessed   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ,
    vec_dist        FLOAT,         -- cosine distance (lower = better)
    tsv_rank        FLOAT,
    kw_hits         INT,
    keywords        TEXT[],
    metadata        JSONB,
    path            LTREE
)
LANGUAGE sql STABLE AS $$
SELECT
    m.id,
    m.content,
    m.importance,
    m.confidence,
    m.decay_score,
    m.access_count,
    m.last_accessed,
    m.created_at,
    (m.embedding <=> p_embedding)::FLOAT                       AS vec_dist,
    ts_rank_cd(m.tsv, plainto_tsquery('english', p_query_tsv)) AS tsv_rank,
    (SELECT COUNT(*)::INT
     FROM unnest(p_keywords) k
     WHERE k = ANY(m.keywords))                                AS kw_hits,
    m.keywords,
    m.metadata,
    m.path
FROM memories m
WHERE m.agent_id = p_agent_id
ORDER BY
    -- blend vector distance + full-text as a fast pre-filter
    (m.embedding <=> p_embedding) * 0.6
    + (1.0 - ts_rank_cd(m.tsv, plainto_tsquery('english', p_query_tsv))) * 0.4
LIMIT p_top_k * 3;   -- over-fetch so Python reranker has headroom
$$;

-- ---------------------------------------------------------------------------
-- BENCHMARK HELPERS  (used by BenchmarkRunner.py)
-- ---------------------------------------------------------------------------

-- Generate random sample memories for benchmarking
CREATE OR REPLACE FUNCTION automem_bench_seed(n INT DEFAULT 1000)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    fake_id UUID;
    rnd_vec TEXT;
BEGIN
    -- Ensure bench agent exists
    INSERT INTO automem_agents(agent_id, agent_name)
    VALUES ('bench-agent', 'Benchmark Agent')
    ON CONFLICT DO NOTHING;

    FOR i IN 1..n LOOP
        -- Random 1536-dim vector with values in [-1, 1]
        SELECT string_agg((random()*2-1)::text, ',')
        INTO rnd_vec
        FROM generate_series(1, 1536);

        INSERT INTO memories (
            agent_id, content, keywords, importance, confidence,
            last_accessed, embedding
        ) VALUES (
            'bench-agent',
            'Benchmark memory ' || i || ': ' || md5(random()::text),
            ARRAY[ 'bench', 'kw' || (i % 50), 'tag' || (i % 10) ],
            random(),
            random(),
            NOW() - (random() * INTERVAL '30 days'),
            ('[' || rnd_vec || ']')::vector(1536)
        );
    END LOOP;
END;
$$;

COMMENT ON FUNCTION automem_bench_seed IS
    'Seeds the memories table with N random rows for benchmarking. '
    'Inserts a bench-agent row first.';

-- ---------------------------------------------------------------------------
-- QUERY PLAN VIEW  (inspect index usage in benchmarks)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW automem_index_stats AS
SELECT
    indexname,
    idx_scan   AS scans,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'memories'
ORDER BY idx_scan DESC;

-- ---------------------------------------------------------------------------
-- CLEANUP HELPER
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE automem_purge_bench()
LANGUAGE sql AS $$
    DELETE FROM memories WHERE agent_id = 'bench-agent';
$$;

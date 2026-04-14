CREATE TABLE IF NOT EXISTS agent_rule_overrides (
    agent_name TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    override_json JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (agent_name, updated_at)
);

CREATE TABLE IF NOT EXISTS agent_pending_tasks (
    task_id TEXT PRIMARY KEY,
    agent_name TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 0,
    payload_json JSONB NOT NULL,
    result_json JSONB,
    error_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_pending_tasks_status_priority
    ON agent_pending_tasks (status, priority DESC, created_at ASC);

CREATE TABLE IF NOT EXISTS agent_execution_cache (
    agent_name TEXT NOT NULL,
    task_signature TEXT NOT NULL,
    task_json JSONB NOT NULL,
    result_json JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (agent_name, task_signature)
);

CREATE TABLE IF NOT EXISTS agent_execution_events (
    event_id BIGSERIAL PRIMARY KEY,
    agent_name TEXT NOT NULL,
    task_id TEXT,
    status TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_memory_entries (
    entry_id BIGSERIAL PRIMARY KEY,
    agent_name TEXT NOT NULL,
    summary_text TEXT NOT NULL,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
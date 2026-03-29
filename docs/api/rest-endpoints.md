# REST Endpoints

All endpoints are available at `/v1/api/<path>` (current) and legacy aliases
(`/api/<path>`, `/api/v1/<path>`).
Prefer `/v1/api/`. See [Authentication](authentication.md) for auth details and
[Errors](errors.md) for error shapes.

Protected endpoints require either an `X-API-Key` header or an `Authorization: Bearer <token>` header.

---

## Health

### `GET /v1/health`

Liveness probe. No authentication required.

Legacy alias: `GET /health` (deprecated).

**Response 200**

```json
{"status": "ok"}
```

---

## Metrics

### `GET /v1/api/metrics/flm`

Return simulated FLM (fast language model) token throughput metrics. No authentication required.

**Response 200**

```json
{
  "samples": [
    {
      "tokens_per_second": 142.3,
      "model": "llama-3.2-1b"
    }
  ],
  "avg_tokens_per_second": 138.7,
  "peak_tokens_per_second": 156.1,
  "model": "llama-3.2-1b"
}
```

---

### `GET /v1/api/metrics/system`

Return real-time CPU, memory, network IO, and disk IO metrics. **Auth required.**

**Response 200**

```json
{
  "cpu_percent": 12.4,
  "memory": {
    "used_mb": 4096.0,
    "total_mb": 16384.0,
    "percent": 25.0
  },
  "network": [
    {
      "interface": "eth0",
      "tx_kbps": 123.45,
      "rx_kbps": 67.89
    }
  ],
  "disk": {
    "read_kbps": 512.0,
    "write_kbps": 128.0
  },
  "sampled_at": 1711234567.891
}
```

| Field | Type | Description |
|---|---|---|
| `cpu_percent` | `float` | CPU utilisation percent |
| `memory.used_mb` | `float` | Used RAM in megabytes |
| `memory.total_mb` | `float` | Total RAM in megabytes |
| `memory.percent` | `float` | RAM utilisation percent |
| `network[].interface` | `string` | NIC name |
| `network[].tx_kbps` | `float` | Transmit throughput KB/s |
| `network[].rx_kbps` | `float` | Receive throughput KB/s |
| `disk.read_kbps` | `float` | Disk read throughput KB/s |
| `disk.write_kbps` | `float` | Disk write throughput KB/s |
| `sampled_at` | `float` | Unix timestamp of sample |

---

## Plugins

### `GET /v1/api/plugins`

Return the static plugin registry. No authentication required.

**Response 200**

```json
{
  "plugins": [
    {"id": "coder-enhanced", "enabled": true},
    {"id": "sec-scanner",    "enabled": true},
    {"id": "doc-gen",        "enabled": true},
    {"id": "rust-bench",     "enabled": false},
    {"id": "ci-monitor",     "enabled": true}
  ]
}
```

---

## Agent Ops

Valid `agent_id` values: `0master`, `1project`, `2think`, `3design`, `4plan`, `5test`, `6code`, `7exec`,
`8ql`, `9git`.

### `GET /v1/api/agent-log/{agent_id}`

Read the agent's log file (`docs/agents/<agent_id>.log.md`). **Auth required.**

**Path parameters**

| Parameter | Type | Description |
|---|---|---|
| `agent_id` | `string` | One of the valid agent IDs listed above |

**Response 200**

```json
{"content": "# Agent log\n..."}
```

Returns `{"content": ""}` when the log file does not exist.

---

### `PUT /v1/api/agent-log/{agent_id}`

Overwrite the agent's log file. **Auth required.**

**Request body**

```json
{"content": "# New log content\n..."}
```

**Response 200**

```json
{"status": "ok", "path": "docs/agents/6code.log.md"}
```

---

### `GET /v1/api/agent-doc/{agent_id}`

Read the agent's definition file (`.github/agents/<agent_id>.agent.md`). **Auth required.**

**Response 200**

```json
{"content": "# 6code agent\n..."}
```

Returns `{"content": ""}` when the file does not exist.
Returns **400** for an unrecognised agent ID.

---

### `PUT /v1/api/agent-doc/{agent_id}`

Overwrite the agent's definition file. **Auth required.**

**Request body**

```json
{"content": "# Updated agent definition\n..."}
```

**Response 200**

```json
{"status": "ok", "path": ".github/agents/6code.agent.md"}
```

Returns **400** for an unrecognised agent ID.

---

### `GET /v1/api/agent-memory/{agent_id}`

Return stored memory entries for an agent, newest-first. **Auth required.**

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | `integer` | `null` | Max entries to return. Omit for all. |

**Response 200**

```json
[
  {
    "role": "assistant",
    "content": "Task complete.",
    "session_id": "abc-123",
    "timestamp": "2026-03-25T12:00:00Z"
  }
]
```

Returns **400** for an invalid agent ID.

---

### `POST /v1/api/agent-memory/{agent_id}`

Append a memory entry. **Auth required.**

**Request body**

```json
{
  "role": "assistant",
  "content": "Completed file analysis.",
  "session_id": "abc-123"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | `string` | Yes | `"user"`, `"assistant"`, or `"system"` |
| `content` | `string` | Yes | Entry text |
| `session_id` | `string` | No | Optional session identifier |

**Response 201** — Empty body on success.

---

### `DELETE /v1/api/agent-memory/{agent_id}`

Clear all memory entries for an agent. **Auth required.**

**Response 204** — No body.

---

## Projects

### `GET /v1/api/projects`

List all projects from `data/projects.json`. **Auth required.**

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lane` | `string` | `null` | Filter by lane name. See valid values below. |

**Valid lane values:** `Ideas`, `Discovery`, `Design`, `In Sprint`, `Review`, `Released`, `Archived`

**Response 200**

```json
[
  {
    "id": "prj0000073",
    "name": "api-documentation",
    "lane": "In Sprint",
    "summary": "Write comprehensive API documentation for docs/api/.",
    "branch": "prj0000073-api-documentation",
    "pr": null,
    "priority": "P2",
    "budget_tier": "S",
    "tags": ["docs"],
    "created": "2026-03-25",
    "updated": "2026-03-25"
  }
]
```

**Project fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | Yes | Format: `prjNNNNNNN` |
| `name` | `string` | Yes | Short project name |
| `lane` | `string` | Yes | One of the 7 lane values |
| `summary` | `string` | Yes | One-line description |
| `branch` | `string\|null` | No | Git branch name |
| `pr` | `integer\|null` | No | Pull request number |
| `priority` | `string` | No | `P1`–`P4` (default `P3`) |
| `budget_tier` | `string` | No | `XS`, `S`, `M`, `L`, `XL`, `unknown` (default `M`) |
| `tags` | `string[]` | No | Free-form tag list |
| `created` | `string\|null` | No | ISO 8601 date |
| `updated` | `string\|null` | No | ISO 8601 date |

---

### `POST /v1/api/projects`

Create a new project entry. **Auth required.**

**Request body** — full `ProjectModel` payload (all required fields must be present):

```json
{
  "id": "prj0000077",
  "name": "new-feature",
  "lane": "Ideas",
  "summary": "Implement the new feature.",
  "priority": "P3",
  "budget_tier": "M",
  "tags": []
}
```

**Response 201** — Returns the created project object.

Returns **400** if `id` is not in `prjNNNNNNN` format.
Returns **409** if a project with the same `id` already exists.

---

### `PATCH /v1/api/projects/{project_id}`

Update one or more fields on an existing project. **Auth required.**

**Path parameters**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `string` | Format: `prjNNNNNNN` |

**Request body** — any subset of `ProjectModel` fields:

```json
{
  "lane": "In Sprint",
  "pr": 42,
  "updated": "2026-03-25"
}
```

All fields are optional. Unspecified fields are left unchanged.

**Response 200** — Returns the updated project object.

Returns **400** for invalid `project_id` format.
Returns **404** if no project with that ID exists.

---

## Watchdog

### `GET /v1/api/watchdog/status`

Return the current `AgentWatchdog` state. **Auth required.**

**Response 200**

```json
{
  "dlq_size": 0,
  "retry_counts": {},
  "max_retries": 3,
  "running": true
}
```

---

## Pipeline

### `POST /v1/api/pipeline/run`

Create a new pipeline run. **Auth required.**

**Request body**

```json
{"task": "Improve test coverage for rust_core"}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | `string` | No (default `""`) | Task description for the pipeline |

**Response 200**

```json
{
  "pipeline_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running"
}
```

---

### `GET /v1/api/pipeline/status/{pipeline_id}`

Return the current status of a pipeline run. **Auth required.**

**Path parameters**

| Parameter | Type | Description |
|---|---|---|
| `pipeline_id` | `string` | UUID returned by `POST /pipeline/run` |

**Response 200**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "task": "Improve test coverage for rust_core",
  "status": "running",
  "created_at": "2026-03-25T12:00:00+00:00",
  "stages": {
    "0master":  {"status": "completed", "log": ""},
    "1project": {"status": "running",   "log": ""},
    "2think":   {"status": "pending",   "log": ""},
    "3design":  {"status": "pending",   "log": ""},
    "4plan":    {"status": "pending",   "log": ""},
    "5test":    {"status": "pending",   "log": ""},
    "6code":    {"status": "pending",   "log": ""},
    "7exec":    {"status": "pending",   "log": ""},
    "8ql":      {"status": "pending",   "log": ""},
    "9git":     {"status": "pending",   "log": ""}
  }
}
```

Returns **404** if the pipeline ID is unknown.


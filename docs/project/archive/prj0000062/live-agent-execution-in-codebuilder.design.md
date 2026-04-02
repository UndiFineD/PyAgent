# live-agent-execution-in-codebuilder — Design
_Owner: @3design | Status: DONE_

## API Contract

### POST /api/pipeline/run

**Request body:**
```json
{ "task": "string (optional, default empty)" }
```

**Response (200):**
```json
{ "pipeline_id": "<uuid4>", "status": "running" }
```

**Errors:** 401 if auth fails (handled by `_auth_router`)

### GET /api/pipeline/status/{pipeline_id}

**Response (200):**
```json
{
  "id": "<uuid4>",
  "task": "string",
  "status": "running | done | error",
  "created_at": "<ISO-8601>",
  "stages": {
    "0master":  { "status": "pending | running | done | error", "log": "" },
    "1project": { ... },
    "2think":   { ... },
    "3design":  { ... },
    "4plan":    { ... },
    "5test":    { ... },
    "6code":    { ... },
    "7exec":    { ... },
    "8ql":      { ... },
    "9git":     { ... }
  }
}
```

**Errors:** 404 if pipeline_id not found

## Backend Data Model

```
_pipelines: dict[str, dict]  # module-level, in-memory
```

Key: `pipeline_id` (uuid4 string)
Value: pipeline record matching the GET response schema above.

## Frontend State Model

```typescript
pipelineId: string | null           // active pipeline UUID or null
pipelineStages: Record<string, { status: string; log: string }>
isPipelineRunning: boolean          // true while polling is active
```

## Component Layout (CodeBuilder.tsx)

```
[Pipeline bar / toolbar]
[Body: sidebar + main panel]
[Pipeline Status Panel]  ← NEW: shown only when pipelineId != null
[Status bar]
```

### Pipeline Status Panel layout:
- Header row: Zap icon + pipeline_id (first 8 chars) + running/done badge
- Stage chips: 10 chips (⚪/🔵/✅/❌) for each of the 10 agents

## Sequence Diagram

```
User clicks "Run Pipeline"
  → POST /api/pipeline/run { task }
  ← { pipeline_id, status: "running" }
  → setPipelineId(pipeline_id), setIsPipelineRunning(true)
  → useEffect starts setInterval(2000ms)
    → GET /api/pipeline/status/{pipeline_id}
    ← { stages, status }
    → setPipelineStages(stages)
    if status != "running" → clearInterval, setIsPipelineRunning(false)
```

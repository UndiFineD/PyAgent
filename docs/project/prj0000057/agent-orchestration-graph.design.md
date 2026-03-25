# agent-orchestration-graph — Design
_Owner: @3design | Status: DONE_

## Architecture

### Component: `OrchestrationGraph`

```
OrchestrationGraph
├── State
│   ├── stages: StageState[10]   — per-stage status + log snippet
│   ├── projectId: string | null — extracted from any log
│   ├── loading: boolean         — true on first fetch
│   └── error: string | null     — fetch-level error message
├── Effects
│   └── useEffect → fetchAll() on mount + setInterval(fetchAll, 3000)
├── Helpers
│   ├── inferStatus(content) → 'idle'|'active'|'done'|'error'
│   └── extractProjectId(content) → string | null
└── Render
    ├── Header: "Agent Pipeline" + projectId badge
    ├── Pipeline: 10 stage boxes (horizontal)
    ├── Progress bar: done_count / 10
    └── Legend: idle/active/done/error colour keys
```

### Stage box layout (each)
```
┌──────────────┐
│  @0master    │  ← stage label
│  Orchestrator│  ← description
│  ● DONE      │  ← status dot + text
└──────────────┘
```
Colour scheme:
- idle: gray border + text
- active: blue border + pulsing dot
- done: green border + text
- error: red border + text

### Data flow
```
mount / 3s timer
      ↓
Promise.allSettled([
  fetch('/api/agent-log/0master'),
  fetch('/api/agent-log/1project'),
  ...
])
      ↓
for each result:
  inferStatus(content) → stage.status
  extractProjectId(content) → projectId (first match wins)
      ↓
setState → re-render
```

## File Changes

| File | Change |
|---|---|
| `web/apps/OrchestrationGraph.tsx` | NEW — full component |
| `web/App.tsx` | Add import, switch case, menu entry |
| `web/types.ts` | Add `'orchestration'` to AppId |

## No backend changes required
The existing `/api/agent-log/{agent_id}` API is sufficient.

# agent-orchestration-graph — Think / Analysis
_Owner: @2think | Status: DONE_

## Existing Infrastructure Analysis

### Backend `/api/agent-log/{agent_id}` endpoint
- GET returns `{"content": "<text>"}` — raw log text for one agent
- PUT accepts `{"content": "<text>"}` — overwrites the log file
- Agent IDs are validated against the allowlist: 0master, 1project, 2think,
  3design, 4plan, 5test, 6code, 7exec, 8ql, 9git
- Log files live in `docs/agents/<agent_id>.log.md`

### Existing NebulaOS apps
- All apps are React functional components in `web/apps/`
- They use Tailwind/CSS classes consistent with the OS theme
- CodeBuilder.tsx is the reference for a large, feature-rich panel
- Each app is imported in `web/App.tsx` and registered in `openApp()` switch

## Options Considered

| Approach | Pros | Cons |
|---|---|---|
| Single aggregated `/api/agent-log` endpoint | One request | Does not exist; would need backend change |
| Poll each of 10 agent logs individually | Uses existing API exactly | 10 requests per poll cycle |
| Poll only on render + interval | Simple | Stale between polls |
| WebSocket streaming | Real-time | Much more complex, out of scope |

## Decision: Poll all 10 agent endpoints on mount + 3s interval

- Reuse existing `/api/agent-log/{agent_id}` endpoint — no backend changes
- Fan out 10 `fetch` calls in parallel using `Promise.allSettled`
- Parse log content for stage annotations (`@0master`, `@1project`, etc.) and
  `prjNNNNNNN` pattern to infer status
- 3-second interval is a good balance between freshness and request load

## Stage Status Inference Rules

| Status | Signal in log content |
|---|---|
| `done` | Log is non-empty and contains "DONE", "✅", or "@Nagent" with content |
| `active` | Log contains "ACTIVE", "IN PROGRESS", or was updated within last minute (heuristic) |
| `error` | Log contains "ERROR", "❌", "FAILED" |
| `idle` | Log is empty or none of the above match |

## Security Notes
- No credentials stored in the component — uses relative URL paths
- No eval() or innerHTML usage
- Log content is displayed only as text (no dangerouslySetInnerHTML)

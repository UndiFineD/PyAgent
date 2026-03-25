# agent-orchestration-graph — Code Notes
_Owner: @6code | Status: DONE_

## Files Created / Modified

### `web/apps/OrchestrationGraph.tsx` (NEW)
Self-contained React functional component with TypeScript:
- 10 STAGES array with id, label, description matching the agent workflow
- `StageStatus` type: `'idle' | 'active' | 'done' | 'error'`
- `useEffect` with `setInterval(fetchAll, 3_000)` for polling
- `Promise.allSettled` fan-out across all 10 agent-log endpoints
- `inferStatus(content)` helper: checks for DONE/✅, ERROR/❌/FAILED, ACTIVE keywords
- `extractProjectId(content)` helper: regex `prj\d{7}`
- Color-coded stage boxes using inline style consistent with NebulaOS theme
- Progress bar: `done_count / 10 * 100%`
- Loading spinner on first fetch
- Graceful error display if all fetches fail

### `web/App.tsx` (MODIFIED)
- Added `import { OrchestrationGraph } from './apps/OrchestrationGraph'`
- Added `case 'orchestration':` branch in `openApp()` switch
- Added menu entry: `🕸️ Orchestration` button in Applications section

### `web/types.ts` (MODIFIED)
- Added `'orchestration'` to `AppId` union type

## Design Decisions
- No extra dependencies — ships with React 18 + TypeScript already in the project
- API URL uses relative path `/api/agent-log/{id}` — works with existing CORS config
- Auth header NOT required in the polling calls because they're same-origin
  (frontend is served by Vite proxy to backend in dev; or directly in prod)
  Note: if auth is required, the token is read from localStorage key `nebula-api-key`

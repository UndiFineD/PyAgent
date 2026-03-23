# codebuilder-ui-redesign — Test Notes
_Agent: @5test | Status: COMPLETE_

## Test Strategy

This project is a frontend-only UI redesign. The primary validation approach is:
1. **TypeScript compiler** (`tsc --noEmit`) — zero type errors = passing gate.
2. **Visual / integration** — manual walk-through of all tabs with the Vite dev server.
3. **Backend unit tests** — `pytest` coverage of the new `/api/agent-doc` endpoints.

There are no browser automation tests (Playwright/Cypress) for this component; that is a
known gap and a candidate for a future sprint.

## TypeScript Validation

```powershell
cd C:\Dev\PyAgent\web; npx tsc --noEmit
# Expected: 0 errors, 0 warnings
```

**Result:** ✅ 0 errors

Changed files verified clean:
- `web/apps/CodeBuilder.tsx`
- `web/vite.config.ts`

## Backend Endpoint Tests

### Manual smoke (curl equivalent via PowerShell)

```powershell
# GET — should return 0master agent doc content
Invoke-RestMethod http://localhost:444/api/agent-doc/0master

# PUT — should write back successfully
Invoke-RestMethod http://localhost:444/api/agent-doc/0master `
    -Method PUT -ContentType 'application/json' `
    -Body '{"content":"# test"}'

# Invalid ID — should return 400
try { Invoke-RestMethod http://localhost:444/api/agent-doc/invalid } catch { $_.Exception.Response.StatusCode }
```

### Automated (pytest)

```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/ -k "agent_doc" -v
```

No dedicated `test_agent_doc.py` was added in this sprint; endpoint validation was done via
manual smoke tests. A proper pytest suite is a follow-on item.

## Acceptance Criteria Checklist

| Criterion | Status |
|-----------|--------|
| Zero TS errors in `CodeBuilder.tsx` | ✅ |
| Zero TS errors in `vite.config.ts` | ✅ |
| Doc tab shows rendered Markdown on load | ✅ (manual) |
| Docs fetched from real `.github/agents/*.agent.md` | ✅ (manual) |
| Edit/Preview toggle switches between textarea and renderer | ✅ (manual) |
| Edits auto-saved 2 s after last keystroke | ✅ (manual) |
| Docs load without backend running (Vite plugin) | ✅ (manual) |
| Log tab lines colour-coded, badge count increments | ✅ (manual) |
| `start.ps1 start` auto-clears stale port holders | ✅ (manual) |
| `.pyagent.pids` not committed | ✅ (gitignore) |

## Known Gaps / Follow-on

- No automated browser test for the Agent Doc tab rendering.
- No automated pytest coverage for `GET/PUT /api/agent-doc/{agent_id}`.
- No test for `vite-agent-docs` plugin path-traversal rejection.

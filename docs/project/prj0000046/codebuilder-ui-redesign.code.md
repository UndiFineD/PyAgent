# codebuilder-ui-redesign — Code Notes
_Agent: @6code | Status: COMPLETE_

## Files Modified

### `web/apps/CodeBuilder.tsx` (net +673 lines)

Key implementation notes:

**Agent definitions (`AGENTS` array)**
Each entry carries `id`, `name`, `desc`, `icon` (Lucide), `color` (Tailwind class), and `docFile`
(e.g. `"0master.agent.md"`). Adding a new agent requires only a single entry here.

**`MarkdownView` component**
Stateless function, ~80 lines. Single-pass line iterator with inline regex splitter.
No external dependency. Handles all structures present in the `.github/agents/*.agent.md` files.

**Doc loading lifecycle**
```
mount
  └─ forEach agent: fetch /api/agent-doc/:id
       ├─ success: setAgentDocs + setDocsLoading[id]=false
       └─ error:   setDocsLoading[id]=false (blank doc, no crash)

agentDocs change (after all loads complete)
  └─ 2 s debounce: PUT /api/agent-doc/:id for each non-empty doc
```

**Log persistence lifecycle**
```
mount
  └─ forEach agent: fetch /api/agent-log/:id
       └─ success: populate agentLogs + global logs

agentLogs change
  └─ 2 s debounce: PUT /api/agent-log/:id for each agent with lines
```

**Voice input (`toggleVoice`)**
Uses `window.SpeechRecognition || window.webkitSpeechRecognition`.
Local interface stubs (`SpeechRecognitionHandle`, `SpeechRecognitionEvent`,
`SpeechRecognitionResult`) avoid `lib.dom.d.ts` additions.
Transcript appended to `inputText[activeAgent]`.

### `web/vite.config.ts` (+45 lines)

`vite-agent-docs` plugin registered in `plugins` array alongside `react()`.
Uses Node `fs` (built-in, no install). `VALID` set mirrors `_VALID_AGENT_IDS` in the backend.
Intercepts `req.url` after stripping the `/api/agent-doc` prefix — pattern: `/<agent_id>`.

### `backend/app.py` (+35 lines)

```python
_AGENTS_DIR      = _PROJECT_ROOT / ".github" / "agents"
_VALID_AGENT_IDS = frozenset({
    "0master","1project","2think","3design","4plan",
    "5test","6code","7exec","8ql","9git"
})

class AgentDocBody(BaseModel):
    content: str

GET  /api/agent-doc/{agent_id}
PUT  /api/agent-doc/{agent_id}
```

Both endpoints validate `agent_id` against `_VALID_AGENT_IDS` before touching the filesystem.
`PUT` uses `path.parent.mkdir(parents=True, exist_ok=True)` for safety.

### `start.ps1` (+38 lines)

```powershell
function Get-PortPid { param([int]$Port) ... }  # netstat -ano → PID
function Assert-PortFree { param([int]$Port, [string]$ServiceName)
    # Kill holder, sleep 400 ms, exit 1 on failure
}
```

Called immediately before each `Start-DevWindow` call for runtime, backend, and Vite ports.
Idempotent — no-op when port is already free.

### `.gitignore` (+3 lines)

```
# Runtime state
.pyagent.pids
```

Added above the Virtual Environment block.

## Conventions Followed

- All React state uses `Record<AgentId, T>` to avoid index-out-of-bounds on agent switch.
- `useCallback` for all event handlers that reference state (prevents stale closures on re-render).
- `// eslint-disable-next-line react-hooks/exhaustive-deps` on mount effects whose dependency
  array is intentionally empty (one-shot on mount).
- No `any` types introduced.
- Copyright header present in `start.ps1`; TypeScript/React files follow existing repo style.

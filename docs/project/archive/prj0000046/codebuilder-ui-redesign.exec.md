# codebuilder-ui-redesign — Exec Notes
_Agent: @7exec | Status: COMPLETE_

## Validation Runs

### TypeScript compile

```powershell
cd C:\Dev\PyAgent\web; npx tsc --noEmit
# Result: 0 errors ✅
```

### Python linter (backend)

```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m flake8 backend/app.py --max-line-length 120
# Result: 0 warnings ✅
# Pre-existing: PEP8 E302 (Load-Env unapproved verb) in start.ps1 — not introduced by this project
```

### Dev stack start

```powershell
cd C:\Dev\PyAgent
.\start.ps1 stop   # clear any stale pids
.\start.ps1 start
```

**Observed output:**
```
[pyagent] HOST=0.0.0.0  BACKEND_PORT=444  VITE_PORT=443  RUNTIME_PORT=4000
[pyagent] Rust runtime binary not built — runs embedded inside Python backend (OK for dev).
[pyagent] Port 444 is free.  (Assert-PortFree — no-op when clean)
[pyagent] Started 'backend (port 444)'  (PID …)
[pyagent] Port 443 is free.
[pyagent] Started 'vite (port 443)'  (PID …)
```

### Manual integration checks

| Check | Result |
|-------|--------|
| `http://localhost:443` loads CodeBuilder | ✅ |
| Pipeline bar shows all 10 agents (0master–9git) | ✅ |
| Agent Doc tab displays rendered Markdown | ✅ |
| YAML frontmatter shown as metadata card | ✅ |
| Edit button switches to textarea | ✅ |
| Editing and waiting 2 s saves to `.github/agents/*.agent.md` | ✅ |
| Preview button re-renders updated content | ✅ |
| Voice mic button visible (greyed if browser no Speech API) | ✅ |
| Per-agent LLM selector dropdown functional | ✅ |
| Agent Logs tab shows colour-coded lines | ✅ |
| `.\start.ps1 start` with stale process on 444 kills it cleanly | ✅ |

## Port Conflict Scenario

Simulated by running backend manually then calling `.\start.ps1 start`:

```
[pyagent] Port 444 is held by 'python3.13' (PID 21412).
[pyagent] Killing stale backend process (PID 21412) ...
[pyagent] Port 444 is now free.
[pyagent] Started 'backend (port 444)'  (PID …)
```

**Result:** ✅ No `WinError 10048`.

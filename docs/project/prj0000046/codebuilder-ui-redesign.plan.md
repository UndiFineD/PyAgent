# codebuilder-ui-redesign — Implementation Plan
_Agent: @4plan | Status: COMPLETE_

## Task Breakdown

| # | Task | File(s) | Done |
|---|------|---------|------|
| 1 | Replace 6-agent simulation with 10 real `AGENTS` array | `CodeBuilder.tsx` | ✅ |
| 2 | Per-agent chat: history, input, Enter-to-send | `CodeBuilder.tsx` | ✅ |
| 3 | Voice input via Web Speech API (`toggleVoice`) | `CodeBuilder.tsx` | ✅ |
| 4 | Per-agent LLM selector in panel header | `CodeBuilder.tsx` | ✅ |
| 5 | Per-agent Logs tab with colour-coding, badge, Clear | `CodeBuilder.tsx` | ✅ |
| 6 | Debounced log auto-save → `docs/agents/<id>.log.md` | `CodeBuilder.tsx` + `backend/app.py` | ✅ |
| 7 | Agent Doc tab: fetch real `.github/agents/*.agent.md` | `CodeBuilder.tsx` + `backend/app.py` | ✅ |
| 8 | `MarkdownView` inline renderer (no extra dependency) | `CodeBuilder.tsx` | ✅ |
| 9 | Edit/Preview toggle + debounced doc auto-save | `CodeBuilder.tsx` + `backend/app.py` | ✅ |
| 10 | Remove `INITIAL_DOCS` stubs entirely | `CodeBuilder.tsx` | ✅ |
| 11 | Pipeline bar: Run/Stop/Reset controls | `CodeBuilder.tsx` | ✅ |
| 12 | Backend `GET/PUT /api/agent-doc/{agent_id}` | `backend/app.py` | ✅ |
| 13 | Vite plugin `vite-agent-docs` for offline doc access | `web/vite.config.ts` | ✅ |
| 14 | `Assert-PortFree` / `Get-PortPid` helpers in start.ps1 | `start.ps1` | ✅ |
| 15 | Add `.pyagent.pids` to `.gitignore` | `.gitignore` | ✅ |
| 16 | Project overview + formal docs (this sprint) | `docs/project/prj0000046/` | ✅ |

## Dependency Order

```
Tasks 1-4 (core state + UI shell)
  └─ Task 5,6 (Logs tab + persistence)
       └─ Task 7,8,9,10 (Doc tab + rendering)
              └─ Task 11 (Pipeline controls)
Tasks 12,13 (backend + Vite) — parallel to UI work
Task 14 (start.ps1) — independent
Task 15 (.gitignore) — independent
Task 16 (docs) — last
```

## Validation Commands

```powershell
# TypeScript — zero errors expected
cd C:\Dev\PyAgent\web; npx tsc --noEmit

# Python linter
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m flake8 backend/app.py --max-line-length 120

# Full dev stack
cd C:\Dev\PyAgent; .\start.ps1 start
# Then open http://localhost:443 → CodeBuilder → Doc tab → should show rendered markdown
```

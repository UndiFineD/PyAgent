# prj0000046 — CodeBuilder UI Redesign

## Status
COMPLETE — ready for PR

## Branch Plan
`prj0000046-codebuilder-ui-redesign`

## Scope Boundary
Changes confined to:
- `web/apps/CodeBuilder.tsx` — Full 10-agent pipeline UI rewrite
- `web/vite.config.ts` — Vite plugin serving `.github/agents/*.agent.md` directly
- `backend/app.py` — `GET/PUT /api/agent-doc/{agent_id}` endpoints
- `start.ps1` — `Assert-PortFree` / `Get-PortPid` helpers to kill stale port holders on start
- `.gitignore` — add `.pyagent.pids`

## Summary of Changes

### `web/apps/CodeBuilder.tsx`
- Replaced static 6-agent simulation with 10 real agents (`0master`–`9git`)
- Per-agent chat with history, voice input (Web Speech API), per-agent LLM selector
- Per-agent Logs tab: colour-coded, badge count, debounced auto-save to `docs/agents/<id>.log.md`
- Agent Doc tab: fetches real `.github/agents/*.agent.md` on mount, renders as formatted Markdown
  (YAML frontmatter card, headings, bold/italic, inline code, fenced code blocks, bullet lists)
- Edit/Preview toggle — Edit mode opens raw textarea; auto-saves edits back to disk (2 s debounce)
- Pipeline bar with Run/Stop/Reset; status bar; `INITIAL_DOCS` embedded stubs fully removed

### `web/vite.config.ts`
- `vite-agent-docs` plugin intercepts `GET /api/agent-doc/:id` and `PUT /api/agent-doc/:id`
  at the Vite dev-server layer, serving `.github/agents/` content without needing the FastAPI backend

### `backend/app.py`
- `AgentDocBody` Pydantic model
- `GET /api/agent-doc/{agent_id}` — reads `.github/agents/<id>.agent.md`
- `PUT /api/agent-doc/{agent_id}` — writes back with path-traversal protection via `_VALID_AGENT_IDS` allowlist

### `start.ps1`
- `Get-PortPid` — finds the PID listening on a given TCP port via `netstat -ano`
- `Assert-PortFree` — kills the stale holder and waits for socket release before launching each service
- Prevents `[Errno 10048] address already in use` on restart/start

## Acceptance Criteria
- [x] Zero TypeScript errors in `CodeBuilder.tsx` and `vite.config.ts`
- [x] Agent Doc tab displays rendered Markdown (not a download prompt)
- [x] Docs loaded from actual `.github/agents/*.agent.md` files
- [x] Edit/Preview toggle works; edits auto-saved to disk
- [x] Backend doc endpoints added and validated (no Python linter errors)
- [x] `start.ps1 start` auto-kills stale port holders
- [x] `.pyagent.pids` added to `.gitignore`

## Legacy Project Overview Exception
This project overview predates the modern project identity template introduced after prj0000046 was created and committed. It uses the pre-modern layout (Status / Branch Plan / Scope Boundary) and does not carry a modern Project Identity section. No corrective migration is required for this legacy file; future projects must use the modern template. Ownership: @0master (documented), @1project (template compliance going forward).

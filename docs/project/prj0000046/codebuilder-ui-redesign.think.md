# codebuilder-ui-redesign — Think Notes
_Agent: @2think | Status: COMPLETE_

## Problem Statement

The existing `web/apps/CodeBuilder.tsx` was a read-only demo with six hard-coded simulated agents
that bore no relationship to the actual PyAgent swarm. It had no real I/O, no connection to the
agent documentation files, and no way to interact with actual LLMs or observe runtime behaviour.

Key gaps identified:
1. **Wrong agent count** — 6 agents vs. the real 10 (`0master`–`9git`).
2. **No real docs** — embedded markdown stubs disconnected from `.github/agents/*.agent.md`.
3. **No persistence** — logs and edits vanished on reload.
4. **No interactivity** — text input, voice, and per-agent LLM selection were absent.
5. **Port collision** — `start.ps1` crashed with `WinError 10048` if a stale process held a port.

## Alternatives Considered

### Option A — Patch the existing component
Add agents 7–10 and wire a fetch for doc content. Minimally invasive but leaves the architectural
debt intact: hardcoded stubs, no log persistence, no voice, no LLM selector.

### Option B — Full rewrite (chosen)
Replace the entire component with a purpose-built 10-agent pipeline UI that:
- Loads real docs from `.github/agents/` via the backend or Vite plugin
- Persists logs to `docs/agents/<id>.log.md`
- Supports voice input, per-agent LLM selection, Edit/Preview for docs

### Option C — Separate app route
Create a new `/agents` route and leave `CodeBuilder` as-is.
Rejected: adds route complexity without retiring the broken component.

## Key Decisions

1. **Vite plugin over backend-only fetching** — agent docs must load even when the FastAPI backend
   (port 444) is not running. A Vite `configureServer` middleware handles `GET/PUT /api/agent-doc/:id`
   directly from disk, falling through to the proxy when the backend is live.

2. **Local `MarkdownView` component** — no `react-markdown` dependency introduced. A lightweight
   (~80-line) recursive renderer handles all markdown structures present in the agent files:
   YAML frontmatter card, ATX headings (h1–h3), bold/italic inline, backtick code,
   fenced code blocks, bullet lists, horizontal rules.

3. **Debounced auto-save (2 s)** — edits to both logs and docs are flushed to disk via `PUT`
   requests 2 seconds after the last change. The doc save is gated behind `docsLoading` to
   prevent overwriting real files with the empty default state during mount.

4. **`_VALID_AGENT_IDS` allowlist** — path traversal protection in the backend uses a `frozenset`
   of the 10 valid agent IDs checked before any filesystem operation.

5. **Per-agent LLM selector** — placed in each agent's panel header rather than a global toolbar,
   allowing different agents to use different models within the same session.

6. **`Assert-PortFree` in `start.ps1`** — kills stale port holders via `netstat -ano` + `Stop-Process`
   before each service launch, making `.\start.ps1 start` idempotent.

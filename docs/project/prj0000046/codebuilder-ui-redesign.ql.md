# codebuilder-ui-redesign — Security / CodeQL Review
_Agent: @8ql | Status: COMPLETE_

## Threat Surface

| Surface | Description |
|---------|-------------|
| `GET /api/agent-doc/{agent_id}` | Reads a file from `.github/agents/` |
| `PUT /api/agent-doc/{agent_id}` | Writes a file to `.github/agents/` |
| `vite-agent-docs` plugin | Node `fs` reads/writes `.github/agents/` at dev time |
| `Assert-PortFree` | Reads `netstat` output; calls `Stop-Process` |

## Path Traversal (OWASP A01 / CWE-22)

**Backend:**
`agent_id` is validated against `_VALID_AGENT_IDS` (a Python `frozenset`) before any filesystem
operation. No string concatenation into a path until after validation passes.

```python
if agent_id not in _VALID_AGENT_IDS:
    raise HTTPException(status_code=400, detail=f"Unknown agent_id: {agent_id!r}")
path = _AGENTS_DIR / f"{agent_id}.agent.md"   # safe: agent_id is one of 10 known values
```

**Vite plugin (dev-time only):**
Same `VALID` set applied:
```typescript
const VALID = new Set(['0master','1project','2think','3design','4plan','5test','6code','7exec','8ql','9git']);
if (!VALID.has(agentId)) { next(); return; }
```

**Verdict:** ✅ Path traversal mitigated.

## Injection (OWASP A03)

- No SQL in this component.
- `start.ps1` `Assert-PortFree`: PID parsed from `netstat` output with regex `(\d+)$`; passed
  directly to `Stop-Process -Id` as an integer. No shell interpolation.
- Vite plugin: file path constructed from validated `agentId` only — no user-supplied segments.

**Verdict:** ✅ No injection vectors.

## XSS (OWASP A03)

`MarkdownView` renders into React JSX — all string segments are passed as React `children`
(escaped automatically by React's reconciler). No `dangerouslySetInnerHTML` used anywhere.

**Verdict:** ✅ XSS not possible via doc content.

## Sensitive Data Exposure (OWASP A02)

- `.pyagent.pids` added to `.gitignore` — runtime PID file not committed to VCS.
- Agent docs (`.github/agents/*.agent.md`) are configuration, not secrets. They are already in VCS.
- No API keys, tokens, or secrets introduced.

**Verdict:** ✅ No sensitive data exposure.

## SSRF (OWASP A10)

The frontend fetches `/api/agent-doc/:id` — a relative URL, no user-controlled host.
No URL construction from user input.

**Verdict:** ✅ No SSRF vector.

## Authentication / Access Control (OWASP A01, A07)

The `PUT /api/agent-doc/{agent_id}` endpoint has no authentication. This is an acceptable
**dev-only** risk: the backend binds to `localhost`/`0.0.0.0` on the dev machine, not exposed
to the internet. Production deployments must add authentication before exposing this endpoint.

**Known gap:** Add token or session auth to `PUT /api/agent-doc` and `PUT /api/agent-log`
before any non-local deployment.

## Dependency Audit

No new npm or Python packages introduced. `lucide-react` (existing), `react` (existing).
`fs` and `path` in `vite.config.ts` are Node built-ins — no install, no CVE surface.

## Summary

| Check | Result |
|-------|--------|
| Path traversal | ✅ Mitigated via allowlist |
| Injection (shell, SQL) | ✅ Not applicable / safe |
| XSS | ✅ React JSX escaping |
| Sensitive data in VCS | ✅ `.pyagent.pids` gitignored |
| SSRF | ✅ No user-controlled URL |
| Auth on write endpoints | ⚠️ Dev-only risk — must add auth for production |

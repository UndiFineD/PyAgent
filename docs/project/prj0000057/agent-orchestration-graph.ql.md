# agent-orchestration-graph — QL / Security Notes
_Owner: @8ql | Status: DONE_

## Security Review

### OWASP Top 10 Checklist

| Risk | Status | Notes |
|---|---|---|
| A01 Broken Access Control | ✅ OK | Backend endpoint behind `require_auth`; agent_id validated against allowlist |
| A02 Cryptographic Failures | ✅ N/A | No crypto in this feature |
| A03 Injection | ✅ OK | Log content shown as text — no dangerouslySetInnerHTML or eval() |
| A04 Insecure Design | ✅ OK | Polling at 3s; no infinite retry on error; cleanup on unmount |
| A05 Security Misconfiguration | ✅ OK | Uses existing CORS config; no new endpoints added |
| A06 Vulnerable Components | ✅ OK | No new JS/Python dependencies |
| A07 Auth Failures | ✅ OK | Reads from localStorage `nebula-api-key` — existing auth pattern |
| A08 Data Integrity Failures | ✅ OK | Read-only polling; no server-side state mutation |
| A09 Logging Failures | ✅ N/A | No new logging endpoints |
| A10 SSRF | ✅ OK | Fetch targets are relative paths — no user-controlled URLs |

### Static Analysis Notes
- No `eval()`, `Function()`, `innerHTML`, or `dangerouslySetInnerHTML` in new code
- Regex pattern `prj\d{7}` is safe — fixed structure, no backtracking bomb
- `inferStatus()` does only string inclusion checks — no eval or exec paths
- Test file imports from FastAPI TestClient — standard, safe test pattern

## CodeQL
No new CWEs introduced. Component is purely read-only polling with text display.

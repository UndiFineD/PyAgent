# agent-memory-persistence — Security Review

_Owner: @8ql_

## OWASP Top 10 review

| Risk | Assessment |
|---|---|
| A01 Broken Access Control | All endpoints behind `require_auth`; agent_id path param does not expose cross-agent data if token is validated per-agent (MVP: any valid token can access any agent — acceptable for internal tool) |
| A02 Cryptographic Failures | Memory stored as plaintext JSON; no PII expected in MVP. If PII is added later, encryption at rest should be added. |
| A03 Injection | `agent_id` used as directory path component — must be sanitized to prevent path traversal. **Action: validate `agent_id` matches `^[a-zA-Z0-9_-]+$` before use in path.** |
| A04 Insecure Design | Append-only log with clear; per-agent lock prevents concurrent corruption |
| A05 Security Misconfiguration | No new config surface |
| A06 Vulnerable Components | No new dependencies |
| A07 Auth Failures | Uses existing `require_auth` |
| A08 Data Integrity | JSON round-trip; no deserialization of untrusted class instances |
| A09 Logging Failures | Uses structured logging from prj0000063 |
| A10 SSRF | No outbound requests |

## Required fix before merge

- `agent_id` path traversal: add regex validation in endpoint or MemoryStore._path():
  ```python
  import re
  if not re.match(r'^[a-zA-Z0-9_-]+$', agent_id):
      raise ValueError(f"Invalid agent_id: {agent_id}")
  ```

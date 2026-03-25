# live-agent-execution-in-codebuilder — Security / QL Notes
_Owner: @8ql | Status: DONE_

## OWASP Top 10 Review

### A01 — Broken Access Control
- Both `/api/pipeline/run` and `/api/pipeline/status/{pipeline_id}` are on
  `_auth_router` which requires `require_auth`. No unauthenticated access.
- `pipeline_id` is a UUID4 — not guessable; acts as an unguessable token for
  the pipeline resource.

### A02 — Cryptographic Failures
- No sensitive data stored in pipeline records. Task text is user-supplied
  plaintext — no encryption needed.

### A03 — Injection
- `pipeline_id` route parameter is used only as a dict key lookup.
  No SQL, file paths, or shell commands involved. Zero injection surface.
- Task text `body.task` is stored as-is (user's own data) and returned
  in GET response. No template rendering, no eval, no subprocess.

### A04 — Insecure Design
- In-memory store resets on server restart — clearly a demo design.
  Documented as such. Not suitable for production persistence without a
  persistent store (out of scope).

### A05 — Security Misconfiguration
- `_pipelines` is a module-level dict — standard Python pattern, not a
  security misconfiguration.

### A07 — Authentication Failures
- Auth handled by existing `require_auth` dependency. No bypass.

### A09 — Security Logging
- Pipeline creation is visible in normal FastAPI access logs.
  No PII in pipeline records; task text is user-supplied and expected.

## Static Analysis Notes

- No new `TODO: FIXME` or `noqa` suppressions introduced.
- Pydantic model `PipelineRunRequest` validates input at the framework level.
- No external HTTP calls made server-side.

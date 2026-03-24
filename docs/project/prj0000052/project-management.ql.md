# project-management — Security Scan Results

_Status: CLEARED_
_Scanner: @8ql | Updated: 2026-03-24_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| `backend/app.py` | OWASP input validation, path traversal, injection | manual + regex |
| `web/apps/ProjectManager.tsx` | XSS, open redirect, SSRF | manual |
| `data/projects.json` | data integrity | manual |

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| — | — | — | — | No findings |

## Security Notes

### `PATCH /api/projects/{id}`
- `project_id` validated against `^prj\d{7}$` allowlist regex before any lookup — no path traversal possible.
- Patch payload goes through Pydantic `ProjectPatch` model with `Literal` type constraints on `lane`, `priority`, `budget_tier` — no injection vector.
- Write is atomic: `.tmp` file written then `Path.replace()` — no partial-write corruption.
- No user-supplied file paths are accepted.

### `POST /api/projects`
- `id` field validated by the same `^prj\d{7}$` regex.
- Full `ProjectModel` Pydantic validation on all enum fields.
- Duplicate ID check returns 409 — no overwrite of existing entries.

### `web/apps/ProjectManager.tsx`
- All data rendered via React JSX — no `dangerouslySetInnerHTML`; XSS risk is nil.
- External links (`href`) are constructed from `GITHUB_PR_BASE` constant + a validated integer PR number — no open-redirect risk.
- `docs/project/` folder links use a constant base URL + the project `id` field (validated `prjNNNNNNN` format from API) — no SSRF.
- No credentials, tokens, or secrets handled on the client.

## False Positives
| ID | Reason |
|---|---|
| — | — |

## Cleared
Current status: CLEARED — no actionable findings.

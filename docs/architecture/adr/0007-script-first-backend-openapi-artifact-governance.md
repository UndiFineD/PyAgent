# ADR-0007 - Script-First Backend OpenAPI Artifact Governance

## Status

- Accepted

## Date

- 2026-04-03

## Owners

- @3design
- Reviewers: @4plan, @8ql

## Context

`backend/app.py` already exposes a FastAPI OpenAPI contract at runtime, but the repository does not persist that schema in a committed artifact. Existing documentation under `docs/api/*.md` is narrative and hand-authored, while `.github/workflows/ci.yml` currently runs lightweight checks only. The repository also contains other FastAPI applications whose import readiness differs from `backend.app`, so a repo-wide single-spec strategy would create unnecessary brittleness in phase one.

The project needs a reviewable, deterministic OpenAPI artifact for the backend worker without making pytest, CI, or MkDocs responsible for generation.

## Decision

Adopt a script-first, backend-only OpenAPI pipeline for phase one.

The chosen architecture is:
- `backend/app.py` remains the sole schema authority for this project.
- a dedicated generator script writes a committed JSON artifact to `docs/api/openapi/backend_openapi.json`.
- a narrow pytest selector verifies drift against `app.openapi()` in read-only mode.
- CI runs only the drift selector and never regenerates or commits the artifact.
- MkDocs publishes the committed file because it lives under `docs/`, but MkDocs does not own generation.

## Alternatives considered

### Alternative A - Pytest-owned golden file updates

- Summary: use pytest update mode to regenerate the committed schema artifact.
- Why not chosen: it conflates verification with artifact production and makes routine test runs harder to reason about.

### Alternative B - CI-only ephemeral artifact generation

- Summary: generate OpenAPI only in CI and publish it as a workflow artifact.
- Why not chosen: it removes normal pull-request reviewability and delays drift visibility until after push.

### Alternative C - MkDocs-owned generation

- Summary: import `backend.app` during docs builds and generate the schema as part of `mkdocs build`.
- Why not chosen: it couples docs publication to backend import side effects and expands blast radius beyond the current lightweight CI model.

## Consequences

### Positive

- The backend contract becomes reviewable in ordinary Git diffs.
- Generation, verification, and publication ownership stay separated and easier to reason about.
- The docs tree gains a publishable static JSON asset without replacing narrative documentation.
- Future expansion to multiple specs remains possible through the `docs/api/openapi/` directory.

### Negative / Trade-offs

- Contributors must remember to rerun a generation command when routes or schemas change.
- `backend.app` import side effects remain a dependency for both generation and drift checks.
- Phase one deliberately excludes other FastAPI apps, so the repository still lacks a unified multi-app API contract.

## Implementation impact

- Affected components: `backend/app.py` as schema source, a new generator script under `scripts/`, a committed JSON artifact under `docs/api/openapi/`, a narrow pytest drift test, and a small CI workflow update.
- Migration/rollout notes: introduce the generator first, then commit the initial artifact, then add the drift test and CI enforcement.
- Backward compatibility notes: narrative docs remain intact; no runtime endpoint behavior changes are required for phase one.

## Validation and monitoring

- Tests or checks required: docs policy pytest selector, architecture governance validation, and a narrow pytest drift selector once implementation exists.
- Runtime signals or metrics to monitor: none in phase one; this is a build-time and repository-governance concern.
- Rollback triggers: repeated instability from `backend.app` import side effects or contributor confusion that cannot be resolved with a deterministic generation command.

## Related links

- Related project artifact(s): `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.think.md`, `docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.design.md`
- Related architecture docs: `docs/architecture/adr/0001-architecture-decision-record-template.md`
- Supersedes/Superseded-by (if any): none
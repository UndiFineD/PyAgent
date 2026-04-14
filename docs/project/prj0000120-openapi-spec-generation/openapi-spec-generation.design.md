# openapi-spec-generation - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-03_

## Selected Option
Option A: script-first committed backend schema with pytest drift enforcement and lightweight CI verification.

This design matches the project convergence decision and keeps phase one intentionally narrow:
- `backend/app.py` is the only schema authority in scope.
- schema generation is an explicit maintainer action, not a side effect of pytest, CI, or MkDocs.
- the committed artifact is reviewable in normal pull requests.
- MkDocs remains a publication consumer of the committed file instead of the generator.

## Problem Statement and Goals
The repository already exposes a FastAPI OpenAPI surface from `backend/app.py`, but that contract only exists at runtime. The design goal is to add a deterministic, committed OpenAPI artifact for the backend worker, verify drift with a narrow pytest selector, and expose the artifact through the existing docs tree without coupling every FastAPI app in the repository into a single generation workflow.

Phase-one goals:
- produce one committed backend schema artifact from `backend/app.py`
- make regeneration explicit and deterministic
- fail CI when the committed artifact drifts from `app.openapi()`
- preserve the current narrative `docs/api/*.md` pages as the human-readable layer

## Architecture
### High-Level Flow
1. A maintainer runs a dedicated repository script from the project root.
2. The script imports `backend.app`, calls `app.openapi()`, and writes a canonical JSON artifact.
3. The artifact is committed under the docs tree so it is both reviewable in Git and publishable by MkDocs as a static file.
4. A narrow pytest selector re-imports `backend.app`, regenerates the schema in memory, and compares it against the committed artifact using deterministic JSON serialization.
5. CI runs only the drift selector. CI never regenerates or commits the artifact.
6. Narrative API docs can link to the published JSON artifact, but MkDocs does not own generation.

### Component Responsibilities
| Component | Responsibility | Phase-one rule |
|---|---|---|
| `backend/app.py` | authoritative FastAPI schema source | only backend app in scope |
| `scripts/generate_backend_openapi.py` | explicit maintainer generation entrypoint | writes artifact; no test ownership |
| `docs/api/openapi/backend_openapi.json` | canonical committed schema artifact | deterministic JSON, committed to Git |
| `tests/docs/test_backend_openapi_drift.py` | read-only drift verification | compares generated vs committed schema |
| `.github/workflows/ci.yml` | lightweight enforcement | runs narrow pytest selector only |
| `docs/api/index.md` | narrative publication entrypoint | links to artifact; does not generate it |

## Intended Artifact Location
| Item | Path | Rationale |
|---|---|---|
| generation script | `scripts/generate_backend_openapi.py` | explicit, repository-level maintainer command |
| committed schema artifact | `docs/api/openapi/backend_openapi.json` | docs-adjacent, publishable by MkDocs, leaves room for future multi-spec files |
| drift check | `tests/docs/test_backend_openapi_drift.py` | narrow contract gate tied to the published artifact |

The artifact path is intentionally inside `docs/` so MkDocs can publish it as a static asset without becoming the generator. The `openapi/` subdirectory also leaves a clean future expansion path such as `github_webhook_openapi.json` or `chat_api_openapi.json` if later projects intentionally expand scope.

## Generation Flow
### Maintainer Command Contract
The canonical phase-one command is:

```powershell
python scripts/generate_backend_openapi.py
```

Expected behavior:
- import `backend.app` from the repository root
- call `app.openapi()` exactly once for the generation payload
- serialize the result to `docs/api/openapi/backend_openapi.json`
- write canonical JSON formatting with stable ordering for reviewable diffs
- exit non-zero if import or file write fails

### Serialization Contract
The script and drift test must treat semantic content as authoritative and allow only formatting-level normalization:
- canonical format: UTF-8 JSON with newline terminator
- key ordering: sorted for deterministic diffs
- indentation: stable human-reviewable output
- semantic fields: preserved exactly as produced by `app.openapi()`

No phase-one normalization may drop paths, schema fields, tags, examples, descriptions, or OpenAPI metadata.

## Drift-Check Strategy
The drift check is a read-only pytest selector that:
- loads `docs/api/openapi/backend_openapi.json`
- imports `backend.app`
- computes `app.openapi()` in memory
- serializes both payloads with the same canonical sort/format rules
- fails on any semantic difference

This check is intentionally narrow. It does not:
- regenerate files during normal test runs
- update the artifact in place
- run a docs build
- import `src/github_app.py` or `src/chat/api.py`

## CI Touch Points
Phase one touches only the existing lightweight workflow in `.github/workflows/ci.yml`.

Required CI behavior:
- add one step in the quick job to run `pytest tests/docs/test_backend_openapi_drift.py -q`
- keep the check read-only
- fail the job on drift
- avoid adding `mkdocs build` ownership to the quick path

The design explicitly defers any broader docs build or release-publication workflow. If a later project wants `mkdocs build --strict`, it should be introduced as a separate docs-quality lane after the schema pipeline is stable.

## Docs and Publication Relationship
MkDocs already publishes narrative API docs from `docs/api/*.md`. Phase one keeps that model.

Publication contract:
- `docs/api/index.md` may link to `openapi/backend_openapi.json`
- the JSON artifact is published because it resides under `docs/`
- narrative pages remain hand-authored and can summarize or reference the generated contract
- MkDocs must not invoke schema generation as part of `mkdocs build`

This keeps ownership boundaries clear:
- generation owner: explicit script
- verification owner: pytest + CI
- publication owner: existing MkDocs static docs pipeline

## Interfaces & Contracts
| Interface ID | Contract | Planned implementation anchor |
|---|---|---|
| `IFACE-OAS-001` | `backend.app:app` is the only phase-one schema authority. | `PT-OAS-001` |
| `IFACE-OAS-002` | `scripts/generate_backend_openapi.py` provides the canonical generation entrypoint and writes no files outside `docs/api/openapi/backend_openapi.json`. | `PT-OAS-001` |
| `IFACE-OAS-003` | `docs/api/openapi/backend_openapi.json` is a committed artifact with deterministic JSON serialization and no semantic field stripping. | `PT-OAS-002` |
| `IFACE-OAS-004` | `tests/docs/test_backend_openapi_drift.py` is read-only and compares canonicalized JSON output from `app.openapi()` against the committed artifact. | `PT-OAS-003` |
| `IFACE-OAS-005` | `.github/workflows/ci.yml` runs only the narrow drift selector for this feature and does not generate artifacts. | `PT-OAS-004` |
| `IFACE-OAS-006` | `docs/api/index.md` links to the committed artifact; MkDocs publishes it as a static file but does not generate it. | `PT-OAS-005` |
| `IFACE-OAS-007` | Secondary FastAPI apps remain explicitly excluded from phase one and must not be imported by generation or drift checks. | `PT-OAS-006` |

## Acceptance Criteria
| AC ID | Requirement | Verification signal | Interface linkage |
|---|---|---|---|
| `AC-OAS-001` | A single explicit generator command exists for backend-only schema production. | `python scripts/generate_backend_openapi.py` exits `0` and updates only the committed artifact path when schema changes exist. | `IFACE-OAS-001`, `IFACE-OAS-002` |
| `AC-OAS-002` | The committed artifact lives at `docs/api/openapi/backend_openapi.json` with deterministic JSON formatting. | Git diff shows stable ordering-only formatting and no writes outside the declared artifact path. | `IFACE-OAS-002`, `IFACE-OAS-003` |
| `AC-OAS-003` | Drift detection is read-only and fails on semantic mismatch. | `pytest tests/docs/test_backend_openapi_drift.py -q` passes when artifact is fresh and fails when artifact content is manually altered. | `IFACE-OAS-003`, `IFACE-OAS-004` |
| `AC-OAS-004` | CI enforcement stays lightweight and does not perform generation or MkDocs builds. | Quick workflow step executes only the narrow pytest selector and fails closed on drift. | `IFACE-OAS-004`, `IFACE-OAS-005` |
| `AC-OAS-005` | Docs publication remains consumer-only. | `docs/api/index.md` references the JSON artifact and `mkdocs.yml` requires no generation-specific logic. | `IFACE-OAS-005`, `IFACE-OAS-006` |
| `AC-OAS-006` | Phase-one scope remains backend-only. | Generator and drift test code paths import `backend.app` only; no `src/github_app.py` or `src/chat/api.py` imports appear in the lane. | `IFACE-OAS-001`, `IFACE-OAS-007` |
| `AC-OAS-007` | The design remains handoff-ready for implementation without broad open questions. | Canonical design contains artifact path, command contract, CI touch point, docs relationship, exclusions, and interface-to-task traceability. | all |

## Interface-to-Task Traceability
This block defines the minimum implementation anchors that `@4plan` must refine into executable tasks.

| Planned task ID | Expected implementation focus | Interfaces covered |
|---|---|---|
| `PT-OAS-001` | add backend-only generation script entrypoint and import contract | `IFACE-OAS-001`, `IFACE-OAS-002` |
| `PT-OAS-002` | add committed artifact path and deterministic serializer behavior | `IFACE-OAS-002`, `IFACE-OAS-003` |
| `PT-OAS-003` | add read-only pytest drift check | `IFACE-OAS-003`, `IFACE-OAS-004` |
| `PT-OAS-004` | wire lightweight CI drift enforcement | `IFACE-OAS-004`, `IFACE-OAS-005` |
| `PT-OAS-005` | link narrative docs to published artifact without moving generation into MkDocs | `IFACE-OAS-006` |
| `PT-OAS-006` | encode backend-only scope guard and secondary-app exclusions | `IFACE-OAS-007` |

## Non-Functional Requirements
- Performance: local generation and drift verification must stay narrow enough for routine contributor use and lightweight CI execution.
- Security: generation and drift checks must not require secrets, network access, or writes outside the declared artifact path.
- Testability: the drift check must be independently runnable with a single pytest selector.
- Maintainability: artifact naming and directory layout must support future multi-spec expansion without renaming the phase-one file.

## Risks and Rollback
| Risk | Impact | Mitigation | Rollback trigger |
|---|---|---|---|
| `backend.app` import side effects make generation noisy or unstable | medium | keep scope to one backend app, document explicit command, avoid coupling to docs build | generator or drift test fails consistently in clean CI/local environments |
| contributors forget to regenerate the artifact | high | drift test fails closed in CI and locally | repeated drift failures despite clear command documentation |
| schema publication expands prematurely to other FastAPI apps | medium | explicit backend-only scope contract and exclusions | any implementation proposal requiring multi-app imports in this project |

Rollback posture:
- remove CI selector and generator only if backend import side effects prove unmanageable in phase one
- retain narrative docs regardless of schema automation outcome
- defer broader API-contract automation to a follow-on project instead of broadening this lane

## Exclusions and Deferred Items
Excluded from phase one:
- generating schemas for `src/github_app.py`
- generating schemas for `src/chat/api.py`
- aggregating multiple FastAPI apps into one OpenAPI document
- moving generation into pytest update mode
- making MkDocs own generation
- adding `mkdocs build --strict` to the current quick CI job
- enriching FastAPI metadata beyond what `backend.app` already exposes, unless required for deterministic generation

Deferred items for later projects:
- multi-spec directory expansion for additional FastAPI surfaces
- stricter documentation build enforcement
- downstream consumers such as SDK generation or rendered OpenAPI reference pages

## ADR Impact
This design introduces an architecture decision and requires ADR coverage.

- ADR file: `docs/architecture/adr/0007-script-first-backend-openapi-artifact-governance.md`
- ADR scope: backend-only committed OpenAPI artifact generation ownership, drift enforcement, and docs publication separation

## Open Questions
None for phase-one design handoff. Future expansion to additional FastAPI apps is intentionally deferred instead of left ambiguous.
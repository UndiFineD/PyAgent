# openapi-spec-generation - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-03_

## Root Cause Analysis
- FastAPI already generates OpenAPI for `backend/app.py` through the default `.openapi()` method and default `/openapi.json` route, but the repository does not persist that schema anywhere. Runtime inspection in the project venv produced `backend_paths=56` and `backend_schemas=17`.
- The current idea text is partially stale. `docs/api/index.md` is no longer a mkdocstrings placeholder; prior project work in `docs/project/archive/prj0000073/prj0000073.think.md` and `docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md` established a hand-curated API reference plus MkDocs nav entries.
- The actual gap is now machine-readable contract drift prevention, not initial human-readable docs creation. `mkdocs.yml` already publishes `docs/api/*`, but `.github/workflows/ci.yml` does not run `mkdocs build` and no workflow validates a committed OpenAPI artifact.
- Importing `backend.app` for schema generation is feasible but not side-effect free. It emits dev-mode auth warnings, backend startup logs, initializes tracing, and loads `docs/project/kanban.json` at import time.
- The repository contains additional FastAPI apps in `src/github_app.py` and `src/chat/api.py`. `src/chat/api.py` failed to import in the current workspace probe because `chat.models` is not importable from the repository root. A repo-wide single-spec strategy would therefore be brittle on day one.

## Current-State Evidence

### Repository Evidence
| Evidence type | Path | Observation |
|---|---|---|
| Main backend app | `backend/app.py` | `app = FastAPI(title="PyAgent Backend Worker", version="0.1.0")` with no custom `openapi_url`, `docs_url`, or `redoc_url`; default FastAPI OpenAPI behavior applies. |
| Secondary FastAPI app | `src/github_app.py` | Separate webhook app with its own schema surface and title. |
| Tertiary FastAPI app | `src/chat/api.py` | Separate chat API; current import path is not ready for the same generation workflow as `backend/app.py`. |
| Docs publication | `mkdocs.yml` | API nav already points at `docs/api/index.md`, `authentication.md`, `rest-endpoints.md`, `websocket.md`, and `errors.md`. |
| CI reality | `.github/workflows/ci.yml` | Quick checks run pre-commit, placeholder smoke, and Rust benchmark smoke only; no MkDocs or OpenAPI validation step exists. |
| Existing docs guardrail | `tests/docs/test_api_docs_exist.py` | Canaries enforce presence and minimum content for human-written `docs/api/*`, not schema parity. |

### Prior Art
- `docs/project/archive/prj0000073/prj0000073.think.md` chose a hybrid documentation model: use FastAPI schema as a source of truth for shapes, but keep narrative docs hand-crafted.
- `docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md` shows `docs/api/*` and backend route changes already move together when endpoint contracts change.
- `docs/project/archive/prj0000076/prj0000076.think.md` tracks both idea000021 and idea000031 and confirms the long-running gap was undiscoverable API docs plus missing build validation.

### External Evidence
- FastAPI GitHub docs (`docs/en/docs/how-to/extending-openapi.md`) confirm that `.openapi()` is the normal generation path, it uses `app.routes`, and `app.openapi_schema` can be cached or overridden.
- FastAPI GitHub docs (`docs/en/docs/tutorial/metadata.md`) confirm `/openapi.json` is the default route unless `openapi_url` is changed and that docs URLs are configurable but optional.
- MkDocs GitHub README confirms MkDocs is a static-site generator built from Markdown and YAML config, which supports publication of generated or hand-curated API artifacts but does not itself solve schema extraction.

## Constraints
- Must remain on branch `prj0000120-openapi-spec-generation` and only update discovery-scope artifacts in this phase.
- Must not require application runtime services, secrets, or database access merely to verify schema freshness.
- Must not make docs publication depend on importing every FastAPI app in the repo, because current secondary surfaces do not share the same import readiness.
- Must keep CI cost low enough to fit the current lightweight workflow design in `.github/workflows/ci.yml`.
- Must preserve the existing hand-written `docs/api/*` narrative docs instead of replacing them with low-signal generated Markdown.

## Stakeholder Impact
- Backend maintainers: need a deterministic way to refresh a canonical schema when routes or models change.
- Docs maintainers: need a stable input that can be referenced from `docs/api/` and future docs automation without rewriting existing narrative docs.
- CI/release owners: need a fast drift signal that does not introduce brittle environment assumptions.
- Frontend and external integrators: benefit from a committed, reviewable contract artifact instead of runtime-only discovery.
- Owners of `src/github_app.py` and `src/chat/api.py`: affected only if a future design expands from backend-only to multi-spec publication.

## Options
### Option A - Script-first committed backend schema with test and CI verification
Create a dedicated generator script that imports `backend.app`, writes a committed `openapi.json` for that app only, and leaves `docs/api/*` as narrative documentation. A targeted pytest check validates the committed file against `app.openapi()`. CI runs the check but does not generate or commit artifacts.

**Task-type coverage**
- Literature review: aligns with existing hybrid docs precedent from `docs/project/archive/prj0000073/prj0000073.think.md`.
- Alternative enumeration: isolates generation ownership in a deterministic maintainer action rather than tests, CI, or MkDocs.
- Prior art search: follows the repository pattern where docs and backend changes move together (`docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.git.md`).
- Constraint mapping: respects lightweight CI and avoids repo-wide multi-app imports.
- Stakeholder impact: low blast radius for docs, backend, and CI owners.
- Risk enumeration: captured below with testability mapping.

**SWOT**
- Strengths: explicit source of truth; reviewable artifact diffs; easy local regeneration; clean separation between generation and verification.
- Weaknesses: committed artifact can drift if maintainers forget to regenerate it before commit.
- Opportunities: future docs pages can link directly to the JSON or render from it without changing the contract owner.
- Threats: generator may accidentally capture environment-specific data if import side effects leak into schema customization later.

**Security and operational risks**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Import side effects make generation noisy or non-deterministic | M | M | keep generator backend-only; sanitize env in script; avoid startup network calls | targeted pytest compares normalized JSON output |
| Maintainer forgets to refresh committed file | M | H | add drift test that fails when `app.openapi()` differs | CI pytest selector for OpenAPI drift |
| Schema accidentally includes deprecated aliases without intended guidance | M | M | document versioning/alias policy in generated metadata and docs references | assertion on expected path groups and metadata in test |

### Option B - Test-first golden file generation workflow
Make pytest the primary owner of the artifact by generating the schema inside tests and using a golden-file pattern for `openapi.json`. Local developers run the test in update mode to refresh the artifact; CI enforces parity.

**Task-type coverage**
- Literature review: fits the repository bias toward pytest-driven gates from `docs/setup.md`.
- Alternative enumeration: pushes ownership into tests instead of a dedicated script.
- Prior art search: differs from prior docs projects, which used documentation files and explicit operational commands instead of test-authored assets.
- Constraint mapping: still backend-only, but mixes verification and artifact production responsibilities.
- Stakeholder impact: raises burden on test maintainers and contributors unfamiliar with golden-update flows.
- Risk enumeration: captured below with testability mapping.

**SWOT**
- Strengths: strong drift enforcement once configured; single place for parity logic.
- Weaknesses: poor ergonomics for maintainers; tests become stateful when update mode is needed; harder to explain operationally.
- Opportunities: easy to normalize output before comparison.
- Threats: contributors may bypass or misunderstand update semantics, causing noisy failures.

**Security and operational risks**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Tests mutate tracked files in normal runs | M | H | require explicit update flag and fail-safe default read-only mode | CI ensures no file writes occur during normal selector |
| Golden-file normalization hides meaningful route changes | M | M | normalize only ordering/format, not semantic fields | unit tests for normalization helper |
| Developer experience becomes confusing and slows routine endpoint work | H | M | document exact update command and keep selector narrow | contributor dry-run command and failure messaging review |

### Option C - CI-first ephemeral generation without a committed schema
Generate the backend schema in CI only, upload it as an artifact, and optionally use it in later publish steps. The repository keeps narrative `docs/api/*` but not a tracked `openapi.json`.

**Task-type coverage**
- Literature review: matches the idea statement that CI could own verification, but diverges from existing reviewable artifact patterns.
- Alternative enumeration: removes local artifact ownership entirely.
- Prior art search: conflicts with prior docs work that values in-repo reviewability for API-facing changes.
- Constraint mapping: keeps working tree clean but makes local debugging harder.
- Stakeholder impact: shifts ownership mostly to CI/release maintainers.
- Risk enumeration: captured below with testability mapping.

**SWOT**
- Strengths: no committed generated file churn; clean repository diffs.
- Weaknesses: consumers cannot inspect the canonical schema in normal code review; local verification depends on CI parity.
- Opportunities: can be extended into release artifacts later.
- Threats: artifact visibility and retention are weaker than committed files for day-to-day development.

**Security and operational risks**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Contract drift is only visible after push | H | H | provide optional local generation helper anyway | pre-push or local smoke command parity |
| CI environment differences hide local import problems | M | M | keep a local import smoke command in docs | same python probe used locally and in CI |
| Artifact retention/publishing breaks discoverability | M | M | publish as named artifact and link from docs/release notes | CI artifact existence assertion |

### Option D - Docs-build-owned generation inside MkDocs workflow
Make `mkdocs build` responsible for importing the backend app, generating `openapi.json`, and optionally rendering derivative documentation during docs build.

**Task-type coverage**
- Literature review: leverages existing MkDocs nav and onboarding guidance, but not an established extraction path in the repo.
- Alternative enumeration: couples generation to documentation publication.
- Prior art search: stronger coupling than prior docs work in `prj0000073`, which explicitly kept narrative docs separate from build-time schema generation.
- Constraint mapping: most exposed to import-side effects and CI/docs environment drift.
- Stakeholder impact: highest blast radius across docs, CI, and backend owners.
- Risk enumeration: captured below with testability mapping.

**SWOT**
- Strengths: one command could validate docs publication and schema freshness together.
- Weaknesses: generation becomes unavailable without MkDocs dependencies; docs build failures block contract refresh.
- Opportunities: could eventually enable richer rendered API pages from the schema.
- Threats: docs build becomes brittle because importing `backend.app` already emits warnings/logs and repo-wide app discovery is not clean.

**Security and operational risks**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| MkDocs build becomes dependent on backend import side effects and env state | H | H | isolate generation from docs build or provide stable env defaults | `mkdocs build --strict` plus import smoke in CI |
| Expanding build to multiple FastAPI apps fails on unresolved imports like `src/chat/api.py` | H | M | explicitly scope docs build to backend app only | test that only backend spec target is invoked |
| Docs pipeline cost grows beyond current lightweight CI profile | M | M | move docs build to optional or separate job | dedicated docs job duration budget |

## Decision Matrix
| Criterion | Opt A Script-first | Opt B Test-first | Opt C CI-first | Opt D Docs-build-first |
|---|---|---|---|---|
| Reviewable committed artifact | High | High | Low | Medium |
| Local maintainer ergonomics | High | Medium | Medium | Low |
| CI cost fit with current workflow | High | Medium | Medium | Low |
| Exposure to import side effects | Medium | Medium | Medium | High |
| Compatibility with current `docs/api/*` model | High | Medium | Medium | Medium |
| Future extensibility to richer docs publication | High | Medium | Medium | High |
| Risk of hidden drift | Low | Low | Medium | Medium |

## Recommendation
**Option A - Script-first committed backend schema with test and CI verification.**

This is the best fit because it separates concerns cleanly:
- generation is an explicit maintainer action,
- verification is automated and cheap,
- CI stays lightweight,
- `docs/api/*` remains the narrative layer,
- and the project avoids coupling schema freshness to MkDocs or to repo-wide multi-app imports.

The recommended design handoff for `@3design` is:
1. Treat `backend/app.py` as the phase-one authority for a committed schema.
2. Add a dedicated generation command/script outside pytest.
3. Add a narrow pytest drift check that compares committed JSON with `backend.app.openapi()`.
4. Add a lightweight CI selector for that drift check, not a docs-build-owned contract.
5. Keep MkDocs as a publication consumer of the committed artifact or a linked reference, not the producer.

## Open Questions
- Should phase one explicitly exclude `src/github_app.py` and `src/chat/api.py`, or should `@3design` define a multi-spec directory layout from the start?
- Where should the committed backend schema live so it fits both developer review and docs publication best: `docs/api/openapi.json`, `backend/openapi.json`, or another docs-adjacent path?
- Should the drift test normalize ordering only, or preserve raw `app.openapi()` output byte-for-byte?
- Is a lightweight CI-only pytest selector sufficient, or does the repository want a separate docs job later for `mkdocs build --strict` once schema generation is in place?
- Should the generated schema include additional FastAPI metadata and tags now, or should metadata enrichment be deferred until the contract pipeline exists?
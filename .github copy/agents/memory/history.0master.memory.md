# PyAgent — Master Agent Memory

_Last updated: 2026-04-04_

**Next available prj:** see `data/nextproject.md`

---

## 2026-03-27 — prj0000089 agent-learning-loop — RELEASED ✅ PR #231
## 2026-04-04 — prj0000123 RELEASED ✅ PR #285 #286

- Post-merge hotfix for PR #284 CI drift (`test_ac_oas_003_drift_check_is_read_only_and_semantic`).
- Fix: narrow canonicalization in `tests/docs/test_backend_openapi_drift.py` stripping volatile `ValidationError`/`HTTPValidationError` schema internals.
- Commits: `ce50ffe3df` (artifact regeneration), `e09a9f3228` (test stabilization), `693c137c2a` (memory closure).
- PR #285 was merged before fix commit; PR #286 opened as replacement. CI green on #286; merged.
- Registry: registered in `data/projects.json` + `kanban.json` as Released; `nextproject.md` advanced to `prj0000124`.

## 2026-04-04 — prj0000122 — green-phase handoff pending (@6code)

- Full pipeline: @2think (Option A) → @3design (API-key bootstrap, opaque refresh tokens, file-backed session store) → @4plan (T-JRT-001 to T-JRT-009) → @5test (RED: 5 failing, `POST /v1/auth/session` 404).
- Implementation scope: `backend/auth_session_store.py` (new), `backend/auth.py`, `backend/app.py`.
- Next step: @6code green-phase (paused for prj0000123 hotfix; resume after prj0000124 is initialized).

## 2026-04-04 — prj0000121 RELEASED ✅ PR #281, prj0000120 RELEASED ✅ PR #280

- prj0000120: openapi-spec-generation — full pipeline; PR #280 merged; idea000021 archived.
- prj0000121: ci-setup-python-stack-overflow — hotfix for `actions/setup-python@v5` stack overflow; PR #281 merged.
- Registry closure via PR #282 on `prj0000121-ci-setup-python-stack-overflow`.

---


**Branch:** `prj0000089-agent-learning-loop`
**PR:** [#231](https://github.com/UndiFineD/PyAgent/pull/231) — **merged 2026-03-27**
**Status:** RELEASED — project docs and registry moved to Released after merge
**Priority:** P2 | **Budget:** M | **Tags:** agents, quality, process

**Deliverable:** Learning-loop governance rules added across all 10 role files, plus follow-up test/quality remediations that stabilized `pytest -v --maxfail=1` (1181 passed, 35 skipped). Kanban and projects registry updated to Released.

---

## 2026-03-26 — prj0000082 agent-execution-sandbox — DISCOVERY 🔍

**Branch:** `prj0000082-agent-execution-sandbox`
**Status:** DISCOVERY — @1project complete; project folder + 9 stubs created; 129 structure tests pass
**Priority:** P2 | **Budget:** S | **Tags:** security, sandbox, core
**Commits (so far):** `27e67365c` (kanban/projects.json), `1b0441373` (project.md), `1067b8395` (8 stubs)

**Deliverable scope:** `SandboxMixin` — per-agent allowlist for filesystem paths and network hosts; `SandboxViolationError` on unauthorized access; integrated with `StateTransaction`/`StorageTransaction` hooks in `src/core/base/mixins/`.

**@1project scope notes:** No existing sandbox code in `src/` — net-new module. Integration point: `src/core/base/mixins/`. Hook surface: `src/core/base/agent_state_manager.py`.

**Next:** Handoff to @2think for options exploration.

---

## 2026-03-26 — prj0000081 mcp-server-ecosystem — RELEASED ✅ PR #223

**Branch:** `prj0000081-mcp-server-ecosystem`
**PR:** [#223](https://github.com/UndiFineD/PyAgent/pull/223) — **merged 2026-03-26**
**Status:** RELEASED — full pipeline complete; PR #223 merged to main
**Priority:** P3 | **Budget:** L | **Tags:** tools, mcp, ecosystem

**Deliverable:** MCP server ecosystem: `McpClient` (JSON-RPC stdio), `McpRegistry` (hot-load lifecycle), `McpSandbox` (hardened subprocess — allowlist env, list-args, SHA-256 pin), `McpToolAdapter` (LLM tool bridge). 33/33 tests, 89.4% coverage, ruff clean, @8ql gate passed.

---

## 2026-03-26 — prj0000080 cort-reasoning-pipeline — RELEASED ✅ PR #221

**Branch:** `prj0000080-cort-reasoning-pipeline`
**PR:** [#221](https://github.com/UndiFineD/PyAgent/pull/221) — **merged 2026-03-26**
**Status:** RELEASED — full pipeline complete (@1project→@2think→@3design→@4plan→@5test→@6code→@7exec→@8ql→@9git)
**Priority:** P2 | **Budget:** M

**Deliverable:** Chain-of-Recursive-Thoughts reasoning pipeline: N-round recursive self-critique with M alternative chains per round (temperature-variant via `asyncio.gather`), pure-heuristic `EvaluationEngine` (Correctness 0.5 / Completeness 0.3 / Reasoning-depth 0.2), usable as `CortMixin` or standalone `CortAgent`. 33/33 tests, 97.4% coverage, ruff clean, OWASP clear.

**Key components:** `src/core/reasoning/{CortCore,CortAgent,EvaluationEngine,__init__}.py`

---

## 2026-03-26 — prj0000079 automem-hybrid-search — REVIEW 🔎 PR #220

**Branch:** `prj0000079-automem-hybrid-search`
**PR:** [#220](https://github.com/UndiFineD/PyAgent/pull/220) — open, awaiting review
**Status:** REVIEW — @1project→@6code→@9git complete; awaiting merge
**Priority:** P2 | **Budget:** L

**Deliverable:** 9-component AutoMem hybrid memory search (Vector+Graph+Temporal+Lexical) on PostgreSQL (pgvector HNSW + Apache AGE + tsvector); BenchmarkRunner; NebulaOS `AutoMemBenchmark.tsx` dashboard; full AppRegistry auto-discovery system (11 apps, 3 categories); asyncpg + pgvector added to requirements.txt.

---

## 2026-03-26 — prj0000078 pm-swot-risk-ui — RELEASED ✅ PR #219

**Branch:** `prj0000078-pm-swot-risk-ui`  
**PR:** [#219](https://github.com/UndiFineD/PyAgent/pull/219) — **merged 2026-03-26**  
**Status:** RELEASED — @1project→@4plan→@6code→@7exec→@8ql→@9git complete  
**Priority:** P3 | **Budget:** S

**Deliverable:** Two toolbar buttons ("SWOT" + "Risk") added to `FilterBar` in `web/apps/ProjectManager.tsx`. Clicking each opens a modal showing the corresponding section from `kanban.md` (Vite `?raw` build-time import). No backend changes.

**Next available prj:** prj0000089 — also written to `data/nextproject.md`

**prj0000079–prj0000088 allocated 2026-03-26** — 10 Ideas from `docs/architecture/archive` review: automem-hybrid-search, cort-reasoning-pipeline, mcp-server-ecosystem, agent-execution-sandbox, llm-circuit-breaker, immutable-audit-trail, shadow-mode-replay, universal-agent-shell, n8n-workflow-bridge, ai-fuzzing-security (read by Project Manager UI)

---

## 2026-03-26 — prj0000076 future-ideas-kanban — RELEASED ✅ PR #218

**Branch:** `prj0000076-future-ideas-kanban`
**PR:** [#218](https://github.com/UndiFineD/PyAgent/pull/218) — **merged 2026-03-26**
**Status:** RELEASED — @1project→@2think→@4plan→@9git complete; @3design/@5test/@6code/@7exec/@8ql SKIPPED (doc-only)
**Priority:** P3 | **Budget:** M

**Deliverable:** 38 improvement ideas written to `## Future Ideas` section in `docs/project/kanban.md`.

### ⚠️ P1 security findings from audit — need follow-up projects

| # | idea-ID | Finding | Recommended action |
|---|---|---|---|
| 1 | idea-001 | `rust_core/2026-03-11-keys.priv` private key committed to repo | New project: git-filter-branch secret removal + rotate key |
| 2 | idea-002 | `deploy/compose.yaml` references non-existent Dockerfile | New project: fix compose dep chain |
| 3 | idea-003 | `mypy.ini` `ignore_errors = True` disables type checking | New project: enable mypy + fix type errors |

### Idea count by priority
P1: 3 | P2: 11 | P3: 21 | P4: 3 — Total: 38

### Pre-commit blocker flagged by @9git
109 ruff errors in `src/` + `tests/` make the shared ruff pre-commit gate fail.  
→ Recommended as future project (prj0000078 candidate).

**Next available prj:** see `data/nextproject.md`

---

## 2026-03-26 — prj0000076 future-ideas-kanban — IN DISCOVERY

**Branch:** `prj0000076-future-ideas-kanban`
**Status:** DELEGATED → @1project (creating folder + project overview)
**Priority:** P3 | **Budget:** M

**Goal:** Full workspace audit to surface future improvement ideas; add a SWOT-prioritised idea table to `kanban.md` with priority, impact, urgency, and description columns.

**Acceptance criteria:**
- `docs/project/prj0000076/prj0000076.project.md` exists with branch plan
- `docs/project/prj0000076/prj0000076.think.md` populated with improvement ideas from workspace audit
- `kanban.md` gains a new `## Future Ideas` section (or equivalent) with SWOT-ranked rows
- All structure tests pass (shard 1 stays green)

**Scope boundary:**
- In scope: `docs/project/kanban.md`, `data/projects.json`, new prj0000076 folder, workspace audit for ideas
- Out of scope: implementing any of the surfaced ideas (those become future prj IDs)
- Expected branch: `prj0000076-future-ideas-kanban`

**Next:** @2think produces `.think.md` with audit findings → @3design → @4plan → @5test → @6code → @7exec → @8ql → @9git

---

## 2026-03-26 — prj0000077 ci-backend-deps — RELEASED ✅

**PRs:** [#216](https://github.com/UndiFineD/PyAgent/pull/216) (main fix) + [#217](https://github.com/UndiFineD/PyAgent/pull/217) (hotfix shard 1)
**Status:** MERGED — all 10 CI shards + CodeQL green

**Root cause:** Three backend runtime deps missing from `requirements.txt` caused `ModuleNotFoundError` at pytest collection time (shards 5,7,8,9,10 exit code 2). CodeQL QL query had dual `select` + nonexistent `getKey()` method. Race condition: kanban test count fix was pushed after PR #216 merged → required hotfix PR #217.

**Fixes delivered:**
- `requirements.txt`: `psutil>=5.9`, `PyJWT>=2.8`, `python-json-logger>=3.0`
- `codeql/codeql-custom-queries-python/example.ql`: single `eval()` detection query
- `.github/agents/data/0master.log.md`: restored proper markdown content
- `tests/structure/test_kanban.py`: counts updated 76→77 (PR #217)

**Lesson:** Always verify PR merge timing before pushing dependent commits. If CI starts and a merge is imminent, confirm inclusion before pushing a follow-up commit.

**Next available prj:** prj0000078

---

## 2026-03-26 — prj0000075 security/CI follow-up (commit 6191188cc)

**Branch:** `prj0000075-ci-simplification` | **PR:** #213 (open)
**Status:** PUSHED — CI re-run in progress. All local tests pass (142 CI+structure tests, flake8 clean).

**Fixes delivered in this session:**
- **Dependabot #49 (GHSA-4r2r-cf2h-4wgq, yamux 0.12.1):** Local fork `rust_core/p2p/libp2p-yamux/` removes yamux 0.12.x compat layer entirely. `Cargo.lock` now only contains yamux 0.13.10.
- **Dependabot #52 (picomatch method-injection):** `npm update picomatch` → 4.0.4 in `web/package-lock.json`; `npm audit` reports 0 vulnerabilities.
- **CodeQL alert #12:** Removed unused `Type` import from `web/apps/Editor.tsx`
- **CodeQL alert #13:** Removed unused `beforeEach`/`afterEach` imports from `web/hooks/useWebSocket.test.ts`
- **CodeQL Python job failure:** Fixed dual `from...select` blocks in `codeql/codeql-custom-queries-python/example.ql` — QL only allows one select per file; combined into single query using `or` with string message variable.
- **CI shard 2/3 failure:** Fixed `tests/structure/test_ci_yaml.py` W391 (our file) + pre-existing flake8 issues in 9 other test files (F401, W605, E402, F541).

---

## 2026-03-25 — prj0000075 CI Simplification

**Branch:** `prj0000075-ci-simplification`
**PR:** [#213](https://github.com/UndiFineD/PyAgent/pull/213) — open, awaiting merge
**Status:** REVIEW — all @1project–@9git stages complete; 165 tests pass; @8ql: no blocking findings

**Changes delivered:**
- 4 redundant workflows deleted (`core-quality`, `pm`, `quality`, `testing-infra`)
- `security.yml` created (CodeQL Python+JS, push/PR/weekly, minimal permissions)
- pre-commit lint fixes: I001, ruff config migration to `[tool.ruff.lint]`, D203/D213 conflict
- `docs/setup.md` — Local Testing section added
- Agent workflow improvements: `5test` + `6code` lint policy; `7exec` pre-commit gate; `8ql` redesigned (security-only → quality+security gate with lessons-learned loop)
- Lessons written to `6code.memory.md` + `8ql.memory.md`

**Project boundary:**
- Scope: `.github/workflows/*.yml` audit + `.pre-commit-config.yaml` expansion + `docs/` CI guidance update
- Out of scope: Python/Rust/TS source code, test files
- Expected branch: `prj0000075-ci-simplification`
- Next available prj: prj0000077

---

## 2026-03-25 — prj0000074 Workspace Meta Improvements

**Branch:** `prj0000074-workspace-meta-improvements`
**PR:** [#212](https://github.com/UndiFineD/PyAgent/pull/212) — open, awaiting merge
**Status:** COMPLETE — 842 tests pass, all 9 workflow artifacts created, PR open

**Changes:**
- 20 `*.memory.md` + `*.log.md` moved `docs/agents/` → `.github/agents/data/` via git mv; all references updated (agent defs, backend/app.py, tests, scripts)
- `5test.agent.md` + `6code.agent.md` — Google-style docstrings policy + ruff `D` codes
- `2think.agent.md` — 6 research task types + minimum depth guideline
- `docs/architecture/` restructured: 14 old files deleted, 4 numbered files created (`0overview`–`3projects`); ≤8 limit tested
- `docs/project/kanban.md` — Risk Register (5 rows) + SWOT Analysis appended
- Test updates: architecture naming test (new), kanban row counts 72→76, test_docs_exist path fix

**Next available prj:** prj0000077 (prj0000075 and prj0000076 reserved in Ideas)

---

## 2026-03-25 — prj0000073 API Documentation (MERGED — PR #210)

**Branch:** `prj0000073-api-documentation`
**PR:** [#210](https://github.com/UndiFineD/PyAgent/pull/210) — MERGED
**Status:** Released

---

## 2026-03-25 — prj0000071 Dark Mode Accessibility (MERGED — PR #211)

**Branch:** `prj0000071-dark-mode-accessibility`
**PR:** [#211](https://github.com/UndiFineD/PyAgent/pull/211) — MERGED
**Status:** Released

---

## 2026-03-25 — Four new projects allocated (prj0000073–076)

All four are in Discovery lane, branches created and pushed, @1project setup complete for each.

| ID | Name | Branch | Goal |
|---|---|---|---|
| prj0000073 | api-documentation | `prj0000073-api-documentation` | Proper API reference docs for all backend endpoints, WebSocket protocol, auth |
| prj0000074 | workspace-meta-improvements | `prj0000074-workspace-meta-improvements` | Agent file co-location, docstrings policy, architecture restructure, SWOT+risk in kanban, deeper @2think |
| prj0000075 | ci-simplification | `prj0000075-ci-simplification` | Audit/remove 5 GitHub workflow files; replace with pre-commit hooks |
| prj0000076 | future-ideas-kanban | `prj0000076-future-ideas-kanban` | Workspace audit → ≥20 future ideas table in kanban.md |

**Next step for each:** @2think begins on each branch.
**Next available prj:** prj0000077

---

## 2026-03-25 — prj0000072 WebSocket Reconnect Logic

**Branch:** `prj0000072-websocket-reconnect-logic`
**PR:** [#209](https://github.com/UndiFineD/PyAgent/pull/209) — open, awaiting merge
**Status:** COMPLETE — all 9 workflow artifacts created, Python 835 tests pass, 0 warnings

**Changes:**
- `web/hooks/useWebSocket.ts` — exponential backoff + full-jitter; `baseDelay`, `maxDelay`, `maxRetries`, `reconnectAttempts`; `reconnectDelay` deprecated as alias
- `web/hooks/useWebSocket.test.ts` — 9 Vitest tests (exports, formula, backwards-compat)
- `docs/project/prj0000072/` — 9 workflow artifacts: project, think, design, plan, test, code, exec, ql, git

**Lessons:** Full agent workflow (all 9 artifacts) must be completed on the project branch before git handoff, even for single-file changes. Branch gate (`git branch --show-current` → switch to project branch) must be the first action. Skipping artifacts from the prior session required retroactive creation on the correct branch.

**Next available prj:** prj0000073

---

## 2026-03-24 — prj0000054 Backend Authentication

**Branch:** `prj0000054-backend-authentication`
**PR:** [#192](https://github.com/UndiFineD/PyAgent/pull/192) — open, awaiting review
**Status:** COMPLETE — 4 commits pushed, PR open, kanban→Review

**Changes:**
- `backend/auth.py` — NEW: standalone auth module (API-key + JWT HS256, DEV_MODE, hmac.compare_digest, WS close 4401)
- `backend/app.py` — APIRouter pattern; all 8 protected endpoints require auth; `/health` exempt; WS auth via query params
- `backend/requirements.txt` — PyJWT>=2.8.0 added
- `tests/test_backend_auth.py` — 17 tests all passing (unit + integration)
- `docs/project/prj0000054/` — 9 artifacts complete
- `data/projects.json` + `docs/project/kanban.md` — prj0000054 → Review, pr=192

**Env vars:** `PYAGENT_API_KEY`, `PYAGENT_JWT_SECRET` (both unset → DEV_MODE, all requests pass)
**Lessons:** PyJWT not pre-installed (run `pip install PyJWT>=2.8.0`); project.md needs full modern template with `**Goal:**`, `**Scope boundary:**`, `**Handoff rule:**`, `**Failure rule:**` sub-fields in Branch Plan section.

**Next:** prj0000053 template fix on that branch before PR #191 merges; triage Ideas lane for prj0000055+

---

## 2026-03-24 — prj0000053 HMAC Webhook Verification

**Branch:** `prj0000053-hmac-webhook-verification`
**PR:** [#191](https://github.com/UndiFineD/PyAgent/pull/191) — open, awaiting review
**Status:** COMPLETE — pushed, PR open
**Note:** project.md may be missing modern template sub-fields (`**Scope boundary:**`, `**Handoff rule:**`, `**Failure rule:**`) — fix before merging PR #191.

---

## 2026-03-24 — prj0000052 Project Management

**Branch:** `prj0000052-project-management`
**PR:** [#190](https://github.com/UndiFineD/PyAgent/pull/190) — open, awaiting review
**Status:** COMPLETE — pushed, PR open, all 9 artifacts complete

**Changes:**
- `data/projects.json` — 62-entry machine-readable project registry
- `docs/project/kanban.md` — 7-lane Kanban board (single source of truth)
- `backend/app.py` — `GET /api/projects`, `PATCH /api/projects/{id}`, `POST /api/projects`
- `web/apps/ProjectManager.tsx` — editable NebulaOS Kanban app: drag-drop lane transitions, edit modal, new-project creation, folder path links
- `tests/structure/test_kanban.py` — 20 structure tests (all pass)
- Agent files updated: `0master.agent.md` + `1project.agent.md` with lifecycle board conventions

**Next:** prj0000053 (HMAC webhook verification) or triage Ideas lane

---

## 2026-03-23 — prj0000046 CodeBuilder UI Redesign

**Branch:** `prj0000046-codebuilder-ui-redesign`
**PR:** [#184](https://github.com/UndiFineD/PyAgent/pull/184) — open, awaiting review
**Status:** COMPLETE — pushed, PR open

**Changes:** Full rewrite of `web/apps/CodeBuilder.tsx` (10-agent pipeline, per-agent LLM selector, Logs tab, Agent Doc tab with Markdown renderer and edit/preview toggle, docs loaded from real `.github/agents/*.agent.md`). Vite plugin for agent doc serving. Backend `GET/PUT /api/agent-doc/{id}` endpoints. `start.ps1` port-free helpers. `.gitignore` addition.

**Notes:** prj0000043 and prj0000044 are absent from the project inventory — gap was pre-existing, not caused by this session.

---

---

## 2026-03-22 Session Summary — prj0000011–prj0000020 Implementation Wave COMPLETE

All 10 projects (prj0000011 through prj0000020) fully implemented and merged to `main`.

| Project | Branch | Code | Docs (9/9) | Status |
|---------|--------|------|------------|--------|
| prj0000011 | prj0000011-core-project-structure | ✅ | ✅ | MERGED |
| prj0000012 | prj0000012-deployment-operations | ✅ | ✅ | MERGED |
| prj0000013 | prj0000013-dev-tools-autonomy | ✅ | ✅ | MERGED |
| prj0000014 | prj0000014-dev-tools-capabilities | ✅ | ✅ | MERGED |
| prj0000015 | prj0000015-dev-tools-implementation | ✅ | ✅ | MERGED |
| prj0000016 | prj0000016-dev-tools-structure | ✅ | ✅ | MERGED |
| prj0000017 | prj0000017-dev-tools-utilities | ✅ | ✅ | MERGED |
| prj0000018 | prj0000018-documentation-assets | ✅ | ✅ | MERGED |
| prj0000019 | prj0000019-future-roadmap | ✅ | ✅ | MERGED |
| prj0000020 | prj0000020-github-import | ✅ | ✅ | MERGED |

**Known open gap (prj0000020):** HMAC webhook signature verification not yet implemented in `src/github_app.py`. Documented in `docs/project/prj0000020/github-import.ql.md`. Assign a follow-on sprint.

---

## 2026-03-21 Session Summary — Project Governance Closure Wave

All 42 projects have been surveyed and governance PRs created:

| PR | Branch | Projects | Status |
|---|---|---|---|
| #127 | prj037-tools-crdt-security | prj0000042 | open |
| #128 | prj0000002-core-system | prj0000002 | open |
| #129 | prj0000003-hybrid-llm-security | prj0000003 | open |
| #130 | prj0000039-conftest-typing-fixes | prj0000039 | open |
| #131 | prj0000041-flm | prj0000041 | open |
| #132 | prj0000009-community-collaboration | prj009,010,019,020,024,025,027,029,040 | open |
| #133 | prj0000011-core-project-structure | prj011-018,021-023,026,028,030-038 | open |
| #134 | prj0000001-async-runtime | prj0000001 | open |
| #135 | prj0000005-llm-swarm-architecture | prj0000005 | open (IN_PROGRESS: 13/16 tasks) |

**Previously merged:** prj0000004 (#123), prj0000006 (#124), prj0000007 (#125), prj0000008 (#126).

**prj0000005 remaining tasks:**
- `src/swarm/swarm_node.py` — minimal peer with ping/pong
- `tests/test_swarm_node.py`
- `scripts/run_swarm_demo.py`

---

## Standing Policy — Branch Isolation

- One `prjNNNNNNN` workstream maps to one branch. Project work must not piggyback on the active branch of another project.
- `@0master` assigns or validates the expected branch during project kickoff and ensures `@1project` records that branch, the scope boundary, and the git handoff rule in the project overview.
- `@9git` is expected to reject mixed-project changes, inherited branches, and broad staging guidance for project work.
- When branch hygiene fails, `@0master` owns the correction loop: update the governing guidance, return the task to the agent that owns the project boundary, and do not normalize the failure as an accepted workflow.

## Standing Policy — Project Numbering Ownership

- `@0master` owns `prjNNNNNNN` allocation, validation, and continuity tracking.
- Project numbering is part of the project boundary. A project is not fully defined until the assigned `prjNNNNNNN`, project folder, and expected branch agree.
- `@1project` must consume the identifier assigned by `@0master`. It must not invent, renumber, or resolve ambiguity on its own.
- Do not reuse old numbers or skip numbers casually. If a number is reserved, retired, skipped, or corrected, record the reason here before downstream handoff.
- If numbering is missing, conflicting, or ambiguous, stop the workflow and send the task back through `@0master` before project setup continues.

## Project Numbering Tracking

- Latest confirmed project folder in `docs/project/`: `prj0000042`.
- Project folder numbering migrated from 3-digit (`prj001`-`prj038`) to 7-digit (`prj0000001`-`prj0000042`).
- Legacy duplicate groups were resolved by assigning unique 7-digit identifiers during migration.
- `prj0000043` allocated 2026-03-22: `prj0000043-p2p-security-deps` — libp2p 0.49→0.56, 6 Dependabot CVEs. PR open.
- `prj0000044` allocated 2026-03-22: `prj0000044-transaction-managers` — add missing StorageTransaction/ProcessTransaction/ContextTransaction stubs for CI. PR #136 open.
- `prj0000045` allocated 2026-03-22: `prj0000045-transaction-managers-full` — full proper design of all four transaction managers (src/transactions/ package, BaseTransaction ABC, LLM context integration, encrypted storage, remote memory). **MERGED** — PR #137 squash-merged to main 2026-03-22. 317 tests pass, 4 skip, 0 fail.
- `prj0000046` allocated 2026-03-22: `prj0000046-flm-tps-benchmark` — FLM provider tokens-per-second benchmark script (`scripts/FlmTpsBenchmark.py`). Branch: `prj0000046-flm-tps-benchmark`. Includes accumulated session test fixes (sync loops, git.md sections, flake8, registry isolation). FLM backend offline at time of run; script ready for when server is available.
- `prj0000047` allocated: `prj0000047-conky-real-metrics` — Conky.tsx real CPU/memory/network IO via psutil. Branch: `prj0000047-conky-real-metrics`. PR #185 **MERGED**. psutil added to backend/requirements.txt; CI fully clean on main.
- `prj0000048` allocated 2026-03-23: `prj0000048-taskbar-config` — Add taskbar always-visible toggle to NebulaOS Settings modal. Branch: `prj0000048-taskbar-config`. PR #186 **MERGED** `bfe0e44ae`. 16/16 Vitest; tsc clean; npm run build (618 kB); 17/17 docs policy. Security: loadOsConfig type-guarded; saveOsConfig try/catch'd.
- `prj0000049` allocated 2026-03-23: `prj0000049-dependabot-security-fixes` — Resolve 6 Dependabot CVEs (1 high, 3 medium, 2 low) all in rust_core/p2p via libp2p 0.49→0.56 bump. PR #187 **MERGED** `568f8c5e1`. 7/7 security tests; cargo build clean; 619 Python tests pass. yamux 0.10.2→0.13.10, ring 0.16→0.17, idna 0.2.3→1.1.0, ed25519-dalek 1→2, curve25519-dalek 3→4, snow 0.9.3→0.9.6.
- `prj0000050` allocated 2026-03-23: `prj0000050-install-script` — Add `.\ install.ps1` developer setup script (Python venv, pip deps, maturin Rust build, npm web deps). PR #188 **MERGED**. 57/57 structure tests; 656/656 full suite; security APPROVED (maturin pinned ==1.12.5).
- `prj0000051` allocated 2026-03-23: `prj0000051-readme-update` — Comprehensive README.md rewrite covering PyAgent v4.0.0-VOYAGER, NebulaOS frontend (with screenshot), FastAPI backend, Rust Core, install.ps1/start.ps1, 8 architecture decisions, 51-project history table, 10 future roadmap items. 44 structural tests. 700 tests pass. PR #189 **MERGED** `b34eea378`.
- Next `prjNNNNNNN` to allocate: `prj0000052` (validate against `docs/project/` inventory before assignment).

## 2026-03-24 — prj0000052 Project Management COMPLETE

**Branch:** `prj0000052-project-management`
**Commit:** `c5703b6c3`
**Status:** PUSHED — PR pending

**Deliverables:**
- `data/projects.json` — 62-entry machine-readable project registry (all 7 lanes)
- `docs/project/kanban.md` — canonical 7-lane Kanban board with all 62 entries
- `web/apps/ProjectManager.tsx` — NebulaOS Kanban app (lane columns, filter bar, project cards)
- `web/App.tsx` + `web/types.ts` — 'projectmanager' registered and in menu
- `backend/app.py` — GET /api/projects endpoint (optional ?lane= filter, Pydantic validation)
- `.github/agents/0master.agent.md` — added Project lifecycle board section + step 3a
- `.github/agents/1project.agent.md` — added lifecycle board conventions + step 1a
- **Tests:** 685 pass (20/20 kanban structural tests green)

**Next `prjNNNNNNN` to allocate:** `prj0000073`

## 2026-03-25 — Kanban Cleanup & Test Warning Fixes

**Status:** COMPLETE — committed to main as `cb46038ad` (warnings) + kanban cleanup

**Work done:**
- Fixed pytest warnings: removed duplicate pytest config from pyproject.toml, closed unclosed file handles in 3 test files, replaced short JWT test keys (10–11 bytes) with 32+ byte keys, added filterwarnings for internal ResourceWarnings. Result: 835 passed, 9 skipped, **0 warnings**.
- Cleaned up kanban.md and data/projects.json: all 19 projects (prj0000052–0070) confirmed merged (PRs #190–#208) and moved to Released. Removed 4 duplicate entries (prj0000067–0070 duplication). Updated test count assertions.
- Kanban now: Ideas=2 (prj0000071, 0072), In Sprint=0, Review=2 (prj0000043, 0044), Released=67, Archived=1, Total=72.

## Branch Registry (all 72 projects)

| Dir | Expected Branch | Status |
|---|---|---|
| prj0000001 | `prj0000001-async-runtime` | pre-existing |
| prj0000002 | `prj0000002-core-system` | assigned 2026-03-21 |
| prj0000003 | `prj0000003-hybrid-llm-security` | assigned 2026-03-21 |
| prj0000004 | `prj0000004-llm-context-consolidation` | assigned 2026-03-21 |
| prj0000005 | `prj0000005-llm-swarm-architecture` | assigned 2026-03-21 |
| prj0000006 | `prj0000006-unified-transaction-manager` | assigned 2026-03-21 |
| prj0000007 | `prj0000007-advanced-research` | assigned 2026-03-21 |
| prj0000008 | `prj0000008-agent-workflow` | assigned 2026-03-21 |
| prj0000009 | `prj0000009-community-collaboration` | assigned 2026-03-21 |
| prj0000010 | `prj0000010-context-management` | assigned 2026-03-21 |
| prj0000011 | `prj0000011-core-project-structure` | assigned 2026-03-21 |
| prj0000012 | `prj0000012-deployment-operations` | assigned 2026-03-21 |
| prj0000013 | `prj0000013-dev-tools-autonomy` | assigned 2026-03-21 |
| prj0000014 | `prj0000014-dev-tools-capabilities` | assigned 2026-03-21 |
| prj0000015 | `prj0000015-dev-tools-implementation` | assigned 2026-03-21 |
| prj0000016 | `prj0000016-dev-tools-structure` | assigned 2026-03-21 |
| prj0000017 | `prj0000017-dev-tools-utilities` | assigned 2026-03-21 |
| prj0000018 | `prj0000018-documentation-assets` | assigned 2026-03-21 |
| prj0000019 | `prj0000019-future-roadmap` | assigned 2026-03-21 |
| prj0000020 | `prj0000020-github-import` | assigned 2026-03-21 |
| prj0000021 | `prj0000021-project-management-governance` | assigned 2026-03-21 |
| prj0000022 | `prj0000022-swarm-architecture` | assigned 2026-03-21 |
| prj0000023 | `prj0000023-testing-infrastructure` | assigned 2026-03-21 |
| prj0000024 | `prj0000024-async-runtime` | assigned 2026-03-21 |
| prj0000025 | `prj0000025-core-system` | assigned 2026-03-21 |
| prj0000026 | `prj0000026-test-coverage-quality` | assigned 2026-03-21 |
| prj0000027 | `prj0000027-encrypted-memory-blocks` | assigned 2026-03-21 |
| prj0000028 | `prj0000028-transport-t1` | assigned 2026-03-21 |
| prj0000029 | `prj0000029-llm-ui-backend-worker` | assigned 2026-03-21 |
| prj0000030 | `prj0000030-agent-doc-frequency` | assigned 2026-03-21 |
| prj0000031 | `prj0000031-streaming-website` | assigned 2026-03-21 |
| prj0000032 | `prj0000032-agents` | assigned 2026-03-21 |
| prj0000033 | `prj0000033-chat` | assigned 2026-03-21 |
| prj0000034 | `prj0000034-context-manager` | assigned 2026-03-21 |
| prj0000035 | `prj0000035-multimodal` | assigned 2026-03-21 |
| prj0000036 | `prj0000036-plugins` | assigned 2026-03-21 |
| prj0000037 | `prj0000037-tools` | assigned 2026-03-21 |
| prj0000038 | `prj0000038-python-function-coverage` | assigned 2026-03-21 |
| prj0000039 | `prj0000039-conftest-typing-fixes` | assigned 2026-03-21 |
| prj0000040 | `prj0000040-core-system` | assigned 2026-03-21 |
| prj0000041 | `prj0000041-flm` | assigned 2026-03-21 |
| prj0000042 | `prj0000042-tools-crdt-security` | pre-existing |
| prj0000043 | `prj0000043-p2p-security-deps` | assigned 2026-03-22 |
| prj0000044 | `prj0000044-transaction-managers` | assigned 2026-03-22 |
| prj0000045 | `prj0000045-transaction-managers-full` | PR #137 open — COMPLETE |

## Learning Loop — Branch Hygiene

- Record branch hygiene failures in `docs/agents/9git.memory.md` with: date, project, observed branch, failure type, and required fix.
- Reflect recurring failures or policy changes here so future coordinators enforce the updated workflow earlier.
- Shared-branch history under unrelated projects is a warning signal, not an exception path.
- 2026-03-20: Added mandatory "Branch gate" preflight to `@2think` through `@8ql` agent definitions.
    Downstream agents must now stop immediately on expected/observed branch mismatch,
    mark their project artifact + memory entry as BLOCKED, and hand back to `@0master`.
- 2026-03-20: Extended branch-gate enforcement to `@1project` and `@0master` delegation preflight.
    Result: branch mismatch is now blocked at project setup, planning/execution, and git handoff layers.

---

## ✅ Completed subsystems (do NOT reimplement)

| Subsystem | Plan file | Notes |
|---|---|---|
| Async Runtime | 2026-03-10-async-runtime-plan.md | 215+ tests passing, zero sync loops |
| FLM / Fastflow integration | 2026-03-08-flm-plan.md | OpenAI adapter, tool-call loop complete |
| Context Manager & Skills Registry | 2026-03-09-context_management-plan.md | Windowing + skill discovery live |
| Advanced Research packages | prj007-advanced_research/ | 5 skeleton packages importable; code/test DONE; exec/ql/git pending |
| Future Roadmap tooling | future-roadmap-plan.md | Vision templates, milestone generator complete |
| Community Chat | community-collaboration-plan.md | FastAPI, MCP tools, GitHub webhooks live |
| Agent Workflow basics | agent-workflow-plan.md | TaskState, Task, TaskQueue, WorkflowEngine, CoRT live |
| GitHub Importer skeleton | github-import-plan.md | Importer skeleton fully implemented |
| Unified Transaction Manager | prj006-unified-transaction-manager/ | Full pipeline DONE (75d5c3e) — 205 tests, 100% coverage |

---

## 🗂️ Implementation Phases

### Phase 1 — Foundation & Infrastructure
**Status:** 🔴 PENDING — BLOCKING all other phases  
**Goal:** Establish stable core infrastructure: 
    CI green, transaction managers unified, project structure clean, LLM context consolidated.

**Subsystems:**
- **Conftest typing fixes** (`conftest-typing-fixes-plan.md`) 
    — URGENT: blocks all CI gates; 6 tasks
- **Unified transaction manager** (`unified-transaction-manager-plan.md`) 
    — 7 tasks; StorageTransaction, MemoryTransaction, ProcessTransaction, ContextTransaction unification
- **Core project structure** (`core-project-structure-plan.md`) 
    — 7 tasks; directory layout, module boundaries, import hygiene
- **LLM context consolidation** (`llm-context-consolidation-plan.md`) 
    — 6 tasks; single ContextWindow, token budget tracking
- **Core system modules** (`core-system-plan.md`) 
    — 8 task groups; runtime bootstrap, observability, error taxonomy
- **Testing infrastructure** (`testing-infrastructure-plan.md`) 
    — CI enforcement, async loop checker, pytest fixtures

**Brainstorm designs to feed into @1think:**
- `docs/project/*/brainstorm.md` files covering: core architecture, 
    transaction design, context management, testing

**Acceptance criteria:**
- All CI pipelines green (pytest, ruff, mypy)
- All four transaction types (Storage/Memory/Process/Context) unified under single interface
- Zero circular imports; `conftest.py` fully typed
- LLM context consolidation: one ContextWindow class in use across codebase

---

### Phase 2 — Core Agent & Swarm Features
**Status:** 🟡 PENDING — unblocked after Phase 1  
**Goal:** Implement full swarm orchestration: agent registry, task scheduler, 
    distributed memory stores, inter-agent communication.

**Subsystems:**
- **Swarm architecture** (`swarm-architecture-plan.md`) 
    — 6+ tasks; AgentRegistry, TaskScheduler, MemoryStore, metrics, inter-agent protocols
- **LLM swarm architecture** (`llm-swarm-architecture-plan.md`) 
    — 6 phases; multi-LLM routing, load balancing, fallback chains
- **Deployment operations** (`deployment-operations-plan.md`) 
    — 7 tasks; Docker Compose, provisioning, health checks
- **Dev tools capabilities** (`dev-tools-capabilities-plan.md`) 
    — 6 tasks; code analysis, metrics, dependency graphs
- **Dev tools autonomy** (`dev-tools-autonomy-plan.md`) 
    — 7 tasks; self-healing, auto-fix pipelines

**Brainstorm designs to feed into @1think:**
- Swarm topology design, LLM router design, agent registry schema, task scheduler algorithm

**Acceptance criteria:**
- AgentRegistry can register/discover/heartbeat agents
- TaskScheduler can assign tasks to agents based on capability and load
- Multi-LLM routing with fallback chains functional
- Docker Compose stack brings up full swarm locally

---

### Phase 3 — Security, Encrypted Memory & Transport
**Status:** 🟡 PENDING — unblocked after Phase 1; partially after Phase 2  
**Goal:** End-to-end encrypted agent communication, Rust-native crypto primitives, and P2P transport layer.

**Subsystems:**
- **Hybrid LLM security** (`hybrid-llm-security-plan.md`) 
    — 14/15 tasks pending; Rust crypto core, key exchange, auth
- **Encrypted memory blocks** (`encrypted-memory-blocks-plan.md`) 
    — 20 tasks; X25519 ECDH + ChaCha20-Poly1305 in Rust, PyO3 bindings
- **Transport T-1** (`transport-t1-plan.md`) 
    — 20 tasks; Ed25519 NodeIdentity, Noise_XX handshake, QUIC scaffold
- **P2P CRDT** (brainstorm) 
    — libp2p + Automerge for distributed agent state

**Brainstorm designs to feed into @1think:**
- Crypto primitive selection, key derivation scheme, Noise protocol integration, QUIC transport design

**Acceptance criteria:**
- All memory reads/writes through EncryptedMemoryBlock with X25519 + ChaCha20-Poly1305
- Ed25519 NodeIdentity: every agent has a keypair; messages are signed
- Noise_XX handshake completes between two agent nodes
- QUIC loopback transport passes integration tests
- All Rust code passes `cargo clippy -D warnings`

---

### Phase 4 — UI, Developer Tools & Polish
**Status:** 🟡 PENDING — unblocked after Phase 2  
**Goal:** Production-quality frontend + backend streaming, developer self-improvement tools, 
    documentation, and governance.

**Subsystems:**
- **LLM UI backend worker** (`llm-ui-backend-worker-plan.md`) 
    — 16 tasks; FastAPI + WebSocket streaming, WebRTC signaling, voice input, AI action control
- **Dev tools structure / utilities / implementation** (`dev-tools-*-plan.md`) 
    — 16 tasks across 3 files
- **Test coverage quality** (`test-coverage-quality-plan.md`) 
    — 8 tasks; mypy strict, ruff full ruleset, coverage thresholds
- **Documentation assets** (`documentation-assets-plan.md`) 
    — 7 tasks; MkDocs, diagrams, changelog
- **Project management governance** (`project-management-governance-plan.md`) 
    — PM dashboards, risk matrix, budget tracking

**Acceptance criteria:**
- WebSocket streaming UI delivers tokens in real-time
- WebRTC signaling scaffold functional
- MkDocs site builds cleanly (`mkdocs build --strict`)
- Coverage ≥ 80% on all `src/` modules
- Governance templates operational (risk matrix, budget tracker)

---

## 🔗 Agent workflow

```
@0master → @1think → @2plan → @3test → @4code → @5exec → @6ql → @7git → @0master
```

## 📁 Key file locations

- Brainstorm designs: `docs/project/*/brainstorm.md`
- Implementation plans: `docs/project/*/plan.md`
- Agent memory files: `docs/agents/<N><name>.memory.md`
- Architecture docs: `docs/architecture/`
- Agent definitions: `.github/agents/`

---

## 🤖 Auto-handoff (agent/runSubagent)

When the master agent sets strategy and delegates work, it should trigger the next agent 
in the pipeline automatically using `agent/runSubagent`.

### Expected automatic handoff chain (primary workflow)
1. **@0master** establishes strategy and delegates to **@1project** via `agent/runSubagent`.
2. **@1project** executes planning and then delegates to **@9git** via `agent/runSubagent`.
3. **@9git** performs git operations (branching, commits, PRs) and, when complete, 
automatically returns control to **@0master** via `agent/runSubagent`.

> This ensures the workflow is self-advancing: the master agent kickstarts the process, 
handoffs are explicit via `agent/runSubagent`, and completion naturally flows back to the master.

### 🧠 MCP Server & Skills Awareness
Agents should be aware of available MCP servers and the skills registered under `.agents/skills`. 
They can reference or invoke these skills as part of their workflow 
(e.g., using `agent/runSubagent` or tool-call patterns) to reuse existing capabilities 
instead of reimplementing logic.


## 2026-04-02 — prj0000114 escalated to artifact-driven pipeline refactor

- Trigger: user requested a fuller refactor for IdeaTracker because 200k ideas is only the beginning and incremental outputs/artifacts are needed for future scale.
- Planning delivered by @4plan:
	- Refactor plan written to `docs/project/prj0000114-ideatracker-batching-verbosity/ideatracker-batching-verbosity.plan.md`.
	- Direction: keep `scripts/IdeaTracker.py` as CLI entrypoint, move heavy work behind helper modules, and persist deterministic batch artifacts under `docs/project/`.
- Implementation delivered by @6code:
	- Added helper modules:
		- `scripts/idea_tracker_artifacts.py`
		- `scripts/idea_tracker_pipeline.py`
		- `scripts/idea_tracker_similarity.py`
	- Refactored `scripts/IdeaTracker.py` into an artifact-driven pipeline.
	- Added/maintained batch-persisted artifacts in `docs/project/` for:
		- progress
		- mapping
		- references
		- section names
		- tokens
		- similarities
	- Preserved final outputs:
		- `docs/project/ideatracker.json`
		- split `docs/project/ideatracker-NNNNNN.json` files
	- Added rewrite-safe incremental behavior so rerunning the same batch window replaces stable rows rather than duplicating them.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `26 passed, 0 failed`
	- editor diagnostics: no errors in pipeline modules or tracker tests.
- Current branch: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — prj0000114 IdeaTracker batching and verbosity project initialized and implemented

- Trigger: user requested `scripts/IdeaTracker.py` become more verbose and scale better for 100,000+ ideas with batch processing around 1000.
- Project boundary assigned:
	- Project id: `prj0000114`
	- Branch: `prj0000114-ideatracker-batching-verbosity`
	- Lane: `Discovery`
- Governance setup delivered by @1project:
	- Added project artifacts under `docs/project/prj0000114-ideatracker-batching-verbosity/`
	- Updated `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`
	- Validation:
		- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
- Implementation delivered by @6code:
	- `scripts/IdeaTracker.py`: added batch-size and verbose support, stderr progress logging, and blocking-based duplicate candidate narrowing to avoid full O(n^2) comparisons.
	- `tests/test_idea_tracker.py`: added focused coverage for batching/progress and duplicate-candidate blocking behavior.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `16 passed, 0 failed`
	- editor diagnostics: no errors in `scripts/IdeaTracker.py` or `tests/test_idea_tracker.py`
- Notes:
	- Unrelated pre-existing idea-merge workspace changes were preserved and not used as scope for `prj0000114` implementation.
	- Current branch after handoff: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — @10idea merge/archive pass executed

- Trigger: user requested another @10idea merge of similar ideas and archival of superseded ideas.
- Branch gate:
	- Observed before action: `main` (blocked for project-scoped idea maintenance).
	- Switched to: `feature/idea-merge-archive-10idea` before delegation.
- Delegation: @10idea executed candidate analysis with existing idea tooling and performed one high-confidence semantic consolidation.
- Delivered:
	- Created `docs/project/ideas/idea000132-external-ai-learning-jsonl-shards-hardening.md`.
	- Archived (moved):
		- `docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000123-shard-202602-306-jsonl-hardening.md`
		- `docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000124-shard-202602-693-jsonl-hardening.md`
	- Refreshed `docs/project/ideatracker.json`.
- Reported tracker deltas:
	- total: 131 -> 132
	- active: 120 -> 119
	- archived: 11 -> 13
	- ready: 51 -> 52
	- blocked: 80 -> 80
- Governance validation:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`.

## 2026-04-02 — PR #270 merged (pre-commit-first quality gates)

- Branch: `feature/idea-merge-archive-10idea` → main
- Merge commit: `be6513c50f`
- Contents merged:
	- `.pre-commit-config.yaml`: added ruff-format, rust-fmt, rust-clippy; upgraded secret-scan to --fail-on-severity HIGH
	- `.github/workflows/security.yml`: deleted (redundant — ci.yml covers via pre-commit run --all-files)
	- `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`: created
	- `docs/project/ideas/archive/idea000{004,005,006,007}*`: archived (superseded by idea000131)
	- `docs/project/ideatracker.json`: active=120, archived=11
- Note: PR #269 (full legacy corpus, 206k ideas) also already merged at 4ab8ef807f.
- Current HEAD: be6513c50f (main, clean, up to date)
- Status: CLOSED

## 2026-04-01 — Parallel-first agent coordination policy

- Trigger: user requested agents to operate more independently and in parallel where safe.
- Decision:
	- Adopt parallel-first delegation for independent work packages.
	- Enforce explicit file ownership boundaries per work package.
	- Require synchronization barriers before implementation and before validation/git.
	- Keep git-affecting operations strictly sequential.
- Files updated:
	- `.github/agents/0master.agent.md`
	- `.github/agents/tools/0master.tools.md`
	- `.github/agents/governance/shared-governance-checklist.md`
- Expected effect:
	- Higher throughput in discovery/planning phases without increasing branch/scope risk.
	- Reduced coordination bottlenecks by making parallelization default when isolation is clear.

## 2026-04-01 — Parallel policy rollout across specialist agents

- Trigger: user requested additional improvement after initial parallel-first master/governance update.
- Decision:
	- Extend independent-parallel policy into role-local instructions for `@1project`..`@10idea`.
	- Keep git-affecting and final signoff actions strictly sequential.
- Files updated:
	- `.github/agents/1project.agent.md`
	- `.github/agents/2think.agent.md`
	- `.github/agents/3design.agent.md`
	- `.github/agents/4plan.agent.md`
	- `.github/agents/5test.agent.md`
	- `.github/agents/6code.agent.md`
	- `.github/agents/7exec.agent.md`
	- `.github/agents/8ql.agent.md`
	- `.github/agents/9git.agent.md`
	- `.github/agents/10idea.agent.md`
- Validation:
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.

## 2026-04-01 — Shared parallel agent register

- Trigger: user requested shared JSON register for parallel work tracking across `@0master` and all sub-agents.
- Delivered:
	- Added canonical register file: `.github/agents/data/parallel_agents_register.json`.
	- Added mandatory register usage to `@0master` policy and shared governance checklist.
	- Added lock/touched-file coordination requirement to 0master tools guidance.
- Register scope:
	- active wave metadata, per-agent package status, touched/planned files, lock ids, file locks, lockfiles, and event log.
- Expected effect:
	- deterministic parallel ownership and conflict prevention for overlapping file edits.

## 2026-04-01 — Executable parallel register CLI

- Trigger: user requested next-step executable tooling for atomic and standardized register updates.
- Delivered:
	- Added `scripts/parallel_register.py` with commands:
	  - `acquire-lock`
	  - `release-lock`
	  - `touch-file`
	  - `close-wave`
	- Added focused tests: `tests/test_parallel_register.py`.
	- Added governance/tooling references for standardized command usage.
- Validation:
	- `python -m pytest -q tests/test_parallel_register.py` -> `4 passed`.

## 2026-03-29 — Agent workflow hardening from lessons-learned sweep

- Scope: reviewed all agent instruction files and cross-checked recurring blockers from history memory logs.
- Changes applied:
	- Raised @0master pre-delegation scorecard with two additional hard-gate categories: docs-policy readiness and pre-commit baseline readiness.
	- Upgraded @1project `<project>.git.md` template to modern Branch Plan / Scope Validation / Failure Disposition format to prevent docs-policy drift.
	- Added @7exec interruption handling rule: repeated `KeyboardInterrupt`/inconclusive full-suite runs now block handoff.
	- Added @7exec mandatory docs-policy gate before @8ql handoff.
	- Added @8ql mandatory exact failing-selector rerun evidence for blocker-remediation passes.
	- Added @9git docs-only closure preflight for repo-wide `run-precommit-checks` baseline debt visibility.
	- Added project-artifact docs-policy validation command in operational inputs for all agents (`0master`..`9git`).
- Rationale:
	- Addresses recurring failures seen in history memory: missing `## Branch Plan` in project git artifacts, inconclusive interrupted validation runs, and docs-only git closures blocked late by repo-wide pre-commit debt.
- Next actions:
	- Validate policy docs tests and architecture ADR governance tests.
	- If green, keep these rules as active hardening baseline.

## 2026-03-29 — Cross-link rollout to shared governance checklist

- Scope: created one canonical governance checklist and linked all ten agent files to consume it at task start.
- Changes applied:
	- Added `.github/agents/governance/shared-governance-checklist.md` as the shared source for branch/scope/docs-policy and handoff-evidence gates.
	- Updated `.github/agents/0master.agent.md` through `.github/agents/9git.agent.md` operational sections to read and apply the shared checklist.
- Validation:
	- `pytest tests/docs/test_agent_workflow_policy_docs.py tests/docs/test_architecture_adr_governance.py` -> `15 passed`.

## 2026-03-29 — CI shard-1 coverage gate remediation

- Trigger: GitHub Actions run 23716956870 failed at job `Run tests (shard 1/10)`, step `Coverage gate (stage 1)`.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- Direction accepted: switch gate to `--cov=src` and run tests that actually execute `src`.
- Change delegated to @6code:
	- `.github/workflows/ci.yml` coverage gate command updated to:
	  - `pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=40 -q`
- Validation evidence:
	- `pytest tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py -q` -> `13 passed`.
	- New gate command run locally -> `Required test coverage of 40% reached. Total coverage: 94.48%`.

## 2026-03-29 — prj0000101 @9git continuation and PR #250 verification

- Preflight branch gate:
	- Observed branch: `prj0000101-pending-definition`
	- Expected branch (from project Branch Plan): `prj0000101-pending-definition`
	- Result: PASS
- PR verification:
	- Active PR payload confirms PR #250 is OPEN and includes health-probe implementation/test diffs.
	- Local branch tip before remediation: `fedc7658f`.
- Delegated remediation to @6code for unresolved major `web/apps/ProjectManager.tsx` review comments:
	1. remove unrelated fallback SWOT/risk context in idea-scoped prompt generation.
	2. source fresh kanban register content at trigger time with graceful fallback.
- @6code result:
	- Commit: `4c2d56938` (`fix(projectmanager): use idea-only insight context and fresh kanban source`).
	- Validation reported: no file diagnostics, `web` build passed, targeted ProjectManager tests passed.
- Git handoff progress:
	- Pushed branch update: `fedc7658f..4c2d56938` to `origin/prj0000101-pending-definition`.
	- @9git closure still requires final PR-level merge decision.

## 2026-03-29 — Post-merge continuation into prj0000102

- Trigger: user confirmed PR merged and requested continuation.
- Governance normalization performed:
	- Fixed lane drift via governance tooling and validated registry/kanban consistency.
	- Current result: `VALIDATION_OK` with `projects=102` and `kanban_rows=102`.
- Branch isolation enforced:
	- Created and switched to dedicated project branch `prj0000102-pyproject-requirements-sync`.
- Delegation progression completed:
	- @1project initialized canonical project artifacts and synced registry metadata for prj0000102.
	- @2think completed options exploration.
	- @3design finalized selected design.
	- @4plan finalized implementation roadmap.
	- @5test finalized test artifact and handoff criteria.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> OK.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` passed in each delegated phase.
- Delivery state:
	- Branch pushed: `origin/prj0000102-pyproject-requirements-sync`.
	- Ready for @6code implementation handoff on prj0000102.

## 2026-03-30 — prj0000102 @6code implementation completion

- Trigger: user requested automatic continuation into @6code implementation.
- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch (project Branch Plan): `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @6code delivery:
	- Implemented canonical dependency authority and deterministic requirements emission.
	- Added dependency drift and policy enforcement wiring into shared CI checks.
	- Added/updated concrete tests for canonical-source, deterministic output, drift gate, and policy validation.
	- Updated project code artifact status for implementation evidence.
- @6code commit:
	- `5658a0e00` — `feat(deps): enforce canonical pyproject requirements sync`.
- Validation evidence (reported by @6code):
	- dependency selectors and targeted test files passing.
	- docs policy test passing.
	- ruff and mypy passing for touched implementation files.
	- dependency audit `--check` passing.
- Publish state:
	- Pushed `30e7ecf65..5658a0e00` to `origin/prj0000102-pyproject-requirements-sync`.
- Next workflow step:
	- Ready for @7exec runtime validation handoff.

## 2026-03-30 — prj0000102 @7exec/@8ql/@9git closure progression

- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch: `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @7exec completion:
	- Runtime validation suite executed and logged.
	- Exec artifact committed: `85027f9e9`.
- @8ql completion:
	- Focused quality/security checks completed with clear gate.
	- QL artifact committed: `44bcf6fa8`.
- @9git first pass:
	- Opened PR #251 for `prj0000102-pyproject-requirements-sync` -> `main`.
	- Initial artifact state BLOCKED due formatter baseline failure (`tests/tools/test_dependency_audit.py`).
- Blocker remediation:
	- Applied formatter fix to blocker file and re-ran formatter gate successfully.
	- Re-ran docs policy gate successfully.
- @9git closure:
	- Updated git artifact status to DONE and recorded pre-commit evidence.
	- Narrow closure commit: `7fc4994bc` (`docs(git): close prj0000102 git handoff`).
	- Pushed branch update to origin and PR #251 reflects latest commits.

## 2026-03-30 — prj0000105 post-merge release registry synchronization

- Trigger: user confirmed PR #258 merged and requested continuation.
- Actions completed:
	- Transitioned `prj0000105` to `Released` using registry governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #258`) in board artifacts.
	- Revalidated project registry/kanban consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000105 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=105`, `kanban_rows=105`).
- Outcome:
	- Post-merge governance state for prj0000105 is synchronized and ready for next project continuation (`prj0000106`).

## 2026-03-30 — prj0000106 post-merge release registry synchronization

- Trigger: user confirmed PR #259 merged and requested project wrap-up and return to main.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000106` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #259`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000106 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=106`, `kanban_rows=106`).
- Outcome:
	- Project prj0000106 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000107 post-merge release registry synchronization

- Trigger: user confirmed PR #260 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000107` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #260`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000107 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=107`, `kanban_rows=107`).
- Outcome:
	- Project prj0000107 is formally closed in Released lane and main is ready for next project allocation (`prj0000108`).

## 2026-03-31 — prj0000108 post-merge release registry synchronization

- Trigger: user confirmed PR #261 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000108` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #261`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000108 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=108`, `kanban_rows=108`).
- Outcome:
	- Project prj0000108 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000109 allocation and initialization for next idea

- Trigger: user requested a new project for the next idea.
- Selection outcome:
	- Candidate scan selected `idea000002-missing-compose-dockerfile` as the next unimplemented `P1` idea not yet represented in the active project registry.
	- Assigned project ID `prj0000109` from `data/nextproject.md` and expected branch `prj0000109-idea000002-missing-compose-dockerfile`.
- Actions completed:
	- Finalized prior idea archival move on `main` and pushed baseline commit.
	- Created and switched to dedicated branch `prj0000109-idea000002-missing-compose-dockerfile`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
- Outcome:
	- New project `prj0000109` is initialized and ready for `@2think` discovery handoff.

## 2026-03-31 — Global lessons-learned workflow hardening (all projects)

- Trigger: user requested implementation of fixes from lessons learned across all projects.
- Changes applied:
	- Enhanced `scripts/project_registry_governance.py` with automated idea archival support:
		- New `sync-idea-archive` command to archive idea files for all `Released` projects.
		- `set-lane --lane Released` now auto-archives matching `ideaNNNNNN-*.md` files.
		- `validate` now fails when released idea-backed projects have unarchived or missing archive files.
	- Extended `tests/docs/test_agent_workflow_policy_docs.py` with policy assertions for release archival requirements and governance command coverage.
- Validation evidence:
	- `python scripts/project_registry_governance.py sync-idea-archive` -> `moved=0` (repository already compliant).
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.

## 2026-04-01 — prj0000111 post-merge release registry synchronization

- Trigger: user requested continuation after PR #264 check-fix cycle and merge.
- Actions completed:
	- Verified PR #264 merged (`headRefName=prj0000111-ci-detached-head-governance-gate`, merged at `2026-04-01T07:29:54Z`).
	- Registered missing `prj0000111` in canonical governance artifacts:
		- `docs/project/kanban.json`
		- `docs/project/kanban.md`
		- `data/projects.json`
		- `data/nextproject.md` advanced to `prj0000112`.
	- Updated lane metrics in kanban markdown header/summary to keep board counters consistent.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=111`, `kanban_rows=111`).
- Outcome:
	- Project `prj0000111` is formally closed in `Released` lane and next ID allocation baseline is restored.

## 2026-04-01 — prj0000110 allocation and initialization for next idea

- Trigger: user requested to start the next project.
- Selection outcome:
	- Candidate scan selected `idea000004-quality-workflow-branch-trigger` as the next unimplemented idea not represented in active project tags.
	- Assigned project ID `prj0000110` from `data/nextproject.md` and expected branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
- Actions completed:
	- Created and switched to dedicated branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=110`, `kanban_rows=110`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- New project `prj0000110` is initialized in Discovery and ready for `@2think` handoff.

## 2026-04-01 — prj0000110 CI workload reduction implementation

- Trigger: user approved implementing CI reductions using pre-commit-aligned governance.
- Actions completed:
	- Updated `.github/workflows/ci.yml` to add a single-run `governance` job (`Governance Gate`) that runs pre-commit quality hooks and strict mypy once per workflow.
	- Reduced shard duplication in `test` job by removing repeated strict mypy execution across all 10 shards.
	- Added conditional Rust build skip for lightweight shards 1-3 to reduce unnecessary setup cost.
	- Expanded `tests/ci/test_ci_workflow.py` with assertions that lock the new governance/test-shard responsibilities.
- Validation evidence:
	- `python -m pytest -q tests/ci/test_ci_workflow.py` -> `6 passed`.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- CI now performs governance checks once and keeps shard jobs focused on tests, reducing duplicated work while preserving deterministic policy gates.

## 2026-04-01 — Added @10idea agent for idea merge and archival governance

- Trigger: user requested a dedicated idea curation agent to monitor `docs/project/ideas`, merge similar ideas into a new consolidated idea, and archive superseded ideas.
- Actions completed:
	- Added `.github/agents/10idea.agent.md` with explicit workflow for similarity detection, merged-idea creation, and archive moves.
	- Added role support files:
		- `.github/agents/tools/10idea.tools.md`
		- `.github/agents/skills/10idea.skills.md`
		- `.github/agents/data/current.10idea.memory.md`
		- `.github/agents/data/history.10idea.memory.md`
		- `.github/agents/data/2026-04-01.10idea.log.md`
	- Integrated `@10idea` into UI/runtime discovery paths:
		- `web/vite.config.ts` valid agent-doc IDs
		- `web/apps/CodeBuilder.tsx` agent type + catalog entry
		- `web/apps/OrchestrationGraph.tsx` stage list
		- `web/apps/ProjectManager.tsx` required flow + responsibilities text
- Outcome:
	- `@10idea` is now available as a first-class agent for idea deduplication and archival operations.

## 2026-03-31 — prj0000109 post-merge release registry synchronization

- Trigger: user confirmed PR #262 merged.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000109` to `Released` via governance tooling with canonical merged metadata (`branch: merged`, `pr: #262`).
	- Auto-archived the released idea file `idea000002-missing-compose-dockerfile.md` into `docs/project/ideas/archive/` via governance automation.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000109 --lane Released --branch merged --pr #262` -> updated and archived 1 idea file.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
- Outcome:
	- Project prj0000109 is formally closed in Released lane and release-closure archival policy was applied automatically.

## 2026-04-02 — prj0000114 escalated to artifact-driven pipeline refactor

- Trigger: user requested a fuller refactor for IdeaTracker because 200k ideas is only the beginning and incremental outputs/artifacts are needed for future scale.
- Planning delivered by @4plan:
	- Refactor plan written to `docs/project/prj0000114-ideatracker-batching-verbosity/ideatracker-batching-verbosity.plan.md`.
	- Direction: keep `scripts/IdeaTracker.py` as CLI entrypoint, move heavy work behind helper modules, and persist deterministic batch artifacts under `docs/project/`.
- Implementation delivered by @6code:
	- Added helper modules:
		- `scripts/idea_tracker_artifacts.py`
		- `scripts/idea_tracker_pipeline.py`
		- `scripts/idea_tracker_similarity.py`
	- Refactored `scripts/IdeaTracker.py` into an artifact-driven pipeline.
	- Added/maintained batch-persisted artifacts in `docs/project/` for:
		- progress
		- mapping
		- references
		- section names
		- tokens
		- similarities
	- Preserved final outputs:
		- `docs/project/ideatracker.json`
		- split `docs/project/ideatracker-NNNNNN.json` files
	- Added rewrite-safe incremental behavior so rerunning the same batch window replaces stable rows rather than duplicating them.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `26 passed, 0 failed`
	- editor diagnostics: no errors in pipeline modules or tracker tests.
- Current branch: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — prj0000114 IdeaTracker batching and verbosity project initialized and implemented

- Trigger: user requested `scripts/IdeaTracker.py` become more verbose and scale better for 100,000+ ideas with batch processing around 1000.
- Project boundary assigned:
	- Project id: `prj0000114`
	- Branch: `prj0000114-ideatracker-batching-verbosity`
	- Lane: `Discovery`
- Governance setup delivered by @1project:
	- Added project artifacts under `docs/project/prj0000114-ideatracker-batching-verbosity/`
	- Updated `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`
	- Validation:
		- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
- Implementation delivered by @6code:
	- `scripts/IdeaTracker.py`: added batch-size and verbose support, stderr progress logging, and blocking-based duplicate candidate narrowing to avoid full O(n^2) comparisons.
	- `tests/test_idea_tracker.py`: added focused coverage for batching/progress and duplicate-candidate blocking behavior.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `16 passed, 0 failed`
	- editor diagnostics: no errors in `scripts/IdeaTracker.py` or `tests/test_idea_tracker.py`
- Notes:
	- Unrelated pre-existing idea-merge workspace changes were preserved and not used as scope for `prj0000114` implementation.
	- Current branch after handoff: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — @10idea merge/archive pass executed

- Trigger: user requested another @10idea merge of similar ideas and archival of superseded ideas.
- Branch gate:
	- Observed before action: `main` (blocked for project-scoped idea maintenance).
	- Switched to: `feature/idea-merge-archive-10idea` before delegation.
- Delegation: @10idea executed candidate analysis with existing idea tooling and performed one high-confidence semantic consolidation.
- Delivered:
	- Created `docs/project/ideas/idea000132-external-ai-learning-jsonl-shards-hardening.md`.
	- Archived (moved):
		- `docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000123-shard-202602-306-jsonl-hardening.md`
		- `docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000124-shard-202602-693-jsonl-hardening.md`
	- Refreshed `docs/project/ideatracker.json`.
- Reported tracker deltas:
	- total: 131 -> 132
	- active: 120 -> 119
	- archived: 11 -> 13
	- ready: 51 -> 52
	- blocked: 80 -> 80
- Governance validation:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`.

## 2026-04-02 — PR #270 merged (pre-commit-first quality gates)

- Branch: `feature/idea-merge-archive-10idea` → main
- Merge commit: `be6513c50f`
- Contents merged:
	- `.pre-commit-config.yaml`: added ruff-format, rust-fmt, rust-clippy; upgraded secret-scan to --fail-on-severity HIGH
	- `.github/workflows/security.yml`: deleted (redundant — ci.yml covers via pre-commit run --all-files)
	- `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`: created
	- `docs/project/ideas/archive/idea000{004,005,006,007}*`: archived (superseded by idea000131)
	- `docs/project/ideatracker.json`: active=120, archived=11
- Note: PR #269 (full legacy corpus, 206k ideas) also already merged at 4ab8ef807f.
- Current HEAD: be6513c50f (main, clean, up to date)
- Status: CLOSED

## 2026-04-01 — Parallel-first agent coordination policy

- Trigger: user requested agents to operate more independently and in parallel where safe.
- Decision:
	- Adopt parallel-first delegation for independent work packages.
	- Enforce explicit file ownership boundaries per work package.
	- Require synchronization barriers before implementation and before validation/git.
	- Keep git-affecting operations strictly sequential.
- Files updated:
	- `.github/agents/0master.agent.md`
	- `.github/agents/tools/0master.tools.md`
	- `.github/agents/governance/shared-governance-checklist.md`
- Expected effect:
	- Higher throughput in discovery/planning phases without increasing branch/scope risk.
	- Reduced coordination bottlenecks by making parallelization default when isolation is clear.

## 2026-04-01 — Parallel policy rollout across specialist agents

- Trigger: user requested additional improvement after initial parallel-first master/governance update.
- Decision:
	- Extend independent-parallel policy into role-local instructions for `@1project`..`@10idea`.
	- Keep git-affecting and final signoff actions strictly sequential.
- Files updated:
	- `.github/agents/1project.agent.md`
	- `.github/agents/2think.agent.md`
	- `.github/agents/3design.agent.md`
	- `.github/agents/4plan.agent.md`
	- `.github/agents/5test.agent.md`
	- `.github/agents/6code.agent.md`
	- `.github/agents/7exec.agent.md`
	- `.github/agents/8ql.agent.md`
	- `.github/agents/9git.agent.md`
	- `.github/agents/10idea.agent.md`
- Validation:
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.

## 2026-04-01 — Shared parallel agent register

- Trigger: user requested shared JSON register for parallel work tracking across `@0master` and all sub-agents.
- Delivered:
	- Added canonical register file: `.github/agents/data/parallel_agents_register.json`.
	- Added mandatory register usage to `@0master` policy and shared governance checklist.
	- Added lock/touched-file coordination requirement to 0master tools guidance.
- Register scope:
	- active wave metadata, per-agent package status, touched/planned files, lock ids, file locks, lockfiles, and event log.
- Expected effect:
	- deterministic parallel ownership and conflict prevention for overlapping file edits.

## 2026-04-01 — Executable parallel register CLI

- Trigger: user requested next-step executable tooling for atomic and standardized register updates.
- Delivered:
	- Added `scripts/parallel_register.py` with commands:
	  - `acquire-lock`
	  - `release-lock`
	  - `touch-file`
	  - `close-wave`
	- Added focused tests: `tests/test_parallel_register.py`.
	- Added governance/tooling references for standardized command usage.
- Validation:
	- `python -m pytest -q tests/test_parallel_register.py` -> `4 passed`.

## 2026-03-29 — Agent workflow hardening from lessons-learned sweep

- Scope: reviewed all agent instruction files and cross-checked recurring blockers from history memory logs.
- Changes applied:
	- Raised @0master pre-delegation scorecard with two additional hard-gate categories: docs-policy readiness and pre-commit baseline readiness.
	- Upgraded @1project `<project>.git.md` template to modern Branch Plan / Scope Validation / Failure Disposition format to prevent docs-policy drift.
	- Added @7exec interruption handling rule: repeated `KeyboardInterrupt`/inconclusive full-suite runs now block handoff.
	- Added @7exec mandatory docs-policy gate before @8ql handoff.
	- Added @8ql mandatory exact failing-selector rerun evidence for blocker-remediation passes.
	- Added @9git docs-only closure preflight for repo-wide `run-precommit-checks` baseline debt visibility.
	- Added project-artifact docs-policy validation command in operational inputs for all agents (`0master`..`9git`).
- Rationale:
	- Addresses recurring failures seen in history memory: missing `## Branch Plan` in project git artifacts, inconclusive interrupted validation runs, and docs-only git closures blocked late by repo-wide pre-commit debt.
- Next actions:
	- Validate policy docs tests and architecture ADR governance tests.
	- If green, keep these rules as active hardening baseline.

## 2026-03-29 — Cross-link rollout to shared governance checklist

- Scope: created one canonical governance checklist and linked all ten agent files to consume it at task start.
- Changes applied:
	- Added `.github/agents/governance/shared-governance-checklist.md` as the shared source for branch/scope/docs-policy and handoff-evidence gates.
	- Updated `.github/agents/0master.agent.md` through `.github/agents/9git.agent.md` operational sections to read and apply the shared checklist.
- Validation:
	- `pytest tests/docs/test_agent_workflow_policy_docs.py tests/docs/test_architecture_adr_governance.py` -> `15 passed`.

## 2026-03-29 — CI shard-1 coverage gate remediation

- Trigger: GitHub Actions run 23716956870 failed at job `Run tests (shard 1/10)`, step `Coverage gate (stage 1)`.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- Direction accepted: switch gate to `--cov=src` and run tests that actually execute `src`.
- Change delegated to @6code:
	- `.github/workflows/ci.yml` coverage gate command updated to:
	  - `pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=40 -q`
- Validation evidence:
	- `pytest tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py -q` -> `13 passed`.
	- New gate command run locally -> `Required test coverage of 40% reached. Total coverage: 94.48%`.

## 2026-03-29 — prj0000101 @9git continuation and PR #250 verification

- Preflight branch gate:
	- Observed branch: `prj0000101-pending-definition`
	- Expected branch (from project Branch Plan): `prj0000101-pending-definition`
	- Result: PASS
- PR verification:
	- Active PR payload confirms PR #250 is OPEN and includes health-probe implementation/test diffs.
	- Local branch tip before remediation: `fedc7658f`.
- Delegated remediation to @6code for unresolved major `web/apps/ProjectManager.tsx` review comments:
	1. remove unrelated fallback SWOT/risk context in idea-scoped prompt generation.
	2. source fresh kanban register content at trigger time with graceful fallback.
- @6code result:
	- Commit: `4c2d56938` (`fix(projectmanager): use idea-only insight context and fresh kanban source`).
	- Validation reported: no file diagnostics, `web` build passed, targeted ProjectManager tests passed.
- Git handoff progress:
	- Pushed branch update: `fedc7658f..4c2d56938` to `origin/prj0000101-pending-definition`.
	- @9git closure still requires final PR-level merge decision.

## 2026-03-29 — Post-merge continuation into prj0000102

- Trigger: user confirmed PR merged and requested continuation.
- Governance normalization performed:
	- Fixed lane drift via governance tooling and validated registry/kanban consistency.
	- Current result: `VALIDATION_OK` with `projects=102` and `kanban_rows=102`.
- Branch isolation enforced:
	- Created and switched to dedicated project branch `prj0000102-pyproject-requirements-sync`.
- Delegation progression completed:
	- @1project initialized canonical project artifacts and synced registry metadata for prj0000102.
	- @2think completed options exploration.
	- @3design finalized selected design.
	- @4plan finalized implementation roadmap.
	- @5test finalized test artifact and handoff criteria.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> OK.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` passed in each delegated phase.
- Delivery state:
	- Branch pushed: `origin/prj0000102-pyproject-requirements-sync`.
	- Ready for @6code implementation handoff on prj0000102.

## 2026-03-30 — prj0000102 @6code implementation completion

- Trigger: user requested automatic continuation into @6code implementation.
- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch (project Branch Plan): `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @6code delivery:
	- Implemented canonical dependency authority and deterministic requirements emission.
	- Added dependency drift and policy enforcement wiring into shared CI checks.
	- Added/updated concrete tests for canonical-source, deterministic output, drift gate, and policy validation.
	- Updated project code artifact status for implementation evidence.
- @6code commit:
	- `5658a0e00` — `feat(deps): enforce canonical pyproject requirements sync`.
- Validation evidence (reported by @6code):
	- dependency selectors and targeted test files passing.
	- docs policy test passing.
	- ruff and mypy passing for touched implementation files.
	- dependency audit `--check` passing.
- Publish state:
	- Pushed `30e7ecf65..5658a0e00` to `origin/prj0000102-pyproject-requirements-sync`.
- Next workflow step:
	- Ready for @7exec runtime validation handoff.

## 2026-03-30 — prj0000102 @7exec/@8ql/@9git closure progression

- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch: `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @7exec completion:
	- Runtime validation suite executed and logged.
	- Exec artifact committed: `85027f9e9`.
- @8ql completion:
	- Focused quality/security checks completed with clear gate.
	- QL artifact committed: `44bcf6fa8`.
- @9git first pass:
	- Opened PR #251 for `prj0000102-pyproject-requirements-sync` -> `main`.
	- Initial artifact state BLOCKED due formatter baseline failure (`tests/tools/test_dependency_audit.py`).
- Blocker remediation:
	- Applied formatter fix to blocker file and re-ran formatter gate successfully.
	- Re-ran docs policy gate successfully.
- @9git closure:
	- Updated git artifact status to DONE and recorded pre-commit evidence.
	- Narrow closure commit: `7fc4994bc` (`docs(git): close prj0000102 git handoff`).
	- Pushed branch update to origin and PR #251 reflects latest commits.

## 2026-03-30 — prj0000105 post-merge release registry synchronization

- Trigger: user confirmed PR #258 merged and requested continuation.
- Actions completed:
	- Transitioned `prj0000105` to `Released` using registry governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #258`) in board artifacts.
	- Revalidated project registry/kanban consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000105 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=105`, `kanban_rows=105`).
- Outcome:
	- Post-merge governance state for prj0000105 is synchronized and ready for next project continuation (`prj0000106`).

## 2026-03-30 — prj0000106 post-merge release registry synchronization

- Trigger: user confirmed PR #259 merged and requested project wrap-up and return to main.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000106` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #259`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000106 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=106`, `kanban_rows=106`).
- Outcome:
	- Project prj0000106 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000107 post-merge release registry synchronization

- Trigger: user confirmed PR #260 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000107` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #260`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000107 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=107`, `kanban_rows=107`).
- Outcome:
	- Project prj0000107 is formally closed in Released lane and main is ready for next project allocation (`prj0000108`).

## 2026-03-31 — prj0000108 post-merge release registry synchronization

- Trigger: user confirmed PR #261 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000108` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #261`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000108 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=108`, `kanban_rows=108`).
- Outcome:
	- Project prj0000108 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000109 allocation and initialization for next idea

- Trigger: user requested a new project for the next idea.
- Selection outcome:
	- Candidate scan selected `idea000002-missing-compose-dockerfile` as the next unimplemented `P1` idea not yet represented in the active project registry.
	- Assigned project ID `prj0000109` from `data/nextproject.md` and expected branch `prj0000109-idea000002-missing-compose-dockerfile`.
- Actions completed:
	- Finalized prior idea archival move on `main` and pushed baseline commit.
	- Created and switched to dedicated branch `prj0000109-idea000002-missing-compose-dockerfile`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
- Outcome:
	- New project `prj0000109` is initialized and ready for `@2think` discovery handoff.

## 2026-03-31 — Global lessons-learned workflow hardening (all projects)

- Trigger: user requested implementation of fixes from lessons learned across all projects.
- Changes applied:
	- Enhanced `scripts/project_registry_governance.py` with automated idea archival support:
		- New `sync-idea-archive` command to archive idea files for all `Released` projects.
		- `set-lane --lane Released` now auto-archives matching `ideaNNNNNN-*.md` files.
		- `validate` now fails when released idea-backed projects have unarchived or missing archive files.
	- Extended `tests/docs/test_agent_workflow_policy_docs.py` with policy assertions for release archival requirements and governance command coverage.
- Validation evidence:
	- `python scripts/project_registry_governance.py sync-idea-archive` -> `moved=0` (repository already compliant).
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.

## 2026-04-01 — prj0000111 post-merge release registry synchronization

- Trigger: user requested continuation after PR #264 check-fix cycle and merge.
- Actions completed:
	- Verified PR #264 merged (`headRefName=prj0000111-ci-detached-head-governance-gate`, merged at `2026-04-01T07:29:54Z`).
	- Registered missing `prj0000111` in canonical governance artifacts:
		- `docs/project/kanban.json`
		- `docs/project/kanban.md`
		- `data/projects.json`
		- `data/nextproject.md` advanced to `prj0000112`.
	- Updated lane metrics in kanban markdown header/summary to keep board counters consistent.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=111`, `kanban_rows=111`).
- Outcome:
	- Project `prj0000111` is formally closed in `Released` lane and next ID allocation baseline is restored.

## 2026-04-01 — prj0000110 allocation and initialization for next idea

- Trigger: user requested to start the next project.
- Selection outcome:
	- Candidate scan selected `idea000004-quality-workflow-branch-trigger` as the next unimplemented idea not represented in active project tags.
	- Assigned project ID `prj0000110` from `data/nextproject.md` and expected branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
- Actions completed:
	- Created and switched to dedicated branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=110`, `kanban_rows=110`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- New project `prj0000110` is initialized in Discovery and ready for `@2think` handoff.

## 2026-04-01 — prj0000110 CI workload reduction implementation

- Trigger: user approved implementing CI reductions using pre-commit-aligned governance.
- Actions completed:
	- Updated `.github/workflows/ci.yml` to add a single-run `governance` job (`Governance Gate`) that runs pre-commit quality hooks and strict mypy once per workflow.
	- Reduced shard duplication in `test` job by removing repeated strict mypy execution across all 10 shards.
	- Added conditional Rust build skip for lightweight shards 1-3 to reduce unnecessary setup cost.
	- Expanded `tests/ci/test_ci_workflow.py` with assertions that lock the new governance/test-shard responsibilities.
- Validation evidence:
	- `python -m pytest -q tests/ci/test_ci_workflow.py` -> `6 passed`.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- CI now performs governance checks once and keeps shard jobs focused on tests, reducing duplicated work while preserving deterministic policy gates.

## 2026-04-01 — Added @10idea agent for idea merge and archival governance

- Trigger: user requested a dedicated idea curation agent to monitor `docs/project/ideas`, merge similar ideas into a new consolidated idea, and archive superseded ideas.
- Actions completed:
	- Added `.github/agents/10idea.agent.md` with explicit workflow for similarity detection, merged-idea creation, and archive moves.
	- Added role support files:
		- `.github/agents/tools/10idea.tools.md`
		- `.github/agents/skills/10idea.skills.md`
		- `.github/agents/data/current.10idea.memory.md`
		- `.github/agents/data/history.10idea.memory.md`
		- `.github/agents/data/2026-04-01.10idea.log.md`
	- Integrated `@10idea` into UI/runtime discovery paths:
		- `web/vite.config.ts` valid agent-doc IDs
		- `web/apps/CodeBuilder.tsx` agent type + catalog entry
		- `web/apps/OrchestrationGraph.tsx` stage list
		- `web/apps/ProjectManager.tsx` required flow + responsibilities text
- Outcome:
	- `@10idea` is now available as a first-class agent for idea deduplication and archival operations.

## 2026-03-31 — prj0000109 post-merge release registry synchronization

- Trigger: user confirmed PR #262 merged.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000109` to `Released` via governance tooling with canonical merged metadata (`branch: merged`, `pr: #262`).
	- Auto-archived the released idea file `idea000002-missing-compose-dockerfile.md` into `docs/project/ideas/archive/` via governance automation.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000109 --lane Released --branch merged --pr #262` -> updated and archived 1 idea file.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
- Outcome:
	- Project prj0000109 is formally closed in Released lane and release-closure archival policy was applied automatically.


## 2026-04-02 — prj0000114 escalated to artifact-driven pipeline refactor

- Trigger: user requested a fuller refactor for IdeaTracker because 200k ideas is only the beginning and incremental outputs/artifacts are needed for future scale.
- Planning delivered by @4plan:
	- Refactor plan written to `docs/project/prj0000114-ideatracker-batching-verbosity/ideatracker-batching-verbosity.plan.md`.
	- Direction: keep `scripts/IdeaTracker.py` as CLI entrypoint, move heavy work behind helper modules, and persist deterministic batch artifacts under `docs/project/`.
- Implementation delivered by @6code:
	- Added helper modules:
		- `scripts/idea_tracker_artifacts.py`
		- `scripts/idea_tracker_pipeline.py`
		- `scripts/idea_tracker_similarity.py`
	- Refactored `scripts/IdeaTracker.py` into an artifact-driven pipeline.
	- Added/maintained batch-persisted artifacts in `docs/project/` for:
		- progress
		- mapping
		- references
		- section names
		- tokens
		- similarities
	- Preserved final outputs:
		- `docs/project/ideatracker.json`
		- split `docs/project/ideatracker-NNNNNN.json` files
	- Added rewrite-safe incremental behavior so rerunning the same batch window replaces stable rows rather than duplicating them.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `26 passed, 0 failed`
	- editor diagnostics: no errors in pipeline modules or tracker tests.
- Current branch: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — prj0000114 IdeaTracker batching and verbosity project initialized and implemented

- Trigger: user requested `scripts/IdeaTracker.py` become more verbose and scale better for 100,000+ ideas with batch processing around 1000.
- Project boundary assigned:
	- Project id: `prj0000114`
	- Branch: `prj0000114-ideatracker-batching-verbosity`
	- Lane: `Discovery`
- Governance setup delivered by @1project:
	- Added project artifacts under `docs/project/prj0000114-ideatracker-batching-verbosity/`
	- Updated `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`
	- Validation:
		- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
- Implementation delivered by @6code:
	- `scripts/IdeaTracker.py`: added batch-size and verbose support, stderr progress logging, and blocking-based duplicate candidate narrowing to avoid full O(n^2) comparisons.
	- `tests/test_idea_tracker.py`: added focused coverage for batching/progress and duplicate-candidate blocking behavior.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `16 passed, 0 failed`
	- editor diagnostics: no errors in `scripts/IdeaTracker.py` or `tests/test_idea_tracker.py`
- Notes:
	- Unrelated pre-existing idea-merge workspace changes were preserved and not used as scope for `prj0000114` implementation.
	- Current branch after handoff: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — @10idea merge/archive pass executed

- Trigger: user requested another @10idea merge of similar ideas and archival of superseded ideas.
- Branch gate:
	- Observed before action: `main` (blocked for project-scoped idea maintenance).
	- Switched to: `feature/idea-merge-archive-10idea` before delegation.
- Delegation: @10idea executed candidate analysis with existing idea tooling and performed one high-confidence semantic consolidation.
- Delivered:
	- Created `docs/project/ideas/idea000132-external-ai-learning-jsonl-shards-hardening.md`.
	- Archived (moved):
		- `docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000123-shard-202602-306-jsonl-hardening.md`
		- `docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000124-shard-202602-693-jsonl-hardening.md`
	- Refreshed `docs/project/ideatracker.json`.
- Reported tracker deltas:
	- total: 131 -> 132
	- active: 120 -> 119
	- archived: 11 -> 13
	- ready: 51 -> 52
	- blocked: 80 -> 80
- Governance validation:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`.

## 2026-04-02 — PR #270 merged (pre-commit-first quality gates)

- Branch: `feature/idea-merge-archive-10idea` → main
- Merge commit: `be6513c50f`
- Contents merged:
	- `.pre-commit-config.yaml`: added ruff-format, rust-fmt, rust-clippy; upgraded secret-scan to --fail-on-severity HIGH
	- `.github/workflows/security.yml`: deleted (redundant — ci.yml covers via pre-commit run --all-files)
	- `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`: created
	- `docs/project/ideas/archive/idea000{004,005,006,007}*`: archived (superseded by idea000131)
	- `docs/project/ideatracker.json`: active=120, archived=11
- Note: PR #269 (full legacy corpus, 206k ideas) also already merged at 4ab8ef807f.
- Current HEAD: be6513c50f (main, clean, up to date)
- Status: CLOSED

## 2026-04-01 — Parallel-first agent coordination policy

- Trigger: user requested agents to operate more independently and in parallel where safe.
- Decision:
	- Adopt parallel-first delegation for independent work packages.
	- Enforce explicit file ownership boundaries per work package.
	- Require synchronization barriers before implementation and before validation/git.
	- Keep git-affecting operations strictly sequential.
- Files updated:
	- `.github/agents/0master.agent.md`
	- `.github/agents/tools/0master.tools.md`
	- `.github/agents/governance/shared-governance-checklist.md`
- Expected effect:
	- Higher throughput in discovery/planning phases without increasing branch/scope risk.
	- Reduced coordination bottlenecks by making parallelization default when isolation is clear.

## 2026-04-01 — Parallel policy rollout across specialist agents

- Trigger: user requested additional improvement after initial parallel-first master/governance update.
- Decision:
	- Extend independent-parallel policy into role-local instructions for `@1project`..`@10idea`.
	- Keep git-affecting and final signoff actions strictly sequential.
- Files updated:
	- `.github/agents/1project.agent.md`
	- `.github/agents/2think.agent.md`
	- `.github/agents/3design.agent.md`
	- `.github/agents/4plan.agent.md`
	- `.github/agents/5test.agent.md`
	- `.github/agents/6code.agent.md`
	- `.github/agents/7exec.agent.md`
	- `.github/agents/8ql.agent.md`
	- `.github/agents/9git.agent.md`
	- `.github/agents/10idea.agent.md`
- Validation:
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.

## 2026-04-01 — Shared parallel agent register

- Trigger: user requested shared JSON register for parallel work tracking across `@0master` and all sub-agents.
- Delivered:
	- Added canonical register file: `.github/agents/data/parallel_agents_register.json`.
	- Added mandatory register usage to `@0master` policy and shared governance checklist.
	- Added lock/touched-file coordination requirement to 0master tools guidance.
- Register scope:
	- active wave metadata, per-agent package status, touched/planned files, lock ids, file locks, lockfiles, and event log.
- Expected effect:
	- deterministic parallel ownership and conflict prevention for overlapping file edits.

## 2026-04-01 — Executable parallel register CLI

- Trigger: user requested next-step executable tooling for atomic and standardized register updates.
- Delivered:
	- Added `scripts/parallel_register.py` with commands:
	  - `acquire-lock`
	  - `release-lock`
	  - `touch-file`
	  - `close-wave`
	- Added focused tests: `tests/test_parallel_register.py`.
	- Added governance/tooling references for standardized command usage.
- Validation:
	- `python -m pytest -q tests/test_parallel_register.py` -> `4 passed`.

## 2026-03-29 — Agent workflow hardening from lessons-learned sweep

- Scope: reviewed all agent instruction files and cross-checked recurring blockers from history memory logs.
- Changes applied:
	- Raised @0master pre-delegation scorecard with two additional hard-gate categories: docs-policy readiness and pre-commit baseline readiness.
	- Upgraded @1project `<project>.git.md` template to modern Branch Plan / Scope Validation / Failure Disposition format to prevent docs-policy drift.
	- Added @7exec interruption handling rule: repeated `KeyboardInterrupt`/inconclusive full-suite runs now block handoff.
	- Added @7exec mandatory docs-policy gate before @8ql handoff.
	- Added @8ql mandatory exact failing-selector rerun evidence for blocker-remediation passes.
	- Added @9git docs-only closure preflight for repo-wide `run-precommit-checks` baseline debt visibility.
	- Added project-artifact docs-policy validation command in operational inputs for all agents (`0master`..`9git`).
- Rationale:
	- Addresses recurring failures seen in history memory: missing `## Branch Plan` in project git artifacts, inconclusive interrupted validation runs, and docs-only git closures blocked late by repo-wide pre-commit debt.
- Next actions:
	- Validate policy docs tests and architecture ADR governance tests.
	- If green, keep these rules as active hardening baseline.

## 2026-03-29 — Cross-link rollout to shared governance checklist

- Scope: created one canonical governance checklist and linked all ten agent files to consume it at task start.
- Changes applied:
	- Added `.github/agents/governance/shared-governance-checklist.md` as the shared source for branch/scope/docs-policy and handoff-evidence gates.
	- Updated `.github/agents/0master.agent.md` through `.github/agents/9git.agent.md` operational sections to read and apply the shared checklist.
- Validation:
	- `pytest tests/docs/test_agent_workflow_policy_docs.py tests/docs/test_architecture_adr_governance.py` -> `15 passed`.

## 2026-03-29 — CI shard-1 coverage gate remediation

- Trigger: GitHub Actions run 23716956870 failed at job `Run tests (shard 1/10)`, step `Coverage gate (stage 1)`.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- Direction accepted: switch gate to `--cov=src` and run tests that actually execute `src`.
- Change delegated to @6code:
	- `.github/workflows/ci.yml` coverage gate command updated to:
	  - `pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=40 -q`
- Validation evidence:
	- `pytest tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py -q` -> `13 passed`.
	- New gate command run locally -> `Required test coverage of 40% reached. Total coverage: 94.48%`.

## 2026-03-29 — prj0000101 @9git continuation and PR #250 verification

- Preflight branch gate:
	- Observed branch: `prj0000101-pending-definition`
	- Expected branch (from project Branch Plan): `prj0000101-pending-definition`
	- Result: PASS
- PR verification:
	- Active PR payload confirms PR #250 is OPEN and includes health-probe implementation/test diffs.
	- Local branch tip before remediation: `fedc7658f`.
- Delegated remediation to @6code for unresolved major `web/apps/ProjectManager.tsx` review comments:
	1. remove unrelated fallback SWOT/risk context in idea-scoped prompt generation.
	2. source fresh kanban register content at trigger time with graceful fallback.
- @6code result:
	- Commit: `4c2d56938` (`fix(projectmanager): use idea-only insight context and fresh kanban source`).
	- Validation reported: no file diagnostics, `web` build passed, targeted ProjectManager tests passed.
- Git handoff progress:
	- Pushed branch update: `fedc7658f..4c2d56938` to `origin/prj0000101-pending-definition`.
	- @9git closure still requires final PR-level merge decision.

## 2026-03-29 — Post-merge continuation into prj0000102

- Trigger: user confirmed PR merged and requested continuation.
- Governance normalization performed:
	- Fixed lane drift via governance tooling and validated registry/kanban consistency.
	- Current result: `VALIDATION_OK` with `projects=102` and `kanban_rows=102`.
- Branch isolation enforced:
	- Created and switched to dedicated project branch `prj0000102-pyproject-requirements-sync`.
- Delegation progression completed:
	- @1project initialized canonical project artifacts and synced registry metadata for prj0000102.
	- @2think completed options exploration.
	- @3design finalized selected design.
	- @4plan finalized implementation roadmap.
	- @5test finalized test artifact and handoff criteria.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> OK.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` passed in each delegated phase.
- Delivery state:
	- Branch pushed: `origin/prj0000102-pyproject-requirements-sync`.
	- Ready for @6code implementation handoff on prj0000102.

## 2026-03-30 — prj0000102 @6code implementation completion

- Trigger: user requested automatic continuation into @6code implementation.
- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch (project Branch Plan): `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @6code delivery:
	- Implemented canonical dependency authority and deterministic requirements emission.
	- Added dependency drift and policy enforcement wiring into shared CI checks.
	- Added/updated concrete tests for canonical-source, deterministic output, drift gate, and policy validation.
	- Updated project code artifact status for implementation evidence.
- @6code commit:
	- `5658a0e00` — `feat(deps): enforce canonical pyproject requirements sync`.
- Validation evidence (reported by @6code):
	- dependency selectors and targeted test files passing.
	- docs policy test passing.
	- ruff and mypy passing for touched implementation files.
	- dependency audit `--check` passing.
- Publish state:
	- Pushed `30e7ecf65..5658a0e00` to `origin/prj0000102-pyproject-requirements-sync`.
- Next workflow step:
	- Ready for @7exec runtime validation handoff.

## 2026-03-30 — prj0000102 @7exec/@8ql/@9git closure progression

- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch: `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @7exec completion:
	- Runtime validation suite executed and logged.
	- Exec artifact committed: `85027f9e9`.
- @8ql completion:
	- Focused quality/security checks completed with clear gate.
	- QL artifact committed: `44bcf6fa8`.
- @9git first pass:
	- Opened PR #251 for `prj0000102-pyproject-requirements-sync` -> `main`.
	- Initial artifact state BLOCKED due formatter baseline failure (`tests/tools/test_dependency_audit.py`).
- Blocker remediation:
	- Applied formatter fix to blocker file and re-ran formatter gate successfully.
	- Re-ran docs policy gate successfully.
- @9git closure:
	- Updated git artifact status to DONE and recorded pre-commit evidence.
	- Narrow closure commit: `7fc4994bc` (`docs(git): close prj0000102 git handoff`).
	- Pushed branch update to origin and PR #251 reflects latest commits.

## 2026-03-30 — prj0000105 post-merge release registry synchronization

- Trigger: user confirmed PR #258 merged and requested continuation.
- Actions completed:
	- Transitioned `prj0000105` to `Released` using registry governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #258`) in board artifacts.
	- Revalidated project registry/kanban consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000105 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=105`, `kanban_rows=105`).
- Outcome:
	- Post-merge governance state for prj0000105 is synchronized and ready for next project continuation (`prj0000106`).

## 2026-03-30 — prj0000106 post-merge release registry synchronization

- Trigger: user confirmed PR #259 merged and requested project wrap-up and return to main.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000106` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #259`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000106 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=106`, `kanban_rows=106`).
- Outcome:
	- Project prj0000106 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000107 post-merge release registry synchronization

- Trigger: user confirmed PR #260 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000107` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #260`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000107 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=107`, `kanban_rows=107`).
- Outcome:
	- Project prj0000107 is formally closed in Released lane and main is ready for next project allocation (`prj0000108`).

## 2026-03-31 — prj0000108 post-merge release registry synchronization

- Trigger: user confirmed PR #261 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000108` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #261`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000108 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=108`, `kanban_rows=108`).
- Outcome:
	- Project prj0000108 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000109 allocation and initialization for next idea

- Trigger: user requested a new project for the next idea.
- Selection outcome:
	- Candidate scan selected `idea000002-missing-compose-dockerfile` as the next unimplemented `P1` idea not yet represented in the active project registry.
	- Assigned project ID `prj0000109` from `data/nextproject.md` and expected branch `prj0000109-idea000002-missing-compose-dockerfile`.
- Actions completed:
	- Finalized prior idea archival move on `main` and pushed baseline commit.
	- Created and switched to dedicated branch `prj0000109-idea000002-missing-compose-dockerfile`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
- Outcome:
	- New project `prj0000109` is initialized and ready for `@2think` discovery handoff.

## 2026-03-31 — Global lessons-learned workflow hardening (all projects)

- Trigger: user requested implementation of fixes from lessons learned across all projects.
- Changes applied:
	- Enhanced `scripts/project_registry_governance.py` with automated idea archival support:
		- New `sync-idea-archive` command to archive idea files for all `Released` projects.
		- `set-lane --lane Released` now auto-archives matching `ideaNNNNNN-*.md` files.
		- `validate` now fails when released idea-backed projects have unarchived or missing archive files.
	- Extended `tests/docs/test_agent_workflow_policy_docs.py` with policy assertions for release archival requirements and governance command coverage.
- Validation evidence:
	- `python scripts/project_registry_governance.py sync-idea-archive` -> `moved=0` (repository already compliant).
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.

## 2026-04-01 — prj0000111 post-merge release registry synchronization

- Trigger: user requested continuation after PR #264 check-fix cycle and merge.
- Actions completed:
	- Verified PR #264 merged (`headRefName=prj0000111-ci-detached-head-governance-gate`, merged at `2026-04-01T07:29:54Z`).
	- Registered missing `prj0000111` in canonical governance artifacts:
		- `docs/project/kanban.json`
		- `docs/project/kanban.md`
		- `data/projects.json`
		- `data/nextproject.md` advanced to `prj0000112`.
	- Updated lane metrics in kanban markdown header/summary to keep board counters consistent.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=111`, `kanban_rows=111`).
- Outcome:
	- Project `prj0000111` is formally closed in `Released` lane and next ID allocation baseline is restored.

## 2026-04-01 — prj0000110 allocation and initialization for next idea

- Trigger: user requested to start the next project.
- Selection outcome:
	- Candidate scan selected `idea000004-quality-workflow-branch-trigger` as the next unimplemented idea not represented in active project tags.
	- Assigned project ID `prj0000110` from `data/nextproject.md` and expected branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
- Actions completed:
	- Created and switched to dedicated branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=110`, `kanban_rows=110`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- New project `prj0000110` is initialized in Discovery and ready for `@2think` handoff.

## 2026-04-01 — prj0000110 CI workload reduction implementation

- Trigger: user approved implementing CI reductions using pre-commit-aligned governance.
- Actions completed:
	- Updated `.github/workflows/ci.yml` to add a single-run `governance` job (`Governance Gate`) that runs pre-commit quality hooks and strict mypy once per workflow.
	- Reduced shard duplication in `test` job by removing repeated strict mypy execution across all 10 shards.
	- Added conditional Rust build skip for lightweight shards 1-3 to reduce unnecessary setup cost.
	- Expanded `tests/ci/test_ci_workflow.py` with assertions that lock the new governance/test-shard responsibilities.
- Validation evidence:
	- `python -m pytest -q tests/ci/test_ci_workflow.py` -> `6 passed`.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- CI now performs governance checks once and keeps shard jobs focused on tests, reducing duplicated work while preserving deterministic policy gates.

## 2026-04-01 — Added @10idea agent for idea merge and archival governance

- Trigger: user requested a dedicated idea curation agent to monitor `docs/project/ideas`, merge similar ideas into a new consolidated idea, and archive superseded ideas.
- Actions completed:
	- Added `.github/agents/10idea.agent.md` with explicit workflow for similarity detection, merged-idea creation, and archive moves.
	- Added role support files:
		- `.github/agents/tools/10idea.tools.md`
		- `.github/agents/skills/10idea.skills.md`
		- `.github/agents/data/current.10idea.memory.md`
		- `.github/agents/data/history.10idea.memory.md`
		- `.github/agents/data/2026-04-01.10idea.log.md`
	- Integrated `@10idea` into UI/runtime discovery paths:
		- `web/vite.config.ts` valid agent-doc IDs
		- `web/apps/CodeBuilder.tsx` agent type + catalog entry
		- `web/apps/OrchestrationGraph.tsx` stage list
		- `web/apps/ProjectManager.tsx` required flow + responsibilities text
- Outcome:
	- `@10idea` is now available as a first-class agent for idea deduplication and archival operations.

## 2026-03-31 — prj0000109 post-merge release registry synchronization

- Trigger: user confirmed PR #262 merged.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000109` to `Released` via governance tooling with canonical merged metadata (`branch: merged`, `pr: #262`).
	- Auto-archived the released idea file `idea000002-missing-compose-dockerfile.md` into `docs/project/ideas/archive/` via governance automation.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000109 --lane Released --branch merged --pr #262` -> updated and archived 1 idea file.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
- Outcome:
	- Project prj0000109 is formally closed in Released lane and release-closure archival policy was applied automatically.

## 2026-04-02 — prj0000114 escalated to artifact-driven pipeline refactor

- Trigger: user requested a fuller refactor for IdeaTracker because 200k ideas is only the beginning and incremental outputs/artifacts are needed for future scale.
- Planning delivered by @4plan:
	- Refactor plan written to `docs/project/prj0000114-ideatracker-batching-verbosity/ideatracker-batching-verbosity.plan.md`.
	- Direction: keep `scripts/IdeaTracker.py` as CLI entrypoint, move heavy work behind helper modules, and persist deterministic batch artifacts under `docs/project/`.
- Implementation delivered by @6code:
	- Added helper modules:
		- `scripts/idea_tracker_artifacts.py`
		- `scripts/idea_tracker_pipeline.py`
		- `scripts/idea_tracker_similarity.py`
	- Refactored `scripts/IdeaTracker.py` into an artifact-driven pipeline.
	- Added/maintained batch-persisted artifacts in `docs/project/` for:
		- progress
		- mapping
		- references
		- section names
		- tokens
		- similarities
	- Preserved final outputs:
		- `docs/project/ideatracker.json`
		- split `docs/project/ideatracker-NNNNNN.json` files
	- Added rewrite-safe incremental behavior so rerunning the same batch window replaces stable rows rather than duplicating them.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `26 passed, 0 failed`
	- editor diagnostics: no errors in pipeline modules or tracker tests.
- Current branch: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — prj0000114 IdeaTracker batching and verbosity project initialized and implemented

- Trigger: user requested `scripts/IdeaTracker.py` become more verbose and scale better for 100,000+ ideas with batch processing around 1000.
- Project boundary assigned:
	- Project id: `prj0000114`
	- Branch: `prj0000114-ideatracker-batching-verbosity`
	- Lane: `Discovery`
- Governance setup delivered by @1project:
	- Added project artifacts under `docs/project/prj0000114-ideatracker-batching-verbosity/`
	- Updated `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`
	- Validation:
		- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
- Implementation delivered by @6code:
	- `scripts/IdeaTracker.py`: added batch-size and verbose support, stderr progress logging, and blocking-based duplicate candidate narrowing to avoid full O(n^2) comparisons.
	- `tests/test_idea_tracker.py`: added focused coverage for batching/progress and duplicate-candidate blocking behavior.
- Direct validation by @0master:
	- `runTests tests/test_idea_tracker.py` -> `16 passed, 0 failed`
	- editor diagnostics: no errors in `scripts/IdeaTracker.py` or `tests/test_idea_tracker.py`
- Notes:
	- Unrelated pre-existing idea-merge workspace changes were preserved and not used as scope for `prj0000114` implementation.
	- Current branch after handoff: `prj0000114-ideatracker-batching-verbosity`

## 2026-04-02 — @10idea merge/archive pass executed

- Trigger: user requested another @10idea merge of similar ideas and archival of superseded ideas.
- Branch gate:
	- Observed before action: `main` (blocked for project-scoped idea maintenance).
	- Switched to: `feature/idea-merge-archive-10idea` before delegation.
- Delegation: @10idea executed candidate analysis with existing idea tooling and performed one high-confidence semantic consolidation.
- Delivered:
	- Created `docs/project/ideas/idea000132-external-ai-learning-jsonl-shards-hardening.md`.
	- Archived (moved):
		- `docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000123-shard-202602-306-jsonl-hardening.md`
		- `docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md` -> `docs/project/ideas/archive/idea000124-shard-202602-693-jsonl-hardening.md`
	- Refreshed `docs/project/ideatracker.json`.
- Reported tracker deltas:
	- total: 131 -> 132
	- active: 120 -> 119
	- archived: 11 -> 13
	- ready: 51 -> 52
	- blocked: 80 -> 80
- Governance validation:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`.

## 2026-04-02 — PR #270 merged (pre-commit-first quality gates)

- Branch: `feature/idea-merge-archive-10idea` → main
- Merge commit: `be6513c50f`
- Contents merged:
	- `.pre-commit-config.yaml`: added ruff-format, rust-fmt, rust-clippy; upgraded secret-scan to --fail-on-severity HIGH
	- `.github/workflows/security.yml`: deleted (redundant — ci.yml covers via pre-commit run --all-files)
	- `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`: created
	- `docs/project/ideas/archive/idea000{004,005,006,007}*`: archived (superseded by idea000131)
	- `docs/project/ideatracker.json`: active=120, archived=11
- Note: PR #269 (full legacy corpus, 206k ideas) also already merged at 4ab8ef807f.
- Current HEAD: be6513c50f (main, clean, up to date)
- Status: CLOSED

## 2026-04-01 — Parallel-first agent coordination policy

- Trigger: user requested agents to operate more independently and in parallel where safe.
- Decision:
	- Adopt parallel-first delegation for independent work packages.
	- Enforce explicit file ownership boundaries per work package.
	- Require synchronization barriers before implementation and before validation/git.
	- Keep git-affecting operations strictly sequential.
- Files updated:
	- `.github/agents/0master.agent.md`
	- `.github/agents/tools/0master.tools.md`
	- `.github/agents/governance/shared-governance-checklist.md`
- Expected effect:
	- Higher throughput in discovery/planning phases without increasing branch/scope risk.
	- Reduced coordination bottlenecks by making parallelization default when isolation is clear.

## 2026-04-01 — Parallel policy rollout across specialist agents

- Trigger: user requested additional improvement after initial parallel-first master/governance update.
- Decision:
	- Extend independent-parallel policy into role-local instructions for `@1project`..`@10idea`.
	- Keep git-affecting and final signoff actions strictly sequential.
- Files updated:
	- `.github/agents/1project.agent.md`
	- `.github/agents/2think.agent.md`
	- `.github/agents/3design.agent.md`
	- `.github/agents/4plan.agent.md`
	- `.github/agents/5test.agent.md`
	- `.github/agents/6code.agent.md`
	- `.github/agents/7exec.agent.md`
	- `.github/agents/8ql.agent.md`
	- `.github/agents/9git.agent.md`
	- `.github/agents/10idea.agent.md`
- Validation:
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.

## 2026-04-01 — Shared parallel agent register

- Trigger: user requested shared JSON register for parallel work tracking across `@0master` and all sub-agents.
- Delivered:
	- Added canonical register file: `.github/agents/data/parallel_agents_register.json`.
	- Added mandatory register usage to `@0master` policy and shared governance checklist.
	- Added lock/touched-file coordination requirement to 0master tools guidance.
- Register scope:
	- active wave metadata, per-agent package status, touched/planned files, lock ids, file locks, lockfiles, and event log.
- Expected effect:
	- deterministic parallel ownership and conflict prevention for overlapping file edits.

## 2026-04-01 — Executable parallel register CLI

- Trigger: user requested next-step executable tooling for atomic and standardized register updates.
- Delivered:
	- Added `scripts/parallel_register.py` with commands:
	  - `acquire-lock`
	  - `release-lock`
	  - `touch-file`
	  - `close-wave`
	- Added focused tests: `tests/test_parallel_register.py`.
	- Added governance/tooling references for standardized command usage.
- Validation:
	- `python -m pytest -q tests/test_parallel_register.py` -> `4 passed`.

## 2026-03-29 — Agent workflow hardening from lessons-learned sweep

- Scope: reviewed all agent instruction files and cross-checked recurring blockers from history memory logs.
- Changes applied:
	- Raised @0master pre-delegation scorecard with two additional hard-gate categories: docs-policy readiness and pre-commit baseline readiness.
	- Upgraded @1project `<project>.git.md` template to modern Branch Plan / Scope Validation / Failure Disposition format to prevent docs-policy drift.
	- Added @7exec interruption handling rule: repeated `KeyboardInterrupt`/inconclusive full-suite runs now block handoff.
	- Added @7exec mandatory docs-policy gate before @8ql handoff.
	- Added @8ql mandatory exact failing-selector rerun evidence for blocker-remediation passes.
	- Added @9git docs-only closure preflight for repo-wide `run-precommit-checks` baseline debt visibility.
	- Added project-artifact docs-policy validation command in operational inputs for all agents (`0master`..`9git`).
- Rationale:
	- Addresses recurring failures seen in history memory: missing `## Branch Plan` in project git artifacts, inconclusive interrupted validation runs, and docs-only git closures blocked late by repo-wide pre-commit debt.
- Next actions:
	- Validate policy docs tests and architecture ADR governance tests.
	- If green, keep these rules as active hardening baseline.

## 2026-03-29 — Cross-link rollout to shared governance checklist

- Scope: created one canonical governance checklist and linked all ten agent files to consume it at task start.
- Changes applied:
	- Added `.github/agents/governance/shared-governance-checklist.md` as the shared source for branch/scope/docs-policy and handoff-evidence gates.
	- Updated `.github/agents/0master.agent.md` through `.github/agents/9git.agent.md` operational sections to read and apply the shared checklist.
- Validation:
	- `pytest tests/docs/test_agent_workflow_policy_docs.py tests/docs/test_architecture_adr_governance.py` -> `15 passed`.

## 2026-03-29 — CI shard-1 coverage gate remediation

- Trigger: GitHub Actions run 23716956870 failed at job `Run tests (shard 1/10)`, step `Coverage gate (stage 1)`.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- Direction accepted: switch gate to `--cov=src` and run tests that actually execute `src`.
- Change delegated to @6code:
	- `.github/workflows/ci.yml` coverage gate command updated to:
	  - `pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=40 -q`
- Validation evidence:
	- `pytest tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py -q` -> `13 passed`.
	- New gate command run locally -> `Required test coverage of 40% reached. Total coverage: 94.48%`.

## 2026-03-29 — prj0000101 @9git continuation and PR #250 verification

- Preflight branch gate:
	- Observed branch: `prj0000101-pending-definition`
	- Expected branch (from project Branch Plan): `prj0000101-pending-definition`
	- Result: PASS
- PR verification:
	- Active PR payload confirms PR #250 is OPEN and includes health-probe implementation/test diffs.
	- Local branch tip before remediation: `fedc7658f`.
- Delegated remediation to @6code for unresolved major `web/apps/ProjectManager.tsx` review comments:
	1. remove unrelated fallback SWOT/risk context in idea-scoped prompt generation.
	2. source fresh kanban register content at trigger time with graceful fallback.
- @6code result:
	- Commit: `4c2d56938` (`fix(projectmanager): use idea-only insight context and fresh kanban source`).
	- Validation reported: no file diagnostics, `web` build passed, targeted ProjectManager tests passed.
- Git handoff progress:
	- Pushed branch update: `fedc7658f..4c2d56938` to `origin/prj0000101-pending-definition`.
	- @9git closure still requires final PR-level merge decision.

## 2026-03-29 — Post-merge continuation into prj0000102

- Trigger: user confirmed PR merged and requested continuation.
- Governance normalization performed:
	- Fixed lane drift via governance tooling and validated registry/kanban consistency.
	- Current result: `VALIDATION_OK` with `projects=102` and `kanban_rows=102`.
- Branch isolation enforced:
	- Created and switched to dedicated project branch `prj0000102-pyproject-requirements-sync`.
- Delegation progression completed:
	- @1project initialized canonical project artifacts and synced registry metadata for prj0000102.
	- @2think completed options exploration.
	- @3design finalized selected design.
	- @4plan finalized implementation roadmap.
	- @5test finalized test artifact and handoff criteria.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> OK.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` passed in each delegated phase.
- Delivery state:
	- Branch pushed: `origin/prj0000102-pyproject-requirements-sync`.
	- Ready for @6code implementation handoff on prj0000102.

## 2026-03-30 — prj0000102 @6code implementation completion

- Trigger: user requested automatic continuation into @6code implementation.
- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch (project Branch Plan): `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @6code delivery:
	- Implemented canonical dependency authority and deterministic requirements emission.
	- Added dependency drift and policy enforcement wiring into shared CI checks.
	- Added/updated concrete tests for canonical-source, deterministic output, drift gate, and policy validation.
	- Updated project code artifact status for implementation evidence.
- @6code commit:
	- `5658a0e00` — `feat(deps): enforce canonical pyproject requirements sync`.
- Validation evidence (reported by @6code):
	- dependency selectors and targeted test files passing.
	- docs policy test passing.
	- ruff and mypy passing for touched implementation files.
	- dependency audit `--check` passing.
- Publish state:
	- Pushed `30e7ecf65..5658a0e00` to `origin/prj0000102-pyproject-requirements-sync`.
- Next workflow step:
	- Ready for @7exec runtime validation handoff.

## 2026-03-30 — prj0000102 @7exec/@8ql/@9git closure progression

- Branch gate preflight:
	- Observed branch: `prj0000102-pyproject-requirements-sync`
	- Expected branch: `prj0000102-pyproject-requirements-sync`
	- Result: PASS
- @7exec completion:
	- Runtime validation suite executed and logged.
	- Exec artifact committed: `85027f9e9`.
- @8ql completion:
	- Focused quality/security checks completed with clear gate.
	- QL artifact committed: `44bcf6fa8`.
- @9git first pass:
	- Opened PR #251 for `prj0000102-pyproject-requirements-sync` -> `main`.
	- Initial artifact state BLOCKED due formatter baseline failure (`tests/tools/test_dependency_audit.py`).
- Blocker remediation:
	- Applied formatter fix to blocker file and re-ran formatter gate successfully.
	- Re-ran docs policy gate successfully.
- @9git closure:
	- Updated git artifact status to DONE and recorded pre-commit evidence.
	- Narrow closure commit: `7fc4994bc` (`docs(git): close prj0000102 git handoff`).
	- Pushed branch update to origin and PR #251 reflects latest commits.

## 2026-03-30 — prj0000105 post-merge release registry synchronization

- Trigger: user confirmed PR #258 merged and requested continuation.
- Actions completed:
	- Transitioned `prj0000105` to `Released` using registry governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #258`) in board artifacts.
	- Revalidated project registry/kanban consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000105 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=105`, `kanban_rows=105`).
- Outcome:
	- Post-merge governance state for prj0000105 is synchronized and ready for next project continuation (`prj0000106`).

## 2026-03-30 — prj0000106 post-merge release registry synchronization

- Trigger: user confirmed PR #259 merged and requested project wrap-up and return to main.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000106` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #259`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000106 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=106`, `kanban_rows=106`).
- Outcome:
	- Project prj0000106 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000107 post-merge release registry synchronization

- Trigger: user confirmed PR #260 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000107` from `Review` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #260`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000107 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=107`, `kanban_rows=107`).
- Outcome:
	- Project prj0000107 is formally closed in Released lane and main is ready for next project allocation (`prj0000108`).

## 2026-03-31 — prj0000108 post-merge release registry synchronization

- Trigger: user confirmed PR #261 merged and requested wrap-up on main.
- Actions completed:
	- Transitioned `prj0000108` to `Released` via governance tooling.
	- Corrected released metadata to canonical merged values (`branch: merged`, `pr: #261`) in kanban artifacts.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000108 --lane Released` -> updated.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=108`, `kanban_rows=108`).
- Outcome:
	- Project prj0000108 is formally closed in Released lane and repository state is aligned on `main`.

## 2026-03-31 — prj0000109 allocation and initialization for next idea

- Trigger: user requested a new project for the next idea.
- Selection outcome:
	- Candidate scan selected `idea000002-missing-compose-dockerfile` as the next unimplemented `P1` idea not yet represented in the active project registry.
	- Assigned project ID `prj0000109` from `data/nextproject.md` and expected branch `prj0000109-idea000002-missing-compose-dockerfile`.
- Actions completed:
	- Finalized prior idea archival move on `main` and pushed baseline commit.
	- Created and switched to dedicated branch `prj0000109-idea000002-missing-compose-dockerfile`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
- Outcome:
	- New project `prj0000109` is initialized and ready for `@2think` discovery handoff.

## 2026-03-31 — Global lessons-learned workflow hardening (all projects)

- Trigger: user requested implementation of fixes from lessons learned across all projects.
- Changes applied:
	- Enhanced `scripts/project_registry_governance.py` with automated idea archival support:
		- New `sync-idea-archive` command to archive idea files for all `Released` projects.
		- `set-lane --lane Released` now auto-archives matching `ideaNNNNNN-*.md` files.
		- `validate` now fails when released idea-backed projects have unarchived or missing archive files.
	- Extended `tests/docs/test_agent_workflow_policy_docs.py` with policy assertions for release archival requirements and governance command coverage.
- Validation evidence:
	- `python scripts/project_registry_governance.py sync-idea-archive` -> `moved=0` (repository already compliant).
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.

## 2026-04-01 — prj0000111 post-merge release registry synchronization

- Trigger: user requested continuation after PR #264 check-fix cycle and merge.
- Actions completed:
	- Verified PR #264 merged (`headRefName=prj0000111-ci-detached-head-governance-gate`, merged at `2026-04-01T07:29:54Z`).
	- Registered missing `prj0000111` in canonical governance artifacts:
		- `docs/project/kanban.json`
		- `docs/project/kanban.md`
		- `data/projects.json`
		- `data/nextproject.md` advanced to `prj0000112`.
	- Updated lane metrics in kanban markdown header/summary to keep board counters consistent.
- Validation evidence:
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=111`, `kanban_rows=111`).
- Outcome:
	- Project `prj0000111` is formally closed in `Released` lane and next ID allocation baseline is restored.

## 2026-04-01 — prj0000110 allocation and initialization for next idea

- Trigger: user requested to start the next project.
- Selection outcome:
	- Candidate scan selected `idea000004-quality-workflow-branch-trigger` as the next unimplemented idea not represented in active project tags.
	- Assigned project ID `prj0000110` from `data/nextproject.md` and expected branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
- Actions completed:
	- Created and switched to dedicated branch `prj0000110-idea000004-quality-workflow-branch-trigger`.
	- Delegated initialization to `@1project`, which created canonical project artifacts and synced `kanban.json`, `kanban.md`, `data/projects.json`, and `data/nextproject.md`.
	- Published initialized branch to origin.
- Validation evidence (from `@1project`):
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=110`, `kanban_rows=110`).
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- New project `prj0000110` is initialized in Discovery and ready for `@2think` handoff.

## 2026-04-01 — prj0000110 CI workload reduction implementation

- Trigger: user approved implementing CI reductions using pre-commit-aligned governance.
- Actions completed:
	- Updated `.github/workflows/ci.yml` to add a single-run `governance` job (`Governance Gate`) that runs pre-commit quality hooks and strict mypy once per workflow.
	- Reduced shard duplication in `test` job by removing repeated strict mypy execution across all 10 shards.
	- Added conditional Rust build skip for lightweight shards 1-3 to reduce unnecessary setup cost.
	- Expanded `tests/ci/test_ci_workflow.py` with assertions that lock the new governance/test-shard responsibilities.
- Validation evidence:
	- `python -m pytest -q tests/ci/test_ci_workflow.py` -> `6 passed`.
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
- Outcome:
	- CI now performs governance checks once and keeps shard jobs focused on tests, reducing duplicated work while preserving deterministic policy gates.

## 2026-04-01 — Added @10idea agent for idea merge and archival governance

- Trigger: user requested a dedicated idea curation agent to monitor `docs/project/ideas`, merge similar ideas into a new consolidated idea, and archive superseded ideas.
- Actions completed:
	- Added `.github/agents/10idea.agent.md` with explicit workflow for similarity detection, merged-idea creation, and archive moves.
	- Added role support files:
		- `.github/agents/tools/10idea.tools.md`
		- `.github/agents/skills/10idea.skills.md`
		- `.github/agents/data/current.10idea.memory.md`
		- `.github/agents/data/history.10idea.memory.md`
		- `.github/agents/data/2026-04-01.10idea.log.md`
	- Integrated `@10idea` into UI/runtime discovery paths:
		- `web/vite.config.ts` valid agent-doc IDs
		- `web/apps/CodeBuilder.tsx` agent type + catalog entry
		- `web/apps/OrchestrationGraph.tsx` stage list
		- `web/apps/ProjectManager.tsx` required flow + responsibilities text
- Outcome:
	- `@10idea` is now available as a first-class agent for idea deduplication and archival operations.

## 2026-03-31 — prj0000109 post-merge release registry synchronization

- Trigger: user confirmed PR #262 merged.
- Actions completed:
	- Switched to `main` and fast-forwarded from origin.
	- Transitioned `prj0000109` to `Released` via governance tooling with canonical merged metadata (`branch: merged`, `pr: #262`).
	- Auto-archived the released idea file `idea000002-missing-compose-dockerfile.md` into `docs/project/ideas/archive/` via governance automation.
	- Revalidated registry and board consistency.
- Validation evidence:
	- `python scripts/project_registry_governance.py set-lane --id prj0000109 --lane Released --branch merged --pr #262` -> updated and archived 1 idea file.
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK` (`projects=109`, `kanban_rows=109`).
- Outcome:
	- Project prj0000109 is formally closed in Released lane and release-closure archival policy was applied automatically.

--- Appended from current ---

# Current Memory - 0master

## Metadata
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.0master.memory.md in chronological order, then clear Entries.

## Entries

## 2026-04-04 — prj0000126 released and prj0000127 advanced

- PR `#290` was re-verified as `MERGED` and prj0000126 closure executed.
- @1project closure results for `prj0000126`:
	- Set Released status in `data/projects.json` and `docs/project/kanban.json` with PR linkage.
	- Updated `docs/project/prj0000126-private-key-in-repo/private-key-in-repo.project.md` to closure alignment.
	- Applied idea archival policy: moved `docs/project/ideas/idea000001-private-key-in-repo.md` to `docs/project/ideas/archive/idea000001-private-key-in-repo.md`.
	- Validation: docs policy 17 passed; registry validate VALIDATION_OK projects=149.
	- Commit: `a14eafdffa` pushed.
- Continuation moved to `prj0000127-mypy-strict-enforcement`.
- @2think completed on prj0000127:
	- Replaced placeholder options with concrete progressive strictness alternatives.
	- Updated M1 to DONE.
	- Validation: docs policy 17 passed.
	- Commit: `ed767e8ee5` pushed.
- @3design completed on prj0000127:
	- Produced actionable design for phased mypy strict rollout, CI warn->required gating, rollback/failure handling, and acceptance mapping.
	- Updated M2 to DONE.
	- Validation: docs policy 17 passed.
	- Commit: `bd58fd954f` pushed.
- Next step: @4plan on prj0000127.
- @4plan completed on prj0000127:
	- Produced executable task plan `T-MYPY-001` through `T-MYPY-010` with phased warn->required rollout and rollback checkpoints.
	- Updated M3 to DONE.
	- Validation: docs policy 17 passed.
	- Commit: `f061c45cf8` pushed.
- @5test RED completed on prj0000127:
	- Added RED docs policy tests for strict-lane contract and N=5 promotion contract.
	- RED evidence: targeted selector failed as expected prior to GREEN implementation.
	- Commit: `de56fb3950` pushed.
- @6code GREEN warn-phase completed on prj0000127:
	- Implemented strict allowlist warning lane contract in CI with explicit `--config-file pyproject.toml`.
	- Preserved broad warning lane with explicit `--config-file mypy.ini`.
	- Updated runbook artifacts with F1/F2/F3 rollback taxonomy and N=5 promotion prerequisites.
	- Validation: targeted docs selector passed; full docs policy 19 passed.
	- Commit: `f5eaaddd6f` pushed.
- @7exec validation gate passed on prj0000127:
	- Docs policy selector and full docs policy pass.
	- Strict allowlist mypy command pass and broad mypy warning lane command pass.
	- Commit: `feae4e155b` pushed.
- @8ql quality/security gate passed on prj0000127:
	- Docs policy and registry governance pass; YAML sanity + secret scan clear.
	- No HIGH/CRITICAL blockers.
	- Commit: `6d18812994` pushed.
- @9git handoff:
	- Opened PR `#291` -> https://github.com/UndiFineD/PyAgent/pull/291
	- State: OPEN
	- Scope: warn-phase contracts and gates only; required-phase promotion intentionally deferred.
- Next step: continue with required-phase promotion track (`T-MYPY-007+`) after PR review/merge.

## 2026-04-04 — prj0000126 program kickoff: next 24 ideas started

- User objective: make a rapid implementation plan for next 24 ideas and start projects.
- Branch established: `prj0000126-next-24-ideas-rollout` (from `main`).
- @1project batch startup completed for 24 ideas:
	- Created project boundaries `prj0000126` through `prj0000149`.
	- Lane strategy applied:
		- Discovery: `prj0000126`-`prj0000129`
		- Ideas queue: `prj0000130`-`prj0000149`
	- Added rollout plan artifact in `prj0000126` project folder (6 waves × 4 projects).
	- Registry synchronization:
		- `data/projects.json` updated with 24 new project records.
		- `docs/project/kanban.json` updated with matching lane entries.
		- `data/nextproject.md` advanced to `prj0000150`.
- Governance checks:
	- `tests/docs/test_agent_workflow_policy_docs.py` -> 17 passed.
	- `scripts/project_registry_governance.py validate` -> VALIDATION_OK, projects=149.
- Delivery commit from @1project: `e3b91adfca` pushed.
- Next step for execution speed: run parallel discovery/design on the first 4 Discovery projects (`prj0000126`-`prj0000129`) and keep the remaining 20 in queue.

## 2026-04-04 — prj0000125 @4plan phase complete

- @4plan produced `llm-gateway-lessons-learned-fixes.plan.md` with 6 tasks (T-LGW2-001..006).
- Wave C and D: ZERO remaining — already done in design commit `1c16acfde6`.
- Wave A tasks: T-LGW2-001 (budget-denied RED), T-LGW2-002 (provider-exception RED), T-LGW2-003 (degraded-telemetry RED), T-LGW2-004 (GREEN implementation).
- Wave B tasks: T-LGW2-005 (ordering-skeleton RED), T-LGW2-006 (event_log GREEN).
- Governance: docs policy 17 passed.
- Commit: `af64828b3f plan(prj0000125)` pushed to origin.
- Next step: @5test — write all 4 RED tasks (T-LGW2-001, 002, 003, 005) in one session, parallel-safe.

## 2026-04-04 — prj0000125 @5test RED phase complete

- @5test added RED tests for T-LGW2-001, T-LGW2-002, T-LGW2-003, and T-LGW2-005 in `tests/core/gateway/test_gateway_core_orchestration.py`.
- RED evidence captured as expected (4 failed, 4 passed):
	- budget-denied path still calls provider
	- provider exception still propagates
	- telemetry emit exception still propagates
	- deterministic event-order sentinel fails (`assert 1 < 0`)
- Commit: `3d19b335b7 test(prj0000125)` pushed to origin.
- Next step: @6code GREEN phase for T-LGW2-004 and T-LGW2-006.

## 2026-04-04 — prj0000125 @6code, @7exec, @8ql, @9git progression

- @6code GREEN complete:
	- Implemented fail-closed runtime in `src/core/gateway/gateway_core.py` (budget-denied guard, provider-exception fail envelope, degraded telemetry guard).
	- Implemented deterministic shared `event_log` ordering pattern in `tests/core/gateway/test_gateway_core_orchestration.py`.
	- Validation: `tests/core/gateway/` = 9 passed.
	- Commit: `52d4386d2e` pushed.
- @7exec validation gate:
	- `tests/core/gateway/test_gateway_core_orchestration.py` = 8 passed
	- `tests/core/gateway/test_gateway_core.py` = 1 passed
	- `tests/core/gateway/` = 9 passed
	- `tests/docs/test_agent_workflow_policy_docs.py` = 17 passed
	- Commit: `77b2166d06` pushed.
- @8ql quality/security gate:
	- Focused gateway tests pass, docs governance pass, architecture governance VALIDATION_OK, py_compile pass.
	- No HIGH/CRITICAL blockers.
	- Commit: `2fddad4f67` pushed.
- @9git first attempt blocked by pre-commit D417 (test docstring arg descriptions).
- Remediation wave executed:
	- @6code fixed D417 in orchestration tests and preserved staged ql/register artifacts.
	- Commit: `9fea47aa60` pushed.
- @9git retry:
	- Opened PR `#289` -> https://github.com/UndiFineD/PyAgent/pull/289
	- State: OPEN
	- Title: `prj0000125: gateway lessons-learned fail-closed and deterministic ordering fixes`
	- Branch to `main` handoff completed.

## 2026-04-04 — prj0000125 @3design phase complete

- Trigger: @2think was already done (commit `644dd9dc6f`); user re-submitted "learn all lessons" prompt from new session; advanced to @3design.
- @3design produced `llm-gateway-lessons-learned-fixes.design.md` with 4-wave design:
  - Wave A (Critical): fail-closed runtime — budget-denied guard, provider exception → `status=failed`+`commit_failure`, degraded telemetry trap.
  - Wave B (High): shared chronological event log fixture replaces concatenated `.calls` lists; ordering asserted via `event_log.index()`.
  - Wave C (High): prj0000124 project.md milestones all set DONE; ADR 0009 `## Part 2 — prj0000125 Remediation` appended.
  - Wave D (Closed): `gateway_core.py` is COMPLIANT with snake_case naming standard; no rename needed.
- Governance: docs policy 17 passed; architecture governance VALIDATION_OK (9 ADRs).
- Commit: `1c16acfde6 design(prj0000125)` pushed to origin.
- Next step: @4plan — execute A → B → C → D wave ordering.

## 2026-04-04 — prj0000124 released and prj0000125 initialized

- Trigger: user reported PR `#287` merged and requested wrap-up, switch to `main`, commit uncommitted files, and start a new lessons-learned fixes project.
- prj0000124 wrap-up:
	- Verified merged state of PR `#287` on `main`.
	- @1project performed post-merge closure on `prj0000124-llm-gateway`:
		- `data/projects.json` -> `Released`, `pr: "#287"`
		- `docs/project/kanban.json` -> `Released`, `pr: "#287"`
		- preserved and committed valid outstanding dashboard/project-doc updates already present in working tree.
		- validation: `tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`; `project_registry_governance.py validate` -> `VALIDATION_OK, projects=124`.
	- @9git opened closure PR `#288` for release bookkeeping: https://github.com/UndiFineD/PyAgent/pull/288
- main sync:
	- Switched local repo to `main` and fast-forwarded to merge commit `1392b0f7a5` (PR `#287`).
	- Confirmed `data/nextproject.md` = `prj0000125` before new-project allocation.
- prj0000125 boundary:
	- Project id: `prj0000125`
	- Name: `llm-gateway-lessons-learned-fixes`
	- Branch: `prj0000125-llm-gateway-lessons-learned-fixes`
	- Lane: `Discovery`
	- Source context: follow-up remediation project for lessons learned from merged PR `#287` / prj0000124.
	- Scope themes:
		1. fail-closed gateway runtime hardening (budget denial, provider exceptions, telemetry degradation)
		2. orchestration test determinism fixes
		3. documentation/governance consistency and markdown-lint cleanup
		4. naming/convention review for gateway modules
	- @1project initialized all 9 artifacts, registered prj0000125, and advanced `data/nextproject.md` to `prj0000126`.
	- Validation: `tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`; `project_registry_governance.py validate` -> `VALIDATION_OK, projects=125`.
- Next step: @2think discovery for prj0000125.

## 2026-04-04 — prj0000123 reopened CI stabilization via PR #286
## 2026-04-04 — prj0000124 initialized — LLM Gateway greenfield

## 2026-04-04 — prj0000124 phase-one slice advanced to Review (PR #287)

- Continuation trigger: user requested `continue` after project initialization.
- Delivery progression completed:
	- @2think selected Option C (Hybrid Split-Plane Gateway) and completed options artifact.
	- @3design finalized architecture and created ADR `0009-llm-gateway-hybrid-split-plane.md`.
	- @4plan produced executable roadmap (`T-LGW-001+`) with RED entrypoint.
	- @5test created RED slice in `tests/core/gateway/test_gateway_core_orchestration.py` (contract-level expected failures).
	- @6code implemented green slice in `src/core/gateway/gateway_core.py` + package init.
	- @7exec validated slice and surfaced/cleared two gate blockers (format + core-quality naming/validate contract).
	- @8ql quality/security gate: PASS/CLEAR (no blocking severity).
	- @9git opened PR `#287`: https://github.com/UndiFineD/PyAgent/pull/287.
- Current status:
	- Branch: `prj0000124-llm-gateway`
	- Lane intent: Review (open PR, merge pending)
	- Scope shipped in this slice: fail-closed orchestration contract baseline only, not full gateway.
- Key evidence snapshots:
	- `tests/core/gateway/test_gateway_core_orchestration.py` -> 4 passed
	- `tests/core/gateway/test_gateway_core.py` -> 1 passed
	- `tests/test_core_quality.py -k gateway_core...` -> pass
	- docs/registry/adr governance validations -> pass

- Trigger: user requested wrap-up of prj0000123 and new project start for an LLM Gateway component.
- prj0000123 closure:
	- PR #286 CI: `CI / Lightweight = success` (run `23980087164`). Merged via `gh pr merge 286` → squash SHA `ab7eb81d80`.
	- Registered prj0000123 in `data/projects.json` and `docs/project/kanban.json` as Released (was missing from registry).
	- `data/nextproject.md` advanced to `prj0000124` then `prj0000125` after both registrations.
- prj0000124 project boundary:
	- Project id: `prj0000124`
	- Name: `llm-gateway`
	- Expected branch: `prj0000124-llm-gateway`
	- Lane: `Discovery`
	- Idea tag: none (greenfield)
	- Commit: `b4ebed30c6` on `origin/prj0000124-llm-gateway`
- Feature scope (10 pillars):
	1. Routing and load balancing
	2. Authentication and access control
	3. Token budgeting
	4. Guardrails and policy enforcement
	5. Semantic caching
	6. Model fallback
	7. Observability
	8. Context management
	9. Memory integration
	10. Tool and skill catchers
- Primary source area: `src/core/gateway/` (new subsystem)
- @1project validation evidence:
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
	- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK, projects=124`
- Next step: @2think discovery for prj0000124.
- Active parallel work: prj0000122 (@6code green-phase pending — paused during hotfix/new-project init).
## 2026-04-03 — prj0000120 execution, quality, and git handoff completed

- @7exec validation: PASS
	- `python scripts/generate_backend_openapi.py` -> PASS
	- `python -m pytest -q tests/docs/test_backend_openapi_drift.py` -> PASS (`3 passed`)
	- `python -m pytest -q tests/docs/test_api_docs_exist.py` -> PASS (`8 passed`)
- @8ql gate: PASS/CLEAR for @9git
	- No HIGH/CRITICAL blockers; only informational/low non-blocking notes.
- @9git handoff: completed
	- Narrow staging on project scope.
	- Commits: `9fc8772df8` and `3e8aab7448` pushed to `origin/prj0000120-openapi-spec-generation`.
	- PR opened: `#280` (`feat(prj0000120): backend-only OpenAPI spec generation pipeline`) targeting `main`.
- Disposition: project branch is in review state awaiting user merge signal for post-merge closure.

## 2026-04-02 — prj0000115 allocated for idea000131 ci-security-quality-workflow-consolidation

## 2026-04-02 — prj0000115 @2think discovery completed

- @2think recommended: Option C — Hybrid (fast pre-commit for developer-facing + scheduled CodeQL/pip-audit).
- Key findings:
	- ci.yml already lightweight: runs pre-commit run --all-files + smoke test.
	- .pre-commit-config.yaml already has ruff, mypy, rust-fmt, rust-clippy, secret-scan, enforce-branch.
	- Missing: no scheduled security workflow; CodeQL assets exist but unwired; pip_audit_results.json is manual artifact.
- Open questions for @3design: scan severity thresholds, CodeQL on PRs vs main-only, triage ownership, scheduled runtime budget.
- Think artifact committed: b5939efba6
- Next step: @3design to design scheduled security workflows + lightweight CI contract.


- Trigger: user confirmed PR #271 merged (prj0000114) and requested next project.
- prj0000114 closed: lane moved to Released, pushed, verified VALIDATION_OK (projects=113 before update).
- Memory rollover: current.0master.memory.md entries appended to history. Entries section cleared.
- Switched to main, pulled origin (merged PR #271 at HEAD 878b75235b).
- Project boundary assigned:
	- Project id: prj0000115
	- Idea: idea000131-ci-security-quality-workflow-consolidation
	- Branch: prj0000115-ci-security-quality-workflow-consolidation
	- Lane: Discovery
- @1project delivered:
	- Project artifacts under docs/project/prj0000115-ci-security-quality-workflow-consolidation/
	- Registry updated: kanban.json, data/projects.json, data/nextproject.md (now prj0000116)
	- Idea file updated: planned project mapping = prj0000115
	- python scripts/project_registry_governance.py validate -> VALIDATION_OK, projects=114
	- Docs policy: 16 passed, 1 pre-existing failure (prj0000005 missing legacy git.md)
	- Commit: 1cd2c8041fa89e529dadbc89248250583a48134c pushed to origin
- Memory rollover committed: 04c9a8991f
- Next step: @2think discovery for pre-commit-first CI consolidation options.


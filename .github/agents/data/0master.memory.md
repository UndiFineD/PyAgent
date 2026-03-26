# PyAgent — Master Agent Memory

_Last updated: 2026-03-26_

---

## 2026-03-26 — prj0000078 pm-swot-risk-ui — REVIEW 🔍 PR #219

**Branch:** `prj0000078-pm-swot-risk-ui`  
**PR:** [#219](https://github.com/UndiFineD/PyAgent/pull/219) — open, awaiting merge  
**Status:** REVIEW — full agent workflow complete (@1project→@4plan→@6code→@7exec→@8ql→@9git)  
**Priority:** P3 | **Budget:** S

**Deliverable:** Two toolbar buttons ("SWOT" + "Risk") added to `FilterBar` in `web/apps/ProjectManager.tsx`. Clicking each opens a modal showing the corresponding section from `kanban.md` (loaded via Vite `?raw` build-time import). No backend changes.

**Quality gate:** @8ql PASS — no security findings, all 8 AC met, 129 structure tests pass.

**Next available prj:** prj0000079

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

**Next available prj:** prj0000078

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

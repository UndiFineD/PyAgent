# 9git Memory

This file records git operations, branch status, 
and pull request coordination notes.

## Standing Rules

- One project, one branch. A `prjNNN` task must use its own project-specific branch.
- Do not treat another project's active branch as valid just because it already contains related repository changes.
- Validate branch/project match before any staging, commit, push, or PR action.
- Validate changed-file scope against the project overview scope boundary before any staging.
- After `git add` of the validated project files, run `pre-commit` before commit, push, or PR actions.
- Treat that `pre-commit` run as a local workstation gate; do not mirror it as a GitHub-side requirement unless explicitly requested.
- Do not bypass the post-staging `pre-commit` run with `--no-verify` or skipped hooks for normal project work.
- Do not use blanket staging for project work (`git add .`, `git add -A`, or equivalent).
- On validation failure, stop git work, update the project git artifact, record a short retrospective note here, and hand the task back to `@0master`.
- Before any `gh pr view/create/edit`, run `gh auth status` and record the result in git handoff evidence.
- If `gh` returns 401 and `GITHUB_TOKEN` is present, clear the session override (`Remove-Item Env:GITHUB_TOKEN`) and retry `gh auth status` before declaring BLOCKED.
- Prefer branch-scoped PR commands: `gh pr view --head <branch>` then `gh pr create --base main --head <branch>` when missing, otherwise `gh pr edit`.

## Retrospective Notes

- 2026-03-20 — Branch hygiene policy tightened after multiple project artifacts referenced unrelated `prj037-*` branches. Future agents must treat this pattern as a validation failure and trigger correction rather than continuing git work.
- 2026-03-20 — `@9git` now requires a post-staging `pre-commit` run before commit/push/PR actions so narrowed staging is validated before repository updates leave the workstation.
- 2026-03-20 — User requested blanket `add -A, commit, push, PR, pull` while working tree had 6,932 changes (120 outside `src-old/`) and missing `prj037` plan artifact; workflow was halted and handed back for scope/plan correction.
- 2026-03-26 — prj0000076: `run-precommit-checks` hook uses `pass_filenames: false`, making it a repo-wide Python check that always runs regardless of `--files` filter. This hook was already failing on the branch before @9git changes (confirmed by stash test). ruff+mypy both returned Skipped for JSON/MD tracking files. Pre-existing failure should be tracked as a separate remediation project assigned to @0master.
- 2026-03-27 — prj0000086: handoff staging scope was valid (`docs/project/prj0000086-universal-agent-shell/universal-agent-shell.git.md` only), but mandatory post-staging `pre-commit` failed on unrelated repository-wide violations, so commit/push/PR actions were blocked and returned to @0master.
- 2026-03-27 — prj0000088: scope validation passed (`docs/project/kanban.md` + `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.git.md`) and unrelated untracked CodeQL examples were excluded; handoff still blocked because `run-precommit-checks` failed on existing repo-wide Ruff docstring issues in `src/core/memory/AutoMemCore.py`, so no commit/push/PR was performed and task was returned to @0master.
- 2026-03-28 — prj0000091: branch and scope validation passed; staging was narrowed to approved project files while `docs/project/PROJECT_DASHBOARD.md` remained intentionally unstaged as out-of-scope. Mandatory post-staging `pre-commit` failed on existing repository-wide Ruff violations in `tests/` outside staged files, so commit/push/PR actions were blocked and disposition was recorded in project git artifact.
- 2026-03-28 — prj0000092: branch and scope validation passed on `prj0000092-mypy-strict-enforcement`; narrow staging included project artifacts, strict-lane config/CI/tests, src/core compatibility fix, registry/kanban/nextproject updates, and agent-memory files, while `pip_audit_results.json` and `docs/project/PROJECT_DASHBOARD.md` were explicitly excluded as out-of-scope.
- 2026-03-28 — prj0000092 follow-up: local commit and push succeeded, but `gh` PR creation was blocked by `HTTP 401: Bad credentials`; preserve pushed-branch PR URL in project git artifact and hand off for authenticated PR creation.
- 2026-03-29 — prj0000098: branch/scope validation passed, narrow staging + post-staging pre-commit passed, and push to origin succeeded; GitHub CLI PR view/create both blocked by `HTTP 401: Bad credentials`.
	Pattern: PR operations blocked by expired or missing GitHub CLI authentication after successful push.
	Root cause: `gh` token/session was invalid for GraphQL API calls (`gh pr view`, `gh pr create`).
	Prevention: Run `gh auth status` and refresh credentials (`gh auth login`) before invoking @9git PR steps.
	First seen: 2026-03-28.
	Seen in: `prj0000092-mypy-strict-enforcement`, `prj0000098-backend-health-check-endpoint`.
	Recurrence count: 2.
	Promotion status: Promoted to hard rule (require `gh` auth check before PR operations).
- 2026-03-28 — prj0000093: branch/scope validation passed and narrow staging correctly excluded `docs/project/PROJECT_DASHBOARD.md` and `pip_audit_results.json`, but mandatory post-staging `pre-commit` failed on repository-wide `ruff check src tests` baseline debt (141 violations outside staged scope); commit/push/PR was blocked and returned to @0master.
- 2026-03-28 — prj0000095: branch validation passed and straightforward Ruff auto-fixes were applied to changed files, but mandatory `run-precommit-checks` remained blocked by environment-level dependency drift during pytest collection.
	Pattern: Pre-commit blocked by Python dependency mismatch outside narrowed staging scope.
	Root cause: Interpreter environment used by hook resolved `pydantic` with incompatible `pydantic-core` (`2.43.0` vs required `2.41.5`).
	Prevention: Pin and repair Python dependency pair in the environment used by hooks before invoking `@9git` handoff.
	First seen: 2026-03-28.
	Seen in: `prj0000095-source-stub-remediation`.
	Recurrence count: 1.
	Promotion status: Candidate (not promoted; threshold is >=2).
- 2026-03-29 — prj0000099: branch/scope validation passed and narrow staging was prepared for project closure, but mandatory post-staging `pre-commit` failed in `run-precommit-checks` due repository-wide Ruff findings in `tests/` outside staged scope; commit/push/PR were blocked and handoff returned to `@0master`.
	Pattern: Project-scoped handoff blocked by repository-wide hook baseline debt.
	Root cause: `run-precommit-checks` executes `ruff check src tests` without staged-file scoping.
	Prevention: Reduce baseline Ruff debt or split hook policy so project-scoped docs handoffs are not blocked by unrelated violations.
	First seen: 2026-03-28.
	Seen in: `prj0000093-projectmanager-ideas-autosync`, `prj0000099-stub-module-elimination`.
	Recurrence count: 2.
	Promotion status: Promoted to hard rule (run/verify repo-wide hook health before starting @9git handoff for docs-only closures).
- 2026-03-29 — prj0000099 completion: branch validation, scoped staging, post-staging pre-commit, commit, push, and PR creation all completed successfully.
	Pattern: GitHub CLI authentication can fail when an invalid `GITHUB_TOKEN` environment override is present even with a valid keyring login.
	Root cause: `gh` preferred the invalid environment token and returned `HTTP 401` until the override was cleared.
	Prevention: Run `gh auth status`, clear invalid `GITHUB_TOKEN` for the session, then retry `gh pr view/create` on the active account.
	First seen: 2026-03-29.
	Seen in: `prj0000099-stub-module-elimination`.
	Recurrence count: 1.
	Promotion status: Candidate (not promoted; threshold is >=2).
- 2026-03-29 — PR command hardening: standardized @9git PR flow to `gh auth status` -> branch-scoped `gh pr view --head <branch>` -> `gh pr create --base main --head <branch>` or `gh pr edit`.
	Pattern: Ad-hoc PR command variants increase failure rate and duplicate/failed PR attempts under partial auth states.
	Root cause: Missing deterministic command order and missing preflight auth gate in prior runs.
	Prevention: Enforce the command playbook in @9git operating procedure and record auth evidence in git artifacts.
	First seen: 2026-03-29.
	Seen in: `prj0000092-mypy-strict-enforcement`, `prj0000098-backend-health-check-endpoint`, `prj0000099-stub-module-elimination`.
	Recurrence count: 3.
	Promotion status: Promoted to hard rule.

## Auto-handoff

Once git operations, PRs, and merges are complete, 
the next agent to run is **@0master**. 
Invoke it via `agent/runSubagent` to continue the cycle.


--- Appended from current ---

# Current Memory - 9git

## Metadata
- agent: @9git
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-03
- rollover: At new project start, append this file's entries to history.9git.memory.md in chronological order, then clear Entries.

## Entries

## 2026-04-04 - prj0000127-mypy-strict-enforcement warn-phase PR handoff
- task_id: prj0000127-mypy-strict-enforcement
- status: DONE
- branch_expected: prj0000127-mypy-strict-enforcement
- branch_observed: prj0000127-mypy-strict-enforcement
- branch_validation: PASS
- scope_validation: PASS (PR handoff only; no new staging/commit in this step)
- notes:
	- Existing PR check returned none for branch head.
	- PR created to `main` with requested title/body: https://github.com/UndiFineD/PyAgent/pull/291.
	- PR body includes @2think/@3design/@4plan completion, RED+GREEN warn-phase status, @7exec and @8ql pass evidence, and explicit non-promotion note for required phase.
	- Working tree remained dirty from pre-existing modifications (`.github/agents/data/parallel_agents_register.json`, project exec artifact).

## 2026-04-04 - prj0000124-llm-gateway post-merge closure
- task_id: prj0000124-llm-gateway-closure-pr
- status: DONE
- branch_expected: prj0000124-llm-gateway
- branch_observed: prj0000124-llm-gateway
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- GH auth validated with active keyring session.
	- Existing open PR check returned none before creation (`gh pr list --state open --head prj0000124-llm-gateway --json number,url,state,title` -> `[]`).
	- Closure delta against `origin/main` is narrow: only commit `7a80167983` (`chore(prj0000124): post-merge closure and dashboard sync`).
	- Closure PR opened to `main`: https://github.com/UndiFineD/PyAgent/pull/288.
	- Mandatory docs gates passed: dashboard refresh, docs policy (`17 passed`), docs-only preflight, and staged-file pre-commit at `2026-04-04T16:47:40.3176222+01:00`.
	- Narrow staged manifest limited to `llm-gateway.git.md`, `current.9git.memory.md`, and `2026-04-04.9git.log.md`.
	- Final docs-only evidence commit prepared with message `docs(agents): record prj0000124 closure PR handoff`.

## 2026-04-04 - prj0000122-jwt-refresh-token-support
- task_id: prj0000122-jwt-refresh-token-support
- status: DONE
- branch_expected: prj0000122-jwt-refresh-token-support
- branch_observed: prj0000122-jwt-refresh-token-support
- branch_validation: PASS
- scope_validation: PASS_WITH_EXCLUSION
- notes:
	- Mandatory dashboard gate executed before staging (`python scripts/generate_project_dashboard.py`).
	- Mandatory placeholder scans executed; baseline placeholder hits were outside staged scope.
	- Narrow allowlist staging applied to backend auth slice + prj0000122 artifacts + lane memory/log updates.
	- Out-of-scope `docs/project/PROJECT_DASHBOARD.md` remained unstaged.
	- Governance gates passed:
		- `python scripts/project_registry_governance.py validate` -> `VALIDATION_OK`.
		- `python scripts/architecture_governance.py validate` -> `VALIDATION_OK`.
		- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
	- Staged-file pre-commit passed at `2026-04-04T13:32:14.9728197+01:00`.
	- Primary commit created: `40d1714506` (`feat(prj0000122): add jwt refresh session support slice`).
	- @9git evidence commit created: `c58e1cb918` (`docs(prj0000122): record @9git handoff evidence`).
	- Branch pushed to `origin/prj0000122-jwt-refresh-token-support`.
	- PR created to main: https://github.com/UndiFineD/PyAgent/pull/284.

## 2026-04-03 - prj0000121-ci-setup-python-stack-overflow
- task_id: prj0000121-ci-setup-python-stack-overflow
- status: DONE
- branch_expected: prj0000121-ci-setup-python-stack-overflow
- branch_observed: prj0000121-ci-setup-python-stack-overflow
- branch_validation: PASS
- scope_validation: PASS_WITH_EXCLUSION
- notes:
	- Mandatory dashboard refresh gate executed successfully before staging (`python scripts/generate_project_dashboard.py`).
	- Scope allowlist applied; excluded generated out-of-scope `docs/project/PROJECT_DASHBOARD.md` from staging.
	- Mandatory staged-file pre-commit gate passed (`pre-commit run --files (git diff --cached --name-only)`).
	- Hotfix/lane commit created: `8546a063f8` (`ci(prj0000121): pin setup-python to v4 for lightweight checks`).
	- @9git evidence commit created: `b2476d0fd2` (`docs(prj0000121): record @9git handoff evidence`).
	- Docs policy gate passed before PR: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
	- Branch push completed to origin/prj0000121-ci-setup-python-stack-overflow.
	- PR created to main: https://github.com/UndiFineD/PyAgent/pull/281.
	- Timestamped pre-commit evidence rerun captured at `2026-04-03T22:30:33.5134334+01:00` with all hooks passing.

## 2026-04-03 - prj0000117-rust-sub-crate-unification
- task_id: prj0000117-rust-sub-crate-unification
- status: IN_PROGRESS
- branch_expected: prj0000117-rust-sub-crate-unification
- branch_observed: prj0000117-rust-sub-crate-unification
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Branch gate passed; `git pull` -> `Already up to date`.
	- Commit timeline collected from `origin/main..HEAD` with 9 project commits (project init -> think -> design -> plan -> test -> feat -> exec -> ql -> ql pass).
	- Existing PR check for branch returned none (`gh pr view --head prj0000117-rust-sub-crate-unification` -> not found).
	- Quality evidence assembled from @7exec and @8ql artifacts:
		- Workspace/CI selectors passing (`7 passed`, `8 passed`, then consolidated `15 passed`).
		- Docs policy baseline remains known non-project failure (`1 failed, 16 passed`) for missing historical legacy file `prj0000005`.
		- Rust metadata/workspace integrity checks passed.
	- Prepared @9git scope-manifest for final docs-only handoff files and recorded pending pre-commit evidence in project git artifact.
	- Next actions: dashboard refresh gate -> scoped staging -> pre-commit -> final commit/push -> PR create.

### Lesson
- Pattern: Recording the exact `origin/main..HEAD` timeline before final handoff prevents ambiguity when multiple quality-stage commits exist in close succession.
- Root cause: Parallel stage cadence can produce similar commit subjects (`quality/security gate evidence`) that are hard to disambiguate without timeline capture.
- Prevention: Always add ordered commit table (hash + subject) to project git summary before final @9git commit.
- First seen: 2026-04-03
- Seen in: prj0000117-rust-sub-crate-unification
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-04-03 - prj0000116-rust-criterion-benchmarks
- task_id: prj0000116-rust-criterion-benchmarks
- status: IN_PROGRESS
- branch_expected: prj0000116-rust-criterion-benchmarks
- branch_observed: prj0000116-rust-criterion-benchmarks
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Branch gate passed; `git pull` → `Already up to date`.
	- Full commit timeline assembled: 10 upstream commits (think → design → plan → test → feat → exec → ql × 3 → fix).
	- @8ql cleared to @9git: all quality gates PASS; docs policy baseline fail is pre-existing non-blocking.
	- 11/11 project tests pass; cargo clippy 0 warnings; ruff clean on test files.
	- `rust_core/Cargo.lock` was modified (unstaged companion to committed Cargo.toml bench dep); staged in @9git final commit.
	- Dashboard gate executed; broad side-effect files excluded from staging.
	- Staged manifest: git.md, project.md (dashboard), current.9git.memory.md, 2026-04-03.9git.log.md, rust_core/Cargo.lock.
	- Commit `217f136e38` (`docs(prj0000116): finalize git handoff and PR readiness`) pushed.
	- PR: https://github.com/UndiFineD/PyAgent/pull/273.
- status: DONE

### Lesson
- Pattern: `rust_core/Cargo.lock` updated silently when `cargo bench` or `cargo clippy --bench` runs; must check `git diff --name-only` before finalizing scope manifest and always include Cargo.lock alongside Cargo.toml changes.
- Root cause: Cargo deterministically regenerates Cargo.lock on any bench/clippy invocation that resolves new deps.
- Prevention: Always check for Cargo.lock diff after any Rust task; stage it in the same commit as Cargo.toml.
- First seen: 2026-04-03
- Seen in: prj0000116-rust-criterion-benchmarks
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-04-02 - prj0000115-ci-security-quality-workflow-consolidation
- task_id: prj0000115-ci-security-quality-workflow-consolidation
- status: DONE
- branch_expected: prj0000115-ci-security-quality-workflow-consolidation
- branch_observed: prj0000115-ci-security-quality-workflow-consolidation
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Branch gate passed (`git branch --show-current`), and `git pull` returned `Already up to date`.
	- Handoff timeline assembled from plan -> test -> code -> exec -> ql commits.
	- Test evidence confirmed from upstream artifacts: `14/14` CI tests pass; docs policy has one known non-blocking baseline exception.
	- Mandatory dashboard gate executed before staging; out-of-scope generated docs changes remained unstaged.
	- Staged-file pre-commit gate passed for allowlist files.
	- Final @9git commit pushed: `efc2790124`.
	- PR created: https://github.com/UndiFineD/PyAgent/pull/272.

### Lesson
- Pattern: Project handoff quality improves when timeline evidence is captured from the exact stage-labeled commit chain before final @9git commit.
- Root cause: Without explicit stage-to-commit mapping, PR reviewers must reconstruct provenance manually.
- Prevention: Always include a concise plan -> test -> code -> exec -> ql timeline in the git artifact before final staging.
- First seen: 2026-04-02
- Seen in: prj0000115-ci-security-quality-workflow-consolidation
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-03-30 - prj0000104-idea000014-processing
- task_id: prj0000104-idea000014-processing
- status: DONE
- branch_expected: prj0000104-idea000014-processing
- branch_observed: prj0000104-idea000014-processing
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Mandatory placeholder scan found baseline placeholders in `src/` unrelated to this project scope.
	- Mandatory dashboard refresh gate executed; generated broad out-of-scope docs changes, excluded from staging.
	- Commit created: 08aa9e35899b7d57a847ea562e95bfbf7f8a9d45.
	- Branch pushed to origin and PR opened: https://github.com/UndiFineD/PyAgent/pull/256.

### Lesson
- Pattern: Project dashboard refresh can stage broad unrelated project docs and must be isolated from narrow handoff scope.
- Root cause: `scripts/generate_project_dashboard.py` updates multiple historical project artifacts as side-effects.
- Prevention: Run dashboard gate early, then explicitly unstage non-project files before pre-commit and commit.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-03-30 - prj0000105-idea000016-mixin-architecture-base
- task_id: prj0000105-idea000016-mixin-architecture-base
- status: DONE
- branch_expected: prj0000105-idea000016-mixin-architecture-base
- branch_observed: prj0000105-idea000016-mixin-architecture-base
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Mandatory dashboard refresh gate executed before staging (`python scripts/generate_project_dashboard.py`).
	- Narrow scope staging applied; out-of-scope dashboard side effects and unrelated idea artifact remained unstaged.
	- Placeholder gate scans for staged Python scope returned zero hits.
	- Mandatory pre-commit gate passed on exact staged manifest.
	- Primary project commit created: `5d8c531a7`.
	- Handoff evidence commit created: `d1de21933`.
	- Branch pushed: `prj0000105-idea000016-mixin-architecture-base` -> `origin/prj0000105-idea000016-mixin-architecture-base`.
	- PR confirmed: https://github.com/UndiFineD/PyAgent/pull/258.

### Lesson
- Pattern: Dashboard generation side effects must be treated as out-of-scope unless explicitly included by project boundary.
- Root cause: The dashboard script updates multiple historical project artifacts beyond the active project.
- Prevention: Run dashboard generation first, validate scope, and stage by explicit allowlist only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 2
- Promotion status: HARD

## 2026-03-30 - prj0000106-idea000080-smart-prompt-routing-system
- task_id: prj0000106-idea000080-smart-prompt-routing-system
- status: DONE
- branch_expected: prj0000106-idea000080-smart-prompt-routing-system
- branch_observed: prj0000106-idea000080-smart-prompt-routing-system
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Governance lane reconciliation executed with canonical tooling; prj0000106 moved to Review for PR handoff.
	- Baseline lane mismatch for prj0000104 was also reconciled to restore registry/kanban validation consistency.
	- Mandatory dashboard refresh gate executed and broad out-of-scope changes remained unstaged.
	- Placeholder gate for staged Python scope passed after targeted verification.
	- Mandatory pre-commit gate passed on exact staged manifest (40 files).
	- Commit created: 58cfd2e5c27bc551cf7f1a8266beedc9a98e71d7.
	- Branch pushed and tracking set on origin/prj0000106-idea000080-smart-prompt-routing-system.
	- PR created: https://github.com/UndiFineD/PyAgent/pull/259.

### Lesson
- Pattern: Mandatory dashboard generation frequently introduces unrelated documentation diffs during project-scoped git handoff.
- Root cause: scripts/generate_project_dashboard.py rewrites summary files for many projects outside current scope.
- Prevention: Run dashboard gate before staging and enforce explicit allowlist staging for project boundary files only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system
- Recurrence count: 3
- Promotion status: HARD

## 2026-03-31 - prj0000107-idea000015-specialized-agent-library
- task_id: prj0000107-idea000015-specialized-agent-library
- status: DONE
- branch_expected: prj0000107-idea000015-specialized-agent-library
- branch_observed: prj0000107-idea000015-specialized-agent-library
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Continued closure from @8ql commit `e54adfcc74435c3dbf9a73f14213a5a542124ba4`.
	- Verified requested scope inclusion from existing commit: `docs/project/kanban.json` plus agent/governance instruction updates.
	- Verified migration from `kanban.md` to `kanban.json` references in updated instruction files (`rg` no `kanban.md` matches; expected `kanban.json` matches present).
	- Mandatory dashboard gate executed; broad out-of-scope project doc side effects remained unstaged.
	- Docs policy gate passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
	- PR created for branch: https://github.com/UndiFineD/PyAgent/pull/260.

### Lesson
- Pattern: Mandatory dashboard generation introduces unrelated project-doc churn during scoped @9git closure work.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project overview files in a single run.
- Prevention: Run dashboard gate before staging, then enforce explicit file allowlist staging for active project artifacts only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system; prj0000107-idea000015-specialized-agent-library
- Recurrence count: 4
- Promotion status: HARD

## 2026-03-31 - prj0000108-idea000019-crdt-python-ffi-bindings
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- status: DONE
- branch_expected: prj0000108-idea000019-crdt-python-ffi-bindings
- branch_observed: prj0000108-idea000019-crdt-python-ffi-bindings
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Received @8ql clear from `idea000019-crdt-python-ffi-bindings.ql.md` (`Status: DONE`, `CLEAR -> @9git`).
	- Mandatory dashboard refresh gate executed successfully: `python scripts/generate_project_dashboard.py` (`DASHBOARD_EXIT=0`).
	- Docs policy gate passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
	- GH auth 401 override resolved via playbook by removing invalid `GITHUB_TOKEN` env override; `gh auth status` now active/pass.
	- Dashboard-generated out-of-scope docs changes detected and held unstaged for strict narrow-scope closure staging.
	- @9git closure evidence commit created and pushed: `121792c1bdfe4a5b96935d3a36b0b4498f8d7f4d`.
	- PR opened to `main`: https://github.com/UndiFineD/PyAgent/pull/261 (state: OPEN).

### Lesson
- Pattern: Invalid session-level `GITHUB_TOKEN` can silently flip gh auth active account state and block PR automation.
- Root cause: Shell environment override token was stale/invalid while keyring login remained valid.
- Prevention: Always run `gh auth status`; if 401 and env token exists, remove `GITHUB_TOKEN` and re-check before PR actions.
- First seen: 2026-03-31
- Seen in: prj0000108-idea000019-crdt-python-ffi-bindings
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-03-31 - prj0000109-idea000002-missing-compose-dockerfile
	- Confirmed branch gate pass on expected project branch.
	- Mandatory dashboard refresh gate executed before staging; broad out-of-scope changes detected and excluded.
	- Explicitly excluded unrelated generated local file `.github/agents/data/pip_audit_current_8ql.json` from staging/commit.
	- Existing branch commits pushed to origin.
	- PR created targeting `main`: https://github.com/UndiFineD/PyAgent/pull/262.
	- Staged-file pre-commit gate passed for handoff artifacts (PRECOMMIT_RC=0).
	- @9git closure commit created and pushed: `7251daa69629e3100985f70301dfbfad008b6cbb`.
	- Post-push `gh` query hit `HTTP 401` due invalid `GITHUB_TOKEN`; resolved by clearing env override and re-running `gh auth status`.

## 2026-04-04 - prj0000124-llm-gateway
- task_id: prj0000124-llm-gateway
- status: DONE
- branch_expected: prj0000124-llm-gateway
- branch_observed: prj0000124-llm-gateway
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Branch gate verified (`git branch --show-current` -> `prj0000124-llm-gateway`).
	- Scope gate verified from `git diff --name-only origin/main...HEAD`; gateway slice files + project docs/registry artifacts are in-bounds for prj0000124.
	- Existing PR check performed with compatible command: `gh pr list --state open --head prj0000124-llm-gateway`; no open PR found before creation.
	- Mandatory dashboard/docs gates passed before staging:
	  - `python scripts/generate_project_dashboard.py`
	  - `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`
	  - `pre-commit run run-precommit-checks 2>&1` -> PASS
	- Narrow staging applied to required handoff files only; out-of-scope dashboard side effects intentionally left unstaged.
	- Staged-file pre-commit passed at `2026-04-04T16:18:52.3751756+01:00`.
	- PR created: https://github.com/UndiFineD/PyAgent/pull/287.
	- Pending at record-write time: final docs-only handoff commit/push with message `chore(prj0000124): complete git handoff and open gateway core slice PR`.

### Lesson
- Pattern: GH CLI subcommand flags differ across versions (`gh pr view --head` unavailable in this environment).
- Root cause: Local gh version does not support `--head` on `gh pr view`.
- Prevention: Use `gh pr list --state open --head <branch>` for branch-based PR discovery to avoid duplicate PRs.
- First seen: 2026-04-04
- Seen in: prj0000124-llm-gateway
- Recurrence count: 1
- Promotion status: CANDIDATE
### Lesson
- Pattern: Dashboard refresh consistently introduces broad out-of-scope churn during narrow project closure handoffs.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project artifacts globally by design.
- Prevention: Run dashboard gate before staging, then enforce explicit allowlist staging and verify excluded unrelated generated files stay untouched.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system; prj0000107-idea000015-specialized-agent-library; prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 5
- Promotion status: HARD

## 2026-04-01 - prj0000110-idea000004-quality-workflow-branch-trigger
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- status: DONE
- branch_expected: prj0000110-idea000004-quality-workflow-branch-trigger
- branch_observed: prj0000110-idea000004-quality-workflow-branch-trigger
- branch_validation: PASS
- scope_validation: PASS_WITH_EXCLUSION
- notes:
	- Active working tree contains unrelated pre-existing modification in `scripts/project_registry_governance.py`; excluded from @9git scope and must remain unstaged.
	- Mandatory dashboard refresh gate executed before staging; generated broad out-of-scope docs updates and they were left unstaged.
	- Staged-file pre-commit gate passed on exact allowlist (PRECOMMIT_RC=0).
	- Docs policy validation passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
	- @9git commit pushed: `8ea6cfff85e448b23c253fc194ec71009cb51579`.
	- PR created targeting `main`: https://github.com/UndiFineD/PyAgent/pull/263.
	- gh auth override issue recurred and was resolved by removing invalid `GITHUB_TOKEN` env override before PR command.

### Lesson
- Pattern: Session-level `GITHUB_TOKEN` overrides can break gh auth and must be cleared to restore keyring-based authentication.
- Root cause: Invalid environment token shadowed valid keyring credentials during PR automation.
- Prevention: Always run `gh auth status`; if invalid token appears and env override exists, remove `GITHUB_TOKEN` and re-run auth check before PR operations.
- First seen: 2026-03-31
- Seen in: prj0000108-idea000019-crdt-python-ffi-bindings; prj0000110-idea000004-quality-workflow-branch-trigger
- Recurrence count: 2
- Promotion status: HARD


---
agent: "0master"
description: "Fallback rules and operational constraints for the 0master agent."
---

# Base Rules: 0master

These rules act as a resilient fallback for the `@0master` agent. 
They may be dynamically updated by `@agentwriter`, 
or superseded by PostgreSQL database records during workflow orchestration.

## Core Constraints
1. **Preserve State**: Always log intermediate work to `.github/agents/data/`.
2. **Acknowledge Overrides**: 
    If the PostgreSQL schema provides a newer rule for a given context, 
    obey the database rule over this file.
3. **Continuous Learning**: 
    If a task fails, analyze the failure signature and propose updates 
    to this file via `@agentwriter` or using your own file editing tools.
4. **Scope Strictness**: 
    Do not perform tasks outside the explicit capabilities of `@0master`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

**Lesson:** Always verify PR merge timing before pushing dependent commits. If CI starts and a merge is imminent, confirm inclusion before pushing a follow-up commit.
**Lessons:** Full agent workflow (all 9 artifacts) must be completed on the project branch before git handoff, even for single-file changes. Branch gate (`git branch --show-current` → switch to project branch) must be the first action. Skipping artifacts from the prior session required retroactive creation on the correct branch.
**Lessons:** PyJWT not pre-installed (run `pip install PyJWT>=2.8.0`); project.md needs full modern template with `**Goal:**`, `**Scope boundary:**`, `**Handoff rule:**`, `**Failure rule:**` sub-fields in Branch Plan section.
**Root cause:** Three backend runtime deps missing from `requirements.txt` caused `ModuleNotFoundError` at pytest collection time (shards 5,7,8,9,10 exit code 2). CodeQL QL query had dual `select` + nonexistent `getKey()` method. Race condition: kanban test count fix was pushed after PR #216 merged → required hotfix PR #217.
- Fix: narrow canonicalization in `tests/docs/test_backend_openapi_drift.py` stripping volatile `ValidationError`/`HTTPValidationError` schema internals.
- Fixed lane drift via governance tooling and validated registry/kanban consistency.
- Fixed pytest warnings: removed duplicate pytest config from pyproject.toml, closed unclosed file handles in 3 test files, replaced short JWT test keys (10–11 bytes) with 32+ byte keys, added filterwarnings for internal ResourceWarnings. Result: 835 passed, 9 skipped, **0 warnings**.
- Lessons written to `6code.memory.md` + `8ql.memory.md`
- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- pre-commit lint fixes: I001, ruff config migration to `[tool.ruff.lint]`, D203/D213 conflict

### Learned Rules & Historical Patterns

**Lesson:** Always verify PR merge timing before pushing dependent commits. If CI starts and a merge is imminent, confirm inclusion before pushing a follow-up commit.
**Lessons:** Full agent workflow (all 9 artifacts) must be completed on the project branch before git handoff, even for single-file changes. Branch gate (`git branch --show-current` → switch to project branch) must be the first action. Skipping artifacts from the prior session required retroactive creation on the correct branch.
**Lessons:** PyJWT not pre-installed (run `pip install PyJWT>=2.8.0`); project.md needs full modern template with `**Goal:**`, `**Scope boundary:**`, `**Handoff rule:**`, `**Failure rule:**` sub-fields in Branch Plan section.
**Root cause:** Three backend runtime deps missing from `requirements.txt` caused `ModuleNotFoundError` at pytest collection time (shards 5,7,8,9,10 exit code 2). CodeQL QL query had dual `select` + nonexistent `getKey()` method. Race condition: kanban test count fix was pushed after PR #216 merged → required hotfix PR #217.
- Fix: narrow canonicalization in `tests/docs/test_backend_openapi_drift.py` stripping volatile `ValidationError`/`HTTPValidationError` schema internals.
- Fixed lane drift via governance tooling and validated registry/kanban consistency.
- Fixed pytest warnings: removed duplicate pytest config from pyproject.toml, closed unclosed file handles in 3 test files, replaced short JWT test keys (10–11 bytes) with 32+ byte keys, added filterwarnings for internal ResourceWarnings. Result: 835 passed, 9 skipped, **0 warnings**.
- Lessons written to `6code.memory.md` + `8ql.memory.md`
- Lessons-learned fixes are now enforced as repository-wide automation and policy tests for all projects.
- Root cause: gate executed only governance tests while measuring `--cov=tests`, which produced synthetic low total coverage.
- pre-commit lint fixes: I001, ruff config migration to `[tool.ruff.lint]`, D203/D213 conflict

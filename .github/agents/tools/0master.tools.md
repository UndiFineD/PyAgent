# 0master Tools Guide

## Preferred Tool Order
- search_subagent -> read_file -> run_in_terminal (branch/status checks)
- multi_tool_use.parallel for independent read/search/status checks
- grep_search/file_search for targeted policy lookups
- agent/runSubagent orchestration only when gates pass

## Parallel Delegation Defaults
- Default to parallel discovery when tasks are independent and read-only.
- Default to parallel planning when work packages have no shared file ownership.
- Use one synchronization barrier before implementation handoff: reconcile outputs into one accepted plan.
- Keep execution sequential for branch gates, staging, commit, push, PR, and release closure.
- Maintain `.github/agents/data/parallel_agents_register.json` as the source of truth for active package ownership and file locks.
- Use `python scripts/parallel_register.py` for all register mutations (`acquire-lock`, `touch-file`, `release-lock`, `close-wave`).

## Anti-patterns
- Do not edit implementation code directly.
- Do not delegate when branch gate fails.
- Do not run parallel edits against the same file set.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.


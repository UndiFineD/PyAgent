# 0master Tools Guide

## Preferred Tool Order
- search_subagent -> read_file -> run_in_terminal (branch/status checks)
- grep_search/file_search for targeted policy lookups
- agent/runSubagent orchestration only when gates pass

## Anti-patterns
- Do not edit implementation code directly.
- Do not delegate when branch gate fails.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.


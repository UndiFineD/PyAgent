# Tools Framework Implementation Plan

**Goal:** Ensure the `src/tools/` framework is fully implemented, tested, 
    and documented as a reusable set of CLI/agent utilities.

## Checklist (implementation status)

- [x] Create a central tool registry for `src/tools/` and add CLI dispatch support.
- [x] Implement usable versions of key tools (`git_utils`, `netcalc`, `nettest`, `ssl_utils`) rather than placeholders.
- [x] Ensure each tool supports `--help` and behaves as a real CLI utility.
- [x] Update `docs/tools.md` with usage examples and verify it covers all registered tools.
- [x] Add unit tests for tool registry and for each tool's core functionality.
- [x] Ensure `tests/tools/test_tools_sanity.py` remains green and exercises each tool’s main entrypoint.
- [x] Ensure all tools are async-friendly where required (no blocking loops).
- [x] Provide a `9git` alias tool for the `@9git` agent workflow (implements Git helper operations via `git_utils`).

## Notes

The tools framework is intended as a lightweight runtime utility layer 
for agents and CLI scripts. It should be safe to use in automated workflows 
(CI, development scripts) and should not introduce synchronous blocking loops 
that violate the async runtime constraints.

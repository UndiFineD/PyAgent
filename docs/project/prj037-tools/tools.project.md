# tools

**Project ID:** `prj037-tools`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Create a central tool registry for `src/tools/` and add CLI dispatch support.
- [x] Implement usable versions of key tools (`git_utils`, `netcalc`, `nettest`, `ssl_utils`) rather than placeholders.
- [x] Ensure each tool supports `--help` and behaves as a real CLI utility.
- [x] Update `docs/tools.md` with usage examples and verify it covers all registered tools.
- [x] Add unit tests for tool registry and for each tool's core functionality.
- [x] Ensure `tests/tools/test_tools_sanity.py` remains green and exercises each tool’s main entrypoint.
- [x] Ensure all tools are async-friendly where required (no blocking loops).
- [x] Provide a `9git` alias tool for the `@9git` agent workflow (implements Git helper operations via `git_utils`).

## Status

8 of 8 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\inference\tools.rs`
  - `src\chat\mcp_tools.py`
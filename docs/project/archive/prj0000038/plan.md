# Python Function Coverage Test

**Goal:** Add a lightweight, automatic test that exercises as many Python functions as possible to improve coverage metrics and catch obvious runtime failures.

## Checklist (implementation status)

- [x] Add a new test file that detects and calls functions across `src/` (excluding tests).
- [x] Ensure the test does not fail on harmless uncallable functions or missing imports.
- [x] Ensure the test runs quickly enough for CI (limit number of functions tested).
- [x] Add documentation to `docs/tools.md` or `docs/project` explaining the purpose and how to adapt it.

## Notes

The test is intentionally opportunistic; its goal is to surface runtime errors with minimal assumptions. It does not validate correctness beyond the ability to execute a function with basic arguments.

# Conftest Typing Fixes Design (2026-03-08)
> **2026-03-08:** Resolve typing issues in `conftest.py` while preserving current behavior.

## Goal
Resolve the reported `conftest.py` typing issues while preserving runtime behavior.

## Scope
Fixes requested by user:
- Monkey-patch target signatures (`_patched_spec`, `_patched_module`)
- Missing annotations (`__enter__`, nested `logged_open`, `__exit__`, `_debug_log`)
- Callsite alignment at `_debug_log(...)`
- `session.exitstatus = 1` typing-safe assignment

## Approach
Use **annotations + small Protocols**:
1. Add internal Protocols for minimal pytest/session attributes used in this file.
2. Keep monkey-patch input params flexible, but use strict return types:
   - `_patched_spec(...) -> ModuleSpec | None`
   - `_patched_module(...) -> ModuleType`
3. Apply balanced typing to nested wrappers (`logged_write`, `logged_open`) and context methods.
4. Preserve session finish behavior and use a safe typed cast before writing `exitstatus`.

## Behavioral Constraints
- No intended functional behavior change.
- Keep current import-fixer resolution and session-finish semantics.

## Validation Plan
- Run focused tests for new `conftest` behavior.
- Run related regression tests to ensure no hook regressions.

## Risks and Mitigations
- Risk: Over-constraining monkey-patch signatures.
  - Mitigation: Flexible args on patched callables.
- Risk: Type-only edits accidentally alter behavior.
  - Mitigation: no control-flow changes; test verification after patch.

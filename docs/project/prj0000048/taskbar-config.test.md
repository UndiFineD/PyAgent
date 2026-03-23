# taskbar-config — Test Artifacts

_Status: TESTS_WRITTEN — awaiting @6code implementation_
_Tester: @5test | Updated: 2026-03-23_

---

## Test Strategy

### Test framework

**Vitest 4.x** with **jsdom** environment + **@testing-library/react v16** + **@testing-library/user-event v14**.

Both are configured in `web/package.json` (`vitest`, `@testing-library/react`, `@testing-library/user-event`, `jsdom`) and the test environment is set in `web/vite.config.ts` (`test.environment: 'jsdom'`, `test.globals: true`).

No new dependencies are required.

### Test file

**`web/App.taskbar-config.test.tsx`** — 16 tests across 5 suites.

Run with:
```
cd web && npx vitest run App.taskbar-config.test.tsx
```

### Login bypass

The real `Login` component calls `onLogin()` after a 1 500 ms fake-OAuth `setTimeout`. Advancing that delay via `vi.useFakeTimers()` deadlocks with `userEvent`'s async Promise chains. To avoid this, the test file uses `vi.mock('./components/Login')` to replace Login with an instant-fire stub button. This is hoisted before any imports and does not affect any other test files.

### Fake-timer policy

- **Suites 1, 2, 3, 5** — real timers (no `vi.useFakeTimers()`). The mock login fires synchronously.
- **Suite 4 (hideTaskbar guard)** — `vi.useFakeTimers()` is required to control the 2 000 ms hide timeout without real waiting. Mouse events in this suite use synchronous `fireEvent` (not async `userEvent`) to avoid `act()`/fake-timer deadlocks.

---

## Test Cases

| ID   | Suite                              | Description                                              | Plan task | Pre-impl status |
|------|------------------------------------|----------------------------------------------------------|-----------|-----------------|
| T-01 | types: OsConfig                    | DEFAULT_OS_CONFIG is exported from ./types               | Task 1    | FAIL ✓          |
| T-02 | types: OsConfig                    | DEFAULT_OS_CONFIG.taskbarAlwaysVisible defaults to false  | Task 1    | FAIL ✓          |
| T-03 | types: OsConfig                    | DEFAULT_OS_CONFIG has full OsConfig shape                | Task 1    | FAIL ✓          |
| T-04 | Settings button (Task 8)           | Dropdown contains a "Settings" button                    | Task 8    | FAIL ✓          |
| T-05 | Settings modal (Task 9)            | Clicking Settings shows "Always show taskbar" label      | Task 9    | FAIL ✓          |
| T-06 | Settings modal (Task 9)            | role=switch toggle defaults to aria-checked=false        | Task 9    | FAIL ✓          |
| T-07 | Settings modal (Task 9)            | Toggle flips aria-checked to true                        | Task 9    | FAIL ✓          |
| T-08 | Settings modal (Task 9)            | Toggle persists to localStorage "nebula-os-config"       | Task 6    | FAIL ✓          |
| T-09 | Settings modal (Task 9)            | Stored taskbarAlwaysVisible=true loads into toggle       | Task 4+5  | FAIL ✓          |
| T-10 | Settings modal (Task 9)            | Backdrop click closes modal                              | Task 9    | FAIL ✓          |
| T-11 | Settings modal (Task 9)            | X button closes modal                                    | Task 9    | FAIL ✓          |
| T-12 | Settings modal (Task 9)            | Escape key closes modal                                  | Task 10   | FAIL ✓          |
| T-13 | hideTaskbar guard (Task 7)         | Taskbar stays visible when taskbarAlwaysVisible=true     | Task 7    | FAIL ✓          |
| T-14 | hideTaskbar guard (Task 7)         | Taskbar auto-hides when taskbarAlwaysVisible=false       | Task 7    | PASS (existing) |
| T-15 | osConfig persistence (Task 6)      | nebula-os-config key written to localStorage on mount    | Task 6    | FAIL ✓          |
| T-16 | osConfig persistence (Task 6)      | Stored value is valid JSON with taskbarAlwaysVisible     | Task 6    | FAIL ✓          |

**T-14 passes even before implementation** — it tests that the existing auto-hide behaviour is *preserved* after Task 7's guard is inserted. This is intentional: the test is a regression guard.

---

## Validation Results

| ID   | Result            | Note                                                                        |
|------|-------------------|-----------------------------------------------------------------------------|
| T-01 | FAIL (pre-impl)   | `expected undefined to be defined` — DEFAULT_OS_CONFIG not yet exported     |
| T-02 | FAIL (pre-impl)   | `Cannot read properties of undefined (reading 'taskbarAlwaysVisible')`      |
| T-03 | FAIL (pre-impl)   | Same as T-02                                                                |
| T-04 | FAIL (pre-impl)   | Dropdown renders but has no "Settings" button (Task 8 not implemented)      |
| T-05 | FAIL (pre-impl)   | "Hamburger menu trigger button" throws before Settings modal test begins    |
| T-06 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-07 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-08 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-09 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-10 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-11 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-12 | FAIL (pre-impl)   | Same as T-05                                                                |
| T-13 | FAIL (pre-impl)   | Taskbar hides (guard not in hideTaskbar yet)                                |
| T-14 | PASS              | Existing hide behaviour works correctly                                     |
| T-15 | FAIL (pre-impl)   | nebula-os-config absent (saveOsConfig effect not yet added)                 |
| T-16 | FAIL (pre-impl)   | Same as T-15                                                                |

Run completed in ~6 s (16 tests: 15 failed, 1 passed). No timeouts.

---

## Unresolved Failures
_None — all failures are expected pre-implementation failures. @6code should make all 16 tests pass._

---

## Notes for @6code

1. **DOM selectors used in tests** — do not change the following structural patterns:
   - Taskbar: `div.fixed.h-12` (the 48px bar, not the 8px trigger zone)
   - Dropdown trigger: `.relative > button` inside the taskbar
   - Settings modal: `role="switch"` on the toggle, `aria-checked` attribute
   - Modal panel discovery: `.rounded-xl.shadow-2xl` for close-button lookup
   - Modal backdrop: class containing `z-[60]`
2. **localStorage key** — must be exactly `nebula-os-config`.
3. **role=switch** — the toggle button MUST have `role="switch"` and `aria-checked={osConfig.taskbarAlwaysVisible}` as specified in the plan (Task 9).

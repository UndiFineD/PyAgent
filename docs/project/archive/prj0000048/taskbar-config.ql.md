# QL/Security Review: prj0000048 — Taskbar Config

## Status
Issues Found → Fixed → **Clean**

_Scanner: @8ql | Updated: 2026-03-23_

## Files Reviewed

| File | Notes |
|---|---|
| `web/types.ts` | `OsConfig` interface + `DEFAULT_OS_CONFIG` constant |
| `web/App.tsx` | `loadOsConfig`, `saveOsConfig`, taskbar guard, settings modal JSX |
| `web/App.taskbar-config.test.tsx` | Vitest suite — 16 feature tests |
| `docs/project/prj0000048/taskbar-config.git.md` | Git summary doc |

## Security Findings

### XSS (A03)
**PASS.** No `dangerouslySetInnerHTML`. No user input rendered as HTML. The only localStorage value consumed is `taskbarAlwaysVisible` (boolean), used in a conditional CSS class and `aria-checked` attribute — neither is an HTML injection vector.

### Injection via localStorage (A03)
**PASS.** `loadOsConfig` reads `nebula-os-config` from localStorage, parses it with `JSON.parse`, and reads only a strongly-typed property. No `eval`, no `innerHTML`, no dynamic property access with untrusted keys.

### Data Integrity — JSON parse guard (A08)
**Issue found and fixed.**

**Original code** (before fix):
```typescript
return raw ? { ...DEFAULT_OS_CONFIG, ...JSON.parse(raw) } : DEFAULT_OS_CONFIG;
```

The `...JSON.parse(raw)` spread accepted any object from `localStorage` without type-
validating its fields. An attacker or corrupted entry could set `taskbarAlwaysVisible`
to a non-boolean (e.g. `"evil"`) which would:
- Cause the ARIA attribute `aria-checked` to receive an unexpected string value.
- Technically keep runtime functionality (truthy/falsy) but violate TypeScript's type
  contract at runtime.

**Fix applied to `web/App.tsx`:**
- `loadOsConfig` now validates the parsed value is a plain object.
- Only `taskbarAlwaysVisible` is extracted, guarded with a `typeof === 'boolean'` check;
  falls back to `DEFAULT_OS_CONFIG.taskbarAlwaysVisible` if invalid.
- Extra properties injected from localStorage are never read.

### Access Control (A01)
**PASS.** Settings dialog only controls UI-local state (taskbar visibility preference).
No API calls, no privileged operations, no authentication bypass.

### SSRF / External requests (A10)
**PASS.** No new `fetch()` or HTTP calls introduced by this PR. The pre-existing
`bg-[url('https://grainy-gradients.vercel.app/noise.svg')]` CSS reference is unchanged
and is not part of this PR's scope.

## Code Quality Findings

### `saveOsConfig` — missing try/catch
**Issue found and fixed.**  
`localStorage.setItem()` can throw `QuotaExceededError` (storage full) or `SecurityError`
(private browsing in some browsers). The original call was uncaught.

**Fix applied:** wrapped in `try/catch` with a silent catch — persistence is best-effort
and failure should not crash the UI.

### No `console.log`
**PASS.** None found in any changed file.

### No hardcoded secrets or credentials
**PASS.** No API keys, tokens, or passwords.

### TypeScript strict — no `any` in new code
**PASS.**  All new interfaces (`OsConfig`), function signatures (`loadOsConfig(): OsConfig`,
`saveOsConfig(cfg: OsConfig): void`), and event handlers (`(e: KeyboardEvent)`) carry
explicit types. `unknown` + `Record<string, unknown>` used correctly in the parse guard.

### No `@ts-ignore` / `@ts-expect-error`
**PASS.** None found.

### `localStorage` access wrapped in try/catch
**PASS (after fix).** Both `loadOsConfig` (read + parse) and `saveOsConfig` (write) are
now wrapped.

### Settings modal UX trap check
**PASS.**
- Backdrop `onClick={() => setSettingsOpen(false)}` ✅
- Inner panel `onClick={(e) => e.stopPropagation()}` — purposeful, prevents backdrop
  handler from firing when clicking inside the dialog. Not hiding errors. ✅
- Escape key: `useEffect` registers a `keydown` listener scoped to when `settingsOpen`
  is true; cleans up on unmount. ✅
- X button: `onClick={() => setSettingsOpen(false)}` with `aria-label="Close settings"`. ✅

### ARIA — `role="switch"` with `aria-checked`
**PASS.** The toggle button uses `role="switch"` and `aria-checked={osConfig.taskbarAlwaysVisible}`.
React serialises booleans to `"true"` / `"false"` for HTML attributes — correct per ARIA spec.
After the data-integrity fix `taskbarAlwaysVisible` is guaranteed to be `boolean`, so
`aria-checked` will always receive a valid value.

## Summary

Two issues found and patched in `web/App.tsx`:

| # | Severity | Description | Fix |
|---|---|---|---|
| 1 | Medium | `loadOsConfig` spread accepted unvalidated types from localStorage; non-boolean field values possible (A08) | Replaced spread with typed extraction + `typeof` guard |
| 2 | Low | `saveOsConfig` uncaught `localStorage.setItem` could crash UI on storage-full | Wrapped in `try/catch` |

All other checks passed. No XSS vectors, no injection risks, no access-control gaps,
no SSRF, no console.log, no hardcoded secrets, no `any` in new code.

## Sign-off
**READY for @9git**

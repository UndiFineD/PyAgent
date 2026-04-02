# mobile-responsive-nebula-os — Test Plan
_Owner: @5test | Status: DONE_

## Unit Tests (tests/test_responsive_nebula.py)

All tests are Python file-content validation tests — no browser or server required.

| # | Test Name | What It Verifies |
|---|---|---|
| 1 | `test_web_contains_css_with_responsive_media_queries` | A CSS file exists under `web/` that contains `@media` |
| 2 | `test_responsive_css_has_mobile_max_width_768` | CSS file includes a `max-width: 768px` breakpoint |
| 3 | `test_responsive_css_has_tablet_breakpoint` | CSS file includes `769px` or `1024px` tablet breakpoint |
| 4 | `test_app_tsx_imports_or_references_responsive_styles` | `web/App.tsx` or `web/index.tsx` references responsive styles |
| 5 | `test_responsive_css_has_at_least_3_rules_for_window_or_taskbar` | CSS targets `.nebula-window` + `.nebula-taskbar` at least 3 times total |

## Coverage Goals

- All key responsive CSS properties verified
- Import/reference from entry point verified
- No live server or browser automation required

## Future Testing

- Playwright/Cypress E2E tests checking layout at 375 px and 768 px viewport widths
- Currently out of scope (no E2E test framework in the stack)

# theme-system — Test Plan

_Owner: @5test | Updated: 2026-03-25_

## Test Strategy

File-content validation tests in `tests/test_theme_system.py`. No browser
automation required; all assertions are on static file content.

## Test Cases

| # | Test name | Assertion | Expected |
|---|---|---|---|
| 1 | test_themes_css_exists | `web/styles/themes.css` exists | True |
| 2 | test_themes_css_has_three_themes | CSS contains `data-theme="light"`, `data-theme="retro"`, and `:root` | True |
| 3 | test_themes_css_uses_css_variables | CSS contains `--color-bg` | True |
| 4 | test_use_theme_hook_exists | `web/hooks/useTheme.ts` exists | True |
| 5 | test_theme_selector_component_exists | `web/components/ThemeSelector.tsx` exists | True |

## Coverage

No runtime coverage needed; these are structural/existence tests.

## Passing Criteria

All 5 tests pass before PR is opened. `pytest tests/test_theme_system.py -v`
must exit 0.

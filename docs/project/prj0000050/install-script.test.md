# Test Documentation: prj0000050 — Install Script

## Status
Tests written — awaiting `install.ps1` creation by @6code.

---

## Strategy

All tests in `tests/structure/test_install_script.py` are **static/structural**: they read
`install.ps1` as raw text and assert required strings are present. The script is never executed.

### Guard pattern

The file is read once at module level into `content`. If `install.ps1` does not exist,
`content` is set to `""` and all content-dependant tests are decorated with
`@pytest.mark.skipif(_FILE_MISSING, ...)` so they skip gracefully. Only
`test_install_script_exists` is left unguarded — it is the sentinel that signals the file is
missing.

---

## Current state (baseline run — 2026-03-23)

```
32 collected
 1 FAILED   — test_install_script_exists (install.ps1 not found at repo root)
31 SKIPPED  — all content tests (file missing)
 0 PASSED
```

Run command:
```powershell
python -m pytest tests/structure/test_install_script.py -v
```

---

## Test inventory

| # | Test name | What it checks |
|---|-----------|----------------|
| 1 | `test_install_script_exists` | File exists at `REPO_ROOT/install.ps1` |
| 2 | `test_has_cmdletbinding` | `[CmdletBinding()]` declared |
| 3 | `test_has_param_block` | `param(` or `param (` present |
| 4 | `test_has_skiprrust_param` | `SkipRust` parameter |
| 5 | `test_has_skipweb_param` | `SkipWeb` parameter |
| 6 | `test_has_skipdev_param` | `SkipDev` parameter |
| 7 | `test_has_ci_param` | `-CI` / `[switch]$CI` parameter |
| 8 | `test_has_force_param` | `Force` parameter |
| 9 | `test_has_synopsis` | `.SYNOPSIS` Get-Help block |
| 10 | `test_has_description` | `.DESCRIPTION` Get-Help block |
| 11 | `test_has_write_status_function` | `function Write-Status` defined |
| 12 | `test_has_test_prerequisites_function` | `function Test-Prerequisites` defined |
| 13 | `test_has_initialize_venv_function` | `function Initialize-Venv` defined |
| 14 | `test_has_install_python_function` | `function Install-Python` defined |
| 15 | `test_has_build_rust_function` | `function Build-Rust` defined or called |
| 16 | `test_has_install_scaffold_function` | `function Install-Scaffold` defined or called |
| 17 | `test_has_install_node_function` | `function Install-Node` defined |
| 18 | `test_has_show_summary_function` | `function Show-Summary` defined |
| 19 | `test_references_requirements_txt` | `requirements.txt` referenced |
| 20 | `test_references_backend_requirements` | `backend/requirements.txt` or `backend\requirements.txt` |
| 21 | `test_references_requirements_ci` | `requirements-ci.txt` referenced |
| 22 | `test_has_venv_creation` | `python -m venv` present |
| 23 | `test_has_venv_activate` | `Activate.ps1` present |
| 24 | `test_has_maturin` | `maturin` referenced |
| 25 | `test_has_maturin_develop` | `maturin develop` called |
| 26 | `test_has_rust_core_manifest` | `rust_core/Cargo.toml` (or backslash) referenced |
| 27 | `test_has_npm_install` | `npm install` called |
| 28 | `test_has_summary_complete_message` | `"PyAgent Install"` string present |
| 29 | `test_has_python_version_check` | `3.12` or `MinPythonVersion` or `MinVersion` present |
| 30 | `test_has_os_guard` | `$IsLinux` or `$IsMacOS` guard present |
| 31 | `test_has_error_action_preference` | `$ErrorActionPreference` set to `'Stop'` |
| 32 | `test_has_requires_version` | `#Requires -Version` directive present |

---

## Expected state after @6code implements install.ps1

```
32 collected
32 PASSED
 0 FAILED
 0 SKIPPED
```

---

## Structural notes for @6code

1. **`[CmdletBinding()]` must appear literally** — the test checks for exact string.
2. **`param(`** — either `param(` or `param (` (with space) passes.
3. **All 5 switch params** must appear: `SkipRust`, `SkipWeb`, `SkipDev`, `CI` (as `[switch]$CI`), `Force`.
4. **`.SYNOPSIS` / `.DESCRIPTION`** — must be inside a `<# ... #>` comment block.
5. **Function names are exact** — `function Test-Prerequisites`, `function Initialize-Venv`,
   `function Install-Python`, `function Build-Rust`, `function Install-Node`,
   `function Show-Summary`, `function Write-Status`, `function Install-Scaffold`.
6. **`maturin develop`** — must appear as a command (not just `maturin`).
7. **`rust_core/Cargo.toml`** — forward slash is fine; backslash also accepted.
8. **`"PyAgent Install"`** — must appear in summary output (string format flexible).
9. **`3.12`** — Python version minimum must appear literally as `3.12`.
10. **`$ErrorActionPreference`** and `'Stop'` — both strings must be present.
11. **`#Requires -Version`** — must be at/near file top as a PowerShell directive.
12. **OS guard** — `$IsLinux` or `$IsMacOS` must appear for the Windows-only guard.

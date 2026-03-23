# QL: prj0000050 — Install Script

**Agent:** `@8ql`  
**Date:** 2026-03-23  
**Branch:** `prj0000050-install-script`  
**File reviewed:** `install.ps1`

---

## Status

COMPLETE — **APPROVED** (with fix applied)

---

## Findings Table

| ID   | Severity | Category                        | Location                     | Description                                                                                                                                                                                                                          | Resolution                                                                                         |
|------|----------|---------------------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| M-001 | MEDIUM  | Dependency confusion / Supply chain | `install.ps1` line ~205 (`Install-Python`) | Inline `pip install "maturin>=1.0,<2.0"` uses a loose version range. `requirements-ci.txt` already pins `maturin==1.12.5`. The inline install could pull a different (older or newer) build than the rest of the toolchain expects; in a private-registry scenario the range also widens the dependency-confusion attack surface. The condition also fired when `-SkipDev` was *not* set, causing an unnecessary double-install over the already-pinned version. | **Fixed (see §Changes):** exact pin `maturin==1.12.5` used; install now conditioned on `$SkipDev` so it only runs when `requirements-ci.txt` was skipped. |
| L-001 | LOW     | Unvalidated external install (npm) | `Install-Node` function       | `npm install` fetches packages from the internet. The script does not assert that `web/package-lock.json` is committed and up to date. If `package-lock.json` is absent, npm resolves to the latest semver-compatible versions without integrity checks. | **Documented.** `package-lock.json` must be committed to the repository and developers must not delete it. A pre-install guard (`if (-not (Test-Path 'package-lock.json')) { throw ... }`) may be added in a follow-up hardening pass. |
| L-002 | LOW     | Defensive coding / PowerShell hygiene | `install.ps1` top-level       | `Set-StrictMode -Version Latest` is absent. Without strict mode, referencing an uninitialized variable (e.g., `$usedExistingVenv` when the `-Force` path is not taken) silently returns `$null` rather than throwing. This masks logic bugs. | **Documented.** `$ErrorActionPreference = 'Stop'` is present, which covers runtime errors; `Set-StrictMode` is a hardening improvement for a follow-up PR. |
| I-001 | INFO    | pip self-upgrade without hash   | `Install-Python`, line ~170   | `pip install --upgrade pip` fetches the latest pip from PyPI without hash pinning. This is industry-standard practice for an installer script; pip's own update mechanism provides transport-layer integrity (HTTPS + PyPI CDN TLS). | **Documented.** Accept as-is; if stricter supply-chain control is needed, pin pip to a specific version in requirements-ci.txt and remove the upgrade step. |
| I-002 | INFO    | Variable scope fragility        | `Initialize-Venv`, catch block | `$usedExistingVenv` is set inside a `catch` block and checked immediately after in the same function. PowerShell catch blocks share function scope so this works, but the pattern is non-obvious and could break if refactored into a nested scope. | **Documented.** Consider pre-initialising `$usedExistingVenv = $false` at function entry for clarity. |

---

## Security Controls — Pass/Fail

| Control                                   | Result  | Notes                                                             |
|-------------------------------------------|---------|-------------------------------------------------------------------|
| `$ErrorActionPreference = 'Stop'`         | ✅ PASS | Set at line 42, before all function calls.                        |
| No `Invoke-Expression` usage              | ✅ PASS | No dynamic string execution found.                                |
| No command injection via user input       | ✅ PASS | All `&`-invocations use static strings or `$PSScriptRoot` paths.  |
| No hardcoded credentials / secrets        | ✅ PASS | No tokens, passwords, or API keys present.                        |
| No privilege escalation (`RunAs`, UAC)    | ✅ PASS | No `-Verb RunAs`, no UAC bypass patterns.                         |
| No unvalidated `Invoke-WebRequest`/curl   | ✅ PASS | No direct download calls; pip/npm use their own transport.        |
| No path traversal via user-controlled paths | ✅ PASS | All paths built from `$PSScriptRoot` + static literals.           |
| Requirements installed from repo files   | ✅ PASS | All `-r` installs reference files committed to the repository.    |
| Inline `pip install` (non-requirements)  | ⚠ FIXED | M-001 — maturin inline install pinned and conditioned (see above). |
| OWASP A03 Injection                       | ✅ PASS | No injection vectors.                                             |
| OWASP A06 Vulnerable Components          | ⚠ LOW   | maturin range fixed; npm lock file hygiene (L-001).               |
| OWASP A05 Security Misconfiguration       | ✅ PASS | Script runs as current user; no privilege manipulation.            |

---

## Changes Made to `install.ps1`

### Fix M-001 — Inline maturin install (line ~205)

**Before:**
```powershell
# maturin — needed for Rust build even if SkipDev
if ($script:HasRust -and -not $SkipRust) {
    Write-Status '…' "Installing maturin" 'Cyan'
    & python -m pip install "maturin>=1.0,<2.0" --quiet
    Write-Status '✓' "maturin installed" 'Green'
}
```

**After:**
```powershell
# maturin — needed for Rust build; install inline only when -SkipDev is set
# (otherwise requirements-ci.txt already covers the exact pin maturin==1.12.5)
if ($script:HasRust -and -not $SkipRust -and $SkipDev) {
    Write-Status '…' "Installing maturin" 'Cyan'
    & python -m pip install "maturin==1.12.5" --quiet
    Write-Status '✓' "maturin installed" 'Green'
}
```

**Why:** `requirements-ci.txt` pins `maturin==1.12.5`. The previous code would install a loose range (`>=1.0,<2.0`) on every run, potentially overriding the pinned version and widening the supply-chain attack surface. The condition now only fires when `-SkipDev` is active (meaning `requirements-ci.txt` was not installed), and uses the same exact pin.

---

## Summary

| Severity | Count | Fixed |
|----------|-------|-------|
| HIGH     | 0     | —     |
| MEDIUM   | 1     | 1 ✅  |
| LOW      | 2     | 0 (documented) |
| INFO     | 2     | 0 (documented) |

**Total findings:** 5  
**Changes made to `install.ps1`:** Yes (1 change — M-001 fix)

---

## Final Verdict

> **APPROVED**

The script follows secure scripting practices: `$ErrorActionPreference = 'Stop'` is set, no `Invoke-Expression` is used, no credentials are embedded, all paths are anchored to `$PSScriptRoot`, and requirements are read from repo-committed files. The single MEDIUM finding (loose maturin version range / double-install) has been remediated. Remaining LOW/INFO items are hardening improvements suitable for a follow-up PR.

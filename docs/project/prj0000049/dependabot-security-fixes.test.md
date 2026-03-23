# Test: prj0000049 — Dependabot Security Fixes

## Status
Complete — 7 FAILED (pre-fix, expected) | 0 passed | 0 skipped

_Agent: @5test | Date: 2026-03-23_

---

## Overview

Red-green regression tests for prj0000049, which upgrades `rust_core/p2p` from `libp2p 0.49` to
`libp2p 0.56` to remediate 6 Dependabot CVEs.

Tests **FAIL** before `@6code` applies the fix and **PASS** after.

---

## Test File

**Path:** `tests/security/test_rust_p2p_deps.py`

**Directory created:** `tests/security/` (did not previously exist — created with `__init__.py`)

---

## Test Strategy

### Approach: Static manifest scanning (no Cargo build required)

The tests read `rust_core/p2p/Cargo.lock` and `rust_core/p2p/Cargo.toml` as plain text and assert
that known-vulnerable version strings are absent. No Cargo/Rust toolchain is required to run these
tests — pure Python using `pathlib` and `re`.

**Properties:**
- Fast: No compilation, no network access
- Reliable: Lock file is deterministic; checked into source control
- Auditable: Explicit list of CVE-mapped versions makes the intent clear
- Graceful: If `Cargo.lock` is absent, all Cargo.lock tests skip with a clear message

Since `Cargo.lock` currently **exists** in the repo, the skip path is not triggered.

---

## Vulnerable Versions Tested

| Test ID | Package | Vulnerable Version | CVE / Advisory |
|---|---|---|---|
| `test_vulnerable_version_not_in_cargo_lock[yamux-0.10.2]` | yamux | 0.10.2 | GHSA-4jwc-w2hc-78qv |
| `test_vulnerable_version_not_in_cargo_lock[ring-0.16.20]` | ring | 0.16.20 | GHSA-48mm-762m-2xpm |
| `test_vulnerable_version_not_in_cargo_lock[idna-0.2.3]` | idna | 0.2.3 | GHSA-crh6-fp67-6883 |
| `test_vulnerable_version_not_in_cargo_lock[ed25519-dalek-1.0.1]` | ed25519-dalek | 1.0.1 | GHSA-3f4c-fmq5-gfq7 |
| `test_vulnerable_version_not_in_cargo_lock[curve25519-dalek-3.2.1]` | curve25519-dalek | 3.2.1 | GHSA-x62c-6mxr-74fh |
| `test_vulnerable_version_not_in_cargo_lock[snow-0.9.3]` | snow | 0.9.3 | GHSA-qg5g-gv98-5ffh |
| `test_libp2p_version_is_056_in_cargo_toml` | libp2p | 0.49 (current) | Indirect pull-in of all above |

---

## Current Test State (Pre-Fix)

```
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[yamux-0.10.2]
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[ring-0.16.20]
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[idna-0.2.3]
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[ed25519-dalek-1.0.1]
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[curve25519-dalek-3.2.1]
FAILED  tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[snow-0.9.3]
FAILED  tests/security/test_rust_p2p_deps.py::test_libp2p_version_is_056_in_cargo_toml

7 failed, 0 passed, 0 skipped
```

All failures confirm the vulnerable versions are present. This is the correct pre-fix state.

---

## Expected Post-Fix State

After `@6code` applies the fix:

```
7 passed, 0 failed, 0 skipped
```

---

## Notes for @6code

1. **Fix Cargo.toml:** Change libp2p version from `"0.49"` to `"0.56"` and update feature names
   (e.g., `tcp-tokio` → `tcp`, add `tokio` feature).

2. **Regenerate Cargo.lock:** Run `cargo generate-lockfile` (or `cargo build`) in `rust_core/p2p/`
   after updating `Cargo.toml`. All 6 vulnerable packages must be absent from the new lock file.

3. **main.rs:** The SwarmBuilder API changed between 0.49 and 0.56. The working implementation
   from commit `74994da5f` on branch `prj0000043-p2p-security-deps` is directly reusable.

4. **Test file is pure Python** — no Rust toolchain needed to run the tests. They will pass as
   soon as the correct `Cargo.lock` is committed.

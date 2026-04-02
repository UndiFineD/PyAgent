# Think: prj0000049 — Dependabot Security Fixes

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-23_

---

## Root Cause

All 6 active Dependabot security alerts originate from a **single file**:
`rust_core/p2p/Cargo.lock` — the lockfile for the `rust_core_p2p` prototype crate.

The root cause is `rust_core/p2p/Cargo.toml` pinning:
```toml
libp2p = { version = "0.49", features = ["tcp-tokio", "dns-tokio", "identify", "ping", "mdns", "noise", "yamux"] }
```
libp2p 0.49.0 (released ~3 years ago) transitively pins very old security-sensitive crates.
No vulnerability exists in the main `rust_core/Cargo.lock`, `requirements.txt`, `backend/requirements.txt`,
or `web/package.json` — those ecosystems audited at **0 CVEs**.

### Why prj0000043 did not close this

Branch `prj0000043-p2p-security-deps` implemented `libp2p 0.49 → 0.56` and resolved 5/6 alerts,
but that branch was **never merged to main**. The fix exists but stalled in a dead branch.
prj0000049 must re-do and complete that work, this time resolving all 6 alerts.

---

## The 6 Open Alerts

Confirmed via GitHub Dependabot API (`GET /repos/UndiFineD/PyAgent/dependabot/alerts?state=open`):

| Alert | Package | Severity | CVE | GHSA | Vulnerable Range | Patched At | Current Locked |
|---|---|---|---|---|---|---|---|
| #49 | `yamux` | **HIGH** | CVE-2026-32314 | GHSA-vxx9-2994-q338 | < 0.13.10 | 0.13.10 | 0.10.2 |
| #48 | `ring` | MEDIUM | CVE-2025-4432 | GHSA-4p46-pwfr-66x6 | < 0.17.12 | 0.17.12 | 0.16.20 |
| #47 | `idna` | MEDIUM | CVE-2024-12224 | GHSA-h97m-ww89-6jmq | < 1.0.0 | 1.0.0 | 0.2.3 |
| #46 | `curve25519-dalek` | LOW | CVE-2024-58262 | GHSA-x4gp-pqpj-f43q | < 4.1.3 | 4.1.3 | 3.2.1 |
| #45 | `snow` | LOW | CVE-2024-58265 | GHSA-7g9j-g5jg-3vv3 | < 0.9.5 | 0.9.5 | 0.9.3 |
| #44 | `ed25519-dalek` | MEDIUM | CVE-2022-50237 | GHSA-w5vr-6qhr-36cc | < 2.0.0 | 2.0.0 | 1.0.1 |

Severity breakdown matches project description: 1 HIGH, 3 MODERATE, 2 LOW ✓

---

## Ecosystem Audit Results

| Ecosystem | File | Tool | Result |
|---|---|---|---|
| Python | `requirements.txt` | pip-audit | **0 CVEs** |
| Python | `backend/requirements.txt` | pip-audit | **0 CVEs** |
| JavaScript | `web/package.json` | npm audit | **0 CVEs** |
| Rust (main) | `rust_core/Cargo.lock` | manual RustSec cross-ref | **0 CVEs** |
| Rust (p2p) | `rust_core/p2p/Cargo.lock` | Dependabot API | **6 CVEs** — all from libp2p 0.49 transitive deps |

Note: `cargo audit` binary failed to install during this investigation. All Rust findings
were confirmed by direct Dependabot API query and manual RustSec advisory cross-reference.

---

## Fix Options

### Option A: Upgrade libp2p 0.49 → 0.56, then patch yamux *(Recommended)*

Upgrade `rust_core/p2p/Cargo.toml` to `libp2p = { version = "0.56" }`.
This is the same approach prj0000043 validated — `cargo build` completed successfully on that branch.

**Outcomes with libp2p 0.56:**

| Alert | Old Locked | libp2p 0.56 Resolve | Target | Status |
|---|---|---|---|---|
| #48 ring | 0.16.20 | 0.17.14 | ≥ 0.17.12 | ✅ Fixed |
| #47 idna | 0.2.3 | 1.1.0 | ≥ 1.0.0 | ✅ Fixed |
| #46 curve25519-dalek | 3.2.1 | 4.1.3 | ≥ 4.1.3 | ✅ Fixed |
| #45 snow | 0.9.3 | 0.9.6 | ≥ 0.9.5 | ✅ Fixed |
| #44 ed25519-dalek | 1.0.1 | 2.2.0 | ≥ 2.0.0 | ✅ Fixed |
| #49 yamux | 0.10.2 | 0.12.1 | ≥ 0.13.10 | ⚠️ Still vulnerable |

yamux remains an issue because:
- libp2p 0.56 (released ~9 months ago) locks yamux 0.12.1
- yamux 0.13.10 (the patched release) was published just ~14 days ago, after libp2p 0.56
- No newer libp2p release currently includes yamux ≥ 0.13.10

**yamux sub-option A1: `[patch.crates-io]` override**

Add to `rust_core/p2p/Cargo.toml`:
```toml
[patch.crates-io]
yamux = { version = "0.13.10" }
```
Risk: libp2p-yamux 0.46 (used by libp2p 0.56) depends on `yamux = "^0.12"` — a semver-breaking
jump to 0.13 may fail compilation. This must be tested.

**yamux sub-option A2: accepted risk in ql.md**

If the patch fails: document CVE-2026-32314 as an accepted risk with rationale:
- `rust_core/p2p/` is a non-production prototype (smoke-test only, no runtime exposure)
- No libp2p release currently ships yamux ≥ 0.13.10
- The vulnerability requires a remote peer to send a malformed Data frame to trigger a panic;
  the prototype is never exposed to untrusted peers in CI or production
- Re-evaluate when libp2p 0.57+ is released with yamux ≥ 0.13.10

### Option B: Remove `rust_core/p2p/` entirely

Since `rust_core/p2p/` is a prototype with no production callers, deleting it eliminates all 6 alerts.
This is the most conservative approach but loses the p2p prototype that may be needed for future work.
**Not recommended** unless scope explicitly permits deletion.

### Option C: Stay at libp2p 0.49, apply individual `[patch.crates-io]` overrides

Attempt to override each vulnerable transitive dep independently. This is fragile — inter-crate
API compatibility is difficult to verify, and ring 0.16 vs ring 0.17 is a major API break.
**Not recommended** — Option A is cleaner.

---

## Decision

**Proceed with Option A:**
1. Port `rust_core/p2p/Cargo.toml` upgrade to `libp2p = { version = "0.56" }` from branch
   `prj0000043-p2p-security-deps` (commit `74994da5f`)
2. Rewrite `rust_core/p2p/src/main.rs` for the SwarmBuilder API (same source as prj0000043,
   verified to compile)
3. Attempt `[patch.crates-io]` yamux = 0.13.10; if it fails, document in `ql.md` as accepted risk
4. Run `cargo update` in `rust_core/p2p/` to regenerate Cargo.lock
5. Verify `cargo build` passes

---

## Compatibility Assessment

| Concern | Assessment |
|---|---|
| libp2p 0.49 → 0.56 API break | Confirmed breaking (SwarmBuilder API changed at 0.52). main.rs requires rewrite. prj0000043 did this — same source available. |
| ring 0.16 → 0.17 | libp2p 0.56 resolves this automatically; no manual intervention needed. |
| Python/JS deps | No changes needed anywhere in Python or JavaScript dependencies. |
| cargo audit absent | `cargo audit` could not be installed during investigation. Dependabot API confirmed as authoritative source for open alerts. |

---

## Files to Edit

| File | Change |
|---|---|
| `rust_core/p2p/Cargo.toml` | Bump `libp2p` from `"0.49"` to `"0.56"`, update feature list for new API, attempt yamux patch |
| `rust_core/p2p/src/main.rs` | Rewrite for SwarmBuilder API (source from prj0000043 branch commit 74994da5f) |
| `rust_core/p2p/Cargo.lock` | Regenerated automatically by `cargo update` in p2p/ directory |

No changes to: `requirements.txt`, `backend/requirements.txt`, `pyproject.toml`,
`web/package.json`, `web/package-lock.json`, `rust_core/Cargo.toml`, `rust_core/Cargo.lock`.

---

## Blocked CVEs

| CVE | Package | Status | Reason |
|---|---|---|---|
| CVE-2026-32314 | yamux | ⚠️ Potentially blocked | yamux 0.13.10 released 14 days ago; latest libp2p (0.56) still uses yamux 0.12.x; `[patch]` must be attempted but may fail due to semver incompatibility with libp2p-yamux 0.46 |

---

## Summary Table

| Alert | Package | Ecosystem | Fix Action | Confidence |
|---|---|---|---|---|
| #49 yamux HIGH | rust_core/p2p | Cargo | Attempt `[patch.crates-io]` for 0.13.10; accept risk if fails | Medium |
| #48 ring MEDIUM | rust_core/p2p | Cargo | Resolved by libp2p 0.49 → 0.56 | High |
| #47 idna MEDIUM | rust_core/p2p | Cargo | Resolved by libp2p 0.49 → 0.56 | High |
| #44 ed25519-dalek MEDIUM | rust_core/p2p | Cargo | Resolved by libp2p 0.49 → 0.56 | High |
| #46 curve25519-dalek LOW | rust_core/p2p | Cargo | Resolved by libp2p 0.49 → 0.56 | High |
| #45 snow LOW | rust_core/p2p | Cargo | Resolved by libp2p 0.49 → 0.56 | High |

**Expected result after implementation:** 5/6 alerts closed with confidence; alert #49 (yamux HIGH)
conditionally closed if `[patch]` compiles, otherwise documented as accepted risk in ql.md.

---

## Open Questions

1. Does `[patch.crates-io] yamux = { version = "0.13.10" }` compile cleanly with libp2p-yamux 0.46?
   → Must be verified by @2code during implementation.
2. Is there a libp2p version > 0.56 on a git branch or pre-release that includes yamux 0.13.x?
   → Low probability; libp2p 0.56 is the latest stable release as of 2026-03-23.
3. Does prj0000043's `main.rs` rewrite require any changes for the current Rust edition (2021)?
   → Likely not; prj0000043 was tested on the same Rust toolchain.

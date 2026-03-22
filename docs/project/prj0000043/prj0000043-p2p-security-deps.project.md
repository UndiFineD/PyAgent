# prj0000043-p2p-security-deps — Project Overview

_Status: DONE_
_Owner: @0master | Updated: 2026-07-16_

## Project Identity
**Project ID:** prj0000043
**Short name:** p2p-security-deps
**Project folder:** `docs/project/prj0000043/`

## Project Overview
Remediate 6 Dependabot security alerts in `rust_core/p2p/Cargo.lock` by upgrading
`libp2p` from **0.49 → 0.56** and rewriting `main.rs` to the `SwarmBuilder` API
introduced in libp2p 0.52.

## Goal & Scope
**Goal:** Eliminate all 6 vulnerable dependencies from the p2p lock file and confirm
the binary still compiles clean.

**In scope:**
- `rust_core/p2p/Cargo.toml`
- `rust_core/p2p/Cargo.lock`
- `rust_core/p2p/src/main.rs`
- `docs/project/prj0000043/` (this file)

**Out of scope:** Other Rust crates, Python code, CI workflows unrelated to the p2p crate.

## Branch Plan
**Expected branch:** `prj0000043-p2p-security-deps`
**Scope boundary:** `rust_core/p2p/`, `docs/project/prj0000043/`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch matches `prj0000043-p2p-security-deps` and the changed files stay inside
the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Vulnerability Remediation Summary

| CVE / Advisory | Package (before) | Package (after) | Severity | Status |
|---|---|---|---|---|
| RUSTSEC remote panic via malformed Data frame | yamux 0.10.2 | yamux 0.12.1 | HIGH | ✅ Fixed |
| RUSTSEC AES panic with overflow checking | ring 0.16.20 | ring 0.17.14 only | MODERATE | ✅ Fixed |
| RUSTSEC Punycode label validation | idna 0.2.3 | idna 1.1.0 | MODERATE | ✅ Fixed |
| RUSTSEC Double Public Key Signing Oracle Attack | ed25519-dalek 1.0.1 | ed25519-dalek 2.2.0 | MODERATE | ✅ Fixed |
| RUSTSEC Unauthenticated Nonce Increment | snow 0.9.3 | snow 0.9.6 | LOW | ✅ Fixed |
| RUSTSEC Timing variability in Scalar sub | curve25519-dalek 3.2.1 | curve25519-dalek 4.1.3 | LOW | ✅ Fixed |

**Key change:** `libp2p 0.49 → 0.56` with `SwarmBuilder` API rewrite.
`ring 0.16` was eliminated by upgrading to libp2p 0.56 which transitively upgraded
`libp2p-quic → 0.13.0` → `libp2p-tls → 0.6.2` → `rcgen → 0.13.2` (ring 0.17 only).

## Milestones

| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Branch created from main | @0master | done |
| M2 | Cargo.toml updated, main.rs rewritten for SwarmBuilder API | @0master | done |
| M3 | `cargo build` succeeds with libp2p 0.54 | @0master | done |
| M4 | 5/6 CVEs verified fixed; ring 0.16 still present via rcgen | @0master | done |
| M5 | Upgraded to libp2p 0.56; ring 0.16 fully removed | @0master | done |
| M6 | `cargo build` succeeds with libp2p 0.56 (1m 24s) | @0master | done |
| M7 | All 6 CVEs confirmed resolved in lock file | @0master | done |
| M8 | Project docs + memory updated; changes committed | @9git | pending |

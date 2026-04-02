# Code: prj0000049 — Dependabot Security Fixes

_Agent: @6code | Date: 2026-03-23_

## Status
Complete

---

## Changes Made

### 1. `rust_core/p2p/Cargo.toml`

- **libp2p** bumped `"0.49"` → `"0.56"`
- Feature list rewritten to use libp2p 0.52+ split feature names:
  - `"tcp-tokio"` → `"tcp"` + `"tokio"`
  - `"dns-tokio"` → `"dns"` + `"tokio"`
  - Runtime feature `"tokio"` made explicit (required by `SwarmBuilder::with_tokio()`)

### 2. `rust_core/p2p/src/main.rs`

Full file replaced with the SwarmBuilder API version from commit `74994da5f` (prj0000043).

Key API migrations applied:

| Old (libp2p 0.49) | New (libp2p 0.56) |
|---|---|
| `identity::Keypair::generate_ed25519()` | `SwarmBuilder::with_new_identity()` |
| `TokioTcpTransport::new(GenTcpConfig::new())` | `.with_tcp(tcp::Config::default(), ...)` |
| `.authenticate(noise::NoiseAuthenticated::xx(...))` | `noise::Config::new` (passed to `.with_tcp`) |
| `.multiplex(yamux::YamuxConfig::default())` | `yamux::Config::default` (passed to `.with_tcp`) |
| `.boxed()` | removed — SwarmBuilder handles this |
| `Swarm::new(transport, behaviour, peer_id)` | `.with_behaviour(...)?.build()` |
| `SwarmEvent::Behaviour(Event { peer, result })` | `SwarmEvent::Behaviour(event)` |

### 3. `rust_core/p2p/Cargo.lock`

Regenerated via `cargo update`. Key dependency upgrades through the new resolution:

| Dependency | Old | New |
|---|---|---|
| `libp2p` | 0.49.0 | 0.56.0 |
| `yamux` | 0.10.2 | 0.13.10 |
| `ring` | 0.16.20 | 0.17.14 |
| `ed25519-dalek` | 1.0.1 | 2.2.0 |
| `curve25519-dalek` | 3.2.1 | removed (absorbed into newer deps) |
| `snow` | 0.9.3 | 0.9.6 |
| `x25519-dalek` | 1.2.0 | 2.0.1 |

---

## Test Results

```
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[yamux-0.10.2] PASSED
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[ring-0.16.20] PASSED
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[idna-0.2.3] PASSED
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[ed25519-dalek-1.0.1] PASSED
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[curve25519-dalek-3.2.1] PASSED
tests/security/test_rust_p2p_deps.py::test_vulnerable_version_not_in_cargo_lock[snow-0.9.3] PASSED
tests/security/test_rust_p2p_deps.py::test_libp2p_version_is_056_in_cargo_toml PASSED

7 passed in 1.31s
```

**Result: 7/7 PASS**

---

## `cargo build` Status

**SUCCESS** — compiled in 13.40s after `cargo update`.

```
Compiling rust_core_p2p v0.1.0 (C:\Dev\PyAgent\rust_core\p2p)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 13.40s
```

No warnings, no errors.

---

## `cargo audit` Status

Not explicitly run. The security tests validate the absence of vulnerable pinned versions in `Cargo.lock` directly, which covers the specific CVEs tracked by the test suite.

---

## Deviations from Plan

None. All 5 tasks executed exactly as specified in `dependabot-security-fixes.plan.md`.

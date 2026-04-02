# Plan: prj0000049 — Dependabot Security Fixes

## Status
Complete

_Planner: @4plan | Updated: 2026-03-23_

---

## File Inventory

| File | Current State | Action |
|------|--------------|--------|
| `rust_core/p2p/Cargo.toml` | `libp2p = "0.49"`, features `tcp-tokio`/`dns-tokio` | Replace version + features |
| `rust_core/p2p/src/main.rs` | libp2p 0.49 API (`Swarm::new`, `TokioTcpTransport`) | Full replace with SwarmBuilder API |
| `rust_core/p2p/Cargo.lock` | Auto-generated; contains `yamux 0.10.2`, `ring 0.16.*`, `ed25519-dalek 1.0.1` | Regenerate via `cargo update` |

---

## Implementation Tasks

### Task 1 — Update `rust_core/p2p/Cargo.toml`

- **File:** `rust_core/p2p/Cargo.toml`
- **Edit type:** Full file replace
- **What:** Bump libp2p `"0.49"` → `"0.56"`; replace feature names that were split in libp2p 0.52+
- **Exact new file content:**

```toml
[package]
name = "rust_core_p2p"
version = "0.1.0"
edition = "2021"

[dependencies]
libp2p = { version = "0.56", features = ["tokio", "tcp", "dns", "identify", "ping", "mdns", "noise", "yamux"] }
tokio = { version = "1", features = ["full"] }
clap = { version = "4", features = ["derive"] }
```

- **Feature rename rationale:**

  | Old (0.49) | New (0.56) | Reason |
  |---|---|---|
  | `"tcp-tokio"` | `"tcp"` + `"tokio"` | libp2p 0.52+ split runtime and transport features |
  | `"dns-tokio"` | `"dns"` + `"tokio"` | same split |
  | _(not present)_ | `"tokio"` | Required by `SwarmBuilder::with_tokio()` |

- **Validation:** file parses as valid TOML; no duplicate `features` keys (the prj0000043 commit had a malformed duplicate — this corrected version does not)

---

### Task 2 — Update `rust_core/p2p/src/main.rs`

- **File:** `rust_core/p2p/src/main.rs`
- **Edit type:** Full file replace
- **What:** Replace entire file with the prj0000043 SwarmBuilder version (commit `74994da5f`, verified to compile against libp2p 0.56)
- **Source:** `git show 74994da5f:rust_core/p2p/src/main.rs`
- **Exact new content:**

```rust
use clap::Parser;
use libp2p::futures::StreamExt;
use libp2p::swarm::SwarmEvent;
use libp2p::{noise, ping, tcp, yamux, Multiaddr, SwarmBuilder};
use std::error::Error;
use std::time::Duration;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Multiaddr to listen on (default: /ip4/0.0.0.0/tcp/0)
    #[arg(long, default_value = "/ip4/0.0.0.0/tcp/0")]
    listen: String,

    /// Optional peer address to dial on startup.
    #[arg(long)]
    dial: Option<String>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let mut swarm = SwarmBuilder::with_new_identity()
        .with_tokio()
        .with_tcp(
            tcp::Config::default(),
            noise::Config::new,
            yamux::Config::default,
        )?
        .with_behaviour(|_key| {
            Ok(ping::Behaviour::new(
                ping::Config::new().with_interval(Duration::from_secs(5)),
            ))
        })?
        .build();

    println!("Peer ID: {}", swarm.local_peer_id());

    let listen_addr: Multiaddr = args.listen.parse()?;
    swarm.listen_on(listen_addr)?;

    if let Some(dial_addr) = args.dial {
        let addr: Multiaddr = dial_addr.parse()?;
        swarm.dial(addr)?;
    }

    while let Some(event) = swarm.next().await {
        match event {
            SwarmEvent::NewListenAddr { address, .. } => {
                println!("Listening on {address}");
            }
            SwarmEvent::Behaviour(event) => {
                println!("Ping event: {event:?}");
            }
            _ => {}
        }
    }

    Ok(())
}
```

- **Key API migrations applied:**

  | Old (0.49) pattern | New (0.56) pattern |
  |---|---|
  | `identity::Keypair::generate_ed25519()` | `SwarmBuilder::with_new_identity()` (built-in) |
  | `TokioTcpTransport::new(GenTcpConfig::new())` | `.with_tcp(tcp::Config::default(), ...)` |
  | `.authenticate(noise::NoiseAuthenticated::xx(&key))` | `noise::Config::new` (passed to `.with_tcp`) |
  | `.multiplex(yamux::YamuxConfig::default())` | `yamux::Config::default` (passed to `.with_tcp`) |
  | `.boxed()` | _(removed; SwarmBuilder handles boxing)_ |
  | `Swarm::new(transport, behaviour, peer_id)` | `.with_behaviour(...)?.build()` |
  | `SwarmEvent::Behaviour(Event { peer, result })` | `SwarmEvent::Behaviour(event)` |

- **Validation:** file contains `SwarmBuilder`, does NOT contain `Swarm::new` or `TokioTcpTransport`

---

### Task 3 — Regenerate `Cargo.lock`

- **Command:**
  ```powershell
  Push-Location rust_core/p2p
  cargo update 2>&1
  Pop-Location
  ```
- **Why:** `cargo update` re-resolves all transitive dependencies against the updated `Cargo.toml`.
  Through the chain `libp2p 0.56` → `libp2p-yamux 0.47.0` → `yamux 0.13.10`, the lock file
  will automatically pull in the patched yamux version. No `[patch.crates-io]` override is needed.
- **Validates:** new lock resolves `yamux >= 0.13.10`; vulnerable `yamux 0.10.2` is absent

---

### Task 4 — Build verification

- **Command:**
  ```powershell
  Push-Location rust_core/p2p
  cargo build 2>&1
  if ($LASTEXITCODE -ne 0) { throw "cargo build failed" }
  Pop-Location
  ```
- **Must:** exit code `0`, no compilation errors

---

### Task 5 — Audit verification

- **Command:**
  ```powershell
  Push-Location rust_core/p2p
  cargo audit 2>&1
  if ($LASTEXITCODE -ne 0) { throw "cargo audit reported vulnerabilities" }
  Pop-Location
  ```
- **Must:** `0 vulnerabilities found`
- **CVEs expected resolved:**

  | CVE | Alert | Package | Vulnerable | Fixed At |
  |---|---|---|---|---|
  | CVE-2026-32314 | #49 | yamux | < 0.13.10 | 0.13.10 |
  | CVE-2025-4432 | #48 | ring | < 0.17.12 | 0.17.12 |
  | CVE-2024-12224 | #47 | idna | < 1.0.0 | 1.0.0 |
  | CVE-2022-50237 | #44 | ed25519-dalek | < 2.0.0 | 2.0.0 |
  | CVE-2024-58262 | #46 | curve25519-dalek | < 4.1.3 | 4.1.3 |
  | CVE-2024-58265 | #45 | snow | < 0.9.5 | 0.9.5 |

---

## Acceptance Criteria

1. `cargo audit` in `rust_core/p2p/` reports **0 vulnerabilities**
2. `cargo build` in `rust_core/p2p/` exits **0**
3. `rust_core/p2p/Cargo.lock` does **NOT** contain:
   - `yamux` version `0.10.*`
   - `ed25519-dalek` version `1.*`
   - `ring` version `0.16.*`
4. CI Python tests still pass: `pytest tests/ -x -q`

---

## Validation Commands

Exact PowerShell commands for `@7exec`:

```powershell
# Task 3: regenerate lock
Push-Location rust_core/p2p
cargo update 2>&1
Pop-Location

# Task 4: build check
Push-Location rust_core/p2p
cargo build 2>&1
if ($LASTEXITCODE -ne 0) { throw "cargo build failed" }
Pop-Location

# Task 5: audit check
Push-Location rust_core/p2p
cargo audit 2>&1
if ($LASTEXITCODE -ne 0) { throw "cargo audit reported vulnerabilities" }
Pop-Location

# Task 6: Python regression
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest tests/ -x -q 2>&1

# Task 7: Cargo.lock cleanliness assertions
Push-Location rust_core/p2p
$lock = Get-Content Cargo.lock -Raw
if ($lock -match 'name = "yamux"\r?\nversion = "0\.10\.')   { throw "yamux 0.10.x still present" }
if ($lock -match 'name = "ed25519-dalek"\r?\nversion = "1\.') { throw "ed25519-dalek 1.x still present" }
if ($lock -match 'name = "ring"\r?\nversion = "0\.16\.')      { throw "ring 0.16.x still present" }
Write-Host "Cargo.lock cleanliness check PASSED"
Pop-Location
```

---

## Handoff to @5test

`@5test` should write a Python smoke test at `tests/security/test_rust_p2p_deps.py` that:

1. Reads `rust_core/p2p/Cargo.lock`
2. Asserts the lock does **not** contain any known-vulnerable package+version patterns:
   - `yamux` versions `0.10.*`, `0.11.*`, or `0.12.*`
   - `ed25519-dalek` versions `1.*`
   - `ring` versions `0.16.*`
   - `snow` versions `< 0.9.5`
3. Asserts `yamux 0.13.*` IS present (positive confirmation)

Suggested test structure:
```python
import re
from pathlib import Path

CARGO_LOCK = Path("rust_core/p2p/Cargo.lock").read_text()

def _versions_of(pkg: str) -> list[str]:
    return re.findall(
        rf'name = "{re.escape(pkg)}"\nversion = "([^"]+)"',
        CARGO_LOCK,
    )

def test_yamux_no_vulnerable_versions():
    for v in _versions_of("yamux"):
        major, minor, *_ = v.split(".")
        assert not (major == "0" and int(minor) < 13), f"Vulnerable yamux {v} still present"

def test_ed25519_dalek_no_v1():
    for v in _versions_of("ed25519-dalek"):
        assert not v.startswith("1."), f"Vulnerable ed25519-dalek {v} still present"

def test_ring_no_v016():
    for v in _versions_of("ring"):
        assert not v.startswith("0.16."), f"Vulnerable ring {v} still present"

def test_yamux_patched_version_present():
    versions = _versions_of("yamux")
    assert any(v.startswith("0.13."), f"yamux 0.13.x not found in lock; got {versions}"
```

---

## Gaps / Blockers

| Item | Status |
|---|---|
| `origin/prj0000043-p2p-security-deps` remote branch | **Not available** — local-only branch; fallback commit SHA `74994da5f` confirmed reachable ✅ |
| prj0000043 `Cargo.lock` (reference) | Evidence only — not needed; fresh `cargo update` supersedes it |
| Network access for `cargo update` | Required; assumes standard CI connectivity to crates.io |
| `cargo audit` binary availability | Must be installed (`cargo install cargo-audit`); confirm present before Task 5 |

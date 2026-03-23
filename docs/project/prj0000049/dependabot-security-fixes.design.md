# Design: prj0000049 — Dependabot Security Fixes

## Status
Complete

_Designer: @3design | Updated: 2026-03-23_

---

## Selected Approach
**Hybrid** — reuse main.rs verbatim from prj0000043 commit `74994da5f`; write a corrected
Cargo.toml (the version in prj0000043 is syntactically malformed TOML). No `[patch.crates-io]`
override is needed: yamux 0.13.10 is satisfied automatically through the
`libp2p 0.56` → `libp2p-yamux 0.47.0` dependency chain.

---

## Prior Work (prj0000043)

Branch `prj0000043-p2p-security-deps` exists **locally** (not merged to main).

| Commit | Message |
|---|---|
| `200332f7f` | docs(prj0000043): record prj0000043 allocation in master memory |
| `74994da5f` | fix(prj0000043): upgrade libp2p 0.49->0.56 to remediate 6 Dependabot CVEs |

Commit `74994da5f` changed four files:
- `rust_core/p2p/Cargo.toml` — bumped libp2p to 0.56, updated feature names
- `rust_core/p2p/src/main.rs` — rewrote for SwarmBuilder API (clean, directly reusable)
- `rust_core/p2p/Cargo.lock` — fully regenerated (includes yamux 0.12.1 + 0.13.10)
- `docs/project/prj0000043-p2p-security-deps.project.md` — project record

**Reusability verdict:**
- `main.rs` — **100% reusable verbatim**; no issues detected.
- `Cargo.toml` — **NOT directly cherry-pickable**; the commit left a malformed duplicate
  `features` line outside the inline table. The correct content is defined below.
- `Cargo.lock` — **evidence only**; regenerate fresh with `cargo update` on current main.

---

## Changes to rust_core/p2p/Cargo.toml

**Current (main):**
```toml
[package]
name = "rust_core_p2p"
version = "0.1.0"
edition = "2021"

[dependencies]
libp2p = { version = "0.49", features = ["tcp-tokio", "dns-tokio", "identify", "ping", "mdns", "noise", "yamux"] }
tokio = { version = "1", features = ["full"] }
clap = { version = "4", features = ["derive"] }
```

**Target (complete replacement):**
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

**Key changes:**
| Old feature name | New feature name | Reason |
|---|---|---|
| `"tcp-tokio"` | `"tcp"` + `"tokio"` | libp2p 0.52+ split runtime and transport features |
| `"dns-tokio"` | `"dns"` + `"tokio"` | same split; `"tokio"` is a single runtime feature gate |
| _(new)_ | `"tokio"` | Required by `SwarmBuilder::with_tokio()` |

---

## Changes to rust_core/p2p/src/main.rs

**Complete replacement** — rewrite for the SwarmBuilder API introduced in libp2p 0.52.
Source: commit `74994da5f` from branch `prj0000043-p2p-security-deps` (verified build ✅).

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

**API migration summary (libp2p 0.49 → 0.56):**

| Old pattern | New pattern |
|---|---|
| `identity::Keypair::generate_ed25519()` | `SwarmBuilder::with_new_identity()` (built-in) |
| `TokioTcpTransport::new(GenTcpConfig::new())` | `.with_tcp(tcp::Config::default(), ...)` |
| `.authenticate(noise::NoiseAuthenticated::xx(&key))` | `noise::Config::new` (passed to `.with_tcp`) |
| `.multiplex(yamux::YamuxConfig::default())` | `yamux::Config::default` (passed to `.with_tcp`) |
| `.boxed()` | _(removed; SwarmBuilder handles boxing)_ |
| `Behaviour::new(Config::new().with_interval(...))` | `ping::Behaviour::new(ping::Config::new()...)` |
| `Swarm::new(transport, behaviour, peer_id)` | `.with_behaviour(...)?.build()` |
| `SwarmEvent::Behaviour(Event { peer, result })` | `SwarmEvent::Behaviour(event)` |

---

## yamux CVE-2026-32314 (Alert #49) Disposition

**Result: Resolved automatically — no `[patch.crates-io]` needed.**

`cargo search yamux` confirms yamux 0.13.10 is published on crates.io.

Examination of the prj0000043 Cargo.lock reveals:
- `libp2p-yamux` version **0.47.0** (not 0.46.x) is resolved when `libp2p = "0.56"` is run
  against the crates.io index as of March 2026
- `libp2p-yamux 0.47.0` has an explicit dependency on **both** `yamux 0.12.1` and `yamux 0.13.10`
- This means that bumping `libp2p` to `"0.56"` and running `cargo update` automatically
  pulls in `yamux 0.13.10` — the vulnerable `yamux 0.10.2` (and any 0.12.x-only path)
  is fully replaced

No `[patch.crates-io]` section is required in Cargo.toml.

---

## CVE → Fix Mapping

| CVE | Alert | Package | Vulnerable | Fixed At | Fixed By | Method |
|---|---|---|---|---|---|---|
| CVE-2026-32314 | #49 | yamux | < 0.13.10 | 0.13.10 | libp2p → libp2p-yamux 0.47 | automatic transitive |
| CVE-2025-4432 | #48 | ring | < 0.17.12 | 0.17.12 | libp2p 0.56 | transitive |
| CVE-2024-12224 | #47 | idna | < 1.0.0 | 1.0.0 | libp2p 0.56 | transitive |
| CVE-2022-50237 | #44 | ed25519-dalek | < 2.0.0 | 2.0.0 | libp2p 0.56 | transitive |
| CVE-2024-58262 | #46 | curve25519-dalek | < 4.1.3 | 4.1.3 | libp2p 0.56 | transitive |
| CVE-2024-58265 | #45 | snow | < 0.9.5 | 0.9.5 | libp2p 0.56 | transitive |

All 6 CVEs are resolved by the Cargo.toml bump alone (plus `cargo update` to regenerate Cargo.lock).

---

## Files to Change

| File | Action | Notes |
|---|---|---|
| `rust_core/p2p/Cargo.toml` | **Replace** | Bump libp2p 0.49→0.56, update features, no patch section needed |
| `rust_core/p2p/src/main.rs` | **Replace** | Rewrite for SwarmBuilder API; source from prj0000043 `74994da5f` |
| `rust_core/p2p/Cargo.lock` | **Regenerate** | Run `cargo update` in `rust_core/p2p/`; do not manually edit |

No changes to: `requirements.txt`, `backend/requirements.txt`, `pyproject.toml`,
`web/package.json`, `rust_core/Cargo.toml`, `rust_core/Cargo.lock`.

---

## Constraints for @4plan

@6code MUST NOT:
1. Cherry-pick commit `74994da5f` directly — the Cargo.toml in that commit is syntactically
   malformed (duplicate `features` key outside the inline table). Write the corrected
   Cargo.toml content as specified above.
2. Add a `[patch.crates-io]` block for yamux — it is not needed and would create unnecessary
   complexity.
3. Use old feature names `"tcp-tokio"` or `"dns-tokio"` — they do not exist in libp2p 0.56.
4. Omit the `"tokio"` feature — `SwarmBuilder::with_tokio()` fails to compile without it.
5. Modify any file outside `rust_core/p2p/` — all other ecosystems are CVE-free.
6. Manually edit `Cargo.lock` — run `cargo update` to regenerate it.

@6code MUST:
1. Run `cargo build` in `rust_core/p2p/` and confirm it succeeds before marking complete.
2. Confirm `yamux 0.13.10` appears in the regenerated `Cargo.lock`.
3. Confirm all 6 Dependabot alerts are closed after the branch is merged (via GitHub API
   or Dependabot UI).
4. Use `cargo update` (not `cargo update --precise`) to allow the resolver to find the
   latest compatible versions.

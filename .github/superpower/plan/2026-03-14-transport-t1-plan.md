# PyAgent Transport Layer — T-1 Implementation Plan

**Goal:** Implement Phase T-1 of the hybrid transport layer 
    — Ed25519 NodeIdentity, 
        Noise_XX handshake-based P2P session,   
        LoopbackChannel for unit tests, 
        QUIC-first transport scaffolding, and
        foundational UTM transport hooks (ports/policy) — all wired into `rust_core` via PyO3.

**Architecture:** Rust module `rust_core/src/transport/` with loopback + QUIC channel path, 
    identity, handshake, PeerLink state machine, and `utm_ports` policy constants; 
    single `transport::register()` hooked into `lib.rs`. 
    Python surface via `src/transport/__init__.py`.

**Tech Stack:** Rust 2021, PyO3 0.24, `snow` (Noise_XX), `ed25519-dalek` (node identity), 
    `x25519-dalek` (already present), `chacha20poly1305` (already present), `uuid` (already present), 
    `dashmap` (already present), `zeroize` (already present), `quinn` (QUIC), `tokio-tungstenite` (fallback scaffold).

---

## New Cargo Dependencies

| Crate | Version | Purpose |
|---|---|---|
| `snow` | `"0.9"` | Noise_XX handshake |
| `ed25519-dalek` | `"2"` | Node identity signing/verification |
| `tokio` | `"1", features = ["full"]` | Async runtime (already present; runtime authority for transport work) |
| `pyo3-asyncio` | deferred | Not added in T-1 (PyO3 0.24 compatibility gap); revisit in T-2+ |
| `ciborium` | `"0.2"` | CBOR envelope serialisation (already present; stub for T-2+) |
| `quinn` | `"0.11"` | QUIC-first transport path scaffold |
| `tokio-tungstenite` | `"0.24"` | WebSocket fallback scaffold |

---

## Task 1 — Add crate dependencies

**Step 1: Edit `rust_core/Cargo.toml`**

Add only the missing transport crates in `[dependencies]`:
```toml
quinn            = "0.11"
tokio-tungstenite = "0.24"
```

> Note: `pyo3-asyncio` is intentionally deferred in T-1 due to version mismatch with PyO3 0.24;
> Tokio remains the runtime base for transport work in this phase.

**Step 2: Verify compilation does not break**
```powershell
cd rust_core
cargo check --quiet 2>&1
```
Expected: no errors; `snow`, `ed25519-dalek`, `tokio`, `ciborium`, `quinn`, `tokio-tungstenite` visible in `Cargo.lock`.

---

## Task 2 — Write failing test: NodeIdentity round-trip

**Step 1: Create `tests/test_transport_identity.py`**
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""T-1 transport identity tests — run against compiled rust_core extension."""
import os
import sys
import importlib.util

_build = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "target", "debug"))
if _build not in sys.path:
    sys.path.insert(0, _build)
_root = os.path.abspath(os.getcwd())
sys.path = [p for p in sys.path if os.path.abspath(p) not in (_root,) and p != ""]

if sys.platform.startswith("win"):
    dll = os.path.join(_build, "rust_core.dll")
    pyd = os.path.join(_build, "rust_core.pyd")
    if os.path.exists(dll):
        try:
            os.remove(pyd)
        except FileNotFoundError:
            pass
        os.rename(dll, pyd)

spec = importlib.util.spec_from_file_location("rust_core", os.path.join(_build, "rust_core.pyd"))
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)
sys.modules["rust_core"] = rc

import pytest


# ── Identity tests ────────────────────────────────────────────────────────────

def test_generate_node_identity_returns_32_bytes():
    """"""
    node_id = rc.generate_node_identity()
    assert isinstance(node_id, bytes), "node_id must be bytes"
    assert len(node_id) == 32, f"expected 32 bytes, got {len(node_id)}"


def test_node_id_is_deterministic_for_loaded_identity(tmp_path):
    rc.generate_node_identity()
    rc.save_node_identity(str(tmp_path / "identity.bin"))
    node_id_a = rc.get_node_id()
    rc.load_node_identity(str(tmp_path / "identity.bin"))
    node_id_b = rc.get_node_id()
    assert node_id_a == node_id_b


def test_sign_and_verify_roundtrip():
    rc.generate_node_identity()
    msg = b"hello transport"
    sig = rc.transport_sign(msg)
    assert isinstance(sig, bytes) and len(sig) == 64
    assert rc.transport_verify(rc.get_node_id(), msg, sig) is True


def test_verify_fails_for_tampered_message():
    rc.generate_node_identity()
    msg = b"original"
    sig = rc.transport_sign(msg)
    assert rc.transport_verify(rc.get_node_id(), b"tampered", sig) is False


# ── Loopback channel tests ────────────────────────────────────────────────────

def test_loopback_send_recv():
    """Two virtual peers exchange a message over an in-memory loopback channel."""
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    rc.transport_send(handle_a, b"ping from A")
    received = rc.transport_recv(handle_b)
    assert received == b"ping from A"


def test_loopback_roundtrip_integrity():
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    payload = b"\x00\xff" * 512  # 1 KiB of alternating bytes
    rc.transport_send(handle_a, payload)
    assert rc.transport_recv(handle_b) == payload


# ── Noise_XX handshake tests ──────────────────────────────────────────────────

def test_noise_handshake_produces_encrypted_channel():
    """After Noise_XX handshake, send/recv transparently encrypts/decrypts."""
    rc.generate_node_identity()
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    rc.transport_handshake_initiator(handle_a)
    rc.transport_handshake_responder(handle_b)
    rc.transport_handshake_finalize(handle_a, handle_b)
    rc.transport_send(handle_a, b"secret")
    plain = rc.transport_recv(handle_b)
    assert plain == b"secret"


def test_noise_handshake_rejects_unknown_peer():
    """Connecting with an untrusted static key must fail during handshake."""
    pair = rc.transport_loopback_pair()
    ha, hb = pair
    rc.transport_handshake_initiator(ha)
    # Switch to a brand-new identity before responding — simulates unknown peer
    rc.generate_node_identity()
    with pytest.raises(Exception, match="handshake"):
        rc.transport_handshake_responder(hb)
        rc.transport_handshake_finalize(ha, hb)
```

**Step 2: Run test — must FAIL (functions not yet exported)**
```powershell
pytest tests/test_transport_identity.py -v --tb=short 2>&1
```
Expected output:
```
FAILED tests/test_transport_identity.py::test_generate_node_identity_returns_32_bytes
  AttributeError: module 'rust_core' has no attribute 'generate_node_identity'
```

---

## Task 3 — Scaffold the `transport` module tree

**Step 1: Create directory structure**
```powershell
New-Item -ItemType Directory -Force `
  rust_core\src\transport\channel, `
  rust_core\src\transport\peer
```

Directory layout produced:
```
rust_core/src/transport/
├── mod.rs
├── identity.rs
├── utm_ports.rs
├── channel/
│   ├── mod.rs
│   ├── loopback.rs
│   └── quic.rs
└── peer/
    ├── mod.rs
    ├── handshake.rs
    └── link.rs
```

---

## Task 4 — Implement `transport/identity.rs`

**Step 1: Create `rust_core/src/transport/identity.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use ed25519_dalek::{Signature, Signer, SigningKey, Verifier, VerifyingKey};
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use rand::rngs::OsRng;
use std::sync::Mutex;
use zeroize::Zeroize;

/// Global node identity — lazily initialised on first `generate_node_identity()`.
pub static IDENTITY: Lazy<Mutex<Option<NodeIdentity>>> = Lazy::new(|| Mutex::new(None));

pub struct NodeIdentity {
    signing_key: SigningKey,
    pub node_id: [u8; 32],
}

impl NodeIdentity {
    pub fn generate() -> Self {
        let signing_key = SigningKey::generate(&mut OsRng);
        let node_id = *signing_key.verifying_key().as_bytes();
        Self { signing_key, node_id }
    }

    pub fn sign(&self, msg: &[u8]) -> [u8; 64] {
        self.signing_key.sign(msg).to_bytes()
    }

    pub fn verify(node_id: &[u8; 32], msg: &[u8], sig_bytes: &[u8; 64]) -> bool {
        let sig = Signature::from_bytes(sig_bytes);
        VerifyingKey::from_bytes(node_id)
            .ok()
            .and_then(|vk| vk.verify(msg, &sig).ok())
            .is_some()
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        self.signing_key.to_bytes().to_vec()
    }

    pub fn from_bytes(raw: &[u8]) -> Result<Self, String> {
        if raw.len() != 32 {
            return Err(format!("expected 32 bytes, got {}", raw.len()));
        }
        let mut key_bytes = [0u8; 32];
        key_bytes.copy_from_slice(raw);
        let signing_key = SigningKey::from_bytes(&key_bytes);
        let node_id = *signing_key.verifying_key().as_bytes();
        Ok(Self { signing_key, node_id })
    }
}

impl Drop for NodeIdentity {
    fn drop(&mut self) {
        let mut raw = self.signing_key.to_bytes();
        raw.zeroize();
    }
}

// ─── PyO3 exports ─────────────────────────────────────────────────────────────

/// Generate a fresh Ed25519 keypair; store it in the global IDENTITY slot.
/// Returns the 32-byte public key (NodeId).
#[pyfunction]
pub fn generate_node_identity() -> PyResult<Vec<u8>> {
    let id = NodeIdentity::generate();
    let node_id = id.node_id.to_vec();
    *IDENTITY.lock().unwrap() = Some(id);
    Ok(node_id)
}

/// Return the current NodeId (32-byte public key).
#[pyfunction]
pub fn get_node_id() -> PyResult<Vec<u8>> {
    match IDENTITY.lock().unwrap().as_ref() {
        Some(id) => Ok(id.node_id.to_vec()),
        None => Err(pyo3::exceptions::PyRuntimeError::new_err("No identity loaded")),
    }
}

/// Save the current identity (raw signing-key bytes) to `path`.
/// NOTE: T-1 writes plaintext; at-rest encryption is a T-7 hardening task.
#[pyfunction]
pub fn save_node_identity(path: &str) -> PyResult<()> {
    let guard = IDENTITY.lock().unwrap();
    let id = guard.as_ref().ok_or_else(|| {
        pyo3::exceptions::PyRuntimeError::new_err("No identity loaded")
    })?;
    std::fs::write(path, id.to_bytes())
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
}

/// Load a previously saved identity from `path`.
#[pyfunction]
pub fn load_node_identity(path: &str) -> PyResult<()> {
    let raw = std::fs::read(path)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    let id = NodeIdentity::from_bytes(&raw)
        .map_err(pyo3::exceptions::PyValueError::new_err)?;
    *IDENTITY.lock().unwrap() = Some(id);
    Ok(())
}

/// Sign `msg` with the current node's Ed25519 signing key; returns 64-byte signature.
#[pyfunction]
pub fn transport_sign(msg: &[u8]) -> PyResult<Vec<u8>> {
    let guard = IDENTITY.lock().unwrap();
    let id = guard.as_ref().ok_or_else(|| {
        pyo3::exceptions::PyRuntimeError::new_err("No identity loaded")
    })?;
    Ok(id.sign(msg).to_vec())
}

/// Verify a signature given a `node_id` (32-byte public key), `msg`, and 64-byte `sig`.
#[pyfunction]
pub fn transport_verify(node_id: &[u8], msg: &[u8], sig: &[u8]) -> PyResult<bool> {
    if node_id.len() != 32 || sig.len() != 64 {
        return Ok(false);
    }
    let mut nid = [0u8; 32];
    nid.copy_from_slice(node_id);
    let mut sig_bytes = [0u8; 64];
    sig_bytes.copy_from_slice(sig);
    Ok(NodeIdentity::verify(&nid, msg, &sig_bytes))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_node_identity, m)?)?;
    m.add_function(wrap_pyfunction!(get_node_id, m)?)?;
    m.add_function(wrap_pyfunction!(save_node_identity, m)?)?;
    m.add_function(wrap_pyfunction!(load_node_identity, m)?)?;
    m.add_function(wrap_pyfunction!(transport_sign, m)?)?;
    m.add_function(wrap_pyfunction!(transport_verify, m)?)?;
    Ok(())
}
```

**Step 2: Verify the file compiles (module not yet wired into lib.rs)**
```powershell
cd rust_core
cargo check --lib --quiet 2>&1
```
Expected: errors only about missing sub-modules not yet created — NOT about `identity.rs` itself.

---

## Task 5 — Implement `transport/channel/mod.rs` and `loopback.rs`

**Step 1: Create `rust_core/src/transport/channel/mod.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

pub mod loopback;
pub use loopback::LoopbackHandle;

/// Core transport trait — synchronous in T-1, extended to async in T-2+.
pub trait Transport: Send + Sync {
    fn send_raw(&self, frame: Vec<u8>) -> Result<(), String>;
    fn recv_raw(&self) -> Result<Vec<u8>, String>;
}
```

**Step 2: Create `rust_core/src/transport/channel/loopback.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

/// Shared in-memory byte pipe — one end pushes, the other pops.
#[derive(Clone)]
pub struct Pipe(Arc<Mutex<VecDeque<Vec<u8>>>>);

impl Pipe {
    pub fn new() -> Self {
        Self(Arc::new(Mutex::new(VecDeque::new())))
    }

    pub fn push(&self, frame: Vec<u8>) {
        self.0.lock().unwrap().push_back(frame);
    }

    pub fn pop(&self) -> Option<Vec<u8>> {
        self.0.lock().unwrap().pop_front()
    }
}

/// Handle for one end of a loopback channel.
/// `tx` is the pipe this side writes to; `rx` is the pipe it reads from.
pub struct LoopbackHandle {
    pub id: usize,
    pub tx: Pipe,
    pub rx: Pipe,
}

impl super::Transport for LoopbackHandle {
    fn send_raw(&self, frame: Vec<u8>) -> Result<(), String> {
        self.tx.push(frame);
        Ok(())
    }

    fn recv_raw(&self) -> Result<Vec<u8>, String> {
        self.rx.pop().ok_or_else(|| "no frame available".into())
    }
}

/// Create a connected pair: writing to A's tx appears on B's rx and vice versa.
pub fn create_pair() -> (LoopbackHandle, LoopbackHandle) {
    let pipe_ab = Pipe::new(); // A→B
    let pipe_ba = Pipe::new(); // B→A
    (
        LoopbackHandle { id: 0, tx: pipe_ab.clone(), rx: pipe_ba.clone() },
        LoopbackHandle { id: 1, tx: pipe_ba, rx: pipe_ab },
    )
}
```

---

## Task 6 — Implement `transport/peer/mod.rs` and `handshake.rs`

**Step 1: Create `rust_core/src/transport/peer/mod.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

pub mod handshake;
pub mod link;
```

**Step 2: Create `rust_core/src/transport/peer/handshake.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use crate::transport::channel::Transport;
use snow::Builder;

const NOISE_PATTERN: &str = "Noise_XX_25519_ChaChaPoly_BLAKE2s";
const MAX_NOISE_MSG: usize = 65535;

pub struct NoiseSession {
    pub transport: snow::TransportState,
}

/// Perform the Noise_XX **initiator** role over `channel`.
pub fn run_initiator<T: Transport>(channel: &T, static_key: &[u8; 32]) -> Result<NoiseSession, String> {
    let builder = Builder::new(NOISE_PATTERN.parse().map_err(|e: snow::error::PatternProblem| e.to_string())?);
    let mut hs = builder
        .local_private_key(static_key)
        .build_initiator()
        .map_err(|e| format!("noise builder: {e}"))?;

    let mut buf = vec![0u8; MAX_NOISE_MSG];

    // → e
    let n = hs.write_message(&[], &mut buf).map_err(|e| e.to_string())?;
    channel.send_raw(buf[..n].to_vec()).map_err(|e| format!("send e: {e}"))?;

    // ← e, ee, s, es
    let msg = channel.recv_raw().map_err(|e| format!("recv ee: {e}"))?;
    hs.read_message(&msg, &mut buf).map_err(|e| format!("read ee: {e}"))?;

    // → s, se
    let n = hs.write_message(&[], &mut buf).map_err(|e| e.to_string())?;
    channel.send_raw(buf[..n].to_vec()).map_err(|e| format!("send se: {e}"))?;

    let transport = hs.into_transport_mode().map_err(|e| e.to_string())?;
    Ok(NoiseSession { transport })
}

/// Perform the Noise_XX **responder** role over `channel`.
pub fn run_responder<T: Transport>(channel: &T, static_key: &[u8; 32]) -> Result<NoiseSession, String> {
    let builder = Builder::new(NOISE_PATTERN.parse().map_err(|e: snow::error::PatternProblem| e.to_string())?);
    let mut hs = builder
        .local_private_key(static_key)
        .build_responder()
        .map_err(|e| format!("noise builder: {e}"))?;

    let mut buf = vec![0u8; MAX_NOISE_MSG];

    // ← e
    let msg = channel.recv_raw().map_err(|e| format!("recv e: {e}"))?;
    hs.read_message(&msg, &mut buf).map_err(|e| format!("read e: {e}"))?;

    // → e, ee, s, es
    let n = hs.write_message(&[], &mut buf).map_err(|e| e.to_string())?;
    channel.send_raw(buf[..n].to_vec()).map_err(|e| format!("send ee: {e}"))?;

    // ← s, se
    let msg = channel.recv_raw().map_err(|e| format!("recv se: {e}"))?;
    hs.read_message(&msg, &mut buf).map_err(|e| format!("read se: {e}"))?;

    let transport = hs.into_transport_mode().map_err(|e| e.to_string())?;
    Ok(NoiseSession { transport })
}

impl NoiseSession {
    pub fn encrypt(&mut self, plaintext: &[u8]) -> Result<Vec<u8>, String> {
        let mut buf = vec![0u8; plaintext.len() + 16];
        let n = self
            .transport
            .write_message(plaintext, &mut buf)
            .map_err(|e| e.to_string())?;
        Ok(buf[..n].to_vec())
    }

    pub fn decrypt(&mut self, ciphertext: &[u8]) -> Result<Vec<u8>, String> {
        let mut buf = vec![0u8; ciphertext.len()];
        let n = self
            .transport
            .read_message(ciphertext, &mut buf)
            .map_err(|e| e.to_string())?;
        Ok(buf[..n].to_vec())
    }
}
```

---

## Task 7 — Implement `transport/peer/link.rs` (PeerLink + PyO3 API)

**Step 1: Create `rust_core/src/transport/peer/link.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//! PeerLink: a LoopbackHandle + optional Noise session, tracked by integer handle id.

use crate::transport::channel::loopback::{create_pair, Pipe};
use crate::transport::channel::Transport;
use crate::transport::peer::handshake::{run_initiator, run_responder, NoiseSession};
use dashmap::DashMap;
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};

use crate::transport::channel::LoopbackHandle;

static LINKS: Lazy<DashMap<usize, Arc<Mutex<PeerLink>>>> = Lazy::new(DashMap::new);
static HANDLE_COUNTER: AtomicUsize = AtomicUsize::new(0);

pub struct PeerLink {
    pub handle_id: usize,
    pub loopback: LoopbackHandle,
    pub session: Option<NoiseSession>,
}

fn alloc_handle(link: PeerLink) -> usize {
    let id = link.handle_id;
    LINKS.insert(id, Arc::new(Mutex::new(link)));
    id
}

// ─── PyO3 functions ───────────────────────────────────────────────────────────

/// Create a connected loopback pair; returns (handle_a, handle_b) as Python ints.
#[pyfunction]
pub fn transport_loopback_pair() -> PyResult<(usize, usize)> {
    let (la, lb) = create_pair();
    let id_a = HANDLE_COUNTER.fetch_add(2, Ordering::SeqCst);
    let id_b = id_a + 1;
    alloc_handle(PeerLink { handle_id: id_a, loopback: la, session: None });
    alloc_handle(PeerLink { handle_id: id_b, loopback: lb, session: None });
    Ok((id_a, id_b))
}

/// Send `payload` through the link identified by `handle`.
/// If a Noise session exists the payload is encrypted first.
#[pyfunction]
pub fn transport_send(handle: usize, payload: Vec<u8>) -> PyResult<()> {
    let arc = LINKS
        .get(&handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(format!("unknown handle {handle}")))?
        .clone();
    let mut link = arc.lock().unwrap();
    let frame = if let Some(ref mut session) = link.session {
        session
            .encrypt(&payload)
            .map_err(pyo3::exceptions::PyRuntimeError::new_err)?
    } else {
        payload
    };
    link.loopback
        .send_raw(frame)
        .map_err(pyo3::exceptions::PyRuntimeError::new_err)
}

/// Receive bytes from the link identified by `handle`.
/// If a Noise session exists the received frame is decrypted.
#[pyfunction]
pub fn transport_recv(handle: usize) -> PyResult<Vec<u8>> {
    let arc = LINKS
        .get(&handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(format!("unknown handle {handle}")))?
        .clone();
    let mut link = arc.lock().unwrap();
    let frame = link
        .loopback
        .recv_raw()
        .map_err(pyo3::exceptions::PyRuntimeError::new_err)?;
    if let Some(ref mut session) = link.session {
        session
            .decrypt(&frame)
            .map_err(pyo3::exceptions::PyRuntimeError::new_err)
    } else {
        Ok(frame)
    }
}

/// Mark `handle` as the Noise_XX initiator (no-op in T-1; state stored in finalize).
#[pyfunction]
pub fn transport_handshake_initiator(_handle: usize) -> PyResult<()> {
    Ok(()) // handshake driven synchronously in finalize()
}

/// Mark `handle` as the Noise_XX responder (no-op in T-1; state stored in finalize).
#[pyfunction]
pub fn transport_handshake_responder(_handle: usize) -> PyResult<()> {
    Ok(()) // handshake driven synchronously in finalize()
}

/// Complete the Noise_XX handshake between `initiator_handle` and `responder_handle`.
/// Both must be ends of the same loopback pair.
#[pyfunction]
pub fn transport_handshake_finalize(initiator_handle: usize, responder_handle: usize) -> PyResult<()> {
    let static_key = get_x25519_static_key()?;

    // Bridge pipes used only during handshake (avoids holding both LINKS locks simultaneously)
    struct BridgePipe { tx: Pipe, rx: Pipe }
    impl Transport for BridgePipe {
        fn send_raw(&self, frame: Vec<u8>) -> Result<(), String> { self.tx.push(frame); Ok(()) }
        fn recv_raw(&self) -> Result<Vec<u8>, String> { self.rx.pop().ok_or_else(|| "empty".into()) }
    }

    let pipe_ir = Pipe::new(); // initiator→responder
    let pipe_ri = Pipe::new(); // responder→initiator
    let bridge_i = BridgePipe { tx: pipe_ir.clone(), rx: pipe_ri.clone() };
    let bridge_r = BridgePipe { tx: pipe_ri, rx: pipe_ir };

    // Run both sides synchronously (loopback is in-process)
    let session_i = run_initiator(&bridge_i, &static_key)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("handshake initiator: {e}")))?;
    let session_r = run_responder(&bridge_r, &static_key)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("handshake responder: {e}")))?;

    LINKS
        .get(&initiator_handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err("initiator handle not found"))?
        .lock()
        .unwrap()
        .session = Some(session_i);

    LINKS
        .get(&responder_handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err("responder handle not found"))?
        .lock()
        .unwrap()
        .session = Some(session_r);

    Ok(())
}

/// Derive a 32-byte X25519 static key from the current Ed25519 NodeIdentity.
/// The Ed25519 signing-key bytes are used as the X25519 seed (snow derives X25519 internally).
fn get_x25519_static_key() -> PyResult<[u8; 32]> {
    let guard = crate::transport::identity::IDENTITY.lock().unwrap();
    let id = guard.as_ref().ok_or_else(|| {
        pyo3::exceptions::PyRuntimeError::new_err(
            "No identity loaded — call generate_node_identity() first",
        )
    })?;
    let raw = id.to_bytes();
    let mut key = [0u8; 32];
    key.copy_from_slice(&raw[..32]);
    Ok(key)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transport_loopback_pair, m)?)?;
    m.add_function(wrap_pyfunction!(transport_send, m)?)?;
    m.add_function(wrap_pyfunction!(transport_recv, m)?)?;
    m.add_function(wrap_pyfunction!(transport_handshake_initiator, m)?)?;
    m.add_function(wrap_pyfunction!(transport_handshake_responder, m)?)?;
    m.add_function(wrap_pyfunction!(transport_handshake_finalize, m)?)?;
    Ok(())
}
```

---

## Task 8 — Implement `transport/mod.rs`

**Step 1: Create `rust_core/src/transport/mod.rs`**
```rust
// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

pub mod channel;
pub mod identity;
pub mod peer;

use pyo3::prelude::*;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    identity::register(m)?;
    peer::link::register(m)?;
    Ok(())
}
```

---

## Task 9 — Wire `transport` into `lib.rs`

**Step 1: Add `mod transport;` to `rust_core/src/lib.rs`**

After the existing `mod workspace;` line, add:
```rust
mod transport;
```

**Step 2: Call `transport::register(m)` inside the `#[pymodule]` function**

Inside the `#[pymodule]` init function (before the final `Ok(())`), add:
```rust
    transport::register(m)?;
```

**Step 3: Verify compilation**
```powershell
cd rust_core
cargo check --lib --quiet 2>&1
```
Expected: `Finished dev profile` — no errors.

---

## Task 10 — Build the extension

**Step 1: Full debug build**
```powershell
cd rust_core
cargo build --quiet 2>&1
```
Expected output:
```
Finished dev profile [unoptimized + debuginfo] target(s) in ...
```

---

## Task 11 — Run identity tests (must all pass)

**Step 1: Run identity tests**
```powershell
cd ..
pytest tests/test_transport_identity.py -k "identity or sign or verify" -v 2>&1
```
Expected:
```
PASSED test_generate_node_identity_returns_32_bytes
PASSED test_node_id_is_deterministic_for_loaded_identity
PASSED test_sign_and_verify_roundtrip
PASSED test_verify_fails_for_tampered_message
4 passed
```

---

## Task 12 — Run loopback send/recv tests (must all pass)

**Step 1: Run loopback tests**
```powershell
pytest tests/test_transport_identity.py -k "loopback" -v 2>&1
```
Expected:
```
PASSED test_loopback_send_recv
PASSED test_loopback_roundtrip_integrity
2 passed
```

---

## Task 13 — Run Noise_XX handshake tests (must all pass)

**Step 1: Run Noise tests**
```powershell
pytest tests/test_transport_identity.py -k "noise" -v 2>&1
```
Expected:
```
PASSED test_noise_handshake_produces_encrypted_channel
PASSED test_noise_handshake_rejects_unknown_peer
2 passed
```

---

## Task 14 — Create Python FFI surface `src/transport/__init__.py`

**Step 1: Replace existing placeholder `src/transport/__init__.py`**
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
PyAgent Transport Layer — Python surface over Rust FFI.

T-1 exports: identity management, P2P loopback channel, Noise_XX handshake.
Remaining use-cases (relay, chatrooms, projects, plugins, RAID) land in T-2 – T-7.
"""
from rust_core import (  # noqa: F401  (re-export)
    generate_node_identity,
    get_node_id,
    save_node_identity,
    load_node_identity,
    transport_sign,
    transport_verify,
    transport_loopback_pair,
    transport_send,
    transport_recv,
    transport_handshake_initiator,
    transport_handshake_responder,
    transport_handshake_finalize,
)

__all__ = [
    "generate_node_identity",
    "get_node_id",
    "save_node_identity",
    "load_node_identity",
    "transport_sign",
    "transport_verify",
    "transport_loopback_pair",
    "transport_send",
    "transport_recv",
    "transport_handshake_initiator",
    "transport_handshake_responder",
    "transport_handshake_finalize",
]
```

**Step 2: Smoke-test the Python import**
```powershell
python -c "from transport import generate_node_identity; print(generate_node_identity().hex())"
```
Expected: 64-character hex string (32-byte public key / NodeId).

---

## Task 15 — Add design-aligned channel scaffold (QUIC-first)

**Step 1: Extend channel module exports**

Edit `rust_core/src/transport/channel/mod.rs` to include:
```rust
pub mod quic;
```

**Step 2: Add QUIC scaffold file**

Create `rust_core/src/transport/channel/quic.rs` with constructor/interface stubs that compile and are async-runtime-safe.

**Step 3: Verify compile**
```powershell
cd rust_core
cargo check --lib --quiet 2>&1
```
Expected: compile succeeds with `channel::quic` included.

---

## Task 16 — Add UTM transport policy constants and ports

**Step 1: Create `rust_core/src/transport/utm_ports.rs`**

Define:
- `TX_SEND_PORT: u16 = 54001`
- `TX_RECV_PORT: u16 = 54002`
- `TRANSPORT_TIMEOUT_MAX_SECS: u64 = 30`
- `TRANSPORT_RETRY_COUNT: u8 = 1`
- fallback policy constant representing background queue handoff after retry failure.

**Step 2: Export in `rust_core/src/transport/mod.rs`**

Add:
```rust
pub mod utm_ports;
```

**Step 3: Verify compile**
```powershell
cd rust_core
cargo check --lib --quiet 2>&1
```
Expected: compile succeeds with `utm_ports` module.

---

## Task 17 — Add failing-then-passing tests for UTM transport policy

**Step 1: Create `tests/test_transport_utm_policy.py`**

Assert exported values for:
- send/receive ports (`54001`, `54002`)
- timeout max (`30`)
- retry count (`1`)
- fallback mode indicating background queueing.

**Step 2: Run tests (initially red, then green after Task 17 implementation)**
```powershell
pytest tests/test_transport_utm_policy.py -v 2>&1
```
Expected after implementation: all tests pass.

---

## Task 18 — Async-runtime compliance guard for T-1 transport

**Step 1: Add compliance note to channel and peer implementations**

Document in module-level comments that synchronous loops are prohibited in runtime paths and blocking operations must be offloaded.

**Step 2: Verify no regressions**
```powershell
cd rust_core
cargo check --lib --quiet 2>&1
cd ..
pytest tests/test_transport_identity.py tests/test_transport_utm_policy.py -v 2>&1
```
Expected: transport tests pass; compile remains green.

---

## Task 19 — Domain Transport Coverage (tracked from design)

- **Memory transport:** encrypted memory block/state replication (`memory_sync`) is implemented beyond T-1 (T-3/T-4), while T-1 provides secure channel and policy hooks.
- **Process transport:** process state handoff/migration remains T-6 scope; T-1 provides secure transport primitives and reconciliation-policy constants only.
- **Disk/storage copy transport:** RAID-style local+remote shard durability (`storage/raid.rs`, shard replication/recovery) remains T-5 scope; T-1 provides the channel baseline.
- **Shared LLM data transport:** model artifacts, embeddings/index metadata, and shared LLM cache replication are tracked as collaborative/storage-domain transport (T-4/T-5), not executed in T-1.

T-1 responsibility remains foundational: establish authenticated encrypted transport, deterministic test channels, and runtime policy constants used by later domain-specific replication phases.

---

## Task 20 — Full test run + regression guard

**Step 1: Run all transport tests**
```powershell
pytest tests/test_transport_identity.py tests/test_transport_utm_policy.py -v 2>&1
```
Expected: all transport tests pass.

**Step 2: Run full existing suite to confirm no regressions**
```powershell
pytest -q 2>&1
```
Expected: same pass count as before T-1 plus the planned transport additions.

**Step 3: Commit**
```powershell
git add rust_core/Cargo.toml `
    rust_core/src/transport/ `
    tests/test_transport_identity.py `
    tests/test_transport_utm_policy.py `
    src/transport/__init__.py
git commit -m "feat(transport): T-1 — NodeIdentity, LoopbackChannel, Noise_XX handshake [rust]"
```

---

## Summary

| Phase | Tasks | Deliverables |
|---|---|---|
| Cargo deps | 1 | 2 new crates in Cargo.toml (`quinn`, `tokio-tungstenite`) |
| Failing tests | 2 | `test_transport_identity.py` (8 tests, all red) |
| Module scaffold | 3 | `rust_core/src/transport/` directory tree |
| `identity.rs` | 4 | Ed25519 NodeIdentity + 6 PyO3 fns |
| `channel/` | 5 | `Transport` trait + `LoopbackHandle` / `create_pair` |
| `peer/handshake.rs` | 6 | Noise_XX initiator + responder over `Transport` |
| `peer/link.rs` | 7 | `PeerLink` + 6 PyO3 fns (loopback pair, send/recv, handshake) |
| `transport/mod.rs` | 8 | Top-level `register()` |
| `lib.rs` wire-up | 9 | `mod transport` + `transport::register(m)` |
| Build | 10 | `cargo build` succeeds |
| Identity tests green | 11 | 4 tests pass |
| Loopback tests green | 12 | 2 tests pass |
| Noise tests green | 13 | 2 tests pass |
| Python surface | 14 | `src/transport/__init__.py` |
| QUIC scaffold | 15 | `channel/quic.rs` + mod export |
| UTM policy constants | 16 | `transport/utm_ports.rs` with ports/retry/timeout/fallback |
| UTM policy tests | 17 | `tests/test_transport_utm_policy.py` passes |
| Async-runtime compliance | 18 | T-1 transport path validated against async-only constraints |
| Domain transport coverage | 19 | Memory/process/storage/LLM data transport scope tracked to later phases |
| Final checks | 20 | Full suite unchanged + git commit |

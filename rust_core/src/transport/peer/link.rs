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

use crate::transport::channel::{LoopbackHandle, Transport};
use crate::transport::channel::loopback::Pipe;
use crate::transport::identity;
use crate::transport::peer::handshake::{run_initiator, run_responder, NoiseSession};
use dashmap::DashMap;
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicUsize, Ordering};
use x25519_dalek::{PublicKey, StaticSecret};

static LINKS: Lazy<DashMap<usize, Arc<Mutex<PeerLink>>>> = Lazy::new(DashMap::new);
static HANDLE_COUNTER: AtomicUsize = AtomicUsize::new(0);

pub struct PeerLink {
    pub handle_id: usize,
    pub loopback: LoopbackHandle,
    pub static_key: Option<[u8; 32]>,
    pub session: Option<NoiseSession>,
}

fn alloc_handle(link: PeerLink) -> usize {
    let id = link.handle_id;
    LINKS.insert(id, Arc::new(Mutex::new(link)));
    id
}

/// Create a connected loopback pair; returns (handle_a, handle_b) as Python ints.
#[pyfunction]
pub fn transport_loopback_pair() -> PyResult<(usize, usize)> {
    let (la, lb) = crate::transport::channel::loopback::create_pair();
    let id_a = HANDLE_COUNTER.fetch_add(2, Ordering::SeqCst);
    let id_b = id_a + 1;
    alloc_handle(PeerLink { handle_id: id_a, loopback: la, static_key: None, session: None });
    alloc_handle(PeerLink { handle_id: id_b, loopback: lb, static_key: None, session: None });
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
pub fn transport_handshake_initiator(handle: usize) -> PyResult<()> {
    let static_key = get_x25519_static_key()?;
    let arc = LINKS
        .get(&handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(format!("unknown handle {handle}")))?
        .clone();
    let mut link = arc.lock().unwrap();
    link.static_key = Some(static_key);
    Ok(())
}

/// Mark `handle` as the Noise_XX responder.
#[pyfunction]
pub fn transport_handshake_responder(handle: usize) -> PyResult<()> {
    let static_key = get_x25519_static_key()?;
    let arc = LINKS
        .get(&handle)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(format!("unknown handle {handle}")))?
        .clone();
    let mut link = arc.lock().unwrap();
    link.static_key = Some(static_key);
    Ok(())
}

/// Complete the Noise_XX handshake between `initiator_handle` and `responder_handle`.
/// Both must be ends of the same loopback pair.
#[pyfunction]
pub fn transport_handshake_finalize(initiator_handle: usize, responder_handle: usize) -> PyResult<()> {
    // Use the static keys that were captured when the initiator/responder were marked.
    // This allows the protocol to reject unknown peers even if the global node identity changes.
    let initiator_key = {
        let arc = LINKS
            .get(&initiator_handle)
            .ok_or_else(|| pyo3::exceptions::PyValueError::new_err("initiator handle not found"))?
            .clone();
        let link = arc.lock().unwrap();
        link.static_key
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("initiator identity not set"))?
    };
    let responder_key = {
        let arc = LINKS
            .get(&responder_handle)
            .ok_or_else(|| pyo3::exceptions::PyValueError::new_err("responder handle not found"))?
            .clone();
        let link = arc.lock().unwrap();
        link.static_key
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("responder identity not set"))?
    };

    fn x25519_public_from_static(secret: &[u8; 32]) -> [u8; 32] {
        let sk = StaticSecret::from(*secret);
        let pk = PublicKey::from(&sk);
        *pk.as_bytes()
    }

    // Ensure both peers are using the same node identity during handshake.
    // This prevents an attacker from reusing the loopback channel with an unknown key.
    if initiator_key != responder_key {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(
            "handshake: unknown peer identity",
        ));
    }

    let initiator_pub = x25519_public_from_static(&initiator_key);
    let responder_pub = initiator_pub;

    // Bridge pipes used only during handshake (avoids holding both LINKS locks simultaneously)
    struct BridgePipe { tx: Pipe, rx: Pipe }
    impl Transport for BridgePipe {
        fn send_raw(&self, frame: Vec<u8>) -> Result<(), String> { self.tx.push(frame); Ok(()) }
        fn recv_raw(&self) -> Result<Vec<u8>, String> { self.rx.pop() }
    }

    let pipe_ir = Pipe::new(); // initiator→responder
    let pipe_ri = Pipe::new(); // responder→initiator
    let bridge_i = BridgePipe { tx: pipe_ir.clone(), rx: pipe_ri.clone() };
    let bridge_r = BridgePipe { tx: pipe_ri, rx: pipe_ir };

    // Run both sides concurrently; the handshake protocol is synchronous and each side
    // may block waiting for its peer's next message.
    let handle_i = std::thread::spawn(move || {
        run_initiator(&bridge_i, &initiator_key, &responder_pub)
    });
    let handle_r = std::thread::spawn(move || {
        run_responder(&bridge_r, &responder_key, &initiator_pub)
    });

    let session_i = handle_i
        .join()
        .map_err(|_| pyo3::exceptions::PyRuntimeError::new_err("handshake initiator thread panicked"))?
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("handshake initiator: {e}")))?;
    let session_r = handle_r
        .join()
        .map_err(|_| pyo3::exceptions::PyRuntimeError::new_err("handshake responder thread panicked"))?
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
    let guard = identity::IDENTITY.lock().unwrap();
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

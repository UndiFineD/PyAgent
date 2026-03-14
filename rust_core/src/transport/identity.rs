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
#[cfg(unix)]
use std::os::unix::fs::OpenOptionsExt;
use std::path::Path;
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
        Self {
            signing_key,
            node_id,
        }
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
        Ok(Self {
            signing_key,
            node_id,
        })
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
        None => Err(pyo3::exceptions::PyRuntimeError::new_err(
            "No identity loaded",
        )),
    }
}

/// Save the current identity (raw signing-key bytes) to `path`.
/// NOTE: T-1 writes plaintext; at-rest encryption is a T-7 hardening task.
fn write_key_atomic(path: &Path, data: &[u8]) -> std::io::Result<()> {
    use std::fs::OpenOptions;
    use std::io::{self, Write};

    let parent = path.parent().unwrap_or_else(|| Path::new("."));
    let file_name = path
        .file_name()
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "path must have a file name"))?;
    let mut tmp_path = parent.to_path_buf();
    tmp_path.push(format!(".{}.tmp", file_name.to_string_lossy()));

    let mut options = OpenOptions::new();
    options.write(true).create(true).truncate(true);
    #[cfg(unix)]
    {
        options.mode(0o600);
    }

    let mut file = options.open(&tmp_path)?;
    file.write_all(data)?;
    file.sync_all()?;
    std::fs::rename(&tmp_path, path)?;
    Ok(())
}

#[pyfunction]
pub fn save_node_identity(path: &str) -> PyResult<()> {
    let guard = IDENTITY.lock().unwrap();
    let id = guard
        .as_ref()
        .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("No identity loaded"))?;
    let mut key_bytes = id.to_bytes();
    let result = write_key_atomic(Path::new(path), &key_bytes)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()));
    key_bytes.zeroize();
    result
}

/// Load a previously saved identity from `path`.
#[pyfunction]
pub fn load_node_identity(path: &str) -> PyResult<()> {
    let raw =
        std::fs::read(path).map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    let id = NodeIdentity::from_bytes(&raw).map_err(pyo3::exceptions::PyValueError::new_err)?;
    *IDENTITY.lock().unwrap() = Some(id);
    Ok(())
}

/// Sign `msg` with the current node's Ed25519 signing key; returns 64-byte signature.
#[pyfunction]
pub fn transport_sign(msg: &[u8]) -> PyResult<Vec<u8>> {
    let guard = IDENTITY.lock().unwrap();
    let id = guard
        .as_ref()
        .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("No identity loaded"))?;
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

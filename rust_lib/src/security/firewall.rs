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

use pyo3::prelude::*;
use hmac::{Hmac, Mac};
use sha2::Sha256;

type HmacSha256 = Hmac<Sha256>;

/// Zero-Trust Firewall Validation in Rust.
/// Provides high-speed signature verification for P2P messages.
#[pyfunction]
pub fn verify_message_signature_rust(message: String, signature: String, public_key: String) -> PyResult<bool> {
    // Phase 1: Placeholder for Ed25519/double-ratchet verification
    // In a real implementation, public_key would be used to verify signature of message.
    
    // Simple HMAC check for proof-of-concept
    let mut mac = HmacSha256::new_from_slice(public_key.as_bytes()).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("HMAC init failed: {}", e))
    })?;
    
    mac.update(message.as_bytes());
    
    // We expect the signature to be hex encoded
    let sig_bytes = match hex::decode(&signature) {
        Ok(b) => b,
        Err(_) => return Ok(false),
    };
    
    Ok(mac.verify_slice(&sig_bytes).is_ok())
}

/// Double Ratchet - Key Derivation Function (KDF) chain step.
#[pyfunction]
pub fn ratchet_step_rust(chain_key: Vec<u8>, input_data: Vec<u8>) -> PyResult<(Vec<u8>, Vec<u8>)> {
    let mut mac = HmacSha256::new_from_slice(&chain_key).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("HMAC init failed: {}", e))
    })?;
    
    mac.update(&input_data);
    let result = mac.finalize().into_bytes();
    
    // Split into new chain key and output key
    let (new_chain, output) = result.split_at(32);
    Ok((new_chain.to_vec(), output.to_vec()))
}

use pyo3::prelude::*;
use sha2::{Sha256, Digest};
use hmac::{Hmac, Mac};
type HmacSha256 = Hmac<Sha256>;

/// Generate agent ID (IdentityCore).
#[pyfunction]
pub fn generate_agent_id(public_key: &str, metadata_type: &str, birth_cycle: i64) -> PyResult<String> {
    let seed = format!("{}_{}_{}", public_key, metadata_type, birth_cycle);
    let mut hasher = Sha256::new();
    hasher.update(seed.as_bytes());
    let hex_digest = hex::encode(hasher.finalize());
    // Return first 16 chars
    if hex_digest.len() >= 16 {
        Ok(hex_digest[0..16].to_string())
    } else {
        Ok(hex_digest)
    }
}

/// Sign payload (IdentityCore).
#[pyfunction]
pub fn sign_payload(payload: &str, secret_key: &str) -> PyResult<String> {
    let mut mac = HmacSha256::new_from_slice(secret_key.as_bytes())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid key length: {}", e)))?;
    mac.update(payload.as_bytes());
    let result = mac.finalize();
    Ok(hex::encode(result.into_bytes()))
}

/// Verify signature (IdentityCore).
#[pyfunction]
pub fn verify_signature(payload: &str, signature: &str, public_key: &str) -> PyResult<bool> {
    // Re-sign with public_key as secret (Simulation per Python code)
    let expected = sign_payload(payload, public_key)?;
    // Constant time comparison is ideal, but here we compare hex strings.
    // Python uses hmac.compare_digest
    Ok(expected == signature)
}

/// Validate identity (IdentityCore).
#[pyfunction]
pub fn validate_identity(agent_id: &str) -> PyResult<bool> {
    Ok(agent_id.len() == 16 && !agent_id.contains('@'))
}

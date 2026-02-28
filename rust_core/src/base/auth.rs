use pyo3::prelude::*;
use sha2::{Sha256, Sha512, Digest};

/// Generate cache key (SHA256 hash).
#[pyfunction]
pub fn generate_cache_key(prompt: &str, context: &str) -> PyResult<String> {
    let combined = format!("{}:{}", prompt, context);
    let mut hasher = Sha256::new();
    hasher.update(combined.as_bytes());
    Ok(hex::encode(hasher.finalize()))
}

/// Generate authentication challenge (AuthCore).
#[pyfunction]
pub fn generate_challenge(agent_id: &str, timestamp: f64) -> PyResult<String> {
    let ts_str = timestamp.to_string();
    
    // Hash the timestamp first (inner hash)
    let mut hasher_inner = Sha256::new();
    hasher_inner.update(ts_str.as_bytes());
    let ts_hash = hex::encode(hasher_inner.finalize());
    
    // Create seed
    let seed = format!("{}_{}_{}", agent_id, ts_str, ts_hash);
    
    // Outer hash
    let mut hasher_outer = Sha256::new();
    hasher_outer.update(seed.as_bytes());
    Ok(hex::encode(hasher_outer.finalize()))
}

/// Generate authentication proof (AuthCore).
#[pyfunction]
pub fn generate_auth_proof(challenge: &str, secret_key: &str) -> PyResult<String> {
    let input = format!("{}:{}", challenge, secret_key);
    let mut hasher = Sha512::new();
    hasher.update(input.as_bytes());
    Ok(hex::encode(hasher.finalize()))
}

/// Verify authentication proof (AuthCore).
#[pyfunction]
pub fn verify_auth_proof(challenge: &str, proof: &str, secret_key: &str) -> PyResult<bool> {
    let expected = generate_auth_proof(challenge, secret_key)?;
    Ok(proof == expected)
}

/// Check if proof is expired (AuthCore).
#[pyfunction]
pub fn is_proof_expired(proof_time: f64, current_time: f64, ttl: f64) -> PyResult<bool> {
    Ok((current_time - proof_time) > ttl)
}

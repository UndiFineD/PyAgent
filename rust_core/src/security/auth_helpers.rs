use pyo3::prelude::*;
use sha2::Digest;

/// Specialized Auth Challenge generation (AuthCore).
#[pyfunction]
pub fn generate_challenge(agent_id: &str) -> PyResult<String> {
    let mut hasher = sha2::Sha256::new();
    hasher.update(agent_id.as_bytes());
    hasher.update(std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?.as_secs().to_string().as_bytes());
    Ok(format!("{:x}", hasher.finalize()))
}

/// Specialized Auth Proof generation (AuthCore).
#[pyfunction]
pub fn generate_auth_proof(challenge: &str, secret_key: &str) -> PyResult<String> {
    let mut hasher = sha2::Sha512::new();
    hasher.update(format!("{}:{}", challenge, secret_key).as_bytes());
    Ok(format!("{:x}", hasher.finalize()))
}

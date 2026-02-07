use pyo3::prelude::*;
use sha2::{Sha256, Digest};

/// Generates a stable hash for an error message (ignoring line numbers/paths).
#[pyfunction]
pub fn generate_failure_hash(error_msg: &str) -> PyResult<String> {
    let normalized: String = error_msg.to_lowercase()
        .chars()
        .filter(|c| !c.is_numeric())
        .collect();
        
    let mut hasher = Sha256::new();
    hasher.update(normalized.as_bytes());
    Ok(hex::encode(hasher.finalize()))
}

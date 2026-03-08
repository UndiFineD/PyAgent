pub mod text_analysis;
pub mod secrets;
pub mod vulnerability;
pub mod injection;
pub mod patterns;
pub mod auth_helpers;
pub mod crypto;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // obtain Python GIL token for submodule initializers
    let py = m.py();
    m.add_function(wrap_pyfunction!(text_analysis::analyze_thought_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text_analysis::scan_hardcoded_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text_analysis::scan_insecure_patterns_rust, m)?)?;

    m.add_function(wrap_pyfunction!(secrets::scan_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(secrets::scan_pii_rust, m)?)?;

    m.add_function(wrap_pyfunction!(vulnerability::scan_code_vulnerabilities_rust, m)?)?;

    m.add_function(wrap_pyfunction!(injection::scan_injections_rust, m)?)?;

    m.add_function(wrap_pyfunction!(patterns::scan_optimization_patterns_rust, m)?)?;

    m.add_function(wrap_pyfunction!(auth_helpers::generate_challenge, m)?)?;
    m.add_function(wrap_pyfunction!(auth_helpers::generate_auth_proof, m)?)?;

    // encryption helpers (added by security core rewrite plan)
    m.add_function(wrap_pyfunction!(crypto::encrypt_data, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::decrypt_data, m)?)?;
    // allow the Python side to load pub/priv keys from the filesystem
    m.add_function(wrap_pyfunction!(crypto::load_keys, m)?)?;
    // transaction API stubs
    m.add_function(wrap_pyfunction!(crypto::begin_transaction, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::commit_transaction, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::rollback_transaction, m)?)?;
    // key rotation
    m.add_function(wrap_pyfunction!(crypto::current_key_version, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::rotate_keys, m)?)?;
    // key management helpers
    m.add_function(wrap_pyfunction!(crypto::export_keys, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::clear_keys, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::cleanup_transactions, m)?)?;
    // metrics endpoint
    m.add_function(wrap_pyfunction!(crypto::gather_metrics, m)?)?;
    Ok(())
}

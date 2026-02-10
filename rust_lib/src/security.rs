pub mod text_analysis;
pub mod secrets;
pub mod vulnerability;
pub mod injection;
pub mod patterns;
pub mod auth_helpers;
pub mod firewall;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
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
    
    m.add_function(wrap_pyfunction!(firewall::verify_message_signature_rust, m)?)?;
    m.add_function(wrap_pyfunction!(firewall::ratchet_step_rust, m)?)?;
    Ok(())
}

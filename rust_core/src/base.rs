pub mod autonomy;
pub mod auth;
pub mod resilience;
pub mod identity;
pub mod pruning;
pub mod verification;
pub mod convergence;
pub mod error_mapping;
pub mod privacy;
pub mod logging;
pub mod io;


use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(autonomy::identify_blind_spots, m)?)?;
    m.add_function(wrap_pyfunction!(autonomy::calculate_daemon_sleep_interval, m)?)?;
    m.add_function(wrap_pyfunction!(autonomy::generate_self_improvement_plan, m)?)?;

    m.add_function(wrap_pyfunction!(auth::generate_cache_key, m)?)?;
    m.add_function(wrap_pyfunction!(auth::generate_challenge, m)?)?;
    m.add_function(wrap_pyfunction!(auth::generate_auth_proof, m)?)?;
    m.add_function(wrap_pyfunction!(auth::verify_auth_proof, m)?)?;
    m.add_function(wrap_pyfunction!(auth::is_proof_expired, m)?)?;

    m.add_function(wrap_pyfunction!(resilience::calculate_backoff, m)?)?;
    m.add_function(wrap_pyfunction!(resilience::should_attempt_recovery, m)?)?;
    m.add_function(wrap_pyfunction!(resilience::evaluate_state_transition, m)?)?;

    m.add_function(wrap_pyfunction!(identity::generate_agent_id, m)?)?;
    m.add_function(wrap_pyfunction!(identity::sign_payload, m)?)?;
    m.add_function(wrap_pyfunction!(identity::verify_signature, m)?)?;
    m.add_function(wrap_pyfunction!(identity::validate_identity, m)?)?;

    m.add_function(wrap_pyfunction!(pruning::calculate_decay, m)?)?;
    m.add_function(wrap_pyfunction!(pruning::is_in_refractory, m)?)?;
    m.add_function(wrap_pyfunction!(pruning::update_weight_on_fire_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pruning::should_prune, m)?)?;

    m.add_function(wrap_pyfunction!(verification::calculate_anchoring_fallback, m)?)?;
    m.add_function(wrap_pyfunction!(verification::check_latent_reasoning, m)?)?;
    m.add_function(wrap_pyfunction!(verification::is_response_valid_rust, m)?)?;

    m.add_function(wrap_pyfunction!(convergence::verify_fleet_health, m)?)?;

    m.add_function(wrap_pyfunction!(error_mapping::get_error_code, m)?)?;
    m.add_function(wrap_pyfunction!(error_mapping::get_error_documentation_link, m)?)?;

    m.add_function(wrap_pyfunction!(privacy::redact_pii, m)?)?;

    m.add_function(wrap_pyfunction!(logging::mask_sensitive_logs, m)?)?;
    m.add_function(wrap_pyfunction!(logging::build_log_entry_rust, m)?)?;

    m.add_function(wrap_pyfunction!(io::save_atomic_rust, m)?)?;
    m.add_function(wrap_pyfunction!(io::parse_config_rust, m)?)?;

    Ok(())
}

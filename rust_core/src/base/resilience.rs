use pyo3::prelude::*;
use rand::Rng;

/// Calculate backoff with jitter (ResilienceCore).
#[pyfunction]
pub fn calculate_backoff(
    failure_count: i32,
    threshold: i32,
    base_timeout: f64,
    multiplier: f64,
    max_timeout: f64,
    jitter_mode: Option<&str>,
) -> PyResult<f64> {
    if failure_count < threshold {
        return Ok(0.0);
    }

    let exponent = i32::max(0, failure_count - threshold);
    // Pow implementation
    let backoff = f64::min(max_timeout, base_timeout * multiplier.powi(exponent));

    let mode = jitter_mode.unwrap_or("full");
    let mut rng = rand::thread_rng();

    let result = match mode {
        "full" => rng.gen_range((base_timeout / 2.0)..backoff),
        "equal" => (backoff / 2.0) + rng.gen_range(0.0..(backoff / 2.0)),
        _ => {
            // Legacy 10%
            let jitter = backoff * 0.1 * rng.gen_range(-1.0..1.0);
            f64::max(base_timeout / 2.0, backoff + jitter)
        }
    };
    
    Ok(result)
}

/// Should attempt recovery (ResilienceCore).
#[pyfunction]
pub fn should_attempt_recovery(last_failure: f64, current_time: f64, timeout: f64) -> PyResult<bool> {
    Ok((current_time - last_failure) > timeout)
}

/// Evaluate state transition (ResilienceCore).
#[pyfunction]
pub fn evaluate_state_transition(
    current_state: &str,
    success_count: i32,
    needed: i32,
    failure_count: i32,
    threshold: i32
) -> PyResult<String> {
    let new_state = match current_state {
        "CLOSED" => {
            if failure_count >= threshold {
                "OPEN"
            } else {
                "CLOSED"
            }
        },
        "HALF_OPEN" => {
            if success_count >= needed {
                "CLOSED"
            } else {
                "HALF_OPEN"
            }
        },
        _ => current_state,
    };
    Ok(new_state.to_string())
}

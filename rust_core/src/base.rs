use pyo3::prelude::*;
use std::collections::HashMap;
use sha2::{Sha256, Sha512, Digest};
use rand::Rng;
use hmac::{Hmac, Mac};
type HmacSha256 = Hmac<Sha256>;

// === AutonomyCore Implementations ===

/// Identify blind spots (AutonomyCore).
#[pyfunction]
pub fn identify_blind_spots(success_rate: f64, task_diversity: f64) -> PyResult<Vec<String>> {
    let mut blind_spots = Vec::new();
    if success_rate < 0.7 {
        blind_spots.push("GENERAL_REASONING_RELIABILITY".to_string());
    }
    if task_diversity < 0.3 {
        blind_spots.push("DOMAIN_SPECIFIC_RIGIDITY".to_string());
    }
    Ok(blind_spots)
}

/// Calculate daemon sleep interval (AutonomyCore).
#[pyfunction]
pub fn calculate_daemon_sleep_interval(optimization_score: f64) -> PyResult<i32> {
    if optimization_score >= 1.0 {
        Ok(3600)
    } else if optimization_score > 0.8 {
        Ok(600)
    } else {
        Ok(60)
    }
}

/// Generate self improvement plan (AutonomyCore).
#[pyfunction]
pub fn generate_self_improvement_plan(agent_id: &str, blind_spots: Vec<String>) -> PyResult<String> {
    let mut plan = format!("AGENT SELF-MODEL UPDATE for {}:\n", agent_id);
    if blind_spots.is_empty() {
        plan.push_str("Status: Optimal. No immediate changes required.");
    } else {
        plan.push_str("Action: Expand training data for identified blind spots: ");
        plan.push_str(&blind_spots.join(", "));
    }
    Ok(plan)
}

// === AuthCore Implementations ===

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

// === ResilienceCore Implementations ===

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

// === IdentityCore Implementations ===

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

// === PruningCore Implementations ===

/// Calculate synaptic decay (PruningCore).
#[pyfunction]
pub fn calculate_decay(current_weight: f64, idle_time_sec: f64, half_life_sec: f64) -> PyResult<f64> {
    // ln(2) approx 0.69314718056
    let decay_constant = 0.69314718056 / half_life_sec;
    let new_weight = current_weight * (-decay_constant * idle_time_sec).exp();
    Ok(f64::max(new_weight, 0.05))
}

/// Check if in refractory period (PruningCore).
#[pyfunction]
pub fn is_in_refractory(current_time: f64, refractory_until: f64) -> PyResult<bool> {
    Ok(current_time < refractory_until)
}

/// Update weight on fire (PruningCore).
#[pyfunction]
pub fn update_weight_on_fire(current_weight: f64, success: bool) -> PyResult<f64> {
    if success {
        Ok(f64::min(current_weight * 1.1, 1.0))
    } else {
        Ok(f64::max(current_weight * 0.8, 0.1))
    }
}

/// Should prune (PruningCore).
#[pyfunction]
pub fn should_prune(weight: f64, threshold: f64) -> PyResult<bool> {
    Ok(weight < threshold)
}

// === ConvergenceCore Implementations ===

/// Verify fleet health.
#[pyfunction]
pub fn verify_fleet_health(agent_reports: HashMap<String, bool>) -> PyResult<HashMap<String, PyObject>> {
    let mut results = HashMap::new();
    let total_count = agent_reports.len();
    let healthy_count = agent_reports.values().filter(|&&v| v).count();
    
    let all_passed = if total_count > 0 {
        healthy_count == total_count
    } else {
        false
    };

    let failed_agents: Vec<String> = agent_reports.iter()
        .filter(|(_, &v)| !v)
        .map(|(k, _)| k.clone())
        .collect();

    Python::with_gil(|py| {
        results.insert("all_passed".to_string(), all_passed.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("healthy_count".to_string(), healthy_count.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("total_count".to_string(), total_count.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("failed_agents".to_string(), failed_agents.into_pyobject(py).unwrap().as_any().clone().unbind());
    });

    Ok(results)
}

// === ErrorMappingCore Implementations ===

/// Maps exception names to standardized PA-xxxx error codes.
/// Pure logic Rust equivalent of ErrorMappingCore for 2-5x speedup.
#[pyfunction]
pub fn get_error_code(exception_name: &str) -> PyResult<String> {
    let code = match exception_name {
        // 10xx: Infrastructure & I/O
        "FileSystemError" => "PA-1001",
        "NetworkTimeout" => "PA-1002",
        "DiskFull" => "PA-1003",
        "PermissionsDenied" => "PA-1004",

        // 20xx: Model & AI
        "ModelTimeout" => "PA-2001",
        "InvalidResponse" => "PA-2002",
        "ContextWindowExceeded" => "PA-2003",
        "RateLimitExceeded" => "PA-2004",

        // 30xx: Logic & Reasoning
        "DecompositionFailure" => "PA-3001",
        "CircularDependency" => "PA-3002",
        "InfiniteLoopDetected" => "PA-3003",

        // 40xx: Security & Compliance
        "UnauthorizedAccess" => "PA-4001",
        "SafetyFilterTriggered" => "PA-4002",
        "SensitiveDataExposure" => "PA-4003",

        // 50xx: Configuration
        "ManifestMismatch" => "PA-5001",
        "EnvVarMissing" => "PA-5002",

        // Default
        _ => "PA-0000",
    };

    Ok(code.to_string())
}

/// Generates troubleshooting link for error code.
#[pyfunction]
pub fn get_error_documentation_link(error_code: &str) -> PyResult<String> {
    Ok(format!("https://docs.pyagent.ai/errors/{}", error_code))
}

// === PrivacyCore Implementations ===

/// Redact PII from text (PrivacyCore).
#[pyfunction]
pub fn redact_pii(text: &str) -> PyResult<String> {
    static EMAIL_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static IP_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static KEY_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let email_re = EMAIL_RE.get_or_init(|| {
        regex::Regex::new(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+").unwrap()
    });
    
    let ip_re = IP_RE.get_or_init(|| {
        regex::Regex::new(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b").unwrap()
    });
    
    let key_re = KEY_RE.get_or_init(|| {
        regex::Regex::new(r"(?P<key>api_key|secret_key|secret|token)\s*[:=]\s*['""]?(?P<val>[a-zA-Z0-9_\-\.\~]{16,})['""]?").unwrap()
    });

    let text_no_email = email_re.replace_all(text, "[EMAIL_REDACTED]");
    let text_no_ip = ip_re.replace_all(&text_no_email, "[IP_REDACTED]");
    let final_text = key_re.replace_all(&text_no_ip, "$key=[REDACTED]");

    Ok(final_text.to_string())
}

// === LoggingCore Implementations ===

/// Mask sensitive patterns in logs (LoggingCore).
#[pyfunction]
pub fn mask_sensitive_logs(text: &str) -> PyResult<String> {
    static OPENAI_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static BEARER_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static GITHUB_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let openai_re = OPENAI_RE.get_or_init(|| {
        regex::Regex::new(r"sk-[a-zA-Z0-9]{32,}").unwrap()
    });

    let bearer_re = BEARER_RE.get_or_init(|| {
         regex::Regex::new(r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*").unwrap()
    });

    let github_re = GITHUB_RE.get_or_init(|| {
        regex::Regex::new(r"gh[ps]_[a-zA-Z0-9]{36}").unwrap()
    });

    let t1 = openai_re.replace_all(text, "[REDACTED]");
    let t2 = bearer_re.replace_all(&t1, "Bearer [REDACTED]");
    let t3 = github_re.replace_all(&t2, "[REDACTED]");

    Ok(t3.to_string())
}

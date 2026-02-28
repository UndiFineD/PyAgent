use pyo3::prelude::*;

/// Calculate anchoring strength fallback (AgentVerifier).
/// Uses word overlap / intersection as a baseline heuristic.
#[pyfunction]
pub fn calculate_anchoring_fallback(result: &str, context_text: &str) -> PyResult<f64> {
    if result.is_empty() || context_text.is_empty() {
        return Ok(0.5);
    }

    let result_lower = result.to_lowercase();
    let context_lower = context_text.to_lowercase();
    
    let context_words: std::collections::HashSet<&str> = context_lower.split_whitespace().collect();
    let result_words: Vec<&str> = result_lower.split_whitespace().collect();
    
    if result_words.is_empty() {
        return Ok(0.0);
    }
    
    let mut overlap_count = 0;
    for word in &result_words {
        if context_words.contains(word) {
            overlap_count += 1;
        }
    }
    
    let mut score = overlap_count as f64 / result_words.len() as f64;
    
    if result_words.len() < 5 {
        score *= 0.5;
    }
    
    Ok(f64::min(1.0, score * 1.5))
}

/// Check for latent reasoning (AgentVerifier).
/// Detects excessive non-ASCII characters.
#[pyfunction]
pub fn check_latent_reasoning(content: &str, threshold: f64) -> PyResult<bool> {
    if content.is_empty() {
        return Ok(true);
    }
    
    let non_ascii_count = content.chars().filter(|c| !c.is_ascii()).count();
    let ratio = non_ascii_count as f64 / content.len() as f64;
    
    Ok(ratio <= threshold)
}

/// Validate response (BaseAgentCore).
#[pyfunction]
pub fn is_response_valid_rust(response: &str, min_length: usize) -> PyResult<(bool, String)> {
    if response.is_empty() {
        return Ok((false, "Response is empty".to_string()));
    }
    
    if response.len() < min_length {
        return Ok((false, format!("Response too short (< {} chars)", min_length)));
    }
    
    if response.len() > 1_000_000 {
        return Ok((false, "Response too long (> 1M chars)".to_string()));
    }
    
    Ok((true, "".to_string()))
}

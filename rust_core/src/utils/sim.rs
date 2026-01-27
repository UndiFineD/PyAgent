use pyo3::prelude::*;
use rand::seq::SliceRandom;
use rand::Rng;
use std::collections::HashSet;

// === SimulationCore Implementations ===

/// Returns a list of agent indices that are designated to 'fail' (Phase 181).
#[pyfunction]
pub fn calculate_stochastic_failures(agent_count: usize, failure_rate: f64) -> PyResult<Vec<usize>> {
    let mut rng = rand::thread_rng();
    let num_failures = (agent_count as f64 * failure_rate) as usize;
    let mut indices: Vec<usize> = (0..agent_count).collect();
    indices.shuffle(&mut rng);
    Ok(indices.into_iter().take(num_failures).collect())
}

/// Simulates network/hardware jitter by adding a random spike.
#[pyfunction]
pub fn apply_latency_spike(base_latency: f64, spike_probability: f64) -> PyResult<f64> {
    let mut rng = rand::thread_rng();
    if rng.gen_bool(spike_probability) {
        Ok(base_latency * (1.5 + rng.gen_range(0.0..2.0)))
    } else {
        Ok(base_latency)
    }
}

#[pyfunction]
pub fn score_tool_relevance(name: &str, description: &str, query: &str) -> PyResult<f64> {
    let query_lower = query.to_lowercase();
    let name_lower = name.to_lowercase();
    let desc_lower = description.to_lowercase();
    let mut score = 0.0;

    if query_lower.contains(&name_lower) {
        score += 10.0;
    }

    let re = regex::Regex::new(r"\w+").unwrap();
    let desc_words: HashSet<&str> = re.find_iter(&desc_lower).map(|m| m.as_str()).collect();
    let query_words: HashSet<&str> = re.find_iter(&query_lower).map(|m| m.as_str()).collect();

    let common_count = desc_words.intersection(&query_words).count();
    score += common_count as f64 * 2.0;

    Ok(score)
}

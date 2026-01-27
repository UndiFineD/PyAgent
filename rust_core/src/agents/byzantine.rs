use pyo3::prelude::*;
use std::collections::HashMap;

/// Calculate Agreement Score (ByzantineCore).
#[pyfunction]
pub fn calculate_agreement_score(votes: Vec<Bound<'_, pyo3::types::PyDict>>) -> PyResult<f64> {
    if votes.is_empty() {
        return Ok(0.0);
    }
    
    let mut hash_weights: HashMap<String, f64> = HashMap::new();
    let mut total_weight = 0.0;
    
    for vote in votes {
        let w: f64 = vote.get_item("weight")?.ok_or_else(|| pyo3::exceptions::PyKeyError::new_err("weight missing"))?.extract()?;
        let h: String = vote.get_item("hash")?.ok_or_else(|| pyo3::exceptions::PyKeyError::new_err("hash missing"))?.extract()?;
        
        *hash_weights.entry(h).or_insert(0.0) += w;
        total_weight += w;
    }
    
    if total_weight == 0.0 {
        return Ok(0.0);
    }
    
    let max_agreement = hash_weights.values().cloned().fold(0.0, f64::max);
    Ok(max_agreement / total_weight)
}

/// Select Committee (ByzantineCore).
#[pyfunction]
#[allow(dead_code)]
pub fn select_committee(agents_reliability: HashMap<String, f64>, min_size: usize) -> PyResult<Vec<String>> {
    let mut eligible: Vec<(String, f64)> = agents_reliability.iter()
        .filter(|&(_, &score)| score > 0.7)
        .map(|(k, &v)| (k.clone(), v))
        .collect();
        
    eligible.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    let mut committee: Vec<String> = eligible.into_iter().map(|(n, _)| n).collect();
    
    if committee.len() < min_size {
        let mut all: Vec<(String, f64)> = agents_reliability.into_iter().collect();
        all.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        
        committee = all.into_iter()
            .take(min_size)
            .map(|(n, _)| n)
            .collect();
    }
    
    Ok(committee)
}

/// Get Required Quorum (ByzantineCore).
#[pyfunction]
#[allow(dead_code)]
pub fn get_required_quorum(change_type: &str) -> PyResult<f64> {
    match change_type {
        "infrastructure" | "security" | "core" => Ok(0.8),
        "documentation" | "examples" | "comments" => Ok(0.5),
        _ => Ok(0.67),
    }
}

/// Detect Deviating Hashes (ByzantineCore).
#[pyfunction]
pub fn detect_deviating_hashes(votes: Vec<Bound<'_, pyo3::types::PyDict>>, consensus_hash: String) -> PyResult<Vec<String>> {
    let mut deviants = Vec::new();
    for vote in votes {
        let h: String = vote.get_item("hash")?.ok_or_else(|| pyo3::exceptions::PyKeyError::new_err("hash missing"))?.extract()?;
        let id: String = vote.get_item("id")?.ok_or_else(|| pyo3::exceptions::PyKeyError::new_err("id missing"))?.extract()?;
        
        if h != consensus_hash {
            deviants.push(id);
        }
    }
    Ok(deviants)
}

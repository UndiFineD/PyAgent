use pyo3::prelude::*;
use std::collections::HashMap;

/// Calculate consensus winner (ConsensusCore).
#[pyfunction]
pub fn calculate_consensus_winner(proposals: Vec<String>, weights: Option<Vec<f64>>) -> PyResult<String> {
    if proposals.is_empty() {
        return Ok("".to_string());
    }
    
    let mut counts: HashMap<String, f64> = HashMap::new();
    
    // Create map
    for (i, p) in proposals.iter().enumerate() {
        let weight = if let Some(ref w) = weights {
             if i < w.len() { w[i] } else { 1.0 }
        } else {
            1.0
        };
        *counts.entry(p.clone()).or_insert(0.0) += weight;
    }
    
    // Sort logic: Weight desc, then Length desc
    let mut entries: Vec<(&String, &f64)> = counts.iter().collect();
    
    entries.sort_by(|a, b| {
        // Compare weights (desc)
        b.1.partial_cmp(a.1).unwrap_or(std::cmp::Ordering::Equal)
        // Then length (desc)
        .then_with(|| b.0.len().cmp(&a.0.len()))
    });
    
    match entries.first() {
        Some((winner, _)) => Ok(winner.to_string()),
        None => Ok("".to_string())
    }
}

/// Calculate agreement score 0..1 (ConsensusCore).
#[pyfunction]
#[allow(dead_code)]
pub fn calculate_agreement_score(votes: Vec<Bound<'_, pyo3::types::PyDict>>) -> PyResult<f64> {
    if votes.is_empty() {
        return Ok(0.0);
    }
    
    // Simple logic: if majority agree, high score
    let mut yes = 0;
    let total = votes.len();
    
    for v in votes {
         if let Some(approve) = v.get_item("approve")? {
             if approve.is_truthy()? {
                 yes += 1;
             }
         }
    }
    
    Ok(yes as f64 / total as f64)
}

/// Aggregate compliance scores (ComplianceCore).
/// Moved here temporarily or permanently? Usually ComplianceCore but referenced in agents.rs
#[pyfunction]
#[allow(dead_code)]
pub fn aggregate_score_rust(severities: Vec<String>) -> PyResult<f64> {
    if severities.is_empty() {
        return Ok(1.0);
    }

    let mut score = 1.0;
    for sev in severities {
        match sev.as_str() {
            "CRITICAL" => score -= 0.5,
            "WARNING" => score -= 0.1,
            "INFO" => score -= 0.02,
            _ => (),
        }
    }

    Ok(if score < 0.0 { 0.0 } else { score })
}

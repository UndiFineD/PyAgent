use pyo3::prelude::*;

/// Apply top-k mask to logits.
/// Sets all values outside top-k to negative infinity.
#[pyfunction]
pub fn top_k_mask_rust(
    logits: Vec<f32>,
    k: usize,
) -> PyResult<Vec<f32>> {
    if k >= logits.len() || k == 0 {
        return Ok(logits);
    }
    
    // Find k-th largest value
    let mut sorted: Vec<f32> = logits.iter().cloned().collect();
    sorted.sort_by(|a, b| b.partial_cmp(a).unwrap_or(std::cmp::Ordering::Equal));
    let threshold = sorted[k - 1];
    
    // Mask values below threshold
    let result: Vec<f32> = logits
        .iter()
        .map(|&v| if v >= threshold { v } else { f32::NEG_INFINITY })
        .collect();
    
    Ok(result)
}

/// Apply top-p (nucleus) mask to logits.
/// Keeps tokens with cumulative probability <= p.
#[pyfunction]
pub fn top_p_mask_rust(
    logits: Vec<f32>,
    p: f32,
) -> PyResult<Vec<f32>> {
    if p >= 1.0 || logits.is_empty() {
        return Ok(logits);
    }
    
    // Convert to probabilities using softmax
    let max_logit = logits.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
    let exp_sum: f32 = logits.iter().map(|&l| (l - max_logit).exp()).sum();
    let probs: Vec<f32> = logits.iter().map(|&l| (l - max_logit).exp() / exp_sum).collect();
    
    // Sort indices by probability (descending)
    let mut indices: Vec<usize> = (0..probs.len()).collect();
    indices.sort_by(|&a, &b| probs[b].partial_cmp(&probs[a]).unwrap_or(std::cmp::Ordering::Equal));
    
    // Find cumulative probability cutoff
    let mut cumsum = 0.0f32;
    let mut keep_indices = std::collections::HashSet::new();
    for &idx in &indices {
        cumsum += probs[idx];
        keep_indices.insert(idx);
        if cumsum > p {
            break;
        }
    }
    
    // Mask values not in top-p
    let result: Vec<f32> = logits
        .iter()
        .enumerate()
        .map(|(i, &v)| if keep_indices.contains(&i) { v } else { f32::NEG_INFINITY })
        .collect();
    
    Ok(result)
}

/// Gumbel sampling: adds Gumbel noise and returns argmax.
/// This implements the Gumbel-Softmax trick for sampling.
#[pyfunction]
pub fn gumbel_sample_rust(
    logits: Vec<f32>,
    temperature: f32,
    seed: u64,
) -> PyResult<usize> {
    if logits.is_empty() {
        return Err(pyo3::exceptions::PyValueError::new_err("empty logits"));
    }
    
    // Simple LCG for reproducible randomness
    let mut state = seed;
    let mut next_random = || {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        (state >> 33) as f64 / (1u64 << 31) as f64
    };
    
    let temp = temperature.max(1e-8) as f64;
    let mut max_val = f64::NEG_INFINITY;
    let mut max_idx = 0;
    
    for (i, &logit) in logits.iter().enumerate() {
        if logit == f32::NEG_INFINITY {
            continue;
        }
        // Gumbel noise: -log(-log(U))
        let u = next_random();
        let u = u.max(1e-10).min(1.0 - 1e-10);
        let gumbel = -(-u.ln()).ln();
        let score = (logit as f64 / temp) + gumbel;
        
        if score > max_val {
            max_val = score;
            max_idx = i;
        }
    }
    
    Ok(max_idx)
}

/// Compute beam search scores with length penalty.
/// Returns updated scores for each beam.
#[pyfunction]
pub fn beam_score_rust(
    log_probs: Vec<f32>,
    prev_scores: Vec<f32>,
    lengths: Vec<usize>,
    length_penalty: f32,
    vocab_size: usize,
) -> PyResult<Vec<f32>> {
    let num_beams = prev_scores.len();
    if log_probs.len() != num_beams * vocab_size {
        return Err(pyo3::exceptions::PyValueError::new_err("shape mismatch"));
    }
    
    let mut scores = Vec::with_capacity(num_beams * vocab_size);
    
    for beam in 0..num_beams {
        let length = lengths[beam] + 1;
        let length_norm = (length as f32).powf(length_penalty);
        
        for v in 0..vocab_size {
            let log_prob = log_probs[beam * vocab_size + v];
            let new_score = (prev_scores[beam] + log_prob) / length_norm;
            scores.push(new_score);
        }
    }
    
    Ok(scores)
}

/// Compute repetition and presence penalties for logits.
/// Returns modified logits.
#[pyfunction]
pub fn compute_penalties_rust(
    logits: Vec<f32>,
    token_counts: Vec<(usize, usize)>,  // (token_id, count) pairs
    repetition_penalty: f32,
    presence_penalty: f32,
    frequency_penalty: f32,
) -> PyResult<Vec<f32>> {
    let mut result = logits.clone();
    
    for (token_id, count) in token_counts {
        if token_id >= result.len() {
            continue;
        }
        
        let count = count as f32;
        let val = result[token_id];
        
        // Presence penalty: applied once if token is present
        let p_penalty = if count > 0.0 { presence_penalty } else { 0.0 };
        
        // Frequency penalty: applied proportional to count
        let f_penalty = count * frequency_penalty;
        
        // Repetition penalty: multiplicative
        // If logit > 0, dist = logit / penalty, else logit * penalty
        let r_penalty_factor = if count > 0.0 { repetition_penalty } else { 1.0 };
        
        let mut new_val = val;
        
        // Apply additive
        new_val -= p_penalty + f_penalty;
        
        // Apply multiplicative
        if r_penalty_factor != 1.0 {
             new_val = if new_val > 0.0 {
                 new_val / r_penalty_factor
             } else {
                 new_val * r_penalty_factor
             };
        }
        
        result[token_id] = new_val;
    }
    
    Ok(result)
}

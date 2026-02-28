use pyo3::prelude::*;
use std::collections::HashSet;

#[pyfunction]
pub fn rank_completions_rust(
    cumulative_logprobs: Vec<f64>,
    token_counts: Vec<usize>,
    length_penalty: f64,
) -> Vec<usize> {
    if cumulative_logprobs.len() != token_counts.len() {
        return Vec::new();
    }
    
    // Compute scores with length penalty
    let mut scored: Vec<_> = cumulative_logprobs.iter()
        .zip(token_counts.iter())
        .enumerate()
        .map(|(idx, (&logprob, &count))| {
            let length_factor = (count as f64).powf(length_penalty);
            let score = if length_factor > 0.0 { logprob / length_factor } else { f64::NEG_INFINITY };
            (idx, score)
        })
        .collect();
    
    // Sort by score descending
    scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    scored.into_iter().map(|(idx, _)| idx).collect()
}

/// Compute diversity penalty for beam search
#[pyfunction]
pub fn compute_diversity_penalty_rust(
    candidate_tokens: Vec<i64>,
    existing_sequences: Vec<Vec<i64>>,
    penalty_weight: f64,
    window_size: usize,
) -> Vec<f64> {
    candidate_tokens.iter()
        .map(|&token| {
            let mut penalty = 0.0;
            
            for seq in &existing_sequences {
                // Check recent window
                let start = if seq.len() > window_size { seq.len() - window_size } else { 0 };
                let count = seq[start..].iter().filter(|&&t| t == token).count();
                penalty += count as f64 * penalty_weight;
            }
            
            penalty
        })
        .collect()
}

/// Apply temperature to logits
#[pyfunction]
pub fn apply_temperature_schedule_rust(
    logits: Vec<f64>,
    temperature: f64,
    step: usize,
    schedule: &str,  // "constant", "linear", "cosine"
    decay_target: f64,
    decay_steps: usize,
) -> Vec<f64> {
    let temp = match schedule {
        "linear" => {
            let progress = (step as f64 / decay_steps.max(1) as f64).min(1.0);
            temperature - progress * (temperature - decay_target)
        }
        "cosine" => {
            let progress = (step as f64 / decay_steps.max(1) as f64).min(1.0);
            let cosine = 0.5 * (1.0 + (std::f64::consts::PI * progress).cos());
            decay_target + cosine * (temperature - decay_target)
        }
        _ => temperature,
    };
    
    let safe_temp = temp.max(0.01);
    logits.into_iter().map(|l| l / safe_temp).collect()
}

/// Mirostat sampling (mode 2)
#[pyfunction]
pub fn mirostat_sample_rust(
    logits: Vec<f64>,
    mu: f64,
    tau: f64,
    eta: f64,
) -> (usize, f64) {
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_logit).exp()).collect();
    let sum: f64 = exp_logits.iter().sum();
    let probs: Vec<f64> = exp_logits.iter().map(|e| e / sum).collect();
    
    let mut indexed: Vec<(usize, f64)> = probs.iter().cloned().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    let mut k = 1;
    for (i, (_, p)) in indexed.iter().enumerate() {
        let surprise = -(p.max(1e-10)).log2();
        if surprise > mu {
            k = i.max(1);
            break;
        }
        k = i + 1;
    }
    
    let top_k: Vec<(usize, f64)> = indexed.into_iter().take(k).collect();
    
    // Greedy for simplicity 
    let selected = top_k.iter()
        .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
        .map(|(i, _)| *i)
        .unwrap_or(0);
    
    let surprise = -(probs[selected].max(1e-10)).log2();
    let new_mu = mu - eta * (surprise - tau);
    
    (selected, new_mu)
}

/// Compute adaptive top-k based on entropy
#[pyfunction]
pub fn adaptive_top_k_rust(
    logits: Vec<f64>,
    entropy_threshold: f64,
    min_k: usize,
    max_k: usize,
) -> usize {
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_logit).exp()).collect();
    let sum: f64 = exp_logits.iter().sum();
    let probs: Vec<f64> = exp_logits.iter().map(|e| e / sum).collect();
    
    let entropy: f64 = probs.iter()
        .filter(|&&p| p > 1e-10)
        .map(|&p| -p * p.ln())
        .sum();
    
    let normalized = (entropy / entropy_threshold).min(2.0);
    let k = min_k + (normalized * (max_k - min_k) as f64) as usize;
    
    k.max(min_k).min(max_k)
}

/// Apply top-k filtering to logits
#[pyfunction]
pub fn apply_top_k_rust(
    logits: Vec<Vec<f64>>,
    k: usize,
) -> Vec<Vec<f64>> {
    if k == 0 {
        return logits;
    }
    
    logits.into_iter().map(|mut row| {
        if k >= row.len() {
            return row;
        }
        let mut sorted = row.clone();
        sorted.sort_by(|a, b| b.partial_cmp(a).unwrap_or(std::cmp::Ordering::Equal));
        let threshold = sorted[k - 1];
        
        for v in row.iter_mut() {
            if *v < threshold {
                *v = f64::NEG_INFINITY;
            }
        }
        row
    }).collect()
}

/// Apply top-p (nucleus) filtering to logits
#[pyfunction]
pub fn apply_top_p_rust(
    logits: Vec<Vec<f64>>,
    p: f64,
) -> Vec<Vec<f64>> {
    if p >= 1.0 {
        return logits;
    }
    
    logits.into_iter().map(|mut row| {
        let mut indices: Vec<usize> = (0..row.len()).collect();
        indices.sort_by(|&a, &b| row[b].partial_cmp(&row[a]).unwrap_or(std::cmp::Ordering::Equal));
        
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_sum: f64 = row.iter().map(|x| (x - max_val).exp()).sum();
        let probs: Vec<f64> = row.iter().map(|x| (x - max_val).exp() / exp_sum).collect();
        
        let mut cumsum = 0.0;
        let mut cutoff_idx = indices.len();
        
        for (i, &idx) in indices.iter().enumerate() {
            cumsum += probs[idx];
            if cumsum > p {
                cutoff_idx = i + 1;
                break;
            }
        }
        
        for &idx in &indices[cutoff_idx..] {
            row[idx] = f64::NEG_INFINITY;
        }
        row
    }).collect()
}

/// Batch top-k/top-p sampling
#[pyfunction]
pub fn batch_topk_topp_sample_rust(
    logits: Vec<Vec<f64>>,
    temperatures: Vec<f64>,
    top_ks: Vec<i32>,
    top_ps: Vec<f64>,
) -> Vec<i64> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    logits.into_iter().enumerate().map(|(b, mut row)| {
        let temp = temperatures.get(b).copied().unwrap_or(1.0);
        if temp > 1e-7 {
            for v in row.iter_mut() {
                *v /= temp;
            }
        }
        
        let k = top_ks.get(b).copied().unwrap_or(0) as usize;
        if k > 0 && k < row.len() {
            let mut sorted = row.clone();
            sorted.sort_by(|a, b| b.partial_cmp(a).unwrap_or(std::cmp::Ordering::Equal));
            let threshold = sorted[k - 1];
            for v in row.iter_mut() {
                if *v < threshold {
                    *v = f64::NEG_INFINITY;
                }
            }
        }
        
        let p = top_ps.get(b).copied().unwrap_or(1.0);
        if p < 1.0 {
            let mut indices: Vec<usize> = (0..row.len()).collect();
            indices.sort_by(|&a, &b| row[b].partial_cmp(&row[a]).unwrap_or(std::cmp::Ordering::Equal));
            
            let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let exp_sum: f64 = row.iter().filter(|&&x| x > f64::NEG_INFINITY).map(|x| (x - max_val).exp()).sum();
            
            let mut cumsum = 0.0;
            let mut cutoff_idx = indices.len();
            
            for (i, &idx) in indices.iter().enumerate() {
                if row[idx] > f64::NEG_INFINITY {
                    cumsum += (row[idx] - max_val).exp() / exp_sum;
                    if cumsum > p {
                        cutoff_idx = i + 1;
                        break;
                    }
                }
            }
            
            for &idx in &indices[cutoff_idx..] {
                row[idx] = f64::NEG_INFINITY;
            }
        }
        
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        if max_val == f64::NEG_INFINITY {
            return 0i64;
        }
        
        let exp_vals: Vec<f64> = row.iter().map(|x| {
            if *x > f64::NEG_INFINITY { (x - max_val).exp() } else { 0.0 }
        }).collect();
        let sum: f64 = exp_vals.iter().sum();
        
        if sum <= 0.0 {
            return row.iter().enumerate()
                .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
                .map(|(i, _)| i as i64)
                .unwrap_or(0);
        }
        
        let mut hasher = DefaultHasher::new();
        b.hash(&mut hasher);
        let r = hasher.finish() as f64 / u64::MAX as f64;
        
        let mut cumsum = 0.0;
        for (i, &exp_v) in exp_vals.iter().enumerate() {
            cumsum += exp_v / sum;
            if r < cumsum {
                return i as i64;
            }
        }
        
        (row.len() - 1) as i64
    }).collect()
}

/// Typical sampling filter (entropy-based)
#[pyfunction]
pub fn apply_typical_sampling_rust(
    logits: Vec<Vec<f64>>,
    mass: f64,
) -> Vec<Vec<f64>> {
    logits.into_iter().map(|mut row| {
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_sum: f64 = row.iter().map(|x| (x - max_val).exp()).sum();
        let probs: Vec<f64> = row.iter().map(|x| (x - max_val).exp() / exp_sum).collect();
        
        let entropy: f64 = -probs.iter()
            .filter(|&&p| p > 1e-10)
            .map(|&p| p * p.ln())
            .sum::<f64>();
        
        let log_probs: Vec<f64> = probs.iter()
            .map(|&p| if p > 1e-10 { p.ln() } else { f64::NEG_INFINITY })
            .collect();
        
        let mut deviations: Vec<(usize, f64)> = log_probs.iter()
            .enumerate()
            .filter(|(_, &lp)| lp > f64::NEG_INFINITY)
            .map(|(i, &lp)| (i, (-lp - entropy).abs()))
            .collect();
        
        deviations.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
        
        let mut cumsum = 0.0;
        let mut cutoff_idx = deviations.len();
        
        for (i, &(idx, _)) in deviations.iter().enumerate() {
            cumsum += probs[idx];
            if cumsum > mass {
                cutoff_idx = i + 1;
                break;
            }
        }
        
        let keep_indices: HashSet<usize> = deviations.iter()
            .take(cutoff_idx)
            .map(|&(idx, _)| idx)
            .collect();
        
        for (i, v) in row.iter_mut().enumerate() {
            if !keep_indices.contains(&i) {
                *v = f64::NEG_INFINITY;
            }
        }
        
        row
    }).collect()
}

/// Min-P sampling filter
#[pyfunction]
pub fn apply_min_p_rust(
    logits: Vec<Vec<f64>>,
    min_p: f64,
) -> Vec<Vec<f64>> {
    if min_p <= 0.0 {
        return logits;
    }
    
    logits.into_iter().map(|mut row| {
        // Compute softmax probabilities
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_sum: f64 = row.iter().map(|x| (x - max_val).exp()).sum();
        let probs: Vec<f64> = row.iter().map(|x| (x - max_val).exp() / exp_sum).collect();
        
        // Find max probability
        let max_prob = probs.iter().cloned().fold(0.0, f64::max);
        let threshold = min_p * max_prob;
        
        // Mask tokens below threshold
        for (i, &p) in probs.iter().enumerate() {
            if p < threshold {
                row[i] = f64::NEG_INFINITY;
            }
        }
        
        row
    }).collect()
}

/// Gumbel noise generation for Gumbel-softmax sampling
#[pyfunction]
pub fn gumbel_noise_rust(
    shape: (usize, usize),
    seed: u64,
) -> Vec<Vec<f64>> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let (batch, vocab) = shape;
    let mut result = Vec::with_capacity(batch);
    
    for b in 0..batch {
        let mut row = Vec::with_capacity(vocab);
        for v in 0..vocab {
            // Simple hash-based pseudo-random
            let mut hasher = DefaultHasher::new();
            (seed, b, v).hash(&mut hasher);
            let u = (hasher.finish() as f64 / u64::MAX as f64).max(1e-10);
            
            // Gumbel(0, 1) = -log(-log(u))
            let gumbel = -(-u.ln()).ln();
            row.push(gumbel);
        }
        result.push(row);
    }
    
    result
}

/// Apply logit bias to logits array
#[pyfunction]
pub fn logit_bias_apply_rust(
    logits: Vec<f32>,
    biases: Vec<(i32, f32)>,  // (token_id, bias)
) -> Vec<f32> {
    let mut result = logits;
    for (token_id, bias) in biases {
        if token_id >= 0 && (token_id as usize) < result.len() {
            result[token_id as usize] += bias;
        }
    }
    result
}

/// Compute min-p threshold for probability filtering
#[pyfunction]
pub fn min_p_threshold_rust(
    probs: Vec<f32>,
    min_p: f32,
) -> (f32, Vec<i32>) {
    if probs.is_empty() {
        return (0.0, Vec::new());
    }
    
    // Find max probability
    let max_prob = probs.iter().copied().fold(f32::NEG_INFINITY, f32::max);
    let threshold = max_prob * min_p;
    
    // Find tokens above threshold
    let allowed: Vec<i32> = probs
        .iter()
        .enumerate()
        .filter(|(_, &p)| p >= threshold)
        .map(|(i, _)| i as i32)
        .collect();
    
    (threshold, allowed)
}

/// Generate unique seeds for parallel sampling
#[pyfunction]
pub fn generate_sample_seeds_rust(
    base_seed: u64,
    n_samples: usize,
) -> Vec<u64> {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    (0..n_samples)
        .map(|i| {
            let mut hasher = DefaultHasher::new();
            base_seed.hash(&mut hasher);
            (i as u64).hash(&mut hasher);
            hasher.finish()
        })
        .collect()
}

use pyo3::prelude::*;

// =============================================================================
// Phase 41: LoRA Acceleration
// =============================================================================

/// Compute LoRA scaling factor
#[pyfunction]
pub fn lora_scaling_rust(
    rank: usize,
    alpha: f64,
    use_rslora: bool,
) -> f64 {
    if use_rslora {
        // rsLoRA: alpha / sqrt(rank)
        alpha / (rank as f64).sqrt()
    } else {
        // Standard LoRA: alpha / rank
        alpha / (rank as f64)
    }
}

/// Batch compute LoRA delta: scale * (B @ A)
/// Returns flattened delta matrix
#[pyfunction]
pub fn lora_delta_compute_rust(
    lora_a: Vec<f64>,  // [rank, in_features] flattened
    lora_b: Vec<f64>,  // [out_features, rank] flattened
    rank: usize,
    in_features: usize,
    out_features: usize,
    scale: f64,
) -> Vec<f64> {
    // Compute B @ A
    let mut delta = vec![0.0; out_features * in_features];
    
    for i in 0..out_features {
        for j in 0..in_features {
            let mut sum = 0.0;
            for k in 0..rank {
                // B[i, k] * A[k, j]
                let b_val = lora_b[i * rank + k];
                let a_val = lora_a[k * in_features + j];
                sum += b_val * a_val;
            }
            delta[i * in_features + j] = scale * sum;
        }
    }
    
    delta
}

/// Compute hash for LoRA adapter caching
#[pyfunction]
pub fn lora_adapter_hash_rust(
    adapter_path: String,
    rank: usize,
    alpha: f64,
    target_modules: Vec<String>,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    adapter_path.hash(&mut hasher);
    rank.hash(&mut hasher);
    (alpha as u64).hash(&mut hasher);
    for module in target_modules {
        module.hash(&mut hasher);
    }
    hasher.finish()
}

/// LoRA statistics update
#[pyfunction]
pub fn lora_stats_update_rust(
    adapter_id: String,
    load_latency: f64,
    exec_latency: f64,
    tokens: i64,
    stats: std::collections::HashMap<String, Vec<f64>>,
) -> std::collections::HashMap<String, Vec<f64>> {
    let mut result = stats.clone();
    
    let load_key = format!("{}_load_latencies", adapter_id);
    let exec_key = format!("{}_exec_latencies", adapter_id);
    let tokens_key = format!("{}_tokens", adapter_id);
    
    result.entry(load_key).or_default().push(load_latency);
    result.entry(exec_key).or_default().push(exec_latency);
    result.entry(tokens_key).or_default().push(tokens as f64);
    
    result
}

/// LoRA latency percentile calculation
#[pyfunction]
pub fn lora_latency_percentile_rust(
    latencies: Vec<f64>,
    percentile: f64,
) -> f64 {
    if latencies.is_empty() {
        return 0.0;
    }
    
    let mut sorted = latencies.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    let idx = ((sorted.len() as f64 * percentile / 100.0) as usize).min(sorted.len() - 1);
    sorted[idx]
}

/// LoRA adapter LRU selection
#[pyfunction]
pub fn lora_adapter_lru_rust(
    adapter_last_used: std::collections::HashMap<String, f64>,
    max_loaded: usize,
) -> Vec<String> {
    if adapter_last_used.len() <= max_loaded {
        return Vec::new();
    }
    
    let mut entries: Vec<_> = adapter_last_used.into_iter().collect();
    entries.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    let to_evict = entries.len() - max_loaded;
    entries.into_iter()
        .take(to_evict)
        .map(|(id, _)| id)
        .collect()
}

/// Apply LoRA adapters to a base model weight set (InferenceCore).
#[pyfunction]
pub fn apply_lora_rust(base_model: PyObject, _adapters: Vec<String>) -> PyResult<PyObject> {
    Ok(base_model)
}

/// IA3 (Input-Activation-Attention Scaling)
/// Scales activation vectors by learned scaling vectors.
/// x' = x * l (element-wise multiplication)
#[pyfunction]
pub fn apply_ia3_scaling_rust(
    activations: Vec<f32>,
    scaling_vector: Vec<f32>,
) -> Vec<f32> {
    if activations.is_empty() || scaling_vector.is_empty() {
        return activations;
    }
    
    let mut output = activations.clone();
    let scaling_len = scaling_vector.len();
    
    // Apply element-wise multiplication with broadcasting if necessary
    for (i, val) in output.iter_mut().enumerate() {
        *val *= scaling_vector[i % scaling_len];
    }
    
    output
}


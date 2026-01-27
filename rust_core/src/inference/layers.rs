use pyo3::prelude::*;

// =============================================================================
// State Space Model (SSM) / Mamba Acceleration
// =============================================================================

/// Discretize SSM A and B matrices using zero-order hold
/// Returns (dA, dB) as flattened arrays
#[allow(non_snake_case)]
#[pyfunction]
pub fn ssm_discretize_rust(
    a_log: Vec<f64>,      // [d_inner * ssm_state] - log of A diagonal
    b: Vec<Vec<f64>>,     // [batch, ssm_state]
    dt: Vec<Vec<f64>>,    // [batch, d_inner]
) -> (Vec<Vec<Vec<f64>>>, Vec<Vec<Vec<f64>>>) {
    let batch_size = dt.len();
    let d_inner = if dt.is_empty() { 0 } else { dt[0].len() };
    let ssm_state = if b.is_empty() { 0 } else { b[0].len() };
    
    if d_inner == 0 || ssm_state == 0 || batch_size == 0 {
        return (vec![], vec![]);
    }
    
    // A = -exp(A_log) is negative for stability
    let a_neg: Vec<f64> = a_log.iter().map(|l| -l.exp()).collect();
    
    let mut dA = vec![vec![vec![0.0f64; ssm_state]; d_inner]; batch_size];
    let mut dB = vec![vec![vec![0.0f64; ssm_state]; d_inner]; batch_size];
    
    for batch in 0..batch_size {
        for d in 0..d_inner {
            let dt_val = dt[batch][d];
            for s in 0..ssm_state {
                // A is [d_inner, ssm_state] stored row-major
                let a_idx = d * ssm_state + s;
                let a_val = if a_idx < a_neg.len() { a_neg[a_idx] } else { -1.0 };
                
                // dA = exp(dt * A)
                dA[batch][d][s] = (dt_val * a_val).exp();
                
                // dB = dt * B (simplified)
                dB[batch][d][s] = dt_val * b[batch][s];
            }
        }
    }
    
    (dA, dB)
}

/// Apply SSM recurrence step for single timestep
/// Returns (output, new_state)
#[allow(non_snake_case)]
#[pyfunction]
pub fn ssm_step_rust(
    x: Vec<Vec<f64>>,         // [batch, d_inner]
    state: Vec<Vec<Vec<f64>>>, // [batch, d_inner, ssm_state]
    dA: Vec<Vec<Vec<f64>>>,   // [batch, d_inner, ssm_state]
    dB: Vec<Vec<Vec<f64>>>,   // [batch, d_inner, ssm_state]
    c: Vec<Vec<f64>>,         // [batch, ssm_state]
    d_skip: Vec<f64>,         // [d_inner]
) -> (Vec<Vec<f64>>, Vec<Vec<Vec<f64>>>) {
    let batch_size = x.len();
    let d_inner = if x.is_empty() { 0 } else { x[0].len() };
    let ssm_state = if c.is_empty() { 0 } else { c[0].len() };
    
    if batch_size == 0 || d_inner == 0 || ssm_state == 0 {
        return (vec![], vec![]);
    }
    
    let mut new_state = vec![vec![vec![0.0f64; ssm_state]; d_inner]; batch_size];
    let mut output = vec![vec![0.0f64; d_inner]; batch_size];
    
    for batch in 0..batch_size {
        for d in 0..d_inner {
            // State update: h' = dA * h + dB * x
            for s in 0..ssm_state {
                new_state[batch][d][s] = 
                    dA[batch][d][s] * state[batch][d][s] + 
                    dB[batch][d][s] * x[batch][d];
            }
            
            // Output: y = C @ h + D * x
            let mut y = d_skip.get(d).copied().unwrap_or(0.0) * x[batch][d];
            for s in 0..ssm_state {
                y += c[batch][s] * new_state[batch][d][s];
            }
            output[batch][d] = y;
        }
    }
    
    (output, new_state)
}

/// Parallel prefix scan for SSM (associative scan)
/// Computes output[t] = gates[t] * output[t-1] + values[t]
#[pyfunction]
pub fn parallel_scan_rust(
    gates: Vec<Vec<Vec<f64>>>,  // [batch, seq_len, dim]
    values: Vec<Vec<Vec<f64>>>, // [batch, seq_len, dim]
) -> Vec<Vec<Vec<f64>>> {
    let batch_size = gates.len();
    if batch_size == 0 {
        return vec![];
    }
    let seq_len = gates[0].len();
    if seq_len == 0 {
        return gates;
    }
    let dim = if gates[0].is_empty() { 0 } else { gates[0][0].len() };
    
    let mut output = vec![vec![vec![0.0f64; dim]; seq_len]; batch_size];
    
    for batch in 0..batch_size {
        // Initialize first position
        for d in 0..dim {
            output[batch][0][d] = values[batch][0][d];
        }
        
        // Sequential scan (parallelizable with work-efficient algorithm)
        for t in 1..seq_len {
            for d in 0..dim {
                output[batch][t][d] = 
                    gates[batch][t][d] * output[batch][t-1][d] + 
                    values[batch][t][d];
            }
        }
    }
    
    output
}

/// Causal conv1d update for single step (used in Mamba decoding)
#[pyfunction]
pub fn causal_conv1d_update_rust(
    x: Vec<Vec<f64>>,              // [batch, d_inner] - new input
    conv_state: Vec<Vec<Vec<f64>>>, // [batch, d_inner, kernel_size]
    weight: Vec<Vec<f64>>,         // [d_inner, kernel_size]
) -> (Vec<Vec<f64>>, Vec<Vec<Vec<f64>>>) {
    let batch_size = x.len();
    let d_inner = if x.is_empty() { 0 } else { x[0].len() };
    let kernel_size = if weight.is_empty() { 0 } else { weight[0].len() };
    
    if batch_size == 0 || d_inner == 0 || kernel_size == 0 {
        return (vec![], vec![]);
    }
    
    let mut new_state = vec![vec![vec![0.0f64; kernel_size]; d_inner]; batch_size];
    let mut output = vec![vec![0.0f64; d_inner]; batch_size];
    
    for batch in 0..batch_size {
        for d in 0..d_inner {
            // Shift state left and insert new value
            for k in 0..(kernel_size - 1) {
                new_state[batch][d][k] = conv_state[batch][d][k + 1];
            }
            new_state[batch][d][kernel_size - 1] = x[batch][d];
            
            // Apply convolution
            let mut sum = 0.0;
            for k in 0..kernel_size {
                sum += new_state[batch][d][k] * weight[d][k];
            }
            output[batch][d] = sum;
        }
    }
    
    (output, new_state)
}

/// SiLU (Swish) activation: x * sigmoid(x)
#[pyfunction]
pub fn silu_activation_rust(x: Vec<Vec<f64>>) -> Vec<Vec<f64>> {
    x.iter().map(|row| {
        row.iter().map(|&v| {
            let sigmoid = 1.0 / (1.0 + (-v.clamp(-20.0, 20.0)).exp());
            v * sigmoid
        }).collect()
    }).collect()
}

// =============================================================================
// Multi-Head Latent Attention (MLA) / DeepSeek Acceleration
// =============================================================================

/// Multi-head Latent Attention compressed KV projection
/// Compresses KV using low-rank approximation
#[pyfunction]
pub fn mla_compress_kv_rust(
    hidden_states: Vec<Vec<f64>>, // [batch * seq, hidden_size]
    kv_proj_weight: Vec<Vec<f64>>, // [kv_lora_rank, hidden_size]
) -> Vec<Vec<f64>> {
    let num_tokens = hidden_states.len();
    let kv_lora_rank = kv_proj_weight.len();
    let hidden_size = if kv_proj_weight.is_empty() { 0 } else { kv_proj_weight[0].len() };
    
    if num_tokens == 0 || kv_lora_rank == 0 || hidden_size == 0 {
        return vec![];
    }
    
    // c_kv = hidden @ kv_proj.T
    let mut compressed = vec![vec![0.0f64; kv_lora_rank]; num_tokens];
    
    for token in 0..num_tokens {
        for r in 0..kv_lora_rank {
            let mut sum = 0.0;
            for h in 0..hidden_size.min(hidden_states[token].len()) {
                sum += hidden_states[token][h] * kv_proj_weight[r][h];
            }
            compressed[token][r] = sum;
        }
    }
    
    compressed
}

/// Grouped-query attention head mapping for MLA
#[pyfunction]
pub fn mla_head_mapping_rust(
    num_heads: usize,
    num_kv_heads: usize,
) -> Vec<usize> {
    if num_kv_heads == 0 {
        return vec![0; num_heads];
    }
    
    let ratio = num_heads / num_kv_heads;
    (0..num_heads).map(|h| h / ratio).collect()
}

// =============================================================================
// Pooling Engine Acceleration
// =============================================================================

/// Compute mean pooling over embeddings with attention mask
/// embeddings: [seq_len, hidden_size], mask: [seq_len]
#[pyfunction]
pub fn mean_pool_rust(
    embeddings: Vec<Vec<f64>>,
    mask: Vec<f64>,
) -> Vec<f64> {
    if embeddings.is_empty() {
        return Vec::new();
    }
    
    let hidden_size = embeddings[0].len();
    let mut result = vec![0.0; hidden_size];
    let mut total_weight = 0.0;
    
    for (i, emb) in embeddings.iter().enumerate() {
        let weight = if i < mask.len() { mask[i] } else { 1.0 };
        total_weight += weight;
        
        for (j, &val) in emb.iter().enumerate() {
            result[j] += val * weight;
        }
    }
    
    if total_weight > 0.0 {
        for val in result.iter_mut() {
            *val /= total_weight;
        }
    }
    
    result
}

/// Extract CLS token embedding (first token)
#[pyfunction]
pub fn cls_pool_rust(embeddings: Vec<Vec<f64>>) -> Vec<f64> {
    embeddings.into_iter().next().unwrap_or_default()
}

/// Extract last token embedding
#[pyfunction]
pub fn last_token_pool_rust(
    embeddings: Vec<Vec<f64>>,
    mask: Vec<f64>,
) -> Vec<f64> {
    // Find last non-masked position
    let last_idx = mask.iter()
        .enumerate()
        .rev()
        .find(|(_, &m)| m > 0.0)
        .map(|(i, _)| i)
        .unwrap_or(embeddings.len().saturating_sub(1));
    
    embeddings.get(last_idx).cloned().unwrap_or_default()
}

/// Apply Matryoshka dimensionality reduction
#[pyfunction]
pub fn matryoshka_truncate_rust(
    embedding: Vec<f64>,
    target_dim: usize,
    normalize: bool,
) -> Vec<f64> {
    let mut result: Vec<f64> = embedding.into_iter().take(target_dim).collect();
    
    if normalize && !result.is_empty() {
        let norm: f64 = result.iter().map(|x| x * x).sum::<f64>().sqrt();
        if norm > 1e-12 {
            for val in result.iter_mut() {
                *val /= norm;
            }
        }
    }
    
    result
}

/// Compute attention-weighted pooling
/// Uses softmax over scores to weight embeddings
#[pyfunction]
pub fn attention_pool_rust(
    embeddings: Vec<Vec<f64>>,
    attention_scores: Vec<f64>,
) -> Vec<f64> {
    if embeddings.is_empty() {
        return Vec::new();
    }
    
    let hidden_size = embeddings[0].len();
    
    // Softmax over attention scores
    let max_score = attention_scores.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exp_scores: Vec<f64> = attention_scores.iter()
        .map(|s| (s - max_score).exp())
        .collect();
    let sum: f64 = exp_scores.iter().sum();
    let weights: Vec<f64> = exp_scores.iter().map(|e| e / sum).collect();
    
    // Weighted sum
    let mut result = vec![0.0; hidden_size];
    for (i, emb) in embeddings.iter().enumerate() {
        let w = weights.get(i).unwrap_or(&0.0);
        for (j, &val) in emb.iter().enumerate() {
            result[j] += val * w;
        }
    }
    
    result
}

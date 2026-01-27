use pyo3::prelude::*;

/// Pool sequences with strategy
#[pyfunction]
pub fn pool_sequences_rust(
    hidden_states: Vec<Vec<f64>>,
    seq_starts: Vec<usize>,
    seq_lens: Vec<usize>,
    strategy: i32,  // 1=MEAN, 2=MAX, 3=FIRST, 4=LAST
) -> Vec<Vec<f64>> {
    let mut results = Vec::new();
    
    for (start, len) in seq_starts.iter().zip(seq_lens.iter()) {
        let end = (start + len).min(hidden_states.len());
        if *start >= hidden_states.len() || end <= *start {
            results.push(vec![0.0; hidden_states.get(0).map(|v| v.len()).unwrap_or(0)]);
            continue;
        }
        
        let slice = &hidden_states[*start..end];
        if slice.is_empty() {
            results.push(Vec::new());
            continue;
        }
        
        let dim = slice[0].len();
        let pooled = match strategy {
            1 => {
                // MEAN
                let mut sum = vec![0.0; dim];
                for row in slice {
                    for (i, &v) in row.iter().enumerate() {
                        if i < dim { sum[i] += v; }
                    }
                }
                sum.iter().map(|&v| v / slice.len() as f64).collect()
            },
            2 => {
                // MAX
                let mut max_vals = vec![f64::NEG_INFINITY; dim];
                for row in slice {
                    for (i, &v) in row.iter().enumerate() {
                        if i < dim { max_vals[i] = max_vals[i].max(v); }
                    }
                }
                max_vals
            },
            3 => {
                // FIRST
                slice[0].clone()
            },
            4 => {
                // LAST
                slice[slice.len() - 1].clone()
            },
            _ => vec![0.0; dim],
        };
        
        results.push(pooled);
    }
    
    results
}

/// Pooling cursor advance
#[pyfunction]
pub fn pooling_cursor_advance_rust(
    current_pos: usize,
    seq_len: usize,
    num_tokens: usize,
) -> (usize, usize, bool) {
    let new_pos = (current_pos + num_tokens).min(seq_len);
    let remaining = seq_len.saturating_sub(new_pos);
    let is_complete = new_pos >= seq_len;
    (new_pos, remaining, is_complete)
}

/// Attention-weighted pooling
#[pyfunction]
pub fn attention_weighted_pool_rust(
    hidden_states: Vec<Vec<f64>>,
    attention_weights: Vec<f64>,
) -> Vec<f64> {
    if hidden_states.is_empty() || attention_weights.is_empty() {
        return Vec::new();
    }
    
    let dim = hidden_states[0].len();
    let mut result = vec![0.0; dim];
    let mut weight_sum: f64 = 0.0;
    
    for (row, &weight) in hidden_states.iter().zip(attention_weights.iter()) {
        weight_sum += weight;
        for (i, &v) in row.iter().enumerate() {
            if i < dim {
                result[i] += v * weight;
            }
        }
    }
    
    if weight_sum > 1e-9 {
        for v in &mut result {
            *v /= weight_sum;
        }
    }
    
    result
}

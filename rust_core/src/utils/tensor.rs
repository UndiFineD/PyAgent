use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use std::collections::HashMap;

/// Validate tensor shape matches expected dimensions (PyTorch/TensorFlow).
#[pyfunction]
pub fn validate_tensor_shape_rust(
    shape: Vec<i64>,
    expected_rank: i64,
    dim_constraints: HashMap<i64, i64> // index -> expected_size, -1 for any
) -> PyResult<bool> {
    if shape.len() as i64 != expected_rank {
        return Ok(false);
    }
    
    for (idx, expected_size) in dim_constraints.into_iter() {
        if idx < 0 || idx >= shape.len() as i64 {
            continue;
        }
        let actual = shape[idx as usize];
        if expected_size != -1 && actual != expected_size {
            return Ok(false);
        }
    }
    
    Ok(true)
}

/// Compute logits mask for repetition penalty / constraints.
/// Returns a Vec<bool> mask where true means suppressed (masked out).
#[pyfunction]
#[allow(unused_variables)]
pub fn compute_logits_mask_rust(
    token_ids: Vec<i64>,
    vocab_size: i64,
    banned_tokens: Vec<i64>
) -> PyResult<Vec<bool>> {
    let mut mask = vec![false; vocab_size as usize];
    
    for token_id in banned_tokens {
        if token_id >= 0 && token_id < vocab_size {
            mask[token_id as usize] = true;
        }
    }
    
    Ok(mask)
}

/// High-speed vector similarity search (MemoryCore).
#[pyfunction]
pub fn search_vector_rust(query_vec: Vec<f32>, database: Vec<Vec<f32>>, top_k: usize) -> PyResult<Vec<usize>> {
    let mut scores: Vec<(usize, f32)> = database.iter().enumerate().map(|(i, vec)| {
        let dot_product: f32 = query_vec.iter().zip(vec.iter()).map(|(q, v)| q * v).sum();
        (i, dot_product)
    }).collect();
    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    Ok(scores.into_iter().take(top_k).map(|(i, _)| i).collect())
}

/// Apply temperature scaling to logits array.
#[pyfunction]
pub fn apply_temperature_rust(logits: Vec<f64>, temperature: f64) -> PyResult<Vec<f64>> {
    if temperature <= 0.0 {
        return Err(PyValueError::new_err("Temperature must be greater than 0"));
    }
    if temperature == 1.0 {
        return Ok(logits);
    }
    
    let scaled: Vec<f64> = logits.iter().map(|&x| x / temperature).collect();
    Ok(scaled)
}

/// Apply Top-K filtering.
/// Sets all logits below the top-k threshold to -infinity (or min float).
#[pyfunction]
pub fn apply_top_k_rust(logits: Vec<f64>, k: usize) -> PyResult<Vec<f64>> {
    if k == 0 || k >= logits.len() {
        return Ok(logits);
    }
    
    let mut indices: Vec<usize> = (0..logits.len()).collect();
    // Sort indices by value descending
    indices.sort_by(|&a, &b| logits[b].partial_cmp(&logits[a]).unwrap_or(std::cmp::Ordering::Equal));
    
    let cutoff_val = logits[indices[k-1]];
    
    let filtered: Vec<f64> = logits.iter()
        .map(|&val| if val >= cutoff_val { val } else { f64::NEG_INFINITY })
        .collect();
        
    Ok(filtered)
}

/// Apply Frequency/Presence penalties to logits.
#[pyfunction]
pub fn apply_repetition_penalty_rust(
    logits: Vec<f64>,
    past_tokens: Vec<i64>,
    penalty: f64
) -> PyResult<Vec<f64>> {
    let mut new_logits = logits.clone();
    let mut counts = HashMap::new();
    
    for token in past_tokens {
        *counts.entry(token).or_insert(0) += 1;
    }
    
    for (token_id, _) in counts {
        if token_id >= 0 && (token_id as usize) < new_logits.len() {
            let idx = token_id as usize;
            // Standard repetition penalty is division for positive logits, multiplication for negative
            // But common implementation is just additive or multiplicative penalty
            // Here we implement the multiplicative penalty where penalty > 1.0 reduces probability
            let val = new_logits[idx];
            if val < 0.0 {
                new_logits[idx] = val * penalty; // Make negative more negative
            } else {
                new_logits[idx] = val / penalty; // Make positive less positive
            }
        }
    }
    
    Ok(new_logits)
}

/// Encode raw tensor buffers (f32) into base64 or optimized format for network transport.
#[pyfunction]
pub fn encode_slice_rust(data: Vec<f32>) -> PyResult<String> {
    use base64::{Engine as _, engine::general_purpose};
    
    // Safety: ensure we are just treating f32 bytes as u8 bytes
    let byte_slice: &[u8] = unsafe {
        std::slice::from_raw_parts(
            data.as_ptr() as *const u8,
            data.len() * 4
        )
    };
    
    Ok(general_purpose::STANDARD.encode(byte_slice))
}

/// Encode tensor metadata for Redis/msgpack.
#[pyfunction]
pub fn msgpack_encode_tensor_meta_rust(
    shape: Vec<i64>,
    dtype: String,
    device: String
) -> PyResult<Vec<u8>> {
    // Simple manual packing or using rmp-serde if available
    // For this utility, we'll just use a JSON string as bytes for simplicity unless performance is critical
    let json_val = serde_json::json!({
        "shape": shape,
        "dtype": dtype,
        "device": device
    });
    
    let bytes = serde_json::to_vec(&json_val).map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(bytes)
}

/// Append logprobs (dict<int, float>) to a flat list of (token_id, logprob) tuples.
#[pyfunction]
pub fn flat_logprobs_append_rust(
    target_list: &Bound<'_, pyo3::types::PyList>,
    new_logprobs: HashMap<i64, f64>
) -> PyResult<()> {
    // This function modifies a Python list in-place
    for (k, v) in new_logprobs {
        let tuple = (k, v);
        target_list.append(tuple)?;
    }
    Ok(())
}

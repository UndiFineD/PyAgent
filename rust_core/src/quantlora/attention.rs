use pyo3::prelude::*;

/// Fast attention softmax with optional scaling.
/// Computes softmax(scores / sqrt(head_dim)) for attention.
#[pyfunction]
pub fn attention_softmax_rust(
    scores: Vec<f32>,
    seq_len: usize,
    head_dim: usize,
) -> PyResult<Vec<f32>> {
    if scores.is_empty() {
        return Ok(vec![]);
    }
    
    let scale = 1.0 / (head_dim as f32).sqrt();
    let num_rows = scores.len() / seq_len;
    
    let mut result = Vec::with_capacity(scores.len());
    
    for row_idx in 0..num_rows {
        let start = row_idx * seq_len;
        let end = start + seq_len;
        let row = &scores[start..end];
        
        // Scale and find max for numerical stability
        let scaled: Vec<f32> = row.iter().map(|s| s * scale).collect();
        let max_val = scaled.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
        
        // Exp and sum
        let exp_vals: Vec<f32> = scaled.iter().map(|s| (s - max_val).exp()).collect();
        let sum: f32 = exp_vals.iter().sum();
        
        // Normalize
        for val in exp_vals {
            result.push(val / sum);
        }
    }
    
    Ok(result)
}

/// Expand KV cache for Grouped Query Attention (GQA).
/// Repeats KV heads to match query head count.
/// kv: [batch, num_kv_heads, seq_len, head_dim]
/// Returns: [batch, num_heads, seq_len, head_dim]
#[pyfunction]
pub fn gqa_expand_kv_rust(
    kv: Vec<f32>,
    batch_size: usize,
    num_heads: usize,
    num_kv_heads: usize,
    seq_len: usize,
    head_dim: usize,
) -> PyResult<Vec<f32>> {
    if num_heads % num_kv_heads != 0 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "num_heads must be divisible by num_kv_heads"
        ));
    }
    
    let repeat_factor = num_heads / num_kv_heads;
    let input_head_stride = seq_len * head_dim;
    let input_batch_stride = num_kv_heads * input_head_stride;
    
    let output_size = batch_size * num_heads * seq_len * head_dim;
    let mut result = Vec::with_capacity(output_size);
    
    for b in 0..batch_size {
        for h in 0..num_heads {
            let kv_head = h / repeat_factor;
            let src_offset = b * input_batch_stride + kv_head * input_head_stride;
            
            for s in 0..seq_len {
                for d in 0..head_dim {
                    result.push(kv[src_offset + s * head_dim + d]);
                }
            }
        }
    }
    
    Ok(result)
}

/// Build slot mapping for paged attention.
/// Maps token positions to (block_idx, slot_offset) pairs.
#[pyfunction]
pub fn slot_mapping_rust(
    seq_lens: Vec<usize>,
    block_size: usize,
    num_blocks_per_seq: Vec<usize>,
) -> PyResult<Vec<(usize, usize)>> {
    let mut mapping = Vec::new();
    let mut block_offset = 0;
    
    for (seq_idx, &seq_len) in seq_lens.iter().enumerate() {
        let blocks_for_seq = num_blocks_per_seq.get(seq_idx).copied().unwrap_or(0);
        
        for pos in 0..seq_len {
            let block_in_seq = pos / block_size;
            let slot_in_block = pos % block_size;
            
            if block_in_seq < blocks_for_seq {
                mapping.push((block_offset + block_in_seq, slot_in_block));
            }
        }
        
        block_offset += blocks_for_seq;
    }
    
    Ok(mapping)
}

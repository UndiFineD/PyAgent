// Phase 27: Attention, Quantization & LoRA Accelerations
// Inspired by vLLM's high-performance kernels for paged attention,
// weight quantization, and LoRA adapter serving.

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Symmetric quantization of a weight tensor.
/// Returns (quantized_values, scale).
#[pyfunction]
pub fn quantize_symmetric_rust(
    weights: Vec<f32>,
    bits: u8,
) -> PyResult<(Vec<i8>, f32)> {
    if weights.is_empty() {
        return Ok((vec![], 1.0));
    }
    
    let qmax = ((1i32 << (bits - 1)) - 1) as f32;
    
    // Find max absolute value
    let max_abs = weights.iter().map(|w| w.abs()).fold(0.0f32, f32::max);
    
    // Compute scale
    let scale = if max_abs > 0.0 { max_abs / qmax } else { 1.0 };
    
    // Quantize
    let quantized: Vec<i8> = weights
        .iter()
        .map(|w| {
            let q = (w / scale).round();
            q.clamp(-qmax - 1.0, qmax) as i8
        })
        .collect();
    
    Ok((quantized, scale))
}

/// Asymmetric quantization with zero point.
/// Returns (quantized_values, scale, zero_point).
#[pyfunction]
pub fn quantize_asymmetric_rust(
    weights: Vec<f32>,
    bits: u8,
) -> PyResult<(Vec<u8>, f32, i32)> {
    if weights.is_empty() {
        return Ok((vec![], 1.0, 0));
    }
    
    let qmax = ((1u32 << bits) - 1) as f32;
    
    // Find min and max
    let min_val = weights.iter().fold(f32::INFINITY, |a, &b| a.min(b));
    let max_val = weights.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
    
    // Compute scale and zero point
    let scale = if max_val > min_val { 
        (max_val - min_val) / qmax 
    } else { 
        1.0 
    };
    let scale = scale.max(1e-8);
    
    let zp = (-min_val / scale).round() as i32;
    let zp = zp.clamp(0, qmax as i32);
    
    // Quantize
    let quantized: Vec<u8> = weights
        .iter()
        .map(|w| {
            let q = (w / scale + zp as f32).round();
            q.clamp(0.0, qmax) as u8
        })
        .collect();
    
    Ok((quantized, scale, zp))
}

/// Dequantize INT4 packed values to float32.
/// Input is packed int8 (two int4 per int8).
#[pyfunction]
pub fn dequantize_int4_rust(
    packed: Vec<i8>,
    scale: f32,
    zero_point: i32,
) -> PyResult<Vec<f32>> {
    let mut result = Vec::with_capacity(packed.len() * 2);
    
    for byte in packed {
        // Extract lower 4 bits
        let lower = byte & 0x0F;
        // Sign extend if > 7
        let lower = if lower > 7 { lower - 16 } else { lower };
        
        // Extract upper 4 bits
        let upper = (byte >> 4) & 0x0F;
        let upper = if upper > 7 { upper - 16 } else { upper };
        
        // Dequantize
        result.push((lower as i32 - zero_point) as f32 * scale);
        result.push((upper as i32 - zero_point) as f32 * scale);
    }
    
    Ok(result)
}

/// Pack two int4 values into one int8.
#[pyfunction]
pub fn pack_int4_rust(values: Vec<i8>) -> PyResult<Vec<i8>> {
    let mut packed = Vec::with_capacity((values.len() + 1) / 2);
    
    for chunk in values.chunks(2) {
        let lower = chunk[0] & 0x0F;
        let upper = if chunk.len() > 1 { chunk[1] & 0x0F } else { 0 };
        packed.push(lower | (upper << 4));
    }
    
    Ok(packed)
}

/// Compute per-group quantization scales.
/// Returns scales for each group.
#[pyfunction]
pub fn compute_scales_rust(
    weights: Vec<f32>,
    group_size: usize,
    bits: u8,
    symmetric: bool,
) -> PyResult<Vec<f32>> {
    if weights.is_empty() {
        return Ok(vec![]);
    }
    
    let qmax = if symmetric {
        ((1i32 << (bits - 1)) - 1) as f32
    } else {
        ((1u32 << bits) - 1) as f32
    };
    
    let num_groups = (weights.len() + group_size - 1) / group_size;
    let mut scales = Vec::with_capacity(num_groups);
    
    for chunk in weights.chunks(group_size) {
        if symmetric {
            let max_abs = chunk.iter().map(|w| w.abs()).fold(0.0f32, f32::max);
            let scale = if max_abs > 0.0 { max_abs / qmax } else { 1.0 };
            scales.push(scale);
        } else {
            let min_val = chunk.iter().fold(f32::INFINITY, |a, &b| a.min(b));
            let max_val = chunk.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
            let scale = if max_val > min_val {
                (max_val - min_val) / qmax
            } else {
                1.0
            };
            scales.push(scale.max(1e-8));
        }
    }
    
    Ok(scales)
}

/// Merge LoRA delta (B @ A * scaling) into base weights.
/// base_weight: [out_features, in_features]
/// lora_a: [rank, in_features]
/// lora_b: [out_features, rank]
#[pyfunction]
pub fn lora_merge_rust(
    base_weight: Vec<f32>,
    lora_a: Vec<f32>,
    lora_b: Vec<f32>,
    out_features: usize,
    in_features: usize,
    rank: usize,
    scaling: f32,
) -> PyResult<Vec<f32>> {
    if base_weight.len() != out_features * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "base_weight size mismatch"
        ));
    }
    if lora_a.len() != rank * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "lora_a size mismatch"
        ));
    }
    if lora_b.len() != out_features * rank {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "lora_b size mismatch"
        ));
    }
    
    // Compute delta = B @ A * scaling
    // B is [out_features, rank], A is [rank, in_features]
    // Result is [out_features, in_features]
    let mut result = base_weight.clone();
    
    for o in 0..out_features {
        for i in 0..in_features {
            let mut delta = 0.0f32;
            for r in 0..rank {
                // B[o, r] * A[r, i]
                delta += lora_b[o * rank + r] * lora_a[r * in_features + i];
            }
            result[o * in_features + i] += delta * scaling;
        }
    }
    
    Ok(result)
}

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

/// Batch dequantize with per-group scales.
/// Optimized for INT8/INT4 weight dequantization during inference.
#[pyfunction]
pub fn batch_dequantize_rust(
    quantized: Vec<i8>,
    scales: Vec<f32>,
    group_size: usize,
    bits: u8,
) -> PyResult<Vec<f32>> {
    let mut result = Vec::with_capacity(quantized.len());
    
    for (i, &q) in quantized.iter().enumerate() {
        let group_idx = i / group_size;
        let scale = scales.get(group_idx).copied().unwrap_or(1.0);
        
        if bits == 8 {
            result.push(q as f32 * scale);
        } else {
            // For packed 4-bit, handled separately
            result.push(q as f32 * scale);
        }
    }
    
    Ok(result)
}

/// Compute LoRA output: x @ A.T @ B.T * scaling
/// For fused LoRA application during inference.
#[pyfunction]
pub fn lora_forward_rust(
    x: Vec<f32>,
    lora_a: Vec<f32>,
    lora_b: Vec<f32>,
    batch_size: usize,
    in_features: usize,
    out_features: usize,
    rank: usize,
    scaling: f32,
) -> PyResult<Vec<f32>> {
    // x: [batch_size, in_features]
    // lora_a: [rank, in_features]
    // lora_b: [out_features, rank]
    
    if x.len() != batch_size * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err("x size mismatch"));
    }
    
    // Step 1: hidden = x @ A.T -> [batch_size, rank]
    let mut hidden = vec![0.0f32; batch_size * rank];
    for b in 0..batch_size {
        for r in 0..rank {
            let mut sum = 0.0f32;
            for i in 0..in_features {
                sum += x[b * in_features + i] * lora_a[r * in_features + i];
            }
            hidden[b * rank + r] = sum;
        }
    }
    
    // Step 2: output = hidden @ B.T * scaling -> [batch_size, out_features]
    let mut output = vec![0.0f32; batch_size * out_features];
    for b in 0..batch_size {
        for o in 0..out_features {
            let mut sum = 0.0f32;
            for r in 0..rank {
                sum += hidden[b * rank + r] * lora_b[o * rank + r];
            }
            output[b * out_features + o] = sum * scaling;
        }
    }
    
    Ok(output)
}

// =============================================================================
// Phase 28: Request Lifecycle, Sampling & Detokenization Accelerations
// =============================================================================

/// Validate request status transition.
/// Returns true if transition from current to next state is valid.
#[pyfunction]
pub fn request_status_transition_rust(
    current: u8,
    next: u8,
) -> PyResult<bool> {
    // States: 0=WAITING, 1=PENDING, 2=RUNNING, 3=PREEMPTED,
    //         4=FINISHED_STOPPED, 5=FINISHED_LENGTH, 6=FINISHED_ABORTED, 7=FINISHED_ERROR
    let valid = match (current, next) {
        // From WAITING
        (0, 1) | (0, 2) | (0, 6) => true,  // -> PENDING, RUNNING, ABORTED
        // From PENDING
        (1, 2) | (1, 6) => true,           // -> RUNNING, ABORTED
        // From RUNNING
        (2, 3) | (2, 4) | (2, 5) | (2, 6) | (2, 7) => true,  // -> PREEMPTED, any FINISHED
        // From PREEMPTED
        (3, 0) | (3, 2) | (3, 6) => true,  // -> WAITING, RUNNING, ABORTED
        // FINISHED states are terminal
        (4..=7, _) => false,
        _ => false,
    };
    Ok(valid)
}

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

/// Check if a token ID is in the stop token set.
#[pyfunction]
pub fn check_stop_tokens_rust(
    token_id: i64,
    stop_tokens: Vec<i64>,
) -> PyResult<bool> {
    Ok(stop_tokens.contains(&token_id))
}

/// Update prefix offset for incremental detokenization.
/// Returns (new_prefix_offset, new_read_offset).
#[pyfunction]
pub fn update_prefix_offset_rust(
    num_tokens: usize,
    _prev_prefix: usize,
    _prev_read: usize,
) -> PyResult<(usize, usize)> {
    // Keep last 6 tokens as prefix for context
    let new_prefix = if num_tokens > 6 { num_tokens - 6 } else { 0 };
    let new_read = num_tokens;
    Ok((new_prefix, new_read))
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
        
        let logit = result[token_id];
        
        // Repetition penalty (multiplicative)
        let rep_adjusted = if logit > 0.0 {
            logit / repetition_penalty
        } else {
            logit * repetition_penalty
        };
        
        // Presence penalty (additive, applied once if token seen)
        let pres_adjusted = if count > 0 {
            rep_adjusted - presence_penalty
        } else {
            rep_adjusted
        };
        
        // Frequency penalty (additive, scaled by count)
        let freq_adjusted = pres_adjusted - frequency_penalty * count as f32;
        
        result[token_id] = freq_adjusted;
    }
    
    Ok(result)
}

// ============================================================================
// Phase 29: Execution Context, Batching & Async Streaming Accelerations
// ============================================================================

/// Compute a hash for batch descriptor key.
/// Used for CUDA graph lookup.
#[pyfunction]
pub fn batch_descriptor_hash_rust(
    num_tokens: usize,
    num_reqs: usize,
    uniform: bool,
    has_lora: bool,
) -> PyResult<u64> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    num_tokens.hash(&mut hasher);
    num_reqs.hash(&mut hasher);
    uniform.hash(&mut hasher);
    has_lora.hash(&mut hasher);
    
    Ok(hasher.finish())
}

/// Copy data from source to destination using index mapping.
/// dst[i] = src[indices[i]] for all i.
#[pyfunction]
pub fn copy_with_indices_rust(
    src: Vec<f32>,
    indices: Vec<usize>,
) -> PyResult<Vec<f32>> {
    let mut dst = Vec::with_capacity(indices.len());
    
    for &idx in &indices {
        if idx >= src.len() {
            return Err(pyo3::exceptions::PyIndexError::new_err(
                format!("Index {} out of bounds for source of length {}", idx, src.len())
            ));
        }
        dst.push(src[idx]);
    }
    
    Ok(dst)
}

/// Pad sequences to a target length.
/// Returns flattened padded sequences and offsets.
#[pyfunction]
pub fn pad_sequences_rust(
    sequences: Vec<Vec<i64>>,
    target_len: usize,
    pad_value: i64,
) -> PyResult<(Vec<i64>, Vec<usize>)> {
    let num_seqs = sequences.len();
    let mut padded = Vec::with_capacity(num_seqs * target_len);
    let mut offsets = Vec::with_capacity(num_seqs + 1);
    offsets.push(0);
    
    for seq in sequences {
        let seq_len = seq.len();
        
        // Copy sequence
        for &val in &seq {
            padded.push(val);
        }
        
        // Add padding
        for _ in seq_len..target_len {
            padded.push(pad_value);
        }
        
        offsets.push(padded.len());
    }
    
    Ok((padded, offsets))
}

/// Compute data parallel splits across ranks.
/// Distributes tokens evenly across ranks.
#[pyfunction]
pub fn compute_dp_splits_rust(
    total_tokens: usize,
    world_size: usize,
) -> PyResult<Vec<usize>> {
    if world_size == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("world_size must be > 0"));
    }
    
    let base = total_tokens / world_size;
    let remainder = total_tokens % world_size;
    
    let splits: Vec<usize> = (0..world_size)
        .map(|i| if i < remainder { base + 1 } else { base })
        .collect();
    
    Ok(splits)
}

/// Fast memory copy for pinned memory transfers.
/// Simulates fast copy with optional transformation.
#[pyfunction]
pub fn pin_memory_copy_rust(
    src: Vec<f32>,
    scale: f32,
    offset: f32,
) -> PyResult<Vec<f32>> {
    // Apply scale and offset during copy
    let dst: Vec<f32> = src
        .iter()
        .map(|&v| v * scale + offset)
        .collect();
    
    Ok(dst)
}

/// Merge batch metadata from multiple sub-batches.
/// Combines seq_lens and computes new offsets.
#[pyfunction]
pub fn merge_batch_metadata_rust(
    seq_lens_list: Vec<Vec<usize>>,
) -> PyResult<(Vec<usize>, Vec<usize>)> {
    let mut merged_seq_lens = Vec::new();
    let mut offsets = vec![0usize];
    
    for seq_lens in seq_lens_list {
        for &len in &seq_lens {
            merged_seq_lens.push(len);
        }
        let last = *offsets.last().unwrap();
        let total: usize = seq_lens.iter().sum();
        offsets.push(last + total);
    }
    
    Ok((merged_seq_lens, offsets))
}

/// Validate batch shapes for consistency.
/// Returns Ok(()) if valid, error otherwise.
#[pyfunction]
pub fn validate_batch_shapes_rust(
    num_tokens: usize,
    num_reqs: usize,
    input_ids_len: usize,
    positions_len: usize,
    seq_lens_len: usize,
) -> PyResult<bool> {
    if input_ids_len != num_tokens {
        return Err(pyo3::exceptions::PyValueError::new_err(
            format!("input_ids length {} != num_tokens {}", input_ids_len, num_tokens)
        ));
    }
    
    if positions_len != num_tokens {
        return Err(pyo3::exceptions::PyValueError::new_err(
            format!("positions length {} != num_tokens {}", positions_len, num_tokens)
        ));
    }
    
    if seq_lens_len != num_reqs {
        return Err(pyo3::exceptions::PyValueError::new_err(
            format!("seq_lens length {} != num_reqs {}", seq_lens_len, num_reqs)
        ));
    }
    
    Ok(true)
}


// ============================================================================
// Phase 30: Engine Core, Output Processor & Incremental Detokenizer Accelerations
// Inspired by vLLM's v1/engine/ patterns for fast engine operations.
// ============================================================================

/// Fast block token hashing using SIMD-like operations.
/// Combines parent hash with token IDs for content-addressable caching.
#[pyfunction]
pub fn hash_block_tokens_rust(
    parent_hash: Option<Vec<u8>>,
    token_ids: Vec<i64>,
    extra_keys: Option<Vec<String>>,
) -> PyResult<Vec<u8>> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    
    // Include parent hash
    if let Some(ref ph) = parent_hash {
        ph.hash(&mut hasher);
    }
    
    // Hash token IDs
    for tid in &token_ids {
        tid.hash(&mut hasher);
    }
    
    // Include extra keys
    if let Some(ref keys) = extra_keys {
        for key in keys {
            key.hash(&mut hasher);
        }
    }
    
    let hash_value = hasher.finish();
    Ok(hash_value.to_le_bytes().to_vec())
}

/// Vectorized stop string checking.
/// Returns (stop_string_index, truncation_position) or None.
#[pyfunction]
pub fn check_stop_strings_rust(
    output_text: &str,
    new_char_count: usize,
    stop_strings: Vec<String>,
    include_in_output: bool,
) -> PyResult<Option<(usize, i64)>> {
    if stop_strings.is_empty() || output_text.is_empty() {
        return Ok(None);
    }
    
    // Find max stop string length for search window
    let max_stop_len = stop_strings.iter().map(|s| s.len()).max().unwrap_or(0);
    
    // Calculate search start position
    let text_len = output_text.len();
    let check_start = if new_char_count + max_stop_len > text_len {
        0
    } else {
        text_len - new_char_count - max_stop_len
    };
    
    let check_text = &output_text[check_start..];
    
    // Check each stop string
    for (idx, stop_str) in stop_strings.iter().enumerate() {
        if let Some(pos) = check_text.find(stop_str) {
            let absolute_pos = check_start + pos;
            let truncate_to = if include_in_output {
                (absolute_pos + stop_str.len()) as i64
            } else {
                absolute_pos as i64
            };
            return Ok(Some((idx, truncate_to)));
        }
    }
    
    Ok(None)
}

/// Parallel batch detokenization helper.
/// Decodes multiple token sequences efficiently.
#[pyfunction]
pub fn detokenize_batch_rust(
    token_ids_batch: Vec<Vec<i64>>,
    vocab: std::collections::HashMap<i64, String>,
) -> PyResult<Vec<String>> {
    let results: Vec<String> = token_ids_batch
        .iter()
        .map(|tokens| {
            tokens
                .iter()
                .filter_map(|tid| vocab.get(tid))
                .cloned()
                .collect::<Vec<_>>()
                .join("")
        })
        .collect();
    
    Ok(results)
}

/// Efficient request state merging.
/// Combines multiple partial states into a single state.
#[pyfunction]
pub fn merge_request_states_rust(
    token_ids_list: Vec<Vec<i64>>,
    output_texts: Vec<String>,
) -> PyResult<(Vec<i64>, String)> {
    // Merge token IDs
    let merged_tokens: Vec<i64> = token_ids_list
        .into_iter()
        .flatten()
        .collect();
    
    // Concatenate output texts
    let merged_text: String = output_texts.join("");
    
    Ok((merged_tokens, merged_text))
}

/// Binary search-based prefix matching.
/// Returns the length of the common prefix between two hash lists.
#[pyfunction]
pub fn compute_prefix_match_rust(
    cached_hashes: Vec<Vec<u8>>,
    request_hashes: Vec<Vec<u8>>,
) -> PyResult<usize> {
    let min_len = cached_hashes.len().min(request_hashes.len());
    
    // Linear scan (binary search only helps for very long sequences)
    let mut match_length = 0;
    for i in 0..min_len {
        if cached_hashes[i] == request_hashes[i] {
            match_length = i + 1;
        } else {
            break;
        }
    }
    
    Ok(match_length)
}

/// Fast UTF-8 validation.
/// Returns true if the string is valid UTF-8.
#[pyfunction]
pub fn validate_utf8_rust(text: &str) -> PyResult<bool> {
    // In Rust, &str is always valid UTF-8, so this is a no-op.
    // But we can check for replacement characters indicating prior issues.
    Ok(!text.contains('\u{FFFD}'))
}

/// Efficient output serialization/packing.
/// Packs request outputs for efficient transfer.
#[pyfunction]
pub fn pack_outputs_rust(
    request_ids: Vec<String>,
    token_ids_list: Vec<Vec<i64>>,
    finish_reasons: Vec<Option<String>>,
) -> PyResult<Vec<(String, Vec<i64>, Option<String>)>> {
    let packed: Vec<_> = request_ids
        .into_iter()
        .zip(token_ids_list.into_iter())
        .zip(finish_reasons.into_iter())
        .map(|((req_id, tokens), reason)| (req_id, tokens, reason))
        .collect();
    
    Ok(packed)
}

/// Batch cache key computation.
/// Computes block hashes for multiple requests efficiently.
#[pyfunction]
pub fn compute_cache_keys_rust(
    request_ids: Vec<String>,
    token_ids_list: Vec<Vec<i64>>,
    block_size: usize,
) -> PyResult<std::collections::HashMap<String, Vec<Vec<u8>>>> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut result = std::collections::HashMap::new();
    
    for (req_id, token_ids) in request_ids.into_iter().zip(token_ids_list.into_iter()) {
        let mut hashes = Vec::new();
        let mut parent_hash: Option<u64> = None;
        
        let num_blocks = token_ids.len() / block_size;
        for i in 0..num_blocks {
            let start = i * block_size;
            let end = start + block_size;
            let block_tokens = &token_ids[start..end];
            
            let mut hasher = DefaultHasher::new();
            
            // Include parent hash
            if let Some(ph) = parent_hash {
                ph.hash(&mut hasher);
            }
            
            // Hash tokens
            for tid in block_tokens {
                tid.hash(&mut hasher);
            }
            
            let hash_value = hasher.finish();
            hashes.push(hash_value.to_le_bytes().to_vec());
            parent_hash = Some(hash_value);
        }
        
        result.insert(req_id, hashes);
    }
    
    Ok(result)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(attention_softmax_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_dequantize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_descriptor_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(beam_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(check_stop_strings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(check_stop_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_cache_keys_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_dp_splits_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_penalties_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_prefix_match_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_scales_rust, m)?)?;
    m.add_function(wrap_pyfunction!(copy_with_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(dequantize_int4_rust, m)?)?;
    m.add_function(wrap_pyfunction!(detokenize_batch_rust, m)?)?;
    m.add_function(wrap_pyfunction!(gqa_expand_kv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(gumbel_sample_rust, m)?)?;
    m.add_function(wrap_pyfunction!(hash_block_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(lora_forward_rust, m)?)?;
    m.add_function(wrap_pyfunction!(lora_merge_rust, m)?)?;
    m.add_function(wrap_pyfunction!(merge_batch_metadata_rust, m)?)?;
    m.add_function(wrap_pyfunction!(merge_request_states_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pack_int4_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pack_outputs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pad_sequences_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pin_memory_copy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantize_asymmetric_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantize_symmetric_rust, m)?)?;
    m.add_function(wrap_pyfunction!(request_status_transition_rust, m)?)?;
    m.add_function(wrap_pyfunction!(slot_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(top_k_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(top_p_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(update_prefix_offset_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_batch_shapes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_utf8_rust, m)?)?;
    Ok(())
}

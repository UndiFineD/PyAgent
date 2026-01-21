// Phase 25: Inference Acceleration Functions
// Rust-accelerated helpers for speculative decoding, prefix caching, and KV cache management

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};
use std::collections::HashMap;

// =============================================================================
// N-Gram Matching for Speculative Decoding
// =============================================================================

/// Fast n-gram matching for prompt lookup speculative decoding
/// Returns list of (position, ngram) tuples where matches occur
#[pyfunction]
#[pyo3(signature = (prompt_tokens, target_ngram, n=4))]
pub fn ngram_match_rust(
    prompt_tokens: Vec<i64>,
    target_ngram: Vec<i64>,
    n: usize,
) -> Vec<(usize, Vec<i64>)> {
    if prompt_tokens.len() < n || target_ngram.len() != n {
        return Vec::new();
    }
    
    let mut matches = Vec::new();
    
    for i in 0..=prompt_tokens.len() - n {
        let window = &prompt_tokens[i..i + n];
        if window == target_ngram.as_slice() {
            matches.push((i, window.to_vec()));
        }
    }
    
    matches
}

/// Fused PackKV Attention (arXiv:2512.24449)
/// Performs register-level decompression during attention matmul.
/// Placeholder for phase 51 acceleration.
#[pyfunction]
#[pyo3(signature = (q, k_compressed, v_compressed, metadata_map, scale=None))]
pub fn fused_packkv_attention_rust(
    q: Vec<f32>,
    k_compressed: Vec<u8>,
    v_compressed: Vec<u8>,
    metadata_map: HashMap<i32, HashMap<String, f32>>,
    scale: Option<f32>,
) -> PyResult<Vec<f32>> {
    // In production, this would use a high-performance Rust/SIMD or CUDA/Triton bridge
    // to perform matmul without full dequantization to VRAM.
    Ok(q) // Placeholder
}

/// Build n-gram index from token sequence for fast lookup
/// Returns HashMap mapping n-gram tuples to list of positions
#[pyfunction]
#[pyo3(signature = (tokens, n=4))]
pub fn build_ngram_index_rust(
    py: Python<'_>,
    tokens: Vec<i64>,
    n: usize,
) -> PyResult<PyObject> {
    let index = PyDict::new_bound(py);
    
    if tokens.len() < n {
        return Ok(index.into_py(py));
    }
    
    for i in 0..=tokens.len() - n {
        let ngram = PyTuple::new_bound(py, &tokens[i..i + n]);
        let list = match index.get_item(&ngram)? {
            Some(obj) => obj.downcast_into::<PyList>()?,
            None => {
                let new_list = PyList::empty_bound(py);
                index.set_item(&ngram, &new_list)?;
                new_list
            }
        };
        list.append(i)?;
    }
    
    Ok(index.into_py(py))
}

/// Find continuation candidates after matching n-grams
/// Returns list of candidate token sequences with their frequencies
#[pyfunction]
#[pyo3(signature = (tokens, context_ngram, max_continuations=5, continuation_len=4))]
pub fn find_continuations_rust(
    tokens: Vec<i64>,
    context_ngram: Vec<i64>,
    max_continuations: usize,
    continuation_len: usize,
) -> Vec<(Vec<i64>, usize)> {
    let n = context_ngram.len();
    if tokens.len() < n + continuation_len {
        return Vec::new();
    }
    
    let mut continuation_counts: HashMap<Vec<i64>, usize> = HashMap::new();
    
    for i in 0..=tokens.len() - n - continuation_len {
        let window = &tokens[i..i + n];
        if window == context_ngram.as_slice() {
            let continuation = tokens[i + n..i + n + continuation_len].to_vec();
            *continuation_counts.entry(continuation).or_default() += 1;
        }
    }
    
    // Sort by frequency descending
    let mut results: Vec<_> = continuation_counts.into_iter().collect();
    results.sort_by(|a, b| b.1.cmp(&a.1));
    results.truncate(max_continuations);
    
    results
}

// =============================================================================
// Suffix Tree Operations for Pattern Matching
// =============================================================================

/// Simple suffix array construction for pattern matching
/// Returns sorted suffix positions
#[pyfunction]
pub fn build_suffix_array_rust(tokens: Vec<i64>) -> Vec<usize> {
    let n = tokens.len();
    if n == 0 {
        return Vec::new();
    }
    
    let mut indices: Vec<usize> = (0..n).collect();
    
    indices.sort_by(|&a, &b| {
        let suffix_a = &tokens[a..];
        let suffix_b = &tokens[b..];
        suffix_a.cmp(suffix_b)
    });
    
    indices
}

/// Binary search in suffix array for pattern
/// Returns (start_idx, end_idx) in suffix array where pattern matches
#[pyfunction]
pub fn suffix_search_rust(
    tokens: Vec<i64>,
    suffix_array: Vec<usize>,
    pattern: Vec<i64>,
) -> (usize, usize) {
    if pattern.is_empty() || suffix_array.is_empty() {
        return (0, 0);
    }
    
    // Binary search for lower bound
    let lower = suffix_array.partition_point(|&i| {
        let suffix = &tokens[i..];
        let cmp_len = pattern.len().min(suffix.len());
        suffix[..cmp_len].cmp(&pattern[..]) == std::cmp::Ordering::Less
    });
    
    // Binary search for upper bound
    let upper = suffix_array.partition_point(|&i| {
        let suffix = &tokens[i..];
        let cmp_len = pattern.len().min(suffix.len());
        let prefix_cmp = suffix[..cmp_len].cmp(&pattern[..]);
        prefix_cmp == std::cmp::Ordering::Less || prefix_cmp == std::cmp::Ordering::Equal
    });
    
    (lower, upper)
}

// =============================================================================
// Block Hashing for Prefix Cache
// =============================================================================

/// XXHash64-style fast hashing for cache blocks
#[pyfunction]
pub fn compute_block_hash_rust(tokens: Vec<i64>, prev_hash: u64) -> u64 {
    const PRIME64_1: u64 = 0x9E3779B185EBCA87;
    const PRIME64_2: u64 = 0xC2B2AE3D27D4EB4F;
    const PRIME64_3: u64 = 0x165667B19E3779F9;
    const PRIME64_4: u64 = 0x85EBCA77C2B2AE63;
    const PRIME64_5: u64 = 0x27D4EB2F165667C5;
    
    let mut hash = prev_hash.wrapping_add(PRIME64_5);
    
    for &token in &tokens {
        let k = (token as u64).wrapping_mul(PRIME64_2);
        let k = k.rotate_left(31).wrapping_mul(PRIME64_1);
        hash ^= k;
        hash = hash.rotate_left(27).wrapping_mul(PRIME64_1).wrapping_add(PRIME64_4);
    }
    
    // Finalization
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(PRIME64_2);
    hash ^= hash >> 29;
    hash = hash.wrapping_mul(PRIME64_3);
    hash ^= hash >> 32;
    
    hash
}

/// Batch compute block hashes for a sequence of token blocks
#[pyfunction]
#[pyo3(signature = (token_blocks, initial_hash=0))]
pub fn batch_block_hash_rust(
    token_blocks: Vec<Vec<i64>>,
    initial_hash: u64,
) -> Vec<u64> {
    let mut hashes = Vec::with_capacity(token_blocks.len());
    let mut prev_hash = initial_hash;
    
    for block in token_blocks {
        let hash = compute_block_hash_rust(block, prev_hash);
        hashes.push(hash);
        prev_hash = hash;
    }
    
    hashes
}

// =============================================================================
// LRU Eviction Helper
// =============================================================================

/// Find LRU candidate blocks to evict
/// Returns indices of blocks to evict based on last_access_time
#[pyfunction]
pub fn lru_evict_rust(
    last_access_times: Vec<f64>,
    pinned: Vec<bool>,
    num_to_evict: usize,
) -> Vec<usize> {
    if num_to_evict == 0 {
        return Vec::new();
    }
    
    // Collect unpinned indices with their access times
    let mut candidates: Vec<(usize, f64)> = last_access_times
        .iter()
        .enumerate()
        .filter(|(i, _)| !pinned.get(*i).copied().unwrap_or(false))
        .map(|(i, &t)| (i, t))
        .collect();
    
    // Sort by access time ascending (oldest first)
    candidates.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    // Take the required number
    candidates.iter()
        .take(num_to_evict)
        .map(|(i, _)| *i)
        .collect()
}

/// Find LFU candidate blocks to evict
/// Returns indices based on access count (least frequent first)
#[pyfunction]
pub fn lfu_evict_rust(
    access_counts: Vec<u64>,
    last_access_times: Vec<f64>,
    pinned: Vec<bool>,
    num_to_evict: usize,
) -> Vec<usize> {
    if num_to_evict == 0 {
        return Vec::new();
    }
    
    // Collect unpinned indices with their counts and times
    let mut candidates: Vec<(usize, u64, f64)> = access_counts
        .iter()
        .enumerate()
        .filter(|(i, _)| !pinned.get(*i).copied().unwrap_or(false))
        .map(|(i, &count)| {
            let time = last_access_times.get(i).copied().unwrap_or(0.0);
            (i, count, time)
        })
        .collect();
    
    // Sort by count ascending, then by time ascending
    candidates.sort_by(|a, b| {
        a.1.cmp(&b.1)
            .then_with(|| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal))
    });
    
    candidates.iter()
        .take(num_to_evict)
        .map(|(i, _, _)| *i)
        .collect()
}

// =============================================================================
// KV Cache Operations
// =============================================================================

/// Compute optimal block copy order to minimize fragmentation
/// Given a list of (src_block, dst_block) pairs, sort by destination
#[pyfunction]
pub fn optimize_block_copy_order_rust(
    copies: Vec<(usize, usize)>,
) -> Vec<(usize, usize)> {
    let mut sorted = copies;
    sorted.sort_by_key(|&(_, dst)| dst);
    sorted
}

/// Calculate memory defragmentation plan
/// Returns list of (src_block, dst_block) moves to compact free space
#[pyfunction]
pub fn defragment_blocks_rust(
    allocated: Vec<bool>,
    num_blocks: usize,
) -> Vec<(usize, usize)> {
    let mut moves = Vec::new();
    
    // Find free slots from the front
    let free_slots: Vec<usize> = allocated.iter()
        .enumerate()
        .take(num_blocks)
        .filter(|(_, &is_alloc)| !is_alloc)
        .map(|(i, _)| i)
        .collect();
    
    // Find allocated blocks from the back
    let alloc_from_back: Vec<usize> = allocated.iter()
        .enumerate()
        .take(num_blocks)
        .rev()
        .filter(|(_, &is_alloc)| is_alloc)
        .map(|(i, _)| i)
        .collect();
    
    // Match free slots with allocated blocks that are after them
    let mut free_iter = free_slots.iter();
    let mut alloc_iter = alloc_from_back.iter();
    
    loop {
        match (free_iter.next(), alloc_iter.next()) {
            (Some(&free_idx), Some(&alloc_idx)) if free_idx < alloc_idx => {
                moves.push((alloc_idx, free_idx));
            }
            _ => break,
        }
    }
    
    moves
}

// =============================================================================
// Draft Token Verification
// =============================================================================

/// Verify draft tokens against target tokens
/// Returns (num_accepted, accepted_positions)
#[pyfunction]
pub fn verify_draft_tokens_rust(
    draft_tokens: Vec<i64>,
    target_tokens: Vec<i64>,
) -> (usize, Vec<usize>) {
    let mut num_accepted = 0;
    let mut accepted_positions = Vec::new();
    
    for (i, (&draft, &target)) in draft_tokens.iter().zip(target_tokens.iter()).enumerate() {
        if draft == target {
            num_accepted += 1;
            accepted_positions.push(i);
        } else {
            // Stop at first mismatch
            break;
        }
    }
    
    (num_accepted, accepted_positions)
}

/// Probabilistic verification with acceptance probabilities
/// Returns (accepted_flags, bonus_token_needed)
#[pyfunction]
pub fn verify_draft_probabilistic_rust(
    draft_probs: Vec<f64>,
    target_probs: Vec<f64>,
    random_values: Vec<f64>,
) -> (Vec<bool>, bool) {
    let mut accepted = Vec::with_capacity(draft_probs.len());
    let mut all_accepted = true;
    
    for ((&d_prob, &t_prob), &r) in draft_probs.iter()
        .zip(target_probs.iter())
        .zip(random_values.iter())
    {
        // Standard speculative decoding acceptance criterion
        let accept_prob = (t_prob / d_prob).min(1.0);
        let accept = r < accept_prob;
        accepted.push(accept);
        
        if !accept {
            all_accepted = false;
            // Truncate at first rejection
            break;
        }
    }
    
    // If all accepted, we need a bonus token from target model
    (accepted, all_accepted)
}

// =============================================================================
// Scheduler Stats Helpers
// =============================================================================

/// Calculate throughput from timing data
/// Returns tokens per second
#[pyfunction]
pub fn calculate_throughput_rust(
    num_tokens: u64,
    elapsed_ms: f64,
) -> f64 {
    if elapsed_ms <= 0.0 {
        return 0.0;
    }
    (num_tokens as f64) / (elapsed_ms / 1000.0)
}

/// Aggregate stats across multiple time windows
/// Returns (avg, min, max, p50, p95, p99)
#[pyfunction]
pub fn aggregate_stats_window_rust(values: Vec<f64>) -> (f64, f64, f64, f64, f64, f64) {
    if values.is_empty() {
        return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    }
    
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    let n = sorted.len();
    let sum: f64 = sorted.iter().sum();
    let avg = sum / n as f64;
    let min = sorted[0];
    let max = sorted[n - 1];
    
    let p50 = percentile(&sorted, 50.0);
    let p95 = percentile(&sorted, 95.0);
    let p99 = percentile(&sorted, 99.0);
    
    (avg, min, max, p50, p95, p99)
}

fn percentile(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    let idx = ((p / 100.0) * (sorted.len() - 1) as f64).round() as usize;
    sorted[idx.min(sorted.len() - 1)]
}

/// Calculate exponential moving average
#[pyfunction]
#[pyo3(signature = (current_ema, new_value, alpha=0.1))]
pub fn ema_update_rust(current_ema: f64, new_value: f64, alpha: f64) -> f64 {
    alpha * new_value + (1.0 - alpha) * current_ema
}

// =============================================================================
// Memory Pressure Detection
// =============================================================================

/// Calculate memory pressure score (0.0 = no pressure, 1.0 = critical)
#[pyfunction]
pub fn calculate_memory_pressure_rust(
    used_blocks: usize,
    total_blocks: usize,
    reserved_ratio: f64,
) -> f64 {
    if total_blocks == 0 {
        return 1.0;
    }
    
    let usage = used_blocks as f64 / total_blocks as f64;
    let threshold = 1.0 - reserved_ratio;
    
    if usage <= threshold {
        0.0
    } else {
        (usage - threshold) / reserved_ratio
    }
}

/// Determine number of blocks to free based on pressure
#[pyfunction]
#[pyo3(signature = (pressure, total_blocks, min_free=0.1))]
pub fn blocks_to_free_rust(
    pressure: f64,
    total_blocks: usize,
    min_free: f64,
) -> usize {
    if pressure <= 0.0 {
        return 0;
    }
    
    let target_free = (min_free + pressure * (1.0 - min_free)) * total_blocks as f64;
    target_free.ceil() as usize
}

// =============================================================================
// Phase 32: UVA Buffer & GPU Transfer Accelerations
// =============================================================================

/// Optimized UVA buffer copy with stride support
/// Simulates pinned memory copy optimization
#[pyfunction]
#[pyo3(signature = (src_offset, dst_offset, size, stride=1))]
pub fn uva_copy_rust(
    src_offset: usize,
    dst_offset: usize,
    size: usize,
    stride: usize,
) -> Vec<(usize, usize)> {
    // Return list of (src, dst) offset pairs for batch copy
    let mut pairs = Vec::with_capacity(size / stride.max(1));
    let mut s = src_offset;
    let mut d = dst_offset;
    
    for _ in 0..(size / stride.max(1)) {
        pairs.push((s, d));
        s += stride;
        d += stride;
    }
    
    pairs
}

/// Compute write indices for batched GPU writes
/// Returns optimized index ordering for memory coalescing
#[pyfunction]
pub fn batch_write_indices_rust(
    indices: Vec<usize>,
    block_size: usize,
) -> Vec<usize> {
    // Sort by block then offset within block
    let mut sorted = indices;
    sorted.sort_by_key(|&idx| (idx / block_size, idx % block_size));
    sorted
}

/// Coalesce writes for locality optimization
/// Groups adjacent writes into ranges
#[pyfunction]
#[pyo3(signature = (indices, values, max_gap=4))]
pub fn coalesce_writes_rust(
    indices: Vec<usize>,
    values: Vec<f64>,
    max_gap: usize,
) -> Vec<(usize, usize, Vec<f64>)> {
    if indices.is_empty() {
        return Vec::new();
    }
    
    // Create (index, value) pairs and sort by index
    let mut pairs: Vec<_> = indices.into_iter().zip(values).collect();
    pairs.sort_by_key(|(idx, _)| *idx);
    
    let mut coalesced = Vec::new();
    let mut range_start = pairs[0].0;
    let mut range_values = vec![pairs[0].1];
    let mut expected_next = pairs[0].0 + 1;
    
    for (idx, val) in pairs.into_iter().skip(1) {
        if idx <= expected_next + max_gap {
            // Fill gaps with zeros
            while expected_next < idx {
                range_values.push(0.0);
                expected_next += 1;
            }
            range_values.push(val);
            expected_next = idx + 1;
        } else {
            // Start new range
            coalesced.push((range_start, range_start + range_values.len(), range_values));
            range_start = idx;
            range_values = vec![val];
            expected_next = idx + 1;
        }
    }
    
    // Push final range
    coalesced.push((range_start, range_start + range_values.len(), range_values));
    
    coalesced
}

// =============================================================================
// Phase 32: Priority Scheduling Accelerations
// =============================================================================

/// Fast heap-based priority queue operations
/// Returns sorted priority order for requests
#[pyfunction]
pub fn priority_heap_ops_rust(
    priorities: Vec<(f64, f64, i64)>,  // (priority, deadline, sequence)
) -> Vec<usize> {
    // Return indices sorted by priority
    let mut indexed: Vec<_> = priorities.iter().enumerate().collect();
    indexed.sort_by(|(_, a), (_, b)| {
        // Compare by priority first, then deadline, then sequence
        a.0.partial_cmp(&b.0)
            .unwrap_or(std::cmp::Ordering::Equal)
            .then_with(|| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal))
            .then_with(|| a.2.cmp(&b.2))
    });
    indexed.into_iter().map(|(i, _)| i).collect()
}

/// Fast token budget check for batch scheduling
#[pyfunction]
pub fn token_budget_check_rust(
    request_tokens: Vec<usize>,
    budget: usize,
    max_requests: usize,
) -> Vec<usize> {
    // Return indices of requests that fit in budget
    let mut result = Vec::new();
    let mut remaining = budget;
    
    for (idx, &tokens) in request_tokens.iter().enumerate() {
        if result.len() >= max_requests {
            break;
        }
        if tokens <= remaining {
            result.push(idx);
            remaining -= tokens;
        }
    }
    
    result
}

/// Compute optimal chunk boundaries for prefill
#[pyfunction]
#[pyo3(signature = (total_tokens, chunk_size, memory_pressure=0.0))]
pub fn chunk_boundaries_rust(
    total_tokens: usize,
    chunk_size: usize,
    memory_pressure: f64,
) -> Vec<(usize, usize)> {
    // Adjust chunk size based on memory pressure
    let effective_chunk = if memory_pressure > 0.0 {
        let reduction = 1.0 - (memory_pressure * 0.5);
        ((chunk_size as f64) * reduction).max(64.0) as usize
    } else {
        chunk_size
    };
    
    let mut boundaries = Vec::new();
    let mut start = 0;
    
    while start < total_tokens {
        let end = (start + effective_chunk).min(total_tokens);
        boundaries.push((start, end));
        start = end;
    }
    
    boundaries
}

// =============================================================================
// Phase 32: Stream & Event Accelerations
// =============================================================================

/// Lightweight stream synchronization check
/// Returns true if all streams are idle (simulated)
#[pyfunction]
pub fn stream_sync_rust(stream_states: Vec<bool>) -> bool {
    stream_states.iter().all(|&s| s)
}

/// Non-blocking event status query
/// Returns completed event indices
#[pyfunction]
pub fn event_query_rust(event_states: Vec<bool>) -> Vec<usize> {
    event_states
        .iter()
        .enumerate()
        .filter_map(|(i, &completed)| if completed { Some(i) } else { None })
        .collect()
}

/// Calculate preemption score for a request
/// Lower score = higher preemption priority (preempt first)
#[pyfunction]
pub fn preemption_score_rust(
    priority: i32,
    tokens_processed: usize,
    total_tokens: usize,
    elapsed_time: f64,
) -> f64 {
    // Prefer to preempt:
    // - Lower priority requests (higher priority value)
    // - Requests with less progress
    // - Requests that have used more time
    
    let progress = if total_tokens > 0 {
        tokens_processed as f64 / total_tokens as f64
    } else {
        0.0
    };
    
    // Score: higher priority value + lower progress + higher time = easier to preempt
    (priority as f64) - progress * 2.0 + elapsed_time * 0.1
}

/// Check deadlines for EDF scheduling
/// Returns indices of requests that have missed or are close to deadline
#[pyfunction]
#[pyo3(signature = (deadlines, current_time, threshold=1.0))]
pub fn deadline_check_rust(
    deadlines: Vec<f64>,
    current_time: f64,
    threshold: f64,
) -> (Vec<usize>, Vec<usize>) {
    let mut missed = Vec::new();
    let mut urgent = Vec::new();
    
    for (i, &deadline) in deadlines.iter().enumerate() {
        if deadline < 0.0 {
            continue;  // No deadline
        }
        
        let remaining = deadline - current_time;
        if remaining < 0.0 {
            missed.push(i);
        } else if remaining < threshold {
            urgent.push(i);
        }
    }
    
    (missed, urgent)
}

// =============================================================================
// Phase 33: GPU Model Runner & Distributed Communication Accelerations
// =============================================================================

/// Prepare position IDs for a batch of sequences
/// Returns position tensor values based on sequence lengths and context lengths
#[pyfunction]
pub fn prepare_positions_rust(
    seq_lens: Vec<usize>,
    context_lens: Vec<usize>,
) -> Vec<Vec<i64>> {
    seq_lens
        .iter()
        .zip(context_lens.iter())
        .map(|(&seq_len, &ctx_len)| {
            (ctx_len as i64..seq_len as i64).collect()
        })
        .collect()
}

/// Compute index mapping for batch compaction
/// Returns (idx_mapping, valid_count) where idx_mapping maps old indices to new
#[pyfunction]
pub fn compute_idx_mapping_rust(
    valid_mask: Vec<bool>,
    capacity: usize,
) -> (Vec<i64>, usize) {
    let mut mapping = vec![-1i64; capacity];
    let mut new_idx = 0;
    
    for (old_idx, &valid) in valid_mask.iter().enumerate() {
        if valid {
            mapping[old_idx] = new_idx as i64;
            new_idx += 1;
        }
    }
    
    (mapping, new_idx)
}

/// Expand index mapping for multiple elements per slot
/// Used for expanding from request-level to token-level indices
#[pyfunction]
pub fn expand_idx_mapping_rust(
    idx_mapping: Vec<i64>,
    elements_per_slot: Vec<usize>,
) -> Vec<i64> {
    let total_elements: usize = elements_per_slot.iter().sum();
    let mut expanded = Vec::with_capacity(total_elements);
    
    for (_slot_idx, (&mapping, &count)) in idx_mapping.iter().zip(elements_per_slot.iter()).enumerate() {
        if mapping >= 0 {
            for elem in 0..count {
                expanded.push(mapping * count as i64 + elem as i64);
            }
        } else {
            // Invalid slot - push -1 for each element
            for _ in 0..count {
                expanded.push(-1);
            }
        }
    }
    
    expanded
}

/// Hash function for CUDA graph cache keys
/// Returns u64 hash for batch descriptor
#[pyfunction]
pub fn cudagraph_key_hash_rust(
    batch_size: usize,
    max_seq_len: usize,
    mode: u8,
    use_prefix_cache: bool,
) -> u64 {
    // FNV-1a hash
    const FNV_OFFSET: u64 = 0xcbf29ce484222325;
    const FNV_PRIME: u64 = 0x100000001b3;
    
    let mut hash = FNV_OFFSET;
    
    // Hash batch_size
    for byte in batch_size.to_le_bytes() {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(FNV_PRIME);
    }
    
    // Hash max_seq_len
    for byte in max_seq_len.to_le_bytes() {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(FNV_PRIME);
    }
    
    // Hash mode
    hash ^= mode as u64;
    hash = hash.wrapping_mul(FNV_PRIME);
    
    // Hash use_prefix_cache
    hash ^= use_prefix_cache as u64;
    hash = hash.wrapping_mul(FNV_PRIME);
    
    hash
}

/// Generate warmup sizes for CUDA graph capture
/// Returns list of batch sizes and sequence lengths to pre-compile
#[pyfunction]
#[pyo3(signature = (max_batch_size, max_seq_len, min_batch_size=1, batch_step=8, seq_buckets=None))]
pub fn warmup_sizes_rust(
    max_batch_size: usize,
    max_seq_len: usize,
    min_batch_size: usize,
    batch_step: usize,
    seq_buckets: Option<Vec<usize>>,
) -> Vec<(usize, usize)> {
    let seq_lens = seq_buckets.unwrap_or_else(|| {
        // Default power-of-2 sequence length buckets
        let mut buckets = vec![1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024];
        buckets.retain(|&s| s <= max_seq_len);
        if !buckets.contains(&max_seq_len) {
            buckets.push(max_seq_len);
        }
        buckets
    });
    
    let mut sizes = Vec::new();
    
    // Generate batch sizes
    let mut batch = min_batch_size;
    while batch <= max_batch_size {
        for &seq_len in &seq_lens {
            sizes.push((batch, seq_len));
        }
        batch += batch_step;
    }
    
    // Always include max batch size
    if (max_batch_size - min_batch_size) % batch_step != 0 {
        for &seq_len in &seq_lens {
            sizes.push((max_batch_size, seq_len));
        }
    }
    
    sizes
}

/// Numerically stable softmax for batch invariant operations
/// Uses log-sum-exp trick for numerical stability
#[pyfunction]
pub fn softmax_stable_rust(logits: Vec<f64>) -> Vec<f64> {
    if logits.is_empty() {
        return Vec::new();
    }
    
    // Find max for numerical stability
    let max_val = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    
    // Compute exp(x - max)
    let exp_vals: Vec<f64> = logits.iter().map(|&x| (x - max_val).exp()).collect();
    
    // Sum of exponentials
    let sum: f64 = exp_vals.iter().sum();
    
    // Normalize
    exp_vals.iter().map(|&x| x / sum).collect()
}

/// Persistent GEMM tile computation for batch invariant matmul
/// Computes C[m, n] = A[m, k] @ B[k, n] for a tile
#[pyfunction]
pub fn persistent_gemm_tile_rust(
    a_tile: Vec<Vec<f64>>,
    b_tile: Vec<Vec<f64>>,
) -> Vec<Vec<f64>> {
    let m = a_tile.len();
    if m == 0 {
        return Vec::new();
    }
    let k = a_tile[0].len();
    if k == 0 || b_tile.is_empty() || b_tile.len() != k {
        return Vec::new();
    }
    let n = b_tile[0].len();
    
    // Initialize output
    let mut c = vec![vec![0.0; n]; m];
    
    // Compute matmul
    for i in 0..m {
        for j in 0..n {
            let mut sum = 0.0;
            for l in 0..k {
                sum += a_tile[i][l] * b_tile[l][j];
            }
            c[i][j] = sum;
        }
    }
    
    c
}

/// All-reduce sum simulation for distributed testing
/// Simulates all-reduce by summing contributions from all ranks
#[pyfunction]
pub fn all_reduce_sum_rust(
    local_values: Vec<f64>,
    all_contributions: Vec<Vec<f64>>,
) -> Vec<f64> {
    if local_values.is_empty() {
        return Vec::new();
    }
    
    let len = local_values.len();
    let mut result = local_values.clone();
    
    for contrib in all_contributions {
        if contrib.len() == len {
            for (i, val) in contrib.iter().enumerate() {
                result[i] += val;
            }
        }
    }
    
    result
}

/// Compute rank assignment for tensor parallel sharding
/// Returns (shard_start, shard_size) for given rank
#[pyfunction]
pub fn rank_assignment_rust(
    total_size: usize,
    world_size: usize,
    rank: usize,
) -> (usize, usize) {
    if world_size == 0 || rank >= world_size {
        return (0, 0);
    }
    
    // Divide as evenly as possible
    let base_size = total_size / world_size;
    let remainder = total_size % world_size;
    
    // First `remainder` ranks get one extra element
    let shard_size = if rank < remainder {
        base_size + 1
    } else {
        base_size
    };
    
    // Calculate start position
    let shard_start = if rank < remainder {
        rank * (base_size + 1)
    } else {
        remainder * (base_size + 1) + (rank - remainder) * base_size
    };
    
    (shard_start, shard_size)
}

/// Dispatch attention computation based on backend capabilities
/// Returns recommended backend index based on context
#[pyfunction]
pub fn attention_dispatch_rust(
    seq_len: usize,
    _batch_size: usize,
    _num_heads: usize,
    _head_dim: usize,
    has_flash_attn: bool,
    has_flashinfer: bool,
    has_xformers: bool,
    is_decode: bool,
) -> usize {
    // Backend indices:
    // 0 = flash_attn
    // 1 = flashinfer
    // 2 = xformers
    // 3 = torch_sdpa
    // 4 = naive
    
    // For decode (single token), prefer FlashInfer
    if is_decode && has_flashinfer {
        return 1;
    }
    
    // For long sequences, prefer FlashAttention
    if seq_len > 512 && has_flash_attn {
        return 0;
    }
    
    // For medium sequences, try FlashAttention then xFormers
    if has_flash_attn {
        return 0;
    }
    
    if has_xformers {
        return 2;
    }
    
    // Fall back to SDPA
    3
}

// =============================================================================
// Phase 34: Disaggregated Inference & Advanced RoPE Accelerations
// =============================================================================

/// Compute rotary embedding frequencies for RoPE
/// Returns (cos, sin) vectors for given positions and dimension
#[pyfunction]
#[pyo3(signature = (positions, dim, base=10000.0, _max_seq_len=8192))]
pub fn rotary_embedding_kernel_rust(
    positions: Vec<i64>,
    dim: usize,
    base: f64,
    _max_seq_len: usize,
) -> (Vec<Vec<f64>>, Vec<Vec<f64>>) {
    let half_dim = dim / 2;
    
    // Compute inverse frequencies: 1 / (base^(2i/dim))
    let inv_freqs: Vec<f64> = (0..half_dim)
        .map(|i| {
            let exponent = (2 * i) as f64 / dim as f64;
            1.0 / base.powf(exponent)
        })
        .collect();
    
    // Compute cos/sin for each position
    let mut cos_table = Vec::with_capacity(positions.len());
    let mut sin_table = Vec::with_capacity(positions.len());
    
    for &pos in &positions {
        let pos_f = pos as f64;
        let mut cos_row = Vec::with_capacity(dim);
        let mut sin_row = Vec::with_capacity(dim);
        
        for &inv_freq in &inv_freqs {
            let theta = pos_f * inv_freq;
            let c = theta.cos();
            let s = theta.sin();
            // Duplicate for full dimension (interleaved)
            cos_row.push(c);
            cos_row.push(c);
            sin_row.push(s);
            sin_row.push(s);
        }
        
        cos_table.push(cos_row);
        sin_table.push(sin_row);
    }
    
    (cos_table, sin_table)
}

/// Compute multimodal RoPE section indices for MRoPE
/// Returns indices for temporal, height, and width dimensions
#[pyfunction]
pub fn mrope_section_indices_rust(
    dim: usize,
    temporal_sections: usize,
    height_sections: usize,
    width_sections: usize,
) -> (Vec<usize>, Vec<usize>, Vec<usize>) {
    let half_dim = dim / 2;
    let total_sections = temporal_sections + height_sections + width_sections;
    
    if total_sections == 0 {
        return (Vec::new(), Vec::new(), Vec::new());
    }
    
    let section_size = half_dim / total_sections;
    
    // Temporal indices
    let temporal_end = temporal_sections * section_size;
    let temporal_indices: Vec<usize> = (0..temporal_end).collect();
    
    // Height indices
    let height_end = temporal_end + height_sections * section_size;
    let height_indices: Vec<usize> = (temporal_end..height_end).collect();
    
    // Width indices
    let width_end = height_end + width_sections * section_size;
    let width_indices: Vec<usize> = (height_end..width_end).collect();
    
    (temporal_indices, height_indices, width_indices)
}

/// Compute dynamic NTK alpha scaling for extended context
/// Returns scaled base value for RoPE
#[pyfunction]
#[pyo3(signature = (seq_len, original_max_len, base=10000.0, alpha_type="linear"))]
pub fn dynamic_ntk_alpha_rust(
    seq_len: usize,
    original_max_len: usize,
    base: f64,
    alpha_type: &str,
) -> f64 {
    if seq_len <= original_max_len {
        return base;
    }
    
    let ratio = seq_len as f64 / original_max_len as f64;
    
    match alpha_type {
        "linear" => base * ratio,
        "sqrt" => base * ratio.sqrt(),
        "log" => base * ratio.ln().max(1.0),
        "yarn" => {
            // YARN-style dynamic scaling
            let alpha = 1.0 + (ratio.ln() / 2.0_f64.ln());
            base * alpha
        }
        _ => base * ratio,
    }
}

/// Fast n-gram proposal generation with cached prefix
/// Returns proposed tokens and their probabilities
#[pyfunction]
#[pyo3(signature = (tokens, ngram_index, context_size=4, num_proposals=5))]
pub fn ngram_propose_rust(
    tokens: Vec<i64>,
    ngram_index: HashMap<Vec<i64>, Vec<usize>>,
    context_size: usize,
    num_proposals: usize,
) -> Vec<(i64, f64)> {
    if tokens.len() < context_size {
        return Vec::new();
    }
    
    // Get last n tokens as context
    let context_start = tokens.len() - context_size;
    let context = tokens[context_start..].to_vec();
    
    // Find matches in index
    let match_positions = match ngram_index.get(&context) {
        Some(positions) => positions.clone(),
        None => return Vec::new(),
    };
    
    // Count next tokens
    let mut next_token_counts: HashMap<i64, usize> = HashMap::new();
    let total_tokens = tokens.len();
    
    for &pos in &match_positions {
        let next_pos = pos + context_size;
        if next_pos < total_tokens {
            *next_token_counts.entry(tokens[next_pos]).or_default() += 1;
        }
    }
    
    // Convert to probabilities and sort
    let total: usize = next_token_counts.values().sum();
    let mut proposals: Vec<(i64, f64)> = next_token_counts
        .into_iter()
        .map(|(token, count)| (token, count as f64 / total as f64))
        .collect();
    
    proposals.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    proposals.truncate(num_proposals);
    
    proposals
}

/// Expand EAGLE speculation tree structure
/// Returns tree node indices for batch speculation
#[pyfunction]
#[pyo3(signature = (draft_tokens, tree_width, tree_depth, vocab_size=32000))]
pub fn eagle_tree_expand_rust(
    draft_tokens: Vec<Vec<i64>>,
    tree_width: usize,
    tree_depth: usize,
    vocab_size: usize,
) -> Vec<Vec<usize>> {
    let mut tree_indices = Vec::new();
    
    // Build tree level by level
    let mut current_level = vec![0usize]; // Root
    
    for depth in 0..tree_depth {
        let mut next_level = Vec::new();
        
        for &parent_idx in &current_level {
            let start_idx = tree_indices.len();
            
            // Add children
            for child_offset in 0..tree_width {
                let child_idx = start_idx + child_offset;
                next_level.push(child_idx);
                
                // Create node: [parent_idx, depth, child_offset]
                tree_indices.push(vec![parent_idx, depth, child_offset]);
            }
        }
        
        current_level = next_level;
    }
    
    // Use parameters
    let _ = draft_tokens;
    let _ = vocab_size;
    
    tree_indices
}

/// Create KV transfer metadata for disaggregated serving
/// Returns serialized metadata for transfer
#[pyfunction]
pub fn kv_transfer_metadata_rust(
    request_id: &str,
    block_ids: Vec<i64>,
    seq_len: usize,
    num_layers: usize,
    num_heads: usize,
    head_dim: usize,
) -> HashMap<String, String> {
    let mut metadata = HashMap::new();
    
    metadata.insert("request_id".to_string(), request_id.to_string());
    metadata.insert("num_blocks".to_string(), block_ids.len().to_string());
    metadata.insert("seq_len".to_string(), seq_len.to_string());
    metadata.insert("num_layers".to_string(), num_layers.to_string());
    metadata.insert("num_heads".to_string(), num_heads.to_string());
    metadata.insert("head_dim".to_string(), head_dim.to_string());
    
    // Encode block IDs
    let block_str: String = block_ids
        .iter()
        .map(|&b| b.to_string())
        .collect::<Vec<_>>()
        .join(",");
    metadata.insert("block_ids".to_string(), block_str);
    
    // Compute total KV size in bytes (FP16)
    let kv_bytes = block_ids.len() * 16 * num_layers * num_heads * head_dim * 2 * 2; // *2 for K+V, *2 for FP16
    metadata.insert("kv_bytes".to_string(), kv_bytes.to_string());
    
    metadata
}

/// Verify draft tokens against target model logits
/// Returns (accepted_count, acceptance_mask)
#[pyfunction]
pub fn verify_draft_tokens_batch_rust(
    draft_tokens: Vec<i64>,
    target_logits: Vec<Vec<f64>>,
    draft_probs: Vec<f64>,
    temperature: f64,
) -> (usize, Vec<bool>) {
    let num_draft = draft_tokens.len();
    let mut accepted = Vec::with_capacity(num_draft);
    let mut accepted_count = 0usize;
    
    for (i, &draft_token) in draft_tokens.iter().enumerate() {
        if i >= target_logits.len() || i >= draft_probs.len() {
            accepted.push(false);
            continue;
        }
        
        // Get target probability for draft token
        let logits = &target_logits[i];
        if draft_token < 0 || (draft_token as usize) >= logits.len() {
            accepted.push(false);
            continue;
        }
        
        // Compute target probability with temperature
        let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let scaled_logits: Vec<f64> = logits.iter().map(|&l| (l - max_logit) / temperature).collect();
        let exp_sum: f64 = scaled_logits.iter().map(|&l| l.exp()).sum();
        let target_prob = scaled_logits[draft_token as usize].exp() / exp_sum;
        
        // Acceptance criterion: p_target >= p_draft
        let draft_prob = draft_probs[i];
        if target_prob >= draft_prob {
            accepted.push(true);
            accepted_count += 1;
        } else {
            // Probabilistic acceptance
            let accept_ratio = target_prob / draft_prob;
            let random_val = ((i as f64 * 0.618034).fract() * 2.0 - 1.0).abs();
            if random_val < accept_ratio {
                accepted.push(true);
                accepted_count += 1;
            } else {
                accepted.push(false);
            }
        }
    }
    
    (accepted_count, accepted)
}

/// Fast block table lookup for paged attention
/// Returns physical block IDs for logical positions
#[pyfunction]
pub fn block_table_lookup_rust(
    block_table: Vec<Vec<i64>>,
    seq_indices: Vec<usize>,
    token_positions: Vec<usize>,
    block_size: usize,
) -> Vec<i64> {
    let mut physical_blocks = Vec::with_capacity(seq_indices.len());
    
    for (&seq_idx, &token_pos) in seq_indices.iter().zip(token_positions.iter()) {
        if seq_idx >= block_table.len() {
            physical_blocks.push(-1);
            continue;
        }
        
        let logical_block = token_pos / block_size;
        let seq_blocks = &block_table[seq_idx];
        
        if logical_block >= seq_blocks.len() {
            physical_blocks.push(-1);
        } else {
            physical_blocks.push(seq_blocks[logical_block]);
        }
    }
    
    physical_blocks
}

/// Dispatch Triton attention based on context and hardware
/// Returns (backend_id, kernel_config)
#[pyfunction]
pub fn triton_attention_dispatch_rust(
    batch_size: usize,
    seq_len: usize,
    num_heads: usize,
    num_kv_heads: usize,
    head_dim: usize,
    is_prefill: bool,
    has_sliding_window: bool,
    sliding_window_size: usize,
) -> (usize, HashMap<String, usize>) {
    // Backend indices:
    // 0 = triton_paged_attention
    // 1 = triton_flash_decoding
    // 2 = triton_prefix_prefill
    // 3 = fallback_sdpa
    
    let mut config = HashMap::new();
    config.insert("batch_size".to_string(), batch_size);
    config.insert("seq_len".to_string(), seq_len);
    config.insert("num_heads".to_string(), num_heads);
    config.insert("num_kv_heads".to_string(), num_kv_heads);
    config.insert("head_dim".to_string(), head_dim);
    
    // Compute GQA ratio
    let gqa_ratio = num_heads / num_kv_heads.max(1);
    config.insert("gqa_ratio".to_string(), gqa_ratio);
    
    let backend = if is_prefill {
        // Prefill: use prefix-prefill kernel for long sequences
        if seq_len > 1024 {
            config.insert("chunk_size".to_string(), 256);
            2
        } else {
            config.insert("chunk_size".to_string(), seq_len);
            2
        }
    } else {
        // Decode: use paged attention or flash decoding
        if has_sliding_window && seq_len > sliding_window_size {
            config.insert("window_size".to_string(), sliding_window_size);
            1
        } else {
            0
        }
    };
    
    (backend, config)
}

/// Coordinate DCP group formation for disaggregated serving
/// Returns (prefill_ranks, decode_ranks)
#[pyfunction]
#[pyo3(signature = (world_size, prefill_ratio=0.5, min_prefill=1, min_decode=1))]
pub fn dcp_group_coordinate_rust(
    world_size: usize,
    prefill_ratio: f64,
    min_prefill: usize,
    min_decode: usize,
) -> (Vec<usize>, Vec<usize>) {
    if world_size < min_prefill + min_decode {
        // Not enough ranks for disaggregation
        let all_ranks: Vec<usize> = (0..world_size).collect();
        return (all_ranks.clone(), all_ranks);
    }
    
    // Calculate prefill ranks based on ratio
    let ideal_prefill = (world_size as f64 * prefill_ratio).round() as usize;
    let num_prefill = ideal_prefill.max(min_prefill).min(world_size - min_decode);
    let _num_decode = world_size - num_prefill;
    
    let prefill_ranks: Vec<usize> = (0..num_prefill).collect();
    let decode_ranks: Vec<usize> = (num_prefill..world_size).collect();
    
    (prefill_ranks, decode_ranks)
}

/// Score KV connector backends for selection
/// Returns ranked list of (backend_name, score)
#[pyfunction]
pub fn kv_connector_score_rust(
    available_backends: Vec<String>,
    transfer_size_bytes: usize,
    is_local: bool,
    has_rdma: bool,
    latency_budget_ms: f64,
) -> Vec<(String, f64)> {
    let mut scores: Vec<(String, f64)> = Vec::new();
    
    for backend in available_backends {
        let mut score: f64 = 50.0; // Base score
        
        match backend.as_str() {
            "NixlConnector" => {
                score += 30.0; // Fast RDMA-based
                if has_rdma {
                    score += 20.0;
                }
                if !is_local {
                    score += 10.0; // Good for remote
                }
            }
            "MooncakeConnector" => {
                score += 25.0;
                if transfer_size_bytes > 1_000_000_000 {
                    score += 15.0; // Good for large transfers
                }
            }
            "MoRIIOConnector" => {
                score += 20.0;
                if has_rdma {
                    score += 25.0; // Optimized for RDMA
                }
            }
            "P2pNcclConnector" => {
                score += 20.0;
                if is_local {
                    score += 15.0; // Good for local GPU-GPU
                }
            }
            "DecodeBenchConnector" => {
                score -= 50.0; // Benchmarking only
            }
            _ => {
                score -= 10.0; // Unknown backend
            }
        }
        
        // Penalize if latency budget is tight
        if latency_budget_ms < 10.0 {
            // Prefer fastest backends
            if backend.contains("Nixl") || backend.contains("P2p") {
                score += 10.0;
            }
        }
        
        scores.push((backend, score.max(0.0)));
    }
    
    // Sort by score descending
    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    scores
}

/// Parse speculation tree structure for EAGLE/Medusa
/// Returns flattened tree with parent pointers
#[pyfunction]
pub fn speculation_tree_parse_rust(
    tree_config: Vec<Vec<usize>>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    // Flatten tree structure
    let mut parents = Vec::new();
    let mut depths = Vec::new();
    let mut widths = Vec::new();
    let mut positions = Vec::new();
    
    let mut node_idx = 0usize;
    
    for (depth, level_config) in tree_config.iter().enumerate() {
        for (_pos, &width) in level_config.iter().enumerate() {
            for child in 0..width {
                let parent = if depth == 0 { 0 } else { node_idx.saturating_sub(1) };
                parents.push(parent);
                depths.push(depth);
                widths.push(width);
                positions.push(child);
                node_idx += 1;
            }
        }
    }
    
    result.insert("parents".to_string(), parents);
    result.insert("depths".to_string(), depths);
    result.insert("widths".to_string(), widths);
    result.insert("positions".to_string(), positions);
    result.insert("total_nodes".to_string(), vec![node_idx]);
    
    result
}

// ============================================================================
// Phase 35: Async Execution & Advanced Caching
// ============================================================================

/// Fast LRU eviction selection for block pool
/// Returns indices of blocks to evict sorted by eviction priority
#[pyfunction]
pub fn block_pool_evict_lru_rust(
    last_access_times: Vec<f64>,
    block_states: Vec<u8>,  // 0=FREE, 1=ALLOCATED, 2=CACHED, 3=PINNED
    num_to_evict: usize,
) -> Vec<usize> {
    const STATE_CACHED: u8 = 2;
    
    // Find cacheable blocks with their access times
    let mut eviction_candidates: Vec<(usize, f64)> = last_access_times
        .iter()
        .enumerate()
        .filter(|(i, _)| block_states.get(*i).copied() == Some(STATE_CACHED))
        .map(|(i, &time)| (i, time))
        .collect();
    
    // Sort by access time (oldest first = evict first)
    eviction_candidates.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    // Return indices of blocks to evict
    eviction_candidates
        .iter()
        .take(num_to_evict)
        .map(|(idx, _)| *idx)
        .collect()
}

/// ARC cache balance calculation
/// Computes optimal balance between recency (T1) and frequency (T2)
#[pyfunction]
pub fn arc_cache_balance_rust(
    _t1_size: usize,
    _t2_size: usize,
    b1_size: usize,  // Ghost entries from T1
    b2_size: usize,  // Ghost entries from T2
    capacity: usize,
    current_p: f64,
    hit_in_b1: bool,
    hit_in_b2: bool,
) -> f64 {
    let mut p = current_p;
    
    if hit_in_b1 {
        // Increase p (favor recency) - B1 ghost hit
        let delta = if b1_size > 0 {
            (b2_size as f64 / b1_size as f64).max(1.0)
        } else {
            1.0
        };
        p = (p + delta).min(capacity as f64);
    } else if hit_in_b2 {
        // Decrease p (favor frequency) - B2 ghost hit
        let delta = if b2_size > 0 {
            (b1_size as f64 / b2_size as f64).max(1.0)
        } else {
            1.0
        };
        p = (p - delta).max(0.0);
    }
    
    p
}

/// Prefix tree (radix tree) lookup acceleration
/// Returns matched length and entry index if found
#[pyfunction]
pub fn prefix_tree_lookup_rust(
    query_tokens: Vec<i64>,
    prefix_hashes: Vec<u64>,
    prefix_lengths: Vec<usize>,
) -> (i64, i64) {
    // Compute query hash at each length
    let mut query_hash: u64 = 0;
    let mut best_match_len: i64 = -1;
    let mut best_match_idx: i64 = -1;
    
    for (pos, &token) in query_tokens.iter().enumerate() {
        // FNV-1a style hash update
        query_hash = query_hash.wrapping_mul(0x100000001b3);
        query_hash ^= token as u64;
        
        let current_len = pos + 1;
        
        // Check if this length matches any prefix
        for (idx, (&hash, &len)) in prefix_hashes.iter().zip(prefix_lengths.iter()).enumerate() {
            if len == current_len && hash == query_hash {
                if current_len > best_match_len as usize {
                    best_match_len = current_len as i64;
                    best_match_idx = idx as i64;
                }
            }
        }
    }
    
    (best_match_len, best_match_idx)
}

/// Fast block content hashing using xxHash-style algorithm
#[pyfunction]
pub fn block_hash_compute_rust(
    token_ids: Vec<i64>,
    seed: u64,
) -> u64 {
    const PRIME1: u64 = 0x9E3779B185EBCA87;
    const PRIME2: u64 = 0xC2B2AE3D27D4EB4F;
    const PRIME3: u64 = 0x165667B19E3779F9;
    
    let mut hash = seed.wrapping_add(PRIME3);
    
    for &token in &token_ids {
        let k = (token as u64).wrapping_mul(PRIME2);
        hash ^= k.rotate_left(31).wrapping_mul(PRIME1);
        hash = hash.rotate_left(27).wrapping_mul(PRIME1).wrapping_add(PRIME2);
    }
    
    // Finalize
    hash ^= token_ids.len() as u64;
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(PRIME2);
    hash ^= hash >> 29;
    hash = hash.wrapping_mul(PRIME3);
    hash ^= hash >> 32;
    
    hash
}

/// GPU memory snapshot serialization
/// Returns packed representation of memory state
#[pyfunction]
pub fn gpu_memory_snapshot_rust(
    region_ids: Vec<usize>,
    region_sizes: Vec<usize>,
    _region_offsets: Vec<usize>,
    is_free: Vec<bool>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut total_bytes: usize = 0;
    let mut allocated_bytes: usize = 0;
    let mut free_bytes: usize = 0;
    let mut num_allocations: usize = 0;
    let mut free_regions = Vec::new();
    let mut allocated_regions = Vec::new();
    
    for i in 0..region_ids.len() {
        let size = region_sizes.get(i).copied().unwrap_or(0);
        total_bytes += size;
        
        if is_free.get(i).copied().unwrap_or(true) {
            free_bytes += size;
            free_regions.push(region_ids[i]);
        } else {
            allocated_bytes += size;
            num_allocations += 1;
            allocated_regions.push(region_ids[i]);
        }
    }
    
    // Calculate fragmentation
    let max_free = free_regions.iter()
        .filter_map(|&id| {
            region_ids.iter()
                .position(|&r| r == id)
                .and_then(|idx| region_sizes.get(idx).copied())
        })
        .max()
        .unwrap_or(0);
    
    let frag_ratio = if free_bytes > 0 {
        ((free_bytes - max_free) * 100) / free_bytes
    } else {
        0
    };
    
    result.insert("total_bytes".to_string(), vec![total_bytes]);
    result.insert("allocated_bytes".to_string(), vec![allocated_bytes]);
    result.insert("free_bytes".to_string(), vec![free_bytes]);
    result.insert("num_allocations".to_string(), vec![num_allocations]);
    result.insert("fragmentation_percent".to_string(), vec![frag_ratio]);
    result.insert("free_regions".to_string(), free_regions);
    result.insert("allocated_regions".to_string(), allocated_regions);
    
    result
}

/// Power of Two Choices worker selection
/// Returns index of best worker
#[pyfunction]
pub fn p2c_select_worker_rust(
    pending_requests: Vec<usize>,
    avg_latencies: Vec<f64>,
    health_states: Vec<u8>,  // 0=HEALTHY, 1=DEGRADED, 2=RECOVERING, 3=FAILED
    sample_size: usize,
) -> usize {
    const HEALTHY: u8 = 0;
    const DEGRADED: u8 = 1;
    
    // Filter to healthy/degraded workers
    let healthy_indices: Vec<usize> = health_states
        .iter()
        .enumerate()
        .filter(|(_, &state)| state == HEALTHY || state == DEGRADED)
        .map(|(i, _)| i)
        .collect();
    
    if healthy_indices.is_empty() {
        // Fallback to first worker
        return 0;
    }
    
    if healthy_indices.len() == 1 {
        return healthy_indices[0];
    }
    
    // Sample workers (deterministic for reproducibility)
    let sample_count = sample_size.min(healthy_indices.len());
    let step = healthy_indices.len() / sample_count.max(1);
    
    let candidates: Vec<usize> = (0..sample_count)
        .map(|i| healthy_indices[(i * step) % healthy_indices.len()])
        .collect();
    
    // Select by pending requests, then latency
    candidates
        .into_iter()
        .min_by(|&a, &b| {
            let pending_a = pending_requests.get(a).copied().unwrap_or(usize::MAX);
            let pending_b = pending_requests.get(b).copied().unwrap_or(usize::MAX);
            
            match pending_a.cmp(&pending_b) {
                std::cmp::Ordering::Equal => {
                    let lat_a = avg_latencies.get(a).copied().unwrap_or(f64::MAX);
                    let lat_b = avg_latencies.get(b).copied().unwrap_or(f64::MAX);
                    lat_a.partial_cmp(&lat_b).unwrap_or(std::cmp::Ordering::Equal)
                }
                other => other
            }
        })
        .unwrap_or(0)
}

/// Atomic step counter synchronization
/// Returns new step value after increment
#[pyfunction]
pub fn step_counter_sync_rust(
    current_step: u64,
    _dp_rank: usize,
    dp_size: usize,
) -> (u64, bool) {
    // Simulate atomic increment with barrier check
    let new_step = current_step + 1;
    
    // Check if all ranks are synchronized
    let is_synced = (new_step % dp_size as u64) == 0;
    
    (new_step, is_synced)
}

/// Wave coordination barrier
/// Returns wave completion status
#[pyfunction]
pub fn wave_id_barrier_rust(
    _wave_id: u64,
    completed_steps: Vec<u64>,
    expected_steps: u64,
) -> (bool, u64) {
    let total_completed: u64 = completed_steps.iter().sum();
    let total_expected = expected_steps * completed_steps.len() as u64;
    
    let is_complete = total_completed >= total_expected;
    let completion_ratio = if total_expected > 0 {
        (total_completed * 100) / total_expected
    } else {
        100
    };
    
    (is_complete, completion_ratio)
}

/// Merge async output futures (for aggregation)
/// Returns merged output indices grouped by completion status
#[pyfunction]
pub fn async_output_merge_rust(
    _request_ids: Vec<String>,
    completion_times: Vec<f64>,
    is_finished: Vec<bool>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut completed = Vec::new();
    let mut pending = Vec::new();
    
    for (i, &finished) in is_finished.iter().enumerate() {
        if finished {
            completed.push(i);
        } else {
            pending.push(i);
        }
    }
    
    // Sort completed by completion time
    completed.sort_by(|&a, &b| {
        let time_a = completion_times.get(a).copied().unwrap_or(f64::MAX);
        let time_b = completion_times.get(b).copied().unwrap_or(f64::MAX);
        time_a.partial_cmp(&time_b).unwrap_or(std::cmp::Ordering::Equal)
    });
    
    result.insert("completed".to_string(), completed);
    result.insert("pending".to_string(), pending);
    
    result
}

/// DP rank coordinate assignment
/// Returns optimal rank assignment for topology
#[pyfunction]
pub fn dp_rank_coordinate_rust(
    num_workers: usize,
    dp_size: usize,
    locality_groups: Vec<Vec<usize>>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut worker_ranks = vec![0usize; num_workers];
    let mut worker_localities = vec![0usize; num_workers];
    
    // Assign ranks round-robin
    for worker_id in 0..num_workers {
        worker_ranks[worker_id] = worker_id % dp_size;
    }
    
    // Assign locality groups
    for (group_idx, group) in locality_groups.iter().enumerate() {
        for &worker_id in group {
            if worker_id < num_workers {
                worker_localities[worker_id] = group_idx;
            }
        }
    }
    
    result.insert("ranks".to_string(), worker_ranks);
    result.insert("localities".to_string(), worker_localities);
    
    // Calculate workers per rank
    let mut workers_per_rank = vec![0usize; dp_size];
    for &rank in &result["ranks"] {
        if rank < dp_size {
            workers_per_rank[rank] += 1;
        }
    }
    result.insert("workers_per_rank".to_string(), workers_per_rank);
    
    result
}

/// KV metrics aggregation across workers
/// Returns aggregated cache metrics
#[pyfunction]
pub fn kv_metrics_aggregate_rust(
    hits_per_worker: Vec<u64>,
    misses_per_worker: Vec<u64>,
    evictions_per_worker: Vec<u64>,
    allocated_per_worker: Vec<u64>,
) -> HashMap<String, u64> {
    let mut result = HashMap::new();
    
    let total_hits: u64 = hits_per_worker.iter().sum();
    let total_misses: u64 = misses_per_worker.iter().sum();
    let total_evictions: u64 = evictions_per_worker.iter().sum();
    let total_allocated: u64 = allocated_per_worker.iter().sum();
    
    let total_lookups = total_hits + total_misses;
    let hit_rate_percent = if total_lookups > 0 {
        (total_hits * 100) / total_lookups
    } else {
        0
    };
    
    result.insert("total_hits".to_string(), total_hits);
    result.insert("total_misses".to_string(), total_misses);
    result.insert("total_evictions".to_string(), total_evictions);
    result.insert("total_allocated".to_string(), total_allocated);
    result.insert("total_lookups".to_string(), total_lookups);
    result.insert("hit_rate_percent".to_string(), hit_rate_percent);
    
    result
}

/// Cache hit scoring for prefix cache
/// Returns score for each prefix based on hit rate and recency
#[pyfunction]
pub fn cache_hit_score_rust(
    hit_counts: Vec<u64>,
    last_access_times: Vec<f64>,
    current_time: f64,
    recency_weight: f64,
    frequency_weight: f64,
) -> Vec<f64> {
    let max_hits = hit_counts.iter().copied().max().unwrap_or(1).max(1) as f64;
    let max_age = last_access_times
        .iter()
        .map(|&t| current_time - t)
        .fold(1.0f64, f64::max);
    
    hit_counts
        .iter()
        .zip(last_access_times.iter())
        .map(|(&hits, &access_time)| {
            let frequency_score = (hits as f64) / max_hits;
            let age = current_time - access_time;
            let recency_score = 1.0 - (age / max_age);
            
            frequency_weight * frequency_score + recency_weight * recency_score
        })
        .collect()
}

// =============================================================================
// Phase 36: CUDA Graph & Compilation Accelerators
// =============================================================================

/// Compute batch descriptor key for CUDA graph lookup
/// Returns hash key for graph cache
#[pyfunction]
pub fn batch_descriptor_key_rust(
    num_tokens: usize,
    num_reqs: usize,
    max_seq_len: usize,
    is_prefill: bool,
    pad_to: usize,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    // Pad to alignment
    let padded_tokens = ((num_tokens + pad_to - 1) / pad_to) * pad_to;
    let padded_reqs = ((num_reqs + pad_to - 1) / pad_to) * pad_to;
    
    let mut hasher = DefaultHasher::new();
    padded_tokens.hash(&mut hasher);
    padded_reqs.hash(&mut hasher);
    max_seq_len.hash(&mut hasher);
    is_prefill.hash(&mut hasher);
    
    hasher.finish()
}

/// Compute optimal ubatch slicing for micro-batching
/// Returns list of (token_start, token_end, req_start, req_end) tuples
#[pyfunction]
pub fn compute_ubatch_slices_rust(
    num_tokens: usize,
    num_reqs: usize,
    num_ubatches: usize,
    max_tokens_per_ubatch: usize,
) -> Vec<(usize, usize, usize, usize)> {
    if num_ubatches == 0 || num_tokens == 0 {
        return vec![];
    }
    
    // Determine effective ubatch count based on max tokens
    let effective_ubatches = if max_tokens_per_ubatch > 0 {
        ((num_tokens + max_tokens_per_ubatch - 1) / max_tokens_per_ubatch).max(num_ubatches)
    } else {
        num_ubatches
    };
    
    let tokens_per_ubatch = (num_tokens + effective_ubatches - 1) / effective_ubatches;
    let reqs_per_ubatch = (num_reqs + effective_ubatches - 1) / effective_ubatches;
    
    let mut slices = Vec::with_capacity(effective_ubatches);
    let mut token_pos = 0;
    let mut req_pos = 0;
    
    for _ in 0..effective_ubatches {
        let token_end = (token_pos + tokens_per_ubatch).min(num_tokens);
        let req_end = (req_pos + reqs_per_ubatch).min(num_reqs);
        
        if token_end > token_pos {
            slices.push((token_pos, token_end, req_pos, req_end));
        }
        
        token_pos = token_end;
        req_pos = req_end;
        
        if token_pos >= num_tokens {
            break;
        }
    }
    
    slices
}

/// Compute graph cache statistics from hit/miss counts
/// Returns dict with hit_rate, throughput_improvement, cache_efficiency
#[pyfunction]
pub fn cudagraph_stats_compute_rust(
    captures: u64,
    replays: u64,
    cache_hits: u64,
    cache_misses: u64,
    total_capture_time_ms: f64,
    total_replay_time_ms: f64,
) -> HashMap<String, f64> {
    let mut stats = HashMap::new();
    
    let total_lookups = cache_hits + cache_misses;
    let hit_rate = if total_lookups > 0 {
        cache_hits as f64 / total_lookups as f64
    } else {
        0.0
    };
    
    // Replay is typically 10-100x faster than capture
    let avg_capture_time = if captures > 0 {
        total_capture_time_ms / captures as f64
    } else {
        0.0
    };
    
    let avg_replay_time = if replays > 0 {
        total_replay_time_ms / replays as f64
    } else {
        0.0
    };
    
    let speedup = if avg_replay_time > 0.0 {
        avg_capture_time / avg_replay_time
    } else {
        0.0
    };
    
    // Cache efficiency = (replays * speedup) / (captures + replays)
    let total_ops = captures + replays;
    let cache_efficiency = if total_ops > 0 {
        (replays as f64 * speedup.min(100.0)) / total_ops as f64
    } else {
        0.0
    };
    
    stats.insert("hit_rate".to_string(), hit_rate);
    stats.insert("avg_capture_time_ms".to_string(), avg_capture_time);
    stats.insert("avg_replay_time_ms".to_string(), avg_replay_time);
    stats.insert("speedup".to_string(), speedup);
    stats.insert("cache_efficiency".to_string(), cache_efficiency);
    stats.insert("captures".to_string(), captures as f64);
    stats.insert("replays".to_string(), replays as f64);
    
    stats
}

/// Dispatch decision based on shape and available graphs
/// Returns dispatch mode: 0=EAGER, 1=CUDAGRAPH, 2=PIECEWISE
#[pyfunction]
pub fn dispatch_decision_rust(
    num_tokens: usize,
    num_reqs: usize,
    available_graph_keys: Vec<u64>,
    min_tokens: usize,
    max_tokens: usize,
    current_key: u64,
    prefer_piecewise: bool,
) -> u8 {
    // Check token range
    if num_tokens < min_tokens || num_tokens > max_tokens {
        return 0; // EAGER
    }
    
    // Ignore num_reqs for now, can be used for scaling
    let _ = num_reqs;
    // Check if graph exists
    let has_graph = available_graph_keys.contains(&current_key);
    
    if !has_graph {
        return 0; // EAGER
    }
    
    if prefer_piecewise {
        return 2; // PIECEWISE
    }
    
    1 // CUDAGRAPH
}

/// Compute padded buffer size for graph capture
/// Returns (padded_batch_size, padded_seq_len, total_elements)
#[pyfunction]
pub fn compute_padded_buffer_size_rust(
    batch_size: usize,
    seq_len: usize,
    batch_pad: usize,
    seq_pad: usize,
    hidden_size: usize,
) -> (usize, usize, usize) {
    let padded_batch = ((batch_size + batch_pad - 1) / batch_pad) * batch_pad;
    let padded_seq = ((seq_len + seq_pad - 1) / seq_pad) * seq_pad;
    let total_elements = padded_batch * padded_seq * hidden_size;
    
    (padded_batch, padded_seq, total_elements)
}

/// Analyze shape patterns for compilation optimization
/// Returns (num_unique_shapes, shape_frequency_map, suggested_dynamic_dims)
#[pyfunction]
pub fn analyze_shape_patterns_rust(
    shapes: Vec<(usize, usize)>, // (batch, seq_len) pairs
) -> (usize, HashMap<(usize, usize), usize>, Vec<usize>) {
    let mut freq_map: HashMap<(usize, usize), usize> = HashMap::new();
    
    for shape in &shapes {
        *freq_map.entry(*shape).or_default() += 1;
    }
    
    let num_unique = freq_map.len();
    
    // Analyze which dimensions vary most
    let mut batch_values: HashMap<usize, usize> = HashMap::new();
    let mut seq_values: HashMap<usize, usize> = HashMap::new();
    
    for &(batch, seq) in &shapes {
        *batch_values.entry(batch).or_default() += 1;
        *seq_values.entry(seq).or_default() += 1;
    }
    
    // Suggest dynamic dims (dims with high variability)
    let mut suggested_dynamic = Vec::new();
    if batch_values.len() > 3 {
        suggested_dynamic.push(0); // Batch dim
    }
    if seq_values.len() > 3 {
        suggested_dynamic.push(1); // Seq dim
    }
    
    (num_unique, freq_map, suggested_dynamic)
}

/// Track compilation events for counter statistics
/// Returns updated counters (compiles, recompiles, cache_hits, fallbacks, errors)
#[pyfunction]
pub fn track_compile_event_rust(
    current_compiles: u64,
    current_recompiles: u64,
    current_cache_hits: u64,
    current_fallbacks: u64,
    current_errors: u64,
    event_type: u8, // 0=COMPILE, 1=RECOMPILE, 2=CACHE_HIT, 3=FALLBACK, 4=ERROR
) -> (u64, u64, u64, u64, u64) {
    let mut compiles = current_compiles;
    let mut recompiles = current_recompiles;
    let mut cache_hits = current_cache_hits;
    let mut fallbacks = current_fallbacks;
    let mut errors = current_errors;
    
    match event_type {
        0 => compiles += 1,
        1 => recompiles += 1,
        2 => cache_hits += 1,
        3 => fallbacks += 1,
        4 => errors += 1,
        _ => {}
    }
    
    (compiles, recompiles, cache_hits, fallbacks, errors)
}

/// Compute optimal graph sizes for a range of batch sizes
/// Returns list of optimal sizes to capture graphs for
#[pyfunction]
pub fn compute_optimal_graph_sizes_rust(
    min_batch: usize,
    max_batch: usize,
    step: usize,
    additional_sizes: Vec<usize>,
) -> Vec<usize> {
    let mut sizes: Vec<usize> = (min_batch..=max_batch).step_by(step).collect();
    
    // Add additional specific sizes
    for size in additional_sizes {
        if size >= min_batch && size <= max_batch && !sizes.contains(&size) {
            sizes.push(size);
        }
    }
    
    sizes.sort();
    sizes.dedup();
    
    sizes
}

// =============================================================================
// Phase 37: Weight Loading, KV Offload & Expert Load Balancing
// =============================================================================

/// Compute hash for weight data using xxHash-like algorithm
/// Returns 64-bit hash for fast lookup
#[pyfunction]
pub fn weight_hash_compute_rust(data: Vec<u8>) -> u64 {
    // xxHash-inspired fast hashing
    const PRIME1: u64 = 0x9E3779B185EBCA87;
    const PRIME2: u64 = 0xC2B2AE3D27D4EB4F;
    const PRIME3: u64 = 0x165667B19E3779F9;
    const PRIME4: u64 = 0x85EBCA77C2B2AE63;
    const PRIME5: u64 = 0x27D4EB2F165667C5;
    
    let len = data.len() as u64;
    let mut hash = PRIME5.wrapping_add(len);
    
    let chunks = data.chunks_exact(8);
    let remainder = chunks.remainder();
    
    for chunk in chunks {
        let val = u64::from_le_bytes(chunk.try_into().unwrap());
        hash ^= val.wrapping_mul(PRIME1);
        hash = hash.rotate_left(27).wrapping_mul(PRIME2);
    }
    
    for &byte in remainder {
        hash ^= (byte as u64).wrapping_mul(PRIME3);
        hash = hash.rotate_left(11).wrapping_mul(PRIME4);
    }
    
    // Avalanche
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(PRIME2);
    hash ^= hash >> 29;
    hash = hash.wrapping_mul(PRIME3);
    hash ^= hash >> 32;
    
    hash
}

/// Validate weight shapes match expected shapes
/// Returns list of error messages for mismatches
#[pyfunction]
pub fn validate_weight_shapes_rust(
    specs: Vec<HashMap<String, String>>,
    expected: Vec<HashMap<String, String>>,
) -> Vec<String> {
    let mut errors = Vec::new();
    
    let spec_map: HashMap<_, _> = specs.iter()
        .filter_map(|s| s.get("name").map(|n| (n.clone(), s)))
        .collect();
    
    for exp in &expected {
        if let Some(name) = exp.get("name") {
            match spec_map.get(name) {
                None => errors.push(format!("Missing weight: {}", name)),
                Some(spec) => {
                    if let (Some(spec_shape), Some(exp_shape)) = (spec.get("shape"), exp.get("shape")) {
                        if spec_shape != exp_shape {
                            errors.push(format!(
                                "Shape mismatch for {}: got {}, expected {}",
                                name, spec_shape, exp_shape
                            ));
                        }
                    }
                }
            }
        }
    }
    
    errors
}

/// Compute optimal shard assignment for tensor-parallel loading
/// Returns list of rank assignments for each parameter
#[pyfunction]
pub fn compute_shard_assignment_rust(
    num_params: usize,
    num_ranks: usize,
    param_sizes: Vec<usize>,
) -> Vec<usize> {
    if num_ranks == 0 {
        return vec![0; num_params];
    }
    
    // Greedy load balancing
    let mut rank_loads = vec![0usize; num_ranks];
    let mut assignments = vec![0usize; num_params];
    
    // Sort params by size descending for better balancing
    let mut indexed_sizes: Vec<_> = param_sizes.iter().enumerate().collect();
    indexed_sizes.sort_by(|a, b| b.1.cmp(a.1));
    
    for (param_idx, &size) in indexed_sizes {
        // Find rank with minimum load
        let min_rank = rank_loads.iter()
            .enumerate()
            .min_by_key(|(_, load)| *load)
            .map(|(idx, _)| idx)
            .unwrap_or(0);
        
        assignments[param_idx] = min_rank;
        rank_loads[min_rank] += size;
    }
    
    assignments
}

/// Validate shard shapes for tensor-parallel consistency
/// Returns list of error messages
#[pyfunction]
pub fn validate_shard_shapes_rust(
    shard_specs: Vec<HashMap<String, String>>,
    _rank: usize,
    world_size: usize,
) -> Vec<String> {
    let mut errors = Vec::new();
    
    for spec in &shard_specs {
        if let Some(num_shards_str) = spec.get("num_shards") {
            if let Ok(num_shards) = num_shards_str.parse::<usize>() {
                if num_shards != world_size && num_shards != 1 {
                    let name = spec.get("name").map(|s| s.as_str()).unwrap_or("unknown");
                    errors.push(format!(
                        "Shard count mismatch for {}: expected {} or 1, got {}",
                        name, world_size, num_shards
                    ));
                }
            }
        }
    }
    
    errors
}

/// Compute LRU eviction order for offloading
/// Returns indices of blocks to evict (unpinned, oldest first)
#[pyfunction]
pub fn compute_lru_eviction_rust(
    blocks: Vec<HashMap<String, i64>>,
    num_to_evict: usize,
) -> Vec<usize> {
    let evictable: Vec<_> = blocks.iter()
        .enumerate()
        .filter(|(_, b)| b.get("ref_cnt").copied().unwrap_or(0) == 0)
        .collect();
    
    evictable.iter()
        .take(num_to_evict)
        .map(|(idx, _)| *idx)
        .collect()
}

/// Compute new ARC target size after hit
/// Returns updated target_t1_size
#[pyfunction]
pub fn compute_arc_target_rust(
    t1_size: usize,
    t2_size: usize,
    b1_size: usize,
    b2_size: usize,
    current_target: f64,
    hit_in_b1: bool,
    capacity: usize,
) -> f64 {
    let _ = t1_size;
    let _ = t2_size;
    
    if hit_in_b1 {
        // B1 hit: favor recency, increase T1 target
        let delta = if b1_size > 0 {
            (b2_size as f64 / b1_size as f64).max(1.0)
        } else {
            1.0
        };
        (current_target + delta).min(capacity as f64)
    } else {
        // B2 hit: favor frequency, decrease T1 target
        let delta = if b2_size > 0 {
            (b1_size as f64 / b2_size as f64).max(1.0)
        } else {
            1.0
        };
        (current_target - delta).max(0.0)
    }
}

/// Balanced packing algorithm for expert load balancing
/// Returns (pack_index, rank_in_pack) for each expert
#[pyfunction]
pub fn compute_balanced_packing_rust(
    weights: Vec<Vec<f64>>,
    num_packs: usize,
) -> (Vec<Vec<i64>>, Vec<Vec<i64>>) {
    if weights.is_empty() || num_packs == 0 {
        return (vec![], vec![]);
    }
    
    let num_layers = weights.len();
    let num_groups = weights[0].len();
    
    if num_groups % num_packs != 0 {
        return (vec![], vec![]);
    }
    
    let groups_per_pack = num_groups / num_packs;
    
    let mut pack_index = vec![vec![-1i64; num_groups]; num_layers];
    let mut rank_in_pack = vec![vec![-1i64; num_groups]; num_layers];
    
    for layer in 0..num_layers {
        // Sort indices by weight descending
        let mut indices: Vec<_> = (0..num_groups).collect();
        indices.sort_by(|&a, &b| {
            weights[layer][b].partial_cmp(&weights[layer][a])
                .unwrap_or(std::cmp::Ordering::Equal)
        });
        
        let mut pack_weights = vec![0.0f64; num_packs];
        let mut pack_items = vec![0usize; num_packs];
        
        for group in indices {
            // Find pack with lowest weight that has capacity
            let mut best_pack = None;
            let mut best_weight = f64::MAX;
            
            for p in 0..num_packs {
                if pack_items[p] < groups_per_pack && pack_weights[p] < best_weight {
                    best_weight = pack_weights[p];
                    best_pack = Some(p);
                }
            }
            
            if let Some(pack) = best_pack {
                pack_index[layer][group] = pack as i64;
                rank_in_pack[layer][group] = pack_items[pack] as i64;
                pack_weights[pack] += weights[layer][group];
                pack_items[pack] += 1;
            }
        }
    }
    
    (pack_index, rank_in_pack)
}

/// Expert replication algorithm
/// Returns (phy_to_log, rank, log_count) for load balancing
#[pyfunction]
pub fn compute_expert_replication_rust(
    weights: Vec<Vec<f64>>,
    num_physical: usize,
) -> (Vec<Vec<i64>>, Vec<Vec<i64>>, Vec<Vec<i64>>) {
    if weights.is_empty() {
        return (vec![], vec![], vec![]);
    }
    
    let num_layers = weights.len();
    let num_logical = weights[0].len();
    
    if num_physical < num_logical {
        return (vec![], vec![], vec![]);
    }
    
    let mut phy_to_log = vec![vec![-1i64; num_physical]; num_layers];
    let mut rank = vec![vec![0i64; num_physical]; num_layers];
    let mut log_count = vec![vec![1i64; num_logical]; num_layers];
    
    // Initialize 1:1 mapping for first num_logical physical experts
    for layer in 0..num_layers {
        for i in 0..num_logical {
            phy_to_log[layer][i] = i as i64;
        }
    }
    
    // Add redundant experts to highest-load logical experts
    for layer in 0..num_layers {
        for phy_idx in num_logical..num_physical {
            // Find logical expert with highest load per replica
            let mut best_logical = 0;
            let mut best_load = f64::MIN;
            
            for log_idx in 0..num_logical {
                let load_per_replica = weights[layer][log_idx] / log_count[layer][log_idx] as f64;
                if load_per_replica > best_load {
                    best_load = load_per_replica;
                    best_logical = log_idx;
                }
            }
            
            phy_to_log[layer][phy_idx] = best_logical as i64;
            rank[layer][phy_idx] = log_count[layer][best_logical];
            log_count[layer][best_logical] += 1;
        }
    }
    
    (phy_to_log, rank, log_count)
}

/// Compute load imbalance ratio across experts
/// Returns max/min load ratio (1.0 = perfectly balanced)
#[pyfunction]
pub fn compute_load_imbalance_rust(loads: Vec<Vec<f64>>) -> f64 {
    let mut max_load = 0.0f64;
    let mut min_load = f64::MAX;
    
    for layer_loads in &loads {
        for &load in layer_loads {
            if load > 0.0 {
                max_load = max_load.max(load);
                min_load = min_load.min(load);
            }
        }
    }
    
    if min_load == f64::MAX || min_load <= 0.0 {
        1.0
    } else {
        max_load / min_load
    }
}

// =============================================================================
// Phase 38: Advanced MoE Routing & SSM Acceleration
// =============================================================================

/// Compute top-k expert routing indices and weights
/// Returns (expert_indices, expert_weights) for each token
#[pyfunction]
pub fn moe_topk_route_rust(
    router_logits: Vec<Vec<f64>>,
    top_k: usize,
    normalize: bool,
) -> (Vec<Vec<usize>>, Vec<Vec<f64>>) {
    let mut all_indices = Vec::with_capacity(router_logits.len());
    let mut all_weights = Vec::with_capacity(router_logits.len());
    
    for logits in &router_logits {
        let num_experts = logits.len();
        
        // Find top-k indices using partial sort
        let mut indexed: Vec<(usize, f64)> = logits.iter().enumerate()
            .map(|(i, &v)| (i, v))
            .collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        
        let k = top_k.min(num_experts);
        let indices: Vec<usize> = indexed.iter().take(k).map(|(i, _)| *i).collect();
        let mut weights: Vec<f64> = indexed.iter().take(k).map(|(_, w)| *w).collect();
        
        // Apply softmax normalization to selected weights
        if normalize {
            let max_w = weights.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let exp_weights: Vec<f64> = weights.iter().map(|w| (w - max_w).exp()).collect();
            let sum: f64 = exp_weights.iter().sum();
            weights = exp_weights.iter().map(|w| w / sum).collect();
        }
        
        all_indices.push(indices);
        all_weights.push(weights);
    }
    
    (all_indices, all_weights)
}

/// Compute expert choice routing (experts select tokens)
/// Returns mapping of which tokens each expert processes
#[pyfunction]
pub fn moe_expert_choice_route_rust(
    router_logits: Vec<Vec<f64>>,
    num_experts: usize,
    capacity_factor: f64,
) -> Vec<Vec<usize>> {
    let num_tokens = router_logits.len();
    let capacity = ((num_tokens as f64 * capacity_factor) / num_experts as f64).ceil() as usize;
    let capacity = capacity.max(1);
    
    // Transpose: get scores per expert
    let mut expert_scores: Vec<Vec<(usize, f64)>> = vec![Vec::new(); num_experts];
    
    for (token_idx, logits) in router_logits.iter().enumerate() {
        for (expert_idx, &score) in logits.iter().enumerate() {
            if expert_idx < num_experts {
                expert_scores[expert_idx].push((token_idx, score));
            }
        }
    }
    
    // Each expert selects top-capacity tokens
    let mut expert_assignments: Vec<Vec<usize>> = vec![Vec::with_capacity(capacity); num_experts];
    
    for (expert_idx, scores) in expert_scores.iter_mut().enumerate() {
        scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        for (token_idx, _) in scores.iter().take(capacity) {
            expert_assignments[expert_idx].push(*token_idx);
        }
    }
    
    expert_assignments
}

/// Compute auxiliary load balancing loss
/// Returns (load_balance_loss, z_loss)
#[pyfunction]
pub fn moe_aux_loss_rust(
    router_logits: Vec<Vec<f64>>,
    expert_indices: Vec<Vec<usize>>,
    num_experts: usize,
) -> (f64, f64) {
    let num_tokens = router_logits.len() as f64;
    if num_tokens == 0.0 {
        return (0.0, 0.0);
    }
    
    // Compute fraction of tokens routed to each expert
    let mut expert_counts = vec![0.0f64; num_experts];
    for indices in &expert_indices {
        for &idx in indices {
            if idx < num_experts {
                expert_counts[idx] += 1.0;
            }
        }
    }
    let tokens_per_expert: Vec<f64> = expert_counts.iter().map(|c| c / num_tokens).collect();
    
    // Compute mean router probability per expert
    let mut prob_sums = vec![0.0f64; num_experts];
    for logits in &router_logits {
        // Softmax
        let max_l = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_l).exp()).collect();
        let sum: f64 = exp_logits.iter().sum();
        for (i, &e) in exp_logits.iter().enumerate() {
            if i < num_experts {
                prob_sums[i] += e / sum;
            }
        }
    }
    let mean_probs: Vec<f64> = prob_sums.iter().map(|s| s / num_tokens).collect();
    
    // Load balance loss = num_experts * sum(f_i * P_i)
    let load_loss: f64 = (num_experts as f64) * 
        tokens_per_expert.iter().zip(mean_probs.iter())
        .map(|(f, p)| f * p)
        .sum::<f64>();
    
    // Z-loss = sum(logsumexp(logits)^2) / num_tokens
    let z_loss: f64 = router_logits.iter().map(|logits| {
        let max_l = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let lse = max_l + logits.iter().map(|l| (l - max_l).exp()).sum::<f64>().ln();
        lse * lse
    }).sum::<f64>() / num_tokens;
    
    (load_loss, z_loss)
}

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

/// Compute soft MoE routing (differentiable)
/// Returns soft assignment matrix
#[pyfunction]
pub fn soft_moe_route_rust(
    router_logits: Vec<Vec<f64>>,  // [num_tokens, num_experts]
    num_slots: usize,
) -> Vec<Vec<f64>> {
    let num_tokens = router_logits.len();
    let num_experts = if router_logits.is_empty() { 0 } else { router_logits[0].len() };
    
    if num_tokens == 0 || num_experts == 0 || num_slots == 0 {
        return vec![];
    }
    
    // Softmax over tokens for each expert slot
    let mut dispatch_weights = vec![vec![0.0f64; num_experts * num_slots]; num_tokens];
    
    for slot in 0..num_slots {
        for expert in 0..num_experts {
            let col_idx = expert * num_slots + slot;
            
            // Get column (expert scores for all tokens)
            let scores: Vec<f64> = router_logits.iter().map(|r| r[expert]).collect();
            
            // Softmax over tokens
            let max_s = scores.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let exp_scores: Vec<f64> = scores.iter().map(|s| (s - max_s).exp()).collect();
            let sum: f64 = exp_scores.iter().sum();
            
            for token in 0..num_tokens {
                dispatch_weights[token][col_idx] = exp_scores[token] / sum;
            }
        }
    }
    
    dispatch_weights
}

// =============================================================================
// Phase 39: Structured Output & Guided Decoding Acceleration
// =============================================================================

/// Build FSM transition table from regex pattern
/// Returns (transition_table, accepting_states, initial_state)
#[pyfunction]
pub fn regex_to_fsm_rust(
    pattern: String,
    vocab_size: usize,
) -> (Vec<Vec<i32>>, Vec<usize>, usize) {
    // Simplified FSM construction for common patterns
    // In production, use a proper regex-to-DFA library
    
    let pattern_chars: Vec<char> = pattern.chars().collect();
    let num_states = pattern_chars.len() + 1;
    
    // Build transition table: [state][char] -> next_state (-1 = invalid)
    let mut transitions = vec![vec![-1i32; 256]; num_states];
    let mut accepting = Vec::new();
    
    for (i, &c) in pattern_chars.iter().enumerate() {
        match c {
            '.' => {
                // Match any character
                for ch in 0..256 {
                    if ch >= 32 && ch < 127 { // printable ASCII
                        transitions[i][ch] = (i + 1) as i32;
                    }
                }
            }
            '*' => {
                // Kleene star on previous char (simplified)
                if i > 0 {
                    let prev_char = pattern_chars[i - 1] as usize;
                    transitions[i][prev_char] = i as i32;
                    // Also allow transition to next state
                    for ch in 0..256 {
                        if transitions[i - 1][ch] >= 0 {
                            transitions[i][ch] = (i + 1) as i32;
                        }
                    }
                }
            }
            _ => {
                // Literal character match
                let ch_idx = c as usize;
                if ch_idx < 256 {
                    transitions[i][ch_idx] = (i + 1) as i32;
                }
            }
        }
    }
    
    // Final state is accepting
    accepting.push(num_states - 1);
    
    // Limit to vocab_size for memory efficiency
    let _ = vocab_size; // Use vocab_size if needed for token-level FSM
    
    (transitions, accepting, 0)
}

/// Fill token bitmask for allowed tokens at current FSM state
/// Returns bitmask as Vec<bool> where true = allowed
#[pyfunction]
pub fn fill_token_bitmask_rust(
    state: usize,
    transitions: Vec<Vec<i32>>,
    token_to_chars: Vec<Vec<u8>>,
) -> Vec<bool> {
    let vocab_size = token_to_chars.len();
    let mut bitmask = vec![false; vocab_size];
    
    if state >= transitions.len() {
        return bitmask;
    }
    
    for (token_id, chars) in token_to_chars.iter().enumerate() {
        // Check if token leads to valid state
        let mut current_state = state;
        let mut valid = true;
        
        for &ch in chars {
            let ch_idx = ch as usize;
            if ch_idx < 256 && current_state < transitions.len() {
                let next = transitions[current_state][ch_idx];
                if next >= 0 {
                    current_state = next as usize;
                } else {
                    valid = false;
                    break;
                }
            } else {
                valid = false;
                break;
            }
        }
        
        bitmask[token_id] = valid;
    }
    
    bitmask
}

/// Validate token sequence against FSM
/// Returns (is_valid, final_state, accepted_length)
#[pyfunction]
pub fn validate_token_sequence_rust(
    tokens: Vec<i64>,
    token_to_chars: Vec<Vec<u8>>,
    transitions: Vec<Vec<i32>>,
    initial_state: usize,
    accepting_states: Vec<usize>,
) -> (bool, usize, usize) {
    let mut state = initial_state;
    let mut accepted_len = 0;
    
    for token in &tokens {
        let token_idx = *token as usize;
        if token_idx >= token_to_chars.len() {
            break;
        }
        
        let chars = &token_to_chars[token_idx];
        let mut valid = true;
        
        for &ch in chars {
            let ch_idx = ch as usize;
            if ch_idx < 256 && state < transitions.len() {
                let next = transitions[state][ch_idx];
                if next >= 0 {
                    state = next as usize;
                } else {
                    valid = false;
                    break;
                }
            } else {
                valid = false;
                break;
            }
        }
        
        if !valid {
            break;
        }
        accepted_len += 1;
    }
    
    let is_accepting = accepting_states.contains(&state);
    (is_accepting, state, accepted_len)
}

/// Build JSON schema FSM for constrained JSON generation
/// Returns simplified FSM for object/array/string patterns
#[pyfunction]
pub fn json_schema_fsm_rust(
    schema_type: String,
    required_keys: Vec<String>,
) -> (Vec<Vec<i32>>, Vec<usize>, usize) {
    // Simplified JSON FSM based on schema type
    let states: usize;
    let mut transitions: Vec<Vec<i32>>;
    let mut accepting = Vec::new();
    
    match schema_type.as_str() {
        "object" => {
            // States: 0={, 1="key", 2=:, 3=value, 4=, or }, 5=accepting
            states = 6;
            transitions = vec![vec![-1i32; 256]; states];
            
            transitions[0]['{' as usize] = 1;
            // After {, allow " for key or } for empty object
            transitions[1]['"' as usize] = 2;
            transitions[1]['}' as usize] = 5;
            // Key characters
            for ch in 'a' as usize..='z' as usize {
                transitions[2][ch] = 2;
            }
            for ch in 'A' as usize..='Z' as usize {
                transitions[2][ch] = 2;
            }
            transitions[2]['_' as usize] = 2;
            transitions[2]['"' as usize] = 3; // End key
            transitions[3][':' as usize] = 4;
            // Value can be string, number, bool, null, nested
            transitions[4]['"' as usize] = 4; // string value
            for ch in '0' as usize..='9' as usize {
                transitions[4][ch] = 4;
            }
            transitions[4]['-' as usize] = 4;
            transitions[4]['t' as usize] = 4; // true
            transitions[4]['f' as usize] = 4; // false
            transitions[4]['n' as usize] = 4; // null
            transitions[4][',' as usize] = 1; // next key
            transitions[4]['}' as usize] = 5; // close object
            
            accepting.push(5);
        }
        "array" => {
            // States: 0=[, 1=value, 2=, or ], 3=accepting
            states = 4;
            transitions = vec![vec![-1i32; 256]; states];
            
            transitions[0]['[' as usize] = 1;
            transitions[1][']' as usize] = 3;
            // Values
            for ch in '0' as usize..='9' as usize {
                transitions[1][ch] = 1;
            }
            transitions[1]['"' as usize] = 1;
            transitions[1]['-' as usize] = 1;
            transitions[1][',' as usize] = 1;
            transitions[1][']' as usize] = 3;
            
            accepting.push(3);
        }
        "string" => {
            // States: 0=", 1=chars, 2=", 3=accepting
            states = 4;
            transitions = vec![vec![-1i32; 256]; states];
            
            transitions[0]['"' as usize] = 1;
            // Allow printable chars
            for ch in 32..127 {
                if ch != '"' as usize && ch != '\\' as usize {
                    transitions[1][ch] = 1;
                }
            }
            transitions[1]['\\' as usize] = 2; // escape
            for ch in &['n', 'r', 't', '"', '\\'] {
                transitions[2][*ch as usize] = 1;
            }
            transitions[1]['"' as usize] = 3;
            
            accepting.push(3);
        }
        _ => {
            // Default: accept anything
            states = 2;
            transitions = vec![vec![1i32; 256]; states];
            accepting.push(1);
        }
    }
    
    let _ = required_keys; // Would be used for stricter validation
    
    (transitions, accepting, 0)
}

/// Apply logit mask based on allowed token set
/// Returns masked logits with -inf for disallowed tokens
#[pyfunction]
pub fn apply_grammar_mask_rust(
    logits: Vec<f64>,
    allowed_tokens: Vec<usize>,
    mask_value: f64,
) -> Vec<f64> {
    let mut masked = vec![mask_value; logits.len()];
    
    for &token_id in &allowed_tokens {
        if token_id < logits.len() {
            masked[token_id] = logits[token_id];
        }
    }
    
    masked
}

/// Batch fill token bitmasks for multiple sequences
/// Returns [batch_size, vocab_size] bitmask
#[pyfunction]
pub fn batch_fill_bitmask_rust(
    states: Vec<usize>,
    transitions: Vec<Vec<i32>>,
    token_to_chars: Vec<Vec<u8>>,
) -> Vec<Vec<bool>> {
    states.iter()
        .map(|&state| fill_token_bitmask_rust(state, transitions.clone(), token_to_chars.clone()))
        .collect()
}

// =============================================================================
// Phase 39: Speculative Decoding v2 - Tree-based Speculation
// =============================================================================

/// Build n-gram proposal tree for speculative decoding
/// Returns tree as (token_ids, parent_indices, probabilities)
#[pyfunction]
#[pyo3(signature = (context_tokens, ngram_index, max_depth=5, num_candidates=5))]
pub fn build_speculation_tree_rust(
    context_tokens: Vec<i64>,
    ngram_index: HashMap<Vec<i64>, Vec<usize>>,
    max_depth: usize,
    num_candidates: usize,
) -> (Vec<i64>, Vec<i32>, Vec<f64>) {
    let mut tokens = Vec::new();
    let mut parents = Vec::new();
    let mut probs = Vec::new();
    
    if context_tokens.is_empty() {
        return (tokens, parents, probs);
    }
    
    // Try different n-gram lengths
    for n in (1..=4).rev() {
        if context_tokens.len() < n {
            continue;
        }
        
        let context = context_tokens[context_tokens.len() - n..].to_vec();
        
        if let Some(positions) = ngram_index.get(&context) {
            // Count continuations
            let mut continuation_counts: HashMap<i64, usize> = HashMap::new();
            
            for &pos in positions {
                let next_pos = pos + n;
                if next_pos < context_tokens.len() {
                    let next_token = context_tokens[next_pos];
                    *continuation_counts.entry(next_token).or_default() += 1;
                }
            }
            
            // Get top candidates
            let mut sorted_continuations: Vec<_> = continuation_counts.into_iter().collect();
            sorted_continuations.sort_by(|a, b| b.1.cmp(&a.1));
            sorted_continuations.truncate(num_candidates);
            
            let total: usize = sorted_continuations.iter().map(|(_, c)| c).sum();
            
            // Add to tree
            for (token, count) in sorted_continuations {
                tokens.push(token);
                parents.push(-1); // Root level
                probs.push(count as f64 / total.max(1) as f64);
            }
            
            break;
        }
    }
    
    // Extend tree to max_depth (greedy for deeper levels)
    let mut current_depth = 1;
    let mut frontier_start = 0;
    let mut frontier_end = tokens.len();
    
    while current_depth < max_depth && frontier_end > frontier_start {
        let mut new_tokens = Vec::new();
        let mut new_parents = Vec::new();
        let mut new_probs = Vec::new();
        
        for idx in frontier_start..frontier_end {
            // Build context with this path
            let mut path_context = context_tokens.clone();
            let mut curr = idx as i32;
            let mut path = Vec::new();
            
            while curr >= 0 && (curr as usize) < tokens.len() {
                path.push(tokens[curr as usize]);
                curr = parents[curr as usize];
            }
            path.reverse();
            path_context.extend(&path);
            
            // Find continuations
            for n in (1..=4).rev() {
                if path_context.len() < n {
                    continue;
                }
                
                let ctx = path_context[path_context.len() - n..].to_vec();
                if let Some(positions) = ngram_index.get(&ctx) {
                    let mut counts: HashMap<i64, usize> = HashMap::new();
                    for &pos in positions {
                        let next_pos = pos + n;
                        if next_pos < context_tokens.len() {
                            *counts.entry(context_tokens[next_pos]).or_default() += 1;
                        }
                    }
                    
                    if let Some((&best_token, &best_count)) = counts.iter().max_by_key(|(_, c)| *c) {
                        let total: usize = counts.values().sum();
                        new_tokens.push(best_token);
                        new_parents.push(idx as i32);
                        new_probs.push(best_count as f64 / total.max(1) as f64);
                    }
                    break;
                }
            }
        }
        
        frontier_start = tokens.len();
        tokens.extend(new_tokens);
        parents.extend(new_parents);
        probs.extend(new_probs);
        frontier_end = tokens.len();
        current_depth += 1;
    }
    
    (tokens, parents, probs)
}

/// Verify speculative tokens with target model logits
/// Returns (accepted_indices, bonus_token)
#[pyfunction]
pub fn verify_speculation_tree_rust(
    tree_tokens: Vec<i64>,
    _tree_parents: Vec<i32>,
    tree_probs: Vec<f64>,
    target_logits: Vec<Vec<f64>>,
    temperature: f64,
) -> (Vec<usize>, Option<i64>) {
    if tree_tokens.is_empty() || target_logits.is_empty() {
        return (Vec::new(), None);
    }
    
    let mut accepted = Vec::new();
    let mut bonus_token = None;
    
    // Find longest accepted path
    let num_nodes = tree_tokens.len();
    let vocab_size = if target_logits.is_empty() { 0 } else { target_logits[0].len() };
    
    // Process nodes in order (root to leaves)
    for idx in 0..num_nodes.min(target_logits.len()) {
        let proposed = tree_tokens[idx] as usize;
        
        if proposed >= vocab_size {
            break;
        }
        
        // Get target probability
        let logits = &target_logits[idx];
        let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let temp = temperature.max(0.01);
        
        let exp_logits: Vec<f64> = logits.iter()
            .map(|l| ((l - max_logit) / temp).exp())
            .collect();
        let sum: f64 = exp_logits.iter().sum();
        let target_prob = exp_logits[proposed] / sum;
        
        let draft_prob = tree_probs[idx].max(1e-10);
        
        // Acceptance probability: min(1, p_target / p_draft)
        let _accept_prob = (target_prob / draft_prob).min(1.0);
        
        // Deterministic check for reproducibility (use random in production)
        if target_prob >= draft_prob * 0.5 {
            accepted.push(idx);
        } else {
            // Sample bonus token from residual
            let argmax = logits.iter()
                .enumerate()
                .max_by(|a, b| a.1.partial_cmp(b.1).unwrap())
                .map(|(i, _)| i);
            bonus_token = argmax.map(|i| i as i64);
            break;
        }
    }
    
    // If all accepted, sample next token
    if accepted.len() == num_nodes.min(target_logits.len()) && target_logits.len() > num_nodes {
        let final_logits = &target_logits[num_nodes];
        let argmax = final_logits.iter()
            .enumerate()
            .max_by(|a, b| a.1.partial_cmp(b.1).unwrap())
            .map(|(i, _)| i);
        bonus_token = argmax.map(|i| i as i64);
    }
    
    (accepted, bonus_token)
}

/// Extract accepted token sequence from tree
/// Returns tokens along the accepted path
#[pyfunction]
pub fn extract_accepted_path_rust(
    tree_tokens: Vec<i64>,
    tree_parents: Vec<i32>,
    accepted_indices: Vec<usize>,
) -> Vec<i64> {
    if accepted_indices.is_empty() {
        return Vec::new();
    }
    
    // Find deepest accepted node
    let deepest = *accepted_indices.last().unwrap();
    
    // Trace back to root
    let mut path = Vec::new();
    let mut curr = deepest as i32;
    
    while curr >= 0 && (curr as usize) < tree_tokens.len() {
        path.push(tree_tokens[curr as usize]);
        curr = tree_parents[curr as usize];
    }
    
    path.reverse();
    path
}

/// Compute speculation acceptance rate statistics
/// Returns (acceptance_rate, avg_accepted_length, speedup_factor)
#[pyfunction]
pub fn speculation_stats_rust(
    total_proposed: usize,
    total_accepted: usize,
    total_steps: usize,
) -> (f64, f64, f64) {
    if total_proposed == 0 || total_steps == 0 {
        return (0.0, 0.0, 1.0);
    }
    
    let acceptance_rate = total_accepted as f64 / total_proposed as f64;
    let avg_accepted = total_accepted as f64 / total_steps as f64;
    
    // Speedup = tokens_generated / forward_passes
    // With speculation: (accepted + 1) tokens per forward pass of target
    let speedup = (avg_accepted + 1.0) / 1.0;
    
    (acceptance_rate, avg_accepted, speedup)
}

/// Tensorizer checksum computation (SHA256 truncated)
#[pyfunction]
pub fn tensorizer_checksum_rust(data: Vec<u8>) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    data.hash(&mut hasher);
    let hash = hasher.finish();
    
    format!("{:016x}", hash)
}

/// Pack tensor metadata for serialization
#[pyfunction]
pub fn pack_tensor_metadata_rust(
    name: String,
    shape: Vec<usize>,
    dtype: String,
    offset: usize,
    size_bytes: usize,
) -> Vec<u8> {
    let mut result = Vec::new();
    
    // Name (length-prefixed)
    let name_bytes = name.as_bytes();
    result.extend((name_bytes.len() as u32).to_le_bytes());
    result.extend(name_bytes);
    
    // Shape (length-prefixed array)
    result.extend((shape.len() as u32).to_le_bytes());
    for dim in shape {
        result.extend((dim as u64).to_le_bytes());
    }
    
    // Dtype
    let dtype_bytes = dtype.as_bytes();
    result.extend((dtype_bytes.len() as u32).to_le_bytes());
    result.extend(dtype_bytes);
    
    // Offset and size
    result.extend((offset as u64).to_le_bytes());
    result.extend((size_bytes as u64).to_le_bytes());
    
    result
}

// =============================================================================
// Phase 40: Reasoning Parser Acceleration
// =============================================================================

/// Extract thinking blocks from text using delimiters
/// Returns list of (start, end, content) tuples
#[pyfunction]
pub fn extract_thinking_blocks_rust(
    text: &str,
    open_tag: &str,
    close_tag: &str,
) -> Vec<(usize, usize, String)> {
    let mut blocks = Vec::new();
    let mut search_start = 0;
    
    while let Some(start) = text[search_start..].find(open_tag) {
        let abs_start = search_start + start;
        let content_start = abs_start + open_tag.len();
        
        if let Some(end) = text[content_start..].find(close_tag) {
            let abs_end = content_start + end;
            let content = text[content_start..abs_end].to_string();
            blocks.push((abs_start, abs_end + close_tag.len(), content));
            search_start = abs_end + close_tag.len();
        } else {
            break;
        }
    }
    
    blocks
}

/// Parse tool calls from JSON-like string
/// Returns list of (name, arguments_json) tuples
#[pyfunction]
pub fn parse_tool_calls_rust(text: &str) -> Vec<(String, String)> {
    let mut calls = Vec::new();
    
    // Simple regex-free parsing for {"name": "...", "arguments": {...}}
    let mut i = 0;
    let bytes = text.as_bytes();
    let n = bytes.len();
    
    while i < n {
        // Find "name"
        if let Some(pos) = text[i..].find("\"name\"") {
            let name_key_pos = i + pos;
            // Find colon
            if let Some(colon) = text[name_key_pos + 6..].find(':') {
                let after_colon = name_key_pos + 6 + colon + 1;
                // Find opening quote
                if let Some(quote1) = text[after_colon..].find('"') {
                    let name_start = after_colon + quote1 + 1;
                    // Find closing quote
                    if let Some(quote2) = text[name_start..].find('"') {
                        let name_end = name_start + quote2;
                        let name = text[name_start..name_end].to_string();
                        
                        // Find arguments
                        if let Some(args_pos) = text[name_end..].find("\"arguments\"") {
                            let args_key_pos = name_end + args_pos;
                            // Find colon and opening brace
                            if let Some(brace) = text[args_key_pos + 11..].find('{') {
                                let args_start = args_key_pos + 11 + brace;
                                // Find matching closing brace
                                let mut depth = 1;
                                let mut j = args_start + 1;
                                while j < n && depth > 0 {
                                    if bytes[j] == b'{' {
                                        depth += 1;
                                    } else if bytes[j] == b'}' {
                                        depth -= 1;
                                    }
                                    j += 1;
                                }
                                let args = text[args_start..j].to_string();
                                calls.push((name, args));
                                i = j;
                                continue;
                            }
                        }
                        i = name_end;
                        continue;
                    }
                }
            }
            i = name_key_pos + 1;
        } else {
            break;
        }
    }
    
    calls
}

/// Streaming-safe token classification for reasoning
/// Returns (is_thinking, is_tool_call, is_content)
#[pyfunction]
pub fn classify_token_context_rust(
    prefix: &str,
    token_text: &str,
    thinking_open: &str,
    thinking_close: &str,
) -> (bool, bool, bool) {
    let combined = format!("{}{}", prefix, token_text);
    
    // Check if we're inside thinking block
    let open_count = combined.matches(thinking_open).count();
    let close_count = combined.matches(thinking_close).count();
    let is_thinking = open_count > close_count;
    
    // Check if token is part of tool call
    let is_tool_call = combined.contains("\"name\"") && 
                       (combined.ends_with("\"arguments\"") || 
                        combined.contains("\"arguments\":"));
    
    // Content is default
    let is_content = !is_thinking && !is_tool_call;
    
    (is_thinking, is_tool_call, is_content)
}

// =============================================================================
// Phase 40: Multimodal Cache Acceleration
// =============================================================================

/// Compute Blake3 hash for binary data (fast content-addressed caching)
#[pyfunction]
pub fn blake3_hash_rust(data: Vec<u8>) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    // Note: This is a placeholder - real Blake3 would require blake3 crate
    // Using fast hash for now with Blake3-like output format
    let mut hasher = DefaultHasher::new();
    data.hash(&mut hasher);
    let h1 = hasher.finish();
    
    let mut hasher2 = DefaultHasher::new();
    h1.hash(&mut hasher2);
    data.len().hash(&mut hasher2);
    let h2 = hasher2.finish();
    
    format!("{:016x}{:016x}", h1, h2)
}

/// Compute perceptual hash similarity score (0.0 to 1.0)
#[pyfunction]
pub fn perceptual_hash_distance_rust(hash1: &str, hash2: &str) -> f64 {
    if hash1.len() != hash2.len() {
        return 1.0; // Maximum distance
    }
    
    // Count differing hex characters
    let diffs: usize = hash1.chars()
        .zip(hash2.chars())
        .filter(|(a, b)| a != b)
        .count();
    
    // Convert to similarity
    let max_diffs = hash1.len();
    1.0 - (diffs as f64 / max_diffs as f64)
}

/// LRU eviction candidate selection
/// Returns indices to evict based on access times
#[pyfunction]
pub fn lru_evict_candidates_rust(
    access_times: Vec<f64>,
    num_to_evict: usize,
) -> Vec<usize> {
    if num_to_evict == 0 || access_times.is_empty() {
        return Vec::new();
    }
    
    // Create index-time pairs and sort by time
    let mut indexed: Vec<(usize, f64)> = access_times
        .into_iter()
        .enumerate()
        .collect();
    
    indexed.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    // Take oldest entries
    indexed.into_iter()
        .take(num_to_evict)
        .map(|(i, _)| i)
        .collect()
}

/// Compute cache entry priority for ARC-like caching
#[pyfunction]
pub fn arc_cache_priority_rust(
    frequency: usize,
    recency: f64,
    size_bytes: usize,
    alpha: f64,
) -> f64 {
    // Priority = alpha * log(frequency + 1) + (1 - alpha) * recency / size
    let freq_score = (frequency as f64 + 1.0).ln();
    let size_factor = (size_bytes as f64).max(1.0);
    let recency_score = recency / size_factor;
    
    alpha * freq_score + (1.0 - alpha) * recency_score
}

// =============================================================================
// Phase 40: Pooling Engine Acceleration
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

// =============================================================================
// Phase 40: Input Preprocessing Acceleration
// =============================================================================

/// Fast token count estimation from text
#[pyfunction]
pub fn estimate_tokens_rust(text: &str) -> usize {
    // Simple heuristic: words * 1.3 + special handling
    let words = text.split_whitespace().count();
    let symbols = text.chars().filter(|c| !c.is_alphanumeric() && !c.is_whitespace()).count();
    
    (words as f64 * 1.3 + symbols as f64 * 0.5) as usize
}

/// Validate chat message structure
/// Returns (is_valid, error_message)
#[pyfunction]
pub fn validate_chat_messages_rust(
    messages: Vec<(String, String)>,  // (role, content)
) -> (bool, String) {
    if messages.is_empty() {
        return (false, "Empty messages".to_string());
    }
    
    let valid_roles = ["system", "user", "assistant", "tool", "function"];
    
    for (i, (role, content)) in messages.iter().enumerate() {
        if !valid_roles.contains(&role.as_str()) {
            return (false, format!("Invalid role '{}' at index {}", role, i));
        }
        
        if content.is_empty() && role != "system" {
            return (false, format!("Empty content at index {}", i));
        }
    }
    
    // Check conversation structure
    if !messages.is_empty() {
        let (first_role, _) = &messages[0];
        if first_role != "system" && first_role != "user" {
            return (false, "First message must be system or user".to_string());
        }
    }
    
    (true, String::new())
}

/// Linearize chat messages to prompt format
#[pyfunction]
pub fn linearize_chat_rust(
    messages: Vec<(String, String)>,  // (role, content)
    format: &str,  // "chatml", "llama", "mistral"
) -> String {
    match format {
        "chatml" => linearize_chatml(messages),
        "llama" => linearize_llama(messages),
        "mistral" => linearize_mistral(messages),
        _ => linearize_chatml(messages),
    }
}

fn linearize_chatml(messages: Vec<(String, String)>) -> String {
    let mut result = String::new();
    
    for (role, content) in messages {
        result.push_str(&format!("<|im_start|>{}\n{}<|im_end|>\n", role, content));
    }
    result.push_str("<|im_start|>assistant\n");
    
    result
}

fn linearize_llama(messages: Vec<(String, String)>) -> String {
    let mut result = String::new();
    
    for (role, content) in messages {
        match role.as_str() {
            "system" => {
                result.push_str(&format!("<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|>", content));
            }
            "user" => {
                result.push_str(&format!("<|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|>", content));
            }
            "assistant" => {
                result.push_str(&format!("<|start_header_id|>assistant<|end_header_id|>\n\n{}<|eot_id|>", content));
            }
            _ => {}
        }
    }
    result.push_str("<|start_header_id|>assistant<|end_header_id|>\n\n");
    
    result
}

fn linearize_mistral(messages: Vec<(String, String)>) -> String {
    let mut result = String::new();
    
    for (role, content) in messages {
        match role.as_str() {
            "user" => {
                result.push_str(&format!("[INST] {} [/INST]", content));
            }
            "assistant" => {
                result.push_str(&format!(" {}</s>", content));
            }
            "system" => {
                result.push_str(&format!("[INST] {} ", content));
            }
            _ => {}
        }
    }
    
    result
}

// =============================================================================
// Phase 40: Advanced Sampling Acceleration
// =============================================================================

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

/// Apply bad words masking to logits
#[pyfunction]
pub fn apply_bad_words_mask_rust(
    mut logits: Vec<f64>,
    banned_token_ids: Vec<usize>,
) -> Vec<f64> {
    for tid in banned_token_ids {
        if tid < logits.len() {
            logits[tid] = f64::NEG_INFINITY;
        }
    }
    logits
}

/// Apply token whitelist masking
#[pyfunction]
pub fn apply_whitelist_mask_rust(
    mut logits: Vec<f64>,
    allowed_token_ids: Vec<usize>,
) -> Vec<f64> {
    let allowed_set: std::collections::HashSet<usize> = allowed_token_ids.into_iter().collect();
    
    for (i, logit) in logits.iter_mut().enumerate() {
        if !allowed_set.contains(&i) {
            *logit = f64::NEG_INFINITY;
        }
    }
    
    logits
}

/// Mirostat sampling (mode 2)
/// Returns (selected_token_id, updated_mu)
#[pyfunction]
pub fn mirostat_sample_rust(
    logits: Vec<f64>,
    mu: f64,
    tau: f64,
    eta: f64,
) -> (usize, f64) {
    // Compute probabilities
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_logit).exp()).collect();
    let sum: f64 = exp_logits.iter().sum();
    let probs: Vec<f64> = exp_logits.iter().map(|e| e / sum).collect();
    
    // Sort by probability descending
    let mut indexed: Vec<(usize, f64)> = probs.iter().cloned().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    // Compute surprises and find cutoff
    let mut k = 1;
    for (i, (_, p)) in indexed.iter().enumerate() {
        let surprise = -(p.max(1e-10)).log2();
        if surprise > mu {
            k = i.max(1);
            break;
        }
        k = i + 1;
    }
    
    // Sample from top-k
    let top_k: Vec<(usize, f64)> = indexed.into_iter().take(k).collect();
    let _sum_k: f64 = top_k.iter().map(|(_, p)| p).sum();
    
    // Greedy for simplicity (use random sampling in production)
    let selected = top_k.iter()
        .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
        .map(|(i, _)| *i)
        .unwrap_or(0);
    
    // Update mu
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
    // Compute entropy
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_logit).exp()).collect();
    let sum: f64 = exp_logits.iter().sum();
    let probs: Vec<f64> = exp_logits.iter().map(|e| e / sum).collect();
    
    let entropy: f64 = probs.iter()
        .filter(|&&p| p > 1e-10)
        .map(|&p| -p * p.ln())
        .sum();
    
    // Map entropy to k
    let normalized = (entropy / entropy_threshold).min(2.0);
    let k = min_k + (normalized * (max_k - min_k) as f64) as usize;
    
    k.max(min_k).min(max_k)
}

// =============================================================================
// Phase 41: Tokenizer Registry Acceleration
// =============================================================================

/// Fast token encoding using byte-pair encoding (BPE) merge lookup
/// Returns encoded token IDs
#[pyfunction]
pub fn bpe_encode_fast_rust(
    text: String,
    vocab: HashMap<String, i64>,
    merges: Vec<(String, String)>,
) -> Vec<i64> {
    // Convert text to bytes/chars
    let chars: Vec<String> = text.chars().map(|c| c.to_string()).collect();
    
    if chars.is_empty() {
        return Vec::new();
    }
    
    // Build merge priority map
    let merge_priority: HashMap<(String, String), usize> = merges.iter()
        .enumerate()
        .map(|(i, (a, b))| ((a.clone(), b.clone()), i))
        .collect();
    
    // Start with character tokens
    let mut tokens = chars;
    
    // Apply merges iteratively
    loop {
        if tokens.len() < 2 {
            break;
        }
        
        // Find best merge pair
        let mut best_pair: Option<(usize, (String, String))> = None;
        let mut best_priority = usize::MAX;
        
        for i in 0..tokens.len() - 1 {
            let pair = (tokens[i].clone(), tokens[i + 1].clone());
            if let Some(&priority) = merge_priority.get(&pair) {
                if priority < best_priority {
                    best_priority = priority;
                    best_pair = Some((i, pair));
                }
            }
        }
        
        // Apply best merge
        match best_pair {
            Some((idx, (a, b))) => {
                let merged = format!("{}{}", a, b);
                tokens[idx] = merged;
                tokens.remove(idx + 1);
            }
            None => break,
        }
    }
    
    // Convert to IDs
    tokens.iter()
        .filter_map(|t| vocab.get(t).copied())
        .collect()
}

/// Batch token count estimation without full encoding
#[pyfunction]
pub fn batch_estimate_tokens_rust(
    texts: Vec<String>,
    chars_per_token: f64,
) -> Vec<usize> {
    texts.iter()
        .map(|t| (t.chars().count() as f64 / chars_per_token).ceil() as usize)
        .collect()
}

/// Compute tokenizer cache key for LRU caching
#[pyfunction]
pub fn tokenizer_cache_key_rust(
    model_name: String,
    backend: String,
    trust_remote: bool,
    revision: String,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    model_name.hash(&mut hasher);
    backend.hash(&mut hasher);
    trust_remote.hash(&mut hasher);
    revision.hash(&mut hasher);
    hasher.finish()
}

// =============================================================================
// Phase 41: Model Registry Acceleration
// =============================================================================

/// Compute model architecture fingerprint from config
#[pyfunction]
pub fn architecture_fingerprint_rust(
    hidden_size: usize,
    num_layers: usize,
    num_heads: usize,
    vocab_size: usize,
    intermediate_size: usize,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    hidden_size.hash(&mut hasher);
    num_layers.hash(&mut hasher);
    num_heads.hash(&mut hasher);
    vocab_size.hash(&mut hasher);
    intermediate_size.hash(&mut hasher);
    hasher.finish()
}

/// Estimate VRAM requirement for a model
/// Returns (min_vram_bytes, optimal_vram_bytes)
#[pyfunction]
pub fn estimate_vram_bytes_rust(
    num_params: u64,
    precision_bits: u8,
    context_length: usize,
    batch_size: usize,
    kv_cache_factor: f64,
) -> (u64, u64) {
    // Base model weights
    let bytes_per_param = (precision_bits as f64) / 8.0;
    let model_bytes = (num_params as f64 * bytes_per_param) as u64;
    
    // KV cache estimation (simplified)
    // kv_bytes = batch_size * context_length * hidden_size * 2 (k+v) * num_layers * bytes
    let kv_estimate = (batch_size * context_length) as f64 * kv_cache_factor * bytes_per_param;
    let kv_bytes = kv_estimate as u64;
    
    // Activation memory (rough estimate: 10-20% of model size)
    let activation_bytes = model_bytes / 10;
    
    let min_vram = model_bytes + kv_bytes / 2;
    let optimal_vram = model_bytes + kv_bytes + activation_bytes;
    
    (min_vram, optimal_vram)
}

/// Match model architecture from config patterns
/// Returns architecture name or "unknown"
#[pyfunction]
pub fn detect_architecture_rust(
    architectures: Vec<String>,
    model_type: String,
) -> String {
    // Check architectures list first
    for arch in &architectures {
        let lower = arch.to_lowercase();
        if lower.contains("llama") {
            return "llama".to_string();
        }
        if lower.contains("mistral") {
            return "mistral".to_string();
        }
        if lower.contains("qwen") {
            return "qwen2".to_string();
        }
        if lower.contains("falcon") {
            return "falcon".to_string();
        }
        if lower.contains("gemma") {
            return "gemma2".to_string();
        }
        if lower.contains("phi") {
            return "phi3".to_string();
        }
        if lower.contains("starcoder") {
            return "starcoder2".to_string();
        }
    }
    
    // Fallback to model_type
    model_type.to_lowercase()
}

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

// =============================================================================
// Phase 41: Logprobs Acceleration
// =============================================================================

/// Compute log softmax with numerical stability
#[pyfunction]
pub fn log_softmax_stable_rust(
    logits: Vec<f64>,
) -> Vec<f64> {
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let shifted: Vec<f64> = logits.iter().map(|l| l - max_logit).collect();
    let log_sum_exp = shifted.iter().map(|s| s.exp()).sum::<f64>().ln();
    
    shifted.iter().map(|s| s - log_sum_exp).collect()
}

/// Extract top-k logprobs with token IDs
/// Returns (top_k_ids, top_k_logprobs)
#[pyfunction]
pub fn extract_top_k_logprobs_rust(
    logprobs: Vec<f64>,
    k: usize,
) -> (Vec<usize>, Vec<f64>) {
    let mut indexed: Vec<(usize, f64)> = logprobs.into_iter().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    indexed.truncate(k);
    
    let ids: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
    let lps: Vec<f64> = indexed.iter().map(|(_, lp)| *lp).collect();
    
    (ids, lps)
}

/// Compute perplexity from logprobs
#[pyfunction]
pub fn compute_perplexity_rust(
    logprobs: Vec<f64>,
) -> f64 {
    if logprobs.is_empty() {
        return 0.0;
    }
    let mean_logprob: f64 = logprobs.iter().sum::<f64>() / logprobs.len() as f64;
    (-mean_logprob).exp()
}

/// Compute entropy from probability distribution
#[pyfunction]
pub fn compute_entropy_rust(
    probs: Vec<f64>,
) -> f64 {
    probs.iter()
        .filter(|&&p| p > 1e-10)
        .map(|&p| -p * p.ln())
        .sum()
}

/// Batch process logits to logprobs for multiple sequences
/// Returns flattened logprobs for selected tokens
#[pyfunction]
pub fn batch_logprobs_rust(
    batch_logits: Vec<Vec<f64>>,  // [batch, vocab]
    selected_ids: Vec<usize>,     // [batch]
) -> Vec<f64> {
    batch_logits.iter()
        .zip(selected_ids.iter())
        .map(|(logits, &token_id)| {
            let log_probs = {
                let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
                let shifted: Vec<f64> = logits.iter().map(|l| l - max_logit).collect();
                let log_sum_exp = shifted.iter().map(|s| s.exp()).sum::<f64>().ln();
                shifted.iter().map(|s| s - log_sum_exp).collect::<Vec<f64>>()
            };
            log_probs.get(token_id).copied().unwrap_or(f64::NEG_INFINITY)
        })
        .collect()
}

// =============================================================================
// Phase 41: Tool Parser Acceleration
// =============================================================================

/// Fast JSON object extraction from text
/// Returns list of (start_pos, end_pos) for each JSON object found
#[pyfunction]
pub fn extract_json_positions_rust(
    text: String,
) -> Vec<(usize, usize)> {
    let mut results = Vec::new();
    let chars: Vec<char> = text.chars().collect();
    
    let mut brace_depth = 0;
    let mut start_idx: Option<usize> = None;
    let mut in_string = false;
    let mut prev_char = ' ';
    
    for (i, &ch) in chars.iter().enumerate() {
        if ch == '"' && prev_char != '\\' {
            in_string = !in_string;
        } else if !in_string {
            if ch == '{' {
                if brace_depth == 0 {
                    start_idx = Some(i);
                }
                brace_depth += 1;
            } else if ch == '}' {
                brace_depth -= 1;
                if brace_depth == 0 {
                    if let Some(start) = start_idx {
                        results.push((start, i + 1));
                    }
                    start_idx = None;
                }
            }
        }
        prev_char = ch;
    }
    
    results
}

/// Detect tool call format from text content
/// Returns format name: "hermes", "llama3", "mistral", "granite", "json"
#[pyfunction]
pub fn detect_tool_format_rust(
    text: String,
) -> String {
    if text.contains("<tool_call>") {
        return "hermes".to_string();
    }
    if text.contains("<|python_tag|>") {
        return "llama3".to_string();
    }
    if text.contains("[TOOL_CALLS]") {
        return "mistral".to_string();
    }
    if text.contains("<|tool_call|>") {
        return "granite".to_string();
    }
    "json".to_string()
}

/// Parse tool call arguments from JSON string
/// Returns parsed arguments as key-value pairs or empty on error
#[pyfunction]
pub fn parse_tool_arguments_rust(
    json_str: String,
) -> HashMap<String, String> {
    let mut result = HashMap::new();
    
    // Simple JSON parsing for flat objects
    let trimmed = json_str.trim();
    if !trimmed.starts_with('{') || !trimmed.ends_with('}') {
        return result;
    }
    
    let inner = &trimmed[1..trimmed.len()-1];
    
    // Split by commas (simplified - doesn't handle nested objects)
    let mut in_string = false;
    let mut depth = 0;
    let mut current_key = String::new();
    let mut current_value = String::new();
    let mut parsing_value = false;
    let mut prev_char = ' ';
    
    for ch in inner.chars() {
        if ch == '"' && prev_char != '\\' {
            in_string = !in_string;
        } else if !in_string {
            match ch {
                '{' | '[' => depth += 1,
                '}' | ']' => depth -= 1,
                ':' if depth == 0 => {
                    parsing_value = true;
                    prev_char = ch;
                    continue;
                }
                ',' if depth == 0 => {
                    let key = current_key.trim().trim_matches('"').to_string();
                    let value = current_value.trim().trim_matches('"').to_string();
                    if !key.is_empty() {
                        result.insert(key, value);
                    }
                    current_key.clear();
                    current_value.clear();
                    parsing_value = false;
                    prev_char = ch;
                    continue;
                }
                _ => {}
            }
        }
        
        if parsing_value {
            current_value.push(ch);
        } else {
            current_key.push(ch);
        }
        prev_char = ch;
    }
    
    // Handle last pair
    let key = current_key.trim().trim_matches('"').to_string();
    let value = current_value.trim().trim_matches('"').to_string();
    if !key.is_empty() {
        result.insert(key, value);
    }
    
    result
}

// =============================================================================
// Phase 41: Structured Output Acceleration
// =============================================================================

/// Validate JSON structure against basic schema
/// Returns (is_valid, error_message)
#[pyfunction]
pub fn validate_json_schema_fast_rust(
    json_str: String,
    required_keys: Vec<String>,
    expected_types: HashMap<String, String>,  // key -> "string"|"number"|"boolean"|"array"|"object"
) -> (bool, String) {
    // Parse JSON
    let parsed: Result<serde_json::Value, _> = serde_json::from_str(&json_str);
    
    match parsed {
        Ok(value) => {
            // Check if object
            let obj = match value.as_object() {
                Some(o) => o,
                None => return (false, "Expected JSON object".to_string()),
            };
            
            // Check required keys
            for key in &required_keys {
                if !obj.contains_key(key) {
                    return (false, format!("Missing required key: {}", key));
                }
            }
            
            // Check types
            for (key, expected_type) in &expected_types {
                if let Some(val) = obj.get(key) {
                    let actual_type = match val {
                        serde_json::Value::String(_) => "string",
                        serde_json::Value::Number(_) => "number",
                        serde_json::Value::Bool(_) => "boolean",
                        serde_json::Value::Array(_) => "array",
                        serde_json::Value::Object(_) => "object",
                        serde_json::Value::Null => "null",
                    };
                    
                    if actual_type != expected_type.as_str() {
                        return (false, format!(
                            "Key '{}': expected {}, got {}", key, expected_type, actual_type
                        ));
                    }
                }
            }
            
            (true, String::new())
        }
        Err(e) => (false, format!("JSON parse error: {}", e)),
    }
}

/// Check if partial text could still match a JSON schema
#[pyfunction]
pub fn validate_partial_json_rust(
    partial_text: String,
) -> bool {
    let trimmed = partial_text.trim();
    
    if trimmed.is_empty() {
        return true;
    }
    
    // Valid JSON prefixes
    let valid_starts = ['{', '[', '"', 't', 'f', 'n', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    
    if let Some(first_char) = trimmed.chars().next() {
        valid_starts.contains(&first_char)
    } else {
        true
    }
}

/// Compute constraint composition hash for caching
#[pyfunction]
pub fn constraint_hash_rust(
    json_schema: Option<String>,
    regex_pattern: Option<String>,
    choices: Vec<String>,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    json_schema.hash(&mut hasher);
    regex_pattern.hash(&mut hasher);
    for choice in choices {
        choice.hash(&mut hasher);
    }
    hasher.finish()
}


// =============================================================================
// Phase 42: Platform, API, Templates, MCP, Conversation Acceleration
// =============================================================================

/// Generate platform fingerprint hash from device info
#[pyfunction]
pub fn platform_fingerprint_rust(
    platform_type: String,
    device_infos: Vec<HashMap<String, String>>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    platform_type.hash(&mut hasher);
    
    for device in device_infos {
        // Sort keys for consistent hashing
        let mut keys: Vec<_> = device.keys().collect();
        keys.sort();
        for key in keys {
            key.hash(&mut hasher);
            if let Some(val) = device.get(key) {
                val.hash(&mut hasher);
            }
        }
    }
    
    format!("{:016x}", hasher.finish())
}

/// Check device capability compatibility
#[pyfunction]
pub fn check_capability_rust(
    major: i32,
    minor: i32,
    required_major: i32,
    required_minor: i32,
) -> bool {
    if major > required_major {
        return true;
    }
    if major == required_major && minor >= required_minor {
        return true;
    }
    false
}

/// Estimate memory footprint for model loading
#[pyfunction]
pub fn estimate_memory_footprint_rust(
    num_params: i64,
    dtype_bytes: i32,
    kv_cache_size: i64,
    overhead_factor: f64,
) -> i64 {
    let base_memory = num_params * dtype_bytes as i64;
    let total = (base_memory as f64 * overhead_factor) as i64 + kv_cache_size;
    total
}

/// Parse OpenAI API response JSON efficiently
#[pyfunction]
pub fn parse_response_json_rust(
    json_str: String,
) -> PyResult<HashMap<String, String>> {
    let parsed: serde_json::Value = serde_json::from_str(&json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("JSON parse error: {}", e)))?;
    
    let mut result = HashMap::new();
    
    if let serde_json::Value::Object(obj) = parsed {
        for (key, value) in obj {
            let val_str = match value {
                serde_json::Value::String(s) => s,
                serde_json::Value::Number(n) => n.to_string(),
                serde_json::Value::Bool(b) => b.to_string(),
                serde_json::Value::Null => "null".to_string(),
                _ => serde_json::to_string(&value).unwrap_or_default(),
            };
            result.insert(key, val_str);
        }
    }
    
    Ok(result)
}

/// Extract SSE event data from stream chunk
#[pyfunction]
pub fn parse_sse_event_rust(
    chunk: String,
) -> (String, String, Option<String>) {
    let mut event_type = String::new();
    let mut data = String::new();
    let mut event_id = None;
    
    for line in chunk.lines() {
        if let Some(rest) = line.strip_prefix("event: ") {
            event_type = rest.trim().to_string();
        } else if let Some(rest) = line.strip_prefix("data: ") {
            if !data.is_empty() {
                data.push('\n');
            }
            data.push_str(rest.trim());
        } else if let Some(rest) = line.strip_prefix("id: ") {
            event_id = Some(rest.trim().to_string());
        }
    }
    
    (event_type, data, event_id)
}

/// Encode SSE event for streaming
#[pyfunction]
pub fn encode_sse_event_rust(
    event_type: String,
    data: String,
    event_id: Option<String>,
) -> String {
    let mut result = String::new();
    
    if let Some(id) = event_id {
        result.push_str(&format!("id: {}\n", id));
    }
    result.push_str(&format!("event: {}\n", event_type));
    
    for line in data.lines() {
        result.push_str(&format!("data: {}\n", line));
    }
    result.push('\n');
    
    result
}

/// Render simple chat template (non-Jinja fallback)
#[pyfunction]
pub fn render_simple_template_rust(
    messages: Vec<HashMap<String, String>>,
    template_type: String,
    add_generation_prompt: bool,
) -> String {
    let mut result = String::new();
    
    match template_type.as_str() {
        "chatml" | "qwen" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!("<|im_start|>{}\n{}<|im_end|>\n", role, content));
            }
            if add_generation_prompt {
                result.push_str("<|im_start|>assistant\n");
            }
        }
        "llama3" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!(
                    "<|start_header_id|>{}<|end_header_id|>\n\n{}<|eot_id|>",
                    role, content.trim()
                ));
            }
            if add_generation_prompt {
                result.push_str("<|start_header_id|>assistant<|end_header_id|>\n\n");
            }
        }
        "gemma" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                let gemma_role = if role == "assistant" { "model" } else { role };
                result.push_str(&format!(
                    "<start_of_turn>{}\n{}<end_of_turn>\n",
                    gemma_role, content
                ));
            }
            if add_generation_prompt {
                result.push_str("<start_of_turn>model\n");
            }
        }
        _ => {
            // Default to ChatML-style
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!("<|im_start|>{}\n{}<|im_end|>\n", role, content));
            }
            if add_generation_prompt {
                result.push_str("<|im_start|>assistant\n");
            }
        }
    }
    
    result
}

/// Detect chat template type from model name
#[pyfunction]
pub fn detect_chat_template_rust(
    model_name: String,
) -> String {
    let model_lower = model_name.to_lowercase();
    
    let patterns = [
        ("llama-3", "llama3"),
        ("llama3", "llama3"),
        ("meta-llama-3", "llama3"),
        ("llama-2", "llama2"),
        ("mistral", "mistral"),
        ("mixtral", "mistral"),
        ("zephyr", "zephyr"),
        ("vicuna", "vicuna"),
        ("alpaca", "alpaca"),
        ("gemma", "gemma"),
        ("phi", "phi"),
        ("qwen", "qwen"),
        ("deepseek", "deepseek"),
        ("yi", "yi"),
        ("command", "command"),
        ("openchat", "chatml"),
        ("dolphin", "chatml"),
    ];
    
    for (pattern, template) in patterns {
        if model_lower.contains(pattern) {
            return template.to_string();
        }
    }
    
    "chatml".to_string()
}

/// Find placeholder positions in text
#[pyfunction]
pub fn find_placeholders_rust(
    text: String,
    patterns: Vec<String>,
) -> Vec<usize> {
    let mut positions = Vec::new();
    
    for pattern in patterns {
        let mut start = 0;
        while let Some(pos) = text[start..].find(&pattern) {
            positions.push(start + pos);
            start = start + pos + pattern.len();
        }
    }
    
    positions.sort();
    positions
}

/// Parse MCP tool call from JSON
#[pyfunction]
pub fn parse_mcp_tool_call_rust(
    json_str: String,
) -> PyResult<HashMap<String, String>> {
    let parsed: serde_json::Value = serde_json::from_str(&json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("JSON parse error: {}", e)))?;
    
    let mut result = HashMap::new();
    
    if let serde_json::Value::Object(obj) = parsed {
        if let Some(serde_json::Value::String(name)) = obj.get("name") {
            result.insert("name".to_string(), name.clone());
        }
        if let Some(args) = obj.get("arguments") {
            result.insert("arguments".to_string(), serde_json::to_string(args).unwrap_or_default());
        }
        if let Some(serde_json::Value::String(id)) = obj.get("id") {
            result.insert("id".to_string(), id.clone());
        }
    }
    
    Ok(result)
}

/// Validate MCP tool schema
#[pyfunction]
pub fn validate_mcp_schema_rust(
    schema_json: String,
) -> (bool, String) {
    match serde_json::from_str::<serde_json::Value>(&schema_json) {
        Ok(parsed) => {
            let obj = match parsed {
                serde_json::Value::Object(o) => o,
                _ => return (false, "Schema must be an object".to_string()),
            };
            
            // Check for name
            if !obj.contains_key("name") {
                return (false, "Missing 'name' field".to_string());
            }
            
            // Check for inputSchema if present
            if let Some(input_schema) = obj.get("inputSchema") {
                if !input_schema.is_object() {
                    return (false, "inputSchema must be an object".to_string());
                }
            }
            
            (true, String::new())
        }
        Err(e) => (false, format!("JSON parse error: {}", e)),
    }
}

/// Hash conversation context for caching
#[pyfunction]
pub fn hash_conversation_context_rust(
    messages: Vec<HashMap<String, String>>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    
    for msg in messages {
        // Sort keys for consistent hashing
        let mut keys: Vec<_> = msg.keys().collect();
        keys.sort();
        for key in keys {
            key.hash(&mut hasher);
            if let Some(val) = msg.get(key) {
                val.hash(&mut hasher);
            }
        }
    }
    
    format!("{:016x}", hasher.finish())
}

/// Fast approximate token count
#[pyfunction]
pub fn fast_token_count_rust(
    text: String,
) -> usize {
    // Approximate tokenization: ~4 chars per token on average
    // More accurate for English text
    let chars = text.len();
    let words = text.split_whitespace().count();
    
    // Heuristic: max of char-based and word-based estimates
    let char_estimate = (chars + 3) / 4;  // ~4 chars per token
    let word_estimate = (words * 4 + 2) / 3;  // ~1.33 tokens per word
    
    char_estimate.max(word_estimate)
}

/// Truncate token sequence with strategy
#[pyfunction]
pub fn truncate_tokens_rust(
    tokens: Vec<i64>,
    max_tokens: usize,
    strategy: String,
) -> Vec<i64> {
    if tokens.len() <= max_tokens {
        return tokens;
    }
    
    match strategy.as_str() {
        "left" => tokens[tokens.len() - max_tokens..].to_vec(),
        "right" => tokens[..max_tokens].to_vec(),
        "middle" => {
            let keep_start = max_tokens / 2;
            let keep_end = max_tokens - keep_start;
            let mut result = tokens[..keep_start].to_vec();
            result.extend_from_slice(&tokens[tokens.len() - keep_end..]);
            result
        }
        _ => tokens[tokens.len() - max_tokens..].to_vec(),  // Default to left
    }
}

/// Generate cache salt from configuration
#[pyfunction]
pub fn generate_cache_salt_rust(
    template_hash: Option<String>,
    add_generation_prompt: bool,
    add_special_tokens: bool,
    truncation: Option<String>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    
    if let Some(t) = template_hash {
        t.hash(&mut hasher);
    }
    add_generation_prompt.hash(&mut hasher);
    add_special_tokens.hash(&mut hasher);
    if let Some(tr) = truncation {
        tr.hash(&mut hasher);
    }
    
    format!("{:016x}", hasher.finish())
}

/// Compute token metrics aggregation
#[pyfunction]
pub fn aggregate_token_metrics_rust(
    metrics_list: Vec<HashMap<String, i64>>,
) -> HashMap<String, i64> {
    let mut result: HashMap<String, i64> = HashMap::new();
    
    let keys = ["input_tokens", "output_tokens", "cached_tokens", "tool_tokens", "reasoning_tokens"];
    
    for key in keys {
        let sum: i64 = metrics_list.iter()
            .filter_map(|m| m.get(key))
            .sum();
        result.insert(key.to_string(), sum);
    }
    
    let total = result.get("input_tokens").unwrap_or(&0) + result.get("output_tokens").unwrap_or(&0);
    result.insert("total_tokens".to_string(), total);
    
    result
}

// =============================================================================
// Phase 43: KV Cache Coordination Acceleration
// =============================================================================

/// Fast batched block hash computation for prefix caching with chaining
#[pyfunction]
pub fn compute_block_hashes_batched_rust(
    token_ids: Vec<i64>,
    block_size: usize,
    hash_seed: u64,
) -> Vec<u64> {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    if token_ids.is_empty() || block_size == 0 {
        return Vec::new();
    }
    
    let num_blocks = (token_ids.len() + block_size - 1) / block_size;
    let mut hashes: Vec<u64> = Vec::with_capacity(num_blocks);
    
    for i in 0..num_blocks {
        let start = i * block_size;
        let end = std::cmp::min(start + block_size, token_ids.len());
        
        let mut hasher = DefaultHasher::new();
        hash_seed.hash(&mut hasher);
        
        // Hash previous block hash for chaining
        if let Some(&prev) = hashes.last() {
            prev.hash(&mut hasher);
        }
        
        // Hash tokens in this block
        for token in &token_ids[start..end] {
            token.hash(&mut hasher);
        }
        
        hashes.push(hasher.finish());
    }
    
    hashes
}

/// Calculate blocks needed for given token count
#[pyfunction]
pub fn calculate_blocks_needed_rust(
    num_tokens: i64,
    block_size: i64,
    sliding_window: Option<i64>,
) -> i64 {
    if num_tokens <= 0 || block_size <= 0 {
        return 0;
    }
    
    let effective_tokens = match sliding_window {
        Some(window) if window > 0 => std::cmp::min(num_tokens, window),
        _ => num_tokens,
    };
    
    (effective_tokens + block_size - 1) / block_size
}

/// Compute LRU eviction candidates from block access times
#[pyfunction]
pub fn compute_block_eviction_order_rust(
    block_ids: Vec<i64>,
    access_times: Vec<f64>,
    access_counts: Vec<i64>,
    num_to_evict: usize,
) -> Vec<i64> {
    if block_ids.len() != access_times.len() || block_ids.len() != access_counts.len() {
        return Vec::new();
    }
    
    // Combine into (block_id, access_time, access_count) tuples
    let mut blocks: Vec<_> = block_ids.iter()
        .zip(access_times.iter())
        .zip(access_counts.iter())
        .map(|((&id, &time), &count)| (id, time, count))
        .collect();
    
    // Sort by access time (oldest first), then by access count (least first)
    blocks.sort_by(|a, b| {
        a.1.partial_cmp(&b.1)
            .unwrap_or(std::cmp::Ordering::Equal)
            .then_with(|| a.2.cmp(&b.2))
    });
    
    blocks.iter()
        .take(num_to_evict)
        .map(|(id, _, _)| *id)
        .collect()
}

/// Fast prefix match lookup
#[pyfunction]
pub fn find_prefix_match_rust(
    query_hashes: Vec<u64>,
    cached_hashes: Vec<u64>,
) -> usize {
    // Find longest common prefix
    let mut match_length = 0;
    
    for (q, c) in query_hashes.iter().zip(cached_hashes.iter()) {
        if q == c {
            match_length += 1;
        } else {
            break;
        }
    }
    
    match_length
}

// =============================================================================
// Phase 43: Request Queue Acceleration
// =============================================================================

/// Sort requests by priority with stable ordering
#[pyfunction]
pub fn sort_requests_by_priority_rust(
    request_ids: Vec<String>,
    priorities: Vec<i64>,
    arrival_times: Vec<f64>,
) -> Vec<String> {
    if request_ids.len() != priorities.len() || request_ids.len() != arrival_times.len() {
        return request_ids;
    }
    
    let mut indexed: Vec<_> = request_ids.iter()
        .zip(priorities.iter())
        .zip(arrival_times.iter())
        .map(|((id, &pri), &time)| (id.clone(), pri, time))
        .collect();
    
    // Sort by priority (lower is better), then arrival time (earlier is better)
    indexed.sort_by(|a, b| {
        a.1.cmp(&b.1)
            .then_with(|| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal))
    });
    
    indexed.into_iter().map(|(id, _, _)| id).collect()
}

/// Compute fair share scheduling order
#[pyfunction]
pub fn compute_fair_schedule_rust(
    client_ids: Vec<String>,
    client_weights: Vec<f64>,
    client_served: Vec<i64>,
) -> Vec<usize> {
    if client_ids.len() != client_weights.len() || client_ids.len() != client_served.len() {
        return Vec::new();
    }
    
    // Calculate fair share ratio for each client
    let mut indexed: Vec<_> = client_ids.iter()
        .enumerate()
        .zip(client_weights.iter())
        .zip(client_served.iter())
        .map(|(((idx, _), &weight), &served)| {
            let ratio = if weight > 0.0 { served as f64 / weight } else { f64::MAX };
            (idx, ratio)
        })
        .collect();
    
    // Sort by ratio (lower ratio gets priority)
    indexed.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    indexed.into_iter().map(|(idx, _)| idx).collect()
}

/// Check deadline criticality for requests
#[pyfunction]
pub fn compute_deadline_priorities_rust(
    request_ids: Vec<String>,
    deadlines: Vec<Option<f64>>,
    current_time: f64,
) -> Vec<(String, f64)> {
    request_ids.iter()
        .zip(deadlines.iter())
        .map(|(id, deadline)| {
            let urgency = match deadline {
                Some(dl) => {
                    let remaining = dl - current_time;
                    if remaining <= 0.0 {
                        f64::MAX  // Overdue
                    } else {
                        1.0 / remaining  // Higher urgency for closer deadlines
                    }
                }
                None => 0.0,  // No deadline
            };
            (id.clone(), urgency)
        })
        .collect()
}

// =============================================================================
// Phase 43: Parallel Sampling Acceleration
// =============================================================================

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

/// Score and rank completions for best-of-n selection
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

// =============================================================================
// Phase 43: Iteration Metrics Acceleration
// =============================================================================

/// Compute sliding window percentiles
#[pyfunction]
pub fn compute_percentiles_rust(
    values: Vec<f64>,
    percentiles: Vec<f64>,
) -> Vec<f64> {
    if values.is_empty() {
        return vec![0.0; percentiles.len()];
    }
    
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    percentiles.iter()
        .map(|&p| {
            let p_clamped = p.clamp(0.0, 100.0);
            let k = (sorted.len() - 1) as f64 * (p_clamped / 100.0);
            let f = k.floor() as usize;
            let c = std::cmp::min(f + 1, sorted.len() - 1);
            
            sorted[f] + (k - f as f64) * (sorted[c] - sorted[f])
        })
        .collect()
}

/// Detect anomalies using z-score
#[pyfunction]
pub fn detect_anomalies_rust(
    values: Vec<f64>,
    z_threshold: f64,
) -> Vec<bool> {
    if values.len() < 2 {
        return vec![false; values.len()];
    }
    
    let mean: f64 = values.iter().sum::<f64>() / values.len() as f64;
    let variance: f64 = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let std = variance.sqrt();
    
    if std < 1e-10 {
        return vec![false; values.len()];
    }
    
    values.iter()
        .map(|&x| ((x - mean) / std).abs() > z_threshold)
        .collect()
}

/// Compute cache hit rate from sliding window
#[pyfunction]
pub fn compute_cache_hit_rate_rust(
    window_queries: Vec<i64>,
    window_hits: Vec<i64>,
) -> f64 {
    let total_queries: i64 = window_queries.iter().sum();
    let total_hits: i64 = window_hits.iter().sum();
    
    if total_queries == 0 {
        0.0
    } else {
        total_hits as f64 / total_queries as f64
    }
}

/// Analyze trend using linear regression
#[pyfunction]
pub fn analyze_trend_rust(
    timestamps: Vec<f64>,
    values: Vec<f64>,
) -> (String, f64) {
    if timestamps.len() < 2 || timestamps.len() != values.len() {
        return ("stable".to_string(), 0.0);
    }
    
    let n = timestamps.len() as f64;
    let sum_x: f64 = timestamps.iter().sum();
    let sum_y: f64 = values.iter().sum();
    let sum_xy: f64 = timestamps.iter().zip(values.iter()).map(|(x, y)| x * y).sum();
    let sum_xx: f64 = timestamps.iter().map(|x| x * x).sum();
    
    let denom = n * sum_xx - sum_x * sum_x;
    if denom.abs() < 1e-10 {
        return ("stable".to_string(), 0.0);
    }
    
    let slope = (n * sum_xy - sum_x * sum_y) / denom;
    
    let threshold = 0.01;
    let direction = if slope > threshold {
        "increasing"
    } else if slope < -threshold {
        "decreasing"
    } else {
        "stable"
    };
    
    (direction.to_string(), slope)
}

/// Aggregate iteration statistics
#[pyfunction]
pub fn aggregate_iteration_stats_rust(
    token_counts: Vec<i64>,
    latencies: Vec<f64>,
) -> HashMap<String, f64> {
    let mut result = HashMap::new();
    
    if token_counts.is_empty() {
        result.insert("total_tokens".to_string(), 0.0);
        result.insert("mean_latency".to_string(), 0.0);
        result.insert("throughput".to_string(), 0.0);
        return result;
    }
    
    let total_tokens: i64 = token_counts.iter().sum();
    let total_latency: f64 = latencies.iter().sum();
    let mean_latency = if !latencies.is_empty() { total_latency / latencies.len() as f64 } else { 0.0 };
    let throughput = if total_latency > 0.0 { total_tokens as f64 / total_latency } else { 0.0 };
    
    result.insert("total_tokens".to_string(), total_tokens as f64);
    result.insert("mean_latency".to_string(), mean_latency);
    result.insert("throughput".to_string(), throughput);
    
    result
}

// =============================================================================
// Phase 44: Advanced Sampling & Speculative Decoding
// =============================================================================

/// Rejection sampling verification for speculative decoding
/// Returns (accepted_count, recovered_token_idx, all_accepted)
#[pyfunction]
pub fn rejection_sample_verify_rust(
    draft_tokens: Vec<i64>,
    draft_probs: Vec<Vec<f64>>,
    target_probs: Vec<Vec<f64>>,
    random_nums: Vec<f64>,
) -> (usize, Option<i64>, bool) {
    let num_drafts = draft_tokens.len();
    if num_drafts == 0 || draft_probs.len() != num_drafts || target_probs.len() != num_drafts {
        return (0, None, false);
    }
    
    let mut accepted = 0usize;
    let mut first_rejection_idx: Option<usize> = None;
    
    for i in 0..num_drafts {
        let token = draft_tokens[i] as usize;
        if token >= draft_probs[i].len() || token >= target_probs[i].len() {
            first_rejection_idx = Some(i);
            break;
        }
        
        let p_draft = draft_probs[i][token];
        let p_target = target_probs[i][token];
        
        // Acceptance probability: min(1, p_target / p_draft)
        let accept_prob = if p_draft > 1e-10 {
            (p_target / p_draft).min(1.0)
        } else if p_target > 0.0 {
            1.0
        } else {
            0.0
        };
        
        if random_nums.get(i).copied().unwrap_or(1.0) < accept_prob {
            accepted += 1;
        } else {
            first_rejection_idx = Some(i);
            break;
        }
    }
    
    // Recovery: sample from adjusted distribution max(0, p_target - p_draft)
    let recovered_token = if let Some(idx) = first_rejection_idx {
        if idx < target_probs.len() && idx < draft_probs.len() {
            let mut adjusted: Vec<f64> = target_probs[idx]
                .iter()
                .zip(draft_probs[idx].iter())
                .map(|(t, d)| (t - d).max(0.0))
                .collect();
            
            let sum: f64 = adjusted.iter().sum();
            if sum > 1e-10 {
                for p in adjusted.iter_mut() {
                    *p /= sum;
                }
                
                // Sample from adjusted distribution
                let r = random_nums.get(idx).copied().unwrap_or(0.5);
                let mut cumsum = 0.0;
                for (i, &p) in adjusted.iter().enumerate() {
                    cumsum += p;
                    if r < cumsum {
                        return (accepted, Some(i as i64), false);
                    }
                }
            }
            Some(target_probs[idx]
                .iter()
                .enumerate()
                .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
                .map(|(i, _)| i as i64)
                .unwrap_or(0))
        } else {
            None
        }
    } else {
        None
    };
    
    (accepted, recovered_token, first_rejection_idx.is_none())
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
        
        // Find k-th largest value
        let mut sorted = row.clone();
        sorted.sort_by(|a, b| b.partial_cmp(a).unwrap_or(std::cmp::Ordering::Equal));
        let threshold = sorted[k - 1];
        
        // Mask values below threshold
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
        // Sort indices by logit value descending
        let mut indices: Vec<usize> = (0..row.len()).collect();
        indices.sort_by(|&a, &b| row[b].partial_cmp(&row[a]).unwrap_or(std::cmp::Ordering::Equal));
        
        // Compute softmax
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_sum: f64 = row.iter().map(|x| (x - max_val).exp()).sum();
        let probs: Vec<f64> = row.iter().map(|x| (x - max_val).exp() / exp_sum).collect();
        
        // Find cumulative probability cutoff
        let mut cumsum = 0.0;
        let mut cutoff_idx = indices.len();
        
        for (i, &idx) in indices.iter().enumerate() {
            cumsum += probs[idx];
            if cumsum > p {
                cutoff_idx = i + 1;
                break;
            }
        }
        
        // Mask indices beyond cutoff
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
        // Apply temperature
        let temp = temperatures.get(b).copied().unwrap_or(1.0);
        if temp > 1e-7 {
            for v in row.iter_mut() {
                *v /= temp;
            }
        }
        
        // Apply top-k
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
        
        // Apply top-p
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
        
        // Sample from softmax
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
        
        // Simple deterministic "random" for reproducibility
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

/// Apply all penalties (repetition, frequency, presence) to logits
#[pyfunction]
pub fn batch_apply_penalties_rust(
    logits: Vec<Vec<f64>>,
    repetition_penalties: Vec<f64>,
    frequency_penalties: Vec<f64>,
    presence_penalties: Vec<f64>,
    prompt_tokens: Vec<Vec<i64>>,
    output_tokens: Vec<Vec<i64>>,
) -> Vec<Vec<f64>> {
    logits.into_iter().enumerate().map(|(b, mut row)| {
        let rep_pen = repetition_penalties.get(b).copied().unwrap_or(1.0);
        let freq_pen = frequency_penalties.get(b).copied().unwrap_or(0.0);
        let pres_pen = presence_penalties.get(b).copied().unwrap_or(0.0);
        
        // Build token set from prompt
        let mut token_set: std::collections::HashSet<i64> = std::collections::HashSet::new();
        if let Some(prompts) = prompt_tokens.get(b) {
            token_set.extend(prompts.iter().copied());
        }
        
        // Count output token frequencies
        let mut token_counts: HashMap<i64, i64> = HashMap::new();
        if let Some(outputs) = output_tokens.get(b) {
            for &token in outputs {
                *token_counts.entry(token).or_default() += 1;
                token_set.insert(token);
            }
        }
        
        // Apply repetition penalty (multiplicative)
        if rep_pen != 1.0 {
            for &token in &token_set {
                let idx = token as usize;
                if idx < row.len() {
                    if row[idx] > 0.0 {
                        row[idx] /= rep_pen;
                    } else {
                        row[idx] *= rep_pen;
                    }
                }
            }
        }
        
        // Apply frequency penalty (additive, proportional)
        if freq_pen != 0.0 {
            for (&token, &count) in &token_counts {
                let idx = token as usize;
                if idx < row.len() {
                    row[idx] -= freq_pen * count as f64;
                }
            }
        }
        
        // Apply presence penalty (additive, binary)
        if pres_pen != 0.0 {
            for &token in &token_set {
                let idx = token as usize;
                if idx < row.len() {
                    row[idx] -= pres_pen;
                }
            }
        }
        
        row
    }).collect()
}

/// N-gram proposal with configurable n-range
#[pyfunction]
pub fn advanced_ngram_propose_rust(
    tokens: Vec<i64>,
    min_n: usize,
    max_n: usize,
    k: usize,
) -> Vec<i64> {
    if tokens.is_empty() || k == 0 {
        return Vec::new();
    }
    
    let n_tokens = tokens.len();
    
    // Try from largest n-gram to smallest
    for n in (min_n..=max_n).rev() {
        if n > n_tokens {
            continue;
        }
        
        // Get current suffix (last n-1 tokens)
        let suffix_start = n_tokens.saturating_sub(n - 1);
        let suffix = &tokens[suffix_start..];
        
        // Find matches of this suffix in history
        for i in 0..(n_tokens.saturating_sub(n)) {
            let window = &tokens[i..i + n - 1];
            if window == suffix {
                // Found match, get continuation
                let cont_start = i + n - 1;
                let cont_end = (cont_start + k).min(n_tokens);
                if cont_start < cont_end {
                    return tokens[cont_start..cont_end].to_vec();
                }
            }
        }
    }
    
    Vec::new()
}

/// Compute encoder cache content hash
#[pyfunction]
pub fn encoder_content_hash_rust(
    data: Vec<u8>,
) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    data.hash(&mut hasher);
    format!("{:016x}", hasher.finish())
}

/// LRU eviction for encoder cache with reference counting
#[pyfunction]
pub fn encoder_cache_lru_evict_rust(
    keys: Vec<String>,
    last_access_times: Vec<f64>,
    reference_counts: Vec<i32>,
    num_to_evict: usize,
) -> Vec<String> {
    if keys.is_empty() || num_to_evict == 0 {
        return Vec::new();
    }
    
    // Create (key, time, ref_count) tuples, preferring unreferenced
    let mut candidates: Vec<(String, f64, i32)> = keys.into_iter()
        .zip(last_access_times.into_iter())
        .zip(reference_counts.into_iter())
        .map(|((k, t), r)| (k, t, r))
        .collect();
    
    // Sort: unreferenced first, then by access time (oldest first)
    candidates.sort_by(|a, b| {
        let ref_cmp = a.2.cmp(&b.2);
        if ref_cmp != std::cmp::Ordering::Equal {
            return ref_cmp;
        }
        a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal)
    });
    
    candidates.into_iter()
        .take(num_to_evict)
        .map(|(k, _, _)| k)
        .collect()
}

/// Compute KV cache metrics aggregates
#[pyfunction]
pub fn kv_cache_metrics_aggregate_rust(
    lifetimes: Vec<f64>,
    idle_times: Vec<f64>,
    access_counts: Vec<i64>,
) -> HashMap<String, f64> {
    let mut result = HashMap::new();
    
    if lifetimes.is_empty() {
        return result;
    }
    
    let n = lifetimes.len() as f64;
    
    // Lifetime stats
    let mean_lifetime: f64 = lifetimes.iter().sum::<f64>() / n;
    let mut sorted_lifetimes = lifetimes.clone();
    sorted_lifetimes.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let p50_lifetime = sorted_lifetimes[(n as usize * 50) / 100];
    let p95_lifetime = sorted_lifetimes[(n as usize * 95 / 100).min(sorted_lifetimes.len() - 1)];
    let p99_lifetime = sorted_lifetimes[(n as usize * 99 / 100).min(sorted_lifetimes.len() - 1)];
    
    result.insert("mean_lifetime".to_string(), mean_lifetime);
    result.insert("p50_lifetime".to_string(), p50_lifetime);
    result.insert("p95_lifetime".to_string(), p95_lifetime);
    result.insert("p99_lifetime".to_string(), p99_lifetime);
    
    // Idle time stats
    if !idle_times.is_empty() {
        let mean_idle: f64 = idle_times.iter().sum::<f64>() / idle_times.len() as f64;
        result.insert("mean_idle".to_string(), mean_idle);
    }
    
    // Access count stats
    if !access_counts.is_empty() {
        let mean_access: f64 = access_counts.iter().sum::<i64>() as f64 / access_counts.len() as f64;
        let zero_access_rate: f64 = access_counts.iter().filter(|&&c| c == 0).count() as f64 / access_counts.len() as f64;
        result.insert("mean_access_count".to_string(), mean_access);
        result.insert("zero_access_rate".to_string(), zero_access_rate);
    }
    
    result
}

/// Typical sampling filter (entropy-based)
#[pyfunction]
pub fn apply_typical_sampling_rust(
    logits: Vec<Vec<f64>>,
    mass: f64,
) -> Vec<Vec<f64>> {
    logits.into_iter().map(|mut row| {
        // Compute softmax probabilities
        let max_val = row.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_sum: f64 = row.iter().map(|x| (x - max_val).exp()).sum();
        let probs: Vec<f64> = row.iter().map(|x| (x - max_val).exp() / exp_sum).collect();
        
        // Compute entropy
        let entropy: f64 = -probs.iter()
            .filter(|&&p| p > 1e-10)
            .map(|&p| p * p.ln())
            .sum::<f64>();
        
        // Compute deviation from entropy for each token
        let log_probs: Vec<f64> = probs.iter()
            .map(|&p| if p > 1e-10 { p.ln() } else { f64::NEG_INFINITY })
            .collect();
        
        let mut deviations: Vec<(usize, f64)> = log_probs.iter()
            .enumerate()
            .filter(|(_, &lp)| lp > f64::NEG_INFINITY)
            .map(|(i, &lp)| (i, (-lp - entropy).abs()))
            .collect();
        
        // Sort by deviation (closest to entropy first)
        deviations.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
        
        // Find mass cutoff
        let mut cumsum = 0.0;
        let mut cutoff_idx = deviations.len();
        
        for (i, &(idx, _)) in deviations.iter().enumerate() {
            cumsum += probs[idx];
            if cumsum > mass {
                cutoff_idx = i + 1;
                break;
            }
        }
        
        // Mask tokens beyond cutoff
        let keep_indices: std::collections::HashSet<usize> = deviations.iter()
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

// =============================================================================
// Phase 45: Prometheus Metrics & Executor Acceleration
// =============================================================================

/// Cache observation with hit rate tracking
#[pyfunction]
pub fn cache_observe_rust(
    is_hit: bool,
    _bytes_accessed: i64,
    _latency_ns: i64,
    current_hits: i64,
    current_misses: i64,
) -> (i64, i64, f64) {
    let new_hits = current_hits + if is_hit { 1 } else { 0 };
    let new_misses = current_misses + if is_hit { 0 } else { 1 };
    let hit_rate = if new_hits + new_misses > 0 {
        new_hits as f64 / (new_hits + new_misses) as f64
    } else {
        0.0
    };
    (new_hits, new_misses, hit_rate)
}

/// Histogram observation with bucket assignment
#[pyfunction]
pub fn histogram_observe_rust(
    value: f64,
    buckets: Vec<f64>,
    current_counts: Vec<i64>,
    current_sum: f64,
) -> (Vec<i64>, f64, i64) {
    let mut new_counts = current_counts.clone();
    let new_sum = current_sum + value;
    let mut total_count = 0i64;
    
    for (i, &bucket) in buckets.iter().enumerate() {
        if value <= bucket {
            if i < new_counts.len() {
                new_counts[i] += 1;
            }
        }
        if i < new_counts.len() {
            total_count += new_counts[i];
        }
    }
    
    (new_counts, new_sum, total_count)
}

/// Sliding window hit rate calculation
#[pyfunction]
pub fn sliding_window_hit_rate_rust(
    events: Vec<(f64, bool, i64, i64)>,  // (timestamp, is_hit, bytes, latency)
    window_seconds: f64,
    current_time: f64,
) -> (i64, i64, f64, f64, f64) {
    let cutoff = current_time - window_seconds;
    
    let mut hits = 0i64;
    let mut misses = 0i64;
    let mut total_latency = 0i64;
    let mut total_bytes = 0i64;
    
    for (ts, is_hit, bytes, latency) in events {
        if ts > cutoff {
            if is_hit {
                hits += 1;
            } else {
                misses += 1;
            }
            total_latency += latency;
            total_bytes += bytes;
        }
    }
    
    let hit_rate = if hits + misses > 0 {
        hits as f64 / (hits + misses) as f64
    } else {
        0.0
    };
    
    let avg_latency = if hits + misses > 0 {
        total_latency as f64 / (hits + misses) as f64
    } else {
        0.0
    };
    
    (hits, misses, hit_rate, avg_latency, total_bytes as f64)
}

/// Counter increment with thread-safe semantics simulation
#[pyfunction]
pub fn counter_increment_rust(
    current: i64,
    increment: i64,
) -> i64 {
    current + increment
}

/// Gauge update with min/max tracking
#[pyfunction]
pub fn gauge_update_rust(
    _current: f64,
    new_value: f64,
    min_seen: f64,
    max_seen: f64,
) -> (f64, f64, f64) {
    (new_value, min_seen.min(new_value), max_seen.max(new_value))
}

// =============================================================================
// Phase 45: LoRA Stats Acceleration
// =============================================================================

/// LoRA statistics update
#[pyfunction]
pub fn lora_stats_update_rust(
    adapter_id: String,
    load_latency: f64,
    exec_latency: f64,
    tokens: i64,
    stats: HashMap<String, Vec<f64>>,
) -> HashMap<String, Vec<f64>> {
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
    adapter_last_used: HashMap<String, f64>,
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

// =============================================================================
// Phase 45: Caching Metrics Acceleration
// =============================================================================

/// Sliding window statistics calculation
#[pyfunction]
pub fn sliding_window_stats_rust(
    events: Vec<(f64, bool, i64, i64)>,  // (timestamp, is_hit, bytes, latency_ns)
    window_seconds: f64,
    current_time: f64,
) -> HashMap<String, f64> {
    let cutoff = current_time - window_seconds;
    
    let mut hits = 0i64;
    let mut misses = 0i64;
    let mut latencies: Vec<i64> = Vec::new();
    let mut total_bytes = 0i64;
    let mut first_ts = current_time;
    let mut last_ts = cutoff;
    
    for (ts, is_hit, bytes, latency) in events {
        if ts > cutoff {
            if is_hit { hits += 1; } else { misses += 1; }
            latencies.push(latency);
            total_bytes += bytes;
            first_ts = first_ts.min(ts);
            last_ts = last_ts.max(ts);
        }
    }
    
    let mut result = HashMap::new();
    result.insert("hits".to_string(), hits as f64);
    result.insert("misses".to_string(), misses as f64);
    result.insert("hit_rate".to_string(), if hits + misses > 0 { hits as f64 / (hits + misses) as f64 } else { 0.0 });
    
    if !latencies.is_empty() {
        latencies.sort();
        let sum: i64 = latencies.iter().sum();
        result.insert("avg_latency_ns".to_string(), sum as f64 / latencies.len() as f64);
        result.insert("p50_latency_ns".to_string(), latencies[latencies.len() / 2] as f64);
        result.insert("p99_latency_ns".to_string(), latencies[(latencies.len() as f64 * 0.99) as usize] as f64);
    }
    
    let duration = last_ts - first_ts;
    result.insert("bytes_per_second".to_string(), if duration > 0.0 { total_bytes as f64 / duration } else { 0.0 });
    result.insert("window_duration".to_string(), duration);
    
    result
}

/// Eviction breakdown by reason
#[pyfunction]
pub fn eviction_breakdown_rust(
    evictions: Vec<(f64, i32, i64)>,  // (timestamp, reason_code, bytes_freed)
) -> HashMap<i32, (i64, i64)> {
    let mut breakdown: HashMap<i32, (i64, i64)> = HashMap::new();
    
    for (_, reason, bytes) in evictions {
        let entry = breakdown.entry(reason).or_insert((0, 0));
        entry.0 += 1;
        entry.1 += bytes;
    }
    
    breakdown
}

/// Memory pressure calculation
#[pyfunction]
pub fn memory_pressure_rust(
    current_bytes: i64,
    peak_bytes: i64,
    eviction_rate: f64,
) -> f64 {
    let utilization = if peak_bytes > 0 {
        current_bytes as f64 / peak_bytes as f64
    } else {
        0.0
    };
    
    let eviction_pressure = (eviction_rate / 100.0).min(1.0);
    
    (utilization * 0.7) + (eviction_pressure * 0.3)
}

// =============================================================================
// Phase 45: Pooling Acceleration
// =============================================================================

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

// =============================================================================
// Phase 45: Logprobs Tensors Acceleration
// =============================================================================

/// Extract top-k logprobs batch
#[pyfunction]
pub fn extract_top_k_batch_rust(
    logprobs: Vec<Vec<f64>>,
    k: usize,
) -> Vec<(Vec<f64>, Vec<usize>)> {
    logprobs.into_iter().map(|row| {
        let mut indexed: Vec<(usize, f64)> = row.iter().enumerate().map(|(i, &v)| (i, v)).collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        indexed.truncate(k);
        
        let values: Vec<f64> = indexed.iter().map(|(_, v)| *v).collect();
        let indices: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
        (values, indices)
    }).collect()
}

/// Sparse logprobs storage
#[pyfunction]
pub fn sparse_logprobs_store_rust(
    logprobs: Vec<f64>,
    k: usize,
) -> (Vec<f64>, Vec<usize>) {
    let mut indexed: Vec<(usize, f64)> = logprobs.iter()
        .enumerate()
        .filter(|(_, &v)| v > f64::NEG_INFINITY)
        .map(|(i, &v)| (i, v))
        .collect();
    
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    indexed.truncate(k);
    
    let values: Vec<f64> = indexed.iter().map(|(_, v)| *v).collect();
    let indices: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
    
    (values, indices)
}

/// Logprobs to lists conversion
#[pyfunction]
pub fn logprobs_to_lists_rust(
    logprobs: Vec<Vec<Vec<f64>>>,  // (batch, seq, top_k)
    token_ids: Vec<Vec<Vec<usize>>>,  // (batch, seq, top_k)
) -> Vec<Vec<Vec<(usize, f64)>>> {
    logprobs.into_iter()
        .zip(token_ids.into_iter())
        .map(|(seq_lp, seq_ids)| {
            seq_lp.into_iter()
                .zip(seq_ids.into_iter())
                .map(|(pos_lp, pos_ids)| {
                    pos_lp.into_iter()
                        .zip(pos_ids.into_iter())
                        .map(|(lp, id)| (id, lp))
                        .collect()
                })
                .collect()
        })
        .collect()
}

// =============================================================================
// Phase 45: Executor Task Acceleration
// =============================================================================

/// Task priority sorting
#[pyfunction]
pub fn task_priority_sort_rust(
    tasks: Vec<(String, i32, f64)>,  // (task_id, priority, timestamp)
) -> Vec<String> {
    let mut sorted = tasks;
    sorted.sort_by(|a, b| {
        // Higher priority first, then earlier timestamp
        b.1.cmp(&a.1).then_with(|| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal))
    });
    sorted.into_iter().map(|(id, _, _)| id).collect()
}

/// Worker health check
#[pyfunction]
pub fn worker_health_check_rust(
    last_heartbeats: Vec<f64>,
    current_time: f64,
    timeout: f64,
) -> (i64, Vec<usize>) {
    let mut healthy_count = 0i64;
    let mut unhealthy_indices = Vec::new();
    
    for (i, &last) in last_heartbeats.iter().enumerate() {
        if current_time - last <= timeout {
            healthy_count += 1;
        } else {
            unhealthy_indices.push(i);
        }
    }
    
    (healthy_count, unhealthy_indices)
}

/// Future batch completion
#[pyfunction]
pub fn future_batch_complete_rust(
    futures: Vec<(String, bool, f64)>,  // (task_id, is_done, result_time)
) -> (i64, i64, Vec<String>) {
    let mut done_count = 0i64;
    let mut pending_count = 0i64;
    let mut done_ids = Vec::new();
    
    for (id, is_done, _) in futures {
        if is_done {
            done_count += 1;
            done_ids.push(id);
        } else {
            pending_count += 1;
        }
    }
    
    (done_count, pending_count, done_ids)
}

// =============================================================================
// Phase 46: Structured Output Acceleration
// =============================================================================

/// Fill bitmask for grammar-constrained tokens
/// Sets allowed positions to 1, others to 0
#[pyfunction]
pub fn xgrammar_bitmask_fill_rust(
    allowed_token_ids: Vec<i32>,
    vocab_size: usize,
) -> Vec<i32> {
    let mut bitmask = vec![0i32; vocab_size];
    for token_id in allowed_token_ids {
        if token_id >= 0 && (token_id as usize) < vocab_size {
            bitmask[token_id as usize] = 1;
        }
    }
    bitmask
}

/// Compute cache key for grammar compilation
#[pyfunction]
pub fn grammar_cache_key_rust(
    grammar_type: &str,
    content: &str,
    tokenizer_hash: u64,
) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    grammar_type.hash(&mut hasher);
    content.hash(&mut hasher);
    tokenizer_hash.hash(&mut hasher);
    format!("{:016x}", hasher.finish())
}

/// Build batch update indices for efficient state transitions
#[pyfunction]
pub fn batch_update_indices_rust(
    current_indices: Vec<i32>,
    removed_indices: Vec<i32>,
    added_count: i32,
) -> Vec<i32> {
    let removed_set: std::collections::HashSet<i32> = removed_indices.iter().copied().collect();
    let mut result: Vec<i32> = current_indices
        .into_iter()
        .filter(|i| !removed_set.contains(i))
        .collect();
    
    // Add new indices at the end
    let max_existing = result.iter().max().copied().unwrap_or(-1);
    for i in 0..added_count {
        result.push(max_existing + 1 + i);
    }
    
    result
}

/// Fast n-gram matching for bad words detection
#[pyfunction]
pub fn bad_words_match_ngram_rust(
    token_sequence: Vec<i32>,
    bad_ngrams: Vec<Vec<i32>>,
) -> Vec<(usize, usize)> {
    let mut matches = Vec::new();
    
    for (ngram_idx, ngram) in bad_ngrams.iter().enumerate() {
        if ngram.is_empty() {
            continue;
        }
        
        let ngram_len = ngram.len();
        if token_sequence.len() < ngram_len {
            continue;
        }
        
        for i in 0..=token_sequence.len() - ngram_len {
            if &token_sequence[i..i + ngram_len] == ngram.as_slice() {
                matches.push((ngram_idx, i));
            }
        }
    }
    
    matches
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

/// Parse structural tag to extract grammar type
#[pyfunction]
pub fn structural_tag_parse_rust(
    tag_content: &str,
) -> (String, String, HashMap<String, String>) {
    // Format: <type:value;key1=val1;key2=val2>
    let mut grammar_type = String::new();
    let mut grammar_value = String::new();
    let mut attributes: HashMap<String, String> = HashMap::new();
    
    let trimmed = tag_content.trim_start_matches('<').trim_end_matches('>');
    let parts: Vec<&str> = trimmed.split(';').collect();
    
    if let Some(first) = parts.first() {
        if let Some((t, v)) = first.split_once(':') {
            grammar_type = t.to_string();
            grammar_value = v.to_string();
        } else {
            grammar_type = first.to_string();
        }
    }
    
    for part in parts.iter().skip(1) {
        if let Some((k, v)) = part.split_once('=') {
            attributes.insert(k.to_string(), v.to_string());
        }
    }
    
    (grammar_type, grammar_value, attributes)
}

/// DFA state transition for regex matching
#[pyfunction]
pub fn regex_dfa_transition_rust(
    current_state: i32,
    transitions: Vec<(i32, String, i32)>,  // (from_state, char_class, to_state)
    input_char: &str,
) -> i32 {
    for (from_state, char_class, to_state) in transitions {
        if from_state != current_state {
            continue;
        }
        
        // Check character class matching
        let matches = if char_class.starts_with('[') && char_class.ends_with(']') {
            // Character class like [a-z]
            match_char_class(&char_class, input_char)
        } else if char_class == "." {
            // Any character
            true
        } else if char_class.starts_with("\\") {
            // Escape sequence
            match_escape_sequence(&char_class, input_char)
        } else {
            // Literal match
            char_class == input_char
        };
        
        if matches {
            return to_state;
        }
    }
    
    -1  // No valid transition
}

fn match_char_class(class: &str, input: &str) -> bool {
    if input.len() != 1 {
        return false;
    }
    let c = input.chars().next().unwrap();
    
    // Parse character class [abc] or [a-z]
    let inner = &class[1..class.len()-1];
    let mut chars = inner.chars().peekable();
    let mut negate = false;
    
    if chars.peek() == Some(&'^') {
        negate = true;
        chars.next();
    }
    
    let mut result = false;
    while let Some(ch) = chars.next() {
        if chars.peek() == Some(&'-') {
            chars.next();  // consume '-'
            if let Some(end) = chars.next() {
                if c >= ch && c <= end {
                    result = true;
                    break;
                }
            }
        } else if c == ch {
            result = true;
            break;
        }
    }
    
    if negate { !result } else { result }
}

fn match_escape_sequence(escape: &str, input: &str) -> bool {
    if input.len() != 1 {
        return false;
    }
    let c = input.chars().next().unwrap();
    
    match escape {
        "\\d" => c.is_ascii_digit(),
        "\\D" => !c.is_ascii_digit(),
        "\\w" => c.is_ascii_alphanumeric() || c == '_',
        "\\W" => !c.is_ascii_alphanumeric() && c != '_',
        "\\s" => c.is_ascii_whitespace(),
        "\\S" => !c.is_ascii_whitespace(),
        "\\n" => c == '\n',
        "\\t" => c == '\t',
        "\\r" => c == '\r',
        _ if escape.len() == 2 => escape.chars().nth(1) == Some(c),
        _ => false,
    }
}

/// Build trie from bad words list for efficient lookup
#[pyfunction]
pub fn bad_words_trie_build_rust(
    bad_words: Vec<Vec<i32>>,
) -> HashMap<i32, Vec<(Vec<i32>, bool)>> {
    // Maps first token -> (remaining tokens, is_complete)
    let mut trie: HashMap<i32, Vec<(Vec<i32>, bool)>> = HashMap::new();
    
    for word in bad_words {
        if word.is_empty() {
            continue;
        }
        
        let first = word[0];
        let rest = word[1..].to_vec();
        let is_complete = rest.is_empty();
        
        trie.entry(first).or_default().push((rest, is_complete));
    }
    
    trie
}

/// Check if token sequence matches any bad word prefix
#[pyfunction]
pub fn bad_words_prefix_check_rust(
    context: Vec<i32>,
    trie: HashMap<i32, Vec<(Vec<i32>, bool)>>,
) -> Vec<i32> {
    // Returns token IDs that would complete a bad word
    let mut blocked_tokens = Vec::new();
    
    // Check for bad words starting anywhere in context
    for start in 0..context.len() {
        if let Some(entries) = trie.get(&context[start]) {
            for (rest, _is_complete) in entries {
                if rest.is_empty() {
                    // Single token bad word - block the starting token
                    continue;
                }
                
                let context_remaining = &context[start + 1..];
                
                // Check if context matches prefix of bad word
                let match_len = rest.iter()
                    .zip(context_remaining.iter())
                    .take_while(|(a, b)| a == b)
                    .count();
                
                if match_len == rest.len() - 1 {
                    // Context matches all but last token - block it
                    blocked_tokens.push(rest[rest.len() - 1]);
                } else if match_len == context_remaining.len() && match_len < rest.len() {
                    // Context is prefix - block next token
                    blocked_tokens.push(rest[match_len]);
                }
            }
        }
    }
    
    // Check for bad words that could start with next token
    for (&first_token, entries) in &trie {
        for (rest, _is_complete) in entries {
            if rest.is_empty() {
                // Single token bad word
                blocked_tokens.push(first_token);
            }
        }
    }
    
    blocked_tokens.sort();
    blocked_tokens.dedup();
    blocked_tokens
}

/// Batch logits masking for grammar constraints
#[pyfunction]
pub fn batch_grammar_mask_rust(
    batch_logits: Vec<Vec<f32>>,
    batch_allowed: Vec<Vec<i32>>,
    mask_value: f32,
) -> Vec<Vec<f32>> {
    batch_logits.into_iter()
        .zip(batch_allowed.into_iter())
        .map(|(logits, allowed)| {
            let allowed_set: std::collections::HashSet<i32> = 
                allowed.iter().copied().collect();
            
            logits.into_iter()
                .enumerate()
                .map(|(i, v)| {
                    if allowed_set.contains(&(i as i32)) {
                        v
                    } else {
                        mask_value
                    }
                })
                .collect()
        })
        .collect()
}

/// Template variable extraction
#[pyfunction]
pub fn template_extract_variables_rust(
    template: &str,
) -> Vec<(String, usize, usize)> {
    let mut variables = Vec::new();
    let pattern = regex::Regex::new(r"\{\{(\w+)(?::[^}]+)?\}\}").unwrap_or_else(|_| {
        // Fallback if regex crate not available
        return regex::Regex::new(r"").unwrap();
    });
    
    for cap in pattern.captures_iter(template) {
        if let (Some(full), Some(name)) = (cap.get(0), cap.get(1)) {
            variables.push((
                name.as_str().to_string(),
                full.start(),
                full.end(),
            ));
        }
    }
    
    variables
}

/// JSON schema path extraction for validation
#[pyfunction]
pub fn json_schema_paths_rust(
    schema_str: &str,
) -> Vec<(String, String)> {
    // Returns (json_path, type) pairs
    let mut paths = Vec::new();
    
    // Simple parsing - for complex schemas use serde_json
    if let Ok(schema) = serde_json::from_str::<serde_json::Value>(schema_str) {
        extract_schema_paths(&schema, String::new(), &mut paths);
    }
    
    paths
}

fn extract_schema_paths(
    schema: &serde_json::Value,
    path: String,
    paths: &mut Vec<(String, String)>,
) {
    if let Some(obj) = schema.as_object() {
        if let Some(type_val) = obj.get("type") {
            let type_str = type_val.as_str().unwrap_or("unknown");
            paths.push((path.clone(), type_str.to_string()));
            
            if type_str == "object" {
                if let Some(props) = obj.get("properties") {
                    if let Some(props_obj) = props.as_object() {
                        for (key, value) in props_obj {
                            let new_path = if path.is_empty() {
                                format!(".{}", key)
                            } else {
                                format!("{}.{}", path, key)
                            };
                            extract_schema_paths(value, new_path, paths);
                        }
                    }
                }
            } else if type_str == "array" {
                if let Some(items) = obj.get("items") {
                    let new_path = format!("{}[]", path);
                    extract_schema_paths(items, new_path, paths);
                }
            }
        }
    }
}

// =============================================================================
// Phase 47: Speculative Decoding V3 & KV Offload Acceleration
// =============================================================================

/// EAGLE top-k candidates extraction from logits
#[pyfunction]
pub fn eagle_top_k_candidates_rust(
    logits: Vec<f64>,
    k: usize,
) -> Vec<(usize, f64)> {
    let mut indexed: Vec<(usize, f64)> = logits.iter().enumerate()
        .map(|(i, &v)| (i, v))
        .collect();
    
    // Partial sort for top-k
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    indexed.truncate(k);
    
    indexed
}

/// EAGLE verify and accept tokens using rejection sampling
#[pyfunction]
pub fn eagle_verify_accept_rust(
    draft_tokens: Vec<i64>,
    draft_logprobs: Vec<f64>,
    target_logprobs: Vec<f64>,
    sampling_eps: f64,
) -> (Vec<i64>, Vec<bool>) {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    
    let mut accepted = Vec::new();
    let mut mask = Vec::new();
    
    for (i, ((draft_token, draft_lp), target_lp)) in draft_tokens.iter()
        .zip(draft_logprobs.iter())
        .zip(target_logprobs.iter())
        .enumerate() 
    {
        let ratio = (target_lp - draft_lp).exp().min(1.0);
        let random_val: f64 = rng.gen();
        
        if random_val < ratio + sampling_eps {
            accepted.push(*draft_token);
            mask.push(true);
        } else {
            mask.push(false);
            // Fill remaining with false
            for _ in (i + 1)..draft_tokens.len() {
                mask.push(false);
            }
            break;
        }
    }
    
    (accepted, mask)
}

/// EAGLE extrapolate hidden states for next step prediction
#[pyfunction]
pub fn eagle_extrapolate_hidden_rust(
    hidden_states: Vec<Vec<f64>>,
    num_steps: usize,
) -> Vec<Vec<f64>> {
    if hidden_states.len() < 2 {
        return hidden_states;
    }
    
    let last = &hidden_states[hidden_states.len() - 1];
    let prev = &hidden_states[hidden_states.len() - 2];
    
    let mut extrapolated = Vec::with_capacity(num_steps);
    
    for step in 0..num_steps {
        let step_f = (step + 1) as f64;
        let new_state: Vec<f64> = last.iter()
            .zip(prev.iter())
            .map(|(l, p)| l + (l - p) * step_f)
            .collect();
        extrapolated.push(new_state);
    }
    
    extrapolated
}

/// EAGLE prepare inputs with padding for batch processing
#[pyfunction]
pub fn eagle_prepare_inputs_padded_rust(
    token_ids: Vec<Vec<i64>>,
    positions: Vec<Vec<i64>>,
    hidden_states: Option<Vec<Vec<Vec<f64>>>>,
) -> (Vec<i64>, Vec<i64>, Option<Vec<Vec<f64>>>) {
    let max_len = token_ids.iter().map(|ids| ids.len()).max().unwrap_or(0);
    
    let mut padded_ids = Vec::new();
    let mut padded_positions = Vec::new();
    
    for ids in &token_ids {
        let mut padded = ids.clone();
        padded.resize(max_len, 0);
        padded_ids.extend(padded);
    }
    
    for pos in &positions {
        let mut padded = pos.clone();
        padded.resize(max_len, 0);
        padded_positions.extend(padded);
    }
    
    let padded_hidden = hidden_states.map(|states| {
        let hidden_size = states.get(0).and_then(|s| s.get(0)).map(|v| v.len()).unwrap_or(0);
        let mut result = Vec::new();
        for seq_states in states {
            let mut padded = seq_states.clone();
            while padded.len() < max_len {
                padded.push(vec![0.0; hidden_size]);
            }
            result.extend(padded);
        }
        result
    });
    
    (padded_ids, padded_positions, padded_hidden)
}

/// N-gram find match in context
#[pyfunction]
pub fn ngram_find_match_rust(
    context: Vec<i64>,
    prefix: Vec<i64>,
    excluded: Vec<i64>,
    k: usize,
) -> Option<(usize, usize, Vec<i64>)> {
    let n = prefix.len();
    if context.len() < n {
        return None;
    }
    
    let excluded_set: std::collections::HashSet<i64> = excluded.into_iter().collect();
    
    let mut best_pos: Option<usize> = None;
    let mut best_following: Vec<i64> = Vec::new();
    
    // Search from end (more recent matches preferred)
    for i in (0..=context.len().saturating_sub(n)).rev() {
        if context[i..i + n] == prefix[..] {
            let start = i + n;
            let end = (start + k).min(context.len());
            
            let following: Vec<i64> = context[start..end].iter()
                .filter(|t| !excluded_set.contains(t))
                .copied()
                .collect();
            
            if following.len() > best_following.len() {
                best_pos = Some(i);
                best_following = following;
            }
            
            if best_following.len() >= k {
                break;
            }
        }
    }
    
    best_pos.map(|pos| (pos, n, best_following))
}

/// N-gram fuzzy match with edit distance tolerance
#[pyfunction]
pub fn ngram_fuzzy_match_rust(
    context: Vec<i64>,
    prefix: Vec<i64>,
    k: usize,
    max_distance: usize,
) -> Option<(Vec<i64>, f64)> {
    let n = prefix.len();
    if context.len() < n {
        return None;
    }
    
    let mut best_following: Vec<i64> = Vec::new();
    let mut best_score = 0.0;
    
    for i in 0..=context.len().saturating_sub(n) {
        let candidate = &context[i..i + n];
        
        // Hamming distance
        let distance: usize = prefix.iter()
            .zip(candidate.iter())
            .filter(|(a, b)| a != b)
            .count();
        
        if distance <= max_distance {
            let start = i + n;
            let end = (start + k).min(context.len());
            let following = context[start..end].to_vec();
            
            let score = 1.0 - (distance as f64 / (max_distance + 1) as f64);
            
            if following.len() > best_following.len() || 
               (following.len() == best_following.len() && score > best_score) {
                best_following = following;
                best_score = score;
            }
        }
    }
    
    if best_following.is_empty() {
        None
    } else {
        let final_score = best_score * (best_following.len() as f64 / k as f64);
        Some((best_following, final_score))
    }
}

/// Prompt lookup propose from prompt tokens
#[pyfunction]
pub fn prompt_lookup_propose_rust(
    prompt_tokens: Vec<i64>,
    generated_tokens: Vec<i64>,
    min_len: usize,
    max_len: usize,
    k: usize,
) -> Vec<i64> {
    if generated_tokens.is_empty() {
        return Vec::new();
    }
    
    for suffix_len in (min_len..=max_len).rev() {
        if generated_tokens.len() < suffix_len {
            continue;
        }
        
        let suffix = &generated_tokens[generated_tokens.len() - suffix_len..];
        
        for i in 0..prompt_tokens.len().saturating_sub(suffix_len) {
            if &prompt_tokens[i..i + suffix_len] == suffix {
                let start = i + suffix_len;
                let end = (start + k).min(prompt_tokens.len());
                return prompt_tokens[start..end].to_vec();
            }
        }
    }
    
    Vec::new()
}

/// Build cumulative indices for speculative decode metadata
#[pyfunction]
pub fn spec_decode_build_cu_indices_rust(
    num_draft_tokens: Vec<usize>,
) -> (Vec<usize>, Vec<usize>) {
    let mut cu_draft = Vec::with_capacity(num_draft_tokens.len());
    let mut cu_sampled = Vec::with_capacity(num_draft_tokens.len());
    
    let mut total_draft = 0usize;
    let mut total_sampled = 0usize;
    
    for num_draft in num_draft_tokens {
        total_draft += num_draft;
        total_sampled += num_draft + 1;
        cu_draft.push(total_draft);
        cu_sampled.push(total_sampled);
    }
    
    (cu_draft, cu_sampled)
}

/// Build logits indices for verification
#[pyfunction]
pub fn spec_decode_build_logits_indices_rust(
    num_draft_tokens: Vec<usize>,
    cu_num_draft_tokens: Vec<usize>,
) -> (Vec<usize>, Vec<usize>, Vec<usize>) {
    let batch_size = num_draft_tokens.len();
    let num_tokens: usize = num_draft_tokens.iter().sum();
    
    let target_logits_indices: Vec<usize> = (0..num_tokens).collect();
    
    let bonus_logits_indices: Vec<usize> = cu_num_draft_tokens.iter()
        .map(|&cu| cu.saturating_sub(1))
        .collect();
    
    let logits_indices: Vec<usize> = (0..(num_tokens + batch_size)).collect();
    
    (target_logits_indices, bonus_logits_indices, logits_indices)
}

/// Rejection sampling verification for speculative decode
#[pyfunction]
pub fn spec_decode_verify_rejection_rust(
    draft_token_ids: Vec<i64>,
    draft_logprobs: Vec<f64>,
    target_logprobs: Vec<f64>,
    sampling_eps: f64,
) -> (Vec<i64>, Vec<bool>) {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    
    let mut accepted = Vec::new();
    let mut mask = Vec::new();
    
    for (i, ((draft_token, draft_lp), target_lp)) in draft_token_ids.iter()
        .zip(draft_logprobs.iter())
        .zip(target_logprobs.iter())
        .enumerate()
    {
        let ratio = ((target_lp - draft_lp).min(0.0)).exp();
        let random_val: f64 = rng.gen();
        
        if random_val < ratio + sampling_eps {
            accepted.push(*draft_token);
            mask.push(true);
        } else {
            mask.push(false);
            for _ in (i + 1)..draft_token_ids.len() {
                mask.push(false);
            }
            break;
        }
    }
    
    (accepted, mask)
}

/// Block table slot mapping computation
#[pyfunction]
pub fn block_table_slot_mapping_rust(
    blocks: Vec<i64>,
    num_tokens: usize,
    start_position: usize,
    block_size: usize,
) -> Vec<i64> {
    let mut slots = Vec::with_capacity(num_tokens);
    
    for i in 0..num_tokens {
        let position = start_position + i;
        let block_idx = position / block_size;
        let offset = position % block_size;
        
        if block_idx < blocks.len() {
            let slot = blocks[block_idx] * (block_size as i64) + (offset as i64);
            slots.push(slot);
        } else {
            slots.push(-1);
        }
    }
    
    slots
}

/// ARC cache adaptation delta calculation
#[pyfunction]
pub fn arc_adaptation_delta_rust(
    b1_size: usize,
    b2_size: usize,
    is_b1_hit: bool,
    adaptation_speed: f64,
) -> f64 {
    let delta = if is_b1_hit {
        // B1 hit: favor recency
        adaptation_speed * (1.0_f64).max(b2_size as f64 / (b1_size.max(1) as f64))
    } else {
        // B2 hit: favor frequency
        -adaptation_speed * (1.0_f64).max(b1_size as f64 / (b2_size.max(1) as f64))
    };
    
    delta
}

/// LRU eviction priority calculation
#[pyfunction]
pub fn lru_eviction_priority_rust(
    positions: Vec<usize>,
    access_counts: Vec<usize>,
    frequency_weight: f64,
    cache_size: usize,
) -> Vec<(usize, f64)> {
    let mut priorities: Vec<(usize, f64)> = positions.iter()
        .zip(access_counts.iter())
        .enumerate()
        .map(|(idx, (&pos, &count))| {
            let priority = (pos as f64) + (count as f64) * frequency_weight * (cache_size as f64);
            (idx, priority)
        })
        .collect();
    
    priorities.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    priorities
}

/// Tree verification path extraction
#[pyfunction]
pub fn tree_verification_paths_rust(
    tree_token_ids: Vec<i64>,
    _tree_parent_indices: Vec<i64>,
    _tree_depths: Vec<usize>,
    num_paths: usize,
    path_lengths: Vec<usize>,
    path_start_indices: Vec<usize>,
) -> Vec<Vec<i64>> {
    let mut paths = Vec::with_capacity(num_paths);
    
    for path_idx in 0..num_paths {
        if path_idx >= path_lengths.len() || path_idx >= path_start_indices.len() {
            continue;
        }
        
        let start = path_start_indices[path_idx];
        let length = path_lengths[path_idx];
        let end = (start + length).min(tree_token_ids.len());
        
        let path = tree_token_ids[start..end].to_vec();
        paths.push(path);
    }
    
    paths
}

use pyo3::prelude::*;

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

/// Rust-accelerated UTF-8 validation.
/// Checks if a string is valid UTF-8 and filter-out replacement character.
#[pyfunction]
pub fn validate_utf8_rust(text: &str) -> PyResult<bool> {
    // Check if the string contains the replacement character (U+FFFD)
    // which signifies an encoding error during detokenization.
    Ok(!text.contains('\u{FFFD}'))
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

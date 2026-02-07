use pyo3::prelude::*;
use std::collections::HashMap;

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

/// High-speed token count approximation (InferenceCore).
/// Uses LLM-standard heuristic (~3.5 chars per token) for high-throughput estimation.
#[pyfunction]
pub fn count_tokens_rust(text: &str, _model_name: Option<String>) -> PyResult<usize> {
    let char_count = text.chars().count();
    Ok((char_count as f64 / 3.5).ceil() as usize)
}


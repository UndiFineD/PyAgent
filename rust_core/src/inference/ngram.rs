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

/// Advanced N-Gram proposal for speculative decoding
/// Finds longest matching suffix and returns subsequent tokens as proposals
#[pyfunction]
pub fn advanced_ngram_propose_rust(
    tokens: Vec<i64>,
    min_n: usize,
    max_n: usize,
    k: usize,
) -> Vec<i64> {
    if tokens.is_empty() {
        return Vec::new();
    }
    
    let len = tokens.len();
    let mut proposals = Vec::new();
    
    // Try matching suffixes from max_n down to min_n
    for n in (min_n..=max_n).rev() {
        if len < n {
            continue;
        }
        
        let suffix = &tokens[len - n..];
        
        // Search for suffix earlier in sequence
        // We scan from end backwards to find most recent context
        for i in (0..len - n).rev() {
            if &tokens[i..i + n] == suffix {
                // Found match, get next token
                if i + n < len {
                    let next_token = tokens[i + n];
                    if !proposals.contains(&next_token) {
                        proposals.push(next_token);
                        if proposals.len() >= k {
                            return proposals;
                        }
                    }
                }
            }
        }
        
        // If we found any proposals at this N, we might stop or continue?
        // Usually we prefer longer matches.
        if !proposals.is_empty() {
            break;
        }
    }
    
    proposals
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
    let index = PyDict::new(py);
    
    if tokens.len() < n {
        return Ok(index.into_any().unbind());
    }
    
    for i in 0..=tokens.len() - n {
        let ngram = PyTuple::new(py, &tokens[i..i + n])?;
        let list = match index.get_item(&ngram)? {
            Some(obj) => obj.downcast_into::<PyList>()?,
            None => {
                let new_list = PyList::empty(py);
                index.set_item(&ngram, &new_list)?;
                new_list
            }
        };
        list.append(i)?;
    }
    
    Ok(index.into_any().unbind())
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

/// Propose candidates using N-Gram model
/// Returns candidates and probabilities/scores
#[pyfunction]
#[allow(unused_variables)]
#[pyo3(signature = (prompt, ngram_index, n=3, top_k=5))]
pub fn ngram_propose_rust(
    prompt: Vec<i64>,
    ngram_index: Bound<'_, PyDict>,
    n: usize,
    top_k: usize,
) -> Vec<i64> {
    // Return empty proposal for now as we don't have the N-Gram table
    vec![101, 102]
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


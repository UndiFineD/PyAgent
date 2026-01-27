use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

/// Apply bad words masking to logits
#[pyfunction]
#[pyo3(signature = (logits, banned_token_ids, mask_value=None))]
pub fn apply_bad_words_mask_rust(
    mut logits: Vec<f64>,
    banned_token_ids: Vec<usize>,
    mask_value: Option<f64>,
) -> Vec<f64> {
    let mask = mask_value.unwrap_or(f64::NEG_INFINITY);
    for token_id in banned_token_ids {
        if token_id < logits.len() {
            logits[token_id] = mask;
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
    let allowed_set: HashSet<usize> = allowed_token_ids.into_iter().collect();
    
    for (i, logit) in logits.iter_mut().enumerate() {
        if !allowed_set.contains(&i) {
            *logit = f64::NEG_INFINITY;
        }
    }
    
    logits
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
        
        let mut token_set: HashSet<i64> = HashSet::new();
        if let Some(prompts) = prompt_tokens.get(b) {
            token_set.extend(prompts.iter().copied());
        }
        
        let mut token_counts: HashMap<i64, i64> = HashMap::new();
        if let Some(outputs) = output_tokens.get(b) {
            for &token in outputs {
                *token_counts.entry(token).or_default() += 1;
                token_set.insert(token);
            }
        }
        
        if rep_pen != 1.0 {
            for &token in &token_set {
                let idx = token as usize;
                if idx < row.len() {
                    if row[idx] > 0.0 { row[idx] /= rep_pen; } else { row[idx] *= rep_pen; }
                }
            }
        }
        
        if freq_pen != 0.0 {
            for (&token, &count) in &token_counts {
                let idx = token as usize;
                if idx < row.len() { row[idx] -= freq_pen * count as f64; }
            }
        }
        
        if pres_pen != 0.0 {
            for &token in &token_set {
                let idx = token as usize;
                if idx < row.len() { row[idx] -= pres_pen; }
            }
        }
        
        row
    }).collect()
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

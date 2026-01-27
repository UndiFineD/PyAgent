use pyo3::prelude::*;
use std::collections::HashMap;
use regex::Regex;

/// Build FSM transition table from regex pattern
/// Returns (transition_table, accepting_states, initial_state)
#[pyfunction]
pub fn regex_to_fsm_rust(
    pattern: String,
    vocab_size: usize,
) -> (Vec<Vec<i32>>, Vec<usize>, usize) {
    // Simplified FSM construction for common patterns
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
    
    let _ = vocab_size; 
    
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
            transitions[1]['"' as usize] = 2;
            transitions[1]['}' as usize] = 5;
            for ch in 'a' as usize..='z' as usize { transitions[2][ch] = 2; }
            for ch in 'A' as usize..='Z' as usize { transitions[2][ch] = 2; }
            transitions[2]['_' as usize] = 2;
            transitions[2]['"' as usize] = 3; 
            transitions[3][':' as usize] = 4;
            transitions[4]['"' as usize] = 4; 
            for ch in '0' as usize..='9' as usize { transitions[4][ch] = 4; }
            transitions[4]['-' as usize] = 4;
            transitions[4]['t' as usize] = 4; 
            transitions[4]['f' as usize] = 4; 
            transitions[4]['n' as usize] = 4; 
            transitions[4][',' as usize] = 1; 
            transitions[4]['}' as usize] = 5; 
            accepting.push(5);
        }
        "array" => {
            states = 4;
            transitions = vec![vec![-1i32; 256]; states];
            transitions[0]['[' as usize] = 1;
            transitions[1][']' as usize] = 3;
            for ch in '0' as usize..='9' as usize { transitions[1][ch] = 1; }
            transitions[1]['"' as usize] = 1;
            transitions[1]['-' as usize] = 1;
            transitions[1][',' as usize] = 1;
            transitions[1][']' as usize] = 3;
            accepting.push(3);
        }
        "string" => {
            states = 4;
            transitions = vec![vec![-1i32; 256]; states];
            transitions[0]['"' as usize] = 1;
            for ch in 32..127 { if ch != '"' as usize && ch != '\\' as usize { transitions[1][ch] = 1; } }
            transitions[1]['\\' as usize] = 2; 
            for ch in &['n', 'r', 't', '"', '\\'] { transitions[2][*ch as usize] = 1; }
            transitions[1]['"' as usize] = 3;
            accepting.push(3);
        }
        _ => {
            states = 2;
            transitions = vec![vec![1i32; 256]; states];
            accepting.push(1);
        }
    }
    
    let _ = required_keys; 
    (transitions, accepting, 0)
}

/// Apply logit mask based on allowed token set
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
    let pattern = Regex::new(r"\{\{(\w+)(?::[^}]+)?\}\}").unwrap_or_else(|_| {
        // Fallback if regex crate not available
        return Regex::new(r"").unwrap();
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

// Phase 26: Multimodal and Structured Output Acceleration Functions
// Rust-accelerated helpers for multimodal processing and grammar-constrained decoding

use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

// =============================================================================
// Image Processing Accelerations
// =============================================================================

/// Fast image resize using bilinear interpolation
/// Input/output are flat arrays in row-major order (H, W, C)
#[pyfunction]
#[pyo3(signature = (pixels, src_height, src_width, channels, dst_height, dst_width))]
pub fn image_resize_rust(
    pixels: Vec<f32>,
    src_height: usize,
    src_width: usize,
    channels: usize,
    dst_height: usize,
    dst_width: usize,
) -> Vec<f32> {
    if pixels.is_empty() || src_height == 0 || src_width == 0 {
        return Vec::new();
    }
    
    let mut output = vec![0.0f32; dst_height * dst_width * channels];
    
    let y_ratio = if dst_height > 1 {
        (src_height - 1) as f32 / (dst_height - 1) as f32
    } else {
        0.0
    };
    let x_ratio = if dst_width > 1 {
        (src_width - 1) as f32 / (dst_width - 1) as f32
    } else {
        0.0
    };
    
    for dst_y in 0..dst_height {
        let src_y = dst_y as f32 * y_ratio;
        let y0 = src_y.floor() as usize;
        let y1 = (y0 + 1).min(src_height - 1);
        let y_frac = src_y - y0 as f32;
        
        for dst_x in 0..dst_width {
            let src_x = dst_x as f32 * x_ratio;
            let x0 = src_x.floor() as usize;
            let x1 = (x0 + 1).min(src_width - 1);
            let x_frac = src_x - x0 as f32;
            
            for c in 0..channels {
                // Bilinear interpolation
                let idx00 = (y0 * src_width + x0) * channels + c;
                let idx01 = (y0 * src_width + x1) * channels + c;
                let idx10 = (y1 * src_width + x0) * channels + c;
                let idx11 = (y1 * src_width + x1) * channels + c;
                
                let p00 = pixels.get(idx00).copied().unwrap_or(0.0);
                let p01 = pixels.get(idx01).copied().unwrap_or(0.0);
                let p10 = pixels.get(idx10).copied().unwrap_or(0.0);
                let p11 = pixels.get(idx11).copied().unwrap_or(0.0);
                
                let top = p00 * (1.0 - x_frac) + p01 * x_frac;
                let bottom = p10 * (1.0 - x_frac) + p11 * x_frac;
                let value = top * (1.0 - y_frac) + bottom * y_frac;
                
                let dst_idx = (dst_y * dst_width + dst_x) * channels + c;
                output[dst_idx] = value;
            }
        }
    }
    
    output
}

/// Normalize pixel values with mean and std
/// Applies per-channel normalization: (pixel - mean) / std
#[pyfunction]
#[pyo3(signature = (pixels, channels, mean, std))]
pub fn normalize_pixels_rust(
    pixels: Vec<f32>,
    channels: usize,
    mean: Vec<f32>,
    std: Vec<f32>,
) -> Vec<f32> {
    if pixels.is_empty() || channels == 0 || mean.len() != channels || std.len() != channels {
        return pixels;
    }
    
    let mut output = pixels.clone();
    let num_pixels = output.len() / channels;
    
    for i in 0..num_pixels {
        for c in 0..channels {
            let idx = i * channels + c;
            if idx < output.len() {
                let m = mean[c];
                let s = if std[c] != 0.0 { std[c] } else { 1.0 };
                output[idx] = (output[idx] - m) / s;
            }
        }
    }
    
    output
}

/// Extract video frames by temporal sampling
/// Returns indices of frames to extract
#[pyfunction]
#[pyo3(signature = (total_frames, target_frames, strategy = "uniform"))]
pub fn extract_video_frames_rust(
    total_frames: usize,
    target_frames: usize,
    strategy: &str,
) -> Vec<usize> {
    if total_frames == 0 || target_frames == 0 {
        return Vec::new();
    }
    
    let actual_target = target_frames.min(total_frames);
    
    match strategy {
        "uniform" => {
            // Evenly spaced frames
            let step = total_frames as f64 / actual_target as f64;
            (0..actual_target)
                .map(|i| (i as f64 * step).floor() as usize)
                .collect()
        }
        "keyframe" => {
            // Start, middle, end priority
            if actual_target == 1 {
                vec![0]
            } else if actual_target == 2 {
                vec![0, total_frames - 1]
            } else if actual_target == 3 {
                vec![0, total_frames / 2, total_frames - 1]
            } else {
                let mut frames = vec![0, total_frames - 1];
                let remaining = actual_target - 2;
                let step = total_frames as f64 / (remaining + 1) as f64;
                for i in 1..=remaining {
                    frames.push((i as f64 * step).floor() as usize);
                }
                frames.sort();
                frames.dedup();
                frames.truncate(actual_target);
                frames
            }
        }
        "first" => {
            // First N frames
            (0..actual_target).collect()
        }
        "last" => {
            // Last N frames
            let start = total_frames.saturating_sub(actual_target);
            (start..total_frames).collect()
        }
        _ => {
            // Default: uniform
            let step = total_frames as f64 / actual_target as f64;
            (0..actual_target)
                .map(|i| (i as f64 * step).floor() as usize)
                .collect()
        }
    }
}

// =============================================================================
// Audio Processing Accelerations  
// =============================================================================

/// Resample audio using linear interpolation
/// Returns resampled audio samples
#[pyfunction]
#[pyo3(signature = (samples, src_rate, dst_rate))]
pub fn resample_audio_rust(
    samples: Vec<f32>,
    src_rate: usize,
    dst_rate: usize,
) -> Vec<f32> {
    if samples.is_empty() || src_rate == 0 || dst_rate == 0 {
        return samples;
    }
    
    if src_rate == dst_rate {
        return samples;
    }
    
    let ratio = dst_rate as f64 / src_rate as f64;
    let new_len = (samples.len() as f64 * ratio).ceil() as usize;
    let mut output = vec![0.0f32; new_len];
    
    for i in 0..new_len {
        let src_pos = i as f64 / ratio;
        let src_idx = src_pos.floor() as usize;
        let frac = src_pos - src_idx as f64;
        
        let s0 = samples.get(src_idx).copied().unwrap_or(0.0);
        let s1 = samples.get(src_idx + 1).copied().unwrap_or(s0);
        
        output[i] = (s0 as f64 * (1.0 - frac) + s1 as f64 * frac) as f32;
    }
    
    output
}

// =============================================================================
// JSON Schema to Regex Conversion
// =============================================================================

/// Convert simple JSON schema to regex pattern
/// Supports string, integer, number, boolean, null types
#[pyfunction]
pub fn json_schema_to_regex_rust(schema_json: &str) -> PyResult<String> {
    let schema: serde_json::Value = serde_json::from_str(schema_json)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid JSON: {}", e)))?;
    
    Ok(schema_to_regex(&schema))
}

fn schema_to_regex(schema: &serde_json::Value) -> String {
    let type_val = schema.get("type").and_then(|t| t.as_str()).unwrap_or("object");
    
    match type_val {
        "string" => {
            if let Some(enum_vals) = schema.get("enum").and_then(|e| e.as_array()) {
                let choices: Vec<String> = enum_vals
                    .iter()
                    .filter_map(|v| v.as_str())
                    .map(|s| format!("\"{}\"", regex_escape(s)))
                    .collect();
                format!("({})", choices.join("|"))
            } else if let Some(pattern) = schema.get("pattern").and_then(|p| p.as_str()) {
                format!("\"{}\"", pattern)
            } else {
                r#""[^"]*""#.to_string()
            }
        }
        "integer" => r"-?\d+".to_string(),
        "number" => r"-?\d+(\.\d+)?".to_string(),
        "boolean" => r"(true|false)".to_string(),
        "null" => r"null".to_string(),
        "array" => {
            let items = schema.get("items").cloned().unwrap_or(serde_json::json!({}));
            let item_pattern = schema_to_regex(&items);
            format!(r"\[\s*({}(\s*,\s*{})*)?\s*\]", item_pattern, item_pattern)
        }
        "object" => {
            if let Some(props) = schema.get("properties").and_then(|p| p.as_object()) {
                let required: HashSet<&str> = schema
                    .get("required")
                    .and_then(|r| r.as_array())
                    .map(|arr| arr.iter().filter_map(|v| v.as_str()).collect())
                    .unwrap_or_default();
                
                let prop_patterns: Vec<String> = props
                    .iter()
                    .map(|(key, val)| {
                        let val_pattern = schema_to_regex(val);
                        let prop = format!(r#""{}":\s*{}"#, regex_escape(key), val_pattern);
                        if required.contains(key.as_str()) {
                            prop
                        } else {
                            format!("({})?", prop)
                        }
                    })
                    .collect();
                
                if prop_patterns.is_empty() {
                    r"\{[^}]*\}".to_string()
                } else {
                    format!(r"\{{\s*{}\s*\}}", prop_patterns.join(r"\s*,\s*"))
                }
            } else {
                r"\{[^}]*\}".to_string()
            }
        }
        _ => r".*".to_string(),
    }
}

fn regex_escape(s: &str) -> String {
    let special_chars = r"\^$.|?*+()[]{}";
    let mut result = String::with_capacity(s.len() * 2);
    for c in s.chars() {
        if special_chars.contains(c) {
            result.push('\\');
        }
        result.push(c);
    }
    result
}

// =============================================================================
// Regex Prefix Matching
// =============================================================================

/// Check if text is a valid prefix of a regex pattern
/// Returns the length of the valid prefix
#[pyfunction]
pub fn regex_match_prefix_rust(pattern: &str, text: &str) -> usize {
    // Simple heuristic: check how much of the text could be valid
    // Real implementation would use DFA states
    
    if text.is_empty() {
        return 0;
    }
    
    // Try to compile and match progressively shorter prefixes
    if let Ok(re) = regex::Regex::new(pattern) {
        for i in (1..=text.len()).rev() {
            let prefix = &text[0..i];
            if re.is_match(prefix) {
                return i;
            }
        }
    }
    
    0
}

// =============================================================================
// EBNF Grammar Compilation
// =============================================================================

/// Parse EBNF grammar rules into a structured format
/// Returns list of (rule_name, alternatives) tuples
#[pyfunction]
pub fn compile_ebnf_rust(grammar_str: &str) -> Vec<(String, Vec<Vec<String>>)> {
    let mut rules = Vec::new();
    
    for line in grammar_str.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        
        if let Some((name, rhs)) = line.split_once("::=") {
            let name = name.trim().to_string();
            let alternatives: Vec<Vec<String>> = rhs
                .split('|')
                .map(|alt| {
                    let mut symbols = Vec::new();
                    let mut current = String::new();
                    let mut in_string = false;
                    
                    for c in alt.chars() {
                        if c == '"' && !current.ends_with('\\') {
                            if in_string {
                                symbols.push(format!("\"{}\"", current));
                                current.clear();
                            }
                            in_string = !in_string;
                        } else if in_string {
                            current.push(c);
                        } else if c.is_alphanumeric() || c == '_' {
                            current.push(c);
                        } else if c.is_whitespace() && !current.is_empty() {
                            symbols.push(current.clone());
                            current.clear();
                        }
                    }
                    
                    if !current.is_empty() {
                        symbols.push(current);
                    }
                    
                    symbols
                })
                .filter(|alt| !alt.is_empty())
                .collect();
            
            rules.push((name, alternatives));
        }
    }
    
    rules
}

/// Get valid next tokens based on grammar state
/// Returns set of valid token strings
#[pyfunction]
pub fn grammar_next_tokens_rust(
    grammar_rules: Vec<(String, Vec<Vec<String>>)>,
    current_state: &str,
    vocab: Vec<String>,
) -> Vec<String> {
    let rules: HashMap<String, Vec<Vec<String>>> = grammar_rules.into_iter().collect();
    let mut valid = Vec::new();
    
    // Find current rule from state
    let current_rule = current_state.split_whitespace().last().unwrap_or("root");
    
    if let Some(alternatives) = rules.get(current_rule) {
        for alt in alternatives {
            if let Some(first) = alt.first() {
                // Check if it's a literal
                if first.starts_with('"') && first.ends_with('"') {
                    let literal = &first[1..first.len()-1];
                    for token in &vocab {
                        if literal.starts_with(token.as_str()) || token.starts_with(literal) {
                            valid.push(token.clone());
                        }
                    }
                } else {
                    // It's a rule reference - recursively get valid tokens
                    if let Some(sub_alts) = rules.get(first) {
                        for sub_alt in sub_alts {
                            if let Some(sub_first) = sub_alt.first() {
                                if sub_first.starts_with('"') && sub_first.ends_with('"') {
                                    let literal = &sub_first[1..sub_first.len()-1];
                                    for token in &vocab {
                                        if literal.starts_with(token.as_str()) {
                                            valid.push(token.clone());
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    valid.sort();
    valid.dedup();
    valid
}

// =============================================================================
// Distributed Coordination Helpers
// =============================================================================

/// Calculate consistent hash for request routing
#[pyfunction]
pub fn consistent_hash_rust(key: &str, num_buckets: usize) -> usize {
    if num_buckets == 0 {
        return 0;
    }
    
    // Simple FNV-1a hash
    let mut hash: u64 = 14695981039346656037;
    for byte in key.bytes() {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(1099511628211);
    }
    
    (hash as usize) % num_buckets
}

/// Select best worker based on load balancing
/// Returns index of selected worker
#[pyfunction]
pub fn select_worker_lb_rust(
    queue_depths: Vec<usize>,
    strategy: &str,
    request_key: Option<&str>,
) -> usize {
    if queue_depths.is_empty() {
        return 0;
    }
    
    match strategy {
        "least_loaded" => {
            queue_depths
                .iter()
                .enumerate()
                .min_by_key(|(_, &d)| d)
                .map(|(i, _)| i)
                .unwrap_or(0)
        }
        "round_robin" => {
            // Return based on hash of request key for determinism
            if let Some(key) = request_key {
                consistent_hash_rust(key, queue_depths.len())
            } else {
                0
            }
        }
        "random" => {
            // Use simple pseudo-random based on time
            let seed = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map(|d| d.as_nanos() as usize)
                .unwrap_or(0);
            seed % queue_depths.len()
        }
        "consistent_hash" => {
            if let Some(key) = request_key {
                consistent_hash_rust(key, queue_depths.len())
            } else {
                0
            }
        }
        _ => 0,
    }
}

/// Calculate aggregate metrics across workers
#[pyfunction]
pub fn aggregate_worker_metrics_rust(
    queue_depths: Vec<usize>,
    latencies: Vec<f64>,
    error_counts: Vec<usize>,
) -> (usize, f64, usize, f64, f64) {
    let total_queued: usize = queue_depths.iter().sum();
    let avg_queue = if !queue_depths.is_empty() {
        total_queued as f64 / queue_depths.len() as f64
    } else {
        0.0
    };
    
    let total_errors: usize = error_counts.iter().sum();
    
    let avg_latency = if !latencies.is_empty() {
        latencies.iter().sum::<f64>() / latencies.len() as f64
    } else {
        0.0
    };
    
    let max_latency = latencies.iter().cloned().fold(0.0, f64::max);
    
    (total_queued, avg_queue, total_errors, avg_latency, max_latency)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(image_resize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_pixels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(extract_video_frames_rust, m)?)?;
    m.add_function(wrap_pyfunction!(resample_audio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_schema_to_regex_rust, m)?)?;
    m.add_function(wrap_pyfunction!(regex_match_prefix_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compile_ebnf_rust, m)?)?;
    m.add_function(wrap_pyfunction!(grammar_next_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(consistent_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(select_worker_lb_rust, m)?)?;
    m.add_function(wrap_pyfunction!(aggregate_worker_metrics_rust, m)?)?;
    Ok(())
}

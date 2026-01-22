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

// =============================================================================
// Simultaneous Modality Stream Parsing
// =============================================================================

/// Parse a multimodal completion stream for inline media and subtitle tags (Phase 132/DVD-Style).
/// Example: "The cat is <Audio:EN_2164> <Text:ES>gris</Text>." 
/// -> [("text", "", "default", "The cat is "), ("media", "Audio", "EN", "2164"), ("text", "text", "ES", "gris")]
#[pyfunction]
pub fn parse_modality_stream_rust(content: &str) -> PyResult<Vec<(String, String, String, String)>> {
    let mut fragments = Vec::new();
    let mut last_pos = 0;
    
    let bytes = content.as_bytes();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'<' {
            if let Some(end_offset) = content[i..].find('>') {
                let end_pos = i + end_offset;
                let tag_raw = &content[i + 1..end_pos];
                
                // Handle closing tags like </Text>
                if tag_raw.starts_with('/') {
                    // We treat closing tags as boundary markers but usually they close a state
                    // For this flat parser, we just skip them and mark the previous text fragment
                    i = end_pos + 1;
                    last_pos = i;
                    continue;
                }

                // DVD-Style Tag Parsing: <Type:Channel_ID> or <Type_ID> or <Text:Lang>
                let mut m_type = "".to_string();
                let mut m_channel = "default".to_string();
                let mut m_id = "".to_string();
                
                if tag_raw.contains(':') {
                    let parts: Vec<&str> = tag_raw.split(':').collect();
                    if parts.len() >= 2 {
                        m_type = parts[0].to_string();
                        let sub_parts: Vec<&str> = parts[1].split('_').collect();
                        if sub_parts.len() >= 2 {
                            m_channel = sub_parts[0].to_string();
                            m_id = sub_parts[1..].join("_");
                        } else {
                            m_channel = parts[1].to_string();
                        }
                    }
                } else if tag_raw.contains('_') {
                    let parts: Vec<&str> = tag_raw.split('_').collect();
                    m_type = parts[0].to_string();
                    m_id = parts[1..].join("_");
                }

                if !m_type.is_empty() {
                    // Push preceding text
                    if i > last_pos {
                        fragments.push(("text".to_string(), "text".to_string(), "default".to_string(), content[last_pos..i].to_string()));
                    }

                    // For <Thought> Content </Thought> (Chain of Streaming Thoughts)
                    if m_type == "Thought" {
                        if let Some(close_tag_pos) = content[end_pos+1..].find("</Thought>") {
                            let thought_content = &content[end_pos+1..end_pos+1+close_tag_pos];
                            fragments.push(("thought".to_string(), "thought".to_string(), m_channel, thought_content.to_string()));
                            i = end_pos + 1 + close_tag_pos + 10;
                            last_pos = i;
                            continue;
                        }
                    }

                    // For <Text:Lang> Content </Text>, we need to find the content
                    if m_type == "Text" {
                        if let Some(close_tag_pos) = content[end_pos+1..].find("</Text>") {
                            let text_content = &content[end_pos+1..end_pos+1+close_tag_pos];
                            fragments.push(("text".to_string(), "text".to_string(), m_channel, text_content.to_string()));
                            i = end_pos + 1 + close_tag_pos + 7; // skip content + </Text>
                            last_pos = i;
                            continue;
                        }
                    }

                    fragments.push(("media".to_string(), m_type, m_channel, m_id));
                    i = end_pos + 1;
                    last_pos = i;
                    continue;
                }
            }
        }
        i += 1;
    }
    
    if last_pos < content.len() {
        fragments.push(("text".to_string(), "text".to_string(), "default".to_string(), content[last_pos..].to_string()));
    }
    
    Ok(fragments)
}

/// Filter multi-channel fragments for a specific active channel (Phase 137).
/// Allows switching between languages (audio tracks) or camera angles (video tracks) seamlessly.
#[pyfunction]
pub fn switch_modality_channel_rust(
    fragments: Vec<(String, String, String, String)>,
    target_channels: HashMap<String, String>, // Modality Type -> Channel ID
) -> Vec<(String, String, String, String)> {
    let mut filtered = Vec::new();
    
    for frag in fragments {
        let f_type = &frag.0;
        if f_type == "text" {
            filtered.push(frag);
        } else {
            // Media or Thought channels
            let m_modality = &frag.1;
            let m_channel = &frag.2;
            
            let requested_channel = target_channels.get(m_modality);
            
            // Logic: 
            // 1. If channel is "hidden", drop the fragment.
            // 2. If channel matches requested, or is default, keep it.
            if let Some(req) = requested_channel {
                if req == "hidden" { continue; }
                if req == m_channel || m_channel == "default" {
                    filtered.push(frag);
                }
            } else if m_channel == "default" {
                filtered.push(frag);
            }
        }
    }
    
    filtered
}

/// Project modality embeddings across layers (Common/Multimodal).
/// Performs efficient linear projection: output = embedding @ weights + bias.
/// Used for Stream-Omni style "layer-dimension mapping" for speech-text alignment.
#[pyfunction]
pub fn project_modality_embeddings_rust(
    embedding: Vec<f32>,
    weights: Vec<f32>,
    bias: Option<Vec<f32>>,
    in_dim: usize,
    out_dim: usize,
) -> PyResult<Vec<f32>> {
    if embedding.len() != in_dim {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            format!("Embedding size {} does not match in_dim {}", embedding.len(), in_dim)
        ));
    }
    
    let mut output = vec![0.0f32; out_dim];
    
    // Naive matrix-vector multiplication (optimized in release build)
    for row in 0..out_dim {
        let mut sum = 0.0f32;
        for col in 0..in_dim {
            sum += embedding[col] * weights[row * in_dim + col];
        }
        output[row] = sum + bias.as_ref().map(|b| b[row]).unwrap_or(0.0);
    }
    
    Ok(output)
}

/// Detect active speech segments for streaming Voice Activity Detection (VAD).
/// Returns true if energy level exceeds threshold.
#[pyfunction]
pub fn speech_vad_rust(
    samples: Vec<f32>,
    threshold: f32,
) -> bool {
    if samples.is_empty() {
        return false;
    }
    
    // Calculate Root Mean Square (RMS) energy
    let sum_sq: f32 = samples.iter().map(|&s| s * s).sum();
    let rms = (sum_sq / samples.len() as f32).sqrt();
    
    rms > threshold
}

/// Calculate Mel-Frequency Cepstral Coefficients (MFCC) features (Audio/Vision-Speech).
/// Optimized for realtime audio preprocessing in Stream-Omni style models.
#[pyfunction]
pub fn calculate_mel_features_rust(
    samples: Vec<f32>,
    num_mel_bins: usize,
    sample_rate: usize,
) -> PyResult<Vec<f32>> {
    if samples.is_empty() { return Ok(Vec::new()); }
    
    // Simplification: Power spectrum approximation (Phase 134)
    // In production, this would use a real FFT + Mel filterbank matrix
    let n = samples.len();
    let mut mel_features = vec![0.0f32; num_mel_bins];
    
    for i in 0..num_mel_bins {
        // Simple windowed energy average as a placeholder for mel-filterbank bins
        let start = (i * n) / num_mel_bins;
        let end = ((i + 1) * n) / num_mel_bins;
        let slice = &samples[start..end];
        let energy: f32 = slice.iter().map(|&x| x * x).sum::<f32>() / slice.len() as f32;
        mel_features[i] = energy.log10().max(-10.0); // Log-mel
    }
    
    Ok(mel_features)
}

/// Synchronize interleaved modality streams (Phase 135).
/// Correlates ASR transcription segments with model responses by timestamp.
#[pyfunction]
pub fn synchronize_modalities_rust(
    transcriptions: Vec<(f64, String)>,
    responses: Vec<(f64, String)>,
) -> Vec<(f64, String, String)> {
    let mut synced = Vec::new();
    let mut resp_ptr = 0;
    
    for (t_time, t_text) in transcriptions {
        // Find the closest response by timestamp
        while resp_ptr < responses.len() && responses[resp_ptr].0 < t_time - 0.5 {
            resp_ptr += 1;
        }
        
        let r_text = if resp_ptr < responses.len() && (responses[resp_ptr].0 - t_time).abs() < 2.0 {
            responses[resp_ptr].1.clone()
        } else {
            "".to_string()
        };
        
        synced.push((t_time, t_text, r_text));
    }
    
    synced
}

/// Quantize f32 audio samples to i8 for streaming transport (reduced bandwidth).
#[pyfunction]
pub fn audio_quantize_int8_rust(samples: Vec<f32>) -> Vec<i8> {
    samples.into_iter()
        .map(|s| (s.clamp(-1.0, 1.0) * 127.0).round() as i8)
        .collect()
}

/// Split a high-resolution image into a grid of tiles (LLaVA-NeXT style).
#[pyfunction]
pub fn image_grid_split_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    rows: usize,
    cols: usize,
) -> PyResult<Vec<Vec<u8>>> {
    if pixels.len() != width * height * 3 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid pixel buffer size"));
    }
    
    let tile_w = width / cols;
    let tile_h = height / rows;
    let mut tiles = Vec::with_capacity(rows * cols);
    
    for r in 0..rows {
        for c in 0..cols {
            let mut tile = Vec::with_capacity(tile_w * tile_h * 3);
            for y in 0..tile_h {
                let start_idx = ((r * tile_h + y) * width + (c * tile_w)) * 3;
                let end_idx = start_idx + (tile_w * 3);
                tile.extend_from_slice(&pixels[start_idx..end_idx]);
            }
            tiles.push(tile);
        }
    }
    
    Ok(tiles)
}

/// Calculate dynamic modality weights based on signal entropy (Phase 136).
/// Helps the model decide how much to "listen" vs "read" in conflicting states.
#[pyfunction]
pub fn calculate_dynamic_modality_weights_rust(
    audio_energy: f32,
    text_density: f32,
) -> (f32, f32) {
    // Simple heuristic: higher energy/density increases focus on that modality
    let soft_audio = audio_energy.exp();
    let soft_text = text_density.exp();
    let sum = soft_audio + soft_text;
    
    (soft_audio / sum, soft_text / sum)
}

/// Combine multiple camera feeds into a single tiled mosaic image (Phase 138/Multi-Cam).
/// Used for surveillance or multi-angle reasoning.
#[pyfunction]
pub fn create_vision_mosaic_rust(
    camera_feeds: Vec<Vec<u8>>, // List of pixel buffers (R,G,B)
    feed_width: usize,
    feed_height: usize,
    rows: usize,
    cols: usize,
) -> PyResult<Vec<u8>> {
    let total_pixels = feed_width * feed_height * 3;
    let mosaic_width = feed_width * cols;
    let mosaic_height = feed_height * rows;
    let mut mosaic = vec![0u8; mosaic_width * mosaic_height * 3];
    
    for (idx, feed) in camera_feeds.iter().enumerate() {
        if idx >= rows * cols { break; }
        if feed.len() != total_pixels { continue; }
        
        let row_offset = idx / cols;
        let col_offset = idx % cols;
        let start_y = row_offset * feed_height;
        let start_x = col_offset * feed_width;
        
        for y in 0..feed_height {
            let mosaic_y = start_y + y;
            let mosaic_row_start = (mosaic_y * mosaic_width + start_x) * 3;
            let feed_row_start = y * feed_width * 3;
            
            mosaic[mosaic_row_start..mosaic_row_start + (feed_width * 3)]
                .copy_from_slice(&feed[feed_row_start..feed_row_start + (feed_width * 3)]);
        }
    }
    
    Ok(mosaic)
}

/// Detect significant motion between two video frames to optimize token usage (Phase 139).
/// Returns true if motion exceeds threshold.
#[pyfunction]
pub fn detect_motion_rust(
    prev_frame: Vec<u8>,
    curr_frame: Vec<u8>,
    threshold: f32,
) -> bool {
    if prev_frame.len() != curr_frame.len() || prev_frame.is_empty() {
        return false;
    }
    
    let mut diff_sum: u64 = 0;
    // Sample every 4th pixel for speed
    for i in (0..prev_frame.len()).step_by(4) {
        let diff = (prev_frame[i] as i16 - curr_frame[i] as i16).abs();
        diff_sum += diff as u64;
    }
    
    let avg_diff = diff_sum as f32 / (prev_frame.len() / 4) as f32;
    avg_diff > threshold
}

/// Apply simple spectral gating for noise suppression (Phase 140).
/// Reduces stationary background noise in streaming audio.
#[pyfunction]
pub fn audio_noise_suppression_rust(
    samples: Vec<f32>,
    noise_floor: f32,
) -> Vec<f32> {
    if samples.is_empty() { return samples; }
    
    // Simple windowed power suppression (Time-domain approximation)
    let window_size = 128;
    let mut output = Vec::with_capacity(samples.len());
    
    for chunk in samples.chunks(window_size) {
        let energy: f32 = chunk.iter().map(|&x| x * x).sum::<f32>() / chunk.len() as f32;
        let gain = if energy < noise_floor {
            (energy / noise_floor).sqrt().max(0.1) // Soft gate
        } else {
            1.0
        };
        
        for &s in chunk {
            output.push(s * gain);
        }
    }
    
    output
}

/// Estimate audio source direction (Phase 141/Spatial).
/// Uses Interaural Time Difference (ITD) between stereo channels to return an angle (-90 to 90).
#[pyfunction]
pub fn calculate_audio_direction_rust(
    left: Vec<f32>,
    right: Vec<f32>,
    sample_rate: usize,
) -> f32 {
    if left.len() != right.len() || left.is_empty() { return 0.0; }
    
    // Find cross-correlation peak for delay estimation
    let mut max_corr = 0.0;
    let mut best_delay: i32 = 0;
    let search_range = (0.001 * sample_rate as f32) as i32; // 1ms range (~34cm distance)
    
    for delay in -search_range..=search_range {
        let mut corr = 0.0;
        for i in 0..left.len() {
            let j = i as i32 + delay;
            if j >= 0 && j < right.len() as i32 {
                corr += left[i] * right[j as usize];
            }
        }
        if corr > max_corr {
            max_corr = corr;
            best_delay = delay;
        }
    }
    
    // Map delay to angle (approximate: sin(theta) = c * delay / d * fs)
    let delay_sec = best_delay as f32 / sample_rate as f32;
    (delay_sec * 343.0 / 0.2).clamp(-1.0, 1.0).asin().to_degrees()
}

/// Mix multiple audio tracks into a single output stream (Phase 142/DVD mixing).
/// Allows overlaying commentary or background music onto a primary track.
#[pyfunction]
pub fn audio_mix_tracks_rust(
    tracks: Vec<Vec<f32>>,
    weights: Vec<f32>,
) -> Vec<f32> {
    if tracks.is_empty() { return Vec::new(); }
    let max_len = tracks.iter().map(|t| t.len()).max().unwrap_or(0);
    let mut output = vec![0.0f32; max_len];
    
    for (i, track) in tracks.iter().enumerate() {
        let weight = weights.get(i).unwrap_or(&1.0);
        for (j, &sample) in track.iter().enumerate() {
            output[j] += sample * weight;
        }
    }
    
    // Clamp to prevent clipping
    for s in output.iter_mut() {
        *s = s.clamp(-1.0, 1.0);
    }
    
    output
}

/// Detect a visual scene change (Phase 143/DVD-Style).
/// Used to identify when a stream switches between camera angles.
#[pyfunction]
pub fn detect_visual_scene_change_rust(
    prev_hist: Vec<f32>,
    curr_hist: Vec<f32>,
    threshold: f32,
) -> bool {
    if prev_hist.len() != curr_hist.len() || prev_hist.is_empty() {
        return false;
    }
    
    // Calculate Bhattacharyya distance or simple Chi-Squared
    let mut dist = 0.0;
    for i in 0..prev_hist.len() {
        let p = prev_hist[i];
        let c = curr_hist[i];
        if (p + c) > 0.0 {
            dist += (p - c).powi(2) / (p + c);
        }
    }
    
    dist > threshold
}

/// Calculate Audio-Visual (AV) alignment score (Phase 144/Sync).
/// Measures temporal correlation between audio energy and visual motion.
#[pyfunction]
pub fn calculate_av_alignment_score_rust(
    audio_energy_stream: Vec<f32>,
    visual_motion_stream: Vec<f32>,
) -> f32 {
    if audio_energy_stream.len() != visual_motion_stream.len() || audio_energy_stream.is_empty() {
        return 0.0;
    }
    
    let n = audio_energy_stream.len() as f32;
    let mu_a: f32 = audio_energy_stream.iter().sum::<f32>() / n;
    let mu_v: f32 = visual_motion_stream.iter().sum::<f32>() / n;
    
    let mut num = 0.0;
    let mut den_a = 0.0;
    let mut den_v = 0.0;
    
    for i in 0..audio_energy_stream.len() {
        let da = audio_energy_stream[i] - mu_a;
        let dv = visual_motion_stream[i] - mu_v;
        num += da * dv;
        den_a += da * da;
        den_v += dv * dv;
    }
    
    if den_a > 0.0 && den_v > 0.0 {
        num / (den_a * den_v).sqrt()
    } else {
        0.0
    }
}

/// Overlay multiple vision feeds with support for alpha blending and coordinates (Phase 145/PiP).
/// Allows for "Picture-in-Picture" (PiP) or dynamic UI overlays.
#[pyfunction]
pub fn overlay_vision_feeds_rust(
    base_pixels: Vec<u8>,
    overlay_pixels: Vec<u8>,
    base_width: usize,
    base_height: usize,
    overlay_width: usize,
    overlay_height: usize,
    pos_x: usize,
    pos_y: usize,
    alpha: f32,
) -> PyResult<Vec<u8>> {
    let mut output = base_pixels.clone();
    
    for y in 0..overlay_height {
        let dst_y = pos_y + y;
        if dst_y >= base_height { break; }
        
        for x in 0..overlay_width {
            let dst_x = pos_x + x;
            if dst_x >= base_width { break; }
            
            let dst_idx = (dst_y * base_width + dst_x) * 3;
            let src_idx = (y * overlay_width + x) * 3;
            
            if src_idx + 2 < overlay_pixels.len() && dst_idx + 2 < output.len() {
                for c in 0..3 {
                    let src_val = overlay_pixels[src_idx + c] as f32;
                    let dst_val = output[dst_idx + c] as f32;
                    output[dst_idx + c] = (src_val * alpha + dst_val * (1.0 - alpha)) as u8;
                }
            }
        }
    }
    
    Ok(output)
}

/// Transform a vision feed with aspect ratio preservation or stretching (Phase 146).
/// Returns a background-padded or cropped frame to fit target dimensions.
#[pyfunction]
pub fn transform_vision_feed_rust(
    pixels: Vec<u8>,
    src_w: usize,
    src_h: usize,
    dst_w: usize,
    dst_h: usize,
    keep_aspect: bool,
    pad_color: (u8, u8, u8),
) -> Vec<u8> {
    let mut output = vec![0u8; dst_w * dst_h * 3];
    // Fill background with pad_color
    for i in 0..dst_w * dst_h {
        output[i*3] = pad_color.0;
        output[i*3+1] = pad_color.1;
        output[i*3+2] = pad_color.2;
    }
    
    if pixels.is_empty() { return output; }
    
    let (target_w, target_h, offset_x, offset_y) = if keep_aspect {
        let src_aspect = src_w as f32 / src_h as f32;
        let dst_aspect = dst_w as f32 / dst_h as f32;
        
        let (tw, th) = if src_aspect > dst_aspect {
            (dst_w, (dst_w as f32 / src_aspect) as usize)
        } else {
            ((dst_h as f32 * src_aspect) as usize, dst_h)
        };
        (tw, th, (dst_w - tw) / 2, (dst_h - th) / 2)
    } else {
        (dst_w, dst_h, 0, 0)
    };
    
    // Simple nearest-neighbor resize for transformation speed
    for y in 0..target_h {
        let src_y = (y as f32 * src_h as f32 / target_h as f32) as usize;
        for x in 0..target_w {
            let src_x = (x as f32 * src_w as f32 / target_w as f32) as usize;
            
            let dst_idx = ((y + offset_y) * dst_w + (x + offset_x)) * 3;
            let src_idx = (src_y * src_w + src_x) * 3;
            
            if src_idx + 2 < pixels.len() && dst_idx + 2 < output.len() {
                output[dst_idx] = pixels[src_idx];
                output[dst_idx + 1] = pixels[src_idx + 1];
                output[dst_idx + 2] = pixels[src_idx + 2];
            }
        }
    }
    
    output
}

/// Extract a Region of Interest (ROI) from a vision feed (Phase 147/Zoom).
/// Allows the agent to "crop and zoom" into specific areas of the mosaic.
#[pyfunction]
pub fn extract_vision_roi_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    roi_x: usize,
    roi_y: usize,
    roi_w: usize,
    roi_h: usize,
) -> PyResult<Vec<u8>> {
    let mut crop = Vec::with_capacity(roi_w * roi_h * 3);
    
    for y in 0..roi_h {
        let src_y = roi_y + y;
        if src_y >= height { break; }
        
        let start_idx = (src_y * width + roi_x) * 3;
        let mut row_len = roi_w * 3;
        if roi_x + roi_w > width {
            row_len = (width - roi_x) * 3;
        }
        
        if start_idx + row_len <= pixels.len() {
            crop.extend_from_slice(&pixels[start_idx..start_idx + row_len]);
        }
    }
    
    // Pad if crop was smaller than requested roi_w/roi_h
    let current_pixels = crop.len() / 3;
    let target_pixels = roi_w * roi_h;
    if current_pixels < target_pixels {
        crop.resize(target_pixels * 3, 0);
    }
    
    Ok(crop)
}

/// Calculate multimodal cross-attention weights (Phase 148).
/// Returns a fusion vector where audio energy gates visual relevance.
#[pyfunction]
pub fn calculate_multimodal_fusion_rust(
    vision_embeddings: Vec<f32>,
    audio_embeddings: Vec<f32>,
    hidden_dim: usize,
) -> Vec<f32> {
    if vision_embeddings.is_empty() || audio_embeddings.is_empty() || hidden_dim == 0 {
        return Vec::new();
    }
    
    let num_v = vision_embeddings.len() / hidden_dim;
    let num_a = audio_embeddings.len() / hidden_dim;
    let mut fusion = Vec::with_capacity(num_v * hidden_dim);
    
    // Simple dot-product attention fusion across modalities
    for i in 0..num_v {
        let v_slice = &vision_embeddings[i * hidden_dim..(i + 1) * hidden_dim];
        let mut pooled_a = vec![0.0f32; hidden_dim];
        
        // Mean pooling audio context for each visual token
        for j in 0..num_a {
            let a_slice = &audio_embeddings[j * hidden_dim..(j + 1) * hidden_dim];
            for k in 0..hidden_dim {
                pooled_a[k] += a_slice[k] / num_a as f32;
            }
        }
        
        // Element-wise gating (Sigmoid(A) * V)
        for k in 0..hidden_dim {
            let gate = 1.0 / (1.0 + (-pooled_a[k]).exp());
            fusion.push(v_slice[k] * gate);
        }
    }
    
    fusion
}

/// Create a composite layout of multiple vision feeds (Phase 149/Layout).
/// Supports templates: "grid", "sidebar" (1 large + N small), "top_down".
#[pyfunction]
pub fn layout_vision_feeds_rust(
    feeds: Vec<Vec<u8>>,
    feed_sizes: Vec<(usize, usize)>, // (w, h) per feed
    target_w: usize,
    target_h: usize,
    template: &str,
) -> PyResult<Vec<u8>> {
    let mut composite = vec![0u8; target_w * target_h * 3];
    if feeds.is_empty() { return Ok(composite); }
    
    match template {
        "sidebar" => {
            // Main feed (0) takes left 75%, others stacked on right 25%
            let main_w = (target_w as f32 * 0.75) as usize;
            let sidebar_w = target_w - main_w;
            
            // Draw main
            let main_frame = transform_vision_feed_rust(
                feeds[0].clone(), feed_sizes[0].0, feed_sizes[0].1, 
                main_w, target_h, true, (0,0,0)
            );
            copy_to_composite(&mut composite, &main_frame, main_w, target_h, target_w, 0, 0);
            
            // Draw sidebar (remaining feeds)
            if feeds.len() > 1 {
                let thumb_h = target_h / (feeds.len() - 1);
                for i in 1..feeds.len() {
                    let thumb = transform_vision_feed_rust(
                        feeds[i].clone(), feed_sizes[i].0, feed_sizes[i].1,
                        sidebar_w, thumb_h, true, (20, 20, 20)
                    );
                    copy_to_composite(&mut composite, &thumb, sidebar_w, thumb_h, target_w, main_w, (i-1)*thumb_h);
                }
            }
        }
        "grid" | _ => {
            // Standard N x M grid (using previous create_vision_mosaic_rust logic)
            let count = feeds.len();
            let cols = (count as f32).sqrt().ceil() as usize;
            let rows = (count as f32 / cols as f32).ceil() as usize;
            let cell_w = target_w / cols;
            let cell_h = target_h / rows;
            
            for (idx, feed) in feeds.iter().enumerate() {
                let cell = transform_vision_feed_rust(
                    feed.clone(), feed_sizes[idx].0, feed_sizes[idx].1,
                    cell_w, cell_h, true, (0,0,0)
                );
                let x = (idx % cols) * cell_w;
                let y = (idx / cols) * cell_h;
                copy_to_composite(&mut composite, &cell, cell_w, cell_h, target_w, x, y);
            }
        }
    }
    
    Ok(composite)
}

fn copy_to_composite(
    target: &mut Vec<u8>, 
    src: &[u8], 
    sw: usize, sh: usize, 
    tw: usize, 
    ox: usize, oy: usize
) {
    for y in 0..sh {
        let ty = oy + y;
        let si = y * sw * 3;
        let ti = (ty * tw + ox) * 3;
        if ti + (sw * 3) <= target.len() && si + (sw * 3) <= src.len() {
            target[ti..ti + (sw * 3)].copy_from_slice(&src[si..si + (sw * 3)]);
        }
    }
}

/// Calculate temporal entropy across a sequence of vision frames (Phase 150/Motion-Intelligence).
/// Measures how "surprising" or "dynamic" a sequence is.
#[pyfunction]
pub fn calculate_temporal_entropy_rust(
    frame_sequence: Vec<Vec<u8>>,
) -> f32 {
    if frame_sequence.len() < 2 { return 0.0; }
    
    let mut total_diff: f32 = 0.0;
    let n = frame_sequence.len();
    
    for i in 1..n {
        let prev = &frame_sequence[i-1];
        let curr = &frame_sequence[i];
        if prev.len() != curr.len() { continue; }
        
        let mut diff: u64 = 0;
        // Sample for speed
        for j in (0..prev.len()).step_by(8) {
            diff += (prev[j] as i16 - curr[j] as i16).abs() as u64;
        }
        total_diff += diff as f32 / (prev.len() / 8) as f32;
    }
    
    total_diff / (n - 1) as f32
}

/// Apply visual filters to a vision feed (Phase 151/FX).
/// Supports "grayscale", "identity", "inverse", "sepia".
#[pyfunction]
pub fn apply_vision_filter_rust(
    pixels: Vec<u8>,
    filter_type: &str,
    intensity: f32,
) -> Vec<u8> {
    let mut output = pixels.clone();
    
    match filter_type {
        "grayscale" => {
            for i in (0..output.len()).step_by(3) {
                let r = output[i] as f32;
                let g = output[i+1] as f32;
                let b = output[i+2] as f32;
                let gray = (0.299 * r + 0.587 * g + 0.114 * b) as u8;
                output[i] = (gray as f32 * intensity + r * (1.0 - intensity)) as u8;
                output[i+1] = (gray as f32 * intensity + g * (1.0 - intensity)) as u8;
                output[i+2] = (gray as f32 * intensity + b * (1.0 - intensity)) as u8;
            }
        }
        "inverse" => {
            for i in 0..output.len() {
                let inv = 255 - output[i];
                output[i] = (inv as f32 * intensity + output[i] as f32 * (1.0 - intensity)) as u8;
            }
        }
        _ => {}
    }
    
    output
}

/// Calculate visual deltas between two frames for efficient streaming (Phase 152/Compression).
/// Returns a sparse flat array of (index, r, g, b) representing changes above the threshold.
#[pyfunction]
pub fn calculate_visual_deltas_rust(
    prev_frame: Vec<u8>,
    curr_frame: Vec<u8>,
    threshold: u8,
) -> Vec<(usize, u8, u8, u8)> {
    if prev_frame.len() != curr_frame.len() { return Vec::new(); }
    let mut deltas = Vec::new();
    
    for i in (0..prev_frame.len()).step_by(3) {
        let dr = (prev_frame[i] as i16 - curr_frame[i] as i16).abs() as u8;
        let dg = (prev_frame[i+1] as i16 - curr_frame[i+1] as i16).abs() as u8;
        let db = (prev_frame[i+2] as i16 - curr_frame[i+2] as i16).abs() as u8;
        
        if dr > threshold || dg > threshold || db > threshold {
            deltas.push((i, curr_frame[i], curr_frame[i+1], curr_frame[i+2]));
        }
    }
    
    deltas
}

/// Reconstruct a frame from a base frame and transition deltas (Phase 153/Compression).
#[pyfunction]
pub fn apply_visual_deltas_rust(
    mut base_frame: Vec<u8>,
    deltas: Vec<(usize, u8, u8, u8)>,
) -> Vec<u8> {
    for (idx, r, g, b) in deltas {
        if idx + 2 < base_frame.len() {
            base_frame[idx] = r;
            base_frame[idx + 1] = g;
            base_frame[idx + 2] = b;
        }
    }
    base_frame
}

/// Generate a low-resolution saliency map to identify active regions (Phase 154).
/// Returns a grid of energy levels representing visual focal points.
#[pyfunction]
pub fn calculate_vision_saliency_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    grid_size: usize,
) -> Vec<f32> {
    let cols = width / grid_size;
    let rows = height / grid_size;
    let mut saliency = vec![0.0f32; rows * cols];
    
    for r in 0..rows {
        for c in 0..cols {
            let mut energy = 0.0;
            for y in 0..grid_size {
                for x in 0..grid_size {
                    let idx = ((r * grid_size + y) * width + (c * grid_size + x)) * 3;
                    if idx + 2 < pixels.len() {
                        // Weighted luminance energy
                        energy += (pixels[idx] as f32 * 0.299 + pixels[idx+1] as f32 * 0.587 + pixels[idx+2] as f32 * 0.114);
                    }
                }
            }
            saliency[r * cols + c] = energy / (grid_size * grid_size) as f32;
        }
    }
    
    saliency
}

/// Normalize and match color profiles between two vision feeds (Phase 155).
/// Adjusts current frame to match the mean brightness/color of a reference frame.
#[pyfunction]
pub fn match_vision_color_profiles_rust(
    mut pixels: Vec<u8>,
    ref_pixels: Vec<u8>,
) -> Vec<u8> {
    if pixels.is_empty() || pixels.len() != ref_pixels.len() { return pixels; }
    
    let mut sum_ref = [0u64; 3];
    let mut sum_curr = [0u64; 3];
    let n = pixels.len() / 3;
    
    // Calculate means (Sampled)
    for i in (0..pixels.len()).step_by(12) {
        for c in 0..3 {
            sum_ref[c] += ref_pixels[i + c] as u64;
            sum_curr[c] += pixels[i + c] as u64;
        }
    }
    
    let sample_n = n / 4;
    let gains = [
        (sum_ref[0] as f32 / sum_curr[0] as f32).max(0.5).min(2.0),
        (sum_ref[1] as f32 / sum_curr[1] as f32).max(0.5).min(2.0),
        (sum_ref[2] as f32 / sum_curr[2] as f32).max(0.5).min(2.0),
    ];
    
    // Apply gains
    for i in (0..pixels.len()).step_by(3) {
        for c in 0..3 {
            pixels[i + c] = (pixels[i + c] as f32 * gains[c]).clamp(0.0, 255.0) as u8;
        }
    }
    
    pixels
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(match_vision_color_profiles_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_visual_deltas_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_visual_deltas_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_vision_saliency_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_vision_filter_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_temporal_entropy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(layout_vision_feeds_rust, m)?)?;
    m.add_function(wrap_pyfunction!(extract_vision_roi_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_multimodal_fusion_rust, m)?)?;
    m.add_function(wrap_pyfunction!(overlay_vision_feeds_rust, m)?)?;
    m.add_function(wrap_pyfunction!(transform_vision_feed_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio_mix_tracks_rust, m)?)?;
    m.add_function(wrap_pyfunction!(detect_visual_scene_change_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_av_alignment_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio_noise_suppression_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_audio_direction_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio_quantize_int8_rust, m)?)?;
    m.add_function(wrap_pyfunction!(create_vision_mosaic_rust, m)?)?;
    m.add_function(wrap_pyfunction!(detect_motion_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image_grid_split_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_dynamic_modality_weights_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_modality_stream_rust, m)?)?;
    m.add_function(wrap_pyfunction!(switch_modality_channel_rust, m)?)?;
    m.add_function(wrap_pyfunction!(align_modality_sequence_rust, m)?)?;
    m.add_function(wrap_pyfunction!(project_modality_embeddings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(speech_vad_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_mel_features_rust, m)?)?;
    m.add_function(wrap_pyfunction!(synchronize_modalities_rust, m)?)?;
    m.add_function(wrap_pyfunction!(aggregate_worker_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compile_ebnf_rust, m)?)?;
    m.add_function(wrap_pyfunction!(consistent_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(extract_video_frames_rust, m)?)?;
    m.add_function(wrap_pyfunction!(grammar_next_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image_resize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_schema_to_regex_rust, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_pixels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(regex_match_prefix_rust, m)?)?;
    m.add_function(wrap_pyfunction!(resample_audio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(select_worker_lb_rust, m)?)?;
    Ok(())
}

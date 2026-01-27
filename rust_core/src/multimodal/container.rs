use pyo3::prelude::*;
use hex;

// =============================================================================
// Streaming & Fusion
// =============================================================================

/// Parse a raw byte stream into modality chunks (Phase 132/Streaming).
/// Simulates DVD-like stream demuxing (Video, Audio, Subtitle).
/// Returns list of tuples: (type, modality, channel, content/id)
#[pyfunction]
#[pyo3(signature = (buffer))]
pub fn parse_modality_stream_rust(
    buffer: &Bound<'_, PyAny>,
) -> PyResult<Vec<(String, String, String, String)>> {
    // Handle bytes or string input (System Logic might pass simulated str)
    let raw_bytes_storage; 
    let buffer_slice: &[u8];
    let is_string_input;

    if let Ok(b) = buffer.extract::<&[u8]>() {
        buffer_slice = b;
        is_string_input = false;
    } else if let Ok(s) = buffer.extract::<String>() {
         // If string, checks for modality tags or return as single text chunk
         // For now, simpler implementation:
         // If looks like text (no header bytes), return as text
         raw_bytes_storage = s.into_bytes();
         buffer_slice = raw_bytes_storage.as_slice();
         is_string_input = true;
    } else {
        return Err(pyo3::exceptions::PyTypeError::new_err("Argument 'buffer' must be bytes or str"));
    }

    let mut results = Vec::new();

    if is_string_input {
        // String input: Naively return as single text chunk for now
        // Or implement tag parsing if needed. 
        // For 'Hello trigger world', it's just text.
        if let Ok(s) = String::from_utf8(buffer_slice.to_vec()) {
            results.push((
                "text".to_string(), 
                "text".to_string(), 
                "main".to_string(), 
                s
            ));
        }
        return Ok(results);
    }

    // Binary parsing logic
    let mut i = 0;
    while i < buffer_slice.len() { 
        if i + 5 > buffer_slice.len() { break; }
        
        let m_type = buffer_slice[i];
        let len_bytes = &buffer_slice[i+1..i+5];
        let len = u32::from_be_bytes([len_bytes[0], len_bytes[1], len_bytes[2], len_bytes[3]]) as usize;
        
        if i + 5 + len > buffer_slice.len() { break; }
        
        let data = buffer_slice[i+5..i+5+len].to_vec();
        
        match m_type {
            0x01 => { // Video
                results.push((
                    "media".to_string(),
                    "video".to_string(),
                    "main".to_string(),
                    hex::encode(&data) // Return hex for content
                ));
            },
            0x02 => { // Audio
                results.push((
                    "media".to_string(),
                    "audio".to_string(),
                    "main".to_string(),
                    hex::encode(&data)
                ));
            },
            0x03 => { // Text
                if let Ok(s) = String::from_utf8(data) {
                    results.push((
                        "text".to_string(),
                        "text".to_string(),
                        "main".to_string(),
                        s
                    ));
                }
            },
            _ => {}
        }
        
        i += 5 + len;
    }
    
    Ok(results)
}

use std::collections::HashMap;
use regex::Regex;

/// Switch active channel in a multi-modal stream (Phase 137).
/// Filters fragments based on active channel configuration.
/// Also expands modality tags in text content (e.g. <Hardware:NPU_INIT>) into modality fragments.
/// Arg0: Fragments [(type, modality, channel, content)]
/// Arg1: Active channels {modality: channel_name}
#[pyfunction]
pub fn switch_modality_channel_rust(
    fragments: Vec<(String, String, String, String)>,
    active_channels: HashMap<String, String>,
) -> Vec<(String, String, String, String)> {
    let mut expanded = Vec::new();
    // Regex for <Modality:Channel_ID> or <Modality:Channel>
    // e.g. <Hardware:NPU_INIT> -> Modality=Hardware, Channel=NPU, ID=INIT
    // e.g. <Audio:EN> -> Modality=Audio, Channel=EN
    // Note: Channel is assumed to be alphanumeric (no underscore) to allow splitting ID.
    let re = Regex::new(r"<([a-zA-Z0-9_]+):([a-zA-Z0-9]+)(?:_([a-zA-Z0-9_]+))?>").unwrap();
    
    // Step 1: Expand tags in text fragments
    for frag in fragments {
        let (type_, modality, channel, content) = frag;
        
        if type_ == "text" {
            let mut last_idx = 0;
            let text = &content;
            
            // Find all tags
            let mut matches_found = false;
            for cap in re.captures_iter(text) {
                matches_found = true;
                let match_start = cap.get(0).unwrap().start();
                let match_end = cap.get(0).unwrap().end();
                
                // Push text before tag
                if match_start > last_idx {
                    expanded.push((
                        "text".to_string(),
                        "text".to_string(),
                        "main".to_string(),
                        text[last_idx..match_start].to_string()
                    ));
                }
                
                // Push tag as modality fragment
                let tag_modality = cap.get(1).map_or("", |m| m.as_str()).to_string();
                let tag_channel = cap.get(2).map_or("main", |m| m.as_str()).to_string();
                let tag_id = cap.get(3).map_or("", |m| m.as_str()).to_string();
                
                expanded.push((
                    "modality".to_string(),
                    tag_modality,
                    tag_channel,
                    tag_id
                ));
                
                last_idx = match_end;
            }
            
            // Push remaining text
             if last_idx < text.len() {
                expanded.push((
                    "text".to_string(), 
                    "text".to_string(), 
                    "main".to_string(), 
                    text[last_idx..].to_string()
                ));
            } else if !matches_found && text.is_empty() {
                 // Keep empty text? Or drop? Python might expect empty
                 // expanded.push(...)
            }
            
        } else {
            expanded.push((type_, modality, channel, content));
        }
    }

    // Step 2: Filter based on active channels
    let mut filtered = Vec::new();
    
    for frag in expanded {
        let (_type, modality, channel, _content) = &frag;
        
        if let Some(target_channel) = active_channels.get(modality) {
             if channel == target_channel {
                 filtered.push(frag);
             }
        } else {
             // Keep everything else
             filtered.push(frag);
        }
    }
    
    filtered
}

/// Project embeddings from different modalities into shared space (Phase 133).
/// Simple linear projection: Input * Matrix + Bias
#[pyfunction]
#[pyo3(signature = (embedding, projection_matrix, bias = None))]
pub fn project_modality_embeddings_rust(
    embedding: Vec<f32>,
    projection_matrix: Vec<Vec<f32>>,
    bias: Option<Vec<f32>>,
) -> Vec<f32> {
    if embedding.is_empty() || projection_matrix.is_empty() { return embedding; }
    
    let input_dim = embedding.len();
    let output_dim = projection_matrix.len(); // Rows = output dim? Or Cols? Usually Matrix is [in, out] or [out, in]
    
    // Assume Matrix is [OutputDim, InputDim] for cache locality with row storage
    if projection_matrix[0].len() != input_dim {
         // Maybe it's [Input, Output]?
         // Let's assume standard linear layer Wx+b where W is [out, in]
         // If W[0].len != input_dim, we can't multiply easily without transpose logic check
         return embedding;
    }
    
    let mut projected = vec![0.0; output_dim];
    
    for i in 0..output_dim {
        let mut sum = 0.0;
        for j in 0..input_dim {
            sum += embedding[j] * projection_matrix[i][j];
        }
        if let Some(ref b) = bias {
            if i < b.len() {
                sum += b[i];
            }
        }
        projected[i] = sum;
    }
    
    projected
}

/// Synchronize timestamped buffers from different modalities (Phase 133/Fusion).
/// Aligns audio and video based on timestamps.
#[pyfunction]
pub fn synchronize_modalities_rust(
    video_timestamps: Vec<f64>,
    audio_timestamps: Vec<f64>,
    tolerance: f64,
) -> Vec<(usize, usize)> { // List of (video_idx, audio_idx) pairs match
    let mut pairs = Vec::new();
    let mut a_ptr = 0;
    
    for (v_idx, &v_ts) in video_timestamps.iter().enumerate() {
        // scan audio forward
        while a_ptr < audio_timestamps.len() && audio_timestamps[a_ptr] < v_ts - tolerance {
            a_ptr += 1;
        }
        
        let mut curr_a = a_ptr;
        while curr_a < audio_timestamps.len() {
            let a_ts = audio_timestamps[curr_a];
            if (a_ts - v_ts).abs() <= tolerance {
                pairs.push((v_idx, curr_a));
            } else if a_ts > v_ts + tolerance {
                break;
            }
            curr_a += 1;
        }
    }
    
    pairs
}

/// Calculate dynamic weights for modality fusion based on confidence/noise (Phase 134).
#[pyfunction]
pub fn calculate_dynamic_modality_weights_rust(
    vision_confidence: f32,
    audio_confidence: f32,
    text_confidence: f32,
) -> (f32, f32, f32) {
    let sum = vision_confidence + audio_confidence + text_confidence;
    if sum == 0.0 {
        (0.33, 0.33, 0.33)
    } else {
        (
            vision_confidence / sum,
            audio_confidence / sum,
            text_confidence / sum
        )
    }
}

/// Fuse features from multiple modalities (Weighted Sum / Concatenation)
#[pyfunction]
pub fn calculate_multimodal_fusion_rust(
    features: Vec<Vec<f32>>,
    weights: Vec<f32>,
    method: &str,
) -> Vec<f32> {
     if features.is_empty() { return Vec::new(); }
     
     match method {
         "concat" => {
             features.into_iter().flatten().collect()
         },
         "weighted_sum" => {
             let len = features[0].len();
             let mut result = vec![0.0; len];
             
             for (i, feat) in features.iter().enumerate() {
                 let w = weights.get(i).copied().unwrap_or(1.0);
                 if feat.len() == len {
                     for j in 0..len {
                         result[j] += feat[j] * w;
                     }
                 }
             }
             result
         },
         _ => Vec::new()
     }
}

/// Calculate alignment score between Audio and Video (Lip-sync check / Event detection).
#[pyfunction]
pub fn calculate_av_alignment_score_rust(
    audio_energy: Vec<f32>,
    visual_motion: Vec<f32>,
) -> f32 {
    // Cross-correlation check
    if audio_energy.is_empty() || visual_motion.is_empty() { return 0.0; }
    
    let len = audio_energy.len().min(visual_motion.len());
    let mut correlation = 0.0;
    
    for i in 0..len {
        correlation += audio_energy[i] * visual_motion[i];
    }
    
    correlation / len as f32
}

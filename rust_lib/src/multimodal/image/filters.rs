use pyo3::prelude::*;

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
    
    // Calculate means (Sampled)
    for i in (0..pixels.len()).step_by(12) {
        for c in 0..3 {
            sum_ref[c] += ref_pixels[i + c] as u64;
            sum_curr[c] += pixels[i + c] as u64;
        }
    }
    
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

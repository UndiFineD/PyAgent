use pyo3::prelude::*;

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

use pyo3::prelude::*;
use std::f32::consts::PI;

// =============================================================================
// Audio Processing Accelerations
// =============================================================================

/// Basic audio resampling using linear interpolation
#[pyfunction]
#[pyo3(signature = (samples, orig_sr, target_sr))]
pub fn resample_audio_rust(
    samples: Vec<f32>,
    orig_sr: u32,
    target_sr: u32,
) -> Vec<f32> {
    if orig_sr == target_sr || samples.is_empty() {
        return samples;
    }
    
    let ratio = orig_sr as f32 / target_sr as f32;
    let new_len = (samples.len() as f32 / ratio).ceil() as usize;
    let mut output = Vec::with_capacity(new_len);
    
    for i in 0..new_len {
        let src_idx = i as f32 * ratio;
        let idx0 = src_idx.floor() as usize;
        let idx1 = (idx0 + 1).min(samples.len() - 1);
        let frac = src_idx - idx0 as f32;
        
        let s0 = samples.get(idx0).copied().unwrap_or(0.0);
        let s1 = samples.get(idx1).copied().unwrap_or(0.0);
        
        output.push(s0 * (1.0 - frac) + s1 * frac);
    }
    
    output
}

/// Simple noise gate for noise suppression
#[pyfunction]
#[pyo3(signature = (samples, threshold = 0.01))]
pub fn audio_noise_suppression_rust(
    samples: Vec<f32>,
    threshold: f32,
) -> Vec<f32> {
    samples.into_iter()
        .map(|s| if s.abs() < threshold { 0.0 } else { s })
        .collect()
}

/// Calculate approximate direction of audio source given multi-channel input
/// Assumes interleaved channels (e.g., L, R, L, R...)
/// Returns angle in radians (-PI to PI)
#[pyfunction]
pub fn calculate_audio_direction_rust(
    interleaved_samples: Vec<f32>,
    channels: usize,
) -> f32 {
    if channels < 2 || interleaved_samples.len() < channels {
        return 0.0;
    }
    
    let mut l_energy = 0.0;
    let mut r_energy = 0.0;
    
    // Simple intensity panning approximation for stereo
    for chunk in interleaved_samples.chunks(channels) {
        if chunk.len() >= 2 {
            l_energy += chunk[0].abs();
            r_energy += chunk[1].abs();
        }
    }
    
    if l_energy + r_energy == 0.0 {
        return 0.0;
    }
    
    // Map energy balance to angle: Left = -PI/2, Right = PI/2, Center = 0
    let balance = (r_energy - l_energy) / (r_energy + l_energy);
    balance * (PI / 2.0)
}

/// Mix multiple audio tracks into one
#[pyfunction]
pub fn audio_mix_tracks_rust(
    tracks: Vec<Vec<f32>>,
    weights: Vec<f32>,
) -> Vec<f32> {
    if tracks.is_empty() { return Vec::new(); }
    
    let max_len = tracks.iter().map(|t| t.len()).max().unwrap_or(0);
    let mut mixed = vec![0.0f32; max_len];
    let default_weight = 1.0;
    
    for (i, track) in tracks.iter().enumerate() {
        let w = weights.get(i).copied().unwrap_or(default_weight);
        for (j, &sample) in track.iter().enumerate() {
            mixed[j] += sample * w;
        }
    }
    
    // Normalize to prevent clipping? Optionally clamp
    for s in mixed.iter_mut() {
        *s = s.clamp(-1.0, 1.0);
    }
    
    mixed
}

/// Calculate Mel Spectrogram features (Placeholder/Stub for heavy computation)
/// In a real system, this would use rustfft.
#[pyfunction]
#[pyo3(signature = (samples, _sample_rate, n_mels = 80, n_fft = 400, hop_length = 160))]
pub fn calculate_mel_features_rust(
    samples: Vec<f32>,
    _sample_rate: u32,
    n_mels: usize,
    n_fft: usize,
    hop_length: usize,
) -> Vec<Vec<f32>> {
    // Simplified specific implementation or placeholder
    if samples.len() < n_fft { return Vec::new(); }
    
    let num_frames = (samples.len() - n_fft) / hop_length + 1;
    let mut mels = Vec::with_capacity(num_frames);
    
    for _ in 0..num_frames {
        let frame = vec![0.0f32; n_mels];
        // TODO: Implement FFT and Mel filterbank application
        mels.push(frame); 
    }
    mels
}

/// Quantize audio samples to int8
#[pyfunction]
pub fn audio_quantize_int8_rust(samples: Vec<f32>) -> Vec<i8> {
    samples.into_iter().map(|s| {
        (s.clamp(-1.0, 1.0) * 127.0).round() as i8
    }).collect()
}

/// Simple Voice Activity Detection (VAD) based on energy
#[pyfunction]
#[pyo3(signature = (samples, sample_rate, frame_duration_ms = 30, threshold = 0.01))]
pub fn speech_vad_rust(
    samples: Vec<f32>,
    sample_rate: u32,
    frame_duration_ms: usize,
    threshold: f32,
) -> Vec<(usize, usize)> { // Returns list of (start_sample, end_sample) tuples
    let frame_size = (sample_rate as usize * frame_duration_ms) / 1000;
    let mut segments = Vec::new();
    let mut in_speech = false;
    let mut start = 0;
    
    for (i, frame) in samples.chunks(frame_size).enumerate() {
        let energy: f32 = frame.iter().map(|x| x * x).sum::<f32>() / frame.len() as f32;
        let is_speech = energy > threshold;
        
        let current_pos = i * frame_size;
        
        if is_speech && !in_speech {
            in_speech = true;
            start = current_pos;
        } else if !is_speech && in_speech {
            in_speech = false;
            segments.push((start, current_pos));
        }
    }
    
    if in_speech {
        segments.push((start, samples.len()));
    }
    
    segments
}

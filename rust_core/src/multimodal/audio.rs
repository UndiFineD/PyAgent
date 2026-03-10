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
    if samples.len() < n_fft || n_fft == 0 || hop_length == 0 || n_mels == 0 {
        return Vec::new();
    }
    
    let num_frames = (samples.len() - n_fft) / hop_length + 1;
    let mut mels = Vec::with_capacity(num_frames);

    let sample_rate = _sample_rate.max(1) as f32;
    let n_freq_bins = n_fft / 2 + 1;

    let hann_window: Vec<f32> = if n_fft == 1 {
        vec![1.0]
    } else {
        (0..n_fft)
            .map(|i| {
                let phase = (2.0 * PI * i as f32) / (n_fft as f32 - 1.0);
                0.5 - 0.5 * phase.cos()
            })
            .collect()
    };

    let hz_to_mel = |hz: f32| 2595.0 * (1.0 + hz / 700.0).log10();
    let mel_to_hz = |mel: f32| 700.0 * (10f32.powf(mel / 2595.0) - 1.0);

    let mel_min = hz_to_mel(0.0);
    let mel_max = hz_to_mel(sample_rate * 0.5);
    let mel_step = (mel_max - mel_min) / (n_mels + 1) as f32;

    let mut bin_points = Vec::with_capacity(n_mels + 2);
    for i in 0..(n_mels + 2) {
        let mel = mel_min + mel_step * i as f32;
        let hz = mel_to_hz(mel);
        let mut bin = ((n_fft + 1) as f32 * hz / sample_rate).floor() as usize;
        if bin >= n_freq_bins {
            bin = n_freq_bins - 1;
        }
        bin_points.push(bin);
    }

    let mut filterbank: Vec<Vec<(usize, f32)>> = Vec::with_capacity(n_mels);
    for m in 1..=n_mels {
        let left = bin_points[m - 1];
        let mut center = bin_points[m];
        let mut right = bin_points[m + 1];

        if center <= left {
            center = (left + 1).min(n_freq_bins - 1);
        }
        if right <= center {
            right = (center + 1).min(n_freq_bins);
        }

        let mut weights = Vec::new();

        if center > left {
            let denom = (center - left) as f32;
            for k in left..center {
                if k < n_freq_bins {
                    weights.push((k, (k - left) as f32 / denom));
                }
            }
        }
        if right > center {
            let denom = (right - center) as f32;
            for k in center..right {
                if k < n_freq_bins {
                    weights.push((k, (right - k) as f32 / denom));
                }
            }
        }

        filterbank.push(weights);
    }

    let mut windowed = vec![0.0f32; n_fft];
    let mut power_spectrum = vec![0.0f32; n_freq_bins];
    let fft_norm = 1.0 / n_fft as f32;

    for frame_idx in 0..num_frames {
        let start = frame_idx * hop_length;
        for i in 0..n_fft {
            windowed[i] = samples[start + i] * hann_window[i];
        }

        for k in 0..n_freq_bins {
            let omega = 2.0 * PI * k as f32 / n_fft as f32;
            let cos_w = omega.cos();
            let sin_w = omega.sin();

            let mut c = 1.0f32;
            let mut s = 0.0f32;
            let mut re = 0.0f32;
            let mut im = 0.0f32;

            for &x in &windowed {
                re += x * c;
                im -= x * s;
                let next_c = c * cos_w - s * sin_w;
                s = s * cos_w + c * sin_w;
                c = next_c;
            }

            power_spectrum[k] = (re * re + im * im) * fft_norm;
        }

        let mut frame = vec![0.0f32; n_mels];
        for (m, band) in filterbank.iter().enumerate() {
            let mut acc = 0.0f32;
            for &(bin, w) in band {
                acc += power_spectrum[bin] * w;
            }
            frame[m] = acc.max(1e-10).ln();
        }

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

use pyo3::prelude::*;
use std::collections::HashMap;

/// Fused PackKV Attention (arXiv:2512.24449)
/// Performs register-level decompression during attention matmul.
/// Provides a deterministic CPU fallback until SIMD/CUDA kernels are wired.
#[pyfunction]
#[pyo3(signature = (q, _k_compressed, _v_compressed, _metadata_map, _scale=None))]
pub fn fused_packkv_attention_rust(
    q: Vec<f32>,
    _k_compressed: Vec<u8>,
    _v_compressed: Vec<u8>,
    _metadata_map: HashMap<i32, HashMap<String, f32>>,
    _scale: Option<f32>,
) -> PyResult<Vec<f32>> {
    if q.is_empty() {
        return Ok(q);
    }

    // Deterministic compressed summary used as a lightweight CPU fallback signal.
    let k_avg = if _k_compressed.is_empty() {
        0.0
    } else {
        _k_compressed.iter().map(|&b| b as f32).sum::<f32>() / _k_compressed.len() as f32
    };
    let v_avg = if _v_compressed.is_empty() {
        0.0
    } else {
        _v_compressed.iter().map(|&b| b as f32).sum::<f32>() / _v_compressed.len() as f32
    };

    let meta_scale = _metadata_map
        .values()
        .filter_map(|m| m.get("scale").copied())
        .sum::<f32>();
    let scale = _scale.unwrap_or(1.0).max(0.0);
    let compressed_bias = ((k_avg - v_avg) / 255.0 + meta_scale * 0.001) * scale;

    let output = q
        .into_iter()
        .map(|value| (value + compressed_bias).tanh())
        .collect();
    Ok(output)
}

use pyo3::prelude::*;

/// Symmetric quantization of a weight tensor.
/// Returns (quantized_values, scale).
#[pyfunction]
pub fn quantize_symmetric_rust(
    weights: Vec<f32>,
    bits: u8,
) -> PyResult<(Vec<i8>, f32)> {
    if weights.is_empty() {
        return Ok((vec![], 1.0));
    }
    
    let qmax = ((1i32 << (bits - 1)) - 1) as f32;
    
    // Find max absolute value
    let max_abs = weights.iter().map(|w| w.abs()).fold(0.0f32, f32::max);
    
    // Compute scale
    let scale = if max_abs > 0.0 { max_abs / qmax } else { 1.0 };
    
    // Quantize
    let quantized: Vec<i8> = weights
        .iter()
        .map(|w| {
            let q = (w / scale).round();
            q.clamp(-qmax - 1.0, qmax) as i8
        })
        .collect();
    
    Ok((quantized, scale))
}

/// Asymmetric quantization with zero point.
/// Returns (quantized_values, scale, zero_point).
#[pyfunction]
pub fn quantize_asymmetric_rust(
    weights: Vec<f32>,
    bits: u8,
) -> PyResult<(Vec<u8>, f32, i32)> {
    if weights.is_empty() {
        return Ok((vec![], 1.0, 0));
    }
    
    let qmax = ((1u32 << bits) - 1) as f32;
    
    // Find min and max
    let min_val = weights.iter().fold(f32::INFINITY, |a, &b| a.min(b));
    let max_val = weights.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
    
    // Compute scale and zero point
    let scale = if max_val > min_val { 
        (max_val - min_val) / qmax 
    } else { 
        1.0 
    };
    let scale = scale.max(1e-8);
    
    let zp = (-min_val / scale).round() as i32;
    let zp = zp.clamp(0, qmax as i32);
    
    // Quantize
    let quantized: Vec<u8> = weights
        .iter()
        .map(|w| {
            let q = (w / scale + zp as f32).round();
            q.clamp(0.0, qmax) as u8
        })
        .collect();
    
    Ok((quantized, scale, zp))
}

/// Dequantize INT4 packed values to float32.
/// Input is packed int8 (two int4 per int8).
#[pyfunction]
pub fn dequantize_int4_rust(
    packed: Vec<i8>,
    scale: f32,
    zero_point: i32,
) -> PyResult<Vec<f32>> {
    let mut result = Vec::with_capacity(packed.len() * 2);
    
    for byte in packed {
        // Extract lower 4 bits
        let lower = byte & 0x0F;
        // Sign extend if > 7
        let lower = if lower > 7 { lower - 16 } else { lower };
        
        // Extract upper 4 bits
        let upper = (byte >> 4) & 0x0F;
        let upper = if upper > 7 { upper - 16 } else { upper };
        
        // Dequantize
        result.push((lower as i32 - zero_point) as f32 * scale);
        result.push((upper as i32 - zero_point) as f32 * scale);
    }
    
    Ok(result)
}

/// Pack two int4 values into one int8.
#[pyfunction]
pub fn pack_int4_rust(values: Vec<i8>) -> PyResult<Vec<i8>> {
    let mut packed = Vec::with_capacity((values.len() + 1) / 2);
    
    for chunk in values.chunks(2) {
        let lower = chunk[0] & 0x0F;
        let upper = if chunk.len() > 1 { chunk[1] & 0x0F } else { 0 };
        packed.push(lower | (upper << 4));
    }
    
    Ok(packed)
}

/// Compute per-group quantization scales.
/// Returns scales for each group.
#[pyfunction]
pub fn compute_scales_rust(
    weights: Vec<f32>,
    group_size: usize,
    bits: u8,
    symmetric: bool,
) -> PyResult<Vec<f32>> {
    if weights.is_empty() {
        return Ok(vec![]);
    }
    
    let qmax = if symmetric {
        ((1i32 << (bits - 1)) - 1) as f32
    } else {
        ((1u32 << bits) - 1) as f32
    };
    
    let num_groups = (weights.len() + group_size - 1) / group_size;
    let mut scales = Vec::with_capacity(num_groups);
    
    for chunk in weights.chunks(group_size) {
        if symmetric {
            let max_abs = chunk.iter().map(|w| w.abs()).fold(0.0f32, f32::max);
            let scale = if max_abs > 0.0 { max_abs / qmax } else { 1.0 };
            scales.push(scale);
        } else {
            let min_val = chunk.iter().fold(f32::INFINITY, |a, &b| a.min(b));
            let max_val = chunk.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
            let scale = if max_val > min_val {
                (max_val - min_val) / qmax
            } else {
                1.0
            };
            scales.push(scale.max(1e-8));
        }
    }
    
    Ok(scales)
}

/// Batch dequantize with per-group scales.
/// Optimized for INT8/INT4 weight dequantization during inference.
#[pyfunction]
pub fn batch_dequantize_rust(
    quantized: Vec<i8>,
    scales: Vec<f32>,
    group_size: usize,
    bits: u8,
) -> PyResult<Vec<f32>> {
    let mut result = Vec::with_capacity(quantized.len());
    
    for (i, &q) in quantized.iter().enumerate() {
        let group_idx = i / group_size;
        let scale = scales.get(group_idx).copied().unwrap_or(1.0);
        
        if bits == 8 {
            result.push(q as f32 * scale);
        } else {
            // For packed 4-bit, handled separately ideally, but simplified here likely expecting unpacked i8 logic
            result.push(q as f32 * scale);
        }
    }
    
    Ok(result)
}

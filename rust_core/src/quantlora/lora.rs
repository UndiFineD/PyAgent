use pyo3::prelude::*;

/// Merge LoRA delta (B @ A * scaling) into base weights.
/// base_weight: [out_features, in_features]
/// lora_a: [rank, in_features]
/// lora_b: [out_features, rank]
#[pyfunction]
pub fn lora_merge_rust(
    base_weight: Vec<f32>,
    lora_a: Vec<f32>,
    lora_b: Vec<f32>,
    out_features: usize,
    in_features: usize,
    rank: usize,
    scaling: f32,
) -> PyResult<Vec<f32>> {
    if base_weight.len() != out_features * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "base_weight size mismatch"
        ));
    }
    if lora_a.len() != rank * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "lora_a size mismatch"
        ));
    }
    if lora_b.len() != out_features * rank {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "lora_b size mismatch"
        ));
    }
    
    // Compute delta = B @ A * scaling
    // B is [out_features, rank], A is [rank, in_features]
    // Result is [out_features, in_features]
    let mut result = base_weight.clone();
    
    for o in 0..out_features {
        for i in 0..in_features {
            let mut delta = 0.0f32;
            for r in 0..rank {
                // B[o, r] * A[r, i]
                delta += lora_b[o * rank + r] * lora_a[r * in_features + i];
            }
            result[o * in_features + i] += delta * scaling;
        }
    }
    
    Ok(result)
}

/// Compute LoRA output: x @ A.T @ B.T * scaling
/// For fused LoRA application during inference.
#[pyfunction]
pub fn lora_forward_rust(
    x: Vec<f32>,
    lora_a: Vec<f32>,
    lora_b: Vec<f32>,
    batch_size: usize,
    in_features: usize,
    out_features: usize,
    rank: usize,
    scaling: f32,
) -> PyResult<Vec<f32>> {
    // x: [batch_size, in_features]
    // lora_a: [rank, in_features]
    // lora_b: [out_features, rank]
    
    if x.len() != batch_size * in_features {
        return Err(pyo3::exceptions::PyValueError::new_err("x size mismatch"));
    }
    
    // Step 1: hidden = x @ A.T -> [batch_size, rank]
    let mut hidden = vec![0.0f32; batch_size * rank];
    for b in 0..batch_size {
        for r in 0..rank {
            let mut sum = 0.0f32;
            for i in 0..in_features {
                sum += x[b * in_features + i] * lora_a[r * in_features + i];
            }
            hidden[b * rank + r] = sum;
        }
    }
    
    // Step 2: output = hidden @ B.T * scaling -> [batch_size, out_features]
    let mut output = vec![0.0f32; batch_size * out_features];
    for b in 0..batch_size {
        for o in 0..out_features {
            let mut sum = 0.0f32;
            for r in 0..rank {
                sum += hidden[b * rank + r] * lora_b[o * rank + r];
            }
            output[b * out_features + o] = sum * scaling;
        }
    }
    
    Ok(output)
}

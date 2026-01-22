// Phase 51: Multimedia & Attention
// High-performance Rust kernels for cross-modal attention and sequence alignment.

use pyo3::prelude::*;
use std::iter::zip;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cross_modal_attention_rust, m)?)?;
    m.add_function(wrap_pyfunction!(align_sequences_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_multimodal_coherence_rust, m)?)?;
    Ok(())
}

#[pyfunction]
/// Performs a fast cross-modal dot-product attention calculation.
/// q: Query sequence (Modality A), k: Key sequence (Modality B), v: Value sequence (Modality B).
pub fn cross_modal_attention_rust(
    q: Vec<Vec<f32>>,
    k: Vec<Vec<f32>>,
    v: Vec<Vec<f32>>,
    scale: f32,
) -> PyResult<Vec<Vec<f32>>> {
    let n_q = q.len();
    let n_k = k.len();
    if n_q == 0 || n_k == 0 {
        return Ok(vec![]);
    }
    let d = q[0].len();
    
    let mut outputs = vec![vec![0.0; d]; n_q];
    
    for i in 0..n_q {
        let mut weights = vec![0.0; n_k];
        let mut sum_exp = 0.0;
        
        // Compute dot product and softmax
        for j in 0..n_k {
            let dot: f32 = zip(&q[i], &k[j]).map(|(a, b)| a * b).sum();
            let score = (dot * scale).exp();
            weights[j] = score;
            sum_exp += score;
        }
        
        // Normalize and generate value output
        if sum_exp > 0.0 {
            for j in 0..n_k {
                let weight = weights[j] / sum_exp;
                for (out_val, v_val) in zip(&mut outputs[i], &v[j]) {
                    *out_val += weight * v_val;
                }
            }
        }
    }
    
    Ok(outputs)
}

#[pyfunction]
/// Align two sequences (e.g. video frames and audio samples) using attention mapping.
/// Returns a list of indices in seq_b that most closely align with seq_a.
pub fn align_sequences_rust(
    seq_a: Vec<Vec<f32>>,
    seq_b: Vec<Vec<f32>>,
) -> PyResult<Vec<usize>> {
    let mut alignment = Vec::with_capacity(seq_a.len());
    
    for vec_a in seq_a {
        let mut best_idx = 0;
        let mut max_sim = -1.0;
        
        for (j, vec_b) in seq_b.iter().enumerate() {
            let dot: f32 = zip(&vec_a, vec_b).map(|(a, b)| a * b).sum();
            if dot > max_sim {
                max_sim = dot;
                best_idx = j;
            }
        }
        alignment.push(best_idx);
    }
    
    Ok(alignment)
}

#[pyfunction]
/// Calculate a coherence score between two multimodal channels.
/// 1.0 means perfectly synchronized/coherent, < 0.5 means mismatched.
pub fn calculate_multimodal_coherence_rust(
    channel_a: Vec<Vec<f32>>,
    channel_b: Vec<Vec<f32>>,
) -> PyResult<f32> {
    if channel_a.is_empty() || channel_b.is_empty() {
        return Ok(0.0);
    }
    
    let n = channel_a.len().min(channel_b.len());
    let mut total_sim = 0.0;
    
    for i in 0..n {
        let dot: f32 = zip(&channel_a[i], &channel_b[i]).map(|(a, b)| a * b).sum();
        total_sim += dot;
    }
    
    Ok(total_sim / n as f32)
}

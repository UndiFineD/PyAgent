use pyo3::prelude::*;
use ndarray::prelude::*;
use rayon::prelude::*;

/// Fast cosine similarity search across a matrix of embeddings.
/// Returns the top K matches with their indices and similarity scores.
#[pyfunction]
pub fn top_k_cosine_similarity(
    query: Vec<f32>,
    embeddings: Vec<Vec<f32>>,
    k: usize,
) -> PyResult<Vec<(usize, f32)>> {
    if embeddings.is_empty() || query.is_empty() {
        return Ok(vec![]);
    }

    let q_arr = Array1::from_vec(query);
    let q_norm = (q_arr.mapv(|x| x * x).sum()).sqrt();
    
    // Process embeddings in parallel
    let mut scores: Vec<(usize, f32)> = embeddings.into_par_iter().enumerate().map(|(idx, emb)| {
        let e_arr = Array1::from_vec(emb);
        let dot = q_arr.dot(&e_arr);
        let e_norm = (e_arr.mapv(|x| x * x).sum()).sqrt();
        
        let similarity = if q_norm > 0.0 && e_norm > 0.0 {
            dot / (q_norm * e_norm)
        } else {
            0.0
        };
        (idx, similarity)
    }).collect();

    // Sort by similarity descending
    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    // Return Top K
    Ok(scores.into_iter().take(k).collect())
}

#[pyfunction]
pub fn average_feature_vectors(vectors: Vec<Vec<f32>>) -> PyResult<Vec<f32>> {
    if vectors.is_empty() {
        return Ok(vec![]);
    }
    let dim = vectors[0].len();
    let mut total = vec![0.0; dim];
    for v in &vectors {
        for (i, &val) in v.iter().enumerate().take(dim) {
            total[i] += val;
        }
    }
    let n = vectors.len() as f32;
    for val in total.iter_mut() {
        *val /= n;
    }
    Ok(total)
}

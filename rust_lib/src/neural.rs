pub mod config;
pub mod cache;
pub mod layers;
pub mod clustering;
pub mod ops;
pub mod inference_utils;
pub mod types;
pub mod network;
pub mod transformer;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<config::HardwareProfile>()?;
    m.add_class::<config::TransformerConfig>()?;
    m.add_class::<cache::KVCache>()?;
    m.add_class::<transformer::NeuralTransformer>()?;
    m.add_class::<network::FlexibleNeuralNetwork>()?;
    m.add_class::<types::GenerationStats>()?;

    m.add_function(wrap_pyfunction!(clustering::cluster_interactions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(ops::top_k_cosine_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(ops::average_feature_vectors, m)?)?;
    
    m.add_function(wrap_pyfunction!(inference_utils::generate_synthetic_snippets_with_stats, m)?)?;
    m.add_function(wrap_pyfunction!(inference_utils::generate_synthetic_snippets, m)?)?;
    m.add_function(wrap_pyfunction!(inference_utils::vectorize_text_insight_with_stats, m)?)?;
    m.add_function(wrap_pyfunction!(inference_utils::vectorize_text_insight, m)?)?;
    m.add_function(wrap_pyfunction!(inference_utils::generate_neural_response, m)?)?;

    Ok(())
}

use pyo3::prelude::*;
use rand::prelude::*;

use crate::neural::types::GenerationStats;
use crate::neural::config::{HardwareProfile, TransformerConfig};
use crate::neural::transformer::NeuralTransformer;

#[pyfunction]
pub fn generate_synthetic_snippets_with_stats(count: usize) -> PyResult<(Vec<String>, GenerationStats)> {
    let start = std::time::Instant::now();
    let mut rng = thread_rng();
    let templates = [
        "def func_{}(*args): return sum(args)",
        "async def handle_{}(req): return await req.json()",
        "class Node_{}: def __init__(self): self.v = 0",
        "lambda x: x if x > 0 else 0",
    ];
    let mut results = Vec::with_capacity(count);
    let mut total_tokens = 0;

    for i in 0..count {
        let tpl = templates[rng.gen_range(0..templates.len())];
        let snippet = tpl.replace("{}", &i.to_string());
        total_tokens += snippet.split_whitespace().count();
        results.push(snippet);
    }

    let duration = start.elapsed();
    let duration_ms = duration.as_secs_f64() * 1000.0;
    let tps = if duration.as_secs_f64() > 0.0 {
        total_tokens as f64 / duration.as_secs_f64()
    } else {
        0.0
    };

    // Cost: 0.0005 cent per token = 0.000005 USD per token
    let cost_usd = (total_tokens as f64) * 0.000005;

    Ok((
        results,
        GenerationStats {
            token_count: total_tokens,
            tps,
            duration_ms,
            cost_usd,
        },
    ))
}

#[pyfunction]
pub fn generate_synthetic_snippets(count: usize) -> PyResult<Vec<String>> {
    let (snippets, _) = generate_synthetic_snippets_with_stats(count)?;
    Ok(snippets)
}

#[pyfunction]
pub fn vectorize_text_insight_with_stats(text: &str) -> PyResult<(Vec<f32>, GenerationStats)> {
    let start = std::time::Instant::now();
    
    // We create a fresh instance here as a stateless utility
    let profile = HardwareProfile::new(None);
    let config = TransformerConfig::auto_configure(&profile);
    let transformer = NeuralTransformer::new(config);
    
    let vector = transformer.vectorize(text)?;
    let tokens = text.split_whitespace().count().max(1);
    
    let duration = start.elapsed();
    let duration_secs = duration.as_secs_f64();
    let tps = if duration_secs > 0.0 { tokens as f64 / duration_secs } else { 0.0 };
    
    // Cost: 0.0005 cent per token = 0.000005 USD per token
    let cost_usd = (tokens as f64) * 0.000005;

    Ok((vector, GenerationStats {
        token_count: tokens,
        tps,
        duration_ms: duration_secs * 1000.0,
        cost_usd,
    }))
}

#[pyfunction]
pub fn vectorize_text_insight(text: &str) -> PyResult<Vec<f32>> {
    let (vec, _) = vectorize_text_insight_with_stats(text)?;
    Ok(vec)
}

/// Shorthand for generating a response without full stats (Phase 319).
#[pyfunction]
pub fn generate_neural_response(prompt: &str) -> PyResult<String> {
    let profile = HardwareProfile::new(None);
    let config = TransformerConfig::auto_configure(&profile);
    let transformer = NeuralTransformer::new(config);
    let (res, _) = transformer.generate_response_with_stats(prompt)?;
    Ok(res)
}

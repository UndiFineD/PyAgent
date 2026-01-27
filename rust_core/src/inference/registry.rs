use pyo3::prelude::*;

// =============================================================================
// Phase 41: Model Registry Acceleration
// =============================================================================

/// Compute model architecture fingerprint from config
#[pyfunction]
pub fn architecture_fingerprint_rust(
    hidden_size: usize,
    num_layers: usize,
    num_heads: usize,
    vocab_size: usize,
    intermediate_size: usize,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    hidden_size.hash(&mut hasher);
    num_layers.hash(&mut hasher);
    num_heads.hash(&mut hasher);
    vocab_size.hash(&mut hasher);
    intermediate_size.hash(&mut hasher);
    hasher.finish()
}

/// Estimate VRAM requirement for a model
/// Returns (min_vram_bytes, optimal_vram_bytes)
#[pyfunction]
pub fn estimate_vram_bytes_rust(
    num_params: u64,
    precision_bits: u8,
    context_length: usize,
    batch_size: usize,
    kv_cache_factor: f64,
) -> (u64, u64) {
    // Base model weights
    let bytes_per_param = (precision_bits as f64) / 8.0;
    let model_bytes = (num_params as f64 * bytes_per_param) as u64;
    
    // KV cache estimation (simplified)
    // kv_bytes = batch_size * context_length * hidden_size * 2 (k+v) * num_layers * bytes
    let kv_estimate = (batch_size * context_length) as f64 * kv_cache_factor * bytes_per_param;
    let kv_bytes = kv_estimate as u64;
    
    // Activation memory (rough estimate: 10-20% of model size)
    let activation_bytes = model_bytes / 10;
    
    let min_vram = model_bytes + kv_bytes / 2;
    let optimal_vram = model_bytes + kv_bytes + activation_bytes;
    
    (min_vram, optimal_vram)
}

/// Match model architecture from config patterns
/// Returns architecture name or "unknown"
#[pyfunction]
pub fn detect_architecture_rust(
    architectures: Vec<String>,
    model_type: String,
) -> String {
    // Check architectures list first
    for arch in &architectures {
        let lower = arch.to_lowercase();
        if lower.contains("llama") {
            return "llama".to_string();
        }
        if lower.contains("mistral") {
            return "mistral".to_string();
        }
        if lower.contains("qwen") {
            return "qwen2".to_string();
        }
        if lower.contains("falcon") {
            return "falcon".to_string();
        }
        if lower.contains("gemma") {
            return "gemma2".to_string();
        }
        if lower.contains("phi") {
            return "phi3".to_string();
        }
        if lower.contains("starcoder") {
            return "starcoder2".to_string();
        }
    }
    
    // Fallback to model_type
    model_type.to_lowercase()
}

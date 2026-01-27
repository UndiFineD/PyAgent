use pyo3::prelude::*;
use sysinfo::System;

// Hardware profile detailing system capabilities.
#[pyclass]
#[derive(Clone, Debug)]
pub struct HardwareProfile {
    #[pyo3(get)]
    pub cpu_cores: usize,
    #[pyo3(get)]
    pub total_memory_gb: f64,
    #[pyo3(get)]
    pub available_memory_gb: f64,
    #[pyo3(get)]
    pub has_gpu: bool,
    #[pyo3(get)]
    pub vram_gb: f64,
}

#[pymethods]
impl HardwareProfile {
    #[new]
    pub fn new(vram_override: Option<f64>) -> Self {
        let mut sys = System::new_all();
        sys.refresh_all();

        let total_mem = sys.total_memory() as f64 / 1024.0 / 1024.0 / 1024.0;
        let avail_mem = sys.available_memory() as f64 / 1024.0 / 1024.0 / 1024.0;
        let cores = sys.cpus().len();

        // Simple heuristic for GPU detection (Simulated or via env)
        let has_gpu = vram_override.is_some() || std::env::var("CUDA_VISIBLE_DEVICES").is_ok();
        let vram = vram_override.unwrap_or(if has_gpu { 4.0 } else { 0.0 });

        HardwareProfile {
            cpu_cores: cores,
            total_memory_gb: total_mem,
            available_memory_gb: avail_mem,
            has_gpu,
            vram_gb: vram,
        }
    }
}

/// Dynamic Transformer Configuration based on Hardware.
#[pyclass]
#[derive(Clone, Debug)]
pub struct TransformerConfig {
    #[pyo3(get)]
    pub d_model: usize,
    #[pyo3(get)]
    pub n_heads: usize,
    #[pyo3(get)]
    pub n_kv_heads: usize,
    #[pyo3(get)]
    pub n_layers: usize,
    #[pyo3(get)]
    pub d_ff: usize,
}

#[pymethods]
impl TransformerConfig {
    #[staticmethod]
    pub fn auto_configure(profile: &HardwareProfile) -> Self {
        // Scaling logic based on VRAM and Total RAM
        if profile.vram_gb >= 24.0 || profile.available_memory_gb >= 64.0 {
            // "Heavy" scale: Grouped-Query Attention (GQA) with 16Q/8KV
            TransformerConfig { d_model: 1024, n_heads: 16, n_kv_heads: 8, n_layers: 24, d_ff: 4 * 1024 }
        } else if profile.vram_gb >= 8.0 || profile.available_memory_gb >= 16.0 {
            // "Medium" scale: 8Q/4KV
            TransformerConfig { d_model: 512, n_heads: 8, n_kv_heads: 4, n_layers: 12, d_ff: 2 * 1024 }
        } else {
            // "Light" scale: 4Q/2KV
            TransformerConfig { d_model: 256, n_heads: 4, n_kv_heads: 2, n_layers: 6, d_ff: 1024 }
        }
    }
}

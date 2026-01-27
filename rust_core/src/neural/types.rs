use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug)]
pub struct GenerationStats {
    #[pyo3(get)]
    pub token_count: usize,
    #[pyo3(get)]
    pub tps: f64,
    #[pyo3(get)]
    pub duration_ms: f64,
    #[pyo3(get)]
    pub cost_usd: f64,
}

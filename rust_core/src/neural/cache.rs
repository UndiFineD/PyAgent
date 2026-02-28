use pyo3::prelude::*;
use ndarray::prelude::*;

/// Key-Value Cache for optimized multi-step inference.
#[pyclass]
#[derive(Clone)]
pub struct KVCache {
    pub k: Vec<Array3<f32>>, // Layer -> [Seq, N_KV_Heads, Head_Dim]
    pub v: Vec<Array3<f32>>,
}

#[pymethods]
impl KVCache {
    #[new]
    pub fn new(n_layers: usize) -> Self {
        KVCache {
            k: vec![Array3::zeros((0, 0, 0)); n_layers],
            v: vec![Array3::zeros((0, 0, 0)); n_layers],
        }
    }

    pub fn clear(&mut self) {
        for layer_k in &mut self.k {
            *layer_k = Array3::zeros((0, 0, 0));
        }
        for layer_v in &mut self.v {
            *layer_v = Array3::zeros((0, 0, 0));
        }
    }
}

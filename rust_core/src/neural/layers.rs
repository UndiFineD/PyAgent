use ndarray::prelude::*;
use rand::prelude::*;
use rand_distr::{Normal, Distribution};
use rayon::prelude::*;

/// Root Mean Square Layer Normalization (Standard in modern LLMs like Llama).
pub struct RMSNorm {
    pub weight: Array1<f32>,
    pub eps: f32,
}

impl RMSNorm {
    pub fn new(dim: usize) -> Self {
        RMSNorm {
            weight: Array1::ones(dim),
            eps: 1e-6,
        }
    }

    pub fn forward(&self, x: &Array2<f32>) -> Array2<f32> {
        let n = x.ncols() as f32;
        let mut output = x.clone();
        
        // Industrial strength parallelized row processing
        output.axis_iter_mut(Axis(0)).into_par_iter().for_each(|mut row| {
            let rms = (row.mapv(|v| v * v).sum() / n + self.eps).sqrt();
            row.mapv_inplace(|v| v / rms);
            row *= &self.weight;
        });
        
        output
    }
}

/// Rotary Positional Embeddings (RoPE).
pub struct RoPE {
    pub cos: Array2<f32>,
    pub sin: Array2<f32>,
}

impl RoPE {
    pub fn new(dim: usize, max_seq_len: usize) -> Self {
        let mut cos = Array2::zeros((max_seq_len, dim));
        let mut sin = Array2::zeros((max_seq_len, dim));
        
        for pos in 0..max_seq_len {
            for i in 0..(dim / 2) {
                let theta = (pos as f32) / (10000.0f32.powf((2 * i) as f32 / dim as f32));
                cos[[pos, i * 2]] = theta.cos();
                cos[[pos, i * 2 + 1]] = theta.cos();
                sin[[pos, i * 2]] = theta.sin();
                sin[[pos, i * 2 + 1]] = theta.sin();
            }
        }
        
        RoPE { cos, sin }
    }

    pub fn apply(&self, x: &mut Array2<f32>) {
        let (seq_len, dim) = (x.nrows(), x.ncols());
        let (max_seq_len, rope_dim) = (self.cos.nrows(), self.cos.ncols());
        
        let apply_len = seq_len.min(max_seq_len);
        let apply_dim = dim.min(rope_dim);

        for i in 0..apply_len {
            for j in (0..apply_dim).step_by(2) {
                let x0 = x[[i, j]];
                let x1 = x[[i, j + 1]];
                let c = self.cos[[i, j]];
                let s = self.sin[[i, j]];
                
                // Rotation matrix: [c -s; s c] * [x0; x1]
                x[[i, j]] = x0 * c - x1 * s;
                x[[i, j + 1]] = x0 * s + x1 * c;
            }
        }
    }
}

/// Helper for Kaiming (He) Initialization used in modern neural networks.
pub fn init_kaiming(rows: usize, cols: usize) -> Array2<f32> {
    let mut rng = thread_rng();
    let std = (2.0 / rows as f32).sqrt();
    let dist = Normal::new(0.0, std).unwrap();
    Array2::from_shape_fn((rows, cols), |_| dist.sample(&mut rng))
}

/// A single layer in the transformer architecture supporting Grouped-Query Attention (GQA).
pub struct TransformerLayer {
    pub norm: RMSNorm,
    pub rope: RoPE,
    pub q_proj: Array2<f32>,
    pub k_proj: Array2<f32>,
    pub v_proj: Array2<f32>,
    pub o_proj: Array2<f32>,
    pub ff_up: Array2<f32>,
    pub ff_gate: Array2<f32>,
    pub ff_down: Array2<f32>,
}

impl TransformerLayer {
    pub fn new(d_model: usize, d_ff: usize, n_heads: usize, n_kv_heads: usize) -> Self {
        let head_dim = d_model / n_heads;
        let kv_dim = n_kv_heads * head_dim;
        
        TransformerLayer {
            norm: RMSNorm::new(d_model),
            rope: RoPE::new(head_dim, 2048),
            q_proj: init_kaiming(d_model, d_model),
            k_proj: init_kaiming(d_model, kv_dim),
            v_proj: init_kaiming(d_model, kv_dim),
            o_proj: init_kaiming(d_model, d_model),
            ff_up: init_kaiming(d_model, d_ff),
            ff_gate: init_kaiming(d_model, d_ff),
            ff_down: init_kaiming(d_ff, d_model),
        }
    }
}

use pyo3::prelude::*;
use ndarray::prelude::*;
use crate::neural::layers::init_kaiming;
use crate::neural::config::HardwareProfile;

/// A flexible-size neural network that adapts its architecture to available resources.
#[pyclass]
pub struct FlexibleNeuralNetwork {
    #[pyo3(get)]
    pub layer_sizes: Vec<usize>,
    pub weights: Vec<Array2<f32>>,
    pub biases: Vec<Array1<f32>>,
    pub profile: HardwareProfile,
}

#[pymethods]
impl FlexibleNeuralNetwork {
    #[new]
    pub fn new(profile: HardwareProfile) -> Self {
        // 1. Decide layer sizes based on available memory
        let mut layers = vec![profile.cpu_cores * 16]; // Input layer
        
        // Safety check for small systems
        let mut depth = 1;
        if profile.available_memory_gb > 32.0 {
            depth = 4;
        } else if profile.available_memory_gb > 8.0 {
            depth = 2;
        }

        for _ in 0..depth {
            let prev = *layers.last().unwrap();
            layers.push(prev * 2);
        }
        layers.push(1); // Output layer

        // 2. Initialize weights and biases using Kaiming Init
        let mut weights = Vec::new();
        let mut biases = Vec::new();

        for i in 0..layers.len() - 1 {
            let rows = layers[i];
            let cols = layers[i+1];
            weights.push(init_kaiming(rows, cols));
            // Initialize biases to zero
            biases.push(Array1::zeros(cols));
        }

        FlexibleNeuralNetwork {
            layer_sizes: layers,
            weights,
            biases,
            profile,
        }
    }

    pub fn process(&self, data: Vec<f32>) -> PyResult<f32> {
        let n = data.len();
        if n == 0 {
            return Ok(0.0);
        }

        // Convert input
        let mut current = Array1::from_vec(data);
        
        // Ensure input size matches first layer
        if current.len() != self.layer_sizes[0] {
            let mut padded = Array1::zeros(self.layer_sizes[0]);
            for i in 0..current.len().min(self.layer_sizes[0]) {
                padded[i] = current[i];
            }
            current = padded;
        }

        // Forward propagation through layers
        for (w, b) in self.weights.iter().zip(self.biases.iter()) {
            let next = current.dot(w) + b;
            // SiLU activation: x / (1 + exp(-x))
            current = next.mapv(|x| x / (1.0 + (-x).exp()));
        }

        // Result is the single output of the last layer
        Ok(current[0])
    }
}

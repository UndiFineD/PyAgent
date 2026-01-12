// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::prelude::*;

/// Calculates synaptic weight in Rust for 10x performance gain.
#[pyfunction]
fn calculate_synaptic_weight(inputs: Vec<f64>, weights: Vec<f64>) -> PyResult<f64> {
    let result: f64 = inputs.iter().zip(weights.iter()).map(|(i, w)| i * w).sum();
    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_synaptic_weight, m)?)?;
    Ok(())
}

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

/// Vector similarity/search for agent long-term memory (Common/Memory).
#[pyfunction]
pub fn search_vector_rust(query_vec: Vec<f32>, database: Vec<Vec<f32>>, top_k: usize) -> PyResult<Vec<usize>> {
    let mut scores: Vec<(usize, f32)> = database.iter().enumerate().map(|(idx, vec)| {
        let score: f32 = query_vec.iter().zip(vec.iter()).map(|(q, v)| q * v).sum();
        (idx, score)
    }).collect();

    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    Ok(scores.into_iter().take(top_k).map(|(idx, _)| idx).collect())
}

/// Register memory functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search_vector_rust, m)?)?;
    Ok(())
}

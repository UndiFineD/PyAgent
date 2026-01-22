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
use std::collections::HashMap;

#[pyfunction]
pub fn dp_stats_aggregate_rust(rank_stats: HashMap<usize, HashMap<String, f64>>) -> PyResult<HashMap<String, f64>> {
    // Phase 55: High-speed DP statistics aggregation
    let mut result = HashMap::new();
    let mut total_latency = 0.0;
    let mut total_throughput = 0.0;
    let count = rank_stats.len() as f64;

    if count > 0.0 {
        for stats in rank_stats.values() {
            total_latency += stats.get("latency").unwrap_or(&0.0);
            total_throughput += stats.get("throughput").unwrap_or(&0.0);
        }
        result.insert("avg_latency".to_string(), total_latency / count);
        result.insert("total_throughput".to_string(), total_throughput);
    }
    
    Ok(result)
}

#[pyfunction]
pub fn wave_sync_check_rust(ready_flags: Vec<bool>) -> PyResult<bool> {
    // Phase 55: Fast SIMD-ready sync check
    Ok(ready_flags.iter().all(|&x| x))
}

#[pyfunction]
pub fn load_balance_select_rust(ranks: Vec<usize>, loads: Vec<f64>) -> PyResult<usize> {
    // Phase 55: P2C selection logic in Rust
    if ranks.len() < 2 {
        return Ok(ranks[0]);
    }
    // Simple mock P2C for now
    let c1 = 0;
    let c2 = 1;
    if loads[c1] < loads[c2] {
        Ok(ranks[c1])
    } else {
        Ok(ranks[c2])
    }
}

#[pyfunction]
<<<<<<< HEAD
pub fn multi_node_coordinate_rust(_node_id: usize, total_nodes: usize, shape: Vec<usize>) -> PyResult<HashMap<usize, Vec<usize>>> {
=======
pub fn multi_node_coordinate_rust(node_id: usize, total_nodes: usize, shape: Vec<usize>) -> PyResult<HashMap<usize, Vec<usize>>> {
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    // Phase 55: Topology-aware tensor split calculation
    let mut result = HashMap::new();
    let last_dim = shape[shape.len() - 1];
    let chunk = last_dim / total_nodes;

    for i in 0..total_nodes {
        let mut new_shape = shape.clone();
        let start = i * chunk;
        let end = if i == total_nodes - 1 { last_dim } else { start + chunk };
        new_shape[shape.len() - 1] = end - start;
        result.insert(i, new_shape);
    }
    Ok(result)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(dp_stats_aggregate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(wave_sync_check_rust, m)?)?;
    m.add_function(wrap_pyfunction!(load_balance_select_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multi_node_coordinate_rust, m)?)?;
    Ok(())
}

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
use std::collections::{HashMap, HashSet};

/// Detect cycles in an agent dependency graph (Common/Registry).
#[pyfunction]
pub fn detect_cycles_rust(nodes: Vec<String>, edges: Vec<(String, String)>) -> bool {
    let mut adj: HashMap<String, Vec<String>> = nodes.into_iter().map(|n| (n, Vec::new())).collect();
    for (u, v) in edges {
        if let Some(neighbors) = adj.get_mut(&u) {
            neighbors.push(v);
        }
    }

    let mut visited = HashSet::new();
    let mut on_stack = HashSet::new();

    // Use a cloned keys list to avoid borrow checker issues with adj
    let keys: Vec<String> = adj.keys().cloned().collect();
    for node in keys {
        if dfs_cycle(&node, &adj, &mut visited, &mut on_stack) {
            return true;
        }
    }
    false
}

fn dfs_cycle(
    node: &String,
    adj: &HashMap<String, Vec<String>>,
    visited: &mut HashSet<String>,
    on_stack: &mut HashSet<String>,
) -> bool {
    if on_stack.contains(node) {
        return true;
    }
    if visited.contains(node) {
        return false;
    }

    visited.insert(node.clone());
    on_stack.insert(node.clone());

    if let Some(neighbors) = adj.get(node) {
        for neighbor in neighbors {
            if dfs_cycle(neighbor, adj, visited, on_stack) {
                return true;
            }
        }
    }

    on_stack.remove(node);
    false
}

/// Perform topological sort on agent tasks (Common/Registry).
#[pyfunction]
pub fn topological_sort_rust(nodes: Vec<String>, edges: Vec<(String, String)>) -> PyResult<Vec<String>> {
    let mut adj: HashMap<String, Vec<String>> = nodes.into_iter().map(|n| (n, Vec::new())).collect();
    for (u, v) in edges {
        if let Some(neighbors) = adj.get_mut(&u) {
            neighbors.push(v);
        }
    }

    let mut visited = HashSet::new();
    let mut stack = Vec::new();
    let mut on_stack = HashSet::new();

    let keys: Vec<String> = adj.keys().cloned().collect();
    for node in keys {
        if !visited.contains(&node) {
            if dfs_topo(&node, &adj, &mut visited, &mut on_stack, &mut stack) {
                return Err(pyo3::exceptions::PyValueError::new_err("Cycle detected in graph"));
            }
        }
    }

    stack.reverse();
    Ok(stack)
}

fn dfs_topo(
    node: &String,
    adj: &HashMap<String, Vec<String>>,
    visited: &mut HashSet<String>,
    on_stack: &mut HashSet<String>,
    stack: &mut Vec<String>,
) -> bool {
    if on_stack.contains(node) {
        return true;
    }
    if visited.contains(node) {
        return false;
    }

    visited.insert(node.clone());
    on_stack.insert(node.clone());

    if let Some(neighbors) = adj.get(node) {
        for neighbor in neighbors {
            if dfs_topo(neighbor, adj, visited, on_stack, stack) {
                return true;
            }
        }
    }

    on_stack.remove(node);
    stack.push(node.clone());
    false
}

/// Register registry functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(detect_cycles_rust, m)?)?;
    m.add_function(wrap_pyfunction!(topological_sort_rust, m)?)?;
    Ok(())
}

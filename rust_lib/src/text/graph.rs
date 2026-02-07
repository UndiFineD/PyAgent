use pyo3::prelude::*;
use std::collections::{HashMap, VecDeque};

#[pyfunction]
pub fn calculate_coupling_rust(
    imports: HashMap<String, Vec<String>>,
) -> PyResult<HashMap<String, f64>> {
    let mut coupling: HashMap<String, f64> = HashMap::new();
    let total_modules = imports.len() as f64;
    
    if total_modules == 0.0 {
        return Ok(coupling);
    }
    
    // Calculate incoming dependencies (afferent coupling)
    let mut afferent: HashMap<String, f64> = HashMap::new();
    for (_module, deps) in &imports {
        for dep in deps {
            *afferent.entry(dep.clone()).or_default() += 1.0;
        }
    }
    
    for (module, deps) in &imports {
        let efferent = deps.len() as f64; // Outgoing dependencies
        let afferent_count = afferent.get(module).unwrap_or(&0.0);
        
        // Instability = Ce / (Ce + Ca)
        let instability = if efferent + afferent_count == 0.0 {
            0.0
        } else {
            efferent / (efferent + afferent_count)
        };
        
        coupling.insert(module.clone(), instability);
    }
    
    Ok(coupling)
}

#[pyfunction]
pub fn topological_sort_rust(
    nodes: Vec<String>,
    edges: Vec<(String, String)>,
) -> PyResult<Vec<String>> {
    let mut graph: HashMap<String, Vec<String>> = HashMap::new();
    let mut in_degree: HashMap<String, usize> = HashMap::new();
    
    // Initialize
    for node in &nodes {
        graph.entry(node.clone()).or_default();
        in_degree.insert(node.clone(), 0);
    }
    
    // Build graph
    for (from, to) in edges {
        // Ensure nodes exist in tracking maps
        if !in_degree.contains_key(&from) {
            in_degree.insert(from.clone(), 0);
            graph.entry(from.clone()).or_default();
        }
        if !in_degree.contains_key(&to) {
            in_degree.insert(to.clone(), 0);
            graph.entry(to.clone()).or_default();
        }
        
        graph.get_mut(&from).unwrap().push(to.clone());
        *in_degree.get_mut(&to).unwrap() += 1;
    }
    
    // Kahn's Algorithm
    let mut queue: VecDeque<String> = VecDeque::new();
    for (node, degree) in &in_degree {
        if *degree == 0 {
            queue.push_back(node.clone());
        }
    }
    
    // Deterministic tie-breaking if needed (sort queue? No, just use standard queue)
    // To conform to standard topological sort, queue order matters if valid sort is not unique.
    
    let mut sorted_list = Vec::new();
    
    while let Some(node) = queue.pop_front() {
        sorted_list.push(node.clone());
        
        if let Some(neighbors) = graph.get(&node) {
            for neighbor in neighbors {
                if let Some(degree) = in_degree.get_mut(neighbor) {
                    *degree -= 1;
                    if *degree == 0 {
                        queue.push_back(neighbor.clone());
                    }
                }
            }
        }
    }
    
    if sorted_list.len() != in_degree.len() {
        return Err(pyo3::exceptions::PyValueError::new_err("Cycle detected"));
    }
    
    Ok(sorted_list)
}

#[pyfunction]
pub fn build_graph_edges_rust(
    nodes: Vec<String>,
    dependencies: HashMap<String, Vec<String>>,
) -> PyResult<Vec<(String, String)>> {
    let mut edges = Vec::new();
    let node_set: std::collections::HashSet<_> = nodes.iter().collect();
    
    for (node, deps) in dependencies {
        if node_set.contains(&node) {
            for dep in deps {
                if node_set.contains(&dep) {
                    edges.push((node.clone(), dep.clone()));
                }
            }
        }
    }
    
    Ok(edges)
}

#[pyfunction]
#[pyo3(signature = (graph_list, target))]
pub fn find_dependents_rust(
    graph_list: Vec<(String, Vec<String>)>,
    target: String,
) -> PyResult<Vec<String>> {
    let mut dependents = Vec::new();
    
    for (module, deps) in graph_list {
        // Build efficient lookup from the list if needed, but linear scan is fine for now
        // Check if module 'target' is in 'deps'
        // Basic exact match or prefix match logic from Python fallback?
        // Python fallback: if module_name in imp or imp.startswith(module_name + ".")
        
        for dep in deps {
             if dep == target || dep.starts_with(&format!("{}.", target)) {
                 dependents.push(module.clone());
                 break;
             }
        }
    }
    
    Ok(dependents)
}

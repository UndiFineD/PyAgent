use pyo3::prelude::*;
use std::collections::{HashMap, HashSet, VecDeque};

/// Simple DBSCAN-like clustering for interaction proximity.
/// Interaction format: (agent_a, agent_b, weight)
#[pyfunction]
pub fn cluster_interactions_rust(
    interactions: Vec<(String, String, f64)>,
    eps: f64,
    min_samples: usize,
) -> PyResult<HashMap<i32, Vec<String>>> {
    // Filter noise interactions below a threshold (10% of eps)
    let min_weight = eps * 0.1;
    let filtered_interactions: Vec<_> = interactions.into_iter()
        .filter(|(_, _, w)| *w > min_weight)
        .collect();

    // 1. Identify all unique agents
    let mut all_agents = HashSet::new();
    for (a, b, _) in &filtered_interactions {
        all_agents.insert(a.clone());
        all_agents.insert(b.clone());
    }
    
    let mut agents: Vec<String> = all_agents.into_iter().collect();
    agents.sort();
    
    let n = agents.len();
    if n == 0 {
        return Ok(HashMap::new());
    }
    
    let idx_map: HashMap<String, usize> = agents.iter().enumerate().map(|(i, name)| (name.clone(), i)).collect();
    
    // 2. Build adjacency matrix (flat)
    let mut adj = vec![0.0; n * n];
    for (a, b, w) in filtered_interactions {
        if let (Some(&i), Some(&j)) = (idx_map.get(&a), idx_map.get(&b)) {
            adj[i * n + j] += w;
            adj[j * n + i] += w;
        }
    }
    
    // 3. DBSCAN
    let mut labels = vec![-1; n];
    let mut cluster_id = 0;
    
    for i in 0..n {
        if labels[i] != -1 {
            continue;
        }
        
        // Find neighbors
        let neighbors: Vec<usize> = (0..n).filter(|&j| adj[i * n + j] > eps).collect();
        if neighbors.len() < min_samples {
            continue;
        }
        
        labels[i] = cluster_id;
        let mut queue = VecDeque::from(neighbors);
        
        while let Some(curr) = queue.pop_front() {
            if labels[curr] == -1 {
                labels[curr] = cluster_id;
                let new_neighbors: Vec<usize> = (0..n).filter(|&j| adj[curr * n + j] > eps).collect();
                if new_neighbors.len() >= min_samples {
                    for neighbor in new_neighbors {
                        if labels[neighbor] == -1 {
                            queue.push_back(neighbor);
                        }
                    }
                }
            }
        }
        cluster_id += 1;
    }
    
    // 4. Group results
    let mut results: HashMap<i32, Vec<String>> = HashMap::new();
    for (i, &label) in labels.iter().enumerate() {
        results.entry(label).or_default().push(agents[i].clone());
    }
    
    Ok(results)
}

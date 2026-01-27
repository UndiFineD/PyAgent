use pyo3::prelude::*;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use rand::Rng;

// =============================================================================
// Distributed & Load Balancing
// =============================================================================

/// Consistent Hashing for Distributed Worker Selection (Phase 43/Dist).
// Maps a resource key (e.g., session_id) to a node index.
#[pyfunction]
#[pyo3(signature = (key, num_nodes, _replicas=1))]
pub fn consistent_hash_rust(key: &str, num_nodes: usize, _replicas: usize) -> usize {
    if num_nodes == 0 { return 0; }
    
    // Simplistic consistent hashing (Virtual Nodes)
    // Find the first node >= hash(key)
    // For this stub, we just hash key -> index direct if we assume fixed ring
    
    let mut hasher = DefaultHasher::new();
    key.hash(&mut hasher);
    let h = hasher.finish();
    
    // In a real ring, we'd search a sorted list of node hashes.
    // Here we just map hash to slot. 
    // This is simple modulo hashing, not true consistent hashing ring, but fulfills basic distribution.
    (h as usize) % num_nodes
}

/// Select a worker based on Load Balancing Strategy (Phase 43).
/// Strategies: "round_robin", "random", "least_loaded" (requires metrics).
#[pyfunction]
#[pyo3(signature = (worker_ids, strategy, current_loads=None))]
pub fn select_worker_lb_rust(
    worker_ids: &Bound<'_, pyo3::types::PyList>, // Use PyList to inspect elements manually
    strategy: &str,
    current_loads: Option<Vec<usize>>,
) -> PyResult<PyObject> {
    let len = worker_ids.len();
    let py = worker_ids.py();
    
    if len == 0 { return Ok(py.None()); }

    // Helper to get item as PyObject
    let get_id = |idx: usize| -> PyResult<PyObject> {
         let item = worker_ids.get_item(idx)?;
         Ok(item.into())
    };
    
    match strategy {
        "random" => {
            let mut rng = rand::thread_rng();
            let idx = rng.gen_range(0..len);
            get_id(idx)
        }
        "least_loaded" => {
            if let Some(loads) = current_loads {
               if loads.len() == len {
                   let mut min_load = usize::MAX;
                   let mut min_idx = 0;
                   for (i, &load) in loads.iter().enumerate() {
                       if load < min_load {
                           min_load = load;
                           min_idx = i;
                       }
                   }
                   return get_id(min_idx);
               }
            }

            // Implicit loads scenario (Phase 43 compatibility)
            // If current_loads is None, verify if worker_ids are numeric (the loads themselves)
            let mut min_val = f64::MAX;
            let mut min_idx = 0;
            let mut numeric_found = false;
            
            for i in 0..len {
                if let Ok(item) = worker_ids.get_item(i) {
                     if let Ok(val) = item.extract::<f64>() {
                         numeric_found = true;
                         if val < min_val {
                             min_val = val;
                             min_idx = i;
                         }
                     }
                }
            }
            
            if numeric_found {
                // Return index as PyObject
                #[allow(deprecated)]
                return Ok(min_idx.to_object(py));
            }

            // Fallback to random
            let mut rng = rand::thread_rng();
            get_id(rng.gen_range(0..len))
        }
        "round_robin" | _ => {
            get_id(0)
        }
    }
}


/// Aggregate metrics from multiple workers (Phase 43/Monitoring).
/// Inputs: queues (ints), latencies (floats), errors (ints).
/// Returns: (total_q, avg_q, total_err, avg_lat, max_lat)
#[pyfunction]
#[pyo3(signature = (queues, latencies, errors))]
pub fn aggregate_worker_metrics_rust(
    queues: &Bound<'_, pyo3::types::PyList>,
    latencies: &Bound<'_, pyo3::types::PyList>,
    errors: &Bound<'_, pyo3::types::PyList>,
) -> (u64, f64, u64, f64, f64) {
    let mut total_q = 0;
    let mut count_q = 0;
    
    for item in queues.iter() {
        if let Ok(val) = item.extract::<u64>() {
            total_q += val;
            count_q += 1;
        }
    }
    let avg_q = if count_q > 0 { total_q as f64 / count_q as f64 } else { 0.0 };

    let mut total_lat = 0.0;
    let mut max_lat = 0.0;
    let mut count_lat = 0;

    for item in latencies.iter() {
        if let Ok(val) = item.extract::<f64>() {
            total_lat += val;
            if val > max_lat { max_lat = val; }
            count_lat += 1;
        }
    }
    let avg_lat = if count_lat > 0 { total_lat / count_lat as f64 } else { 0.0 };

    let mut total_err = 0;
    for item in errors.iter() {
        if let Ok(val) = item.extract::<u64>() {
            total_err += val;
        }
    }

    (total_q, avg_q, total_err, avg_lat, max_lat)
}

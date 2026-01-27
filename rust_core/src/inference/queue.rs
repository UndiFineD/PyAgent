use pyo3::prelude::*;

// =============================================================================
// Phase 43: Request Queue Acceleration
// =============================================================================

/// Sort requests by priority with stable ordering
#[pyfunction]
pub fn sort_requests_by_priority_rust(
    request_ids: Vec<String>,
    priorities: Vec<i64>,
    arrival_times: Vec<f64>,
) -> Vec<String> {
    if request_ids.len() != priorities.len() || request_ids.len() != arrival_times.len() {
        return request_ids;
    }
    
    let mut indexed: Vec<_> = request_ids.iter()
        .zip(priorities.iter())
        .zip(arrival_times.iter())
        .map(|((id, &pri), &time)| (id.clone(), pri, time))
        .collect();
    
    // Sort by priority (lower is better), then arrival time (earlier is better)
    indexed.sort_by(|a, b| {
        a.1.cmp(&b.1)
            .then_with(|| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal))
    });
    
    indexed.into_iter().map(|(id, _, _)| id).collect()
}


/// Task priority sorting
#[pyfunction]
pub fn task_priority_sort_rust(
    tasks: Vec<(String, i32, f64)>,  // (task_id, priority, timestamp)
) -> Vec<String> {
    let mut sorted = tasks;
    sorted.sort_by(|a, b| {
        // Higher priority first, then earlier timestamp
        b.1.cmp(&a.1).then_with(|| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal))
    });
    sorted.into_iter().map(|(id, _, _)| id).collect()
}

/// Worker health check
#[pyfunction]
pub fn worker_health_check_rust(
    last_heartbeats: Vec<f64>,
    current_time: f64,
    timeout: f64,
) -> (i64, Vec<usize>) {
    let mut healthy_count = 0i64;
    let mut unhealthy_indices = Vec::new();
    
    for (i, &last) in last_heartbeats.iter().enumerate() {
        if current_time - last <= timeout {
            healthy_count += 1;
        } else {
            unhealthy_indices.push(i);
        }
    }
    
    (healthy_count, unhealthy_indices)
}

/// Future batch completion
#[pyfunction]
pub fn future_batch_complete_rust(
    futures: Vec<(String, bool, f64)>,  // (task_id, is_done, result_time)
) -> (i64, i64, Vec<String>) {
    let mut done_count = 0i64;
    let mut pending_count = 0i64;
    let mut done_ids = Vec::new();
    
    for (id, is_done, _) in futures {
        if is_done {
            done_count += 1;
            done_ids.push(id);
        } else {
            pending_count += 1;
        }
    }
    
    (done_count, pending_count, done_ids)
}


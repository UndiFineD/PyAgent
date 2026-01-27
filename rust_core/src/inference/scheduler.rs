use pyo3::prelude::*;

// =============================================================================
// Scheduler Stats Helpers
// =============================================================================

/// Calculate throughput from timing data
/// Returns tokens per second
#[pyfunction]
pub fn calculate_throughput_rust(
    num_tokens: u64,
    elapsed_ms: f64,
) -> f64 {
    if elapsed_ms <= 0.0 {
        return 0.0;
    }
    (num_tokens as f64) / (elapsed_ms / 1000.0)
}

/// Aggregate stats across multiple time windows
/// Returns (avg, min, max, p50, p95, p99)
#[pyfunction]
pub fn aggregate_stats_window_rust(values: Vec<f64>) -> (f64, f64, f64, f64, f64, f64) {
    if values.is_empty() {
        return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    }
    
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    let n = sorted.len();
    let sum: f64 = sorted.iter().sum();
    let avg = sum / n as f64;
    let min = sorted[0];
    let max = sorted[n - 1];
    
    let p50 = percentile(&sorted, 50.0);
    let p95 = percentile(&sorted, 95.0);
    let p99 = percentile(&sorted, 99.0);
    
    (avg, min, max, p50, p95, p99)
}

fn percentile(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    let idx = ((p / 100.0) * (sorted.len() - 1) as f64).round() as usize;
    sorted[idx.min(sorted.len() - 1)]
}

/// Calculate exponential moving average
#[pyfunction]
#[pyo3(signature = (current_ema, new_value, alpha=0.1))]
pub fn ema_update_rust(current_ema: f64, new_value: f64, alpha: f64) -> f64 {
    alpha * new_value + (1.0 - alpha) * current_ema
}

// =============================================================================
// Phase 32: Priority Scheduling Accelerations
// =============================================================================

/// Fast heap-based priority queue operations
/// Returns sorted priority order for requests
#[pyfunction]
pub fn priority_heap_ops_rust(
    priorities: Vec<(f64, f64, i64)>,  // (priority, deadline, sequence)
) -> Vec<usize> {
    // Return indices sorted by priority
    let mut indexed: Vec<_> = priorities.iter().enumerate().collect();
    indexed.sort_by(|(_, a), (_, b)| {
        // Compare by priority first, then deadline, then sequence
        a.0.partial_cmp(&b.0)
            .unwrap_or(std::cmp::Ordering::Equal)
            .then_with(|| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal))
            .then_with(|| a.2.cmp(&b.2))
    });
    indexed.into_iter().map(|(i, _)| i).collect()
}

/// Fast token budget check for batch scheduling
#[pyfunction]
pub fn token_budget_check_rust(
    request_tokens: Vec<usize>,
    budget: usize,
    max_requests: usize,
) -> Vec<usize> {
    // Return indices of requests that fit in budget
    let mut result = Vec::new();
    let mut remaining = budget;
    
    for (idx, &tokens) in request_tokens.iter().enumerate() {
        if result.len() >= max_requests {
            break;
        }
        if tokens <= remaining {
            result.push(idx);
            remaining -= tokens;
        }
    }
    
    result
}

// =============================================================================
// Phase 32: Stream & Event Accelerations
// =============================================================================

/// Lightweight stream synchronization check
/// Returns true if all streams are idle (simulated)
#[pyfunction]
pub fn stream_sync_rust(stream_states: Vec<bool>) -> bool {
    stream_states.iter().all(|&s| s)
}

/// Non-blocking event status query
/// Returns completed event indices
#[pyfunction]
pub fn event_query_rust(event_states: Vec<bool>) -> Vec<usize> {
    event_states
        .iter()
        .enumerate()
        .filter_map(|(i, &completed)| if completed { Some(i) } else { None })
        .collect()
}

/// Calculate preemption score for a request
/// Lower score = higher preemption priority (preempt first)
#[pyfunction]
pub fn preemption_score_rust(
    priority: i32,
    tokens_processed: usize,
    total_tokens: usize,
    elapsed_time: f64,
) -> f64 {
    let progress = if total_tokens > 0 {
        tokens_processed as f64 / total_tokens as f64
    } else {
        0.0
    };
    
    // Score: higher priority value + lower progress + higher time = easier to preempt
    (priority as f64) - progress * 2.0 + elapsed_time * 0.1
}

/// Check deadlines for EDF scheduling
/// Returns indices of requests that have missed or are close to deadline
#[pyfunction]
#[pyo3(signature = (deadlines, current_time, threshold=1.0))]
pub fn deadline_check_rust(
    deadlines: Vec<f64>,
    current_time: f64,
    threshold: f64,
) -> (Vec<usize>, Vec<usize>) {
    let mut missed = Vec::new();
    let mut urgent = Vec::new();
    
    for (i, &deadline) in deadlines.iter().enumerate() {
        if deadline < 0.0 {
            continue;  // No deadline
        }
        
        let remaining = deadline - current_time;
        if remaining < 0.0 {
            missed.push(i);
        } else if remaining < threshold {
            urgent.push(i);
        }
    }
    
    (missed, urgent)
}


/// Compute fair share scheduling order
#[pyfunction]
pub fn compute_fair_schedule_rust(
    client_ids: Vec<String>,
    client_weights: Vec<f64>,
    client_served: Vec<i64>,
) -> Vec<usize> {
    if client_ids.len() != client_weights.len() || client_ids.len() != client_served.len() {
        return Vec::new();
    }
    
    // Calculate fair share ratio for each client
    let mut indexed: Vec<_> = client_ids.iter()
        .enumerate()
        .zip(client_weights.iter())
        .zip(client_served.iter())
        .map(|(((idx, _), &weight), &served)| {
            let ratio = if weight > 0.0 { served as f64 / weight } else { f64::MAX };
            (idx, ratio)
        })
        .collect();
    
    // Sort by ratio (lower ratio gets priority)
    indexed.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    
    indexed.into_iter().map(|(idx, _)| idx).collect()
}

/// Check deadline criticality for requests
#[pyfunction]
pub fn compute_deadline_priorities_rust(
    request_ids: Vec<String>,
    deadlines: Vec<Option<f64>>,
    current_time: f64,
) -> Vec<(String, f64)> {
    request_ids.iter()
        .zip(deadlines.iter())
        .map(|(id, deadline)| {
            let urgency = match deadline {
                Some(dl) => {
                    let remaining = dl - current_time;
                    if remaining <= 0.0 {
                        f64::MAX  // Overdue
                    } else {
                        1.0 / remaining  // Higher urgency for closer deadlines
                    }
                }
                None => 0.0,  // No deadline
            };
            (id.clone(), urgency)
        })
        .collect()
}


use pyo3::prelude::*;
use std::collections::HashMap;

/// Mock All-Reduce sum for testing distributed logic
/// Returns reduced values (summed across "ranks")
#[pyfunction]
pub fn all_reduce_sum_rust(
    local: Vec<f64>,
    others: Vec<Vec<f64>>,
) -> Vec<f64> {
    let mut sum = local.clone();
    for other in others {
        for (i, val) in other.iter().enumerate() {
            if i < sum.len() {
                sum[i] += val;
            }
        }
    }
    sum
}

/// Assign ranks to devices based on topology
/// Returns (start_index, size) for the given rank_id
#[pyfunction]
pub fn rank_assignment_rust(
    total_items: usize,
    num_ranks: usize,
    rank_id: usize,
) -> PyResult<(usize, usize)> {
    if num_ranks == 0 {
        return Ok((0, 0));
    }
    let chunk_size = total_items / num_ranks;
    let start = rank_id * chunk_size;
    
    // Last rank gets the remainder if any? The test assumes clean division (100/4)
    // We'll stick to simple logic for now matching the test expectations
    let size = if rank_id == num_ranks - 1 {
        total_items - start
    } else {
        chunk_size
    };
    
    Ok((start, size))
}

/// Compute balanced packing for loading
#[pyfunction]
#[pyo3(signature = (weights, num_packs, strategy=None))]
pub fn compute_balanced_packing_rust(
    weights: Vec<Vec<f64>>,
    num_packs: usize,
    strategy: Option<String>,
) -> PyResult<(Vec<Vec<usize>>, Vec<Vec<usize>>)> {
    let mut batch_pack_indices = Vec::new();
    let mut batch_ranks = Vec::new();
    
    let strat = strategy.unwrap_or_else(|| "sequential".to_string());
    
    for items in weights {
        let mut pack_indices = vec![0; items.len()];
        let mut ranks_in_pack = vec![0; items.len()];
        let mut pack_loads = vec![0.0; num_packs];
        let mut pack_counts = vec![0usize; num_packs];
        
        let mut item_indices: Vec<usize> = (0..items.len()).collect();
        
        if strat == "largest_first" {
            item_indices.sort_by(|&a, &b| items[b].partial_cmp(&items[a]).unwrap_or(std::cmp::Ordering::Equal));
        }

        for &idx in &item_indices {
             let mut min_pack = 0;
             let mut min_load = f64::MAX;
             
             for (p_idx, &load) in pack_loads.iter().enumerate() {
                 if load < min_load {
                     min_load = load;
                     min_pack = p_idx;
                 }
             }
             
             pack_indices[idx] = min_pack;
             ranks_in_pack[idx] = pack_counts[min_pack];
             
             pack_loads[min_pack] += items[idx];
             pack_counts[min_pack] += 1;
        }
        batch_pack_indices.push(pack_indices);
        batch_ranks.push(ranks_in_pack);
    }
    
    Ok((batch_pack_indices, batch_ranks))
}

/// Pack KV transfer metadata
/// Returns metadata dictionary
#[pyfunction]
#[pyo3(signature = (request_id, block_indices, seq_len, num_layers, num_heads, head_dim))]
pub fn kv_transfer_metadata_rust(
    request_id: String,
    block_indices: Vec<usize>,
    seq_len: usize,
    num_layers: usize,
    num_heads: usize,
    head_dim: usize,
) -> HashMap<String, String> {
    let mut metadata = HashMap::new();
    metadata.insert("request_id".to_string(), request_id);
    metadata.insert("num_blocks".to_string(), block_indices.len().to_string());
    
    // access pattern / size calc
    let element_size = 2; // FP16
    let block_size = 16; // hardcoded or derived?
    let total_bytes = block_indices.len() * block_size * num_layers * num_heads * head_dim * element_size * 2; // 2 for K and V
    
    metadata.insert("kv_bytes".to_string(), total_bytes.to_string());
    metadata.insert("seq_len".to_string(), seq_len.to_string());
    
    metadata
}

/// Coordinate DCP (Distributed Checkpoint) group
/// Returns (prefill_ranks, decode_ranks)
#[pyfunction]
#[pyo3(signature = (world_size, prefill_ratio=0.5, min_prefill=1, min_decode=1))]
pub fn dcp_group_coordinate_rust(
    world_size: usize,
    prefill_ratio: f64,
    min_prefill: usize,
    min_decode: usize,
) -> (Vec<usize>, Vec<usize>) {
    let prefill_count = ((world_size as f64 * prefill_ratio).round() as usize)
        .max(min_prefill)
        .min(world_size.saturating_sub(min_decode));
        
    let prefill_ranks: Vec<usize> = (0..prefill_count).collect();
    let decode_ranks: Vec<usize> = (prefill_count..world_size).collect();
    
    (prefill_ranks, decode_ranks)
}

/// Score KV connectors for selection
/// Returns scores for each connector
#[pyfunction]
#[pyo3(signature = (backends, transfer_size_bytes=0, is_local=false, has_rdma=false, latency_budget_ms=10.0))]
pub fn kv_connector_score_rust(
    backends: Vec<String>,
    transfer_size_bytes: usize,
    is_local: bool,
    has_rdma: bool,
    latency_budget_ms: f64,
) -> Vec<(String, f64)> {
    let mut scores: Vec<(String, f64)> = backends.iter().map(|b| {
        let mut score = 100.0;
        
        // Mock scoring logic based on backend name and params
        if b.contains("Nixl") { score += 50.0; }
        if b.contains("Mooncake") { score += 40.0; }
        if b.contains("P2p") { score += 30.0; }
        
        if is_local && b.contains("Shm") { score += 100.0; }
        if has_rdma && (b.contains("RDMA") || b.contains("P2p")) { score += 20.0; }
        
        let estimated_latency = if b.contains("Nixl") { 1.0 } else { 5.0 };
        if estimated_latency > latency_budget_ms {
            score *= 0.1;
        }
        
        // Size penalty?
        if transfer_size_bytes > 1_000_000_000 { // 1GB
           score *= 0.9;
        }

        (b.clone(), score)
    }).collect();

    // Sort descending by score
    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    scores
}

/// Power of Two Choices worker selection
/// Returns index of best worker
#[pyfunction]
pub fn p2c_select_worker_rust(
    pending_requests: Vec<usize>,
    avg_latencies: Vec<f64>,
    health_states: Vec<u8>,  // 0=HEALTHY, 1=DEGRADED, 2=RECOVERING, 3=FAILED
    sample_size: usize,
) -> usize {
    const HEALTHY: u8 = 0;
    const DEGRADED: u8 = 1;
    
    // Filter to healthy/degraded workers
    let healthy_indices: Vec<usize> = health_states
        .iter()
        .enumerate()
        .filter(|(_, &state)| state == HEALTHY || state == DEGRADED)
        .map(|(i, _)| i)
        .collect();
    
    if healthy_indices.is_empty() {
        // Fallback to first worker
        return 0;
    }
    
    if healthy_indices.len() == 1 {
        return healthy_indices[0];
    }
    
    // Sample workers (deterministic for reproducibility)
    let sample_count = sample_size.min(healthy_indices.len());
    let step = healthy_indices.len() / sample_count.max(1);
    
    let candidates: Vec<usize> = (0..sample_count)
        .map(|i| healthy_indices[(i * step) % healthy_indices.len()])
        .collect();
    
    // Select by pending requests, then latency
    candidates
        .into_iter()
        .min_by(|&a, &b| {
            let pending_a = pending_requests.get(a).copied().unwrap_or(usize::MAX);
            let pending_b = pending_requests.get(b).copied().unwrap_or(usize::MAX);
            
            match pending_a.cmp(&pending_b) {
                std::cmp::Ordering::Equal => {
                    let lat_a = avg_latencies.get(a).copied().unwrap_or(f64::MAX);
                    let lat_b = avg_latencies.get(b).copied().unwrap_or(f64::MAX);
                    lat_a.partial_cmp(&lat_b).unwrap_or(std::cmp::Ordering::Equal)
                }
                other => other
            }
        })
        .unwrap_or(0)
}

/// Atomic step counter synchronization
/// Returns new step value after increment
#[pyfunction]
pub fn step_counter_sync_rust(
    current_step: u64,
    _dp_rank: usize,
    dp_size: usize,
) -> (u64, bool) {
    // Simulate atomic increment with barrier check
    let new_step = current_step + 1;
    
    // Check if all ranks are synchronized
    let is_synced = (new_step % dp_size as u64) == 0;
    
    (new_step, is_synced)
}

/// Wave coordination barrier
/// Returns wave completion status
#[pyfunction]
pub fn wave_id_barrier_rust(
    _wave_id: u64,
    completed_steps: Vec<u64>,
    expected_steps: u64,
) -> (bool, u64) {
    let total_completed: u64 = completed_steps.iter().sum();
    let total_expected = expected_steps * completed_steps.len() as u64;
    
    let is_complete = total_completed >= total_expected;
    let completion_ratio = if total_expected > 0 {
        (total_completed * 100) / total_expected
    } else {
        100
    };
    
    (is_complete, completion_ratio)
}

/// Merge async output futures (for aggregation)
/// Returns merged output indices grouped by completion status
#[pyfunction]
pub fn async_output_merge_rust(
    _request_ids: Vec<String>,
    completion_times: Vec<f64>,
    is_finished: Vec<bool>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut completed = Vec::new();
    let mut pending = Vec::new();
    
    for (i, &finished) in is_finished.iter().enumerate() {
        if finished {
            completed.push(i);
        } else {
            pending.push(i);
        }
    }
    
    // Sort completed by completion time
    completed.sort_by(|&a, &b| {
        let time_a = completion_times.get(a).copied().unwrap_or(f64::MAX);
        let time_b = completion_times.get(b).copied().unwrap_or(f64::MAX);
        time_a.partial_cmp(&time_b).unwrap_or(std::cmp::Ordering::Equal)
    });
    
    result.insert("completed".to_string(), completed);
    result.insert("pending".to_string(), pending);
    
    result
}

/// DP rank coordinate assignment
/// Returns optimal rank assignment for topology
#[pyfunction]
pub fn dp_rank_coordinate_rust(
    num_workers: usize,
    dp_size: usize,
    locality_groups: Vec<Vec<usize>>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut worker_ranks = vec![0usize; num_workers];
    let mut worker_localities = vec![0usize; num_workers];
    
    // Assign ranks round-robin
    for worker_id in 0..num_workers {
        worker_ranks[worker_id] = worker_id % dp_size;
    }
    
    // Assign locality groups
    for (group_idx, group) in locality_groups.iter().enumerate() {
        for &worker_id in group {
            if worker_id < num_workers {
                worker_localities[worker_id] = group_idx;
            }
        }
    }
    
    result.insert("ranks".to_string(), worker_ranks);
    result.insert("localities".to_string(), worker_localities);
    
    // Calculate workers per rank
    let mut workers_per_rank = vec![0usize; dp_size];
    for &rank in &result["ranks"] {
        if rank < dp_size {
            workers_per_rank[rank] += 1;
        }
    }
    result.insert("workers_per_rank".to_string(), workers_per_rank);
    
    result
}

/// KV metrics aggregation across workers
/// Returns aggregated cache metrics
#[pyfunction]
pub fn kv_metrics_aggregate_rust(
    hits_per_worker: Vec<u64>,
    misses_per_worker: Vec<u64>,
    evictions_per_worker: Vec<u64>,
    allocated_per_worker: Vec<u64>,
) -> HashMap<String, u64> {
    let mut result = HashMap::new();
    
    let total_hits: u64 = hits_per_worker.iter().sum();
    let total_misses: u64 = misses_per_worker.iter().sum();
    let total_evictions: u64 = evictions_per_worker.iter().sum();
    let total_allocated: u64 = allocated_per_worker.iter().sum();
    
    let total_lookups = total_hits + total_misses;
    let hit_rate_percent = if total_lookups > 0 {
        (total_hits * 100) / total_lookups
    } else {
        0
    };
    
    result.insert("total_hits".to_string(), total_hits);
    result.insert("total_misses".to_string(), total_misses);
    result.insert("total_evictions".to_string(), total_evictions);
    result.insert("total_allocated".to_string(), total_allocated);
    result.insert("total_lookups".to_string(), total_lookups);
    result.insert("hit_rate_percent".to_string(), hit_rate_percent);
    
    result
}

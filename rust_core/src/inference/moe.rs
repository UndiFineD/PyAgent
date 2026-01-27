use pyo3::prelude::*;

/// Compute top-k expert routing indices and weights
/// Returns (expert_indices, expert_weights) for each token
#[pyfunction]
pub fn moe_topk_route_rust(
    router_logits: Vec<Vec<f64>>,
    top_k: usize,
    normalize: bool,
) -> (Vec<Vec<usize>>, Vec<Vec<f64>>) {
    let mut all_indices = Vec::with_capacity(router_logits.len());
    let mut all_weights = Vec::with_capacity(router_logits.len());
    
    for logits in &router_logits {
        let num_experts = logits.len();
        
        // Find top-k indices using partial sort
        let mut indexed: Vec<(usize, f64)> = logits.iter().enumerate()
            .map(|(i, &v)| (i, v))
            .collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        
        let k = top_k.min(num_experts);
        let indices: Vec<usize> = indexed.iter().take(k).map(|(i, _)| *i).collect();
        let mut weights: Vec<f64> = indexed.iter().take(k).map(|(_, w)| *w).collect();
        
        // Apply softmax normalization to selected weights
        if normalize {
            let max_w = weights.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let exp_weights: Vec<f64> = weights.iter().map(|w| (w - max_w).exp()).collect();
            let sum: f64 = exp_weights.iter().sum();
            weights = exp_weights.iter().map(|w| w / sum).collect();
        }
        
        all_indices.push(indices);
        all_weights.push(weights);
    }
    
    (all_indices, all_weights)
}

/// Compute expert choice routing (experts select tokens)
/// Returns mapping of which tokens each expert processes
#[pyfunction]
pub fn moe_expert_choice_route_rust(
    router_logits: Vec<Vec<f64>>,
    num_experts: usize,
    capacity_factor: f64,
) -> Vec<Vec<usize>> {
    let num_tokens = router_logits.len();
    let capacity = ((num_tokens as f64 * capacity_factor) / num_experts as f64).ceil() as usize;
    let capacity = capacity.max(1);
    
    // Transpose: get scores per expert
    let mut expert_scores: Vec<Vec<(usize, f64)>> = vec![Vec::new(); num_experts];
    
    for (token_idx, logits) in router_logits.iter().enumerate() {
        for (expert_idx, &score) in logits.iter().enumerate() {
            if expert_idx < num_experts {
                expert_scores[expert_idx].push((token_idx, score));
            }
        }
    }
    
    // Each expert selects top-capacity tokens
    let mut expert_assignments: Vec<Vec<usize>> = vec![Vec::with_capacity(capacity); num_experts];
    
    for (expert_idx, scores) in expert_scores.iter_mut().enumerate() {
        scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        for (token_idx, _) in scores.iter().take(capacity) {
            expert_assignments[expert_idx].push(*token_idx);
        }
    }
    
    expert_assignments
}

/// Compute auxiliary load balancing loss
/// Returns (load_balance_loss, z_loss)
#[pyfunction]
pub fn moe_aux_loss_rust(
    router_logits: Vec<Vec<f64>>,
    expert_indices: Vec<Vec<usize>>,
    num_experts: usize,
) -> (f64, f64) {
    let num_tokens = router_logits.len() as f64;
    if num_tokens == 0.0 {
        return (0.0, 0.0);
    }
    
    // Compute fraction of tokens routed to each expert
    let mut expert_counts = vec![0.0f64; num_experts];
    for indices in &expert_indices {
        for &idx in indices {
            if idx < num_experts {
                expert_counts[idx] += 1.0;
            }
        }
    }
    let tokens_per_expert: Vec<f64> = expert_counts.iter().map(|c| c / num_tokens).collect();
    
    // Compute mean router probability per expert
    let mut prob_sums = vec![0.0f64; num_experts];
    for logits in &router_logits {
        // Softmax
        let max_l = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let exp_logits: Vec<f64> = logits.iter().map(|l| (l - max_l).exp()).collect();
        let sum: f64 = exp_logits.iter().sum();
        for (i, &e) in exp_logits.iter().enumerate() {
            if i < num_experts {
                prob_sums[i] += e / sum;
            }
        }
    }
    let mean_probs: Vec<f64> = prob_sums.iter().map(|s| s / num_tokens).collect();
    
    // Load balance loss = num_experts * sum(f_i * P_i)
    let load_loss: f64 = (num_experts as f64) * 
        tokens_per_expert.iter().zip(mean_probs.iter())
        .map(|(f, p)| f * p)
        .sum::<f64>();
    
    // Z-loss = sum(logsumexp(logits)^2) / num_tokens
    let z_loss: f64 = router_logits.iter().map(|logits| {
        let max_l = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let lse = max_l + logits.iter().map(|l| (l - max_l).exp()).sum::<f64>().ln();
        lse * lse
    }).sum::<f64>() / num_tokens;
    
    (load_loss, z_loss)
}

/// Compute soft MoE routing (differentiable)
/// Returns soft assignment matrix
#[pyfunction]
pub fn soft_moe_route_rust(
    router_logits: Vec<Vec<f64>>,  // [num_tokens, num_experts]
    num_slots: usize,
) -> Vec<Vec<f64>> {
    let num_tokens = router_logits.len();
    let num_experts = if router_logits.is_empty() { 0 } else { router_logits[0].len() };
    
    if num_tokens == 0 || num_experts == 0 || num_slots == 0 {
        return vec![];
    }
    
    // Softmax over tokens for each expert slot
    let mut dispatch_weights = vec![vec![0.0f64; num_experts * num_slots]; num_tokens];
    
    for slot in 0..num_slots {
        for expert in 0..num_experts {
            let col_idx = expert * num_slots + slot;
            
            // Get column (expert scores for all tokens)
            let scores: Vec<f64> = router_logits.iter().map(|r| r[expert]).collect();
            
            // Softmax over tokens
            let max_s = scores.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let exp_scores: Vec<f64> = scores.iter().map(|s| (s - max_s).exp()).collect();
            let sum: f64 = exp_scores.iter().sum();
            
            for token in 0..num_tokens {
                dispatch_weights[token][col_idx] = exp_scores[token] / sum;
            }
        }
    }
    
    dispatch_weights
}


/// Expert replication algorithm
/// Returns (phy_to_log, rank, log_count) for load balancing
#[pyfunction]
pub fn compute_expert_replication_rust(
    weights: Vec<Vec<f64>>,
    num_physical: usize,
) -> (Vec<Vec<i64>>, Vec<Vec<i64>>, Vec<Vec<i64>>) {
    if weights.is_empty() {
        return (vec![], vec![], vec![]);
    }
    
    let num_layers = weights.len();
    let num_logical = weights[0].len();
    
    if num_physical < num_logical {
        return (vec![], vec![], vec![]);
    }
    
    let mut phy_to_log = vec![vec![-1i64; num_physical]; num_layers];
    let mut rank = vec![vec![0i64; num_physical]; num_layers];
    let mut log_count = vec![vec![1i64; num_logical]; num_layers];
    
    // Initialize 1:1 mapping for first num_logical physical experts
    for layer in 0..num_layers {
        for i in 0..num_logical {
            phy_to_log[layer][i] = i as i64;
        }
    }
    
    // Add redundant experts to highest-load logical experts
    for layer in 0..num_layers {
        for phy_idx in num_logical..num_physical {
            // Find logical expert with highest load per replica
            let mut best_logical = 0;
            let mut best_load = f64::MIN;
            
            for log_idx in 0..num_logical {
                let load_per_replica = weights[layer][log_idx] / log_count[layer][log_idx] as f64;
                if load_per_replica > best_load {
                    best_load = load_per_replica;
                    best_logical = log_idx;
                }
            }
            
            phy_to_log[layer][phy_idx] = best_logical as i64;
            rank[layer][phy_idx] = log_count[layer][best_logical];
            log_count[layer][best_logical] += 1;
        }
    }
    
    (phy_to_log, rank, log_count)
}

/// Compute load imbalance ratio across experts
/// Returns max/min load ratio (1.0 = perfectly balanced)
#[pyfunction]
pub fn compute_load_imbalance_rust(loads: Vec<Vec<f64>>) -> f64 {
    let mut max_load = 0.0f64;
    let mut min_load = f64::MAX;
    
    for layer_loads in &loads {
        for &load in layer_loads {
            if load > 0.0 {
                max_load = max_load.max(load);
                min_load = min_load.min(load);
            }
        }
    }
    
    if min_load == f64::MAX || min_load <= 0.0 {
        1.0
    } else {
        max_load / min_load
    }
}


use pyo3::prelude::*;

fn softmax_probability(logits: &[f64], token_idx: usize, temperature: f64) -> Option<f64> {
    if token_idx >= logits.len() {
        return None;
    }
    let t = if temperature.is_finite() && temperature > 0.0 {
        temperature
    } else {
        1.0
    };

    let scaled: Vec<f64> = logits.iter().map(|v| v / t).collect();
    let max_val = scaled.iter().copied().fold(f64::NEG_INFINITY, f64::max);

    let exps: Vec<f64> = scaled.iter().map(|v| (v - max_val).exp()).collect();
    let denom: f64 = exps.iter().sum();
    if !denom.is_finite() || denom <= 0.0 {
        return None;
    }

    Some(exps[token_idx] / denom)
}

// =============================================================================
// Draft Token Verification
// =============================================================================

/// Verify draft tokens against target tokens
/// Returns (num_accepted, accepted_positions)
#[pyfunction]
pub fn verify_draft_tokens_rust(
    draft_tokens: Vec<i64>,
    target_tokens: Vec<i64>,
) -> (usize, Vec<usize>) {
    let mut num_accepted = 0;
    let mut accepted_positions = Vec::new();

    for (i, (&draft, &target)) in draft_tokens.iter().zip(target_tokens.iter()).enumerate() {
        if draft == target {
            num_accepted += 1;
            accepted_positions.push(i);
        } else {
            // Stop at first mismatch
            break;
        }
    }

    (num_accepted, accepted_positions)
}

/// Probabilistic verification with acceptance probabilities
/// Returns (accepted_flags, bonus_token_needed)
#[pyfunction]
pub fn verify_draft_probabilistic_rust(
    draft_probs: Vec<f64>,
    target_probs: Vec<f64>,
    random_values: Vec<f64>,
) -> (Vec<bool>, bool) {
    let mut accepted = Vec::with_capacity(draft_probs.len());
    let mut all_accepted = true;

    for ((&d_prob, &t_prob), &r) in draft_probs
        .iter()
        .zip(target_probs.iter())
        .zip(random_values.iter())
    {
        // Standard speculative decoding acceptance criterion
        let accept_prob = if d_prob <= 0.0 {
            if t_prob > 0.0 {
                1.0
            } else {
                0.0
            }
        } else {
            (t_prob / d_prob).min(1.0)
        };
        let accept = r < accept_prob;
        accepted.push(accept);

        if !accept {
            all_accepted = false;
            // Truncate at first rejection
            break;
        }
    }

    // If all accepted, we need a bonus token from target model
    (accepted, all_accepted)
}

/// Verify a batch of draft tokens
/// Returns (accepted_count, mask)
#[pyfunction]
#[pyo3(signature = (draft_tokens, target_logits, draft_probs, temperature=1.0))]
pub fn verify_draft_tokens_batch_rust(
    draft_tokens: Vec<i64>,
    target_logits: Vec<Vec<f64>>,
    draft_probs: Vec<f64>,
    temperature: f64,
) -> (usize, Vec<bool>) {
    let mut mask = Vec::with_capacity(draft_tokens.len());
    let mut accepted_count = 0;

    for (i, &token) in draft_tokens.iter().enumerate() {
        if token < 0 {
            mask.push(false);
            continue;
        }
        let token_idx = token as usize;
        if i >= target_logits.len() {
            mask.push(false);
            continue;
        }

        let logits = &target_logits[i];
        let Some(target_prob) = softmax_probability(logits, token_idx, temperature) else {
            mask.push(false);
            continue;
        };

        let draft_prob = draft_probs.get(i).copied().unwrap_or(0.0).clamp(0.0, 1.0);
        let accept = target_prob >= draft_prob;
        mask.push(accept);
        if accept {
            accepted_count += 1;
        }
    }

    (accepted_count, mask)
}

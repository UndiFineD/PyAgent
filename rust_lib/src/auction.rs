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
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

/// Combinatorial optimization for large-scale bidding (Swarm/Auction).
/// Implements Vickrey-Clarke-Groves (VCG) prices for multi-slot auctions.
#[pyfunction]
pub fn calculate_vcg_prices_rust(
    bids: HashMap<String, f64>,
    num_slots: usize,
) -> HashMap<String, f64> {
    if bids.is_empty() || num_slots == 0 {
        return HashMap::new();
    }

    let mut bids_vec: Vec<(String, f64)> = bids.into_iter().collect();
    // Sort descending by bid amount
    bids_vec.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    let num_winners = num_slots.min(bids_vec.len());
    let winners = &bids_vec[..num_winners];
    let others = &bids_vec[num_winners..];

    let mut prices = HashMap::new();

    // VCG Price for each winner
    // If bidder i vanishes, the (N)th bidder (first loser) takes the last slot.
    // In a simple multi-unit auction, VCG price is simply the highest losing bid.
    let highest_losing_bid = if others.is_empty() {
        0.0
    } else {
        others[0].1
    };

    for (name, _) in winners {
        prices.insert(name.clone(), highest_losing_bid);
    }

    prices
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_vcg_prices_rust, m)?)?;
    Ok(())
}

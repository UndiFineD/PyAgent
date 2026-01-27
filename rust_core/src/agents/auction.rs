use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Enforce VRAM Quota (AuctionCore).
#[pyfunction]
pub fn enforce_vram_quota(agent_vram_request: f64, total_available: f64, quota_percent: f64) -> PyResult<bool> {
    Ok(agent_vram_request <= (total_available * quota_percent))
}

/// Calculate VCG Auction (AuctionCore).
#[pyfunction]
pub fn calculate_vcg_auction(_py: Python<'_>, bids: Vec<Bound<'_, PyDict>>, slots: usize) -> PyResult<Vec<PyObject>> {
    let mut bids_with_val: Vec<(Bound<'_, PyDict>, f64)> = Vec::with_capacity(bids.len());
    
    for bid in bids {
        if let Some(item) = bid.get_item("amount")? {
             if let Ok(amount) = item.extract::<f64>() {
                 bids_with_val.push((bid, amount));
             } else {
                 return Err(pyo3::exceptions::PyValueError::new_err("Bid missing amount"));
             }
        } else {
             return Err(pyo3::exceptions::PyKeyError::new_err("Bid missing amount"));
        }
    }
    
    bids_with_val.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    let count = bids_with_val.len();
    let clearing_price = if count > slots {
        bids_with_val[slots].1
    } else {
        0.0
    };
    
    let take = std::cmp::min(count, slots);
    let mut winners = Vec::with_capacity(take);
    
    for i in 0..take {
        let (bid, _) = &bids_with_val[i];
        bid.set_item("price_paid", clearing_price)?;
        winners.push(bid.clone().into());
    }
    
    Ok(winners)
}

/// Calculate VCG Auction (AuctionCore Mapping Alias).
#[pyfunction]
pub fn calculate_vcg_prices(py: Python<'_>, bids: Vec<Bound<'_, PyDict>>, slots: usize) -> PyResult<Vec<PyObject>> {
    calculate_vcg_auction(py, bids, slots)
}

/// Calculate bid priority score (AuctionCore).
#[pyfunction]
#[allow(dead_code)]
pub fn calculate_bid_priority_score(amount: f64, urgency: f64, reputation: f64) -> PyResult<f64> {
    Ok(amount * 0.5 + urgency * 0.3 + reputation * 0.2)
}

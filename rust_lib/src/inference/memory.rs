use pyo3::prelude::*;
use std::collections::HashMap;

// =============================================================================
// Memory Pressure Detection
// =============================================================================

/// Calculate memory pressure score (0.0 = no pressure, 1.0 = critical)
#[pyfunction]
pub fn calculate_memory_pressure_rust(
    used_blocks: usize,
    total_blocks: usize,
    reserved_ratio: f64,
) -> f64 {
    if total_blocks == 0 {
        return 1.0;
    }
    
    let usage = used_blocks as f64 / total_blocks as f64;
    let threshold = 1.0 - reserved_ratio;
    
    if usage <= threshold {
        0.0
    } else {
        (usage - threshold) / reserved_ratio
    }
}

/// Determine number of blocks to free based on pressure
#[pyfunction]
#[pyo3(signature = (pressure, total_blocks, min_free=0.1))]
pub fn blocks_to_free_rust(
    pressure: f64,
    total_blocks: usize,
    min_free: f64,
) -> usize {
    if pressure <= 0.0 {
        return 0;
    }
    
    let target_free = (min_free + pressure * (1.0 - min_free)) * total_blocks as f64;
    target_free.ceil() as usize
}

/// Compute optimal chunk boundaries for prefill
#[pyfunction]
#[pyo3(signature = (total_tokens, chunk_size, memory_pressure=0.0))]
pub fn chunk_boundaries_rust(
    total_tokens: usize,
    chunk_size: usize,
    memory_pressure: f64,
) -> Vec<(usize, usize)> {
    // Adjust chunk size based on memory pressure
    let effective_chunk = if memory_pressure > 0.0 {
        let reduction = 1.0 - (memory_pressure * 0.5);
        ((chunk_size as f64) * reduction).max(64.0) as usize
    } else {
        chunk_size
    };
    
    let mut boundaries = Vec::new();
    let mut start = 0;
    
    while start < total_tokens {
        let end = (start + effective_chunk).min(total_tokens);
        boundaries.push((start, end));
        start = end;
    }
    
    boundaries
}

// =============================================================================
// Phase 32: UVA Buffer & GPU Transfer Accelerations
// =============================================================================

/// Optimized UVA buffer copy with stride support
/// Simulates pinned memory copy optimization
#[pyfunction]
#[pyo3(signature = (src_offset, dst_offset, size, stride=1))]
pub fn uva_copy_rust(
    src_offset: usize,
    dst_offset: usize,
    size: usize,
    stride: usize,
) -> Vec<(usize, usize)> {
    // Return list of (src, dst) offset pairs for batch copy
    let mut pairs = Vec::with_capacity(size / stride.max(1));
    let mut s = src_offset;
    let mut d = dst_offset;
    
    for _ in 0..(size / stride.max(1)) {
        pairs.push((s, d));
        s += stride;
        d += stride;
    }
    
    pairs
}

/// Compute write indices for batched GPU writes
/// Returns optimized index ordering for memory coalescing
#[pyfunction]
pub fn batch_write_indices_rust(
    indices: Vec<usize>,
    block_size: usize,
) -> Vec<usize> {
    // Sort by block then offset within block
    let mut sorted = indices;
    sorted.sort_by_key(|&idx| (idx / block_size, idx % block_size));
    sorted
}

/// Coalesce writes for locality optimization
/// Groups adjacent writes into ranges
#[pyfunction]
#[pyo3(signature = (indices, values, max_gap=4))]
pub fn coalesce_writes_rust(
    indices: Vec<usize>,
    values: Vec<f64>,
    max_gap: usize,
) -> Vec<(usize, usize, Vec<f64>)> {
    if indices.is_empty() {
        return Vec::new();
    }
    
    // Create (index, value) pairs and sort by index
    let mut pairs: Vec<_> = indices.into_iter().zip(values).collect();
    pairs.sort_by_key(|(idx, _)| *idx);
    
    let mut coalesced = Vec::new();
    let mut range_start = pairs[0].0;
    let mut range_values = vec![pairs[0].1];
    let mut expected_next = pairs[0].0 + 1;
    
    for (idx, val) in pairs.into_iter().skip(1) {
        if idx <= expected_next + max_gap {
            // Fill gaps with zeros
            while expected_next < idx {
                range_values.push(0.0);
                expected_next += 1;
            }
            range_values.push(val);
            expected_next = idx + 1;
        } else {
            // Start new range
            coalesced.push((range_start, range_start + range_values.len(), range_values));
            range_start = idx;
            range_values = vec![val];
            expected_next = idx + 1;
        }
    }
    
    // Push final range
    coalesced.push((range_start, range_start + range_values.len(), range_values));
    
    coalesced
}

/// GPU memory snapshot serialization
/// Returns packed representation of memory state
#[pyfunction]
pub fn gpu_memory_snapshot_rust(
    region_ids: Vec<usize>,
    region_sizes: Vec<usize>,
    _region_offsets: Vec<usize>,
    is_free: Vec<bool>,
) -> HashMap<String, Vec<usize>> {
    let mut result = HashMap::new();
    
    let mut total_bytes: usize = 0;
    let mut allocated_bytes: usize = 0;
    let mut free_bytes: usize = 0;
    let mut num_allocations: usize = 0;
    let mut free_regions = Vec::new();
    let mut allocated_regions = Vec::new();
    
    for i in 0..region_ids.len() {
        let size = region_sizes.get(i).copied().unwrap_or(0);
        total_bytes += size;
        
        if is_free.get(i).copied().unwrap_or(true) {
            free_bytes += size;
            free_regions.push(region_ids[i]);
        } else {
            allocated_bytes += size;
            num_allocations += 1;
            allocated_regions.push(region_ids[i]);
        }
    }
    
    // Calculate fragmentation
    let max_free = free_regions.iter()
        .filter_map(|&id| {
            region_ids.iter()
                .position(|&r| r == id)
                .and_then(|idx| region_sizes.get(idx).copied())
        })
        .max()
        .unwrap_or(0);
    
    let frag_ratio = if free_bytes > 0 {
        ((free_bytes - max_free) * 100) / free_bytes
    } else {
        0
    };
    
    result.insert("total_bytes".to_string(), vec![total_bytes]);
    result.insert("allocated_bytes".to_string(), vec![allocated_bytes]);
    result.insert("free_bytes".to_string(), vec![free_bytes]);
    result.insert("num_allocations".to_string(), vec![num_allocations]);
    result.insert("fragmentation_percent".to_string(), vec![frag_ratio]);
    result.insert("free_regions".to_string(), free_regions);
    result.insert("allocated_regions".to_string(), allocated_regions);
    
    result
}

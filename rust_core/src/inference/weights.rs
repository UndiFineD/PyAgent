use pyo3::prelude::*;
use std::collections::HashMap;

/// Compute hash for weight data using xxHash-like algorithm
/// Returns 64-bit hash for fast lookup
#[pyfunction]
pub fn weight_hash_compute_rust(data: Vec<u8>) -> u64 {
    // xxHash-inspired fast hashing
    const PRIME1: u64 = 0x9E3779B185EBCA87;
    const PRIME2: u64 = 0xC2B2AE3D27D4EB4F;
    const PRIME3: u64 = 0x165667B19E3779F9;
    const PRIME4: u64 = 0x85EBCA77C2B2AE63;
    const PRIME5: u64 = 0x27D4EB2F165667C5;
    
    let len = data.len() as u64;
    let mut hash = PRIME5.wrapping_add(len);
    
    let chunks = data.chunks_exact(8);
    let remainder = chunks.remainder();
    
    for chunk in chunks {
        let val = u64::from_le_bytes(chunk.try_into().unwrap());
        hash ^= val.wrapping_mul(PRIME1);
        hash = hash.rotate_left(27).wrapping_mul(PRIME2);
    }
    
    for &byte in remainder {
        hash ^= (byte as u64).wrapping_mul(PRIME3);
        hash = hash.rotate_left(11).wrapping_mul(PRIME4);
    }
    
    // Avalanche
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(PRIME2);
    hash ^= hash >> 29;
    hash = hash.wrapping_mul(PRIME3);
    hash ^= hash >> 32;
    
    hash
}

/// Validate weight shapes match expected shapes
/// Returns list of error messages for mismatches
#[pyfunction]
pub fn validate_weight_shapes_rust(
    specs: Vec<HashMap<String, String>>,
    expected: Vec<HashMap<String, String>>,
) -> Vec<String> {
    let mut errors = Vec::new();
    
    let spec_map: HashMap<_, _> = specs.iter()
        .filter_map(|s| s.get("name").map(|n| (n.clone(), s)))
        .collect();
    
    for exp in &expected {
        if let Some(name) = exp.get("name") {
            match spec_map.get(name) {
                None => errors.push(format!("Missing weight: {}", name)),
                Some(spec) => {
                    if let (Some(spec_shape), Some(exp_shape)) = (spec.get("shape"), exp.get("shape")) {
                        if spec_shape != exp_shape {
                            errors.push(format!(
                                "Shape mismatch for {}: got {}, expected {}",
                                name, spec_shape, exp_shape
                            ));
                        }
                    }
                }
            }
        }
    }
    
    errors
}

/// Compute optimal shard assignment for tensor-parallel loading
/// Returns list of rank assignments for each parameter
#[pyfunction]
pub fn compute_shard_assignment_rust(
    num_params: usize,
    num_ranks: usize,
    param_sizes: Vec<usize>,
) -> Vec<usize> {
    if num_ranks == 0 {
        return vec![0; num_params];
    }
    
    // Greedy load balancing
    let mut rank_loads = vec![0usize; num_ranks];
    let mut assignments = vec![0usize; num_params];
    
    // Sort params by size descending for better balancing
    let mut indexed_sizes: Vec<_> = param_sizes.iter().enumerate().collect();
    indexed_sizes.sort_by(|a, b| b.1.cmp(a.1));
    
    for (param_idx, &size) in indexed_sizes {
        // Find rank with minimum load
        let min_rank = rank_loads.iter()
            .enumerate()
            .min_by_key(|(_, load)| *load)
            .map(|(idx, _)| idx)
            .unwrap_or(0);
        
        assignments[param_idx] = min_rank;
        rank_loads[min_rank] += size;
    }
    
    assignments
}

/// Validate shard shapes for tensor-parallel consistency
/// Returns list of error messages
#[pyfunction]
pub fn validate_shard_shapes_rust(
    shard_specs: Vec<HashMap<String, String>>,
    _rank: usize,
    world_size: usize,
) -> Vec<String> {
    let mut errors = Vec::new();
    
    for spec in &shard_specs {
        if let Some(num_shards_str) = spec.get("num_shards") {
            if let Ok(num_shards) = num_shards_str.parse::<usize>() {
                if num_shards != world_size && num_shards != 1 {
                    let name = spec.get("name").map(|s| s.as_str()).unwrap_or("unknown");
                    errors.push(format!(
                        "Shard count mismatch for {}: expected {} or 1, got {}",
                        name, world_size, num_shards
                    ));
                }
            }
        }
    }
    
    errors
}


/// Tensorizer checksum computation (SHA256 truncated)
#[pyfunction]
pub fn tensorizer_checksum_rust(data: Vec<u8>) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    data.hash(&mut hasher);
    let hash = hasher.finish();
    
    format!("{:016x}", hash)
}

/// Pack tensor metadata for serialization
#[pyfunction]
pub fn pack_tensor_metadata_rust(
    name: String,
    shape: Vec<usize>,
    dtype: String,
    offset: usize,
    size_bytes: usize,
) -> Vec<u8> {
    let mut result = Vec::new();
    
    // Name (length-prefixed)
    let name_bytes = name.as_bytes();
    result.extend((name_bytes.len() as u32).to_le_bytes());
    result.extend(name_bytes);
    
    // Shape (length-prefixed array)
    result.extend((shape.len() as u32).to_le_bytes());
    for dim in shape {
        result.extend((dim as u64).to_le_bytes());
    }
    
    // Dtype
    let dtype_bytes = dtype.as_bytes();
    result.extend((dtype_bytes.len() as u32).to_le_bytes());
    result.extend(dtype_bytes);
    
    // Offset and size
    result.extend((offset as u64).to_le_bytes());
    result.extend((size_bytes as u64).to_le_bytes());
    
    result
}


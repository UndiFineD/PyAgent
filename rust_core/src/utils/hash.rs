use pyo3::prelude::*;
use std::collections::HashMap;
use std::fs;
use md5::{Md5, Digest};
use sha2::Sha256;

/// Fast hashing for shard lookup (Phase 131).
/// Uses a simplified FNV-1a hash for sub-millisecond page access.
#[pyfunction]
pub fn fast_hash(key: &str) -> PyResult<String> {
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in key.as_bytes() {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    Ok(format!("{:016x}", hash))
}

/// xxHash-style fast hash (using FNV-1a for now, can add xxhash crate later).
/// Returns 64-bit hex hash string.
#[pyfunction]
pub fn xxhash_rust(data: &str) -> PyResult<String> {
    // FNV-1a 64-bit as fast non-cryptographic hash
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in data.as_bytes() {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    Ok(format!("{:016x}", hash))
}

/// Fast hash for cache keys with optional prefix.
#[pyfunction]
pub fn fast_cache_hash_rust(key: &str, prefix: Option<&str>) -> PyResult<String> {
    let full_key = match prefix {
        Some(p) => format!("{}:{}", p, key),
        None => key.to_string(),
    };
    
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in full_key.as_bytes() {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    Ok(format!("{:016x}", hash))
}

/// MD5 sharding for InteractionRegistry (Phase 318).
#[pyfunction]
pub fn calculate_interaction_shard_md5(key: &str, shard_count: usize) -> PyResult<usize> {
    let mut hasher = Md5::new();
    hasher.update(key.as_bytes());
    let result = hasher.finalize();
    
    let mut seed_bytes = [0u8; 8];
    seed_bytes.copy_from_slice(&result[..8]);
    let seed = u64::from_be_bytes(seed_bytes);
    
    Ok((seed as usize) % shard_count)
}

#[pyfunction]
pub fn generate_hash(data: &str) -> PyResult<String> {
    // Phase 131: SHA-256 integrity calculation
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let result = hasher.finalize();
    Ok(format!("{:x}", result))
}

#[pyfunction]
pub fn verify_integrity(data: &str, expected_hash: &str) -> PyResult<bool> {
    let actual = generate_hash(data)?;
    Ok(actual == expected_hash)
}

/// Bulk hash files for filesystem integrity (FileSystemCore).
#[pyfunction]
pub fn bulk_hash_files_rust(paths: Vec<String>) -> PyResult<HashMap<String, String>> {
    let mut results = HashMap::new();
    for path in paths {
        if let Ok(content) = fs::read(&path) {
            let mut hasher = Sha256::new();
            hasher.update(&content);
            results.insert(path, hex::encode(hasher.finalize()));
        }
    }
    Ok(results)
}

/// Adler-32 based sharding (KnowledgeCore).
#[pyfunction]
pub fn get_adler32_shard(key: &str, shard_count: usize) -> PyResult<usize> {
    let mut a: u32 = 1;
    let mut b: u32 = 0;
    for byte in key.as_bytes() {
        a = (a + *byte as u32) % 65521;
        b = (b + a) % 65521;
    }
    let adler = (b << 16) | a;
    Ok((adler as usize) % shard_count)
}

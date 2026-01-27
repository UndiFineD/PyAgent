use pyo3::prelude::*;
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::hash::{Hash, Hasher};

#[pyfunction]
pub fn normalize_and_hash_rust(content: &str) -> PyResult<String> {
    // Normalize: lowercase, trim, remove whitespace
    let normalized: String = content
        .to_lowercase()
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect();
        
    let mut hasher = DefaultHasher::new();
    normalized.hash(&mut hasher);
    Ok(format!("{:x}", hasher.finish()))
}

#[pyfunction]
pub fn fast_cache_key_rust(parts: &Bound<'_, PyAny>) -> PyResult<String> {
    let mut hasher = DefaultHasher::new();
    if let Ok(s) = parts.extract::<String>() {
        s.hash(&mut hasher);
    } else if let Ok(list) = parts.extract::<Vec<String>>() {
        for part in list {
            part.hash(&mut hasher);
        }
    } else {
        return Err(pyo3::exceptions::PyTypeError::new_err("Expected string or list of strings"));
    }
    Ok(format!("{:x}", hasher.finish()))
}

#[pyfunction]
pub fn fast_prefix_key_rust(key: &str, length: usize) -> PyResult<String> {
    if key.len() <= length {
        Ok(key.to_string())
    } else {
        Ok(key[..length].to_string())
    }
}

#[pyfunction]
pub fn partition_to_shards_rust(
    items: Vec<String>,
    shard_count: usize,
) -> PyResult<Vec<Vec<String>>> {
    let mut shards = vec![Vec::new(); shard_count];
    
    for item in items {
        let mut hasher = DefaultHasher::new();
        item.hash(&mut hasher);
        let hash = hasher.finish();
        let shard_idx = (hash as usize) % shard_count;
        shards[shard_idx].push(item);
    }
    
    Ok(shards)
}

#[pyfunction]
pub fn calculate_shard_id_rust(
    key: &str,
    total_shards: usize,
) -> PyResult<usize> {
    let mut hasher = DefaultHasher::new();
    key.hash(&mut hasher);
    let hash = hasher.finish();
    Ok((hash as usize) % total_shards)
}

#[pyfunction]
pub fn merge_knowledge_rust(base_json: &str, delta_json: &str) -> PyResult<String> {
    let mut base: HashMap<String, serde_json::Value> = serde_json::from_str(base_json)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        
    let delta: HashMap<String, serde_json::Value> = serde_json::from_str(delta_json)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        
    for (k, v) in delta {
        base.insert(k, v);
    }
    
    serde_json::to_string(&base)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}

#[pyfunction]
pub fn filter_stable_knowledge_rust(
    knowledge_json: &str,
    stability_threshold: f64,
) -> PyResult<String> {
    let knowledge: HashMap<String, serde_json::Value> = serde_json::from_str(knowledge_json)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        
    let mut filtered = HashMap::new();
    
    for (k, v) in knowledge {
        // Assuming value schema has "stability" or "confidence" field
        // If it's just a raw value, we can't filter.
        // Let's assume structure: {"data": ..., "confidence": 0.9}
        if let Some(conf) = v.get("confidence").and_then(|c| c.as_f64()) {
            if conf >= stability_threshold {
                filtered.insert(k, v);
            }
        } else if let Some(stab) = v.get("stability").and_then(|s| s.as_f64()) {
            if stab >= stability_threshold {
                filtered.insert(k, v);
            }
        } else {
            // Keep items without score? Or drop? Assuming keep if unsure, or drop.
            // Let's keep for safety if schema is mixed.
            filtered.insert(k, v);
        }
    }
    
    serde_json::to_string(&filtered)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}

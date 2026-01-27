use pyo3::prelude::*;
use std::collections::HashMap;
use serde_json::Value;

/// Count the number of leaves in a nested JSON structure.
/// A leaf is any value that is not an object or array.
#[pyfunction]
pub fn json_count_leaves_rust(json_str: &str) -> PyResult<u64> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    fn count_leaves(v: &Value) -> u64 {
        match v {
            Value::Object(map) => map.values().map(count_leaves).sum(),
            Value::Array(arr) => arr.iter().map(count_leaves).sum(),
            _ => 1,
        }
    }
    
    Ok(count_leaves(&value))
}

/// Iterate all leaf values in a nested JSON structure.
/// Returns a list of leaf values as strings.
#[pyfunction]
pub fn json_iter_leaves_rust(json_str: &str) -> PyResult<Vec<String>> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    fn collect_leaves(v: &Value, acc: &mut Vec<String>) {
        match v {
            Value::Object(map) => {
                for val in map.values() {
                    collect_leaves(val, acc);
                }
            }
            Value::Array(arr) => {
                for val in arr {
                    collect_leaves(val, acc);
                }
            }
            Value::String(s) => acc.push(s.clone()),
            Value::Number(n) => acc.push(n.to_string()),
            Value::Bool(b) => acc.push(b.to_string()),
            Value::Null => acc.push("null".to_string()),
        }
    }
    
    let mut leaves = Vec::new();
    collect_leaves(&value, &mut leaves);
    Ok(leaves)
}

/// Flatten a nested JSON structure to dot-notation keys.
/// Returns a HashMap of path -> value.
#[pyfunction]
pub fn json_flatten_rust(json_str: &str, separator: &str) -> PyResult<HashMap<String, String>> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    fn flatten(v: &Value, prefix: &str, sep: &str, acc: &mut HashMap<String, String>) {
        match v {
            Value::Object(map) => {
                for (k, val) in map {
                    let new_key = if prefix.is_empty() {
                        k.clone()
                    } else {
                        format!("{}{}{}", prefix, sep, k)
                    };
                    flatten(val, &new_key, sep, acc);
                }
            }
            Value::Array(arr) => {
                for (i, val) in arr.iter().enumerate() {
                    let new_key = format!("{}[{}]", prefix, i);
                    flatten(val, &new_key, sep, acc);
                }
            }
            Value::String(s) => {
                acc.insert(prefix.to_string(), s.clone());
            }
            Value::Number(n) => {
                acc.insert(prefix.to_string(), n.to_string());
            }
            Value::Bool(b) => {
                acc.insert(prefix.to_string(), b.to_string());
            }
            Value::Null => {
                acc.insert(prefix.to_string(), "null".to_string());
            }
        }
    }
    
    let mut result = HashMap::new();
    flatten(&value, "", separator, &mut result);
    Ok(result)
}

/// Get the maximum depth of a nested JSON structure.
#[pyfunction]
pub fn json_depth_rust(json_str: &str) -> PyResult<u64> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    fn depth(v: &Value) -> u64 {
        match v {
            Value::Object(map) if !map.is_empty() => {
                1 + map.values().map(depth).max().unwrap_or(0)
            }
            Value::Array(arr) if !arr.is_empty() => {
                1 + arr.iter().map(depth).max().unwrap_or(0)
            }
            Value::Object(_) | Value::Array(_) => 1,
            _ => 0,
        }
    }
    
    Ok(depth(&value))
}

/// Get a value at a dot-notation path in JSON.
/// Returns the value as a string, or None if not found.
#[pyfunction]
pub fn json_get_path_rust(json_str: &str, path: &str, separator: &str) -> PyResult<Option<String>> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    fn get_at_path<'a>(v: &'a Value, parts: &[&str]) -> Option<&'a Value> {
        if parts.is_empty() {
            return Some(v);
        }
        
        let part = parts[0];
        
        // Check for array index notation
        if let Some(idx_str) = part.strip_prefix('[').and_then(|s| s.strip_suffix(']')) {
            if let Ok(idx) = idx_str.parse::<usize>() {
                if let Value::Array(arr) = v {
                    return arr.get(idx).and_then(|next| get_at_path(next, &parts[1..]));
                }
            }
            return None;
        }
        
        // Regular object key
        if let Value::Object(map) = v {
            return map.get(part).and_then(|next| get_at_path(next, &parts[1..]));
        }
        
        None
    }
    
    let parts: Vec<&str> = path.split(separator).collect();
    
    match get_at_path(&value, &parts) {
        Some(Value::String(s)) => Ok(Some(s.clone())),
        Some(Value::Number(n)) => Ok(Some(n.to_string())),
        Some(Value::Bool(b)) => Ok(Some(b.to_string())),
        Some(Value::Null) => Ok(Some("null".to_string())),
        Some(v) => Ok(Some(v.to_string())),
        None => Ok(None),
    }
}

/// Validate if all leaves in JSON match a pattern.
/// Returns true if all string leaves match the regex pattern.
#[pyfunction]
pub fn json_validate_leaves_rust(json_str: &str, pattern: &str) -> PyResult<bool> {
    let value: Value = serde_json::from_str(json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    
    let re = regex::Regex::new(pattern)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid regex: {}", e)))?;
    
    fn validate(v: &Value, re: &regex::Regex) -> bool {
        match v {
            Value::Object(map) => map.values().all(|val| validate(val, re)),
            Value::Array(arr) => arr.iter().all(|val| validate(val, re)),
            Value::String(s) => re.is_match(s),
            _ => true, // Non-string leaves always pass
        }
    }
    
    Ok(validate(&value, &re))
}

/// Fast extraction of JSON tool calls from a string.
/// Returns vector of (start_idx, end_idx, name, arguments_json) tuples.
#[pyfunction]
pub fn extract_json_tool_calls_rust(
    model_output: &str,
) -> PyResult<Vec<(usize, usize, String, String)>> {
    let mut results = Vec::new();
    
    // Find JSON arrays that look like tool calls
    let bytes = model_output.as_bytes();
    let mut i = 0;
    
    while i < bytes.len() {
        // Look for opening bracket
        if bytes[i] == b'[' {
            let start = i;
            let mut bracket_count = 1;
            i += 1;
            
            while i < bytes.len() && bracket_count > 0 {
                match bytes[i] {
                    b'[' => bracket_count += 1,
                    b']' => bracket_count -= 1,
                    _ => {}
                }
                i += 1;
            }
            
            if bracket_count == 0 {
                let json_str = &model_output[start..i];
                
                // Try to parse as JSON
                if let Ok(parsed) = serde_json::from_str::<serde_json::Value>(json_str) {
                    if let Some(arr) = parsed.as_array() {
                        for item in arr {
                            if let Some(obj) = item.as_object() {
                                if let Some(name) = obj.get("name").and_then(|v| v.as_str()) {
                                    let args = obj.get("arguments")
                                        .or_else(|| obj.get("parameters"))
                                        .map(|v| v.to_string())
                                        .unwrap_or_else(|| "{}".to_string());
                                    
                                    results.push((start, i, name.to_string(), args));
                                }
                            }
                        }
                    }
                }
            }
        } else {
            i += 1;
        }
    }
    
    Ok(results)
}

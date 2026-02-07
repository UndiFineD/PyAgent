use pyo3::prelude::*;
use std::collections::HashMap;

// =============================================================================
// Phase 41: Tool Parser Acceleration
// =============================================================================

/// Fast JSON object extraction from text
/// Returns list of (start_pos, end_pos) for each JSON object found
#[pyfunction]
pub fn extract_json_positions_rust(
    text: String,
) -> Vec<(usize, usize)> {
    let mut results = Vec::new();
    let chars: Vec<char> = text.chars().collect();
    
    let mut brace_depth = 0;
    let mut start_idx: Option<usize> = None;
    let mut in_string = false;
    let mut prev_char = ' ';
    
    for (i, &ch) in chars.iter().enumerate() {
        if ch == '"' && prev_char != '\\' {
            in_string = !in_string;
        } else if !in_string {
            if ch == '{' {
                if brace_depth == 0 {
                    start_idx = Some(i);
                }
                brace_depth += 1;
            } else if ch == '}' {
                brace_depth -= 1;
                if brace_depth == 0 {
                    if let Some(start) = start_idx {
                        results.push((start, i + 1));
                    }
                    start_idx = None;
                }
            }
        }
        prev_char = ch;
    }
    
    results
}

/// Detect tool call format from text content
/// Returns format name: "hermes", "llama3", "mistral", "granite", "json"
#[pyfunction]
pub fn detect_tool_format_rust(
    text: String,
) -> String {
    if text.contains("<tool_call>") {
        return "hermes".to_string();
    }
    if text.contains("<|python_tag|>") {
        return "llama3".to_string();
    }
    if text.contains("[TOOL_CALLS]") {
        return "mistral".to_string();
    }
    if text.contains("<|tool_call|>") {
        return "granite".to_string();
    }
    "json".to_string()
}

/// Parse tool call arguments from JSON string
/// Returns parsed arguments as key-value pairs or empty on error
#[pyfunction]
pub fn parse_tool_arguments_rust(
    json_str: String,
) -> HashMap<String, String> {
    let mut result = HashMap::new();
    
    // Simple JSON parsing for flat objects
    let trimmed = json_str.trim();
    if !trimmed.starts_with('{') || !trimmed.ends_with('}') {
        return result;
    }
    
    let inner = &trimmed[1..trimmed.len()-1];
    
    // Split by commas (simplified - doesn't handle nested objects)
    let mut in_string = false;
    let mut depth = 0;
    let mut current_key = String::new();
    let mut current_value = String::new();
    let mut parsing_value = false;
    let mut prev_char = ' ';
    
    for ch in inner.chars() {
        if ch == '"' && prev_char != '\\' {
            in_string = !in_string;
        } else if !in_string {
            match ch {
                '{' | '[' => depth += 1,
                '}' | ']' => depth -= 1,
                ':' if depth == 0 => {
                    parsing_value = true;
                    prev_char = ch;
                    continue;
                }
                ',' if depth == 0 => {
                    let key = current_key.trim().trim_matches('"').to_string();
                    let value = current_value.trim().trim_matches('"').to_string();
                    if !key.is_empty() {
                        result.insert(key, value);
                    }
                    current_key.clear();
                    current_value.clear();
                    parsing_value = false;
                    prev_char = ch;
                    continue;
                }
                _ => {}
            }
        }
        
        if parsing_value {
            current_value.push(ch);
        } else {
            current_key.push(ch);
        }
        prev_char = ch;
    }
    
    // Handle last pair
    let key = current_key.trim().trim_matches('"').to_string();
    let value = current_value.trim().trim_matches('"').to_string();
    if !key.is_empty() {
        result.insert(key, value);
    }
    
    result
}

// =============================================================================
// Phase 41: Structured Output Acceleration
// =============================================================================

/// Validate JSON structure against basic schema
/// Returns (is_valid, error_message)
#[pyfunction]
pub fn validate_json_schema_fast_rust(
    json_str: String,
    required_keys: Vec<String>,
    expected_types: HashMap<String, String>,  // key -> "string"|"number"|"boolean"|"array"|"object"
) -> (bool, String) {
    // Parse JSON
    let parsed: Result<serde_json::Value, _> = serde_json::from_str(&json_str);
    
    match parsed {
        Ok(value) => {
            // Check if object
            let obj = match value.as_object() {
                Some(o) => o,
                None => return (false, "Expected JSON object".to_string()),
            };
            
            // Check required keys
            for key in &required_keys {
                if !obj.contains_key(key) {
                    return (false, format!("Missing required key: {}", key));
                }
            }
            
            // Check types
            for (key, expected_type) in &expected_types {
                if let Some(val) = obj.get(key) {
                    let actual_type = match val {
                        serde_json::Value::String(_) => "string",
                        serde_json::Value::Number(_) => "number",
                        serde_json::Value::Bool(_) => "boolean",
                        serde_json::Value::Array(_) => "array",
                        serde_json::Value::Object(_) => "object",
                        serde_json::Value::Null => "null",
                    };
                    
                    if actual_type != expected_type.as_str() {
                        return (false, format!(
                            "Key '{}': expected {}, got {}", key, expected_type, actual_type
                        ));
                    }
                }
            }
            
            (true, String::new())
        }
        Err(e) => (false, format!("JSON parse error: {}", e)),
    }
}

/// Check if partial text could still match a JSON schema
#[pyfunction]
pub fn validate_partial_json_rust(
    partial_text: String,
) -> bool {
    let trimmed = partial_text.trim();
    
    if trimmed.is_empty() {
        return true;
    }
    
    // Valid JSON prefixes
    let valid_starts = ['{', '[', '"', 't', 'f', 'n', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    
    if let Some(first_char) = trimmed.chars().next() {
        valid_starts.contains(&first_char)
    } else {
        true
    }
}

/// Computes constraint composition hash
#[pyfunction]
pub fn constraint_hash_rust(
    json_schema: Option<String>,
    regex_pattern: Option<String>,
    choices: Vec<String>,
) -> u64 {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    json_schema.hash(&mut hasher);
    regex_pattern.hash(&mut hasher);
    for choice in choices {
        choice.hash(&mut hasher);
    }
    hasher.finish()
}


/// Parse MCP tool call from JSON
#[pyfunction]
pub fn parse_mcp_tool_call_rust(
    json_str: String,
) -> PyResult<HashMap<String, String>> {
    let parsed: serde_json::Value = serde_json::from_str(&json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("JSON parse error: {}", e)))?;
    
    let mut result = HashMap::new();
    
    if let serde_json::Value::Object(obj) = parsed {
        if let Some(serde_json::Value::String(name)) = obj.get("name") {
            result.insert("name".to_string(), name.clone());
        }
        if let Some(args) = obj.get("arguments") {
            result.insert("arguments".to_string(), serde_json::to_string(args).unwrap_or_default());
        }
        if let Some(serde_json::Value::String(id)) = obj.get("id") {
            result.insert("id".to_string(), id.clone());
        }
    }
    
    Ok(result)
}

/// Validate MCP tool schema
#[pyfunction]
pub fn validate_mcp_schema_rust(
    schema_json: String,
) -> (bool, String) {
    match serde_json::from_str::<serde_json::Value>(&schema_json) {
        Ok(parsed) => {
            let obj = match parsed {
                serde_json::Value::Object(o) => o,
                _ => return (false, "Schema must be an object".to_string()),
            };
            
            // Check for name
            if !obj.contains_key("name") {
                return (false, "Missing 'name' field".to_string());
            }
            
            // Check for inputSchema if present
            if let Some(input_schema) = obj.get("inputSchema") {
                if !input_schema.is_object() {
                    return (false, "inputSchema must be an object".to_string());
                }
            }
            
            (true, String::new())
        }
        Err(e) => (false, format!("JSON parse error: {}", e)),
    }
}


/// Parse tool calls from JSON-like string
/// Returns list of (name, arguments_json) tuples
#[pyfunction]
pub fn parse_tool_calls_rust(text: &str) -> Vec<(String, String)> {
    let mut calls = Vec::new();
    
    // Simple regex-free parsing for {"name": "...", "arguments": {...}}
    let mut i = 0;
    let bytes = text.as_bytes();
    let n = bytes.len();
    
    while i < n {
        // Find "name"
        if let Some(pos) = text[i..].find("\"name\"") {
            let name_key_pos = i + pos;
            // Find colon
            if let Some(colon) = text[name_key_pos + 6..].find(':') {
                let after_colon = name_key_pos + 6 + colon + 1;
                // Find opening quote
                if let Some(quote1) = text[after_colon..].find('"') {
                    let name_start = after_colon + quote1 + 1;
                    // Find closing quote
                    if let Some(quote2) = text[name_start..].find('"') {
                        let name_end = name_start + quote2;
                        let name = text[name_start..name_end].to_string();
                        
                        // Find arguments
                        if let Some(args_pos) = text[name_end..].find("\"arguments\"") {
                            let args_key_pos = name_end + args_pos;
                            // Find colon and opening brace
                            if let Some(brace) = text[args_key_pos + 11..].find('{') {
                                let args_start = args_key_pos + 11 + brace;
                                // Find matching closing brace
                                let mut depth = 1;
                                let mut j = args_start + 1;
                                while j < n && depth > 0 {
                                    if bytes[j] == b'{' {
                                        depth += 1;
                                    } else if bytes[j] == b'}' {
                                        depth -= 1;
                                    }
                                    j += 1;
                                }
                                let args = text[args_start..j].to_string();
                                calls.push((name, args));
                                i = j;
                                continue;
                            }
                        }
                        i = name_end;
                        continue;
                    }
                }
            }
            i = name_key_pos + 1;
        } else {
            break;
        }
    }
    
    calls
}


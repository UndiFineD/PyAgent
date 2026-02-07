use pyo3::prelude::*;
use std::collections::HashMap;

// =============================================================================
// Phase 42: Platform, API, Templates, MCP, Conversation Acceleration
// =============================================================================

/// Generate platform fingerprint hash from device info
#[pyfunction]
pub fn platform_fingerprint_rust(
    platform_type: String,
    device_infos: Vec<HashMap<String, String>>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    platform_type.hash(&mut hasher);
    
    for device in device_infos {
        // Sort keys for consistent hashing
        let mut keys: Vec<_> = device.keys().collect();
        keys.sort();
        for key in keys {
            key.hash(&mut hasher);
            if let Some(val) = device.get(key) {
                val.hash(&mut hasher);
            }
        }
    }
    
    format!("{:016x}", hasher.finish())
}

/// Check device capability compatibility
#[pyfunction]
pub fn check_capability_rust(
    major: i32,
    minor: i32,
    required_major: i32,
    required_minor: i32,
) -> bool {
    if major > required_major {
        return true;
    }
    if major == required_major && minor >= required_minor {
        return true;
    }
    false
}

/// Estimate memory footprint for model loading
#[pyfunction]
pub fn estimate_memory_footprint_rust(
    num_params: i64,
    dtype_bytes: i32,
    kv_cache_size: i64,
    overhead_factor: f64,
) -> i64 {
    let base_memory = num_params * dtype_bytes as i64;
    let total = (base_memory as f64 * overhead_factor) as i64 + kv_cache_size;
    total
}

/// Parse OpenAI API response JSON efficiently
#[pyfunction]
pub fn parse_response_json_rust(
    json_str: String,
) -> PyResult<HashMap<String, String>> {
    let parsed: serde_json::Value = serde_json::from_str(&json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("JSON parse error: {}", e)))?;
    
    let mut result = HashMap::new();
    
    if let serde_json::Value::Object(obj) = parsed {
        for (key, value) in obj {
            let val_str = match value {
                serde_json::Value::String(s) => s,
                serde_json::Value::Number(n) => n.to_string(),
                serde_json::Value::Bool(b) => b.to_string(),
                serde_json::Value::Null => "null".to_string(),
                _ => serde_json::to_string(&value).unwrap_or_default(),
            };
            result.insert(key, val_str);
        }
    }
    
    Ok(result)
}

/// Extract SSE event data from stream chunk
#[pyfunction]
pub fn parse_sse_event_rust(
    chunk: String,
) -> (String, String, Option<String>) {
    let mut event_type = String::new();
    let mut data = String::new();
    let mut event_id = None;
    
    for line in chunk.lines() {
        if let Some(rest) = line.strip_prefix("event: ") {
            event_type = rest.trim().to_string();
        } else if let Some(rest) = line.strip_prefix("data: ") {
            if !data.is_empty() {
                data.push('\n');
            }
            data.push_str(rest.trim());
        } else if let Some(rest) = line.strip_prefix("id: ") {
            event_id = Some(rest.trim().to_string());
        }
    }
    
    (event_type, data, event_id)
}

/// Encode SSE event for streaming
#[pyfunction]
pub fn encode_sse_event_rust(
    event_type: String,
    data: String,
    event_id: Option<String>,
) -> String {
    let mut result = String::new();
    
    if let Some(id) = event_id {
        result.push_str(&format!("id: {}\n", id));
    }
    result.push_str(&format!("event: {}\n", event_type));
    
    for line in data.lines() {
        result.push_str(&format!("data: {}\n", line));
    }
    result.push('\n');
    
    result
}

/// Render simple chat template (non-Jinja fallback)
#[pyfunction]
pub fn render_simple_template_rust(
    messages: Vec<HashMap<String, String>>,
    template_type: String,
    add_generation_prompt: bool,
) -> String {
    let mut result = String::new();
    
    match template_type.as_str() {
        "chatml" | "qwen" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!("<|im_start|>{}\n{}<|im_end|>\n", role, content));
            }
            if add_generation_prompt {
                result.push_str("<|im_start|>assistant\n");
            }
        }
        "llama3" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!(
                    "<|start_header_id|>{}<|end_header_id|>\n\n{}<|eot_id|>",
                    role, content.trim()
                ));
            }
            if add_generation_prompt {
                result.push_str("<|start_header_id|>assistant<|end_header_id|>\n\n");
            }
        }
        "gemma" => {
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                let gemma_role = if role == "assistant" { "model" } else { role };
                result.push_str(&format!(
                    "<start_of_turn>{}\n{}<end_of_turn>\n",
                    gemma_role, content
                ));
            }
            if add_generation_prompt {
                result.push_str("<start_of_turn>model\n");
            }
        }
        _ => {
            // Default to ChatML-style
            for msg in &messages {
                let role = msg.get("role").map(|s| s.as_str()).unwrap_or("user");
                let content = msg.get("content").map(|s| s.as_str()).unwrap_or("");
                result.push_str(&format!("<|im_start|>{}\n{}<|im_end|>\n", role, content));
            }
            if add_generation_prompt {
                result.push_str("<|im_start|>assistant\n");
            }
        }
    }
    
    result
}

/// Detect chat template type from model name
#[pyfunction]
pub fn detect_chat_template_rust(
    model_name: String,
) -> String {
    let model_lower = model_name.to_lowercase();
    
    let patterns = [
        ("llama-3", "llama3"),
        ("llama3", "llama3"),
        ("meta-llama-3", "llama3"),
        ("llama-2", "llama2"),
        ("mistral", "mistral"),
        ("mixtral", "mistral"),
        ("zephyr", "zephyr"),
        ("vicuna", "vicuna"),
        ("alpaca", "alpaca"),
        ("gemma", "gemma"),
        ("phi", "phi"),
        ("qwen", "qwen"),
        ("deepseek", "deepseek"),
        ("yi", "yi"),
        ("command", "command"),
        ("openchat", "chatml"),
        ("dolphin", "chatml"),
    ];
    
    for (pattern, template) in patterns {
        if model_lower.contains(pattern) {
            return template.to_string();
        }
    }
    
    "chatml".to_string()
}

/// Find placeholder positions in text
#[pyfunction]
pub fn find_placeholders_rust(
    text: String,
    patterns: Vec<String>,
) -> Vec<usize> {
    let mut positions = Vec::new();
    
    for pattern in patterns {
        let mut start = 0;
        while let Some(pos) = text[start..].find(&pattern) {
            positions.push(start + pos);
            start = start + pos + pattern.len();
        }
    }
    
    positions.sort();
    positions
}

/// Hash conversation context for caching
#[pyfunction]
pub fn hash_conversation_context_rust(
    messages: Vec<HashMap<String, String>>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    
    for msg in messages {
        // Sort keys for consistent hashing
        let mut keys: Vec<_> = msg.keys().collect();
        keys.sort();
        for key in keys {
            key.hash(&mut hasher);
            if let Some(val) = msg.get(key) {
                val.hash(&mut hasher);
            }
        }
    }
    
    format!("{:016x}", hasher.finish())
}

/// Generate cache salt from configuration
#[pyfunction]
pub fn generate_cache_salt_rust(
    template_hash: Option<String>,
    add_generation_prompt: bool,
    add_special_tokens: bool,
    truncation: Option<String>,
) -> String {
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    
    if let Some(t) = template_hash {
        t.hash(&mut hasher);
    }
    add_generation_prompt.hash(&mut hasher);
    add_special_tokens.hash(&mut hasher);
    if let Some(tr) = truncation {
        tr.hash(&mut hasher);
    }
    
    format!("{:016x}", hasher.finish())
}

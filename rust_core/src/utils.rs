use pyo3::prelude::*;

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

/// Evaluate a math formula with variables using meval (moved directly/duplicated? No, exposed).
/// Note: evaluate_formula requires HashMap which we need to import.
use std::collections::HashMap;

/// Evaluate a math formula with variables using meval.
/// This is a safe, minimal Rust core for FormulaEngineCore parity.
#[pyfunction]
pub fn evaluate_formula(formula: &str, variables: HashMap<String, f64>) -> PyResult<f64> {
    let mut expr = formula.to_string();

    // Replace {var} placeholders with numeric values
    for (k, v) in variables.iter() {
        let placeholder = format!("{{{}}}", k);
        expr = expr.replace(&placeholder, &v.to_string());
    }

    match meval::eval_str(expr) {
        Ok(val) => Ok(val),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e.to_string())),
    }
}

/// Compress Python content using Regex (ContextCompressorCore).
#[pyfunction]
pub fn compress_python_regex(content: &str) -> PyResult<String> {
    static PY_SIG_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    let re = PY_SIG_RE.get_or_init(|| {
        regex::Regex::new(r"(?m)^\s*(?:async\s+)?(?:def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*.*?:").unwrap()
    });

    let matches: Vec<&str> = re.find_iter(content).map(|m| m.as_str().trim()).collect();
    Ok(matches.join("\n"))
}

/// Recursively flattens a nested dictionary into env-style keys (ConfigHygieneCore).
/// e.g. {"db": {"host": "localhost"}} -> {"PREFIX_DB_HOST": "localhost"}
#[pyfunction]
pub fn flatten_env_vars(
    _py: Python<'_>,
    input_dict: &Bound<'_, pyo3::types::PyDict>,
    prefix: &str
) -> PyResult<std::collections::HashMap<String, String>> {
    let mut result = std::collections::HashMap::new();
    
    // Helper stack for recursion simulation or we can just use recursive function
    // But since we are inside pyfunction, a recursive helper is cleaner.
    fn recurse(
        dict: &Bound<'_, pyo3::types::PyDict>,
        current_prefix: &str,
        acc: &mut std::collections::HashMap<String, String>
    ) -> PyResult<()> {
        for (k, v) in dict.iter() {
            let key_str: String = k.extract()?;
            let new_key = format!("{}{}", current_prefix, key_str.to_uppercase());

            if let Ok(sub_dict) = v.downcast::<pyo3::types::PyDict>() {
                 let next_prefix = format!("{}_", new_key);
                 recurse(sub_dict, &next_prefix, acc)?;
            } else {
                 let val_str = v.to_string();
                 acc.insert(new_key, val_str);
            }
        }
        Ok(())
    }

    // Since prefix usually comes in like "PYAGENT_", we use it directly.
    recurse(input_dict, prefix, &mut result)?;
    Ok(result)
}

/// Recursively removes files older than max_age_days (CurationCore).
/// Returns count of removed files.
#[pyfunction]
pub fn prune_directory_rust(directory: &str, max_age_days: i64) -> PyResult<u64> {
    use walkdir::WalkDir;
    let mut count = 0;
    let threshold = std::time::SystemTime::now()
        .checked_sub(std::time::Duration::from_secs((max_age_days as u64) * 86400))
        .unwrap_or_else(std::time::SystemTime::now);

    for entry in WalkDir::new(directory).into_iter().filter_map(|e| e.ok()) {
        if let Ok(metadata) = entry.metadata() {
            if metadata.is_file() {
                if let Ok(modified) = metadata.modified() {
                    if modified < threshold {
                        if std::fs::remove_file(entry.path()).is_ok() {
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    Ok(count)
}

/// Forcefully removes all __pycache__ folders (CurationCore).
/// Returns count of removed directories.
#[pyfunction]
pub fn deep_clean_pycache_rust(root_dir: &str) -> PyResult<u64> {
    use walkdir::WalkDir;
    let mut count = 0;
    
    // Collect paths first to avoid iterator invalidation during deletion
    let mut targets = Vec::new();

    for entry in WalkDir::new(root_dir).into_iter().filter_map(|e| e.ok()) {
         if entry.file_type().is_dir() && entry.file_name() == "__pycache__" {
             targets.push(entry.path().to_owned());
         }
    }

    // Sort reverse to delete deepest first (though __pycache__ usually don't nest)
    // Actually, remove_dir_all handles the tree. We just need to ensure we don't try 
    // to traverse into a deleted directory if `walkdir` was yielding lazily.
    // The collection step above solves the lazy yield issue.

    for path in targets {
        if std::fs::remove_dir_all(&path).is_ok() {
            count += 1;
        }
    }

    Ok(count)
}

/// Summarize Markdown content (ContextCompressorCore).
#[pyfunction]
pub fn summarize_markdown(content: &str) -> PyResult<String> {
    static MD_HEADER_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    let re = MD_HEADER_RE.get_or_init(|| {
        regex::Regex::new(r"(?m)^(#+ .*)").unwrap()
    });
    
    let matches: Vec<&str> = re.find_iter(content).map(|m| m.as_str()).collect();
    Ok(matches.join("\n"))
}

// === SearchCore Implementations ===

use pyo3::types::PyDict;

/// Parses Bing web search results into Markdown blocks.
#[pyfunction]
pub fn parse_bing_results(data: Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    if let Some(web_pages) = data.get_item("webPages")? {
        if let Ok(web_pages_dict) = web_pages.downcast::<PyDict>() {
            if let Some(value_list) = web_pages_dict.get_item("value")? {
                let values: Vec<Bound<'_, PyDict>> = value_list.extract()?;
                for v in values {
                    let name: String = v.get_item("name")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "Untitled Result".to_string());
                    let url: String = v.get_item("url")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "#".to_string());
                    let snippet: String = v.get_item("snippet")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "No snippet available.".to_string());
                    results.push(format!("### {}\nURL: {}\n{}\n", name, url, snippet));
                }
            }
        }
    }
    Ok(results)
}

/// Parses Google Custom Search results into Markdown blocks.
#[pyfunction]
pub fn parse_google_results(data: Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    if let Some(items_list) = data.get_item("items")? {
        let items: Vec<Bound<'_, PyDict>> = items_list.extract()?;
        for item in items {
            let title: String = item.get_item("title")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "Untitled Result".to_string());
            let link: String = item.get_item("link")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "#".to_string());
            let snippet: String = item.get_item("snippet")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "No snippet available.".to_string());
            results.push(format!("### {}\nURL: {}\n{}\n", title, link, snippet));
        }
    }
    Ok(results)
}

/// Parses DuckDuckGo results from ddg_search library format.
#[pyfunction]
pub fn parse_ddg_results(data: Vec<Bound<'_, PyDict>>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    for r in data {
        let title: String = r.get_item("title")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "Untitled Result".to_string());
        let href: String = r.get_item("href")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "#".to_string());
        let body: String = r.get_item("body")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "No description available.".to_string());
        results.push(format!("### {}\nURL: {}\n{}\n", title, href, body));
    }
    Ok(results)
}

/// Combines list of results into a single string with a provider-specific indicator.
#[pyfunction]
pub fn format_results_block(results: Vec<String>, provider: &str) -> PyResult<String> {
    if results.is_empty() {
        return Ok(format!("No {} results found.", provider));
    }
    Ok(results.join("\n"))
}

// === SimulationCore Implementations ===

use rand::seq::SliceRandom;
use rand::Rng;

/// Returns a list of agent indices that are designated to 'fail' (Phase 181).
#[pyfunction]
pub fn calculate_stochastic_failures(agent_count: usize, failure_rate: f64) -> PyResult<Vec<usize>> {
    let mut rng = rand::thread_rng();
    let num_failures = (agent_count as f64 * failure_rate) as usize;
    let mut indices: Vec<usize> = (0..agent_count).collect();
    indices.shuffle(&mut rng);
    Ok(indices.into_iter().take(num_failures).collect())
}

/// Simulates network/hardware jitter by adding a random spike.
#[pyfunction]
pub fn apply_latency_spike(base_latency: f64, spike_probability: f64) -> PyResult<f64> {
    let mut rng = rand::thread_rng();
    if rng.gen_bool(spike_probability) {
        Ok(base_latency * (1.5 + rng.gen_range(0.0..2.0)))
    } else {
        Ok(base_latency)
    }
}

/// Generates a simple ASCII progress bar.
#[pyfunction]
pub fn format_progress_bar(current: usize, total: usize, width: usize) -> PyResult<String> {
    if total == 0 { return Ok("[] 0% (0/0)".to_string()); }
    let percent = current as f64 / total as f64;
    let filled = (width as f64 * percent) as usize;
    let bar = "=".repeat(filled) + &"-".repeat(width - filled);
    Ok(format!("[{}] {:3.0}% ({}/{})", bar, percent * 100.0, current, total))
}

/// Generates an OpenAPI 3.0 spec string from tool definitions.
#[pyfunction]
pub fn generate_openapi_spec(tool_definitions: Vec<Bound<'_, PyDict>>, version: &str) -> PyResult<String> {
    let mut paths = Vec::new();
    
    for tool in tool_definitions {
        let name: String = tool.get_item("name")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "unknown".to_string());
        let properties: String = r#"{"input": {"type": "string"}}"#.to_string(); // Simplified for now
        
        paths.push(format!(
            r#""/tools/{}": {{ "post": {{ "summary": "Execute {}", "operationId": "{}", "requestBody": {{ "content": {{ "application/json": {{ "schema": {{ "type": "object", "properties": {} }} }} }} }}, "responses": {{ "200": {{ "description": "OK" }} }} }} }}"#,
            name, name, name, properties
        ));
    }

    Ok(format!(
        r#"{{ "openapi": "3.0.0", "info": {{ "title": "PyAgent Fleet API", "version": "{}" }}, "paths": {{ {} }} }}"#,
        version,
        paths.join(", ")
    ))
}

#[pyfunction]
pub fn score_tool_relevance(name: &str, description: &str, query: &str) -> PyResult<f64> {
    let query_lower = query.to_lowercase();
    let name_lower = name.to_lowercase();
    let desc_lower = description.to_lowercase();
    let mut score = 0.0;

    if query_lower.contains(&name_lower) {
        score += 10.0;
    }

    let re = regex::Regex::new(r"\w+").unwrap();
    let desc_words: std::collections::HashSet<&str> = re.find_iter(&desc_lower).map(|m| m.as_str()).collect();
    let query_words: std::collections::HashSet<&str> = re.find_iter(&query_lower).map(|m| m.as_str()).collect();

    let common_count = desc_words.intersection(&query_words).count();
    score += common_count as f64 * 2.0;

    Ok(score)
}

/// Ensures script starts with common safety flags (`set -euo pipefail`) if not present (BashCore).
#[pyfunction]
pub fn ensure_safety_flags_rust(content: &str) -> PyResult<String> {
    let header = "set -euo pipefail";
    
    if content.contains(header) {
        return Ok(content.to_string());
    }

    let lines: Vec<&str> = content.lines().collect();
    // Check if empty
    if lines.is_empty() {
        return Ok(format!("#!/bin/bash\n{}\n\n", header));
    }

    // Insert after shebang if present
    if lines[0].starts_with("#!") {
        if lines.len() > 1 {
            // Reconstruct content to insert efficiently? 
            // String manipulation in Rust:
            let mut result = String::with_capacity(content.len() + header.len() + 10);
            result.push_str(lines[0]);
            result.push('\n');
            result.push('\n'); // Extra newline for style
            result.push_str(header);
            result.push('\n');
            for line in &lines[1..] {
                result.push_str(line);
                result.push('\n');
            }
            // Trim trailing newline if original didn't have one? 
            // For bash scripts, trailing newline is good.
            return Ok(result);
        } else {
             return Ok(format!("{}\n\n{}\n", lines[0], header));
        }
    }

    // No shebang, just prepend
    Ok(format!("#!/bin/bash\n{}\n\n{}", header, content))
}

/// Parses `adb devices` output to list connected device serials (AndroidCore).
#[pyfunction]
pub fn parse_adb_devices_rust(output: &str) -> PyResult<Vec<String>> {
    let mut devices = Vec::new();
    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with("List of devices") {
            continue;
        }
        
        let parts: Vec<&str> = trimmed.split_whitespace().collect();
        if parts.len() >= 2 {
            if parts[1] == "device" {
                devices.push(parts[0].to_string());
            }
        }
    }
    Ok(devices)
}

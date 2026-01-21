// cspell:ignore peekable walkdir pipefail halstead signum dtype nbytes RUNPOD
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::{HashMap, HashSet};

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

/// Evaluate a math formula with variables using a minimal hand-written parser.
/// This is a safe, dependency-free Rust core for FormulaEngineCore parity.
#[pyfunction]
pub fn evaluate_formula(formula: &str, variables: HashMap<String, f64>) -> PyResult<f64> {
    let mut expr = formula.to_string();

    // Replace {var} placeholders with numeric values
    for (k, v) in variables.iter() {
        let placeholder = format!("{{{}}}", k);
        expr = expr.replace(&placeholder, &v.to_string());
    }

    match mini_eval(&expr) {
        Ok(val) => Ok(val),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e)),
    }
}

/// Simple recursive descent parser for basic math (+ - * / ^ ( ))
fn mini_eval(expr: &str) -> Result<f64, String> {
    let mut it = expr.chars().filter(|c| !c.is_whitespace()).peekable();
    parse_expr(&mut it)
}

fn parse_expr<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let mut val = parse_term(it)?;
    while let Some(&c) = it.peek() {
        match c {
            '+' => {
                it.next();
                val += parse_term(it)?;
            }
            '-' => {
                it.next();
                val -= parse_term(it)?;
            }
            _ => break,
        }
    }
    Ok(val)
}

fn parse_term<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let mut val = parse_power(it)?;
    while let Some(&c) = it.peek() {
        match c {
            '*' => {
                it.next();
                val *= parse_power(it)?;
            }
            '/' => {
                it.next();
                let div = parse_power(it)?;
                if div == 0.0 {
                    return Err("Division by zero".into());
                }
                val /= div;
            }
            _ => break,
        }
    }
    Ok(val)
}

fn parse_power<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let val = parse_factor(it)?;
    if let Some(&'^') = it.peek() {
        it.next();
        Ok(val.powf(parse_power(it)?)) // Right-associative
    } else {
        Ok(val)
    }
}

fn parse_factor<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    match it.next() {
        Some('(') => {
            let val = parse_expr(it)?;
            if it.next() != Some(')') {
                return Err("Missing closing parenthesis".into());
            }
            Ok(val)
        }
        Some('-') => Ok(-parse_factor(it)?),
        Some('+') => Ok(parse_factor(it)?),
        Some(c) if c.is_digit(10) || c == '.' => {
            let mut s = c.to_string();
            while let Some(&c) = it.peek() {
                if c.is_digit(10) || c == '.' || c == 'e' || c == 'E' {
                    s.push(it.next().unwrap());
                } else if (c == '+' || c == '-') && (s.ends_with('e') || s.ends_with('E')) {
                    s.push(it.next().unwrap());
                } else {
                    break;
                }
            }
            s.parse::<f64>().map_err(|_| format!("Invalid number: {}", s))
        }
        Some(c) => Err(format!("Unexpected character: {}", c)),
        None => Err("Unexpected end of expression".into()),
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
) -> PyResult<HashMap<String, String>> {
    let mut result = HashMap::new();
    
    fn recurse(
        dict: &Bound<'_, pyo3::types::PyDict>,
        current_prefix: &str,
        acc: &mut HashMap<String, String>
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
    
    let mut targets = Vec::new();
    for entry in WalkDir::new(root_dir).into_iter().filter_map(|e| e.ok()) {
         if entry.file_type().is_dir() && entry.file_name() == "__pycache__" {
             targets.push(entry.path().to_owned());
         }
    }

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
        let properties = r#"{"input": {"type": "string"}}"#;
        
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
    let desc_words: HashSet<&str> = re.find_iter(&desc_lower).map(|m| m.as_str()).collect();
    let query_words: HashSet<&str> = re.find_iter(&query_lower).map(|m| m.as_str()).collect();

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
    if lines.is_empty() {
        return Ok(format!("#!/bin/bash\n{}\n\n", header));
    }

    if lines[0].starts_with("#!") {
        if lines.len() > 1 {
            let mut result = String::with_capacity(content.len() + header.len() + 10);
            result.push_str(lines[0]);
            result.push_str("\n\n");
            result.push_str(header);
            result.push('\n');
            for line in &lines[1..] {
                result.push_str(line);
                result.push('\n');
            }
            return Ok(result);
        } else {
             return Ok(format!("{}\n\n{}\n", lines[0], header));
        }
    }

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

/// Calculate code health metrics for Python files (Phase 318).
#[pyfunction]
pub fn calculate_metrics_rust(content: &str) -> PyResult<HashMap<String, f64>> {
    let mut results = HashMap::new();
    let mut loc = 0.0;
    let mut comments = 0.0;
    let mut blanks = 0.0;
    let mut cc = 1.0;
    let mut func_count = 0.0;
    let mut class_count = 0.0;
    let mut import_count = 0.0;

    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            blanks += 1.0;
        } else if trimmed.starts_with('#') || trimmed.starts_with("//") {
            comments += 1.0;
        } else {
            loc += 1.0;
        }
    }

    // Cyclomatic Complexity decision points (C901 approximation)
    let re_cc = regex::Regex::new(r"(?:\bif\b|\bwhile\b|\bfor\b|\bexcept\b|\band\b|\bor\b)").unwrap();
    let re_func = regex::Regex::new(r"(?m)^\s*(?:async\s+)?def\s+").unwrap();
    let re_class = regex::Regex::new(r"(?m)^\s*class\s+").unwrap();
    let re_import = regex::Regex::new(r"(?m)^\s*(?:from|import)\s+").unwrap();

    cc += re_cc.find_iter(content).count() as f64;
    func_count += re_func.find_iter(content).count() as f64;
    class_count += re_class.find_iter(content).count() as f64;
    import_count += re_import.find_iter(content).count() as f64;

    // Maintainability Index (MI)
    let halstead_volume = loc * (func_count + class_count + 1.0).log10() / 2.0_f64.log10(); // log2
    let mi = 171.0 
        - 5.2 * (halstead_volume + 1.0).ln() 
        - 0.23 * cc 
        - 16.2 * (loc + 1.0).ln() 
        + 50.0 * ( (2.4 * (comments / (loc + comments + 1.0))).sqrt() ).sin();

    results.insert("lines_of_code".to_string(), loc);
    results.insert("lines_of_comments".to_string(), comments);
    results.insert("blank_lines".to_string(), blanks);
    results.insert("cyclomatic_complexity".to_string(), cc);
    results.insert("function_count".to_string(), func_count);
    results.insert("class_count".to_string(), class_count);
    results.insert("import_count".to_string(), import_count);
    results.insert("maintainability_index".to_string(), mi.max(0.0).min(100.0));

    Ok(results)
}

/// MD5 sharding for InteractionRegistry (Phase 318).
#[pyfunction]
pub fn calculate_interaction_shard_md5(key: &str, shard_count: usize) -> PyResult<usize> {
    use md5::{Md5, Digest};
    let mut hasher = Md5::new();
    hasher.update(key.as_bytes());
    let result = hasher.finalize();
    
    let mut seed_bytes = [0u8; 8];
    seed_bytes.copy_from_slice(&result[..8]);
    let seed = u64::from_be_bytes(seed_bytes);
    
    Ok((seed as usize) % shard_count)
}

// ============================================================
// Phase 17: vLLM-Inspired Math & Utility Functions
// ============================================================

/// Ceiling division without floating point.
/// Uses: (a + b - 1) / b for positive values, which gives ceiling division.
#[pyfunction]
pub fn cdiv_rust(a: i64, b: i64) -> PyResult<i64> {
    if b == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("division by zero"));
    }
    // For ceiling division: (a + b - 1) / b for positive a and b
    // General formula that works for any signs:
    if (a >= 0 && b > 0) || (a <= 0 && b < 0) {
        // Same sign: ceiling is (a + b - sign(b)) / b
        Ok((a + b - b.signum()) / b)
    } else {
        // Different signs: regular division already truncates toward zero
        Ok(a / b)
    }
}

/// Return the smallest power of 2 >= n.
#[pyfunction]
pub fn next_power_of_2_rust(n: u64) -> PyResult<u64> {
    if n == 0 {
        return Ok(1);
    }
    if n & (n - 1) == 0 {
        return Ok(n);  // Already a power of 2
    }
    Ok(1u64 << (64 - n.leading_zeros()))
}

/// Return the largest power of 2 <= n (inclusive).
#[pyfunction]
pub fn prev_power_of_2_rust(n: u64) -> PyResult<u64> {
    if n == 0 {
        return Ok(1);
    }
    Ok(1u64 << (63 - n.leading_zeros()))
}

/// Round n up to the nearest multiple.
#[pyfunction]
pub fn round_up_rust(n: i64, multiple: i64) -> PyResult<i64> {
    if multiple == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("multiple cannot be zero"));
    }
    let abs_multiple = multiple.abs();
    // (n + multiple - 1) / multiple * multiple for positive, but we use cdiv
    let cdiv_val = if (n >= 0 && abs_multiple > 0) || (n <= 0 && multiple < 0) {
        (n + abs_multiple - 1) / abs_multiple
    } else if n == 0 {
        0
    } else {
        n / abs_multiple
    };
    Ok(cdiv_val * abs_multiple)
}

/// Round n down to the nearest multiple.
#[pyfunction]
pub fn round_down_rust(n: i64, multiple: i64) -> PyResult<i64> {
    if multiple == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("multiple cannot be zero"));
    }
    Ok((n / multiple) * multiple)
}

/// Atomic counter add operation (placeholder for actual atomic).
#[pyfunction]
pub fn atomic_counter_add_rust(current: i64, delta: i64) -> PyResult<i64> {
    Ok(current + delta)
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

/// Calculate cache hit ratio from hits and total.
#[pyfunction]
pub fn cache_hit_ratio_rust(hits: u64, total: u64) -> PyResult<f64> {
    if total == 0 {
        return Ok(0.0);
    }
    Ok(hits as f64 / total as f64)
}

/// Batch ceiling division for multiple values.
#[pyfunction]
pub fn batch_cdiv_rust(values: Vec<i64>, divisor: i64) -> PyResult<Vec<i64>> {
    if divisor == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("division by zero"));
    }
    Ok(values.into_iter().map(|a| -(a / -divisor)).collect())
}

/// Batch next_power_of_2 for multiple values.
#[pyfunction]
pub fn batch_next_power_of_2_rust(values: Vec<u64>) -> PyResult<Vec<u64>> {
    Ok(values.into_iter().map(|n| {
        if n == 0 {
            1
        } else if n & (n - 1) == 0 {
            n
        } else {
            1u64 << (64 - n.leading_zeros())
        }
    }).collect())
}

// ============================================================================
// Phase 22: JSONTree Utilities
// ============================================================================

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

// ============================================================================
// Phase 23: Advanced Serialization & Validation
// ============================================================================

/// Encode tensor metadata for msgpack (dtype, shape).
/// Returns a tuple of (dtype_str, shape_tuple) for zero-copy serialization.
#[pyfunction]
pub fn msgpack_encode_tensor_meta_rust(
    dtype: &str,
    shape: Vec<i64>,
    nbytes: usize,
    threshold: usize,
) -> PyResult<(String, Vec<i64>, bool)> {
    // Determine if tensor should be inlined or referenced
    let inline = nbytes < threshold;
    Ok((dtype.to_string(), shape, inline))
}

/// Validate a tensor shape against expected dimensions with symbolic names.
/// bindings maps symbolic names to expected values.
/// Returns (valid, collected_bindings).
#[pyfunction]
pub fn validate_tensor_shape_rust(
    actual_shape: Vec<i64>,
    expected: Vec<String>,
    bindings: HashMap<String, i64>,
    dynamic_dims: HashSet<String>,
) -> PyResult<(bool, HashMap<String, i64>)> {
    if actual_shape.len() != expected.len() {
        return Ok((false, bindings));
    }
    
    let mut collected = bindings.clone();
    
    for (actual, exp) in actual_shape.iter().zip(expected.iter()) {
        // Try to parse as integer
        if let Ok(expected_val) = exp.parse::<i64>() {
            if *actual != expected_val {
                return Ok((false, collected));
            }
        } else {
            // Symbolic dimension
            if dynamic_dims.contains(exp) {
                // Dynamic dims always pass, but collect binding
                collected.insert(exp.clone(), *actual);
            } else if let Some(&bound_val) = collected.get(exp) {
                // Check against bound value
                if *actual != bound_val {
                    return Ok((false, collected));
                }
            } else {
                // New symbolic dim, collect binding
                collected.insert(exp.clone(), *actual);
            }
        }
    }
    
    Ok((true, collected))
}

/// Apply temperature scaling to logits vector.
/// Returns scaled logits.
#[pyfunction]
pub fn apply_temperature_rust(logits: Vec<f32>, temperature: f32) -> PyResult<Vec<f32>> {
    if temperature == 1.0 {
        return Ok(logits);
    }
    
    Ok(logits.into_iter().map(|l| l / temperature).collect())
}

/// Apply top-k filtering - set all but top k logits to -inf.
#[pyfunction]
pub fn apply_top_k_rust(mut logits: Vec<f32>, k: usize) -> PyResult<Vec<f32>> {
    if k >= logits.len() {
        return Ok(logits);
    }
    
    // Find kth largest value
    let mut sorted = logits.clone();
    sorted.sort_by(|a, b| b.partial_cmp(a).unwrap_or(std::cmp::Ordering::Equal));
    let threshold = sorted[k - 1];
    
    // Mask values below threshold
    for l in logits.iter_mut() {
        if *l < threshold {
            *l = f32::NEG_INFINITY;
        }
    }
    
    Ok(logits)
}

/// Apply repetition penalty to logits for tokens that have appeared.
#[pyfunction]
pub fn apply_repetition_penalty_rust(
    mut logits: Vec<f32>,
    input_ids: Vec<usize>,
    penalty: f32,
) -> PyResult<Vec<f32>> {
    if penalty == 1.0 {
        return Ok(logits);
    }
    
    let seen: HashSet<usize> = input_ids.into_iter().collect();
    
    for token_id in seen {
        if token_id < logits.len() {
            if logits[token_id] > 0.0 {
                logits[token_id] /= penalty;
            } else {
                logits[token_id] *= penalty;
            }
        }
    }
    
    Ok(logits)
}

/// Compute a mask for bad words - returns indices that should be set to -inf.
#[pyfunction]
pub fn compute_logits_mask_rust(
    input_ids: Vec<usize>,
    bad_words_ids: Vec<Vec<usize>>,
    vocab_size: usize,
) -> PyResult<Vec<usize>> {
    let mut mask = Vec::new();
    
    for bad_word in bad_words_ids.iter() {
        if bad_word.is_empty() {
            continue;
        }
        
        if bad_word.len() == 1 {
            // Single token bad word
            let token_id = bad_word[0];
            if token_id < vocab_size && !mask.contains(&token_id) {
                mask.push(token_id);
            }
        } else {
            // Multi-token sequence
            let prefix_len = bad_word.len() - 1;
            if input_ids.len() >= prefix_len {
                let actual_prefix = &input_ids[input_ids.len() - prefix_len..];
                let expected_prefix = &bad_word[..prefix_len];
                
                if actual_prefix == expected_prefix {
                    let last_token = bad_word[bad_word.len() - 1];
                    if last_token < vocab_size && !mask.contains(&last_token) {
                        mask.push(last_token);
                    }
                }
            }
        }
    }
    
    Ok(mask)
}

/// Serialize a slice/range as a tuple for msgpack.
#[pyfunction]
pub fn encode_slice_rust(start: Option<i64>, stop: Option<i64>, step: Option<i64>) -> PyResult<(Option<i64>, Option<i64>, Option<i64>)> {
    Ok((start, stop, step))
}

// ============================================================================
// Phase 24: Advanced Observability & Parsing
// ============================================================================

/// Fast diff computation between two counter snapshots.
/// Returns a HashMap of field names to their differences.
#[pyfunction]
pub fn structured_counter_diff_rust(
    current: HashMap<String, i64>,
    baseline: HashMap<String, i64>,
) -> PyResult<HashMap<String, i64>> {
    let mut diff = HashMap::new();
    
    for (key, current_val) in current.iter() {
        let baseline_val = baseline.get(key).unwrap_or(&0);
        let delta = current_val - baseline_val;
        if delta != 0 {
            diff.insert(key.clone(), delta);
        }
    }
    
    // Check for keys only in baseline (negative diffs)
    for (key, baseline_val) in baseline.iter() {
        if !current.contains_key(key) && *baseline_val != 0 {
            diff.insert(key.clone(), -baseline_val);
        }
    }
    
    Ok(diff)
}

/// Fast append for FlatLogprobs - returns new end index.
#[pyfunction]
pub fn flat_logprobs_append_rust(
    token_ids: Vec<i64>,
    _logprobs: Vec<f64>,
    _ranks: Vec<Option<i32>>,
    current_length: usize,
) -> PyResult<(usize, usize)> {
    let start_idx = current_length;
    let end_idx = current_length + token_ids.len();
    Ok((start_idx, end_idx))
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

/// Fast deduplication of log messages using a bloom filter approximation.
/// Returns indices of messages that should be logged (first occurrence).
#[pyfunction]
pub fn dedupe_log_messages_rust(
    messages: Vec<String>,
) -> PyResult<Vec<usize>> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    
    for (idx, msg) in messages.iter().enumerate() {
        // Use hash for faster lookup
        let hash = fast_hash_inner(msg);
        if !seen.contains(&hash) {
            seen.insert(hash);
            result.push(idx);
        }
    }
    
    Ok(result)
}

// Helper for fast hashing
fn fast_hash_inner(key: &str) -> u64 {
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in key.as_bytes() {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

/// Detect cloud provider from environment variables.
/// Returns provider name or "UNKNOWN".
#[pyfunction]
pub fn detect_cloud_provider_rust(
    env_vars: HashMap<String, String>,
) -> PyResult<String> {
    let env_to_provider = [
        ("AWS_REGION", "AWS"),
        ("AWS_EXECUTION_ENV", "AWS"),
        ("AZURE_HTTP_USER_AGENT", "AZURE"),
        ("GOOGLE_CLOUD_PROJECT", "GCP"),
        ("RUNPOD_DC_ID", "RUNPOD"),
        ("LAMBDA_LABS_ENV", "LAMBDA"),
        ("DIGITALOCEAN_ACCESS_TOKEN", "DIGITALOCEAN"),
        ("LINODE_TOKEN", "LINODE"),
    ];
    
    for (env_var, provider) in env_to_provider.iter() {
        if env_vars.contains_key(*env_var) {
            return Ok(provider.to_string());
        }
    }
    
    Ok("UNKNOWN".to_string())
}

/// Validate prompt structure and return error messages.
#[pyfunction]
pub fn validate_prompt_rust(
    prompt_type: &str,
    has_text: bool,
    has_token_ids: bool,
    has_embeds: bool,
    token_count: usize,
) -> PyResult<Vec<String>> {
    let mut errors = Vec::new();
    
    match prompt_type {
        "text" => {
            if !has_text {
                errors.push("Empty prompt text in TextPrompt".to_string());
            }
        }
        "tokens" => {
            if !has_token_ids || token_count == 0 {
                errors.push("Empty token_ids in TokensPrompt".to_string());
            }
        }
        "embeds" => {
            if !has_embeds {
                errors.push("Missing prompt_embeds in EmbedsPrompt".to_string());
            }
        }
        _ => {
            errors.push(format!("Unknown prompt type: {}", prompt_type));
        }
    }
    
    Ok(errors)
}

/// Parse tool call from XML format.
/// Returns (name, arguments_json) or None.
#[pyfunction]
pub fn parse_xml_tool_call_rust(
    xml_content: &str,
) -> PyResult<Option<(String, String)>> {
    // Simple regex-like parsing for <name>...</name> and <arguments>...</arguments>
    let name_start = xml_content.find("<name>");
    let name_end = xml_content.find("</name>");
    let args_start = xml_content.find("<arguments>");
    let args_end = xml_content.find("</arguments>");
    
    if let (Some(ns), Some(ne), Some(as_), Some(ae)) = (name_start, name_end, args_start, args_end) {
        if ns < ne && as_ < ae {
            let name = xml_content[ns + 6..ne].trim().to_string();
            let args = xml_content[as_ + 11..ae].trim().to_string();
            return Ok(Some((name, args)));
        }
    }
    
    Ok(None)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(apply_latency_spike, m)?)?;
    m.add_function(wrap_pyfunction!(apply_repetition_penalty_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_temperature_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_top_k_rust, m)?)?;
    m.add_function(wrap_pyfunction!(atomic_counter_add_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_cdiv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_next_power_of_2_rust, m)?)?;
    m.add_function(wrap_pyfunction!(cache_hit_ratio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_interaction_shard_md5, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_stochastic_failures, m)?)?;
    m.add_function(wrap_pyfunction!(cdiv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compress_python_regex, m)?)?;
    m.add_function(wrap_pyfunction!(compute_logits_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(dedupe_log_messages_rust, m)?)?;
    m.add_function(wrap_pyfunction!(deep_clean_pycache_rust, m)?)?;
    m.add_function(wrap_pyfunction!(detect_cloud_provider_rust, m)?)?;
    m.add_function(wrap_pyfunction!(encode_slice_rust, m)?)?;
    m.add_function(wrap_pyfunction!(ensure_safety_flags_rust, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_formula, m)?)?;
    m.add_function(wrap_pyfunction!(extract_json_tool_calls_rust, m)?)?;
    m.add_function(wrap_pyfunction!(fast_cache_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(fast_hash, m)?)?;
    m.add_function(wrap_pyfunction!(flat_logprobs_append_rust, m)?)?;
    m.add_function(wrap_pyfunction!(flatten_env_vars, m)?)?;
    m.add_function(wrap_pyfunction!(format_progress_bar, m)?)?;
    m.add_function(wrap_pyfunction!(format_results_block, m)?)?;
    m.add_function(wrap_pyfunction!(generate_openapi_spec, m)?)?;
    m.add_function(wrap_pyfunction!(json_count_leaves_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_depth_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_flatten_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_get_path_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_iter_leaves_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_validate_leaves_rust, m)?)?;
    m.add_function(wrap_pyfunction!(msgpack_encode_tensor_meta_rust, m)?)?;
    m.add_function(wrap_pyfunction!(next_power_of_2_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_adb_devices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_bing_results, m)?)?;
    m.add_function(wrap_pyfunction!(parse_ddg_results, m)?)?;
    m.add_function(wrap_pyfunction!(parse_google_results, m)?)?;
    m.add_function(wrap_pyfunction!(parse_xml_tool_call_rust, m)?)?;
    m.add_function(wrap_pyfunction!(prev_power_of_2_rust, m)?)?;
    m.add_function(wrap_pyfunction!(prune_directory_rust, m)?)?;
    m.add_function(wrap_pyfunction!(round_down_rust, m)?)?;
    m.add_function(wrap_pyfunction!(round_up_rust, m)?)?;
    m.add_function(wrap_pyfunction!(score_tool_relevance, m)?)?;
    m.add_function(wrap_pyfunction!(structured_counter_diff_rust, m)?)?;
    m.add_function(wrap_pyfunction!(summarize_markdown, m)?)?;
    m.add_function(wrap_pyfunction!(validate_prompt_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_tensor_shape_rust, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_rust, m)?)?;
    Ok(())
}

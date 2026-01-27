use pyo3::prelude::*;
use std::collections::HashSet;

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

#[pyfunction]
pub fn find_literal_rust(content: &str, search: &str) -> PyResult<i64> {
    // Phase 130: Optimized string search (KMP-lite)
    match content.find(search) {
        Some(pos) => Ok(pos as i64),
        None => Ok(-1),
    }
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

/// Generates a simple ASCII progress bar.
#[pyfunction]
pub fn format_progress_bar(current: usize, total: usize, width: usize) -> PyResult<String> {
    if total == 0 { return Ok("[] 0% (0/0)".to_string()); }
    let percent = current as f64 / total as f64;
    let filled = (width as f64 * percent) as usize;
    let bar = "=".repeat(filled) + &"-".repeat(width - filled);
    Ok(format!("[{}] {:3.0}% ({}/{})", bar, percent * 100.0, current, total))
}

/// Combines list of results into a single string with a provider-specific indicator.
#[pyfunction]
pub fn format_results_block(results: Vec<String>, provider: &str) -> PyResult<String> {
    if results.is_empty() {
        return Ok(format!("No {} results found.", provider));
    }
    Ok(results.join("\n"))
}

/// Estimate token count using heuristic
#[pyfunction]
pub fn estimate_tokens_rust(text: &str) -> usize {
    // Simple heuristic: words * 1.3 + special handling
    let words = text.split_whitespace().count();
    let symbols = text.chars().filter(|c| !c.is_alphanumeric() && !c.is_whitespace()).count();

    (words as f64 * 1.3 + symbols as f64 * 0.5) as usize
}

/// Convert CamelCase to snake_case (AgentRegistryCore, OrchestratorRegistryCore).
/// High-frequency function (~300 calls) during registry scanning.
#[pyfunction]
pub fn to_snake_case_rust(name: &str) -> PyResult<String> {
    static RE1: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static RE2: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let re1 = RE1.get_or_init(|| {
        regex::Regex::new(r"(.)([A-Z][a-z]+)").unwrap()
    });

    let re2 = RE2.get_or_init(|| {
        regex::Regex::new(r"([a-z0-9])([A-Z])").unwrap()
    });

    let s1 = re1.replace_all(name, "${1}_${2}");
    let s2 = re2.replace_all(&s1, "${1}_${2}");
    Ok(s2.to_lowercase())
}


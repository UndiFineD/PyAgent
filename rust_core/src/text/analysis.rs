use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;

#[pyfunction]
pub fn analyze_code_quality_rust(
    file_path: &str,
    content: &str,
) -> PyResult<HashMap<String, f64>> {
    analyze_code_quality_internal(file_path, content)
}

fn analyze_code_quality_internal(
    _file_path: &str,
    content: &str,
) -> PyResult<HashMap<String, f64>> {
    let mut metrics: HashMap<String, f64> = HashMap::new();
    
    // Lines of code
    let loc = content.lines().count() as f64;
    metrics.insert("loc".to_string(), loc);
    
    // Comment ratio
    let comment_lines = content.lines().filter(|l| l.trim().starts_with('#') || l.trim().starts_with("//")).count() as f64;
    if loc > 0.0 {
        metrics.insert("comment_ratio".to_string(), comment_lines / loc);
    } else {
        metrics.insert("comment_ratio".to_string(), 0.0);
    }
    
    // TODO function count
    let todo_count = content.to_lowercase().matches("todo").count() as f64;
    metrics.insert("todo_count".to_string(), todo_count);
    
    Ok(metrics)
}

#[pyfunction]
pub fn count_untyped_functions_rust(content: &str) -> PyResult<usize> {
    // Basic heuristic: check for function definitions
    // Count all "def name(" occurences
    let def_regex = Regex::new(r"def\s+\w+\s*\(").unwrap();
    // Count "def name(...) ->" occurrences
    let typed_regex = Regex::new(r"def\s+\w+\s*\([^)]*\)\s*->").unwrap();
    
    let defs = def_regex.find_iter(content).count();
    let typed = typed_regex.find_iter(content).count();
    
    // Ensure we don't underflow if typed regex somehow matches more than defs (unlikely)
    Ok(defs.saturating_sub(typed))
}

#[pyfunction]
pub fn find_duplicate_code_rust(
    files: HashMap<String, String>,
    min_lines: usize,
) -> PyResult<Vec<(String, String, usize)>> {
    let mut duplicates = Vec::new();
    
    // Very simplified block hash comparison
    let mut blocks: HashMap<u64, Vec<(String, usize)>> = HashMap::new();
    
    for (path, content) in &files {
        let lines: Vec<&str> = content.lines().collect();
        if lines.len() < min_lines {
            continue;
        }
        
        for i in 0..=(lines.len() - min_lines) {
            let window = &lines[i..i+min_lines];
            let joined = window.join("\n");
            
            // Simple hash
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            
            let mut hasher = DefaultHasher::new();
            joined.hash(&mut hasher);
            let hash = hasher.finish();
            
            blocks.entry(hash).or_default().push((path.clone(), i));
        }
    }
    
    for (_, locations) in blocks {
        if locations.len() > 1 {
           // We have duplicates
           // Just report pairs for now
           for i in 0..locations.len() {
               for j in (i+1)..locations.len() {
                   duplicates.push((locations[i].0.clone(), locations[j].0.clone(), locations[i].1));
               }
           }
        }
    }
    
    // Deduplicate the result list
    duplicates.sort(); 
    duplicates.dedup();
    
    Ok(duplicates)
}

#[pyfunction]
pub fn analyze_tech_debt_rust(
    content: &str,
) -> PyResult<HashMap<String, usize>> {
    let mut debt: HashMap<String, usize> = HashMap::new();
    
    let markers = vec!["TODO", "FIXME", "HACK", "XXX", "BUG"];
    
    for marker in markers {
        let count = content.matches(marker).count();
        if count > 0 {
            debt.insert(marker.to_string(), count);
        }
    }
    
    Ok(debt)
}

#[pyfunction]
pub fn analyze_security_patterns_rust(
    content: &str,
    patterns: HashMap<String, String>,
) -> PyResult<Vec<(String, usize, String)>> {
    let mut risks = Vec::new();
    
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|(name, p)| Regex::new(&p).ok().map(|r| (name, r)))
        .collect();
        
    for (i, line) in content.lines().enumerate() {
        for (name, regex) in &regexes {
            if regex.is_match(line) {
                risks.push((name.clone(), i + 1, line.trim().to_string()));
            }
        }
    }
    
    Ok(risks)
}

#[pyfunction]
pub fn calculate_complexity_rust(content: &str) -> PyResult<f64> {
    // Simple cyclomatic complexity approximation
    // Count branching keywords
    let keywords = vec!["if ", "else", "elif", "for ", "while ", "try", "except", "case ", "match "];
    
    let mut complexity = 1.0;
    
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("#") { continue; }
        
        for kw in &keywords {
            // Very naive check, but fast
            if trimmed.contains(kw) {
                complexity += 1.0;
            }
        }
    }
    
    Ok(complexity)
}

#[pyfunction]
pub fn prepare_debt_records_rust(
    files: HashMap<String, String>,
) -> PyResult<Vec<(String, String, usize, String)>> {
    let mut records = Vec::new();
    let markers = vec!["TODO", "FIXME", "HACK"];
    
    for (path, content) in files {
        for (i, line) in content.lines().enumerate() {
            for marker in &markers {
                if line.contains(marker) {
                    records.push((path.clone(), marker.to_string(), i + 1, line.trim().to_string()));
                }
            }
        }
    }
    
    Ok(records)
}

#[pyfunction]
pub fn validate_semver_rust(version: &str) -> PyResult<bool> {
    let re = Regex::new(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$").unwrap();
    Ok(re.is_match(version))
}

#[pyfunction]
pub fn analyze_failure_strategy_rust(
    logs: Vec<String>,
) -> PyResult<String> {
    // Heuristic analysis of logs to determine failure pattern
    let log_content = logs.join("\n");
    let lower = log_content.to_lowercase();
    
    if lower.contains("timeout") {
        Ok("timeout".to_string())
    } else if lower.contains("memory") || lower.contains("oom") {
        Ok("resource_exhaustion".to_string())
    } else if lower.contains("syntax") || lower.contains("parse error") {
        Ok("syntax_error".to_string())
    } else {
        Ok("unknown".to_string())
    }
}

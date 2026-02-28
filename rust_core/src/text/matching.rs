use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;
use std::fs;
use walkdir::WalkDir;
use rayon::prelude::*;

/// Match a list of regex patterns against content.
/// Returns the index of the first pattern resulting in a match, or -1.
#[pyfunction]
pub fn match_patterns_rust(
    content: &str,
    patterns: Vec<String>,
) -> PyResult<i64> {
    for (idx, pattern) in patterns.iter().enumerate() {
        if let Ok(regex) = Regex::new(pattern) {
             if regex.is_match(content) {
                 return Ok(idx as i64);
             }
        }
    }
    Ok(-1)
}

/// Bulk match patterns across multiple contents.
#[pyfunction]
pub fn bulk_match_patterns_rust(
    patterns: Vec<String>,
    contents: Vec<String>,
) -> PyResult<Vec<HashMap<String, Vec<String>>>> {
    // Compile regexes once
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|p| Regex::new(&p).ok().map(|r| (p, r)))
        .collect();
    
    let results: Vec<HashMap<String, Vec<String>>> = contents
        .par_iter() // Parallel iteration
        .map(|content| {
            let mut file_results = HashMap::new();
            for (pattern, regex) in &regexes {
                let matches: Vec<String> = regex
                    .find_iter(content)
                    .map(|m| m.as_str().to_string())
                    .collect();
                
                if !matches.is_empty() {
                    file_results.insert(pattern.clone(), matches);
                }
            }
            file_results
        })
        .collect();
    
    Ok(results)
}

/// Check content for suppression comments.
#[pyfunction]
pub fn check_suppression_rust(
    content: &str,
    suppression_marker: &str,
    lines_context: usize,
) -> PyResult<Vec<usize>> {
    let mut suppressed_lines = Vec::new();
    let lines: Vec<&str> = content.lines().collect();
    
    for (i, line) in lines.iter().enumerate() {
        if line.contains(suppression_marker) {
            // Mark lines within context range as suppressed
            let start = i.saturating_sub(lines_context);
            let end = (i + lines_context + 1).min(lines.len());
            for j in start..end {
                suppressed_lines.push(j + 1); // 1-based indexing
            }
        }
    }
    
    suppressed_lines.sort_unstable();
    suppressed_lines.dedup();
    
    Ok(suppressed_lines)
}

/// Scan lines for multiple patterns.
#[pyfunction]
pub fn scan_lines_multi_pattern_rust(
    content: &str,
    patterns: HashMap<String, String>,
) -> PyResult<Vec<(usize, String, String)>> {
    let mut results = Vec::new();
    
    // Compile regexes
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|(name, p)| Regex::new(&p).ok().map(|r| (name, r)))
        .collect();
    
    for (i, line) in content.lines().enumerate() {
        for (name, regex) in &regexes {
            if regex.is_match(line) {
                results.push((i + 1, name.clone(), line.trim().to_string()));
            }
        }
    }
    
    Ok(results)
}

/// Batch scan files for patterns.
#[pyfunction]
pub fn batch_scan_files_rust(
    file_map: HashMap<String, String>, // path -> content
    patterns: HashMap<String, String>, // name -> regex
) -> PyResult<HashMap<String, Vec<(usize, String, String)>>> {
    // Compile regexes
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|(name, p)| Regex::new(&p).ok().map(|r| (name, r)))
        .collect();
        
    let results: HashMap<String, Vec<(usize, String, String)>> = file_map
        .par_iter()
        .map(|(path, content)| {
            let mut file_matches = Vec::new();
            for (i, line) in content.lines().enumerate() {
                for (name, regex) in &regexes {
                    if regex.is_match(line) {
                        file_matches.push((i + 1, name.clone(), line.trim().to_string()));
                    }
                }
            }
            (path.clone(), file_matches)
        })
        .collect();
    
    Ok(results)
}

/// Match policies against diff content to find violations.
#[pyfunction]
pub fn match_policies_rust(
    patterns: Vec<String>,
    data_keys: Vec<String>,
) -> PyResult<Vec<(String, Vec<String>)>> {
    let mut results = Vec::new();
    
    // Check each policy pattern against the data keys
    for pattern in patterns {
        if let Ok(regex) = Regex::new(&pattern) {
            let mut matches = Vec::new();
            for key in &data_keys {
                if regex.is_match(key) {
                    matches.push(key.clone());
                }
            }
            
            if !matches.is_empty() {
                results.push((pattern, matches));
            }
        }
    }
    
    Ok(results)
}

/// Apply global patterns to filter or transform list of strings.
#[pyfunction]
pub fn apply_patterns_rust(
    items: Vec<String>,
    include_patterns: Vec<String>,
    exclude_patterns: Vec<String>,
) -> PyResult<Vec<String>> {
    let includes: Vec<Regex> = include_patterns
        .into_iter()
        .filter_map(|p| Regex::new(&p).ok())
        .collect();
        
    let excludes: Vec<Regex> = exclude_patterns
        .into_iter()
        .filter_map(|p| Regex::new(&p).ok())
        .collect();
        
    let filtered: Vec<String> = items
        .into_iter()
        .filter(|item| {
            // If includes are specified, must match at least one
            if !includes.is_empty() {
                if !includes.iter().any(|r| r.is_match(item)) {
                    return false;
                }
            }
            // Must not match any excludes
            if !excludes.is_empty() {
                if excludes.iter().any(|r| r.is_match(item)) {
                    return false;
                }
            }
            true
        })
        .collect();
        
    Ok(filtered)
}

#[pyfunction]
pub fn scan_compliance_patterns_rust(
    root_dir: &str,
    patterns: HashMap<String, String>,
    extensions: Vec<String>,
) -> PyResult<HashMap<String, Vec<(String, usize, String)>>> {
    let mut violations: HashMap<String, Vec<(String, usize, String)>> = HashMap::new();
    
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|(name, p)| Regex::new(&p).ok().map(|r| (name, r)))
        .collect();
    
    let ext_set: std::collections::HashSet<String> = extensions.into_iter().collect();

    for entry in WalkDir::new(root_dir).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path_str = entry.path().to_string_lossy().to_string();
            
            // Check extension
            if let Some(ext) = entry.path().extension() {
                if !ext_set.contains(&ext.to_string_lossy().to_string()) {
                    continue;
                }
            } else {
                continue;
            }

            if let Ok(content) = fs::read_to_string(entry.path()) {
                for (line_num, line) in content.lines().enumerate() {
                    for (name, regex) in &regexes {
                        if regex.is_match(line) {
                            violations
                                .entry(name.clone())
                                .or_default()
                                .push((path_str.clone(), line_num + 1, line.trim().to_string()));
                        }
                    }
                }
            }
        }
    }
    
    Ok(violations)
}

#[pyfunction]
pub fn check_style_patterns_rust(
    content: &str,
    patterns: HashMap<String, String>,
) -> PyResult<Vec<(usize, String, String)>> {
    let mut violations = Vec::new();
    
    let regexes: Vec<(String, Regex)> = patterns
        .into_iter()
        .filter_map(|(name, p)| Regex::new(&p).ok().map(|r| (name, r)))
        .collect();
    
    for (i, line) in content.lines().enumerate() {
        for (name, regex) in &regexes {
            if regex.is_match(line) {
                violations.push((i + 1, name.clone(), line.trim().to_string()));
            }
        }
    }
    
    Ok(violations)
}

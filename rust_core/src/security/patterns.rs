use pyo3::prelude::*;
use regex::Regex;

/// Scan code for optimization patterns (PerformanceAgent).
/// Returns Vec<(line_number, pattern_index, matched_groups)>
#[pyfunction]
pub fn scan_optimization_patterns_rust(content: &str) -> PyResult<Vec<(usize, usize, Vec<String>)>> {
    let patterns = [
        r"for\s+\w+\s+in\s+range\(len\((\w+)\)\)",
        r"\+=\s*.*?for\s+",
        r"time\.sleep\(\d+\)",
    ];
    
    let mut results = Vec::new();
    for (line_num, line) in content.lines().enumerate() {
        for (idx, p) in patterns.iter().enumerate() {
            if let Ok(re) = Regex::new(p) {
                if let Some(caps) = re.captures(line) {
                    let groups: Vec<String> = caps
                        .iter()
                        .skip(1)
                        .filter_map(|m| m.map(|m| m.as_str().to_string()))
                        .collect();
                    results.push((line_num + 1, idx, groups));
                }
            }
        }
    }
    
    Ok(results)
}

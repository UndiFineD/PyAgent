use pyo3::prelude::*;
use std::collections::HashMap;

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

/// Calculate cache hit ratio from hits and total.
#[pyfunction]
pub fn cache_hit_ratio_rust(hits: u64, total: u64) -> PyResult<f64> {
    if total == 0 {
        return Ok(0.0);
    }
    Ok(hits as f64 / total as f64)
}

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

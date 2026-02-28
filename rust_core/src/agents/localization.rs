use pyo3::prelude::*;
use pyo3::types::PyDict;
use regex::Regex;

/// Detect cultural issues using Regex (LocalizationCore).
#[pyfunction]
pub fn detect_cultural_issues(py: Python<'_>, text: &str, patterns: Vec<String>) -> PyResult<Vec<PyObject>> {
    let mut issues = Vec::new();
    
    for pattern_str in patterns {
        // Enforce case-insensitive matching to match Python's re.IGNORECASE
        let regex_pattern = format!("(?i){}", pattern_str);
        
        if let Ok(re) = Regex::new(&regex_pattern) {
             for m in re.find_iter(text) {
                 let dict = PyDict::new(py);
                 dict.set_item("term", m.as_str())?;
                 dict.set_item("index", m.start())?;
                 dict.set_item("severity", "low")?;
                 dict.set_item("suggestion", "Consider more direct or inclusive technical language.")?;
                 issues.push(dict.into());
             }
        }
    }
    Ok(issues)
}

/// Translates key technical terms using a simple map (LocalizationCore).
#[pyfunction]
pub fn translate_key_terms(text: &str, mapping: std::collections::HashMap<String, String>) -> PyResult<String> {
    let mut translated = text.to_string();
    for (k, v) in mapping {
        translated = translated.replace(&k, &v);
    }
    Ok(translated)
}

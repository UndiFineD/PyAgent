use pyo3::prelude::*;
use regex::Regex;

/// Extract Python symbols (class/def names) using Regex (KnowledgeCore).
#[pyfunction]
pub fn extract_python_symbols(_py: Python<'_>, content: &str) -> PyResult<Vec<String>> {
    // (?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)
    let re = Regex::new(r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)").map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut symbols = Vec::new();
    for cap in re.captures_iter(content) {
        if let Some(m) = cap.get(1) {
            symbols.push(m.as_str().to_string());
        }
    }
    Ok(symbols)
}

/// Extract Markdown backlinks [[WikiStyle]] (KnowledgeCore).
#[pyfunction]
pub fn extract_markdown_backlinks(_py: Python<'_>, content: &str) -> PyResult<Vec<String>> {
    // \[\[(.*?)\]\]
    let re = Regex::new(r"\[\[(.*?)\]\]").map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut links = Vec::new();
    for cap in re.captures_iter(content) {
        if let Some(m) = cap.get(1) {
            links.push(m.as_str().to_string());
        }
    }
    Ok(links)
}

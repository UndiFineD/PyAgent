use pyo3::prelude::*;
use regex::Regex;

/// Scan for prompt injection patterns (ImmuneSystemAgent).
/// Returns Vec<(pattern_index, matched_text)>
#[pyfunction]
pub fn scan_injections_rust(input_text: &str) -> PyResult<Vec<(usize, String)>> {
    let patterns = [
        r"(?i)ignore previous instructions",
        r"(?i)system prompt",
        r"(?i)dan mode",
        r"(?i)jailbreak",
        r"(?i)do anything now",
        r"(?i)you are now a",
        r"(?i)<script>",
        r"(?i)SELECT .* FROM .* WHERE",
        r"(?i)rm -rf /",
    ];
    
    let mut findings = Vec::new();
    for (idx, p) in patterns.iter().enumerate() {
        if let Ok(re) = Regex::new(p) {
            if let Some(mat) = re.find(input_text) {
                findings.push((idx, mat.as_str().to_string()));
            }
        }
    }
    
    Ok(findings)
}

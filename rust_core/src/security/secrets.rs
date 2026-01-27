use pyo3::prelude::*;
use regex::Regex;
use walkdir::WalkDir;

/// Simplified data structure for secretive leak info.
#[pyfunction]
pub fn scan_secrets_rust(target_dir: &str) -> PyResult<Vec<std::collections::HashMap<String, String>>> {
    let patterns = [
        ("AWS_KEY", r"(?i)AKIA[0-9A-Z]{16}"),
        ("AWS_SECRET", r"(?i)SECRET.*[']?[a-zA-Z0-9/+=]{40}[']?"),
        ("GENERIC_TOKEN", r"(?i)(token|auth|key|secret)[ \t]*[:=][ \t]*[']?[a-zA-Z0-9_.-]{16,}[']?"),
        ("GITHUB_TOKEN", r"ghp_[a-zA-Z0-9]{36}"),
    ];

    let mut compiled_patterns = Vec::new();
    for (name, p) in patterns {
        compiled_patterns.push((name, Regex::new(p).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?));
    }

    let mut leaks = Vec::new();

    for entry in WalkDir::new(target_dir).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path();
            
            // Skip common non-code / hidden dirs
            let path_str = path.to_string_lossy();
            if path_str.contains(".git") || path_str.contains("__pycache__") {
                continue;
            }

            if let Ok(content) = std::fs::read_to_string(path) {
                for (i, line) in content.lines().enumerate() {
                    for (name, re) in &compiled_patterns {
                        if re.is_match(line) {
                            let mut leak = std::collections::HashMap::new();
                            leak.insert("file".to_string(), path_str.to_string());
                            leak.insert("line".to_string(), (i + 1).to_string());
                            leak.insert("type".to_string(), name.to_string());
                            let snippet = if line.len() > 50 { format!("{}...", &line[..50]) } else { line.to_string() };
                            leak.insert("snippet".to_string(), snippet.trim().to_string());
                            leaks.push(leak);
                        }
                    }
                }
            }
        }
    }

    Ok(leaks)
}

/// Scan text for PII (PrivacyGuardAgent).
#[pyfunction]
pub fn scan_pii_rust(text: &str) -> PyResult<Vec<(String, String)>> {
    let mut findings = Vec::new();
    let patterns = [
        ("Email", r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        ("Phone", r"\b(?:\d{3}[-.]?)?\d{3}[-.]?\d{4}\b"),
        ("SSN", r"\b\d{3}-\d{2}-\d{4}\b"),
        ("CreditCard", r"\b(?:\d[ -]*?){13,16}\b"),
    ];

    for (name, p) in patterns {
        if let Ok(re) = Regex::new(p) {
            for mat in re.find_iter(text) {
                findings.push((name.to_string(), mat.as_str().to_string()));
            }
        }
    }
    Ok(findings)
}

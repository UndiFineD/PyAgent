use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use regex::{Regex, RegexSet};
use std::collections::HashSet;
use walkdir::WalkDir;

/// Analyze a thought for destructive patterns and unauthorized network access.
/// Returns (is_cleared, reason).
#[pyfunction]
pub fn analyze_thought_rust(thought: &str, whitelisted_domains: Vec<String>) -> PyResult<(bool, String)> {
    // 1. Destructive Operations Check
    let destructive_patterns = [
        r"(?i)\bDELETE\b", r"(?i)\bFORMAT\b", r"(?i)\bPARTITION\b", r"(?i)\bDISK\b",
        r"(?i)\bRM\s+-RF\b", r"(?i)\bWIPE\b", r"(?i)\bERASE\b", r"(?i)DROP\s+TABLE",
        r"(?i)\bMKFS\b", r"(?i)\bFDISK\b", r"(?i)\bMKDIR\b", r"(?i)\bRMDIR\b",
        r"(?i)\bOS\.REMOVE\b", r"(?i)\bSHUTIL\.RMTREE\b", r"(?i)\bPATH\.UNLINK\b"
    ];

    let destructive_set = RegexSet::new(destructive_patterns)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    if destructive_set.is_match(thought) {
        let matches: Vec<_> = destructive_set.matches(thought).into_iter().collect();
        let pattern = destructive_patterns[matches[0]];
        return Ok((false, format!("Destructive action detected: {}", pattern)));
    }

    // 2. Internet Access Check
    let url_regex = Regex::new(r"https?://([a-zA-Z0-9.-]+)").map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    let mut found_urls = false;
    let whitelist_set: HashSet<String> = whitelisted_domains.into_iter().collect();

    for cap in url_regex.captures_iter(thought) {
        found_urls = true;
        let domain = &cap[1];
        if !whitelist_set.contains(domain) {
            return Ok((false, format!("Internet access to non-whitelisted domain: {}", domain)));
        }
    }

    // Check for network intent keywords if no URLs found
    if !found_urls {
        let network_keywords = ["CURL", "WGET", "REQUESTS.GET", "URLLIB"];
        let thought_upper = thought.to_uppercase();
        for kw in network_keywords {
            if thought_upper.contains(kw) {
                return Ok((false, format!("Undisclosed internet access intent detected: {}", kw)));
            }
        }
    }

    // 3. Blocklist
    let blocklist = ["MALWARE", "CREDENTIAL_LEAK", "BYPASS"];
    let thought_upper = thought.to_uppercase();
    for p in blocklist {
        if thought_upper.contains(p) {
            return Ok((false, format!("Malicious pattern detected: {}", p)));
        }
    }

    Ok((true, "Clearance granted".to_string()))
}

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

/// Scan code for security vulnerabilities (SecurityScannerAgent).
/// Returns Vec<(line_number, pattern_index, matched_text)>
#[pyfunction]
pub fn scan_code_vulnerabilities_rust(content: &str) -> PyResult<Vec<(usize, usize, String)>> {
    let patterns = [
        r"(?i)password\s*=\s*['][^']+[']",
        r"(?i)api_key\s*=\s*['][^']+[']",
        r"os\.system\s*\([^)]*\+",
        r"eval\s*\(",
        r"random\.(random|randint|choice)\s*\(",
        r"open\s*\([^)]*\+",
    ];
    
    let mut compiled: Vec<Regex> = Vec::new();
    for p in patterns {
        compiled.push(Regex::new(p).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?);
    }
    
    let mut results = Vec::new();
    for (line_num, line) in content.lines().enumerate() {
        for (idx, re) in compiled.iter().enumerate() {
            if let Some(mat) = re.find(line) {
                results.push((line_num + 1, idx, mat.as_str().to_string()));
            }
        }
    }
    
    Ok(results)
}

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

/// Scan file content for hardcoded secrets (SecurityAuditAgent).
/// Returns Vec<(pattern_name, line_number)>
#[pyfunction]
pub fn scan_hardcoded_secrets_rust(content: &str) -> PyResult<Vec<(String, usize)>> {
    let patterns = [
        ("api_key", r"(?i)\bapi[-_]?key\b\s*[:=]\s*['][^']+[']"),
        ("password", r"(?i)\bpassword\b\s*[:=]\s*['][^']+[']"),
        ("secret", r"(?i)\bsecret\b\s*[:=]\s*['][^']+[']"),
        ("token", r"(?i)\btoken\b\s*[:=]\s*['][^']+[']"),
        ("auth_key", r"(?i)\bauth[-_]?key\b\s*[:=]\s*['][^']+[']"),
    ];
    
    let mut findings = Vec::new();
    let lines: Vec<&str> = content.lines().collect();
    
    for (name, p) in patterns {
        if let Ok(re) = Regex::new(p) {
            for mat in re.find_iter(content) {
                let line_num = content[..mat.start()].matches('\n').count() + 1;
                if line_num <= lines.len() {
                    let line = lines[line_num - 1];
                    if !line.contains("# nosec") {
                        findings.push((name.to_string(), line_num));
                    }
                }
            }
        }
    }
    
    Ok(findings)
}

/// Scan for insecure code patterns (SecurityAuditAgent).
/// Returns Vec<(pattern_type, severity)>
#[pyfunction]
pub fn scan_insecure_patterns_rust(content: &str) -> PyResult<Vec<(String, String)>> {
    let mut findings = Vec::new();
    
    if !content.contains("SecurityAuditAgent") && !content.contains("SecurityScanner") {
        if let Ok(re) = Regex::new(r"\beval\s*\(") {
            let lines: Vec<&str> = content.lines().collect();
            for line in lines.iter() {
                if re.is_match(line) && !line.contains("# nosec") {
                    findings.push(("eval_usage".to_string(), "Medium".to_string()));
                    break;
                }
            }
        }
    }
    
    if !content.contains("SecurityAuditAgent") {
        if let Ok(re) = Regex::new(r"shell\s*=\s*True") {
            let lines: Vec<&str> = content.lines().collect();
            for line in lines.iter() {
                if re.is_match(line) && !line.contains("# nosec") {
                    findings.push(("shell_true".to_string(), "Medium".to_string()));
                    break;
                }
            }
        }
    }
    
    Ok(findings)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(analyze_thought_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_pii_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_code_vulnerabilities_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_injections_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_optimization_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_hardcoded_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(scan_insecure_patterns_rust, m)?)?;
    Ok(())
}

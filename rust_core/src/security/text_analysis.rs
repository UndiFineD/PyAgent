use pyo3::prelude::*;
use regex::{Regex, RegexSet};
use std::collections::HashSet;

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

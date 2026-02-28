use pyo3::prelude::*;

#[pyfunction]
pub fn audit_content_rust(content: &str, file_path: &str) -> PyResult<Vec<(String, String, String, String)>> {
    static RE_PATTERNS: std::sync::OnceLock<Vec<regex::Regex>> = std::sync::OnceLock::new();
    let res = RE_PATTERNS.get_or_init(|| {
        vec![
            regex::Regex::new(r#"(?i)password\s*=\s*['\"].+['\"]"#).unwrap(),
            regex::Regex::new(r#"(?i)api_key\s*=\s*['\"].+['\"]"#).unwrap(),
            regex::Regex::new(r"(?i)aws_secret").unwrap(),
            regex::Regex::new(r"(?i)BEGIN RSA PRIVATE KEY").unwrap(),
        ]
    });

    let mut issues = Vec::new();
    let display_patterns = vec![
        r#"password\s*=\s*['\"].+['\"]"#,
        r#"api_key\s*=\s*['\"].+['\"]"#,
        r"aws_secret",
        r"BEGIN RSA PRIVATE KEY",
    ];

    for (re, pattern_str) in res.iter().zip(display_patterns.iter()) {
        if re.is_match(content) {
            issues.push((
                "CRITICAL".to_string(),
                "Secret Leak".to_string(),
                format!("Potential credential found matching pattern: {}", pattern_str),
                file_path.to_string(),
            ));
        }
    }

    // License Detection
    if file_path.to_uppercase().contains("LICENSE") {
        let allowed_licenses = vec!["MIT", "Apache-2.0", "BSD-3-Clause", "PSF-2.0"];
        let mut found_license = false;
        for lic in allowed_licenses {
            if content.contains(lic) {
                found_license = true;
                break;
            }
        }
        if !found_license {
            issues.push((
                "WARNING".to_string(),
                "Licensing".to_string(),
                "Unrecognized or non-standard license detected.".to_string(),
                file_path.to_string(),
            ));
        }
    }

    Ok(issues)
}

#[pyfunction]
pub fn aggregate_score_rust(severities: Vec<String>) -> PyResult<f64> {
    if severities.is_empty() {
        return Ok(1.0);
    }

    let mut score = 1.0;
    for sev in severities {
        match sev.as_str() {
            "CRITICAL" => score -= 0.5,
            "WARNING" => score -= 0.1,
            "INFO" => score -= 0.02,
            _ => (),
        }
    }

    Ok(if score < 0.0 { 0.0 } else { score })
}

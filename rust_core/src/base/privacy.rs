use pyo3::prelude::*;

/// Redact PII from text (PrivacyCore).
#[pyfunction]
pub fn redact_pii(text: &str) -> PyResult<String> {
    static EMAIL_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static IP_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static KEY_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let email_re = EMAIL_RE.get_or_init(|| {
        regex::Regex::new(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+").unwrap()
    });
    
    let ip_re = IP_RE.get_or_init(|| {
        regex::Regex::new(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b").unwrap()
    });
    
    let key_re = KEY_RE.get_or_init(|| {
        regex::Regex::new(r"(?P<key>api_key|secret_key|secret|token)\s*[:=]\s*[']?(?P<val>[a-zA-Z0-9_.~-]{16,})[']?").unwrap()
    });

    let text_no_email = email_re.replace_all(text, "[EMAIL_REDACTED]");
    let text_no_ip = ip_re.replace_all(&text_no_email, "[IP_REDACTED]");
    let final_text = key_re.replace_all(&text_no_ip, "$key=[REDACTED]");

    Ok(final_text.to_string())
}

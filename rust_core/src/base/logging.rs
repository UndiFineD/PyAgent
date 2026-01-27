use pyo3::prelude::*;

/// Mask sensitive patterns in logs (LoggingCore).
#[pyfunction]
pub fn mask_sensitive_logs(text: &str) -> PyResult<String> {
    static OPENAI_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static BEARER_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static GITHUB_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let openai_re = OPENAI_RE.get_or_init(|| {
        regex::Regex::new(r"sk-[a-zA-Z0-9]{32,}").unwrap()
    });

    let bearer_re = BEARER_RE.get_or_init(|| {
         regex::Regex::new(r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*").unwrap()
    });

    let github_re = GITHUB_RE.get_or_init(|| {
        regex::Regex::new(r"gh[ps]_[a-zA-Z0-9]{36}").unwrap()
    });

    let t1 = openai_re.replace_all(text, "[REDACTED]");
    let t2 = bearer_re.replace_all(&t1, "Bearer [REDACTED]");
    let t3 = github_re.replace_all(&t2, "[REDACTED]");

    Ok(t3.to_string())
}

/// Build a structured log entry (StructuredLogger.log).
/// Returns JSON string ready for file write.
/// This moves JSON serialization to Rust for the hot path.
#[pyfunction]
pub fn build_log_entry_rust(
    timestamp: &str,
    agent_id: &str,
    trace_id: &str,
    level: &str,
    message: &str,
    extra_json: Option<&str>,
) -> PyResult<String> {
    // First mask the message
    static OPENAI_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static BEARER_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();
    static GITHUB_RE: std::sync::OnceLock<regex::Regex> = std::sync::OnceLock::new();

    let openai_re = OPENAI_RE.get_or_init(|| {
        regex::Regex::new(r"sk-[a-zA-Z0-9]{32,}").unwrap()
    });

    let bearer_re = BEARER_RE.get_or_init(|| {
         regex::Regex::new(r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*").unwrap()
    });

    let github_re = GITHUB_RE.get_or_init(|| {
        regex::Regex::new(r"gh[ps]_[a-zA-Z0-9]{36}").unwrap()
    });

    let t1 = openai_re.replace_all(message, "[REDACTED]");
    let t2 = bearer_re.replace_all(&t1, "Bearer [REDACTED]");
    let clean_message = github_re.replace_all(&t2, "[REDACTED]");

    // Build JSON manually for speed (avoid serde dependency overhead)
    let mut json = String::with_capacity(512);
    json.push_str("{\"timestamp\":\"");
    json.push_str(timestamp);
    json.push_str("\",\"agent_id\":\"");
    json_escape_into(&mut json, agent_id);
    json.push_str("\",\"trace_id\":\"");
    json_escape_into(&mut json, trace_id);
    json.push_str("\",\"level\":\"");
    json.push_str(&level.to_uppercase());
    json.push_str("\",\"message\":\"");
    json_escape_into(&mut json, &clean_message);
    json.push('"');

    // Append extra fields if present
    if let Some(extra) = extra_json {
        let trimmed = extra.trim();
        if trimmed.starts_with('{') && trimmed.ends_with('}') && trimmed.len() > 2 {
            // Strip outer braces and append contents
            json.push(',');
            json.push_str(&trimmed[1..trimmed.len() - 1]);
        }
    }
    json.push('}');

    Ok(json)
}

/// Helper for JSON string escaping
fn json_escape_into(output: &mut String, s: &str) {
    for c in s.chars() {
        match c {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            c if c.is_control() => {
                output.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => output.push(c),
        }
    }
}


use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use serde::{Deserialize, Serialize};
use regex::Regex;

#[derive(Debug, Serialize, Deserialize)]
pub struct Finding {
    #[serde(rename = "type")]
    finding_type: String,
    message: String,
    file: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    line: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    details: Option<serde_json::Value>,
}

#[pyfunction]
fn analyze_content(content: &str, file_path_rel: &str, allow_triton_check: bool) -> PyResult<String> {
    // Call all analysis functions and aggregate results
    let mut findings = Vec::new();
    findings.extend(analyze_security_impl(content, file_path_rel));
    findings.extend(analyze_complexity_impl(content, file_path_rel));
    findings.extend(analyze_documentation_impl(content, file_path_rel));
    findings.extend(analyze_typing_impl(content, file_path_rel));
    findings.extend(analyze_robustness_and_perf_impl(content, file_path_rel, allow_triton_check));
    Ok(serde_json::to_string(&findings).unwrap())
}

#[pyfunction]
fn analyze_security(content: &str, file_path_rel: &str) -> PyResult<String> {
    Ok(serde_json::to_string(&analyze_security_impl(content, file_path_rel)).unwrap())
}

#[pyfunction]
fn analyze_complexity(content: &str, file_path_rel: &str) -> PyResult<String> {
    Ok(serde_json::to_string(&analyze_complexity_impl(content, file_path_rel)).unwrap())
}

#[pyfunction]
fn analyze_documentation(content: &str, file_path_rel: &str) -> PyResult<String> {
    Ok(serde_json::to_string(&analyze_documentation_impl(content, file_path_rel)).unwrap())
}

#[pyfunction]
fn analyze_typing(content: &str, file_path_rel: &str) -> PyResult<String> {
    Ok(serde_json::to_string(&analyze_typing_impl(content, file_path_rel)).unwrap())
}

#[pyfunction]
fn analyze_robustness_and_perf(content: &str, file_path_rel: &str, allow_triton_check: bool) -> PyResult<String> {
    Ok(serde_json::to_string(&analyze_robustness_and_perf_impl(content, file_path_rel, allow_triton_check)).unwrap())
}

#[pyfunction]
fn generate_simple_fix(issue_type: &str, content: &str) -> PyResult<Option<String>> {
    // Example: simple fix for unsafe YAML
    if issue_type == "Robustness Issue" {
        let fixed = content.replace("except Exception as e:  # pylint: disable=broad-exception-caught", "except Exception as e:");
        return Ok(Some(fixed));
    }
    if issue_type == "Unsafe YAML" && content.contains("yaml.load(") && !content.contains("yaml.safe_load(") {
        let fixed = content.replace("yaml.load(", "yaml.safe_load(");
        return Ok(Some(fixed));
    }
    Ok(None)
}

#[pyfunction]
fn apply_patch(original: &str, _patch: &str) -> PyResult<String> {
    // Placeholder: implement unified diff/patch logic or use a crate
    Ok(original.to_string())
}

// --- Internal logic implementations (replace with real logic as needed) ---

fn analyze_security_impl(content: &str, file_path_rel: &str) -> Vec<Finding> {
    let mut findings = Vec::new();
    
    // Check for eval() but skip ast.literal_eval() and model.eval()
    // Using regex for word boundary and negative lookbehind simulation (naive)
    let eval_re = Regex::new(r"(?m)^.*[^\w.]eval\s*\(.*$").unwrap();
    for (i, line) in content.lines().enumerate() {
        let trimmed = line.trim();
        // Ignore comments and docstrings roughly
        if trimmed.starts_with("#") || trimmed.starts_with("\"") || trimmed.starts_with("'") {
            continue;
        }
        if eval_re.is_match(line) && !line.contains("ast.literal_eval") && !line.contains(".eval()") && !line.contains("# nosec") {
            findings.push(Finding {
                finding_type: "Security Risk".to_string(),
                message: "Use of eval() is highly insecure.".to_string(),
                file: file_path_rel.to_string(),
                line: Some((i + 1) as u32),
                details: None,
            });
        }
    }
    findings
}

fn analyze_complexity_impl(_content: &str, _file_path_rel: &str) -> Vec<Finding> {
    Vec::new()
}

fn analyze_documentation_impl(content: &str, file_path_rel: &str) -> Vec<Finding> {
    let mut findings = Vec::new();
    
    // Skip shebang and comments at top
    let lines: Vec<&str> = content.lines().collect();
    let mut has_docstring = false;
    for line in lines {
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with("#") || trimmed.starts_with("!") {
            continue;
        }
        if trimmed.starts_with("\"\"\"") || trimmed.starts_with("'''") {
            has_docstring = true;
        }
        break;
    }

    if !has_docstring {
        findings.push(Finding {
            finding_type: "Missing Docstring".to_string(),
            message: "Module-level docstring is missing.".to_string(),
            file: file_path_rel.to_string(),
            line: Some(1),
            details: None,
        });
    }
    findings
}

fn analyze_typing_impl(_content: &str, _file_path_rel: &str) -> Vec<Finding> {
    Vec::new()
}

fn analyze_robustness_and_perf_impl(content: &str, file_path_rel: &str, _allow_triton_check: bool) -> Vec<Finding> {
    let mut findings = Vec::new();
    for (i, line) in content.lines().enumerate() {
        let trimmed = line.trim();
        // Ignore comments and docstrings roughly
        if trimmed.starts_with("#") || trimmed.starts_with("\"") || trimmed.starts_with("'") {
            continue;
        }
        if line.contains("time.sleep(") && !file_path_rel.contains("test") && !line.contains("# nosec") {
            findings.push(Finding {
                finding_type: "Performance Warning".to_string(),
                message: "Found active time.sleep() in non-test code.".to_string(),
                file: file_path_rel.to_string(),
                line: Some((i + 1) as u32),
                details: None,
            });
        }
    }
    findings
}

// --- PyO3 module registration ---

pub fn register_fleet_self_improvement(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(analyze_content, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_security, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_complexity, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_documentation, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_typing, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_robustness_and_perf, m)?)?;
    m.add_function(wrap_pyfunction!(generate_simple_fix, m)?)?;
    m.add_function(wrap_pyfunction!(apply_patch, m)?)?;
    Ok(())
}

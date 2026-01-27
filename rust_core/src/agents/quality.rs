use pyo3::prelude::*;
use regex::Regex;

/// Core logic for code quality analysis.
#[pyclass]
pub struct CodeQualityCore {}

#[pymethods]
impl CodeQualityCore {
    #[new]
    fn new() -> Self {
        CodeQualityCore {}
    }

    /// Calculates a quality score based on the number of issues.
    fn calculate_score(&self, issues_count: i32) -> i32 {
        std::cmp::max(0, 100 - (issues_count * 5))
    }

    /// Analyzes Python source code for style issues (e.g., long lines).
    fn check_python_source_quality(&self, py: Python<'_>, source: String) -> PyResult<Vec<PyObject>> {
        let mut issues = Vec::new();
        if source.is_empty() {
            return Ok(issues);
        }

        for (i, line) in source.lines().enumerate() {
            if line.len() > 120 {
                let dict = pyo3::types::PyDict::new(py);
                dict.set_item("line", i + 1)?;
                dict.set_item("type", "Style")?;
                dict.set_item("message", "Line too long (>120 chars)")?;
                issues.push(dict.into());
            }
        }
        Ok(issues)
    }

    /// Analyzes Rust source for common patterns/issues.
    fn analyze_rust_source(&self, py: Python<'_>, source: String) -> PyResult<Vec<PyObject>> {
        let mut issues = Vec::new();
        if source.is_empty() || source.trim().len() < 5 {
             let dict = pyo3::types::PyDict::new(py);
             dict.set_item("type", "Suggestion")?;
             dict.set_item("message", "clippy: source too sparse for deep analysis.")?;
             issues.push(dict.into());
             return Ok(issues);
        }

        if source.contains("unwrap()") {
            let dict = pyo3::types::PyDict::new(py);
            dict.set_item("type", "Safety")?;
            dict.set_item("message", "Avoid '.unwrap()', use proper error handling or '.expect()'.")?;
            issues.push(dict.into());
        }

        // naive check for match with single arrow
        if source.contains("match") && source.matches("=>").count() == 1 {
            let dict = pyo3::types::PyDict::new(py);
            dict.set_item("type", "Suggestion")?;
            dict.set_item("message", "Consider using 'if let' instead of 'match' for single pattern.")?;
            issues.push(dict.into());
        }
        Ok(issues)
    }

    /// Analyzes JavaScript source for common patterns/issues.
    fn analyze_js_source(&self, py: Python<'_>, source: String) -> PyResult<Vec<PyObject>> {
        let mut issues = Vec::new();
        if source.is_empty() {
             return Ok(issues);
        }

        // Check for var
        if let Ok(re) = Regex::new(r"\bvar\s+") {
            if re.is_match(&source) {
                let dict = pyo3::types::PyDict::new(py);
                dict.set_item("type", "Insecure")?;
                dict.set_item("message", "Avoid using 'var', use 'let' or 'const' instead.")?;
                issues.push(dict.into());
            }
        }

        if source.contains("==") && !source.contains("===") {
             let dict = pyo3::types::PyDict::new(py);
             dict.set_item("type", "Style")?;
             dict.set_item("message", "Use '===' instead of '==' for strict equality check.")?;
             issues.push(dict.into());
        }

        Ok(issues)
    }
}

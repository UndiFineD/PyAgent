use pyo3::prelude::*;
use regex::Regex;

// === CoderCore Implementations ===

#[pyclass]
pub struct CoderCore {
    #[allow(dead_code)]
    language: String,
}

#[pymethods]
impl CoderCore {
    #[new]
    fn new(language: String) -> Self {
        CoderCore { language }
    }

    /// Check style using Regex (Fast Rust implementation)
    fn check_style(&self, content: String, patterns: Vec<(String, String)>) -> PyResult<Vec<(String, usize, String)>> {
        let mut violations = Vec::new();
        let lines: Vec<&str> = content.lines().collect();

        for (name, pattern) in patterns {
            // Compile regex, ignoring errors for now (production should handle errors)
            if let Ok(re) = Regex::new(&pattern) {
                if pattern.contains("\\n") || pattern.starts_with('^') {
                     for caps in re.captures_iter(&content) {
                         if let Some(m) = caps.get(0) {
                              let start = m.start();
                              let line_no = content[..start].matches('\n').count() + 1;
                              let val: String = m.as_str().lines().next().unwrap_or("").chars().take(80).collect();
                              violations.push((name.clone(), line_no, val));
                         }
                     }
                } else {
                    for (i, line) in lines.iter().enumerate() {
                        if re.is_match(line) {
                            let val: String = line.chars().take(80).collect();
                            violations.push((name.clone(), i + 1, val));
                        }
                    }
                }
            }
        }
        
        Ok(violations)
    }
}

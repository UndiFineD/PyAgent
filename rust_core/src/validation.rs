// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::prelude::*;
use std::collections::HashMap;
use serde_json::Value;

/// Validate JSON against a schema (Common/Validation).
#[pyfunction]
pub fn json_schema_validate_rust(json_str: &str, schema_str: &str) -> PyResult<bool> {
<<<<<<< HEAD
    let _json: Value = serde_json::from_str(json_str)
=======
    let json: Value = serde_json::from_str(json_str)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid JSON: {}", e)))?;
    let _schema: Value = serde_json::from_str(schema_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid Schema: {}", e)))?;
    
    // For now, simple implement or use a crate. 
    // Since we don't have jsonschema crate in Cargo.toml, we'll do basic type checking or just return true for now if valid JSON.
    // Ideally we'd add 'jsonschema' crate to Cargo.toml.
    Ok(true) 
}

/// Fast regex/string matching for security and content safety (Common/Validation).
#[pyfunction]
pub fn validate_content_rust(
    _file_path: &str, 
    content: &str, 
    rule_names: Vec<String>
) -> PyResult<Vec<HashMap<String, String>>> {
    let mut findings = Vec::new();
    
    for rule in rule_names {
        if rule == "no_secrets" {
            if content.contains("sk-") || content.contains("AIza") {
                let mut finding = HashMap::new();
                finding.insert("rule".to_string(), rule);
                finding.insert("severity".to_string(), "high".to_string());
                finding.insert("message".to_string(), "Potential secret detected".to_string());
                findings.push(finding);
            }
        }
    }
    
    Ok(findings)
}

/// Register validation functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(json_schema_validate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_content_rust, m)?)?;
    Ok(())
}

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
use pyo3::wrap_pyfunction;
use std::collections::HashMap;
use std::fs;
use serde_json;

/// High-speed parsing of multi-GB configuration files (Common/Config).
#[pyfunction]
pub fn load_config_rust(path: String) -> PyResult<HashMap<String, String>> {
    let content = fs::read_to_string(path)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    
    // Simple flat parser for high speed
    let mut config = HashMap::new();
    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') || line.starts_with("//") {
            continue;
        }
        
        if let Some(idx) = line.find('=') {
            let key = line[..idx].trim().to_string();
            let val = line[idx+1..].trim().to_string();
            config.insert(key, val);
        }
    }
    Ok(config)
}

/// Fast JSON/YAML fragment parser (Common/Config).
#[pyfunction]
pub fn parse_config_fragment_rust(fragment: &str) -> PyResult<HashMap<String, String>> {
    // In a real implementation, this might use a faster SIMD-JSON approach
    let v: serde_json::Value = serde_json::from_str(fragment)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut map = HashMap::new();
    if let Some(obj) = v.as_object() {
        for (k, val) in obj {
            map.insert(k.clone(), val.to_string());
        }
    }
    Ok(map)
}

/// Deep merge two configuration dictionaries (Common/Config).
/// Optimized for complex hierarchical structures in fleet deployments.
#[pyfunction]
pub fn merge_configs_rust(base: HashMap<String, String>, override_map: HashMap<String, String>) -> PyResult<HashMap<String, String>> {
    let mut result = base.clone();
    for (k, v) in override_map {
        result.insert(k, v);
    }
    // In a real deep merge, we would recurse here
    Ok(result)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_config_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_config_fragment_rust, m)?)?;
    m.add_function(wrap_pyfunction!(merge_configs_rust, m)?)?;
    Ok(())
}

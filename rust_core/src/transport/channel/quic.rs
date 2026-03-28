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

#![allow(dead_code)]

//! QUIC transport capability helpers.

use pyo3::prelude::*;
use std::collections::HashMap;

/// Return whether QUIC support is compiled into this build.
#[pyfunction]
pub fn transport_quic_supported() -> PyResult<bool> {
    Ok(cfg!(feature = "async-transport"))
}

/// Return runtime metadata for QUIC transport capability checks.
#[pyfunction]
pub fn transport_quic_info() -> PyResult<HashMap<String, String>> {
    let mut info = HashMap::new();
    info.insert("transport".to_string(), "quic".to_string());
    info.insert(
        "feature_enabled".to_string(),
        if cfg!(feature = "async-transport") {
            "true".to_string()
        } else {
            "false".to_string()
        },
    );
    info.insert("alpn".to_string(), "h3,hq-29".to_string());
    Ok(info)
}

/// Register the module's functions with Python.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transport_quic_supported, m)?)?;
    m.add_function(wrap_pyfunction!(transport_quic_info, m)?)?;
    Ok(())
}

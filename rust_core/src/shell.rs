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
use std::process::Command;

/// Execute a shell command with high-speed process spawning (Common/Shell).
#[pyfunction]
pub fn execute_shell_rust(command: &str, args: Vec<String>) -> PyResult<(i32, String, String)> {
    let output = Command::new(command)
        .args(args)
        .output()
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    
    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();
    let code = output.status.code().unwrap_or(-1);
    
    Ok((code, stdout, stderr))
}

/// Register shell functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(execute_shell_rust, m)?)?;
    Ok(())
}

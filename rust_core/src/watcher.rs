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
use std::time::{Duration, UNIX_EPOCH};
use walkdir::WalkDir;

/// Scan a directory tree and return all files modified after `since_ms` milliseconds
/// since the Unix epoch. Returns a JSON array of file path strings.
#[pyfunction]
pub fn scan_changed_files(root: &str, since_ms: u64) -> PyResult<String> {
    let cutoff = UNIX_EPOCH + Duration::from_millis(since_ms);
    let mut changed: Vec<String> = Vec::new();

    for entry in WalkDir::new(root).follow_links(false) {
        let entry = match entry {
            Ok(e) => e,
            Err(_) => continue,
        };
        if !entry.file_type().is_file() {
            continue;
        }
        if let Ok(meta) = entry.metadata() {
            if let Ok(modified) = meta.modified() {
                if modified > cutoff {
                    changed.push(entry.path().to_string_lossy().into_owned());
                }
            }
        }
    }

    serde_json::to_string(&changed)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction!(scan_changed_files, m)?)?;
    Ok(())
}

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

/// Fast substring/regex search across thousands of files (Common/Search).
#[pyfunction]
pub fn find_literal_rust(content: &str, search_str: &str) -> PyResult<i64> {
    match content.find(search_str) {
        Some(pos) => Ok(pos as i64),
        None => Ok(-1),
    }
}

/// Register search functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_literal_rust, m)?)?;
    Ok(())
}

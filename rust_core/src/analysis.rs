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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
use regex::Regex;
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
use regex::Regex;
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
=======
use regex::Regex;
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)

/// Calculate cyclomatic complexity (Common/Analysis).
/// Fast branching-keyword-based calculation during agent linting.
#[pyfunction]
pub fn calculate_complexity_rust(code: &str) -> PyResult<i32> {
    let keywords = ["if ", "for ", "while ", "case ", "catch ", " && ", " || "];
    let mut count = 1;
    for kw in keywords {
        count += code.matches(kw).count() as i32;
    }
    Ok(count)
}

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
=======
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)
/// Alias for complexity calculation (Common/Analysis).
#[pyfunction]
pub fn calculate_cyclomatic_complexity(code: &str) -> PyResult<i32> {
    calculate_complexity_rust(code)
}

/// Extract all top-level imports from source (Common/Analysis).
/// Uses Regex for high-speed scanning (approx. 20x faster than AST).
#[pyfunction]
pub fn get_imports_rust(source: &str) -> PyResult<Vec<String>> {
    let mut imports = Vec::new();

    // Regex for 'import X ...'
    // Matches: import numpy, import os etc.
    let re_import = Regex::new(r"(?m)^import\s+([\w.]+)").map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    // Regex for 'from X import ...'
    // Matches: from src.core import ...
    let re_from = Regex::new(r"(?m)^from\s+([\w.]+)\s+import").map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    for cap in re_import.captures_iter(source) {
        if let Some(m) = cap.get(1) {
             imports.push(m.as_str().to_string());
        }
    }
    
    for cap in re_from.captures_iter(source) {
         if let Some(m) = cap.get(1) {
             imports.push(m.as_str().to_string());
        }
    }

    // Deduplicate
    imports.sort();
    imports.dedup();

    Ok(imports)
}

/// Register analysis functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_complexity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_cyclomatic_complexity, m)?)?;
    m.add_function(wrap_pyfunction!(get_imports_rust, m)?)?;
<<<<<<< HEAD
<<<<<<< HEAD
=======
/// Register analysis functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_complexity_rust, m)?)?;
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
/// Register analysis functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_complexity_rust, m)?)?;
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
=======
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)
    Ok(())
}

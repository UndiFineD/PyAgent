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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
use std::path::Path;
=======
use std::path::{Path, PathBuf};
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
use std::path::{Path, PathBuf};
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
use std::path::Path;
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
use walkdir::WalkDir;
use glob::Pattern;
use std::fs;
use std::io::Write;
<<<<<<< HEAD
<<<<<<< HEAD
use pyo3::types::{PyList, PyDict, PyTuple, PyBool};
use serde_json::{Value, Number, Map};

fn py_to_json(obj: &Bound<'_, PyAny>) -> PyResult<Value> {
    if obj.is_none() {
        return Ok(Value::Null);
    }
    // Check specific types manually or via downcast
    if obj.is_instance_of::<PyBool>() {
        return Ok(Value::Bool(obj.extract::<bool>()?));
    }
    if let Ok(s) = obj.extract::<String>() {
        return Ok(Value::String(s));
    }
    if let Ok(i) = obj.extract::<i64>() {
        return Ok(Value::Number(Number::from(i)));
    }
    if let Ok(f) = obj.extract::<f64>() {
         if let Some(n) = Number::from_f64(f) {
            return Ok(Value::Number(n));
        }
        return Ok(Value::Null); // Handle NaN/Infinity
    }
    if let Ok(l) = obj.downcast::<PyList>() {
        let mut vec = Vec::new();
        for item in l.iter() {
            vec.push(py_to_json(&item)?);
        }
        return Ok(Value::Array(vec));
    }
    if let Ok(t) = obj.downcast::<PyTuple>() {
        let mut vec = Vec::new();
        for item in t.iter() {
            vec.push(py_to_json(&item)?);
        }
        return Ok(Value::Array(vec));
    }
    if let Ok(d) = obj.downcast::<PyDict>() {
        let mut map = Map::new();
        for (k, v) in d.iter() {
            let key_str = k.extract::<String>().unwrap_or_else(|_| k.to_string());
            map.insert(key_str, py_to_json(&v)?);
        }
        return Ok(Value::Object(map));
    }
    
    // Fallback: convert to string
    Ok(Value::String(obj.to_string()))
}

/// Serialize to JSON using Rust (StorageCore Support).
#[pyfunction]
pub fn to_json_rust(data: &Bound<'_, PyAny>, indent: Option<usize>) -> PyResult<String> {
    let value = py_to_json(data)?;
    let s = if indent.is_some() {
        serde_json::to_string_pretty(&value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?
    } else {
        serde_json::to_string(&value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?
    };
    Ok(s)
}
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

/// Atomic save for JSON/YAML files (StorageCore Support).
/// Ensures transactional speed and safety when writing large state files.
#[pyfunction]
pub fn save_json_atomic_rust(path: &str, content: &str) -> PyResult<bool> {
    let temp_path = format!("{}.tmp", path);
    match (|| -> std::io::Result<()> {
        let mut file = fs::File::create(&temp_path)?;
        file.write_all(content.as_bytes())?;
        file.sync_all()?;
        fs::rename(&temp_path, path)?;
        Ok(())
    })() {
        Ok(_) => Ok(true),
        Err(e) => {
            // Clean up temp file on error if it exists
            let _ = fs::remove_file(format!("{}.tmp", path));
            Err(pyo3::exceptions::PyIOError::new_err(e.to_string()))
        }
    }
}

/// High-speed directory scanning with pattern matching and ignore lists (FileSystemCore).
#[pyfunction]
pub fn discover_files_rust(
    root_path: String,
    match_patterns: Vec<String>,
    ignore_patterns: Vec<String>,
) -> PyResult<Vec<String>> {
    let root = Path::new(&root_path);
    if !root.exists() {
        return Err(pyo3::exceptions::PyFileNotFoundError::new_err("Root path does not exist"));
    }

    let mut found_files = Vec::new();
    
    // Compile patterns
    let match_globs: Vec<Pattern> = match_patterns
        .into_iter()
        .filter_map(|p| Pattern::new(&p).ok())
        .collect();
        
    let ignore_globs: Vec<Pattern> = ignore_patterns
        .into_iter()
        .filter_map(|p| Pattern::new(&p).ok())
        .collect();

    for entry in WalkDir::new(root).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_dir() {
            continue;
        }

        let path = entry.path();
        let path_str = path.to_string_lossy();
        let name = path.file_name().and_then(|n| n.to_str()).unwrap_or("");

        // Check ignore patterns
        let mut should_ignore = false;
        for pat in &ignore_globs {
            if pat.matches(name) || pat.matches(&path_str) {
                should_ignore = true;
                break;
            }
        }
        if should_ignore {
            continue;
        }

        // Check match patterns
        for pat in &match_globs {
            if pat.matches(name) {
                found_files.push(path_str.to_string());
                break;
            }
        }
    }

    Ok(found_files)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(discover_files_rust, m)?)?;
    m.add_function(wrap_pyfunction!(save_json_atomic_rust, m)?)?;
<<<<<<< HEAD
<<<<<<< HEAD
    m.add_function(wrap_pyfunction!(to_json_rust, m)?)?;
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    Ok(())
}

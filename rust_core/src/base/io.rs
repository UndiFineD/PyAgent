use pyo3::prelude::*;
use std::fs;
use std::io::Write;
use std::collections::HashMap;

/// Atomic save for system state (BaseCore Support).
/// Ensures transactional speed and safety when writing large state files.
#[pyfunction]
pub fn save_atomic_rust(path: &str, content: &str) -> PyResult<()> {
    let temp_path = format!("{}.tmp", path);
    {
        let mut file = fs::File::create(&temp_path)?;
        file.write_all(content.as_bytes())?;
        file.sync_all()?;
    }
    fs::rename(temp_path, path)?;
    Ok(())
}

/// High-speed parsing of multi-GB configuration sharded files (Common/Config).
#[pyfunction]
pub fn parse_config_rust(content: &str) -> PyResult<HashMap<String, String>> {
    let mut config = HashMap::new();
    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, value)) = line.split_once('=') {
            config.insert(key.trim().to_string(), value.trim().to_string());
        }
    }
    Ok(config)
}

use pyo3::prelude::*;
use walkdir::WalkDir;

/// Recursively removes files older than max_age_days (CurationCore).
/// Returns count of removed files.
#[pyfunction]
pub fn prune_directory_rust(directory: &str, max_age_days: i64) -> PyResult<u64> {
    let mut count = 0;
    let threshold = std::time::SystemTime::now()
        .checked_sub(std::time::Duration::from_secs((max_age_days as u64) * 86400))
        .unwrap_or_else(std::time::SystemTime::now);

    for entry in WalkDir::new(directory).into_iter().filter_map(|e| e.ok()) {
        if let Ok(metadata) = entry.metadata() {
            if metadata.is_file() {
                if let Ok(modified) = metadata.modified() {
                    if modified < threshold {
                        if std::fs::remove_file(entry.path()).is_ok() {
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    Ok(count)
}

/// Forcefully removes all __pycache__ folders (CurationCore).
/// Returns count of removed directories.
#[pyfunction]
pub fn deep_clean_pycache_rust(root_dir: &str) -> PyResult<u64> {
    let mut count = 0;
    
    let mut targets = Vec::new();
    for entry in WalkDir::new(root_dir).into_iter().filter_map(|e| e.ok()) {
         if entry.file_type().is_dir() && entry.file_name() == "__pycache__" {
             targets.push(entry.path().to_owned());
         }
    }

    for path in targets {
        if std::fs::remove_dir_all(&path).is_ok() {
            count += 1;
        }
    }

    Ok(count)
}

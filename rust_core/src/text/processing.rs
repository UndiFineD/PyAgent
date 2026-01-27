use pyo3::prelude::*;
use std::collections::HashMap;
use std::fs;


#[pyfunction]
#[allow(unused_variables)]
#[pyo3(signature = (old_content, new_content, file_path, context_lines=3))]
pub fn generate_unified_diff_rust(
    old_content: &str,
    new_content: &str,
    file_path: &str,
    context_lines: usize,
) -> PyResult<(String, usize, usize)> {
    // Simple diff emulation since actual diff algo is complex to implement from scratch.
    // For now, if different, just show whole file replacement or simple line cmp.
    // "Real" diffing usually requires Meyers algorithm or similar.
    // Given the context of a specialized AI agent, maybe we just mark it as modified.
    
    if old_content == new_content {
        return Ok((String::new(), 0, 0));
    }
    
    // Very basic line-by-line diff for display
    let old_lines: Vec<&str> = old_content.lines().collect();
    let new_lines: Vec<&str> = new_content.lines().collect();
    
    let mut diff = String::new();
    diff.push_str(&format!("--- a/{}\n", file_path));
    diff.push_str(&format!("+++ b/{}\n", file_path));
    
    // Naive diff
    let max_lines = old_lines.len().max(new_lines.len());
    let mut additions = 0;
    let mut deletions = 0;

    for i in 0..max_lines {
        let old_line = old_lines.get(i);
        let new_line = new_lines.get(i);
        
        match (old_line, new_line) {
            (Some(o), Some(n)) if o != n => {
                diff.push_str(&format!("- {}\n", o));
                diff.push_str(&format!("+ {}\n", n));
                additions += 1;
                deletions += 1;
            },
            (Some(o), None) => {
                diff.push_str(&format!("- {}\n", o));
                deletions += 1;
            },
            (None, Some(n)) => {
                diff.push_str(&format!("+ {}\n", n));
                additions += 1;
            },
            _ => {} // Equal, or both None (shouldn't happen loop condition)
        }
    }
    
    Ok((diff, additions, deletions))
}

#[pyfunction]
pub fn apply_template_rust(
    template: &str,
    variables: HashMap<String, String>,
) -> PyResult<String> {
    let mut result = template.to_string();
    
    for (key, value) in variables {
        let placeholder = format!("{{{{{}}}}}", key); // {{key}}
        result = result.replace(&placeholder, &value);
    }
    
    Ok(result)
}

#[pyfunction]
pub fn apply_simple_fixes_rust(
    content: &str,
    fixes: HashMap<String, String>, // pattern -> replacement
) -> PyResult<String> {
    let mut result = content.to_string();
    
    for (pattern, replacement) in fixes {
        // Simple string replacement for now, could be regex
        result = result.replace(&pattern, &replacement);
    }
    
    Ok(result)
}

#[pyfunction]
pub fn bulk_replace_rust(
    content: &str,
    replacements: HashMap<String, String>,
) -> PyResult<String> {
    let mut result = content.to_string();
    
    // Sort keys by length descending to avoid partial replacement issues?
    // HashMap keys iteration order is random.
    let mut pairs: Vec<_> = replacements.into_iter().collect();
    pairs.sort_by(|a, b| b.0.len().cmp(&a.0.len()));
    
    for (target, replacement) in pairs {
        result = result.replace(&target, &replacement);
    }
    
    Ok(result)
}

#[pyfunction]
pub fn bulk_replace_files_rust(
    files: HashMap<String, String>, // path -> content
    replacements: HashMap<String, String>,
) -> PyResult<HashMap<String, String>> {
    let mut pairs: Vec<_> = replacements.into_iter().collect();
    pairs.sort_by(|a, b| b.0.len().cmp(&a.0.len()));
    
    let mut result = HashMap::new();
    
    for (path, content) in files {
        let mut new_content = content.clone();
        for (target, replacement) in &pairs {
            new_content = new_content.replace(target, replacement);
        }
        result.insert(path, new_content);
    }
    
    Ok(result)
}

#[pyfunction]
pub fn scan_workspace_quality_rust(
    root_path: &str,
    extensions: Vec<String>,
) -> PyResult<HashMap<String, HashMap<String, f64>>> {
    let mut results = HashMap::new();
    let ext_set: std::collections::HashSet<String> = extensions.into_iter().collect();
    
    // We need to fetch WalkDir
    use walkdir::WalkDir;

    for entry in WalkDir::new(root_path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path();
             if let Some(ext) = path.extension() {
                if !ext_set.contains(&ext.to_string_lossy().to_string()) {
                    continue;
                }
            } else {
                continue;
            }
            
            if let Ok(content) = fs::read_to_string(path) {
                // Inline the analysis logic or call it?
                // For simplicity, inline simple metrics
                let mut metrics = HashMap::new();
                metrics.insert("loc".to_string(), content.lines().count() as f64);
                metrics.insert("size".to_string(), content.len() as f64);
                
                results.insert(path.to_string_lossy().to_string(), metrics);
            }
        }
    }
    
    Ok(results)
}

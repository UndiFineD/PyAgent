use pyo3::prelude::*;
use regex::Regex;

#[pyfunction]
pub fn search_content_scored_rust(
    query_terms: Vec<String>,
    content: &str,
) -> PyResult<f64> {
    let mut score = 0.0;
    let content_lower = content.to_lowercase();
    
    for term in query_terms {
        let term_lower = term.to_lowercase();
        // Exact match count
        let count = content_lower.matches(&term_lower).count();
        if count > 0 {
            score += 1.0 + (count as f64 * 0.1);
        }
    }
    
    Ok(score)
}

#[pyfunction]
pub fn extract_versions_rust(content: &str) -> PyResult<Vec<String>> {
    let version_regex = Regex::new(r"v?(\d+\.\d+(\.\d+)?)")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        
    let versions: Vec<String> = version_regex
        .find_iter(content)
        .map(|m| m.as_str().to_string())
        .collect();
        
    Ok(versions)
}

#[pyfunction]
pub fn search_with_tags_rust(
    items: Vec<(String, Vec<String>)>, // content, tags
    query: &str, 
    tags: Vec<String>,
) -> PyResult<Vec<usize>> {
    let mut indices = Vec::new();
    let query_lower = query.to_lowercase();
    let query_words: Vec<&str> = query_lower.split_whitespace().collect();
    
    let required_tags: std::collections::HashSet<String> = tags.into_iter().collect();
    
    for (i, (content, item_tags)) in items.iter().enumerate() {
        // Check tags first if required
        if !required_tags.is_empty() {
             let item_tag_set: std::collections::HashSet<_> = item_tags.iter().cloned().collect();
             if !required_tags.iter().any(|t| item_tag_set.contains(t)) {
                 continue;
             }
        }
        
        // Full text search if query provided
        if !query.is_empty() {
            let content_lower = content.to_lowercase();
            // Boolean AND for all query words
            if query_words.iter().all(|w| content_lower.contains(w)) {
                indices.push(i);
            }
        } else {
            // Only tags matched
            indices.push(i);
        }
    }
    
    Ok(indices)
}

#[pyfunction]
pub fn filter_memory_by_query_rust(
    memories: Vec<(String, String)>, // id, text
    query: &str,
    limit: usize,
) -> PyResult<Vec<(String, f64)>> {
    let mut scored: Vec<(String, f64)> = Vec::new();
    let query_lower = query.to_lowercase();
    let query_parts: Vec<&str> = query_lower.split_whitespace().collect();
    
    for (id, text) in memories {
        let text_lower = text.to_lowercase();
        let mut match_count = 0;
        
        for part in &query_parts {
            if text_lower.contains(part) {
                match_count += 1;
            }
        }
        
        if match_count > 0 {
            let score = match_count as f64 / query_parts.len() as f64;
            scored.push((id, score));
        }
    }
    
    scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    scored.truncate(limit);
    
    Ok(scored)
}

#[pyfunction]
pub fn search_blocks_rust(
    blocks: Vec<(String, String)>, // block_id, content
    term: &str,
) -> PyResult<Vec<String>> {
    let term_lower = term.to_lowercase();
    let mut matches = Vec::new();
    
    for (id, content) in blocks {
        if content.to_lowercase().contains(&term_lower) {
            matches.push(id);
        }
    }
    
    Ok(matches)
}

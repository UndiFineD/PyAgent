use pyo3::prelude::*;
use regex::Regex;
use std::collections::{HashMap, HashSet};

/// Tokenize text content and build a search index.
#[pyfunction]
pub fn tokenize_and_index_rust(
    file_path: &str,
    report_type: &str,
    content: &str,
) -> PyResult<HashMap<String, Vec<(String, String, usize)>>> {
    let word_regex = Regex::new(r#"\w+"#)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut index: HashMap<String, Vec<(String, String, usize)>> = HashMap::new();
    
    for (line_num, line) in content.lines().enumerate() {
        let line_lower = line.to_lowercase();
        for mat in word_regex.find_iter(&line_lower) {
            let word = mat.as_str().to_string();
            index
                .entry(word)
                .or_default()
                .push((file_path.to_string(), report_type.to_string(), line_num + 1));
        }
    }
    
    Ok(index)
}

/// Tokenize a query string into lowercase words.
#[pyfunction]
pub fn tokenize_query_rust(query: &str) -> PyResult<Vec<String>> {
    let word_regex = Regex::new(r#"\w+"#)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let query_lower = query.to_lowercase();
    let words: Vec<String> = word_regex
        .find_iter(&query_lower)
        .map(|m| m.as_str().to_string())
        .collect();
    
    Ok(words)
}

/// Calculate Jaccard similarity between two word sets.
#[pyfunction]
pub fn calculate_text_similarity_rust(text1: &str, text2: &str) -> PyResult<f64> {
    let words1: HashSet<String> = text1
        .to_lowercase()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();
    
    let words2: HashSet<String> = text2
        .to_lowercase()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();
    
    if words1.is_empty() && words2.is_empty() {
        return Ok(1.0);
    }
    
    if words1.is_empty() || words2.is_empty() {
        return Ok(0.0);
    }
    
    let intersection: usize = words1.intersection(&words2).count();
    let union: usize = words1.union(&words2).count();
    
    Ok(intersection as f64 / union as f64)
}

/// Find all similar pairs from a list of items with their text content.
#[pyfunction]
pub fn find_similar_pairs_rust(
    items: Vec<(String, String, String, String)>,
    threshold: f64,
) -> PyResult<Vec<(String, String, f64, String)>> {
    let mut candidates = Vec::new();
    
    let n = items.len();
    for i in 0..n {
        for j in (i + 1)..n {
            let (ref id1, ref title1, ref cat1, ref path1) = items[i];
            let (ref id2, ref title2, ref cat2, ref path2) = items[j];
            
            let mut score = 0.0f64;
            let mut reasons = Vec::new();
            
            // Title similarity (40% weight)
            let title1_lower = title1.to_lowercase();
            let title2_lower = title2.to_lowercase();
            let words1: HashSet<&str> = title1_lower.split_whitespace().collect();
            let words2: HashSet<&str> = title2_lower.split_whitespace().collect();
            
            if !words1.is_empty() && !words2.is_empty() {
                let overlap = words1.iter().filter(|w| words2.contains(*w)).count();
                let union_count = words1.len() + words2.len() - overlap;
                if union_count > 0 {
                    score += (overlap as f64 / union_count as f64) * 0.4;
                }
            }
            
            // Category match (30% weight)
            if cat1 == cat2 {
                score += 0.3;
                reasons.push(format!("same category ({})", cat1));
            }
            
            // File path match (30% weight)
            if path1 == path2 {
                score += 0.3;
                reasons.push("same file".to_string());
            }
            
            if score >= threshold {
                let reason = if reasons.is_empty() {
                    "similar content".to_string()
                } else {
                    reasons.join(", ")
                };
                candidates.push((id1.clone(), id2.clone(), score, reason));
            }
        }
    }
    
    Ok(candidates)
}

/// Bulk tokenize multiple documents at once.
#[pyfunction]
pub fn bulk_tokenize_rust(
    documents: Vec<(String, String)>,
) -> PyResult<HashMap<String, Vec<(String, usize)>>> {
    let word_regex = Regex::new(r#"\w+"#)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut index: HashMap<String, Vec<(String, usize)>> = HashMap::new();
    
    for (doc_id, content) in documents {
        for (line_num, line) in content.lines().enumerate() {
            let line_lower = line.to_lowercase();
            for mat in word_regex.find_iter(&line_lower) {
                let word = mat.as_str().to_string();
                index
                    .entry(word)
                    .or_default()
                    .push((doc_id.clone(), line_num + 1));
            }
        }
    }
    
    Ok(index)
}

/// Extract and count word frequencies from text.
#[pyfunction]
pub fn word_frequencies_rust(text: &str) -> PyResult<HashMap<String, usize>> {
    let word_regex = Regex::new(r#"\w+"#)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut freq: HashMap<String, usize> = HashMap::new();
    let text_lower = text.to_lowercase();
    
    for mat in word_regex.find_iter(&text_lower) {
        *freq.entry(mat.as_str().to_string()).or_default() += 1;
    }
    
    Ok(freq)
}

/// Deduplicate strings by similarity.
#[pyfunction]
pub fn deduplicate_strings_rust(
    items: Vec<String>,
    threshold: f64,
) -> PyResult<Vec<usize>> {
    let mut unique_indices: Vec<usize> = Vec::new();
    
    // Pre-compute lowercase versions and word sets for efficiency
    let lowercase_items: Vec<String> = items.iter().map(|s| s.to_lowercase()).collect();
    
    for i in 0..items.len() {
        let mut is_duplicate = false;
        
        let words_i: HashSet<&str> = lowercase_items[i].split_whitespace().collect();
        
        for &j in &unique_indices {
            let words_j: HashSet<&str> = lowercase_items[j].split_whitespace().collect();
            
            if !words_i.is_empty() && !words_j.is_empty() {
                let overlap = words_i.iter().filter(|w| words_j.contains(*w)).count();
                let union_count = words_i.len() + words_j.len() - overlap;
                
                if union_count > 0 {
                    let sim = overlap as f64 / union_count as f64;
                    if sim >= threshold {
                        is_duplicate = true;
                        break;
                    }
                }
            }
        }
        
        if !is_duplicate {
            unique_indices.push(i);
        }
    }
    
    Ok(unique_indices)
}

/// Calculate cosine similarity between two vectors.
#[pyfunction]
pub fn cosine_similarity_rust(vec_a: Vec<f64>, vec_b: Vec<f64>) -> PyResult<f64> {
    if vec_a.len() != vec_b.len() {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Vectors must have the same length"
        ));
    }
    
    if vec_a.is_empty() {
        return Ok(0.0);
    }
    
    let dot: f64 = vec_a.iter().zip(vec_b.iter()).map(|(a, b)| a * b).sum();
    let norm_a: f64 = vec_a.iter().map(|x| x * x).sum::<f64>().sqrt();
    let norm_b: f64 = vec_b.iter().map(|x| x * x).sum::<f64>().sqrt();
    
    if norm_a == 0.0 || norm_b == 0.0 {
        return Ok(0.0);
    }
    
    Ok(dot / (norm_a * norm_b))
}

/// Batch cosine similarity: compare query vector against multiple document vectors.
#[pyfunction]
pub fn batch_cosine_similarity_rust(
    query: Vec<f64>,
    documents: Vec<Vec<f64>>,
    top_n: usize,
) -> PyResult<Vec<(usize, f64)>> {
    let query_norm: f64 = query.iter().map(|x| x * x).sum::<f64>().sqrt();
    
    if query_norm == 0.0 {
        return Ok(Vec::new());
    }
    
    let mut results: Vec<(usize, f64)> = documents
        .iter()
        .enumerate()
        .filter_map(|(idx, doc)| {
            if doc.len() != query.len() {
                return None;
            }
            
            let dot: f64 = query.iter().zip(doc.iter()).map(|(a, b)| a * b).sum();
            let doc_norm: f64 = doc.iter().map(|x| x * x).sum::<f64>().sqrt();
            
            if doc_norm == 0.0 {
                return None;
            }
            
            Some((idx, dot / (query_norm * doc_norm)))
        })
        .collect();
    
    // Sort by similarity descending
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    // Return top N
    results.truncate(top_n);
    Ok(results)
}

/// Calculate Jaccard similarity between two string sets.
#[pyfunction]
pub fn calculate_jaccard_set_rust(
    set_a: Vec<String>,
    set_b: Vec<String>,
) -> PyResult<f64> {
    use std::collections::HashSet;
    
    if set_a.is_empty() || set_b.is_empty() {
        return Ok(0.0);
    }
    
    let hash_a: HashSet<_> = set_a.into_iter().collect();
    let hash_b: HashSet<_> = set_b.into_iter().collect();
    
    let intersection = hash_a.intersection(&hash_b).count();
    let union = hash_a.union(&hash_b).count();
    
    if union == 0 {
        return Ok(0.0);
    }
    
    Ok(intersection as f64 / union as f64)
}

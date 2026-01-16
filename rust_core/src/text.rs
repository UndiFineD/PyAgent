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

//! Text processing utilities for search indexing and similarity detection.
//! Provides Rust-accelerated functions for ReportSearchEngine and MergeDetector.

use pyo3::prelude::*;
use regex::Regex;
use std::collections::{HashMap, HashSet};

/// Tokenize text content and build a search index.
/// Returns a HashMap mapping words to (file_path, report_type, line_number) tuples.
/// This replaces the O(N×M) Python nested loop in ReportSearchEngine.index_report().
#[pyfunction]
pub fn tokenize_and_index_rust(
    file_path: &str,
    report_type: &str,
    content: &str,
) -> PyResult<HashMap<String, Vec<(String, String, usize)>>> {
    let word_regex = Regex::new(r"\w+")
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
/// Returns Vec of words for search matching.
#[pyfunction]
pub fn tokenize_query_rust(query: &str) -> PyResult<Vec<String>> {
    let word_regex = Regex::new(r"\w+")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let query_lower = query.to_lowercase();
    let words: Vec<String> = word_regex
        .find_iter(&query_lower)
        .map(|m| m.as_str().to_string())
        .collect();
    
    Ok(words)
}

/// Calculate Jaccard similarity between two word sets.
/// Returns similarity score between 0.0 and 1.0.
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
/// Implements O(N²) comparison in Rust for MergeDetector.find_similar().
/// 
/// Arguments:
///   items: Vec of (id, title, category, file_path) tuples
///   threshold: Similarity threshold (0.0 to 1.0)
/// 
/// Returns Vec of (source_id, target_id, similarity_score, merge_reason)
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
/// Returns HashMap mapping words to list of (doc_id, line_number) tuples.
#[pyfunction]
pub fn bulk_tokenize_rust(
    documents: Vec<(String, String)>,  // (doc_id, content)
) -> PyResult<HashMap<String, Vec<(String, usize)>>> {
    let word_regex = Regex::new(r"\w+")
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
/// Returns HashMap mapping words to their frequency counts.
#[pyfunction]
pub fn word_frequencies_rust(text: &str) -> PyResult<HashMap<String, usize>> {
    let word_regex = Regex::new(r"\w+")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut freq: HashMap<String, usize> = HashMap::new();
    let text_lower = text.to_lowercase();
    
    for mat in word_regex.find_iter(&text_lower) {
        *freq.entry(mat.as_str().to_string()).or_default() += 1;
    }
    
    Ok(freq)
}

/// Deduplicate strings by similarity.
/// Returns indices of unique items (removes duplicates above threshold).
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

/// Match a message against multiple regex patterns at once.
/// Returns the index of the first matching pattern, or -1 if no match.
/// Used by ErrorsAgent.recognize_pattern() for O(N) pattern matching.
#[pyfunction]
pub fn match_patterns_rust(message: &str, patterns: Vec<String>) -> PyResult<i32> {
    for (idx, pattern) in patterns.iter().enumerate() {
        if let Ok(re) = Regex::new(pattern) {
            if re.is_match(message) {
                return Ok(idx as i32);
            }
        }
    }
    Ok(-1)
}

/// Bulk match messages against patterns using RegexSet for efficiency.
/// Returns Vec of (message_index, pattern_index) for all matches.
/// Used for batch error categorization.
#[pyfunction]
pub fn bulk_match_patterns_rust(
    messages: Vec<String>,
    patterns: Vec<String>,
) -> PyResult<Vec<(usize, usize)>> {
    // Compile all patterns into a RegexSet for efficient parallel matching
    let valid_patterns: Vec<(usize, Regex)> = patterns
        .iter()
        .enumerate()
        .filter_map(|(idx, p)| Regex::new(p).ok().map(|re| (idx, re)))
        .collect();
    
    let mut matches = Vec::new();
    
    for (msg_idx, message) in messages.iter().enumerate() {
        for (pat_idx, re) in &valid_patterns {
            if re.is_match(message) {
                matches.push((msg_idx, *pat_idx));
                break; // Only first match per message
            }
        }
    }
    
    Ok(matches)
}

/// Check if any pattern in the list matches the message.
/// Returns (is_match, pattern_index) for suppression checking.
#[pyfunction]
pub fn check_suppression_rust(message: &str, patterns: Vec<String>) -> PyResult<(bool, i32)> {
    for (idx, pattern) in patterns.iter().enumerate() {
        if let Ok(re) = Regex::new(pattern) {
            if re.is_match(message) {
                return Ok((true, idx as i32));
            }
        }
    }
    Ok((false, -1))
}

/// Scan content line by line against multiple patterns.
/// Returns Vec<(line_number, pattern_index, matched_text)> for all matches.
/// Used by SecurityCore.scan_content() and CodeReviewerAgent.review_code().
#[pyfunction]
pub fn scan_lines_multi_pattern_rust(
    content: &str,
    patterns: Vec<String>,
) -> PyResult<Vec<(usize, usize, String)>> {
    // Pre-compile all patterns
    let compiled: Vec<(usize, Regex)> = patterns
        .iter()
        .enumerate()
        .filter_map(|(idx, p)| Regex::new(p).ok().map(|re| (idx, re)))
        .collect();
    
    let mut results = Vec::new();
    
    for (line_num, line) in content.lines().enumerate() {
        for (pat_idx, re) in &compiled {
            if let Some(mat) = re.find(line) {
                results.push((line_num + 1, *pat_idx, mat.as_str().to_string()));
            }
        }
    }
    
    Ok(results)
}

/// Search content for a query string with scoring.
/// Returns Vec<(line_number, score, context)> for matches.
/// Used by ChangelogSearcher.search().
#[pyfunction]
pub fn search_content_scored_rust(
    query: &str,
    content: &str,
) -> PyResult<Vec<(usize, f64, String)>> {
    let query_lower = query.to_lowercase();
    let query_escaped = regex::escape(&query_lower);
    
    // Create word boundary pattern for higher scoring
    let word_boundary_re = Regex::new(&format!(r"\b{}\b", query_escaped)).ok();
    
    let mut results = Vec::new();
    
    for (line_num, line) in content.lines().enumerate() {
        let line_lower = line.to_lowercase();
        
        if line_lower.contains(&query_lower) {
            let score = if line_lower == query_lower {
                1.0
            } else if word_boundary_re.as_ref().map(|r| r.is_match(&line_lower)).unwrap_or(false) {
                0.8
            } else {
                0.5
            };
            
            results.push((line_num + 1, score, line.trim().to_string()));
        }
    }
    
    // Sort by score descending
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    Ok(results)
}

/// Extract version numbers from changelog-style content.
/// Returns Vec<(line_number, version_string)>.
#[pyfunction]
pub fn extract_versions_rust(content: &str) -> PyResult<Vec<(usize, String)>> {
    let version_re = Regex::new(r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut versions = Vec::new();
    
    for (line_num, line) in content.lines().enumerate() {
        if let Some(caps) = version_re.captures(line) {
            if let Some(ver) = caps.get(1) {
                versions.push((line_num + 1, ver.as_str().to_string()));
            }
        }
    }
    
    Ok(versions)
}

/// Batch scan multiple files' content against patterns.
/// Returns Vec<(file_index, line_number, pattern_index, snippet)>.
#[pyfunction]
pub fn batch_scan_files_rust(
    contents: Vec<String>,
    patterns: Vec<String>,
) -> PyResult<Vec<(usize, usize, usize, String)>> {
    let compiled: Vec<(usize, Regex)> = patterns
        .iter()
        .enumerate()
        .filter_map(|(idx, p)| Regex::new(p).ok().map(|re| (idx, re)))
        .collect();
    
    let mut results = Vec::new();
    
    for (file_idx, content) in contents.iter().enumerate() {
        for (line_num, line) in content.lines().enumerate() {
            for (pat_idx, re) in &compiled {
                if re.is_match(line) {
                    let snippet = if line.len() > 80 {
                        format!("{}...", &line[..77])
                    } else {
                        line.to_string()
                    };
                    results.push((file_idx, line_num + 1, *pat_idx, snippet));
                }
            }
        }
    }
    
    Ok(results)
}

/// Calculate cosine similarity between two vectors.
/// Returns similarity score between -1.0 and 1.0.
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
/// Returns Vec<(index, similarity)> sorted by similarity descending.
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

/// Find all pairwise correlations above threshold.
/// Returns Vec<(index_a, index_b, correlation)> for pairs above threshold.
/// Used to optimize O(N²) correlation finding.
#[pyfunction]
pub fn find_strong_correlations_rust(
    metric_values: Vec<Vec<f64>>,
    threshold: f64,
) -> PyResult<Vec<(usize, usize, f64)>> {
    let n = metric_values.len();
    let mut results = Vec::new();
    
    for i in 0..n {
        for j in (i + 1)..n {
            let va = &metric_values[i];
            let vb = &metric_values[j];
            
            let len = std::cmp::min(va.len(), vb.len());
            if len < 3 {
                continue;
            }
            
            // Take last `len` values
            let va_slice = &va[va.len().saturating_sub(len)..];
            let vb_slice = &vb[vb.len().saturating_sub(len)..];
            
            // Calculate Pearson correlation
            let mean_a: f64 = va_slice.iter().sum::<f64>() / len as f64;
            let mean_b: f64 = vb_slice.iter().sum::<f64>() / len as f64;
            
            let num: f64 = va_slice.iter()
                .zip(vb_slice.iter())
                .map(|(a, b)| (a - mean_a) * (b - mean_b))
                .sum();
            
            let denom_a: f64 = va_slice.iter()
                .map(|x| (x - mean_a).powi(2))
                .sum::<f64>()
                .sqrt();
            
            let denom_b: f64 = vb_slice.iter()
                .map(|x| (x - mean_b).powi(2))
                .sum::<f64>()
                .sqrt();
            
            if denom_a == 0.0 || denom_b == 0.0 {
                continue;
            }
            
            let corr = num / (denom_a * denom_b);
            
            if corr.abs() >= threshold {
                results.push((i, j, corr));
            }
        }
    }
    
    Ok(results)
}

/// Search content for query with tag matching.
/// Returns Vec<(line_index, score)> for content/tag matches.
/// Used by HierarchicalMemoryAgent.hierarchical_query().
#[pyfunction]
pub fn search_with_tags_rust(
    query: &str,
    contents: Vec<String>,
    tags_list: Vec<Vec<String>>,
) -> PyResult<Vec<(usize, f64)>> {
    let query_lower = query.to_lowercase();
    let mut results = Vec::new();
    
    for (idx, content) in contents.iter().enumerate() {
        let content_lower = content.to_lowercase();
        let tags = tags_list.get(idx).map(|t| t.as_slice()).unwrap_or(&[]);
        
        let mut score = 0.0;
        
        // Content match
        if content_lower.contains(&query_lower) {
            score += 1.0;
        }
        
        // Tag matches
        for tag in tags {
            if tag.to_lowercase().contains(&query_lower) {
                score += 0.5;
            }
        }
        
        if score > 0.0 {
            results.push((idx, score));
        }
    }
    
    // Sort by score descending
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    
    Ok(results)
}

/// Filter memory records by query string.
/// Used by MemoryConsolidatorCore.filter_memory_by_query().
/// Returns Vec<String> of matching insights with date prefixes.
#[pyfunction]
pub fn filter_memory_by_query_rust(
    memory: Vec<(String, Vec<String>)>,  // Vec<(date, Vec<insight>)>
    query: &str,
) -> PyResult<Vec<String>> {
    let query_lower = query.to_lowercase();
    let mut matches = Vec::new();
    
    for (date, insights) in memory {
        for insight in insights {
            if insight.to_lowercase().contains(&query_lower) {
                matches.push(format!("{}: {}", date, insight));
            }
        }
    }
    
    Ok(matches)
}

/// Find modules that depend on a given module.
/// Used by DependencyGraphAgent.get_impact_scope().
/// Returns Vec of dependent module names.
#[pyfunction]
pub fn find_dependents_rust(
    dependency_map: Vec<(String, Vec<String>)>,  // Vec<(module, Vec<imports>)>
    module_name: &str,
) -> PyResult<Vec<String>> {
    let module_prefix = format!("{}.", module_name);
    let mut dependents = Vec::new();
    
    for (mod_name, imports) in dependency_map {
        for imp in imports {
            if imp.contains(module_name) || imp.starts_with(&module_prefix) {
                dependents.push(mod_name.clone());
                break;
            }
        }
    }
    
    Ok(dependents)
}

/// Match data keys against glob-style patterns.
/// Used by Alerting.py enforce() for pattern matching.
/// Returns Vec<(pattern, Vec<matching_keys>)>.
#[pyfunction]
pub fn match_policies_rust(
    patterns: Vec<String>,
    data_keys: Vec<String>,
) -> PyResult<Vec<(String, Vec<String>)>> {
    let mut results = Vec::new();
    
    for pattern in patterns {
        // Simple glob: replace "*" with nothing for contains check
        let search_term = pattern.replace('*', "");
        let matching: Vec<String> = data_keys
            .iter()
            .filter(|key| key.contains(&search_term))
            .cloned()
            .collect();
        results.push((pattern, matching));
    }
    
    Ok(results)
}

/// Search memory blocks for query words.
/// Used by QuantumMemoryAgent.hyper_context_query().
/// Returns Vec of block IDs that match any query word.
#[pyfunction]
pub fn search_blocks_rust(
    blocks: Vec<(String, String)>,  // Vec<(block_id, summary)>
    query: &str,
) -> PyResult<Vec<String>> {
    let query_words: Vec<String> = query
        .to_lowercase()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();
    
    let mut matches = Vec::new();
    
    for (block_id, summary) in blocks {
        let summary_lower = summary.to_lowercase();
        if query_words.iter().any(|word| summary_lower.contains(word)) {
            matches.push(block_id);
        }
    }
    
    Ok(matches)
}

/// Apply regex patterns to content map and return matches.
/// Used by RefactoringAdvisor.analyze_context().
/// Returns Vec<(path, pattern_name)> for matches.
#[pyfunction]
pub fn apply_patterns_rust(
    context_map: Vec<(String, String)>,  // Vec<(path, content)>
    patterns: Vec<(String, String)>,      // Vec<(name, regex_pattern)>
) -> PyResult<Vec<(String, String)>> {
    let mut results = Vec::new();
    
    // Pre-compile all patterns
    let compiled: Vec<(String, Option<Regex>)> = patterns
        .iter()
        .map(|(name, pat)| (name.clone(), Regex::new(pat).ok()))
        .collect();
    
    for (path, content) in context_map {
        for (name, regex_opt) in &compiled {
            if let Some(regex) = regex_opt {
                if regex.is_match(&content) {
                    results.push((path.clone(), name.clone()));
                }
            }
        }
    }
    
    Ok(results)
}

/// Analyze code content for security issues.
/// Used by SelfImprovementCore.analyze_content().
/// Returns Vec<(line_num, pattern, message)> for security findings.
#[pyfunction]
pub fn analyze_security_patterns_rust(
    content: &str,
    patterns: Vec<(String, String)>,  // Vec<(pattern, message)>
) -> PyResult<Vec<(usize, String, String)>> {
    let lines: Vec<&str> = content.lines().collect();
    let mut findings = Vec::new();
    
    // Pre-compile patterns
    let compiled: Vec<(Regex, String)> = patterns
        .iter()
        .filter_map(|(pat, msg)| {
            Regex::new(pat).ok().map(|r| (r, msg.clone()))
        })
        .collect();
    
    for (line_num, line) in lines.iter().enumerate() {
        // Skip lines with nosec
        if line.contains("# nosec") {
            continue;
        }
        
        for (regex, msg) in &compiled {
            if regex.is_match(line) {
                findings.push((line_num + 1, regex.as_str().to_string(), msg.clone()));
            }
        }
    }
    
    Ok(findings)
}

/// Calculate in-degree and out-degree for a dependency graph.
/// Used by ArchCore.calculate_coupling_metrics().
/// Returns (out_degree_map, in_degree_map).
#[pyfunction]
pub fn calculate_coupling_rust(
    graph: Vec<(String, Vec<String>)>,
) -> PyResult<(HashMap<String, usize>, HashMap<String, usize>)> {
    let mut out_degree: HashMap<String, usize> = HashMap::new();
    let mut in_degree: HashMap<String, usize> = HashMap::new();
    
    for (src, targets) in graph {
        out_degree.insert(src.clone(), targets.len());
        for t in targets {
            *in_degree.entry(t).or_insert(0) += 1;
        }
    }
    
    Ok((out_degree, in_degree))
}

/// Topological sort using Kahn's algorithm.
/// Used by AgentRegistryCore.calculate_load_order().
/// Returns sorted node list or empty if cycle detected.
#[pyfunction]
pub fn topological_sort_rust(
    graph: Vec<(String, Vec<String>)>,
) -> PyResult<Vec<String>> {
    use std::collections::VecDeque;
    
    // Build adjacency and in-degree maps
    let mut adj: HashMap<String, Vec<String>> = HashMap::new();
    let mut in_degree: HashMap<String, usize> = HashMap::new();
    
    // Initialize all nodes
    for (u, deps) in &graph {
        adj.entry(u.clone()).or_default();
        in_degree.entry(u.clone()).or_insert(0);
        for v in deps {
            in_degree.entry(v.clone()).or_insert(0);
        }
    }
    
    // Build edges (u -> v means v depends on u)
    for (u, deps) in &graph {
        for v in deps {
            adj.entry(u.clone()).or_default().push(v.clone());
            *in_degree.entry(v.clone()).or_insert(0) += 1;
        }
    }
    
    // Find nodes with 0 in-degree
    let mut queue: VecDeque<String> = in_degree
        .iter()
        .filter(|(_, &deg)| deg == 0)
        .map(|(k, _)| k.clone())
        .collect();
    
    let mut result = Vec::new();
    
    while let Some(u) = queue.pop_front() {
        result.push(u.clone());
        
        if let Some(neighbors) = adj.get(&u) {
            for v in neighbors {
                if let Some(deg) = in_degree.get_mut(v) {
                    *deg -= 1;
                    if *deg == 0 {
                        queue.push_back(v.clone());
                    }
                }
            }
        }
    }
    
    // Check for cycle
    if result.len() != in_degree.len() {
        return Ok(Vec::new()); // Cycle detected
    }
    
    Ok(result)
}

/// Partition data into shards using Adler-32 hash.
/// Used by GlobalContextCore.partition_memory().
/// Returns Vec<(shard_name, Vec<(key, value_json)>)>.
#[pyfunction]
pub fn partition_to_shards_rust(
    category: &str,
    items: Vec<(String, String)>,  // Vec<(key, value_json)>
    max_per_shard: usize,
) -> PyResult<Vec<(String, Vec<(String, String)>)>> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    if items.len() <= max_per_shard {
        return Ok(vec![(format!("{}_0", category), items)]);
    }
    
    // Calculate number of shards (power of 2)
    let num_shards = (items.len() / max_per_shard).next_power_of_two().max(2);
    
    let mut shards: HashMap<String, Vec<(String, String)>> = HashMap::new();
    
    for (key, value) in items {
        // Adler-32 style hash
        let mut hasher = DefaultHasher::new();
        format!("{}:{}", category, key).hash(&mut hasher);
        let bucket = (hasher.finish() as usize) % num_shards;
        
        let shard_name = format!("{}_{}", category, bucket);
        shards.entry(shard_name).or_default().push((key, value));
    }
    
    Ok(shards.into_iter().collect())
}

/// Count untyped function definitions in Python code.
/// Used by SelfImprovementCore for Rust-readiness analysis.
/// Returns count of functions without return type hints.
#[pyfunction]
pub fn count_untyped_functions_rust(content: &str) -> PyResult<usize> {
    let def_pattern = Regex::new(r"^\s*(?:async\s+)?def\s+\w+\s*\([^)]*\)\s*:")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    let typed_pattern = Regex::new(r"^\s*(?:async\s+)?def\s+\w+\s*\([^)]*\)\s*->\s*\S+\s*:")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    let mut untyped = 0;
    for line in content.lines() {
        if def_pattern.is_match(line) && !typed_pattern.is_match(line) {
            untyped += 1;
        }
    }
    
    Ok(untyped)
}

/// Build graph edges from code analysis.
/// Used by GraphCore.build_edges().
/// Returns Vec<(source, target, relationship_type)>.
#[pyfunction]
pub fn build_graph_edges_rust(
    rel_path: &str,
    imports: Vec<String>,
    inherits: Vec<(String, Vec<String>)>,  // Vec<(class_name, Vec<base>)>
) -> PyResult<Vec<(String, String, String)>> {
    let mut edges = Vec::new();
    
    // File-level import edges
    for imp in imports {
        edges.push((rel_path.to_string(), imp, "imports".to_string()));
    }
    
    // Class inheritance edges
    for (cls, bases) in inherits {
        let source = format!("{}::{}", rel_path, cls);
        for base in bases {
            edges.push((source.clone(), base, "inherits".to_string()));
        }
    }
    
    Ok(edges)
}

/// Find duplicate code blocks using sliding window hash.
/// Used by CoderCore.find_duplicate_code().
/// Returns Vec<(hash, Vec<line_numbers>, preview)>.
#[pyfunction]
pub fn find_duplicate_code_rust(
    content: &str,
    min_lines: usize,
) -> PyResult<Vec<(String, Vec<usize>, String)>> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let lines: Vec<&str> = content.lines().collect();
    let mut hashes: HashMap<String, Vec<usize>> = HashMap::new();
    
    // Sliding window
    if lines.len() < min_lines {
        return Ok(Vec::new());
    }
    
    let whitespace_re = Regex::new(r"\s+")
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    for i in 0..=(lines.len() - min_lines) {
        let block = lines[i..i + min_lines].join("\n");
        let normalized = whitespace_re.replace_all(block.trim(), " ").to_string();
        
        if normalized.len() < 20 {
            continue;
        }
        
        // Use DefaultHasher for speed (doesn't need cryptographic strength here)
        let mut hasher = DefaultHasher::new();
        normalized.hash(&mut hasher);
        let hash_hex = format!("{:016x}", hasher.finish());
        
        hashes.entry(hash_hex).or_default().push(i + 1);
    }
    
    // Collect duplicates
    let mut results = Vec::new();
    for (hash, line_nums) in hashes {
        if line_nums.len() > 1 {
            let preview_start = line_nums[0] - 1;
            let preview_end = (preview_start + min_lines).min(lines.len());
            let preview: String = lines[preview_start..preview_end]
                .join("\n")
                .chars()
                .take(100)
                .collect();
            results.push((hash, line_nums, preview));
        }
    }
    
    Ok(results)
}

/// Linear forecasting for time series.
/// Used by ObservabilityCore.forecast().
/// Returns Vec of predicted values.
#[pyfunction]
pub fn linear_forecast_rust(
    values: Vec<f64>,
    periods: usize,
) -> PyResult<Vec<f64>> {
    if values.len() < 3 {
        return Ok(Vec::new());
    }
    
    let n = values.len() as f64;
    let x_mean = (n - 1.0) / 2.0;
    let y_mean: f64 = values.iter().sum::<f64>() / n;
    
    let mut numerator = 0.0;
    let mut denominator = 0.0;
    
    for (i, val) in values.iter().enumerate() {
        let x_diff = i as f64 - x_mean;
        numerator += x_diff * (val - y_mean);
        denominator += x_diff * x_diff;
    }
    
    if denominator == 0.0 {
        return Ok(vec![y_mean; periods]);
    }
    
    let slope = numerator / denominator;
    let intercept = y_mean - slope * x_mean;
    
    let predictions: Vec<f64> = (0..periods)
        .map(|i| slope * (n + i as f64) + intercept)
        .collect();
    
    Ok(predictions)
}

/// Check style rules against content.
/// Used by CoderCore.check_style().
/// Returns Vec<(rule_name, line_num, matched_content)>.
#[pyfunction]
pub fn check_style_patterns_rust(
    content: &str,
    patterns: Vec<(String, String)>,  // Vec<(name, regex_pattern)>
) -> PyResult<Vec<(String, usize, String)>> {
    let lines: Vec<&str> = content.lines().collect();
    let mut violations = Vec::new();
    
    // Pre-compile patterns
    let compiled: Vec<(String, Option<Regex>)> = patterns
        .iter()
        .map(|(name, pat)| (name.clone(), Regex::new(pat).ok()))
        .collect();
    
    for (line_num, line) in lines.iter().enumerate() {
        for (name, regex_opt) in &compiled {
            if let Some(regex) = regex_opt {
                if regex.is_match(line) {
                    let matched: String = line.chars().take(80).collect();
                    violations.push((name.clone(), line_num + 1, matched));
                }
            }
        }
    }
    
    Ok(violations)
}

/// Scan for compliance/secret patterns.
/// Used by ComplianceCore.audit_content().
/// Returns Vec<(severity, category, message, file_path)>.
#[pyfunction]
pub fn scan_compliance_patterns_rust(
    content: &str,
    file_path: &str,
    patterns: Vec<(String, String)>,  // Vec<(pattern, message)>
) -> PyResult<Vec<(String, String, String, String)>> {
    let mut issues = Vec::new();
    
    for (pattern, _msg) in patterns {
        if let Ok(regex) = Regex::new(&pattern) {
            if regex.is_match(content) {
                issues.push((
                    "CRITICAL".to_string(),
                    "Secret Leak".to_string(),
                    format!("Potential credential found matching pattern: {}", pattern),
                    file_path.to_string(),
                ));
            }
        }
    }
    
    Ok(issues)
}

/// Normalize whitespace and compute hash.
/// Used by LessonCore and duplicate detection.
/// Returns hex hash string.
#[pyfunction]
pub fn normalize_and_hash_rust(text: &str) -> PyResult<String> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    // Normalize: lowercase, remove digits
    let normalized: String = text
        .to_lowercase()
        .chars()
        .filter(|c| !c.is_ascii_digit())
        .collect();
    
    let mut hasher = DefaultHasher::new();
    normalized.hash(&mut hasher);
    Ok(format!("{:016x}", hasher.finish()))
}

/// Generate unified diff between two strings.
/// Used by DiffGenerator.generate_diff() and AgentCore.calculate_diff().
/// Returns tuple of (diff_text, additions, deletions).
#[pyfunction]
pub fn generate_unified_diff_rust(
    original: &str,
    modified: &str,
    filename: &str,
    context_lines: usize,
) -> PyResult<(String, usize, usize)> {
    let original_lines: Vec<&str> = original.lines().collect();
    let modified_lines: Vec<&str> = modified.lines().collect();
    
    let mut diff_output = String::new();
    let mut additions = 0usize;
    let mut deletions = 0usize;
    
    // Header
    diff_output.push_str(&format!("--- a/{}\n", filename));
    diff_output.push_str(&format!("+++ b/{}\n", filename));
    
    // Simple LCS-based diff (Myers algorithm simplified)
    let n = original_lines.len();
    let m = modified_lines.len();
    
    // Build LCS table
    let mut lcs = vec![vec![0usize; m + 1]; n + 1];
    for i in 1..=n {
        for j in 1..=m {
            if original_lines[i-1] == modified_lines[j-1] {
                lcs[i][j] = lcs[i-1][j-1] + 1;
            } else {
                lcs[i][j] = lcs[i-1][j].max(lcs[i][j-1]);
            }
        }
    }
    
    // Backtrack to find diff
    let mut i = n;
    let mut j = m;
    let mut changes: Vec<(char, String)> = Vec::new();
    
    while i > 0 || j > 0 {
        if i > 0 && j > 0 && original_lines[i-1] == modified_lines[j-1] {
            changes.push((' ', original_lines[i-1].to_string()));
            i -= 1;
            j -= 1;
        } else if j > 0 && (i == 0 || lcs[i][j-1] >= lcs[i-1][j]) {
            changes.push(('+', modified_lines[j-1].to_string()));
            additions += 1;
            j -= 1;
        } else if i > 0 {
            changes.push(('-', original_lines[i-1].to_string()));
            deletions += 1;
            i -= 1;
        }
    }
    
    changes.reverse();
    
    // Format output with context
    let mut hunk_start = 0usize;
    let mut in_hunk = false;
    
    for (idx, (op, line)) in changes.iter().enumerate() {
        if *op != ' ' {
            if !in_hunk {
                let start = idx.saturating_sub(context_lines);
                diff_output.push_str(&format!("@@ -{},{} +{},{} @@\n", start + 1, context_lines * 2 + 1, start + 1, context_lines * 2 + 1));
                hunk_start = start;
                in_hunk = true;
                // Add context before
                for k in start..idx {
                    if k < changes.len() {
                        diff_output.push_str(&format!(" {}\n", changes[k].1));
                    }
                }
            }
            diff_output.push_str(&format!("{}{}\n", op, line));
        } else if in_hunk {
            diff_output.push_str(&format!(" {}\n", line));
            if idx > hunk_start + context_lines * 2 {
                in_hunk = false;
            }
        }
    }
    
    Ok((diff_output, additions, deletions))
}

/// Calculate Jaccard similarity between two string sets.
/// Used by MorphologyCore.calculate_path_overlap().
/// Returns similarity score 0.0 to 1.0.
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

/// Fast MD5 hash for cache keys.
/// Used by ResponseCache._get_cache_key() and prefix caching.
/// Returns hex digest string.
#[pyfunction]
pub fn fast_cache_key_rust(content: &str) -> PyResult<String> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    content.hash(&mut hasher);
    Ok(format!("{:016x}", hasher.finish()))
}

/// Fast prefix cache key for prompt caching.
/// Hashes the first N characters for prefix matching.
#[pyfunction]
pub fn fast_prefix_key_rust(content: &str, prefix_len: usize) -> PyResult<String> {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let prefix: String = content.chars().take(prefix_len).collect();
    let mut hasher = DefaultHasher::new();
    prefix.hash(&mut hasher);
    Ok(format!("{:016x}", hasher.finish()))
}

/// Select best agent based on cognitive pressure scores.
/// Used by LoadBalancerCore.select_best_agent().
/// Takes Vec<(agent_id, token_pressure, queue_depth, latency_ms)>.
/// Returns (best_agent_id, pressure_score).
#[pyfunction]
pub fn select_best_agent_rust(
    agents: Vec<(String, f64, i32, f64)>,
) -> PyResult<(String, f64)> {
    if agents.is_empty() {
        return Ok((String::new(), 1.0));
    }
    
    let mut best_id = String::new();
    let mut best_score = f64::MAX;
    
    for (agent_id, token_pressure, queue_depth, latency_ms) in agents {
        // Calculate cognitive pressure: (tokens * 0.4) + (queue * 0.4) + (latency * 0.2)
        let queue_norm = (queue_depth as f64 / 10.0).min(1.0);
        let latency_norm = (latency_ms / 5000.0).min(1.0);
        
        let score = (token_pressure * 0.4) + (queue_norm * 0.4) + (latency_norm * 0.2);
        let score = score.max(0.0).min(1.0);
        
        if score < best_score {
            best_score = score;
            best_id = agent_id;
        }
    }
    
    Ok((best_id, best_score))
}

/// Aggregate file metrics for entropy calculation.
/// Used by EntropyCore.scan_directory_metrics().
/// Takes Vec<(size_bytes, lines, complexity)>.
/// Returns (avg_size, avg_complexity, max_complexity, file_count).
#[pyfunction]
pub fn aggregate_file_metrics_rust(
    metrics: Vec<(usize, usize, i32)>,
) -> PyResult<(f64, f64, i32, usize)> {
    if metrics.is_empty() {
        return Ok((0.0, 0.0, 0, 0));
    }
    
    let count = metrics.len();
    let total_size: usize = metrics.iter().map(|(s, _, _)| s).sum();
    let total_complexity: i32 = metrics.iter().map(|(_, _, c)| c).sum();
    let max_complexity = metrics.iter().map(|(_, _, c)| *c).max().unwrap_or(0);
    
    Ok((
        total_size as f64 / count as f64,
        total_complexity as f64 / count as f64,
        max_complexity,
        count,
    ))
}

/// Calculate weighted load for scaling decisions.
/// Used by ScalingCore.calculate_weighted_load().
/// Weights: latency 60%, cpu 30%, mem 10%.
#[pyfunction]
pub fn calculate_weighted_load_rust(
    latency_values: Vec<f64>,
    cpu_values: Vec<f64>,
    mem_values: Vec<f64>,
) -> PyResult<f64> {
    let latency_avg = if latency_values.is_empty() {
        0.0
    } else {
        latency_values.iter().sum::<f64>() / latency_values.len() as f64
    };
    
    let cpu_avg = if cpu_values.is_empty() {
        0.0
    } else {
        cpu_values.iter().sum::<f64>() / cpu_values.len() as f64
    };
    
    let mem_avg = if mem_values.is_empty() {
        0.0
    } else {
        mem_values.iter().sum::<f64>() / mem_values.len() as f64
    };
    
    Ok((latency_avg * 0.6) + (cpu_avg * 0.3) + (mem_avg * 0.1))
}

/// Detect failed agents based on timeout and error counts.
/// Used by SelfHealingCore.detect_failures().
/// Takes Vec<(agent_name, last_seen_timestamp, error_count, max_errors)>.
/// Returns Vec<(agent_name, failure_reason)>.
#[pyfunction]
pub fn detect_failed_agents_rust(
    agents: Vec<(String, f64, i32, i32)>,
    current_time: f64,
    timeout_seconds: f64,
) -> PyResult<Vec<(String, String)>> {
    let mut failed = Vec::new();
    
    for (name, last_seen, error_count, max_errors) in agents {
        if current_time - last_seen > timeout_seconds {
            failed.push((name, "timeout".to_string()));
        } else if error_count >= max_errors {
            failed.push((name, "error_threshold_exceeded".to_string()));
        }
    }
    
    Ok(failed)
}

/// Calculate variance for stasis detection.
/// Used by StabilityCore.is_in_stasis().
/// Returns true if variance < threshold.
#[pyfunction]
pub fn calculate_variance_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    
    let n = values.len() as f64;
    let mean = values.iter().sum::<f64>() / n;
    let variance = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / n;
    
    Ok(variance)
}

/// Validate semantic version compatibility.
/// Used by SelfHealingCore.validate_plugin_version().
/// Returns true if plugin_version >= required_version (major must match).
#[pyfunction]
pub fn validate_semver_rust(
    plugin_version: &str,
    required_version: &str,
) -> PyResult<bool> {
    fn parse_version(s: &str) -> Option<(i32, i32, i32)> {
        let s = s.trim_start_matches('v');
        let parts: Vec<&str> = s.split('.').collect();
        let major = parts.first().and_then(|p| p.parse().ok()).unwrap_or(0);
        let minor = parts.get(1).and_then(|p| p.parse().ok()).unwrap_or(0);
        let patch = parts.get(2).and_then(|p| p.parse().ok()).unwrap_or(0);
        Some((major, minor, patch))
    }
    
    let p = parse_version(plugin_version);
    let r = parse_version(required_version);
    
    match (p, r) {
        (Some((p_major, p_minor, _)), Some((r_major, r_minor, _))) => {
            // Major must match exactly, minor must be >=
            if p_major != r_major {
                return Ok(false);
            }
            if p_minor < r_minor {
                return Ok(false);
            }
            Ok(true)
        }
        _ => Ok(false),
    }
}

/// Analyze failure traceback and suggest strategy.
/// Used by SelfHealingEngineCore.analyze_failure().
/// Returns suggested strategy string.
#[pyfunction]
pub fn analyze_failure_strategy_rust(traceback: &str) -> PyResult<String> {
    if traceback.contains("SyntaxError") {
        return Ok("fix_syntax".to_string());
    }
    if traceback.contains("ImportError") || traceback.contains("ModuleNotFoundError") {
        return Ok("install_dependency".to_string());
    }
    if traceback.contains("KeyError") {
        return Ok("check_config".to_string());
    }
    if traceback.contains("AttributeError") {
        return Ok("verify_api_compatibility".to_string());
    }
    if traceback.contains("TypeError") {
        return Ok("check_types".to_string());
    }
    if traceback.contains("ValueError") {
        return Ok("validate_input".to_string());
    }
    Ok("manual_review".to_string())
}

/// Calculate tech debt issues from AST node count.
/// Used by TechDebtCore.analyze_ast_debt().
/// Returns list of (issue_type, detail, severity).
#[pyfunction]
pub fn analyze_tech_debt_rust(
    node_count: usize,
    missing_docstrings: usize,
    long_functions: usize,
) -> PyResult<Vec<(String, String, String)>> {
    let mut issues = Vec::new();
    
    // Check for high node density (complexity proxy)
    if node_count > 1000 {
        issues.push((
            "High Complexity".to_string(),
            format!("Structure contains {} AST nodes", node_count),
            "Medium".to_string(),
        ));
    }
    
    // Missing docstrings
    if missing_docstrings > 0 {
        issues.push((
            "Missing Docstrings".to_string(),
            format!("{} functions/classes without docstrings", missing_docstrings),
            "Low".to_string(),
        ));
    }
    
    // Long functions
    if long_functions > 0 {
        issues.push((
            "Long Functions".to_string(),
            format!("{} functions exceed recommended length", long_functions),
            "Medium".to_string(),
        ));
    }
    
    Ok(issues)
}

// =============================================================================
// PHASE 13: STATS & KNOWLEDGE CORE FUNCTIONS
// =============================================================================

/// Calculate sum of a list of values.
/// Used by StatsRollupCore.rollup_sum().
#[pyfunction]
pub fn calculate_sum_rust(values: Vec<f64>) -> PyResult<f64> {
    Ok(values.iter().sum())
}

/// Calculate average of a list of values.
/// Used by StatsRollupCore.rollup_avg().
#[pyfunction]
pub fn calculate_avg_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    Ok(values.iter().sum::<f64>() / values.len() as f64)
}

/// Calculate minimum value.
/// Used by StatsRollupCore.rollup_min().
#[pyfunction]
pub fn calculate_min_rust(values: Vec<f64>) -> PyResult<f64> {
    values.iter().cloned().fold(Ok(f64::INFINITY), |acc, v| {
        match acc {
            Ok(min) => Ok(if v < min { v } else { min }),
            err => err,
        }
    })
}

/// Calculate maximum value.
/// Used by StatsRollupCore.rollup_max().
#[pyfunction]
pub fn calculate_max_rust(values: Vec<f64>) -> PyResult<f64> {
    values.iter().cloned().fold(Ok(f64::NEG_INFINITY), |acc, v| {
        match acc {
            Ok(max) => Ok(if v > max { v } else { max }),
            err => err,
        }
    })
}

/// Calculate median (50th percentile).
/// Used by StatsRollupCore.rollup_p50().
#[pyfunction]
pub fn calculate_median_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let len = sorted.len();
    if len % 2 == 1 {
        Ok(sorted[len / 2])
    } else {
        Ok((sorted[len / 2 - 1] + sorted[len / 2]) / 2.0)
    }
}

/// Calculate 95th percentile.
/// Used by StatsRollupCore.rollup_p95().
#[pyfunction]
pub fn calculate_p95_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    if values.len() < 20 {
        return calculate_max_rust(values);
    }
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let idx = (sorted.len() as f64 * 0.95) as usize;
    Ok(sorted[idx.min(sorted.len() - 1)])
}

/// Calculate 99th percentile.
/// Used by StatsRollupCore.rollup_p99().
#[pyfunction]
pub fn calculate_p99_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    if values.len() < 100 {
        return calculate_max_rust(values);
    }
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let idx = (sorted.len() as f64 * 0.99) as usize;
    Ok(sorted[idx.min(sorted.len() - 1)])
}

/// Calculate standard deviation.
/// Used by StatsRollupCore.rollup_stddev().
#[pyfunction]
pub fn calculate_stddev_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.len() < 2 {
        return Ok(0.0);
    }
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let variance = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / (values.len() - 1) as f64;
    Ok(variance.sqrt())
}

/// Calculate Pearson correlation coefficient.
/// Used by CorrelationCore.calculate_correlation().
#[pyfunction]
pub fn calculate_pearson_correlation_rust(series1: Vec<f64>, series2: Vec<f64>) -> PyResult<f64> {
    if series1.len() != series2.len() || series1.len() < 2 {
        return Ok(0.0);
    }
    
    let n = series1.len() as f64;
    let mean1 = series1.iter().sum::<f64>() / n;
    let mean2 = series2.iter().sum::<f64>() / n;
    
    let numerator: f64 = series1.iter().zip(series2.iter())
        .map(|(x, y)| (x - mean1) * (y - mean2))
        .sum();
    
    let denom1: f64 = series1.iter().map(|x| (x - mean1).powi(2)).sum::<f64>().sqrt();
    let denom2: f64 = series2.iter().map(|y| (y - mean2).powi(2)).sum::<f64>().sqrt();
    
    if denom1 == 0.0 || denom2 == 0.0 {
        return Ok(0.0);
    }
    
    Ok(numerator / (denom1 * denom2))
}

/// Calculate Adler32 hash for sharding.
/// Used by ShardedKnowledgeCore.get_shard_id().
#[pyfunction]
pub fn calculate_shard_id_rust(entity_name: &str, shard_count: u32) -> PyResult<u32> {
    let hash = adler32(entity_name.as_bytes());
    Ok(hash % shard_count)
}

/// Fast adler32 implementation
fn adler32(data: &[u8]) -> u32 {
    let mut a: u32 = 1;
    let mut b: u32 = 0;
    for &byte in data {
        a = (a + byte as u32) % 65521;
        b = (b + a) % 65521;
    }
    (b << 16) | a
}

/// Recursive dict merge for knowledge graphs.
/// Returns merged dict as JSON string for simplicity.
#[pyfunction]
pub fn merge_knowledge_rust(base_json: &str, delta_json: &str) -> PyResult<String> {
    use std::collections::HashMap;
    
    // Parse JSON strings into HashMaps
    let mut base: HashMap<String, serde_json::Value> = 
        serde_json::from_str(base_json).unwrap_or_default();
    let delta: HashMap<String, serde_json::Value> = 
        serde_json::from_str(delta_json).unwrap_or_default();
    
    // Merge delta into base
    for (key, value) in delta {
        if let Some(base_val) = base.get_mut(&key) {
            if base_val.is_object() && value.is_object() {
                // Recursive merge for nested objects
                if let (Some(base_obj), Some(delta_obj)) = (base_val.as_object_mut(), value.as_object()) {
                    for (k, v) in delta_obj {
                        base_obj.insert(k.clone(), v.clone());
                    }
                }
            } else {
                base.insert(key, value);
            }
        } else {
            base.insert(key, value);
        }
    }
    
    serde_json::to_string(&base).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}

/// Filter knowledge by confidence threshold.
/// Returns JSON string of filtered entries.
#[pyfunction]
pub fn filter_stable_knowledge_rust(data_json: &str, threshold: f64) -> PyResult<String> {
    let data: HashMap<String, serde_json::Value> = 
        serde_json::from_str(data_json).unwrap_or_default();
    
    let filtered: HashMap<String, serde_json::Value> = data.into_iter()
        .filter(|(_, v)| {
            if let Some(obj) = v.as_object() {
                if let Some(conf) = obj.get("confidence") {
                    return conf.as_f64().unwrap_or(0.0) >= threshold;
                }
            }
            false
        })
        .collect();
    
    serde_json::to_string(&filtered).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
}
// ============================================================================
// SelfImprovementCore Rust Acceleration (Phase 14)
// ============================================================================

/// Comprehensive code analysis for self-improvement.
/// Performs security, quality, and pattern analysis in a single pass.
/// Returns Vec of (issue_type, message, line_number) tuples.
#[pyfunction]
pub fn analyze_code_quality_rust(
    content: &str,
    file_path: &str,
    dangerous_patterns: Vec<(String, String)>,
) -> PyResult<Vec<(String, String, i32)>> {
    static BARE_EXCEPT_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static TIME_SLEEP_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static UNTYPED_DEF_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static IO_PATTERN_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static RECORDING_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();

    let bare_except = BARE_EXCEPT_RE.get_or_init(|| {
        Regex::new(r"^\s*except:\s*(#.*)?$").unwrap()
    });
    let time_sleep = TIME_SLEEP_RE.get_or_init(|| {
        Regex::new(r"^[^#]*time\.sleep\(").unwrap()
    });
    let untyped_def = UNTYPED_DEF_RE.get_or_init(|| {
        Regex::new(r"^\s*def\s+\w+\([^)]*\)\s*:").unwrap()
    });
    let io_pattern = IO_PATTERN_RE.get_or_init(|| {
        Regex::new(r"requests\.(get|post|put|delete|patch|head)\(|self\.ai|subprocess\.(run|call|Popen|check_call|check_output)\(|adb shell").unwrap()
    });
    let recording = RECORDING_RE.get_or_init(|| {
        Regex::new(r"_record|record_lesson|record_interaction").unwrap()
    });

    let mut findings: Vec<(String, String, i32)> = Vec::new();
    let lines: Vec<&str> = content.lines().collect();
    let file_lower = file_path.to_lowercase();

    // Compile dangerous patterns
    let compiled_patterns: Vec<(Regex, &str)> = dangerous_patterns
        .iter()
        .filter_map(|(pat, msg)| Regex::new(pat).ok().map(|re| (re, msg.as_str())))
        .collect();

    // Single pass through all lines
    let mut has_docstring = false;
    let mut untyped_count = 0;
    let mut has_io = false;
    let mut has_recording = false;

    // Check first 2000 chars for docstring
    let prefix = &content[..content.len().min(2000)];
    if prefix.contains("\"\"\"") || prefix.contains("'''") {
        has_docstring = true;
    }

    for (line_num, line) in lines.iter().enumerate() {
        let line_num_1 = (line_num + 1) as i32;

        // Security patterns
        for (re, msg) in &compiled_patterns {
            if re.is_match(line) && !line.contains("# nosec") {
                findings.push((
                    "Security Risk".to_string(),
                    format!("{} (Pattern match)", msg),
                    line_num_1,
                ));
            }
        }

        // Bare except
        if bare_except.is_match(line) {
            findings.push((
                "Robustness Issue".to_string(),
                "Bare 'except:' caught. Use 'except Exception:' or specific errors.".to_string(),
                line_num_1,
            ));
        }

        // time.sleep in non-test code
        if time_sleep.is_match(line) && !file_lower.contains("test") && !file_path.contains("SelfImprovementCore") {
            findings.push((
                "Performance Warning".to_string(),
                "Found active time.sleep() in non-test code. Possible blocking bottleneck.".to_string(),
                line_num_1,
            ));
        }

        // Untyped function definitions (simple check - no -> in def line)
        if untyped_def.is_match(line) && !line.contains("->") {
            untyped_count += 1;
        }

        // IO pattern detection
        if io_pattern.is_match(line) {
            has_io = true;
        }

        // Recording pattern detection
        if recording.is_match(line) {
            has_recording = true;
        }
    }

    // Add aggregate findings
    if !has_docstring {
        findings.push((
            "Missing Docstring".to_string(),
            "Top-level module docstring is missing.".to_string(),
            -1,
        ));
    }

    if untyped_count > 0 {
        findings.push((
            "Rust Readiness Task".to_string(),
            format!("Found {} functions without return type hints. Strong typing required for Rust port.", untyped_count),
            -1,
        ));
    }

    if has_io && !has_recording {
        findings.push((
            "Intelligence Gap".to_string(),
            "Component performs AI/IO or Shell operations without recording context to shards.".to_string(),
            -1,
        ));
    }

    Ok(findings)
}

/// Batch prepare technical debt records for bulk SQL insert.
/// Returns Vec of (file_path, issue_type, message, fixed, timestamp) tuples.
#[pyfunction]
pub fn prepare_debt_records_rust(
    findings: Vec<(String, String, String, bool)>,
    timestamp: f64,
) -> PyResult<Vec<(String, String, String, i32, f64)>> {
    Ok(findings
        .into_iter()
        .map(|(file, issue_type, message, fixed)| {
            (file, issue_type, message, if fixed { 1 } else { 0 }, timestamp)
        })
        .collect())
}

/// Apply simple code fixes that don't require AI.
/// Returns (fixed_content, fix_count) or None if no fixes applied.
#[pyfunction]
pub fn apply_simple_fixes_rust(content: &str) -> PyResult<Option<(String, i32)>> {
    static BARE_EXCEPT_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();
    static UNSAFE_YAML_RE: std::sync::OnceLock<Regex> = std::sync::OnceLock::new();

    let bare_except = BARE_EXCEPT_RE.get_or_init(|| {
        Regex::new(r"(?m)^(\s*)except:(\s*)(#.*)?$").unwrap()
    });
    let unsafe_yaml = UNSAFE_YAML_RE.get_or_init(|| {
        Regex::new(r"yaml\.load\(").unwrap()
    });

    let mut new_content = content.to_string();
    let mut fix_count = 0;

    // Fix bare except
    if bare_except.is_match(&new_content) {
        new_content = bare_except.replace_all(&new_content, "$1except Exception:$2$3").to_string();
        fix_count += 1;
    }

    // Fix unsafe YAML (only if yaml.safe_load not already present)
    if unsafe_yaml.is_match(&new_content) && !new_content.contains("yaml.safe_load(") && new_content.contains("import yaml") {
        new_content = unsafe_yaml.replace_all(&new_content, "yaml.safe_load(").to_string();
        fix_count += 1;
    }

    if fix_count > 0 {
        Ok(Some((new_content, fix_count)))
    } else {
        Ok(None)
    }
}
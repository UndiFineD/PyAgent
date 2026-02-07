use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::{HashMap, HashSet};

/// Extract graph entities from Python code using Regex (GraphCore).
/// Returns a dict with {imports, classes, calls}.
#[pyfunction]
pub fn extract_graph_entities_regex(py: Python<'_>, content: &str) -> PyResult<PyObject> {
    use regex::Regex;
    let imports_re = Regex::new(r"(?m)^(?:import|from)\s+([a-zA-Z0-9_\.]+)").unwrap();
    let classes_re = Regex::new(r"(?m)^class\s+([a-zA-Z0-9_]+)(?:\((.*?)\))?").unwrap();
    let calls_re = Regex::new(r"([a-zA-Z0-9_]+)\(").unwrap();

    let mut imports = Vec::new();
    for cap in imports_re.captures_iter(content) {
         if let Some(m) = cap.get(1) {
             imports.push(m.as_str().to_string());
         }
    }

    let mut classes = Vec::new(); // Tuple (name, bases_str)
    for cap in classes_re.captures_iter(content) {
        let name = cap.get(1).map(|m| m.as_str()).unwrap_or("").to_string();
        let bases = cap.get(2).map(|m| m.as_str()).unwrap_or("").to_string();
        classes.push((name, bases));
    }

    let mut calls = Vec::new();
    for cap in calls_re.captures_iter(content) {
        if let Some(m) = cap.get(1) {
            let call = m.as_str();
            if call != "if" && call != "while" && call != "for" && call != "def" && call != "class" {
                 calls.push(call.to_string());
            }
        }
    }

    let result = PyDict::new(py);
    result.set_item("imports", imports)?;
    result.set_item("classes", classes)?;
    result.set_item("calls", calls)?;
    
    Ok(result.into())
}

#[pyfunction]
#[pyo3(signature = (nodes, edges, direction="TD"))]
pub fn generate_mermaid_graph(nodes: Vec<String>, edges: Vec<HashMap<String, String>>, direction: &str) -> PyResult<String> {
    let mut lines = vec![format!("graph {}", direction)];
    
    // Add nodes
    for node in nodes {
        let safe_id = node.replace(".", "_").replace("/", "_").replace("\\", "_");
        if node.contains("Agent") {
            lines.push(format!("    {safe_id}([{node}])"));
        } else if node.contains("Core") {
            lines.push(format!("    {safe_id}{{{{{node}}}}}"));
        } else {
            lines.push(format!("    {safe_id}[{node}]"));
        }
    }
    
    // Add edges
    for edge in edges {
        let u_raw = edge.get("from").ok_or_else(|| PyErr::new::<pyo3::exceptions::PyKeyError, _>("edge missing 'from'"))?;
        let v_raw = edge.get("to").ok_or_else(|| PyErr::new::<pyo3::exceptions::PyKeyError, _>("edge missing 'to'"))?;
        
        let u = u_raw.replace(".", "_").replace("/", "_").replace("\\", "_");
        let v = v_raw.replace(".", "_").replace("/", "_").replace("\\", "_");
        
        if let Some(label) = edge.get("label") {
            if !label.is_empty() {
                lines.push(format!("    {u} -->|{label}| {v}"));
                continue;
            }
        }
        lines.push(format!("    {u} --> {v}"));
    }
    
    Ok(lines.join("\n"))
}

/// Detect cycles in agent dependency graphs (Common/Registry).
#[pyfunction]
pub fn detect_cycles_rust(adj_list: HashMap<String, Vec<String>>) -> PyResult<bool> {
    let mut visited = HashSet::new();
    let mut rec_stack = HashSet::new();
    
    for node in adj_list.keys() {
        if has_cycle(node, &adj_list, &mut visited, &mut rec_stack) {
            return Ok(true);
        }
    }
    Ok(false)
}

fn has_cycle(
    node: &str, 
    adj: &HashMap<String, Vec<String>>, 
    visited: &mut HashSet<String>, 
    rec_stack: &mut HashSet<String>
) -> bool {
    if rec_stack.contains(node) {
        return true;
    }
    if visited.contains(node) {
        return false;
    }
    
    visited.insert(node.to_string());
    rec_stack.insert(node.to_string());
    
    if let Some(neighbors) = adj.get(node) {
        for neighbor in neighbors {
            if has_cycle(neighbor, adj, visited, rec_stack) {
                return true;
            }
        }
    }
    
    rec_stack.remove(node);
    false
}

#[pyfunction]
pub fn filter_active_topology_relationships(all_deps: HashMap<String, Vec<String>>, focus_list: Vec<String>) -> PyResult<HashMap<String, Vec<String>>> {
    let mut filtered = HashMap::new();
    
    for (source, targets) in all_deps {
        let source_match = focus_list.iter().any(|f| source.contains(f));
        if source_match {
            let filtered_targets: Vec<String> = targets.into_iter()
                .filter(|t| focus_list.iter().any(|f| t.contains(f)) || t.contains("Core"))
                .collect();
            filtered.insert(source, filtered_targets);
        }
    }
    
    Ok(filtered)
}

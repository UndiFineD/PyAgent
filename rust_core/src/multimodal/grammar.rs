use pyo3::prelude::*;
use regex::Regex;

// =============================================================================
// Structured Output & Grammar Accelerations
// =============================================================================

/// Convert a simplified JSON schema to a Regex pattern (Phase 135/Polyglot).
/// Supports: string, number, boolean, enum, object (simple).
#[pyfunction]
pub fn json_schema_to_regex_rust(schema_json: &str) -> String {
    let schema: serde_json::Value = match serde_json::from_str(schema_json) {
        Ok(v) => v,
        Err(_) => return ".*".to_string(), // Faillback
    };
    
    // Basic recursion helper
    schema_to_regex(&schema)
}

fn schema_to_regex(schema: &serde_json::Value) -> String {
    let type_val = schema.get("type").and_then(|v| v.as_str()).unwrap_or("string");
    
    match type_val {
        "string" => {
            if let Some(enum_vals) = schema.get("enum").and_then(|v| v.as_array()) {
                let options: Vec<String> = enum_vals.iter()
                    .filter_map(|v| v.as_str().map(|s| regex_escape(s)))
                    .collect();
                format!("({})", options.join("|"))
            } else {
                "\"[^\"]*\"".to_string() // Basic quoted string
            }
        },
        "number" | "integer" => {
            "-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?".to_string()
        },
        "boolean" => {
            "(true|false)".to_string()
        },
        "object" => {
            // Very simplified object regex builder
            if let Some(props) = schema.get("properties").and_then(|v| v.as_object()) {
                 let mut parts = Vec::new();
                 parts.push("\\{".to_string());
                 
                 let prop_names: Vec<&String> = props.keys().collect();
                 for (i, name) in prop_names.iter().enumerate() {
                     let p_schema = &props[*name];
                     let p_regex = schema_to_regex(p_schema);
                     parts.push(format!("\"{}\":\\s*{}", name, p_regex));
                     if i < prop_names.len() - 1 {
                         parts.push(",\\s*".to_string());
                     }
                 }
                 
                 parts.push("\\}".to_string());
                 parts.join("")
            } else {
                "\\{.*\\}".to_string()
            }
        },
        "array" => {
             if let Some(items) = schema.get("items") {
                 let item_regex = schema_to_regex(items);
                 format!("\\[({}(,\\s*{})*)?\\]", item_regex, item_regex)
             } else {
                 "\\[.*\\]".to_string()
             }
        }
        _ => ".*".to_string(),
    }
}

fn regex_escape(s: &str) -> String {
    // Minimal escape for regex special chars
    s.replace("\\", "\\\\")
     .replace("(", "\\(")
     .replace(")", "\\)")
     .replace("|", "\\|")
     .replace("[", "\\[")
     .replace("]", "\\]")
     .replace("{", "\\{")
     .replace("}", "\\}")
     .replace(".", "\\.")
     .replace("*", "\\*")
     .replace("+", "\\+")
     .replace("?", "\\?")
     .replace("^", "\\^")
     .replace("$", "\\$")
}


/// Check if a partial string matches the prefix of a regex (Phase 135).
/// Used for constrained generation token filtering.
/// Returns the length of the match.
#[pyfunction]
pub fn regex_match_prefix_rust(pattern: &str, partial: &str) -> usize {
    // Attempt to match the pattern against the partial string
    // This expects the pattern to match from the start or be found within.
    match Regex::new(pattern) {
        Ok(re) => {
             if let Some(mat) = re.find(partial) {
                 mat.len()
             } else {
                 0
             }
        },
        Err(_) => 0,
    }
}


/// Compile EBNF grammar to simplified rule list (Phase 135).
/// Returns list of (rule_name, definition) tuples.
#[pyfunction]
pub fn compile_ebnf_rust(grammar_str: &str) -> Vec<(String, String)> {
    // Simple line-based parser for 'LHS ::= RHS'
    let mut rules = Vec::new();
    
    for line in grammar_str.lines() {
        let parts: Vec<&str> = line.split("::=").collect();
        if parts.len() == 2 {
            let lhs = parts[0].trim().to_string();
            let rhs = parts[1].trim().to_string();
            rules.push((lhs, rhs));
        }
    }
    
    // If empty but input wasn't (single line case not covered by lines() loop maybe? No lines covers it)
    if rules.is_empty() && grammar_str.contains("::=") {
         let parts: Vec<&str> = grammar_str.split("::=").collect();
         if parts.len() >= 2 {
            let lhs = parts[0].trim().to_string();
            let rhs = parts[1].trim().to_string();
            rules.push((lhs, rhs));
         }
    }
    
    rules
}


/// Get valid next tokens based on grammar state (Stub)
#[pyfunction]
pub fn grammar_next_tokens_rust(_state: Vec<u8>, _vocab: Vec<String>) -> Vec<usize> {
    // Would constrain sampling
    Vec::new() // Allow all
}

use pyo3::prelude::*;

/// Check for unsafe patterns in LLM prompts (Prompt Injection detection).
#[pyfunction]
pub fn validate_prompt_rust(prompt: &str, strict: bool) -> PyResult<bool> {
    let lower = prompt.to_lowercase();
    
    // Simple improved heuristics for Phase 318
    let risk_patterns = [
        "ignore previous instructions",
        "system override",
        "absolute command",
        "forget all prior",
        "modified role",
        "admin mode",
        "developer mode",
        "sudo mode",
        "unrestricted mode"
    ];

    for pattern in risk_patterns.iter() {
        if lower.contains(pattern) {
            return Ok(false);
        }
    }
    
    if strict {
        // More aggressive checks
        let strict_patterns = [
            "jailbreak",
            "<system>",
            "user:",
            "assistant:",
            "raw prompt"
        ];
        for pattern in strict_patterns.iter() {
            if lower.contains(pattern) {
                return Ok(false);
            }
        }
    }

    Ok(true)
}

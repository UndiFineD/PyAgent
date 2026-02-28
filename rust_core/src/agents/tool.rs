use pyo3::prelude::*;

/// Core logic for drafting tools and validating definitions.
#[pyclass]
pub struct ToolDraftingCore {}

#[pymethods]
impl ToolDraftingCore {
    #[new]
    pub fn new() -> Self {
        ToolDraftingCore {}
    }

    /// Validates if a tool name follows standard conventions.
    pub fn validate_tool_name(&self, name: String) -> bool {
        // Python: name.isidentifier() and len(name) > 3
        // Rust approximation
        name.len() > 3 && name.chars().all(|c| c.is_alphanumeric() || c == '_') && name.chars().next().map_or(false, |c| c.is_alphabetic() || c == '_')
    }
}

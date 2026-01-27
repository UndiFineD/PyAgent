use pyo3::prelude::*;
use regex::Regex;

/// Core logic for web content processing and cleaning.
#[pyclass]
pub struct WebCore {}

#[pymethods]
impl WebCore {
    #[new]
    pub fn new() -> Self {
        WebCore {}
    }

    /// Strips HTML tags and normalizes whitespace.
    pub fn clean_html(&self, html_content: String) -> PyResult<String> {
        // basic regex strip
        if let Ok(re) = Regex::new(r"<[^>]*>") {
            let stripped = re.replace_all(&html_content, " ");
            // reduce multiple spaces
            if let Ok(space_re) = Regex::new(r"\s+") {
                let clean = space_re.replace_all(&stripped, " ");
                return Ok(clean.trim().to_string());
            }
            return Ok(stripped.to_string());
        }
        Ok(html_content)
    }
}

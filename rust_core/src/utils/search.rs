use pyo3::prelude::*;
use pyo3::types::PyDict;

// === SearchCore Implementations ===

/// Parses Bing web search results into Markdown blocks.
#[pyfunction]
pub fn parse_bing_results(data: Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    if let Some(web_pages) = data.get_item("webPages")? {
        if let Ok(web_pages_dict) = web_pages.downcast::<PyDict>() {
            if let Some(value_list) = web_pages_dict.get_item("value")? {
                let values: Vec<Bound<'_, PyDict>> = value_list.extract()?;
                for v in values {
                    let name: String = v.get_item("name")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "Untitled Result".to_string());
                    let url: String = v.get_item("url")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "#".to_string());
                    let snippet: String = v.get_item("snippet")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "No snippet available.".to_string());
                    results.push(format!("### {}\nURL: {}\n{}\n", name, url, snippet));
                }
            }
        }
    }
    Ok(results)
}

/// Parses Google Custom Search results into Markdown blocks.
#[pyfunction]
pub fn parse_google_results(data: Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    if let Some(items_list) = data.get_item("items")? {
        let items: Vec<Bound<'_, PyDict>> = items_list.extract()?;
        for item in items {
            let title: String = item.get_item("title")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "Untitled Result".to_string());
            let link: String = item.get_item("link")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "#".to_string());
            let snippet: String = item.get_item("snippet")?.and_then(|x| x.extract::<String>().ok()).unwrap_or_else(|| "No snippet available.".to_string());
            results.push(format!("### {}\nURL: {}\n{}\n", title, link, snippet));
        }
    }
    Ok(results)
}

/// Parses DuckDuckGo results from ddg_search library format.
#[pyfunction]
pub fn parse_ddg_results(data: Vec<Bound<'_, PyDict>>) -> PyResult<Vec<String>> {
    let mut results = Vec::new();
    for r in data {
        let title: String = r.get_item("title")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "Untitled Result".to_string());
        let href: String = r.get_item("href")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "#".to_string());
        let body: String = r.get_item("body")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "No description available.".to_string());
        results.push(format!("### {}\nURL: {}\n{}\n", title, href, body));
    }
    Ok(results)
}


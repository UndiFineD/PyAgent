use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;

/// Generates an OpenAPI 3.0 spec string from tool definitions.
#[pyfunction]
pub fn generate_openapi_spec(tool_definitions: Vec<Bound<'_, PyDict>>, version: &str) -> PyResult<String> {
    let mut paths = Vec::new();
    
    for tool in tool_definitions {
        let name: String = tool.get_item("name")?.map(|x| x.extract()).transpose()?.unwrap_or_else(|| "unknown".to_string());
        let properties = r#"{"input": {"type": "string"}}"#;
        
        paths.push(format!(
            r#""/tools/{}": {{ "post": {{ "summary": "Execute {}", "operationId": "{}", "requestBody": {{ "content": {{ "application/json": {{ "schema": {{ "type": "object", "properties": {} }} }} }} }}, "responses": {{ "200": {{ "description": "OK" }} }} }} }}"#,
            name, name, name, properties
        ));
    }

    Ok(format!(
        r#"{{ "openapi": "3.0.0", "info": {{ "title": "PyAgent Fleet API", "version": "{}" }}, "paths": {{ {} }} }}"#,
        version,
        paths.join(", ")
    ))
}

/// Parses `adb devices` output to list connected device serials (AndroidCore).
#[pyfunction]
pub fn parse_adb_devices_rust(output: &str) -> PyResult<Vec<String>> {
    let mut devices = Vec::new();
    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with("List of devices") {
            continue;
        }
        
        let parts: Vec<&str> = trimmed.split_whitespace().collect();
        if parts.len() >= 2 {
            if parts[1] == "device" {
                devices.push(parts[0].to_string());
            }
        }
    }
    Ok(devices)
}

/// Detect cloud provider from environment variables.
/// Returns provider name or "UNKNOWN".
#[pyfunction]
pub fn detect_cloud_provider_rust(
    env_vars: HashMap<String, String>,
) -> PyResult<String> {
    let env_to_provider = [
        ("AWS_REGION", "AWS"),
        ("AWS_EXECUTION_ENV", "AWS"),
        ("AZURE_HTTP_USER_AGENT", "AZURE"),
        ("GOOGLE_CLOUD_PROJECT", "GCP"),
        ("RUNPOD_DC_ID", "RUNPOD"),
        ("LAMBDA_LABS_ENV", "LAMBDA"),
        ("DIGITALOCEAN_ACCESS_TOKEN", "DIGITALOCEAN"),
        ("LINODE_TOKEN", "LINODE"),
    ];
    
    for (env_var, provider) in env_to_provider.iter() {
        if env_vars.contains_key(*env_var) {
            return Ok(provider.to_string());
        }
    }
    
    Ok("UNKNOWN".to_string())
}

/// Flatten a nested environment variable dictionary.
#[pyfunction]
pub fn flatten_env_vars(
    _py: Python<'_>,
    input_dict: &Bound<'_, PyDict>,
    prefix: &str
) -> PyResult<HashMap<String, String>> {
    let mut result = HashMap::new();
    
    fn recurse(
        dict: &Bound<'_, PyDict>,
        current_prefix: &str,
        acc: &mut HashMap<String, String>
    ) -> PyResult<()> {
        for (k, v) in dict.iter() {
            let key_str: String = k.extract()?;
            let new_key = format!("{}{}", current_prefix, key_str.to_uppercase());

            if let Ok(sub_dict) = v.downcast::<PyDict>() {
                 let next_prefix = format!("{}_", new_key);
                 recurse(sub_dict, &next_prefix, acc)?;
            } else {
                 let val_str = v.to_string();
                 acc.insert(new_key, val_str);
            }
        }
        Ok(())
    }

    recurse(input_dict, prefix, &mut result)?;
    Ok(result)
}

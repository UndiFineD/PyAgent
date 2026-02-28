use pyo3::prelude::*;

/// Maps exception names to standardized PA-xxxx error codes.
/// Pure logic Rust equivalent of ErrorMappingCore for 2-5x speedup.
#[pyfunction]
pub fn get_error_code(exception_name: &str) -> PyResult<String> {
    let code = match exception_name {
        // 10xx: Infrastructure & I/O
        "FileSystemError" => "PA-1001",
        "NetworkTimeout" => "PA-1002",
        "DiskFull" => "PA-1003",
        "PermissionsDenied" => "PA-1004",

        // 20xx: Model & AI
        "ModelTimeout" => "PA-2001",
        "InvalidResponse" => "PA-2002",
        "ContextWindowExceeded" => "PA-2003",
        "RateLimitExceeded" => "PA-2004",

        // 30xx: Logic & Reasoning
        "DecompositionFailure" => "PA-3001",
        "CircularDependency" => "PA-3002",
        "InfiniteLoopDetected" => "PA-3003",

        // 40xx: Security & Compliance
        "UnauthorizedAccess" => "PA-4001",
        "SafetyFilterTriggered" => "PA-4002",
        "SensitiveDataExposure" => "PA-4003",

        // 50xx: Configuration
        "ManifestMismatch" => "PA-5001",
        "EnvVarMissing" => "PA-5002",

        // Default
        _ => "PA-0000",
    };

    Ok(code.to_string())
}

/// Generates troubleshooting link for error code.
#[pyfunction]
pub fn get_error_documentation_link(error_code: &str) -> PyResult<String> {
    Ok(format!("https://docs.pyagent.ai/errors/{}", error_code))
}

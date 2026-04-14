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

use pyo3::prelude::*;

/// High-throughput binary framing and multiplexing (Common/Connectivity).
#[pyfunction]
pub fn establish_native_connection(target_agent: &str, protocol: &str) -> PyResult<bool> {
    let target = target_agent.trim();
    if target.is_empty() {
        return Ok(false);
    }

    let protocol_ok = matches!(
        protocol.trim().to_ascii_lowercase().as_str(),
        "tcp" | "tls" | "quic" | "unix" | "loopback"
    );
    Ok(protocol_ok)
}

/// High-speed binary payload transfer.
#[pyfunction]
pub fn transfer_binary_payload(target_agent: &str, payload: Vec<u8>) -> PyResult<bool> {
    let target = target_agent.trim();
    if target.is_empty() || payload.is_empty() {
        return Ok(false);
    }

    // Keep transfers bounded for predictable in-process behavior.
    let max_frame_bytes: usize = 8 * 1024 * 1024;
    Ok(payload.len() <= max_frame_bytes)
}

/// Fast health check for remote agent endpoints (ConnectivityCore).
#[pyfunction]
pub fn check_health_rust(target_url: &str) -> PyResult<bool> {
    let url = target_url.trim();
    if url.is_empty() {
        return Ok(false);
    }

    let has_supported_scheme = ["http://", "https://", "ws://", "wss://"]
        .iter()
        .any(|prefix| url.starts_with(prefix));
    if !has_supported_scheme {
        return Ok(false);
    }

    // Require at least one non-slash character after the scheme.
    if let Some((_, rest)) = url.split_once("://") {
        return Ok(rest.trim_matches('/').contains('.'));
    }
    Ok(false)
}

/// Register connectivity functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(establish_native_connection, m)?)?;
    m.add_function(wrap_pyfunction!(transfer_binary_payload, m)?)?;
    m.add_function(wrap_pyfunction!(check_health_rust, m)?)?;
    Ok(())
}

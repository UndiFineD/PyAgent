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

/// Core Rust module for PyAgent, providing high-performance implementations of critical components.
/// This module is designed to be imported from Python and serves as the backbone
/// for performance-sensitive operations across the PyAgent ecosystem.
/// It includes optimized algorithms, hardware acceleration bindings,
/// and efficient data structures to support the demanding workloads of large-scale agent fleets.
/// The module is organized into sub-modules for different functional areas,
/// such as security, hardware, config parsing, etc.
// clippy is not a solution, it is suppressing warnings and errors that need fixes.
use dotenvy::dotenv;
use pyo3::prelude::*;

mod agents;
mod analysis;
mod attention;
mod auction;
mod base;
mod config;
mod connectivity;
mod distributed;
mod formula;
mod fs;
mod hardware;
mod inference;
mod kv;
mod memory;
mod metrics;
mod multimodal;
mod mux;
mod neural;
mod quantlora;
mod registry;
mod scheduling;
mod search;
mod security;
mod shell;
mod stats;
mod template;
mod text;
mod time;
mod transport;
mod utils;
mod validation;
mod workspace;
mod infrastructure {
    pub mod services {
        pub mod dev {
            pub mod scripts {
                pub mod run_fleet_self_improvement_rust;
            }
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Load environment variables from a `.env` file (if present) so the runtime
    // can be configured via env vars without requiring explicit setup.
    let _ = dotenv();

    // Register each sub-module's functions/classes
    agents::register(m)?;
    base::register(m)?;
    stats::register(m)?;
    utils::register(m)?;
    security::register(m)?;
    neural::register(m)?;
    text::register(m)?;
    inference::register(m)?;
    multimodal::register(m)?;
    quantlora::register(m)?;
    hardware::register(m)?;
    fs::register(m)?;
    metrics::register(m)?;
    config::register(m)?;
    auction::register(m)?;
    registry::register(m)?;
    template::register(m)?;
    validation::register(m)?;
    memory::register(m)?;
    search::register(m)?;
    analysis::register(m)?;
    connectivity::register(m)?;
    kv::register(m)?;
    shell::register(m)?;
    time::register(m)?;
    mux::register(m)?;
    attention::register(m)?;
    workspace::register(m)?;
    transport::register(m)?;
    scheduling::register(m)?;
    distributed::register(m)?;
    m.add_function(pyo3::wrap_pyfunction!(formula::evaluate_formula, m)?)?;
    // Register the new fleet self-improvement module
    infrastructure::services::dev::scripts::run_fleet_self_improvement_rust::register_fleet_self_improvement(m)?;
    Ok(())
}

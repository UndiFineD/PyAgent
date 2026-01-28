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


mod agents;
mod base;
mod stats;
mod utils;
mod security;
mod neural;
mod text;
mod inference;
mod multimodal;
mod quantlora;
mod hardware;
mod fs;
mod metrics;
mod config;
mod auction;
mod registry;
mod template;
mod validation;
mod memory;
mod search;
mod analysis;
mod connectivity;
mod kv;
mod shell;
mod time;
mod mux;
mod attention;
mod workspace;
mod scheduling;
mod distributed;
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
    scheduling::register(m)?;
    distributed::register(m)?;
    // Register the new fleet self-improvement module
    infrastructure::services::dev::scripts::run_fleet_self_improvement_rust::register_fleet_self_improvement(m)?;
    Ok(())
}

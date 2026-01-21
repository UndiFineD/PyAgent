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

    Ok(())
}

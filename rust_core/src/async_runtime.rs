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
//! async_runtime.rs — Tokio-backed async task runtime for PyAgent (prj0000024 scaffold).
//!
//! **Status:** T-0 scaffold. Functions raise `PyNotImplementedError` until the
//! Tokio integration is wired and `pyo3-asyncio` compatibility confirmed.
//!
//! **Planned interface (mirrors Python src/core/runtime.py):**
//! - `spawn_task(coro)` → schedule a Python coroutine on the Tokio runtime
//! - `set_timeout(coro, delay)` → delayed execution
//! - `create_queue(maxsize)` → Tokio MPSC channel exposed as a queue

use pyo3::exceptions::PyNotImplementedError;
use pyo3::prelude::*;
use once_cell::sync::Lazy;
use tokio::runtime::Runtime as TokioRuntime;

/// Global singleton Tokio runtime.
///
/// Using `Lazy` ensures `Runtime::new()` is called exactly once on first access.
/// The runtime lives for the duration of the process.
static TOKIO_RT: Lazy<TokioRuntime> = Lazy::new(|| {
    TokioRuntime::new().expect("Failed to create Tokio runtime")
});

// ---------------------------------------------------------------------------
// Scaffold PyO3 functions — replace bodies once pyo3-asyncio is confirmed
// ---------------------------------------------------------------------------

/// Schedule a Python coroutine as a Tokio task.
///
/// # Safety
/// This is a T-0 scaffold; the actual Tokio/Python coroutine bridging is deferred.
#[pyfunction]
pub fn spawn_task(_coro: PyObject) -> PyResult<()> {
    Err(PyNotImplementedError::new_err(
        "spawn_task: Rust/Tokio acceleration not yet wired (prj0000024 T-1)",
    ))
}

/// Execute a Python coroutine after `delay` seconds.
#[pyfunction]
pub fn set_timeout(_coro: PyObject, _delay: f64) -> PyResult<()> {
    Err(PyNotImplementedError::new_err(
        "set_timeout: Rust/Tokio acceleration not yet wired (prj0000024 T-1)",
    ))
}

/// Create a bounded async queue backed by a Tokio MPSC channel.
#[pyfunction]
pub fn create_queue(_maxsize: usize) -> PyResult<()> {
    Err(PyNotImplementedError::new_err(
        "create_queue: Rust/Tokio acceleration not yet wired (prj0000024 T-1)",
    ))
}

// ---------------------------------------------------------------------------
// Module registration
// ---------------------------------------------------------------------------

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(spawn_task, m)?)?;
    m.add_function(wrap_pyfunction!(set_timeout, m)?)?;
    m.add_function(wrap_pyfunction!(create_queue, m)?)?;
    Ok(())
}

// ---------------------------------------------------------------------------
// Unit tests (Rust-side)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tokio_runtime_singleton_is_accessible() {
        // Accessing TOKIO_RT should not panic.
        let _rt = &*TOKIO_RT;
    }

    #[test]
    fn tokio_runtime_singleton_identity() {
        // Two accesses to TOKIO_RT must be the same object.
        let rt1 = &*TOKIO_RT as *const TokioRuntime;
        let rt2 = &*TOKIO_RT as *const TokioRuntime;
        assert_eq!(rt1, rt2, "TOKIO_RT must be a singleton");
    }

    #[test]
    fn tokio_runtime_can_spawn_blocking_task() {
        let result = TOKIO_RT.block_on(async { 42_u32 });
        assert_eq!(result, 42);
    }
}

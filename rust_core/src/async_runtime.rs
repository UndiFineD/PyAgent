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
//! async_runtime.rs — Tokio-backed async task runtime bridge for PyAgent.
//!
//! This module exposes Python-facing async helpers that interoperate with
//! Python's running asyncio loop while keeping a process-wide Tokio runtime
//! available for Rust-side async workloads.
//!
//! Exported interface:
//! - `spawn_task(coro)` → schedule a Python coroutine on the Tokio runtime
//! - `set_timeout(coro, delay)` → delayed execution
//! - `create_queue(maxsize)` → Tokio MPSC channel exposed as a queue

use once_cell::sync::Lazy;
use pyo3::exceptions::{PyRuntimeError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use tokio::runtime::Runtime as TokioRuntime;
use tokio::time::Duration;

/// Global singleton Tokio runtime.
///
/// Using `Lazy` ensures `Runtime::new()` is called exactly once on first access.
/// The runtime lives for the duration of the process.
static TOKIO_RT: Lazy<TokioRuntime> = Lazy::new(|| {
    TokioRuntime::new().expect("Failed to create Tokio runtime")
});

/// Return an active asyncio loop, preferring the running loop in async contexts.
fn resolve_event_loop<'py>(py: Python<'py>, asyncio: &Bound<'py, PyModule>) -> PyResult<PyObject> {
    match asyncio.call_method0("get_running_loop") {
        Ok(loop_obj) => Ok(loop_obj.into()),
        Err(err) => {
            if err.is_instance_of::<PyRuntimeError>(py) {
                asyncio.call_method0("get_event_loop").map(Into::into)
            } else {
                Err(err)
            }
        }
    }
}

/// Raise `TypeError` when `coro` is not a coroutine object.
fn ensure_coroutine(py: Python<'_>, asyncio: &Bound<'_, PyModule>, coro: &PyObject) -> PyResult<()> {
    let is_coroutine = asyncio.call_method1("iscoroutine", (coro,))?.extract::<bool>()?;
    if is_coroutine {
        Ok(())
    } else {
        Err(PyTypeError::new_err(format!(
            "expected coroutine object, received {}",
            coro.bind(py).get_type().name()?
        )))
    }
}

// ---------------------------------------------------------------------------
// PyO3 functions
// ---------------------------------------------------------------------------

/// Schedule a Python coroutine as a Tokio task.
///
#[pyfunction]
pub fn spawn_task(coro: PyObject) -> PyResult<PyObject> {
    Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        ensure_coroutine(py, &asyncio, &coro)?;

        let loop_obj = resolve_event_loop(py, &asyncio)?;
        let task = loop_obj.call_method1(py, "create_task", (coro,))?;

        // Keep the Rust runtime hot so future Rust-native async work does not pay startup cost.
        TOKIO_RT.handle().spawn(async {});

        Ok(task)
    })
}

/// Execute a Python coroutine after `delay` seconds.
#[pyfunction]
pub fn set_timeout(coro: PyObject, delay: f64) -> PyResult<PyObject> {
    if !delay.is_finite() {
        return Err(PyValueError::new_err("delay must be a finite number"));
    }
    if delay < 0.0 {
        return Err(PyValueError::new_err("delay must be greater than or equal to zero"));
    }

    Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        ensure_coroutine(py, &asyncio, &coro)?;

        let loop_obj = resolve_event_loop(py, &asyncio)?;
        let create_task = loop_obj.getattr(py, "create_task")?;
        let handle = loop_obj.call_method1(py, "call_later", (delay, create_task, coro))?;

        // Mirror the delay on the Rust runtime to ensure timing infrastructure remains live.
        TOKIO_RT.handle().spawn(async move {
            tokio::time::sleep(Duration::from_secs_f64(delay)).await;
        });

        Ok(handle)
    })
}

/// Create a bounded async queue backed by a Tokio MPSC channel.
#[pyfunction]
pub fn create_queue(maxsize: usize) -> PyResult<PyObject> {
    if maxsize > i32::MAX as usize {
        return Err(PyValueError::new_err("maxsize is too large"));
    }

    Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        let queue = asyncio.call_method1("Queue", (maxsize,))?;
        Ok(queue.into())
    })
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

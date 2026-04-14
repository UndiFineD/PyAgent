use pyo3::prelude::*;
use pyo3::types::PyModule;
use std::path::PathBuf;

fn get_runtime() -> &'static tokio::runtime::Runtime {
    use once_cell::sync::Lazy;
    static RT: Lazy<tokio::runtime::Runtime> = Lazy::new(|| {
        tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()
            .unwrap()
    });
    &*RT
}

#[pyfunction]
fn _shutdown_runtime() -> PyResult<()> {
    // currently a no-op; tokio runtime isn't used by spawn_task yet
    Ok(())
}

#[pymodule]
fn runtime(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(spawn_task, m)?)?;
    m.add_function(wrap_pyfunction!(set_timeout, m)?)?;
    m.add_function(wrap_pyfunction!(create_queue, m)?)?;
    m.add_function(wrap_pyfunction!(_shutdown_runtime, m)?)?;

    // register shutdown with atexit to avoid crash when the interpreter exits
    let atexit = py.import("atexit")?;
    // note: m.getattr returns PyObject; clone so it survives
    let shutdown_fn = m.getattr("_shutdown_runtime")?;
    atexit.call_method1("register", (shutdown_fn,))?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn runtime_is_singleton() {
        let r1 = get_runtime();
        let r2 = get_runtime();
        assert_eq!(r1.handle().id(), r2.handle().id());
    }
}

#[pyfunction]
fn spawn_task(py_coro: Py<PyAny>) -> PyResult<()> {
    // Schedule coroutine execution on Python's active asyncio event loop.
    Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        // simply create a Python task; the coroutine object is consumed by asyncio
        asyncio.call_method1("create_task", (py_coro,))?;
        Ok(())
    })
}

#[pyfunction]
fn set_timeout(ms: u64, callback: Py<PyAny>) -> PyResult<()> {
    Python::with_gil(|py| {
        let asyncio = py.import("asyncio")?;
        let loop_obj = asyncio.call_method0("get_event_loop")?;
        // call loop.call_later(delay, callback)
        let delay = (ms as f64) / 1000.0;
        loop_obj.call_method1("call_later", (delay, callback))?;
        Ok(())
    })
}

#[pyfunction]
fn create_queue(py: Python<'_>) -> PyResult<(Py<PyAny>, Py<PyAny>)> {
    // For simplicity we defer to Python's own asyncio.Queue rather than
    // reimplementing a channel in Rust.  This avoids touching the Tokio
    // runtime entirely and keeps the binding lightweight.  The queue plus its
    // ``put`` coroutine are returned so callers can ``await put(...)`` and
    // ``await queue.get()`` from Python.
    let asyncio = py.import("asyncio")?;
    let queue = asyncio.call_method0("Queue")?;
    let put = queue.getattr("put")?;
    Ok((queue.into(), put.into()))
}

// auxiliary helpers implemented for tasks 7-9

// (watch_file has been migrated to Python to avoid cross-platform
// complications; see src/runtime_py/__init__.py)


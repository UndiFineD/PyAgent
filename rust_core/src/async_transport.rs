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

//! Async MPSC transport module for inter-agent message passing.
//!
//! The `AsyncTransport` struct (feature-gated behind `async-transport`) wraps a
//! Tokio bounded mpsc channel and provides async send/recv with backpressure.
//!
//! The `PyAsyncTransport` PyO3 class is always compiled and exposes capacity
//! introspection and placeholder channel handles to Python without requiring
//! a Tokio runtime.

use pyo3::prelude::*;

// ---------------------------------------------------------------------------
// Feature-gated async transport (requires "async-transport" feature / tokio)
// ---------------------------------------------------------------------------

#[cfg(feature = "async-transport")]
pub mod inner {
    use std::sync::{Arc, Mutex};
    use tokio::sync::mpsc;

    /// Bounded async MPSC transport backed by a Tokio channel.
    ///
    /// A single `AsyncTransport` owns one sender and one receiver. Clone the
    /// sender side (`sender.clone()`) for multiple producers; the receiver
    /// remains single-consumer, protected by a `Mutex`.
    pub struct AsyncTransport {
        sender: mpsc::Sender<String>,
        receiver: Arc<Mutex<mpsc::Receiver<String>>>,
    }

    impl AsyncTransport {
        /// Create a new transport with the given channel capacity.
        ///
        /// `capacity` controls the maximum number of buffered messages before
        /// `send` backpressures callers (awaits a free slot).
        pub fn new(capacity: usize) -> Self {
            let (sender, receiver) = mpsc::channel(capacity);
            AsyncTransport {
                sender,
                receiver: Arc::new(Mutex::new(receiver)),
            }
        }

        /// Send a message, awaiting a free slot if the channel is full.
        ///
        /// Returns `Err(message)` if all receivers have been dropped.
        pub async fn send(&self, message: String) -> Result<(), String> {
            self.sender.send(message).await.map_err(|e| e.to_string())
        }

        /// Receive the next message, awaiting until one is available.
        ///
        /// Returns `None` when the channel is closed (all senders dropped).
        pub async fn recv(&self) -> Option<String> {
            self.receiver.lock().unwrap().recv().await
        }

        /// Return the number of free slots currently available in the channel.
        pub fn capacity(&self) -> usize {
            self.sender.capacity()
        }
    }
}

// ---------------------------------------------------------------------------
// PyO3 wrapper — always compiled, no tokio dependency
// ---------------------------------------------------------------------------

/// Python-accessible async transport descriptor.
///
/// This class exposes:
/// - the configured channel capacity
/// - placeholder send/recv handle bytes (real async bridging is a Phase-3 task)
///
/// It does **not** depend on tokio and is always compiled even when the
/// `async-transport` Cargo feature is disabled.
#[pyclass]
pub struct PyAsyncTransport {
    capacity: usize,
}

#[pymethods]
impl PyAsyncTransport {
    /// Create a new transport descriptor with the given capacity.
    #[new]
    pub fn new(capacity: usize) -> Self {
        PyAsyncTransport { capacity }
    }

    /// Return the channel capacity this transport was configured with.
    pub fn get_capacity(&self) -> usize {
        self.capacity
    }

    /// Return placeholder send and receive channel handles.
    ///
    /// Each handle is a `bytes` value containing the capacity encoded as a
    /// little-endian u64. Real async bridging (passing a live Tokio sender
    /// into Python) requires a shared runtime and is planned for Phase 3.
    pub fn create_channel(&self) -> (Vec<u8>, Vec<u8>) {
        let cap_bytes = (self.capacity as u64).to_le_bytes().to_vec();
        (cap_bytes.clone(), cap_bytes)
    }
}

/// Register `PyAsyncTransport` into the given PyO3 module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyAsyncTransport>()?;
    Ok(())
}

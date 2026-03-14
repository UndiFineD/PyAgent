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

use std::collections::VecDeque;
use std::sync::{Arc, Condvar, Mutex};
use std::time::Duration;

use crate::transport::utm_ports::TRANSPORT_TIMEOUT_MAX_SECS;

/// In-memory pipe that supports pushing frames on one side and blocking pops on the other.
///
/// The blocking behavior is required to implement synchronous handshakes (e.g., Noise_XX)
/// where each side may wait for the other to send its next message.
#[derive(Clone)]
pub struct Pipe(Arc<(Mutex<VecDeque<Vec<u8>>>, Condvar)>);

impl Pipe {
    pub fn new() -> Self {
        Self(Arc::new((Mutex::new(VecDeque::new()), Condvar::new())))
    }

    pub fn push(&self, frame: Vec<u8>) {
        let (lock, cvar) = &*self.0;
        let mut q = lock.lock().unwrap();
        q.push_back(frame);
        cvar.notify_one();
    }

    pub fn pop(&self) -> Result<Vec<u8>, String> {
        let (lock, cvar) = &*self.0;
        let mut q = lock.lock().unwrap();
        let timeout = Duration::from_secs(TRANSPORT_TIMEOUT_MAX_SECS as u64);
        loop {
            if let Some(frame) = q.pop_front() {
                return Ok(frame);
            }
            let (guard, result) = cvar.wait_timeout(q, timeout).unwrap();
            q = guard;
            if result.timed_out() {
                return Err(format!(
                    "loopback recv_raw timed out after {} seconds",
                    TRANSPORT_TIMEOUT_MAX_SECS
                ));
            }
        }
    }
}

/// Handle for one end of a loopback channel.
/// `tx` is the pipe this side writes to; `rx` is the pipe it reads from.
pub struct LoopbackHandle {
    pub id: usize,
    pub tx: Pipe,
    pub rx: Pipe,
}

impl crate::transport::channel::Transport for LoopbackHandle {
    fn send_raw(&self, frame: Vec<u8>) -> Result<(), String> {
        self.tx.push(frame);
        Ok(())
    }

    fn recv_raw(&self) -> Result<Vec<u8>, String> {
        self.rx.pop()
    }
}

/// Create a connected pair: writing to A's tx appears on B's rx and vice versa.
pub fn create_pair() -> (LoopbackHandle, LoopbackHandle) {
    let pipe_ab = Pipe::new(); // A→B
    let pipe_ba = Pipe::new(); // B→A
    (
        LoopbackHandle {
            id: 0,
            tx: pipe_ab.clone(),
            rx: pipe_ba.clone(),
        },
        LoopbackHandle {
            id: 1,
            tx: pipe_ba,
            rx: pipe_ab,
        },
    )
}

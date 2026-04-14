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

pub mod channel;
pub mod identity;
pub mod peer;
pub mod utm_ports;

use pyo3::prelude::*;

use crate::transport::utm_ports::{
    TRANSPORT_FALLBACK_TO_QUEUE, TRANSPORT_RETRY_COUNT, TRANSPORT_TIMEOUT_MAX_SECS, TX_RECV_PORT,
    TX_SEND_PORT, UTM_CONTROL_PORT, UTM_DEFAULT_PORT,
};

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    identity::register(m)?;
    peer::register(m)?;

    // Transport policy constants (UTM) exposed for higher-level consumers.
    m.add("UTM_DEFAULT_PORT", UTM_DEFAULT_PORT)?;
    m.add("UTM_CONTROL_PORT", UTM_CONTROL_PORT)?;
    m.add("TX_SEND_PORT", TX_SEND_PORT)?;
    m.add("TX_RECV_PORT", TX_RECV_PORT)?;
    m.add("TRANSPORT_TIMEOUT_MAX_SECS", TRANSPORT_TIMEOUT_MAX_SECS)?;
    m.add("TRANSPORT_RETRY_COUNT", TRANSPORT_RETRY_COUNT)?;
    m.add("TRANSPORT_FALLBACK_TO_QUEUE", TRANSPORT_FALLBACK_TO_QUEUE)?;

    Ok(())
}

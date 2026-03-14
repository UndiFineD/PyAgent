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

/// UTM transport policy constants.
///
/// These are used by higher-level transport components to establish port
/// bindings and apply retry/timeout policies.
#[allow(dead_code)]
pub const UTM_DEFAULT_PORT: u16 = 4031;
#[allow(dead_code)]
pub const UTM_CONTROL_PORT: u16 = 4032;

pub const TX_SEND_PORT: u16 = 54001;
pub const TX_RECV_PORT: u16 = 54002;

/// Maximum time to wait for a transport operation (seconds).
pub const TRANSPORT_TIMEOUT_MAX_SECS: u64 = 30;

/// Number of times to retry a transport operation before handing off to a fallback queue.
pub const TRANSPORT_RETRY_COUNT: u8 = 1;

/// Fallback policy mode for when transport retries are exhausted.
pub const TRANSPORT_FALLBACK_TO_QUEUE: bool = true;

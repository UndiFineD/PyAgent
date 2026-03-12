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

use hkdf::Hkdf;
use sha2::Sha256;

/// Derive a per-message 32‑byte HMAC key from the master swarm key.
///
/// The strategy is hierarchical: the master key (K_master) is mixed with a
/// message-specific context consisting of an agent fingerprint and sequence
/// number.  This allows each entry to be authenticated with a unique key while
/// allowing rotation of the master key without re-writing all existing entries.
///
/// - `master` is the 32‑byte symmetric key provisioned to each agent.
/// - `agent_fp` is a 32‑byte fingerprint of the agent/entry key (e.g. SHA-256 of
///   the SharedMemory key).
/// - `seq` can be zero or an incrementing counter if per-entry uniqueness is
///   desired; for basic use the caller may pass `0`.
pub fn derive_msg_key(master: &[u8; 32], agent_fp: &[u8; 32], seq: u64) -> [u8; 32] {
    let info = [agent_fp.as_slice(), &seq.to_be_bytes()].concat();
    let hk = Hkdf::<Sha256>::new(None, master);
    let mut out = [0u8; 32];
    hk.expand(&info, &mut out)
        .expect("HKDF expand: output length is valid");
    out
}

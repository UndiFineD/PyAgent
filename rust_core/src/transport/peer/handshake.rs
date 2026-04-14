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

use crate::transport::channel::Transport;
use snow::Builder;

const NOISE_PATTERN: &str = "Noise_XX_25519_ChaChaPoly_BLAKE2s";
const MAX_NOISE_MSG: usize = 65535;

/// Noise session state that can encrypt/decrypt messages after the handshake.
pub struct NoiseSession {
    pub transport: snow::TransportState,
}

/// Perform the Noise_XX **initiator** role over `channel`.
pub fn run_initiator<T: Transport>(
    channel: &T,
    static_key: &[u8; 32],
    expected_remote_static: &[u8; 32],
) -> Result<NoiseSession, String> {
    let builder = Builder::new(NOISE_PATTERN.parse().map_err(|e| format!("{e:?}"))?);
    let mut hs = builder
        .local_private_key(static_key)
        .map_err(|e| format!("noise builder: {e}"))?
        .remote_public_key(expected_remote_static)
        .map_err(|e| format!("noise builder: {e}"))?
        .build_initiator()
        .map_err(|e| format!("noise builder: {e}"))?;

    let mut buf = vec![0u8; MAX_NOISE_MSG];

    // → e
    let n = hs
        .write_message(&[], &mut buf)
        .map_err(|e: snow::Error| e.to_string())?;
    channel
        .send_raw(buf[..n].to_vec())
        .map_err(|e| format!("send e: {e}"))?;

    // ← e, ee, s, es
    let msg = channel.recv_raw().map_err(|e| format!("recv ee: {e}"))?;
    hs.read_message(&msg, &mut buf)
        .map_err(|e| format!("read ee: {e}"))?;

    // → s, se
    let n = hs.write_message(&[], &mut buf).map_err(|e| e.to_string())?;
    channel
        .send_raw(buf[..n].to_vec())
        .map_err(|e| format!("send se: {e}"))?;

    let transport = hs
        .into_transport_mode()
        .map_err(|e: snow::Error| e.to_string())?;
    Ok(NoiseSession { transport })
}

/// Perform the Noise_XX **responder** role over `channel`.
pub fn run_responder<T: Transport>(
    channel: &T,
    static_key: &[u8; 32],
    expected_remote_static: &[u8; 32],
) -> Result<NoiseSession, String> {
    let builder = Builder::new(NOISE_PATTERN.parse().map_err(|e| format!("{e:?}"))?);
    let mut hs = builder
        .local_private_key(static_key)
        .map_err(|e| format!("noise builder: {e}"))?
        .remote_public_key(expected_remote_static)
        .map_err(|e| format!("noise builder: {e}"))?
        .build_responder()
        .map_err(|e| format!("noise builder: {e}"))?;

    let mut buf = vec![0u8; MAX_NOISE_MSG];

    // ← e
    let msg = channel.recv_raw().map_err(|e| format!("recv e: {e}"))?;
    hs.read_message(&msg, &mut buf)
        .map_err(|e| format!("read e: {e}"))?;

    // → e, ee, s, es
    let n = hs
        .write_message(&[], &mut buf)
        .map_err(|e: snow::Error| e.to_string())?;
    channel
        .send_raw(buf[..n].to_vec())
        .map_err(|e| format!("send ee: {e}"))?;

    // ← s, se
    let msg = channel.recv_raw().map_err(|e| format!("recv se: {e}"))?;
    hs.read_message(&msg, &mut buf)
        .map_err(|e| format!("read se: {e}"))?;

    let transport = hs
        .into_transport_mode()
        .map_err(|e: snow::Error| e.to_string())?;
    Ok(NoiseSession { transport })
}

impl NoiseSession {
    pub fn encrypt(&mut self, plaintext: &[u8]) -> Result<Vec<u8>, String> {
        let mut buf = vec![0u8; plaintext.len() + 16];
        let n = self
            .transport
            .write_message(plaintext, &mut buf)
            .map_err(|e| e.to_string())?;
        Ok(buf[..n].to_vec())
    }

    pub fn decrypt(&mut self, ciphertext: &[u8]) -> Result<Vec<u8>, String> {
        let mut buf = vec![0u8; ciphertext.len()];
        let n = self
            .transport
            .read_message(ciphertext, &mut buf)
            .map_err(|e| e.to_string())?;
        Ok(buf[..n].to_vec())
    }
}

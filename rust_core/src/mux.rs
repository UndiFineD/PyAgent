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
use std::collections::HashMap;

/// Result of a demuxing operation.
#[derive(Debug, Clone)]
#[pyclass]
pub struct ModalityPacket {
    #[pyo3(get)]
    pub channel_id: String,
    #[pyo3(get)]
    pub modality_type: String,
    #[pyo3(get)]
    pub timestamp: f64,
    #[pyo3(get)]
    pub payload: Vec<u8>,
}

#[pymethods]
impl ModalityPacket {
    #[new]
    pub fn new(channel_id: String, modality_type: String, timestamp: f64, payload: Vec<u8>) -> Self {
        ModalityPacket {
            channel_id,
            modality_type,
            timestamp,
            payload,
        }
    }
}

/// Mux multiple modality channels into a single binary stream.
/// Format: [Header: 4 bytes][ChannelIDLen: 1 byte][ChannelID][TypeLen: 1 byte][Type][Timestamp: 8 bytes][PayloadLen: 4 bytes][Payload]
#[pyfunction]
pub fn mux_channels_rust(packets: Vec<ModalityPacket>) -> PyResult<Vec<u8>> {
    let mut buffer = Vec::new();
    for packet in packets {
        // Magic header: 0xDEADBEEF
        buffer.extend_from_slice(&[0xDE, 0xAD, 0xBE, 0xEF]);
        
        let cid_bytes = packet.channel_id.as_bytes();
        buffer.push(cid_bytes.len() as u8);
        buffer.extend_from_slice(cid_bytes);
        
        let type_bytes = packet.modality_type.as_bytes();
        buffer.push(type_bytes.len() as u8);
        buffer.extend_from_slice(type_bytes);
        
        buffer.extend_from_slice(&packet.timestamp.to_le_bytes());
        
        buffer.extend_from_slice(&(packet.payload.len() as u32).to_le_bytes());
        buffer.extend_from_slice(&packet.payload);
    }
    Ok(buffer)
}

/// Demux a binary stream back into modality packets.
#[pyfunction]
pub fn demux_channels_rust(data: Vec<u8>) -> PyResult<Vec<ModalityPacket>> {
    let mut packets = Vec::new();
    let mut i = 0;
    while i + 4 <= data.len() {
        if &data[i..i+4] == &[0xDE, 0xAD, 0xBE, 0xEF] {
            i += 4;
            
            if i >= data.len() { break; }
            let cid_len = data[i] as usize;
            i += 1;
            if i + cid_len > data.len() { break; }
            let channel_id = String::from_utf8_lossy(&data[i..i+cid_len]).to_string();
            i += cid_len;
            
            if i >= data.len() { break; }
            let type_len = data[i] as usize;
            i += 1;
            if i + type_len > data.len() { break; }
            let modality_type = String::from_utf8_lossy(&data[i..i+type_len]).to_string();
            i += type_len;
            
            if i + 8 > data.len() { break; }
            let mut ts_bytes = [0u8; 8];
            ts_bytes.copy_from_slice(&data[i..i+8]);
            let timestamp = f64::from_le_bytes(ts_bytes);
            i += 8;
            
            if i + 4 > data.len() { break; }
            let mut plen_bytes = [0u8; 4];
            plen_bytes.copy_from_slice(&data[i..i+4]);
            let payload_len = u32::from_le_bytes(plen_bytes) as usize;
            i += 4;
            
            if i + payload_len > data.len() { break; }
            let payload = data[i..i+payload_len].to_vec();
            i += payload_len;
            
            packets.push(ModalityPacket {
                channel_id,
                modality_type,
                timestamp,
                payload,
            });
        } else {
            i += 1;
        }
    }
    Ok(packets)
}

/// Synchronize multiple modality channels based on timestamps.
/// Groups packets arriving within a certain jitter window.
#[pyfunction]
pub fn synchronize_channels_rust(
    packets: Vec<ModalityPacket>,
    window_ms: f64,
) -> PyResult<HashMap<u64, Vec<ModalityPacket>>> {
    let mut grouped: HashMap<u64, Vec<ModalityPacket>> = HashMap::new();
    for packet in packets {
        let bucket = (packet.timestamp / (window_ms / 1000.0)).floor() as u64;
        grouped.entry(bucket).or_insert_with(Vec::new).push(packet);
    }
    Ok(grouped)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ModalityPacket>()?;
    m.add_function(wrap_pyfunction!(mux_channels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(demux_channels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(synchronize_channels_rust, m)?)?;
    Ok(())
}

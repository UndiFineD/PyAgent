#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, Any


class ProtocolIntelligence:
    """Intelligence engine for decoding and analyzing binary protocols."""

    @staticmethod
    def decode_protobuf(data: bytes) -> Dict[int, Any]:
        """
        Minimal pure-python protobuf decoder (best effort).
        Extracts field number and wire type.
        """
        results: Dict[int, Any] = {}
        index = 0
        while index < len(data):
            try:
                # Read varint for tag (field_number << 3 | wire_type)
                tag = 0
                shift = 0
                while True:
                    b = data[index]
                    tag |= (b & 0x7F) << shift
                    index += 1
                    if not (b & 0x80):
                        break
                    shift += 7

                field_number = tag >> 3
                wire_type = tag & 0x07

                if wire_type == 0:  # Varint
                    val = 0
                    shift = 0
                    while True:
                        b = data[index]
                        val |= (b & 0x7F) << shift
                        index += 1
                        if not (b & 0x80):
                            break
                        shift += 7
                    results[field_number] = val
                elif wire_type == 2:  # Length-delimited
                    length = 0
                    shift = 0
                    while True:
                        b = data[index]
                        length |= (b & 0x7F) << shift
                        index += 1
                        if not (b & 0x80):
                            break
                        shift += 7
                    results[field_number] = data[index : index + length]
                    index += length
                else:
                    # Skip other types for now (fixme: add wire type 1, 5)
                    break
            except Exception:
                break
        return results

    @staticmethod
    def identify_protocol(data: bytes) -> str:
        """Identify common binary protocols based on magic bytes."""
        if data.startswith(b"\x00\x00\x00\x0c"):
            return "GRPC/H2"
        if data.startswith(b"POST"):
            return "HTTP"
        if data.startswith(b"SSH-2.0"):
            return "SSH"
        if data.startswith(b"BEGIN RSA PRIVATE"):
            return "RSA KEY"
        return "Unknown"

    @staticmethod
    def get_tls_poisoning_info() -> Dict[str, Any]:
        """Details on TLS Poisoning techniques for SSRF/CSRF."""
        return {
            "concept": "Using TLS Session Resumption or Session IDs to smuggle data through security boundaries.",
            "target_protocols": ["SMTP", "IMAP", "Memcached"],
            "vulnerability_type": "SSRF / Protocol Smuggling",
            "mitigation": "Disable TLS Session Resumption or strictly validate SNI.",
        }

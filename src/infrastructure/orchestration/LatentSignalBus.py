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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import base64
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from datetime import datetime

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager

class LatentSignalBus:
    """
    Implements Telepathic Signal Compression (Phase 30).
    Facilitates high-bandwidth inter-agent communication using compressed 'latent vectors'
    (simulated as base64-encoded state payloads) instead of plain natural language.
    """
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.latent_space: Dict[str, Any] = {} # channel -> latent_vector

    def transmit_latent(self, channel: str, state_payload: Dict[str, Any]) -> str:
        """
        Compresses a complex state payload into a 'latent signal' and transmits it.
        """
        logging.info(f"LatentSignalBus: Encoding state for channel '{channel}'")
        
        # In a real implementation, this would use a VAE or Autoencoder to minify state.
        # Here we simulate with minified JSON + base64 encoding.
        raw_json = json.dumps(state_payload, separators=(',', ':'))
        latent_vector = base64.b64encode(raw_json.encode()).decode()
        
        self.latent_space[channel] = {
            "vector": latent_vector,
            "timestamp": datetime.now().isoformat(),
            "origin": "telepathic_compression_v1"
        }
        
        # Emit signal to notify listeners of latent update
        if hasattr(self.fleet, 'signals'):
            self.fleet.signals.emit("LATENT_SIGNAL_RECEIVED", {
                "channel": channel,
                "latent_checksum": hash(latent_vector)
            })
            
        return latent_vector

    def receive_latent(self, channel: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves and decompresses the latest latent signal from a channel.
        """
        if channel not in self.latent_space:
            return None
            
        latent_data = self.latent_space[channel]
        vector = latent_data["vector"]
        
        logging.info(f"LatentSignalBus: Decoding latent signal from channel '{channel}'")
        
        try:
            decoded_json = base64.b64decode(vector).decode()
            return json.loads(decoded_json)
        except Exception as e:
            logging.error(f"LatentSignalBus: Decompression failed: {e}")
            return None

    def list_active_channels(self) -> List[str]:
        return list(self.latent_space.keys())
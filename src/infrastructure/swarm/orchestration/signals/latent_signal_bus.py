#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

"""
Latent signal bus.py module.
"""


from __future__ import annotations

import base64
import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class LatentSignalBus:
    """
    Implements Telepathic Signal Compression (Phase 30).
    Facilitates high-bandwidth inter-agent communication using compressed 'latent vectors'
    (simulated as base64-encoded state payloads) instead of plain natural language.
    """

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.latent_space: dict[str, Any] = {}  # channel -> latent_vector

    def transmit_latent(self, channel: str, state_payload: dict[str, Any]) -> str:
        """
        Compresses a complex state payload into a 'latent signal' and transmits it.
        """
        logging.info(f"LatentSignalBus: Encoding state for channel '{channel}'")

        # In a real implementation, this would use a VAE or Autoencoder to minify state.
        # Here we simulate with minified JSON + base64 encoding.
        raw_json = json.dumps(state_payload, separators=(",", ":"))
        latent_vector = base64.b64encode(raw_json.encode()).decode()

        self.latent_space[channel] = {
            "vector": latent_vector,
            "timestamp": datetime.now().isoformat(),
            "origin": "telepathic_compression_v1",
        }

        # Emit signal to notify listeners of latent update
        if hasattr(self.fleet, "signals"):
            self.fleet.signals.emit(
                "LATENT_SIGNAL_RECEIVED",
                {"channel": channel, "latent_checksum": hash(latent_vector)},
            )

        return latent_vector

    def receive_latent(self, channel: str) -> dict[str, Any] | None:
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
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"LatentSignalBus: Decompression failed: {e}")
            return None

    def list_active_channels(self) -> list[str]:
        return list(self.latent_space.keys())

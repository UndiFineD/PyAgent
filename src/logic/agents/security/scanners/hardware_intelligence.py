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

from typing import Dict, List, Any


class HardwareIntelligence:
    """Intelligence module for RF, SDR, and Hardware exploitation (Ported from FISSURE)."""

    @staticmethod
    def get_rf_modulation_types() -> List[str]:
        """Common RF modulations targeted in signal discovery."""
        return ["OOK", "ASK", "FSK", "GFSK", "MSK", "GMSK", "BPSK", "QPSK", "QAM"]

    @staticmethod
    def get_rf_protocol_discovery_primitives() -> Dict[str, str]:
        """Techniques for identifying unknown RF protocols."""
        return {
            "preamble_discovery": (
                "Identifying repeating synchronization patterns at the start of burst transmissions"
            ),
            "packet_length_analysis": (
                "Statistical evaluation of transmission duration to determine payload boundaries"
            ),
            "bit_rate_estimation": (
                "Calculating the clock rate by analyzing the minimum duration of a single bit period"
            ),
            "symbol_mapping_recovery": (
                "Mapping physical signal states (frequency/phase shifts) to logical binary data"
            ),
            "crc_brute_force": (
                "Identifying cyclic redundancy check polynomials by testing common LFSR configurations"
            )
        }

    @staticmethod
    def get_rf_transceiver_configurations() -> Dict[str, Dict[str, Any]]:
        """Common RF transceiver settings (Ported from EvilCrow-RF)."""
        return {
            "cc1101": {
                "frequencies": [300.0, 315.0, 433.92, 868.0, 915.0],
                "modulations": ["2-FSK", "GFSK", "ASK", "OOK", "MSK"],
                "packet_handling": "Hardware-based preamble and sync word insertion"
            },
            "nrf24": {
                "frequency_range": "2.4GHz - 2.525GHz",
                "attack_modes": ["Mousejacking", "KeySniffing"]
            }
        }

    @staticmethod
    def get_rf_attack_patterns() -> Dict[str, str]:
        """Common hardware-level RF attacks (Integrated from Freeway)."""
        return {
            "replay_attack": "Capturing and re-transmitting legitimate signals (e.g., rolling codes with RollJam)",
            "jam_and_listen": "Signal jamming to prevent acknowledgement while capturing the next rolling code",
            "deauthentication_flood": "802.11 management frame spoofing to disconnect clients",
            "baseband_exploitation": "Sending malformed cellular frames to exploit vulnerabilities in modem firmware",
            "signal_injection": "Injecting packets into an established mesh network (e.g., Zigbee, Z-Wave)",
            "beacon_flood": "Flooding the vicinity with fake AP beacon frames to disrupt client scanning",
            "evil_twin_ap": "Hosting a rogue AP with identical SSID and BSSID to intercept client traffic",
            "packet_fuzzing_rf": "Sending malformed 802.11 frames to test driver robustness"
        }

    @staticmethod
    def get_hardware_bus_exploit_gadgets() -> Dict[str, str]:
        """Primitives for intercepting data on physical buses."""
        return {
            "uart_shell_access": "Identifying RX/TX pins to gain root console access via unauthenticated serial ports",
            "i2c_eeprom_dump": "Extracting firmware or secrets from serial memory chips",
            "spi_flash_cloning": "Physical extraction of flash memory for offline reverse engineering",
            "jtag_debugging": "Using Boundary Scan to halt CPU execution and read registers/memory",
            "swd_glitching": "Voltage or clock glitching to bypass read-out protection (RDP) on microcontrollers"
        }

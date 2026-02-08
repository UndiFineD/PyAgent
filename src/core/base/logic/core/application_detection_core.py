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

# Application Detection Core - Inspired by THC amap patterns
# Signature-based application identification using trigger packets and response matching

import asyncio
import socket
import ssl
import re
import binascii
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import warnings

from src.core.base.common.base_core import BaseCore


@dataclass
class ApplicationSignature:
    """Signature for application detection."""
    name: str
    triggers: List[str] = field(default_factory=list)
    protocol: str = "tcp"  # tcp, udp, or both
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    response_regex: str = ""
    compiled_regex: Optional[re.Pattern] = None
    harmful: bool = False

    def __post_init__(self):
        if self.response_regex:
            try:
                self.compiled_regex = re.compile(self.response_regex, re.DOTALL | re.MULTILINE)
            except re.error as e:
                warnings.warn(f"Invalid regex in signature {self.name}: {e}")


@dataclass
class DetectionResult:
    """Result of application detection."""
    host: str
    port: int
    protocol: str
    detected_apps: List[str] = field(default_factory=list)
    raw_response: Optional[bytes] = None
    response_length: int = 0
    confidence_score: float = 0.0
    matched_signatures: List[str] = field(default_factory=list)


@dataclass
class DetectionConfig:
    """Configuration for application detection."""
    timeout: float = 5.0
    max_response_size: int = 4096
    skip_harmful: bool = False
    ssl_enabled: bool = True
    concurrent_scans: int = 10
    retry_attempts: int = 1


class ApplicationDetectionCore(BaseCore):
    """
    Application Detection Core implementing signature-based application identification.

    Inspired by THC amap, this core provides:
    - Trigger packet sending
    - Response signature matching
    - TCP/UDP protocol support
    - SSL/TLS detection
    - Harmful trigger filtering
    """

    def __init__(self, config: Optional[DetectionConfig] = None):
        super().__init__()
        self.config = config or DetectionConfig()

        # Default application signatures inspired by amap
        self.signatures = self._load_default_signatures()

    def _load_default_signatures(self) -> List[ApplicationSignature]:
        """Load default application signatures."""
        return [
            # HTTP signatures
            ApplicationSignature(
                name="http",
                triggers=["GET / HTTP/1.0\r\n\r\n"],
                protocol="tcp",
                response_regex=r"^HTTP/\d+\.\d+\s+\d+",
                harmful=False
            ),
            ApplicationSignature(
                name="https/ssl",
                protocol="tcp",
                response_regex=r"^\x16\x03[\x00-\x03]",  # SSL/TLS handshake
                harmful=False
            ),

            # FTP signatures
            ApplicationSignature(
                name="ftp",
                triggers=["USER anonymous\r\n"],
                protocol="tcp",
                response_regex=r"^220.*ftp",
                harmful=False
            ),

            # SSH signatures
            ApplicationSignature(
                name="ssh",
                protocol="tcp",
                response_regex=r"^SSH-\d+\.\d+",
                harmful=False
            ),

            # SMTP signatures
            ApplicationSignature(
                name="smtp",
                triggers=["EHLO test\r\n"],
                protocol="tcp",
                response_regex=r"^220.*smtp|^250",
                harmful=False
            ),

            # POP3 signatures
            ApplicationSignature(
                name="pop3",
                triggers=["USER test\r\n"],
                protocol="tcp",
                response_regex=r"^\+OK.*pop3",
                harmful=False
            ),

            # IMAP signatures
            ApplicationSignature(
                name="imap",
                triggers=["a001 LOGIN test test\r\n"],
                protocol="tcp",
                response_regex=r"^\* OK.*imap",
                harmful=False
            ),

            # Telnet signatures
            ApplicationSignature(
                name="telnet",
                protocol="tcp",
                response_regex=r"^\xff[\xfb-\xfe]",  # Telnet negotiation
                harmful=False
            ),

            # RDP signatures
            ApplicationSignature(
                name="rdp",
                protocol="tcp",
                response_regex=r"^\x03\x00\x00\x0b\x06\xd0\x00\x00\x124\x00",  # RDP cookie
                harmful=False
            ),

            # MySQL signatures
            ApplicationSignature(
                name="mysql",
                protocol="tcp",
                response_regex=r"^\x0a[\x00-\x05]\x00\x00\x00",  # MySQL greeting packet
                harmful=False
            ),

            # PostgreSQL signatures
            ApplicationSignature(
                name="postgresql",
                protocol="tcp",
                response_regex=r"^Npgsql|^\x00\x00\x00\x08\x04\xd2\x16\x2f",  # PostgreSQL protocol
                harmful=False
            ),

            # Redis signatures
            ApplicationSignature(
                name="redis",
                triggers=["PING\r\n"],
                protocol="tcp",
                response_regex=r"^\+PONG",
                harmful=False
            ),

            # Memcached signatures
            ApplicationSignature(
                name="memcached",
                triggers=["stats\r\n"],
                protocol="tcp",
                response_regex=r"^STAT ",
                harmful=False
            ),

            # MongoDB signatures
            ApplicationSignature(
                name="mongodb",
                protocol="tcp",
                response_regex=r"^\x41\x00\x00\x00",  # MongoDB response header
                harmful=False
            ),

            # Elasticsearch signatures
            ApplicationSignature(
                name="elasticsearch",
                triggers=["GET / HTTP/1.0\r\n\r\n"],
                protocol="tcp",
                response_regex=r'"cluster_name"',
                harmful=False
            ),

            # Docker API signatures
            ApplicationSignature(
                name="docker-api",
                triggers=["GET /_ping HTTP/1.0\r\n\r\n"],
                protocol="tcp",
                response_regex=r"^OK",
                harmful=False
            ),

            # Kubernetes API signatures
            ApplicationSignature(
                name="kubernetes-api",
                triggers=["GET /api HTTP/1.0\r\n\r\n"],
                protocol="tcp",
                response_regex=r'"kind"',
                harmful=False
            ),

            # SNMP signatures (UDP)
            ApplicationSignature(
                name="snmp",
                protocol="udp",
                response_regex=r"^\x30\x81",  # SNMP response
                harmful=False
            ),

            # NTP signatures (UDP)
            ApplicationSignature(
                name="ntp",
                protocol="udp",
                response_regex=r"^\x1c\x00\x00",  # NTP response
                harmful=False
            ),

            # DNS signatures (UDP)
            ApplicationSignature(
                name="dns",
                protocol="udp",
                response_regex=r"^\x81\x80",  # DNS response header
                harmful=False
            ),
        ]

    def add_signature(self, signature: ApplicationSignature) -> None:
        """Add a custom application signature."""
        self.signatures.append(signature)

    def remove_signature(self, name: str) -> bool:
        """Remove a signature by name."""
        for i, sig in enumerate(self.signatures):
            if sig.name == name:
                self.signatures.pop(i)
                return True
        return False

    async def detect_applications(self, targets: List[Tuple[str, int, str]]) -> List[DetectionResult]:
        """
        Detect applications on multiple targets.

        Args:
            targets: List of (host, port, protocol) tuples

        Returns:
            List of detection results
        """
        semaphore = asyncio.Semaphore(self.config.concurrent_scans)
        tasks = []

        for host, port, protocol in targets:
            task = self._detect_single_target(host, port, protocol, semaphore)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, DetectionResult):
                valid_results.append(result)
            elif isinstance(result, Exception):
                self.logger.debug(f"Detection error: {result}")

        return valid_results

    async def _detect_single_target(self, host: str, port: int, protocol: str,
                                  semaphore: asyncio.Semaphore) -> DetectionResult:
        """Detect applications on a single target."""
        result = DetectionResult(host=host, port=port, protocol=protocol)

        async with semaphore:
            # Get relevant signatures for this protocol
            relevant_sigs = [sig for sig in self.signatures
                           if sig.protocol in [protocol, "both"]]

            if self.config.skip_harmful:
                relevant_sigs = [sig for sig in relevant_sigs if not sig.harmful]

            # Try each signature
            for signature in relevant_sigs:
                try:
                    detection = await self._test_signature(host, port, protocol, signature)
                    if detection:
                        result.detected_apps.append(signature.name)
                        result.matched_signatures.append(signature.name)
                        result.raw_response = detection.get('response')
                        result.response_length = detection.get('length', 0)

                except Exception as e:
                    self.logger.debug(f"Error testing {signature.name} on {host}:{port}: {e}")

            # Calculate confidence score
            result.confidence_score = self._calculate_confidence(result)

        return result

    async def _test_signature(self, host: str, port: int, protocol: str,
                            signature: ApplicationSignature) -> Optional[Dict[str, Any]]:
        """Test a single signature against a target."""
        # Send triggers if any
        for trigger in signature.triggers:
            try:
                response = await self._send_trigger(host, port, protocol, trigger)
                if response and self._matches_signature(response, signature):
                    return {
                        'response': response,
                        'length': len(response),
                        'signature': signature.name
                    }
            except Exception as e:
                self.logger.debug(f"Trigger failed for {signature.name}: {e}")

        # If no triggers, just try to get a response
        if not signature.triggers:
            try:
                response = await self._get_response(host, port, protocol)
                if response and self._matches_signature(response, signature):
                    return {
                        'response': response,
                        'length': len(response),
                        'signature': signature.name
                    }
            except Exception as e:
                self.logger.debug(f"Response check failed for {signature.name}: {e}")

        return None

    async def _send_trigger(self, host: str, port: int, protocol: str, trigger: str) -> Optional[bytes]:
        """Send a trigger packet and get response."""
        try:
            if protocol.lower() == "tcp":
                return await self._send_tcp_trigger(host, port, trigger)
            elif protocol.lower() == "udp":
                return await self._send_udp_trigger(host, port, trigger)
            else:
                return None
        except Exception as e:
            self.logger.debug(f"Trigger send failed: {e}")
            return None

    async def _send_tcp_trigger(self, host: str, port: int, trigger: str) -> Optional[bytes]:
        """Send TCP trigger and get response."""
        try:
            # Try SSL first if enabled
            if self.config.ssl_enabled and port in [443, 8443, 9443]:
                try:
                    return await self._send_ssl_trigger(host, port, trigger)
                except Exception:
                    pass  # Fall back to plain TCP

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.config.timeout
            )

            # Send trigger
            if trigger.startswith("0x"):
                # Hex encoded trigger
                trigger_data = binascii.unhexlify(trigger[2:])
            else:
                trigger_data = trigger.encode('utf-8', errors='ignore')

            writer.write(trigger_data)
            await writer.drain()

            # Read response
            response = await asyncio.wait_for(
                reader.read(self.config.max_response_size),
                timeout=self.config.timeout
            )

            writer.close()
            await writer.wait_closed()

            return response if response else None

        except Exception:
            return None

    async def _send_ssl_trigger(self, host: str, port: int, trigger: str) -> Optional[bytes]:
        """Send SSL/TLS trigger and get response."""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=context),
                timeout=self.config.timeout
            )

            # Send trigger
            if trigger.startswith("0x"):
                trigger_data = binascii.unhexlify(trigger[2:])
            else:
                trigger_data = trigger.encode('utf-8', errors='ignore')

            writer.write(trigger_data)
            await writer.drain()

            # Read response
            response = await asyncio.wait_for(
                reader.read(self.config.max_response_size),
                timeout=self.config.timeout
            )

            writer.close()
            await writer.wait_closed()

            return response if response else None

        except Exception:
            return None

    async def _send_udp_trigger(self, host: str, port: int, trigger: str) -> Optional[bytes]:
        """Send UDP trigger and get response."""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.config.timeout)

            # Send trigger
            if trigger.startswith("0x"):
                trigger_data = binascii.unhexlify(trigger[2:])
            else:
                trigger_data = trigger.encode('utf-8', errors='ignore')

            sock.sendto(trigger_data, (host, port))

            # Receive response
            response, _ = sock.recvfrom(self.config.max_response_size)
            sock.close()

            return response if response else None

        except Exception:
            return None

    async def _get_response(self, host: str, port: int, protocol: str) -> Optional[bytes]:
        """Get response without sending a trigger (for protocols that respond immediately)."""
        try:
            if protocol.lower() == "tcp":
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port),
                    timeout=self.config.timeout
                )

                # Read initial response
                response = await asyncio.wait_for(
                    reader.read(self.config.max_response_size),
                    timeout=self.config.timeout
                )

                writer.close()
                await writer.wait_closed()

                return response if response else None

            elif protocol.lower() == "udp":
                # For UDP, we can't really "get response" without sending something
                # Send a minimal trigger
                return await self._send_udp_trigger(host, port, "")

        except Exception:
            return None

    def _matches_signature(self, response: bytes, signature: ApplicationSignature) -> bool:
        """Check if response matches signature."""
        if not signature.compiled_regex:
            return False

        # Check length constraints
        if signature.min_length is not None and len(response) < signature.min_length:
            return False
        if signature.max_length is not None and len(response) > signature.max_length:
            return False

        # Check regex match
        try:
            response_str = response.decode('utf-8', errors='ignore')
            return bool(signature.compiled_regex.search(response_str))
        except Exception:
            return False

    def _calculate_confidence(self, result: DetectionResult) -> float:
        """Calculate confidence score for detection result."""
        if not result.detected_apps:
            return 0.0

        # Base confidence on number of matches and response characteristics
        confidence = min(len(result.detected_apps) * 0.3, 0.6)

        # Bonus for response length (more data = more confidence)
        if result.response_length > 10:
            confidence += 0.2

        # Bonus for multiple signatures matching
        if len(result.matched_signatures) > 1:
            confidence += 0.2

        return min(confidence, 1.0)

    def get_detection_summary(self, results: List[DetectionResult]) -> Dict[str, Any]:
        """Generate summary of detection results."""
        total_targets = len(results)
        detected_targets = len([r for r in results if r.detected_apps])
        unique_apps = set()

        for result in results:
            unique_apps.update(result.detected_apps)

        app_counts = {}
        for result in results:
            for app in result.detected_apps:
                app_counts[app] = app_counts.get(app, 0) + 1

        return {
            'total_targets': total_targets,
            'detected_targets': detected_targets,
            'detection_rate': detected_targets / total_targets if total_targets > 0 else 0,
            'unique_applications': len(unique_apps),
            'application_counts': app_counts,
            'applications_found': sorted(unique_apps)
        }
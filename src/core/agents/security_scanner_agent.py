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


"""
Module: security_scanner_agent
Agent for comprehensive security scanning using patterns from aem-hacker.
Implements vulnerability scanning, payload generation, SSRF detection, and reconnaissance.
"""


from __future__ import annotations

from typing import Any, Dict, List

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.mixins.payload_generator_mixin import PayloadGeneratorMixin
from src.core.base.mixins.reconnaissance_mixin import ReconnaissanceMixin
from src.core.base.mixins.ssrf_detector_mixin import SSRFDetectorMixin
from src.core.base.mixins.vulnerability_scanner_mixin import VulnerabilityScannerMixin


class SecurityScannerAgent(
        BaseAgent,
        VulnerabilityScannerMixin,
        PayloadGeneratorMixin,
        SSRFDetectorMixin,
        ReconnaissanceMixin
    ):
    """Comprehensive security scanner agent inspired by aem-hacker patterns.

    Features:
    - Modular vulnerability scanning with extensible checks
    - Payload generation for various exploit types
    - SSRF detection using callback server pattern
    - Target reconnaissance and service fingerprinting
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        VulnerabilityScannerMixin.__init__(self, **kwargs)
        PayloadGeneratorMixin.__init__(self, **kwargs)
        SSRFDetectorMixin.__init__(self, **kwargs)
        ReconnaissanceMixin.__init__(self, **kwargs)


    async def comprehensive_security_scan(
        self,
        targets: List[str],
        my_host: str,
        detector_port: int = 8080,
        workers: int = 4,
    ) -> Dict[str, Any]:
        """Perform comprehensive security scan on targets.

        Args:
            targets: List of target URLs
            my_host: Host for SSRF callbacks
            detector_port: Port for SSRF detector
            workers: Number of parallel workers

        Returns:
            Scan results dictionary
        """
        results = {
            'reconnaissance': {},
            'vulnerabilities': {},
            'ssrf_findings': [],
            'summary': {}
        }

        # Start SSRF detector
        if not self.start_ssrf_detector(port=detector_port):
            self.logger.error("Failed to start SSRF detector")
            return results

        try:
            # Reconnaissance phase
            self.logger.info(f"Starting reconnaissance on {len(targets)} targets")
            recon_results = await self.discover_targets(targets, workers=workers)
            results['reconnaissance'] = recon_results
            # Fingerprint discovered services
            fingerprints = {}
            for url in recon_results.keys():
                fingerprint = await self.fingerprint_service(url)
                fingerprints[url] = fingerprint
            results['fingerprints'] = fingerprints
            # Vulnerability scanning phase
            self.logger.info("Starting vulnerability scanning")
            vuln_results = {}
            for target in targets:
                findings = await self.run_vulnerability_scan(
                    target, my_host, workers=workers
                )
                if findings:
                    vuln_results[target] = findings

            results['vulnerabilities'] = vuln_results
            # Check for SSRF triggers
            ssrf_data = self._ssrf_data.copy()
            results['ssrf_findings'] = ssrf_data
            # Generate summary
            results['summary'] = self._generate_scan_summary(results)
        finally:
            self.stop_ssrf_detector()

        return results


    def _generate_scan_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of scan results."""
        summary = {
            'targets_scanned': len(results.get('reconnaissance', {})),
            'endpoints_discovered': sum(len(endpoints) for endpoints in results.get('reconnaissance', {}).values()),
            'vulnerabilities_found': sum(len(findings) for findings in results.get('vulnerabilities', {}).values()),
            'ssrf_triggers': len(results.get('ssrf_findings', {})),
            'service_types': {}
        }

        # Count service types
        for fingerprint in results.get('fingerprints', {}).values():
            svc_type = fingerprint.get('service_type', 'unknown')
            summary['service_types'][svc_type] = summary['service_types'].get(svc_type, 0) + 1
        return summary


    async def generate_exploit_payload(self, exploit_type: str, **kwargs) -> str:
        """Generate exploit payload for specific vulnerability type.

        Args:
            exploit_type: Type of exploit ('ssrf_rce', 'xss', 'deserialization', 'groovy_rce')
            **kwargs: Additional parameters for payload generation

        Returns:
            Generated payload
        """
        if exploit_type == 'ssrf_rce':
            fake_aem = kwargs.get('fake_aem_host', 'localhost')
            return self.generate_ssrf_rce_payload(fake_aem)
        elif exploit_type == 'xss':
            payload_type = kwargs.get('payload_type', 'reflected')
            index = kwargs.get('index', 0)
            return self.generate_xss_payload(payload_type, index)
        elif exploit_type == 'deserialization':
            payload_type = kwargs.get('payload_type', 'java_object_array')
            return self.generate_deserialization_payload(payload_type).decode('latin-1')
        elif exploit_type == 'groovy_rce':
            command = kwargs.get('command', 'whoami')
            return self.generate_groovy_rce_payload(command)
        else:
            raise ValueError(f"Unknown exploit type: {exploit_type}")


    async def add_custom_vulnerability_check(self, name: str, check_func) -> None:
        """Add custom vulnerability check.

        Args:
            name: Check name
            check_func: Check function
        """
        self.register_vulnerability_check(name, check_func)

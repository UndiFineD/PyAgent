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
Nuclei-style Vulnerability Template Engine

Inspired by Nuclei templates from .external/0day-templates repository.
Implements YAML-based vulnerability detection templates with DSL matchers.
"""

import logging
import asyncio
import yaml
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests


@dataclass
class TemplateInfo:
    """Template metadata"""
    name: str
    author: str
    severity: str
    description: str
    reference: Optional[List[str]] = None
    tags: Optional[List[str]] = None


@dataclass
class TemplateRequest:
    """HTTP request specification"""
    method: str
    path: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None


@dataclass
class MatcherCondition:
    """Matcher condition specification"""
    type: str
    dsl: Optional[List[str]] = None
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    words: Optional[List[str]] = None
    regex: Optional[List[str]] = None


@dataclass
class TemplateHTTP:
    """HTTP template specification"""
    requests: List[TemplateRequest]
    matchers: List[MatcherCondition]
    matchers_condition: Optional[str] = None  # "and" or "or"


@dataclass
class NucleiTemplate:
    """Complete Nuclei template"""
    id: str
    info: TemplateInfo
    http: Optional[TemplateHTTP] = None


@dataclass
class ScanResult:
    """Result from template execution"""
    template_id: str
    url: str
    matched: bool
    info: TemplateInfo
    request_details: Dict[str, Any]
    response_details: Dict[str, Any]
    extracted_data: Optional[Dict[str, Any]] = None


class NucleiTemplateEngine:
    """
    Nuclei-style vulnerability detection engine.

    Based on patterns from .external/0day-templates repository.
    """

    def __init__(self):
        self.templates: Dict[str, NucleiTemplate] = {}
        self.logger = logging.getLogger(__name__)

    def load_template_from_yaml(self, yaml_content: str) -> Optional[NucleiTemplate]:
        """
        Load a template from YAML content.

        Args:
            yaml_content: YAML template content

        Returns:
            Parsed NucleiTemplate or None if parsing fails
        """
        try:
            data = yaml.safe_load(yaml_content)

            # Parse info section
            info_data = data.get('info', {})
            info = TemplateInfo(
                name=info_data.get('name', ''),
                author=info_data.get('author', ''),
                severity=info_data.get('severity', 'info'),
                description=info_data.get('description', ''),
                reference=info_data.get('reference', []),
                tags=info_data.get('tags', [])
            )

            # Parse HTTP section
            http_data = data.get('http')
            http = None
            if http_data:
                requests = []
                for req_data in http_data.get('requests', []):
                    request = TemplateRequest(
                        method=req_data.get('method', 'GET'),
                        path=req_data.get('path', '/'),
                        headers=req_data.get('headers', {}),
                        body=req_data.get('body')
                    )
                    requests.append(request)

                matchers = []
                for matcher_data in http_data.get('matchers', []):
                    matcher = MatcherCondition(
                        type=matcher_data.get('type', 'word'),
                        dsl=matcher_data.get('dsl'),
                        status_code=matcher_data.get('status_code'),
                        headers=matcher_data.get('headers'),
                        body=matcher_data.get('body'),
                        words=matcher_data.get('words'),
                        regex=matcher_data.get('regex')
                    )
                    matchers.append(matcher)

                http = TemplateHTTP(
                    requests=requests,
                    matchers=matchers,
                    matchers_condition=http_data.get('matchers-condition')
                )

            template = NucleiTemplate(
                id=data.get('id', ''),
                info=info,
                http=http
            )

            self.templates[template.id] = template
            return template

        except Exception as e:
            self.logger.error(f"Failed to parse template: {e}")
            return None

    def load_template_from_file(self, file_path: str) -> Optional[NucleiTemplate]:
        """
        Load a template from a YAML file.

        Args:
            file_path: Path to the YAML template file

        Returns:
            Parsed NucleiTemplate or None if loading fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.load_template_from_yaml(content)
        except Exception as e:
            self.logger.error(f"Failed to load template from {file_path}: {e}")
            return None

    async def scan_url_with_template(self, template: NucleiTemplate, base_url: str) -> Optional[ScanResult]:
        """
        Scan a URL with a specific template.

        Args:
            template: NucleiTemplate to execute
            base_url: Base URL to scan

        Returns:
            ScanResult if template matches, None otherwise
        """
        if not template.http:
            return None

        try:
            # Execute requests
            for request in template.http.requests:
                url = self._build_url(base_url, request.path)

                # Make HTTP request
                response = await self._make_http_request(
                    url=url,
                    method=request.method,
                    headers=request.headers,
                    body=request.body
                )

                if not response:
                    continue

                # Check matchers
                matched = self._check_matchers(template.http.matchers, response, template.http.matchers_condition)

                if matched:
                    return ScanResult(
                        template_id=template.id,
                        url=url,
                        matched=True,
                        info=template.info,
                        request_details={
                            'method': request.method,
                            'url': url,
                            'headers': request.headers,
                            'body': request.body
                        },
                        response_details={
                            'status_code': response.status_code,
                            'headers': dict(response.headers),
                            'content': response.text[:1000]  # Truncate for storage
                        }
                    )

        except Exception as e:
            self.logger.error(f"Template scan failed for {template.id}: {e}")

        return None

    async def scan_url_with_templates(self, base_url: str, template_ids: Optional[List[str]] = None) -> List[ScanResult]:
        """
        Scan a URL with multiple templates.

        Args:
            base_url: Base URL to scan
            template_ids: Specific template IDs to use (None for all)

        Returns:
            List of matching ScanResults
        """
        results = []
        templates_to_scan = []

        if template_ids:
            templates_to_scan = [self.templates.get(tid) for tid in template_ids if tid in self.templates]
        else:
            templates_to_scan = list(self.templates.values())

        for template in templates_to_scan:
            if template:
                result = await self.scan_url_with_template(template, base_url)
                if result:
                    results.append(result)

        return results

    def _build_url(self, base_url: str, path: str) -> str:
        """Build full URL from base URL and path."""
        base_url = base_url.rstrip('/')
        if path.startswith('/'):
            return f"{base_url}{path}"
        else:
            return f"{base_url}/{path}"

    async def _make_http_request(
        self,
        url: str,
        method: str = 'GET',
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        timeout: int = 10
    ) -> Optional[requests.Response]:
        """Make HTTP request with timeout."""
        try:
            loop = asyncio.get_event_loop()
            # Wrap synchronous requests.request in run_in_executor
            response = await loop.run_in_executor(
                None,
                lambda: requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=body,
                    timeout=timeout,
                    allow_redirects=False
                )
            )
            return response
        except Exception as e:
            self.logger.error(f"HTTP request failed: {e}")
            return None

    def _check_matchers(self, matchers: List[MatcherCondition],
                       response: requests.Response,
                       condition: Optional[str] = None) -> bool:
        """
        Check if response matches the template matchers.

        Args:
            matchers: List of matcher conditions
            response: HTTP response to check
            condition: "and" or "or" condition (default: "or")

        Returns:
            True if matchers are satisfied
        """
        if not matchers:
            return True

        condition = condition or "or"
        results = []

        for matcher in matchers:
            result = self._check_single_matcher(matcher, response)
            results.append(result)

        if condition.lower() == "and":
            return all(results)
        else:  # "or"
            return any(results)

    def _check_single_matcher(self, matcher: MatcherCondition, response: requests.Response) -> bool:
        """Check a single matcher condition."""
        try:
            if matcher.type == "dsl":
                return self._check_dsl_matcher(matcher.dsl or [], response)
            elif matcher.type == "status":
                return response.status_code == matcher.status_code
            elif matcher.type == "word":
                return self._check_word_matcher(matcher.words or [], response.text)
            elif matcher.type == "regex":
                return self._check_regex_matcher(matcher.regex or [], response.text)
            else:
                self.logger.warning(f"Unknown matcher type: {matcher.type}")
                return False
        except Exception as e:
            self.logger.error(f"Matcher check failed: {e}")
            return False

    def _check_dsl_matcher(self, dsl_expressions: List[str], response: requests.Response) -> bool:
        """Check DSL (Domain Specific Language) expressions."""
        # Simplified DSL evaluation - in real Nuclei, this is more complex
        for expr in dsl_expressions:
            if "status_code" in expr and "==" in expr:
                # Simple status code check
                parts = expr.split("==")
                if len(parts) == 2:
                    expected_code = int(parts[1].strip())
                    if response.status_code != expected_code:
                        return False
            elif "duration" in expr and ">=" in expr:
                # Duration check (simplified - would need timing)
                pass
            elif "contains" in expr:
                # Content check
                if "body" in expr and not any(word in response.text for word in ["error", "not found"]):
                    return False

        return True

    def _check_word_matcher(self, words: List[str], content: str) -> bool:
        """Check if any of the words are present in content."""
        content_lower = content.lower()
        return any(word.lower() in content_lower for word in words)

    def _check_regex_matcher(self, patterns: List[str], content: str) -> bool:
        """Check if any regex pattern matches the content."""
        for pattern in patterns:
            try:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            except re.error:
                continue
        return False

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available templates with metadata."""
        return [{
            'id': template.id,
            'name': template.info.name,
            'author': template.info.author,
            'severity': template.info.severity,
            'description': template.info.description,
            'tags': template.info.tags or []
        } for template in self.templates.values()]


# Example usage and test template
SQL_INJECTION_TEMPLATE = """
id: CVE-2024-2879

info:
  name: CVE-2024-2879 - WordPress LayerSlider Plugin - SQL Injection
  author: Stux
  severity: critical
  description: |
    The LayerSlider plugin for WordPress is vulnerable to SQL Injection via the ls_get_popup_markup action in versions 7.9.11 and 7.10.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.
  reference:
    - https://nvd.nist.gov/vuln/detail/CVE-2024-2879
  tags: sqli,wp

http:
  - method: GET
    path:
      - "{{BaseURL}}/wp-admin/admin-ajax.php?action=ls_get_popup_markup&id[where]=1)and (SELECT 6416 FROM (SELECT(SLEEP(6)))nEiK)-- vqlq"

    matchers:
      - type: dsl
        dsl:
          - 'duration>=6'
          - 'status_code == 200'
        condition: and
"""

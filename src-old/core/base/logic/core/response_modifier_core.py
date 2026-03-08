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

# Response Modifier Core - HTTP Response Code Manipulation
# Based on patterns from 200-OK-Modifier Burp extension

import asyncio
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from urllib.parse import urlparse

from src.core.base.logic.core.base_core import BaseCore


@dataclass
class ResponseModificationRule:
    """Rule for modifying HTTP responses"""
    name: str
    condition: str  # Regex pattern for URL or response content
    target_status: int  # Target status code to set
    preserve_original: bool = True  # Include original code in headers
    enabled: bool = True


@dataclass
class ModifiedResponse:
    """Container for modified response data"""
    original_status: int
    modified_status: int
    headers: List[str]
    body: bytes
    rule_applied: str
    timestamp: float


class ResponseModifierCore(BaseCore):
    """
    HTTP Response Modifier Core for security testing and analysis.
    
    Provides capabilities to modify HTTP response codes and content
    for testing purposes, similar to Burp Suite extensions.
    Useful for bypassing client-side validations and testing error handling.
    """

    def __init__(self):
        super().__init__()
        self.modification_rules: List[ResponseModificationRule] = []
        self.modification_history: List[ModifiedResponse] = []
        self.enabled = False

    async def initialize(self) -> bool:
        """Initialize the response modifier core"""
        try:
            # Add default rules for common testing scenarios
            await self.add_default_rules()
            self.logger.info("Response Modifier Core initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Response Modifier Core: {e}")
            return False

    async def add_default_rules(self) -> None:
        """Add default modification rules for common scenarios"""
        default_rules = [
            ResponseModificationRule(
                name="Force 200 OK",
                condition=r".*",  # Match all URLs
                target_status=200,
                preserve_original=True
            ),
            ResponseModificationRule(
                name="Force 403 Forbidden",
                condition=r".*",  # Match all URLs
                target_status=403,
                preserve_original=True
            ),
            ResponseModificationRule(
                name="Force 500 Error",
                condition=r".*",  # Match all URLs
                target_status=500,
                preserve_original=True
            ),
            ResponseModificationRule(
                name="Bypass Auth Errors",
                condition=r"/admin/|/api/auth/",
                target_status=200,
                preserve_original=True
            )
        ]

        for rule in default_rules:
            await self.add_modification_rule(rule)

    async def add_modification_rule(self, rule: ResponseModificationRule) -> None:
        """Add a new response modification rule"""
        self.modification_rules.append(rule)
        self.logger.info(f"Added modification rule: {rule.name}")

    async def remove_modification_rule(self, rule_name: str) -> bool:
        """Remove a modification rule by name"""
        for i, rule in enumerate(self.modification_rules):
            if rule.name == rule_name:
                del self.modification_rules[i]
                self.logger.info(f"Removed modification rule: {rule_name}")
                return True
        return False

    async def enable_modifications(self) -> None:
        """Enable response modifications"""
        self.enabled = True
        self.logger.info("Response modifications enabled")

    async def disable_modifications(self) -> None:
        """Disable response modifications"""
        self.enabled = False
        self.logger.info("Response modifications disabled")

    async def modify_response(
        self,
        url: str,
        status_code: int,
        headers: List[str],
        body: bytes
    ) -> Tuple[int, List[str], bytes]:
        """
        Modify an HTTP response based on active rules
        
        Args:
            url: Request URL
            status_code: Original status code
            headers: Response headers
            body: Response body
            
        Returns:
            Tuple of (modified_status, modified_headers, modified_body)
        """
        if not self.enabled:
            return status_code, headers, body

        for rule in self.modification_rules:
            if not rule.enabled:
                continue

            # Check if rule condition matches URL
            if re.search(rule.condition, url, re.IGNORECASE):
                modified_status = rule.target_status
                modified_headers = headers.copy()
                modified_body = body

                # Preserve original status code in headers if requested
                if rule.preserve_original:
                    # Find status line and modify it
                    if modified_headers:
                        status_line = modified_headers[0]
                        # Replace status code while preserving HTTP version
                        status_pattern = r'HTTP/\d\.\d\s+\d+'
                        replacement = f'HTTP/1.1 {modified_status} OK OriginalCodeWas: {status_code}'
                        modified_headers[0] = re.sub(status_pattern, replacement, status_line)

                # Record modification in history
                modified_response = ModifiedResponse(
                    original_status=status_code,
                    modified_status=modified_status,
                    headers=modified_headers,
                    body=modified_body,
                    rule_applied=rule.name,
                    timestamp=asyncio.get_event_loop().time()
                )
                self.modification_history.append(modified_response)

                self.logger.debug(f"Applied rule '{rule.name}' to {url}: {status_code} -> {modified_status}")
                return modified_status, modified_headers, modified_body

        # No rules matched, return original response
        return status_code, headers, body

    async def get_modification_history(
        self,
        limit: int = 100,
        rule_filter: Optional[str] = None
    ) -> List[ModifiedResponse]:
        """
        Get modification history
        
        Args:
            limit: Maximum number of entries to return
            rule_filter: Filter by rule name (optional)
            
        Returns:
            List of modified responses
        """
        history = self.modification_history

        if rule_filter:
            history = [h for h in history if h.rule_applied == rule_filter]

        return history[-limit:] if limit > 0 else history

    async def clear_history(self) -> None:
        """Clear modification history"""
        self.modification_history.clear()
        self.logger.info("Modification history cleared")

    async def get_active_rules(self) -> List[ResponseModificationRule]:
        """Get list of active modification rules"""
        return [rule for rule in self.modification_rules if rule.enabled]

    async def export_rules(self) -> Dict[str, Any]:
        """Export modification rules to dictionary"""
        return {
            "rules": [
                {
                    "name": rule.name,
                    "condition": rule.condition,
                    "target_status": rule.target_status,
                    "preserve_original": rule.preserve_original,
                    "enabled": rule.enabled
                }
                for rule in self.modification_rules
            ],
            "enabled": self.enabled
        }

    async def import_rules(self, rules_data: Dict[str, Any]) -> None:
        """Import modification rules from dictionary"""
        self.modification_rules.clear()
        
        for rule_data in rules_data.get("rules", []):
            rule = ResponseModificationRule(
                name=rule_data["name"],
                condition=rule_data["condition"],
                target_status=rule_data["target_status"],
                preserve_original=rule_data.get("preserve_original", True),
                enabled=rule_data.get("enabled", True)
            )
            self.modification_rules.append(rule)
        
        self.enabled = rules_data.get("enabled", False)
        self.logger.info(f"Imported {len(self.modification_rules)} modification rules")

    async def analyze_response_patterns(
        self,
        responses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze response patterns for testing insights
        
        Args:
            responses: List of response data dictionaries
            
        Returns:
            Analysis results
        """
        analysis = {
            "total_responses": len(responses),
            "status_distribution": {},
            "modification_suggestions": [],
            "vulnerability_indicators": []
        }

        for response in responses:
            status = response.get("status_code", 0)
            analysis["status_distribution"][status] = analysis["status_distribution"].get(status, 0) + 1

            # Check for common vulnerability patterns
            if status == 403:
                analysis["vulnerability_indicators"].append("Potential authorization bypass opportunity")
            elif status == 500:
                analysis["vulnerability_indicators"].append("Server error - potential injection point")
            elif status == 401:
                analysis["modification_suggestions"].append("Consider forcing 200 OK to bypass auth")

        return analysis

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.modification_rules.clear()
        self.modification_history.clear()
        self.logger.info("Response Modifier Core cleaned up")
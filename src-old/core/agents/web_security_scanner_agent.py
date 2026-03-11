#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/agents/web_security_scanner_agent.description.md

# web_security_scanner_agent

**File**: `src\\core\agents\\web_security_scanner_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 141  
**Complexity**: 1 (simple)

## Overview

Module: web_security_scanner_agent
Agent for web application security scanning, refactored from aem-eye patterns.
Implements multi-agent coordination for distributed scanning tasks.

## Classes (1)

### `WebSecurityScannerAgent`

**Inherits from**: BaseAgent, SecurityMixin, DataProcessingMixin, TaskQueueMixin

Agent for web security scanning using patterns from aem-eye.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.logic.security.web_security_scanner_core.WebSecurityScannerCore`
- `src.core.base.mixins.data_processing_mixin.DataProcessingMixin`
- `src.core.base.mixins.security_mixin.SecurityMixin`
- `src.core.base.mixins.task_queue_mixin.TaskQueueMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid.UUID`

---
*Auto-generated documentation*
## Source: src-old/core/agents/web_security_scanner_agent.improvements.md

# Improvements for web_security_scanner_agent

**File**: `src\\core\agents\\web_security_scanner_agent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 141 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `web_security_scanner_agent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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
Module: web_security_scanner_agent
Agent for web application security scanning, refactored from aem-eye patterns.
Implements multi-agent coordination for distributed scanning tasks.
"""


from typing import Any, Dict, List, Optional

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.logic.security.web_security_scanner_core import (
    WebSecurityScannerCore,
)
from src.core.base.mixins.data_processing_mixin import DataProcessingMixin
from src.core.base.mixins.security_mixin import SecurityMixin
from src.core.base.mixins.task_queue_mixin import TaskQueueMixin


class WebSecurityScannerAgent(
    BaseAgent, SecurityMixin, DataProcessingMixin, TaskQueueMixin
):
    """Agent for web security scanning using patterns from aem-eye."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        SecurityMixin.__init__(self, **kwargs)
        TaskQueueMixin.__init__(self, **kwargs)

        self.scanner_core = WebSecurityScannerCore(
            timeout=kwargs.get("timeout", 10),
            concurrency=kwargs.get("concurrency", 10),
            rate_limit=kwargs.get("rate_limit", 100),
        )

    async def scan_for_vulnerabilities(
        self, hosts: List[str], custom_patterns: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Scan hosts for security vulnerabilities using pattern matching.

        Args:
            hosts: List of hosts/URLs to scan
            custom_patterns: Optional custom regex patterns to check

        Returns:
            Scan results with detected patterns

        """
        # Use default CMS patterns if none provided
        if custom_patterns is None:
            custom_patterns = {
                "aem": r'href="/content/dam|/etc/clientlibs',
                "wordpress": r"wp-content|wp-includes",
                "drupal": r"Drupal|drupal",
                "joomla": r"Joomla|joomla",
            }

        # Distribute scanning across multiple worker tasks
        results = await self._coordinate_scanning(hosts, custom_patterns)

        # Process and analyze results
        analysis = await self._analyze_scan_results(results)

        return {
            "scan_results": results,
            "analysis": analysis,
            "total_hosts_scanned": len(hosts),
            "vulnerable_hosts": len(results),
        }

    async def _coordinate_scanning(
        self, hosts: List[str], patterns: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """Coordinate scanning using task queue pattern similar to aem-eye's job system."""
        # Split hosts into batches for distributed processing
        batch_size = 50
        all_results = {}

        for i in range(0, len(hosts), batch_size):
            batch = hosts[i : i + batch_size]

            # Create scanning task
            task_id = await self.create_task(
                {"type": "scan_batch", "hosts": batch, "patterns": patterns}
            )

            # Execute batch scan
            batch_results = await self.scanner_core.scan_hosts(batch, patterns)
            all_results.update(batch_results)

            # Mark task complete
            await self.complete_task(task_id)

        return all_results

    async def _analyze_scan_results(
        self, results: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Analyze scan results for security insights."""
        pattern_counts = {}
        host_counts = {}

        for host, patterns in results.items():
            for pattern in patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
                if pattern not in host_counts:
                    host_counts[pattern] = []
                host_counts[pattern].append(host)

        return {
            "pattern_distribution": pattern_counts,
            "hosts_by_pattern": host_counts,
            "total_matches": sum(pattern_counts.values()),
        }

    async def detect_cms_instances(self, hosts: List[str]) -> Dict[str, Any]:
        """Detect CMS instances across hosts.

        Args:
            hosts: List of hosts to scan

        Returns:
            CMS detection results

        """
        results = await self.scanner_core.detect_cms_fingerprints(hosts)
        analysis = await self._analyze_scan_results(results)

        return {"cms_detections": results, "analysis": analysis}

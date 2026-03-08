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
LLM_CONTEXT_START

## Source: src-old/core/base/mixins/reconnaissance_mixin.description.md

# reconnaissance_mixin

**File**: `src\core\base\mixins\reconnaissance_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 248  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for reconnaissance_mixin.

## Classes (1)

### `ReconnaissanceMixin`

Mixin providing reconnaissance capabilities for target discovery.

Inspired by aem_discoverer.py patterns for identifying vulnerable services.

**Methods** (6):
- `__init__(self)`
- `_load_default_patterns(self)`
- `_discover_single_target(self, base_url, patterns, timeout, proxy)`
- `_is_interesting_response(self, response)`
- `add_discovery_pattern(self, category, patterns)`
- `get_discovery_patterns(self, category)`

## Dependencies

**Imports** (10):
- `asyncio`
- `concurrent.futures`
- `re`
- `requests`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urljoin`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/reconnaissance_mixin.improvements.md

# Improvements for reconnaissance_mixin

**File**: `src\core\base\mixins\reconnaissance_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 248 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `reconnaissance_mixin_test.py` with pytest tests

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

import asyncio
import concurrent.futures
from typing import List, Dict, Optional, Set
import requests
from urllib.parse import urljoin, urlparse
import re


class ReconnaissanceMixin:
    """
    Mixin providing reconnaissance capabilities for target discovery.

    Inspired by aem_discoverer.py patterns for identifying vulnerable services.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._discovery_patterns: Dict[str, List[str]] = {}
        self._load_default_patterns()

    def _load_default_patterns(self) -> None:
        """Load default discovery patterns."""
        # AEM-specific paths (inspired by aem_discoverer.py)
        self._discovery_patterns["aem"] = [
            "/content/dam.json",
            "/content/geometrixx/en.html",
            "/content/geometrixx/_jcr_content.json",
            "/content/we-retail/en.html",
            "/content/we-retail/_jcr_content.json",
            "/system/console/bundles.json",
            "/libs/granite/core/content/login.html",
            "/crx/de/index.jsp",
            "/crx/explorer/browser/index.jsp",
            "/bin/cpm/package.json",
            "/etc/packages.json",
        ]

        # Common CMS/framework fingerprints
        self._discovery_patterns["cms"] = [
            "/wp-admin/",
            "/administrator/",
            "/umbraco/",
            "/sitecore/",
            "/aem/",
            "/content/",
            "/bin/",
            "/libs/",
            "/etc/",
            "/apps/",
            "/crx/",
        ]

        # Exposed admin interfaces
        self._discovery_patterns["admin"] = [
            "/admin/",
            "/administrator/",
            "/admin.php",
            "/admin.jsp",
            "/system/console/",
            "/crx/de/",
            "/crx/explorer/",
            "/felix/console/",
        ]

        # API endpoints
        self._discovery_patterns["api"] = [
            "/api/",
            "/rest/",
            "/graphql",
            "/bin/querybuilder.json",
            "/libs/cq/search/content.query.json",
        ]

    async def discover_targets(
        self,
        urls: List[str],
        patterns: Optional[List[str]] = None,
        workers: int = 10,
        timeout: int = 5,
        proxy: Optional[Dict] = None,
    ) -> Dict[str, List[str]]:
        """
        Discover potential targets from a list of URLs.

        Args:
            urls: List of base URLs to check
            patterns: Custom patterns to check (optional)
            workers: Number of parallel workers
            timeout: Request timeout
            proxy: Proxy configuration

        Returns:
            Dict mapping URLs to list of discovered endpoints
        """
        if patterns is None:
            patterns = []
            for pattern_list in self._discovery_patterns.values():
                patterns.extend(pattern_list)

        results = {}

        # Run discovery in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            for url in urls:
                future = executor.submit(
                    self._discover_single_target, url, patterns, timeout, proxy
                )
                futures.append((url, future))

            for url, future in futures:
                try:
                    discovered = future.result(timeout=30)
                    if discovered:
                        results[url] = discovered
                except concurrent.futures.TimeoutError:
                    continue
                except Exception:
                    continue

        return results

    def _discover_single_target(
        self, base_url: str, patterns: List[str], timeout: int, proxy: Optional[Dict]
    ) -> List[str]:
        """Discover endpoints for a single target."""
        discovered = []
        proxies = proxy if proxy else {}

        for pattern in patterns:
            try:
                url = urljoin(base_url.rstrip("/") + "/", pattern.lstrip("/"))
                response = requests.get(
                    url, timeout=timeout, proxies=proxies, verify=False
                )

                if self._is_interesting_response(response):
                    discovered.append(url)

            except requests.RequestException:
                continue

        return discovered

    def _is_interesting_response(self, response: requests.Response) -> bool:
        """Check if response indicates an interesting discovery."""
        # Status codes that indicate something exists
        if response.status_code in [200, 301, 302, 401, 403]:
            # Check for AEM-specific content
            content = response.text.lower()
            aem_indicators = [
                "aem",
                "adobe experience manager",
                "cq",
                "crx",
                "granite",
                "sling",
                "felix",
                "jackrabbit",
                "day software",
            ]

            if any(indicator in content for indicator in aem_indicators):
                return True

            # Check for JSON responses (APIs)
            if response.headers.get("content-type", "").startswith("application/json"):
                return True

            # Check for HTML with admin indicators
            if "admin" in content or "console" in content or "login" in content:
                return True

        return False

    async def fingerprint_service(
        self, url: str, proxy: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Fingerprint a service to identify its type.

        Args:
            url: URL to fingerprint

        Returns:
            Dict with fingerprint information
        """
        fingerprint = {
            "url": url,
            "service_type": "unknown",
            "version": "unknown",
            "features": [],
        }

        try:
            proxies = proxy if proxy else {}
            response = requests.get(url, timeout=10, proxies=proxies, verify=False)

            content = response.text

            # AEM detection
            if "adobe experience manager" in content.lower():
                fingerprint["service_type"] = "aem"
                version_match = re.search(
                    r"Adobe Experience Manager (\d+\.\d+)", content, re.I
                )
                if version_match:
                    fingerprint["version"] = version_match.group(1)

            # Felix console
            if "apache felix" in content.lower() or "felix console" in content.lower():
                fingerprint["service_type"] = "felix"
                fingerprint["features"].append("osgi_console")

            # CRX
            if "crx" in content.lower() and "repository" in content.lower():
                fingerprint["features"].append("crx_repository")

            # Generic CMS detection
            if "/wp-admin/" in content or "wordpress" in content.lower():
                fingerprint["service_type"] = "wordpress"
            elif "drupal" in content.lower():
                fingerprint["service_type"] = "drupal"
            elif "joomla" in content.lower():
                fingerprint["service_type"] = "joomla"

        except Exception:
            pass

        return fingerprint

    def add_discovery_pattern(self, category: str, patterns: List[str]) -> None:
        """
        Add custom discovery patterns.

        Args:
            category: Category name
            patterns: List of URL patterns
        """
        if category in self._discovery_patterns:
            self._discovery_patterns[category].extend(patterns)
        else:
            self._discovery_patterns[category] = patterns

    def get_discovery_patterns(
        self, category: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Get discovery patterns.

        Args:
            category: Specific category or None for all

        Returns:
            Patterns dictionary
        """
        if category:
            return {category: self._discovery_patterns.get(category, [])}
        return self._discovery_patterns.copy()

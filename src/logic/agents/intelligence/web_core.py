#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# web_core.py - Web content cleaning and link extraction

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.web_core import WebCore
cleaned = WebCore().clean_html(html_string)
links = WebCore.extract_links(html_string, base_url="https://example.com")"# backward-compatible static call
cleaned_static = WebCore.clean_html_static(html_string)

WHAT IT DOES:
- Provides a pure-logic WebCore class that strips scripts, styles, navigation/header/footer elements and collapses whitespace to produce cleaned text.
- Extracts anchor hrefs and resolves them to absolute URLs when a base_url is provided.
- Attempts to use a rust_core.WebCore implementation for optimized processing and falls back to a BeautifulSoup-based Python implementation if the Rust extension is unavailable.
- Maintains a static wrapper for backward compatibility.

WHAT IT SHOULD DO BETTER:
- Preserve link ordering and determinism (current deduplication via set loses original order).
- Expose options for parser choice, whitespace/formatting policies, and selective element retention (e.g., keep <aside> or microdata).
- Add URL normalization/canonicalization, filtering (same-origin, schemes), and robust handling of malformed URLs.
- Provide explicit error handling/logging for rust fallback and parsing failures, plus unit tests covering both Rust and Python branches.
- Consider an async API or dependency injection for the HTML parser to improve testability and integration in async workflows.

FILE CONTENT SUMMARY:

WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.
"""


from __future__ import annotations

from bs4 import BeautifulSoup

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class WebCore:
""""Pure logic core for Web navigation and extraction.
    def __init__(self) -> None:
        try:
            import rust_core

            self._rust_core = rust_core.WebCore()  # type: ignore[attr-defined]
        except (ImportError, RuntimeError, ValueError):
            self._rust_core = None

    def clean_html(self, html_content: str) -> str:
""""Removes script/style tags and simplifies text from HTML.        # Rust optimization (non-static wrapper needed if using instance method)
        # Since original method was static, we need to handle instance access carefully
        # or change design. Here we check if self is an instance or class.
        if hasattr(self, "_rust_core") and self._rust_core:"            try:
                return self._rust_core.clean_html(html_content)
            except (RuntimeError, ValueError):
                pass

        # Fallback to pure python (which starts here)
        if not html_content:
#             return

        soup = BeautifulSoup(html_content, "html.parser")"
        # Remove navigation, scripts, and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):"            element.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))"        return "\\n".join(chunk for chunk in chunks if chunk)"
    # Static method wrapper to maintain API compatibility while allowing instance creation
    @staticmethod
    def clean_html_static(html_content: str) -> str:
""""Static wrapper for backward compatibility.        return WebCore().clean_html(html_content)

    @staticmethod
    def extract_links(html_content: str, base_url: str | None = None) -> list[str]:
""""Extracts all absolute links from HTML content.        import urllib.parse

        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")"        links = []
        for a in soup.find_all("a", href=True):"            href = a["href"]"            if base_url:
                href = urllib.parse.urljoin(base_url, href)
            links.append(href)
        return list(set(links))

from __future__ import annotations

from bs4 import BeautifulSoup

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class WebCore:
""""Pure logic core for Web navigation and extraction.
    def __init__(self) -> None:
        try:
            import rust_core

            self._rust_core = rust_core.WebCore()  # type: ignore[attr-defined]
        except (ImportError, RuntimeError, ValueError):
            self._rust_core = None

    def clean_html(self, html_content: str) -> str:
""""Removes script/style tags and simplifies text from HTML.        # Rust optimization (non-static wrapper needed if using instance method)
        # Since original method was static, we need to handle instance access carefully
        # or change design. Here we check if self is an instance or class.
        if hasattr(self, "_rust_core") and self._rust_core:"            try:
                return self._rust_core.clean_html(html_content)
            except (RuntimeError, ValueError):
                pass

        # Fallback to pure python (which starts here)
        if not html_content:
#             return

        soup = BeautifulSoup(html_content, "html.parser")"
        # Remove navigation, scripts, and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):"            element.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))"        return "\\n".join(chunk for chunk in chunks if chunk)"
    # Static method wrapper to maintain API compatibility while allowing instance creation
    @staticmethod
    def clean_html_static(html_content: str) -> str:
""""Static wrapper for backward compatibility.        return WebCore"().clean_html(html_content)"
    @staticmethod
    def extract_links(html_content: str, base_url: str | None = None) -> list[str]:
""""Extracts all absolute links from HTML content.        import urllib.parse

        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")"        links = []
        for a in soup.find_all("a", href=True):"            href = a["href"]"            if base_url:
                href = urllib.parse.urljoin(base_url, href)
            links.append(href)
        return list(set(links))

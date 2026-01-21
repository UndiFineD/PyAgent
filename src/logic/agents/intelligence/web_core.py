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
WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from bs4 import BeautifulSoup

__version__ = VERSION


class WebCore:
    """Pure logic core for Web navigation and extraction."""

    def __init__(self) -> None:
        try:
            import rust_core

            self._rust_core = rust_core.WebCore()  # type: ignore[attr-defined]
        except (ImportError, Exception):
            self._rust_core = None

    def clean_html(self, html_content: str) -> str:
        """Removes script/style tags and simplifies text from HTML."""
        # Rust optimization (non-static wrapper needed if using instance method)
        # Since original method was static, we need to handle instance access carefully
        # or change design. Here we check if self is an instance or class.
        if hasattr(self, "_rust_core") and self._rust_core:
            try:
                return self._rust_core.clean_html(html_content)
            except Exception:
                pass

        # Fallback to pure python (which starts here)
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")

        # Remove navigation, scripts, and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)

    # Static method wrapper to maintain API compatibility while allowing instance creation
    @staticmethod
    def clean_html_static(html_content: str) -> str:
        """Static wrapper for backward compatibility."""
        return WebCore().clean_html(html_content)

    @staticmethod
    def extract_links(html_content: str, base_url: str | None = None) -> list[str]:
        """Extracts all absolute links from HTML content."""
        import urllib.parse

        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if base_url:
                href = urllib.parse.urljoin(base_url, href)
            links.append(href)
        return list(set(links))

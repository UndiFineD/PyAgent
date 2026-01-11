#!/usr/bin/env python3

"""
WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.
"""

from src.core.base.version import VERSION
from bs4 import BeautifulSoup
from typing import List, Optional

__version__ = VERSION

class WebCore:
    """Pure logic core for Web navigation and extraction."""

    @staticmethod
    def clean_html(html_content: str) -> str:
        """Removes script/style tags and simplifies text from HTML."""
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove navigation, scripts, and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)

    @staticmethod
    def extract_links(html_content: str, base_url: Optional[str] = None) -> List[str]:
        """Extracts all absolute links from HTML content."""
        import urllib.parse
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url:
                href = urllib.parse.urljoin(base_url, href)
            links.append(href)
        return list(set(links))

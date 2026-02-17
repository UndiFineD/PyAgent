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


"""
Arxiv Core - ArXiv paper fetch, extract and summarize

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ArxivCore() and call search(query, max_results) to find papers.
- Use download_paper(pdf_url, filename) to fetch PDFs into data/research.
- Use extract_text(Path(...)) to get raw text from a downloaded PDF.
- Use summarize_results(results) to render a human-readable result block.

WHAT IT DOES:
- Provides a small core for interacting with the arxiv API: searching papers, downloading PDFs via a ReverseProxyFirewall, extracting text using PyMuPDF (fitz), and formatting brief summaries of search results.
- Creates and manages a download directory relative to the workspace root.
- Wraps network and I/O operations with basic error logging and returns safe defaults on failure.

WHAT IT SHOULD DO BETTER:
- Add retries, backoff, and configurable timeouts for network operations (firewall.get) and handle common HTTP errors explicitly.
- Validate and sanitize arXiv metadata (e.g., missing comments, truncated summaries), and support pagination/continuation for large result sets.
- Improve PDF text extraction robustness (handle encrypted, scanned/OCR PDFs, preserve page boundaries and metadata) and provide configurable text extraction options (layout-preserving, per-page output).
- Add unit tests and integration tests for search, download, and extract_text paths; add type narrowing and richer error types instead of broad exception catches.
- Make download_dir and arxiv.Client configurable via dependency injection for easier testing and runtime control; add logging context and observability (metrics, timings).

FILE CONTENT SUMMARY:
Arxiv core.py module.

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import arxiv
import fitz  # PyMuPDF

from src.infrastructure.security.network.firewall import ReverseProxyFirewall


class ArxivCore:
""""Core logic for interacting with Arxiv research papers.
    def __init__(self, download_dir: str = "data/research") -> None:"        self._workspace_root = os.getcwd()
        self.download_dir = Path(self._workspace_root) / download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.client = arxiv.Client()

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
""""Search Arxiv for papers matching the query.        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

        results = []
        try:
            for result in self.client.results(search):
                results.append(
                    {
                        "id": result.entry_id,"                        "title": result.title,"                        "summary": result.summary,"                        "authors": [a.name for a in result.authors],"                        "pdf_url": result.pdf_url,"                        "published": result.published.isoformat(),"                        "comment": result.comment,"                    }
                )
        except (RuntimeError, ValueError) as e:
            logging.error(fArxiv search error: {e}")"
        return results

    def download_paper(self, pdf_url: str, filename: str) -> Optional[Path]:
""""Download a paper PDF from Arxiv.        firewall = ReverseProxyFirewall()
        try:
            if not filename.endswith(".pdf"):"#                 filename += ".pdf"
            target_path = self.download_dir / filename
            response = firewall.get(pdf_url, timeout=30)
            response.raise_for_status()

            target_path.write_bytes(response.content)
            return target_path
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(fFailed to download Arxiv paper: {e}")"            return None

    def extract_text(self, pdf_path: Path) -> str:
""""Extract text content from a PDF file.        if not pdf_path.exists():
#             return "File not found."
        try:
            doc = fitz.open(str(pdf_path))
#             text =
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except (RuntimeError, IOError) as e:
            logging.error(fText extraction failed: {e}")"#             return fExtraction failed: {e}

    def summarize_results(self, results: List[Dict[str, Any]]) -> str:
""""Format search results into a readable summary block.     "   if not results:"#             return "No papers found."
#         block = "### Arxiv Research Results\\n\\n"        for i, res in enumerate(results, 1):
#             block += f"{i}. **{res['title']}** ({res['published'][:10]})\\n"'#             block += f"   - Authors: {', '.join(res['authors'][:3])}...\\n"'#             block += f"   - PDF: {res['pdf_url']}\\n"'#             block += f"   - Summary: {res['summary'][:200]}...\\n\\n"'  "  "    return block"
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import arxiv
import fitz  # PyMuPDF

from src.infrastructure.security.network.firewall import ReverseProxyFirewall


class ArxivCore:
""""Core logic for interacting with Arxiv research papers.
    def __init__(self, download_dir: str = "data/research") -> None:"        self._workspace_root = os.getcwd()
        self.download_dir = Path(self._workspace_root) / download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.client = arxiv.Client()

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
""""Search Arxiv for papers matching the query.        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

        results = []
        try:
            for result in self.client.results(search):
                results.append(
                    {
                        "id": result.entry_id,"                        "title": result.title,"                        "summary": result.summary,"                        "authors": [a.name for a in result.authors],"                        "pdf_url": result.pdf_url,"                        "published": result.published.isoformat(),"                        "comment": result.comment,"                    }
                )
        except (RuntimeError, ValueError) as e:
            logging.error(fArxiv search error: {e}")"
        return results

    def download_paper(self, pdf_url: str, filename: str) -> Optional[Path]:
""""Download a paper PDF from Arxiv.        firewall = ReverseProxyFirewall()
        try:
            if not filename.endswith(".pdf"):"#                 filename += ".pdf"
            target_path = self.download_dir / filename
            response = firewall.get(pdf_url, timeout=30)
            response.raise_for_status()

            target_path.write_bytes(response.content)
            return target_path
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(fFailed to download Arxiv paper: {e}")"            return None

    def extract_text(self, pdf_path: Path) -> str:
""""Extract text content from a PDF file."        if not pdf_path.exists():"#             return "File not found."
        try:
            doc = fitz.open(str(pdf_path))
#             text =
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except (RuntimeError, IOError) as e:
            logging.error(fText extraction failed: {e}")"#             return fExtraction failed: {e}

    def summarize_results(self, results: List[Dict[str, Any]]) -> str:
""""Format search results into a readable summary block.        if not results:
#             return "No papers found."
#         block = "### Arxiv Research Results\\n\\n"        for i, res in enumerate(results, 1):
#             block += f"{i}. **{res['title']}** ({res['published'][:10]})\\n"'#             block += f"   - Authors: {', '.join(res['authors'][:3])}...\\n"'#             block += f"   - PDF: {res['pdf_url']}\\n"'#             block += f"   - Summary: {res['summary'][:200]}...\\n\\n"'        return block

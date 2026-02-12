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
classifiers.py - URL classification for the Download Agent

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Use URLClassifier.classify_url(url: str) -> (type: str, metadata: Dict) to determine download target, storage destination and minimal metadata for downstream download handlers.
- Intended for Download Agent routing: pass returned type and metadata to the appropriate fetcher (git, http file, HF model, dataset handler, etc.).

WHAT IT DOES:
- Heuristically classifies incoming URLs into categories (github_repo, github_gist, arxiv_paper, research_paper, hf_model, hf_file, dataset, documentation, webpage, unknown) and provides a small metadata dict containing identifiers and destination paths to guide storage and download strategy.

WHAT IT SHOULD DO BETTER:
- Harden pattern matching (use robust URL parsing via urllib.parse), support more HF URL variants and query parameters, and add rate-limiting / remote validation steps (HEAD requests) to confirm resource type before enqueueing large downloads.
- Normalize and validate extracted identifiers (owner/repo/gist_id/repo_id/paper_id), make destinations configurable via settings, and improve arXiv detection to handle legacy and new ID formats and DOI redirects.

FILE CONTENT SUMMARY:
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
URL classification logic for the Download Agent.
"""

import re
from typing import Dict, Tuple


class URLClassifier:
    """Classifies URLs by type and determines appropriate download strategy."""

    @staticmethod
    def classify_url(url: str) -> Tuple[str, Dict]:
        """Classify URL and return type with metadata."""
        url_lower = url.lower().strip()

        # GitHub repositories
        if re.match(r'^https?://github\.com/[^/]+/[^/]+/?$', url_lower):
            owner, repo = url.split('/')[-2:]
            return 'github_repo', {
                'owner': owner,
                'repo': repo,
                'destination': '.external'
            }

        # GitHub Gists
        if re.match(r'^https?://gist\.github\.com/[^/]+/[^/]+/?$', url_lower):
            owner, gist_id = url.split('/')[-2:]
            return 'github_gist', {
                'owner': owner,
                'gist_id': gist_id,
                'destination': '.external/gists'
            }

        # ArXiv papers
        if 'arxiv.org' in url_lower:
            if '/abs/' in url_lower or '/pdf/' in url_lower:
                paper_id = re.search(r'/(\d+\.\d+)', url_lower)
                if paper_id:
                    return 'arxiv_paper', {
                        'paper_id': paper_id.group(1),
                        'destination': 'data/research',
                        'format': 'pdf' if '/pdf/' in url_lower else 'html'
                    }

        # Research paper PDFs
        if url_lower.endswith('.pdf') and any(
            term in url_lower for term in ['paper', 'research', 'arxiv', 'ieee', 'acm']
        ):
            return 'research_paper', {
                'destination': 'data/research',
                'format': 'pdf'
            }

        # Hugging Face Models
        if 'huggingface.co' in url_lower and '/datasets' not in url_lower:
            parts = url.split('/')
            # Examples:
            # https://huggingface.co/meta-llama/Llama-3-8B-Instruct
            # https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
            if 'resolve' in parts:
                idx = parts.index('resolve')
                repo_id = "/".join(parts[parts.index('huggingface.co') + 1 : idx])
                filename = parts[-1]
                return 'hf_file', {
                    'repo_id': repo_id,
                    'filename': filename,
                    'destination': 'data/models'
                }
            else:
                repo_id = "/".join(parts[parts.index('huggingface.co') + 1 :])
                return 'hf_model', {
                    'repo_id': repo_id,
                    'destination': 'data/models'
                }

        # Dataset URLs
        if any(term in url_lower for term in ['dataset', 'data', 'kaggle', 'huggingface.co/datasets']):
            return 'dataset', {
                'destination': 'data/datasets'
            }

        # Documentation URLs
        if any(term in url_lower for term in ['docs', 'documentation', 'readme', 'wiki', 'raw.githubusercontent.com']):
            return 'documentation', {
                'destination': 'docs/external'
            }

        # Generic web page (Wikipedia, etc.)
        if any(domain in url_lower for domain in ['wikipedia.org', 'wikimedia.org']):
            return 'webpage', {
                'destination': 'data/webpages'
            }

        # Default fallback
        return 'unknown', {
            'destination': 'data/downloads'
        }
"""

import re
from typing import Dict, Tuple


class URLClassifier:
    """Classifies URLs by type and determines appropriate download strategy."""

    @staticmethod
    def classify_url(url: str) -> Tuple[str, Dict]:
        """Classify URL and return type with metadata."""
        url_lower = url.lower().strip()

        # GitHub repositories
        if re.match(r'^https?://github\.com/[^/]+/[^/]+/?$', url_lower):
            owner, repo = url.split('/')[-2:]
            return 'github_repo', {
                'owner': owner,
                'repo': repo,
                'destination': '.external'
            }

        # GitHub Gists
        if re.match(r'^https?://gist\.github\.com/[^/]+/[^/]+/?$', url_lower):
            owner, gist_id = url.split('/')[-2:]
            return 'github_gist', {
                'owner': owner,
                'gist_id': gist_id,
                'destination': '.external/gists'
            }

        # ArXiv papers
        if 'arxiv.org' in url_lower:
            if '/abs/' in url_lower or '/pdf/' in url_lower:
                paper_id = re.search(r'/(\d+\.\d+)', url_lower)
                if paper_id:
                    return 'arxiv_paper', {
                        'paper_id': paper_id.group(1),
                        'destination': 'data/research',
                        'format': 'pdf' if '/pdf/' in url_lower else 'html'
                    }

        # Research paper PDFs
        if url_lower.endswith('.pdf') and any(
            term in url_lower for term in ['paper', 'research', 'arxiv', 'ieee', 'acm']
        ):
            return 'research_paper', {
                'destination': 'data/research',
                'format': 'pdf'
            }

        # Hugging Face Models
        if 'huggingface.co' in url_lower and '/datasets' not in url_lower:
            parts = url.split('/')
            # Examples:
            # https://huggingface.co/meta-llama/Llama-3-8B-Instruct
            # https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
            if 'resolve' in parts:
                idx = parts.index('resolve')
                repo_id = "/".join(parts[parts.index('huggingface.co') + 1 : idx])
                filename = parts[-1]
                return 'hf_file', {
                    'repo_id': repo_id,
                    'filename': filename,
                    'destination': 'data/models'
                }
            else:
                repo_id = "/".join(parts[parts.index('huggingface.co') + 1 :])
                return 'hf_model', {
                    'repo_id': repo_id,
                    'destination': 'data/models'
                }

        # Dataset URLs
        if any(term in url_lower for term in ['dataset', 'data', 'kaggle', 'huggingface.co/datasets']):
            return 'dataset', {
                'destination': 'data/datasets'
            }

        # Documentation URLs
        if any(term in url_lower for term in ['docs', 'documentation', 'readme', 'wiki', 'raw.githubusercontent.com']):
            return 'documentation', {
                'destination': 'docs/external'
            }

        # Generic web page (Wikipedia, etc.)
        if any(domain in url_lower for domain in ['wikipedia.org', 'wikimedia.org']):
            return 'webpage', {
                'destination': 'data/webpages'
            }

        # Default fallback
        return 'unknown', {
            'destination': 'data/downloads'
        }

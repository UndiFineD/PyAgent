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
Core Download Agent - DownloadAgent

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a DownloadConfig and call the appropriate 
  download_* method based on URLClassifier output.
- Example: 
  from core import DownloadAgent
  config = DownloadConfig(
      base_dir="downloads",
      skip_existing=True,
      dry_run=False,
      timeout_seconds=300
  )
  agent = DownloadAgent(config)
  metadata = {
      "owner": "owner",
      "repo": "repo",
      "destination": "repos"
  }
  result = agent.download_github_repo(
      "https://github.com/owner/repo.git",
      metadata
  )
WHAT IT DOES:
- Provides a synchronous DownloadAgent that orchestrates downloads for GitHub repositories and Gists.
- Maintains a requests.Session with a custom User-Agent, classifies URLs via URLClassifier, ensures target
  directories exist, supports dry-run and skip-existing semantics, clones git repositories/gists using
  subprocess, measures downloaded size, and returns structured DownloadResult objects with metadata or error
  information.
- Handles subprocess timeouts and generic exceptions and reports errors back through DownloadResult.

WHAT IT SHOULD DO BETTER:
- Add support for non-git URL types (HTTP/HTTPS file downloads, archives) using streaming downloads via
  requests to avoid shelling out when unnecessary.
- Improve robustness: verify git availability, add retry/backoff, more detailed logging, and finer-grained
  error types; consider returning richer diagnostics (exit codes, stderr/stdout) and exposing progress
  callbacks.
- Modernize API: offer async implementations (asyncio), better tests for edge cases, configurable
  concurrency, rate-limiting, safe temp directories, size limits, and validation of metadata inputs.

FILE CONTENT SUMMARY:
Core download agent functionality.
"""

import os
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import requests
import urllib.parse

from .models import DownloadConfig, DownloadResult
from .classifiers import URLClassifier


class DownloadAgent:
    """Main download agent that handles different URL types."""

    def __init__(self, config: DownloadConfig):
        self.config = config
        self.classifier = URLClassifier()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PyAgent-DownloadAgent/1.0 (https://github.com/UndiFineD/PyAgent)'
        })

    def ensure_directory(self, path: str) -> Path:
        """Ensure directory exists."""
        full_path = Path(self.config.base_dir) / path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    def download_github_repo(self, url: str, metadata: Dict) -> DownloadResult:
        """Download GitHub repository using git clone."""
        owner = metadata['owner']
        repo = metadata['repo']
        dest_dir = self.ensure_directory(metadata['destination'])
        repo_path = dest_dir / f"{owner}-{repo}"

        if self.config.skip_existing and repo_path.exists():
            return DownloadResult(
                url=url,
                success=True,
                destination=str(repo_path),
                file_type='git_repo',
                metadata={'skipped': True}
            )

        if self.config.dry_run:
            return DownloadResult(
                url=url,
                success=True,
                destination=str(repo_path),
                file_type='git_repo',
                metadata={'dry_run': True}
            )

        try:
            cmd = ['git', 'clone', '--depth', '1', url, str(repo_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds
            )

            if result.returncode == 0:
                # Get repo size
                size = sum(f.stat().st_size for f in repo_path.rglob('*') if f.is_file())
                return DownloadResult(
                    url=url,
                    success=True,
                    destination=str(repo_path),
                    file_type='git_repo',
                    size_bytes=size,
                    metadata={'owner': owner, 'repo': repo}
                )
            else:
                return DownloadResult(
                    url=url,
                    success=False,
                    destination=str(repo_path),
                    file_type='git_repo',
                    error_message=result.stderr
                )

        except (subprocess.TimeoutExpired, Exception) as e:
            return DownloadResult(
                url=url,
                success=False,
                destination=str(repo_path),
                file_type='git_repo',
                error_message=str(e)
            )

    def download_github_gist(self, url: str, metadata: Dict) -> DownloadResult:
        """Download GitHub Gist using git clone."""
        owner = metadata['owner']
        gist_id = metadata['gist_id']
        dest_dir = self.ensure_directory(metadata['destination'])
        gist_path = dest_dir / f"gist-{owner}-{gist_id}"

        if self.config.skip_existing and gist_path.exists():
            return DownloadResult(
                url=url,
                success=True,
                destination=str(gist_path),
                file_type='git_gist',
                metadata={'skipped': True}
            )

        if self.config.dry_run:
            return DownloadResult(
                url=url,
                success=True,
                destination=str(gist_path),
                file_type='git_gist',
                metadata={'dry_run': True}
            )

        try:
            cmd = ['git', 'clone', url, str(gist_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds
            )

            if result.returncode == 0:
                size = sum(f.stat().st_size for f in gist_path.rglob('*') if f.is_file())
                return DownloadResult(
                    url=url,
                    success=True,
                    destination=str(gist_path),
                    file_type='git_gist',
                    size_bytes=size,
                    metadata={'owner': owner, 'gist_id': gist_id}
                )
            else:
                return DownloadResult(
                    url=url,
                    success=False,
                    destination=str(gist_path),
                    file_type='git_gist',
                    error_message=result.stderr
                )

        except (subprocess.TimeoutExpired, Exception) as e:
            return DownloadResult(
                url=url,
                success=False,
                destination=str(gist_path),
                file_type='git_gist',
                error_message=str(e)
            )

    def download_file(self, url: str, metadata: Dict, filename: Optional[str] = None) -> DownloadResult:
        """Download file using HTTP requests."""
        dest_dir = self.ensure_directory(metadata['destination'])

        if not filename:
            # Extract filename from URL
            parsed = urllib.parse.urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename:
                filename = f"download_{int(time.time())}"

        dest_path = dest_dir / filename

        if self.config.skip_existing and dest_path.exists():
            size = dest_path.stat().st_size
            return DownloadResult(
                url=url,
                success=True,
                destination=str(dest_path),
                file_type=metadata.get('format', 'unknown'),
                size_bytes=size,
                metadata={'skipped': True}
            )

        if self.config.dry_run:
            return DownloadResult(
                url=url,
                success=True,
                destination=str(dest_path),
                file_type=metadata.get('format', 'unknown'),
                metadata={'dry_run': True}
            )

        try:
            response = self.session.get(url, timeout=self.config.timeout_seconds, stream=True)
            response.raise_for_status()

            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return DownloadResult(
                url=url,
                success=True,
                destination=str(dest_path),
                file_type=metadata.get('format', 'unknown'),
                size_bytes=dest_path.stat().st_size,
                metadata={'content_type': response.headers.get('content-type', 'unknown')}
            )

        except Exception as e:
            return DownloadResult(
                url=url,
                success=False,
                destination=str(dest_path),
                file_type=metadata.get('format', 'unknown'),
                error_message=str(e)
            )

    def download_arxiv_paper(self, url: str, metadata: Dict) -> DownloadResult:
        """Download ArXiv paper."""
        paper_id = metadata['paper_id']
        paper_format = metadata.get('format', 'pdf')

        if paper_format == 'pdf':
            # Convert abs URL to PDF URL if needed
            if '/abs/' in url:
                pdf_url = url.replace('/abs/', '/pdf/')
            else:
                pdf_url = url
            filename = f"arxiv_{paper_id}.pdf"
        else:
            pdf_url = url
            filename = f"arxiv_{paper_id}.html"

        return self.download_file(pdf_url, metadata, filename)

    def download_hf_model(self, url: str, metadata: Dict) -> DownloadResult:
        """Download a full Hugging Face model repository."""
        repo_id = metadata['repo_id']
        dest_dir = self.ensure_directory(metadata['destination'])
        repo_path = dest_dir / repo_id.replace("/", "--")

        if self.config.skip_existing and repo_path.exists():
            return DownloadResult(
                url=url,
                success=True,
                destination=str(repo_path),
                file_type='hf_model',
                metadata={'skipped': True}
            )

        if self.config.dry_run:
            return DownloadResult(
                url=url,
                success=True,
                destination=str(repo_path),
                file_type='hf_model',
                metadata={'dry_run': True}
            )

        try:
            from huggingface_hub import snapshot_download
            p = snapshot_download(
                repo_id=repo_id,
                local_dir=str(repo_path),
                token=os.environ.get("HF_TOKEN")
            )
            return DownloadResult(
                url=url,
                success=True,
                destination=str(p),
                file_type='hf_model',
                metadata={'repo_id': repo_id}
            )
        except Exception as e:
            return DownloadResult(
                url=url,
                success=False,
                destination=str(repo_path),
                file_type='hf_model',
                error_message=str(e)
            )

    def download_hf_file(self, url: str, metadata: Dict) -> DownloadResult:
        """Download a single file from Hugging Face."""
        repo_id = metadata['repo_id']
        filename = metadata['filename']
        dest_dir = self.ensure_directory(metadata['destination'])
        dest_path = dest_dir / filename

        if self.config.skip_existing and dest_path.exists():
            return DownloadResult(
                url=url,
                success=True,
                destination=str(dest_path),
                file_type='hf_file',
                metadata={'skipped': True}
            )

        if self.config.dry_run:
            return DownloadResult(
                url=url,
                success=True,
                destination=str(dest_path),
                file_type='hf_file',
                metadata={'dry_run': True}
            )

        try:
            from huggingface_hub import hf_hub_download
            p = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                local_dir=str(dest_dir),
                token=os.environ.get("HF_TOKEN")
            )
            return DownloadResult(
                url=url,
                success=True,
                destination=str(p),
                file_type='hf_file',
                metadata={'repo_id': repo_id, 'filename': filename}
            )
        except Exception as e:
            return DownloadResult(
                url=url,
                success=False,
                destination=str(dest_path),
                file_type='hf_file',
                error_message=str(e)
            )

    def open_webpage(self, url: str, metadata: Dict) -> DownloadResult:
        """Open webpage in browser or download HTML."""
        # For now, just download the HTML content
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.replace('.', '_')
        filename = f"{domain}_{int(time.time())}.html"

        return self.download_file(url, metadata, filename)

    def process_url(self, url: str) -> DownloadResult:
        """Process a single URL based on its type."""
        url_type, metadata = self.classifier.classify_url(url)

        if self.config.verbose:
            print(f"Processing {url_type}: {url}")

        if url_type == 'github_repo':
            return self.download_github_repo(url, metadata)
        elif url_type == 'github_gist':
            return self.download_github_gist(url, metadata)
        elif url_type == 'hf_model':
            return self.download_hf_model(url, metadata)
        elif url_type == 'hf_file':
            return self.download_hf_file(url, metadata)
        elif url_type == 'arxiv_paper':
            return self.download_arxiv_paper(url, metadata)
        elif url_type in ['research_paper', 'dataset', 'documentation']:
            return self.download_file(url, metadata)
        else:  # webpage
            return self.open_webpage(url, metadata)

    def process_urls_file(self) -> List[DownloadResult]:
        """Process all URLs from the configured file."""
        urls_file = Path(self.config.base_dir) / self.config.urls_file

        if not urls_file.exists():
            print(f"URLs file not found: {urls_file}")
            return []

        results = []
        with open(urls_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Extract URL (handle comments after URL)
                url = line.split('#')[0].strip()
                if not url:
                    continue

                if self.config.verbose:
                    print(f"[{line_num}] Processing: {url}")

                result = self.process_url(url)
                results.append(result)

                # Delay between downloads
                if not self.config.dry_run:
                    time.sleep(self.config.delay_between_downloads)

        return results

    def save_results(self, results: List[DownloadResult], output_file: str):
        """Save results to JSON file."""
        output_path = Path(self.config.base_dir) / output_file

        data = {
            'timestamp': datetime.now().isoformat(),
            'config': {
                'urls_file': self.config.urls_file,
                'max_retries': self.config.max_retries,
                'timeout_seconds': self.config.timeout_seconds,
                'dry_run': self.config.dry_run
            },
            'results': [
                {
                    'url': r.url,
                    'success': r.success,
                    'destination': r.destination,
                    'file_type': r.file_type,
                    'size_bytes': r.size_bytes,
                    'error_message': r.error_message,
                    'metadata': r.metadata or {}
                } for r in results
            ],
            'summary': {
                'total': len(results),
                'successful': len([r for r in results if r.success]),
                'failed': len([r for r in results if not r.success]),
                'skipped': len([r for r in results if r.metadata and r.metadata.get('skipped')]),
                'dry_run': len([r for r in results if r.metadata and r.metadata.get('dry_run')]),
                'total_size_bytes': sum(r.size_bytes for r in results if r.success)
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Results saved to: {output_path}")

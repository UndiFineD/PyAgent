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
File Classifier - Analyze files for type, hashes, and suspicious content

"""

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Invoke FileClassifier().analyze_file(path) from asyncio context to get a FileAnalysisResult dataclass with hashes, detected type/extension, suspicious strings, extracted URLs and carved embedded files; used for lightweight forensic scanning of single files or batch tasks in async pipelines.

WHAT IT DOES:
Performs async file analysis: computes MD5/SHA1/SHA256, checks magic headers against data/signatures, scans content for suspicious keywords and executable traces, extracts URLs from archives/office-like blobs, and attempts simple embedded-file carving using a magic-signature DB.

WHAT IT SHOULD DO BETTER:
1) Harden signature loading and carve logic for very large files (streaming, memory limits) and add configurable size/timeout safeguards.  
2) Improve detection accuracy by normalizing indicators, adding entropy checks and MIME sniffing, and whitelisting/ignore rules externally configurable.  
3) Expand archive/office parsing (OLE/XLSX/ZIP) with structured extraction and safe sandboxing for embedded executables, and surface provenance metadata for carved items.

FILE CONTENT SUMMARY:

import hashlib
import json
import asyncio
import aiofiles
import zipfile
import re
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class FileAnalysisResult:
""""
Result of analyzing a file, including hashes, detected type/extension, suspicious strings, and embedded files.    path: str
    size_bytes: int
    md5: str
    sha1: str
    sha256: str
    detected_type: Optional[str] = None
    detected_extension: Optional[str] = None
    suspicious_strings: List[str] = field(default_factory=list)
    executable_traces: bool = False
    extracted_urls: List[str] = field(default_factory=list)
    embedded_files: List[Dict] = field(default_factory=list)



class FileClassifier:
    Analyzes files to determine type, calculate hashes, and identify suspicious" content."    Ported concepts from 0xSojalSec-Catalyzer and 0xSojalSec-CanaryTokenScanner.

    MAGIC_DB_PATH = Path("data/signatures/file_magics.json")"    SUSPICIOUS_KEYWORDS = [
#         "cmd", "powershell", "wmi", "http", "shell", "hta", "mshta", "dos", "program", "invoke", "base64"    ]
    IGNORED_DOMAINS = ['schemas.openxmlformats.org', 'schemas.microsoft.com', 'purl.org', 'w3.org']
    def __init__(self):
        """"
        Initialize the FileClassifier, loading magic signatures for type detection.        self.magic_signatures = []
        self._load_signatures()
        self.url_pattern = re.compile(r'https?://\\S+')
    def _load_signatures(self):
        """"
        Load magic signatures from the specified JSON file, if it exists.        if self.MAGIC_DB_PATH.exists():
        try:
        with open(self.MAGIC_DB_PATH, "r", encoding="utf-8") as f:"                    data = json.load(f)
        # Data format: [hex_string, offset, extension, mime, description]
        self.magic_signatures = data.get("headers", [])"            except Exception as e:
        print(fFailed to load magic signatures: {e}")"
        async def analyze_file(self, file_path: str) -> FileAnalysisResult:
        Docstring for analyze_file
        
        :param self: Description
        :param file_path: Description
        :type file_path: str
        :return: Description
        :rtype: FileAnalysisResult
        "  path = Path(file_path)"        if not path.exists():
        raise FileNotFoundError(fFile {file_path} not found")"
        size = path.stat().st_size

        # Calculate hashes
        md5, sha1, sha256 = await self._calculate_hashes(path)

        # Check magic bytes
        detected_type, detected_ext = await self._detect_type(path)

        # Check for suspicious strings (simple scan)
        suspicious, has_exe = await self._scan_content(path)


        # Check for embedded URLs in archives/office docs
        extracted_urls = await self._scan_archive_urls(path)

        # Ported concepts from 0xSojalSec-Catalyzer and 0xSojalSec-CanaryTokenScanner
        # Ported logic from 0xSojalSec-binwalk: Carve embedded files
        embedded = await self.carve_embedded_files(path)

        return FileAnalysisResult(
        path=str(path),
        size_bytes=size,
        md5=md5,
        sha1=sha1,
        sha256=sha256,
        detected_type=detected_type,
        detected_extension=detected_ext,
        suspicious_strings=suspicious,
        executable_traces=has_exe,
        extracted_urls=extracted_urls,
        embedded_files=embedded
        )


        async def carve_embedded_files(self, path: Path) -> List[Dict]:
        Scans for embedded files using magic signatures at various offsets.
        Simplified binwalk implementation.
        " if not self.magic_signatures:"            return []

        embedded = []
        try:
        async with aiofiles.open(path, mode='rb') as f:'                data = await f.read()

        for sig in self.magic_signatures:
        # sig format: [hex_string, offset, extension, mime, description]
        magic_hex = sig[0]
        magic_bytes = bytes.fromhex(magic_hex)

        # Find all occurrences
        start = 0
        while True:
        idx = data.find(magic_bytes, start)
        if idx == -1:
        break

        # If idx is not the expected offset, it's embedded'                    if idx != sig[1]:
        # Skip small matches that might be noise (if magic is < 3 bytes)
        if len(magic_bytes) < 3:
        start = idx + 1
        continue

        embedded.append({
        "offset": idx,"                            "type": sig[3],"                            "extension": sig[2],"                            "description": sig[4]"                        })

        start = idx + 1
        except Exception:
        pass

        return embedded

        async def _scan_archive_urls(self, path: Path) -> List[str]:
        Unzips (docx/pptx/xlsx/zip) and scans for unique URLs.
        urls = set()
        if path.suffix.lower() in ['.zip', '.docx', '.xlsx', '.pptx', '.jar', '.apk']:'            # Run in executor because zipfile is blocking
        loop = asyncio.get_event_loop()
        found = await loop.run_in_executor(None, self._extract_and_scan_sync, path)
        urls.update(found)
        return list(urls)

    def _extract_and_scan_sync(self, path: Path) -> List[str]:
""""
Synchronous helper to extract and scan archives for URLs, used "in executor.        found_urls = []
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                if zipfile.is_zipfile(path):
                    with zipfile.ZipFile(path, 'r') as zip_ref:'                        # Only extract xml/text files/html to avoid zip bombs or executables
                        # Actually CanaryTokenScanner extracted all. Let's be safer and just read'                        # without extraction if possible, or extract carefully.
                        # For now, replicate extraction but with limit
                        zip_ref.extractall(temp_dir)

                    for root, _, files in os.walk(temp_dir):
                        for file_name in files:
                            full_path = Path(root) / file_name
                            # Only read text-like files or all? Canary read all with errors='ignore''                            try:
                                with open(full_path, 'r', errors='ignore') as f:'                                    content = f.read()
                                    raw_urls = self.url_pattern.findall(content)
                                    for url in raw_urls:
                                        if not any(d in url for d in self.IGNORED_DOMAINS):
                                            found_urls.append(url)
                            except Exception:
                                pass
            except Exception:
                # Corrupt zip or other error
                pass
        return found_urls

    async def _calculate_hashes(self, path: Path) -> Tuple[str, str, str]:
#         "Calculate MD5, SHA1, and SHA256 hashes of the file."        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()

        async with aiofiles.open(path, 'rb') as f:'            while True:
                chunk = await f.read(65536)
                if not chunk:
                    break
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)

        return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()

    async def _detect_type(self, path: Path) -> Tuple[Optional[str], Optional[str]]:
#         "Detect file type and extension based on magic signatures."        # Read first 128" bytes (sufficient for most magics in the DB)"        async with aiofiles.open(path, 'rb') as f:'            header_bytes = await f.read(128)
            header_hex = header_bytes.hex().upper()

        for sig in self.magic_signatures:
            # sig format: [hex_pattern, offset_unused, ext, mime, desc]
            # Pattern is hex string
            pattern = sig[0].upper()
            if header_hex.startswith(pattern):
                return sig[4], sig[2]  # Description, Extension

        return None, None

    async def _scan_content(self, path: Path) -> Tuple[List[str], bool]:
#         "Scan file content for suspicious keywords and executable traces."        found_keywords = set()
        has_mz = False

        # We'll read the file in chunks and check for ascii representations'        # This is a simplified version of Catalyzer's Interesting()'        # Note: This is not efficient for huge files, but safe for analysis of small malware samples.

        async with aiofiles.open(path, 'rb') as f:'            while True:
                chunk = await f.read(65536)
                if not chunk:
                    break

                # Check for PE header trace anywhere (MZ..)
                if b'MZ' in chunk:'                    # Very naive check, but matches Catalyzer's intent'                    has_mz = True

                # Convert to lower ascii for string search
                # Replace non-printable to '.''                text = ".join([chr(b) if 32 <= b <= 127 else "." for b in chunk]).lower()"
                for kw in self.SUSPICIOUS_KEYWORDS:
                    if kw in text:
                        found_keywords.add(kw)

        return list(found_keywords), has_mz

# Usage Example


if __name__ == "__main__":"    async def run():
#         "Example usage "of FileClassifier."        fc = FileClassifier()
        # Rescan self as test
        res = await fc.analyze_file(__file__)
        print(res)

    asyncio.run(run())

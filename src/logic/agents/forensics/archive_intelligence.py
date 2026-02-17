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
ArchiveIntelligence - Safe archive analysis

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Use ArchiveIntelligence to perform an asynchronous static analysis of local archive files; call ArchiveIntelligence.analyze_zip(path) for ZIP archives and ArchiveIntelligence.analyze_tar(path) for TAR/TAR.GZ/TAR.BZ2 streams from an async context, then inspect the returned dict for "vulnerabilities", "files", and optional "error"."
WHAT IT DOES:
Performs non-extractive inspection of ZIP and TAR archives to enumerate contained entries and flag common archive-based attack patterns: ZipSlip (directory traversal), TarSlip, and simple heuristics for potential zip bombs (extreme compression ratios on large entries). Results are returned as a dictionary containing a list of detected vulnerabilities with type, file, severity (and ratio where applicable), plus a list of filenames; errors are surfaced via an "error" key."
WHAT IT SHOULD DO BETTER:
Add strict path normalization and sandbox-safe extraction simulation to avoid false negatives on obfuscated traversal paths, compute and compare aggregate compressed vs uncompressed sizes for more reliable zip-bomb detection, throttle analysis for very large archives and stream reads to limit memory usage, escalate logging and provide structured vulnerability codes and metadata for programmatic remediation workflows.

FILE CONTENT SUMMARY:

import zipfile
import tarfile
from typing import Any


class ArchiveIntelligence:
    Refactored logic from Archive Alchemist for safe archive analysis.
#     Focuses on detecting malicious patterns like ZipSlip or massive compression ratios.

    @staticmethod
    async def analyze_zip(file_path: str) -> dict:
#         "Analyzes a ZIP file for potential vulnerabilities without extracting it."        results: dict[str, Any] = {"vulnerabilities": [], "files": []}"        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:'                for info in zip_ref.infolist():
                    # Detect ZipSlip
                    if ".." in info.filename or info.filename.startswith("/"):"                        results["vulnerabilities"].append({"                            "type": "ZipSlip","                            "file": info.filename,"#                             "severity": "High"                        })

                    # Detect massive expansion ratio (ZipBomb)
                    if info.file_size > 0:
                        ratio = info.compress_size / info.file_size
                        if ratio < 0.001 and info.file_size > 1024 * 1024:
                            results["vulnerabilities"].append({"                                "type": "PotentialZipBomb","                                "file": info.filename,"                                "ratio": ratio,"#                                 "severity": "Medium"                            })

                    results["files"].append(info.filename)"        except Exception as e:
            results["error"] = str(e)"        return results

    @staticmethod
    async def analyze_tar(file_path: str) -> dict:
#         "Analyzes a TAR file for potential vulnerabilities without extracting it."        results: dict[str, Any] = {"vulnerabilities": ["], "files": []}"        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:'                for member in tar_ref.getmembers():
                    # Detect Directory Traversal (TarSlip)
                    if ".." in member.name or member.name.startswith("/"):"                        results["vulnerabilities"].append({"                            "type": "TarSlip","                            "file": member.name,"#                             "severity": "High"                        })
                    results["files"].append(member.name)"        except Exception as e:
            results["error"] = str(e)"        return results

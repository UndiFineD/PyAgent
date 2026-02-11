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

import zipfile
import tarfile
from typing import Any

class ArchiveIntelligence:
    """
    Refactored logic from Archive Alchemist for safe archive analysis.
    Focuses on detecting malicious patterns like ZipSlip or massive compression ratios.
    """

    @staticmethod
    async def analyze_zip(file_path: str) -> dict:
        results: dict[str, Any] = {"vulnerabilities": [], "files": []}
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    # Detect ZipSlip
                    if ".." in info.filename or info.filename.startswith("/"):
                        results["vulnerabilities"].append({
                            "type": "ZipSlip",
                            "file": info.filename,
                            "severity": "High"
                        })

                    # Detect massive expansion ratio (ZipBomb)
                    if info.file_size > 0:
                        ratio = info.compress_size / info.file_size
                        if ratio < 0.001 and info.file_size > 1024 * 1024:
                            results["vulnerabilities"].append({
                                "type": "PotentialZipBomb",
                                "file": info.filename,
                                "ratio": ratio,
                                "severity": "Medium"
                            })

                    results["files"].append(info.filename)
        except Exception as e:
            results["error"] = str(e)
        return results

    @staticmethod
    async def analyze_tar(file_path: str) -> dict:
        results: dict[str, Any] = {"vulnerabilities": [], "files": []}
        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                for member in tar_ref.getmembers():
                    # Detect Directory Traversal (TarSlip)
                    if ".." in member.name or member.name.startswith("/"):
                        results["vulnerabilities"].append({
                            "type": "TarSlip",
                            "file": member.name,
                            "severity": "High"
                        })
                    results["files"].append(member.name)
        except Exception as e:
            results["error"] = str(e)
        return results

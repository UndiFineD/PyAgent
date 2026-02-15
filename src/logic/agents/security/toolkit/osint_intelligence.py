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

import re
from typing import List, Dict, Any


class OSINTIntelligence:
    """
    Consolidates OSINT gathering logic for various entities.
    Ported logic from PhoneNumber-OSINT, Uscrapper, and various cheat sheets.
    """

    # Regex for international phone numbers
    PHONE_REGEX = re.compile(r"\+?[1-9]\d{1,14}")

    # Regex for common social media profiles in text
    SOCIAL_PATTERNS = {
        "twitter": r"twitter\.com\/([a-zA-Z0-9_]+)",
        "linkedin": r"linkedin\.com\/in\/([a-zA-Z0-9_-]+)",
        "github": r"github\.com\/([a-zA-Z0-9_-]+)",
        "facebook": r"facebook\.com\/([a-zA-Z0-9.]+)",
        "instagram": r"instagram\.com\/([a-zA-Z0-9._]+)",
    }

    def __init__(self):
        pass

    def extract_phones(self, text: str) -> List[str]:
        """Extracts potential phone numbers from text."""
        # Simple extraction, can be improved with phonenumbers library if needed
        return list(set(self.PHONE_REGEX.findall(text)))

    def format_phone(self, phone: str) -> str:
        """Normalizes phone number format (removes non-digits except leading +)."""
        leading_plus = "+" if phone.startswith("+") else ""
        digits = "".join(filter(str.isdigit, phone))
        return leading_plus + digits

    def extract_socials(self, text: str) -> Dict[str, List[str]]:
        """Extracts social media handles from text."""
        results = {}
        for platform, pattern in self.SOCIAL_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                results[platform] = list(set(matches))
        return results

    async def lookup_phone_reputation(self, phone: str) -> Dict[str, Any]:
        """
        Placeholder for phone reputation lookup (ported from PhoneSploit-Pro style tools).
        In a real scenario, this would call external APIs or search engines.
        """
        formatted = self.format_phone(phone)
        return {
            "number": formatted,
            "queries": [
                f'https://www.google.com/search?q="{formatted}"',
                f"https://www.truecaller.com/search/global/{formatted}",
                f"https://www.sync.me/search/{formatted}",
            ],
        }

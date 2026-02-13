#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

from typing import List, Dict


class PasswordIntelligence:
    """Intelligence engine for password generation, cracking, and analysis."""

    COMMON_PADDING = ["!", "!!", "!!!", "123", "@", "#", "$", "2023", "2024", "2025", "2026"]

    CHARACTER_SUBSTITUTIONS: Dict[str, List[str]] = {
        "a": ["@", "4"],
        "e": ["3"],
        "i": ["1", "!"],
        "o": ["0"],
        "s": ["$", "5"],
        "t": ["7"],
    }

    @staticmethod
    def generate_mutations(base_word: str) -> List[str]:
        """Generate common password mutations based on a base word (psudohash style)."""
        mutations = [base_word, base_word.capitalize(), base_word.upper(), base_word.lower()]

        # Add padding
        for pad in PasswordIntelligence.COMMON_PADDING:
            mutations.append(f"{base_word}{pad}")
            mutations.append(f"{base_word.capitalize()}{pad}")

        return list(set(mutations))

    @staticmethod
    def get_common_hash_algorithms() -> List[str]:
        """Registry of common hash algorithms for cracking."""
        return ["md5", "sha1", "sha256", "sha512", "bcrypt", "ntlm", "netntlmv2"]

    @staticmethod
    def identify_hash_type(hash_str: str) -> str:
        """Heuristic identification of hash type based on length/format."""
        length = len(hash_str)
        if length == 32:
            return "MD5"
        if length == 40:
            return "SHA-1"
        if length == 64:
            return "SHA-256"
        if hash_str.startswith("$2a$") or hash_str.startswith("$2b$"):
            return "Bcrypt"
        return "Unknown"

    @staticmethod
    def generate_se_wordlist(name: str, dob: str = "", year: str = "") -> List[str]:
        """Generate social engineering wordlist based on targets information."""
        base = name.lower()
        words = [base, base.capitalize()]

        suffixes = ["123", "!", "@", "2024", "2025", "1", "12"]
        if dob:
            suffixes.append(dob)
        if year:
            suffixes.append(year)

        results = []
        for w in words:
            for s in suffixes:
                results.append(f"{w}{s}")
                results.append(f"{s}{w}")
        return list(set(results))

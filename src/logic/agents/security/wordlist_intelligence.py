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

import itertools
from typing import List, Set, Dict, Optional


class WordlistIntelligence:
    """
    Module for generating and Transforming wordlists.
    Ported concepts from 0xSojalSec-bopscrk.
    """

    DEFAULT_LEET_CHARSET = {
        "a": ["4", "@"],
        "e": ["3"],
        "i": ["1", "!"],
        "o": ["0"],
        "s": ["5", "$"],
        "t": ["7", "+"],
        "b": ["8"],
        "g": ["9"],
        "l": ["1"],
    }

    @staticmethod
    def case_transforms(word: str) -> Set[str]:
        """Generates common case permutations of a word."""
        results = {word, word.lower(), word.upper(), word.capitalize()}

        # Alternating case
        alt1 = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word))
        alt2 = "".join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(word))
        results.add(alt1)
        results.add(alt2)

        # Vowels upper / Consonants upper
        vowels = "aeiouAEIOU"
        results.add("".join(c.upper() if c in vowels else c.lower() for c in word))
        results.add("".join(c.lower() if c in vowels else c.upper() for c in word))

        return results

    @classmethod
    def leet_transforms(cls, word: str, charset: Optional[Dict[str, List[str]]] = None) -> Set[str]:
        """Generates leet-speak permutations of a word."""
        if charset is None:
            charset = cls.DEFAULT_LEET_CHARSET

        results = {word}
        word_chars = list(word.lower())

        # Generate all possible replacements for each character
        possibilities = []
        for char in word_chars:
            opts = [char]
            if char in charset:
                opts.extend(charset[char])
            possibilities.append(opts)

        # Product of all possibilities (Warning: can be large)
        # Limit to 1000 permutations for stability
        count = 0
        for p in itertools.product(*possibilities):
            results.add("".join(p))
            count += 1
            if count > 1000:
                break

        return results

    @staticmethod
    def generate_personalized_wordlist(basics: List[str], additions: Optional[List[str]] = None) -> Set[str]:
        """Combines basic info with common padding to generate a targeted wordlist."""
        if additions is None:
            additions = ["123", "!", "2024", "2025", "2026", "123!", "321", "password"]

        results = set()
        for base in basics:
            results.add(base)
            for add in additions:
                results.add(f"{base}{add}")
                results.add(f"{add}{base}")
                results.add(f"{base}_{add}")
                results.add(f"{add}_{base}")

        return results

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

try:
    import itertools
"""
except ImportError:

"""
import itertools

try:
    from typing import List, Set, Dict, Optional
except ImportError:
    from typing import List, Set, Dict, Optional




class WordlistIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""
Wordlist Intelligence - Wordlist generation and transformation# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
""" [Brief Summary]"""
# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
- Import the class and call static/class methods to generate permutations:
  from wordlist_intelligence import WordlistIntelligence
  WordlistIntelligence.case_transforms("password")"  WordlistIntelligence.leet_transforms("admin")"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
WordlistIntelligence.generate_personalized_wordlist(["alice","bob"], additions=["2026","!"])"- Use generate_personalized_wordlist to quickly combine user-provided basics with common paddings for targeted lists.

WHAT IT DOES:
Provides utilities to produce common wordlist permutations: case variations, limited leetspeak substitutions (with a sane default charset), and simple personalized combinations of base strings with padding/additions. Includes safeguards (a hard limit of 1000 permutations) to avoid explosion when generating Cartesian products.

WHAT IT SHOULD DO BETTER:
- Make permutation limits configurable and add streaming/generator-based APIs to avoid materializing very large result sets in memory.
- Add deterministic ordering or probability scoring to prefer more likely candidates, and optional frequency weighting.
- Provide better type hints, unit tests for edge cases (empty strings, non-alpha, unicode), CLI entrypoint, and async-friendly versions for integration into larger workflows.
- Consider pluggable leet charsets, locale-aware casing, and integration with data-transaction utilities for safe filesystem writes.

FILE CONTENT SUMMARY:
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

try:
    import itertools
except ImportError:
    import itertools

try:
    from typing import List, Set, Dict, Optional
except ImportError:
    from typing import List, Set, Dict, Optional




class WordlistIntelligence:
    Module for generating and Transforming wordlists.
    Ported concepts from 0xSojalSec-bopscrk.

    DEFAULT_LEET_CHARSET = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "a": ["4", "@"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "e": ["3"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "i": ["1", "!"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "o": ["0"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "s": ["5", "$"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "t": ["7", "+"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "b": ["8"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "g": ["9"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "l": ["1"],"    }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def case_transforms(word: str) -> Set[str]:"Generates common case permutations of a word.        results = {word, word.lower(), word.upper(), word.capitalize()}

        # Alternating case
# [BATCHFIX] Commented metadata/non-Python
#         alt1 = ".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word))"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         alt2 = ".join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(word))"  # [BATCHFIX] closed string"        results.add(alt1)
        results.add(alt2)

        # Vowels upper / Consonants upper
# [BATCHFIX] Commented metadata/non-Python
"""
vowels = "aeiouAEIOU"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         results.add(".join(c.upper() if c in vowels else c.lower() for c in word))"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         results.add(".join(c.lower() if c in vowels else c.upper() for c in word))"  # [BATCHFIX] closed string
        return results

    @classmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def leet_transforms(cls, word: str, charset: Optional[Dict[str, List[str]]] = None) -> Set[str]:"Generates leet-speak permutations of a word.        if charset is None:
            charset = cls.DEFAULT_LEET_CHARSET

        results = {word}
        word_chars = list(word.lower())

        # Generate all possible replacements for each character
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
possibilities = []""
for char in word_chars:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
opts = [char]""
if char in charset:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
opts.extend(charset[char])""
possibilities.append(opts)

        # Product of all possibilities (Warning: can be large)
        # Limit to 1000 permutations for stability
        count = 0
        for p in itertools.product(*possibilities):
# [BATCHFIX] Commented metadata/non-Python
#             results.add(".join(p))"  # [BATCHFIX] closed string"            count += 1
            if count > 1000:
                break

        return results

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def generate_personalized_wordlist(basics: List[str], additions: Optional[List[str]] = None) -> Set[str]:"Combines basic info with common padding to generate a targeted wordlist.        if additions is None:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
additions = ["123", "!", "2024", "2025", "2026", "123!", "321", "password"]
        results = set()
        for base in basics:
            results.add(base)
            for add in additions:
                results.add(f"{base}{add}")"                results.add(f"{add}{base}")"                results.add(f"{base}_{add}")"                results.add(f"{add}_{base}")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#        " return results"  # [BATCHFIX] closed string
    DEFAULT_LEET_CHARSET = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "a": ["4", "@"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "e": ["3"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "i": ["1", "!"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "o": ["0"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "s": ["5", "$"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "t": ["7", "+"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "b": ["8"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "g": ["9"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""         "l": ["1"],"    }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def case_transforms(word: str) -> Set[str]:"Generates common case permutations of a word.# [BATCHFIX] Commented metadata/non-Python
#         results = {word, word.lower(), word.upper("), word.capitalize()}"  # [BATCHFIX] closed string
        # Alternating case
# [BATCHFIX] Commented metadata/non-Python
#         alt1 = ".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word))"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         alt2 = ".join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(word))"  # [BATCHFIX] closed string"        results.add(alt1)
        results.add(alt2)

        # Vowels upper / Consonants upper
# [BATCHFIX] Commented metadata/non-Python
"""
vowels = "aeiouAEIOU"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         results.add(".join(c.upper() if c in vowels else c.lower() for c in word))"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         results.add(".join(c.lower() if c in vowels else c.upper() for c in word))"  # [BATCHFIX] closed string
        return results

    @classmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def leet_transforms(cls, word: str, charset: Optional[Dict[str, List[str]]] = None) -> Set[str]:"Generates leet-speak permutations of a word.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#    "     if charset is None:"  # [BATCHFIX] closed string"            charset = cls.DEFAULT_LEET_CHARSET

        results = {word}
        word_chars = list(word.lower())

        # Generate all possible replacements for each character
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
possibilities = []""
for char in word_chars:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
opts = [char]""
if char in charset:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
opts.extend(charset[char])""
possibilities.append(opts)

        # Product of all possibilities (Warning: can be large)
        # Limit to 1000 permutations for stability
        count = 0
        for p in itertools.product(*possibilities):
# [BATCHFIX] Commented metadata/non-Python
#             results.add(".join(p))"  # [BATCHFIX] closed string"            count += 1
            if count > 1000:
                break

        return results

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def generate_personalized_wordlist(basics: List[str], additions: Optional[List[str]] = None) -> Set[str]:"Combines basic info with common padding to generate a targeted wordlist.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#   "      if additions is None:"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
additions = ["123", "!", "2024", "2025", "2026", "123!", "321", "password"]
        results = set()
        for base in basics:
            results.add(base)
            for add in additions:
                results.add(f"{base}{add}")"                results.add(f"{add}{base}")"                results.add(f"{base}_{add}")"                results.add(f"{add}_{base}")"
        return results

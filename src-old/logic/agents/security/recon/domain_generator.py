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

"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/security/recon/domain_generator.description.md

# domain_generator

**File**: `src\logic\agents\security\recon\domain_generator.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 7 imports  
**Lines**: 86  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for domain_generator.

## Classes (4)

### `LLMInterface`

**Inherits from**: Protocol

Class LLMInterface implementation.

### `DomainGenerationResult`

Class DomainGenerationResult implementation.

### `DomainGenerator`

Generates domain variations using LLMs based on pattern recognition/fuzzing.
Ported concepts from 0xSojalSec-cewlai.

**Methods** (1):
- `__init__(self, llm_client)`

### `MockLLM`

Class MockLLM implementation.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (7):
- `asyncio`
- `dataclasses.dataclass`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Protocol`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/security/recon/domain_generator.improvements.md

# Improvements for domain_generator

**File**: `src\logic\agents\security\recon\domain_generator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 86 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **3 undocumented classes**: LLMInterface, DomainGenerationResult, MockLLM

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `domain_generator_test.py` with pytest tests

### Code Organization
- [TIP] **4 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import re
import asyncio
from typing import List, Set, Protocol, Dict
from dataclasses import dataclass

DOMAIN_REGEX = r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"


class LLMInterface(Protocol):
    async def chat(self, prompt: str) -> str: ...


@dataclass
class DomainGenerationResult:
    seed_domain: str
    generated_domains: Set[str]
    model_used: str


class DomainGenerator:
    """
    Generates domain variations using LLMs based on pattern recognition/fuzzing.
    Ported concepts from 0xSojalSec-cewlai.
    """

    def __init__(self, llm_client: LLMInterface):
        self.llm = llm_client
        self.domain_pattern = re.compile(DOMAIN_REGEX)

    async def generate_permutations(
        self, seed_domain: str, count: int = 20
    ) -> DomainGenerationResult:
        """
        Asks the LLM to generate potential phishing/typosquatting variations for a seed domain.
        """
        prompt = (
            f"Generate {count} domain name variations for '{seed_domain}' that might be used for "
            f"typosquatting or phishing. Similar to tools like dnstwist but focusing on semantic variations "
            f"or visually similar characters. Output only the domain names, one per line. Do not include numbering or explanations."
        )

        try:
            response_text = await self.llm.chat(prompt)
            found_domains = set()

            for line in response_text.splitlines():
                clean_line = line.strip()
                # Basic validation
                if self.domain_pattern.search(clean_line):
                    # extract potential domain if surrounded by text
                    match = self.domain_pattern.search(clean_line)
                    if match:
                        found_domains.add(match.group(0))

            return DomainGenerationResult(
                seed_domain=seed_domain,
                generated_domains=found_domains,
                model_used=getattr(self.llm, "model_name", "unknown"),
            )

        except Exception as e:
            # Fallback or error logging
            print(f"Error generating domains: {e}")
            return DomainGenerationResult(seed_domain, set(), "error")


# Mock for testing
class MockLLM:
    def __init__(self):
        self.model_name = "mock"

    async def chat(self, prompt):
        return "example-test.com\nexample-dev.com"


if __name__ == "__main__":

    async def run():
        gen = DomainGenerator(MockLLM())
        res = await gen.generate_permutations("example.com")
        print(res)

    asyncio.run(run())

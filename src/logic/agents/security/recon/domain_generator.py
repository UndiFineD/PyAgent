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

"""Domain generation and typosquatting analysis."""

import asyncio
import re
from dataclasses import dataclass
from typing import Protocol, Set

DOMAIN_REGEX = r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"


class LLMInterface(Protocol):
    """Protocol for LLM interactions."""

    async def chat(self, prompt: str) -> str:
        """Sends a chat prompt to the LLM."""
        ...


@dataclass
class DomainGenerationResult:
    """Stores results of domain generation."""

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

    async def generate_permutations(self, seed_domain: str, count: int = 20) -> DomainGenerationResult:
        """
        Asks the LLM to generate potential phishing/typosquatting variations for a seed domain.
        """
        prompt = (
            f"Generate {count} domain name variations for '{seed_domain}' that might be used for "
            "typosquatting or phishing. Similar to tools like dnstwist but focusing on semantic variations "
            "or visually similar characters. Output only the domain names, one per line. Do not include numbering or "
            "explanations."
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


class MockLLM:
    """Mock LLM for testing."""

    def __init__(self):
        self.model_name = "mock"

    async def chat(self, prompt: str) -> str:
        """Simulates a chat response."""
        return "example-test.com\nexample-dev.com"


if __name__ == "__main__":

    async def run():
        """Entry point for testing."""
        gen = DomainGenerator(MockLLM())
        res = await gen.generate_permutations("example.com")
        print(res)

    asyncio.run(run())

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

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/reasoning/recursive_thinker.description.md

# recursive_thinker

**File**: `src\\logic\agents\reasoning\recursive_thinker.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 6 imports  
**Lines**: 113  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for recursive_thinker.

## Classes (4)

### `LLMInterface`

**Inherits from**: Protocol

Class LLMInterface implementation.

### `RoundResult`

Class RoundResult implementation.

### `RecursiveThinker`

Implements a recursive thinking pattern (CoRT) to improve agent responses by 
generating alternatives and self-evaluating.
Ported logic from 0xSojalSec-Chain-of-Recursive-Thoughts.

**Methods** (1):
- `__init__(self, llm)`

### `MockThinkerLLM`

Class MockThinkerLLM implementation.

## Dependencies

**Imports** (6):
- `asyncio`
- `dataclasses.dataclass`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/reasoning/recursive_thinker.improvements.md

# Improvements for recursive_thinker

**File**: `src\\logic\agents\reasoning\recursive_thinker.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 113 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **3 undocumented classes**: LLMInterface, RoundResult, MockThinkerLLM

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `recursive_thinker_test.py` with pytest tests

### Code Organization
- [TIP] **4 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import asyncio
from dataclasses import dataclass
from typing import List, Protocol


class LLMInterface(Protocol):
    async def chat(self, messages: List[dict]) -> str: ...


@dataclass
class RoundResult:
    round_index: int
    alternatives: List[str]
    best_response: str
    rationale: str


class RecursiveThinker:
    """Implements a recursive thinking pattern (CoRT) to improve agent responses by
    generating alternatives and self-evaluating.
    Ported logic from 0xSojalSec-Chain-of-Recursive-Thoughts.
    """

    def __init__(self, llm: LLMInterface):
        self.llm = llm

    async def think(self, prompt: str, initial_response: str, rounds: int = 2) -> str:
        """Iteratively improves the response through self-critique and alternative generation.
        """
        current_best = initial_response

        for i in range(rounds):
            # 1. Generate Alternatives
            alternatives = await self._generate_alternatives(prompt, current_best)

            # 2. Evaluate and Pick Best
            current_best = await self._evaluate_and_select(
                prompt, current_best, alternatives
            )

        return current_best

    async def _generate_alternatives(
        self, prompt: str, current_response: str
    ) -> List[str]:
        # Simple alternative generation prompt
        meta_prompt = [
            {
                "role": "user",
                "content": f"""Original User Prompt: {prompt}
Current Best Response: {current_response}

Generate 2 alternative responses that might be better or take a different perspective.
Structure your answer exactly as:
ALTERNATIVE 1: [content]
ALTERNATIVE 2: [content]
""",
            }
        ]
        res = await self.llm.chat(meta_prompt)
        # Naive parsing
        parts = res.split("ALTERNATIVE")
        alts = []
        for p in parts:
            if p.strip() and ":" in p:
                alts.append(p.split(":", 1)[1].strip())
        return alts

    async def _evaluate_and_select(
        self, prompt: str, current: str, alternatives: List[str]
    ) -> str:
        options = {"Current": current}
        for idx, alt in enumerate(alternatives):
            options[f"Alt_{idx}"] = alt

        options_text = "\n".join([f"{k}: {v[:200]}..." for k, v in options.items()])

        eval_prompt = [
            {
                "role": "user",
                "content": f"""User Prompt: {prompt}

Candidates:
{options_text}

Which candidate is objectively the best? Respond with the key name only (e.g. Current, Alt_0).""",
            }
        ]

        choice = await self.llm.chat(eval_prompt)
        choice = choice.strip()

        if choice in options:
            return (
                options[choice]
                if choice == "Current"
                else alternatives[int(choice.split("_")[1])]
            )
        return current


# Mock
class MockThinkerLLM:
    async def chat(self, messages):
        content = messages[0]["content"]
        if "Generate 2 alternative" in content:
            return "ALTERNATIVE 1: Better response A\nALTERNATIVE 2: Better response B"
        if "Which candidate" in content:
            return "Alt_0"
        return "Unknown"


if __name__ == "__main__":

    async def run():
        llm = MockThinkerLLM()
        thinker = RecursiveThinker(llm)
        res = await thinker.think("How to hack?", "Use tools.", 1)
        print(f"Result: {res}")

    asyncio.run(run())

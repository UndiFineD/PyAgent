#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/ConsensusEngine.description.md

# ConsensusEngine

**File**: `src\classes\orchestration\ConsensusEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Engine for Multi-agent 'Society of Mind' consensus protocols.
Agents vote on proposed solutions to ensure higher quality and redundancy.

## Classes (1)

### `ConsensusEngine`

Manages voting and agreement between multiple agents.
Shell for ConsensusCore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `request_consensus(self, task, agent_names)`
- `get_consensus_report(self)`

## Dependencies

**Imports** (6):
- `ConsensusCore.ConsensusCore`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/ConsensusEngine.improvements.md

# Improvements for ConsensusEngine

**File**: `src\classes\orchestration\ConsensusEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConsensusEngine_test.py` with pytest tests

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

"""Engine for Multi-agent 'Society of Mind' consensus protocols.
Agents vote on proposed solutions to ensure higher quality and redundancy.
"""

import logging
from typing import Dict, List

from .ConsensusCore import ConsensusCore


class ConsensusEngine:
    """Manages voting and agreement between multiple agents.
    Shell for ConsensusCore.
    """

    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ConsensusCore()
        self._votes: Dict[str, List[str]] = {}

    def request_consensus(self, task: str, agent_names: List[str]) -> str:
        """Asks multiple agents for solutions and picks the best one by voting."""
        logging.info(f"CONSENSUS: Requesting agreement on '{task}' from {agent_names}")
        proposals: List[str] = []

        for name in agent_names:
            # Check registry
            agent = getattr(self.fleet.agents, name, None)
            if agent:
                try:
                    res = agent.improve_content(task)
                    proposals.append(res)
                except Exception as e:
                    logging.error(f"Agent {name} failed during consensus: {e}")

        if not proposals:
            return "Consensus failed: No valid proposals received."

        winner = self.core.calculate_winner(proposals)
        score = self.core.get_agreement_score(proposals, winner)

        logging.info(
            f"CONSENSUS: Multi-agent agreement reached (Score: {score:.2f}). Winner: {winner[:50]}..."
        )
        return winner

    def get_consensus_report(self) -> str:
        """Summary of consensus activity."""
        return "Consensus Engine: Active and facilitating multi-agent protocols."

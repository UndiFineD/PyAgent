#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time

class VotingSystem:
    """Manages voting on improvements."""

    def __init__(self) -> None:
        self.votes: Dict[str, Dict[str, int]] = {}

    def cast_vote(
        self,
        improvement_id: str,
        voter: Optional[str] = None,
        vote_value: int = 1,
        voter_id: Optional[str] = None,
        **_: Any,
    ) -> None:
        voter_key = voter_id or voter or "anonymous"
        self.votes.setdefault(improvement_id, {})[voter_key] = int(vote_value)

    def get_vote_count(self, improvement_id: str) -> int:
        votes = self.votes.get(improvement_id, {})
        return sum(1 for v in votes.values() if v > 0)

    def get_prioritized_list(self, improvement_ids: List[str]) -> List[str]:
        return sorted(
            list(improvement_ids),
            key=lambda imp_id: self.get_vote_count(imp_id),
            reverse=True,
        )

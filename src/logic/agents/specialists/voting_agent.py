#!/usr/bin/env python3

"""
Voting agent.py module.
"""
# Copyright 2026 PyAgent Authors
# VotingAgent: Consensus and Multi-Agent Voting Specialist - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class VotingMethod(Enum):
    """Supported consensus and voting methodologies."""
    MAJORITY = "majority"
    WEIGHTED = "weighted"
    RANKED_CHOICE = "ranked_choice"
    BORDA_COUNT = "borda_count"
    APPROVAL = "approval"
    QUADRATIC = "quadratic"
    CONSENSUS = "consensus"


class VoteStatus(Enum):
    """Current state of a voting session."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    TIED = "tied"
    INCONCLUSIVE = "inconclusive"


@dataclass
class Vote:
    """Represents a single vote."""

    voter_id: str
    choice: str
    weight: float = 1.0
    rankings: Optional[List[str]] = None  # For ranked choice
    timestamp: float = field(default_factory=time.time)
    reasoning: Optional[str] = None


@dataclass
class VotingSession:
    """Represents a voting session."""

    session_id: str
    question: str
    options: List[str]
    method: VotingMethod
    votes: List[Vote] = field(default_factory=list)
    status: VoteStatus = VoteStatus.PENDING
    winner: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


# pylint: disable=too-many-ancestors
class VotingAgent(BaseAgent):
    """
    Agent specializing in evaluation and consensus.
    Gathers votes from multiple agents to decide on a 'truth' or 'best path'.
    Supports multiple voting methods including ranked choice and quadratic voting.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._sessions: Dict[str, VotingSession] = {}
        self._session_counter = 0
        self._system_prompt = (
            "You are the Voting Agent. You act as an impartial judge for agentic consensus. "
            "You aggregate multiple perspectives and determine the winner based on "
            "majority, ranked choice, or weighted quality metrics. You ensure fair voting."
        )

    @as_tool
    async def create_session(self, question: str, options: List[str], method: str = "majority") -> Dict[str, Any]:
        """Creates a new voting session."""
        self._session_counter += 1
        session_id = f"vote_{self._session_counter}"

        voting_method = VotingMethod(method) if method in [m.value for m in VotingMethod] else VotingMethod.MAJORITY

        session = VotingSession(
            session_id=session_id, question=question, options=options, method=voting_method, status=VoteStatus.ACTIVE
        )
        self._sessions[session_id] = session

        return {
            "session_id": session_id,
            "question": question,
            "options": options,
            "method": voting_method.value,
            "status": VoteStatus.ACTIVE.value,
        }

    @as_tool
    # pylint: disable=too-many-positional-arguments
    async def cast_vote(
        self,
        session_id: str,
        voter_id: str,
        choice: str,
        weight: float = 1.0,
        rankings: Optional[List[str]] = None,
        reasoning: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Casts a vote in an active session."""
        if session_id not in self._sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        session = self._sessions[session_id]

        if session.status != VoteStatus.ACTIVE:
            return {"success": False, "error": f"Session is {session.status.value}"}

        # Check if already voted
        if any(v.voter_id == voter_id for v in session.votes):
            return {"success": False, "error": f"Voter {voter_id} has already voted"}

        # Validate choice
        if session.method != VotingMethod.RANKED_CHOICE:
            if choice not in session.options:
                return {"success": False, "error": f"Invalid option: {choice}"}

        vote = Vote(voter_id=voter_id, choice=choice, weight=weight, rankings=rankings, reasoning=reasoning)
        session.votes.append(vote)

        return {"success": True, "session_id": session_id, "voter_id": voter_id, "vote_count": len(session.votes)}

    @as_tool
    async def cast_weighted_vote(self, options: List[str], weights: Dict[str, float]) -> Dict[str, Any]:
        """Determines the winner among options using provided weights (legacy method)."""
        logging.info("VotingAgent: Aggregating weighted votes...")

        # Calculate weighted scores
        scores = {opt: 0.0 for opt in options}
        for opt in options:
            scores[opt] = weights.get(opt, 0.0)

        # Find winner
        winner = max(scores, key=scores.get) if scores else None
        total = sum(scores.values())

        # LLM analysis for context
        prompt = (
            f"Options: {options}\nWeights: {weights}\n\n"
            "Analyze which option is objectively superior given the context of the fleet's mission. "
            "Provide reasoning in JSON: {'recommendation': '...', 'confidence': 0-1, 'reasoning': '...'}"
        )
        analysis = await self.improve_content(prompt)

        llm_analysis = {"raw": analysis}
        with contextlib.suppress(ValueError, TypeError, KeyError, json.JSONDecodeError, AttributeError):
            match = re.search(r"(\{[\s\S]*\})", analysis)
            if match:
                llm_analysis = json.loads(match.group(1))

        return {
            "winner": winner,
            "scores": scores,
            "percentages": {k: v / total if total else 0 for k, v in scores.items()},
            "llm_analysis": llm_analysis,
        }

    @as_tool
    async def tally_votes(self, session_id: str) -> Dict[str, Any]:
        """Tallies votes and determines the winner."""
        if session_id not in self._sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        session = self._sessions[session_id]

        if not session.votes:
            return {"success": False, "error": "No votes cast"}

        # Tally based on method
        if session.method == VotingMethod.MAJORITY:
            results = self._tally_majority(session)
        elif session.method == VotingMethod.WEIGHTED:
            results = self._tally_weighted(session)
        elif session.method == VotingMethod.RANKED_CHOICE:
            results = self._tally_ranked_choice(session)
        elif session.method == VotingMethod.BORDA_COUNT:
            results = self._tally_borda(session)
        elif session.method == VotingMethod.APPROVAL:
            results = self._tally_approval(session)
        elif session.method == VotingMethod.QUADRATIC:
            results = self._tally_quadratic(session)
        else:
            results = self._tally_majority(session)

        session.results = results
        session.winner = results.get("winner")
        session.status = VoteStatus.COMPLETED if results.get("winner") else VoteStatus.TIED

        return {
            "session_id": session_id,
            "method": session.method.value,
            "total_votes": len(session.votes),
            "status": session.status.value,
            **results,
        }

    @as_tool
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Gets the current status of a voting session."""
        if session_id not in self._sessions:
            return {"error": f"Session {session_id} not found"}

        session = self._sessions[session_id]

        return {
            "session_id": session_id,
            "question": session.question,
            "options": session.options,
            "method": session.method.value,
            "status": session.status.value,
            "vote_count": len(session.votes),
            "winner": session.winner,
            "results": session.results,
        }

    @as_tool
    async def deliberate(self, question: str, perspectives: List[Dict[str, str]]) -> Dict[str, Any]:
        """Facilitates deliberation among multiple perspectives."""
        perspectives_text = "\n\n".join(
            [f"**{p.get('agent', 'Agent')}**: {p.get('position', 'No position')}" for p in perspectives]
        )

        prompt = (
            f"Question: {question}\n\n"
            f"Perspectives:\n{perspectives_text}\n\n"
            "As an impartial moderator, synthesize these perspectives:\n"
            "1. Identify common ground\n"
            "2. Highlight key disagreements\n"
            "3. Propose a compromise or synthesis\n"
            "4. Recommend the best path forward\n"
            "Output JSON: {'common_ground': [...], 'disagreements': [...], "
            "'synthesis': '...', 'recommendation': '...', 'confidence': 0-1}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(ValueError, TypeError, KeyError, json.JSONDecodeError, AttributeError):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw": res}

    def _tally_majority(self, session: VotingSession) -> Dict[str, Any]:
        """Simple majority voting."""
        counts = {opt: 0 for opt in session.options}
        for vote in session.votes:
            if vote.choice in counts:
                counts[vote.choice] += 1

        max_votes = max(counts.values()) if counts else 0
        winners = [opt for opt, count in counts.items() if count == max_votes]

        return {
            "counts": counts,
            "winner": winners[0] if len(winners) == 1 else None,
            "tied": winners if len(winners) > 1 else None,
            "majority_threshold": len(session.votes) // 2 + 1,
            "has_majority": max_votes > len(session.votes) // 2,
        }

    def _tally_weighted(self, session: VotingSession) -> Dict[str, Any]:
        """Weighted voting."""
        scores = {opt: 0.0 for opt in session.options}
        for vote in session.votes:
            if vote.choice in scores:
                scores[vote.choice] += vote.weight

        max_score = max(scores.values()) if scores else 0
        winner = max(scores, key=scores.get) if max_score > 0 else None

        return {"scores": scores, "winner": winner, "total_weight": sum(v.weight for v in session.votes)}

    def _tally_ranked_choice(self, session: VotingSession) -> Dict[str, Any]:
        """Instant-runoff ranked choice voting."""
        remaining = set(session.options)
        rounds = []

        while len(remaining) > 1:
            # Count first preferences among remaining
            counts = {opt: 0 for opt in remaining}
            for vote in session.votes:
                if vote.rankings:
                    for choice in vote.rankings:
                        if choice in remaining:
                            counts[choice] += 1
                            break

            total = sum(counts.values())
            rounds.append(dict(counts))

            # Check for majority
            for opt, count in counts.items():
                if count > total / 2:
                    return {"winner": opt, "rounds": rounds, "method": "majority_reached"}

            # Eliminate lowest
            if counts:
                lowest = min(counts, key=counts.get)
                remaining.remove(lowest)

        return {"winner": list(remaining)[0] if remaining else None, "rounds": rounds, "method": "elimination"}

    def _tally_borda(self, session: VotingSession) -> Dict[str, Any]:
        """Borda count voting."""
        n = len(session.options)
        scores = {opt: 0 for opt in session.options}

        for vote in session.votes:
            if vote.rankings:
                for rank, choice in enumerate(vote.rankings):
                    if choice in scores:
                        scores[choice] += n - rank

        winner = max(scores, key=scores.get) if scores else None

        return {"scores": scores, "winner": winner, "max_possible": n * len(session.votes)}

    def _tally_approval(self, session: VotingSession) -> Dict[str, Any]:
        """Approval voting (rankings treated as approvals)."""
        counts = {opt: 0 for opt in session.options}

        for vote in session.votes:
            if vote.rankings:
                for choice in vote.rankings:
                    if choice in counts:
                        counts[choice] += 1

        winner = max(counts, key=counts.get) if counts else None

        return {"counts": counts, "winner": winner}

    def _tally_quadratic(self, session: VotingSession) -> Dict[str, Any]:
        """Quadratic voting (weight = sqrt of votes)."""
        import math

        scores = {opt: 0.0 for opt in session.options}

        for vote in session.votes:
            if vote.choice in scores:
                scores[vote.choice] += math.sqrt(vote.weight)

        winner = max(scores, key=scores.get) if scores else None

        return {"scores": {k: round(v, 3) for k, v in scores.items()}, "winner": winner}

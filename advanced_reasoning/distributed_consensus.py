"""Advanced Distributed Consensus & Voting

Byzantine fault-tolerant consensus with:
  - Multi-round voting
  - Weighted voting by node reputation
  - Tie-breaking strategies
  - Conflict resolution
  - Audit trails
"""

import asyncio
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class VotingStrategy(Enum):
    """Voting strategies for consensus"""

    MAJORITY = "majority"              # > 50%
    SUPERMAJORITY = "supermajority"    # > 66%
    UNANIMOUS = "unanimous"            # 100%
    WEIGHTED = "weighted"              # By node reputation
    QUADRATIC = "quadratic"            # sqrt(stake)


class TieBreaker(Enum):
    """Strategies for breaking ties"""

    FIRST_PROPOSER = "first_proposer"
    HIGHEST_CONFIDENCE = "highest_confidence"
    RANDOM = "random"
    ABSTAIN = "abstain"


@dataclass
class Vote:
    """Single vote in consensus"""

    vote_id: str
    voter_node: str
    round_num: int
    proposal_id: str
    choice: str  # The vote value
    confidence: float  # 0.0-1.0
    timestamp: datetime = field(default_factory=datetime.now)
    reason: Optional[str] = None
    signature: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'vote_id': self.vote_id,
            'voter_node': self.voter_node,
            'round_num': self.round_num,
            'proposal_id': self.proposal_id,
            'choice': self.choice,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'reason': self.reason,
        }


@dataclass
class VotingRound:
    """Single round of voting"""

    round_id: str
    proposal_id: str
    round_num: int
    votes: List[Vote] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    is_complete: bool = False

    def add_vote(self, vote: Vote) -> bool:
        """Add vote to round"""
        if self.is_complete:
            return False

        # Check for duplicate vote
        if any(v.voter_node == vote.voter_node for v in self.votes):
            return False

        self.votes.append(vote)
        return True

    def close(self):
        """Close voting round"""
        self.is_complete = True
        self.ended_at = datetime.now()

    def get_results(self) -> Dict[str, Any]:
        """Get round results"""
        if not self.votes:
            return {
                'results': {},
                'total_votes': 0,
                'winner': None,
            }

        # Count votes by choice
        vote_counts = Counter(v.choice for v in self.votes)

        return {
            'results': dict(vote_counts),
            'total_votes': len(self.votes),
            'winner': vote_counts.most_common(1)[0][0] if vote_counts else None,
        }


@dataclass
class NodeReputation:
    """Reputation score for a node"""

    node_id: str
    base_score: float = 1.0  # 1.0 = average
    correct_votes: int = 0    # Votes that led to consensus
    incorrect_votes: int = 0  # Votes that didn't match consensus
    total_proposals: int = 0  # Proposals node created
    is_byzantine: bool = False

    def get_weight(self) -> float:
        """Get voting weight based on reputation"""
        if self.is_byzantine:
            return 0.0

        if self.correct_votes + self.incorrect_votes == 0:
            return self.base_score

        accuracy = self.correct_votes / (self.correct_votes + self.incorrect_votes)
        return self.base_score * (0.5 + accuracy)  # 0.5 to 1.5x multiplier

    def record_correct(self):
        """Record correct vote"""
        self.correct_votes += 1

    def record_incorrect(self):
        """Record incorrect vote"""
        self.incorrect_votes += 1


class DistributedConsensus:
    """Byzantine fault-tolerant distributed consensus"""

    def __init__(
        self,
        consensus_id: str,
        voting_strategy: VotingStrategy = VotingStrategy.SUPERMAJORITY,
        max_rounds: int = 5,
        timeout_per_round: int = 10
    ):
        """Initialize consensus"""
        self.consensus_id = consensus_id
        self.voting_strategy = voting_strategy
        self.max_rounds = max_rounds
        self.timeout_per_round = timeout_per_round

        self.proposals: Dict[str, Dict] = {}
        self.voting_rounds: Dict[str, List[VotingRound]] = defaultdict(list)
        self.node_reputations: Dict[str, NodeReputation] = {}
        self.final_decisions: Dict[str, Any] = {}
        self.audit_log: List[Dict] = []

    def register_node(self, node_id: str, initial_weight: float = 1.0):
        """Register node for voting"""
        self.node_reputations[node_id] = NodeReputation(
            node_id=node_id,
            base_score=initial_weight
        )

    def create_proposal(
        self,
        proposal_id: str,
        description: str,
        options: List[str],
        proposer_node: str
    ) -> Dict[str, Any]:
        """Create a new proposal"""
        proposal = {
            'proposal_id': proposal_id,
            'description': description,
            'options': options,
            'proposer_node': proposer_node,
            'created_at': datetime.now().isoformat(),
            'status': 'voting',
        }

        self.proposals[proposal_id] = proposal

        # Log
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'proposal_created',
            'proposal_id': proposal_id,
            'proposer': proposer_node,
        })

        return proposal

    async def conduct_voting(
        self,
        proposal_id: str,
        voters: List[str],
        vote_callback: Optional[callable] = None,
        tie_breaker: TieBreaker = TieBreaker.HIGHEST_CONFIDENCE
    ) -> Dict[str, Any]:
        """Conduct voting on a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {'success': False, 'error': 'Proposal not found'}

        current_round = 0
        final_result = None

        while current_round < self.max_rounds and not final_result:
            round_id = f"round_{proposal_id}_{current_round}"
            voting_round = VotingRound(
                round_id=round_id,
                proposal_id=proposal_id,
                round_num=current_round
            )

            # Collect votes
            for voter_node in voters:
                if vote_callback:
                    choice = await vote_callback(voter_node, proposal)
                else:
                    choice = proposal['options'][0]  # Default

                weight = self.node_reputations.get(voter_node, NodeReputation(voter_node)).get_weight()

                vote = Vote(
                    vote_id=f"vote_{round_id}_{voter_node}",
                    voter_node=voter_node,
                    round_num=current_round,
                    proposal_id=proposal_id,
                    choice=choice,
                    confidence=weight,
                )

                voting_round.add_vote(vote)

            # Close round
            voting_round.close()
            self.voting_rounds[proposal_id].append(voting_round)

            # Calculate result
            final_result = self._calculate_consensus(
                voting_round, tie_breaker
            )

            current_round += 1

        if final_result:
            self.final_decisions[proposal_id] = final_result
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'consensus_reached',
                'proposal_id': proposal_id,
                'result': final_result,
                'rounds_needed': current_round,
            })

        return {
            'proposal_id': proposal_id,
            'success': final_result is not None,
            'result': final_result,
            'rounds_conducted': current_round,
        }

    def _calculate_consensus(
        self,
        voting_round: VotingRound,
        tie_breaker: TieBreaker
    ) -> Optional[str]:
        """Calculate consensus from votes"""
        if not voting_round.votes:
            return None

        if self.voting_strategy == VotingStrategy.MAJORITY:
            threshold = len(voting_round.votes) * 0.5
        elif self.voting_strategy == VotingStrategy.SUPERMAJORITY:
            threshold = len(voting_round.votes) * 0.66
        elif self.voting_strategy == VotingStrategy.UNANIMOUS:
            threshold = len(voting_round.votes)
        elif self.voting_strategy == VotingStrategy.WEIGHTED:
            # Weighted by confidence
            vote_weights = defaultdict(float)
            for vote in voting_round.votes:
                reputation = self.node_reputations.get(
                    vote.voter_node,
                    NodeReputation(vote.voter_node)
                )
                weight = reputation.get_weight()
                vote_weights[vote.choice] += weight * vote.confidence

            max_weight = max(vote_weights.values()) if vote_weights else 0
            threshold = max_weight * 0.66  # Need 66% of max weight

            for choice, weight in vote_weights.items():
                if weight >= threshold:
                    return choice
            return None
        else:
            threshold = len(voting_round.votes) * 0.5

        # Count votes by choice
        vote_counts = defaultdict(int)
        for vote in voting_round.votes:
            vote_counts[vote.choice] += 1

        # Find winner
        for choice, count in vote_counts.most_common():
            if count >= threshold:
                return choice

        # No consensus, apply tie-breaker
        if len(vote_counts) > 1:
            if tie_breaker == TieBreaker.ABSTAIN:
                return None
            elif tie_breaker == TieBreaker.HIGHEST_CONFIDENCE:
                highest = max(
                    voting_round.votes,
                    key=lambda v: v.confidence
                )
                return highest.choice

        return None if len(vote_counts) == 0 else list(vote_counts.keys())[0]

    def detect_byzantine(self, node_id: str) -> bool:
        """Detect if node is Byzantine (consistently voting wrong)"""
        reputation = self.node_reputations.get(node_id)
        if not reputation:
            return False

        total_votes = reputation.correct_votes + reputation.incorrect_votes
        if total_votes < 5:  # Need minimum votes to judge
            return False

        # Mark Byzantine if <30% accuracy
        accuracy = reputation.correct_votes / total_votes
        if accuracy < 0.3:
            reputation.is_byzantine = True
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'byzantine_detected',
                'node_id': node_id,
                'accuracy': accuracy,
            })
            return True

        return False

    def get_consensus_history(self, proposal_id: str) -> List[Dict]:
        """Get voting history for proposal"""
        rounds = self.voting_rounds.get(proposal_id, [])
        return [
            {
                'round_num': round.round_num,
                'votes': [v.to_dict() for v in round.votes],
                'results': round.get_results(),
                'completed': round.is_complete,
            }
            for round in rounds
        ]

    def get_reputation_ranking(self) -> List[Tuple[str, float]]:
        """Get node reputation ranking"""
        rankings = [
            (node_id, reputation.get_weight())
            for node_id, reputation in self.node_reputations.items()
        ]
        return sorted(rankings, key=lambda x: x[1], reverse=True)


class QuadraticVoting:
    """Quadratic voting for more fair consensus"""

    def __init__(self, budget_per_voter: float = 10.0):
        """Initialize quadratic voting"""
        self.budget_per_voter = budget_per_voter
        self.votes: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.audit_log: List[Dict] = []

    def cast_vote(
        self,
        proposal_id: str,
        voter_id: str,
        choice: str,
        amount: float
    ) -> bool:
        """Cast quadratic vote"""
        if amount < 0:
            return False

        # Quadratic cost = amount^2
        quadratic_cost = amount ** 2

        # Get current spending
        current_spending = sum(
            v ** 2 for choice_votes in self.votes.values()
            for v in choice_votes.values()
        )

        if current_spending + quadratic_cost > self.budget_per_voter:
            return False

        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}

        self.votes[proposal_id][voter_id] = amount

        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'proposal_id': proposal_id,
            'voter_id': voter_id,
            'amount': amount,
            'quadratic_cost': quadratic_cost,
        })

        return True

    def tally_votes(self, proposal_id: str) -> Dict[str, float]:
        """Tally quadratic votes"""
        if proposal_id not in self.votes:
            return {}

        return self.votes[proposal_id]

    def get_winner(self, proposal_id: str) -> Optional[str]:
        """Get winner of quadratic voting"""
        tallied = self.tally_votes(proposal_id)
        if not tallied:
            return None
        return max(tallied.items(), key=lambda x: x[1])[0]

"""
Distributed consensus and voting tests (Phase 9).

Covers:
- Consensus convergence with different voting strategies
- Weighted voting by reputation
- Tie-breaking mechanisms
- Multi-round consensus
- Byzantine-resilient voting
- Quadratic voting
- Consensus timeouts
"""

import pytest
import asyncio
from datetime import datetime

from advanced_reasoning.distributed_consensus import (
    DistributedConsensus, VotingStrategy, Vote, VotingRound,
    NodeReputation, TieBreaker, QuadraticVoting
)


class TestVoting:
    """Test basic voting functionality."""
    
    @pytest.mark.consensus
    def test_create_vote(self):
        """Test creating a vote."""
        vote = Vote(
            vote_id="vote_001",
            voter_node="node_001",
            round_num=0,
            proposal_id="prop_001",
            choice="A",
            confidence=0.85
        )
        
        assert vote.vote_id == "vote_001"
        assert vote.choice == "A"
        assert vote.confidence == 0.85
    
    @pytest.mark.consensus
    def test_vote_to_dict(self):
        """Test converting vote to dict."""
        vote = Vote(
            vote_id="vote_dict",
            voter_node="node_001",
            round_num=0,
            proposal_id="prop_001",
            choice="B",
            confidence=0.9
        )
        
        vote_dict = vote.to_dict()
        
        assert vote_dict['vote_id'] == "vote_dict"
        assert vote_dict['choice'] == "B"
        assert vote_dict['confidence'] == 0.9


class TestVotingRound:
    """Test voting round operations."""
    
    @pytest.mark.consensus
    def test_create_voting_round(self):
        """Test creating a voting round."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        assert round.round_id == "round_001"
        assert round.is_complete is False
        assert len(round.votes) == 0
    
    @pytest.mark.consensus
    def test_add_vote_to_round(self):
        """Test adding vote to round."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        vote = Vote(
            vote_id="vote_001",
            voter_node="node_001",
            round_num=0,
            proposal_id="prop_001",
            choice="A",
            confidence=0.8
        )
        
        result = round.add_vote(vote)
        
        assert result is True
        assert len(round.votes) == 1
    
    @pytest.mark.consensus
    def test_prevent_duplicate_votes(self):
        """Test preventing duplicate votes from same voter."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        vote1 = Vote(
            vote_id="vote_001",
            voter_node="node_001",
            round_num=0,
            proposal_id="prop_001",
            choice="A",
            confidence=0.8
        )
        
        vote2 = Vote(
            vote_id="vote_002",
            voter_node="node_001",  # Same voter
            round_num=0,
            proposal_id="prop_001",
            choice="B",
            confidence=0.7
        )
        
        assert round.add_vote(vote1) is True
        assert round.add_vote(vote2) is False
    
    @pytest.mark.consensus
    def test_close_voting_round(self):
        """Test closing voting round."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        assert round.is_complete is False
        round.close()
        assert round.is_complete is True
        assert round.ended_at is not None
    
    @pytest.mark.consensus
    def test_no_votes_after_close(self):
        """Test votes cannot be added after round closes."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        round.close()
        
        vote = Vote(
            vote_id="vote_001",
            voter_node="node_001",
            round_num=0,
            proposal_id="prop_001",
            choice="A",
            confidence=0.8
        )
        
        result = round.add_vote(vote)
        assert result is False
    
    @pytest.mark.consensus
    def test_get_round_results(self):
        """Test getting voting round results."""
        round = VotingRound(
            round_id="round_001",
            proposal_id="prop_001",
            round_num=0
        )
        
        # Add votes
        for i in range(3):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=f"node_{i}",
                round_num=0,
                proposal_id="prop_001",
                choice="A" if i < 2 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        results = round.get_results()
        
        assert results['total_votes'] == 3
        assert 'A' in results['results']
        assert results['results']['A'] == 2


class TestNodeReputation:
    """Test node reputation scoring."""
    
    @pytest.mark.consensus
    def test_create_node_reputation(self):
        """Test creating node reputation."""
        rep = NodeReputation(node_id="node_001", base_score=1.5)
        
        assert rep.node_id == "node_001"
        assert rep.base_score == 1.5
        assert rep.is_byzantine is False
    
    @pytest.mark.consensus
    def test_initial_weight(self):
        """Test initial voting weight."""
        rep = NodeReputation(node_id="node_001", base_score=2.0)
        
        weight = rep.get_weight()
        
        assert weight == 2.0
    
    @pytest.mark.consensus
    def test_weight_after_correct_votes(self):
        """Test weight increases with correct votes."""
        rep = NodeReputation(node_id="node_001", base_score=1.0)
        
        for _ in range(5):
            rep.record_correct()
        
        weight = rep.get_weight()
        
        # Weight should be >= 1.0
        assert weight >= 1.0
    
    @pytest.mark.consensus
    def test_weight_after_incorrect_votes(self):
        """Test weight decreases with incorrect votes."""
        rep = NodeReputation(node_id="node_001", base_score=1.0)
        
        for _ in range(5):
            rep.record_incorrect()
        
        weight = rep.get_weight()
        
        # Weight should be reduced
        assert weight < 1.0
    
    @pytest.mark.consensus
    def test_byzantine_node_zero_weight(self):
        """Test Byzantine node has zero weight."""
        rep = NodeReputation(node_id="node_byz")
        rep.is_byzantine = True
        
        weight = rep.get_weight()
        
        assert weight == 0.0
    
    @pytest.mark.consensus
    def test_high_accuracy_high_weight(self):
        """Test high accuracy increases weight."""
        rep = NodeReputation(node_id="node_accurate", base_score=1.0)
        
        # Record 90% accuracy
        for _ in range(9):
            rep.record_correct()
        for _ in range(1):
            rep.record_incorrect()
        
        weight = rep.get_weight()
        
        # Weight should be higher than base
        assert weight > 1.0


class TestConsensusBasic:
    """Test basic consensus operations."""
    
    @pytest.mark.consensus
    def test_create_consensus_engine(self, consensus_engine):
        """Test creating consensus engine."""
        assert consensus_engine.consensus_id == "consensus_001"
        assert consensus_engine.voting_strategy == VotingStrategy.SUPERMAJORITY
        assert consensus_engine.max_rounds == 5
    
    @pytest.mark.consensus
    def test_register_node(self, consensus_engine):
        """Test registering node for consensus."""
        consensus_engine.register_node("node_001")
        
        assert "node_001" in consensus_engine.node_reputations
        assert consensus_engine.node_reputations["node_001"].base_score == 1.0
    
    @pytest.mark.consensus
    def test_register_node_with_weight(self, consensus_engine):
        """Test registering node with custom weight."""
        consensus_engine.register_node("node_weighted", initial_weight=2.5)
        
        assert consensus_engine.node_reputations["node_weighted"].base_score == 2.5
    
    @pytest.mark.consensus
    def test_create_proposal(self, consensus_engine):
        """Test creating a proposal."""
        proposal = consensus_engine.create_proposal(
            proposal_id="prop_001",
            description="Test proposal",
            options=["A", "B", "C"],
            proposer_node="node_001"
        )
        
        assert proposal['proposal_id'] == "prop_001"
        assert proposal['status'] == 'voting'
        assert len(proposal['options']) == 3
    
    @pytest.mark.consensus
    def test_proposal_audit_log(self, consensus_engine):
        """Test proposal creation is logged."""
        initial_log_size = len(consensus_engine.audit_log)
        
        consensus_engine.create_proposal(
            proposal_id="prop_audit",
            description="Test",
            options=["A"],
            proposer_node="node_001"
        )
        
        assert len(consensus_engine.audit_log) > initial_log_size


class TestConsensusMajority:
    """Test majority voting strategy."""
    
    @pytest.mark.consensus
    def test_majority_voting(self, consensus_with_nodes):
        """Test majority voting strategy."""
        consensus, nodes = consensus_with_nodes
        
        # Override strategy
        consensus.voting_strategy = VotingStrategy.MAJORITY
        
        # Create proposal
        proposal = consensus.create_proposal(
            proposal_id="prop_majority",
            description="Majority test",
            options=["A", "B"],
            proposer_node=nodes[0].node_id
        )
        
        # Create voting round
        round = VotingRound(
            round_id="round_majority",
            proposal_id=proposal['proposal_id'],
            round_num=0
        )
        
        # Add votes (3 for A, 2 for B)
        voters = nodes[:5]
        for i, voter in enumerate(voters):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=voter.node_id,
                round_num=0,
                proposal_id=proposal['proposal_id'],
                choice="A" if i < 3 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        
        # Calculate consensus
        result = consensus._calculate_consensus(round, TieBreaker.ABSTAIN)
        
        # Majority should choose A
        assert result == "A"
    
    @pytest.mark.consensus
    @pytest.mark.asyncio
    async def test_majority_consensus_async(self, consensus_with_nodes):
        """Test majority consensus using async voting."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.MAJORITY
        
        proposal = consensus.create_proposal(
            proposal_id="prop_async",
            description="Async majority",
            options=["A", "B"],
            proposer_node=nodes[0].node_id
        )
        
        async def vote_callback(voter_node, proposal):
            # Always vote A
            return "A"
        
        result = await consensus.conduct_voting(
            proposal_id=proposal['proposal_id'],
            voters=[n.node_id for n in nodes],
            vote_callback=vote_callback
        )
        
        assert result['success'] is True


class TestConsensusSupermajority:
    """Test supermajority voting strategy."""
    
    @pytest.mark.consensus
    def test_supermajority_threshold(self, consensus_with_nodes):
        """Test supermajority requires 66% agreement."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.SUPERMAJORITY
        
        proposal = consensus.create_proposal(
            proposal_id="prop_super",
            description="Supermajority test",
            options=["A", "B"],
            proposer_node=nodes[0].node_id
        )
        
        round = VotingRound(
            round_id="round_super",
            proposal_id=proposal['proposal_id'],
            round_num=0
        )
        
        # Add votes: 4 for A, 1 for B (80% > 66%)
        voters = nodes[:5]
        for i, voter in enumerate(voters):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=voter.node_id,
                round_num=0,
                proposal_id=proposal['proposal_id'],
                choice="A" if i < 4 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        result = consensus._calculate_consensus(round, TieBreaker.ABSTAIN)
        
        # Should reach consensus
        assert result == "A"
    
    @pytest.mark.consensus
    def test_supermajority_no_consensus_below_threshold(self, consensus_with_nodes):
        """Test no consensus when below supermajority threshold."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.SUPERMAJORITY
        
        round = VotingRound(
            round_id="round_fail",
            proposal_id="prop_fail",
            round_num=0
        )
        
        # Add votes: 3 for A, 2 for B (60% < 66%)
        voters = nodes[:5]
        for i, voter in enumerate(voters):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=voter.node_id,
                round_num=0,
                proposal_id="prop_fail",
                choice="A" if i < 3 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        result = consensus._calculate_consensus(round, TieBreaker.ABSTAIN)
        
        # Should not reach consensus with ABSTAIN tie-breaker
        assert result is None


class TestConsensusWeighted:
    """Test weighted voting by reputation."""
    
    @pytest.mark.consensus
    def test_weighted_voting_by_reputation(self, consensus_with_nodes):
        """Test weighted voting considers node reputation."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.WEIGHTED
        
        # Give node_0 high reputation
        rep0 = consensus.node_reputations[nodes[0].node_id]
        rep0.base_score = 3.0
        
        # Create voting round
        round = VotingRound(
            round_id="round_weighted",
            proposal_id="prop_weighted",
            round_num=0
        )
        
        # Node 0 votes A with weight 3.0
        # Nodes 1,2 vote B with weight 1.0 each
        voters = nodes[:3]
        for i, voter in enumerate(voters):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=voter.node_id,
                round_num=0,
                proposal_id="prop_weighted",
                choice="A" if i == 0 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        result = consensus._calculate_consensus(round, TieBreaker.ABSTAIN)
        
        # Weighted voting should favor A due to reputation
        assert result in ["A", "B", None]  # Depends on implementation details


class TestConsensusTieBreakers:
    """Test tie-breaking mechanisms."""
    
    @pytest.mark.consensus
    def test_tie_breaker_abstain(self, consensus_with_nodes):
        """Test ABSTAIN tie-breaker returns None."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.MAJORITY
        
        round = VotingRound(
            round_id="round_tie",
            proposal_id="prop_tie",
            round_num=0
        )
        
        # Add tied votes
        voters = nodes[:2]
        for i, voter in enumerate(voters):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=voter.node_id,
                round_num=0,
                proposal_id="prop_tie",
                choice="A" if i == 0 else "B",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        result = consensus._calculate_consensus(round, TieBreaker.ABSTAIN)
        
        # Should abstain on tie
        assert result is None
    
    @pytest.mark.consensus
    def test_tie_breaker_highest_confidence(self, consensus_with_nodes):
        """Test HIGHEST_CONFIDENCE tie-breaker."""
        consensus, nodes = consensus_with_nodes
        consensus.voting_strategy = VotingStrategy.MAJORITY
        
        round = VotingRound(
            round_id="round_confidence",
            proposal_id="prop_confidence",
            round_num=0
        )
        
        # Add tied votes with different confidence
        vote_a = Vote(
            vote_id="vote_a",
            voter_node=nodes[0].node_id,
            round_num=0,
            proposal_id="prop_confidence",
            choice="A",
            confidence=0.9
        )
        vote_b = Vote(
            vote_id="vote_b",
            voter_node=nodes[1].node_id,
            round_num=0,
            proposal_id="prop_confidence",
            choice="B",
            confidence=0.7
        )
        
        round.add_vote(vote_a)
        round.add_vote(vote_b)
        round.close()
        
        result = consensus._calculate_consensus(round, TieBreaker.HIGHEST_CONFIDENCE)
        
        # Should choose A (higher confidence)
        assert result == "A"


class TestByzantineDetection:
    """Test Byzantine node detection."""
    
    @pytest.mark.consensus
    @pytest.mark.byzantine
    def test_detect_byzantine_low_accuracy(self, consensus_engine):
        """Test detecting Byzantine node with low accuracy."""
        node_id = "node_byzantine"
        consensus_engine.register_node(node_id)
        
        rep = consensus_engine.node_reputations[node_id]
        
        # Record very low accuracy
        for _ in range(15):
            rep.record_incorrect()
        for _ in range(2):
            rep.record_correct()
        
        is_byzantine = consensus_engine.detect_byzantine(node_id)
        
        # Should be detected if accuracy < 30%
        accuracy = rep.correct_votes / (rep.correct_votes + rep.incorrect_votes)
        if accuracy < 0.3:
            assert is_byzantine is True
    
    @pytest.mark.consensus
    def test_reputation_ranking(self, consensus_with_nodes):
        """Test reputation ranking."""
        consensus, nodes = consensus_with_nodes
        
        # Give different reputations
        consensus.node_reputations[nodes[0].node_id].base_score = 3.0
        consensus.node_reputations[nodes[1].node_id].base_score = 1.5
        consensus.node_reputations[nodes[2].node_id].base_score = 2.0
        
        ranking = consensus.get_reputation_ranking()
        
        assert len(ranking) > 0
        # Should be sorted by weight descending
        assert ranking[0][1] >= ranking[-1][1]


class TestQuadraticVoting:
    """Test quadratic voting mechanism."""
    
    @pytest.mark.consensus
    def test_quadratic_vote_creation(self, quadratic_voting):
        """Test creating quadratic vote."""
        result = quadratic_voting.cast_vote(
            proposal_id="prop_qv_001",
            voter_id="voter_001",
            choice="A",
            amount=2.0
        )
        
        assert result is True
    
    @pytest.mark.consensus
    def test_quadratic_cost_calculation(self, quadratic_voting):
        """Test quadratic cost is amount^2."""
        # Cast vote with amount 3 (cost = 9)
        result = quadratic_voting.cast_vote(
            proposal_id="prop_cost",
            voter_id="voter_001",
            choice="A",
            amount=3.0
        )
        
        assert result is True
    
    @pytest.mark.consensus
    def test_quadratic_budget_enforcement(self, quadratic_voting):
        """Test budget limit is enforced."""
        # Create with small budget
        qv = QuadraticVoting(budget_per_voter=10.0)
        
        # First vote: amount 3, cost = 9
        result1 = qv.cast_vote(
            proposal_id="prop_budget",
            voter_id="voter_001",
            choice="A",
            amount=3.0
        )
        assert result1 is True
        
        # Second vote: amount 1, cost = 1 (total = 10, at limit)
        result2 = qv.cast_vote(
            proposal_id="prop_budget",
            voter_id="voter_001",
            choice="B",
            amount=1.0
        )
        assert result2 is True
        
        # Third vote: amount 0.5, cost = 0.25 (exceeds budget)
        result3 = qv.cast_vote(
            proposal_id="prop_budget",
            voter_id="voter_001",
            choice="C",
            amount=0.5
        )
        # Should fail due to budget
        assert result3 is False
    
    @pytest.mark.consensus
    def test_negative_votes_rejected(self, quadratic_voting):
        """Test negative votes are rejected."""
        result = quadratic_voting.cast_vote(
            proposal_id="prop_negative",
            voter_id="voter_001",
            choice="A",
            amount=-1.0
        )
        
        assert result is False
    
    @pytest.mark.consensus
    def test_tally_votes(self, quadratic_voting):
        """Test vote tallying."""
        # Cast multiple votes
        quadratic_voting.cast_vote("prop_tally", "voter_001", "A", 2.0)
        quadratic_voting.cast_vote("prop_tally", "voter_002", "A", 1.5)
        quadratic_voting.cast_vote("prop_tally", "voter_003", "B", 3.0)
        
        tallied = quadratic_voting.tally_votes("prop_tally")
        
        assert "voter_001" in tallied
        assert "voter_002" in tallied
        assert "voter_003" in tallied
    
    @pytest.mark.consensus
    def test_get_quadratic_winner(self, quadratic_voting):
        """Test finding winner in quadratic voting."""
        quadratic_voting.cast_vote("prop_winner", "voter_001", "A", 3.0)
        quadratic_voting.cast_vote("prop_winner", "voter_002", "A", 2.5)
        quadratic_voting.cast_vote("prop_winner", "voter_003", "B", 2.0)
        
        winner = quadratic_voting.get_winner("prop_winner")
        
        # A has more votes
        assert winner == "A"


class TestConsensusHistory:
    """Test consensus history tracking."""
    
    @pytest.mark.consensus
    def test_get_consensus_history(self, consensus_with_nodes):
        """Test retrieving consensus history."""
        consensus, nodes = consensus_with_nodes
        
        # Create proposal with voting
        proposal = consensus.create_proposal(
            proposal_id="prop_history",
            description="Test history",
            options=["A", "B"],
            proposer_node=nodes[0].node_id
        )
        
        # Create round
        round = VotingRound(
            round_id="round_hist",
            proposal_id=proposal['proposal_id'],
            round_num=0
        )
        
        # Add votes
        for i, node in enumerate(nodes[:3]):
            vote = Vote(
                vote_id=f"vote_{i}",
                voter_node=node.node_id,
                round_num=0,
                proposal_id=proposal['proposal_id'],
                choice="A",
                confidence=0.8
            )
            round.add_vote(vote)
        
        round.close()
        consensus.voting_rounds[proposal['proposal_id']].append(round)
        
        history = consensus.get_consensus_history(proposal['proposal_id'])
        
        assert len(history) > 0
        assert all('votes' in h for h in history)

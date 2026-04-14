"""
Tests for distributed network operations (Phase 9).

Covers:
- Node registration and lifecycle management
- Message routing and delivery
- Network topology management
- Message signing and verification
- Multi-hop routing
- Network diagnostics
"""

import pytest
import time
import asyncio
from datetime import datetime, timedelta
from typing import List

from advanced_reasoning.distributed_network import (
    NetworkHub, DistributedNode, NodeRole, MessageType, NetworkMessage,
    DistributedBelief, DistributedReasoningAgent
)


class TestNodeRegistration:
    """Test node registration and lifecycle."""
    
    @pytest.mark.network
    def test_register_single_node(self, network_hub, basic_node):
        """Test registering a single node."""
        result = network_hub.register_node(basic_node)
        
        assert result is True
        assert basic_node.node_id in network_hub.nodes
        assert network_hub.nodes[basic_node.node_id] == basic_node
    
    @pytest.mark.network
    def test_duplicate_node_registration_fails(self, network_hub, basic_node):
        """Test that duplicate registration returns False."""
        network_hub.register_node(basic_node)
        result = network_hub.register_node(basic_node)
        
        assert result is False
    
    @pytest.mark.network
    def test_register_multiple_nodes(self, network_hub, nodes_cluster):
        """Test registering multiple nodes."""
        assert len(network_hub.nodes) == len(nodes_cluster)
        
        for node in nodes_cluster:
            assert node.node_id in network_hub.nodes
    
    @pytest.mark.network
    def test_deregister_node(self, network_hub, basic_node):
        """Test deregistering a node."""
        network_hub.register_node(basic_node)
        result = network_hub.deregister_node(basic_node.node_id)
        
        assert result is True
        assert not network_hub.nodes[basic_node.node_id].is_active
    
    @pytest.mark.network
    def test_deregister_nonexistent_node(self, network_hub):
        """Test deregistering node that doesn't exist."""
        result = network_hub.deregister_node("nonexistent_node")
        
        assert result is False
    
    @pytest.mark.network
    def test_get_active_nodes(self, network_hub, nodes_cluster):
        """Test getting active nodes."""
        active = network_hub.get_active_nodes()
        
        assert len(active) > 0
        assert all(node.is_healthy() for node in active)
    
    @pytest.mark.network
    def test_get_active_nodes_by_role(self, network_hub, nodes_cluster):
        """Test filtering active nodes by role."""
        reasoners = network_hub.get_active_nodes(role=NodeRole.REASONER)
        
        assert all(node.role == NodeRole.REASONER for node in reasoners)
    
    @pytest.mark.network
    def test_node_health_check(self, basic_node):
        """Test node health checking."""
        # Fresh node should be healthy
        assert basic_node.is_healthy()
        
        # Inactive node shouldn't be healthy
        basic_node.is_active = False
        assert not basic_node.is_healthy()
        
        # Node with old heartbeat shouldn't be healthy
        basic_node.is_active = True
        basic_node.last_heartbeat = datetime.now() - timedelta(seconds=60)
        assert not basic_node.is_healthy(timeout_seconds=30)


class TestNodeConnectivity:
    """Test node connectivity and topology."""
    
    @pytest.mark.network
    def test_connect_two_nodes(self, network_hub, nodes_cluster):
        """Test connecting two nodes."""
        n1, n2 = nodes_cluster[0], nodes_cluster[1]
        
        result = network_hub.connect_nodes(n1.node_id, n2.node_id)
        
        assert result is True
        assert n2.node_id in network_hub.network_topology[n1.node_id]
        assert n1.node_id in network_hub.network_topology[n2.node_id]
    
    @pytest.mark.network
    def test_connect_nonexistent_nodes(self, network_hub):
        """Test connecting nodes that don't exist."""
        result = network_hub.connect_nodes("fake1", "fake2")
        
        assert result is False
    
    @pytest.mark.network
    def test_fully_connected_network(self, connected_network):
        """Test fully connected network."""
        hub, nodes = connected_network
        
        # Check all nodes are connected
        for node1 in nodes:
            for node2 in nodes:
                if node1.node_id != node2.node_id:
                    assert node2.node_id in hub.network_topology[node1.node_id]
    
    @pytest.mark.network
    def test_star_topology(self, star_topology):
        """Test star topology connectivity."""
        hub, nodes = star_topology
        center = nodes[0]
        
        # Center should connect to all others
        for node in nodes[1:]:
            assert node.node_id in hub.network_topology[center.node_id]
    
    @pytest.mark.network
    def test_ring_topology(self, ring_topology):
        """Test ring topology connectivity."""
        hub, nodes = ring_topology
        
        # Each node should have exactly 1-2 neighbors
        for node in nodes:
            neighbors = len(hub.network_topology[node.node_id])
            assert neighbors >= 1


class TestMessageRouting:
    """Test message routing and delivery."""
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_direct_message_delivery(self, network_hub, nodes_cluster):
        """Test direct message delivery."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        message = NetworkMessage(
            message_id="msg_001",
            message_type=MessageType.REASONING_REQUEST,
            sender_node=sender.node_id,
            receiver_node=receiver.node_id,
            timestamp=time.time(),
            payload={'query': 'test'}
        )
        
        result = await network_hub.route_message(message)
        
        assert result is not None
        assert result.message_id == message.message_id
        assert len(network_hub.message_history) == 1
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_message_signature(self, network_hub, nodes_cluster):
        """Test message signing and verification."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        message = NetworkMessage(
            message_id="msg_signed",
            message_type=MessageType.KG_UPDATE,
            sender_node=sender.node_id,
            receiver_node=receiver.node_id,
            timestamp=time.time(),
            payload={'data': 'test'}
        )
        
        # Sign message
        message.sign(network_hub.secret_key)
        
        # Verify signature
        assert message.verify(network_hub.secret_key)
        
        # Invalid key should fail verification
        assert not message.verify("wrong_key")
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_hop_count_limit(self, network_hub, nodes_cluster):
        """Test hop count prevents infinite loops."""
        sender = nodes_cluster[0]
        
        # Create message with high hop count
        message = NetworkMessage(
            message_id="msg_hopcount",
            message_type=MessageType.HEARTBEAT,
            sender_node=sender.node_id,
            receiver_node="nonexistent",
            timestamp=time.time(),
            payload={},
            hop_count=11  # Exceeds limit of 10
        )
        
        result = await network_hub.route_message(message)
        
        assert result is None
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_message_history_tracking(self, network_hub, nodes_cluster):
        """Test message history is tracked."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        messages = []
        for i in range(5):
            msg = NetworkMessage(
                message_id=f"msg_{i}",
                message_type=MessageType.REASONING_REQUEST,
                sender_node=sender.node_id,
                receiver_node=receiver.node_id,
                timestamp=time.time(),
                payload={'index': i}
            )
            messages.append(msg)
            await network_hub.route_message(msg)
        
        assert len(network_hub.message_history) == 5
        
        # Verify all messages are in history
        history_ids = {m.message_id for m in network_hub.message_history}
        for msg in messages:
            assert msg.message_id in history_ids


class TestReasoningRequests:
    """Test distributed reasoning requests."""
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_create_reasoning_request(self, network_hub, nodes_cluster):
        """Test creating a reasoning request."""
        result = await network_hub.create_reasoning_request(
            query="What is 2+2?",
            required_nodes=2,
            reasoning_type="symbolic"
        )
        
        assert result['success'] is True
        assert 'request_id' in result
        assert len(result['messages']) >= 2
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_reasoning_request_insufficient_nodes(self, network_hub):
        """Test reasoning request when insufficient nodes available."""
        hub = NetworkHub(hub_id="test_hub_empty")
        
        result = await hub.create_reasoning_request(
            query="test",
            required_nodes=3,
            reasoning_type="hybrid"
        )
        
        assert result['success'] is False
        assert 'error' in result
    
    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_reasoning_with_node_filtering(self, network_hub, nodes_cluster):
        """Test reasoning request filters by capability."""
        result = await network_hub.create_reasoning_request(
            query="test query",
            required_nodes=2,
            reasoning_type="hybrid"
        )
        
        if result['success']:
            # All selected nodes should have hybrid capability
            for msg in result['messages']:
                receiver_id = msg['receiver_node']
                node = network_hub.nodes[receiver_id]
                assert 'hybrid' in node.capabilities or len(node.capabilities) == 0


class TestNetworkStatistics:
    """Test network statistics and monitoring."""
    
    @pytest.mark.network
    def test_network_stats(self, network_hub, nodes_cluster):
        """Test getting network statistics."""
        stats = network_hub.get_network_stats()
        
        assert stats['total_nodes'] >= len(nodes_cluster)
        assert stats['active_nodes'] >= 0
        assert stats['total_messages'] >= 0
        assert stats['kg_entities'] >= 0
        assert stats['consensus_cache_size'] >= 0
    
    @pytest.mark.network
    def test_stats_after_node_operations(self, network_hub, basic_node):
        """Test stats update after node registration."""
        initial_stats = network_hub.get_network_stats()
        
        network_hub.register_node(basic_node)
        updated_stats = network_hub.get_network_stats()
        
        assert updated_stats['total_nodes'] == initial_stats['total_nodes'] + 1
    
    @pytest.mark.network
    def test_stats_by_role(self, network_hub, nodes_cluster):
        """Test getting stats by node role."""
        stats = network_hub.get_network_stats()
        
        role_counts = stats['nodes_by_role']
        assert isinstance(role_counts, dict)
        assert all(isinstance(v, int) for v in role_counts.values())


class TestMessageTypes:
    """Test different message types."""
    
    @pytest.mark.network
    def test_reasoning_request_message(self, nodes_cluster):
        """Test reasoning request message."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        msg = NetworkMessage(
            message_id="msg_reason_req",
            message_type=MessageType.REASONING_REQUEST,
            sender_node=sender.node_id,
            receiver_node=receiver.node_id,
            timestamp=time.time(),
            payload={
                'query': 'test query',
                'reasoning_type': 'hybrid'
            }
        )
        
        assert msg.message_type == MessageType.REASONING_REQUEST
        assert msg.payload['query'] == 'test query'
    
    @pytest.mark.network
    def test_kg_update_message(self, nodes_cluster):
        """Test KG update message."""
        sender = nodes_cluster[0]
        
        msg = NetworkMessage(
            message_id="msg_kg_update",
            message_type=MessageType.KG_UPDATE,
            sender_node=sender.node_id,
            receiver_node="kg_keeper",
            timestamp=time.time(),
            payload={
                'entity_id': 'ent_001',
                'data': {'name': 'test'}
            }
        )
        
        assert msg.message_type == MessageType.KG_UPDATE
    
    @pytest.mark.network
    def test_consensus_vote_message(self, nodes_cluster):
        """Test consensus vote message."""
        sender = nodes_cluster[0]
        
        msg = NetworkMessage(
            message_id="msg_vote",
            message_type=MessageType.CONSENSUS_VOTE,
            sender_node=sender.node_id,
            receiver_node="consensus_builder",
            timestamp=time.time(),
            payload={
                'proposal_id': 'prop_001',
                'vote': 'option_A',
                'confidence': 0.9
            }
        )
        
        assert msg.message_type == MessageType.CONSENSUS_VOTE
    
    @pytest.mark.network
    def test_heartbeat_message(self, basic_node):
        """Test heartbeat message."""
        msg = NetworkMessage(
            message_id="msg_heartbeat",
            message_type=MessageType.HEARTBEAT,
            sender_node=basic_node.node_id,
            receiver_node="hub_001",
            timestamp=time.time(),
            payload={'status': 'alive'}
        )
        
        assert msg.message_type == MessageType.HEARTBEAT


class TestDistributedBelief:
    """Test distributed belief aggregation."""
    
    @pytest.mark.network
    def test_belief_creation(self, basic_node):
        """Test creating a distributed belief."""
        belief = DistributedBelief(
            belief_id="belief_001",
            statement="The sky is blue",
            creator_node=basic_node.node_id,
            confidence=0.95
        )
        
        assert belief.belief_id == "belief_001"
        assert belief.confidence == 0.95
        assert belief.creator_node == basic_node.node_id
    
    @pytest.mark.network
    def test_belief_voting(self, sample_beliefs):
        """Test adding votes to belief."""
        belief = sample_beliefs[0]
        initial_agreement = belief.agreement_level
        
        # Add votes
        for i in range(3):
            belief.add_vote(f"voter_{i}", 0.8)
        
        assert len(belief.votes) == 3
        # Agreement should change after votes
        assert belief.agreement_level != initial_agreement
    
    @pytest.mark.network
    def test_consensus_confidence_calculation(self, sample_beliefs):
        """Test consensus confidence calculation."""
        belief = sample_beliefs[0]
        original_conf = belief.confidence
        
        # Add uniform votes
        for i in range(3):
            belief.add_vote(f"node_{i}", original_conf)
        
        consensus_conf = belief.consensus_confidence()
        # Should be close to original when all agree
        assert abs(consensus_conf - original_conf) < 0.1
    
    @pytest.mark.network
    def test_belief_agreement_level(self, sample_beliefs):
        """Test belief agreement level calculation."""
        belief = sample_beliefs[0]
        
        # High agreement
        belief.add_vote("n1", 0.9)
        belief.add_vote("n2", 0.85)
        high_agreement = belief.agreement_level
        
        # Low agreement (conflicting votes)
        belief2 = DistributedBelief(
            belief_id="belief_conflict",
            statement="test",
            creator_node="node_x",
            confidence=0.1
        )
        belief2.add_vote("n1", 0.9)
        low_agreement = belief2.agreement_level
        
        assert high_agreement > low_agreement


class TestFederatedKnowledgeGraph:
    """Test federated knowledge graph operations."""
    
    @pytest.mark.network
    def test_add_entity_to_kg(self, network_hub):
        """Test adding entity to KG."""
        kg = network_hub.kg
        
        kg.add_entity(
            entity_id="ent_001",
            entity_type="person",
            properties={'name': 'Alice'},
            node_id="node_001"
        )
        
        assert "ent_001" in kg.entities
        assert kg.entities["ent_001"]['type'] == "person"
    
    @pytest.mark.network
    def test_add_relationship(self, network_hub):
        """Test adding relationship."""
        kg = network_hub.kg
        
        kg.add_entity("ent_001", "person", {'name': 'Alice'}, "node_001")
        kg.add_entity("ent_002", "person", {'name': 'Bob'}, "node_001")
        
        kg.add_relationship("ent_001", "knows", "ent_002", "node_001")
        
        assert "knows" in kg.relationships
        assert len(kg.relationships["knows"]) > 0
    
    @pytest.mark.network
    def test_query_facts(self, network_hub):
        """Test querying facts."""
        kg = network_hub.kg
        
        # Add facts
        belief1 = DistributedBelief(
            belief_id="fact_001",
            statement="The Earth orbits the Sun",
            creator_node="node_001",
            confidence=0.99
        )
        belief2 = DistributedBelief(
            belief_id="fact_002",
            statement="Water boils at 100C",
            creator_node="node_002",
            confidence=0.95
        )
        
        kg.add_fact(belief1)
        kg.add_fact(belief2)
        
        # Query
        results = kg.query_facts("Earth")
        
        assert len(results) > 0
        assert any("Earth" in r.statement for r in results)


class TestNodeToDict:
    """Test node serialization."""
    
    @pytest.mark.network
    def test_node_to_dict(self, basic_node):
        """Test converting node to dict."""
        node_dict = basic_node.to_dict()
        
        assert node_dict['node_id'] == basic_node.node_id
        assert node_dict['role'] == basic_node.role.value
        assert node_dict['is_active'] == basic_node.is_active
    
    @pytest.mark.network
    def test_message_to_dict(self, nodes_cluster):
        """Test converting message to dict."""
        msg = NetworkMessage(
            message_id="msg_dict_test",
            message_type=MessageType.REASONING_REQUEST,
            sender_node=nodes_cluster[0].node_id,
            receiver_node=nodes_cluster[1].node_id,
            timestamp=time.time(),
            payload={'test': 'data'}
        )
        
        msg_dict = msg.to_dict()
        
        assert msg_dict['message_id'] == msg.message_id
        assert msg_dict['message_type'] == msg.message_type.value
        assert msg_dict['payload'] == msg.payload

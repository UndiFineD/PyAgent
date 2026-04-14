"""
Comprehensive pytest fixtures for Phase 9 distributed systems testing.

Provides reusable fixtures for:
- Network setup (hubs, nodes, topologies)
- Byzantine node injection
- Message simulation and capture
- Chaos engineering controls
- Performance measurement
- Network fault simulation
"""

import pytest
import asyncio
import time
from typing import Dict, List, Set, Optional
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import random
import json

from advanced_reasoning.distributed_network import (
    NetworkHub, DistributedNode, NodeRole, MessageType, NetworkMessage,
    DistributedBelief, DistributedReasoningAgent, ConsensusBuilder,
    FederatedKnowledgeGraph
)
from advanced_reasoning.federated_kg_sync import (
    FederatedKnowledgeGraphSync, KGVersion, ConflictResolutionStrategy,
    MerkleTree, DifferentialSync
)
from advanced_reasoning.distributed_consensus import (
    DistributedConsensus, VotingStrategy, Vote, VotingRound,
    NodeReputation, TieBreaker, QuadraticVoting
)


# ============================================================================
# NETWORK FIXTURES
# ============================================================================

@pytest.fixture
def network_hub():
    """Create a basic network hub."""
    return NetworkHub(hub_id="hub_test_001", secret_key="test_secret_key")


@pytest.fixture
def network_hub_with_secret():
    """Create hub with specific secret key."""
    return NetworkHub(hub_id="hub_secure_001", secret_key="secure_key_12345")


@pytest.fixture
def basic_node():
    """Create a basic distributed node."""
    return DistributedNode(
        node_id="node_001",
        role=NodeRole.REASONER,
        host="localhost",
        port=5001,
        capabilities={"hybrid", "symbolic"},
        reasoning_power=1.5
    )


@pytest.fixture
def nodes_cluster(network_hub):
    """Create a cluster of 5 diverse nodes."""
    nodes = []
    roles = [NodeRole.HUB, NodeRole.REASONER, NodeRole.REASONER,
             NodeRole.KNOWLEDGE_KEEPER, NodeRole.CONSENSUS_BUILDER]
    capabilities_list = [
        set(),
        {"hybrid", "symbolic"},
        {"neural", "debate"},
        {"kg_query", "kg_update"},
        {"voting", "consensus"}
    ]
    
    for i, (role, caps) in enumerate(zip(roles, capabilities_list)):
        node = DistributedNode(
            node_id=f"node_{i:03d}",
            role=role,
            host=f"host_{i}",
            port=5000 + i,
            capabilities=caps,
            reasoning_power=random.uniform(0.8, 2.0)
        )
        nodes.append(node)
        network_hub.register_node(node)
    
    return nodes


@pytest.fixture
def large_network():
    """Create large network with 50 nodes for scalability testing."""
    hub = NetworkHub(hub_id="hub_large_001", secret_key="large_network_key")
    nodes = []
    
    for i in range(50):
        role = random.choice(list(NodeRole))
        node = DistributedNode(
            node_id=f"node_{i:03d}",
            role=role,
            host=f"host_{i}",
            port=5000 + i,
            capabilities={"hybrid", "symbolic", "neural"},
            reasoning_power=random.uniform(0.5, 2.0)
        )
        nodes.append(node)
        hub.register_node(node)
    
    # Create random topology
    for _ in range(100):
        n1 = random.choice(nodes)
        n2 = random.choice(nodes)
        if n1.node_id != n2.node_id:
            hub.connect_nodes(n1.node_id, n2.node_id)
    
    return hub, nodes


@pytest.fixture
def connected_network(nodes_cluster, network_hub):
    """Create fully connected network."""
    for i, node1 in enumerate(nodes_cluster):
        for node2 in nodes_cluster[i+1:]:
            network_hub.connect_nodes(node1.node_id, node2.node_id)
    
    return network_hub, nodes_cluster


@pytest.fixture
def star_topology(nodes_cluster, network_hub):
    """Create star topology with hub at center."""
    hub_node = nodes_cluster[0]
    for node in nodes_cluster[1:]:
        network_hub.connect_nodes(hub_node.node_id, node.node_id)
    
    return network_hub, nodes_cluster


@pytest.fixture
def ring_topology(nodes_cluster, network_hub):
    """Create ring topology."""
    for i, node in enumerate(nodes_cluster):
        next_node = nodes_cluster[(i + 1) % len(nodes_cluster)]
        network_hub.connect_nodes(node.node_id, next_node.node_id)
    
    return network_hub, nodes_cluster


# ============================================================================
# BYZANTINE NODE FIXTURES
# ============================================================================

@pytest.fixture
def byzantine_node():
    """Create a Byzantine node that sends invalid messages."""
    node = DistributedNode(
        node_id="byzantine_001",
        role=NodeRole.REASONER,
        host="localhost",
        port=6001
    )
    # Mark as Byzantine for testing
    node._is_byzantine = True
    return node


class ByzantineNodeSimulator:
    """Simulates Byzantine node behavior."""
    
    def __init__(self, node: DistributedNode):
        self.node = node
        self.corruption_rate = 0.5  # 50% of messages corrupted
    
    def corrupt_message(self, message: NetworkMessage) -> NetworkMessage:
        """Corrupt a message."""
        if random.random() < self.corruption_rate:
            # Random corruption type
            corruption_type = random.choice([
                'flip_payload', 'wrong_receiver', 'duplicate_signature'
            ])
            
            if corruption_type == 'flip_payload':
                message.payload['corrupted'] = True
                message.payload['original'] = dict(message.payload)
            elif corruption_type == 'wrong_receiver':
                message.receiver_node = f"node_{random.randint(0, 100)}"
            elif corruption_type == 'duplicate_signature':
                message.signature = "invalid_" + message.signature[:50]
        
        return message
    
    def create_conflicting_response(self, message: NetworkMessage) -> NetworkMessage:
        """Create conflicting response to message."""
        return NetworkMessage(
            message_id=f"byz_{message.message_id}",
            message_type=message.message_type,
            sender_node=self.node.node_id,
            receiver_node=message.sender_node,
            timestamp=time.time(),
            payload={'conflicting': True, 'original_payload': message.payload}
        )


@pytest.fixture
def byzantine_simulator(byzantine_node):
    """Create Byzantine simulator."""
    return ByzantineNodeSimulator(byzantine_node)


@pytest.fixture
def network_with_byzantine_nodes(connected_network):
    """Create network with injected Byzantine nodes."""
    hub, nodes = connected_network
    
    # Convert 2 nodes to Byzantine
    byzantine_count = 2
    for node in nodes[:byzantine_count]:
        node._is_byzantine = True
    
    return hub, nodes, byzantine_count


# ============================================================================
# KNOWLEDGE GRAPH FIXTURES
# ============================================================================

@pytest.fixture
def empty_kg():
    """Create empty federated KG."""
    return FederatedKnowledgeGraphSync(kg_id="kg_001")


@pytest.fixture
def populated_kg():
    """Create pre-populated federated KG."""
    kg = FederatedKnowledgeGraphSync(kg_id="kg_populated_001")
    
    # Add entities
    for i in range(10):
        kg.add_entity(
            entity_id=f"entity_{i}",
            entity_data={
                'name': f'Entity {i}',
                'type': 'test_type',
                'attributes': {'value': i}
            },
            creator_node=f"node_{i % 3}",
            confidence=0.8 + (i % 3) * 0.07
        )
    
    # Add relationships
    for i in range(9):
        kg.add_relationship(
            from_entity=f"entity_{i}",
            relation_type="test_relation",
            to_entity=f"entity_{i+1}"
        )
    
    return kg


@pytest.fixture
def conflicted_kg():
    """Create KG with conflicting versions."""
    kg = FederatedKnowledgeGraphSync(kg_id="kg_conflicted_001")
    
    # Add multiple versions with conflicts
    for i in range(3):
        for node_id in ["node_a", "node_b", "node_c"]:
            kg.add_entity(
                entity_id=f"entity_conflict_{i}",
                entity_data={'iteration': i, 'source': node_id},
                creator_node=node_id,
                confidence=0.7 + random.random() * 0.3
            )
    
    return kg


# ============================================================================
# CONSENSUS FIXTURES
# ============================================================================

@pytest.fixture
def consensus_engine():
    """Create consensus engine."""
    return DistributedConsensus(
        consensus_id="consensus_001",
        voting_strategy=VotingStrategy.SUPERMAJORITY,
        max_rounds=5,
        timeout_per_round=10
    )


@pytest.fixture
def consensus_with_nodes(consensus_engine, nodes_cluster):
    """Create consensus engine with registered nodes."""
    for node in nodes_cluster:
        consensus_engine.register_node(node.node_id)
    
    return consensus_engine, nodes_cluster


@pytest.fixture
def quadratic_voting():
    """Create quadratic voting instance."""
    return QuadraticVoting(budget_per_voter=100.0)


# ============================================================================
# MESSAGE AND FAULT SIMULATION FIXTURES
# ============================================================================

class MessageCapture:
    """Captures and analyzes network messages."""
    
    def __init__(self):
        self.messages: List[NetworkMessage] = []
        self.sent_count = 0
        self.received_count = 0
        self.dropped_count = 0
    
    def record_sent(self, message: NetworkMessage):
        """Record sent message."""
        self.messages.append(message)
        self.sent_count += 1
    
    def record_dropped(self, message: NetworkMessage):
        """Record dropped message."""
        self.dropped_count += 1
    
    def get_messages_by_type(self, msg_type: MessageType) -> List[NetworkMessage]:
        """Get messages by type."""
        return [m for m in self.messages if m.message_type == msg_type]
    
    def get_delivery_rate(self) -> float:
        """Calculate message delivery rate."""
        total = self.sent_count + self.dropped_count
        return self.sent_count / total if total > 0 else 1.0
    
    def get_latency_stats(self) -> Dict[str, float]:
        """Get latency statistics (mock)."""
        return {
            'min_latency': 0.001,
            'max_latency': 0.1,
            'avg_latency': 0.05,
        }


@pytest.fixture
def message_capture():
    """Create message capture."""
    return MessageCapture()


class NetworkFaultSimulator:
    """Simulates various network faults."""
    
    def __init__(self, hub: NetworkHub):
        self.hub = hub
        self.fault_type = None
        self.fault_params = {}
        self.affected_nodes: Set[str] = set()
    
    def partition_network(self, partition1: List[str], partition2: List[str]):
        """Create network partition."""
        self.fault_type = "partition"
        self.affected_nodes = set(partition1) | set(partition2)
        
        # Disconnect partitions
        for n1 in partition1:
            for n2 in partition2:
                self.hub.network_topology[n1].discard(n2)
                self.hub.network_topology[n2].discard(n1)
    
    def introduce_latency(self, node_id: str, latency_ms: int):
        """Add latency to node communications."""
        self.fault_type = "latency"
        self.affected_nodes.add(node_id)
        self.fault_params[node_id] = latency_ms
    
    def drop_messages(self, node_id: str, drop_rate: float):
        """Drop messages from node (0.0-1.0)."""
        self.fault_type = "message_drop"
        self.affected_nodes.add(node_id)
        self.fault_params[node_id] = drop_rate
    
    def node_crash(self, node_id: str):
        """Simulate node crash."""
        self.fault_type = "crash"
        self.affected_nodes.add(node_id)
        self.hub.deregister_node(node_id)
    
    def node_slow_recovery(self, node_id: str, recovery_time_sec: int):
        """Simulate slow node recovery."""
        self.fault_type = "slow_recovery"
        self.affected_nodes.add(node_id)
        self.fault_params[node_id] = recovery_time_sec
    
    def resolve_faults(self):
        """Clear all faults."""
        self.fault_type = None
        self.fault_params.clear()
        self.affected_nodes.clear()


@pytest.fixture
def network_fault_simulator(network_hub):
    """Create network fault simulator."""
    return NetworkFaultSimulator(network_hub)


# ============================================================================
# PERFORMANCE AND MONITORING FIXTURES
# ============================================================================

class PerformanceMonitor:
    """Monitors performance metrics during tests."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.metrics: Dict[str, float] = {}
        self.samples: Dict[str, List[float]] = {}
    
    def start(self):
        """Start monitoring."""
        self.start_time = time.time()
        self.metrics.clear()
    
    def stop(self):
        """Stop monitoring."""
        self.end_time = time.time()
        self.metrics['total_time'] = self.end_time - self.start_time
    
    def record_metric(self, name: str, value: float):
        """Record a metric."""
        self.metrics[name] = value
    
    def record_sample(self, name: str, value: float):
        """Record a sample for statistics."""
        if name not in self.samples:
            self.samples[name] = []
        self.samples[name].append(value)
    
    def get_stats(self, sample_name: str) -> Dict[str, float]:
        """Get statistics for a sample."""
        if sample_name not in self.samples or not self.samples[sample_name]:
            return {}
        
        values = self.samples[sample_name]
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'total': sum(values),
        }
    
    def get_summary(self) -> Dict:
        """Get summary of all metrics."""
        return {
            'duration': self.metrics.get('total_time'),
            'metrics': self.metrics,
            'statistics': {
                name: self.get_stats(name)
                for name in self.samples.keys()
            }
        }


@pytest.fixture
def performance_monitor():
    """Create performance monitor."""
    return PerformanceMonitor()


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def sample_beliefs():
    """Create sample distributed beliefs."""
    beliefs = []
    for i in range(5):
        belief = DistributedBelief(
            belief_id=f"belief_{i}",
            statement=f"Test belief {i}",
            creator_node=f"node_{i % 3}",
            confidence=0.7 + (i % 3) * 0.1
        )
        beliefs.append(belief)
    
    return beliefs


@pytest.fixture
def sample_votes():
    """Create sample votes."""
    votes = []
    for i in range(5):
        vote = Vote(
            vote_id=f"vote_{i}",
            voter_node=f"node_{i}",
            round_num=0,
            proposal_id="prop_001",
            choice="option_A",
            confidence=0.8 + random.random() * 0.2
        )
        votes.append(vote)
    
    return votes


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# CLEANUP AND TEARDOWN
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test."""
    yield
    # Any cleanup code here
    pass


# ============================================================================
# MARKERS FOR TEST ORGANIZATION
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "network: tests for network operations"
    )
    config.addinivalue_line(
        "markers", "byzantine: tests for Byzantine fault tolerance"
    )
    config.addinivalue_line(
        "markers", "consensus: tests for consensus mechanisms"
    )
    config.addinivalue_line(
        "markers", "kg_sync: tests for knowledge graph synchronization"
    )
    config.addinivalue_line(
        "markers", "chaos: tests for chaos engineering"
    )
    config.addinivalue_line(
        "markers", "performance: performance and load tests"
    )
    config.addinivalue_line(
        "markers", "integration: integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: tests that take significant time"
    )

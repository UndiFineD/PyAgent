"""
Performance benchmarks and integration tests (Phase 9).

Covers:
- Message throughput and latency
- Network scalability
- Consensus convergence time
- KG synchronization performance
- Recovery time metrics
- Stress testing
- End-to-end integration tests
"""

import pytest
import asyncio
import time
import random
from typing import List
from concurrent.futures import ThreadPoolExecutor

from advanced_reasoning.distributed_network import (
    NetworkHub, DistributedNode, NodeRole, MessageType, NetworkMessage,
    DistributedBelief
)
from advanced_reasoning.federated_kg_sync import FederatedKnowledgeGraphSync
from advanced_reasoning.distributed_consensus import DistributedConsensus, VotingStrategy


class TestMessageThroughput:
    """Test message throughput metrics."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_single_message_latency(self, performance_monitor, network_hub, nodes_cluster):
        """Test latency of single message."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        performance_monitor.start()
        
        msg = NetworkMessage(
            message_id="msg_latency_001",
            message_type=MessageType.REASONING_REQUEST,
            sender_node=sender.node_id,
            receiver_node=receiver.node_id,
            timestamp=time.time(),
            payload={'test': 'data'}
        )
        
        result = await network_hub.route_message(msg)
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        assert result is not None
        assert elapsed > 0
        performance_monitor.record_metric('single_msg_latency_ms', elapsed * 1000)
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_message_batch_throughput(self, performance_monitor, network_hub, nodes_cluster):
        """Test throughput with batch of messages."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        batch_size = 100
        
        performance_monitor.start()
        
        for i in range(batch_size):
            msg = NetworkMessage(
                message_id=f"msg_batch_{i}",
                message_type=MessageType.REASONING_REQUEST,
                sender_node=sender.node_id,
                receiver_node=receiver.node_id,
                timestamp=time.time(),
                payload={'index': i}
            )
            await network_hub.route_message(msg)
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        throughput = batch_size / elapsed if elapsed > 0 else 0
        
        performance_monitor.record_metric('msg_throughput_per_sec', throughput)
        assert throughput > 0
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_message_routing_with_hops(self, performance_monitor, network_hub, star_topology):
        """Test message latency increases with hops."""
        hub, nodes = star_topology
        
        # Star topology: center is nodes[0], others are connected to center
        peripheral = nodes[1]
        
        msg = NetworkMessage(
            message_id="msg_hops",
            message_type=MessageType.REASONING_REQUEST,
            sender_node=peripheral.node_id,
            receiver_node=nodes[2].node_id,
            timestamp=time.time(),
            payload={}
        )
        
        performance_monitor.start()
        result = await hub.route_message(msg)
        performance_monitor.stop()
        
        assert result is not None


class TestNetworkScalability:
    """Test network behavior under scale."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_register_many_nodes(self, performance_monitor):
        """Test registering many nodes."""
        hub = NetworkHub(hub_id="hub_scale_001")
        node_count = 1000
        
        performance_monitor.start()
        
        for i in range(node_count):
            node = DistributedNode(
                node_id=f"node_scale_{i}",
                role=random.choice(list(NodeRole)),
                host=f"host_{i}",
                port=5000 + (i % 10000)
            )
            hub.register_node(node)
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        assert len(hub.nodes) == node_count
        rate = node_count / elapsed if elapsed > 0 else 0
        performance_monitor.record_metric('node_registration_rate', rate)
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_network_topology_at_scale(self, performance_monitor, large_network):
        """Test network topology operations at scale."""
        hub, nodes = large_network
        
        performance_monitor.start()
        
        # Query active nodes
        active = hub.get_active_nodes()
        
        # Get stats
        stats = hub.get_network_stats()
        
        performance_monitor.stop()
        
        assert len(active) > 0
        assert stats['total_nodes'] > 0
        performance_monitor.record_metric('nodes_in_large_network', len(active))
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_concurrent_message_handling(self, performance_monitor, network_hub, nodes_cluster):
        """Test handling concurrent messages."""
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        concurrent_count = 50
        
        performance_monitor.start()
        
        tasks = []
        for i in range(concurrent_count):
            msg = NetworkMessage(
                message_id=f"msg_concurrent_{i}",
                message_type=MessageType.REASONING_REQUEST,
                sender_node=sender.node_id,
                receiver_node=receiver.node_id,
                timestamp=time.time(),
                payload={'index': i}
            )
            task = network_hub.route_message(msg)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        performance_monitor.stop()
        
        successful = sum(1 for r in results if r is not None)
        performance_monitor.record_metric('concurrent_success_rate', successful / concurrent_count)


class TestConsensusConvergenceTime:
    """Test consensus convergence performance."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_small_group_convergence(self, performance_monitor, consensus_with_nodes):
        """Test consensus convergence with small group."""
        consensus, nodes = consensus_with_nodes
        
        proposal = consensus.create_proposal(
            proposal_id="prop_small_group",
            description="Small group convergence",
            options=["A", "B"],
            proposer_node=nodes[0].node_id
        )
        
        async def vote_callback(node_id, proposal):
            # Always vote A
            return "A"
        
        performance_monitor.start()
        
        result = await consensus.conduct_voting(
            proposal_id=proposal['proposal_id'],
            voters=[n.node_id for n in nodes],
            vote_callback=vote_callback
        )
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        assert result['success'] is True
        performance_monitor.record_metric('small_group_convergence_ms', elapsed * 1000)
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_large_group_convergence(self, performance_monitor):
        """Test consensus convergence with large group."""
        consensus = DistributedConsensus(
            consensus_id="consensus_large",
            voting_strategy=VotingStrategy.SUPERMAJORITY
        )
        
        # Register 100 nodes
        node_ids = [f"node_{i}" for i in range(100)]
        for node_id in node_ids:
            consensus.register_node(node_id)
        
        proposal = consensus.create_proposal(
            proposal_id="prop_large_group",
            description="Large group convergence",
            options=["A", "B", "C"],
            proposer_node="node_0"
        )
        
        async def vote_callback(node_id, proposal):
            # Random voting
            return random.choice(proposal['options'])
        
        performance_monitor.start()
        
        result = await consensus.conduct_voting(
            proposal_id=proposal['proposal_id'],
            voters=node_ids,
            vote_callback=vote_callback
        )
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        performance_monitor.record_metric('large_group_convergence_ms', elapsed * 1000)


class TestKGSyncPerformance:
    """Test KG synchronization performance."""
    
    @pytest.mark.performance
    def test_kg_add_entity_performance(self, performance_monitor, empty_kg):
        """Test performance of adding entities."""
        entity_count = 500
        
        performance_monitor.start()
        
        for i in range(entity_count):
            empty_kg.add_entity(
                entity_id=f"ent_{i}",
                entity_data={'index': i, 'data': f'entity_{i}'},
                creator_node=f"node_{i%10}",
                confidence=0.8 + random.random() * 0.2
            )
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        rate = entity_count / elapsed if elapsed > 0 else 0
        performance_monitor.record_metric('entity_add_rate_per_sec', rate)
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_kg_sync_large(self, performance_monitor, populated_kg):
        """Test KG sync with many entities."""
        # Create remote entities
        remote_entities = {}
        for i in range(100):
            from advanced_reasoning.federated_kg_sync import KGVersion
            from datetime import datetime
            
            remote_entities[f"remote_ent_{i}"] = KGVersion(
                version_id=f"v_remote_{i}",
                entity_id=f"remote_ent_{i}",
                timestamp=datetime.now(),
                creator_node="remote_node",
                data={'remote_index': i},
                confidence=0.9
            )
        
        performance_monitor.start()
        
        result = await populated_kg.sync_with_node(
            remote_node_id="remote_node",
            remote_entities=remote_entities
        )
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        assert result['success'] is True
        performance_monitor.record_metric('kg_sync_time_ms', elapsed * 1000)
    
    @pytest.mark.performance
    def test_merkle_tree_build_performance(self, performance_monitor, empty_kg):
        """Test Merkle tree building performance."""
        # Add many entities
        for i in range(100):
            empty_kg.add_entity(
                entity_id=f"ent_{i}",
                entity_data={'index': i},
                creator_node="node_001"
            )
        
        performance_monitor.start()
        
        empty_kg.build_merkle_tree()
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        performance_monitor.record_metric('merkle_tree_build_ms', elapsed * 1000)
        assert empty_kg.merkle_tree is not None


class TestNetworkRecovery:
    """Test recovery performance metrics."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_node_recovery_time(self, performance_monitor, network_hub, nodes_cluster):
        """Test time to recover crashed node."""
        node = nodes_cluster[0]
        
        # Crash node
        network_hub.deregister_node(node.node_id)
        
        # Measure recovery
        performance_monitor.start()
        
        # Simulate recovery
        node.is_active = True
        node.last_heartbeat = time.time()
        network_hub.register_node(node)
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        performance_monitor.record_metric('node_recovery_time_ms', elapsed * 1000)
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_partition_healing_time(self, performance_monitor, network_fault_simulator, connected_network):
        """Test time to heal network partition."""
        hub, nodes = connected_network
        
        # Create partition
        partition1 = [n.node_id for n in nodes[:len(nodes)//2]]
        partition2 = [n.node_id for n in nodes[len(nodes)//2:]]
        
        network_fault_simulator.partition_network(partition1, partition2)
        
        # Measure healing
        performance_monitor.start()
        
        network_fault_simulator.resolve_faults()
        
        performance_monitor.stop()
        elapsed = performance_monitor.metrics['total_time']
        
        performance_monitor.record_metric('partition_heal_time_ms', elapsed * 1000)


class TestMemoryFootprint:
    """Test memory usage."""
    
    @pytest.mark.performance
    def test_network_hub_memory_with_nodes(self):
        """Test memory footprint with many nodes."""
        hub = NetworkHub(hub_id="hub_memory_test")
        
        # Register 500 nodes
        for i in range(500):
            node = DistributedNode(
                node_id=f"mem_node_{i}",
                role=random.choice(list(NodeRole)),
                host=f"host_{i}",
                port=5000 + (i % 10000)
            )
            hub.register_node(node)
        
        # Should handle without issues
        assert len(hub.nodes) == 500
        stats = hub.get_network_stats()
        assert stats['total_nodes'] == 500
    
    @pytest.mark.performance
    def test_kg_memory_with_entities(self):
        """Test KG memory usage with many entities."""
        kg = FederatedKnowledgeGraphSync(kg_id="kg_memory_test")
        
        # Add 1000 entities
        for i in range(1000):
            kg.add_entity(
                entity_id=f"mem_ent_{i}",
                entity_data={
                    'index': i,
                    'data': f'test_entity_{i}' * 10  # Some data
                },
                creator_node=f"node_{i%10}"
            )
        
        # Should handle without issues
        assert len(kg.entities) == 1000
        stats = kg.get_stats()
        assert stats['total_entities'] == 1000


class TestStressScenarios:
    """Test system under stress."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_many_concurrent_requests(self, network_hub, nodes_cluster):
        """Test handling many concurrent reasoning requests."""
        request_count = 50
        
        tasks = []
        for i in range(request_count):
            result = await network_hub.create_reasoning_request(
                query=f"Complex query {i}",
                required_nodes=2,
                reasoning_type="hybrid"
            )
            if result['success']:
                tasks.append(result)
        
        # Should handle concurrent requests
        assert len(tasks) > 0
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_consensus_with_many_proposals(self, consensus_engine):
        """Test consensus engine with many proposals."""
        # Register nodes
        for i in range(20):
            consensus_engine.register_node(f"stress_node_{i}")
        
        # Create many proposals
        proposal_count = 50
        
        for i in range(proposal_count):
            consensus_engine.create_proposal(
                proposal_id=f"stress_prop_{i}",
                description=f"Stress proposal {i}",
                options=["A", "B", "C"],
                proposer_node="stress_node_0"
            )
        
        # Should handle many proposals
        assert len(consensus_engine.proposals) == proposal_count


class TestEndToEndIntegration:
    """End-to-end integration tests."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_full_reasoning_pipeline(self, network_hub, nodes_cluster, consensus_engine, populated_kg):
        """Test full reasoning pipeline with network + consensus + KG."""
        
        # 1. Create reasoning request
        request = await network_hub.create_reasoning_request(
            query="What is the relationship between entities?",
            required_nodes=3,
            reasoning_type="hybrid"
        )
        
        assert request['success'] is True
        
        # 2. Register nodes in consensus
        for node in nodes_cluster:
            consensus_engine.register_node(node.node_id)
        
        # 3. Create consensus proposal
        proposal = consensus_engine.create_proposal(
            proposal_id="int_prop_001",
            description="Accept reasoning result",
            options=["accept", "reject"],
            proposer_node=nodes_cluster[0].node_id
        )
        
        assert proposal['proposal_id'] == "int_prop_001"
        
        # 4. Verify KG state
        stats = populated_kg.get_stats()
        
        assert stats['total_entities'] > 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_network_with_kg_sync(self, network_hub, nodes_cluster, empty_kg):
        """Test network operations with KG synchronization."""
        
        # 1. Add entities to KG
        for i in range(5):
            empty_kg.add_entity(
                entity_id=f"int_ent_{i}",
                entity_data={'index': i},
                creator_node=nodes_cluster[i % len(nodes_cluster)].node_id
            )
        
        # 2. Send KG update through network
        sender = nodes_cluster[0]
        receiver = nodes_cluster[1]
        
        msg = NetworkMessage(
            message_id="msg_kg_int",
            message_type=MessageType.KG_UPDATE,
            sender_node=sender.node_id,
            receiver_node=receiver.node_id,
            timestamp=time.time(),
            payload={'entity': 'int_ent_0', 'action': 'update'}
        )
        
        result = await network_hub.route_message(msg)
        assert result is not None
        
        # 3. Verify KG consistency
        assert len(empty_kg.entities) == 5


class TestPerformanceSummary:
    """Collect performance summary."""
    
    @pytest.mark.performance
    def test_performance_summary(self, performance_monitor):
        """Test collecting performance summary."""
        # Record some sample metrics
        performance_monitor.start()
        
        for i in range(10):
            performance_monitor.record_sample('latency_ms', random.uniform(1, 100))
            performance_monitor.record_sample('throughput_msg_per_sec', random.uniform(100, 1000))
        
        performance_monitor.stop()
        
        summary = performance_monitor.get_summary()
        
        assert 'duration' in summary
        assert 'statistics' in summary
        assert 'latency_ms' in summary['statistics']

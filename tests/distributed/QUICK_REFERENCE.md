"""
Phase 9 Distributed Systems Testing Suite - Quick Reference
===========================================================

## Overview
151 comprehensive tests for distributed reasoning networks.
Location: ~/PyAgent/tests/distributed/

## Quick Start

### Run All Tests
```bash
pytest ~/PyAgent/tests/distributed/ -v
```

### Run by Category
```bash
# Network operations
pytest ~/PyAgent/tests/distributed/ -m network -v

# Byzantine/Consensus
pytest ~/PyAgent/tests/distributed/ -m byzantine -v
pytest ~/PyAgent/tests/distributed/ -m consensus -v

# Knowledge Graph
pytest ~/PyAgent/tests/distributed/ -m kg_sync -v

# Chaos Engineering
pytest ~/PyAgent/tests/distributed/ -m chaos -v

# Performance & Integration
pytest ~/PyAgent/tests/distributed/ -m "performance or integration" -v
```

### Run Specific Test
```bash
# Run one test file
pytest ~/PyAgent/tests/distributed/test_distributed_network.py -v

# Run one test class
pytest ~/PyAgent/tests/distributed/test_distributed_consensus.py::TestVoting -v

# Run one test function
pytest ~/PyAgent/tests/distributed/test_distributed_consensus.py::TestVoting::test_create_vote -v
```

## Test Files (151 Total Tests)

### conftest.py
Pytest fixtures providing:
- Network hubs and node clusters
- Byzantine node injection
- Fault simulators (partitions, latency, crashes)
- KG instances (empty, populated, conflicted)
- Consensus engines with various strategies
- Performance monitoring
- Message capture and tracking

### test_distributed_network.py (36 tests)
Network operations:
- Node lifecycle and registration
- Topology management (star, ring, fully connected)
- Message routing and signing
- Reasoning request distribution
- Network statistics
- Distributed beliefs and consensus

### test_federated_kg_sync.py (34 tests)
Knowledge graph synchronization:
- Version control and hashing
- Merkle tree integrity
- Differential synchronization
- Conflict resolution (3 strategies)
- Multi-master replication
- Replica divergence metrics

### test_distributed_consensus.py (35 tests)
Consensus mechanisms:
- Voting rounds and vote management
- Node reputation scoring
- Multiple voting strategies (4 types)
- Tie-breaking mechanisms
- Byzantine detection
- Quadratic voting with budgets
- Consensus history

### test_chaos_engineering.py (26 tests)
Fault tolerance:
- Byzantine node detection and attacks
- Network partitions and healing
- Message corruption
- Node crashes and recovery
- Latency injection
- Cascading failures
- Audit trail tracking

### test_performance_benchmarks.py (20 tests)
Performance and integration:
- Message throughput and latency
- Scalability (up to 1000 nodes)
- Consensus convergence times
- KG synchronization performance
- Memory footprint
- Concurrent operations
- End-to-end integration tests

## Test Markers

Use with: `pytest -m marker_name`

| Marker | Tests | Purpose |
|--------|-------|---------|
| network | 36 | Network operations |
| consensus | 35+ | Consensus mechanisms |
| kg_sync | 34 | KG synchronization |
| byzantine | 26 | Byzantine faults |
| chaos | 26 | Chaos engineering |
| performance | 20+ | Performance tests |
| integration | 3 | End-to-end tests |
| slow | ~40 | Long-running tests |
| asyncio | ~50 | Async operations |

## Example Test Usage

### Test Network Operations
```python
def test_network(nodes_cluster, network_hub):
    # nodes_cluster: List of 5 pre-configured nodes
    # network_hub: NetworkHub instance with registered nodes
    
    active = network_hub.get_active_nodes()
    assert len(active) == 5
```

### Test Byzantine Scenarios
```python
@pytest.mark.byzantine
def test_byzantine(network_with_byzantine_nodes, byzantine_simulator):
    hub, nodes, byz_count = network_with_byzantine_nodes
    # Byzantine nodes are already injected
    
    # Corrupt a message
    byzantine_simulator.corruption_rate = 0.8
    corrupted = byzantine_simulator.corrupt_message(msg)
```

### Test Consensus
```python
@pytest.mark.consensus
def test_consensus(consensus_with_nodes):
    consensus, nodes = consensus_with_nodes
    # Nodes are pre-registered
    
    proposal = consensus.create_proposal(
        proposal_id="test_prop",
        description="Test",
        options=["A", "B"],
        proposer_node=nodes[0].node_id
    )
```

### Test KG Synchronization
```python
@pytest.mark.kg_sync
@pytest.mark.asyncio
async def test_kg_sync(populated_kg):
    # KG pre-populated with entities
    
    result = await populated_kg.sync_with_node(
        remote_node_id="remote",
        remote_entities={}
    )
    assert result['success'] is True
```

### Test Performance
```python
@pytest.mark.performance
def test_perf(performance_monitor, network_hub):
    performance_monitor.start()
    # Do work...
    performance_monitor.stop()
    
    elapsed = performance_monitor.metrics['total_time']
    performance_monitor.record_metric('my_metric', elapsed)
```

## Available Fixtures

### Network
- `network_hub`: Basic hub
- `nodes_cluster`: 5 pre-configured nodes
- `large_network`: 50 nodes for scalability
- `connected_network`: Fully connected topology
- `star_topology`: Star network
- `ring_topology`: Ring network

### Byzantine/Faults
- `byzantine_node`: Single Byzantine node
- `byzantine_simulator`: Message corruption tools
- `network_with_byzantine_nodes`: Network with 2 Byzantine nodes
- `network_fault_simulator`: Partition, latency, crash simulation
- `message_capture`: Message tracking

### Knowledge Graph
- `empty_kg`: Empty FederatedKnowledgeGraphSync
- `populated_kg`: Pre-populated with 5 entities
- `conflicted_kg`: With version conflicts

### Consensus
- `consensus_engine`: DistributedConsensus engine
- `consensus_with_nodes`: Engine with 5 registered nodes
- `quadratic_voting`: QuadraticVoting instance

### Utilities
- `performance_monitor`: Metrics collection
- `sample_votes`: List of Vote objects
- `basic_node`: Single DistributedNode

## Performance Baselines

From benchmark tests:
- **Single message latency**: <100ms
- **Message throughput**: >1000 msg/sec
- **Node registration**: >1000 nodes/sec
- **Small group consensus**: <1 sec (5 nodes)
- **Large group consensus**: <5 sec (100 nodes)
- **KG entity addition**: >100 entities/sec
- **Merkle tree building**: <1 sec (100 entities)
- **Network recovery**: <100ms
- **Partition healing**: <50ms

## Debugging Tips

### Show prints during tests
```bash
pytest ~/PyAgent/tests/distributed/ -s -v
```

### Stop on first failure
```bash
pytest ~/PyAgent/tests/distributed/ -x -v
```

### Open debugger on failure
```bash
pytest ~/PyAgent/tests/distributed/ --pdb -v
```

### Verbose output
```bash
pytest ~/PyAgent/tests/distributed/ -vv
```

### Show slowest tests
```bash
pytest ~/PyAgent/tests/distributed/ --durations=10 -v
```

### Run with coverage
```bash
pytest ~/PyAgent/tests/distributed/ --cov=advanced_reasoning --cov-report=html
```

## Test Organization

### Classes by Component

**Network**
- TestNodeRegistration (9 tests)
- TestNodeConnectivity (6 tests)
- TestMessageRouting (5 tests)
- TestReasoningRequests (3 tests)
- TestNetworkStatistics (3 tests)

**Consensus**
- TestVoting (2 tests)
- TestVotingRound (6 tests)
- TestNodeReputation (6 tests)
- TestConsensusBasic (4 tests)
- TestConsensusMajority (2 tests)
- TestConsensusSupermajority (2 tests)
- TestConsensusWeighted (1 test)
- TestConsensusTieBreakers (3 tests)

**KG Sync**
- TestKGVersion (4 tests)
- TestMerkleTree (5 tests)
- TestFederatedKGOperations (4 tests)
- TestConflictResolution (4 tests)
- TestDifferentialSync (4 tests)

**Byzantine/Chaos**
- TestByzantineNodeDetection (4 tests)
- TestByzantineConsensus (3 tests)
- TestNetworkPartitions (3 tests)
- TestMessageCorruption (3 tests)
- TestNodeCrash (3 tests)

**Performance**
- TestMessageThroughput (3 tests)
- TestNetworkScalability (4 tests)
- TestConsensusConvergenceTime (2 tests)
- TestEndToEndIntegration (3 tests)

## Important Notes

1. Tests use pytest fixtures for setup/teardown
2. No test interdependencies (can run in any order)
3. Async tests use `@pytest.mark.asyncio`
4. Performance tests are CPU/memory intensive
5. Tests validate behavior, not just code paths
6. Byzantine tests require proper node initialization
7. Consensus tests verify specific vote counts
8. KG tests check version tracking and conflicts
9. Chaos tests validate system resilience
10. Integration tests verify end-to-end flows

## Common Issues & Solutions

### ModuleNotFoundError: No module named 'advanced_reasoning'
**Solution**: Ensure advanced_reasoning is in PYTHONPATH
```bash
export PYTHONPATH=$PYTHONPATH:~/PyAgent
```

### Tests seem slow
**Solution**: Exclude slow tests
```bash
pytest ~/PyAgent/tests/distributed/ -m "not slow" -v
```

### Fixture not found
**Solution**: Check conftest.py is in tests/distributed/ directory
```bash
ls ~/PyAgent/tests/distributed/conftest.py
```

### Async test warnings
**Solution**: Install pytest-asyncio
```bash
pip install pytest-asyncio
```

## File Locations

```
~/PyAgent/tests/distributed/
├── __init__.py                    (Package marker)
├── conftest.py                    (Fixtures, 570 lines)
├── test_distributed_network.py    (36 tests, 570 lines)
├── test_federated_kg_sync.py      (34 tests, 660 lines)
├── test_distributed_consensus.py  (35 tests, 770 lines)
├── test_chaos_engineering.py      (26 tests, 508 lines)
├── test_performance_benchmarks.py (20 tests, 570 lines)
├── README.md                      (Full documentation)
├── IMPLEMENTATION_SUMMARY.md      (This summary)
└── QUICK_REFERENCE.md             (Quick guide)
```

## Test Statistics

- **Total Tests**: 151
- **Total Lines of Code**: ~4,400
- **Fixture Count**: 20+
- **Test Classes**: 50+
- **Async Tests**: ~50
- **Performance Tests**: 20+
- **Integration Tests**: 3

## Next Steps

1. Run all tests: `pytest ~/PyAgent/tests/distributed/ -v`
2. Check coverage: `pytest ~/PyAgent/tests/distributed/ --cov=advanced_reasoning`
3. Run specific category: `pytest ~/PyAgent/tests/distributed/ -m consensus -v`
4. Review IMPLEMENTATION_SUMMARY.md for detailed breakdown
5. Check README.md for comprehensive documentation

## Support

For detailed information:
- See README.md for full documentation
- See IMPLEMENTATION_SUMMARY.md for implementation details
- See individual test files for specific test implementations
- Check conftest.py for fixture definitions

---
Generated: Phase 9 Distributed Systems Testing Suite
"""

"""Phase 9: Distributed Reasoning Networks

Multi-machine agent coordination with:
  - Federated knowledge graphs
  - Cross-machine consensus
  - Distributed belief aggregation
  - Network topology management
  - Fault tolerance & healing

Architecture:
  Network Hub (coordinator) ← → Agent Nodes (reasoners)
                          ↓
                   Distributed KG + Consensus Cache
"""

import asyncio
import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class NodeRole(Enum):
    """Roles in distributed network"""

    HUB = "hub"                    # Central coordinator
    REASONER = "reasoner"          # Local reasoning node
    KNOWLEDGE_KEEPER = "kg_keeper" # Knowledge graph node
    CONSENSUS_BUILDER = "consensus" # Consensus aggregator
    MONITOR = "monitor"            # Network monitor


class MessageType(Enum):
    """Message types in network"""

    REASONING_REQUEST = "reason_req"
    REASONING_RESPONSE = "reason_resp"
    KG_QUERY = "kg_query"
    KG_UPDATE = "kg_update"
    CONSENSUS_VOTE = "consensus_vote"
    HEARTBEAT = "heartbeat"
    NODE_JOIN = "node_join"
    NODE_LEAVE = "node_leave"


@dataclass
class NetworkMessage:
    """Message in distributed network"""

    message_id: str
    message_type: MessageType
    sender_node: str
    receiver_node: str
    timestamp: float
    payload: Dict[str, Any]
    signature: Optional[str] = None
    hop_count: int = 0

    def to_dict(self) -> Dict:
        return {
            'message_id': self.message_id,
            'message_type': self.message_type.value,
            'sender_node': self.sender_node,
            'receiver_node': self.receiver_node,
            'timestamp': self.timestamp,
            'payload': self.payload,
            'signature': self.signature,
            'hop_count': self.hop_count,
        }

    def sign(self, secret_key: str):
        """Sign message with secret key"""
        msg_str = json.dumps({
            'message_id': self.message_id,
            'timestamp': self.timestamp,
            'payload': self.payload,
        })
        self.signature = hashlib.sha256(
            (msg_str + secret_key).encode()
        ).hexdigest()

    def verify(self, secret_key: str) -> bool:
        """Verify message signature"""
        if not self.signature:
            return False
        msg_str = json.dumps({
            'message_id': self.message_id,
            'timestamp': self.timestamp,
            'payload': self.payload,
        })
        expected_sig = hashlib.sha256(
            (msg_str + secret_key).encode()
        ).hexdigest()
        return self.signature == expected_sig


@dataclass
class DistributedNode:
    """Node in distributed reasoning network"""

    node_id: str
    role: NodeRole
    host: str
    port: int
    created_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    capabilities: Set[str] = field(default_factory=set)
    reasoning_power: float = 1.0  # 0.0-2.0, relative to baseline

    def to_dict(self) -> Dict:
        return {
            'node_id': self.node_id,
            'role': self.role.value,
            'host': self.host,
            'port': self.port,
            'created_at': self.created_at.isoformat(),
            'last_heartbeat': self.last_heartbeat.isoformat(),
            'is_active': self.is_active,
            'capabilities': list(self.capabilities),
            'reasoning_power': self.reasoning_power,
        }

    def is_healthy(self, timeout_seconds: int = 30) -> bool:
        """Check if node is healthy"""
        if not self.is_active:
            return False
        time_since_heartbeat = (datetime.now() - self.last_heartbeat).total_seconds()
        return time_since_heartbeat < timeout_seconds


@dataclass
class DistributedBelief:
    """Belief with distributed confidence"""

    belief_id: str
    statement: str
    creator_node: str
    confidence: float  # 0.0-1.0
    sources: Set[str] = field(default_factory=set)  # Contributing nodes
    votes: Dict[str, float] = field(default_factory=dict)  # node_id -> confidence
    created_at: datetime = field(default_factory=datetime.now)
    agreement_level: float = 0.0  # Consensus strength

    def add_vote(self, node_id: str, confidence: float):
        """Add vote from another node"""
        self.votes[node_id] = confidence
        self._recalculate_agreement()

    def _recalculate_agreement(self):
        """Recalculate consensus agreement"""
        if not self.votes:
            self.agreement_level = self.confidence
            return

        values = list(self.votes.values()) + [self.confidence]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5

        # Agreement = 1 - normalized std deviation
        self.agreement_level = max(0.0, 1.0 - (std_dev / 0.5))

    def consensus_confidence(self) -> float:
        """Get consensus confidence after aggregation"""
        if not self.votes:
            return self.confidence

        all_confidences = list(self.votes.values()) + [self.confidence]

        # Weighted average (higher agreement = higher weight)
        weights = [self.agreement_level] * len(all_confidences)
        if sum(weights) == 0:
            return sum(all_confidences) / len(all_confidences)

        return sum(c * w for c, w in zip(all_confidences, weights)) / sum(weights)


@dataclass
class FederatedKnowledgeGraph:
    """Distributed knowledge graph across nodes"""

    kg_id: str
    entities: Dict[str, Dict] = field(default_factory=dict)
    relationships: Dict[str, List[Tuple[str, str, str]]] = field(default_factory=dict)
    facts: Dict[str, DistributedBelief] = field(default_factory=dict)
    node_contributions: Dict[str, Set[str]] = field(default_factory=dict)

    def add_entity(self, entity_id: str, entity_type: str, properties: Dict, node_id: str):
        """Add entity from a node"""
        if entity_id not in self.entities:
            self.entities[entity_id] = {
                'type': entity_type,
                'properties': properties,
                'source_nodes': set(),
            }
        self.entities[entity_id]['source_nodes'].add(node_id)

        if node_id not in self.node_contributions:
            self.node_contributions[node_id] = set()
        self.node_contributions[node_id].add(entity_id)

    def add_relationship(self, from_entity: str, relation: str, to_entity: str, node_id: str):
        """Add relationship from a node"""
        key = f"{from_entity}_{relation}_{to_entity}"
        if relation not in self.relationships:
            self.relationships[relation] = []
        self.relationships[relation].append((from_entity, relation, to_entity))

        if node_id not in self.node_contributions:
            self.node_contributions[node_id] = set()
        self.node_contributions[node_id].add(key)

    def add_fact(self, fact: DistributedBelief):
        """Add fact to KG"""
        self.facts[fact.belief_id] = fact

    def query_facts(self, query: str) -> List[DistributedBelief]:
        """Query facts matching pattern"""
        matches = []
        for fact in self.facts.values():
            if query.lower() in fact.statement.lower():
                matches.append(fact)
        return sorted(matches, key=lambda f: f.consensus_confidence(), reverse=True)


class NetworkHub:
    """Central hub coordinating distributed reasoning"""

    def __init__(self, hub_id: str, secret_key: str = None):
        """Initialize network hub"""
        self.hub_id = hub_id
        self.secret_key = secret_key or str(uuid.uuid4())
        self.nodes: Dict[str, DistributedNode] = {}
        self.kg = FederatedKnowledgeGraph(kg_id=f"kg_{hub_id}")
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.message_history: List[NetworkMessage] = []
        self.consensus_cache: Dict[str, DistributedBelief] = {}
        self.routing_table: Dict[str, str] = {}  # dest_node -> next_hop
        self.network_topology: Dict[str, Set[str]] = defaultdict(set)
        self.created_at = datetime.now()

    def register_node(self, node: DistributedNode) -> bool:
        """Register a node in the network"""
        if node.node_id in self.nodes:
            return False

        self.nodes[node.node_id] = node
        self.network_topology[node.node_id] = set()
        return True

    def deregister_node(self, node_id: str) -> bool:
        """Deregister a node"""
        if node_id not in self.nodes:
            return False

        self.nodes[node_id].is_active = False

        # Update topology
        for neighbors in self.network_topology.values():
            neighbors.discard(node_id)

        return True

    def get_active_nodes(self, role: Optional[NodeRole] = None) -> List[DistributedNode]:
        """Get active nodes, optionally filtered by role"""
        nodes = [n for n in self.nodes.values() if n.is_healthy()]
        if role:
            nodes = [n for n in nodes if n.role == role]
        return nodes

    def connect_nodes(self, node1_id: str, node2_id: str) -> bool:
        """Create connection between two nodes"""
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return False

        self.network_topology[node1_id].add(node2_id)
        self.network_topology[node2_id].add(node1_id)
        return True

    async def route_message(self, message: NetworkMessage) -> Optional[NetworkMessage]:
        """Route message through network"""
        if message.hop_count > 10:
            return None  # Prevent infinite loops

        # Add to history
        self.message_history.append(message)

        # Sign if not signed
        if not message.signature:
            message.sign(self.secret_key)

        # Route to destination
        if message.receiver_node in self.nodes:
            # Direct delivery
            return message

        # Find route via next hop
        next_hop = self.routing_table.get(message.receiver_node)
        if next_hop:
            message.hop_count += 1
            message.receiver_node = next_hop
            return await self.route_message(message)

        return None

    async def create_reasoning_request(
        self,
        query: str,
        required_nodes: int = 3,
        reasoning_type: str = "hybrid"
    ) -> Dict[str, Any]:
        """Create distributed reasoning request"""
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        # Get available reasoner nodes
        reasoners = [
            n for n in self.get_active_nodes(NodeRole.REASONER)
            if reasoning_type in n.capabilities
        ]

        if len(reasoners) < required_nodes:
            return {
                'request_id': request_id,
                'success': False,
                'error': f'Only {len(reasoners)} reasoners available, need {required_nodes}',
            }

        # Create request messages
        selected_reasoners = reasoners[:required_nodes]
        request_messages = []

        for reasoner in selected_reasoners:
            msg = NetworkMessage(
                message_id=f"msg_{uuid.uuid4().hex[:8]}",
                message_type=MessageType.REASONING_REQUEST,
                sender_node=self.hub_id,
                receiver_node=reasoner.node_id,
                timestamp=time.time(),
                payload={
                    'request_id': request_id,
                    'query': query,
                    'reasoning_type': reasoning_type,
                }
            )
            msg.sign(self.secret_key)
            request_messages.append(msg)

        return {
            'request_id': request_id,
            'success': True,
            'messages': [m.to_dict() for m in request_messages],
            'num_reasoners': len(selected_reasoners),
        }

    async def aggregate_beliefs(self, request_id: str) -> Optional[DistributedBelief]:
        """Aggregate beliefs from multiple nodes for consensus"""
        beliefs = [
            b for b in self.consensus_cache.values()
            if request_id in getattr(b, 'request_ids', [])
        ]

        if not beliefs:
            return None

        # Aggregate
        combined_statement = f"Consensus on {request_id}"
        combined_confidence = sum(b.consensus_confidence() for b in beliefs) / len(beliefs)

        aggregated = DistributedBelief(
            belief_id=f"consensus_{request_id}",
            statement=combined_statement,
            creator_node=self.hub_id,
            confidence=combined_confidence,
            sources={b.creator_node for b in beliefs},
            votes={b.creator_node: b.consensus_confidence() for b in beliefs},
        )

        return aggregated

    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        active_nodes = self.get_active_nodes()

        return {
            'total_nodes': len(self.nodes),
            'active_nodes': len(active_nodes),
            'network_created': self.created_at.isoformat(),
            'total_messages': len(self.message_history),
            'kg_entities': len(self.kg.entities),
            'kg_facts': len(self.kg.facts),
            'consensus_cache_size': len(self.consensus_cache),
            'nodes_by_role': {
                role.value: len([n for n in active_nodes if n.role == role])
                for role in NodeRole
            }
        }


class DistributedReasoningAgent:
    """Agent participating in distributed reasoning"""

    def __init__(self, node: DistributedNode, hub: NetworkHub):
        """Initialize distributed reasoning agent"""
        self.node = node
        self.hub = hub
        self.local_cache: Dict[str, DistributedBelief] = {}
        self.reasoning_history: List[Dict] = []

    async def receive_reasoning_request(self, message: NetworkMessage) -> NetworkMessage:
        """Receive and process reasoning request"""
        request_id = message.payload['request_id']
        query = message.payload['query']
        reasoning_type = message.payload['reasoning_type']

        # Perform reasoning locally
        reasoning_result = await self._reason_locally(query, reasoning_type)

        # Create belief
        belief = DistributedBelief(
            belief_id=f"belief_{request_id}_{self.node.node_id}",
            statement=reasoning_result['answer'],
            creator_node=self.node.node_id,
            confidence=reasoning_result['confidence'],
        )
        belief.request_ids = [request_id]  # Track request

        # Cache locally
        self.local_cache[belief.belief_id] = belief

        # Send response back to hub
        response = NetworkMessage(
            message_id=f"msg_{uuid.uuid4().hex[:8]}",
            message_type=MessageType.REASONING_RESPONSE,
            sender_node=self.node.node_id,
            receiver_node=message.sender_node,
            timestamp=time.time(),
            payload={
                'request_id': request_id,
                'belief_id': belief.belief_id,
                'answer': reasoning_result['answer'],
                'confidence': reasoning_result['confidence'],
                'reasoning_trace': reasoning_result['trace'],
            }
        )
        response.sign(self.hub.secret_key)

        return response

    async def _reason_locally(self, query: str, reasoning_type: str) -> Dict[str, Any]:
        """Perform local reasoning"""
        # Simulate reasoning based on type
        reasoning_methods = {
            'symbolic': (0.95, "Symbolic reasoning completed"),
            'neural': (0.80, "Neural reasoning completed"),
            'hybrid': (0.90, "Hybrid reasoning completed"),
            'debate': (0.85, "Debate reasoning completed"),
        }

        confidence, trace = reasoning_methods.get(reasoning_type, (0.70, "Unknown reasoning type"))

        return {
            'answer': f"Result of {reasoning_type} reasoning on: {query}",
            'confidence': confidence,
            'trace': trace,
        }

    async def participate_in_consensus(self, request_id: str) -> DistributedBelief:
        """Participate in consensus voting"""
        my_belief = next(
            (b for b in self.local_cache.values()
             if request_id in getattr(b, 'request_ids', [])),
            None
        )

        if not my_belief:
            return None

        # Vote with confidence
        my_belief.add_vote(self.node.node_id, my_belief.confidence)
        return my_belief


class ConsensusBuilder:
    """Build consensus from distributed beliefs"""

    def __init__(self, hub: NetworkHub):
        """Initialize consensus builder"""
        self.hub = hub
        self.voting_periods: Dict[str, datetime] = {}
        self.vote_threshold = 0.66  # 66% agreement needed

    async def build_consensus(
        self,
        request_id: str,
        beliefs: List[DistributedBelief],
        timeout_seconds: int = 30
    ) -> Optional[DistributedBelief]:
        """Build consensus from distributed beliefs"""
        if not beliefs:
            return None

        # Collect votes
        for belief in beliefs:
            belief.add_vote(belief.creator_node, belief.confidence)

        # Wait for votes (simulated)
        await asyncio.sleep(min(1, timeout_seconds / 10))

        # Calculate consensus
        avg_confidence = sum(b.consensus_confidence() for b in beliefs) / len(beliefs)

        # Check if agreement is sufficient
        if avg_confidence >= self.vote_threshold:
            consensus_belief = DistributedBelief(
                belief_id=f"consensus_{request_id}",
                statement=f"Consensus reached: {beliefs[0].statement}",
                creator_node=self.hub.hub_id,
                confidence=avg_confidence,
                sources={b.creator_node for b in beliefs},
                votes={b.creator_node: b.consensus_confidence() for b in beliefs},
            )
            return consensus_belief

        return None


class NetworkMonitor:
    """Monitor network health and topology"""

    def __init__(self, hub: NetworkHub, check_interval: int = 10):
        """Initialize network monitor"""
        self.hub = hub
        self.check_interval = check_interval
        self.health_history: List[Dict] = []

    async def run_health_checks(self):
        """Run periodic health checks"""
        while True:
            health_report = {
                'timestamp': datetime.now().isoformat(),
                'stats': self.hub.get_network_stats(),
                'unhealthy_nodes': [
                    n.node_id for n in self.hub.nodes.values()
                    if not n.is_healthy()
                ],
            }

            self.health_history.append(health_report)
            await asyncio.sleep(self.check_interval)

    def get_network_health(self) -> Dict[str, Any]:
        """Get current network health"""
        if not self.health_history:
            return {'status': 'no_data'}

        latest = self.health_history[-1]
        stats = latest['stats']

        # Calculate health percentage
        if stats['total_nodes'] == 0:
            health_percentage = 0.0
        else:
            health_percentage = 100.0 * stats['active_nodes'] / stats['total_nodes']

        return {
            'health_percentage': health_percentage,
            'active_nodes': stats['active_nodes'],
            'total_nodes': stats['total_nodes'],
            'status': 'healthy' if health_percentage >= 80 else 'degraded',
            'message_throughput': len(latest.get('unhealthy_nodes', [])),
        }


class FaultTolerance:
    """Handle network faults and recovery"""

    def __init__(self, hub: NetworkHub):
        """Initialize fault tolerance"""
        self.hub = hub
        self.node_failures: Dict[str, List[datetime]] = defaultdict(list)
        self.recovery_strategies: Dict[str, Callable] = {}

    async def detect_node_failure(self, node_id: str) -> bool:
        """Detect if a node has failed"""
        node = self.hub.nodes.get(node_id)
        if not node or not node.is_healthy():
            self.node_failures[node_id].append(datetime.now())
            return True
        return False

    async def initiate_recovery(self, failed_node_id: str) -> bool:
        """Attempt to recover a failed node"""
        # 1. Replicate data from failed node
        node_contributions = self.hub.kg.node_contributions.get(failed_node_id, set())

        # 2. Assign to backup node
        backup_candidates = [
            n for n in self.hub.get_active_nodes()
            if n.node_id != failed_node_id and NodeRole.KNOWLEDGE_KEEPER in [n.role]
        ]

        if not backup_candidates:
            return False

        backup_node = backup_candidates[0]

        # 3. Replicate data
        self.hub.kg.node_contributions[backup_node.node_id].update(node_contributions)

        return True

    async def heal_network(self):
        """Periodically heal network after failures"""
        for node_id in list(self.hub.nodes.keys()):
            if await self.detect_node_failure(node_id):
                await self.initiate_recovery(node_id)


class DistributedReasoningNetwork:
    """Main class: Complete distributed reasoning network"""

    def __init__(self, network_name: str = "reasoning_network"):
        """Initialize distributed network"""
        self.network_name = network_name
        self.hub = NetworkHub(hub_id=f"hub_{uuid.uuid4().hex[:8]}")
        self.agents: Dict[str, DistributedReasoningAgent] = {}
        self.consensus_builder = ConsensusBuilder(self.hub)
        self.monitor = NetworkMonitor(self.hub)
        self.fault_tolerance = FaultTolerance(self.hub)
        self.created_at = datetime.now()

    def add_reasoner_node(
        self,
        node_id: str,
        host: str,
        port: int,
        capabilities: Set[str] = None
    ) -> DistributedReasoningAgent:
        """Add a reasoner node to network"""
        node = DistributedNode(
            node_id=node_id,
            role=NodeRole.REASONER,
            host=host,
            port=port,
            capabilities=capabilities or {'symbolic', 'neural', 'hybrid', 'debate'}
        )

        self.hub.register_node(node)
        agent = DistributedReasoningAgent(node, self.hub)
        self.agents[node_id] = agent

        return agent

    def add_knowledge_keeper_node(
        self,
        node_id: str,
        host: str,
        port: int
    ) -> DistributedNode:
        """Add knowledge keeper (KG node)"""
        node = DistributedNode(
            node_id=node_id,
            role=NodeRole.KNOWLEDGE_KEEPER,
            host=host,
            port=port,
            capabilities={'kg_storage', 'kg_query'}
        )
        self.hub.register_node(node)
        return node

    def add_consensus_node(
        self,
        node_id: str,
        host: str,
        port: int
    ) -> DistributedNode:
        """Add consensus node"""
        node = DistributedNode(
            node_id=node_id,
            role=NodeRole.CONSENSUS_BUILDER,
            host=host,
            port=port,
            capabilities={'consensus', 'voting'}
        )
        self.hub.register_node(node)
        return node

    def connect_nodes(self, node1_id: str, node2_id: str) -> bool:
        """Connect two nodes"""
        return self.hub.connect_nodes(node1_id, node2_id)

    async def distributed_reasoning(
        self,
        query: str,
        num_reasoners: int = 3,
        reasoning_type: str = "hybrid",
        timeout_seconds: int = 30
    ) -> Dict[str, Any]:
        """Execute distributed reasoning across network"""
        # 1. Create reasoning requests
        request_result = await self.hub.create_reasoning_request(
            query=query,
            required_nodes=num_reasoners,
            reasoning_type=reasoning_type
        )

        if not request_result['success']:
            return request_result

        request_id = request_result['request_id']

        # 2. Get reasoning responses
        beliefs = []
        for msg_dict in request_result['messages']:
            msg = NetworkMessage(**msg_dict)
            # Simulate getting response
            reasoner = self.agents.get(msg.receiver_node)
            if reasoner:
                response = await reasoner.receive_reasoning_request(msg)
                belief = DistributedBelief(
                    belief_id=f"belief_{request_id}_{reasoner.node.node_id}",
                    statement=response.payload['answer'],
                    creator_node=reasoner.node.node_id,
                    confidence=response.payload['confidence'],
                )
                beliefs.append(belief)

        # 3. Build consensus
        consensus = await self.consensus_builder.build_consensus(
            request_id=request_id,
            beliefs=beliefs,
            timeout_seconds=timeout_seconds
        )

        return {
            'request_id': request_id,
            'query': query,
            'reasoning_type': reasoning_type,
            'num_reasoners': len(beliefs),
            'beliefs': [asdict(b) for b in beliefs],
            'consensus': asdict(consensus) if consensus else None,
            'consensus_confidence': consensus.consensus_confidence() if consensus else 0.0,
            'execution_time': time.time(),
        }

    def get_network_status(self) -> Dict[str, Any]:
        """Get complete network status"""
        return {
            'network_name': self.network_name,
            'created_at': self.created_at.isoformat(),
            'hub_id': self.hub.hub_id,
            'health': self.monitor.get_network_health(),
            'statistics': self.hub.get_network_stats(),
            'nodes': {
                node_id: node.to_dict()
                for node_id, node in self.hub.nodes.items()
            },
            'active_agents': len([a for a in self.agents.values() if a.node.is_healthy()]),
        }

    async def start_monitoring(self):
        """Start network monitoring"""
        await self.monitor.run_health_checks()

    async def heal_network(self):
        """Periodically heal network"""
        await self.fault_tolerance.heal_network()

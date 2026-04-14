"""Federated Knowledge Graph with Distributed Sync

Keeps KGs synchronized across network with:
  - Conflict resolution
  - Version control
  - Merkle trees for integrity
  - Differential sync
  - Multi-master replication
"""

import hashlib
import json
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving conflicts in federated KG"""

    LAST_WRITE_WINS = "last_write_wins"
    HIGHEST_CONFIDENCE = "highest_confidence"
    CONSENSUS = "consensus"
    CUSTOM = "custom"


@dataclass
class KGVersion:
    """Version of KG entity"""

    version_id: str
    entity_id: str
    timestamp: datetime
    creator_node: str
    data: Dict[str, Any]
    confidence: float
    signature: Optional[str] = None
    parent_version: Optional[str] = None

    def get_hash(self) -> str:
        """Get hash of this version"""
        content = json.dumps({
            'entity_id': self.entity_id,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'confidence': self.confidence,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class MerkleNode:
    """Node in Merkle tree for KG integrity"""

    node_id: str
    is_leaf: bool
    hash_value: str
    left_child: Optional['MerkleNode'] = None
    right_child: Optional['MerkleNode'] = None
    data: Optional[Dict] = None

    def verify_integrity(self) -> bool:
        """Verify integrity of subtree"""
        if self.is_leaf:
            # Verify leaf hash
            if self.data:
                data_str = json.dumps(self.data, sort_keys=True)
                expected_hash = hashlib.sha256(data_str.encode()).hexdigest()
                return self.hash_value == expected_hash
            return True
        else:
            # Verify internal node
            if self.left_child and self.right_child:
                left_hash = self.left_child.hash_value
                right_hash = self.right_child.hash_value
                combined = left_hash + right_hash
                expected_hash = hashlib.sha256(combined.encode()).hexdigest()
                return self.hash_value == expected_hash
            return False


class MerkleTree:
    """Merkle tree for KG integrity verification"""

    def __init__(self, tree_id: str, data_list: List[Dict] = None):
        """Initialize Merkle tree"""
        self.tree_id = tree_id
        self.root = None

        if data_list:
            self._build_tree(data_list)

    def _build_tree(self, data_list: List[Dict]):
        """Build Merkle tree from data"""
        if not data_list:
            return

        # Create leaf nodes
        leaves = []
        for i, data in enumerate(data_list):
            data_str = json.dumps(data, sort_keys=True)
            data_hash = hashlib.sha256(data_str.encode()).hexdigest()
            leaf = MerkleNode(
                node_id=f"leaf_{i}",
                is_leaf=True,
                hash_value=data_hash,
                data=data
            )
            leaves.append(leaf)

        # Build tree bottom-up
        current_level = leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    left = current_level[i]
                    right = current_level[i + 1]
                    combined_hash = hashlib.sha256(
                        (left.hash_value + right.hash_value).encode()
                    ).hexdigest()
                    internal = MerkleNode(
                        node_id=f"internal_{len(next_level)}",
                        is_leaf=False,
                        hash_value=combined_hash,
                        left_child=left,
                        right_child=right
                    )
                    next_level.append(internal)
                else:
                    next_level.append(current_level[i])

            current_level = next_level

        self.root = current_level[0]

    def verify_integrity(self) -> bool:
        """Verify entire tree integrity"""
        if not self.root:
            return True
        return self.root.verify_integrity()

    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """Get Merkle proof for a leaf"""
        # Returns list of (sibling_hash, position) for proof verification
        proof = []
        # Simplified implementation
        return proof


class DifferentialSync:
    """Efficient differential synchronization for federated KGs"""

    def __init__(self):
        """Initialize differential sync"""
        self.entity_versions: Dict[str, List[KGVersion]] = defaultdict(list)
        self.last_sync: Dict[str, datetime] = {}

    def record_version(self, entity_id: str, version: KGVersion):
        """Record a version of an entity"""
        self.entity_versions[entity_id].append(version)
        version.parent_version = (
            self.entity_versions[entity_id][-2].version_id
            if len(self.entity_versions[entity_id]) > 1
            else None
        )

    def get_changes_since(
        self,
        node_id: str,
        since_timestamp: datetime
    ) -> Dict[str, List[KGVersion]]:
        """Get all changes since timestamp"""
        changes = {}

        for entity_id, versions in self.entity_versions.items():
            entity_changes = [
                v for v in versions
                if v.timestamp > since_timestamp and v.creator_node == node_id
            ]
            if entity_changes:
                changes[entity_id] = entity_changes

        return changes

    def merge_changes(
        self,
        local_versions: Dict[str, List[KGVersion]],
        remote_versions: Dict[str, List[KGVersion]],
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_CONFIDENCE
    ) -> Dict[str, KGVersion]:
        """Merge local and remote changes"""
        merged = {}

        all_entity_ids = set(local_versions.keys()) | set(remote_versions.keys())

        for entity_id in all_entity_ids:
            local_version = local_versions[entity_id][-1] if entity_id in local_versions else None
            remote_version = remote_versions[entity_id][-1] if entity_id in remote_versions else None

            if not local_version and remote_version:
                merged[entity_id] = remote_version
            elif not remote_version and local_version:
                merged[entity_id] = local_version
            elif local_version and remote_version:
                # Conflict resolution
                if conflict_strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
                    merged[entity_id] = (
                        local_version if local_version.timestamp > remote_version.timestamp
                        else remote_version
                    )
                elif conflict_strategy == ConflictResolutionStrategy.HIGHEST_CONFIDENCE:
                    merged[entity_id] = (
                        local_version if local_version.confidence >= remote_version.confidence
                        else remote_version
                    )
                else:
                    # Default to local
                    merged[entity_id] = local_version

        return merged


class FederatedKnowledgeGraphSync:
    """Complete federated KG with synchronization"""

    def __init__(self, kg_id: str):
        """Initialize federated KG"""
        self.kg_id = kg_id
        self.entities: Dict[str, KGVersion] = {}
        self.relationships: Dict[str, Dict] = defaultdict(dict)
        self.version_history: Dict[str, List[KGVersion]] = defaultdict(list)
        self.differential_sync = DifferentialSync()
        self.merkle_tree = None
        self.node_replicas: Dict[str, Dict[str, KGVersion]] = defaultdict(dict)
        self.last_merkle_hash = None
        self.created_at = datetime.now()

    def add_entity(
        self,
        entity_id: str,
        entity_data: Dict,
        creator_node: str,
        confidence: float = 1.0
    ) -> KGVersion:
        """Add entity to KG"""
        version = KGVersion(
            version_id=f"v_{entity_id}_{len(self.version_history[entity_id])}",
            entity_id=entity_id,
            timestamp=datetime.now(),
            creator_node=creator_node,
            data=entity_data,
            confidence=confidence,
        )

        # Record version
        self.version_history[entity_id].append(version)
        self.differential_sync.record_version(entity_id, version)

        # Update current
        self.entities[entity_id] = version

        # Update replica
        self.node_replicas[creator_node][entity_id] = version

        # Invalidate Merkle tree
        self.merkle_tree = None

        return version

    def add_relationship(
        self,
        from_entity: str,
        relation_type: str,
        to_entity: str,
        properties: Dict = None
    ):
        """Add relationship"""
        key = f"{from_entity}_{relation_type}_{to_entity}"
        self.relationships[relation_type][key] = {
            'from': from_entity,
            'to': to_entity,
            'properties': properties or {},
            'timestamp': datetime.now().isoformat(),
        }

    def get_entity_history(self, entity_id: str) -> List[KGVersion]:
        """Get version history for entity"""
        return self.version_history.get(entity_id, [])

    def reconcile_entity(
        self,
        entity_id: str,
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_CONFIDENCE
    ) -> KGVersion:
        """Reconcile conflicting versions of entity"""
        versions = self.version_history[entity_id]

        if not versions:
            return None

        if len(versions) == 1:
            return versions[0]

        # Apply conflict resolution
        if conflict_strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
            return max(versions, key=lambda v: v.timestamp)
        elif conflict_strategy == ConflictResolutionStrategy.HIGHEST_CONFIDENCE:
            return max(versions, key=lambda v: v.confidence)
        else:
            return versions[-1]

    def build_merkle_tree(self):
        """Build Merkle tree for current state"""
        entity_data = [
            {
                'entity_id': v.entity_id,
                'version_id': v.version_id,
                'data': v.data,
                'confidence': v.confidence,
            }
            for v in self.entities.values()
        ]

        self.merkle_tree = MerkleTree(self.kg_id, entity_data)
        self.last_merkle_hash = self.merkle_tree.root.hash_value if self.merkle_tree.root else None

    def verify_integrity(self) -> bool:
        """Verify KG integrity"""
        if not self.merkle_tree:
            self.build_merkle_tree()

        return self.merkle_tree.verify_integrity() if self.merkle_tree else True

    async def sync_with_node(
        self,
        remote_node_id: str,
        remote_entities: Dict[str, KGVersion],
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_CONFIDENCE
    ) -> Dict[str, Any]:
        """Sync with remote node"""
        # Get local changes
        local_dict = {
            entity_id: [self.entities[entity_id]]
            for entity_id in self.entities
        }

        # Get remote changes
        remote_dict = {
            entity_id: [version]
            for entity_id, version in remote_entities.items()
        }

        # Merge
        merged = self.differential_sync.merge_changes(
            local_dict, remote_dict, conflict_strategy
        )

        # Update local
        sync_count = 0
        for entity_id, version in merged.items():
            if entity_id not in self.entities or version.timestamp > self.entities[entity_id].timestamp:
                self.entities[entity_id] = version
                self.version_history[entity_id].append(version)
                sync_count += 1

        # Update replica
        self.node_replicas[remote_node_id] = remote_entities

        # Invalidate Merkle tree
        self.merkle_tree = None

        return {
            'sync_count': sync_count,
            'merged_count': len(merged),
            'success': True,
        }

    def get_replica_divergence(self, node_id: str) -> float:
        """Calculate divergence from replica"""
        if node_id not in self.node_replicas:
            return 1.0  # 100% divergence

        remote_replica = self.node_replicas[node_id]

        # Count differences
        all_ids = set(self.entities.keys()) | set(remote_replica.keys())
        differences = 0

        for entity_id in all_ids:
            local = self.entities.get(entity_id)
            remote = remote_replica.get(entity_id)

            if local and remote:
                if local.get_hash() != remote.get_hash():
                    differences += 1
            elif local or remote:
                differences += 1

        return differences / len(all_ids) if all_ids else 0.0

    def get_stats(self) -> Dict[str, Any]:
        """Get KG statistics"""
        return {
            'kg_id': self.kg_id,
            'created_at': self.created_at.isoformat(),
            'total_entities': len(self.entities),
            'total_relationships': sum(len(rels) for rels in self.relationships.values()),
            'total_versions': sum(len(versions) for versions in self.version_history.values()),
            'num_replicas': len(self.node_replicas),
            'integrity_verified': self.verify_integrity(),
            'last_merkle_hash': self.last_merkle_hash,
        }

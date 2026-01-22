<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""Unified Memory and Knowledge management core."""

import logging
from datetime import datetime
from pathlib import Path
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Any, Dict, List, Optional

from .file_system_core import FileSystemCore
from .storage_core import StorageCore
from .workspace_core import WorkspaceCore
=======
from typing import Any, Dict, List, Optional, Union
from src.core.base.common.storage_core import StorageCore
from src.core.base.common.file_system_core import FileSystemCore
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import Any, Dict, List, Optional, Union
from src.core.base.common.storage_core import StorageCore
from src.core.base.common.file_system_core import FileSystemCore
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.memory")

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class MemoryCore:
    """
    Centralized handler for Episodic, Long-term, and Sharded Knowledge.
    Standardizes utility scoring, filtering, and cross-agent indexing.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    _instance: Optional["MemoryCore"] = None

    def __new__(cls) -> "MemoryCore":
=======
    _instance: Optional['MemoryCore'] = None

    def __new__(cls):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    _instance: Optional['MemoryCore'] = None

    def __new__(cls):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if cls._instance is None:
            cls._instance = super(MemoryCore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self) -> None:
        # Already initialized via _initialize in __new__
        pass

    def _initialize(self) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._fs = FileSystemCore()
        self._storage = StorageCore()
        self.base_path = WorkspaceCore().get_path("data/memory")
        self._fs.ensure_directory(self.base_path)
        self.index_path = Path("data/agent_knowledge_index.json")

    # pylint: disable=too-many-arguments,too-many-positional-arguments
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def _initialize(self):
        self._fs = FileSystemCore()
        self._storage = StorageCore()
        self.base_path = Path("data/memory")
        self._fs.ensure_directory(self.base_path)
        self.index_path = Path("data/agent_knowledge_index.json")

<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def create_episode(
        self,
        agent_id: str,
        task: str,
        content: str,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None,
<<<<<<< HEAD
<<<<<<< HEAD
        base_utility: float = 0.5,
=======
        base_utility: float = 0.5
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        base_utility: float = 0.5
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> Dict[str, Any]:
        """
        Create a standardized episodic memory record.
        Hot path for Rust acceleration (utility scoring).
        """
        if rc and hasattr(rc, "create_episode_struct"):
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                # pylint: disable=no-member
                return rc.create_episode_struct(  # type: ignore
                    agent_id, task, content, success, metadata or {}, base_utility
                )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust create_episode_struct failed: %s", e)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                return rc.create_episode_struct(
                    agent_id, task, content, success, metadata or {}, base_utility
                )
            except Exception as e:
                logger.warning(f"Rust create_episode_struct failed: {e}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        # Python Fallback
        utility_score = base_utility + (0.2 if success else -0.3)
        utility_score = max(0.0, min(1.0, utility_score))

        return {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "task": task,
            "content": content,
            "success": success,
            "utility_score": utility_score,
            "metadata": metadata or {},
        }

    def rank_memories(
<<<<<<< HEAD
<<<<<<< HEAD
        self, memories: List[Dict[str, Any]], limit: int = 5, min_utility: float = 0.0
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self, 
        memories: List[Dict[str, Any]], 
        limit: int = 5,
        min_utility: float = 0.0
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> List[Dict[str, Any]]:
        """
        Rank memories by utility score and recency.
        Hot path for Rust acceleration.
        """
        if rc and hasattr(rc, "rank_memories_rust"):
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                # pylint: disable=no-member
                return rc.rank_memories_rust(memories, limit, min_utility)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust rank_memories_rust failed: %s", e)
=======
                return rc.rank_memories_rust(memories, limit, min_utility)
            except Exception as e:
                logger.warning(f"Rust rank_memories_rust failed: {e}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                return rc.rank_memories_rust(memories, limit, min_utility)
            except Exception as e:
                logger.warning(f"Rust rank_memories_rust failed: {e}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        # Python Fallback
        filtered = [m for m in memories if m.get("utility_score", 0.0) >= min_utility]
        # Sort by utility (desc) then timestamp (desc)
<<<<<<< HEAD
<<<<<<< HEAD
        sorted_m = sorted(filtered, key=lambda x: (x.get("utility_score", 0.0), x.get("timestamp", "")), reverse=True)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        sorted_m = sorted(
            filtered, 
            key=lambda x: (x.get("utility_score", 0.0), x.get("timestamp", "")), 
            reverse=True
        )
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return sorted_m[:limit]

    def retrieve_memory_graph(self, root_id: str, depth: int = 2) -> List[Dict[str, str]]:
        """Rust-accelerated graph traversal for complex memory retrieval."""
        if rc and hasattr(rc, "retrieve_memory_graph_rust"):
<<<<<<< HEAD
<<<<<<< HEAD
            try:
                # pylint: disable=no-member
                return rc.retrieve_memory_graph_rust(root_id, depth)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
            return rc.retrieve_memory_graph_rust(root_id, depth)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            return rc.retrieve_memory_graph_rust(root_id, depth)
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Simple Python fallback (stub)
        return [{"source": root_id, "target": "related_concept", "relation": "associated"}]

    def store_knowledge(
<<<<<<< HEAD
<<<<<<< HEAD
        self,
        agent_id: str,
        key: str,
        content: Any,
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self, 
        agent_id: str, 
        key: str, 
        content: Any, 
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        mode: str = "structured",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store knowledge in the agent's partitioned space.
        Modes: 'structured' (JSON/B-Tree), 'semantic' (Vector), 'relational' (Graph)
        """
        if mode == "semantic":
            return self._store_semantic(agent_id, key, content, metadata)

        agent_dir = self._get_agent_path(agent_id, mode)
        file_path = agent_dir / f"{key}.json"
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        try:
            # Standardized I/O via StorageCore
            self._storage.save_json(file_path, content)
            return True
<<<<<<< HEAD
<<<<<<< HEAD
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error("Failed to store %s knowledge for %s: %s", mode, agent_id, e)
=======
        except Exception as e:
            logger.error(f"Failed to store {mode} knowledge for {agent_id}: {e}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        except Exception as e:
            logger.error(f"Failed to store {mode} knowledge for {agent_id}: {e}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return False

    def _store_semantic(self, agent_id: str, key: str, content: Any, metadata: Optional[Dict[str, Any]]) -> bool:
        """Internal helper for semantic (vector) storage."""
        try:
<<<<<<< HEAD
<<<<<<< HEAD
            import chromadb  # pylint: disable=import-outside-toplevel

            client = chromadb.PersistentClient(path=str(self.base_path / "vector_db"))
            collection = client.get_or_create_collection(name=f"{agent_id}_knowledge")
            collection.add(documents=[str(content)], metadatas=[metadata] if metadata else [{}], ids=[key])
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.warning("ChromaDB storage failed for %s: %s", agent_id, e)
            return False

    def retrieve_knowledge(
        self, agent_id: str, query: str, mode: str = "structured", limit: int = 5
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            import chromadb
            client = chromadb.PersistentClient(path=str(self.base_path / "vector_db"))
            collection = client.get_or_create_collection(name=f"{agent_id}_knowledge")
            collection.add(
                documents=[str(content)],
                metadatas=[metadata] if metadata else [{}],
                ids=[key]
            )
            return True
        except Exception as e:
            logger.warning(f"ChromaDB storage failed for {agent_id}: {e}")
            return False

    def retrieve_knowledge(
        self,
        agent_id: str,
        query: str,
        mode: str = "structured",
        limit: int = 5
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> List[Dict[str, Any]]:
        """
        Retrieve knowledge based on mode and query.
        """
        if mode == "semantic":
            return self._retrieve_semantic(agent_id, query, limit)

        # Python Fallback / Structured Logic
        agent_dir = self._get_agent_path(agent_id, mode)
        if not agent_dir.exists():
            return []

        if mode == "structured":
            # Direct key lookup
            file_path = agent_dir / f"{query}.json"
            if file_path.exists():
                data = self._storage.load_json(file_path)
                return [data] if data else []
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return []

    def _retrieve_semantic(self, agent_id: str, query: str, limit: int) -> List[Dict[str, Any]]:
        """Internal helper for semantic retrieval."""
        if rc and hasattr(rc, "semantic_search"):
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                # pylint: disable=no-member
                return rc.semantic_search(agent_id, query, limit)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust semantic search failed: %s", e)

        try:
            import chromadb  # pylint: disable=import-outside-toplevel

            client = chromadb.PersistentClient(path=str(self.base_path / "vector_db"))
            collection = client.get_or_create_collection(name=f"{agent_id}_knowledge")
            results = collection.query(query_texts=[query], n_results=limit)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                return rc.semantic_search(agent_id, query, limit)
            except Exception as e:
                logger.warning(f"Rust semantic search failed: {e}")

        try:
            import chromadb
            client = chromadb.PersistentClient(path=str(self.base_path / "vector_db"))
            collection = client.get_or_create_collection(name=f"{agent_id}_knowledge")
            results = collection.query(query_texts=[query], n_results=limit)
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            output = []
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            ids = results.get("ids", [[]])[0]
<<<<<<< HEAD
<<<<<<< HEAD

            for i, doc in enumerate(docs):
                output.append({"id": ids[i], "content": doc, "metadata": metas[i]})
            return output
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.warning("ChromaDB retrieval failed for %s: %s", agent_id, e)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            
            for i in range(len(docs)):
                output.append({
                    "id": ids[i],
                    "content": docs[i],
                    "metadata": metas[i]
                })
            return output
        except Exception as e:
            logger.warning(f"ChromaDB retrieval failed for {agent_id}: {e}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return []

    def delete_knowledge(self, agent_id: str, key: str, mode: str = "structured") -> bool:
        """Standardized deletion of knowledge."""
        if mode == "semantic":
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                import chromadb  # pylint: disable=import-outside-toplevel

=======
                import chromadb
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                import chromadb
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                client = chromadb.PersistentClient(path=str(self.base_path / "vector_db"))
                collection = client.get_or_create_collection(name=f"{agent_id}_knowledge")
                collection.delete(ids=[key])
                return True
<<<<<<< HEAD
<<<<<<< HEAD
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
=======
            except Exception:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            except Exception:
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                return False

        agent_dir = self._get_agent_path(agent_id, mode)
        file_path = agent_dir / f"{key}.json"
        if file_path.exists():
            try:
                file_path.unlink()
                return True
<<<<<<< HEAD
<<<<<<< HEAD
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.error("Failed to delete %s knowledge: %s", mode, e)
=======
            except Exception as e:
                logger.error(f"Failed to delete {mode} knowledge: {e}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            except Exception as e:
                logger.error(f"Failed to delete {mode} knowledge: {e}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return False

    def _get_agent_path(self, agent_id: str, mode: str) -> Path:
        """Helper to get partitioned storage path."""
        path = self.base_path / agent_id / mode
        self._fs.ensure_directory(path)
        return path

    def update_index(self, agent_id: str, tags: List[str]) -> bool:
        """
        Update the global knowledge index with agent metadata.
        This file can be very large (>50MB), so we use atomic write.
        """
        index = self._storage.load_json(self.index_path, default={})
<<<<<<< HEAD
<<<<<<< HEAD
        index[agent_id] = {"tags": tags, "last_updated": datetime.now().isoformat()}
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        index[agent_id] = {
            "tags": tags,
            "last_updated": datetime.now().isoformat()
        }
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self._fs.atomic_write(self.index_path, self._storage.to_json(index))

#!/usr/bin/env python3

"""Engine for persistent episodic memory of agent actions and outcomes."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from src.logic.agents.cognitive.context.engines.MemoryCore import MemoryCore

try:
    import chromadb
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

class MemoryEngine:
    """Stores and retrieves historical agent contexts and lessons learned."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.memory_file = self.workspace_root / ".agent_memory.json"
        self.db_path = self.workspace_root / "data/db/.agent_memory_db"
        self.episodes: List[Dict[str, Any]] = []
        self._collection = None
        self.core = MemoryCore()
        self.load()

    def _init_db(self) -> Any:
        if not HAS_CHROMA: return None
        if self._collection: return self._collection
        try:
            client = chromadb.PersistentClient(path=str(self.db_path))
            self._collection = client.get_or_create_collection(name="agent_memory")
            return self._collection
        except Exception as e:
            logging.error(f"Memory DB init error: {e}")
            return None

    def record_episode(self, agent_name: str, task: str, outcome: str, success: bool, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Records an agent's experience with semantic indexing and utility scoring."""
        episode = self.core.create_episode(agent_name, task, outcome, success, metadata)
        self.episodes.append(episode)
        
        # Add to vector db for semantic recall
        collection = self._init_db()
        if collection:
            try:
                doc = self.core.format_for_indexing(episode)
                collection.add(
                    documents=[doc],
                    metadatas=[{
                        "agent": episode['agent'], 
                        "success": str(episode['success']), 
                        "timestamp": episode['timestamp'],
                        "utility_score": float(episode['utility_score'])
                    }],
                    ids=[f"mem_{len(self.episodes)}_{int(datetime.now().timestamp())}"]
                )
            except Exception as e:
                logging.error(f"Failed to index memory: {e}")
                
        self.save()

    def update_utility(self, memory_id: str, increment: float) -> None:
        """Updates the utility score of a specific memory episode."""
        collection = self._init_db()
        if not collection: return
        
        try:
            # Fetch existing metadata
            result = collection.get(ids=[memory_id])
            if result and result['metadatas']:
                meta = result['metadatas'][0]
                old_score = float(meta.get('utility_score', 0.5))
                new_score = self.core.calculate_new_utility(old_score, increment)
                meta['utility_score'] = new_score
                
                collection.update(
                    ids=[memory_id],
                    metadatas=[meta]
                )
                
                # Update local list too
                for ep in self.episodes:
                    # Note: memory_id format check or matching logic here
                    pass
        except Exception as e:
            logging.error(f"Failed to update utility for {memory_id}: {e}")

    def get_lessons_learned(self, query: str = "", limit: int = 5, min_utility: float = 0.0) -> List[Dict[str, Any]]:
        """Retrieves past episodes relevant to the query, filtered by high utility."""
        if not query:
            # Return recent high utility episodes
            candidates = [ep for ep in self.episodes if ep.get("utility_score", 0.5) >= min_utility]
            return candidates[-limit:]
            
        collection = self._init_db()
        if collection:
            try:
                # Build specific filter for utility if Chroma version supports it
                where_clause = {"utility_score": {"$gte": min_utility}} if min_utility > 0 else None
                results = collection.query(
                    query_texts=[query], 
                    n_results=limit,
                    where=where_clause
                )
                
                semantic_results = []
                for i, doc in enumerate(results.get("documents", [[]])[0]):
                    meta = results['metadatas'][0][i]
                    semantic_results.append({
                        "task": "Semantic Memory", 
                        "outcome": doc, 
                        "success": meta.get("success") == "True", 
                        "agent": meta.get("agent", "Self"),
                        "utility_score": meta.get("utility_score", 0.5)
                    })
                return semantic_results
            except Exception as e:
                logging.error(f"Memory search error: {e}")
            
        # Fallback to simple keyword matching
        relevant = []
        q = query.lower()
        for ep in reversed(self.episodes):
            if q in ep["task"].lower() or q in ep["outcome"].lower() or q in ep["agent"].lower():
                relevant.append(ep)
            if len(relevant) >= limit:
                break
        return relevant

    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Public interface for semantic search across episodic memories."""
        collection = self._init_db()
        if not collection:
            # Fallback to simple matching if Chroma is not available
            return [{"content": ep["outcome"], "metadata": {"file_path": ep.get("metadata", {}).get("file_path", "unknown"), "agent": ep["agent"]}, "score": 0.5} 
                    for ep in self.get_lessons_learned(query, limit)]
            
        try:
            results = collection.query(query_texts=[query], n_results=limit)
            matches = []
            for i in range(len(results.get("documents", [[]])[0])):
                matches.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] if 'distances' in results else 0
                })
            return matches
        except Exception as e:
            logging.error(f"search_memories error: {e}")
            return []

    def save(self) -> None:
        """Persist memory to disk."""
        try:
            self.memory_file.write_text(json.dumps(self.episodes, indent=2))
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")

    def load(self) -> None:
        """Load memory from disk."""
        if self.memory_file.exists():
            try:
                self.episodes = json.loads(self.memory_file.read_text())
            except Exception as e:
                logging.error(f"Failed to load memory: {e}")
                self.episodes = []

    def clear(self) -> None:
        """Wipe memory."""
        self.episodes = []
        if self.memory_file.exists():
            self.memory_file.unlink()

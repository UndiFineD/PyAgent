#!/usr/bin/env python3

"""Long-term memory for agents using vector storage."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

class LongTermMemory:
    """Manages persistent conversational and factual memory for agents."""
    
    def __init__(self, agent_name: str = "default_agent", collection_name: str = None, persist_directory: str = None) -> None:
        self.agent_name = agent_name
        self.persist_directory = persist_directory or f"data/agents/{agent_name}/memory"
        self.collection_name = collection_name or f"memory_{agent_name}"
        self._client = None
        self._collection = None
        self._enabled = HAS_CHROMADB
        
        if not self._enabled:
            logging.warning("ChromaDB not available. Long-term memory will be disabled.")

    def _init_db(self) -> bool:
        """Initialize the ChromaDB client and collection."""
        if not self._enabled:
            return False
            
        try:
            if self._client is None:
                self._client = chromadb.PersistentClient(path=self.persist_directory)
                self._collection = self._client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            return True
        except Exception as e:
            logging.error(f"LongTermMemory init error: {e}")
            self._enabled = False
            return False

    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None) -> None:
        """Store a thought, observation, or interaction in memory."""
        if not self._init_db():
            return
            
        mem_id = f"mem_{datetime.now().timestamp()}"
        meta = metadata or {}
        meta["timestamp"] = str(datetime.now().isoformat())
        if tags:
            meta["tags"] = ",".join(tags)
            
        try:
            self._collection.add(
                documents=[content],
                metadatas=[meta],
                ids=[mem_id]
            )
        except Exception as e:
            logging.error(f"Error storing memory: {e}")

    def query(self, query_text: str, n_results: int = 5, filter_tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant memories for a given query."""
        if not self._init_db():
            return []
            
        where = {}
        if filter_tags:
            # Simple tag filtering (requires exact match or contains logic if metadata supports it)
            # Here we assume direct metadata filtering for simplicity
            if len(filter_tags) == 1:
                where = {"tags": {"$contains": filter_tags[0]}}
                
        try:
            results = self._collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where if where else None
            )
            
            output = []
            if results and 'documents' in results and results['documents']:
                for i in range(len(results['documents'][0])):
                    output.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            return output
        except Exception as e:
            logging.error(f"Error querying memory: {e}")
            return []

    def clear(self) -> None:
        """Clear all stored memories."""
        if not self._init_db():
            return
        try:
            # Chroma delete with empty where is not always supported or recommended
            # We fetch IDs and then delete
            ids = self._collection.get()['ids']
            if ids:
                self._collection.delete(ids=ids)
        except Exception as e:
            logging.error(f"Error clearing memory: {e}")

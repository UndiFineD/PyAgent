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

# Phase 16: Rust acceleration for keyword matching and scoring

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.logic.agents.cognitive.context.utils.SearchAlgorithm import SearchAlgorithm
from src.logic.agents.cognitive.context.models.SemanticSearchResult import (
    SemanticSearchResult,
)
from typing import Any
import logging

__version__ = VERSION

# Phase 16: Rust acceleration imports
try:
    import rust_core
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for SemanticSearchEngine")


class SemanticSearchEngine:
    """Performs semantic code search using embeddings.

    Provides functionality to search code using semantic similarity
    rather than just keyword matching.

    Attributes:
        results: List of search results.
        index: Index of embedded content.

    Example:
        >>> engine=SemanticSearchEngine()
        >>> results=engine.search("function that handles authentication")
    """

    def __init__(self, persist_directory: str | None = None) -> None:
        """Initialize the semantic search engine."""
        self.results: list[SemanticSearchResult] = []
        self.algorithm: SearchAlgorithm = SearchAlgorithm.KEYWORD
        self.similarity_metric: str = "cosine"
        self.documents: dict[str, str] = {}
        self.persist_directory = persist_directory
        self._client = None
        self._collection = None

    def _get_collection(self) -> Any:
        """Lazy initialization of ChromaDB collection."""
        if self._collection is None:
            try:
                # Handle Pydantic v2 compatibility for older ChromaDB versions
                try:
                    import pydantic
                    if hasattr(pydantic, "__version__") and pydantic.__version__.startswith("2"):
                        try:
                            from pydantic_settings import BaseSettings
                            # Only patch if not already present
                            if not hasattr(pydantic, "BaseSettings"):
                                pydantic.BaseSettings = BaseSettings
                        except ImportError:
                            pass
                except ImportError:
                    pass

                import chromadb
                from chromadb.utils import embedding_functions

                if self.persist_directory:
                    self._client = chromadb.PersistentClient(
                        path=self.persist_directory
                    )
                else:
                    self._client = chromadb.EphemeralClient()

                emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )

                self._collection = self._client.get_or_create_collection(
                    name="pyagent_code",
                    embedding_function=emb_fn,
                    metadata={"hnsw:space": self.similarity_metric},
                )
            except Exception as e:
                logging.warning(
                    f"Failed to initialize ChromaDB: {e}. Falling back to keyword search."
                )
                return None
        return self._collection

    def set_algorithm(self, algorithm: SearchAlgorithm) -> None:
        """Set the search algorithm."""
        self.algorithm = algorithm

    def add_document(self, doc_id: str, content: str) -> None:
        """Add a document to the search index."""
        self.documents[doc_id] = content
        self.index_content(doc_id, content)

    def clear(self) -> None:
        """Clear all indexed documents and results."""
        self.results.clear()
        self.documents.clear()
        collection = self._get_collection()
        if collection:
            # Delete all items in collection by fetching all IDs
            existing_ids = collection.get().get("ids", [])
            if existing_ids:
                collection.delete(ids=existing_ids)

    def index_content(self, file_path: str, content: str) -> None:
        """Index content for searching.

        Args:
            file_path: Path to the file.
            content: File content to index.
        """
        # Update documents storage
        self.documents[file_path] = content

        collection = self._get_collection()
        if collection:
            # Upsert into Chroma
            collection.upsert(
                documents=[content], ids=[file_path], metadatas=[{"path": file_path}]
            )

    def search(
        self, query: str, algorithm: SearchAlgorithm | None = None
    ) -> list[SemanticSearchResult]:
        """Search for related code.

        Args:
            query: Search query.
            algorithm: Search algorithm to use (uses self.algorithm if None).

        Returns:
            List of search results.
        """
        search_algo = algorithm or self.algorithm
        self.results = []

        if search_algo == SearchAlgorithm.SEMANTIC:
            collection = self._get_collection()
            if collection:
                results = collection.query(query_texts=[query], n_results=10)

                if results and "documents" in results and results["documents"]:
                    for i in range(len(results["ids"][0])):
                        file_path = results["ids"][0][i]
                        content = results["documents"][0][i]
                        # Chroma distances: smaller is better for cosine if it's 1-cosine
                        # But Chroma cosine space is usually 1 - cosine similarity
                        # Score: 1.0 - distance
                        distance = (
                            results["distances"][0][i]
                            if "distances" in results
                            else 0.5
                        )
                        score = max(0.0, min(1.0, 1.0 - distance))

                        self.results.append(
                            SemanticSearchResult(
                                file_path=file_path,
                                content_snippet=content[
                                    :200
                                ],  # Longer snippet for semantic
                                similarity_score=score,
                            )
                        )
                return sorted(
                    self.results, key=lambda r: r.similarity_score, reverse=True
                )

        # Fallback to keyword search (original logic)
        # Phase 16: Try Rust-accelerated keyword scoring
        if _RUST_AVAILABLE and hasattr(rust_core, "keyword_search_score_rust"):
            try:
                query_words = query.lower().split()
                doc_items = list(self.documents.items())
                contents = [content for _, content in doc_items]
                scores = rust_core.keyword_search_score_rust(query_words, contents)
                if scores:
                    for i, (file_path, content) in enumerate(doc_items):
                        if scores[i] > 0:
                            self.results.append(
                                SemanticSearchResult(
                                    file_path=file_path,
                                    content_snippet=content[:80],
                                    similarity_score=min(scores[i], 1.0),
                                )
                            )
                    return sorted(self.results, key=lambda r: r.similarity_score, reverse=True)
            except Exception:
                pass  # Fall through to Python implementation
        
        # Python fallback
        query_words = set(query.lower().split())

        for file_path, content in self.documents.items():
            content_lower = content.lower()
            # Better keyword match: check if ANY query word is in content
            matches = [w for w in query_words if w in content_lower]
            if not matches:
                continue

            score = len(matches) / max(1, len(query_words))
            self.results.append(
                SemanticSearchResult(
                    file_path=file_path,
                    content_snippet=content[:80],
                    similarity_score=min(score, 1.0),
                )
            )

        return sorted(self.results, key=lambda r: r.similarity_score, reverse=True)

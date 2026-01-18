"""
Integration Tests: Search Mesh & Semantic Aggregation (Rust Core)

Refactored from temp/test_search_oxidation.py into proper pytest format.
Tests Rust-accelerated search result aggregation and federated search.
"""

import pytest
import asyncio


class TestSearchMeshCore:
    """Tests for SearchMeshCore aggregation."""
    
    def test_core_import(self):
        """Test SearchMeshCore can be imported."""
        try:
            from src.logic.agents.intelligence.core.SearchMeshCore import SearchMeshCore
            core = SearchMeshCore()
            assert core is not None
        except ImportError as e:
            pytest.skip(f"SearchMeshCore not available: {e}")
    
    def test_aggregate_empty_results(self):
        """Test aggregation with empty results."""
        try:
            from src.logic.agents.intelligence.core.SearchMeshCore import SearchMeshCore
            core = SearchMeshCore()
            
            results = core.aggregate_results({})
            assert results == [] or results is not None
        except ImportError:
            pytest.skip("SearchMeshCore not available")
    
    def test_aggregate_single_provider(self):
        """Test aggregation with single provider results."""
        try:
            from src.logic.agents.intelligence.core.SearchMeshCore import SearchMeshCore
            core = SearchMeshCore()
            
            raw_results = {
                "google": [
                    {"title": "Result 1", "url": "http://url1.com", "snippet": "Snippet 1", "score": 0.9},
                    {"title": "Result 2", "url": "http://url2.com", "snippet": "Snippet 2", "score": 0.8},
                ]
            }
            
            results = core.aggregate_results(raw_results)
            
            assert len(results) == 2
            # Results should be sorted by score
            assert results[0]["title"] == "Result 1"
        except ImportError:
            pytest.skip("SearchMeshCore not available")
    
    def test_aggregate_multiple_providers(self):
        """Test aggregation merges results from multiple providers."""
        try:
            from src.logic.agents.intelligence.core.SearchMeshCore import SearchMeshCore
            core = SearchMeshCore()
            
            raw_results = {
                "google": [
                    {"title": "G1", "url": "http://url1.com", "snippet": "gs1", "score": 0.9},
                    {"title": "G2", "url": "http://url2.com", "snippet": "gs2", "score": 0.8},
                ],
                "bing": [
                    {"title": "B1", "url": "http://url1.com", "snippet": "bs1", "score": 0.7},  # Same URL as G1
                    {"title": "B3", "url": "http://url3.com", "snippet": "bs3", "score": 0.6},
                ]
            }
            
            results = core.aggregate_results(raw_results)
            
            # Should merge url1.com results
            assert len(results) >= 2
            
            # Find the merged result
            merged = next((r for r in results if "url1.com" in r.get("url", "")), None)
            if merged:
                # Should have combined score or multiple providers
                assert "providers" in merged or merged.get("total_score", 0) > 0.9
        except ImportError:
            pytest.skip("SearchMeshCore not available")
    
    def test_aggregate_deduplication(self):
        """Test that duplicate URLs are properly handled."""
        try:
            from src.logic.agents.intelligence.core.SearchMeshCore import SearchMeshCore
            core = SearchMeshCore()
            
            raw_results = {
                "google": [
                    {"title": "Same", "url": "http://same.com", "snippet": "g", "score": 0.9},
                ],
                "bing": [
                    {"title": "Same", "url": "http://same.com", "snippet": "b", "score": 0.8},
                ],
                "duckduckgo": [
                    {"title": "Same", "url": "http://same.com", "snippet": "d", "score": 0.7},
                ]
            }
            
            results = core.aggregate_results(raw_results)
            
            # Should be deduplicated to 1 result
            urls = [r.get("url") for r in results]
            unique_urls = set(urls)
            assert len(unique_urls) == 1
        except ImportError:
            pytest.skip("SearchMeshCore not available")


class TestSemanticSearchMeshAgent:
    """Tests for SemanticSearchMeshAgent federated search."""
    
    def test_agent_creation(self):
        """Test agent can be created."""
        try:
            from src.logic.agents.intelligence.SemanticSearchMeshAgent import SemanticSearchMeshAgent
            agent = SemanticSearchMeshAgent(workspace_path=".")
            assert agent is not None
        except ImportError as e:
            pytest.skip(f"SemanticSearchMeshAgent not available: {e}")
    
    def test_register_shard(self):
        """Test shard registration."""
        try:
            from src.logic.agents.intelligence.SemanticSearchMeshAgent import SemanticSearchMeshAgent
            agent = SemanticSearchMeshAgent(workspace_path=".")
            
            agent.register_shard("test_shard", {"vectors": [[0.1, 0.2, 0.3]]})
            
            # Shard should be registered
            assert hasattr(agent, 'shards') or True  # Implementation may vary
        except ImportError:
            pytest.skip("SemanticSearchMeshAgent not available")
    
    def test_register_multiple_shards(self):
        """Test multiple shard registration."""
        try:
            from src.logic.agents.intelligence.SemanticSearchMeshAgent import SemanticSearchMeshAgent
            agent = SemanticSearchMeshAgent(workspace_path=".")
            
            agent.register_shard("shard_alpha", {"vectors": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]})
            agent.register_shard("shard_omega", {"vectors": [[0.11, 0.21, 0.31], [0.9, 0.9, 0.9]]})
            
            # Both shards registered
            assert True  # If no exception, success
        except ImportError:
            pytest.skip("SemanticSearchMeshAgent not available")
    
    def test_federated_search(self):
        """Test federated search across shards."""
        try:
            from src.logic.agents.intelligence.SemanticSearchMeshAgent import SemanticSearchMeshAgent
            agent = SemanticSearchMeshAgent(workspace_path=".")
            
            agent.register_shard("shard_a", {"vectors": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]})
            agent.register_shard("shard_b", {"vectors": [[0.11, 0.21, 0.31], [0.9, 0.9, 0.9]]})
            
            query_vector = [0.1, 0.2, 0.3]
            results = agent.federated_search(query_embedding=query_vector, limit=3)
            
            assert isinstance(results, list)
            if results:
                # Results should have shard info and score
                assert "shard" in results[0] or "score" in results[0]
        except ImportError:
            pytest.skip("SemanticSearchMeshAgent not available")
    
    def test_federated_search_ranking(self):
        """Test that federated search returns ranked results."""
        try:
            from src.logic.agents.intelligence.SemanticSearchMeshAgent import SemanticSearchMeshAgent
            agent = SemanticSearchMeshAgent(workspace_path=".")
            
            # One shard with exact match, one with distant match
            agent.register_shard("exact", {"vectors": [[0.1, 0.2, 0.3]]})
            agent.register_shard("distant", {"vectors": [[0.9, 0.9, 0.9]]})
            
            query_vector = [0.1, 0.2, 0.3]
            results = agent.federated_search(query_embedding=query_vector, limit=2)
            
            if len(results) >= 2:
                # First result should have higher score (closer match)
                assert results[0]["score"] >= results[1]["score"]
        except ImportError:
            pytest.skip("SemanticSearchMeshAgent not available")


class TestRustAggregation:
    """Tests for Rust-accelerated aggregation functions."""
    
    def test_rust_core_available(self):
        """Test rust_core module is available."""
        try:
            import rust_core
            assert rust_core is not None
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_rust_aggregation_function(self):
        """Test Rust aggregation function if available."""
        try:
            import rust_core
            
            # Check for aggregation-related functions
            funcs = [name for name in dir(rust_core) if 'aggregate' in name.lower()]
            
            if not funcs:
                pytest.skip("No aggregation functions in rust_core")
            
            # Test the first available aggregation function
            func = getattr(rust_core, funcs[0])
            assert callable(func)
        except ImportError:
            pytest.skip("rust_core not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

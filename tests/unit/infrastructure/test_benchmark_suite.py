# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import asyncio
from unittest.mock import MagicMock
from src.infrastructure.benchmarks.benchmark_suite import BenchmarkSuite, BenchmarkResult

class TestBenchmarkSuite:
    def test_benchmark_result_derived_metrics(self):
        """Test that BenchmarkResult calculates derived metrics correctly."""
        result = BenchmarkResult(
            name="Test",
            duration=2.0,
            total_tokens=100,
            output_tokens=50
        )
        assert result.tokens_per_sec == 50.0
        assert result.output_tps == 25.0
        assert result.latency_ms_per_token == 20.0

    def test_benchmark_tokenization(self):
        """Test tokenization benchmark execution."""
        suite = BenchmarkSuite()
        test_texts = {"tiny": "hello world"}
        results = suite.benchmark_tokenization(test_texts, iterations=10, compare_rust=False)
        
        assert len(results) >= 1
        assert "Python Tokenization: tiny" in results[0].name
        assert results[0].total_tokens > 0
        assert results[0].duration > 0

    @pytest.mark.asyncio
    async def test_benchmark_agent_performance_sync(self):
        """Test agent performance benchmark with a sync method."""
        suite = BenchmarkSuite()
        mock_agent = MagicMock()
        mock_agent.chat.return_value = "This is a response"
        
        result = await suite.benchmark_agent_performance(
            mock_agent, 
            prompt="Hello", 
            label="SyncAgent", 
            method_name="chat"
        )
        
        assert result.success
        assert result.name == "SyncAgent"
        assert result.total_tokens > 0
        mock_agent.chat.assert_called_once_with("Hello")

    @pytest.mark.asyncio
    async def test_benchmark_agent_performance_async(self):
        """Test agent performance benchmark with an async method."""
        suite = BenchmarkSuite()
        
        async def mock_chat(prompt):
            return "Async response"
            
        mock_agent = MagicMock()
        mock_agent.chat = mock_chat
        
        result = await suite.benchmark_agent_performance(
            mock_agent, 
            prompt="Hello", 
            label="AsyncAgent", 
            method_name="chat"
        )
        
        assert result.success
        assert result.name == "AsyncAgent"
        assert result.metrics.get("output_length", 0) > 0 or result.total_tokens > 0

    def test_run_sustained_throughput(self):
        """Test sustained throughput benchmark execution."""
        suite = BenchmarkSuite()
        test_texts = ["test 1", "test 2"]
        
        # Run for a very short duration for testing
        result = suite.run_sustained_throughput(test_texts, duration_seconds=0.1)
        
        assert result.success
        assert result.duration >= 0.1
        assert result.iterations > 0
        assert result.total_tokens > 0

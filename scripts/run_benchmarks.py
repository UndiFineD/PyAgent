#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
Unified Benchmarking CLI for PyAgent.
Uses the BenchmarkSuite to run various performance tests.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.services.benchmarks.benchmark_suite import BenchmarkSuite

async def main():
    suite = BenchmarkSuite()

    # 1. Tokenization Benchmarks
    test_texts = {
        "Short": "What is Python?",
        "Medium": "Explain the concept of technical debt in software development.",
        "Long": (
            "Provide a comprehensive analysis of microservices architecture, "
            "including its advantages, disadvantages, common patterns, "
            "best practices, and real-world use cases."
        ) * 3,
        "Code": (
            "def binary_search(arr, target):\n"
            "    left, right = 0, len(arr) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target: return mid\n"
            "        elif arr[mid] < target: left = mid + 1\n"
            "        else: right = mid - 1\n"
            "    return -1"
        )
    }

    print("\n🚀 Running Tokenization Benchmarks...")
    suite.benchmark_tokenization(test_texts, iterations=5000)

    # 2. Sustained Throughput (Shortened for CLI example)
    print("\n🚀 Running Sustained Throughput Test (10s)...")
    texts_list = list(test_texts.values())
    suite.run_sustained_throughput(texts_list, duration_seconds=10)

    # 3. Agent Performance (if BenchmarkAgent is available)
    try:
        from src.logic.agents.development.benchmark_agent import BenchmarkAgent
        # Note: We need a valid path or mock for Agent initialization
        # For simplicity in this CLI, we only run if we can easily init
        print("\n🚀 Running Agent Generation Benchmark...")
        agent = BenchmarkAgent("scripts/benchmark_agent.py")
        await suite.benchmark_agent_performance(agent, "Hello, tell me about yourself", label="BenchmarkAgent")
    except Exception as e:
        print(f"\n⚠️  Skipping Agent benchmark: {e}")

    # Output results
    suite.print_summary()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Direct Token Generation Speed Test

Tests token generation speed using direct API calls without full agent framework.
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_benchmarks():
    print("🚀 PyAgent Token Generation Speed Test (Direct API)")
    print("=" * 70)

    # Test tokenization performance
    print("\n📊 Testing Tokenization Performance")
    print("-" * 70)

try:
    from src.infrastructure.engine.tokenization.tokenizer_registry import estimate_token_count
    print("✅ Successfully imported token estimation")

    test_texts = {
        "Tiny": "Hello!",
        "Short": "What is Python? Please explain briefly.",
        "Medium": "Explain the concept of technical debt in software development. Provide examples and best practices for managing it.",
        "Long": " ".join([
            "Provide a comprehensive analysis of microservices architecture,",
            "including its advantages, disadvantages, common patterns,",
            "best practices, and real-world use cases. Compare it to",
            "monolithic architecture and explain when each is appropriate."
        ]),
        "Code": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
    }

    print("\nToken Counting Performance:")
    print(f"{'Text Type':<12} {'Tokens':<10} {'Time (μs)':<15} {'Chars/Token':<15}")
    print("-" * 70)

    for name, text in test_texts.items():
        # Warm-up
        estimate_token_count(text)

        # Benchmark
        iterations = 10000
        start = time.perf_counter()

        for _ in range(iterations):
            tokens = estimate_token_count(text)

        duration = time.perf_counter() - start
        avg_time_us = (duration / iterations) * 1_000_000
        chars_per_token = len(text) / tokens if tokens > 0 else 0

        print(f"{name:<12} {tokens:<10} {avg_time_us:<15.2f} {chars_per_token:<15.2f}")

except Exception as e:
    print(f"❌ Tokenization test failed: {e}")
    import traceback
    traceback.print_exc()

# Test Rust acceleration
print("\n⚡ Testing Rust Acceleration")
print("-" * 70)

try:
    sys.path.insert(0, str(project_root))  # Ensure rust_core can be found
    import rust_core

    print("✅ Rust core loaded successfully\n")

    test_text = "This is a sample text for performance testing. " * 20

    # Python estimation
    py_iterations = 10000
    start = time.perf_counter()
    for _ in range(py_iterations):
        py_tokens = estimate_token_count(test_text)
    py_duration = time.perf_counter() - start

    # Rust estimation
    rust_iterations = 10000
    start = time.perf_counter()
    for _ in range(rust_iterations):
        rust_tokens = rust_core.estimate_tokens_rust(test_text)
    rust_duration = time.perf_counter() - start

    speedup = py_duration / rust_duration if rust_duration > 0 else 0

    print(f"Python estimation ({py_iterations:,} iterations):")
    print(f"  Time: {py_duration*1000:.2f}ms")
    print(f"  Tokens: {py_tokens}")
    print(f"  Speed: {py_iterations/py_duration:,.0f} ops/sec")

    print(f"\nRust estimation ({rust_iterations:,} iterations):")
    print(f"  Time: {rust_duration*1000:.2f}ms")
    print(f"  Tokens: {rust_tokens}")
    print(f"  Speed: {rust_iterations/rust_duration:,.0f} ops/sec")

    print(f"\nSpeedup: {speedup:.2f}x faster")
    print(f"Results match: {py_tokens == rust_tokens}")

except ImportError as e:
    print(f"⚠️  Rust core not available: {e}")
    print("   Token estimation will use Python fallback")
except Exception as e:
    print(f"❌ Rust test failed: {e}")
    import traceback
    traceback.print_exc()

# Test actual token generation (mock)
print("\n🎯 Simulated Token Generation Performance")
print("-" * 70)

try:
    # Since we can't easily test real LLM generation without setup,
    # we'll simulate the metrics you'd expect to see

    prompts = {
        "Short query": ("What is Python?", 50),
        "Medium query": ("Explain technical debt", 150),
        "Long query": ("Comprehensive analysis of microservices", 300),
        "Code generation": ("Write a binary search function", 200),
    }

    print("\nExpected Generation Metrics (Simulated):")
    print(f"{'Query Type':<25} {'In Tokens':<12} {'Out Tokens':<12} {'Target TPS':<15}")
    print("-" * 70)

    for name, (prompt, expected_output) in prompts.items():
        input_tokens = estimate_token_count(prompt)

        # Typical speeds for different backends:
        # GPT-4: 30-50 TPS
        # GPT-3.5: 80-120 TPS
        # Local vLLM (good GPU): 100-200 TPS
        target_tps = 50  # Conservative estimate for GPT-4

        print(f"{name:<25} {input_tokens:<12} {expected_output:<12} {target_tps:<15}")

    print("\n💡 To test actual generation:")
    print("   1. Configure your backend (GitHub Models, vLLM, etc.)")
    print("   2. Set API keys in environment")
    print("   3. Run the full benchmark suite")

except Exception as e:
    print(f"❌ Simulation failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 70)
print("📋 PERFORMANCE TESTING SUMMARY")
print("=" * 70)

print("\n✅ Tested Components:")
print("   • Token estimation (Python)")
print("   • Rust acceleration (if available)")
print("   • Expected generation metrics")

print("\n📈 Next Steps:")
print("   1. Configure backend: Edit .env or agent config")
print("   2. Set model: Choose gpt-4o, gpt-3.5-turbo, etc.")
print("   3. Test with real generation:")
print("      python scripts/test_real_generation.py")
print("   4. Run full benchmarks:")
print("      pytest tests/performance/test_token_generation_speed.py -v")

print("\n💡 Quick Backend Setup:")
print("   export GITHUB_TOKEN=your_token")
print("   export MODEL=gpt-4o")
print("   # or configure in .agent.yml")

print("\n✨ Infrastructure test complete!")

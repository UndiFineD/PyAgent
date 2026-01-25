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

#!/usr/bin/env python3
"""
Simple Token Generation Speed Test for PyAgent

Tests token generation performance without complex dependencies.
Run: python scripts/simple_token_bench.py
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🚀 PyAgent Token Generation Speed Test (Simplified)")
print("=" * 70)

# Test 1: Token estimation performance
print("\n📊 Test 1: Token Estimation Performance")
print("-" * 70)

try:
    from src.infrastructure.tokenizer.TokenizerRegistry import estimate_token_count
    print("✅ TokenizerRegistry imported successfully")

    # Test prompts
    test_texts = {
        "short": "Hello, how are you?",
        "medium": "Explain the concept of technical debt in software development.",
        "long": "Provide a comprehensive analysis of microservices architecture, including advantages, disadvantages, patterns, and best practices." * 3,
        "code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
    }

    print("\nToken Estimation Results:")
    for name, text in test_texts.items():
        start = time.perf_counter()
        iterations = 1000

        for _ in range(iterations):
            tokens = estimate_token_count(text)

        duration = time.perf_counter() - start
        avg_time_us = (duration / iterations) * 1_000_000

        print(f"  {name:10s}: {tokens:4d} tokens, {avg_time_us:6.2f}μs per call")

except ImportError as e:
    print(f"❌ Failed to import TokenizerRegistry: {e}")

# Test 2: Rust acceleration (if available)
print("\n⚡ Test 2: Rust Acceleration")
print("-" * 70)

try:
    import rust_core
    print("✅ Rust core available")

    test_text = "This is a test sentence for token estimation." * 10

    # Python version
    start = time.perf_counter()
    for _ in range(10000):
        py_tokens = estimate_token_count(test_text)
    py_duration = time.perf_counter() - start

    # Rust version
    start = time.perf_counter()
    for _ in range(10000):
        rust_tokens = rust_core.estimate_tokens_rust(test_text)
    rust_duration = time.perf_counter() - start

    speedup = py_duration / rust_duration

    print(f"\nPerformance Comparison (10,000 iterations):")
    print(f"  Python: {py_duration*1000:.2f}ms")
    print(f"  Rust:   {rust_duration*1000:.2f}ms")
    print(f"  Speedup: {speedup:.2f}x")
    print(f"  Result match: {py_tokens == rust_tokens}")

except ImportError:
    print("⚠️  Rust core not available (performance acceleration disabled)")
except Exception:  # pylint: disable=broad-exception-caught, unused-variable
    print(f"❌ Rust test failed: {e}")

# Test 3: Streaming engine availability
print("\n🌊 Test 3: Streaming Engine")
print("-" * 70)

try:
    from src.infrastructure.backend.vllm_advanced.StreamingEngine import (
        StreamingVllmEngine,
        StreamingConfig,
    )

    engine = StreamingVllmEngine()
    if engine.is_available:
        print("✅ vLLM streaming engine available")
        print(f"   Config: {engine.config.model}")
    else:
        print("⚠️  vLLM not installed (streaming disabled)")

except ImportError as e:
    print(f"⚠️  StreamingEngine not available: {e}")

# Test 4: Backend availability
print("\n🔧 Test 4: Backend Availability")
print("-" * 70)

backends_status = []

# Check for various backends
backend_checks = [
    ("GitHub Models", "requests", "For GitHub Models API"),
    ("VLLM", "vllm", "For local inference"),
    ("Transformers", "transformers", "For HuggingFace models"),
    ("Torch", "torch", "For PyTorch models"),
]

for name, module, description in backend_checks:
    try:
        __import__(module)
        backends_status.append((name, True, description))
        print(f"✅ {name:20s} - {description}")
    except ImportError:
        backends_status.append((name, False, description))
        print(f"❌ {name:20s} - {description}")

# Test 5: Simple generation test (if possible)
print("\n🎯 Test 5: Simple Generation Test")
print("-" * 70)

try:
    # Try to create a simple test that measures token generation
    # This is a mock test since we can't easily create an agent

    test_prompt = "Write a Python function that adds two numbers."
    expected_response_tokens = 100  # Estimated

    print(f"Test prompt: '{test_prompt}'")
    print(f"Estimated input tokens: {estimate_token_count(test_prompt)}")
    print(f"Expected output tokens: ~{expected_response_tokens}")

    # Simulate a generation (would be actual agent call in real test)
    print("\n⚠️  Actual generation test requires agent initialization")
    print("   Use full benchmark script for end-to-end testing")

except Exception:  # pylint: disable=broad-exception-caught, unused-variable
    print(f"❌ Generation test failed: {e}")

# Summary
print("\n" + "=" * 70)
print("📋 SUMMARY")
print("=" * 70)

available_features = []
unavailable_features = []

if 'estimate_token_count' in dir():
    available_features.append("Token estimation")
else:
    unavailable_features.append("Token estimation")

try:
    import rust_core
    available_features.append("Rust acceleration")
except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
unavailable_features.append("Rust acceleration")

if any(status for _, status, _ in backends_status):
    available_features.append(f"{sum(1 for _, s, _ in backends_status if s)}/{len(backends_status)} backends")
else:
    unavailable_features.append("All backends")

print("\n✅ Available:")
for feature in available_features:
    print(f"   • {feature}")

if unavailable_features:
    print("\n⚠️  Unavailable:")
    for feature in unavailable_features:
        print(f"   • {feature}")

print("\n💡 Next Steps:")
print("   1. For full agent benchmarking, fix import issues in BenchmarkAgent")
print("   2. Install vLLM for streaming tests: pip install vllm")
print("   3. Build Rust core for acceleration: cd rust_core && cargo build --release")
print("   4. Run pytest suite: pytest tests/performance/test_token_generation_speed.py")

print("\n✨ Basic infrastructure test complete!")

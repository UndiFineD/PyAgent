#!/usr/bin/env python3
"""
Direct Token Generation Speed Test using Rust Core

This script tests token generation speed using the Rust acceleration
without needing the full PyAgent stack.
"""

import time
import sys
from pathlib import Path

# Add project root to sys.path to find rust_core.pyd
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🚀 PyAgent Token Generation Speed Test (Rust Direct)")
print("=" * 70)

# Test Rust core availability and performance
print("\n⚡ Rust Core Token Estimation Benchmark")
print("-" * 70)

try:
    import rust_core
    print("✅ Rust core module loaded successfully\n")
    
    # Test cases with different text lengths and complexities
    test_cases = {
        "Tiny (5 words)": "Hello, how are you today?",
        "Short (20 words)": "Explain the concept of technical debt in software development and provide some practical examples from real-world projects.",
        "Medium (50 words)": " ".join(["This is a medium-length text sample for token counting."] * 5),
        "Long (200 words)": " ".join(["Microservices architecture is a software development approach where applications are built as a collection of small, independent services."] * 10),
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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
""",
        "Very Long (1000 words)": " ".join(["Token estimation performance testing with various text lengths."] * 100),
    }
    
    print("📊 Token Estimation Results:\n")
    print(f"{'Test Case':<20} {'Tokens':<10} {'Time (μs)':<15} {'Tokens/sec':<15}")
    print("-" * 70)
    
    total_tokens = 0
    total_time = 0
    
    for name, text in test_cases.items():
        # Warm-up
        rust_core.estimate_tokens_rust(text)
        
        # Benchmark
        iterations = 10000 if len(text) < 500 else 1000
        start = time.perf_counter()
        
        for _ in range(iterations):
            tokens = rust_core.estimate_tokens_rust(text)
        
        duration = time.perf_counter() - start
        
        avg_time_us = (duration / iterations) * 1_000_000
        tokens_per_sec = tokens / (duration / iterations)
        
        total_tokens += tokens
        total_time += duration / iterations
        
        print(f"{name:<20} {tokens:<10} {avg_time_us:<15.2f} {tokens_per_sec:<15,.0f}")
    
    # Throughput test
    print("\n" + "=" * 70)
    print("🚄 Sustained Throughput Test")
    print("-" * 70)
    
    # Test with continuous token counting for 5 seconds
    test_duration = 2.0  # seconds
    test_text = "This is a sample text for throughput testing. " * 20
    
    print(f"\nRunning continuous token estimation for {test_duration} seconds...")
    
    count = 0
    total_tokens_processed = 0
    start_time = time.perf_counter()
    
    while (time.perf_counter() - start_time) < test_duration:
        tokens = rust_core.estimate_tokens_rust(test_text)
        total_tokens_processed += tokens
        count += 1
    
    actual_duration = time.perf_counter() - start_time
    
    print(f"\nThroughput Results:")
    print(f"  Iterations: {count:,}")
    print(f"  Total tokens processed: {total_tokens_processed:,}")
    print(f"  Duration: {actual_duration:.3f}s")
    print(f"  Iterations/sec: {count/actual_duration:,.0f}")
    print(f"  Tokens/sec: {total_tokens_processed/actual_duration:,.0f}")
    
    # Batch estimation test
    print("\n" + "=" * 70)
    print("📦 Batch Token Estimation")
    print("-" * 70)
    
    # Test batch_estimate_tokens_rust if available
    if hasattr(rust_core, 'batch_estimate_tokens_rust'):
        print("\n✅ Batch estimation available\n")
        
        batch_texts = [
            "Short prompt 1",
            "Medium length prompt for testing purposes",
            "A longer prompt that contains more detailed information about the subject matter",
        ] * 100  # 300 total prompts
        
        # Single estimation
        start = time.perf_counter()
        single_results = [rust_core.estimate_tokens_rust(text) for text in batch_texts]
        single_duration = time.perf_counter() - start
        
        # Batch estimation
        start = time.perf_counter()
        batch_results = rust_core.batch_estimate_tokens_rust(batch_texts, 4.0)  # 4 chars per token
        batch_duration = time.perf_counter() - start
        
        print(f"Batch size: {len(batch_texts)}")
        print(f"Single estimation: {single_duration*1000:.2f}ms")
        print(f"Batch estimation:  {batch_duration*1000:.2f}ms")
        print(f"Speedup: {single_duration/batch_duration:.2f}x")
        print(f"Results match: {single_results == batch_results}")
    else:
        print("\n⚠️  Batch estimation not available in this version")
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    
    print(f"\n✅ Rust Core Performance:")
    print(f"   Average estimation time: {(total_time / len(test_cases)) * 1_000_000:.2f}μs")
    print(f"   Total test tokens: {total_tokens:,}")
    print(f"   Sustained throughput: {total_tokens_processed/actual_duration:,.0f} tokens/sec")
    
    print("\n💡 Next Steps for Full Agent Testing:")
    print("   1. Fix import issues: Change 'Version' to 'version' in imports")
    print("   2. Test with actual LLM backends (GitHub Models, vLLM, etc.)")
    print("   3. Measure end-to-end latency with real prompts")
    print("   4. Compare streaming vs non-streaming performance")
    
    print("\n✨ Rust core benchmark complete!")
    
except ImportError as e:
    print(f"❌ Rust core not available: {e}")
    print("\n💡 To build Rust core:")
    print("   cd rust_core")
    print("   cargo build --release")
    print("   copy target/release/rust_core.pyd ..")
    sys.exit(1)

except AttributeError as e:
    print(f"❌ Rust core function not found: {e}")
    print("\nAvailable Rust core functions:")
    for attr in dir(rust_core):
        if not attr.startswith('_'):
            print(f"   - {attr}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

#!/usr/bin/env python3
"""
5-Minute Sustained Token Throughput Test

Measures maximum token estimation throughput over a 5-minute period.
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🚀 PyAgent 5-Minute Token Throughput Test")
print("=" * 70)

try:
    from src.infrastructure.engine.tokenization.tokenizer_registry import estimate_token_count
    print("✅ Token estimation module loaded\n")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

# Test configuration
TEST_DURATION = 5 * 60  # 5 minutes in seconds
PROGRESS_INTERVAL = 30  # Report progress every 30 seconds

# Test text samples (varying lengths for realistic workload)
test_texts = [
    "What is Python?",
    "Explain the concept of technical debt in software development with examples.",
    "Provide a comprehensive analysis of microservices architecture, including its advantages, disadvantages, common patterns, best practices, and real-world use cases.",
    """
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
    "Write a REST API using FastAPI that handles user authentication and CRUD operations for a todo list application.",
]

# Pre-calculate expected tokens for each text
text_tokens = [estimate_token_count(text) for text in test_texts]
total_text_tokens = sum(text_tokens)

print(f"Test Configuration:")
print(f"  Duration: {TEST_DURATION} seconds ({TEST_DURATION/60:.0f} minutes)")
print(f"  Test texts: {len(test_texts)}")
print(f"  Total tokens per cycle: {total_text_tokens}")
print(f"  Progress updates every: {PROGRESS_INTERVAL}s")
print("\n" + "=" * 70)
print("🏃 Starting sustained throughput test...")
print("=" * 70)

# Warm-up
print("\n🔥 Warming up...")
for text in test_texts:
    estimate_token_count(text)
print("✅ Warm-up complete\n")

# Main test
start_time = time.perf_counter()
last_report = start_time
iterations = 0
total_tokens_processed = 0
text_index = 0

print(f"{'Time (s)':<12} {'Iterations':<15} {'Tokens':<15} {'Tokens/sec':<15} {'Status'}")
print("-" * 70)

try:
    while True:
        current_time = time.perf_counter()
        elapsed = current_time - start_time

        # Check if test duration reached
        if elapsed >= TEST_DURATION:
            break

        # Process one text
        text = test_texts[text_index]
        tokens = estimate_token_count(text)

        iterations += 1
        total_tokens_processed += tokens
        text_index = (text_index + 1) % len(test_texts)

        # Progress report
        if current_time - last_report >= PROGRESS_INTERVAL:
            tokens_per_sec = total_tokens_processed / elapsed
            print(f"{elapsed:<12.1f} {iterations:<15,} {total_tokens_processed:<15,} {tokens_per_sec:<15,.0f} Running...")
            last_report = current_time

except KeyboardInterrupt:
    print("\n⚠️  Test interrupted by user")
    elapsed = time.perf_counter() - start_time

# Final results
end_time = time.perf_counter()
total_duration = end_time - start_time

tokens_per_second = total_tokens_processed / total_duration
iterations_per_second = iterations / total_duration
avg_tokens_per_iteration = total_tokens_processed / iterations if iterations > 0 else 0

print("\n" + "=" * 70)
print("📊 FINAL RESULTS")
print("=" * 70)

print(f"\n⏱️  Duration:")
print(f"   Target: {TEST_DURATION:.0f}s ({TEST_DURATION/60:.0f} minutes)")
print(f"   Actual: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")

print(f"\n🔢 Iterations:")
print(f"   Total iterations: {iterations:,}")
print(f"   Iterations/second: {iterations_per_second:,.1f}")
print(f"   Avg tokens/iteration: {avg_tokens_per_iteration:.1f}")

print(f"\n🎯 Token Throughput:")
print(f"   Total tokens processed: {total_tokens_processed:,}")
print(f"   Tokens per second: {tokens_per_second:,.0f}")
print(f"   Tokens per minute: {tokens_per_second * 60:,.0f}")
print(f"   Tokens per hour: {tokens_per_second * 3600:,.0f}")

print(f"\n📈 Performance Breakdown:")
print(f"   Estimation speed: {1000000/tokens_per_sec:.2f}μs per token")
print(f"   Cycle time: {total_duration/iterations*1000:.2f}ms per iteration")

print("\n" + "=" * 70)
print("✨ Test Complete!")
print("=" * 70)

# Save results
results_file = project_root / "tests" / "performance" / "results" / f"5min_throughput_{int(time.time())}.txt"
results_file.parent.mkdir(parents=True, exist_ok=True)

with open(results_file, "w") as f:
    f.write("5-Minute Token Throughput Test Results\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Duration: {total_duration:.2f}s\n")
    f.write(f"Iterations: {iterations:,}\n")
    f.write(f"Total Tokens: {total_tokens_processed:,}\n")
    f.write(f"Tokens/Second: {tokens_per_second:,.0f}\n")
    f.write(f"Tokens/Minute: {tokens_per_second * 60:,.0f}\n")
    f.write(f"Tokens/Hour: {tokens_per_second * 3600:,.0f}\n")

print(f"\n💾 Results saved to: {results_file}")

#!/usr/bin/env python3
"""
Quick Token Generation Speed Test for PyAgent

A simple, standalone script to test token generation speed.
Run this directly: python scripts/benchmark_token_speed.py
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.logic.agents.development.benchmark_agent import BenchmarkAgent
    from src.infrastructure.engine.tokenization.tokenizer_registry import estimate_token_count
    print("✅ Successfully imported PyAgent modules")
except ImportError as e:
    print(f"❌ Failed to import PyAgent modules: {e}")
    print("Make sure you're running from the project root and dependencies are installed.")
    sys.exit(1)


def measure_token_speed(agent, prompt: str, label: str = "Test") -> dict:
    """Measure token generation speed for a single prompt."""
    print(f"\n{'='*60}")
    print(f"🧪 {label}")
    print(f"{'='*60}")
    print(f"📝 Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    
    # Estimate input tokens
    input_tokens = estimate_token_count(prompt)
    print(f"📊 Input tokens: {input_tokens}")
    
    # Measure generation
    start = time.perf_counter()
    
    try:
        # Attempt different agent methods
        if hasattr(agent, 'improve_content'):
            output = agent.improve_content(prompt)
        elif hasattr(agent, 'chat'):
            output = agent.chat(prompt)
        elif hasattr(agent, 'run_benchmark'):
            # For BenchmarkAgent specifically
            output = agent.run_benchmark("self", prompt)
        else:
            # Try calling the agent directly
            output = str(agent)
            print("⚠️  Using fallback - agent may not support expected methods")
    except Exception as e:
        duration = time.perf_counter() - start
        print(f"❌ Generation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "duration": duration,
        }
    
    duration = time.perf_counter() - start
    
    # Estimate output tokens
    output_tokens = estimate_token_count(str(output))
    total_tokens = input_tokens + output_tokens
    
    # Calculate metrics
    tokens_per_sec = total_tokens / duration if duration > 0 else 0
    output_tps = output_tokens / duration if duration > 0 else 0
    latency_ms = (duration / total_tokens * 1000) if total_tokens > 0 else 0
    
    # Display results
    print(f"\n📈 RESULTS:")
    print(f"   ⏱️  Duration: {duration:.3f}s")
    print(f"   📤 Output tokens: {output_tokens}")
    print(f"   📊 Total tokens: {total_tokens}")
    print(f"   🚀 Tokens/sec (total): {tokens_per_sec:.2f}")
    print(f"   🚀 Tokens/sec (output only): {output_tps:.2f}")
    print(f"   ⏳ Latency per token: {latency_ms:.2f}ms")
    
    if len(str(output)) < 500:
        print(f"\n💬 Output preview:\n{output}\n")
    else:
        print(f"\n💬 Output preview:\n{str(output)[:500]}...\n")
    
    return {
        "success": True,
        "duration": duration,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "tokens_per_sec": tokens_per_sec,
        "output_tps": output_tps,
        "latency_ms": latency_ms,
        "output": str(output),
    }


def main():
    """Run token generation speed tests."""
    print("🚀 PyAgent Token Generation Speed Test")
    print("=" * 60)
    
    # Initialize agent
    print("\n🔧 Initializing BenchmarkAgent...")
    try:
        agent = BenchmarkAgent(".")
        print("✅ Agent initialized successfully")
        print(f"   Backend: {getattr(agent, 'backend', 'unknown')}")
        print(f"   Model: {getattr(agent, 'model', 'unknown')}")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Test prompts
    tests = [
        ("Short prompt", "What is Python?"),
        ("Medium prompt", "Explain the concept of technical debt in software development with examples."),
        ("Long prompt", (
            "Provide a comprehensive analysis of microservices architecture, including its advantages, "
            "disadvantages, common patterns, best practices, and real-world use cases. Compare it to "
            "monolithic architecture and explain when each approach is more appropriate."
        )),
        ("Code generation", (
            "Write a Python function that implements a binary search algorithm. "
            "Include docstrings, type hints, and handle edge cases."
        )),
    ]
    
    # Run tests
    results = []
    for label, prompt in tests:
        result = measure_token_speed(agent, prompt, label)
        results.append(result)
        
        # Small delay between tests
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r.get("success", False)]
    
    if successful:
        avg_tps = sum(r["tokens_per_sec"] for r in successful) / len(successful)
        avg_output_tps = sum(r["output_tps"] for r in successful) / len(successful)
        avg_latency = sum(r["latency_ms"] for r in successful) / len(successful)
        total_tokens = sum(r["total_tokens"] for r in successful)
        total_time = sum(r["duration"] for r in successful)
        
        print(f"\n✅ Successful tests: {len(successful)}/{len(results)}")
        print(f"\n📊 Average Performance:")
        print(f"   Tokens/sec (total): {avg_tps:.2f}")
        print(f"   Tokens/sec (output): {avg_output_tps:.2f}")
        print(f"   Latency/token: {avg_latency:.2f}ms")
        print(f"\n📈 Totals:")
        print(f"   Total tokens processed: {total_tokens}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Overall throughput: {total_tokens/total_time:.2f} tokens/sec")
        
        # Best performance
        best = max(successful, key=lambda r: r["tokens_per_sec"])
        print(f"\n🏆 Best Performance:")
        print(f"   {best['tokens_per_sec']:.2f} tokens/sec")
    else:
        print("❌ No successful tests")
    
    failed = [r for r in results if not r.get("success", False)]
    if failed:
        print(f"\n⚠️  Failed tests: {len(failed)}")
        for r in failed:
            print(f"   - {r.get('error', 'Unknown error')}")
    
    print("\n✨ Test complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

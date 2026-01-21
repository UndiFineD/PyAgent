import time
import rust_core
import statistics
import logging

def run_performance_test(duration_secs=60):
    # 1. Setup Hardware and Model
    profile = rust_core.HardwareProfile(None)
    config = rust_core.TransformerConfig.auto_configure(profile)
    model = rust_core.NeuralTransformer(config)

    print("=" * 50)
    print("TRANSFORMER PERFORMANCE BENCHMARK")
    print("=" * 50)
    print(f"Hardware: {profile.cpu_cores} Cores, {profile.total_memory_gb:.1f}GB RAM")
    print(f"Model:    {model.get_summary()}")
    print(f"Config:   d_model={config.d_model}, d_ff={config.d_ff}, heads={config.n_heads}, layers={config.n_layers}")
    print("-" * 50)

    # 2. Prepare Sample Corpus
    sample_text = (
        "The quick brown fox jumps over the lazy dog. " * 10
    ) # ~90 tokens
    tokens_per_call = len(sample_text.split())

    # 3. Warmup
    print("Warming up...")
    for _ in range(5):
        model.vectorize(sample_text)

    # 4. Benchmarking Loop
    print(f"Running benchmark for {duration_secs} seconds...")
    start_all = time.time()
    total_tokens = 0
    iteration_times = []
    
    while (time.time() - start_all) < duration_secs:
        it_start = time.time()
        
        # We use vectorize to measure the end-to-end Rust implementation
        # including pooling and GQA attention
        model.vectorize(sample_text)
        
        it_end = time.time()
        iteration_times.append(it_end - it_start)
        total_tokens += tokens_per_call

    actual_duration = time.time() - start_all
    avg_latency = statistics.mean(iteration_times) * 1000 # ms
    tps = total_tokens / actual_duration

    print("-" * 50)
    print(f"Total Tokens:      {total_tokens}")
    print(f"Total Time:        {actual_duration:.2f}s")
    print(f"Avg Latency:       {avg_latency:.2f}ms per batch ({tokens_per_call} tokens)")
    print(f"Throughput (TPS):  {tps:.2f} tokens/second")
    print("=" * 50)

if __name__ == "__main__":
    # Run for 5 minutes as requested
    run_performance_test(300)

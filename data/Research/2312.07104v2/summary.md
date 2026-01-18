# SGLang: Efficient Execution of Structured Language Model Programs
**arXiv ID**: 2312.07104
**Date**: December 2023
**GitHub**: [sgl-project/sglang](https://github.com/sgl-project/sglang)

## Summary
SGLang is a domain-specific language and execution runtime for LLMs, primarily distinguished by its **RadixAttention** mechanism. It handles "automatic" KV cache reuse across many independent requests by treating the prompt prefix space as a Radix Tree. This is particularly transformative for agentic workflows where multiple agents share a large system prompt or the same few-shot examples.

## Key Innovations
1.  **RadixAttention**:
    -   Manages KV caches of prefixes (system prompts, history, code contexts) in a **Radix Tree** structure.
    -   When a new request arrives, the system matches the prompt against the tree. If a prefix exists, the system reuses the physical GPU memory blocks (via **PagedAttention**) rather than computing them from scratch.
    -   **Eviction Policy**: Recursive LRU (evicts leaf nodes first).
2.  **Compressed Finite State Machine (FSM) Decoding**: Accelerates constrained/structured output (JSON) by pre-compiling grammars into lookup tables.
3.  **Speculative Grammars**: Combines speculative decoding with grammatical constraints.

## Performance Benchmarks
- **Throughput**: **5.1x – 6.4x** improvement over vLLM in complex LLM programs (e.g., Tree-of-Thought).
- **Latency**: Significant reduction in Time-to-First-Token ($TTFT$) for requests with long cached prefixes.

## Implementation Details for PyAgent
- **Integration Point**: `src/infrastructure/engine/paged_attention/`
- **Key Logic**:
    - `RadixTreeManager`: Maintains the mapping between token sequences and physical block indices.
    - `PrefixMatcher`: Efficiently finds the longest shared prefix in the tree.
    - `BlockMigration`: Logic to move blocks between active and cached states.

## Mathematical Concepts
- **Automatic Prefix Caching**: $KV_{total} = KV_{new} + \text{Lookup}(RadixTree(tokens))$.

## References
- [arXiv:2312.07104](https://arxiv.org/abs/2312.07104)

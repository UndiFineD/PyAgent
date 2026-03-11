# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Memory Subsystem Design

The `memory` package in `src/memory` provides comprehensive memory management for agent knowledge, facts, conversation context, OpenAI LLM models (GGUF), agent state, and remote requests.

> **Core Design Principles**
>
> All memory functions are implemented in Rust for optimal performance, memory safety, and low-level control.
>
> The system uses a key-value (KV) store with dual indexing:
> - **BTree index** for ordered, range-based queries and fast lookups
> - **Graph index** for complex relationship queries and pattern matching
>
> **Lazy tracking** of accessed data enables intelligent swapping out to disk when memory pressure is detected, optimizing memory usage across all components.
>
> The memory subsystem is designed to be complete and self-sufficient, managing:
> - Agent knowledge and conversation context
> - OpenAI LLM models (GGUF format)
> - Agent state and internal data
> - Metadata and configuration
> - Remote requests and their payloads
>
> In the absence of a Rust-based memory manager, the subsystem gracefully degrades to a minimal state.

## Architectural Highlights

- **Rust-native implementation**: All memory functions are implemented in Rust for maximum performance, memory safety, and control
- **Dual indexing**: BTree for ordered lookups and range queries, Graph for complex relationship queries and pattern matching
- **Lazy access tracking**: Data access is tracked lazily to minimize overhead; accessed items are prioritized for retention, while less-used items are candidates for swapping out to disk
- **Memory pressure detection**: Intelligent monitoring of memory usage to detect when swapping out is needed
- **Swapping algorithms**: Dynamic swapping algorithms that balance memory usage with performance requirements
- **Query interface**: Comprehensive `store(content, metadata, tags)` and `query(query_text, n_results, filter_tags)` methods with support for complex filtering and pattern matching

## Design Considerations

1. **Performance optimization** – design for minimal latency and maximum throughput in all memory operations
2. **Memory safety** – Rust's ownership model ensures memory safety without a garbage collector
3. **Scalability** – design for horizontal scaling across fleet nodes with support for sharding
4. **Consistency** – eventual consistency is acceptable; conflict resolution strategy for concurrent writes
5. **Privacy** – ability to purge, encrypt, or anonymize sensitive entries
6. **Indexing strategies** – optimized indexing for both BTree and Graph indices based on workload characteristics
7. **Swapping policies** – dynamic policies that balance memory usage with performance requirements

## Potential Brainstorm Areas

- Advanced swapping algorithms with machine learning-based predictions
- Memory compression techniques for reducing footprint
- Hybrid memory tiers (fast-access RAM, swap disk, archived storage)
- Memory-aware scheduling for agent execution
- Offline/archived memory tier for very old entries
- Memory summarization and pruning policies (synaptic pruning idea)

# Memory Domain Structure

## Overview

The memory domain structure is designed to provide a comprehensive, high-performance memory management system for the PyAgent. The system is built around three core indexing structures: Key-Value (KV), Balanced B-Tree (BTree), and Graph.

## Key-Value (KV) Index

- **Purpose**: Provides fast, direct access to memory elements using a key-value pair
- **Structure**: Simple hash map implementation with O(1) average lookup time
- **Use Cases**: Direct access to specific memory elements, temporary storage, cache lookup
- **Constraints**: No ordered access, no range queries, limited to unique keys

## Balanced B-Tree (BTree) Index

- **Purpose**: Enables ordered access, range queries, and efficient lookups for sorted data
- **Structure**: Self-balancing B-Tree with height-balancing to maintain O(log n) lookup time
- **Use Cases**: Range queries, ordered access, sorted data retrieval, pagination
- **Constraints**: Slower than KV for direct lookups, requires more memory overhead

## Graph Index

- **Purpose**: Supports complex relationship queries and pattern matching across memory elements
- **Structure**: Directed graph with nodes representing memory elements and edges representing relationships
- **Use Cases**: Relationship queries, pattern matching, graph traversal, semantic similarity
- **Constraints**: Most computationally expensive, requires significant memory overhead, complex to implement

## Indexing Strategy

- **Hybrid approach**: Combine all three indices to leverage their strengths while minimizing weaknesses
- **Data placement**: Place frequently accessed data in KV index, sorted data in BTree index, relationship data in Graph index
- **Performance optimization**: Balance memory usage with performance requirements through intelligent data placement

## Implementation Notes

- All indexing structures will be implemented in Rust for optimal performance and memory safety
- The KV index will serve as the primary access point for direct memory lookups
- The BTree index will handle sorted data and range queries efficiently
- The Graph index will be used for complex relationship queries and pattern matching
- Memory pressure detection will monitor usage and trigger swapping when necessary

*Content reused from `src-old/classes/agent/LongTermMemory.py`.*
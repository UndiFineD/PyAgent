# Confucius Code Agent (CCA) & Hierarchical Scaffolding

**Date**: January 11, 2026
**Source**: Meta and Harvard Research
**Paper**: [Confucius Code Agent: A Software Engineering Agent that can Operate at Large-Scale Codebases](https://arxiv.org/abs/2512.10398)
**Writers**: Meta FAIR & Harvard SE Team

## Summary
The Confucius Code Agent (CCA) demonstrates that performance on real-world software tasks is driven more by **scaffolding and architecture** than by model size alone. It achieves state-of-the-art results (52.7 Resolve@1 on SWE-Bench Pro) using a combination of hierarchical memory and recursive build loops.

## Architectural Pillars
1. **Hierarchical Working Memory**: Distinguishes between immediate task context and long-term codebase knowledge.
2. **Persistent Note-Taking**: Agents maintain a "scratchpad" or "dev log" to track state across long-running tasks.
3. **Modular Tooling**: Specialized tools for AST analysis, grep, and build-environment interaction.
4. **Meta-Agent Loops**: A high-level agent drives the build-test-improve cycle, delegating specific sub-tasks to specialists.

## Implementation in PyAgent
As part of our **5-Tier Architecture** rollout:
- **Phase 130** implemented the hierarchical 5-tier structure aligning with the CCA modular approach.
- **B-Tree Sharding** provides the persistent knowledge storage required for large-scale operations.
- The **ReportGenerator** (Autodoc) serves as the persistent documentation engine for the meta-agent loop.

---
*Maintained as part of the PyAgent Key Research Library.*

# TALON: Confidence-Aware Speculative Decoding with Adaptive Token Trees
**arXiv ID**: 2601.07353
**Date**: January 12, 2026
**Authors**: Tianyu Liu, Qitan Lv, Yuhao Shen, Xiao Sun, Xiaoyan Sun

## Summary
TALON is a training-free, budget-driven adaptive tree expansion framework for speculative decoding. It addresses the limitation of fixed-width, fixed-depth draft trees (like those in EAGLE or Medusa) which fail to adapt to varying token difficulty and context uncertainty.

## Key Innovations
1.  **Adaptive Tree Structure**: Unlike static trees, TALON dynamically shapes the draft tree.
    -   **Deep-and-Narrow**: For deterministic contexts (high confidence).
    -   **Shallow-and-Wide**: For uncertain branches (low confidence).
2.  **Budget-Driven Expansion**: The framework constructs the tree iteratively until a fixed token budget is met.
3.  **Hybrid Expansion Strategy**: Uses an adaptive node budget allocation for each layer.
4.  **Training-Free**: Can be plugged into existing tree-based methods (EAGLE-3, etc.).

## Performance
-   Up to **5.16x end-to-end speedup** over auto-regressive decoding.
-   Outperforms state-of-the-art methods like EAGLE-3.

## Implementation Details for PyAgent
-   **Integration Point**: `src/infrastructure/speculative_v2/eagle/Tree.py`
-   **Mechanism**:
    -   Measure confidence (e.g., entropy or top-1 probability) of draft tokens.
    -   Calculate a "budget" per iteration.
    -   Iteratively expand nodes with the highest relative confidence.
    -   Terminate expansion when the budget is exhausted.

## References
-   [arXiv:2601.07353](https://arxiv.org/abs/2601.07353)

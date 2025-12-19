# Grokking

## Overview
**Grokking** is a strange phenomenon observed in training neural networks (specifically on algorithmic datasets like modular arithmetic), where the model achieves perfect training accuracy but poor test accuracy (overfitting) for a long time, and then suddenly—after many more epochs—the test accuracy jumps to 100%.

## The Phases
1.  **Memorization**: The model quickly learns to fit the training data perfectly. Training loss $\to$ 0. Test loss is high.
2.  **Plateau**: The model stays in this state for a very long time (e.g., $10^5$ steps). It seems like it has failed to generalize.
3.  **Grokking (Generalization)**: Suddenly, the test loss drops dramatically. The model has switched from "memorizing" the answers to "understanding" the underlying algorithm (e.g., learning the rule $a + b \pmod p$).

## Why?
The theory is that the "generalizing solution" (the algorithm) is more efficient (smaller weight norm) than the "memorizing solution", but it is harder to find.
*   Weight Decay plays a crucial role. It slowly pushes the model away from the complex memorization solution toward the simpler generalizing solution.

## Implications
*   **Patience**: Just because a model is overfitting doesn't mean it won't eventually generalize.
*   **Training Time**: We might be stopping training too early for some complex tasks.

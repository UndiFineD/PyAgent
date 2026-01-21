# Neurosymbolic AI

Deep Learning is great at perception (seeing, hearing) and pattern recognition, but struggles with explicit reasoning and logic. Symbolic AI (GOFAI) is great at reasoning and logic, but brittle and bad at perception.
**Neurosymbolic AI** aims to combine the best of both worlds: the learnability of neural networks with the reasoning power of symbolic logic.

## 1. The Two Systems (System 1 vs. System 2)

Inspired by Daniel Kahneman's "Thinking, Fast and Slow":
- **System 1 (Neural)**: Fast, intuitive, pattern-matching. (e.g., Recognizing a face).
- **System 2 (Symbolic)**: Slow, deliberative, logical. (e.g., Solving a math problem).

Neurosymbolic systems try to implement this duality.

## 2. Approaches

### A. Symbolic Neuro-Symbolic
The neural network acts as a perception module that feeds symbols into a symbolic reasoner.
- *Example*: A CNN looks at an image and outputs "Cat", "Mat". A logic engine then deduces "The cat is on the mat".
- *Pros*: Interpretable.
- *Cons*: The "Symbol Grounding Problem" (how to map continuous data to discrete symbols) is hard. Gradients can't flow through the discrete logic step easily.

### B. Logic Tensor Networks (LTN)
Logic is embedded directly into the loss function.
- Predicates (like `IsCat(x)`) are continuous functions $[0, 1]$.
- Logical operators ($\land, \lor, \neg$) are implemented using fuzzy logic (t-norms).
- **Training**: The network is trained to satisfy a knowledge base of logical rules (e.g., $\forall x: \text{Cat}(x) \implies \text{Animal}(x)$).

### C. DeepProbLog
Extends probabilistic logic programming (ProbLog) with neural predicates.
- You write a logic program: `addition(X, Y, Z) :- digit(Img1, X), digit(Img2, Y), Z is X + Y.`
- The `digit` predicate is a Neural Network (MNIST classifier).
- The system is trained end-to-end to maximize the probability of the correct sum.

## 3. Benefits

1.  **Data Efficiency**: You can learn from fewer examples if you have rules to guide you.
2.  **Interpretability**: You can inspect the logical rules the system is using.
3.  **Generalization**: Logic generalizes perfectly (2+2 is always 4), whereas neural nets might fail on out-of-distribution numbers.

## Summary

Neurosymbolic AI is a key candidate for the next wave of AI, potentially solving the reasoning deficits of current LLMs.

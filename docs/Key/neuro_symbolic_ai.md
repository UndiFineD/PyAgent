# Neuro-Symbolic AI

Neuro-Symbolic AI aims to bridge the gap between the two main paradigms of Artificial Intelligence: **Connectionism** (Neural Networks) and **Symbolism** (Logic/Rules).

## 1. The Two Systems

- **System 1 (Neural)**: Fast, intuitive, pattern-matching. Good at perception (vision, audio) and handling noisy data.
    - *Weakness*: Opaque, struggles with strict logic, data-hungry.
- **System 2 (Symbolic)**: Slow, deliberative, logical. Good at reasoning, planning, and following strict rules.
    - *Weakness*: Brittle, cannot handle raw sensory data, requires manual rule engineering.

## 2. Key Architectures

### Logic Tensor Networks (LTN)
- **Concept**: Embeds logical formulas into a neural network's loss function.
- **Mechanism**:
    - Predicates (e.g., `IsCat(x)`) are learned as neural networks.
    - Logical rules (e.g., `IsCat(x) -> IsAnimal(x)`) are converted into differentiable constraints (using fuzzy logic).
    - If the network predicts `IsCat(x)=0.9` and `IsAnimal(x)=0.1`, the loss is high because it violates the rule.

### DeepProbLog
- **Concept**: Extends the probabilistic logic programming language ProbLog with neural predicates.
- **Mechanism**:
    - You write a logic program: `addition(X, Y, Z) :- digit(Image1, X), digit(Image2, Y), Z is X + Y.`
    - The `digit` predicate is a Neural Network (CNN) that classifies MNIST images.
    - The system backpropagates the error from the logical result (Z) through the logic program to update the CNN weights.

### Neural Theorem Provers
- **Concept**: Using Transformers to guide symbolic theorem provers (like Lean or Coq).
- **Mechanism**: The LLM suggests the next step in a proof, and the symbolic engine verifies if it's valid. This combines the intuition of the LLM with the rigor of the solver.

## 3. Why it Matters

- **Data Efficiency**: If you tell the model "All men are mortal," it doesn't need to see 1,000 examples of men dying to learn that pattern.
- **Interpretability**: The reasoning process follows explicit logical rules, making it easier to audit.
- **Robustness**: Logical constraints prevent the model from making "impossible" errors (e.g., detecting a car floating in the sky if gravity is a constraint).

## Summary

Neuro-Symbolic AI represents the "Third Wave" of AI, aiming to create systems that can both *learn* from experience and *reason* about what they have learned.

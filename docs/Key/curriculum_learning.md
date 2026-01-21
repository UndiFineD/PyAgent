# Curriculum Learning

A training strategy inspired by how humans learn: start with easy concepts and gradually introduce harder ones.

## 1. The Concept

*   **Standard Training**: Randomly sampling data batches. The model might see a complex calculus problem before it learns addition.
*   **Curriculum Training**: Sorting the dataset by "difficulty" and presenting the easy examples first.
*   **Benefit**: Faster convergence and often better generalization.

## 2. Measuring Difficulty

How do we know which examples are "hard"?
*   **Heuristics**: Sentence length (NLP), Image resolution/noise (Vision).
*   **Teacher Model**: Use a pre-trained model to score the difficulty (e.g., examples with high loss are "hard").
*   **Self-Paced Learning**: The model itself selects examples where it is confident (low loss) and gradually accepts examples with higher loss.

## 3. Applications

*   **LLM Pre-training**: Start with high-quality, simple textbooks (Wikipedia) before moving to noisy internet text (Common Crawl).
*   **Robotics**: Learn to walk on a flat surface before trying to walk on stairs.

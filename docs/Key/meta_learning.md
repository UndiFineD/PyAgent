# Meta-Learning

Standard Deep Learning requires thousands of examples to learn a task (e.g., recognizing cats). Humans can learn from just one example. **Meta-Learning** (Learning to Learn) aims to bridge this gap by training models that can adapt to new tasks rapidly.

## 1. The Problem: Few-Shot Learning

*   **Training**: The model sees many different *tasks* (e.g., Task A: Classify Birds vs. Dogs; Task B: Classify Cars vs. Bikes).
*   **Testing**: The model is given a *new* task (Task C: Classify Apples vs. Oranges) and only 1-5 examples per class. It must learn to classify them instantly.

## 2. MAML (Model-Agnostic Meta-Learning)

The most famous algorithm.
*   **Goal**: Find a set of initial weights $\theta$ that are "easy to fine-tune."
*   **Inner Loop**: For a specific task, take one gradient step from $\theta$ to get $\theta'$.
*   **Outer Loop**: Update the original $\theta$ such that the *loss after the inner loop step* is minimized.
*   **Intuition**: It's like training a runner not to run a specific race, but to have a body type that can quickly adapt to *any* sport.

## 3. Metric-Based Approaches (Prototypical Networks)

Instead of updating weights, learn a metric space.
*   **Embedding**: Map images to vectors.
*   **Prototype**: Calculate the mean vector (centroid) for "Apple" and "Orange" based on the few examples.
*   **Classification**: For a new image, check if its vector is closer to the Apple-centroid or Orange-centroid.

## 4. Memory-Augmented Neural Networks (MANNs)

Using an external memory bank (like a Neural Turing Machine) to store information about the new task. The network learns how to read/write to this memory to solve the task, effectively "caching" the new class definitions.

## 5. In-Context Learning (GPT-3)

LLMs exhibit "emergent" meta-learning. By providing examples in the prompt (Few-Shot Prompting), the model "learns" the task without any weight updates. This is a form of meta-learning where the "inner loop" happens entirely within the forward pass of the attention mechanism.

# Hyperdimensional Computing (HDC)

Hyperdimensional Computing (also known as **Vector Symbolic Architectures** or VSA) is a radical departure from standard Deep Learning. Instead of optimizing weights via backpropagation, it computes with massive, random, high-dimensional vectors using algebra.

## 1. The Representation: Hypervectors

- **Dimensionality**: Vectors are extremely large (e.g., $D=10,000$).
- **Randomness**: They are initialized randomly. In such high dimensions, any two random vectors are **orthogonal** (uncorrelated) with high probability.
- **Holographic**: Information is distributed across the entire vector. You can corrupt 30% of the bits and still recover the information.

## 2. The Algebra of Thought

HDC defines three core operations to manipulate concepts:

1.  **Bundling (Addition)**: Superposition of concepts.
    - $V_{fruit} = V_{apple} + V_{banana}$
    - The result is similar to both inputs. "It's a fruit, like an apple or a banana."
2.  **Binding (Multiplication/XOR)**: Associating concepts (Key-Value pairs).
    - $V_{red\_apple} = V_{color} \otimes V_{red} + V_{shape} \otimes V_{round}$
    - The result is orthogonal to the inputs. You can't confuse "Red" with "Red Apple."
3.  **Permutation (Shifting)**: Encoding sequences or order.
    - $V_{sequence} = \Pi(V_A) + \Pi(\Pi(V_B)) + \dots$

## 3. Learning without Backprop

Learning in HDC is often "One-Shot."
- To learn the class "Cat," you simply sum up all the hypervectors of cat images you've seen.
- $V_{Cat\_Class} = V_{img1} + V_{img2} + V_{img3} \dots$
- Inference is just finding the closest class vector (Cosine Similarity).

## 4. Advantages

- **Extreme Efficiency**: Operations are simple bitwise arithmetic (XOR, Shift, Add). Can run on FPGAs or extremely low-power hardware.
- **Transparency**: You can mathematically decompose a vector to see what concepts it contains (unlike a black-box neural embedding).
- **Robustness**: Highly resistant to noise and hardware failure.

## Summary

HDC mimics the brain's ability to process information in a distributed, robust way, offering a powerful alternative for **Edge AI** and symbolic reasoning tasks where deep learning is too heavy or opaque.

# Latent Representations & Vector Space

**Latent Representations** (or Embeddings) are the fundamental way modern AI systems "understand" the world. They translate discrete, human concepts (words, pixels, sounds) into continuous mathematical vectors.

## 1. What is a Latent Space?

Imagine a 2D graph. You can plot points like (2,3) or (-1,5). Now imagine a graph with 4,096 dimensions. This is the **Latent Space** of a model like Llama 3.

*   Every concept the model knows is a point in this space.
*   **Distance = Meaning**: If two points are close together in this space, their meanings are similar. "Cat" and "Kitten" are neighbors. "Cat" and "Carburetor" are far apart.

## 2. The Manifold Hypothesis

Real-world data (like images of faces) is high-dimensional (1024x1024 pixels = 1 million dimensions). However, the set of *valid* faces occupies a much smaller, lower-dimensional subspace called a **Manifold**.

*   **Compression**: Deep learning models learn to map the high-dimensional input onto this lower-dimensional latent manifold.
*   **Interpolation**: Because the manifold is continuous, we can move smoothly between points. This is why we can morph a face into another face in a GAN or Diffusion model.

## 3. Vector Arithmetic

One of the most famous properties of latent representations is that they support semantic arithmetic.

$$ \text{Vector("King")} - \text{Vector("Man")} + \text{Vector("Woman")} \approx \text{Vector("Queen")} $$

This suggests the model has learned "Gender" as a specific direction (vector) in the latent space. Moving along that vector changes the gender of the concept while preserving other attributes (royalty).

## 4. Types of Latent Representations

### A. Word Embeddings (Static)
*   **Word2Vec / GloVe**: Each word has one fixed vector. "Bank" (river) and "Bank" (money) share the same vector.

### B. Contextual Embeddings (Dynamic)
*   **Transformers (BERT/GPT)**: The vector for "Bank" changes depending on the surrounding words.
    *   "I sat by the bank" $\rightarrow$ Vector A (Nature context)
    *   "I went to the bank" $\rightarrow$ Vector B (Financial context)

### C. Multimodal Embeddings
*   **CLIP / SigLIP**: Maps images and text to the *same* latent space. The vector for a photo of a dog is mathematically close to the vector for the text "A photo of a dog".

## 5. Summary

Latent Representations are the "brain tissue" of AI. They allow models to reason by manipulating geometry. Understanding latent space is key to techniques like RAG (Semantic Search), Clustering, and Anomaly Detection.

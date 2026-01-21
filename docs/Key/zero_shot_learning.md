# Zero-Shot Learning (ZSL)

Standard Supervised Learning can only recognize classes it has seen during training. If you train on Cats and Dogs, it cannot recognize a Zebra.
**Zero-Shot Learning** aims to recognize unseen classes by leveraging **semantic attributes** or descriptions.

## 1. Semantic Embeddings

Instead of mapping an image directly to a class ID (0, 1, 2), we map it to a semantic vector space.
- **Attributes**: We define a Zebra as `[Striped, Horse-like, Black-and-White]`.
- **Word Vectors**: We use word embeddings (Word2Vec, GloVe) for the class names. `Vector("Zebra")` is close to `Vector("Horse") + Vector("Stripes")`.

## 2. The Process

1.  **Train**: Train the model to map images of seen classes (Horses, Tigers) to their semantic vectors.
2.  **Inference**:
    - Show an image of a Zebra (unseen).
    - The model predicts a vector $v$.
    - We look up the nearest class name in the semantic space (even though we never trained on "Zebra" images).

## 3. CLIP (Contrastive Language-Image Pre-training)

CLIP (OpenAI) is the modern state-of-the-art for ZSL.
- It learns a joint embedding space for Images and Text.
- To classify an image, we compare it to the text embeddings of "A photo of a dog", "A photo of a cat", "A photo of a zebra".
- The model picks the text description that matches best.
- This works for *any* concept that can be described in words.

## Summary

Zero-Shot Learning breaks the "closed-world assumption" of standard classification, allowing models to handle the open-ended nature of the real world.

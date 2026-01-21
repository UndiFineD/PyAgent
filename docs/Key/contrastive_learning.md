# Contrastive Learning

Contrastive Learning is the dominant technique in **Self-Supervised Learning**. Instead of requiring human labels ("This is a cat"), the model learns by comparing data points: "This image is similar to that one, but different from this one."

## 1. The Intuition

If you see a photo of a dog from the front and a photo of the same dog from the side, you know they are the same object.
Contrastive Learning forces the neural network to output similar vector embeddings for these two views (Positive Pair) and different embeddings for a photo of a chair (Negative Pair).

## 2. SimCLR (Simple Framework for Contrastive Learning)

A famous algorithm by Google.
1.  **Augmentation**: Take an image $x$. Create two versions: $x_i$ (cropped) and $x_j$ (color distorted).
2.  **Encoder**: Pass both through a ResNet to get vectors $h_i, h_j$.
3.  **Projection**: Map them to a lower dimension $z_i, z_j$.
4.  **Loss Function (InfoNCE)**: Pull $z_i$ and $z_j$ close together (Numerator). Push $z_i$ away from *all other images* in the batch (Denominator).

## 3. CLIP (Contrastive Language-Image Pre-training)

(See [Multimodal-Models.md](Multimodal-Models.md)). CLIP uses contrastive learning between *modalities*.
*   Positive Pair: (Image of Dog, Text "A photo of a dog").
*   Negative Pair: (Image of Dog, Text "A photo of a banana").

## 4. Hard Negative Mining

The model learns best from "Hard Negatives"—examples that are different but look similar.
*   *Easy Negative*: Dog vs. Airplane. (Model learns easily).
*   *Hard Negative*: Wolf vs. Husky. (Model is forced to learn subtle features like ear shape).
*   Retrieval systems (RAG) rely heavily on training with hard negatives to distinguish relevant documents from irrelevant but keyword-heavy documents.

## 5. Collapse

A common failure mode where the model outputs the *exact same vector* for every single input. This minimizes the distance between positive pairs (0) but fails to distinguish anything. Techniques like **MoCo (Momentum Contrast)** and **BYOL (Bootstrap Your Own Latent)** are designed to prevent this.

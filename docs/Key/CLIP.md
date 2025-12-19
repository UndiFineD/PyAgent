# CLIP (Contrastive Language-Image Pre-training)

## Overview
**CLIP**, introduced by OpenAI in 2021, is a multimodal model that learns to associate images with text. Unlike traditional classifiers trained on fixed labels (e.g., "cat", "dog"), CLIP is trained on 400 million (image, text) pairs collected from the internet.

## How it Works: Contrastive Learning
CLIP trains two encoders simultaneously:
1.  **Image Encoder**: (ResNet or ViT) converts an image into a vector.
2.  **Text Encoder**: (Transformer) converts a text caption into a vector.

The goal is to maximize the cosine similarity between the image embedding and its correct text embedding, while minimizing the similarity with all other text embeddings in the batch.
*   **Positive Pair**: (Image of a dog, "A photo of a dog") -> Pull vectors together.
*   **Negative Pair**: (Image of a dog, "A photo of a banana") -> Push vectors apart.

## Zero-Shot Classification
CLIP's superpower is **Zero-Shot Classification**.
To classify an image:
1.  Create a list of possible labels (e.g., "dog", "cat", "car").
2.  Wrap them in a prompt: "A photo of a {label}".
3.  Encode the image and all the prompt texts.
4.  The label with the highest similarity score is the prediction.

This allows CLIP to classify objects it has never explicitly seen during training, as long as it understands the language describing them.

## Impact
*   **DALL-E / Stable Diffusion**: CLIP is the "eye" that guides these generators. It measures how well the generated image matches the text prompt.
*   **Multimodal Search**: Enabling search of image databases using natural language queries.

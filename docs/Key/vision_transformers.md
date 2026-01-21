# Vision Transformers (ViT)

## Overview
**Vision Transformer (ViT)**, introduced by Google Research in 2020 ("An Image is Worth 16x16 Words"), demonstrated that pure Transformer architectures could perform as well as or better than Convolutional Neural Networks (CNNs) for image classification.

## The Concept: Images as Sequences
Transformers were designed for sequences (text). To apply them to 2D images, ViT treats an image as a sequence of patches.

1.  **Patching**: Split the image into fixed-size patches (e.g., 16x16 pixels).
2.  **Linear Projection**: Flatten each patch and map it to a vector (embedding) using a linear layer.
3.  **Position Embeddings**: Add learnable position embeddings to retain spatial information (since Transformers are permutation-invariant).
4.  **Transformer Encoder**: Feed the sequence of patch embeddings into a standard Transformer Encoder (Self-Attention + MLP).
5.  **Classification Head**: Use the output of a special `[CLS]` token (similar to BERT) to predict the class.

## ViT vs. CNN
*   **Inductive Bias**: CNNs have strong inductive biases (translation invariance, locality) built-in. ViT has much less inductive bias.
*   **Data Hunger**: Because it lacks these biases, ViT requires *more data* to train effectively. On mid-sized datasets (ImageNet-1k), ResNet outperforms ViT. On massive datasets (JFT-300M), ViT outperforms ResNet.
*   **Global Receptive Field**: CNNs only see local neighbors in early layers. ViT's self-attention allows every pixel (patch) to attend to every other pixel from the very first layer.

## Impact
ViT marked the beginning of the "Transformer takeover" in Computer Vision. It led to hybrid architectures (Swin Transformer) and multimodal models (CLIP, LLaVA) where text and images share the same architectural principles.

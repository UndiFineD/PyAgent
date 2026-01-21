# Diffusion Transformers (DiT)

Diffusion Transformers (DiT) represent the convergence of the two most powerful architectures in modern AI: **Diffusion Models** (for generation) and **Transformers** (for scaling). They are the backbone of OpenAI's **Sora** and Stability AI's **Stable Diffusion 3**.

## 1. The Shift: U-Net to Transformer

### Traditional Diffusion (Stable Diffusion 1.5 / 2.0)
- **Backbone**: A **U-Net** (CNN-based).
- **Mechanism**: Downsamples the image to a latent space, processes it with convolutions, and upsamples it back.
- **Limitation**: CNNs struggle with global context and don't scale as predictably as Transformers.

### Diffusion Transformer (DiT)
- **Backbone**: A standard **Vision Transformer (ViT)**.
- **Mechanism**:
    1.  **Patchify**: The latent image is chopped into patches (tokens).
    2.  **Process**: These tokens are fed into a Transformer encoder (just like GPT-4 processes text tokens).
    3.  **Depatchify**: The output tokens are rearranged back into an image.

## 2. Why DiT?

### Scalability
Transformers have a proven "Scaling Law": simply adding more layers and compute reliably improves performance. U-Nets saturate earlier. DiT allows image generation models to scale to billions of parameters.

### Flexibility
- **Variable Resolution**: Transformers can handle different aspect ratios and resolutions more naturally than fixed-size CNNs.
- **Multi-Modal**: It's easier to integrate text, audio, and video into a single Transformer architecture.

## 3. Architecture Details

- **Conditioning**: Text prompts (or time steps) are injected into the Transformer via **Adaptive Layer Norm (adaLN)** or Cross-Attention.
- **Positional Embeddings**: Since Transformers have no inherent sense of space (unlike CNNs), 2D (or 3D for video) positional embeddings are crucial.

## 4. Impact: Sora

OpenAI's Sora is essentially a DiT applied to **Spacetime Patches**.
- It treats video as a 3D volume of tokens ($Height \times Width \times Time$).
- By training a massive DiT on these tokens, it learns the physics of the world (how objects move, light reflects, etc.) as a side effect of learning to predict the next "video token."

## Summary

DiT proves that the Transformer architecture is truly universal. By replacing the specialized U-Net with the general-purpose Transformer, we unlock the same massive scaling capabilities for images and video that we saw in text.

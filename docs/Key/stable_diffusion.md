# Stable Diffusion

## Overview
**Stable Diffusion** is a text-to-image model released by Stability AI in 2022. It is based on the **Latent Diffusion Model (LDM)** architecture (Rombach et al.). Unlike DALL-E 2 or Imagen, which were closed-source, Stable Diffusion was released openly, sparking a massive community explosion.

## How it Works: Latent Diffusion
Standard diffusion models operate directly on pixels (e.g., 512x512 images). This is computationally expensive.
Stable Diffusion operates in a compressed **Latent Space**.

1.  **Perceptual Compression (VAE)**: An Autoencoder compresses the image into a smaller latent representation (e.g., 64x64 vectors).
2.  **Diffusion Process**: The diffusion (adding/removing noise) happens in this small latent space. This makes it fast enough to run on consumer GPUs (e.g., 8GB VRAM).
3.  **Conditioning (CLIP)**: A text prompt is encoded by CLIP's text encoder. These embeddings are injected into the U-Net via **Cross-Attention** layers, guiding the denoising process to match the text.
4.  **Decoding**: The final denoised latent is passed through the VAE Decoder to reconstruct the high-resolution image.

## Key Components
*   **U-Net**: The noise predictor.
*   **VAE**: The compressor/decompressor.
*   **CLIP Text Encoder**: The prompt understander.

## Impact
Stable Diffusion became the foundation for the open-source generative art movement, enabling fine-tuning (Dreambooth, LoRA) and control (ControlNet) on personal computers.

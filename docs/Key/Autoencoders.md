# Autoencoders

## What is an Autoencoder?
An Autoencoder is a type of unsupervised neural network used to learn efficient codings (representations) of unlabeled data. The network is trained to copy its input to its output.

## Architecture
It consists of two parts shaped like an hourglass:
1.  **Encoder**: Compresses the input $x$ into a lower-dimensional latent space representation $z$ (the bottleneck).
2.  **Decoder**: Reconstructs the input $\hat{x}$ from the latent representation $z$.

The goal is to minimize the **Reconstruction Loss** ($|x - \hat{x}|^2$). By forcing the data through a bottleneck, the model is forced to learn the most important features (latent variables) and ignore the noise.

## Types

### 1. Denoising Autoencoder
*   **Training**: Add noise to the input image (e.g., grain, blur) but ask the model to reconstruct the *clean* original image.
*   **Use Case**: Removing noise from old photos or audio.

### 2. Variational Autoencoder (VAE)
*   Instead of mapping the input to a fixed vector, a VAE maps it to a **probability distribution** (mean and variance) in the latent space.
*   **Generative**: By sampling from this distribution, VAEs can generate *new* data samples similar to the training data.
*   **Precursor to Diffusion**: VAEs are a key component of modern Stable Diffusion models (which operate in the "Latent" space compressed by a VAE).

### 3. Sparse Autoencoder (SAE)
*   Used in **Mechanistic Interpretability**. It expands the latent space (making it larger than the input) but forces most neurons to be zero (sparse). This helps disentangle "polysemantic" neurons into understandable features.

## Applications
*   **Dimensionality Reduction**: Similar to PCA but non-linear.
*   **Anomaly Detection**: If an autoencoder trained on "normal" data fails to reconstruct a new sample (high error), that sample is likely an anomaly.
*   **Image Compression**: Learning better compression formats than JPEG.

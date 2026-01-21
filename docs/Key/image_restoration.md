# Image Restoration

## Overview
**Image Restoration** is the task of recovering a high-quality image from a degraded version (noisy, blurry, low-resolution, or damaged).

## Super-Resolution (SR)
*   **Goal**: Upscale a low-resolution image to high-resolution (e.g., 4x zoom) while hallucinating realistic details.
*   **SRCNN**: The first deep learning approach.
*   **SRGAN / ESRGAN**: Uses Generative Adversarial Networks. The Generator tries to create a high-res image, and the Discriminator tries to distinguish it from a real high-res photo. This produces sharper textures than simple MSE loss (which leads to blurriness).

## Denoising
*   **Goal**: Remove noise (grain) from an image (e.g., low-light photography).
*   **DnCNN**: A CNN that learns to predict the *noise* (residual) rather than the clean image.
*   **Noise2Noise**: A technique to train denoisers *without* clean ground truth data, by training on pairs of noisy images of the same scene.

## Inpainting
*   **Goal**: Fill in missing or damaged parts of an image.
*   **Context Encoders**: The network looks at the surrounding pixels to predict the missing center.
*   **Diffusion Inpainting**: Modern approaches (like Stable Diffusion Inpainting) use text-guided diffusion to fill the hole with semantically meaningful content (e.g., "replace the dog with a cat").

## Colorization
*   **Goal**: Convert a grayscale image to color.
*   **Mechanism**: The network predicts the `a` and `b` channels (color) of the Lab color space, given the `L` channel (lightness).

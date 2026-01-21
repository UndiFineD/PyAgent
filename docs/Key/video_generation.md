# Video Generation

Video is just a sequence of images, but generating it is exponentially harder due to **Temporal Consistency**. If the background changes randomly between frames, the video flickers and looks fake.

## 1. 3D Convolutions vs. Transformers

*   **3D CNNs**: Treat video as a volume (Height x Width x Time). Good for short clips, but hard to scale.
*   **Video Transformers**: Treat video as a sequence of "Spacetime Patches."
    *   Image Patch: (16x16 pixels).
    *   Spacetime Patch: (16x16 pixels x 2 frames).

## 2. Diffusion for Video

*   **Frame-by-Frame**: Generate Image 1, then generate Image 2 conditioned on Image 1. Prone to drift.
*   **Latent Video Diffusion**: Compress the entire video into a latent block and denoise it all at once.
*   **DiT (Diffusion Transformers)**: Replacing the U-Net (standard in Stable Diffusion) with a Transformer backbone. This scales better and is the architecture behind **Sora**.

## 3. Sora (OpenAI)

*   **Spacetime Patches**: Compresses video into a massive sequence of tokens.
*   **Scalability**: Showed that video generation follows scaling laws (more compute = better physics simulation).
*   **Emergent Physics**: Without being explicitly programmed, it learned 3D consistency, object permanence, and reflections.

## 4. Challenges

*   **Compute**: Generating 1 minute of video takes orders of magnitude more compute than 1 image.
*   **Control**: "Make the character walk left" is harder to specify than "A photo of a cat."

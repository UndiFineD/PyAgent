# Generative Adversarial Networks (GANs)

Before Diffusion Models took over, **GANs** were the kings of generative AI. Introduced by Ian Goodfellow in 2014, they use a game-theoretic approach to generate data.

## 1. The Architecture

A GAN consists of two neural networks fighting a zero-sum game:

1.  **The Generator ($G$)**:
    *   Input: Random noise ($z$).
    *   Output: A fake image ($x_{fake}$).
    *   Goal: Fool the Discriminator into thinking the image is real.

2.  **The Discriminator ($D$)**:
    *   Input: An image (either real from the dataset or fake from $G$).
    *   Output: Probability that the image is real ($0$ to $1$).
    *   Goal: Correctly classify real images as Real and fake images as Fake.

## 2. The Training Process (Minimax Game)

*   **Step 1**: Train $D$ to distinguish real vs. fake.
*   **Step 2**: Train $G$ to maximize the error of $D$.
*   **Equilibrium**: Ideally, the Generator becomes so good that the Discriminator cannot tell the difference (Probability = 0.5).

## 3. Challenges

*   **Mode Collapse**: The Generator finds *one* image that fools the Discriminator and produces it over and over again (e.g., generating only "Golden Retrievers" and ignoring all other dog breeds).
*   **Vanishing Gradients**: If the Discriminator is too perfect, the Generator gets no feedback (gradients are zero) and stops learning.
*   **Training Instability**: Balancing the two networks is notoriously difficult.

## 4. Legacy & Modern Usage

While Diffusion Models (Stable Diffusion) are now preferred for image generation due to stability and diversity, GANs are still used for:
*   **Super Resolution**: Upscaling images (e.g., ESRGAN).
*   **Style Transfer**: Changing the style of an image (e.g., CycleGAN).
*   **Real-Time Generation**: GANs generate an image in a single forward pass (milliseconds), whereas Diffusion requires many steps (seconds).

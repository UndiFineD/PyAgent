# ControlNet

## Overview
**ControlNet** is a neural network structure introduced by Zhang et al. (2023) to add spatial conditioning to pre-trained text-to-image diffusion models (like Stable Diffusion).

## The Problem
Standard diffusion models are controlled by text prompts. However, text is often insufficient to describe precise spatial layouts (e.g., "a person standing in *this exact pose*").

## The Solution: Zero Convolutions
ControlNet creates a trainable copy of the encoding layers of the diffusion model (the U-Net encoder).
1.  **Locked Copy**: The original weights of the Stable Diffusion model are locked (frozen) to preserve its generative knowledge.
2.  **Trainable Copy**: A copy of the encoder weights is created and trained on the new condition (e.g., edge maps, depth maps).
3.  **Zero Convolutions**: The two branches are connected by "zero convolution" layers (1x1 convolutions initialized with zeros).
    *   Initially, the output of the ControlNet branch is zero, so the model behaves exactly like the original Stable Diffusion.
    *   As training progresses, the ControlNet learns to inject the control signal into the main model.

## Applications
ControlNet allows for precise control over generation using various inputs:
*   **Canny Edge**: Generate an image that follows the edges of a sketch.
*   **OpenPose**: Generate a character matching a specific skeleton pose.
*   **Depth Map**: Generate an image that respects the 3D depth of a scene.
*   **Scribble**: Turn a rough doodle into a high-quality artwork.

## Impact
ControlNet turned generative AI from a "slot machine" (random outputs) into a controllable tool for professional workflows in design, animation, and architecture.

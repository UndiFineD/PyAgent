# Multimodal Models

"Multimodal" means a model that can process and understand multiple types of data simultaneously—usually Text and Images, but also Audio, Video, and 3D.

## 1. Vision Transformers (ViT)

How do we feed an image into a Transformer (which expects a sequence of tokens)?
*   **Patching**: Cut the image into small squares (e.g., 16x16 pixels).
*   **Flattening**: Flatten each square into a vector.
*   **Projection**: Linearly project these vectors into embeddings.
*   **Result**: The image is now a sequence of "visual tokens" that can be processed just like text.

## 2. CLIP (Contrastive Language-Image Pre-training)

The bridge between Text and Images.
*   **Training**: Trained on 400M (Image, Caption) pairs from the internet.
*   **Objective**: Maximize the cosine similarity between the image embedding and the correct text embedding, while minimizing it for incorrect texts.
*   **Outcome**: A shared "Latent Space" where the vector for a picture of a dog is close to the vector for the word "dog".
*   **Usage**: Zero-shot image classification, and as the "eyes" for generative models like Stable Diffusion.

## 3. LLaVA (Large Language-and-Vision Assistant)

How to make a Chatbot see?
1.  **Vision Encoder**: Use a pre-trained CLIP or ViT to encode the image into visual tokens.
2.  **Projection Layer**: A simple linear layer (MLP) that translates "visual tokens" into the same dimension as the LLM's "text tokens."
3.  **LLM**: Feed the visual tokens + text tokens into a standard LLM (like Llama).
4.  **Result**: The LLM "sees" the image as if it were a foreign language it has learned to understand.

## 4. Audio & Video

*   **Whisper**: An Encoder-Decoder Transformer trained on 680k hours of audio for speech-to-text. It treats audio spectrograms like images (using Conv1D/ViT approaches).
*   **Sora / Video Gen**: Treating video as a 3D volume of patches (Space x Time).

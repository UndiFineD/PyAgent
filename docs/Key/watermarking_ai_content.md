# Watermarking AI Content

As AI-generated content becomes indistinguishable from human-created content, the need to detect and label it becomes critical for trust, copyright, and preventing misinformation.

## Text Watermarking

### 1. The "Green List" Method
*   **Mechanism**: During token generation, the vocabulary is split into a "Green List" and a "Red List" based on the hash of the previous token.
*   **Constraint**: The model is forced (or strongly encouraged via logits) to pick tokens only from the Green List.
*   **Detection**: To check if a text is AI-generated, you re-compute the Green/Red lists for each token. If a statistically improbable number of tokens are in the Green List, it's watermarked.
*   **Robustness**: Weak. Can be removed by paraphrasing or changing a few words.

## Image Watermarking

### 1. Invisible Noise (SynthID)
*   **Mechanism**: Google DeepMind's SynthID adds an imperceptible digital watermark directly into the pixels of the image.
*   **Robustness**: Designed to survive compression, cropping, and color filters.

### 2. Metadata (C2PA / Content Credentials)
*   **Mechanism**: An open technical standard (Coalition for Content Provenance and Authenticity) that uses cryptography to sign the metadata of a file.
*   **Function**: It records the "provenance" of the asset: who created it, what tools were used (e.g., Photoshop, DALL-E 3), and when.
*   **Adoption**: Supported by Adobe, Microsoft, Google, and camera manufacturers like Leica and Sony.
*   **Limitation**: Metadata can be stripped if the file is screenshotted or converted to a format that doesn't support it.

## Audio Watermarking
*   **Mechanism**: Embedding an inaudible signal (spread spectrum) into the audio waveform.
*   **Use Case**: Detecting AI-generated music or voice clones (Deepfakes).

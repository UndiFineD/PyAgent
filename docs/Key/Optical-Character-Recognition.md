# Optical Character Recognition (OCR)

## Overview
**OCR** is the conversion of images of typed, handwritten, or printed text into machine-encoded text.

## Traditional Approaches (Tesseract)
*   **Tesseract**: The most famous open-source OCR engine (originally HP, now Google).
*   **Pipeline**:
    1.  **Preprocessing**: Binarization, noise removal, rotation correction.
    2.  **Layout Analysis**: Finding text blocks, lines, and words.
    3.  **Character Recognition**: Originally used pattern matching; modern versions (Tesseract 4.0+) use LSTMs.

## Deep Learning Approaches

### CRNN (Convolutional Recurrent Neural Network)
*   **Architecture**:
    1.  **CNN**: Extracts features from the input image (treating text as a texture).
    2.  **RNN (Bi-LSTM)**: Processes the feature sequence to predict character probabilities for each frame.
    3.  **CTC (Connectionist Temporal Classification)**: A loss function that aligns the predicted sequence with the target text without needing explicit character-level bounding boxes.

### TrOCR (Transformer OCR)
*   **Concept**: Introduced by Microsoft, it treats OCR as an image-to-text generation problem using Transformers.
*   **Architecture**:
    *   **Encoder**: Vision Transformer (ViT) or DEIT processes the image patches.
    *   **Decoder**: Text Transformer (like GPT/BERT) generates the text tokens autoregressively.
*   **Benefit**: Outperforms CRNNs on irregular text (curved, handwritten) because it learns global context via attention.

## Challenges
*   **Scene Text**: Text in the wild (street signs, billboards) is much harder than scanned documents due to lighting, perspective, and occlusion.
*   **Handwriting**: High variability in styles makes handwritten text recognition (HTR) a distinct subfield.
